# L06-03 — Linear Regression from First Principles

[← Previous: L06-02](L06-02-data-splitting-leakage-and-cross-validation.md) · [Module home](../README.md) · [Next: L06-04 →](L06-04-classification-with-logistic-regression.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Fitting and Checking a Linear Model](#4-the-procedure-fitting-and-checking-a-linear-model)
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

> **Module M06** · Lesson 3 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-02, P02 (matrices, derivatives)

[Previous: L06-02](L06-02-data-splitting-leakage-and-cross-validation.md) · [Module overview](../README.md) · [Next: L06-04 →](L06-04-classification-with-logistic-regression.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Fit** simple and multiple linear regression by ordinary least squares, and state what the
   normal equations are minimising.
2. **Interpret** a coefficient as the expected change in the target per unit change in a
   feature, holding the others fixed — and name the conditions under which that reading fails.
3. **Derive** the gradient-descent update and explain why unstandardised features make it
   diverge.
4. **Extend** the model to polynomial and interaction terms, and explain why higher degree is
   not automatically better.
5. **Evaluate** a regression with MAE, RMSE and R², and choose among them from the cost of error.
6. **Diagnose** the four assumptions and the three common failure modes: extrapolation,
   multicollinearity and omitted variables.

## 2. Prerequisite Knowledge

Matrix multiplication, the dot product, partial derivatives, and the meaning of "minimise a
function". If the normal equations look unfamiliar, read the derivation in §6 slowly — it is
three lines of calculus.

## 3. Conceptual Explanation

### 3.1 The model

Simple linear regression with one feature:

$$
\hat{y} = w x + b.
$$

Multiple linear regression with $d$ features:

$$
\hat{y} = w_1x_1 + w_2x_2 + \dots + w_dx_d + b = \mathbf{w}^\top \mathbf{x} + b.
$$

Fitting means choosing $\mathbf{w}$ and $b$ to make the predictions close to the observed $y$,
where "close" is measured by the sum of squared errors:

$$
\text{SSE}(\mathbf{w}, b) = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2.
$$

Squaring does two things: it makes over- and under-prediction cost the same, and it punishes
large misses much more than small ones. That second property is a choice, not a law — if a
20-unit miss is not four times worse than a 10-unit miss, squared error is the wrong loss and
MAE is the right one.

### 3.2 Why the least-squares solution is unique

SSE is a convex quadratic in the parameters, so it has one global minimum (up to collinearity).
Setting the derivative to zero gives the normal equations, and solving them gives the closed
form in §6. Convexity is why linear regression has no "local minima" problem and why the
closed-form and gradient-descent solutions agree to machine precision when both converge.

### 3.3 Interpreting coefficients

On the student data the fitted model is

$$
\widehat{\text{score}} = 18.38 + 1.28\,\text{study} + 0.098\,\text{attendance}
+ 0.257\,\text{prior} + 0.897\,\text{sleep}.
$$

- **1.28 per study hour**: one more hour per week is associated with 1.28 more points, holding
  attendance, prior grade and sleep fixed.
- **0.098 per attendance point**: ten percentage points of attendance is about one point.
- **The intercept (18.38)** is the prediction for a student with zero on every feature. It is a
  mathematical anchor, not a realistic student; do not interpret it as a baseline score.

"Associated with" is deliberate. These coefficients are conditional correlations in this
sample. They are not causal effects: students who study more may differ in motivation, and
motivation is not in the model.

### 3.4 Gradient descent

For large $d$ or streaming data the closed form is expensive ($O(nd^2)$) or impossible, so we
descend the loss surface instead:

$$
\mathbf{w} \leftarrow \mathbf{w} - \eta\,\frac{1}{n}\mathbf{X}^\top(\mathbf{X}\mathbf{w} + b - \mathbf{y}),
\qquad
b \leftarrow b - \eta\,\frac{1}{n}\sum_i(\hat{y}_i - y_i).
$$

The learning rate $\eta$ multiplies the gradient. Two failure modes, both visible in the demo:

- **Too small**: convergence is slow but stable.
- **Too large, or features on different scales**: the surface is a long thin valley, the step
  overshoots across it, and the loss grows without bound. On the raw student features,
  $\eta = 0.1$ produces a final loss of about $1.2\times10^{297}$ — divergence, not convergence.
  Standardising the features first gives a final loss of 34.86.

This is not a curiosity. It is the practical reason `StandardScaler` sits in front of almost
every gradient-based model.

### 3.5 Polynomial regression and interactions

Polynomial features replace $x$ with $(x, x^2, \dots, x^p)$; with several features they also add
products such as $x_1x_2$. The model stays **linear in the parameters**, so OLS still applies —
only the design matrix changes.

The cost is variance. On the student data, with 450 training rows:

| Degree | Columns | Train R² | Test R² |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 0.533 | 0.540 |
| 2 | 14 | 0.541 | 0.533 |
| 3 | 34 | 0.567 | 0.487 |
| 4 | 69 | 0.606 | 0.348 |
| 5 | 125 | 0.651 | **−15.688** |

Training R² rises monotonically — more columns always fit the training set better. Test R²
peaks at degree 1 and collapses by degree 5. The polynomial is not "learning more"; it is
memorising noise, and at degree 5 it is so unstable that it beats the mean predictor by doing
worse than it.

### 3.6 The assumptions, and what breaks when they fail

| Assumption | What it buys | Symptom when violated |
| :--- | :--- | :--- |
| Linearity in parameters | the model form is right | curved residual plot; add terms or transform |
| Independent errors | valid standard errors | clustered/time data; use grouped or time-series methods |
| Constant error variance | efficient OLS, valid intervals | funnel-shaped residuals; transform $y$ or use robust SEs |
| No perfect collinearity | unique coefficients | coefficients flip sign when a column is added |
| Exogeneity (for causal claims) | coefficients are effects | omitted variable bias; use design or instruments |

Note what is *not* on the list: normality of $y$. Normality of the **residuals** matters only
for small-sample confidence intervals, not for the point predictions.

## 4. The Procedure: Fitting and Checking a Linear Model

1. Plot $y$ against each candidate feature. Curvature means you need a transform or a term.
2. Split; fit on train only.
3. Fit OLS. Record coefficients **with units**.
4. Compute train and test MAE, RMSE, R².
5. Compare against the mean baseline: a model that cannot beat it has learned nothing.
6. Plot residuals against fitted values and against each feature.
7. Check for collinearity (correlation matrix, variance inflation).
8. If residuals curve, add polynomial or interaction terms, then re-check test R².
9. If test R² falls while train R² rises, stop adding capacity and regularise (L06-06).
10. State the population and the time window the coefficients apply to.

## 5. Worked Examples

### Example 1 — The student model, by hand and by library

With four features, $n = 450$ training rows, the closed form gives the coefficients above and:

```text
test MSE 30.485   RMSE 5.521   MAE 4.532   R2 0.540   adjusted R2 0.527
mean baseline:     MAE 6.782   R2 -0.026
```

Read the two rows together. The model's typical error is 4.5 points; predicting the training
mean for everyone gives 6.8. The R² of 0.54 says just over half the variance in final scores is
associated with these four variables. Nothing here says the other half is random: motivation,
teaching quality and prior knowledge are missing.

The mean baseline's R² is slightly negative (−0.026) because it is the *training* mean applied
to the test set, which happens to have a slightly different mean. That is a useful reminder that
R² can go below zero out of sample.

### Example 2 — One feature, analytically

Take `study_hours` alone. The slope is

$$
w = \frac{\sum_i (x_i - \bar{x})(y_i - \bar{y})}{\sum_i (x_i - \bar{x})^2}
= \frac{\text{cov}(x,y)}{\text{var}(x)},
$$

and the intercept is $b = \bar{y} - w\bar{x}$. This is the same least-squares solution as the
matrix version with $d=1$; if you can compute a covariance and a variance, you can fit a simple
regression by hand. The correlation between study hours and final score in this dataset is 0.56,
which is why the multiple-regression coefficient (1.28) is smaller than the simple slope would
suggest: attendance and prior grade absorb part of the same variation.

### Example 3 — When a high R² is bad news

A model predicting house price from `living_area_sqft` alone reaches R² ≈ 0.5 on the clipped
data. Add `price_per_sqft` and R² jumps — because that column is computed from the price. High
R² is a claim about fit, not about validity; always ask what each column is derived from
(L06-02, §3.9).

## 6. Mathematical Formulation

Write the design matrix $\mathbf{X} \in \mathbb{R}^{n\times(d+1)}$ with a leading column of
ones, and $\mathbf{y}\in\mathbb{R}^n$. The model is $\hat{\mathbf{y}} = \mathbf{X}\mathbf{w}$ and

$$
\text{SSE}(\mathbf{w}) = (\mathbf{y} - \mathbf{X}\mathbf{w})^\top(\mathbf{y} - \mathbf{X}\mathbf{w}).
$$

Differentiate and set to zero:

$$
\nabla_{\mathbf{w}}\text{SSE} = -2\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\mathbf{w}) = 0
\;\;\Longrightarrow\;\;
\mathbf{X}^\top\mathbf{X}\,\mathbf{w} = \mathbf{X}^\top\mathbf{y}.
$$

If $\mathbf{X}^\top\mathbf{X}$ is invertible,

$$
\hat{\mathbf{w}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}.
$$

In code we solve the system with an SVD (`np.linalg.lstsq`) instead of inverting, because
inverting squares the condition number: with near-collinear columns the explicit inverse loses
precision, while the SVD solution remains stable.

**R²** is

$$
R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2},
$$

the fraction of variance explained relative to the mean predictor. **Adjusted R²** penalises
extra parameters:

$$
R^2_{\text{adj}} = 1 - (1 - R^2)\frac{n-1}{n-d-1}.
$$

It rises only when a new feature improves fit by more than chance would.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import numpy as np
import datasets as ds
import linreg as lr
from prep import train_test_split

frame = ds.students()
cols = ["study_hours", "attendance_pct", "prior_grade", "sleep_hours"]
clean = frame[cols].fillna(frame[cols].median())
X, y = clean.to_numpy(), frame["final_score"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0)

model = lr.LinearRegression().fit(X_train, y_train)
print(dict(zip(cols, np.round(model.coef_, 3))), "intercept", round(model.intercept_, 2))
print({k: round(v, 3) for k, v in lr.regression_report(y_test, model.predict(X_test), 4).items()})

baseline = np.full_like(y_test, y_train.mean())
print("baseline MAE", round(lr.mae(y_test, baseline), 3),
      "R2", round(lr.r2_score(y_test, baseline), 3))
```

```text
{'study_hours': 1.28, 'attendance_pct': 0.098, 'prior_grade': 0.257, 'sleep_hours': 0.897} intercept 18.38
{'mse': 30.485, 'rmse': 5.521, 'mae': 4.532, 'r2': 0.54, 'adj_r2': 0.527}
baseline MAE 6.782 R2 -0.026
```

Gradient descent, with and without scaling:

```python
raw = lr.LinearRegressionGD(lr=0.1, epochs=50).fit(X_train, y_train)
scaled = lr.LinearRegressionGD(lr=0.1, epochs=500, standardize=True).fit(X_train, y_train)
print("raw loss first/last:   ", round(raw.loss_history_[0], 1), raw.loss_history_[-1])
print("scaled loss first/last:", round(scaled.loss_history_[0], 1), round(scaled.loss_history_[-1], 2))
print("scaled test R2:", round(scaled.score(X_test, y_test), 4))
```

```text
raw loss first/last:    74.6 1.1713355297443288e+297
scaled loss first/last: 74.6 34.86
scaled test R2: 0.5396
```

Both start at the same loss (74.6) because they start at the same prediction — the training
mean. Then one diverges and the other converges. The only difference is the feature scale.

Polynomial degrees:

```python
for degree in range(1, 6):
    poly = lr.PolynomialFeatures(degree).fit(X_train)
    m = lr.LinearRegression().fit(poly.transform(X_train), y_train)
    print(f"degree {degree}: {poly.n_output_features_:3d} columns "
          f"train R2 {m.score(poly.transform(X_train), y_train):.3f} "
          f"test R2 {m.score(poly.transform(X_test), y_test):.3f}")
```

```text
degree 1:   4 columns train R2 0.533 test R2 0.540
degree 2:  14 columns train R2 0.541 test R2 0.533
degree 3:  34 columns train R2 0.567 test R2 0.487
degree 4:  69 columns train R2 0.606 test R2 0.348
degree 5: 125 columns train R2 0.651 test R2 -15.688
```

## 8. Practical Applications

- **House prices** — the baseline every more complex model must beat; SHAP or coefficient
  inspection gives the valuation breakdown.
- **Demand forecasting** — linear models with calendar and price features are standard baselines.
- **Dose–response in medicine** — with the causal caveat; regression adjustment is not a
  substitute for randomisation.
- **A/B test analysis** — a difference in means is a regression with one binary feature.

## 9. Common Mistakes

1. **Reading coefficients as causal effects.** They are conditional associations in the sample.
2. **Extrapolating.** A model fitted on houses of 1,000–3,000 sqft has no basis for 12,000.
3. **Adding features to raise R².** Training R² cannot fall when you add a column; use adjusted
   R² or test R².
4. **Ignoring collinearity.** Two near-duplicate features make coefficients unstable and their
   signs uninterpretable, even when predictions are fine.
5. **Forgetting the scale.** Reporting an RMSE of 5.5 without units ("points out of 100") makes
   it unreadable.
6. **Fitting on the test set "just to see".** Any decision made after seeing test data
   contaminates the test estimate.

## 10. Practical Exercises

1. Fit simple regression of `final_score` on `study_hours` only. Compute slope and intercept by
   the covariance formula and check against `LinearRegression`.
2. Add `part_time_job` as a 0/1 feature. Interpret its coefficient. Then one-hot encode it and
   explain why the coefficient changes representation but not the predictions.
3. Reproduce the degree table. At which degree does test R² start falling, and what does that say
   about the number of parameters relative to 450 rows?
4. Fit the house-price model on clipped data, then predict the price of a 12,000 sqft house and
   explain why the number is untrustworthy.
5. Compute residuals for the student model and plot them against `attendance_pct`. Is there
   curvature? What term would you add?

## 11. Self-Assessment

**Multiple choice**

1. The normal equations minimise
   a) mean absolute error. b) sum of squared errors. c) R². d) the number of features.
2. Adding a useless feature to OLS will
   a) decrease training R². b) leave training R² unchanged or increase it.
   c) always decrease test R². d) make the model non-convex.
3. Gradient descent on unstandardised features with a large learning rate will typically
   a) converge faster. b) diverge. c) improve R². d) reduce variance.
4. Adjusted R² is preferred to R² when
   a) the target is skewed. b) comparing models with different numbers of features.
   c) there are missing values. d) the data are time-ordered.

**Short answer**

5. Explain in one sentence why the closed-form and gradient-descent solutions should agree.
6. A model has train R² 0.99 and test R² 0.12. Name the diagnosis and one remedy.

<details>
<summary>Answers</summary>

1. **b**. 2. **b** — SSE cannot increase when a column is added, so training R² cannot fall.
3. **b**. 4. **b**. 5. Both minimise the same convex SSE, so they reach the same unique minimum
   when the design matrix is full rank and GD converges.
6. Overfitting (high variance); simplify the model, regularise, or get more data.

</details>

## 12. Key Terms

**Simple/multiple linear regression**, **ordinary least squares**, **normal equations**,
**design matrix**, **residual**, **coefficient**, **intercept**, **SSE**, **RMSE**, **MAE**,
**R²**, **adjusted R²**, **collinearity**, **polynomial regression**, **interaction term**,
**extrapolation**, **omitted variable bias**.

## 13. Further Reading

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning*,
  Chapter 3. — OLS, subset selection and the bias–variance framing.
- Gelman, A. & Hill, J. (2006). *Data Analysis Using Regression and Multilevel/Hierarchical
  Models*, Chapters 3–4. — Regression as a modelling discipline rather than a formula.
- Anscombe, F. (1973). *Graphs in Statistical Analysis*. — Four datasets with identical
  regression statistics and completely different shapes.

## What to Do Next

1. Run `python linreg.py`.
2. Do exercises 1–3 and keep the degree table.
3. Continue to [L06-04 — Classification with Logistic Regression](L06-04-classification-with-logistic-regression.md).

---

**Navigation:** [← Previous: L06-02](L06-02-data-splitting-leakage-and-cross-validation.md) · [Module home](../README.md) · [Next: L06-04 →](L06-04-classification-with-logistic-regression.md)
