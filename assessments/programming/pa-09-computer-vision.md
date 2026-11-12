# PA-09 — Vision Pipeline with a Robustness Study

| | |
| :--- | :--- |
| Assignment | 09 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M09 (L09-01 … L09-06), PA-07 |
| Covers | convolution, transfer learning, augmentation, per-class evaluation, corruption testing |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

A classifier that scores 0.97 on a clean benchmark and 0.61 on phone photos is not a 0.97 system. The
assignment asks you to build the pipeline, then to attack your own model with the conditions it will
meet in use, and to report the gap rather than the headline.

## Problem scenario

Classify 10 classes of small images. You have a clean training set and a small "field" test set of
60 images you assemble yourself (or corrupt synthetically). Deliver a model and a robustness report.

## Learning outcomes

1. Train a CNN or fine-tune a backbone on a small dataset.
2. Apply augmentation deliberately and measure its effect.
3. Evaluate under corruption and report the per-class damage.
4. Distinguish a robustness claim from an accuracy claim.

## Tasks

1. **Baseline.** Logistic regression on raw pixels; macro-F1 on both test sets.
2. **Model.** CNN or fine-tuned backbone; same split; augmentation on/off.
3. **Corruptions.** Blur, noise, low light, downscale, rotation at three severities each.
4. **Table.** Clean vs field vs worst corruption, per class.
5. **Error gallery.** Ten failures grouped by cause.
6. **Verdict.** State what the model is and is not robust to, with numbers.

## Constraints

- CPU-feasible at 32×32 or 64×64; no external APIs.
- Same evaluation set for every variant.
- Report intervals or state that n is too small to separate variants.

## Expected deliverables

`train.py`, `corrupt.py`, `results.md`, error gallery, one-page model card.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Pipeline | 20% | correct split, baseline, reproducibility |
| Model and augmentation | 20% | measured effect, not asserted |
| Corruption study | 30% | severities defined, per-class results |
| Error analysis | 15% | causes grouped, examples shown |
| Claim discipline | 15% | robustness claims bounded by evidence |

## Bonus challenges

- Add corruption training and report the clean-accuracy cost.
- Compare confidence on clean vs corrupted inputs and test whether it is a usable abstention signal.

---

[Assessment index](../README.md) · [PA-08](pa-08-nlp.md) · [PA-10](pa-10-reinforcement-learning.md)
