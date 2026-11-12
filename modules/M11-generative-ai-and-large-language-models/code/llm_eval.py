"""llm_eval.py -- metrics for LLM systems (M11, L11-07 and LAB-11-03).

Four families, because a RAG system can fail at four different places:

    retrieval   recall@k, precision@k, MRR, nDCG@k
    answer      exact match, token F1, ROUGE-L
    grounding   support rate, unsupported-number rate, refusal rate
    operations  latency percentiles, token counts, cost per 1000 queries

Every function takes plain Python values, so it can score a local model, a
hosted API or a human-written answer identically. No dependencies beyond the
standard library and NumPy.

Run ``python llm_eval.py`` for worked examples with known answers.
"""

from __future__ import annotations

import math
import re
import string
import time
from collections import Counter


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

_ARTICLES = re.compile(r"\b(a|an|the)\b", re.UNICODE)


def normalize(text: str) -> str:
    """Lowercase, strip punctuation and articles -- the SQuAD convention."""
    text = text.lower()
    text = "".join(ch for ch in text if ch not in set(string.punctuation))
    text = _ARTICLES.sub(" ", text)
    return " ".join(text.split())


def tokens(text: str) -> list[str]:
    return normalize(text).split()


# ---------------------------------------------------------------------------
# Answer quality
# ---------------------------------------------------------------------------

def exact_match(pred: str, gold: str) -> float:
    """1.0 if the normalised strings are identical. Deliberately harsh."""
    return float(normalize(pred) == normalize(gold))


def token_f1(pred: str, gold: str) -> float:
    """Harmonic mean of token precision and recall (SQuAD-style partial credit)."""
    p, g = tokens(pred), tokens(gold)
    if not p or not g:
        return float(p == g)
    common = Counter(p) & Counter(g)
    overlap = sum(common.values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(p)
    recall = overlap / len(g)
    return 2 * precision * recall / (precision + recall)


def _lcs(a: list[str], b: list[str]) -> int:
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, start=1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def rouge_l(pred: str, gold: str) -> float:
    """Longest-common-subsequence F1 over tokens: order-sensitive overlap."""
    p, g = tokens(pred), tokens(gold)
    if not p or not g:
        return float(p == g)
    lcs = _lcs(p, g)
    if lcs == 0:
        return 0.0
    precision, recall = lcs / len(p), lcs / len(g)
    return 2 * precision * recall / (precision + recall)


# ---------------------------------------------------------------------------
# Retrieval quality
# ---------------------------------------------------------------------------

def recall_at_k(ranked_ids, relevant, k: int) -> float:
    """Fraction of the relevant documents that appear in the top k."""
    relevant = set(relevant)
    if not relevant:
        return 0.0
    return len(set(ranked_ids[:k]) & relevant) / len(relevant)


def precision_at_k(ranked_ids, relevant, k: int) -> float:
    relevant = set(relevant)
    if k == 0:
        return 0.0
    return len(set(ranked_ids[:k]) & relevant) / k


def mrr(ranked_ids, relevant) -> float:
    """Reciprocal rank of the first relevant document (0 if none retrieved)."""
    relevant = set(relevant)
    for i, doc in enumerate(ranked_ids, start=1):
        if doc in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked_ids, relevant, k: int) -> float:
    """Binary-relevance nDCG@k with the usual log2(i+1) discount."""
    relevant = set(relevant)
    dcg = sum(1.0 / math.log2(i + 1)
              for i, doc in enumerate(ranked_ids[:k], start=1) if doc in relevant)
    ideal = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(relevant), k) + 1))
    return dcg / ideal if ideal else 0.0


def retrieval_report(runs, k_values=(1, 3, 5)) -> dict:
    """``runs`` is a list of (ranked_ids, relevant_ids) pairs."""
    out = {}
    for k in k_values:
        out[f"recall@{k}"] = float(sum(recall_at_k(r, rel, k) for r, rel in runs) / len(runs))
        out[f"precision@{k}"] = float(sum(precision_at_k(r, rel, k) for r, rel in runs) / len(runs))
        out[f"ndcg@{k}"] = float(sum(ndcg_at_k(r, rel, k) for r, rel in runs) / len(runs))
    out["mrr"] = float(sum(mrr(r, rel) for r, rel in runs) / len(runs))
    return out


# ---------------------------------------------------------------------------
# Grounding, hallucination and refusal
# ---------------------------------------------------------------------------

_REFUSALS = (
    "i don't know", "i do not know", "not in the context", "cannot find",
    "can't find", "no information", "not mentioned", "unable to answer",
    "the context does not", "not provided", "unknown",
)

_NUMBER = re.compile(r"\d[\d,.]*")


def is_refusal(text: str) -> bool:
    t = text.lower()
    return any(r in t for r in _REFUSALS)


def refusal_rate(answers) -> float:
    if not answers:
        return 0.0
    return float(sum(is_refusal(a) for a in answers) / len(answers))


def support_rate(answer: str, context: str) -> float:
    """Fraction of answer content words that appear in the retrieved context.

    A crude but transparent grounding proxy: content words are normalised tokens
    that are not stopwords and longer than two characters. 1.0 means every
    content word was in the context; 0.4 means the answer is mostly ungrounded.
    """
    stop = {"the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
            "you", "your", "can", "will", "not", "but", "have", "has", "had", "any",
            "all", "out", "per", "into", "its", "their", "they", "there", "which",
            "what", "when", "where", "who", "how", "does", "did", "should", "must"}
    a = [t for t in tokens(answer) if len(t) > 2 and t not in stop]
    if not a:
        return 1.0
    ctx = set(tokens(context))
    return float(sum(t in ctx for t in a) / len(a))


def unsupported_numbers(answer: str, context: str) -> list[str]:
    """Numbers in the answer that do not occur in the context -- a hallucination flag."""
    ctx = set(_NUMBER.findall(context))
    return [n for n in _NUMBER.findall(answer) if n not in ctx]


def answer_report(pairs, k_context: str | None = None) -> dict:
    """``pairs`` is a list of (prediction, gold) tuples."""
    n = len(pairs)
    return {
        "n": n,
        "exact_match": sum(exact_match(p, g) for p, g in pairs) / n,
        "token_f1": sum(token_f1(p, g) for p, g in pairs) / n,
        "rouge_l": sum(rouge_l(p, g) for p, g in pairs) / n,
    }


# ---------------------------------------------------------------------------
# Agreement and operations
# ---------------------------------------------------------------------------

def cohen_kappa(a, b, labels=(0, 1)) -> float:
    """Agreement between two raters, corrected for chance."""
    n = len(a)
    if n == 0:
        return 0.0
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return 0.0 if pe == 1 else (po - pe) / (1 - pe)


def percentile(values, q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, max(0, int(round((q / 100) * (len(s) - 1)))))
    return float(s[idx])


def latency_report(seconds) -> dict:
    return {"n": len(seconds), "mean_s": float(np_mean(seconds)),
            "p50_s": percentile(seconds, 50), "p95_s": percentile(seconds, 95),
            "max_s": float(max(seconds)) if seconds else 0.0}


def np_mean(xs) -> float:
    return float(sum(xs) / len(xs)) if xs else 0.0


def cost_per_1000(prompt_tokens, completion_tokens, price_in, price_out) -> float:
    """Prices are per one million tokens, the usual published unit."""
    return (prompt_tokens * price_in + completion_tokens * price_out) / 1e6 * 1000


class Timer:
    """Context manager: ``with Timer() as t: ...`` then ``t.seconds``."""

    def __init__(self):
        self.seconds = 0.0

    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.seconds = time.perf_counter() - self._t0
        return False


# ---------------------------------------------------------------------------
# Demo with known answers
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 78)
    print("1. Answer metrics on hand-checked examples")
    print("=" * 78)
    cases = [
        ("08:00", "08:00"),
        ("8:00", "08:00"),
        ("The library opens at 08:00.", "08:00"),
        ("09:00", "08:00"),
        ("I don't know", "08:00"),
        ("12 items", "12"),
        ("students may borrow twelve items", "12"),
    ]
    print(f"{'prediction':38s} {'gold':8s} {'EM':>4} {'F1':>5} {'RL':>5}")
    for p, g in cases:
        print(f"{p:38s} {g:8s} {exact_match(p, g):4.0f} {token_f1(p, g):5.2f} "
              f"{rouge_l(p, g):5.2f}")

    print("\nNormalisation is what makes '8:00' and '08:00' differ:")
    print("  normalize('The library opens at 08:00.'):", repr(normalize("The library opens at 08:00.")))
    print("  normalize('08:00'):", repr(normalize("08:00")))

    print("\n" + "=" * 78)
    print("2. Retrieval metrics on three simulated rankings")
    print("=" * 78)
    runs = [
        (["hb-01", "hb-03", "hb-21"], ["hb-01"]),
        (["hb-03", "hb-01", "hb-21"], ["hb-01"]),
        (["hb-03", "hb-21", "hb-07"], ["hb-01"]),
    ]
    rep = retrieval_report(runs)
    for k, v in rep.items():
        print(f"  {k:12s} {v:.3f}")
    print("  first ranking finds the document at position 1, second at 2, third never.")

    print("\n" + "=" * 78)
    print("3. Grounding and hallucination flags")
    print("=" * 78)
    context = ("The Hartley Library is open from 08:00 to 23:00 Monday to Friday. "
               "Group study rooms can be booked seven days in advance.")
    answers = [
        "The library opens at 08:00 and closes at 23:00 on weekdays.",
        "The library opens at 07:00 and closes at midnight.",
        "The library is open 24 hours a day for all students.",
        "I don't know: the context does not say.",
    ]
    for a in answers:
        print(f"  support {support_rate(a, context):.2f}  refusal {is_refusal(a)!s:5s}  "
              f"unsupported numbers {unsupported_numbers(a, context)}  {a}")

    print("\n" + "=" * 78)
    print("4. Agreement between an LLM judge and human labels")
    print("=" * 78)
    human = [1, 1, 0, 0, 1, 0, 1, 1, 0, 0]
    judge_a = [1, 1, 0, 0, 1, 0, 0, 1, 0, 1]
    judge_b = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    print(f"  judge A: agreement {np_mean([a == b for a, b in zip(human, judge_a)]):.2f} "
          f"kappa {cohen_kappa(human, judge_a):.3f}")
    print(f"  judge B: agreement {np_mean([a == b for a, b in zip(human, judge_b)]):.2f} "
          f"kappa {cohen_kappa(human, judge_b):.3f}")
    print("  kappa near 0 means the judge is no better than chance on this sample.")

    print("\n" + "=" * 78)
    print("5. Latency and cost arithmetic")
    print("=" * 78)
    lat = [0.42, 0.51, 0.47, 1.30, 0.55, 0.49, 2.10, 0.58]
    print("  latency:", {k: round(v, 3) for k, v in latency_report(lat).items()})
    print("  cost per 1000 queries at 10 in / 2 out USD per million tokens:",
          round(cost_per_1000(10 * 1000, 2 * 1000, 0.5, 1.5), 4), "USD")
    print("  same, at 0.15/0.60 prices:",
          round(cost_per_1000(10 * 1000, 2 * 1000, 0.15, 0.60), 4), "USD")


if __name__ == "__main__":
    main()
