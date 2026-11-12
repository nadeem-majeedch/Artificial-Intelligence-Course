"""Linear models from first principles: OLS, gradient descent, ridge, lasso.

The point of this module is that the closed-form solution, the iterative solution and
the regularised solutions all estimate the same object from different directions, and
you can check them against each other.

Run `python linreg.py` to reproduce the numbers used in L06-03 and L06-06.
"""

from __future__ import annotations

from itertools import combinations_with_replacement

import numpy as np

__all__ = [
    "LinearRegression",
    "LinearRegressionGD",
    "PolynomialFeatures",
    "Ridge",
    "Lasso",
    "mse",
    "rmse",
    "mae",
    "r2_score",
    "adjusted_r2",
    "regression_report",
]


def _check_X(X):
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    return X


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def mse(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.mean((y_true - y_pred) ** 2))


def rmse(y_true, y_pred) -> float:
    """Root mean squared error, in the units of the target."""
    return float(np.sqrt(mse(y_true, y_pred)))


def mae(y_true, y_pred) -> float:
    """Mean absolute error: less sensitive to a single large miss than RMSE."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.mean(np.abs(y_true - y_pred)))


def r2_score(y_true, y_pred) -> float:
    """Fraction of variance explained; 0 means 'no better than predicting the mean'.

    Can go negative on a test set, which is informative: the model is worse than the
    mean baseline, usually because it was fitted to noise.
    """
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot else 0.0


def adjusted_r2(y_true, y_pred, n_features: int) -> float:
    """R^2 penalised for the number of predictors; rises only if a feature earns it."""
    n = len(np.asarray(y_true))
    r2 = r2_score(y_true, y_pred)
    if n - n_features - 1 <= 0:
        return float("nan")
    return float(1 - (1 - r2) * (n - 1) / (n - n_features - 1))


def regression_report(y_true, y_pred, n_features: int | None = None) -> dict:
    out = {
        "mse": mse(y_true, y_pred),
        "rmse": rmse(y_true, y_pred),
        "mae": mae(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
    }
    if n_features is not None:
        out["adj_r2"] = adjusted_r2(y_true, y_pred, n_features)
    return out


# ---------------------------------------------------------------------------
# Ordinary least squares
# ---------------------------------------------------------------------------
class LinearRegression:
    """Least squares by the normal equations, solved with a stable least-squares call.

    The textbook form is w = (X^T X)^-1 X^T y. We compute it with np.linalg.lstsq,
    which uses an SVD instead of inverting X^T X — the inverse squares the condition
    number, so on collinear features the textbook form loses precision.
    """

    def __init__(self, fit_intercept: bool = True):
        self.fit_intercept = fit_intercept
        self.coef_ = None
        self.intercept_ = 0.0

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y, float).ravel()
        if self.fit_intercept:
            self.mean_ = X.mean(axis=0)
            self.y_mean_ = y.mean()
            Xc = X - self.mean_
            yc = y - self.y_mean_
        else:
            Xc, yc = X, y
        self.coef_, *_ = np.linalg.lstsq(Xc, yc, rcond=None)
        self.intercept_ = float(self.y_mean_ - self.mean_ @ self.coef_) if self.fit_intercept else 0.0
        return self

    def predict(self, X):
        return _check_X(X) @ self.coef_ + self.intercept_

    def score(self, X, y):
        return r2_score(y, self.predict(X))


class LinearRegressionGD:
    """The same model fitted by gradient descent, one epoch = one pass over the data.

    With standardised features and lr = 0.1 this converges in a few hundred epochs. With
    raw features the same learning rate diverges, because the loss surface is a long
    thin valley: that is the practical reason scaling exists.
    """

    def __init__(self, lr: float = 0.1, epochs: int = 500, standardize: bool = False):
        self.lr = lr
        self.epochs = epochs
        self.standardize = standardize
        self.coef_ = None
        self.intercept_ = 0.0
        self.loss_history_ = []

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y, float).ravel()
        if self.standardize:
            self.mean_ = X.mean(axis=0)
            # A unit (not zero) scale for constant columns avoids dividing by zero.
            self.scale_ = np.where(X.std(axis=0) == 0, 1.0, X.std(axis=0))
            X = (X - self.mean_) / self.scale_
        else:
            self.mean_ = np.zeros(X.shape[1])
            self.scale_ = np.ones(X.shape[1])

        n, d = X.shape
        self.coef_ = np.zeros(d)
        self.intercept_ = float(y.mean())
        self.loss_history_ = []

        for _ in range(self.epochs):
            error = X @ self.coef_ + self.intercept_ - y
            self.coef_ -= self.lr * (X.T @ error) / n
            self.intercept_ -= self.lr * error.mean()
            self.loss_history_.append(float(np.mean(error**2)))
        return self

    def predict(self, X):
        X = (_check_X(X) - self.mean_) / self.scale_
        return X @ self.coef_ + self.intercept_

    def score(self, X, y):
        return r2_score(y, self.predict(X))


# ---------------------------------------------------------------------------
# Polynomial features
# ---------------------------------------------------------------------------
class PolynomialFeatures:
    """All monomials up to `degree`, including interactions between features.

    With one feature the result is [x, x^2, ..., x^d]; with two it also includes
    x1*x2, x1^2*x2 and so on. The number of columns grows combinatorially, which is
    exactly why high-degree polynomial regression overfits so quickly.
    """

    def __init__(self, degree: int = 2, include_bias: bool = False):
        self.degree = degree
        self.include_bias = include_bias
        self.powers_ = None

    def fit(self, X, y=None):
        X = _check_X(X)
        d = X.shape[1]
        powers = []
        if self.include_bias:
            powers.append(tuple([0] * d))
        for total in range(1, self.degree + 1):
            for combo in combinations_with_replacement(range(d), total):
                powers.append(tuple(combo.count(j) for j in range(d)))
        self.powers_ = powers
        return self

    def transform(self, X):
        X = _check_X(X)
        return np.column_stack(
            [np.prod(X ** np.array(power), axis=1) for power in self.powers_]
        )

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)

    @property
    def n_output_features_(self):
        return len(self.powers_ or [])


# ---------------------------------------------------------------------------
# Regularised regression
# ---------------------------------------------------------------------------
class Ridge:
    """L2-regularised least squares: minimise |y - Xw|^2 + alpha |w|^2.

    The closed form is w = (X^T X + alpha I)^-1 X^T y. The penalty shrinks every
    coefficient towards zero but never exactly to zero, so ridge keeps all features —
    useful when many predictors each contribute a little.
    """

    def __init__(self, alpha: float = 1.0, fit_intercept: bool = True):
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.coef_ = None
        self.intercept_ = 0.0

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y, float).ravel()
        if self.fit_intercept:
            self.mean_ = X.mean(axis=0)
            self.y_mean_ = y.mean()
            Xc, yc = X - self.mean_, y - self.y_mean_
        else:
            self.mean_, self.y_mean_ = np.zeros(X.shape[1]), 0.0
            Xc, yc = X, y

        d = Xc.shape[1]
        A = Xc.T @ Xc + self.alpha * np.eye(d)
        self.coef_ = np.linalg.solve(A, Xc.T @ yc)
        self.intercept_ = float(self.y_mean_ - self.mean_ @ self.coef_) if self.fit_intercept else 0.0
        return self

    def predict(self, X):
        return _check_X(X) @ self.coef_ + self.intercept_

    def score(self, X, y):
        return r2_score(y, self.predict(X))


class Lasso:
    """L1-regularised least squares, fitted by coordinate descent.

    The L1 penalty has a corner at zero, so the solution is sparse: some coefficients
    become exactly 0 and the model performs feature selection. The soft-threshold
    update in `_soft` is the whole algorithm.

    Features are standardised internally so that one alpha is comparable across
    columns measured in different units.
    """

    def __init__(self, alpha: float = 0.1, epochs: int = 300, tol: float = 1e-6):
        self.alpha = alpha
        self.epochs = epochs
        self.tol = tol
        self.coef_ = None
        self.intercept_ = 0.0

    @staticmethod
    def _soft(value: float, threshold: float) -> float:
        if value > threshold:
            return value - threshold
        if value < -threshold:
            return value + threshold
        return 0.0

    def fit(self, X, y):
        X = _check_X(X)
        y = np.asarray(y, float).ravel()
        self.x_mean_ = X.mean(axis=0)
        self.x_scale_ = np.where(X.std(axis=0) == 0, 1.0, X.std(axis=0))
        Xs = (X - self.x_mean_) / self.x_scale_
        self.y_mean_ = y.mean()
        yc = y - self.y_mean_

        n, d = Xs.shape
        w = np.zeros(d)
        col_sq = (Xs**2).sum(axis=0) / n
        for _ in range(self.epochs):
            max_change = 0.0
            for j in range(d):
                residual = yc - Xs @ w + Xs[:, j] * w[j]
                rho = (Xs[:, j] @ residual) / n
                new = self._soft(rho, self.alpha) / col_sq[j] if col_sq[j] else 0.0
                max_change = max(max_change, abs(new - w[j]))
                w[j] = new
            if max_change < self.tol:
                break

        # Convert back to the original feature scale.
        self.coef_ = w / self.x_scale_
        self.intercept_ = float(self.y_mean_ - self.x_mean_ @ self.coef_)
        self.n_iter_ = _
        return self

    def predict(self, X):
        return _check_X(X) @ self.coef_ + self.intercept_

    def score(self, X, y):
        return r2_score(y, self.predict(X))


if __name__ == "__main__":
    import datasets as ds
    from prep import StandardScaler, train_test_split

    frame = ds.students()
    numeric = ["study_hours", "attendance_pct", "prior_grade", "sleep_hours"]
    clean = frame[numeric].fillna(frame[numeric].median())
    X = clean.to_numpy()
    y = frame["final_score"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, seed=0)

    ols = LinearRegression().fit(X_train, y_train)
    print("OLS coefficients:", dict(zip(numeric, np.round(ols.coef_, 3))), "intercept", round(ols.intercept_, 2))
    print("test:", {k: round(v, 3) for k, v in regression_report(y_test, ols.predict(X_test), len(numeric)).items()})
    print()

    gd_raw = LinearRegressionGD(lr=0.1, epochs=500).fit(X_train, y_train)
    gd_scaled = LinearRegressionGD(lr=0.1, epochs=500, standardize=True).fit(X_train, y_train)
    print("GD raw final MSE:   ", round(gd_raw.loss_history_[-1], 3))
    print("GD scaled final MSE:", round(gd_scaled.loss_history_[-1], 3))
    print("GD scaled test R2:  ", round(gd_scaled.score(X_test, y_test), 4))
    print()

    poly = PolynomialFeatures(degree=2).fit(X_train)
    Xp_train, Xp_test = poly.transform(X_train), poly.transform(X_test)
    model = LinearRegression().fit(Xp_train, y_train)
    print("degree-2 columns:", poly.n_output_features_)
    print("degree-2 test R2:", round(model.score(Xp_test, y_test), 4))
    print()

    print(f"{'alpha':>8s} {'ridge R2':>10s} {'lasso R2':>10s} {'lasso non-zero':>15s}")
    for alpha in [0.0, 1.0, 10.0, 100.0]:
        ridge = Ridge(alpha=alpha).fit(X_train, y_train)
        lasso = Lasso(alpha=alpha if alpha else 1e-8).fit(X_train, y_train)
        print(
            f"{alpha:8.1f} {ridge.score(X_test, y_test):10.4f} "
            f"{lasso.score(X_test, y_test):10.4f} {int(np.sum(np.abs(lasso.coef_) > 1e-8)):15d}"
        )
