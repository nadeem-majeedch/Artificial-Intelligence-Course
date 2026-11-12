# PA-08 — Text Classification from TF-IDF to a Transformer

| | |
| :--- | :--- |
| Assignment | 08 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M08 (L08-01 … L08-06), M06 |
| Covers | tokenisation, TF-IDF, embeddings, fine-tuning, error analysis |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

A support team wants to route incoming messages to one of five queues. A TF-IDF baseline takes ten
minutes and gets most of the way there; a fine-tuned transformer takes longer and may not be worth
it. The assignment requires you to measure both and to justify the choice with numbers and an error
analysis, not with a preference.

## Problem scenario

`messages.csv` has 2,000 short texts with five labels, imbalanced (one class is 8% of the data).
Build three classifiers on the same split: majority class, TF-IDF + logistic regression, and a
pretrained encoder fine-tuned if available (otherwise a hashing-based neural bag-of-words).

## Learning outcomes

1. Build a text pipeline with a tokeniser appropriate to the model.
2. Compare lexical and contextual representations on the same split.
3. Report macro-F1 and per-class results under class imbalance.
4. Analyse errors by category and state the operational cost of each option.

## Tasks

1. **Baseline.** Majority class; report macro-F1 (it will be low — that is the point).
2. **TF-IDF.** Tune `min_df`, `ngram_range` on a validation split; report the chosen settings.
3. **Neural model.** Encoder fine-tuning or a neural bag-of-words; same split, same metric.
4. **Per-class table.** Precision, recall, F1 and support for all five classes, both models.
5. **Error analysis.** Fifty misclassified examples, grouped into at least four categories with
   counts and two verbatim examples each.
6. **Cost.** Training time, inference latency per 1,000 messages, model size on disk.
7. **Recommendation.** One paragraph choosing a model, with the numbers that justify it.

## Constraints

- No test-set tuning.
- Pretrained weights only if already available locally; otherwise state the substitution.
- No external API calls.

## Expected deliverables

`classify.py`, `results.md`, `errors.md`, and the trained model or a script that reproduces it.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Pipeline and baseline | 20% | correct split, baseline reported |
| Model comparison | 25% | same split and metric; tuning only on validation |
| Imbalance handling | 20% | macro and per-class metrics, not accuracy |
| Error analysis | 20% | four categories with counts and examples |
| Recommendation | 15% | justified by cost and accuracy together |

## Bonus challenges

- Add class weighting and report the precision/recall trade at the deployed threshold.
- Measure performance on messages with typos injected at 5% and 15% of tokens.

---

[Assessment index](../README.md) · [PA-07](pa-07-neural-networks.md) · [PA-09](pa-09-computer-vision.md)
