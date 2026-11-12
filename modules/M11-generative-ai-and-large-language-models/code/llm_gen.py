"""llm_gen.py -- sampling, perplexity, grounding and inference cost (M11, L11-02/L11-04/L11-06).

Everything runs locally on CPU with two small pretrained models that are cached
by the Hugging Face hub the first time:

    distilgpt2         82M-parameter decoder, used for next-token sampling
    google/flan-t5-small  77M-parameter encoder-decoder, used for question answering

The file implements the decoding strategies by hand (greedy, temperature,
top-k, nucleus, repetition penalty) so you can read the code that produces the
distribution, instead of calling a black box. It also measures:

    - perplexity of the language model on held-out handbook text
    - whether a prompt-plus-context answer is grounded or hallucinated
    - the exact-match gain from giving the model context
    - the size and latency change from dynamic int8 quantisation
    - the speed-up from the key/value cache

Run ``python llm_gen.py``. The numbers quoted in the lessons come from here.
"""

from __future__ import annotations

import time
from functools import lru_cache

import numpy as np
import torch

from llm_eval import answer_report, is_refusal, refusal_rate, support_rate, unsupported_numbers

DISTILGPT2 = "distilgpt2"
FLAN = "google/flan-t5-small"


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)


# ---------------------------------------------------------------------------
# Model loading (cached in-process)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=2)
def load_causal(name: str = DISTILGPT2):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name)
    model.eval()
    return tok, model


@lru_cache(maxsize=2)
def load_seq2seq(name: str = FLAN):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSeq2SeqLM.from_pretrained(name)
    model.eval()
    return tok, model


def param_bytes(model) -> int:
    return sum(p.numel() * p.element_size() for p in model.parameters())


# ---------------------------------------------------------------------------
# 1. Decoding, implemented by hand
# ---------------------------------------------------------------------------

def _filter_top_k(logits: torch.Tensor, k: int) -> torch.Tensor:
    if k <= 0 or k >= logits.numel():
        return logits
    kth = torch.topk(logits, k).values[-1]
    return torch.where(logits < kth, torch.full_like(logits, -float("inf")), logits)


def _filter_top_p(logits: torch.Tensor, p: float) -> torch.Tensor:
    """Nucleus sampling: keep the smallest set of tokens whose mass reaches p."""
    if p >= 1.0:
        return logits
    sorted_logits, sorted_idx = torch.sort(logits, descending=True)
    probs = torch.softmax(sorted_logits, dim=-1)
    cumulative = torch.cumsum(probs, dim=-1)
    # keep the token that crosses p, drop everything after it
    cutoff = cumulative - probs > p
    sorted_logits = sorted_logits.masked_fill(cutoff, -float("inf"))
    out = torch.full_like(logits, -float("inf"))
    out[sorted_idx] = sorted_logits
    return out


def _apply_repetition_penalty(logits, generated_ids, penalty: float) -> torch.Tensor:
    if penalty == 1.0 or not generated_ids:
        return logits
    ids = torch.tensor(sorted(set(generated_ids)), dtype=torch.long)
    selected = logits[ids]
    logits = logits.clone()
    logits[ids] = torch.where(selected < 0, selected * penalty, selected / penalty)
    return logits


@torch.no_grad()
def sample_text(prompt: str, max_new_tokens: int = 24, temperature: float = 1.0,
                top_k: int | None = None, top_p: float | None = None,
                repetition_penalty: float = 1.0, greedy: bool = False,
                seed: int = 0, model_name: str = DISTILGPT2) -> dict:
    """Generate text token by token and return the text plus diagnostics.

    Diagnostics: mean predictive entropy (nats), distinct-1/2, repetition rate,
    tokens per second and the per-step log-probability of the chosen token.
    """
    tok, model = load_causal(model_name)
    set_seed(seed)
    generator = torch.Generator().manual_seed(seed)
    ids = tok(prompt, return_tensors="pt")["input_ids"]
    prompt_len = ids.shape[1]
    entropies, chosen_logp = [], []
    t0 = time.perf_counter()

    for _ in range(max_new_tokens):
        logits = model(ids).logits[0, -1].double()
        logits = _apply_repetition_penalty(logits, ids[0, prompt_len:].tolist(),
                                           repetition_penalty)
        if greedy:
            logits = torch.where(logits == logits.max(), logits,
                                 torch.full_like(logits, -float("inf")))
        else:
            logits = logits / max(1e-6, temperature)
            if top_k:
                logits = _filter_top_k(logits, top_k)
            if top_p is not None and top_p < 1.0:
                logits = _filter_top_p(logits, top_p)
        probs = torch.softmax(logits, dim=-1)
        entropies.append(float(-(probs * torch.log(probs + 1e-12)).sum()))
        token = int(torch.multinomial(probs, 1, generator=generator))
        chosen_logp.append(float(torch.log(probs[token] + 1e-12)))
        ids = torch.cat([ids, torch.tensor([[token]])], dim=1)
        if token == tok.eos_token_id:
            break

    seconds = time.perf_counter() - t0
    new_ids = ids[0, prompt_len:].tolist()
    text = tok.decode(new_ids, skip_special_tokens=True)
    words = text.split()

    def distinct(n: int) -> float:
        if len(new_ids) < n:
            return 0.0
        grams = [tuple(new_ids[i:i + n]) for i in range(len(new_ids) - n + 1)]
        return len(set(grams)) / len(grams)

    return {
        "text": text,
        "new_tokens": len(new_ids),
        "seconds": seconds,
        "tokens_per_s": len(new_ids) / seconds if seconds else 0.0,
        "mean_entropy": float(np.mean(entropies)) if entropies else 0.0,
        "mean_logp": float(np.mean(chosen_logp)) if chosen_logp else 0.0,
        "distinct_1": distinct(1),
        "distinct_2": distinct(2),
        "repetition_rate": 1.0 - len(set(words)) / len(words) if words else 0.0,
    }


# ---------------------------------------------------------------------------
# 2. Perplexity
# ---------------------------------------------------------------------------

@torch.no_grad()
def perplexity(text: str, model_name: str = DISTILGPT2, stride: int = 256,
               max_tokens: int = 1024) -> dict:
    """Sliding-window perplexity: exp(mean negative log-likelihood per token).

    Only tokens in the newly consumed window contribute, which is the standard
    stride trick that avoids double-counting the overlap.
    """
    tok, model = load_causal(model_name)
    ids = tok(text, return_tensors="pt")["input_ids"][0]
    if len(ids) < 2:
        return {"tokens": len(ids), "perplexity": float("nan"), "nll_per_token": float("nan")}
    ids = ids[:max_tokens]
    total_nll, counted = 0.0, 0
    for begin in range(0, len(ids), stride):
        end = min(begin + stride, len(ids))
        window = ids[max(0, end - model.config.n_positions):end].unsqueeze(0)
        logits = model(window).logits[0].double()
        target = window[0, 1:]
        logprobs = torch.log_softmax(logits[:-1], dim=-1)
        nll = -logprobs.gather(1, target.unsqueeze(1)).squeeze(1)
        # count only the tokens beyond the previous window
        start_in_window = max(0, len(window[0]) - (end - begin))
        total_nll += float(nll[start_in_window - 1:].sum()) if start_in_window else float(nll.sum())
        counted += int(end - begin) - (1 if begin > 0 else 0)
        if end == len(ids):
            break
    nll_per_token = total_nll / max(1, counted)
    return {"tokens": int(len(ids)), "nll_per_token": nll_per_token,
            "perplexity": float(np.exp(nll_per_token))}


# ---------------------------------------------------------------------------
# 3. Question answering with and without context
# ---------------------------------------------------------------------------

def flan_answer(context: str, question: str, instruction: str | None = None,
                max_new_tokens: int = 24) -> dict:
    tok, model = load_seq2seq()
    if instruction is None:
        instruction = ("Answer the question using only the context. "
                       "If the context does not contain the answer, say: I don't know.")
    prompt = f"{instruction}\n\nContext: {context}\n\nQuestion: {question}\nAnswer:"
    enc = tok(prompt, return_tensors="pt", truncation=True, max_length=512)
    t0 = time.perf_counter()
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
    seconds = time.perf_counter() - t0
    text = tok.decode(out[0], skip_special_tokens=True).strip()
    return {"answer": text, "seconds": seconds, "prompt_tokens": int(enc["input_ids"].shape[1])}


def closed_book_answer(question: str, max_new_tokens: int = 24) -> dict:
    tok, model = load_seq2seq()
    prompt = f"Answer the question in as few words as possible.\n\nQuestion: {question}\nAnswer:"
    enc = tok(prompt, return_tensors="pt", truncation=True, max_length=512)
    t0 = time.perf_counter()
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
    seconds = time.perf_counter() - t0
    return {"answer": tok.decode(out[0], skip_special_tokens=True).strip(),
            "seconds": seconds, "prompt_tokens": int(enc["input_ids"].shape[1])}


@torch.no_grad()
def kv_cache_timing(prompt: str, max_new_tokens: int = 32) -> dict:
    """Compare generation with and without the key/value cache."""
    tok, model = load_causal()
    ids = tok(prompt, return_tensors="pt")["input_ids"]
    results = {}
    for use_cache in (False, True):
        ids_run = ids.clone()
        t0 = time.perf_counter()
        for _ in range(max_new_tokens):
            out = model(ids_run, use_cache=use_cache)
            token = int(out.logits[0, -1].argmax())
            ids_run = torch.cat([ids_run, torch.tensor([[token]])], dim=1)
        results["with_cache" if use_cache else "no_cache"] = time.perf_counter() - t0
    results["speedup"] = results["no_cache"] / results["with_cache"]
    return results


# ---------------------------------------------------------------------------
# 4. Quantisation
# ---------------------------------------------------------------------------

def quantization_report(max_new_tokens: int = 16) -> dict:
    """Dynamic int8 quantisation of flan-t5-small: size, latency and quality."""
    import copy

    tok, model = load_seq2seq()
    questions = [
        ("The library opens at 08:00 on weekdays.", "When does the library open?"),
        ("The accommodation deposit is 400 GBP.", "What is the deposit?"),
        ("Students may borrow 12 items at a time.", "How many items can I borrow?"),
        ("The IT helpdesk closes at 20:00 on weekdays.", "When does the IT helpdesk close?"),
    ]
    golds = ["08:00", "400 GBP", "12", "20:00"]

    def run(m, tag):
        preds, seconds = [], []
        for ctx, q in questions:
            prompt = (f"Answer the question using only the context.\n\nContext: {ctx}\n\n"
                      f"Question: {q}\nAnswer:")
            enc = tok(prompt, return_tensors="pt", truncation=True, max_length=256)
            t0 = time.perf_counter()
            with torch.no_grad():
                out = m.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
            seconds.append(time.perf_counter() - t0)
            preds.append(tok.decode(out[0], skip_special_tokens=True).strip())
        rep = answer_report(list(zip(preds, golds)))
        return {"tag": tag, "size_mb": param_bytes(m) / 1e6,
                "mean_latency_s": float(np.mean(seconds)),
                "em": rep["exact_match"], "f1": rep["token_f1"], "preds": preds}

    base = run(model, "fp32")
    try:
        from torch.ao.quantization import quantize_dynamic

        qmodel = quantize_dynamic(copy.deepcopy(model), {torch.nn.Linear}, dtype=torch.qint8)
        quant = run(qmodel, "int8-dynamic")
    except Exception as exc:                       # pragma: no cover - environment dependent
        quant = {"tag": "int8-dynamic", "error": repr(exc)}
    return {"fp32": base, "int8": quant}


# ---------------------------------------------------------------------------
# 5. Demo
# ---------------------------------------------------------------------------

def main() -> None:
    from gen_data import HANDBOOK, QA, UNANSWERABLE

    prompt = "The library opens at"
    print("=" * 88)
    print("1. Decoding strategies from the same prompt, 24 new tokens, seed 0")
    print("=" * 88)
    configs = [
        ("greedy", dict(greedy=True)),
        ("temperature 0.7", dict(temperature=0.7)),
        ("temperature 1.0", dict(temperature=1.0)),
        ("temperature 1.5", dict(temperature=1.5)),
        ("top-k 40, T 1.0", dict(top_k=40, temperature=1.0)),
        ("top-p 0.9, T 1.0", dict(top_p=0.9, temperature=1.0)),
        ("top-p 0.9, T 1.2, rep 1.3", dict(top_p=0.9, temperature=1.2, repetition_penalty=1.3)),
    ]
    print(f"{'strategy':30s} {'entropy':>7} {'distinct-2':>10} {'rep':>5} {'tok/s':>7}  text")
    for name, kw in configs:
        r = sample_text(prompt, **kw)
        print(f"{name:30s} {r['mean_entropy']:7.3f} {r['distinct_2']:10.2f} "
              f"{r['repetition_rate']:5.2f} {r['tokens_per_s']:7.1f}  {r['text'][:44]!r}")

    print("\n" + "=" * 88)
    print("2. Determinism: the same seed reproduces the same text")
    print("=" * 88)
    a = sample_text(prompt, temperature=1.0, seed=7)["text"]
    b = sample_text(prompt, temperature=1.0, seed=7)["text"]
    c = sample_text(prompt, temperature=1.0, seed=8)["text"]
    print(f"  seed 7 twice identical: {a == b}")
    print(f"  seed 7 vs seed 8 differ: {a != c}")
    print(f"  text: {a!r}")

    print("\n" + "=" * 88)
    print("3. Perplexity on held-out handbook text (distilgpt2)")
    print("=" * 88)
    for doc_id in ("hb-13", "hb-17", "hb-22"):
        rep = perplexity(HANDBOOK[doc_id]["text"])
        print(f"  {doc_id} {HANDBOOK[doc_id]['title'][:34]:34s} tokens {rep['tokens']:4d}  "
              f"nll {rep['nll_per_token']:.3f}  perplexity {rep['perplexity']:7.2f}")

    print("\n" + "=" * 88)
    print("4. Grounded versus closed-book answers (flan-t5-small, 15 questions)")
    print("=" * 88)
    n = 15
    grounded, closed = [], []
    ctx_for, lat_g, lat_c = [], [], []
    for item in QA[:n]:
        context = HANDBOOK[item["source"]]["text"]
        g = flan_answer(context, item["q"])
        c = closed_book_answer(item["q"])
        grounded.append((g["answer"], item["a"]))
        closed.append((c["answer"], item["a"]))
        ctx_for.append((g["answer"], context))
        lat_g.append(g["seconds"])
        lat_c.append(c["seconds"])
    gr, cr = answer_report(grounded), answer_report(closed)
    print(f"{'condition':18s} {'EM':>6} {'token F1':>9} {'ROUGE-L':>8} {'support':>8} {'mean s':>7}")
    print(f"{'grounded':18s} {gr['exact_match']:6.2f} {gr['token_f1']:9.2f} "
          f"{gr['rouge_l']:8.2f} "
          f"{np.mean([support_rate(a, c) for a, c in ctx_for]):8.2f} {np.mean(lat_g):7.2f}")
    print(f"{'closed book':18s} {cr['exact_match']:6.2f} {cr['token_f1']:9.2f} "
          f"{cr['rouge_l']:8.2f} {'-':>8} {np.mean(lat_c):7.2f}")
    print("\n  first five grounded answers:")
    for (pred, gold), (ctx, q) in zip(grounded[:5], [(HANDBOOK[i["source"]]["text"], i["q"])
                                                    for i in QA[:5]]):
        print(f"    Q: {q}")
        print(f"       pred {pred!r}  gold {gold!r}")
    print("\n  first five closed-book answers:")
    for pred, gold in closed[:5]:
        print(f"    pred {pred!r}  gold {gold!r}")

    print("\n" + "=" * 88)
    print("5. Unanswerable questions: does the model refuse?")
    print("=" * 88)
    un_g, un_c, flagged = [], [], []
    for q in UNANSWERABLE:
        # the closest document, pretending retrieval returned something irrelevant
        ctx = HANDBOOK["hb-09"]["text"]
        a = flan_answer(ctx, q)
        c = closed_book_answer(q)
        un_g.append(a["answer"])
        un_c.append(c["answer"])
        flagged.append(unsupported_numbers(a["answer"], ctx))
    print(f"  grounded refusal rate   : {refusal_rate(un_g):.2f}")
    print(f"  closed-book refusal rate: {refusal_rate(un_c):.2f}")
    print(f"  grounded answers with numbers absent from the context: "
          f"{sum(1 for f in flagged if f)}/{len(flagged)}")
    for q, a in list(zip(UNANSWERABLE, un_g))[:4]:
        print(f"    Q: {q}\n       -> {a!r}")

    print("\n" + "=" * 88)
    print("6. Prompt template comparison on the same 12 questions")
    print("=" * 88)
    templates = {
        "plain": "Context: {ctx}\n\nQuestion: {q}\nAnswer:",
        "instructed": ("Answer the question using only the context. If the context does "
                       "not contain the answer, say: I don't know.\n\nContext: {ctx}\n\n"
                       "Question: {q}\nAnswer:"),
        "extractive": ("You are a university handbook assistant. Quote the shortest "
                       "span of the context that answers the question, and nothing else.\n\n"
                       "Context: {ctx}\n\nQuestion: {q}\nShort answer:"),
    }
    subset = QA[:12]
    print(f"{'template':12s} {'EM':>6} {'token F1':>9} {'refusals':>9} {'mean s':>7}")
    for name, tpl in templates.items():
        preds, secs = [], []
        tok, model = load_seq2seq()
        for item in subset:
            p = tpl.format(ctx=HANDBOOK[item["source"]]["text"], q=item["q"])
            enc = tok(p, return_tensors="pt", truncation=True, max_length=512)
            t0 = time.perf_counter()
            with torch.no_grad():
                out = model.generate(**enc, max_new_tokens=24, do_sample=False)
            secs.append(time.perf_counter() - t0)
            preds.append(tok.decode(out[0], skip_special_tokens=True).strip())
        rep = answer_report([(p, item["a"]) for p, item in zip(preds, subset)])
        print(f"{name:12s} {rep['exact_match']:6.2f} {rep['token_f1']:9.2f} "
              f"{refusal_rate(preds):9.2f} {np.mean(secs):7.2f}")

    print("\n" + "=" * 88)
    print("7. Quantisation and the key/value cache")
    print("=" * 88)
    qr = quantization_report()
    base = qr["fp32"]
    print(f"  fp32        size {base['size_mb']:.1f} MB  latency {base['mean_latency_s']:.3f}s  "
          f"EM {base['em']:.2f}  F1 {base['f1']:.2f}")
    if "error" in qr["int8"]:
        print(f"  int8        failed: {qr['int8']['error']}")
    else:
        q = qr["int8"]
        print(f"  int8-dynamic size {q['size_mb']:.1f} MB  latency {q['mean_latency_s']:.3f}s  "
              f"EM {q['em']:.2f}  F1 {q['f1']:.2f}")

    kvc = kv_cache_timing("The Hartley Library is open from 08:00 to 23:00", 24)
    print(f"  generation 24 tokens: no cache {kvc['no_cache']:.2f}s  "
          f"cache {kvc['with_cache']:.2f}s  speedup {kvc['speedup']:.1f}x")


if __name__ == "__main__":
    main()
