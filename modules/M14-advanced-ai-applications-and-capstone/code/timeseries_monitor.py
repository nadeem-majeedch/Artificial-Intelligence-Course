"""timeseries_monitor.py -- forecasting, backtesting and drift monitoring (M14, L14-03).

A daily series with trend, weekly and yearly seasonality, then a *changed* stream: the level
shifts and the noise grows. Three forecasters are backtested on rolling origins, and the same
features are monitored with a population stability index (PSI).

    seasonal naive   tomorrow = same weekday last week
    ridge on lags    28 lag features, linear
    gradient boosting 28 lag features, nonlinear

The point is not which model wins on average. It is that the winner changes after the drift,
and that the monitor flags the change before the error metric does -- which is the argument for
monitoring inputs, not just outputs.

Run ``python timeseries_monitor.py``.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge

rng = np.random.default_rng(0)

N = 760
HORIZON = 14
N_LAGS = 28


# ---------------------------------------------------------------------------
# 1. Data
# ---------------------------------------------------------------------------

def make_series(n=N, drift_at=None, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(n)
    level = 100 + 0.05 * t
    weekly = 8 * np.sin(2 * np.pi * t / 7)
    yearly = 12 * np.sin(2 * np.pi * t / 365)
    noise = r.normal(0, 4, n)
    y = level + weekly + yearly + noise
    if drift_at is not None:
        y[drift_at:] += 18                      # level shift
        y[drift_at:] += r.normal(0, 4, n - drift_at)   # extra noise
    return y


def lag_matrix(y, n_lags=N_LAGS):
    """Rows are lag features for predicting y[t]; target is y[t]."""
    X = np.column_stack([y[n_lags - i - 1: len(y) - i - 1] for i in range(n_lags)])
    target = y[n_lags:]
    return X, target


# ---------------------------------------------------------------------------
# 2. Forecasters
# ---------------------------------------------------------------------------

def seasonal_naive(y_hist, horizon=HORIZON, season=7):
    last = y_hist[-season:]
    return np.array([last[i % season] for i in range(horizon)])


def fit_predict(model, X_tr, y_tr, X_future):
    model.fit(X_tr, y_tr)
    return model.predict(X_future)


# ---------------------------------------------------------------------------
# 3. Rolling-origin backtest
# ---------------------------------------------------------------------------

def backtest(y, model_name, n_folds=8):
    errors, covered, widths = [], [], []
    start = len(y) - n_folds * HORIZON
    for f in range(n_folds):
        cut = start + f * HORIZON
        hist = y[:cut]
        actual = y[cut:cut + HORIZON]

        if model_name == "seasonal naive":
            pred = seasonal_naive(hist)
            resid = np.abs(y[N_LAGS:cut] - seasonal_naive_multi(y, cut))
            lo = pred - np.quantile(resid, 0.9)
            hi = pred + np.quantile(resid, 0.9)
        else:
            X, t = lag_matrix(y[:cut])
            X_all, _ = lag_matrix(y[:cut + HORIZON])
            X_future = X_all[len(X):]
            if model_name == "ridge":
                m = Ridge(alpha=1.0)
            else:
                m = GradientBoostingRegressor(n_estimators=120, max_depth=2, random_state=0)
            pred = fit_predict(m, X, t, X_future)

            # one-step residuals on the training window give the interval width
            in_sample = m.predict(X)
            resid = np.abs(t - in_sample)
            lo = pred - np.quantile(resid, 0.9)
            hi = pred + np.quantile(resid, 0.9)

        errors.append(np.abs(actual - pred).mean())
        covered.append(float(((actual >= lo) & (actual <= hi)).mean()))
        widths.append(float((hi - lo).mean()))
    return {"mae": float(np.mean(errors)), "coverage": float(np.mean(covered)),
            "width": float(np.mean(widths))}


def seasonal_naive_multi(y, cut):
    """In-sample one-step seasonal-naive predictions up to `cut`, for residuals."""
    idx = np.arange(N_LAGS, cut)
    return y[idx - 7]


# ---------------------------------------------------------------------------
# 4. Drift monitoring
# ---------------------------------------------------------------------------

def psi(reference, current, bins=10):
    """Population stability index: share-of-population shift between two samples."""
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    ref = np.histogram(reference, bins=edges)[0] / len(reference)
    cur = np.histogram(current, bins=edges)[0] / len(current)
    eps = 1e-6
    return float(np.sum((cur - ref) * np.log((cur + eps) / (ref + eps))))


def drift_report(y_ref, y_new, name):
    X_ref, _ = lag_matrix(y_ref)
    X_new, _ = lag_matrix(y_new)
    vals = []
    for j in [0, 6, 13, 27]:
        vals.append((j, psi(X_ref[:, j], X_new[:, j])))
    worst = max(vals, key=lambda kv: kv[1])
    status = ("stable" if worst[1] < 0.1 else
              "monitor" if worst[1] < 0.25 else "alert")
    print(f"  {name:22s} worst PSI {worst[1]:6.3f} at lag {worst[0] + 1:2d}  -> {status}")
    return worst[1]


# ---------------------------------------------------------------------------
# 5. Demo
# ---------------------------------------------------------------------------

def main():
    y = make_series()
    drift_at = 560
    y_drift = make_series(drift_at=drift_at)

    print("=" * 82)
    print("1. Rolling-origin backtest, 8 folds x 14-day horizon")
    print("=" * 82)
    print(f"  {'model':16s} {'MAE':>7} {'80% coverage':>14} {'mean width':>11}")
    results = {}
    for name in ("seasonal naive", "ridge", "boosting"):
        r = backtest(y, name)
        results[name] = r
        print(f"  {name:16s} {r['mae']:7.2f} {r['coverage']:14.2f} {r['width']:11.2f}")
    print("\n  Coverage above 0.80 means the intervals are too wide; below 0.80, too narrow.")

    print("\n" + "=" * 82)
    print("2. Drift detection with PSI")
    print("=" * 82)
    stable = drift_report(y[:drift_at], y[drift_at:], "after the level shift")
    print("\n  PSI thresholds used: <0.10 stable, 0.10-0.25 monitor, >0.25 alert.")
    print(f"  flagged value: {stable:.3f}")

    print("\n" + "=" * 82)
    print("3. Retrain or not? Error before and after the drift")
    print("=" * 82)
    pre = make_series(drift_at=None)[:]
    print(f"  {'model':16s} {'MAE before':>11} {'MAE after':>10} {'change':>8}")
    for name in ("seasonal naive", "ridge", "boosting"):
        before = backtest(pre[:drift_at], name)["mae"]
        after = backtest(y_drift[drift_at:], name)["mae"]
        print(f"  {name:16s} {before:11.2f} {after:10.2f} {after - before:+8.2f}")
    print("\n  An error metric tells you the model is worse. A drift metric tells you why,")
    print("  and which feature moved -- which is what you need before deciding to retrain.")

    print("\n" + "=" * 82)
    print("4. Monitoring plan this experiment implies")
    print("=" * 82)
    steps = [
        "log the 28 lag features and the forecast for every request",
        "compute PSI weekly against the training distribution, per feature",
        "alert at PSI > 0.25 on any feature, or > 0.10 on three",
        "track rolling MAE with the same window as the backtest",
        "retrain only when both drift and error move; otherwise investigate the data",
    ]
    for s in steps:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
