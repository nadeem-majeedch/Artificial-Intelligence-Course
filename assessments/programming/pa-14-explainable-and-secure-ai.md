# PA-14 — An Audit of a Model You Built

| | |
| :--- | :--- |
| Assignment | 14 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M13 (L13-01 … L13-06), PA-06 |
| Covers | fairness metrics, explanation fidelity, privacy and security testing, model cards |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

Auditing is not a separate activity from building; it is the evidence that the building was done
properly. This assignment takes a model you built earlier (or a provided one), attacks it on four
fronts, and produces the artefacts a reviewer asks for.

## Problem scenario

Use a binary classifier on tabular or image data. Produce a group metrics table, an evaluated
explanation, a membership-inference test and an adversarial test, then write the model card.

## Learning outcomes

1. Compute group metrics and state which fairness definition you chose.
2. Measure explanation fidelity and stability rather than displaying a plot.
3. Run membership inference and an evasion test, and interpret negative results.
4. Write a model card whose claims are all traceable.

## Tasks

1. **Fairness.** Selection rate, TPR, FPR and PPV per group; DP difference and DI ratio.
2. **Mitigation.** Try one mitigation; report the accuracy cost and the metric change.
3. **Explanation.** Global importance plus one local explanation with a fidelity measure.
4. **Privacy.** Membership-inference AUC with the confidence gap; state the result even if negative.
5. **Security.** FGSM at three ε values, or a prompt-injection test if the model is an LLM app.
6. **Model card.** One page, every number traceable to a script.

## Constraints

- Synthetic or licensed data only; no personal records.
- Attacks only against your own local model.
- Report "not measured" rather than estimating.

## Expected deliverables

`audit.py`, `model-card.md`, `risk-register.md` (5 rows), and `results.md`.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Group metrics | 25% | definition chosen, gaps with n |
| Mitigation analysis | 15% | cost reported with benefit |
| Explanation evaluation | 20% | fidelity or stability measured |
| Privacy/security | 25% | tests run, results interpreted honestly |
| Model card | 15% | traceable and falsifiable |

## Bonus challenges

- Add a counterfactual explanation and judge its actionability.
- Extend the risk register with residual scores and a release recommendation.

---

[Assessment index](../README.md) · [PA-13](pa-13-ai-agents.md) · [Analytical assignments](../analytical/README.md)
