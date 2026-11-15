# L06-06 — Bias, Variance, Regularisation and Generalisation

[← Previous: L06-05](L06-05-model-evaluation-metrics-and-roc.md) · [Module home](../README.md) · [Next: L06-07 →](L06-07-k-nearest-neighbours-and-naive-bayes.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Diagnosing and Fixing Generalisation](#4-the-procedure-diagnosing-and-fixing-generalisation)
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

> **Module M06** · Lesson 6 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-03, L06-05

[Previous: L06-05](L06-05-model-evaluation-metrics-and-roc.md) · [Module overview](../README.md) · [Next: L06-07 →](L06-07-k-nearest-neighbours-and-naive-bayes.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Decompose** expected squared error into bias, variance and irreducible noise, and explain
   what each term responds to.
2. **Diagnose** underfitting and overfitting from train/validation scores and learning curves.
3. **Explain** how L2 (ridge) and L1 (lasso) penalties change the solution, and when each is
   appropriate.
4. **Select** a regularisation strength by cross-validation rather than by test score.
5. **Recognise** the levers that reduce variance: more data, simpler models, regularisation,
   averaging, early stopping.
6. **State** why the classic trade-off is a simplification, and what double descent adds.

## 2. Prerequisite Knowledge

Least squares (L06-03), train/validation/test splits and k-fold CV (L06-02), and the metric
vocabulary of L06-05.

## 3. Conceptual Explanation

### 3.1 The decomposition

For a fixed input $x$, with $y = f(x) + \varepsilon$, $\mathbb{E}[\varepsilon]=0$,
$\text{Var}(\varepsilon)=\sigma^2$, and a model $\hat f$ fitted on a random training set:

$$
\mathbb{E}\big[(y - \hat f(x))^2\big]
= \underbrace{\big(\mathbb{E}[\hat f(x)] - f(x)\big)^2}_{\text{bias}^2}
+ \underbrace{\text{Var}\big(\hat f(x)\big)}_{\text{variance}}
+ \underbrace{\sigma^2}_{\text{noise}}.
$$

- **Bias** is error from the model family being too rigid: a straight line fitted to a curve.
  It does not shrink with more data.
- **Variance** is error from sensitivity to the particular training sample: a deep tree that
  changes shape when one row changes. It shrinks with more data and with constraint.
- **Noise** is irreducible. No model can beat it, and any test score near $1-\sigma^2$ claims
  are suspect.

The practical form: **underfitting** is high bias (both train and validation scores poor);
**overfitting** is high variance (train score excellent, validation much worse).

### 3.2 Seeing it in learning curves

The learning curve plots score against training-set size:

```text
unlimited-depth tree
 fraction  n_train  train  validation
      0.2      200    1.0       0.647
      0.5      500    1.0       0.653
      1.0     1000    1.0       0.683

depth-4 tree
 fraction  n_train  train  validation
      0.2      200  0.808       0.747
      0.5      500  0.795       0.743
      1.0     1000  0.775       0.734
```

Read them as diagnoses:

- **Unlimited tree**: train 1.000, validation 0.65–0.68. The gap is enormous and closes only
  slowly with data. Classic high variance. More data would help eventually; constraining the tree
  helps now.
- **Depth-4 tree**: train 0.78–0.81, validation 0.73–0.75. A small gap, both scores mediocre.
  This is closer to high bias: the model is too simple to capture the structure, and more data
  will not fix it.

The two curves answer different questions: "is my model too flexible?" and "would more data
help?" A third case, both scores high and close, is the one you want.

### 3.3 Regularisation

Add a penalty on coefficient size to the loss:

$$
\text{Ridge: } \|\mathbf{y}-\mathbf{X}\mathbf{w}\|^2 + \lambda\|\mathbf{w}\|_2^2
\qquad
\text{Lasso: } \|\mathbf{y}-\mathbf{X}\mathbf{w}\|^2 + \lambda\|\mathbf{w}\|_1.
$$

Ridge has a closed form, $\hat{\mathbf{w}} = (\mathbf{X}^\top\mathbf{X} + \lambda\mathbf{I})^{-1}
\mathbf{X}^\top\mathbf{y}$. The $\lambda\mathbf{I}$ does two useful things: it shrinks
coefficients toward zero (never exactly to zero), and it makes the matrix invertible even when
features are collinear.

Lasso's L1 penalty has a corner at zero, so its solution is sparse — some coefficients are
exactly zero and the model selects features. It has no closed form; coordinate descent with a
soft-threshold update solves it:

$$
w_j \leftarrow \frac{\text{soft}\big(\rho_j,\ \lambda\big)}{\sum_i x_{ij}^2/n},
\qquad
\text{soft}(\rho,\lambda) =
\begin{cases}
\rho-\lambda & \rho>\lambda\\
0 & |\rho|\le\lambda\\
\rho+\lambda & \rho<-\lambda
\end{cases}
$$

Geometry: the L2 constraint region is a sphere, and the loss contours touch it at a generic
point with all coordinates non-zero. The L1 region is a diamond with corners on the axes, and
the contours often touch a corner — hence exact zeros.

Never penalise the intercept. It is a location parameter, not a slope, and shrinking it biases
every prediction.

### 3.4 Choosing $\lambda$

By cross-validation on the training set, never on the test set. Sweep a logarithmic grid
(0.001, 0.01, 0.1, 1, 10, 100), plot CV error against $\log\lambda$ (a "ridge trace"), and pick
the minimum — or one standard error above it, the usual parsimony rule.

On the student data, with four standardised-ish features and 450 training rows:

```text
alpha     ridge R2   lasso R2   lasso non-zero
  0.0       0.5396     0.5396          4
  1.0       0.5396     0.4872          4
 10.0       0.5399    -0.0264          0
100.0       0.5423    -0.0264          0
```

Two lessons in one table. First, ridge barely moves: with $n=450$, $X^\top X$ already dominates
a penalty of 100, so the model is not variance-limited. Second, lasso at $\alpha=10$ kills all
four coefficients and the model collapses to predicting the mean (R² −0.026). A penalty that is
too strong is not "more regularised"; it is a different, worse model.

### 3.5 The levers

| Symptom | Lever | Cost |
| :--- | :--- | :--- |
| High variance | more data | expensive, sometimes impossible |
| High variance | simpler model (depth, k, degree) | may raise bias |
| High variance | L1/L2 penalty | needs tuning; shrinks real effects |
| High variance | averaging (bagging, ensembles) | compute; less interpretable |
| High variance | early stopping | needs a validation stream |
| High bias | richer model, better features | variance |
| High bias | fix the label or features | data work, not modelling |

### 3.6 The trade-off is not the whole story

The U-shaped curve is the classical picture and it is the right default. Modern practice adds
two wrinkles:

- **Double descent**: as model size grows far beyond the interpolation point, test error can
  fall again. This is real in over-parameterised networks, but it does not rescue you on 600
  tabular rows.
- **More data beats more regularisation** when the data are representative. Regularisation is a
  constraint on a model that would otherwise fit noise; it is not a substitute for information.

## 4. The Procedure: Diagnosing and Fixing Generalisation

1. Fit a baseline (mean, majority class, current rule).
2. Fit the simplest model of the family. Record train and validation scores.
3. If both are poor: the model is too simple or the features are uninformative. Stop tuning
   hyperparameters and go back to features.
4. If train is excellent and validation is poor: reduce capacity, add regularisation, get more
   data, or average models.
5. Plot the learning curve at two or three capacities to see which regime you are in.
6. Choose $\lambda$ (or depth, or k) by CV; report the CV mean and spread.
7. Fit on train+validation, evaluate once on test.
8. Report the gap between train and test alongside the score. A model with 0.99 train / 0.70
   test is a different product from 0.73 / 0.72.

## 5. Worked Examples

### Example 1 — Polynomial degree as a capacity dial

From L06-03, 450 training rows:

| Degree | Columns | Train R² | Test R² |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 0.533 | 0.540 |
| 2 | 14 | 0.541 | 0.533 |
| 3 | 34 | 0.567 | 0.487 |
| 4 | 69 | 0.606 | 0.348 |
| 5 | 125 | 0.651 | −15.688 |

Train R² rises; test R² peaks at degree 1. The model at degree 5 has 125 parameters for 450
rows and has fit the noise. If you must use degree 5, ridge it — but there is no reason to on
this data.

### Example 2 — Tree depth

```text
tree unlimited : train 1.000  test 0.679  AUC 0.597
tree depth 5   : train 0.801  test 0.717  AUC 0.696
```

The unlimited tree memorised the training set (accuracy 1.000) and ranks worse than the depth-5
tree on held-out data (AUC 0.597 vs 0.696). The depth limit is a hard constraint on variance; the
forest in L06-08 is a soft one (averaging many high-variance trees).

### Example 3 — Ridge in closed form, checked

With $\lambda=100$ the student model's R² barely changes (0.5396 → 0.5423). That is not a
failure of ridge; it is evidence the model was not overfitting in the first place. Regularisation
helps when the unregularised fit is unstable — many correlated features, few rows, or a very
flexible basis. Always compare, never assume.

## 6. Mathematical Formulation

**Bias–variance identity.** Let $\hat f = \hat f(x; D)$ depend on the random training set $D$.
Then

$$
\mathbb{E}_{D,y}\big[(y-\hat f)^2\big]
= \big(\mathbb{E}_D[\hat f]-f\big)^2 + \mathbb{E}_D\big[(\hat f-\mathbb{E}_D[\hat f])^2\big] + \sigma^2.
$$

The cross term vanishes because $y - f = \varepsilon$ is independent of $D$ and has zero mean.

**Ridge solution.** $\hat{\mathbf{w}} = (\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I})^{-1}
\mathbf{X}^\top\mathbf{y}$. As $\lambda\to\infty$, $\hat{\mathbf{w}}\to 0$.

**Lasso subgradient.** The objective is non-differentiable at zero; the coordinate-wise
soft-threshold solution above is exact for orthonormal designs and converges for general ones.

**Effective degrees of freedom** for ridge: $\text{tr}\big(\mathbf{X}(\mathbf{X}^\top\mathbf{X}+
\lambda\mathbf{I})^{-1}\mathbf{X}^\top\big)$, which falls from $d$ toward 0 as $\lambda$ grows.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import numpy as np
import datasets as ds
import linreg as lr
from prep import train_test_split

frame = ds.students()
cols = ["study_hours", "attendance_pct", "prior_grade", "sleep_hours"]
X = frame[cols].fillna(frame[cols].median()).to_numpy()
y = frame["final_score"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0)

for alpha in [0.0, 1.0, 10.0, 100.0]:
    ridge = lr.Ridge(alpha).fit(X_train, y_train)
    lasso = lr.Lasso(alpha if alpha else 1e-8).fit(X_train, y_train)
    print(f"{alpha:6.1f} ridge {ridge.score(X_test, y_test):.4f} "
          f"lasso {lasso.score(X_test, y_test):.4f} "
          f"nonzero {int(np.sum(np.abs(lasso.coef_) > 1e-8))}")
```

```text
   0.0 ridge 0.5396 lasso 0.5396 nonzero 4
   1.0 ridge 0.5396 lasso 0.4872 nonzero 4
  10.0 ridge 0.5399 lasso -0.0264 nonzero 0
 100.0 ridge 0.5423 lasso -0.0264 nonzero 0
```

Learning curves:

```python
import datasets as ds
import evaluation as ev
from classifiers import DecisionTreeClassifier

frame = ds.loans()
cols = ["annual_income_k", "loan_amount_k", "credit_score",
        "employment_years", "debt_ratio", "default_history"]
X = frame[cols].fillna(frame[cols].median()).to_numpy()
y = frame["approved"].to_numpy()

for label, factory in [
    ("unlimited", lambda: DecisionTreeClassifier()),
    ("depth 4", lambda: DecisionTreeClassifier(max_depth=4, min_samples_leaf=10)),
]:
    curve = ev.learning_curve(factory, X, y, fractions=(0.2, 0.5, 1.0), k=3)
    print(label)
    print(curve.round(3).to_string(index=False))
```

```text
unlimited
 fraction  n_train  train  validation
      0.2      200    1.0       0.647
      0.5      500    1.0       0.653
      1.0     1000    1.0       0.683
depth 4
 fraction  n_train  train  validation
      0.2      200  0.808       0.747
      0.5      500  0.795       0.743
      1.0     1000  0.775       0.734
```

## 8. Practical Applications

- **Credit scorecards** — strong ridge/L1 penalties are standard; monotonic constraints are
  common so that a higher income never lowers the score.
- **Genomics** — $p \gg n$; lasso is the default for selecting a handful of genes from thousands.
- **Sensor forecasting** — early stopping and shallow models beat deep ones when data are few.
- **Recommenders** — matrix factorisation is ridge regression on latent factors, with
  regularisation essential because most entries are missing.

## 9. Common Mistakes

1. Choosing $\lambda$ on the test set. The reported score then describes the test set, not the
   model.
2. Penalising the intercept.
3. Assuming regularisation always helps. If the model is not overfitting, it can only hurt.
4. Reading a lasso zero as "this feature is irrelevant". Correlated features are dropped
   arbitrarily in favour of one another; the group matters, not the survivor.
5. Comparing learning curves built on different splits.
6. Calling a 0.99/0.70 model "99% accurate". Quote both numbers or neither.

## 10. Practical Exercises

1. Reproduce the ridge/lasso table. At which $\alpha$ does lasso drop its first coefficient?
2. Fit ridge with $\alpha \in \{10^{-4}, \dots, 10^{4}\}$ and plot test R² against $\log\alpha$.
   Where is the plateau?
3. Reproduce both learning curves. Which model would benefit more from 10,000 extra rows?
4. Add five noise features to the loan data (random numbers). Compare logistic regression with
   and without L2. What happens to test AUC?
5. Explain in three sentences why L1 produces exact zeros and L2 does not.

## 11. Self-Assessment

**Multiple choice**

1. High variance shows as
   a) low train and low validation score. b) high train and low validation score.
   c) high train and high validation score. d) low train and high validation score.
2. Increasing $\lambda$ in ridge generally
   a) increases variance. b) decreases coefficient magnitudes. c) zeros coefficients exactly.
   d) changes the features.
3. Lasso performs feature selection because
   a) its loss is convex. b) the L1 ball has corners on the axes. c) it uses gradient descent.
   d) it standardises features.
4. Which does **not** reduce variance?
   a) more training data. b) averaging many models. c) a deeper tree. d) a stronger L2 penalty.

**Short answer**

5. Why is the noise term irreducible?
6. Your train accuracy is 0.99 and validation is 0.70. Give two fixes and the cost of each.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **c** — a deeper tree increases variance.
5. It is the randomness in $y$ given $x$; no function of $x$ can predict it.
6. Constrain capacity (possible loss of signal) and add data or average models (cost: data,
   compute, interpretability).

</details>

## 12. Key Terms

**Bias**, **variance**, **irreducible error**, **underfitting**, **overfitting**, **learning
curve**, **regularisation**, **ridge (L2)**, **lasso (L1)**, **shrinkage**, **sparsity**,
**penalty strength**, **effective degrees of freedom**, **double descent**.

## 13. Further Reading

- Hastie, Tibshirani & Friedman (2009). *The Elements of Statistical Learning*, §3.4 and §7. —
  The decomposition and the ridge/lasso geometry.
- Zhang, C. et al. (2021). *Understanding Deep Learning (Still) Requires Rethinking
  Generalization*. CACM. — Double descent and what it does and does not explain.
- scikit-learn user guide, *Linear Models* (Ridge, Lasso, ElasticNet).

## What to Do Next

1. Run `python linreg.py` again and read the ridge/lasso block with §3.4 in mind.
2. Do exercises 3–4; the noise-feature experiment is the core of LAB-06-02.
3. Continue to [L06-07 — k-Nearest Neighbours and Naïve Bayes](L06-07-k-nearest-neighbours-and-naive-bayes.md).

---

**Navigation:** [← Previous: L06-05](L06-05-model-evaluation-metrics-and-roc.md) · [Module home](../README.md) · [Next: L06-07 →](L06-07-k-nearest-neighbours-and-naive-bayes.md)
