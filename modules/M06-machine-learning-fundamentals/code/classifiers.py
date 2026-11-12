"""Classification algorithms written from scratch, plus a small shared API.

Everything here works on NumPy arrays: X is (n_samples, n_features), y is 0/1.

The implementations are deliberately small and readable rather than fast. Where an
algorithm has a scikit-learn counterpart, the lesson shows both and compares them, so
you can see that the library is doing the same arithmetic you just wrote.

Run `python classifiers.py` for a comparison on the loan dataset.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "LogisticRegressionGD",
    "KNNClassifier",
    "GaussianNB",
    "MultinomialNB",
    "DecisionTreeClassifier",
    "RandomForestClassifier",
    "GradientBoostingClassifier",
    "LinearSVM",
]


def _sigmoid(z):
    # Clip to avoid overflow warnings in exp; the result is identical to machine
    # precision for |z| > 35 but does not raise.
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def _check_X(X):
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    return X


# ---------------------------------------------------------------------------
# Logistic regression
# ---------------------------------------------------------------------------
class LogisticRegressionGD:
    """Logistic regression trained by full-batch gradient descent.

    p(y=1 | x) = sigmoid(w·x + b). The loss is mean binary cross-entropy; its gradient
    with respect to w is X^T (p - y) / n, which is why the update below is three lines.

    Parameters
    ----------
    lr : float
        Learning rate. With standardised features, 0.5 converges in a few hundred
        epochs; with raw features it diverges, which is the lesson.
    epochs : int
        Number of full passes.
    l2 : float
        L2 penalty strength (weight decay). Shrinks weights, never the intercept.
    class_weight : {"balanced", None}
        "balanced" multiplies each class's contribution by n / (2 * n_class), which
        stops a 90/10 problem from being solved by predicting the majority class.
    """

    def __init__(self, lr: float = 0.1, epochs: int = 500, l2: float = 0.0, class_weight=None, seed: int = 0):
        self.lr = lr
        self.epochs = epochs
        self.l2 = l2
        self.class_weight = class_weight
        self.seed = seed
        self.w = None
        self.b = 0.0
        self.loss_history_ = []

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y, dtype=float).ravel()
        n, d = X.shape
        rng = np.random.default_rng(self.seed)
        self.w = rng.normal(0.0, 0.01, d)
        self.b = 0.0
        self.loss_history_ = []

        if self.class_weight == "balanced":
            positives = y.sum()
            negatives = n - positives
            weights = np.where(y == 1, n / (2 * max(positives, 1)), n / (2 * max(negatives, 1)))
        else:
            weights = np.ones(n)

        for _ in range(self.epochs):
            p = _sigmoid(X @ self.w + self.b)
            error = (p - y) * weights
            grad_w = X.T @ error / n + self.l2 * self.w
            grad_b = error.mean()
            self.w -= self.lr * grad_w
            self.b -= self.lr * grad_b
            eps = 1e-9
            self.loss_history_.append(
                float(np.mean(-weights * (y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))))
            )
        return self

    def decision_function(self, X):
        return _check_X(X) @ self.w + self.b

    def predict_proba(self, X):
        p = _sigmoid(self.decision_function(X))
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


# ---------------------------------------------------------------------------
# k-nearest neighbours
# ---------------------------------------------------------------------------
class KNNClassifier:
    """Majority vote among the k nearest training points (Euclidean distance).

    No training happens in `fit` — it only stores the data. All the cost is at
    prediction time, which is the trade-off that makes k-NN unsuitable for large or
    latency-critical deployments without an index.
    """

    def __init__(self, k: int = 5, weights: str = "uniform"):
        if weights not in {"uniform", "distance"}:
            raise ValueError("weights must be 'uniform' or 'distance'")
        self.k = k
        self.weights = weights
        self.X_ = None
        self.y_ = None

    def fit(self, X, y):
        self.X_ = _check_X(X)
        self.y_ = np.asarray(y).ravel()
        if self.k > len(self.y_):
            raise ValueError("k cannot exceed the number of training rows")
        return self

    def predict_proba(self, X):
        X = _check_X(X)
        # Squared distances via the expansion |a-b|^2 = |a|^2 - 2ab + |b|^2.
        distances = (
            np.sum(X**2, axis=1)[:, None]
            - 2 * X @ self.X_.T
            + np.sum(self.X_**2, axis=1)[None, :]
        )
        neighbours = np.argsort(distances, axis=1)[:, : self.k]
        proba = np.zeros((len(X), 2))
        for i, idx in enumerate(neighbours):
            labels = self.y_[idx]
            if self.weights == "distance":
                d = np.sqrt(np.maximum(distances[i, idx], 1e-12))
                w = 1.0 / d
            else:
                w = np.ones(self.k)
            proba[i, 1] = np.sum(w * labels) / np.sum(w)
            proba[i, 0] = 1 - proba[i, 1]
        return proba

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


# ---------------------------------------------------------------------------
# Naive Bayes
# ---------------------------------------------------------------------------
class GaussianNB:
    """Naive Bayes with a Gaussian likelihood per feature per class.

    p(y | x) is proportional to p(y) * product_j N(x_j; mean_jy, var_jy). The "naive"
    assumption is that features are conditionally independent given the class; it is
    almost always false and often still works, because the decision only needs the
    ranking of classes to be right.
    """

    def __init__(self, var_smoothing: float = 1e-9):
        self.var_smoothing = var_smoothing
        self.classes_ = None
        self.mean_ = {}
        self.var_ = {}
        self.prior_ = {}

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y).ravel()
        self.classes_ = np.unique(y)
        for c in self.classes_:
            Xc = X[y == c]
            self.mean_[c] = Xc.mean(axis=0)
            self.var_[c] = Xc.var(axis=0) + self.var_smoothing
            self.prior_[c] = len(Xc) / len(y)
        return self

    def predict_log_proba(self, X):
        X = _check_X(X)
        scores = []
        for c in self.classes_:
            log_prior = np.log(self.prior_[c])
            log_likelihood = -0.5 * np.sum(
                np.log(2 * np.pi * self.var_[c]) + (X - self.mean_[c]) ** 2 / self.var_[c], axis=1
            )
            scores.append(log_prior + log_likelihood)
        scores = np.column_stack(scores)
        # Normalise with the log-sum-exp trick so probabilities sum to one.
        top = scores.max(axis=1, keepdims=True)
        log_norm = top + np.log(np.sum(np.exp(scores - top), axis=1, keepdims=True))
        return scores - log_norm

    def predict_proba(self, X):
        return np.exp(self.predict_log_proba(X))

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


class MultinomialNB:
    """Naive Bayes for non-negative counts (word counts, for example).

    Uses Laplace smoothing: count + alpha in every cell, so an unseen feature does not
    produce a zero probability that wipes out the product.
    """

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.classes_ = None
        self.log_prior_ = None
        self.log_prob_ = None

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y).ravel()
        self.classes_ = np.unique(y)
        counts = np.vstack([X[y == c].sum(axis=0) for c in self.classes_])
        self.log_prior_ = np.log(np.array([np.mean(y == c) for c in self.classes_]))
        smoothed = counts + self.alpha
        self.log_prob_ = np.log(smoothed / smoothed.sum(axis=1, keepdims=True))
        return self

    def predict_log_proba(self, X):
        X = _check_X(X)
        scores = X @ self.log_prob_.T + self.log_prior_
        top = scores.max(axis=1, keepdims=True)
        return scores - (top + np.log(np.sum(np.exp(scores - top), axis=1, keepdims=True)))

    def predict_proba(self, X):
        return np.exp(self.predict_log_proba(X))

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------
class _Node:
    __slots__ = ("feature", "threshold", "left", "right", "value", "leaf_id")

    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.leaf_id = None


def _gini(p):
    return 1.0 - np.sum(p**2)


def _entropy(p):
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def _best_split(X, y, criterion, min_samples_leaf):
    """Best binary split by impurity reduction, vectorised per feature.

    For each feature the rows are sorted once; cumulative positive counts then give
    every candidate split's class counts in O(1), so the whole scan is
    O(n_features * n log n) instead of a Python loop over candidates.

    Returns (feature, threshold, gain) or (None, None, 0.0) when no split is legal.
    """
    n, d = X.shape
    if n < 2 * min_samples_leaf:
        return None, None, 0.0

    positives_all = float(y.sum())
    negatives_all = n - positives_all

    def node_impurity(pos, total):
        if total == 0:
            return 0.0
        p1, p0 = pos / total, (total - pos) / total
        if criterion == "gini":
            return 1.0 - (p1 * p1 + p0 * p0)
        terms = np.array([p1, p0])
        terms = terms[terms > 0]
        return float(-(terms * np.log2(terms)).sum())

    parent = node_impurity(positives_all, n)
    best_gain, best_feature, best_threshold = 0.0, None, None

    for feature in range(d):
        values = X[:, feature]
        order = np.argsort(values, kind="mergesort")
        sorted_values, sorted_labels = values[order], y[order]

        left_n = np.arange(1, n)                     # left size for split after i
        left_pos = np.cumsum(sorted_labels)[:-1]
        right_n = n - left_n
        right_pos = positives_all - left_pos

        valid = (
            (sorted_values[1:] != sorted_values[:-1])
            & (left_n >= min_samples_leaf)
            & (right_n >= min_samples_leaf)
        )
        if not np.any(valid):
            continue

        # Weighted child impurity, computed only for legal candidates.
        lp = left_pos[valid]
        ln = left_n[valid]
        rp = right_pos[valid]
        rn = right_n[valid]
        if criterion == "gini":
            imp_left = 1.0 - ((lp / ln) ** 2 + ((ln - lp) / ln) ** 2)
            imp_right = 1.0 - ((rp / rn) ** 2 + ((rn - rp) / rn) ** 2)
        else:
            def entropy_vec(pos, total):
                p1 = pos / total
                p0 = 1.0 - p1
                with np.errstate(divide="ignore", invalid="ignore"):
                    out = -(np.where(p1 > 0, p1 * np.log2(p1), 0.0) + np.where(p0 > 0, p0 * np.log2(p0), 0.0))
                return out
            imp_left = entropy_vec(lp, ln)
            imp_right = entropy_vec(rp, rn)

        weighted = (ln * imp_left + rn * imp_right) / n
        gains = parent - weighted
        k = int(np.argmax(gains))
        if gains[k] > best_gain + 1e-12:
            best_gain = float(gains[k])
            best_feature = feature
            split_positions = np.flatnonzero(valid)
            i = int(split_positions[k])
            best_threshold = (sorted_values[i] + sorted_values[i + 1]) / 2.0
    return best_feature, best_threshold, best_gain


class DecisionTreeClassifier:
    """CART classifier: greedy splits that maximise impurity reduction.

    depth limits, min_samples_leaf and min_samples_split are the three knobs that
    control the bias-variance trade-off. A fully grown tree on this data reaches zero
    training error and is a good demonstration of overfitting.
    """

    def __init__(self, max_depth=None, min_samples_split=2, min_samples_leaf=1,
                 criterion="gini", max_features=None, seed=0):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.max_features = max_features
        self.seed = seed
        self.root_ = None
        self.n_features_ = None
        self.feature_importances_ = None

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y).astype(int).ravel()
        self.n_features_ = X.shape[1]
        self.feature_importances_ = np.zeros(self.n_features_)
        self.root_ = self._grow(X, y, depth=0)
        total = self.feature_importances_.sum()
        if total > 0:
            self.feature_importances_ /= total
        return self

    def _grow(self, X, y, depth):
        counts = np.bincount(y, minlength=2)
        value = counts / counts.sum()
        node = _Node(value=value)

        pure = counts[0] == 0 or counts[1] == 0
        if pure or len(y) < self.min_samples_split:
            return node
        if self.max_depth is not None and depth >= self.max_depth:
            return node

        # Feature subsampling: search on a copy, then map the chosen column back.
        columns = np.arange(X.shape[1])
        if self.max_features is not None and self.max_features < X.shape[1]:
            columns = np.sort(
                np.random.default_rng(self.seed + depth).choice(
                    X.shape[1], self.max_features, replace=False
                )
            )
        view = X[:, columns]

        feature, threshold, gain = _best_split(view, y, self.criterion, self.min_samples_leaf)
        if feature is None:
            return node
        feature = int(columns[feature])

        mask = X[:, feature] <= threshold
        self.feature_importances_[feature] += gain * len(y)
        node.feature = feature
        node.threshold = threshold
        node.left = self._grow(X[mask], y[mask], depth + 1)
        node.right = self._grow(X[~mask], y[~mask], depth + 1)
        return node

    def _leaf_value(self, x, node):
        while node.left is not None:
            node = node.left if x[node.feature] <= node.threshold else node.right
        return node.value

    def predict_proba(self, X):
        X = _check_X(X)
        return np.array([self._leaf_value(x, self.root_) for x in X])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


class RandomForestClassifier:
    """Bagged decision trees with a random feature subset at every split.

    The two sources of randomness decorrelate the trees, which is what turns an
    average of high-variance learners into a low-variance one. Each tree sees a
    bootstrap sample; the forest averages their probabilities.
    """

    def __init__(self, n_estimators=100, max_depth=None, min_samples_leaf=1,
                 max_features="sqrt", seed=0):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.seed = seed
        self.trees_ = []
        self.feature_importances_ = None

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y).astype(int).ravel()
        rng = np.random.default_rng(self.seed)
        n, d = X.shape
        if self.max_features == "sqrt":
            m = max(1, int(np.sqrt(d)))
        elif self.max_features == "log2":
            m = max(1, int(np.log2(d)))
        else:
            m = d if self.max_features is None else int(self.max_features)

        self.trees_ = []
        importances = np.zeros(d)
        for _ in range(self.n_estimators):
            sample = rng.integers(0, n, n)
            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                max_features=m,
                seed=int(rng.integers(0, 10**6)),
            ).fit(X[sample], y[sample])
            self.trees_.append(tree)
            importances += tree.feature_importances_
        self.feature_importances_ = importances / max(self.n_estimators, 1)
        return self

    def predict_proba(self, X):
        return np.mean([t.predict_proba(X) for t in self.trees_], axis=0)

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


# ---------------------------------------------------------------------------
# Gradient boosting
# ---------------------------------------------------------------------------
class _RegressionTree:
    """Shallow least-squares tree used as the boosting base learner."""

    def __init__(self, max_depth=3, min_samples_leaf=5):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root_ = None
        self.n_leaves_ = 0

    def fit(self, X, residual):
        self.n_leaves_ = 0
        self.root_ = self._grow(X, residual, 0)
        return self

    def _grow(self, X, r, depth):
        node = _Node(value=float(np.mean(r)))
        if depth >= self.max_depth or len(r) < 2 * self.min_samples_leaf:
            node.leaf_id = self.n_leaves_
            self.n_leaves_ += 1
            return node

        n = len(r)
        total_ss = np.sum((r - r.mean()) ** 2)
        best_gain, best_feature, best_threshold = 0.0, None, None

        for feature in range(X.shape[1]):
            order = np.argsort(X[:, feature], kind="mergesort")
            sv, sr = X[order, feature], r[order]
            left_n = np.arange(1, n)
            right_n = n - left_n
            csum = np.cumsum(sr)[:-1]
            csum_sq = np.cumsum(sr**2)[:-1]
            total = sr.sum()
            total_sq = np.sum(sr**2)

            valid = (
                (sv[1:] != sv[:-1])
                & (left_n >= self.min_samples_leaf)
                & (right_n >= self.min_samples_leaf)
            )
            if not np.any(valid):
                continue

            ln, rn = left_n[valid].astype(float), right_n[valid].astype(float)
            lsum, lsq = csum[valid], csum_sq[valid]
            rsum = total - lsum
            rsq = total_sq - lsq
            # Gain in sum of squares = parent SS - (left SS + right SS).
            child_ss = (lsq - lsum**2 / ln) + (rsq - rsum**2 / rn)
            gains = total_ss - child_ss
            k = int(np.argmax(gains))
            if gains[k] > best_gain + 1e-12:
                best_gain = float(gains[k])
                best_feature = feature
                positions = np.flatnonzero(valid)
                i = int(positions[k])
                best_threshold = (sv[i] + sv[i + 1]) / 2.0

        if best_feature is None:
            node.leaf_id = self.n_leaves_
            self.n_leaves_ += 1
            return node
        mask = X[:, best_feature] <= best_threshold
        node.feature, node.threshold = best_feature, best_threshold
        node.left = self._grow(X[mask], r[mask], depth + 1)
        node.right = self._grow(X[~mask], r[~mask], depth + 1)
        return node

    def set_leaf_values(self, mapping):
        """Replace each leaf's prediction with a per-leaf value (the Newton step)."""
        def assign(node):
            if node.left is None:
                node.value = float(mapping[node.leaf_id])
            else:
                assign(node.left)
                assign(node.right)

        assign(self.root_)

    def apply(self, X):
        """Leaf identifier per row, so boosting can fit one Newton step per leaf."""
        out = np.empty(len(X), dtype=int)
        for i, x in enumerate(X):
            node = self.root_
            while node.left is not None:
                node = node.left if x[node.feature] <= node.threshold else node.right
            out[i] = node.leaf_id
        return out

    def predict(self, X):
        out = np.empty(len(X))
        for i, x in enumerate(X):
            node = self.root_
            while node.left is not None:
                node = node.left if x[node.feature] <= node.threshold else node.right
            out[i] = node.value
        return out


class GradientBoostingClassifier:
    """Binary gradient boosting with log-loss and Newton leaf values.

    Each round fits a small tree to the pseudo-residual (y - p), then replaces each
    leaf's mean residual with the Newton step sum(r) / sum(p(1-p)). That step is what
    makes it a second-order method rather than plain residual fitting.
    """

    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3, min_samples_leaf=5):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.trees_ = []
        self.base_score_ = 0.0

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y, dtype=float).ravel()
        prior = np.clip(y.mean(), 1e-6, 1 - 1e-6)
        self.base_score_ = float(np.log(prior / (1 - prior)))
        raw = np.full(len(y), self.base_score_)
        self.trees_ = []

        for _ in range(self.n_estimators):
            p = _sigmoid(raw)
            residual = y - p
            tree = _RegressionTree(self.max_depth, self.min_samples_leaf).fit(X, residual)
            leaves = tree.apply(X)
            # Newton step per leaf: sum(residual) / sum(p(1-p)) is the second-order
            # optimum for that leaf, and converges faster than the mean residual.
            steps = {}
            for leaf in np.unique(leaves):
                mask = leaves == leaf
                num = residual[mask].sum()
                den = np.sum(p[mask] * (1 - p[mask]))
                steps[int(leaf)] = num / max(den, 1e-9)
            tree.set_leaf_values(steps)
            raw += self.learning_rate * tree.predict(X)
            self.trees_.append(tree)
        return self

    def decision_function(self, X):
        X = _check_X(X)
        raw = np.full(len(X), self.base_score_)
        for tree in self.trees_:
            raw += self.learning_rate * tree.predict(X)
        return raw

    def predict_proba(self, X):
        p = _sigmoid(self.decision_function(X))
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


# ---------------------------------------------------------------------------
# Linear SVM
# ---------------------------------------------------------------------------
class LinearSVM:
    """Linear support vector machine trained by subgradient descent on hinge loss.

    minimise  (lambda/2)|w|^2 + mean(max(0, 1 - y_i (w·x_i + b))),  y in {-1, +1}
    C = 1/lambda controls the margin/error trade-off: large C means a hard margin and
    a higher risk of overfitting. Kernels are discussed in the lesson; this class is
    the linear case you can inspect.
    """

    def __init__(self, C: float = 1.0, lr: float = 0.01, epochs: int = 300, seed: int = 0):
        self.C = C
        self.lr = lr
        self.epochs = epochs
        self.seed = seed
        self.w = None
        self.b = 0.0

    def fit(self, X, y):
        X = _check_X(X)
        y = np.where(np.asarray(y).ravel() == 1, 1.0, -1.0)
        n, d = X.shape
        self.w = np.zeros(d)
        self.b = 0.0
        lam = 1.0 / (self.C * n)
        for _ in range(self.epochs):
            margins = y * (X @ self.w + self.b)
            active = margins < 1
            grad_w = lam * self.w - (X[active] * y[active, None]).sum(axis=0) / n
            grad_b = -y[active].sum() / n
            self.w -= self.lr * grad_w
            self.b -= self.lr * grad_b
        return self

    def decision_function(self, X):
        return _check_X(X) @ self.w + self.b

    def predict(self, X):
        return (self.decision_function(X) >= 0).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))


if __name__ == "__main__":
    import datasets as ds
    from prep import StandardScaler, train_test_split

    frame = ds.loans()
    numeric = [
        "annual_income_k", "loan_amount_k", "credit_score",
        "employment_years", "debt_ratio", "default_history",
    ]
    X = frame[numeric].fillna(frame[numeric].median()).to_numpy()
    y = frame["approved"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, seed=0, stratify=y)
    scale = StandardScaler().fit(X_train)
    Xtr, Xte = scale.transform(X_train), scale.transform(X_test)

    models = {
        "logistic (gd)": LogisticRegressionGD(lr=0.5, epochs=800),
        "kNN (k=15)": KNNClassifier(k=15),
        "Gaussian NB": GaussianNB(),
        "decision tree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=5),
        "random forest": RandomForestClassifier(n_estimators=60, max_depth=6, min_samples_leaf=5),
        "gradient boosting": GradientBoostingClassifier(n_estimators=80, max_depth=2),
        "linear SVM": LinearSVM(C=0.5, lr=0.02, epochs=400),
    }
    print(f"{'model':20s} {'train':>7s} {'test':>7s}")
    for name, model in models.items():
        model.fit(Xtr, y_train)
        print(f"{name:20s} {model.score(Xtr, y_train):7.3f} {model.score(Xte, y_test):7.3f}")
