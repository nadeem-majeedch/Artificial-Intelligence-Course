# L06-04 — Classification with Logistic Regression

[← Previous: ? Lesson](L06-03-linear-regression-from-first-principles.md) · [Module home](../README.md) · [Next: ? Lesson →](L06-05-model-evaluation-metrics-and-roc.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: A Defensible Logistic Model](#4-the-procedure-a-defensible-logistic-model)
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

> **Module M06** · Lesson 4 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-03 (linear models), P03 (probability, odds)

[Previous: L06-03](L06-03-linear-regression-from-first-principles.md) · [Module overview](../README.md) · [Next: L06-05 →](L06-05-model-evaluation-metrics-and-roc.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** why fitting a straight line to a 0/1 target is the wrong model, not merely an
   inaccurate one.
2. **Derive** the logistic model from the log-odds and interpret its coefficients as odds
   ratios.
3. **Fit** logistic regression by gradient descent on binary cross-entropy, and check the
   gradient numerically.
4. **Separate** the model's score from the decision threshold, and choose a threshold from costs.
5. **Handle** class imbalance with class weights and explain the precision–recall trade it buys.
6. **Report** a classifier with per-class precision and recall rather than accuracy alone.

## 2. Prerequisite Knowledge

You need linear regression (L06-03), the sigmoid shape, conditional probability, and the idea of
a likelihood. Odds are $p/(1-p)$; the log-odds are $\log(p/(1-p))$, which maps $(0,1)$ onto the
whole real line.

## 3. Conceptual Explanation

### 3.1 Why not linear regression?

Three problems, in increasing order of seriousness:

1. **Range.** $w^\top x + b$ can be −4 or 7. A probability must lie in $[0,1]$.
2. **Loss.** Squared error on a 0/1 target punishes a confident correct prediction and a
   confident wrong one symmetrically in probability space, and it is dominated by points far
   from the boundary.
3. **Shape.** The relationship between a risk score and the probability of the event is usually
   S-shaped, not linear: doubling a small risk matters more than doubling a large one.

### 3.2 The model

Logistic regression models the **log-odds** as a linear function:

$$
\log\frac{p}{1-p} = \mathbf{w}^\top\mathbf{x} + b
\quad\Longrightarrow\quad
p(y=1\mid\mathbf{x}) = \sigma(\mathbf{w}^\top\mathbf{x} + b),
\qquad
\sigma(z) = \frac{1}{1+e^{-z}}.
$$

The decision boundary $p = 0.5$ is the hyperplane $\mathbf{w}^\top\mathbf{x} + b = 0$. So the
model is a **linear classifier** with a probabilistic output — the boundary is linear, the score
is not.

### 3.3 Interpreting coefficients

A one-unit increase in $x_j$ adds $w_j$ to the log-odds, i.e. multiplies the odds by
$e^{w_j}$. On standardised features, a coefficient of 0.82 means a one-standard-deviation
increase multiplies the odds of approval by $e^{0.82}\approx 2.27$.

On the loan data (standardised features):

| Feature | Coefficient | Odds multiplier |
| :--- | ---: | ---: |
| credit_score | +0.820 | 2.27 |
| annual_income_k | +0.691 | 2.00 |
| employment_years | +0.358 | 1.43 |
| debt_ratio | −0.470 | 0.63 |
| default_history | −0.551 | 0.58 |
| loan_amount_k | −0.586 | 0.56 |

The signs are what a credit analyst would expect, which is a sanity check, not evidence of
causality. The magnitudes are conditional on the other features.

### 3.4 Fitting: maximum likelihood is cross-entropy

For $n$ independent rows, the likelihood is $\prod_i p_i^{y_i}(1-p_i)^{1-y_i}$. Maximising it is
the same as minimising the negative log-likelihood:

$$
\mathcal{L}(\mathbf{w}, b) = -\frac{1}{n}\sum_{i=1}^{n}\Big[y_i\log p_i + (1-y_i)\log(1-p_i)\Big].
$$

This is **binary cross-entropy**, and it is convex in the parameters. Its gradient is beautifully
simple:

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{w}} = \frac{1}{n}\mathbf{X}^\top(\mathbf{p} - \mathbf{y}),
\qquad
\frac{\partial \mathcal{L}}{\partial b} = \frac{1}{n}\sum_i (p_i - y_i).
$$

The same form as linear regression's gradient, with $p$ in place of $\hat{y}$. That is not a
coincidence: both are generalised linear models with a canonical link.

There is no closed form (the equations are transcendental), so we iterate. Newton's method
(IRLS) converges in a handful of steps; gradient descent needs a few hundred epochs but is
easier to read, which is why `classifiers.py` uses it.

### 3.5 Score, threshold, decision

The model outputs a probability. The *decision* applies a threshold:

```text
score 0.31 → threshold 0.50 → predict "rejected"
score 0.31 → threshold 0.25 → predict "approved"
```

These are different products. The first might be right for a conservative lender; the second for
one maximising approvals. A threshold chosen by habit (0.5) rather than by cost is a silent
policy decision.

### 3.6 Class imbalance

With 16% attrition, a model can reach 84% accuracy by predicting "nobody leaves". The fix is not
to lie about accuracy; it is either to reweight the classes, resample, or move the threshold.
Reweighting multiplies each class's loss contribution by $n/(2n_c)$:

```text
attrition, no class weights : accuracy 0.843  precision 0.538  recall 0.125
attrition, balanced weights : accuracy 0.680  precision 0.306  recall 0.786
```

The balanced model catches 79% of leavers instead of 13%, at the cost of flagging many who
would have stayed. Whether that trade is good depends on the cost of an unnecessary retention
conversation versus the cost of losing an employee — a business question, not a modelling one.

### 3.7 Regularisation

Add $\lambda\lVert\mathbf{w}\rVert_2^2$ to the loss and large coefficients become expensive.
This is exactly ridge regression applied to the log-loss, and it is the default in most
libraries (`C = 1/λ` in scikit-learn). It matters most when features are many or collinear.

## 4. The Procedure: A Defensible Logistic Model

1. Split, stratify on the label.
2. Impute and scale inside a pipeline (L06-02).
3. Fit with cross-validation on the training set; record the CV log-loss or AUC.
4. Inspect coefficients for sign and magnitude sanity.
5. Choose a threshold from the cost matrix — or report the full sweep.
6. Report per-class precision, recall, F1, AUC and the confusion matrix.
7. Check calibration: do predicted 0.2s happen about 20% of the time?
8. Test on the held-out set once; state the baseline you beat.

## 5. Worked Examples

### Example 1 — Loans, end to end

```text
logistic train 0.784 test 0.783 AUC 0.798
confusion matrix (rows actual, cols predicted)
[[234  28]
 [ 53  59]]
class  precision  recall    f1  support
0      0.815      0.893     0.852   262
1      0.678      0.527     0.593   112
accuracy 0.783   average precision 0.668
```

Reading it: of 112 approved applications, 59 were caught (recall 0.53) and 53 were rejected by
the model. Of 87 flagged approvals, 59 were real (precision 0.68). Accuracy 0.783 beats the
majority baseline of 0.701, but only just; the AUC of 0.798 shows the ranking is more useful
than the 0.5 threshold suggests.

### Example 2 — Choosing a threshold

```text
threshold  precision  recall    f1  flagged
     0.10      0.372   0.964 0.537      290
     0.20      0.459   0.857 0.598      209
     0.30      0.484   0.696 0.571      161
     0.40      0.556   0.580 0.568      117
     0.50      0.678   0.527 0.593       87
```

F1 peaks at 0.20 (0.598), not 0.50. If the bank's cost of a missed good applicant is three times
the cost of reviewing a bad one, 0.20 is defensible; if a wrong approval costs a default, 0.50
or higher is. The table, not the default, is the deliverable.

### Example 3 — Reading a coefficient in odds

Credit score is standardised, coefficient 0.820. A 50-point increase in raw score corresponds
to roughly 0.67 standard deviations here, so the odds multiply by
$e^{0.82\times0.67} \approx 1.73$ — a 73% increase in the odds of approval, holding the rest
fixed.

## 6. Mathematical Formulation

**Sigmoid and logit** are inverses:

$$
\sigma(z) = \frac{1}{1+e^{-z}}, \qquad \text{logit}(p) = \log\frac{p}{1-p}, \qquad \sigma(\text{logit}(p)) = p.
$$

**Cross-entropy** for one row: $-y\log p - (1-y)\log(1-p)$.

**Gradient descent update** with learning rate $\eta$ and L2 strength $\lambda$:

$$
\mathbf{w} \leftarrow \mathbf{w} - \eta\Big[\tfrac{1}{n}\mathbf{X}^\top(\mathbf{p}-\mathbf{y}) + \lambda\mathbf{w}\Big],
\qquad
b \leftarrow b - \eta\,\tfrac{1}{n}\textstyle\sum_i(p_i-y_i).
$$

**Odds ratio** for coefficient $w_j$: $e^{w_j}$.

**Class-weighted loss**: replace each term by $c_{y_i}$ times the term, with
$c_1 = n/(2n_1)$ and $c_0 = n/(2n_0)$ for balanced weighting.

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
X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

model = LogisticRegressionGD(lr=0.5, epochs=800).fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

print("coefficients:", dict(zip(cols, np.round(model.w, 3))))
print("accuracy:", round(model.score(X_test, y_test), 4),
      "AUC:", round(ev.roc_auc_score(y_test, proba), 4))
print(ev.classification_report(y_test, pred).round(3).to_string(index=False))
```

```text
coefficients: {'annual_income_k': 0.691, 'loan_amount_k': -0.586, 'credit_score': 0.82,
 'employment_years': 0.358, 'debt_ratio': -0.47, 'default_history': -0.551}
accuracy: 0.7834 AUC: 0.7976
 class  precision  recall    f1  support
    0      0.815   0.893 0.852      262
    1      0.678   0.527 0.593      112
macro      0.747   0.710 0.723      374
```

Class weights on the attrition data:

```python
import datasets as ds
from prep import StandardScaler, train_test_split
from classifiers import LogisticRegressionGD
import evaluation as ev

frame = ds.attrition()
cols = ["age", "monthly_income_k", "years_at_company", "job_satisfaction", "overtime",
        "distance_from_home_km", "num_companies_worked", "environment_satisfaction", "job_level"]
X, y = frame[cols].to_numpy(), frame["attrition"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

for weights in [None, "balanced"]:
    m = LogisticRegressionGD(lr=0.5, epochs=1000, class_weight=weights).fit(X_train, y_train)
    p = m.predict_proba(X_test)[:, 1]
    print(weights, "accuracy", round(m.score(X_test, y_test), 3),
          "precision", round(ev.precision(y_test, (p >= 0.5).astype(int)), 3),
          "recall", round(ev.recall(y_test, (p >= 0.5).astype(int)), 3))
```

```text
None accuracy 0.843 precision 0.538 recall 0.125
balanced accuracy 0.68 precision 0.306 recall 0.786
```

## 8. Practical Applications

- **Credit approval** — the scorecard is a logistic regression in regulated industries precisely
  because each coefficient can be explained and audited.
- **Clinical risk scores** — small, interpretable models are preferred over marginally more
  accurate black boxes when a clinician must act on them.
- **Churn prediction** — class weights or threshold tuning decide how many customers get a
  retention offer.
- **Spam and abuse** — high-dimensional text features, heavily regularised; precision matters
  because false positives cost real users.

## 9. Common Mistakes

1. **Reporting accuracy on imbalanced data.** 84% accuracy with 13% recall is a broken product.
2. **Treating 0.5 as sacred.** The threshold encodes costs; choose it explicitly.
3. **Forgetting to scale.** Gradient descent diverges or crawls; coefficients become
   incomparable.
4. **Perfect separation.** If a feature splits the classes exactly, coefficients diverge; the
   model is unstable and regularisation is mandatory.
5. **Interpreting coefficients as effects.** Same caveat as linear regression, plus the odds
   scale makes magnitude comparisons easy to over-read.
6. **Ignoring calibration.** A model can rank well and be badly calibrated; if you use the
   probability itself (expected cost), check it.

## 10. Practical Exercises

1. Reproduce the loan coefficients and report the odds multiplier for `default_history`.
2. Fit with and without `class_weight="balanced"` on the loan data. Which changes more, precision
   or recall? Why?
3. Using `threshold_sweep`, find the threshold that maximises F1. Compute the cost-optimal
   threshold if a false negative costs 5 and a false positive costs 1.
4. Add `purpose` as one-hot features. Does test AUC improve? Report the change with a CV interval.
5. Explain why the log-loss is unbounded when a confident prediction is wrong, and what that
   implies for outliers in the training set.

## 11. Self-Assessment

**Multiple choice**

1. Logistic regression models
   a) the probability linearly. b) the log-odds linearly. c) the odds quadratically. d) the label.
2. A coefficient of 0.693 multiplies the odds by
   a) 0.693. b) 1.0. c) 2.0. d) e.
3. Raising the threshold from 0.5 to 0.7 will generally
   a) raise recall. b) raise precision. c) raise AUC. d) change the ranking.
4. Class weighting changes
   a) the ROC curve's ranking. b) the loss each class contributes. c) the features. d) the split.

**Short answer**

5. Why is cross-entropy preferred to squared error for classification?
6. A model has AUC 0.90 and accuracy 0.55. What is the likely explanation?

<details>
<summary>Answers</summary>

1. **b**. 2. **c**. 3. **b** — fewer positives flagged, so the ones flagged are more likely
correct. 4. **b**. 5. It is the negative log-likelihood, convex for the logistic model, and it
punishes confident wrong probabilities heavily. 6. The ranking is good but the threshold is
badly placed for the class balance; tune the threshold.

</details>

## 12. Key Terms

**Logistic regression**, **sigmoid**, **logit**, **log-odds**, **odds ratio**, **decision
boundary**, **binary cross-entropy**, **log-loss**, **maximum likelihood**, **class weight**,
**threshold**, **calibration**, **perfect separation**.

## 13. Further Reading

- Hosmer, D., Lemeshow, S. & Sturdivant, R. (2013). *Applied Logistic Regression*, Chapter 1–3.
- Murphy, K. (2022). *Probabilistic Machine Learning: An Introduction*, §10. — The GLM view.
- Van Calster, B. et al. (2019). *Calibration: the Achilles heel of predictive analytics*. BMC
  Medicine. — Why ranking well is not enough.

## What to Do Next

1. Run `python classifiers.py` and compare the logistic row with k-NN and the tree.
2. Do exercises 2–3; you will reuse the threshold analysis in LAB-06-02.
3. Continue to [L06-05 — Model Evaluation: Metrics and ROC](L06-05-model-evaluation-metrics-and-roc.md).

---

**Navigation:** [← Previous: ? Lesson](L06-03-linear-regression-from-first-principles.md) · [Module home](../README.md) · [Next: ? Lesson →](L06-05-model-evaluation-metrics-and-roc.md)
