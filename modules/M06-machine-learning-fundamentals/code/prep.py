"""Data preparation utilities written from scratch (NumPy + pandas only).

These classes follow scikit-learn's fit/transform contract on purpose: once you have
written `fit` and `transform` yourself, `sklearn.preprocessing.StandardScaler` is no
longer a magic box, and the rule that makes leakage impossible — fit on training data
only — becomes obvious rather than memorised.

Run `python prep.py` for a short demonstration.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "Pipeline",
    "train_test_split",
    "train_val_test_split",
    "stratified_indices",
    "StandardScaler",
    "MinMaxScaler",
    "SimpleImputer",
    "OneHotEncoder",
    "clip_outliers_iqr",
    "correlation_with_target",
    "top_k_features",
    "describe_frame",
]


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------
def _as_array(values):
    if isinstance(values, pd.DataFrame):
        return values.to_numpy()
    if isinstance(values, pd.Series):
        return values.to_numpy()
    return np.asarray(values)


def stratified_indices(y, test_size: float = 0.2, seed: int = 0):
    """Return (train_idx, test_idx) preserving the class proportion of `y`."""
    y = _as_array(y).ravel()
    rng = np.random.default_rng(seed)
    classes, counts = np.unique(y, return_counts=True)
    train_parts, test_parts = [], []
    for cls, count in zip(classes, counts):
        idx = np.flatnonzero(y == cls)
        rng.shuffle(idx)
        n_test = int(round(count * test_size))
        # Guarantee at least one example of a rare class in the test set.
        n_test = max(1, min(n_test, count - 1))
        test_parts.append(idx[:n_test])
        train_parts.append(idx[n_test:])
    train = np.concatenate(train_parts)
    test = np.concatenate(test_parts)
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def train_test_split(X, y, test_size: float = 0.2, seed: int = 0, stratify=None):
    """Split arrays into train/test sets, optionally stratified on `stratify`.

    Returns copies so that in-place scaling of the training half cannot silently
    modify the test half (a subtle and very common bug).
    """
    n = len(X)
    if stratify is not None:
        train_idx, test_idx = stratified_indices(stratify, test_size, seed)
    else:
        rng = np.random.default_rng(seed)
        idx = rng.permutation(n)
        n_test = int(round(n * test_size))
        test_idx, train_idx = idx[:n_test], idx[n_test:]
    Xa = _as_array(X)
    ya = _as_array(y)
    return (
        Xa[train_idx].copy(),
        Xa[test_idx].copy(),
        ya[train_idx].copy(),
        ya[test_idx].copy(),
    )


def train_val_test_split(X, y, val_size: float = 0.2, test_size: float = 0.2, seed: int = 0):
    """Three-way split: the validation set tunes, the test set reports once."""
    X_train, X_rest, y_train, y_rest = train_test_split(
        X, y, test_size=val_size + test_size, seed=seed
    )
    relative = test_size / (val_size + test_size)
    X_val, X_test, y_val, y_test = train_test_split(X_rest, y_rest, test_size=relative, seed=seed)
    return X_train, X_val, X_test, y_train, y_val, y_test


# ---------------------------------------------------------------------------
# Scaling
# ---------------------------------------------------------------------------
class StandardScaler:
    """Centre to mean 0 and scale to unit variance, column by column."""

    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        X = _as_array(X).astype(float)
        # NaN-aware: impute first in a real pipeline, but never let one missing value
        # silently turn the whole column into NaN.
        self.mean_ = np.nanmean(X, axis=0)
        std = np.nanstd(X, axis=0)
        # A constant column has std 0; dividing by it produces NaN. Use 1 instead.
        self.scale_ = np.where(np.nan_to_num(std) == 0.0, 1.0, std)
        return self

    def transform(self, X):
        if self.mean_ is None:
            raise RuntimeError("call fit before transform")
        return (_as_array(X).astype(float) - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)


class MinMaxScaler:
    """Map each column onto [0, 1]."""

    def __init__(self, feature_range=(0.0, 1.0)):
        self.lo, self.hi = feature_range
        self.min_ = None
        self.max_ = None

    def fit(self, X):
        X = _as_array(X).astype(float)
        self.min_ = np.nanmin(X, axis=0)
        span = np.nanmax(X, axis=0) - self.min_
        self.max_ = np.where(np.nan_to_num(span) == 0.0, 1.0, span)
        return self

    def transform(self, X):
        if self.min_ is None:
            raise RuntimeError("call fit before transform")
        unit = (_as_array(X).astype(float) - self.min_) / self.max_
        return self.lo + unit * (self.hi - self.lo)

    def fit_transform(self, X):
        return self.fit(X).transform(X)


# ---------------------------------------------------------------------------
# Missing values and categorical encoding
# ---------------------------------------------------------------------------
class SimpleImputer:
    """Fill missing values with a column statistic.

    strategy: "mean", "median" or "most_frequent". Only the training half is used to
    compute the statistic, which is the whole point.
    """

    def __init__(self, strategy: str = "mean"):
        if strategy not in {"mean", "median", "most_frequent"}:
            raise ValueError("strategy must be mean, median or most_frequent")
        self.strategy = strategy
        self.statistics_ = None

    def fit(self, X):
        frame = pd.DataFrame(_as_array(X))
        if self.strategy == "mean":
            self.statistics_ = frame.mean(axis=0).to_numpy()
        elif self.strategy == "median":
            self.statistics_ = frame.median(axis=0).to_numpy()
        else:
            self.statistics_ = frame.mode(axis=0).iloc[0].to_numpy()
        return self

    def transform(self, X):
        if self.statistics_ is None:
            raise RuntimeError("call fit before transform")
        frame = pd.DataFrame(_as_array(X)).astype(float).copy()
        frame = frame.fillna(pd.Series(self.statistics_, index=frame.columns))
        return frame.to_numpy()

    def fit_transform(self, X):
        return self.fit(X).transform(X)


class OneHotEncoder:
    """Encode each categorical column as 0/1 indicator columns.

    Categories are learned in `fit`, so a value seen only in the test set produces an
    all-zero row rather than a shape mismatch. `handle_unknown="ignore"` is the only
    behaviour implemented, and it is what you almost always want.
    """

    def __init__(self, drop_first: bool = False):
        self.drop_first = drop_first
        self.categories_ = []

    def fit(self, X):
        frame = pd.DataFrame(_as_array(X))
        self.categories_ = []
        for col in frame.columns:
            cats = sorted(frame[col].dropna().astype(str).unique())
            if self.drop_first and len(cats) > 1:
                cats = cats[1:]
            self.categories_.append(cats)
        return self

    def transform(self, X):
        frame = pd.DataFrame(_as_array(X))
        blocks = []
        for col, cats in zip(frame.columns, self.categories_):
            values = frame[col].astype(str).to_numpy()
            blocks.append(np.column_stack([(values == c).astype(float) for c in cats]))
        return np.hstack(blocks)

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def get_feature_names(self):
        names = []
        for i, cats in enumerate(self.categories_):
            names.extend([f"col{i}_{c}" for c in cats])
        return names


# ---------------------------------------------------------------------------
# Outliers and feature selection
# ---------------------------------------------------------------------------
def clip_outliers_iqr(values, k: float = 1.5):
    """Winsorise a numeric column at [Q1 - k*IQR, Q3 + k*IQR].

    Returns (clipped_values, lower, upper). Clipping rather than deleting keeps every
    row, which matters when rows are expensive.
    """
    series = pd.Series(values).astype(float)
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return series.clip(lower, upper).to_numpy(), float(lower), float(upper)


def correlation_with_target(X, y) -> pd.DataFrame:
    """Pearson correlation of each numeric column with a numeric target."""
    X = pd.DataFrame(_as_array(X))
    y = pd.Series(_as_array(y).ravel())
    scores = {col: float(np.corrcoef(X[col].astype(float), y)[0, 1]) for col in X.columns}
    out = pd.DataFrame({"feature": list(scores), "correlation": list(scores.values())})
    return out.reindex(out["correlation"].abs().sort_values(ascending=False).index).reset_index(drop=True)


def top_k_features(X, y, k: int = 5):
    """Indices of the k features most correlated with the target."""
    table = correlation_with_target(X, y)
    names = list(pd.DataFrame(_as_array(X)).columns)
    chosen = [names.index(name) for name in table["feature"].head(k)]
    return sorted(chosen)


class Pipeline:
    """Chain preprocessing steps and a final estimator, fitting each on train only.

    steps = [("impute", SimpleImputer("median")), ("scale", StandardScaler()),
             ("model", LogisticRegressionGD())]

    The last step must implement fit/predict; every earlier step must implement
    fit/transform. Calling `fit` on the training half is what prevents leakage: the
    imputer's median and the scaler's mean never see the validation or test rows.
    """

    def __init__(self, steps):
        if not steps:
            raise ValueError("a pipeline needs at least one step")
        self.steps = list(steps)

    def fit(self, X, y=None):
        Xt = _as_array(X).astype(float) if not isinstance(X, pd.DataFrame) else X
        for name, step in self.steps[:-1]:
            Xt = step.fit_transform(Xt)
        self.steps[-1][1].fit(Xt, y)
        return self

    def _transform(self, X):
        Xt = _as_array(X).astype(float) if not isinstance(X, pd.DataFrame) else X
        for _, step in self.steps[:-1]:
            Xt = step.transform(Xt)
        return Xt

    def predict(self, X):
        return self.steps[-1][1].predict(self._transform(X))

    def predict_proba(self, X):
        return self.steps[-1][1].predict_proba(self._transform(X))

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y).ravel()))

    @property
    def model(self):
        return self.steps[-1][1]


def describe_frame(df: pd.DataFrame) -> pd.DataFrame:
    """A compact profile: dtype, missing count, unique count, min/max for numerics."""
    rows = []
    for col in df.columns:
        s = df[col]
        rows.append(
            {
                "column": col,
                "dtype": str(s.dtype),
                "missing": int(s.isna().sum()),
                "unique": int(s.nunique(dropna=True)),
                "min": s.min() if pd.api.types.is_numeric_dtype(s) else "-",
                "max": s.max() if pd.api.types.is_numeric_dtype(s) else "-",
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import datasets as ds

    frame = ds.students()
    print(describe_frame(frame).to_string(index=False))
    print()

    numeric = ["study_hours", "attendance_pct", "prior_grade", "sleep_hours"]
    X = frame[numeric].to_numpy()
    y = frame["final_score"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, seed=0)
    print("train/test rows:", len(X_train), len(X_test))

    imputer = SimpleImputer("median").fit(X_train)
    X_train_clean = imputer.transform(X_train)
    print("missing before/after imputation:", int(np.isnan(X_train).sum()), int(np.isnan(X_train_clean).sum()))

    # Order matters: impute, then scale, and fit both on the training half only.
    scaler = StandardScaler().fit(X_train_clean)
    scaled = scaler.transform(X_train_clean)
    print("train means after scaling:", np.round(scaled.mean(axis=0), 6))
    print("scaled train std:", np.round(scaled.std(axis=0), 3))

    clipped, lo, hi = clip_outliers_iqr(ds.houses()["price_thousands"])
    print("price clip bounds:", round(lo, 1), round(hi, 1))
    print("rows changed by clipping:", int((clipped != ds.houses()["price_thousands"].to_numpy()).sum()))

    cap = ds.houses()[["neighbourhood"]]
    enc = OneHotEncoder().fit(cap.iloc[:600])
    print("one-hot shape:", enc.transform(cap).shape, enc.get_feature_names())
