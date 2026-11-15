# L06-07 — k-Nearest Neighbours and Naïve Bayes

[← Previous: L06-06](L06-06-bias-variance-and-regularisation.md) · [Module home](../README.md) · [Next: L06-08 →](L06-08-trees-forests-boosting-and-svm.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Choosing Between Them](#4-the-procedure-choosing-between-them)
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

> **Module M06** · Lesson 7 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-04, L06-05, P03 (Bayes' theorem)

[Previous: L06-06](L06-06-bias-variance-and-regularisation.md) · [Module overview](../README.md) · [Next: L06-08 →](L06-08-trees-forests-boosting-and-svm.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** k-NN as a memorising estimator: what `fit` does, where the cost lives, and why
   scaling is not optional.
2. **Choose** k and a distance metric, and explain the bias–variance effect of each.
3. **State** why k-NN degrades in high dimensions and what that means for feature selection.
4. **Derive** Gaussian and multinomial naïve Bayes from Bayes' theorem plus the conditional
   independence assumption.
5. **Explain** Laplace smoothing and why it is required for unseen categories.
6. **Compare** both models with logistic regression on the same spam task and explain the
   differences in accuracy, precision, recall and training cost.

## 2. Prerequisite Knowledge

Bayes' theorem, conditional probability, and the normal distribution's density function. If
$P(A\mid B) = P(B\mid A)P(A)/P(B)$ is not automatic for you, revise P03 first.

## 3. Conceptual Explanation

### 3.1 k-NN: the model is the data

Training is one line: store the rows. Prediction finds the k closest training points and takes a
majority vote (or the mean, for regression).

```text
new point x
 ├── compute distance to every training point
 ├── take the k smallest
 └── predict the majority label among them (or average the labels)
```

Consequences follow directly:

- **No training cost, all the cost at prediction.** Fitting is $O(nd)$; predicting one point is
  $O(nd)$; predicting the test set is $O(n_{test}\,n\,d)$. For a million rows this is why
  approximate nearest-neighbour indexes exist.
- **Non-parametric.** The decision boundary can be arbitrarily curved, so bias is low and
  variance is high, especially for small k.
- **Scaling is mandatory.** Distance is dominated by whichever feature has the largest numeric
  range. A salary in dollars and an age in years without scaling makes the model a salary
  classifier.
- **It cannot extrapolate.** Outside the training cloud, the nearest neighbours are far away and
  the prediction is whatever the edge of the data says.

### 3.2 Choosing k

| k | Effect |
| ---: | :--- |
| 1 | boundary follows every point; zero training error, high variance |
| 5–15 | typical starting range; smooths noise without erasing structure |
| large | approaches the global class frequency; high bias |

Odd k avoids ties in binary problems. Use cross-validation; do not guess.

On the spam data (scaled features, 300 test rows):

```text
  k   accuracy  precision  recall     AUC
  1      0.963      0.951   0.812   0.902
  3      0.950      0.902   0.771   0.940
  5      0.950      0.923   0.750   0.963
 15      0.960      1.000   0.750   0.985
 35      0.957      1.000   0.729   0.991
 75      0.943      1.000   0.646   0.990
```

Accuracy is almost flat from k=1 to k=75 (0.94–0.96), while AUC rises steadily and recall falls:
larger k produces smoother, better-ranked probabilities but a more conservative 0.5 decision.
This is a threshold effect as much as a k effect — the ranking improves while the default cut
flags fewer emails.

Distance-weighted voting (`weights="distance"`) helps when neighbours are unevenly spaced: a
point at distance 0.1 should outvote one at distance 4.

### 3.3 The curse of dimensionality

As dimensions grow, distances concentrate: the ratio of the nearest to the farthest distance
approaches 1, so "nearest" stops meaning anything, and you need exponentially more data to keep
the same local density. With 8 features k-NN is fine; with 800, it is not, unless the data lie
on a lower-dimensional manifold (which is what embeddings exploit). Practical responses: select
features, reduce with PCA, or use a model that learns a representation.

### 3.4 Naïve Bayes: Bayes' theorem with a strong assumption

For features $\mathbf{x} = (x_1,\dots,x_d)$ and class $y$:

$$
P(y\mid\mathbf{x}) = \frac{P(\mathbf{x}\mid y)P(y)}{P(\mathbf{x})}
\;\propto\; P(y)\prod_{j=1}^{d}P(x_j\mid y),
$$

where the last step **assumes the features are independent given the class**. That assumption is
almost always false — the words "free" and "winner" co-occur in spam — yet the classifier often
works, because classification only needs the argmax to be right, not the probabilities to be
calibrated.

- **Gaussian NB**: each feature is normal within each class,
  $P(x_j\mid y) = \mathcal{N}(x_j;\mu_{jy},\sigma_{jy}^2)$. Two parameters per feature per class.
- **Multinomial NB**: features are counts (word frequencies), with a categorical likelihood and
  Laplace smoothing $\alpha$: counts become count $+\alpha$.

Everything is done in log space to avoid underflow: adding 20 log-probabilities of −30 each is
fine; multiplying 20 numbers of $10^{-13}$ is not.

### 3.5 Laplace smoothing

Without smoothing, an unseen word in a spam email gives $P(\text{word}\mid\text{spam})=0$, and
the product — and the posterior — collapses to zero regardless of all other evidence. Add
$\alpha$ (usually 1) to every count before normalising:

$$
\hat P(w\mid c) = \frac{\text{count}(w,c)+\alpha}{\sum_{w'}\text{count}(w',c)+\alpha|V|}.
$$

This is not a hack; it is a Dirichlet prior, and it is the difference between a model that
crashes on new vocabulary and one that handles it gracefully.

### 3.6 Why it still works

The independence assumption distorts the posterior probabilities, often pushing them toward 0 or
1. If you need calibrated probabilities for expected cost, recalibrate (Platt scaling or
isotonic regression) or use logistic regression. If you need a fast, interpretable, tiny-memory
classifier on text, naïve Bayes is still a strong baseline — and it trains in one pass.

## 4. The Procedure: Choosing Between Them

1. Scale the features if you use k-NN (and for Gaussian NB it does not change the fit, since the
   likelihood is fitted per feature).
2. For k-NN, choose k and the metric by CV; start with Euclidean and k≈√n.
3. Use distance weighting if density varies.
4. For NB, choose Gaussian for continuous features, multinomial for counts, Bernoulli for
   presence/absence.
5. Smooth (α ≥ 1) whenever a feature value can be unseen.
6. Compare with a linear baseline on the same folds; report AUC and precision/recall, not just
   accuracy.
7. Check the training score against the test score: NB usually has a small gap (low variance);
   k-NN with k=1 has a large one.

## 5. Worked Examples

### Example 1 — A k-NN vote by hand

Two classes, five training points in two dimensions, $k=3$:

| Point | $x_1$ | $x_2$ | Class |
| :--- | ---: | ---: | :--- |
| A | 0 | 0 | 0 |
| B | 1 | 0 | 0 |
| C | 0 | 1 | 1 |
| D | 3 | 3 | 1 |
| E | 3 | 0 | 1 |

Query $q=(1,1)$. Squared Euclidean distances: A 5, B 1, C 1, D 8, E 5. The three nearest are
B, C (distance 1) and then A or E (distance 5) — a tie. With k=3 you must break it (distance
weighting, or a deterministic rule). With k=5 the vote is 3 class-1 vs 2 class-0, so the
prediction is class 1. This is why ties and even k are worth thinking about before you are
surprised by them.

### Example 2 — Spam, three models

```text
model        accuracy  precision  recall     AUC
GaussianNB      0.970      0.855   0.979   0.994
kNN k=5         0.950      0.923   0.750   0.963
logistic        0.983      0.939   0.958   0.998
```

Naïve Bayes has the best recall and the worst precision: it flags aggressively. k-NN at k=5 has
the best precision of the three but misses a quarter of the spam at the 0.5 threshold. Logistic
regression dominates here because the synthetic features are close to linearly separable in
log-odds space — which is a property of this dataset, not a universal law.

The NB train/test gap is 0.974 → 0.970: four thousandths. That is the low-variance signature of
a model with a handful of parameters per feature.

### Example 3 — The independence assumption, concretely

In spam, $P(\text{"free"}\mid\text{spam})$ and $P(\text{"winner"}\mid\text{spam})$ are both
high, and they co-occur far more often than independence would predict. NB multiplies them as if
independent, so it **overcounts** the evidence and produces probabilities closer to 0 and 1 than
the truth. The ranking usually survives; the calibration does not.

## 6. Mathematical Formulation

**Euclidean distance** and the general Minkowski family:

$$
d(\mathbf{x},\mathbf{z}) = \Big(\sum_j |x_j-z_j|^p\Big)^{1/p},
\qquad p=2 \text{ (Euclidean)}, \; p=1 \text{ (Manhattan)}.
$$

**k-NN prediction** (uniform weights):

$$
\hat y = \arg\max_{c}\sum_{i\in N_k(\mathbf{x})}\mathbb{1}[y_i = c].
$$

**Bayes decision rule**:

$$
\hat y = \arg\max_c\; \log P(y=c) + \sum_j \log P(x_j\mid y=c).
$$

**Gaussian log-likelihood**:

$$
\log P(x_j\mid y=c) = -\tfrac12\log(2\pi\sigma_{jc}^2) - \frac{(x_j-\mu_{jc})^2}{2\sigma_{jc}^2}.
$$

**Smoothed multinomial estimate** as in §3.5.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import datasets as ds
from prep import StandardScaler, train_test_split
from classifiers import KNNClassifier, GaussianNB
import evaluation as ev

frame = ds.emails()
cols = ["word_count", "num_links", "uppercase_words", "exclamation_marks",
        "has_attachment", "sender_known", "hour_sent", "contains_free"]
X, y = frame[cols].to_numpy(), frame["is_spam"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

for k in [1, 5, 15, 35]:
    model = KNNClassifier(k=k).fit(X_train, y_train)
    p = model.predict_proba(X_test)[:, 1]
    print(f"k={k:2d} acc {model.score(X_test, y_test):.3f} "
          f"P {ev.precision(y_test, (p >= .5).astype(int)):.3f} "
          f"R {ev.recall(y_test, (p >= .5).astype(int)):.3f} "
          f"AUC {ev.roc_auc_score(y_test, p):.3f}")

nb = GaussianNB().fit(X_train, y_train)
p = nb.predict_proba(X_test)[:, 1]
print(f"NB   acc {nb.score(X_test, y_test):.3f} "
      f"P {ev.precision(y_test, (p >= .5).astype(int)):.3f} "
      f"R {ev.recall(y_test, (p >= .5).astype(int)):.3f} "
      f"AUC {ev.roc_auc_score(y_test, p):.3f}")
print("NB train accuracy:", round(nb.score(X_train, y_train), 3))
```

```text
k= 1 acc 0.963 P 0.951 R 0.812 AUC 0.902
k= 5 acc 0.950 P 0.923 R 0.750 AUC 0.963
k=15 acc 0.960 P 1.000 R 0.750 AUC 0.985
k=35 acc 0.957 P 1.000 R 0.729 AUC 0.991
NB   acc 0.970 P 0.855 R 0.979 AUC 0.994
NB train accuracy: 0.974
```

Fitting NB from the formulas directly, to show there is no hidden step:

```python
import numpy as np

mu = X_train[y_train == 1].mean(axis=0)
var = X_train[y_train == 1].var(axis=0) + 1e-9
log_prior = np.log(y_train.mean())
# log P(x | spam) for the first test row
row = X_test[0]
ll = -0.5 * np.sum(np.log(2 * np.pi * var) + (row - mu) ** 2 / var)
print("first row, log P(x|spam) + log P(spam):", round(float(ll + log_prior), 2))
```

## 8. Practical Applications

- **Text classification** — multinomial NB for spam, topic tagging, language identification.
- **Medical triage** — Gaussian NB as a fast baseline on vitals and labs.
- **Recommendation cold start** — item-based nearest neighbours before enough interaction data
  exists.
- **Anomaly screening** — k-NN distance to the k-th neighbour is itself an anomaly score
  (L06-09).
- **Embedded systems** — NB's tiny parameter count fits in kilobytes.

## 9. Common Mistakes

1. Using k-NN without scaling. Distance is dominated by the widest column.
2. Choosing k=1 because training accuracy is perfect.
3. Comparing k-NN training time to other models' training time and concluding it is cheap.
   Measure prediction time on the deployment batch.
4. Applying Gaussian NB to counts and multinomial NB to continuous features.
5. Using NB probabilities as if calibrated in an expected-cost calculation.
6. Forgetting smoothing, then blaming the model for a zero probability on new vocabulary.
7. Using k-NN on 200 sparse text features without reduction and expecting it to work.

## 10. Practical Exercises

1. Reproduce the k sweep. Which k would you choose for a spam filter that must keep precision
   above 0.95? Which for one that must keep recall above 0.9?
2. Repeat the k sweep without scaling. Report the accuracy at k=5 and explain the change.
3. Implement distance-weighted voting and compare AUC at k=15.
4. Compute Gaussian NB's parameters by hand for one feature (mean, variance per class) and verify
   against the fitted model.
5. Derive the log-space prediction for a 2-feature, 2-class problem with priors 0.3/0.7.

## 11. Self-Assessment

**Multiple choice**

1. k-NN's main cost is at a) training. b) prediction. c) preprocessing only. d) none.
2. Increasing k generally
   a) increases variance. b) decreases variance and increases bias. c) changes the metric.
   d) removes the need for scaling.
3. Naïve Bayes assumes
   a) Gaussian features. b) conditional independence of features given the class.
   c) balanced classes. d) linear decision boundaries.
4. Laplace smoothing is needed because
   a) counts are large. b) unseen feature values give zero likelihood. c) classes are imbalanced.
   d) features are correlated.

**Short answer**

5. Why does k-NN fail in very high dimensions?
6. NB has 0.974 train and 0.970 test accuracy. What does that gap tell you?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Distances concentrate, so nearest neighbours are barely nearer than distant points and local
   density estimates become meaningless without exponentially more data.
6. Very low variance — the model is not memorising. The remaining error is bias or noise, so more
   data will not help much; better features or a richer model might.

</details>

## 12. Key Terms

**k-nearest neighbours**, **distance metric**, **Euclidean distance**, **Manhattan distance**,
**curse of dimensionality**, **lazy learner**, **distance weighting**, **naïve Bayes**,
**conditional independence**, **prior**, **likelihood**, **posterior**, **Gaussian NB**,
**multinomial NB**, **Laplace smoothing**, **log-space computation**, **calibration**.

## 13. Further Reading

- Cover, T. & Hart, P. (1967). *Nearest Neighbor Pattern Classification*. IEEE Transactions on
  Information Theory. — The original consistency result.
- Rish, I. (2001). *An Empirical Study of the Naïve Bayes Classifier*. IJCAI workshop. — Why a
  wrong assumption still classifies well.
- Manning, Raghavan & Schütze (2008). *Introduction to Information Retrieval*, Chapter 13. — NB
  for text, with smoothing.

## What to Do Next

1. Run `python classifiers.py` and `python datasets.py`.
2. Do exercises 1–2; the unscaled comparison is the point.
3. Continue to [L06-08 — Trees, Forests, Boosting and SVMs](L06-08-trees-forests-boosting-and-svm.md).

---

**Navigation:** [← Previous: L06-06](L06-06-bias-variance-and-regularisation.md) · [Module home](../README.md) · [Next: L06-08 →](L06-08-trees-forests-boosting-and-svm.md)
