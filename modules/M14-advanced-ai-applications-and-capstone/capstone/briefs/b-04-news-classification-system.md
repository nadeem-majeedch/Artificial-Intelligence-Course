# B-04 — News Classification System

**Level** Beginner · **Time** 14 h capstone · **Prerequisites** M08, M06, M13

## Problem statement

Assign news articles to topic categories, report macro performance, and analyse how the classifier
behaves on articles from sources it was not trained on.

## Motivation

Text classifiers are easy to get to 90% accuracy and hard to trust: source-specific vocabulary
leaks into the labels, and a model trained on one outlet often fails on another. This project
makes the source-shift problem explicit.

## Objectives

1. Build a text pipeline (tokenise, vectorise, classify) with no leakage.
2. Beat a majority-class and a TF-IDF + logistic baseline.
3. Report macro F1 and per-class results.
4. Measure the performance drop when the test set comes from a different source.

## Scope

**In:** English articles, single-label topic classification, offline evaluation.
**Out:** fake-news detection, sentiment, multilingual, deployment.

## Required knowledge

M08 text preprocessing and evaluation, M06 metrics. You will need to learn subword tokenisation if
you use a transformer; TF-IDF is an acceptable final method if justified.

## Suggested architecture

```text
articles -> clean text -> TF-IDF (or tokeniser + encoder) -> linear or gradient-boosted model
         -> evaluate on (a) random split, (b) source-held-out split
         -> confusion matrix, per-class table, vocabulary inspection
```

## Dataset recommendations

- 20 Newsgroups (public, permissive) for the pipeline.
- AG News (CC BY-SA 4.0) if you want a larger set.
- For the source shift: split 20 Newsgroups by newsgroup hierarchy, or add a second corpus.

State the licence; do not scrape news sites.

## Suggested technologies

Python, scikit-learn. Optional: a small pretrained encoder if it is already cached locally.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | TF-IDF baseline, random-split macro F1 |
| M3 | improved model, source-held-out result, confusion matrix |
| M4 | leakage analysis, report |

## Evaluation metrics

Primary: macro F1 on the held-out split. Supporting: per-class F1, source-shift drop, top features
per class (for interpretability). Baseline: majority class, TF-IDF + logistic.

## Expected deliverables

Code, evaluation set, model card, report with the shift analysis.

## Challenges

1. **Vocabulary leakage.** Headers, bylines and formatting reveal the source. Inspect top features.
2. **Class imbalance.** Some topics dominate. Use macro metrics.
3. **Duplicate near-identical articles** across splits. Deduplicate before splitting.

## Possible extensions

- Compare TF-IDF against a frozen sentence encoder on the same split.
- Test whether removing the top 50 source-indicative terms changes the shift gap.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
