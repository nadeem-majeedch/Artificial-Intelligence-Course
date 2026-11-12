# I-05 — RAG University Document Assistant

**Level** Intermediate · **Time** 14 h capstone · **Prerequisites** M11, M13 (L13-03)

## Problem statement

Build a retrieval-augmented assistant over university regulations that answers with citations and
refuses when the regulations do not cover the question, and evaluate retrieval separately from
answering.

## Motivation

Policy questions have legal consequences and short documents that disagree with each other across
years. An assistant that cites the 2019 regulation when the 2024 one applies is worse than no
assistant. Retrieval quality is the binding constraint, and it is measurable independently.

## Objectives

1. Ingest at least 40 documents with version and effective-date metadata.
2. Compare lexical, dense and hybrid retrieval on a 50-question set.
3. Answer with citation; measure groundedness and citation correctness.
4. Handle version conflict: never cite a superseded document as current.

## Scope

**In:** a fixed corpus with versions, offline evaluation, single-turn questions.
**Out:** live student use, multi-turn dialogue, any personalised advice.

## Required knowledge

M11 RAG pipeline, M13 leakage and access control. You will need to learn embedding retrieval;
BM25 alone is the fallback baseline.

## Suggested architecture

```text
documents (+ version, effective_date) -> chunk by section -> index
question -> retrieve top-k within the current version -> rerank -> answer with section IDs
        -> evaluate: recall@k, citation precision, groundedness, refusal, version errors
```

## Dataset recommendations

- Your institution's public regulations (check licence), or
- The M11 Northfield handbook corpus (CC0-1.0), or
- A synthetic corpus you write with deliberate version conflicts.

Do not use real student records or non-public policy documents.

## Suggested technologies

Python, `rank_bm25`, `faiss` or scikit-learn, optional `sentence-transformers`. Template-based
answers are acceptable if the evaluation is rigorous.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | corpus with versions, recall@5 for BM25 |
| M3 | hybrid retrieval, answer + citation evaluation |
| M4 | version-conflict analysis, report |

## Evaluation metrics

Primary: answer correctness with correct citation. Supporting: recall@5, citation precision,
refusal accuracy on out-of-scope questions, version-error count. Baseline: BM25 + extractive span.

## Expected deliverables

Index, question set, code, model card, report.

## Challenges

1. **Version conflict.** Two documents state different rules. Mitigation: metadata filter before
   ranking, and a test case for it.
2. **Chunking legal text.** Clauses span sections. Mitigation: chunk by section, keep the heading.
3. **Refusal.** Out-of-scope questions invite invention. Mitigation: a 15-question negative set.

## Possible extensions

- Add a reranker and measure the recall/precision trade.
- Compare answer quality with and without the citation requirement.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
