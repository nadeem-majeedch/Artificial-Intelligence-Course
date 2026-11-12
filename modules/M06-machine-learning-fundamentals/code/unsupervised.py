"""Unsupervised learning from scratch: clustering, density, mixtures, PCA, anomalies.

Clustering has no labels, so "did it work?" is a different question than in supervised
learning. This module therefore ships two internal indices (inertia and silhouette) and
a habit: always look at the cluster profiles, not just the number of clusters.

Run `python unsupervised.py` to reproduce the numbers used in L06-09 and LAB-06-03.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "KMeans",
    "AgglomerativeClustering",
    "DBSCAN",
    "GaussianMixture",
    "PCA",
    "silhouette_score",
    "inertia",
    "zscore_anomalies",
    "iqr_anomalies",
    "mahalanobis_scores",
]


def _check_X(X):
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    return X


# ---------------------------------------------------------------------------
# k-means
# ---------------------------------------------------------------------------
class KMeans:
    """Lloyd's algorithm with k-means++ seeding.

    1. Choose k initial centres, each new one sampled with probability proportional to
       its squared distance from the closest chosen centre (k-means++).
    2. Assign every point to its nearest centre.
    3. Move each centre to the mean of its points.
    4. Repeat until assignments stop changing.

    The objective (inertia) never increases, but it is not convex: different seeds can
    converge to different local optima, which is why `n_init > 1` is the default.
    """

    def __init__(self, n_clusters: int = 3, n_init: int = 10, max_iter: int = 300, seed: int = 0):
        self.n_clusters = n_clusters
        self.n_init = n_init
        self.max_iter = max_iter
        self.seed = seed
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = 0

    def _init_centres(self, X, rng):
        n = len(X)
        centres = [X[rng.integers(n)]]
        for _ in range(1, self.n_clusters):
            d2 = np.min(
                np.sum((X[:, None, :] - np.array(centres)[None, :, :]) ** 2, axis=2), axis=1
            )
            total = d2.sum()
            probs = d2 / total if total > 0 else np.full(n, 1.0 / n)
            centres.append(X[rng.choice(n, p=probs)])
        return np.array(centres)

    def fit(self, X):
        X = _check_X(X)
        rng = np.random.default_rng(self.seed)
        best = None
        for _ in range(self.n_init):
            centres = self._init_centres(X, rng)
            for iteration in range(1, self.max_iter + 1):
                distances = np.sum((X[:, None, :] - centres[None, :, :]) ** 2, axis=2)
                labels = np.argmin(distances, axis=1)
                new_centres = np.array(
                    [X[labels == k].mean(axis=0) if np.any(labels == k) else centres[k]
                     for k in range(self.n_clusters)]
                )
                if np.allclose(new_centres, centres):
                    break
                centres = new_centres
            # Inertia: sum over points of the squared distance to the assigned centre.
            # (Sum over features first, then take the minimum over clusters.)
            score = float(np.sum(np.min(distances, axis=1)))
            if best is None or score < best[0]:
                best = (score, centres, labels, iteration)
        self.inertia_, self.cluster_centers_, self.labels_, self.n_iter_ = best
        return self

    def predict(self, X):
        X = _check_X(X)
        distances = np.sum((X[:, None, :] - self.cluster_centers_[None, :, :]) ** 2, axis=2)
        return np.argmin(distances, axis=1)

    def fit_predict(self, X):
        return self.fit(X).labels_


def inertia(X, labels, centres) -> float:
    """Within-cluster sum of squares. Always falls as k grows, so never choose k by it."""
    X = _check_X(X)
    return float(sum(np.sum((X[labels == k] - centres[k]) ** 2) for k in np.unique(labels)))


# ---------------------------------------------------------------------------
# Hierarchical clustering
# ---------------------------------------------------------------------------
class AgglomerativeClustering:
    """Bottom-up clustering: start with every point alone, merge the closest pair.

    Linkage decides what "closest" means between two groups:
      * single   — closest pair of members (chains, can bridge distinct groups)
      * complete — farthest pair (compact, equal-sized clusters)
      * average  — mean pairwise distance (a compromise, the usual default)

    O(n^3) in this readable implementation; real libraries use a priority queue. Keep
    n small when you use it for teaching.
    """

    def __init__(self, n_clusters: int = 2, linkage: str = "average"):
        if linkage not in {"single", "complete", "average"}:
            raise ValueError("linkage must be single, complete or average")
        self.n_clusters = n_clusters
        self.linkage = linkage
        self.labels_ = None
        self.merges_ = []

    def _cluster_distance(self, A, B):
        d = np.sqrt(np.sum((A[:, None, :] - B[None, :, :]) ** 2, axis=2))
        if self.linkage == "single":
            return float(d.min())
        if self.linkage == "complete":
            return float(d.max())
        return float(d.mean())

    def fit(self, X):
        X = _check_X(X)
        n = len(X)
        clusters = {i: [i] for i in range(n)}
        distances = {}
        for i in range(n):
            for j in range(i + 1, n):
                distances[(i, j)] = float(np.linalg.norm(X[i] - X[j]))

        next_id = n
        self.merges_ = []
        while len(clusters) > self.n_clusters:
            best_pair, best_distance = None, np.inf
            ids = list(clusters)
            for a in range(len(ids)):
                for b in range(a + 1, len(ids)):
                    i, j = ids[a], ids[b]
                    if (i, j) in distances:
                        dist = distances[(i, j)]
                    elif (j, i) in distances:
                        dist = distances[(j, i)]
                    else:
                        dist = self._cluster_distance(X[clusters[i]], X[clusters[j]])
                    if dist < best_distance:
                        best_distance, best_pair = dist, (i, j)

            i, j = best_pair
            clusters[next_id] = clusters[i] + clusters[j]
            self.merges_.append((i, j, best_distance, len(clusters[next_id])))
            del clusters[i], clusters[j]
            next_id += 1

        labels = np.empty(n, dtype=int)
        for label, (_, members) in enumerate(sorted(clusters.items())):
            labels[members] = label
        self.labels_ = labels
        return self


# ---------------------------------------------------------------------------
# DBSCAN
# ---------------------------------------------------------------------------
class DBSCAN:
    """Density-based clustering: grow clusters from dense neighbourhoods.

    A point is a *core* point if at least `min_samples` points (including itself) lie
    within `eps`. Clusters are connected components of core points plus their border
    points. Everything else is noise (-1).

    This is the algorithm to reach for when clusters are not spherical and the number
    of clusters is unknown — but eps is a hard threshold, and it does not adapt to
    varying density.
    """

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels_ = None
        self.core_sample_indices_ = None

    def fit(self, X):
        X = _check_X(X)
        n = len(X)
        distances = np.sqrt(np.maximum(
            np.sum(X**2, axis=1)[:, None] - 2 * X @ X.T + np.sum(X**2, axis=1)[None, :], 0
        ))
        neighbours = [np.flatnonzero(distances[i] <= self.eps) for i in range(n)]
        core = np.array([len(nb) >= self.min_samples for nb in neighbours])

        labels = np.full(n, -1, dtype=int)
        cluster = 0
        for i in range(n):
            if not core[i] or labels[i] != -1:
                continue
            labels[i] = cluster
            queue = list(neighbours[i])
            while queue:
                j = queue.pop()
                if labels[j] == -1:
                    labels[j] = cluster
                    if core[j]:
                        queue.extend(neighbours[j])
            cluster += 1

        self.labels_ = labels
        self.core_sample_indices_ = np.flatnonzero(core)
        return self


# ---------------------------------------------------------------------------
# Gaussian mixture model
# ---------------------------------------------------------------------------
class GaussianMixture:
    """Expectation-Maximisation for a mixture of full-covariance Gaussians.

    E-step: responsibilities r_ik ∝ pi_k * N(x_i; mu_k, Sigma_k)
    M-step: mu_k, Sigma_k and pi_k become responsibility-weighted moments.

    Unlike k-means, membership is soft and clusters may be elliptical. The likelihood
    is non-decreasing under each step, which is why the log-likelihood trace is the
    honest convergence check.
    """

    def __init__(self, n_components: int = 3, max_iter: int = 200, tol: float = 1e-6, seed: int = 0):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.seed = seed
        self.weights_ = None
        self.means_ = None
        self.covariances_ = None
        self.log_likelihood_history_ = []

    def _log_gaussian(self, X, mean, cov):
        d = X.shape[1]
        cov = cov + 1e-6 * np.eye(d)          # jitter keeps the covariance invertible
        sign, logdet = np.linalg.slogdet(cov)
        diff = X - mean
        maha = np.sum(diff @ np.linalg.inv(cov) * diff, axis=1)
        return -0.5 * (d * np.log(2 * np.pi) + logdet + maha)

    def fit(self, X):
        X = _check_X(X)
        n, d = X.shape
        rng = np.random.default_rng(self.seed)

        kmeans = KMeans(self.n_components, n_init=5, seed=self.seed).fit(X)
        self.means_ = kmeans.cluster_centers_.copy()
        self.covariances_ = np.array([np.cov(X.T) + 1e-3 * np.eye(d) for _ in range(self.n_components)])
        self.weights_ = np.full(self.n_components, 1.0 / self.n_components)
        self.log_likelihood_history_ = []

        prev_ll = -np.inf
        for _ in range(self.max_iter):
            # E-step: log responsibilities, normalised with log-sum-exp.
            weighted = np.column_stack([
                np.log(self.weights_[k] + 1e-12) + self._log_gaussian(X, self.means_[k], self.covariances_[k])
                for k in range(self.n_components)
            ])
            top = weighted.max(axis=1, keepdims=True)
            log_norm = top + np.log(np.sum(np.exp(weighted - top), axis=1, keepdims=True))
            log_resp = weighted - log_norm
            resp = np.exp(log_resp)
            ll = float(np.sum(log_norm))
            self.log_likelihood_history_.append(ll)

            # M-step: weighted moments.
            nk = resp.sum(axis=0)
            self.weights_ = nk / n
            self.means_ = (resp.T @ X) / nk[:, None]
            for k in range(self.n_components):
                diff = X - self.means_[k]
                self.covariances_[k] = (resp[:, k, None] * diff).T @ diff / nk[k] + 1e-6 * np.eye(d)

            if abs(ll - prev_ll) < self.tol:
                break
            prev_ll = ll
        return self

    def predict_proba(self, X):
        X = _check_X(X)
        weighted = np.column_stack([
            np.log(self.weights_[k] + 1e-12) + self._log_gaussian(X, self.means_[k], self.covariances_[k])
            for k in range(self.n_components)
        ])
        top = weighted.max(axis=1, keepdims=True)
        return np.exp(weighted - top) / np.sum(np.exp(weighted - top), axis=1, keepdims=True)

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)

    def bic(self, X) -> float:
        """Bayesian information criterion; lower is better, penalises parameters."""
        X = _check_X(X)
        n, d = X.shape
        params = self.n_components * (d + d * (d + 1) / 2) + self.n_components - 1
        return float(-2 * self.log_likelihood_history_[-1] + params * np.log(n))


# ---------------------------------------------------------------------------
# PCA
# ---------------------------------------------------------------------------
class PCA:
    """Principal component analysis by singular value decomposition.

    1. Centre each column (PCA is about variance, not location).
    2. SVD: X = U S V^T. The columns of V are the principal directions.
    3. Project: Z = X V[:, :k].

    `explained_variance_ratio_` tells you how much of the total variance each component
    carries; it is the number to quote when you claim a reduction is lossless enough.
    """

    def __init__(self, n_components: int | None = None):
        self.n_components = n_components
        self.components_ = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None
        self.mean_ = None

    def fit(self, X):
        X = _check_X(X)
        self.mean_ = X.mean(axis=0)
        Xc = X - self.mean_
        _, s, vt = np.linalg.svd(Xc, full_matrices=False)
        variance = s**2 / max(len(X) - 1, 1)
        total = variance.sum()
        self.components_ = vt
        self.explained_variance_ = variance
        self.explained_variance_ratio_ = variance / total if total else np.zeros_like(variance)
        k = self.n_components or len(variance)
        self.components_ = vt[:k]
        self.explained_variance_ = variance[:k]
        self.explained_variance_ratio_ = self.explained_variance_ratio_[:k]
        return self

    def transform(self, X):
        return (_check_X(X) - self.mean_) @ self.components_.T

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        """Map a projection back to feature space, using the first k components."""
        Z = np.asarray(Z)
        components = self.components_[: Z.shape[1]]
        return Z @ components + self.mean_


# ---------------------------------------------------------------------------
# Clustering quality
# ---------------------------------------------------------------------------
def silhouette_score(X, labels) -> float:
    """Mean silhouette: (b - a) / max(a, b), with a = mean intra-cluster distance and
    b = mean distance to the nearest other cluster. Ranges -1 to 1; 0 means overlapping.
    """
    X = _check_X(X)
    labels = np.asarray(labels)
    unique = [l for l in np.unique(labels) if l != -1]
    if len(unique) < 2:
        return 0.0
    distances = np.sqrt(np.maximum(
        np.sum(X**2, axis=1)[:, None] - 2 * X @ X.T + np.sum(X**2, axis=1)[None, :], 0
    ))
    scores = []
    for i in range(len(X)):
        if labels[i] == -1:
            continue
        same = labels == labels[i]
        if same.sum() > 1:
            a = distances[i, same].sum() / (same.sum() - 1)
        else:
            a = 0.0
        b = min(distances[i, labels == l].mean() for l in unique if l != labels[i])
        denom = max(a, b)
        scores.append((b - a) / denom if denom else 0.0)
    return float(np.mean(scores))


# ---------------------------------------------------------------------------
# Anomaly detection
# ---------------------------------------------------------------------------
def zscore_anomalies(X, threshold: float = 3.0):
    """Flag rows with any standardised feature beyond `threshold`.

    Assumes roughly Gaussian features and a single population. On skewed data such as
    transaction amounts it over-flags the long right tail.
    """
    X = _check_X(X)
    z = np.abs((X - X.mean(axis=0)) / np.where(X.std(axis=0) == 0, 1, X.std(axis=0)))
    return np.max(z, axis=1) > threshold


def iqr_anomalies(X, k: float = 1.5):
    """Flag rows outside [Q1 - k*IQR, Q3 + k*IQR] on any feature (Tukey's rule)."""
    X = _check_X(X)
    q1 = np.quantile(X, 0.25, axis=0)
    q3 = np.quantile(X, 0.75, axis=0)
    iqr = q3 - q1
    outside = (X < q1 - k * iqr) | (X > q3 + k * iqr)
    return outside.any(axis=1)


def mahalanobis_scores(X, mean=None, cov=None):
    """Squared Mahalanobis distance from the centre, handling correlated features.

    A transaction that is unusual in amount *and* distance jointly is far more
    suspicious than either alone; the inverse covariance matrix supplies that joint
    view, which per-feature z-scores cannot.
    """
    X = _check_X(X)
    mu = X.mean(axis=0) if mean is None else np.asarray(mean, float)
    if cov is None:
        cov = np.cov(X.T) + 1e-6 * np.eye(X.shape[1])
    inv = np.linalg.pinv(np.atleast_2d(cov))
    diff = X - mu
    return np.sum(diff @ inv * diff, axis=1)


if __name__ == "__main__":
    import datasets as ds
    from prep import StandardScaler

    frame = ds.customers()
    cols = ["annual_income_k", "spending_score", "recency_days", "purchase_frequency"]
    X = StandardScaler().fit_transform(frame[cols].to_numpy())

    print("k-means, k=2..6:")
    for k in range(2, 7):
        model = KMeans(k, seed=0).fit(X)
        print(f"  k={k}  inertia={model.inertia_:8.1f}  silhouette={silhouette_score(X, model.labels_):6.3f}")

    best = KMeans(4, seed=0).fit(X)
    sizes = np.bincount(best.labels_)
    print("k=4 cluster sizes:", sizes.tolist())
    for k in range(4):
        profile = frame[cols].to_numpy()[best.labels_ == k].mean(axis=0)
        print(f"  cluster {k}: " + "  ".join(f"{c}={v:.1f}" for c, v in zip(cols, profile)))

    print()
    print("hierarchical (average linkage, 4 clusters):", np.bincount(
        AgglomerativeClustering(4, "average").fit(X[:150]).labels_).tolist())
    print("DBSCAN eps=0.8 min_samples=5:", np.bincount(
        DBSCAN(0.8, 5).fit(X).labels_ + 1).tolist(), "(first bin = noise)")

    gm = GaussianMixture(4, seed=0).fit(X)
    print("GMM weights:", np.round(gm.weights_, 3), "BIC", round(gm.bic(X), 1))

    pca = PCA().fit(StandardScaler().fit_transform(frame[cols].to_numpy()))
    print("PCA explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))
    print("2 components keep:", round(float(pca.explained_variance_ratio_[:2].sum()), 3))

    tx = ds.transactions()
    numeric = ["amount", "distance_from_home_km", "ratio_to_median_spend", "attempts_last_hour"]
    Xt = StandardScaler().fit_transform(np.log1p(tx[numeric].to_numpy()))
    flagged = zscore_anomalies(Xt, 3.0)
    print()
    print("z-score flags:", int(flagged.sum()), "of which fraud:", int(tx.loc[flagged, "is_fraud"].sum()))
    scores = mahalanobis_scores(Xt)
    top = np.argsort(-scores)[:50]
    print("top-50 Mahalanobis precision:", round(float(tx.iloc[top]["is_fraud"].mean()), 3))
