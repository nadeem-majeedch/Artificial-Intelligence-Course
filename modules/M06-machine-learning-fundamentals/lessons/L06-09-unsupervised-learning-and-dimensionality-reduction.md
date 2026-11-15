# L06-09 — Unsupervised Learning: k-Means, PCA and Dimensionality Reduction

[← Previous: L06-08](L06-08-trees-forests-boosting-and-svm.md) · [Module home](../README.md) · [Next: L06-10 →](L06-10-reproducible-ml-pipelines.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Clustering and Anomaly Work](#4-the-procedure-clustering-and-anomaly-work)
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

> **Module M06** · Lesson 9 of 10 · ~100 minutes · Level 300
> **Prerequisites:** L06-02 (scaling), L06-05 (evaluation vocabulary)

[Previous: L06-08](L06-08-trees-forests-boosting-and-svm.md) · [Module overview](../README.md) · [Next: L06-10 →](L06-10-reproducible-ml-pipelines.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Run** k-means, explain each step, and choose k with more than the elbow plot.
2. **Compare** k-means with hierarchical clustering and DBSCAN, and say when each is the right
   tool.
3. **Fit** a Gaussian mixture by expectation–maximisation and explain what "soft" membership buys.
4. **Use** PCA to reduce dimensions, read the explained-variance ratios, and reconstruct.
5. **Detect** anomalies with z-scores, IQR fences and Mahalanobis distance, and report precision
   at a fixed alert budget.
6. **Validate** a clustering with an internal index, stability and domain inspection — never with
   a score alone.

## 2. Prerequisite Knowledge

Scaling (L06-02), distances, variance and covariance, and the confusion matrix vocabulary from
L06-05 (you will reuse precision/recall for anomaly detection).

## 3. Conceptual Explanation

### 3.1 k-means

Lloyd's algorithm:

```text
choose k centres (k-means++: spread them out)
repeat:
  assign each point to its nearest centre
  move each centre to the mean of its assigned points
until assignments stop changing
```

It minimises **inertia**, the within-cluster sum of squares:

$$
\sum_{k=1}^{K}\sum_{x\in C_k}\|x-\mu_k\|^2.
$$

Properties that matter:

- **Convex within each step, not globally.** Different seeds give different local optima, which
  is why `n_init=10` is standard.
- **Assumes spherical, similarly sized clusters.** It will happily cut an elongated cluster in
  half and merge two nearby round ones.
- **k must be chosen.** Inertia always falls as k rises, so "lowest inertia" chooses k = n.
- **Scale first.** Otherwise the widest feature defines the clusters.

### 3.2 Choosing k

Three signals, used together:

1. **Elbow**: plot inertia against k and look for the bend. On the customer data it falls
   620.6 → 350.3 → 211.6 → 194.8 → 184.3 for k=2…6: the drops shrink sharply after k=4, which is a
   readable elbow (though not always this clear).
2. **Silhouette**: for each point, $(b-a)/\max(a,b)$, where $a$ is the mean distance to its own
   cluster and $b$ to the nearest other cluster. Mean over points, range −1…1.
3. **Domain sense**: can you name the segments and act on them? A four-cluster solution that maps
   to "premium loyalists, regulars, lapsing, high-income low-spend" is useful even if silhouette
   prefers two.

```text
k  inertia  silhouette
2    620.6       0.580
3    350.3       0.520
4    211.6       0.539
5    194.8       0.405
6    184.3       0.330
```

Silhouette prefers k=2 here, while k=4 recovers the four planted segments and is the actionable
answer. This is not a contradiction to hide; it is the reason internal indices are advisory. The
silhouette rewards two big well-separated blobs and penalises the smaller, closer segments.

### 3.3 Hierarchical clustering

Bottom-up (agglomerative): start with each point as a cluster; repeatedly merge the closest pair.
Linkage defines cluster-to-cluster distance:

- **single** — closest pair; can chain through a bridge of points;
- **complete** — farthest pair; compact, similar-sized clusters;
- **average** — mean pairwise distance; the usual compromise.

The output is a dendrogram: cut it at a height to get any number of clusters. Cost is $O(n^2)$
memory and $O(n^3)$ time in this readable implementation, so it is for hundreds of rows, not
millions — or use it on cluster centres produced by k-means.

### 3.4 DBSCAN

Density-based: a point is a **core** point if at least `min_samples` points lie within `eps`
(including itself). Clusters are connected components of core points plus their border points.
Everything else is noise (−1).

- Finds arbitrarily shaped clusters.
- Does not need k.
- Has a noise label — often the most useful output.
- Fails when density varies: one `eps` cannot serve both dense and sparse regions.

```text
eps=0.4: 66 noise, clusters of 64, 158, 118, 94
eps=0.5: 20 noise, clusters of 76, 299, 105
eps=0.8:  0 noise, clusters of 190, 310   ← everything absorbed, no longer useful
```

The trend is the lesson: raising `eps` converts noise into clusters until the structure
disappears.

### 3.5 Gaussian mixtures and EM

A GMM models the data as a mixture of $K$ Gaussians:

$$
p(\mathbf{x}) = \sum_{k=1}^{K}\pi_k\,\mathcal{N}(\mathbf{x};\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k).
$$

**E-step**: compute responsibilities $r_{ik} = \pi_k\mathcal{N}(\mathbf{x}_i;\mu_k,\Sigma_k) /
\sum_j \pi_j\mathcal{N}(\mathbf{x}_i;\mu_j,\Sigma_j)$.
**M-step**: update $\pi_k, \mu_k, \Sigma_k$ from the responsibility-weighted moments.

Differences from k-means:

- **Soft** membership: a point can be 0.7 cluster A and 0.3 cluster B.
- **Elliptical** clusters via full covariance.
- **A likelihood**, so BIC can choose K:

```text
GMM k=2  BIC 3027.8
GMM k=3  BIC 2891.1
GMM k=4  BIC 2812.9   ← lowest
GMM k=5  BIC 2871.9
```

- Slower, and sensitive to initialisation (k-means is a common start).

### 3.6 PCA

1. Centre each column.
2. Compute the SVD: $X = U S V^\top$.
3. The columns of $V$ are the principal directions, ordered by variance $s_i^2/(n-1)$.
4. Project onto the first $k$: $Z = X V_{:,1:k}$.

What it is and is not:

- It finds **linear** directions of maximum variance, **not** the directions most useful for
  predicting $y$. A low-variance direction can be the discriminative one.
- It requires scaling when features have different units; otherwise it is a units artefact.
- Components are orthogonal but often uninterpretable; a loading plot helps.
- Reconstruction error is a valid anomaly score: a point that cannot be rebuilt from k components
  is unlike the training population.

On the customer data:

```text
explained variance ratio: [0.870 0.066 0.035 0.028]
2 components keep 93.7%
3 components keep 97.2%
```

One component carries 87% because income, spend, recency and frequency move together in this
synthetic data. That is a finding about the data, not a general law.

### 3.7 Dimensionality reduction beyond PCA

- **t-SNE / UMAP**: non-linear embeddings for visualisation. Preserve local neighbourhoods
  beautifully and global distances poorly. Never read cluster sizes or distances off a t-SNE plot,
  and never use it as a preprocessing step for a supervised model without checking.
- **Feature selection** (L06-02) is often better than projection when interpretability matters.
- **Autoencoders** (M07) learn non-linear compression.

### 3.8 Anomaly detection

| Method | Assumption | Weakness |
| :--- | :--- | :--- |
| z-score, any feature > 3σ | roughly Gaussian, one population | over-flags skewed tails |
| IQR fence | robust to skew | flags too many on heavy tails |
| Mahalanobis | elliptical, correlated features | needs enough rows to estimate covariance |
| Isolation forest / autoencoder | anomalies are few and different | harder to explain |

Evaluate with the same discipline as a classifier: precision and recall at the alert budget, not
accuracy. On the transaction data (0.8% fraud):

```text
z > 3           73 flags   precision 0.438   recall 0.821
IQR k=1.5      932 flags   precision 0.042   recall 1.000
Mahalanobis top 25         precision 0.920   recall 0.590
Mahalanobis top 50         precision 0.680   recall 0.872
```

The IQR fence catches every fraud and buries the reviewer in 932 alerts. Mahalanobis at 25 alerts
is a process someone can actually run. "Best" depends on capacity.

## 4. The Procedure: Clustering and Anomaly Work

1. Scale features; drop identifiers and constants.
2. Look at the data: pair plots or a PCA projection. Never cluster blind.
3. Run k-means for a range of k; record inertia and silhouette.
4. Run DBSCAN at two or three `eps` values; inspect the noise fraction.
5. Fit a GMM if soft membership or elliptical clusters are plausible; use BIC to shortlist K.
6. **Profile every cluster**: means, medians, sizes, and a business label you can defend.
7. Check stability: re-run with different seeds and a bootstrap sample; do the same segments
   reappear?
8. For anomalies, fix the alert budget first, then choose the method and threshold that maximise
   precision at that budget.
9. Validate with domain expertise. A clustering nobody can name is a clustering nobody will use.

## 5. Worked Examples

### Example 1 — One k-means iteration by hand

Points A(1,1), B(2,1), C(8,8), D(9,8); initial centres A and C.

- Assign: A→C1 (distance 0), B→C1 (1), C→C2 (0), D→C2 (1).
- Update: C1 = (1.5, 1), C2 = (8.5, 8).
- Re-assign: unchanged. Converged.
- Inertia: $0.5+0.5+0.5+0.5 = 2.0$.

The final centres are the means of their members, which is why k-means is sometimes described as
"alternating means".

### Example 2 — The four customer segments

At k=4 the algorithm recovers the planted structure exactly (sizes 80, 170, 110, 140):

```text
c0: income 55.3  spending 11.9  recency 53.7  frequency  6.2
c1: income 88.3  spending 80.8  recency 12.7  frequency 21.9
c2: income 32.2  spending 23.9  recency 94.8  frequency  3.4
c3: income 66.4  spending 58.1  recency 31.5  frequency 12.0
```

Names a marketing team can act on: c1 premium loyalists (recent, frequent, high spend), c2
lapsing low-value (old, rare, low spend), c3 steady regulars, c0 high income but low spend
(upsell target). The naming is the deliverable; the labels are not.

### Example 3 — PCA before and after scaling

PCA on unscaled customer data is dominated by `monetary_value` because its variance is in the
thousands while `spending_score` is in the tens. After standardisation, the first component is a
balanced contrast of the four behavioural features and explains 87%. Same algorithm, different
question — which is why "PCA found one factor" is meaningless without stating the preprocessing.

## 6. Mathematical Formulation

**Inertia** as in §3.1. **Silhouette**:

$$
s(i) = \frac{b(i)-a(i)}{\max\{a(i),b(i)\}}.
$$

**EM updates** for a GMM:

$$
r_{ik} = \frac{\pi_k \mathcal{N}(x_i;\mu_k,\Sigma_k)}{\sum_j \pi_j \mathcal{N}(x_i;\mu_j,\Sigma_j)},
\quad
\pi_k = \frac{1}{n}\sum_i r_{ik},
\quad
\mu_k = \frac{\sum_i r_{ik}x_i}{\sum_i r_{ik}},
$$

$$
\Sigma_k = \frac{\sum_i r_{ik}(x_i-\mu_k)(x_i-\mu_k)^\top}{\sum_i r_{ik}}.
$$

**BIC**: $-2\log\hat L + p\log n$, where $p$ counts free parameters; lower is better.

**PCA** via covariance eigen-decomposition: $\Sigma = V\Lambda V^\top$, with
$\lambda_i = s_i^2/(n-1)$ and explained-variance ratio $\lambda_i/\sum_j\lambda_j$.

**Mahalanobis distance**: $d^2(x) = (x-\mu)^\top\Sigma^{-1}(x-\mu)$.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import numpy as np
import datasets as ds
from prep import StandardScaler
from unsupervised import KMeans, silhouette_score, PCA, GaussianMixture

frame = ds.customers()
cols = ["annual_income_k", "spending_score", "recency_days", "purchase_frequency"]
X = StandardScaler().fit_transform(frame[cols].to_numpy())

for k in range(2, 7):
    model = KMeans(k, seed=0).fit(X)
    print(f"k={k} inertia {model.inertia_:8.1f} silhouette {silhouette_score(X, model.labels_):.3f}")

best = KMeans(4, seed=0).fit(X)
print("sizes:", np.bincount(best.labels_).tolist())
for k in range(4):
    profile = frame[cols].to_numpy()[best.labels_ == k].mean(axis=0)
    print(f" c{k}: " + " ".join(f"{n}={v:.1f}" for n, v in zip(cols, profile)))

pca = PCA().fit(X)
print("ratios:", np.round(pca.explained_variance_ratio_, 3))
print("2 components keep:", round(float(pca.explained_variance_ratio_[:2].sum()), 3))
```

```text
k=2 inertia    620.6 silhouette 0.580
k=3 inertia    350.3 silhouette 0.520
k=4 inertia    211.6 silhouette 0.539
k=5 inertia    194.8 silhouette 0.405
k=6 inertia    184.3 silhouette 0.330
sizes: [80, 170, 110, 140]
 c0: annual_income_k=55.3 spending_score=11.9 recency_days=53.7 purchase_frequency=6.2
 c1: annual_income_k=88.3 spending_score=80.8 recency_days=12.7 purchase_frequency=21.9
 c2: annual_income_k=32.2 spending_score=23.9 recency_days=94.8 purchase_frequency=3.4
 c3: annual_income_k=66.4 spending_score=58.1 recency_days=31.5 purchase_frequency=12.0
ratios: [0.87  0.066 0.035 0.028]
2 components keep: 0.937
```

Anomaly detection:

```python
import numpy as np
import datasets as ds
from prep import StandardScaler
from unsupervised import zscore_anomalies, iqr_anomalies, mahalanobis_scores

frame = ds.transactions()
cols = ["amount", "distance_from_home_km", "ratio_to_median_spend", "attempts_last_hour"]
X = StandardScaler().fit_transform(np.log1p(frame[cols].to_numpy()))

flag = zscore_anomalies(X, 3.0)
print("z>3:", int(flag.sum()), "precision", round(frame.loc[flag, "is_fraud"].mean(), 3),
      "recall", round(frame.loc[flag, "is_fraud"].sum() / frame["is_fraud"].sum(), 3))

scores = mahalanobis_scores(X)
for budget in [25, 50, 100]:
    idx = np.argsort(-scores)[:budget]
    print(budget, "precision", round(frame.iloc[idx]["is_fraud"].mean(), 3),
          "recall", round(frame.iloc[idx]["is_fraud"].sum() / frame["is_fraud"].sum(), 3))
```

```text
z>3: 73 precision 0.438 recall 0.821
25 precision 0.92 recall 0.59
50 precision 0.68 recall 0.872
100 precision 0.37 recall 0.949
```

## 8. Practical Applications

- **Customer segmentation** — RFM features, four to eight segments, named by the business.
- **Document clustering** — k-means on TF-IDF or embeddings for topic discovery.
- **Image compression** — keep 50 of 784 principal components; reconstruct with small loss.
- **Predictive maintenance** — Mahalanobis or autoencoder reconstruction error per machine.
- **Fraud triage** — rank by anomaly score, review top-N, measure precision at N.
- **Quality control** — DBSCAN's noise label as "inspect this part".

## 9. Common Mistakes

1. Clustering unscaled features and reporting the result.
2. Choosing k by the elbow alone (or by inertia, which always prefers more clusters).
3. Reading t-SNE distances as real distances.
4. Treating cluster labels as ground truth and training a classifier on them without scepticism.
5. Using a high-variance PCA projection when the discriminative signal is low-variance.
6. Reporting anomaly-detection accuracy on 0.8% positives.
7. Forgetting that GMM needs a likelihood check — non-convergence produces nonsense silently.

## 10. Practical Exercises

1. Reproduce the k=2…6 table. Which k does silhouette choose, and which k recovers the planted
   segments?
2. Standardise, then run k-means with k=4 using seeds 0–4. Do the cluster sizes vary? What does
   that say about stability?
3. Run DBSCAN with `eps` from 0.3 to 1.0 and plot the noise fraction against `eps`.
4. Project the customer data onto two components and reconstruct. Report the mean squared
   reconstruction error.
5. On the transaction data, compute precision and recall at budgets 10, 25, 50, 100 and 200.
   Recommend a budget for a team that can review 30 alerts per day.

## 11. Self-Assessment

**Multiple choice**

1. k-means minimises
   a) the likelihood. b) within-cluster sum of squares. c) the silhouette. d) BIC.
2. Silhouette ranges from
   a) 0 to 1. b) −1 to 1. c) 0 to ∞. d) −∞ to ∞.
3. DBSCAN labels sparse points as
   a) 0. b) −1. c) NaN. d) a new cluster.
4. A GMM differs from k-means because it
   a) needs no scaling. b) gives soft memberships and elliptical clusters. c) always finds the
   global optimum. d) needs no K.

**Short answer**

5. Why is inertia unsuitable for choosing k?
6. Why does PCA require standardisation when features have different units?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. It decreases monotonically as k grows, reaching zero at k = n, so it rewards complexity rather
   than structure.
6. PCA maximises variance, and variance is unit-dependent: a column measured in thousands
   dominates one measured in tens regardless of information content.

</details>

## 12. Key Terms

**Clustering**, **k-means**, **inertia**, **k-means++**, **silhouette**, **agglomerative
clustering**, **linkage**, **dendrogram**, **DBSCAN**, **core point**, **noise point**,
**Gaussian mixture**, **expectation–maximisation**, **responsibility**, **BIC**, **PCA**,
**principal component**, **explained variance**, **t-SNE**, **UMAP**, **anomaly detection**,
**Mahalanobis distance**, **isolation forest**.

## 13. Further Reading

- MacQueen, J. (1967). *Some Methods for Classification and Analysis of Multivariate
  Observations*. — The origin of k-means.
- Ester, M. et al. (1996). *A Density-Based Algorithm for Discovering Clusters in Large Spatial
  Databases with Noise*. KDD. — DBSCAN.
- Jolliffe, I. (2002). *Principal Component Analysis*, 2nd ed.
- von Luxburg, U. et al. (2012). *Clustering: Science or Art?* — Why internal indices cannot
  decide for you.

## What to Do Next

1. Run `python unsupervised.py`.
2. Do exercises 1 and 5; both feed LAB-06-03.
3. Continue to [L06-10 — Reproducible ML Pipelines](L06-10-reproducible-ml-pipelines.md).

---

**Navigation:** [← Previous: L06-08](L06-08-trees-forests-boosting-and-svm.md) · [Module home](../README.md) · [Next: L06-10 →](L06-10-reproducible-ml-pipelines.md)
