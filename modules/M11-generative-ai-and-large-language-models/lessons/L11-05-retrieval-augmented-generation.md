# L11-05 — Retrieval-Augmented Generation

[← Previous: L11-04](L11-04-prompt-engineering-and-in-context-learning.md) · [Module home](../README.md) · [Next: L11-06 →](L11-06-fine-tuning-and-parameter-efficient-adaptation.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Building a RAG System](#4-the-procedure-building-a-rag-system)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Python Implementation](#7-python-implementation)
- [8. Practical Applications](#8-practical-applications)
- [9. Common Mistakes](#9-common-mistakes)
- [10. Practical Exercises](#10-practical-exercises)
- [11. Self-Assessment](#11-self-assessment)
- [12. Key Terms](#12-key-terms)
- [13. Further Reading](#13-further-reading)
- [What to Do Next](#what-to-do-next)

> **Module M11** · Lesson 5 of 7 · ~90 minutes · Level 400
> **Prerequisites:** L11-02 (embeddings), L11-04 (prompting)

[Previous: L11-04](L11-04-prompt-engineering-and-in-context-learning.md) · [Module overview](../README.md) · [Next: L11-06 →](L11-06-fine-tuning-and-parameter-efficient-adaptation.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Draw** the RAG architecture and name the failure mode of each stage.
2. **Ingest** documents from markdown and PDF and chunk them with deliberate overlap.
3. **Compare** dense, lexical and hybrid retrieval on a labelled question set.
4. **Explain** why BM25 beats embeddings on some queries and vice versa.
5. **Implement** reranking and reciprocal rank fusion.
6. **Build** a context that fits a token budget without duplicating text.
7. **Evaluate** retrieval and generation separately, and say which one failed.

## 2. Prerequisite Knowledge

Cosine similarity, the token budget (L11-02), and the refusal-path prompt (L11-04).

## 3. Conceptual Explanation

### 3.1 The architecture

```text
documents ──► ingest ──► chunk ──► embed ─────► vector index ──┐
                                       │                       │
                                  BM25 index ──► fuse ──► rerank ──► context builder
                                                                        │
question ──► embed ─────────────────────────────────────────────────────┘
                                                                        ▼
                                                            prompt + LLM ──► answer
                                                                        │
                                                                    citations
```

Two independent systems: **retrieval** (did we find the right text?) and **generation** (did
the model use it?). Conflating them is the most common RAG mistake — a wrong answer with the
right document retrieved is a generation problem, and no amount of prompt tweaking fixes a
retrieval miss.

### 3.2 Ingestion

Sources are files, PDFs, web pages or databases. Two rules:

- **Preserve provenance.** Every chunk carries its parent document id and position, or you
  cannot cite, debug or deduplicate.
- **Clean before chunking.** PDF extraction yields hyphenation, headers and page numbers;
  strip them or they become embeddings noise. The PDF built for this module is 4 pages and
  extracts 12,471 characters, close to the 11,608 characters of source text.

### 3.3 Chunking

Chunking trades recall against precision:

- too large → the embedding averages several topics and matches nothing well, and the
  context fills with irrelevant text;
- too small → a sentence loses the antecedent it needs ("it is refunded within 28 days" —
  what is "it"?);
- overlap preserves boundary sentences at the cost of duplicate retrieval.

Measured on the handbook with hybrid+rerank:

| chunk words | overlap | chunks | recall@1 | recall@3 | MRR | end-to-end EM |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 40 | 10 | 69 | 0.93 | 1.00 | 0.967 | 0.67 |
| 60 | 15 | 48 | 1.00 | 1.00 | 1.000 | 0.75 |
| 100 | 25 | 24 | 0.93 | 1.00 | 0.967 | 0.75 |

Both extremes lose a question at rank 1. Small chunks fragment answers; large chunks dilute
them. Sixty words with fifteen overlap is the best point measured here, and it is a
**measured** choice, not a universal constant. This document set is short (mean 79 words), so
the optimum is close to a whole document.

### 3.4 Embeddings and vector search

An embedding maps text to a fixed-length vector so that similar meaning is nearby. This
module uses `all-MiniLM-L6-v2`: 384 dimensions, 22M parameters, Apache-2.0. Embeddings are
L2-normalised, so inner product is cosine similarity and a FAISS `IndexFlatIP` is exact
nearest-neighbour search.

Cost: encoding 48 chunks took part of the 44.9 s index build on this CPU — mostly model
loading. For 100,000 chunks, batch encoding dominates and an approximate index (HNSW, IVF)
becomes necessary.

### 3.5 Lexical retrieval: BM25

BM25 scores a document by term overlap, saturating term frequency and normalising by length:

$$
\text{score}(q,d)=\sum_{t\in q}\text{IDF}(t)\cdot
\frac{f_{t,d}(k_1+1)}{f_{t,d}+k_1\left(1-b+b\frac{|d|}{\text{avgdl}}\right)} .
$$

It is unbeatable on rare exact tokens — policy numbers, error codes, names. Here it beat
dense retrieval at rank 1 (0.97 versus 0.90) because the questions quote handbook phrases
almost verbatim.

### 3.6 Hybrid retrieval and reranking

Dense and lexical scores are on different scales, so normalise before fusing:

$$
s=\alpha\,\tilde s_{\text{dense}}+(1-\alpha)\,\tilde s_{\text{BM25}},\qquad \alpha=0.5 .
$$

Measured over 30 questions:

| retriever | recall@1 | recall@3 | MRR | nDCG@3 |
| :--- | ---: | ---: | ---: | ---: |
| dense | 0.90 | 1.00 | 0.944 | 0.959 |
| BM25 | 0.97 | 1.00 | 0.983 | 0.988 |
| hybrid | 1.00 | 1.00 | 1.000 | 1.000 |
| hybrid + rerank | 1.00 | 1.00 | 1.000 | 1.000 |

Hybrid fusion fixes both misses. Reranking does not change these top-line numbers, because
retrieval was already perfect — but it reorders the middle of the list, which matters for
context packing. That is an honest negative result: **on an easy corpus, reranking has
nothing to fix.** The task in LAB-11-02 deliberately includes harder multi-document
questions where it does.

**Late-interaction reranking** (ColBERT-style) scores a query–document pair jointly: sum,
over query tokens, of the maximum similarity to any document token.

$$
\text{score}(q,d)=\sum_{i\in q}\max_{j\in d}\;\cos(e_i,e_j).
$$

Measured on the deposit question, the fused ranking `hb-07#12 (1.00), hb-07#13 (0.80),
hb-09#17 (0.72)` became `hb-07#12 (9.42), hb-07#13 (8.10), hb-06#11 (6.92)` after reranking —
the unrelated assessment document was pushed out of the top three.

**RRF** is the alternative when you cannot normalise scores:

$$
\text{RRF}(d)=\sum_{r\in\text{rankers}}\frac{1}{k+\text{rank}_r(d)} .
$$

### 3.7 Context construction

Pack chunks until the budget is reached, deduplicating identical text. For the deposit
question the top three chunks produced an 810-character context from documents
`['hb-07','hb-07','hb-06']` — two adjacent chunks of the same document plus a `hb-06`
chunk about scholarships. The second is irrelevant but harmless; the first two contain the
answer split across a boundary. **Overlap is what makes that recoverable.**

### 3.8 Generation and citation

The model answers from the packed context. Measured over 12 questions: exact match **0.75**,
token F1 **0.85**, ROUGE-L **0.85**, mean grounding score **1.00**, mean latency **1.84 s**,
refusals 0/12. Two failures are instructive:

- "when does the library open on weekdays" returned `'20:00'` — a real number from the
  context (summer closing time), wrong for the question. Retrieval succeeded; the model
  chose the wrong span.
- "when is the second tuition instalment due" returned `'15 October'` instead of
  `'15 January'`.

Both are generation errors of the *selection* kind, invisible to a retrieval metric. Only
per-question comparison with gold answers catches them.

### 3.9 Advanced RAG

- **Query rewriting** — expand acronyms, resolve pronouns, or generate two paraphrases and fuse with RRF.
- **HyDE** — generate a hypothetical answer and retrieve with it; helps when questions are short and documents are long.
- **Multi-hop** — retrieve, extract a sub-question, retrieve again (three questions in this module need two documents).
- **Parent–child retrieval** — match small chunks, return their larger parent for context.
- **Filtering** — metadata constraints (date, department) before similarity search.
- **Caching** — embed and answer caches; measure hit rate before claiming a saving.

Each adds a stage that can fail. Add one at a time and measure the same metrics.

## 4. The Procedure: Building a RAG System

1. Fix a question set with gold answers *and* gold documents (30+ items).
2. Ingest, clean, chunk; record provenance.
3. Build a BM25 index and a dense index; measure both separately.
4. Fuse; measure again. If fusion does not help, stop and check your normalisation.
5. Add reranking only if the fused top-5 contains the right document but at a bad rank.
6. Pack the context; enforce the token budget.
7. Generate with a refusal path; score answers and grounding.
8. Slice errors by stage: retrieval miss, wrong span, unsupported claim, unnecessary refusal.

## 5. Worked Examples

### Example 1 — a retrieval miss and what it looks like

"What is the difference between a self-certified extension and mitigating circumstances?"
needs `hb-10`. At 40-word chunks the answer is split across two chunks; the top chunk
contains the extension but not the mitigating-circumstances sentence, so the generated answer
omits half the comparison while sounding complete. **Recall@1 was still 1.00** — the metric
was satisfied, the user was not. This is why end-to-end EM is measured separately.

### Example 2 — refusing correctly

The eight unanswerable questions produced a refusal rate of **0.00**: `'15 working days'` for
a dissertation deadline, `'1'` for a scholarship count, `'40 GBP'` for a city-centre parking
fine, `'John C.'` for a professor's name. Every answer was grounded in *some* retrieved text
and none was correct. Compare this with the oracle-context experiment in L11-03, where the
same model also refused 0.00. **A refusal instruction in the prompt is not sufficient.**
Production mitigations: retrieve-then-threshold (refuse if the top score is below a calibrated
cut-off), answer-then-verify (check the answer's numbers against the context), and an explicit
"not found" document.

### Example 3 — hybrid score arithmetic

Dense raw scores 0.46 and 0.46 for two chunks, BM25 10.78 and 9.97. Min-max normalisation
maps dense to (1.00, 0.99) and BM25 to (1.00, 0.86); the fused score at $\alpha=0.5$ is
0.995 for the first and 0.925 for the second. Without normalisation, BM25's scale would
dominate and the "hybrid" would be BM25 in disguise.

## 6. Mathematical Formulation

Cosine similarity on normalised vectors, BM25, score fusion, MaxSim reranking and RRF are
given in §3.5–3.6. Retrieval metrics used throughout:

$$
\text{Recall@}k=\frac{|\text{rel}\cap\text{top}_k|}{|\text{rel}|},\qquad
\text{MRR}=\frac1{|Q|}\sum_{q}\frac{1}{\text{rank}_q(\text{first relevant})},
$$

$$
\text{nDCG@}k=\frac{\text{DCG@}k}{\text{IDCG@}k},\qquad
\text{DCG@}k=\sum_{i=1}^{k}\frac{\text{rel}_i}{\log_2(i+1)} .
$$

## 7. Python Implementation

```python
# run from modules/M11-generative-ai-and-large-language-models/code
from rag import RAGSystem, evaluate_retrievers, build_context
from gen_data import QA

system = RAGSystem()                    # 24 docs -> 48 chunks, MiniLM + FAISS + BM25
print(len(system.chunks), system.dense.embs.shape)
print(evaluate_retrievers(system, QA)["hybrid"])

out = system.answer("How much is the accommodation deposit?")
print(out["answer"], out["docs"], round(out["support"], 2), round(out["seconds"], 2))
```

```text
48 (48, 384)
{'recall@1': 1.0, 'precision@1': 1.0, 'ndcg@1': 1.0, 'recall@3': 1.0,
 'precision@3': 0.333, 'ndcg@3': 1.0, 'recall@5': 1.0, 'precision@5': 0.2,
 'ndcg@5': 1.0, 'mrr': 1.0}
400 GBP ['hb-07', 'hb-07', 'hb-06'] 1.0 1.8
```

The `precision@3 = 0.333` is correct and not a bug: only one document is relevant, so any
k greater than 1 caps precision at 1/k.

## 8. Practical Applications

- **Handbook and policy assistants** — stable facts, high exact-match expectations.
- **Support deflection** — measure the escalation rate, not just answer accuracy.
- **Code and API documentation** — lexical retrieval is strong on identifiers.
- **Clinical or legal retrieval** — add human review; the cost of a confident wrong answer is high.

## 9. Common Mistakes

1. Evaluating the answer without evaluating retrieval, then "fixing" the prompt.
2. Chunking by characters and assuming that equals tokens.
3. No overlap, so answers that straddle a boundary disappear.
4. Fusing unnormalised scores.
5. Packing every retrieved chunk into the context until the window overflows.
6. No refusal path, or a refusal path the model ignores.
7. Claiming reranking helps when retrieval was already perfect.

## 10. Practical Exercises

**Beginner**

1. Reproduce the retrieval table. Which retriever wins at rank 1, and why?
2. Ask three questions the corpus cannot answer and record the answers verbatim.

**Intermediate**

3. Set `alpha` to 0.0, 0.5 and 1.0; report recall@1 and explain the endpoints.
4. Change chunk size to 30 words and re-measure; inspect one broken chunk.
5. Implement a score threshold: refuse when the top fused score is below a value you calibrate on the unanswerable set.

**Advanced**

6. Add query rewriting with two paraphrases and fuse with RRF; measure the delta on the 30 questions.
7. Replace MaxSim reranking with a cross-encoder and compare latency and nDCG.
8. Implement parent–child retrieval: retrieve 40-word chunks, return the parent document.

## 11. Self-Assessment

**Multiple choice**

1. A wrong answer with the correct document in the context is
   a) a retrieval failure. b) a generation failure. c) a chunking failure. d) an embedding failure.
2. BM25 excels at
   a) paraphrase matching. b) rare exact terms. c) image retrieval. d) long documents only.
3. Hybrid retrieval requires
   a) a GPU. b) score normalisation before fusion. c) no index. d) a reranker.
4. MaxSim reranking scores a pair by
   a) cosine of mean vectors. b) summing per-query-token maximum similarities. c) BM25. d) edit distance.

**Short answer**

5. Why can recall@1 be 1.00 while the answer is still wrong?
6. Give one reason to prefer parent–child retrieval over large chunks.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. The right document can be retrieved while the model selects the wrong span within it, or the chunk omits the sentence that matters.
6. It keeps the embedding precise (small child chunks) while giving the generator the wider parent context it needs to answer completely.

</details>

## 12. Key Terms

**RAG**, **ingestion**, **chunking**, **overlap**, **embedding**, **vector database**,
**similarity search**, **cosine similarity**, **BM25**, **hybrid retrieval**, **score fusion**,
**reranking**, **late interaction**, **MaxSim**, **reciprocal rank fusion**, **context
construction**, **grounding**, **citation**, **query rewriting**, **HyDE**.

## 13. Further Reading

- Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*.
- Robertson & Zaragoza (2009). *The Probabilistic Relevance Framework: BM25 and Beyond*.
- Khattab & Zaharia (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction*.
- Cormack, Clarke & Buettcher (2009). *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods*.
- Gao et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey*.

## What to Do Next

1. Run `python rag.py` and keep the tables.
2. Do exercises 1–3, then LAB-11-02.
3. Continue to [L11-06 — Fine-Tuning and Parameter-Efficient Adaptation](L11-06-fine-tuning-and-parameter-efficient-adaptation.md).

---

**Navigation:** [← Previous: L11-04](L11-04-prompt-engineering-and-in-context-learning.md) · [Module home](../README.md) · [Next: L11-06 →](L11-06-fine-tuning-and-parameter-efficient-adaptation.md)
