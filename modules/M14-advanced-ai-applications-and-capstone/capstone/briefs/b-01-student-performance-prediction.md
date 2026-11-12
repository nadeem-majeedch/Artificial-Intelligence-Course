# B-01 — Student Performance Prediction

**Level** Beginner · **Time** 14 h capstone · **Prerequisites** M06, M13 (L13-01)

## Problem statement

Build a model that flags students at risk of failing a module early enough for an advisor to
intervene, and report which students it fails to flag.

## Motivation

Advisors learn about struggling students at the exam. Engagement data — attendance, submissions,
forum activity — is available weeks earlier. The value is not the prediction but the intervention
it enables, and the harm is a false negative that removes support from someone who needed it.

## Objectives

1. Build a leakage-free pipeline over one term of engagement data.
2. Beat a logistic baseline on recall at fixed precision.
3. Report per-group metrics, including at least one group defined by prior attainment.
4. State the intervention the flag would trigger and its cost.

## Scope

**In:** binary at-risk classification at week 6; one institution; one module.
**Out:** deployment, automated messaging, grade prediction, demographic attributes as features.

## Required knowledge

M06 pipeline discipline, M13 fairness metrics. You will need to learn survival-style temporal
validation; the fallback is a simple week-6 cutoff.

## Suggested architecture

```text
LMS logs -> weekly aggregates -> feature table (per student-week)
        -> split by cohort (train: earlier years, test: latest)
        -> logistic baseline -> gradient boosting -> threshold chosen for precision 0.5
        -> per-group table -> error analysis
```

## Dataset recommendations

- Synthetic: generate engagement trajectories with a known at-risk subgroup (`rai_data.py` in M13
  is a starting point).
- Licensed: your institution's anonymised export, only with written approval; do not redistribute.
- Open alternative: OULAD (Open University Learning Analytics, CC-BY 4.0).

State the licence. If you use OULAD, note that its demographics are synthetic-derived and its
cohorts are not yours.

## Suggested technologies

Python, pandas, scikit-learn. No GPU. Keep preprocessing in a script, not a notebook.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | feature table, cohort split, baseline recall/precision |
| M3 | model, threshold curve, per-group table |
| M4 | report with intervention cost and limitations |

## Evaluation metrics

Primary: recall at precision 0.50. Supporting: PR-AUC, calibration by group, false-negative count
per group. Baseline: logistic on attendance only. Uncertainty: bootstrap CI over the test cohort.

## Expected deliverables

Pipeline, model card, 6-page report, five-slide defence.

## Challenges

1. **Feedback loop.** If advisors act on flags, later cohorts are affected by earlier predictions.
   Mitigation: use only pre-intervention data.
2. **Missingness is informative.** Students who disengage stop generating rows.
   Mitigation: model missingness explicitly and report its effect.
3. **Class imbalance.** Failing students are a minority. Mitigation: PR metrics, not accuracy.

## Possible extensions

- Cost-sensitive thresholds using the advisor's time budget.
- Compare week-6 against week-10 prediction to quantify the value of earliness.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
