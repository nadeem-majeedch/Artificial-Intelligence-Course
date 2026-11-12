# L06-08 — Decision Trees, Random Forests, Gradient Boosting and SVMs

[← Previous: ? Lesson](L06-07-k-nearest-neighbours-and-naive-bayes.md) · [Module home](../README.md) · [Next: ? Lesson →](L06-09-unsupervised-learning-and-dimensionality-reduction.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Building and Comparing Tree Models](#4-the-procedure-building-and-comparing-tree-models)
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

> **Module M06** · Lesson 8 of 10 · ~100 minutes · Level 300
> **Prerequisites:** L06-05, L06-06

[Previous: L06-07](L06-07-k-nearest-neighbours-and-naive-bayes.md) · [Module overview](../README.md) · [Next: L06-09 →](L06-09-unsupervised-learning-and-dimensionality-reduction.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Grow** a CART decision tree by hand: compute Gini and entropy, evaluate a split, state the
   gain.
2. **Explain** why a deep tree has low bias and high variance, and how depth, leaf size and
   pruning trade the two.
3. **Describe** bagging and random forests as variance reduction through decorrelation, and
   compute the effect of the correlation between trees.
4. **Explain** gradient boosting as sequential fitting of pseudo-residuals, and why the learning
   rate and the number of rounds trade off.
5. **Explain** the maximum-margin idea, the role of C, and what a kernel does.
6. **Choose** among linear models, trees, forests, boosting and SVMs for a given tabular problem,
   with reasons rather than fashion.

## 2. Prerequisite Knowledge

Impurity as a measure of class mix, the bias–variance decomposition, and logistic regression's
log-loss. For SVMs, the dot product and the idea of a hyperplane.

## 3. Conceptual Explanation

### 3.1 The tree

A decision tree partitions the feature space with axis-aligned splits:

```text
credit_score <= 640 ?
├── yes: debt_ratio <= 0.42 ?
│        ├── yes: reject
│        └── no : reject
└── no : income <= 32 ?
         ├── yes: reject
         └── no : approve
```

Growing it greedily:

1. For each feature, sort the values.
2. For each midpoint between distinct values, split and compute the weighted child impurity.
3. Choose the (feature, threshold) with the largest impurity reduction.
4. Recurse on each side until a stopping rule fires.

Impurity measures for a node with class proportions $p_c$:

$$
\text{Gini} = 1-\sum_c p_c^2,
\qquad
\text{entropy} = -\sum_c p_c\log_2 p_c.
$$

They usually pick similar splits; Gini is cheaper (no logarithm) and is the default in most
libraries.

Three stopping rules do the regularising: `max_depth`, `min_samples_leaf`, `min_samples_split`.
Without them the tree grows until every leaf is pure: training accuracy 1.000, and on the loan
data test accuracy 0.679 — worse than logistic regression.

**Properties worth remembering:**

- No scaling needed; splits depend on order only.
- Axis-aligned boundaries: a diagonal boundary needs many steps to approximate.
- **Unstable**: changing one row can change the whole tree. That instability is exactly what
  bagging fixes.
- Missing values need handling (surrogate splits in some implementations; imputation here).
- Impurity feature importance is biased toward high-cardinality features.

### 3.2 Random forests: averaging decorrelated trees

Bagging: draw $B$ bootstrap samples, fit a deep tree to each, average their predictions. If the
trees were independent, the variance of the average would fall as $\sigma^2/B$. They are not
independent — they all see the same data — so with pairwise correlation $\rho$:

$$
\text{Var}\Big(\frac{1}{B}\sum_b T_b\Big) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2.
$$

As $B\to\infty$ the second term vanishes and the variance floors at $\rho\sigma^2$. The only way
to go lower is to reduce $\rho$. Random forests do that by showing each split a random subset of
features ($\sqrt{d}$ by default for classification), so no single dominant feature makes every
tree identical.

Extras: out-of-bag error is a free validation estimate (each row is out-of-bag for about 37% of
trees), and permutation importance on OOB data is more trustworthy than impurity importance.

### 3.3 Gradient boosting: sequential correction

Boosting builds trees one at a time, each fitted to the errors of the current ensemble:

$$
F_0 = \log\frac{\bar y}{1-\bar y},
\qquad
F_m = F_{m-1} + \nu\, h_m,
$$

where $h_m$ is a small tree fitted to the pseudo-residual $y - \sigma(F_{m-1})$, and $\nu$ is the
learning rate (shrinkage). With log-loss, each leaf's value is the Newton step
$\sum r_i / \sum p_i(1-p_i)$ rather than the mean residual, which converges faster.

The three knobs trade off against one another:

- **more rounds + smaller $\nu$** → better fit, more compute, more overfitting risk;
- **deeper trees** → more interaction captured, higher variance;
- **subsampling rows/columns** → decorrelation, slower convergence, often better generalisation.

Boosting usually beats a single tree and often edges out a forest on tabular data, at the cost of
being harder to tune and easier to overfit if you keep adding rounds.

### 3.4 Ensembles beyond forests

- **Voting/averaging** across different model families reduces variance if their errors are not
  correlated.
- **Stacking** trains a meta-model on out-of-fold predictions. Powerful, and a reliable way to
  leak if the folds are not respected.
- **Blending** is stacking with a holdout instead of folds.

Averaging a logistic regression, a forest and an SVM often gains a point; averaging three nearly
identical forests gains almost nothing. Diversity is the ingredient.

### 3.5 Support vector machines

For linearly separable data there are infinitely many separating hyperplanes. The SVM picks the
one with the **largest margin** — the widest strip containing no points. The points on the strip's
edge are the **support vectors**; everything else could be deleted without changing the model.

Soft margin (the practical version):

$$
\min_{\mathbf{w},b}\ \tfrac12\|\mathbf{w}\|^2 + C\sum_i \max\big(0, 1-y_i(\mathbf{w}^\top\mathbf{x}_i+b)\big),
\qquad y_i\in\{-1,+1\}.
$$

- Large $C$: few margin violations allowed → low bias, high variance.
- Small $C$: wide margin, more violations → smoother boundary.
- The hinge loss is zero once a point is correctly classified beyond the margin, which is why
  only support vectors matter.

**Kernels** replace dot products with $K(\mathbf{x},\mathbf{z})$, implicitly mapping to a
higher-dimensional space where a linear boundary may suffice. The RBF kernel
$K(\mathbf{x},\mathbf{z}) = \exp(-\gamma\|\mathbf{x}-\mathbf{z}\|^2)$ produces curved boundaries;
$\gamma$ controls how far each point's influence reaches.

Costs: training is between $O(n^2)$ and $O(n^3)$ in the naive formulation, and prediction is
$O(n_{SV}d)$. On 1,500 rows that is nothing; on 5 million it is a problem. Scaling is mandatory
because the margin depends on distances.

### 3.6 Choosing a model

| Situation | First choice | Why |
| :--- | :--- | :--- |
| Few rows, many features, need explanation | regularised logistic/linear | low variance, interpretable |
| Mixed tabular data, accuracy matters | gradient boosting or forest | captures interactions, robust to scaling |
| Need a human-readable rule set | shallow tree | auditable, limited accuracy |
| Text counts | multinomial NB or linear SVM | sparse, high-dimensional |
| Small n, curved boundary, low dimensions | SVM with RBF | strong margin, few parameters |
| Streaming or tiny device | NB, logistic | one-pass, small memory |
| Almost no tuning budget | random forest | robust defaults |

## 4. The Procedure: Building and Comparing Tree Models

1. Establish the linear baseline (logistic or ridge). It is surprisingly hard to beat.
2. Fit a shallow tree; inspect depth and leaf sizes; record train/test gap.
3. Fit a forest with sensible defaults (200 trees, `min_samples_leaf` 1–5). Compare CV.
4. Fit gradient boosting; tune rounds and learning rate together, never separately.
5. Compare on the **same folds**, with mean and spread, and on the metric tied to the decision.
6. Inspect permutation importance and the confusion matrix of the winner.
7. Check the errors for a pattern (a subgroup, a feature range, a time period).
8. Only then consider an SVM or a stack, and only if the gap to the target is still material.

## 5. Worked Examples

### Example 1 — One split by hand

A node has 10 rows: 6 positive, 4 negative. Candidate split A sends 5 rows left (4 positive,
1 negative) and 5 right (2 positive, 3 negative).

Parent Gini: $1-(0.6^2+0.4^2) = 0.48$.
Left Gini: $1-(0.8^2+0.2^2) = 0.32$.
Right Gini: $1-(0.4^2+0.6^2) = 0.48$.
Weighted child Gini: $0.5(0.32)+0.5(0.48)=0.40$. **Gain 0.08.**

Parent entropy: $-0.6\log_2 0.6 - 0.4\log_2 0.4 = 0.971$.
Left: $-0.8\log_2 0.8 - 0.2\log_2 0.2 = 0.722$.
Right: 0.971. Weighted: 0.846. **Gain 0.125.**

The two criteria agree on the direction and differ in scale. The tree only needs the argmax, which
is why either works.

### Example 2 — Capacity and averaging on the loan data

```text
model              train  test   AUC
logistic           0.784  0.783  0.798
kNN k=15           0.790  0.743  0.766
GaussianNB         0.766  0.711  0.758
tree depth=5       0.801  0.717  0.696
tree unlimited     1.000  0.679  0.597
forest 100         0.834  0.762  0.802
boosting 100       0.825  0.762  0.790
linear SVM         0.775  0.778  0.795
```

Three stories in one table:

- The unlimited tree has perfect training accuracy and the **worst** AUC. Memorisation is not
  learning.
- The forest beats every single tree, and beats logistic on AUC (0.802 vs 0.798) while losing on
  accuracy — a reminder that the metric chooses the winner.
- Boosting and the forest tie on accuracy at 0.762; the choice would come down to tuning cost,
  inference latency and interpretability.

### Example 3 — Intrusion detection, where the models earn their keep

```text
random forest: accuracy 0.979  precision 0.961  recall 0.937  AUC 0.996
feature importance: serror_rate 0.428, dst_bytes 0.232, num_failed_logins 0.142,
                    duration 0.125, logged_in 0.044, src_bytes 0.016
```

The synthetic attack signature is concentrated in the error rate, which is why one feature carries
43% of the importance. On real NSL-KDD data the importance spreads more evenly, and the r2l family
("remote to local" password guessing) is much harder than dos — which is exactly the kind of
per-family error analysis the lab asks for.

## 6. Mathematical Formulation

**Gini gain** for split $S$:

$$
\Delta = I(\text{parent}) - \frac{n_L}{n}I(\text{left}) - \frac{n_R}{n}I(\text{right}).
$$

**Bagging variance** (pairwise correlation $\rho$):

$$
\text{Var}\Big(\frac{1}{B}\sum_{b=1}^{B}T_b\Big) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2.
$$

**Gradient boosting update** with log-loss:

$$
F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \nu\, h_m(\mathbf{x}),
\qquad
h_m \text{ fitted to } r_i = y_i - \sigma(F_{m-1}(\mathbf{x}_i)).
$$

**SVM primal** (soft margin, hinge loss) as in §3.5, with dual form

$$
\max_{\alpha}\ \sum_i\alpha_i - \tfrac12\sum_{i,j}\alpha_i\alpha_j y_i y_j K(\mathbf{x}_i,\mathbf{x}_j)
\quad\text{s.t.}\quad 0\le\alpha_i\le C,\ \sum_i \alpha_i y_i = 0.
$$

Points with $\alpha_i>0$ are the support vectors.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import datasets as ds
from prep import StandardScaler, train_test_split
from classifiers import (DecisionTreeClassifier, RandomForestClassifier,
                         GradientBoostingClassifier, LinearSVM, LogisticRegressionGD)
import evaluation as ev

frame = ds.loans()
cols = ["annual_income_k", "loan_amount_k", "credit_score",
        "employment_years", "debt_ratio", "default_history"]
X = frame[cols].fillna(frame[cols].median()).to_numpy()
y = frame["approved"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

models = {
    "logistic": LogisticRegressionGD(lr=0.5, epochs=800),
    "tree depth=5": DecisionTreeClassifier(max_depth=5, min_samples_leaf=5),
    "tree unlimited": DecisionTreeClassifier(),
    "forest 100": RandomForestClassifier(n_estimators=100, max_depth=6, min_samples_leaf=5),
    "boosting 100": GradientBoostingClassifier(n_estimators=100, max_depth=2),
    "linear SVM": LinearSVM(C=0.5, lr=0.02, epochs=400),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    p = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else model.decision_function(X_test)
    print(f"{name:14s} train {model.score(X_train, y_train):.3f} "
          f"test {model.score(X_test, y_test):.3f} AUC {ev.roc_auc_score(y_test, p):.3f}")
```

```text
logistic       train 0.784 test 0.783 AUC 0.798
tree depth=5   train 0.801 test 0.717 AUC 0.696
tree unlimited train 1.000 test 0.679 AUC 0.597
forest 100     train 0.834 test 0.762 AUC 0.802
boosting 100   train 0.825 test 0.762 AUC 0.790
linear SVM     train 0.775 test 0.778 AUC 0.795
```

Feature importance from a forest:

```python
import datasets as ds
import numpy as np
from prep import StandardScaler, train_test_split
from classifiers import RandomForestClassifier

frame = ds.intrusion()
cols = ["duration", "src_bytes", "dst_bytes", "count", "srv_count",
        "serror_rate", "num_failed_logins", "logged_in"]
X, y = frame[cols].to_numpy(), frame["is_attack"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)
scaler = StandardScaler().fit(np.log1p(np.clip(X_train, 0, None)))
X_train = scaler.transform(np.log1p(np.clip(X_train, 0, None)))
X_test = scaler.transform(np.log1p(np.clip(X_test, 0, None)))

forest = RandomForestClassifier(n_estimators=60, max_depth=6, min_samples_leaf=5).fit(X_train, y_train)
print(dict(zip(cols, np.round(forest.feature_importances_, 3))))
print("accuracy", round(forest.score(X_test, y_test), 3))
```

```text
{'duration': 0.125, 'src_bytes': 0.016, 'dst_bytes': 0.232, 'count': 0.005,
 'srv_count': 0.007, 'serror_rate': 0.428, 'num_failed_logins': 0.142, 'logged_in': 0.044}
accuracy 0.979
```

## 8. Practical Applications

- **Credit and insurance** — gradient boosting is the workhorse, with SHAP values for adverse
  action notices.
- **Intrusion detection** — forests on flow features; per-family error analysis matters more than
  aggregate accuracy.
- **Medical diagnosis support** — shallow trees are preferred when the rule must be audited.
- **Bioinformatics** — random forests on gene expression, where $p \gg n$.
- **Handwritten digits / small images** — SVM with RBF was the pre-deep-learning standard.

## 9. Common Mistakes

1. Growing trees to purity and calling the training accuracy a result.
2. Tuning boosting rounds without the learning rate (they interact).
3. Reading impurity importance as importance to predictions. Use permutation importance.
4. Using a forest when a single shallow tree is required for auditability.
5. Forgetting to scale before an SVM or k-NN.
6. Adding models to an ensemble that share the same errors. Diversity is the point.
7. Trusting default `max_features` on very wide, sparse data without checking.

## 10. Practical Exercises

1. Compute the Gini and entropy gains for a second candidate split on the node in Example 1 and
   say which the tree would choose.
2. Fit trees with `max_depth` 1, 3, 5, 10, None. Tabulate train/test accuracy and AUC.
3. Compare forests with `max_features` = 1, √d and d on the loan data. Which decorrelation setting
   wins, and why?
4. Vary boosting `n_estimators` from 10 to 300 at a fixed learning rate. Where does test AUC stop
   improving?
5. Fit an SVM with C = 0.01, 0.1, 1, 10. Describe the margin/error trade you observe.

## 11. Self-Assessment

**Multiple choice**

1. A fully grown tree has
   a) high bias, low variance. b) low bias, high variance. c) low bias, low variance.
   d) high bias, high variance.
2. Random forests reduce variance mainly by
   a) deeper trees. b) decorrelating trees via feature subsampling. c) more features.
   d) scaling.
3. In an SVM, increasing C
   a) widens the margin. b) allows fewer margin violations. c) removes support vectors.
   d) reduces variance.
4. Gradient boosting fits each new tree to
   a) the raw labels. b) the pseudo-residuals. c) a bootstrap sample of labels. d) the features.

**Short answer**

5. Why can averaging many identical trees not reduce variance below $\sigma^2$?
6. Give one reason to prefer a shallow tree over a forest in a regulated setting.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. With $\rho=1$ the variance formula gives $\sigma^2$ regardless of $B$; averaging identical
   learners changes nothing.
6. A shallow tree is a readable rule set that can be audited and explained per decision; a forest
   of hundreds of trees cannot.

</details>

## 12. Key Terms

**CART**, **Gini impurity**, **entropy**, **information gain**, **pruning**, **bagging**,
**bootstrap sample**, **out-of-bag error**, **random forest**, **feature subsampling**,
**gradient boosting**, **shrinkage**, **pseudo-residual**, **stacking**, **support vector**,
**margin**, **hinge loss**, **soft margin**, **kernel trick**, **RBF kernel**.

## 13. Further Reading

- Breiman, L. (2001). *Random Forests*. Machine Learning 45. — The original, still the clearest.
- Friedman, J. (2001). *Greedy Function Approximation: A Gradient Boosting Machine*. Annals of
  Statistics.
- Cortes, C. & Vapnik, V. (1995). *Support-Vector Networks*. Machine Learning 20.
- Grinsztajn, L. et al. (2022). *Why do tree-based models still outperform deep learning on
  typical tabular data?* NeurIPS. — The empirical case for this lesson's defaults.

## What to Do Next

1. Run `python classifiers.py`.
2. Do exercises 2–4; the depth and rounds tables are the core of LAB-06-02.
3. Continue to [L06-09 — Unsupervised Learning and Dimensionality Reduction](L06-09-unsupervised-learning-and-dimensionality-reduction.md).

---

**Navigation:** [← Previous: ? Lesson](L06-07-k-nearest-neighbours-and-naive-bayes.md) · [Module home](../README.md) · [Next: ? Lesson →](L06-09-unsupervised-learning-and-dimensionality-reduction.md)
