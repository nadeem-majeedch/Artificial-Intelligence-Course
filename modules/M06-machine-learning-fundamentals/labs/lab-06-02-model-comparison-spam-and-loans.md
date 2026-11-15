# LAB-06-02 — Model Comparison Study: Email Spam and Loan Approval

> **Module M06** · Lab 2 of 4 · ~150 minutes · Level 300
> **Scenarios:** 3 (email spam detection) and 5 (bank loan approval)
> **Prerequisites:** L06-04 to L06-08 · **Pairs with:** NB-06-02

[Previous lab: LAB-06-01](lab-06-01-student-performance-prediction.md) · [Module overview](../README.md) · [Next lab: LAB-06-03 →](lab-06-03-customer-segmentation-and-attrition.md)

The point of this lab is not to find the best classifier. It is to run a comparison that would
survive review: same folds, same preprocessing, a baseline, an interval, a cost-aware threshold,
and an error analysis that says *where* the winner fails.

---

## Scenario 3 — Email spam detection

### Problem description

Classify an email as spam or legitimate from features you could compute from the raw message:
word count, number of links, uppercase words, exclamation marks, attachment, whether the sender is
known, hour sent, and whether the text contains "free". Compare naïve Bayes, k-NN and logistic
regression, then choose an operating point for a mail provider.

### Business context

A mail provider filters billions of messages. A false positive (legitimate mail in the spam folder)
is expensive: people miss job offers and invoices. A false negative is cheap: one more spam in the
inbox. The provider therefore wants high **precision**, and will accept lower recall. This is the
opposite of the usual "catch all spam" framing, and the lab asks you to defend the asymmetry.

### Dataset source and licence

- **In this lab:** `code/datasets.emails(n=1200, seed=0)` — synthetic features, 15.8% spam.
- **Real counterpart:** UCI *SMS Spam Collection* (Almeida, Hidalgo & Yamakami, 2011), CC BY 4.0.
  It contains 5,574 labelled SMS messages; you would extract the same features from the text
  column. Licence permits reuse with attribution.

### Dataset description

1,200 rows, 9 columns, no missing values.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| word_count | int | words in the message |
| num_links | int | hyperlinks |
| uppercase_words | int | all-caps tokens |
| exclamation_marks | int | "!" count |
| has_attachment | int | 0/1 |
| sender_known | int | 0/1 |
| hour_sent | int | 0–23 |
| contains_free | int | 0/1 |
| is_spam | int | target, 15.8% positive |

The features are correlated — spam has more links *and* more uppercase words *and* more
exclamations — which is exactly the situation where naïve Bayes' independence assumption is
wrong.

### Learning objectives

- Compare three model families on identical folds and splits.
- Explain why training time and prediction time differ so much for k-NN.
- Show the effect of feature scaling on k-NN with a measured number.
- Choose a threshold from an explicit cost asymmetry.
- Explain why naïve Bayes can rank well and still be badly calibrated.

### Tasks

1. Split 75/25, stratified, `seed=0`. Scale inside a pipeline.
2. Fit Gaussian NB, k-NN (k = 1, 5, 15, 35) and logistic regression. Report accuracy, precision,
   recall, F1 and AUC for each.
3. Report the majority-class baseline accuracy (≈ 0.84). State what it tells you about accuracy as
   a metric here.
4. Repeat the k-NN run **without scaling** at k = 5. Report the change and explain which feature
   dominates the distance.
5. Time `fit` and `predict` for k-NN and logistic regression on the same data. Report the ratio and
   interpret it.
6. Plot or tabulate the precision–recall trade-off for the best model over thresholds 0.1–0.9.
7. Choose a threshold for the mail provider if a false positive costs 20 and a false negative
   costs 1. Report the resulting precision, recall and number of flagged emails.
8. Compute the naive Bayes train and test accuracy. Does the gap suggest variance or bias?
9. Write a 150-word recommendation: which model, which threshold, which metric, and what would
   make you change your mind.

### Expected results

```text
GaussianNB  accuracy 0.970  precision 0.855  recall 0.979  AUC 0.994
kNN k=5     accuracy 0.950  precision 0.923  recall 0.750  AUC 0.963
logistic    accuracy 0.983  precision 0.939  recall 0.958  AUC 0.998
majority baseline accuracy ≈ 0.84
```

- Without scaling, k-NN accuracy falls noticeably (the `word_count` column dominates distances).
- k-NN prediction is hundreds of times slower than logistic prediction on the same rows.
- A cost ratio of 20:1 pushes the threshold well above 0.5, raising precision at the cost of
  recall.

### Evaluation metrics

Primary: **precision at the chosen threshold** (the user experience cost), with recall, F1 and
AUC as secondary. Also report the confusion matrix and the number of flagged emails per 1,000.

### Deliverables

- A comparison table: model, accuracy, precision, recall, F1, AUC, fit time, predict time.
- The scaling experiment, with numbers.
- The threshold table and a cost-based recommendation.
- The 150-word recommendation.

### Extension challenges

1. Implement multinomial NB on binned word counts and compare with Gaussian NB.
2. Calibrate the best model with isotonic regression (or a reliability plot) and recompute the
   expected cost at the chosen threshold.
3. Add a synthetic "sender reputation" feature and measure whether it displaces `sender_known`.
4. Run a 5-fold stratified CV comparison of the three models and report whether the ranking is
   stable across folds.

---

## Scenario 5 — Bank loan approval

### Problem description

Predict whether a loan application will be approved from income, amount, credit score, employment
history, debt ratio, default history and purpose. The positive rate is 30%, so accuracy is a trap
and the approval class is the one the bank cares about.

### Business context

A bank uses the model to route applications: high scores go to fast-track, low scores to manual
review. Fast-tracking a bad application is costly (default risk); manually reviewing a good one
costs analyst time. The bank wants a threshold with a stated precision, and it needs a model whose
coefficients it can defend to a regulator.

### Dataset source and licence

- **In this lab:** `code/datasets.loans(n=1500, seed=0)` — synthetic, 30% approved, 3% missing
  credit score.
- **Real counterpart:** UCI *Statlog (German Credit Data)* (Hofmann, 1994), CC BY 4.0. It has 1,000
  applications with a good/bad credit label; the mapping from "good credit" to "approved" is a
  modelling decision you must state.
- Note: the German Credit dataset contains a documented age-related attribute. Any use must
  discuss fairness; the module's M13 covers this properly.

### Dataset description

1,500 rows, 8 columns.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| annual_income_k | float | thousands per year, 8–120 |
| loan_amount_k | float | thousands, 1–90 |
| credit_score | float | 350–850, **3% missing** |
| employment_years | float | 0–40 |
| debt_ratio | float | 0.01–0.95 |
| default_history | int | 0/1 |
| purpose | categorical | car/business/education/home/other |
| approved | int | target, 30% positive |

### Learning objectives

- Build a logistic scorecard and interpret coefficients as odds multipliers.
- Quantify the cost of class imbalance with and without class weights.
- Choose a threshold from a cost matrix and show the resulting confusion matrix.
- Demonstrate that an unlimited-depth tree memorises (train 1.000) and generalises worse.
- Report a model comparison on the same folds with a spread, not a single number.

### Tasks

1. Split 75/25 stratified. Impute the missing credit scores inside the pipeline.
2. Fit logistic regression on standardised numeric features. Report coefficients as odds
   multipliers and the test confusion matrix.
3. Report accuracy, precision, recall, F1 and AUC for the approval class. Compare with the
   majority baseline (0.701).
4. Fit with `class_weight="balanced"`. Report the precision/recall change and explain the trade.
5. Fit a decision tree at depth 5 and an unlimited tree. Report train and test accuracy and AUC.
   Explain the difference in one paragraph.
6. Fit a random forest and gradient boosting. Compare all models on 5-fold stratified CV
   (mean ± std).
7. Sweep the threshold from 0.1 to 0.5. Produce the table and choose the threshold for
   $c_{FP} = 1$, $c_{FN} = 5$.
8. Add one-hot `purpose`. Does AUC improve beyond the CV spread?
9. Error analysis: slice the test errors by `default_history` and by `credit_score` quartile.
   Where is recall worst?
10. Write a 200-word model card section covering purpose, population, metrics, threshold and
    limitations.

### Expected results

```text
logistic      train 0.784  test 0.783  AUC 0.798
tree depth 5  train 0.801  test 0.717  AUC 0.696
tree unlimited train 1.000 test 0.679  AUC 0.597
forest 100    train 0.834  test 0.762  AUC 0.802
boosting 100  train 0.825  test 0.762  AUC 0.790
```

- Logistic coefficients (standardised): credit score +0.82, income +0.69, employment +0.36,
  debt ratio −0.47, default history −0.55, loan amount −0.59.
- Recall for approved applications is about 0.53 at threshold 0.5 — a real product limitation.
- The balanced model raises recall and lowers precision; the accuracy may *fall*.
- 5-fold CV: logistic ≈ 0.785 ± 0.019, tree depth 4 ≈ 0.737 ± 0.024, forest ≈ 0.774 ± 0.017.

### Evaluation metrics

**Recall for the approved class at a stated precision**, plus AUC and average precision for
ranking quality. Accuracy is reported only next to the majority baseline. Every comparison uses
the same folds and reports mean ± std.

### Deliverables

- The comparison table with CV mean/std for each model.
- The threshold/cost table with the chosen operating point marked.
- A confusion matrix at that point.
- The error-analysis slices and a one-sentence finding.
- The model-card section.

### Extension challenges

1. Add an interaction between income and loan amount and test whether it survives CV.
2. Replace missing credit scores with a model-based imputation and compare test AUC.
3. Implement a simple stacking ensemble (logistic + forest + SVM) with out-of-fold predictions and
   compare with the best single model.
4. Remove `default_history` and measure the AUC change. Is the model still defensible without it?
5. Simulate a 5% shift in the income distribution and recompute precision at the fixed threshold.
   What does that tell you about monitoring?

---

## Shared requirements

- **One split, one set of folds** for every model in the comparison. Reusing a different split per
  model invalidates the comparison.
- **Baseline first.** Majority class for both scenarios.
- **No test-set threshold tuning.** Choose the threshold on validation or CV predictions, then
  apply it to the test set once.
- **Report the number of flagged cases**, not just the ratio.
- **Every claim needs a number from your run.**

## Evaluation criteria

| Criterion | Weight | What earns full marks |
| :--- | ---: | :--- |
| Comparison design | 30% | identical folds, baselines, intervals, no leakage |
| Metric and threshold reasoning | 25% | cost-aware, prevalence-aware, clearly justified |
| Interpretation of models | 20% | coefficients and errors explained, not just printed |
| Error analysis | 15% | slices that reveal a real pattern |
| Communication | 10% | tables with units, honest limitations |

## Hints

- `evaluation.cross_val_score` takes a **factory**, not a fitted model, so each fold is fresh.
- `evaluation.threshold_sweep` returns the full table; compute expected cost from it directly.
- `Pipeline` keeps imputation and scaling inside the fold — use it for every model that needs
  scaling.
- If the unlimited tree shows train 1.000, that is the expected result, not a bug.

## Reflection

1. Which scenario changed your preferred model once you looked at the cost-weighted metric?
2. Why is "the forest has the best AUC" not enough to choose the forest?
3. What would you need to know about the bank's review capacity to set the threshold?

## Time budget

| Task | Time |
| :--- | ---: |
| Scenario 3, tasks 1–6 | 55 min |
| Scenario 3, tasks 7–9 | 25 min |
| Scenario 5, tasks 1–6 | 50 min |
| Scenario 5, tasks 7–10 | 30 min |
| Write-up | 20 min |

Next: [LAB-06-03 — Customer Segmentation and Employee Attrition](lab-06-03-customer-segmentation-and-attrition.md).

## Starter material

The guided notebook [`nb-06-02-regression-and-classification-workbench.ipynb`](../notebooks/nb-06-02-regression-and-classification-workbench.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
