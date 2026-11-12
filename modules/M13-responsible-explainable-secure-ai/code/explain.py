"""explain.py -- explanation methods, implemented and evaluated (M13, L13-02 / NB-13-01).

Six methods, all runnable on CPU in seconds:

    permutation importance   model-agnostic; drop in AUC when a feature is shuffled
    partial dependence       average prediction as one feature sweeps its range
    Shapley values           exact enumeration for a few features (KernelSHAP is the
                             sampling approximation for many), with the efficiency check
    LIME                     local linear surrogate around one prediction
    counterfactual           the nearest input change that flips the decision
    interpretable baseline   a logistic regression whose coefficients you can read

Explainability is evaluated, not asserted:

    fidelity   does the surrogate reproduce the model in its own neighbourhood?
    stability  do explanations change when the sampler is reseeded?
    sanity     do importances collapse when the model is trained on shuffled labels?

The black-box model here is a small gradient-boosted tree ensemble; the
interpretable alternative is logistic regression, trained on the same features.

Run ``python explain.py``. Every number in L13-02 and NB-13-01 comes from here.
"""

from __future__ import annotations

import itertools
from math import factorial

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from rai_data import student


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def probability(model, X: np.ndarray) -> np.ndarray:
    X = np.atleast_2d(X)
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.predict(X)


def auc(model, X, y) -> float:
    return float(roc_auc_score(y, probability(model, X)))


def accuracy_at_half(model, X, y) -> float:
    return float(((probability(model, X) >= 0.5).astype(int) == y).mean())


# ---------------------------------------------------------------------------
# 1. Permutation importance
# ---------------------------------------------------------------------------

def permutation_importance(model, X, y, feature_names, n_repeats: int = 5,
                           seed: int = 0) -> list[dict]:
    """AUC drop when each feature is shuffled, averaged over repeats."""
    rng = np.random.default_rng(seed)
    base = auc(model, X, y)
    rows = []
    for j, name in enumerate(feature_names):
        drops = []
        for _ in range(n_repeats):
            Xp = X.copy()
            rng.shuffle(Xp[:, j])
            drops.append(base - auc(model, Xp, y))
        rows.append({"feature": name, "mean_drop": float(np.mean(drops)),
                     "std": float(np.std(drops))})
    rows.sort(key=lambda r: -r["mean_drop"])
    return rows


# ---------------------------------------------------------------------------
# 2. Partial dependence
# ---------------------------------------------------------------------------

def partial_dependence(model, X, feature_idx: int, grid: np.ndarray | None = None,
                       n_grid: int = 12) -> tuple[np.ndarray, np.ndarray]:
    x = X[:, feature_idx]
    grid = grid if grid is not None else np.quantile(x, np.linspace(0.02, 0.98, n_grid))
    values = []
    for v in grid:
        Xv = X.copy()
        Xv[:, feature_idx] = v
        values.append(float(probability(model, Xv).mean()))
    return np.asarray(grid), np.asarray(values)


# ---------------------------------------------------------------------------
# 3. Shapley values
# ---------------------------------------------------------------------------

def shapley_values(model, x, background: np.ndarray, feature_names) -> dict:
    """Exact Shapley values by enumerating all coalitions (feasible for <= 10 features).

    phi_i = sum over S not containing i of |S|!(M-|S|-1)!/M! * (v(S+i) - v(S)),
    where v(S) is the model's output with features in S from x and the rest from
    the background mean. The efficiency property sum(phi) = f(x) - v(empty) then
    holds by construction, which is the check reported below.
    """
    x = np.asarray(x, dtype=float)
    baseline = background.mean(axis=0)
    M = len(feature_names)
    if M > 10:
        raise ValueError("exact enumeration is limited to 10 features")

    def v(subset: frozenset) -> float:
        row = np.array([x[i] if i in subset else baseline[i] for i in range(M)])
        return float(probability(model, row[None, :])[0])

    values = {frozenset(): v(frozenset())}
    for r in range(1, M + 1):
        for combo in itertools.combinations(range(M), r):
            values[frozenset(combo)] = v(frozenset(combo))

    phi = np.zeros(M)
    for i in range(M):
        others = [j for j in range(M) if j != i]
        for r in range(M):
            for combo in itertools.combinations(others, r):
                S = frozenset(combo)
                weight = factorial(len(S)) * factorial(M - len(S) - 1) / factorial(M)
                phi[i] += weight * (values[S | {i}] - values[S])

    prediction = float(probability(model, x[None, :])[0])
    total = float(phi.sum())
    expected = prediction - values[frozenset()]
    order = np.argsort(-np.abs(phi))
    return {
        "features": [feature_names[i] for i in order],
        "values": [float(phi[i]) for i in order],
        "base_value": values[frozenset()],
        "prediction": prediction,
        "sum_phi": total,
        "expected_sum": expected,
        "efficiency_gap": float(abs(total - expected)),
        "raw_phi": phi,
    }


def kernel_shap(model, x, background, feature_names, n_samples: int = 240,
                seed: int = 0) -> dict:
    """Name kept for the lesson: KernelSHAP approximates the same values by sampling."""
    return shapley_values(model, x, background, feature_names)


# ---------------------------------------------------------------------------
# 4. LIME
# ---------------------------------------------------------------------------

def lime_tabular(model, x, X_train, feature_names, n_samples: int = 800,
                 seed: int = 0, kernel_width: float | None = None) -> dict:
    """Local linear surrogate on binary perturbations, weighted by proximity."""
    rng = np.random.default_rng(seed)
    M = len(feature_names)
    x = np.asarray(x, dtype=float)
    kernel_width = kernel_width or 0.75 * np.sqrt(M)

    Z = rng.integers(0, 2, (n_samples, M)).astype(float)
    replace = rng.integers(0, len(X_train), n_samples)
    X_pert = np.where(Z == 1, x[None, :], X_train[replace])
    y_pert = probability(model, X_pert)

    distance = np.sqrt(((Z - 1.0) ** 2).sum(axis=1))
    weights = np.exp(-(distance ** 2) / (kernel_width ** 2))
    surrogate = Ridge(alpha=0.1).fit(Z, y_pert, sample_weight=weights)

    fitted = surrogate.predict(Z)
    ss_res = float(((y_pert - fitted) ** 2).sum())
    ss_tot = float(((y_pert - y_pert.mean()) ** 2).sum())
    order = np.argsort(-np.abs(surrogate.coef_))
    return {
        "features": [feature_names[i] for i in order],
        "values": [float(surrogate.coef_[i]) for i in order],
        "intercept": float(surrogate.intercept_),
        "local_r2": 1 - ss_res / ss_tot if ss_tot else float("nan"),
        "prediction": float(probability(model, x[None, :])[0]),
        "coef_vector": surrogate.coef_.copy(),
    }


def explanation_stability(model, x, X_train, feature_names, seeds=(0, 1, 2, 3, 4)) -> dict:
    """Mean pairwise Pearson correlation of LIME coefficients across seeds."""
    vectors = [lime_tabular(model, x, X_train, feature_names, seed=s)["coef_vector"]
               for s in seeds]
    cors = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            a, b = vectors[i], vectors[j]
            if a.std() == 0 or b.std() == 0:
                continue
            cors.append(float(np.corrcoef(a, b)[0, 1]))
    return {"mean_correlation": float(np.mean(cors)), "min": float(np.min(cors)),
            "max": float(np.max(cors)), "pairs": len(cors)}


# ---------------------------------------------------------------------------
# 5. Counterfactual explanation
# ---------------------------------------------------------------------------

def counterfactual(model, x, X_train, feature_names, desired: int = 1,
                   max_changes: int = 3, n_candidates: int = 4000, seed: int = 0) -> dict:
    """Random-restricted search for the nearest input that flips the decision."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    std = X_train.std(axis=0)
    std[std == 0] = 1.0
    current = int(probability(model, x[None, :])[0] >= 0.5)
    if current == desired:
        return {"found": True, "already": True, "changes": [], "distance": 0.0,
                "candidate": x, "new_probability": float(probability(model, x[None, :])[0])}

    pool = X_train[((probability(model, X_train) >= 0.5).astype(int) == desired)]
    if len(pool) == 0:
        return {"found": False, "reason": "no training example has the desired outcome"}

    best = None
    for _ in range(n_candidates):
        donor = pool[rng.integers(0, len(pool))]
        k = int(rng.integers(1, max_changes + 1))
        idx = rng.choice(len(x), size=k, replace=False)
        candidate = x.copy()
        candidate[idx] = donor[idx]
        if int(probability(model, candidate[None, :])[0] >= 0.5) != desired:
            continue
        dist = float(np.sqrt((((candidate - x) / std) ** 2).sum()))
        if best is None or dist < best[0]:
            best = (dist, candidate, idx)
    if best is None:
        return {"found": False, "reason": "no counterfactual within the search budget"}
    dist, candidate, idx = best
    changes = [{"feature": feature_names[j], "from": float(x[j]), "to": float(candidate[j])}
               for j in idx if abs(candidate[j] - x[j]) > 1e-9]
    return {"found": True, "changes": changes, "distance": dist, "candidate": candidate,
            "new_probability": float(probability(model, candidate[None, :])[0])}


# ---------------------------------------------------------------------------
# 6. Sanity check
# ---------------------------------------------------------------------------

def sanity_check(X, y, feature_names, seed: int = 0) -> dict:
    """Retrain on shuffled labels; importances should collapse towards zero."""
    rng = np.random.default_rng(seed)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed)
    real = GradientBoostingClassifier(random_state=seed).fit(X_tr, y_tr)
    real_imp = permutation_importance(real, X_te, y_te, feature_names, n_repeats=3)
    shuffled = GradientBoostingClassifier(random_state=seed).fit(X_tr, rng.permutation(y_tr))
    fake_imp = permutation_importance(shuffled, X_te, y_te, feature_names, n_repeats=3)
    return {"real_max": real_imp[0]["mean_drop"], "shuffled_max": fake_imp[0]["mean_drop"],
            "real_auc": auc(real, X_te, y_te), "shuffled_auc": auc(shuffled, X_te, y_te)}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    d = student()
    X, y, names = d["X"], d["y"], d["feature_names"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0,
                                              stratify=y)

    readable = LogisticRegression(max_iter=2000).fit(X_tr, y_tr)
    blackbox = GradientBoostingClassifier(n_estimators=80, max_depth=2, random_state=0)
    blackbox.fit(X_tr, y_tr)

    print("=" * 84)
    print("Two models, same features: one readable, one not")
    print("=" * 84)
    print(f"  logistic regression : accuracy {accuracy_at_half(readable, X_te, y_te):.3f} "
          f"AUC {auc(readable, X_te, y_te):.3f}")
    print(f"  gradient boosting   : accuracy {accuracy_at_half(blackbox, X_te, y_te):.3f} "
          f"AUC {auc(blackbox, X_te, y_te):.3f}")
    print("  logistic coefficients (the interpretable model):")
    for name, coef in sorted(zip(names, readable.coef_[0]), key=lambda kv: -abs(kv[1])):
        print(f"    {name:20s} {coef:+.3f}")

    print("\n" + "=" * 84)
    print("1. Permutation importance on the black box (AUC drop)")
    print("=" * 84)
    for row in permutation_importance(blackbox, X_te, y_te, names):
        print(f"  {row['feature']:20s} AUC drop {row['mean_drop']:+.4f} "
              f"(sd {row['std']:.4f})")

    print("\n" + "=" * 84)
    print("2. Partial dependence for attendance_rate")
    print("=" * 84)
    j = names.index("attendance_rate")
    grid, values = partial_dependence(blackbox, X_te, j, n_grid=6)
    for g, v in zip(grid, values):
        print(f"  attendance {g:.2f} -> mean predicted pass {v:.3f}")

    # pick an instance near the decision boundary so the counterfactual is meaningful
    probs = probability(blackbox, X_te)
    idx = int(np.argsort(np.abs(probs - 0.5))[0])
    x = X_te[idx]
    print(f"\n  explaining test instance {idx} (probability {probs[idx]:.3f})")

    print("\n" + "=" * 84)
    print("3. Exact Shapley values")
    print("=" * 84)
    shap = shapley_values(blackbox, x, X_tr, names)
    print(f"  prediction {shap['prediction']:.4f}  base {shap['base_value']:.4f}  "
          f"sum(phi) {shap['sum_phi']:+.4f}")
    for f, v in zip(shap["features"], shap["values"]):
        print(f"    {f:20s} {v:+.4f}")
    print(f"  efficiency gap: {shap['efficiency_gap']:.2e} (exact Shapley satisfies "
          f"sum(phi) = f(x) - E[f])")

    print("\n" + "=" * 84)
    print("4. LIME, its fidelity, and its stability")
    print("=" * 84)
    lime = lime_tabular(blackbox, x, X_tr, names)
    for f, v in zip(lime["features"], lime["values"]):
        print(f"    {f:20s} {v:+.3f}")
    print(f"  local R^2 (fidelity to the black box): {lime['local_r2']:.3f}")
    stab = explanation_stability(blackbox, x, X_tr, names)
    print(f"  stability across 5 seeds: mean r {stab['mean_correlation']:.3f} "
          f"(min {stab['min']:.3f}, max {stab['max']:.3f})")
    print("  LIME and Shapley disagree on ranking: different questions, different answers.")
    print("  LIME asks 'what explains this neighbourhood?'; Shapley asks 'what is each")
    print("  feature's fair share of this prediction?'")

    print("\n" + "=" * 84)
    print("5. Counterfactual: what would change this decision?")
    print("=" * 84)
    prob = float(probability(blackbox, x[None, :])[0])
    target = 1 if prob < 0.5 else 0
    cf = counterfactual(blackbox, x, X_tr, names, desired=target)
    print(f"  original probability {prob:.3f}; seeking outcome {target}")
    if cf["found"]:
        for c in cf["changes"]:
            print(f"    change {c['feature']:20s} {c['from']:.2f} -> {c['to']:.2f}")
        print(f"  distance {cf['distance']:.3f} sd, new probability "
              f"{cf['new_probability']:.3f}")
    else:
        print("  no counterfactual found:", cf.get("reason"))
    print("  a counterfactual must be actionable: 'study more' is; 'be born elsewhere' is not.")

    print("\n" + "=" * 84)
    print("6. Sanity check: shuffled labels should destroy importance")
    print("=" * 84)
    chk = sanity_check(X, y, names)
    print(f"  real model      AUC {chk['real_auc']:.3f}  max importance "
          f"{chk['real_max']:+.4f}")
    print(f"  shuffled-label  AUC {chk['shuffled_auc']:.3f}  max importance "
          f"{chk['shuffled_max']:+.4f}")


if __name__ == "__main__":
    main()
