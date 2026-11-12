# I-08 — Recommendation System

**Level** Intermediate · **Time** 14 h capstone · **Prerequisites** M06, M08, M13

## Problem statement

Build a recommender for a catalogue of items and evaluate it with ranking metrics, including a
cold-start analysis and a coverage check.

## Motivation

Offline ranking metrics reward popularity and can hide a system that recommends the same 50 items
to everyone. Coverage, diversity and cold-start performance are the metrics that decide whether a
recommender is useful, and they are usually omitted.

## Scope

**In:** implicit-feedback recommendation on a public dataset, offline evaluation.
**Out:** online A/B testing, deployment, any use of personal data beyond the public dataset.

## Objectives

1. Build a baseline (most-popular) and a personalised model.
2. Evaluate with recall@k, NDCG@k and catalogue coverage.
3. Measure cold-start performance for items with few interactions.
4. Report the diversity of recommendation lists.

## Required knowledge

M06 metrics, matrix factorisation basics. You will need to learn ranking evaluation; the fallback
is precision@k with a popularity baseline.

## Suggested architecture

```text
interactions -> user-item matrix -> baseline: most popular
             -> model: item-item cosine or matrix factorisation (implicit ALS)
             -> evaluate: recall@10, NDCG@10, coverage, intra-list diversity
             -> cold-start slice: items with < 5 interactions
```

## Dataset recommendations

- MovieLens 100k/1M (group recommendation licence, research use — check terms) or
- A synthetic interaction log you generate with a known preference structure (fully controllable).

Do not use scraped personal data or a live platform's logs.

## Suggested technologies

Python, `numpy`/`scipy`, scikit-learn. No GPU.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | popularity baseline, recall@10 |
| M3 | personalised model, coverage and diversity |
| M4 | cold-start analysis, report |

## Evaluation metrics

Primary: recall@10. Supporting: NDCG@10, catalogue coverage, intra-list diversity, cold-start
recall. Baseline: most-popular. Split: leave-one-out per user, with a temporal variant.

## Expected deliverables

Code, evaluation harness, results table, model card, report.

## Challenges

1. **Popularity bias.** The baseline is strong; a model that only re-ranks popular items adds
   little. Report coverage.
2. **Leakage.** A user's future interactions must not enter training. Split by time.
3. **Sparse evaluation.** Few interactions per user means noisy metrics. Report intervals.

## Possible extensions

- Add a diversity re-ranker and measure the accuracy/coverage trade.
- Compare implicit ALS against item-item cosine on cold-start items only.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
