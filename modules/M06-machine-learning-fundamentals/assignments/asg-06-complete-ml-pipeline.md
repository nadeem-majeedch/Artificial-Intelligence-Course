# ASG-06 — A Complete, Reproducible ML Pipeline with Report

| Module | M06 · Machine Learning Fundamentals and Algorithms |
| :--- | :--- |
| Effort | 4–6 hours |
| Type | Assignment, individual |
| Lessons covered | L06-01 to L06-10 |
| Deliverables | `pipeline.py`, `report.md` (≤ 1,500 words), `model-card.md`, `results.json` |

[← Module home](../README.md) · [Course home](../../../README.md)

## Why this assignment

The module's claim is that defending a model is harder than fitting one. This assignment is the
defence: one dataset, one pipeline, one report, and a results file that lets a marker reproduce
every number without reading your notebook history.

Choose **one** of the eight module datasets. If you want to use a real public dataset instead, it
must be the counterpart named in the relevant lab, and you must cite it and its licence.

## The brief

### 1. Problem framing (report §1)

State the decision the model supports, who acts on it, the label, when the label is observed, and
which features are available at prediction time. Name the cost of a false positive and a false
negative in the units of the problem (money, hours, students missed). Choose the metric from that
cost, before you fit anything.

### 2. Pipeline (`pipeline.py`)

- Loads data through `datasets.py` or a documented loader.
- Splits once, reproducibly, with stratification or time ordering as appropriate.
- Contains **all** preprocessing inside a `Pipeline`: imputation, encoding, scaling.
- Cross-validates on the training set; selects hyperparameters there.
- Fits once on train+validation; evaluates once on test.
- Writes `results.json` containing: dataset name and row count, seed, split sizes, config,
  CV mean/std per model, test metrics, confusion matrix, and the chosen threshold with its
  justification.
- Runs end to end with `python pipeline.py` and no manual steps.

### 3. Comparison (report §2)

At least three model families, compared on identical folds. A baseline (majority class or mean
predictor) must be in the table. Report mean ± std and the number of folds. State which model you
chose and why — including why not the one with the best mean if you rejected it.

### 4. Evaluation (report §3)

- Confusion matrix at the deployed threshold.
- Precision, recall and F1 per class; AUC and average precision where relevant.
- A threshold table with expected cost at three candidate thresholds, and your choice.
- A bootstrap 95% interval for the headline metric.
- An error analysis sliced by at least two features, with one named finding.

### 5. Model card (`model-card.md`)

One page: purpose, intended users, training data and population, features, metrics with the split
they were computed on, subgroup performance (or an explicit "not evaluated"), limitations, monitoring
plan, retraining trigger.

### 6. Reproducibility (report §4)

Record the seed, package versions, and how to run the pipeline. Re-run it from a clean state and
confirm the numbers match `results.json`. If they do not, fix the hidden state before submitting.

## Marking rubric

| Criterion | Weight | Full marks | Partial |
| :--- | ---: | :--- | :--- |
| Framing and metric choice | 15% | decision, costs and metric coherent and stated first | metric chosen but not tied to cost |
| Leakage-free pipeline | 25% | everything inside the pipeline, seeded, reproducible | one preprocessing step outside |
| Model comparison | 20% | three families, same folds, baseline, spread | two models or missing baseline |
| Evaluation and threshold | 20% | cost-based threshold, interval, confusion matrix, error slices | metrics without threshold reasoning |
| Model card and limitations | 10% | honest, specific, includes what is not evaluated | generic statements |
| Code quality | 10% | modular, documented, runs end to end | runs, but tangled |

A submission that reports a test score above 0.99 on any of these datasets without explaining it
will be treated as a suspected leak and marked on the audit, not the score.

## Constraints

- Maximum 1,500 words in `report.md`; tables and the model card do not count.
- No test-set tuning. Any threshold or hyperparameter chosen on test invalidates that section.
- Synthetic data must be labelled as synthetic wherever a result is quoted.
- Do not claim clinical, financial or security validity for any model built on module data.
- Standard library plus NumPy, pandas, Matplotlib, seaborn and scikit-learn. The module's own
  implementations are preferred for the models you report; scikit-learn may be used for comparison
  if you say so.

## Submission checklist

- [ ] `pipeline.py` runs from a clean checkout with the documented command.
- [ ] `results.json` matches the report's numbers.
- [ ] `report.md` ≤ 1,500 words, with all five sections.
- [ ] `model-card.md` complete, including limitations.
- [ ] Baseline present in the comparison table.
- [ ] Every random step seeded and the seed recorded.
- [ ] Data source and licence stated.

## Common ways this assignment loses marks

1. A scaler fitted before the split, then a paragraph claiming there is no leakage.
2. A comparison table where each model used a different split.
3. A single accuracy number for an 8%-positive problem.
4. A model card that lists only strengths.
5. A results file that cannot be reproduced because the seed is missing.
6. Error analysis that says "the model is good at easy cases" without a slice table.

## Feedback and resubmission

Marks are returned with the rubric row-by-row and one concrete improvement. A resubmission within
seven days is allowed for the pipeline and reproducibility rows only; the framing and evaluation
marks stand.
