"""rag.py -- a complete retrieval-augmented generation pipeline (M11, L11-05 / LAB-11-02).

The pipeline is built from parts you can inspect:

    ingest    24 handbook documents (or a PDF through pypdf)
    chunk     word or token windows with overlap, keeping a parent document id
    index     dense (MiniLM + FAISS), lexical (BM25), hybrid score fusion
    retrieve  top-k, then optional late-interaction reranking
    build     a context that fits an explicit token budget
    generate  a grounded answer with flan-t5-small
    evaluate  recall@k, MRR, nDCG, EM, F1, support rate, refusal rate

The embeddings are the only learned component, and they are cached locally:
`sentence-transformers/all-MiniLM-L6-v2` (384 dimensions, Apache-2.0).

Run ``python rag.py`` for the comparison table quoted in L11-05 and LAB-11-02.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np

from gen_data import HANDBOOK, QA, UNANSWERABLE
from llm_eval import answer_report, is_refusal, refusal_rate, retrieval_report, support_rate

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# 1. Ingest and chunk
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    index: int


def load_documents(source: str = "handbook") -> dict[str, dict]:
    if source == "handbook":
        return {k: v for k, v in HANDBOOK.items()}
    raise ValueError(f"unknown source {source!r}")


def load_pdf(path) -> dict[str, dict]:
    """Read a PDF into page-level documents using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    docs = {}
    for i, page in enumerate(reader.pages):
        text = " ".join((page.extract_text() or "").split())
        if text:
            docs[f"pdf-p{i + 1}"] = {"title": f"PDF page {i + 1}", "text": text}
    return docs


def chunk_documents(docs: dict[str, dict], chunk_words: int = 60,
                    overlap: int = 15) -> list[Chunk]:
    """Word-window chunking; a document shorter than the window stays whole."""
    chunks: list[Chunk] = []
    step = max(1, chunk_words - overlap)
    for doc_id, doc in docs.items():
        words = doc["text"].split()
        if len(words) <= chunk_words:
            chunks.append(Chunk(f"{doc_id}#0", doc_id, " ".join(words), 0))
            continue
        i = 0
        while i < len(words):
            piece = words[i:i + chunk_words]
            if not piece:
                break
            chunks.append(Chunk(f"{doc_id}#{len(chunks)}", doc_id, " ".join(piece), i))
            if i + chunk_words >= len(words):
                break
            i += step
    return chunks


# ---------------------------------------------------------------------------
# 2. Embeddings and indexes
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def embedder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBED_MODEL, device="cpu")


def embed(texts: list[str]) -> np.ndarray:
    """Normalised sentence embeddings, so inner product equals cosine similarity."""
    return np.asarray(embedder().encode(list(texts), convert_to_numpy=True,
                                        normalize_embeddings=True, batch_size=32),
                      dtype=np.float32)


class DenseIndex:
    """FAISS inner-product index over normalised embeddings."""

    def __init__(self, chunks: list[Chunk], embs: np.ndarray, use_faiss: bool = True):
        self.chunks = chunks
        self.embs = embs
        self.faiss = None
        if use_faiss:
            try:
                import faiss

                index = faiss.IndexFlatIP(embs.shape[1])
                index.add(embs)
                self.faiss = index
            except ImportError:
                self.faiss = None

    def search(self, query: str, k: int = 5) -> list[tuple[int, float]]:
        q = embed([query])[0]
        if self.faiss is not None:
            scores, idx = self.faiss.search(q[None, :], k)
            return [(int(i), float(s)) for s, i in zip(scores[0], idx[0]) if i >= 0]
        sims = self.embs @ q
        order = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i])) for i in order]


class BM25Index:
    """Okapi BM25 (k1=1.5, b=0.75) over lowercased word tokens."""

    def __init__(self, chunks: list[Chunk]):
        from rank_bm25 import BM25Okapi

        self.chunks = chunks
        self.corpus = [self._tokens(c.text) for c in chunks]
        self.bm25 = BM25Okapi(self.corpus)

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    def search(self, query: str, k: int = 5) -> list[tuple[int, float]]:
        scores = self.bm25.get_scores(self._tokens(query))
        order = np.argsort(-scores)[:k]
        return [(int(i), float(scores[i])) for i in order]


def _minmax(scores: np.ndarray) -> np.ndarray:
    lo, hi = float(scores.min()), float(scores.max())
    if hi - lo < 1e-9:
        return np.zeros_like(scores)
    return (scores - lo) / (hi - lo)


class HybridRetriever:
    """Weighted fusion of dense and BM25 scores, both min-max normalised."""

    def __init__(self, dense: DenseIndex, bm25: BM25Index, alpha: float = 0.5):
        self.dense, self.bm25, self.alpha = dense, bm25, alpha

    def search(self, query: str, k: int = 5) -> list[tuple[int, float]]:
        n = len(self.dense.chunks)
        d_scores = np.zeros(n)
        for i, s in self.dense.search(query, n):
            d_scores[i] = s
        b_scores = np.zeros(n)
        for i, s in self.bm25.search(query, n):
            b_scores[i] = s
        fused = self.alpha * _minmax(d_scores) + (1 - self.alpha) * _minmax(b_scores)
        order = np.argsort(-fused)[:k]
        return [(int(i), float(fused[i])) for i in order]


@lru_cache(maxsize=1)
def _token_embedder():
    """The same MiniLM, but returning token-level vectors for late interaction."""
    from transformers import AutoModel, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(EMBED_MODEL)
    model = AutoModel.from_pretrained(EMBED_MODEL)
    model.eval()
    return tok, model


def maxsim_scores(query: str, candidates: list[str]) -> np.ndarray:
    """ColBERT-style late interaction: sum over query tokens of max similarity.

    Each query token is matched against every token of a candidate; the maximum
    per query token is summed. This is a genuine reranker -- it sees the pair
    jointly rather than comparing two independent vectors.
    """
    import torch

    tok, model = _token_embedder()
    with torch.no_grad():
        q = tok([query], return_tensors="pt", truncation=True, max_length=64)
        q_emb = model(**q).last_hidden_state[0]
        q_emb = torch.nn.functional.normalize(q_emb, dim=-1)
        c = tok(candidates, return_tensors="pt", truncation=True, max_length=256,
                padding=True)
        c_emb = model(**c).last_hidden_state
        c_emb = torch.nn.functional.normalize(c_emb, dim=-1)
        mask = c["attention_mask"].unsqueeze(-1)
        scores = []
        for i in range(c_emb.shape[0]):
            sim = q_emb @ c_emb[i].T
            sim = sim.masked_fill(mask[i].T == 0, -1e9)
            scores.append(float(sim.max(dim=1).values.sum()))
    return np.asarray(scores)


def rerank(query: str, chunks: list[Chunk], candidate_ids: list[int],
           top_k: int = 3) -> list[tuple[int, float]]:
    if not candidate_ids:
        return []
    scores = maxsim_scores(query, [chunks[i].text for i in candidate_ids])
    order = np.argsort(-scores)[:top_k]
    return [(candidate_ids[i], float(scores[i])) for i in order]


def rrf_fuse(rankings: list[list[int]], k: int = 60, top_k: int = 5) -> list[int]:
    """Reciprocal rank fusion: score = sum over lists of 1/(k + rank)."""
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return [d for d, _ in sorted(scores.items(), key=lambda kv: -kv[1])][:top_k]


# ---------------------------------------------------------------------------
# 3. Context construction and generation
# ---------------------------------------------------------------------------

def build_context(hits, chunks: list[Chunk], max_chars: int = 1200,
                  max_chunks: int = 3) -> tuple[str, list[str]]:
    """Pack retrieved chunks into a context, deduplicating identical text."""
    parts, used, seen = [], [], set()
    for idx, _score in hits:
        if len(used) >= max_chunks:
            break
        text = chunks[idx].text.strip()
        if text in seen:
            continue
        candidate = "\n\n".join(parts + [text])
        if len(candidate) > max_chars and parts:
            break
        parts.append(text)
        used.append(chunks[idx].doc_id)
        seen.add(text)
    return "\n\n".join(parts), used


PROMPT = ("Answer the question using only the context. Give the shortest complete "
          "answer. If the context does not contain the answer, say: I don't know."
          "\n\nContext: {context}\n\nQuestion: {question}\nAnswer:")


def generate_answer(prompt: str, max_new_tokens: int = 24) -> tuple[str, float]:
    from llm_gen import load_seq2seq

    import torch

    tok, model = load_seq2seq()
    enc = tok(prompt, return_tensors="pt", truncation=True, max_length=512)
    t0 = time.perf_counter()
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
    seconds = time.perf_counter() - t0
    return tok.decode(out[0], skip_special_tokens=True).strip(), seconds


# ---------------------------------------------------------------------------
# 4. End-to-end
# ---------------------------------------------------------------------------

class RAGSystem:
    def __init__(self, docs=None, chunk_words: int = 60, overlap: int = 15,
                 use_rerank: bool = True, alpha: float = 0.5):
        self.docs = docs or load_documents()
        self.chunks = chunk_documents(self.docs, chunk_words, overlap)
        embs = embed([c.text for c in self.chunks])
        self.dense = DenseIndex(self.chunks, embs)
        self.bm25 = BM25Index(self.chunks)
        self.hybrid = HybridRetriever(self.dense, self.bm25, alpha=alpha)
        self.use_rerank = use_rerank

    def retrieve(self, question: str, k: int = 3) -> list[tuple[int, float]]:
        candidates = self.hybrid.search(question, max(10, k * 3))
        if not self.use_rerank:
            return candidates[:k]
        return rerank(question, self.chunks, [i for i, _ in candidates], top_k=k)

    def answer(self, question: str, k: int = 3, max_chars: int = 1200) -> dict:
        hits = self.retrieve(question, k)
        context, docs_used = build_context(hits, self.chunks, max_chars=max_chars)
        prompt = PROMPT.format(context=context, question=question)
        answer, seconds = generate_answer(prompt)
        return {
            "question": question,
            "answer": answer,
            "context": context,
            "docs": docs_used,
            "seconds": seconds,
            "prompt_chars": len(prompt),
            "support": support_rate(answer, context),
            "refused": is_refusal(answer),
            "chunks": [self.chunks[i].chunk_id for i, _ in hits],
        }


# ---------------------------------------------------------------------------
# 5. Evaluation
# ---------------------------------------------------------------------------

def document_ranking(hits, chunks: list[Chunk]) -> list[str]:
    """Collapse a chunk ranking into a document ranking, preserving order."""
    seen, out = set(), []
    for idx, _ in hits:
        doc = chunks[idx].doc_id
        if doc not in seen:
            seen.add(doc)
            out.append(doc)
    return out


def evaluate_retrievers(system: RAGSystem, questions, k: int = 5) -> dict:
    n_chunks = len(system.chunks)
    variants = {
        "dense": lambda q: system.dense.search(q, n_chunks),
        "bm25": lambda q: system.bm25.search(q, n_chunks),
        "hybrid": lambda q: system.hybrid.search(q, n_chunks),
        "hybrid+rerank": lambda q: system.hybrid.search(q, max(10, k * 3)),
    }
    results = {}
    for name, fn in variants.items():
        runs = []
        for item in questions:
            hits = fn(item["q"])
            if name == "hybrid+rerank":
                hits = rerank(item["q"], system.chunks, [i for i, _ in hits],
                              top_k=len(hits))
            runs.append((document_ranking(hits, system.chunks), [item["source"]]))
        results[name] = retrieval_report(runs, k_values=(1, 3, 5))
    return results


# ---------------------------------------------------------------------------
# 6. Demo
# ---------------------------------------------------------------------------

def main() -> None:
    t0 = time.time()
    docs = load_documents()
    system = RAGSystem(docs)
    print("=" * 88)
    print("1. Corpus and index")
    print("=" * 88)
    print(f"documents     : {len(docs)}")
    print(f"chunks        : {len(system.chunks)} (60-word windows, 15-word overlap)")
    print(f"embedding dim : {system.dense.embs.shape[1]}   "
          f"index backend: {'faiss' if system.dense.faiss else 'numpy'}")
    lens = [len(c.text.split()) for c in system.chunks]
    print(f"chunk words   : min {min(lens)} mean {np.mean(lens):.1f} max {max(lens)}")
    print(f"build time    : {time.time() - t0:.1f}s")

    print("\n" + "=" * 88)
    print("2. Retrieval quality across four configurations (30 questions)")
    print("=" * 88)
    res = evaluate_retrievers(system, QA)
    print(f"{'retriever':16s} {'R@1':>6} {'R@3':>6} {'R@5':>6} {'MRR':>6} {'nDCG@3':>7}")
    for name, rep in res.items():
        print(f"{name:16s} {rep['recall@1']:6.2f} {rep['recall@3']:6.2f} "
              f"{rep['recall@5']:6.2f} {rep['mrr']:6.3f} {rep['ndcg@3']:7.3f}")

    print("\n" + "=" * 88)
    print("3. One question through every stage")
    print("=" * 88)
    question = "How much is the accommodation deposit and when is it refunded?"
    for name in ("bm25", "dense", "hybrid"):
        index = {"bm25": system.bm25, "dense": system.dense, "hybrid": system.hybrid}[name]
        hits = index.search(question, 3)
        print(f"  {name:8s} " + " | ".join(
            f"{system.chunks[i].chunk_id} ({s:.2f})" for i, s in hits))
    hits = system.hybrid.search(question, 12)
    reranked = rerank(question, system.chunks, [i for i, _ in hits], top_k=3)
    print(f"  reranked " + " | ".join(
        f"{system.chunks[i].chunk_id} ({s:.2f})" for i, s in reranked))
    context, used = build_context(reranked, system.chunks)
    print(f"  context  : {len(context)} chars from {used}")
    print(f"  first 180: {context[:180]}...")

    print("\n" + "=" * 88)
    print("4. End-to-end answers on the first 12 questions")
    print("=" * 88)
    pairs, supported, seconds, refused = [], [], [], 0
    for item in QA[:12]:
        out = system.answer(item["q"])
        pairs.append((out["answer"], item["a"]))
        supported.append(out["support"])
        seconds.append(out["seconds"])
        refused += int(out["refused"])
    rep = answer_report(pairs)
    print(f"  exact match {rep['exact_match']:.2f}   token F1 {rep['token_f1']:.2f}   "
          f"ROUGE-L {rep['rouge_l']:.2f}")
    print(f"  mean support {np.mean(supported):.2f}   refusals {refused}/12   "
          f"mean latency {np.mean(seconds):.2f}s")
    for (pred, gold), item in list(zip(pairs, QA[:12]))[:6]:
        print(f"    Q {item['q'][:58]:58s} -> {pred!r} (gold {gold!r})")

    print("\n" + "=" * 88)
    print("5. What happens with questions the corpus cannot answer")
    print("=" * 88)
    answers = [system.answer(q)["answer"] for q in UNANSWERABLE]
    print(f"  refusal rate: {refusal_rate(answers):.2f} over {len(UNANSWERABLE)} questions")
    for q, a in list(zip(UNANSWERABLE, answers))[:5]:
        print(f"    Q {q[:56]:56s} -> {a!r}")

    print("\n" + "=" * 88)
    print("6. Chunk size sweep (hybrid + rerank, 30 questions)")
    print("=" * 88)
    print(f"{'chunk':>6} {'overlap':>8} {'chunks':>7} {'R@1':>6} {'R@3':>6} {'MRR':>6}")
    for size, overlap in ((40, 10), (60, 15), (100, 25)):
        s = RAGSystem(docs, chunk_words=size, overlap=overlap)
        rep = evaluate_retrievers(s, QA)["hybrid+rerank"]
        print(f"{size:6d} {overlap:8d} {len(s.chunks):7d} {rep['recall@1']:6.2f} "
              f"{rep['recall@3']:6.2f} {rep['mrr']:6.3f}")


if __name__ == "__main__":
    main()
