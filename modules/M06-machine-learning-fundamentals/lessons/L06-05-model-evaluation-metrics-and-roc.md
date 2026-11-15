# L06-05 — Model Evaluation: Metrics, Confusion Matrices and ROC

[← Previous: L06-04](L06-04-classification-with-logistic-regression.md) · [Module home](../README.md) · [Next: L06-06 →](L06-06-bias-variance-and-regularisation.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Reporting a Classifier Honestly](#4-the-procedure-reporting-a-classifier-honestly)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Python Implementation](#7-python-implementation)
- [8. Practical Applications](#8-practical-applications)
- [9. Common Mistakes](#9-common-mistakes)
- [10. Practical Exercises](#10-practical-exercises)
- [11. Self-Assessment](#11-self-assessment)
- [12. Key Terms](#12-key-terms)
- [13. Further Reading](#13-further-reading)
- [What to Do Next](#what-to-do-next)

> **Module M06** · Lesson 5 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-04

[Previous: L06-04](L06-04-classification-with-logistic-regression.md) · [Module overview](../README.md) · [Next: L06-06 →](L06-06-bias-variance-and-regularisation.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Build** a confusion matrix from predictions and read the four cells correctly.
2. **Compute** accuracy, precision, recall, specificity and F1 by hand, and say which one a
   given decision needs.
3. **Construct** an ROC curve, interpret AUC as a ranking probability, and explain when AUC is
   misleading.
4. **Use** the precision–recall curve and average precision for rare positives.
5. **Choose** a threshold from a cost matrix rather than from habit.
6. **Evaluate** a regression with MAE, RMSE and R² and choose the metric from the error cost.
7. **Report** uncertainty: cross-validation spread and bootstrap confidence intervals.
8. **Explain** a model's behaviour with coefficients, permutation importance and partial
   dependence, and state the limits of each.

## 2. Prerequisite Knowledge

Confusion matrix vocabulary, and the logistic model from L06-04. You should be able to compute a
conditional probability.

## 3. Conceptual Explanation

### 3.1 The four cells

|  | Predicted negative | Predicted positive |
| :--- | ---: | ---: |
| **Actual negative** | true negative (TN) | false positive (FP) |
| **Actual positive** | false negative (FN) | true positive (TP) |

Every metric below is a ratio of these four numbers. There are only four, so any metric that
seems to require a fifth is usually a weighted combination in disguise.

### 3.2 The metrics

$$
\text{accuracy} = \frac{TP+TN}{TP+TN+FP+FN}
\qquad
\text{precision} = \frac{TP}{TP+FP}
$$

$$
\text{recall (sensitivity)} = \frac{TP}{TP+FN}
\qquad
\text{specificity} = \frac{TN}{TN+FP}
$$

$$
F_1 = \frac{2\,\text{precision}\cdot\text{recall}}{\text{precision}+\text{recall}}
$$

- **Accuracy** answers "how often is the model right?" — and is dominated by the majority class.
- **Precision** answers "when it says positive, how often is it right?" — the metric of the
  person who acts on a positive (a blocked card, a flagged student).
- **Recall** answers "of the real positives, how many did it find?" — the metric of the person
  who bears the cost of a miss (a fraudulent charge, a missed diagnosis).
- **F1** is the harmonic mean: it is high only when both are high, and it treats them as equally
  important. If they are not equally important, F1 is the wrong summary.
- **Specificity** answers "of the real negatives, how many did it leave alone?" — the metric of
  the person who receives the false alarms.

Report the matrix, not just the ratio. The ratio hides which error you are making.

### 3.3 The base-rate trap, quantitatively

A screening test with 90% sensitivity and 90% specificity, applied where prevalence is 0.8%
(fraud, a rare disease), has

$$
\text{PPV} = \frac{0.9 \times 0.008}{0.9\times0.008 + 0.1\times0.992}
= \frac{0.0072}{0.0992} \approx 0.073.
$$

Only 7.3% of positive flags are real. The test is not bad; the base rate is low. This is why
fraud and anomaly problems report precision at a fixed alert budget, not accuracy.

### 3.4 ROC and AUC

Sweep the threshold from 1 to 0. At each threshold compute

$$
\text{TPR} = \text{recall}, \qquad \text{FPR} = \frac{FP}{FP+TN},
$$

and plot TPR against FPR. The area under that curve has a clean interpretation:

> AUC is the probability that a randomly chosen positive is scored higher than a randomly
> chosen negative.

Consequences:

- AUC is **threshold-free** and **prevalence-independent** — useful for comparing ranking
  quality across datasets with different positive rates.
- AUC does **not** tell you the precision at the operating point you will deploy. A model can
  have AUC 0.95 and useless precision at 1% prevalence.
- AUC rewards getting the easy negatives right. With 99.2% negatives, a model can look excellent
  while being useless on the positives you care about.
- AUC 0.5 is random ranking; below 0.5 means the score is inverted.

### 3.5 Precision–recall curves

For rare positives, plot precision against recall as the threshold moves. The area is **average
precision (AP)**. It focuses entirely on the positive class and the false positives you generate,
which is what an alert queue actually experiences.

Rule of thumb: report **both** ROC-AUC and AP when positives are under ~10%; report the confusion
matrix at the chosen threshold in every case.

### 3.6 Choosing a threshold from costs

Expected cost at threshold $t$:

$$
C(t) = c_{FP}\cdot FP(t) + c_{FN}\cdot FN(t).
$$

Pick the $t$ that minimises $C$. On the loan sweep, if a false approval costs 10 and a false
rejection costs 1, the optimum is far above 0.5; if the bank is desperate for volume, it is
below. There is no universal threshold, only a universal method for finding it.

### 3.7 Regression metrics

| Metric | Formula | Use when |
| :--- | :--- | :--- |
| MAE | $\frac{1}{n}\sum\lvert y-\hat{y}\rvert$ | all errors cost proportionally; robust to outliers |
| RMSE | $\sqrt{\frac{1}{n}\sum(y-\hat{y})^2}$ | large errors are disproportionately bad |
| R² | $1 - SS_{res}/SS_{tot}$ | comparing to the mean baseline; unitless |
| MAPE | $\frac{1}{n}\sum\lvert (y-\hat{y})/y\rvert$ | percentage error is meaningful; undefined at $y=0$ |

RMSE ≥ MAE always; the gap tells you how concentrated the errors are. On the student model,
RMSE 5.52 vs MAE 4.53: a few large misses.

### 3.8 Uncertainty on a score

A single test number is an estimate. Two tools:

- **Cross-validation spread**: five-fold loan accuracy `0.785 ± 0.019`. A competitor at 0.774 is
  inside one standard deviation — not clearly better.
- **Bootstrap interval**: resample the test rows with replacement 1,000 times and report the
  2.5th–97.5th percentile. On the loan test set, accuracy 0.784 with a 95% interval of
  [0.741, 0.826]. Any claim finer than that interval is noise.

### 3.9 Interpretability

- **Coefficients** (linear/logistic): direction and size per feature, conditional on the rest.
  Precise, but only for models that have them.
- **Tree feature importance**: impurity reduction, biased toward high-cardinality features.
- **Permutation importance**: shuffle one column, measure the drop in score. Model-agnostic,
  intuitive, and computed on validation data.
- **Partial dependence**: average prediction as one feature varies. Shows shape, assumes
  feature independence.

None of these is causal. "The model uses `distance_from_home`" is not "distance causes fraud".

## 4. The Procedure: Reporting a Classifier Honestly

1. Fix the test set before modelling; touch it once.
2. State the baseline: majority class and any existing rule.
3. Report the confusion matrix at the chosen threshold.
4. Report precision, recall and F1 **per class**, plus macro averages.
5. Report ROC-AUC and, if positives are rare, average precision.
6. Report a confidence interval for the headline metric.
7. Show the threshold sweep and justify the threshold from costs.
8. Describe the errors: which rows are wrong, and is there a pattern?
9. State the population and time window.
10. Do not report a metric you would not act on.

## 5. Worked Examples

### Example 1 — Loans, all metrics from one matrix

```text
[[234  28]
 [ 53  59]]
```

- Accuracy: $(234+59)/374 = 0.783$
- Precision (approved): $59/(59+28) = 0.678$
- Recall (approved): $59/(59+53) = 0.527$
- Specificity: $234/(234+28) = 0.893$
- F1: $2(0.678)(0.527)/(0.678+0.527) = 0.593$
- Majority baseline accuracy: $262/374 = 0.701$

The model beats the baseline by 8 points while missing nearly half of the approvable
applications. That is a product decision, and the report must say so.

### Example 2 — Same model, different threshold

```text
threshold  precision  recall    f1  flagged
     0.10      0.372   0.964 0.537      290
     0.20      0.459   0.857 0.598      209
     0.30      0.484   0.696 0.571      161
     0.40      0.556   0.580 0.568      117
     0.50      0.678   0.527 0.593       87
```

No model changed; only the decision did. AUC is constant across these rows. If your report has
one row, you have hidden the trade-off.

### Example 3 — Fraud: why accuracy is useless and AP is not

```text
fraud rate 0.0078 (39 of 5,000)
"predict normal" accuracy 0.992, recall 0
z-score > 3 flags 73, precision 0.438, recall 0.821
Mahalanobis top 25, precision 0.920, recall 0.590
Mahalanobis top 50, precision 0.680, recall 0.872
```

The best row is not the highest recall; it is the one that matches the review team's capacity.
Twenty-five alerts at 92% precision is a workable process. 932 IQR flags at 4% precision is an
inbox nobody will read.

## 6. Mathematical Formulation

Confusion matrix entries for labels $y\in\{0,1\}$:

$$
TP=\sum_i \mathbb{1}[y_i=1,\hat{y}_i=1],\quad
FP=\sum_i \mathbb{1}[y_i=0,\hat{y}_i=1],\quad
FN=\sum_i \mathbb{1}[y_i=1,\hat{y}_i=0],\quad
TN=\sum_i \mathbb{1}[y_i=0,\hat{y}_i=0].
$$

ROC-AUC as a ranking probability:

$$
\text{AUC} = \Pr\big(s(x^+) > s(x^-)\big) + \tfrac12\Pr\big(s(x^+) = s(x^-)\big).
$$

Average precision as a sum over thresholds:

$$
\text{AP} = \sum_k (R_k - R_{k-1})\,P_k.
$$

Bootstrap interval: draw $B$ resamples of size $n$ with replacement, compute $\hat\theta_b$, and
report the $\alpha/2$ and $1-\alpha/2$ quantiles.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import numpy as np
import datasets as ds
from prep import StandardScaler, train_test_split
from classifiers import LogisticRegressionGD
import evaluation as ev

frame = ds.loans()
cols = ["annual_income_k", "loan_amount_k", "credit_score",
        "employment_years", "debt_ratio", "default_history"]
X = frame[cols].fillna(frame[cols].median()).to_numpy()
y = frame["approved"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)
scaler = StandardScaler().fit(X_train)
model = LogisticRegressionGD(lr=0.5, epochs=800).fit(scaler.transform(X_train), y_train)
proba = model.predict_proba(scaler.transform(X_test))[:, 1]
pred = (proba >= 0.5).astype(int)

print(ev.confusion_matrix(y_test, pred))
print(ev.classification_report(y_test, pred).round(3).to_string(index=False))
print("accuracy", round(ev.accuracy(y_test, pred), 4))
print("ROC AUC", round(ev.roc_auc_score(y_test, proba), 4))
print("average precision", round(ev.average_precision(y_test, proba), 4))
print(ev.threshold_sweep(y_test, proba, [0.1, 0.2, 0.3, 0.4, 0.5]).round(3).to_string(index=False))
print("bootstrap:", {k: round(v, 3) for k, v in ev.bootstrap_ci(y_test, pred).items()})
```

```text
[[234  28]
 [ 53  59]]
 class  precision  recall    f1  support
     0      0.815   0.893 0.852      262
     1      0.678   0.527 0.593      112
 macro      0.747   0.710 0.723      374
accuracy 0.7834
ROC AUC 0.7976
average precision 0.6684
 threshold  precision  recall    f1  flagged
       0.1      0.372   0.964 0.537      290
       0.2      0.459   0.857 0.598      209
       0.3      0.484   0.696 0.571      161
       0.4      0.556   0.580 0.568      117
       0.5      0.678   0.527 0.593       87
bootstrap: {'mean': 0.784, 'low': 0.741, 'high': 0.826}
```

Regression metrics:

```python
import datasets as ds, numpy as np, linreg as lr
from prep import train_test_split

frame = ds.students()
cols = ["study_hours", "attendance_pct", "prior_grade", "sleep_hours"]
X = frame[cols].fillna(frame[cols].median()).to_numpy()
y = frame["final_score"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0)
model = lr.LinearRegression().fit(X_train, y_train)
print({k: round(v, 3) for k, v in lr.regression_report(y_test, model.predict(X_test), 4).items()})
```

```text
{'mse': 30.485, 'rmse': 5.521, 'mae': 4.532, 'r2': 0.54, 'adj_r2': 0.527}
```

### Permutation importance

```python
import numpy as np

def permutation_importance(model, X, y, names, seed=0):
    rng = np.random.default_rng(seed)
    base = model.score(X, y)
    out = {}
    for j, name in enumerate(names):
        Xp = X.copy()
        rng.shuffle(Xp[:, j])
        out[name] = round(base - model.score(Xp, y), 4)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))

# X_test, y_test and the fitted model from the loan example
print(permutation_importance(model, scaler.transform(X_test), y_test, cols))
```

```text
{'credit_score': 0.0695, 'annual_income_k': 0.0481, 'loan_amount_k': 0.0481,
 'debt_ratio': 0.0374, 'employment_years': 0.0294, 'default_history': 0.0107}
```

Shuffling one column at a time shows which features the fitted model actually relies on. It is
computed on held-out rows, so it reflects generalisation rather than memorisation. Credit score
costs the most accuracy when destroyed; `default_history` costs the least here even though its
coefficient is large, because it is rare — a reminder that coefficient size and practical
importance are different quantities.

## 8. Practical Applications

- **Credit decisions** — precision at a fixed approval rate, with the confusion matrix in the
  model documentation.
- **Fraud alerts** — precision at the review team's capacity (e.g. top 100 per day), plus recall
  at that budget.
- **Medical screening** — sensitivity chosen from the cost of a missed case, specificity from the
  cost of a follow-up test, prevalence-adjusted PPV quoted explicitly.
- **Churn** — expected-value framing: saved revenue × recall versus incentive cost × (1 −
  precision).

## 9. Common Mistakes

1. Quoting accuracy on a 1%-positive problem.
2. Comparing models by AUC when the deployment threshold is fixed and precision differs.
3. Reporting the best threshold found on the test set.
4. Forgetting that precision depends on prevalence.
5. Using F1 when the two errors have very different costs.
6. Reporting a metric without its interval.
7. Treating feature importance as causal explanation.

## 10. Practical Exercises

1. Compute all five classification metrics by hand from the loan matrix and check them in code.
2. Plot (or tabulate) the ROC curve points at thresholds 0.1–0.9 and verify the AUC by the
   trapezoid rule.
3. Compute the cost-optimal threshold for $c_{FP}=1, c_{FN}=10$ and for $c_{FP}=1, c_{FN}=1$.
4. On the fraud data, compute precision and recall at alert budgets 25, 50 and 100. Which budget
   would you defend to an operations manager?
5. Explain why an AP of 0.67 with AUC 0.80 is not a contradiction.

## 11. Self-Assessment

**Multiple choice**

1. Precision is TP divided by a) TP+FN. b) TP+FP. c) TN+FP. d) TP+TN.
2. AUC equals the probability that
   a) a positive is classified correctly. b) a random positive outranks a random negative.
   c) the model is calibrated. d) precision exceeds recall.
3. Lowering the threshold usually
   a) raises precision and lowers recall. b) raises recall and lowers precision.
   c) leaves both unchanged. d) changes AUC.
4. With 0.1% prevalence, a test with 99% sensitivity and 99% specificity has a PPV of about
   a) 99%. b) 50%. c) 9%. d) 1%.

**Short answer**

5. Why can a model with AUC 0.95 have useless precision in production?
6. What does a bootstrap confidence interval add to a single accuracy number?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **c** — $0.0099/(0.0099+0.00999)\approx 0.09$.
5. Because AUC is threshold-free and prevalence-independent; at 0.1% prevalence even a strong
   ranking produces mostly false positives among the flagged rows.
6. It quantifies sampling noise, so you can tell a real difference between models from fold or
   sample variation.

</details>

## 12. Key Terms

**Confusion matrix**, **accuracy**, **precision**, **recall**, **sensitivity**, **specificity**,
**F1**, **macro average**, **ROC curve**, **AUC**, **precision–recall curve**, **average
precision**, **threshold**, **base rate**, **PPV**, **calibration**, **bootstrap interval**,
**permutation importance**, **partial dependence**, **MAE**, **RMSE**, **R²**, **MAPE**.

## 13. Further Reading

- Saito, T. & Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC
  Plot When Evaluating Binary Classifiers on Imbalanced Datasets*. PLoS ONE.
- Davis, J. & Goadrich, M. (2006). *The Relationship Between Precision-Recall and ROC Curves*.
  ICML.
- scikit-learn user guide, *Model evaluation*. — The reference implementations of every metric
  here.

## What to Do Next

1. Run `python evaluation.py`.
2. Do exercises 2–4 and keep the threshold table for LAB-06-02.
3. Continue to [L06-06 — Bias, Variance and Regularisation](L06-06-bias-variance-and-regularisation.md).

---

**Navigation:** [← Previous: L06-04](L06-04-classification-with-logistic-regression.md) · [Module home](../README.md) · [Next: L06-06 →](L06-06-bias-variance-and-regularisation.md)
