"""Evaluation metrics, resampling and model selection, from scratch.

Every function is short enough to check by hand. That is deliberate: the module's
argument is that a metric you cannot compute yourself is a metric you cannot defend.

Conventions
-----------
* Binary labels are 0 (negative) and 1 (positive).
* `scores` are probabilities or any monotone confidence in the positive class.
* `make_model` is a zero-argument callable returning a fresh, unfitted estimator with
  `fit(X, y)` and `predict(X)` (and `predict_proba(X)` where relevant). Passing a
  factory, not a fitted object, is what makes cross-validation honest.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "confusion_matrix",
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "classification_report",
    "roc_curve",
    "auc",
    "roc_auc_score",
    "precision_recall_curve",
    "average_precision",
    "kfold_indices",
    "stratified_kfold_indices",
    "cross_val_score",
    "grid_search",
    "learning_curve",
    "bootstrap_ci",
    "threshold_sweep",
]


def _arrays(y_true, y_pred):
    return np.asarray(y_true).ravel(), np.asarray(y_pred).ravel()


# ---------------------------------------------------------------------------
# Confusion matrix and friends
# ---------------------------------------------------------------------------
def confusion_matrix(y_true, y_pred, labels=(0, 1)) -> np.ndarray:
    """Counts with rows = actual class, columns = predicted class."""
    y_true, y_pred = _arrays(y_true, y_pred)
    index = {label: i for i, label in enumerate(labels)}
    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    for t, p in zip(y_true, y_pred):
        matrix[index[int(t)], index[int(p)]] += 1
    return matrix


def accuracy(y_true, y_pred) -> float:
    y_true, y_pred = _arrays(y_true, y_pred)
    return float(np.mean(y_true == y_pred))


def precision(y_true, y_pred) -> float:
    """Of everything flagged positive, how much really was? TN and FP ignored."""
    y_true, y_pred = _arrays(y_true, y_pred)
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return float(tp / (tp + fp)) if (tp + fp) else 0.0


def recall(y_true, y_pred) -> float:
    """Of everything actually positive, how much did we catch?"""
    y_true, y_pred = _arrays(y_true, y_pred)
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return float(tp / (tp + fn)) if (tp + fn) else 0.0


def f1_score(y_true, y_pred) -> float:
    """Harmonic mean of precision and recall: punishes an unbalanced pair."""
    p, r = precision(y_true, y_pred), recall(y_true, y_pred)
    return float(2 * p * r / (p + r)) if (p + r) else 0.0


def classification_report(y_true, y_pred, labels=(0, 1)) -> pd.DataFrame:
    """Per-class precision/recall/F1/support plus a macro average."""
    y_true, y_pred = _arrays(y_true, y_pred)
    rows = []
    for label in labels:
        t = (y_true == label)
        p = (y_pred == label)
        tp = np.sum(t & p)
        rows.append(
            {
                "class": int(label),
                "precision": tp / p.sum() if p.sum() else 0.0,
                "recall": tp / t.sum() if t.sum() else 0.0,
                "f1": (
                    2 * tp / (p.sum() + t.sum()) if (p.sum() + t.sum()) else 0.0
                ),
                "support": int(t.sum()),
            }
        )
    frame = pd.DataFrame(rows)
    macro = frame[["precision", "recall", "f1"]].mean()
    frame.loc[len(frame)] = {
        "class": "macro",
        "precision": macro["precision"],
        "recall": macro["recall"],
        "f1": macro["f1"],
        "support": int(len(y_true)),
    }
    return frame


# ---------------------------------------------------------------------------
# Ranking metrics: ROC, AUC, PR
# ---------------------------------------------------------------------------
def roc_curve(y_true, scores):
    """Return (fpr, tpr, thresholds) sweeping every distinct score as a cut-off.

    The curve answers: if I move the threshold, what do I buy in true positives and
    what do I pay in false positives?
    """
    y_true = np.asarray(y_true).ravel()
    scores = np.asarray(scores, dtype=float).ravel()
    order = np.argsort(-scores)
    y = y_true[order]
    s = scores[order]

    distinct = np.where(np.diff(s))[0]
    cut_points = np.r_[distinct, len(s) - 1]
    tps = np.cumsum(y)[cut_points]
    fps = (cut_points + 1) - tps
    positives, negatives = y.sum(), len(y) - y.sum()

    tpr = tps / positives if positives else np.zeros_like(tps, dtype=float)
    fpr = fps / negatives if negatives else np.zeros_like(fps, dtype=float)
    return np.r_[0.0, fpr], np.r_[0.0, tpr], np.r_[np.inf, s[cut_points]]


def auc(fpr, tpr) -> float:
    """Area under the ROC curve by the trapezoid rule.

    Equivalent to the probability that a random positive outranks a random negative.
    """
    fpr, tpr = np.asarray(fpr, float), np.asarray(tpr, float)
    return float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2.0))


def roc_auc_score(y_true, scores) -> float:
    fpr, tpr, _ = roc_curve(y_true, scores)
    return auc(fpr, tpr)


def precision_recall_curve(y_true, scores):
    """Precision/recall at every threshold, ordered from strict to permissive."""
    y_true = np.asarray(y_true).ravel()
    scores = np.asarray(scores, dtype=float).ravel()
    order = np.argsort(-scores)
    y = y_true[order]

    tps = np.cumsum(y)
    fps = np.cumsum(1 - y)
    positives = y.sum()
    precision = tps / np.maximum(tps + fps, 1)
    recall = tps / positives if positives else np.zeros_like(tps, float)
    return np.r_[precision, 1.0], np.r_[recall, 0.0], np.r_[np.inf, scores[order]]


def average_precision(y_true, scores) -> float:
    """Area under the precision-recall curve, as a sum of recall increments.

    AP = sum over thresholds of (recall_i - recall_{i-1}) * precision_i, which is the
    step-wise area under the curve. Preferred to ROC-AUC when positives are rare,
    because it does not reward correct ranking of the (abundant) negatives.
    """
    y_true = np.asarray(y_true).ravel()
    scores = np.asarray(scores, dtype=float).ravel()
    positives = y_true.sum()
    if positives == 0:
        return 0.0
    order = np.argsort(-scores, kind="mergesort")
    y = y_true[order]
    tp = np.cumsum(y)
    fp = np.cumsum(1 - y)
    precision = tp / np.maximum(tp + fp, 1)
    recall = tp / positives
    increments = np.diff(np.r_[0.0, recall])
    return float(np.sum(increments * precision))


def threshold_sweep(y_true, scores, thresholds=None) -> pd.DataFrame:
    """A table of precision, recall and F1 at candidate thresholds."""
    y_true = np.asarray(y_true).ravel()
    scores = np.asarray(scores, dtype=float).ravel()
    if thresholds is None:
        thresholds = np.round(np.arange(0.05, 1.0, 0.05), 2)
    rows = []
    for t in thresholds:
        pred = (scores >= t).astype(int)
        rows.append(
            {
                "threshold": float(t),
                "precision": precision(y_true, pred),
                "recall": recall(y_true, pred),
                "f1": f1_score(y_true, pred),
                "flagged": int(pred.sum()),
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Resampling
# ---------------------------------------------------------------------------
def kfold_indices(n: int, k: int = 5, shuffle: bool = True, seed: int = 0):
    """Yield (train_idx, valid_idx) for k folds."""
    idx = np.arange(n)
    if shuffle:
        np.random.default_rng(seed).shuffle(idx)
    folds = np.array_split(idx, k)
    for i in range(k):
        valid = folds[i]
        train = np.concatenate([folds[j] for j in range(k) if j != i])
        yield train, valid


def stratified_kfold_indices(y, k: int = 5, seed: int = 0):
    """k-fold that keeps the class ratio in every fold.

    Necessary whenever the positive class is rare: with 1% positives, an unstratified
    fold may contain none of them, and its recall is undefined.
    """
    y = np.asarray(y).ravel()
    rng = np.random.default_rng(seed)
    folds = [[] for _ in range(k)]
    for cls in np.unique(y):
        idx = np.flatnonzero(y == cls)
        rng.shuffle(idx)
        for position, chunk in enumerate(np.array_split(idx, k)):
            folds[position].extend(chunk.tolist())
    for i in range(k):
        valid = np.array(sorted(folds[i]))
        held_out = set(int(k) for k in folds[i])
        train = np.array(sorted(set(range(len(y))) - held_out))
        yield train, valid


def cross_val_score(make_model, X, y, k: int = 5, metric=None, stratified: bool = False, seed: int = 0):
    """Fit k times on k-1 folds, score on the held-out fold, return the scores.

    Each fold gets a brand-new model. Reusing a fitted model across folds is the
    commonest way a student accidentally reports a leaked score.
    """
    X = np.asarray(X)
    y = np.asarray(y).ravel()
    if metric is None:
        metric = accuracy
    folds = (
        stratified_kfold_indices(y, k, seed)
        if stratified
        else kfold_indices(len(y), k, seed=seed)
    )
    scores = []
    for train_idx, valid_idx in folds:
        model = make_model()
        model.fit(X[train_idx], y[train_idx])
        scores.append(float(metric(y[valid_idx], model.predict(X[valid_idx]))))
    return np.array(scores)


def grid_search(make_model, param_grid, X, y, k: int = 5, metric=None, stratified: bool = False, seed: int = 0):
    """Exhaustive search over a small parameter grid, scored by cross-validation.

    Returns (best_params, best_score, results_table). The table is the point: a single
    best score hides how flat or spiky the surface is.
    """
    from itertools import product

    X = np.asarray(X)
    y = np.asarray(y).ravel()
    if metric is None:
        metric = accuracy
    keys = list(param_grid)
    rows = []
    for values in product(*(param_grid[k] for k in keys)):
        params = dict(zip(keys, values))

        def factory(params=params):
            return make_model(**params)

        scores = cross_val_score(factory, X, y, k=k, metric=metric, stratified=stratified, seed=seed)
        rows.append({**params, "mean_score": float(scores.mean()), "std": float(scores.std())})
    table = pd.DataFrame(rows).sort_values("mean_score", ascending=False).reset_index(drop=True)
    best = table.iloc[0]
    best_params = {k: best[k] for k in keys}
    return best_params, float(best["mean_score"]), table


def learning_curve(make_model, X, y, fractions=(0.1, 0.3, 0.5, 0.7, 1.0), k: int = 3, metric=None, seed: int = 0):
    """Train and validation score as the training set grows.

    A large gap that closes with more data means variance. A small gap with both scores
    low means bias. That distinction is the whole diagnostic value of the curve.
    """
    X = np.asarray(X)
    y = np.asarray(y).ravel()
    if metric is None:
        metric = accuracy
    rows = []
    n = len(y)
    for fraction in fractions:
        size = max(k, int(n * fraction))
        subset = np.random.default_rng(seed).choice(n, size=size, replace=False)
        train_scores, valid_scores = [], []
        for train_idx, valid_idx in kfold_indices(len(subset), k, seed=seed):
            model = make_model()
            model.fit(X[subset][train_idx], y[subset][train_idx])
            train_scores.append(float(metric(y[subset][train_idx], model.predict(X[subset][train_idx]))))
            valid_scores.append(float(metric(y[subset][valid_idx], model.predict(X[subset][valid_idx]))))
        rows.append(
            {
                "fraction": fraction,
                "n_train": int(size * (k - 1) / k),
                "train": float(np.mean(train_scores)),
                "validation": float(np.mean(valid_scores)),
            }
        )
    return pd.DataFrame(rows)


def bootstrap_ci(y_true, y_pred, metric=accuracy, n_boot: int = 1000, seed: int = 0, alpha: float = 0.05):
    """Percentile bootstrap interval for a metric.

    Resample rows with replacement, recompute the metric, and report the middle
    (1 - alpha) of the resulting distribution. A single number without an interval
    invites over-reading a difference of two decimal places.
    """
    y_true, y_pred = _arrays(y_true, y_pred)
    rng = np.random.default_rng(seed)
    n = len(y_true)
    values = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        values[b] = metric(y_true[idx], y_pred[idx])
    lo, hi = np.quantile(values, [alpha / 2, 1 - alpha / 2])
    return {"mean": float(values.mean()), "low": float(lo), "high": float(hi)}


if __name__ == "__main__":
    import datasets as ds
    from classifiers import LogisticRegressionGD, GaussianNB

    frame = ds.loans()
    numeric = ["annual_income_k", "loan_amount_k", "credit_score", "employment_years", "debt_ratio", "default_history"]
    X = frame[numeric].fillna(frame[numeric].median()).to_numpy()
    y = frame["approved"].to_numpy()

    from prep import StandardScaler, train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, seed=0, stratify=y)
    scaler = StandardScaler().fit(X_train)
    model = LogisticRegressionGD(epochs=800, lr=0.5).fit(scaler.transform(X_train), y_train)
    proba = model.predict_proba(scaler.transform(X_test))[:, 1]
    pred = (proba >= 0.5).astype(int)

    print("confusion matrix (rows actual, cols predicted):")
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred).to_string(index=False))
    print("accuracy:", round(accuracy(y_test, pred), 4))
    print("ROC AUC:", round(roc_auc_score(y_test, proba), 4))
    print("average precision:", round(average_precision(y_test, proba), 4))
    print()
    print(threshold_sweep(y_test, proba, thresholds=[0.1, 0.2, 0.3, 0.4, 0.5]).round(3).to_string(index=False))
    print()
    from prep import Pipeline, SimpleImputer as Imputer

    def make_pipeline():
        return Pipeline(
            [
                ("impute", Imputer("median")),
                ("scale", StandardScaler()),
                ("model", LogisticRegressionGD(epochs=600, lr=0.5)),
            ]
        )

    cv = cross_val_score(make_pipeline, X, y, k=5, stratified=True)
    print("5-fold CV accuracy:", np.round(cv, 4), "mean", round(cv.mean(), 4))
    print("bootstrap 95% CI for accuracy:", {k: round(v, 4) for k, v in bootstrap_ci(y_test, pred).items()})
