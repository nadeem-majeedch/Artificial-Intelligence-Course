# A-11 — Medical Image Segmentation Prototype

**Level** Advanced · **Time** 14 h capstone · **Prerequisites** M09, M13, L14-04

## Problem statement

Segment a structure in a public medical imaging dataset and report Dice, boundary error and
failure cases — as a **research prototype**, not a clinical tool.

## Motivation

Segmentation is the canonical medical-imaging task, and the canonical overclaiming failure. This
project teaches the metrics properly and forces an explicit statement of what the prototype does
not establish. That statement is marked.

## Scope

**In:** one public dataset, one structure, offline evaluation, CPU or single GPU.
**Out:** clinical use, diagnosis, deployment, any claim of medical reliability.

## Objectives

1. Implement a U-Net-style segmentation model on a public dataset.
2. Report Dice and IoU per image, with an aggregate interval.
3. Analyse the three worst cases and identify the pattern.
4. State the validation a clinical claim would require.

## Required knowledge

M09 convolutions and segmentation, M06 metrics. You will need to learn Dice and boundary metrics;
the fallback is pixel accuracy, which is a poor metric and must be reported as such.

## Suggested architecture

```text
images + masks -> normalise -> U-Net (encoder/decoder, skip connections)
              -> evaluate: Dice, IoU, Hausdorff distance (if available)
              -> worst-case gallery -> limitations statement
```

## Dataset recommendations

- A public, licensed medical imaging set with masks — for example a retinal or dermoscopy dataset
  with an explicit research licence. Verify the licence yourself; several "public" medical sets
  have redistribution restrictions.
- Alternatively, a synthetic segmentation task (shapes on noisy backgrounds) with a known ground
  truth if licensing blocks you. State the substitution.

## Suggested technologies

PyTorch; 64×64 or 128×128 patches keep CPU training feasible. Do not download multi-gigabyte
datasets unless storage permits.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | data pipeline, trivial baseline (threshold or centre crop) |
| M3 | U-Net result, per-image Dice distribution |
| M4 | worst-case analysis, limitations, report |

## Evaluation metrics

Primary: mean Dice with 95% interval across images. Supporting: IoU, per-image distribution,
failure rate at Dice < 0.5. Baseline: Otsu threshold or centre prior.

## Expected deliverables

Code, predictions gallery, model card, report with an explicit non-clinical statement.

## Challenges

1. **Licensing.** Medical data often restricts redistribution. Check before you start.
2. **Small datasets.** 100 images means noisy Dice. Report the distribution, not just the mean.
3. **Metric gaming.** Dice rewards large structures; small lesions are missed. Report per-size
   buckets.

## Possible extensions

- Boundary loss and its effect on small structures.
- Test-time augmentation and its effect on the Dice distribution.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
