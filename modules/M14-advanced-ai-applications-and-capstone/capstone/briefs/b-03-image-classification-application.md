# B-03 — Image Classification Application

**Level** Beginner · **Time** 14 h capstone · **Prerequisites** M09, M13 (L13-02)

## Problem statement

Classify images into a fixed set of categories and report, honestly, where the classifier fails
and what that failure would cost a user.

## Motivation

Image classifiers reach high accuracy on curated benchmarks and drop sharply on user photographs.
The gap between the benchmark and the deployment distribution is the subject of this project, not
an inconvenience to be hidden.

## Objectives

1. Build a training pipeline with a held-out set that mimics deployment conditions.
2. Beat a trivial baseline (majority class, or colour histogram + logistic).
3. Report per-class precision, recall and a confusion matrix.
4. Show at least three failures with the images and an explanation.

## Scope

**In:** single-label classification, one dataset plus your own test photos, offline evaluation.
**Out:** object detection, deployment, real-time inference, claims about safety-critical use.

## Required knowledge

M09 convolutional networks, M06 metrics. You will need transfer learning from a pretrained
backbone; the fallback is a small CNN trained from scratch, which is a valid comparison.

## Suggested architecture

```text
images -> resize/augment -> CNN or pretrained backbone (frozen, then fine-tuned)
       -> softmax -> evaluate on (a) benchmark split, (b) your own photos
       -> per-class table -> confusion matrix -> error gallery
```

## Dataset recommendations

- CIFAR-10 (MIT licence) or Fashion-MNIST (MIT) for the pipeline.
- Add 50–100 photos you take yourself, from the intended use setting, as the deployment set.
- Do not use datasets with unclear licensing or scraped personal images.

## Suggested technologies

PyTorch or scikit-learn; CPU is enough for 32×32 images. `torchvision` for transforms if
available.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | baseline accuracy, benchmark split |
| M3 | CNN result, per-class table, deployment-set result |
| M4 | error gallery, report |

## Evaluation metrics

Primary: macro F1 on the deployment set. Supporting: per-class recall, confusion matrix, benchmark
vs deployment gap. Baseline: majority class and colour-histogram logistic.

## Expected deliverables

Code, trained weights (or a training script), error gallery, model card, report.

## Challenges

1. **Domain gap.** Your photos differ from the benchmark in lighting and framing. That is the
   finding.
2. **Small deployment set.** 60 photos give wide intervals. Report them.
3. **Class confusion.** Visually similar classes (cat/dog, shirt/pullover). Show the pairs.

## Possible extensions

- Test-time augmentation and its effect on the gap.
- Confidence calibration: do low-confidence predictions correspond to errors?

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
