# PA-06 — A Leakage-Free Prediction Pipeline

| | |
| :--- | :--- |
| Assignment | 06 |
| Difficulty | Intermediate |
| Estimated time | 5 hours |
| Prerequisites | M06 (L06-02 … L06-10), P04 |
| Covers | splitting, leakage, preprocessing, model comparison, metric choice |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

The most common failure in applied ML is not a weak model; it is a pipeline that leaks. A model that
scores 0.98 in the notebook and 0.71 in production is usually not overfitting — it is measuring
information it will not have at prediction time. This assignment gives you a dataset with three
planted leaks and asks you to find them, then build the pipeline correctly.

## Problem scenario

`applications.csv` predicts whether an applicant will accept an offer. Columns include application
date, decision date, call duration, and a `status` field. Three of them leak the target. Your job is
to find them, justify each removal, and report the honest performance.

## Learning outcomes

1. Identify leakage by reasoning about when each feature becomes available.
2. Build preprocessing inside a pipeline so it is fitted per fold.
3. Compare at least three models with the same split and the same metric.
4. Report per-class performance and calibration, not only accuracy.

## Tasks

1. **Leak audit.** For every column, state when it becomes known. Classify each as available,
   post-outcome, or ambiguous; remove the leaks and record the score change.
2. **Split.** Choose a split appropriate to deployment (the data is time-ordered) and justify it.
3. **Pipeline.** Build a scikit-learn `Pipeline` with imputation, scaling and the model; no
   preprocessing outside the pipeline.
4. **Comparison.** Logistic regression, random forest, gradient boosting — same folds, macro F1 and
   PR-AUC.
5. **Calibration.** Plot or tabulate predicted vs observed rates in deciles.
6. **Error analysis.** Inspect the 20 highest-confidence errors and describe the pattern.
7. **Report.** A results table and a leakage section that a reviewer could verify.

## Constraints

- scikit-learn and pandas only.
- No test-set tuning; use cross-validation on training data.
- Report intervals or seed spread for the headline metric.

## Expected deliverables

`pipeline.py`, `leak_audit.md`, `results.md`, and a model card of one page.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Leak identification | 25% | all three found, with the timing argument |
| Pipeline correctness | 25% | preprocessing fitted inside folds |
| Model comparison | 20% | same split, same metric, three models |
| Calibration and errors | 20% | deciles and a concrete error pattern |
| Report | 10% | reproducible and honest about limits |

## Bonus challenges

- Show the score you would have reported if you had kept each leak, and by how much it inflates.
- Add probability calibration (isotonic or Platt) and report the Brier score change.

---

[Assessment index](../README.md) · [PA-05](pa-05-bayesian-reasoning.md) · [PA-07](pa-07-neural-networks.md)
