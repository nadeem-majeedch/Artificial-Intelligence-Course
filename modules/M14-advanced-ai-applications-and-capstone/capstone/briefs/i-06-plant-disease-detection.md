# I-06 — Plant Disease Detection

**Level** Intermediate · **Time** 14 h capstone · **Prerequisites** M09, M14 (L14-04)

## Problem statement

Classify leaf images into healthy or diseased categories, and quantify the gap between curated
lab images and photos taken in field conditions.

## Motivation

Plant-disease classifiers reach 0.98 on curated datasets and fail in the field, where lighting,
occlusion and background differ. The lab-to-field gap is the research question; the classifier is
the instrument.

## Objectives

1. Train a classifier on a public leaf dataset.
2. Collect or source a small field-condition test set.
3. Measure the accuracy gap between the two, with intervals.
4. Identify which conditions cause the largest drop (lighting, background, occlusion).

## Scope

**In:** single-leaf classification, 3–10 classes, offline evaluation.
**Out:** detection in full-field images, deployment, treatment recommendations, agronomic claims.

## Required knowledge

M09 transfer learning, M06 metrics, L14-04 reproduction discipline.

## Suggested architecture

```text
leaf images -> augmentation (mild) -> pretrained backbone -> fine-tune
             -> evaluate on (a) dataset test split, (b) field-condition set
             -> stratified error analysis by condition -> abstention threshold
```

## Dataset recommendations

- PlantVillage (CC BY-SA 3.0) for training.
- Field photos: your own, or a licensed field dataset; 60–150 images is enough for a gap estimate.
- Never claim agronomic validity from a lab dataset.

## Suggested technologies

PyTorch, CPU-feasible at 128×128. Pretrained weights only if already cached or licensed.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | baseline on dataset split |
| M3 | fine-tuned model, field-set result, per-condition table |
| M4 | gap analysis, abstention policy, report |

## Evaluation metrics

Primary: macro F1 on the field set. Supporting: lab-set F1, gap with CI, per-condition accuracy,
abstention rate at a confidence threshold. Baseline: colour histogram + logistic.

## Expected deliverables

Code, error gallery grouped by condition, model card, report.

## Challenges

1. **Tiny field set.** 60 images give wide intervals. Report them; do not over-claim.
2. **Background leakage.** Lab images have uniform backgrounds; models learn them.
   Mitigation: test with background-replaced images.
3. **Novel classes.** A disease not in training will be forced into a known class.
   Mitigation: confidence-based abstention and an "unknown" analysis.

## Possible extensions

- Background randomisation as a mitigation, measured on the field set.
- Compare abstention policies by cost of a missed disease vs a false alarm.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
