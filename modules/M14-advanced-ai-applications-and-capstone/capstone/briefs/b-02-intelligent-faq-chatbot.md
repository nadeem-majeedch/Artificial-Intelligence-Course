# B-02 — Intelligent FAQ Chatbot

**Level** Beginner · **Time** 14 h capstone · **Prerequisites** M08, M11 (retrieval), M13

## Problem statement

Answer questions about a fixed corpus (a university handbook, a product manual) by retrieving the
relevant passage and answering from it, refusing when the corpus does not contain the answer.

## Motivation

A FAQ bot fails in two ways that matter: it invents an answer, or it answers from an outdated
document. Both are measurable, and both are worse than "I don't know". The project is an exercise
in grounded answering and refusal calibration.

## Objectives

1. Build retrieval over at least 30 documents with a measurable recall@k.
2. Answer from retrieved evidence only, with citations.
3. Measure groundedness and refusal on an unanswerable set.
4. Report a failure taxonomy with at least five real examples.

## Scope

**In:** a fixed corpus, a 60-question evaluation set, offline evaluation.
**Out:** live chat integration, multi-turn dialogue state, any external API dependency.

## Required knowledge

M11 chunking and retrieval, M08 evaluation metrics. You will need to learn a dense retriever; the
fallback is BM25 alone, which is a legitimate baseline.

## Suggested architecture

```text
documents -> chunk (300 tokens, 50 overlap) -> index (BM25 + embeddings)
question -> retrieve top-k -> pack context with delimiters -> answer or refuse
         -> evaluate: recall@k, groundedness, refusal rate, hallucination count
```

## Dataset recommendations

- Your institution's public handbook (check licence), or
- The M11 Northfield corpus (CC0-1.0) if you want a known-good baseline, or
- Any CC-BY documentation set (e.g. a public project's docs).

Write 60 questions yourself: 40 answerable, 20 not. That set is the main artefact.

## Suggested technologies

Python, scikit-learn, `rank_bm25`, optionally `sentence-transformers` (Apache-2.0) if available.
A local small model or a template-based answerer is acceptable; if you use an API, keep the key in
an environment variable and never commit it.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | corpus, index, recall@5 for BM25 |
| M3 | grounded answering, evaluation on 60 questions |
| M4 | failure taxonomy, report |

## Evaluation metrics

Primary: grounded answer rate (supported by a cited passage). Supporting: recall@5, refusal
accuracy on unanswerable questions, citation correctness. Baseline: BM25 + extractive answer.

## Expected deliverables

Index, evaluation set, code, model card, report.

## Challenges

1. **Refusal calibration.** Too eager and it is useless; too lax and it hallucinates.
2. **Chunk boundaries.** Answers split across chunks. Mitigation: overlap, and measure it.
3. **Stale documents.** Version the corpus and note the date in every answer.

## Possible extensions

- Compare dense, lexical and hybrid retrieval on the same 60 questions.
- Add a "confidence" band and measure whether it correlates with correctness.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
