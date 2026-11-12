# I-07 — Traffic Sign Recognition

**Level** Intermediate · **Time** 14 h capstone · **Prerequisites** M09, M13 (L13-04)

## Problem statement

Classify traffic signs from images and measure robustness to blur, low light and small size —
the conditions that decide whether such a model is safe.

## Motivation

A sign classifier that is 99% accurate on a clean benchmark and 60% on a rainy dusk image is not a
99% system. Robustness is measurable by constructing the perturbations and testing them, which is
what this project does.

## Scope

**In:** classification of cropped signs, synthetic corruptions, offline evaluation.
**Out:** detection in video, real-time driving, any safety claim or deployment.

## Objectives

1. Train a classifier on a public sign dataset.
2. Build a corruption suite (blur, noise, low light, downscale, rotation).
3. Report accuracy per corruption and the worst case.
4. Explain which classes are most fragile and why.

## Required knowledge

M09, M13 adversarial robustness basics. You will need to learn corruption benchmarking (e.g.
mCE-style normalised error); the fallback is a simple percentage drop per corruption.

## Suggested architecture

```text
sign crops -> resize -> CNN/pretrained backbone
           -> evaluate on clean + 5 corruptions x 3 severities
           -> per-class, per-corruption table -> fragility analysis
```

## Dataset recommendations

- GTSRB (German Traffic Sign Recognition Benchmark; research licence — check terms before use) or
  a permissively licensed alternative such as a synthetic sign set you render.
- If licensing is unclear, render synthetic signs: a legitimate and fully controllable choice.

## Suggested technologies

PyTorch or scikit-learn on 32×32 crops; CPU sufficient.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | baseline, clean accuracy |
| M3 | corruption suite results |
| M4 | fragility analysis, report |

## Evaluation metrics

Primary: accuracy under the worst corruption. Supporting: clean accuracy, mean accuracy across
severities, per-class fragility rank. Baseline: logistic on raw pixels.

## Expected deliverables

Code, corruption suite, results table, model card, report.

## Challenges

1. **Licence.** GTSRB has research-use terms. If you cannot comply, switch to synthetic.
2. **Corruption realism.** Gaussian blur is not rain. Say what your corruptions do and do not
   represent.
3. **Severity calibration.** Define severities in measurable units, not "mild/medium/severe".

## Possible extensions

- Adversarial training or augmentation and its effect on corruption accuracy.
- Compare a small CNN against a pretrained backbone under corruption.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
