"""fairness.py -- measuring and mitigating disparity (M13, L13-01 / LAB-13-01).

Four metric families, because they disagree and the disagreement is the lesson:

    independence     demographic parity, disparate impact (the 80% rule)
    separation       equal opportunity (TPR gap), equalised odds (TPR + FPR)
    sufficiency      calibration within groups (predicted vs observed rate)
    individual       what a single person could object to, per decision

Two mitigations, at different stages:

    pre-processing   Kamiran-Calders reweighing, applied to training weights
    post-processing  group-specific thresholds chosen for equalised odds

Neither is a solution to a biased label. Both are measurable, which is the point.

Run ``python fairness.py`` for the audit tables quoted in L13-01 and LAB-13-01.
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from rai_data import loans, recruitment, student


# ---------------------------------------------------------------------------
# 1. Group metrics
# ---------------------------------------------------------------------------

def group_metrics(y_true, y_pred, group, names=None) -> dict:
    """Selection rate, TPR, FPR, PPV and accuracy per group."""
    y_true, y_pred, group = map(np.asarray, (y_true, y_pred, group))
    names = names or sorted(set(group.tolist()))
    out = {}
    for name in names:
        mask = group == name
        yt, yp = y_true[mask], y_pred[mask]
        pos, neg = yt == 1, yt == 0
        tp = float((yp[pos] == 1).mean()) if pos.any() else float("nan")
        fp = float((yp[neg] == 1).mean()) if neg.any() else float("nan")
        ppv_denom = yp == 1
        ppv = float(yt[ppv_denom].mean()) if ppv_denom.any() else float("nan")
        out[name] = {
            "n": int(mask.sum()),
            "selection_rate": float(yp.mean()),
            "tpr": tp,
            "fpr": fp,
            "ppv": ppv,
            "accuracy": float((yt == yp).mean()),
            "base_rate": float(yt.mean()),
        }
    return out


def demographic_parity_difference(metrics: dict) -> float:
    rates = [m["selection_rate"] for m in metrics.values()]
    return float(max(rates) - min(rates))


def disparate_impact_ratio(metrics: dict) -> float:
    """The 80% rule: lowest selection rate divided by the highest."""
    rates = [m["selection_rate"] for m in metrics.values()]
    return float(min(rates) / max(rates)) if max(rates) > 0 else float("nan")


def equal_opportunity_difference(metrics: dict) -> float:
    tprs = [m["tpr"] for m in metrics.values()]
    return float(max(tprs) - min(tprs))


def equalized_odds_difference(metrics: dict) -> float:
    gaps = []
    for key in ("tpr", "fpr"):
        vals = [m[key] for m in metrics.values()]
        gaps.append(max(vals) - min(vals))
    return float(max(gaps))


def calibration_by_group(y_true, proba, group, names=None, bins: int = 5) -> dict:
    """Mean predicted probability against observed positive rate, per group."""
    proba, y_true, group = map(np.asarray, (proba, y_true, group))
    names = names or sorted(set(group.tolist()))
    out = {}
    for name in names:
        mask = group == name
        p, y = proba[mask], y_true[mask]
        edges = np.quantile(p, np.linspace(0, 1, bins + 1))
        rows = []
        for i in range(bins):
            lo, hi = edges[i], edges[i + 1]
            sel = (p >= lo) & (p <= hi if i == bins - 1 else p < hi)
            if sel.sum() < 5:
                continue
            rows.append({"bin": i, "n": int(sel.sum()),
                         "mean_pred": float(p[sel].mean()),
                         "observed": float(y[sel].mean())})
        out[name] = {"rows": rows,
                     "mean_pred": float(p.mean()), "observed": float(y.mean()),
                     "brier": float(np.mean((p - y) ** 2))}
    return out


def summarize(y_true, y_pred, group, names=None) -> dict:
    metrics = group_metrics(y_true, y_pred, group, names)
    return {
        "groups": metrics,
        "demographic_parity_difference": demographic_parity_difference(metrics),
        "disparate_impact_ratio": disparate_impact_ratio(metrics),
        "equal_opportunity_difference": equal_opportunity_difference(metrics),
        "equalized_odds_difference": equalized_odds_difference(metrics),
        "accuracy": float(np.mean(np.asarray(y_true) == np.asarray(y_pred))),
    }


# ---------------------------------------------------------------------------
# 2. Pre-processing mitigation: reweighing
# ---------------------------------------------------------------------------

def reweighing_weights(y, group) -> np.ndarray:
    """Kamiran-Calders weights that make label and group independent.

    w(y, g) = P(y) * P(g) / P(y, g). This equalises P(g | y) across groups, not the
    raw cell mass. Mean-normalised to 1.
    """
    y, group = np.asarray(y), np.asarray(group)
    n = len(y)
    weights = np.ones(n)
    for label in np.unique(y):
        for g in np.unique(group):
            mask = (y == label) & (group == g)
            if mask.sum() == 0:
                continue
            p_y = (y == label).mean()
            p_g = (group == g).mean()
            p_yg = mask.mean()
            weights[mask] = (p_y * p_g) / p_yg
    return weights / weights.mean()


# ---------------------------------------------------------------------------
# 3. Post-processing mitigation: group-specific thresholds
# ---------------------------------------------------------------------------

def choose_thresholds(y_true, scores, group, names=None, grid=None) -> dict:
    """Search per-group thresholds that minimise the equalised-odds gap.

    Ties are broken by accuracy, and the search reports the accuracy cost so the
    trade-off is explicit rather than hidden.
    """
    y_true, scores, group = map(np.asarray, (y_true, scores, group))
    names = names or sorted(set(group.tolist()))
    grid = grid if grid is not None else np.linspace(0.05, 0.95, 37)
    best = None
    for t_a in grid:
        for t_b in grid:
            thresholds = {names[0]: t_a, names[1]: t_b}
            pred = np.zeros(len(y_true), dtype=int)
            for name in names:
                mask = group == name
                pred[mask] = (scores[mask] >= thresholds[name]).astype(int)
            m = summarize(y_true, pred, group, names)
            gap = m["equalized_odds_difference"]
            acc = m["accuracy"]
            key = (round(gap, 4), -acc)
            if best is None or key < best[0]:
                best = (key, thresholds, m)
    return {"thresholds": best[1], "metrics": best[2], "gap": best[0][0],
            "accuracy": best[2]["accuracy"]}


# ---------------------------------------------------------------------------
# 4. Audit helper
# ---------------------------------------------------------------------------

def train_and_audit(data: dict, drop_features=(), seed: int = 0, reweigh: bool = False,
                    balance_thresholds: bool = False) -> dict:
    """Fit logistic regression, then report the full fairness summary."""
    X, y, group = data["X"], data["y"], data["group"]
    keep = [i for i, name in enumerate(data["feature_names"]) if name not in drop_features]
    X_used = X[:, keep]
    names = [data["feature_names"][i] for i in keep]
    X_tr, X_te, y_tr, y_te, g_tr, g_te = train_test_split(
        X_used, y, group, test_size=0.3, random_state=seed, stratify=y)
    model = LogisticRegression(max_iter=2000, random_state=seed)
    sample_weight = reweighing_weights(y_tr, g_tr) if reweigh else None
    model.fit(X_tr, y_tr, sample_weight=sample_weight)
    proba = model.predict_proba(X_te)[:, 1]
    pred = (proba >= 0.5).astype(int)
    summary = summarize(y_te, pred, g_te, data["group_names"])
    summary.update({
        "model": model, "features_used": names, "auc": float(roc_auc_score(y_te, proba)),
        "X_test": X_te, "y_test": y_te, "group_test": g_te, "proba": proba,
    })
    if balance_thresholds:
        balanced = choose_thresholds(y_te, proba, g_te, data["group_names"])
        summary["balanced"] = balanced
    return summary


def print_summary(title: str, s: dict) -> None:
    print(f"\n{title}")
    print(f"  accuracy {s['accuracy']:.3f}  AUC {s.get('auc', float('nan')):.3f}  "
          f"features {s.get('features_used', [])}")
    print(f"  {'group':6s} {'n':>5} {'select':>7} {'TPR':>6} {'FPR':>6} "
          f"{'PPV':>6} {'base':>6}")
    for name, m in s["groups"].items():
        print(f"  {name:6s} {m['n']:5d} {m['selection_rate']:7.3f} {m['tpr']:6.3f} "
              f"{m['fpr']:6.3f} {m['ppv']:6.3f} {m['base_rate']:6.3f}")
    print(f"  DP difference {s['demographic_parity_difference']:.3f}   "
          f"DI ratio {s['disparate_impact_ratio']:.3f}   "
          f"EOpp gap {s['equal_opportunity_difference']:.3f}   "
          f"EOdds gap {s['equalized_odds_difference']:.3f}")
    if "balanced" in s:
        b = s["balanced"]
        print(f"  balanced thresholds {b['thresholds']}  gap {b['gap']:.3f}  "
              f"accuracy {b['accuracy']:.3f} (baseline {s['accuracy']:.3f})")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 84)
    print("1. Recruitment: label bias learned from features")
    print("=" * 84)
    rec = recruitment()
    base = train_and_audit(rec)
    print_summary("baseline", base)

    print("\n  reweighing (pre-processing):")
    rw = train_and_audit(rec, reweigh=True)
    print_summary("reweighed", rw)

    print("\n  group-specific thresholds (post-processing):")
    bal = train_and_audit(rec, balance_thresholds=True)
    print_summary("balanced thresholds", bal)

    print("\n  removing the referral feature (a privilege proxy):")
    no_ref = train_and_audit(rec, drop_features=("referral",))
    print_summary("without referral", no_ref)

    print("\n" + "=" * 84)
    print("2. Student: proxy feature drives part of the disparity")
    print("=" * 84)
    st = student()
    s1 = train_and_audit(st)
    print_summary("with tutoring_access", s1)
    s2 = train_and_audit(st, drop_features=("tutoring_access",))
    print_summary("without tutoring_access", s2)
    print(f"\n  accuracy cost of dropping the proxy: "
          f"{s1['accuracy'] - s2['accuracy']:+.3f}")

    print("\n" + "=" * 84)
    print("3. Loans: calibration differs by group even at equal accuracy")
    print("=" * 84)
    ln = loans()
    s3 = train_and_audit(ln)
    print_summary("loans", s3)
    cal = calibration_by_group(s3["y_test"], s3["proba"], s3["group_test"],
                               ln["group_names"], bins=4)
    for g, row in cal.items():
        print(f"  group {g}: mean predicted {row['mean_pred']:.3f}  observed "
              f"{row['observed']:.3f}  Brier {row['brier']:.3f}")
        for b in row["rows"]:
            print(f"    bin {b['bin']}: n={b['n']:4d} pred {b['mean_pred']:.3f} "
                  f"observed {b['observed']:.3f}")

    print("\n" + "=" * 84)
    print("4. The trade-off, summarised")
    print("=" * 84)
    print(f"  {'variant':30s} {'accuracy':>9} {'DP diff':>8} {'EOpp gap':>9}")
    rows = [("recruitment baseline", base), ("recruitment reweighed", rw),
            ("recruitment without referral", no_ref),
            ("student with proxy", s1), ("student without proxy", s2),
            ("loans", s3)]
    for label, s in rows:
        print(f"  {label:30s} {s['accuracy']:9.3f} "
              f"{s['demographic_parity_difference']:8.3f} "
              f"{s['equal_opportunity_difference']:9.3f}")
    print("\n  No row dominates. Reweighing changes who is hired, not who is qualified;")
    print("  dropping a proxy costs accuracy; balancing thresholds trades accuracy for parity.")


if __name__ == "__main__":
    main()
