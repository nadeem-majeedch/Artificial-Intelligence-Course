"""rai_data.py -- synthetic datasets with known, documented bias (M13, L13-01).

Every dataset here is generated in-script with a fixed seed and released under
CC0-1.0. None of them describes real people. That matters: the module is about
detecting and measuring harm, and using real recruitment, student or credit
records to teach that would repeat the harm.

Three datasets, three bias mechanisms:

    recruitment()   LABEL BIAS -- historical hiring used a higher bar for group B
    student()       PROXY BIAS -- access to tutoring is group-correlated, and it
                     predicts the label, so a model can use the proxy instead of merit
    loans()         SAMPLING + BASE-RATE BIAS -- group B is under-represented in the
                     training data and has a different base default rate

Run ``python rai_data.py`` for the dataset cards and the raw disparity in labels.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1. Recruitment
# ---------------------------------------------------------------------------

def recruitment(n: int = 4000, seed: int = 0) -> dict:
    """Synthetic hiring screen with label bias against group B.

    Merit is a function of experience and education only. The recorded hiring
    decision used a higher merit threshold for group B, which is exactly what a
    historically biased process produces: the label encodes the past decision,
    not the candidate's ability.
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.45, "B", "A")
    experience = np.clip(rng.gamma(2.0, 1.6, n), 0, 12).round(1)
    education = np.clip(rng.normal(68, 9, n), 40, 100).round(1)
    interview = np.clip(rng.normal(60, 12, n), 20, 100).round(1)
    referral = np.where(group == "A", rng.random(n) < 0.28, rng.random(n) < 0.08)

    merit = 0.55 * (experience / 12) + 0.45 * ((education - 40) / 60)
    merit = np.clip(merit + rng.normal(0, 0.05, n), 0, 1)
    threshold = np.where(group == "A", 0.52, 0.62)          # the bias
    hired = ((merit > threshold) | (referral & (merit > 0.35))).astype(int)

    X = np.column_stack([experience, education, interview, referral.astype(float)])
    names = ["experience_years", "education_score", "interview_score", "referral"]
    return {
        "X": X, "y": hired, "group": group, "feature_names": names,
        "group_names": ["A", "B"],
        "card": {
            "name": "synthetic recruitment screen",
            "n": n, "seed": seed, "licence": "CC0-1.0",
            "features": names,
            "label": "hired (a historical decision, not ground truth about ability)",
            "bias_mechanism": "label bias: merit threshold 0.52 for group A, 0.62 for B",
            "intended_use": "teaching fairness measurement; never a hiring tool",
            "known_limits": [
                "merit is a synthetic construct",
                "no intersectional groups",
                "referral is a privilege proxy, not a qualification",
            ],
        },
    }


# ---------------------------------------------------------------------------
# 2. Student performance
# ---------------------------------------------------------------------------

def student(n: int = 3000, seed: int = 0) -> dict:
    """Synthetic pass/fail prediction with a proxy feature.

    Tutoring access is correlated with group membership and improves the pass
    probability, so a model maximising accuracy will use the proxy. Removing it
    lowers accuracy -- the central fairness-versus-accuracy tension, measured.
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "C", "D")
    prior = np.clip(rng.normal(62, 11, n), 30, 95)
    attendance = np.clip(rng.beta(6, 3, n), 0, 1)
    tutoring = np.where(group == "C", rng.random(n) < 0.65, rng.random(n) < 0.12)
    study_hours = np.clip(rng.normal(11, 4, n) + 2.5 * tutoring, 1, 30).round(1)

    logit = (-1.4 + 0.045 * (prior - 60) + 1.5 * attendance
             + 0.11 * study_hours + 2.20 * tutoring.astype(float))
    p_pass = 1 / (1 + np.exp(-logit))
    passed = (rng.random(n) < p_pass).astype(int)

    X = np.column_stack([prior, attendance, study_hours, tutoring.astype(float)])
    names = ["prior_attainment", "attendance_rate", "study_hours", "tutoring_access"]
    return {
        "X": X, "y": passed, "group": group, "feature_names": names,
        "group_names": ["C", "D"],
        "card": {
            "name": "synthetic student pass prediction",
            "n": n, "seed": seed, "licence": "CC0-1.0",
            "features": names,
            "label": "passed the module",
            "bias_mechanism": "proxy bias: tutoring_access is group-correlated and predictive",
            "intended_use": "teaching proxy discrimination and explainability",
            "known_limits": ["no temporal effects", "two groups only", "synthetic grade scale"],
        },
    }


# ---------------------------------------------------------------------------
# 3. Loans
# ---------------------------------------------------------------------------

def loans(n: int = 5000, seed: int = 0) -> dict:
    """Synthetic credit approval with an unequal base rate and unequal sampling."""
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.7, "A", "B")
    income = np.clip(rng.lognormal(10.4, 0.45, n), 8_000, 200_000).round(0)
    score = np.clip(rng.normal(640, 70, n), 350, 850).round(0)
    employment = np.clip(rng.gamma(3, 2.2, n), 0, 25).round(1)
    amount = np.clip(rng.lognormal(9.4, 0.55, n), 500, 60_000).round(0)

    base = -1.0 + 0.0032 * (score - 640) + 0.000012 * (income - 40_000) \
        + 0.06 * employment - 0.000018 * amount
    base += np.where(group == "B", 0.55, 0.0)      # unequal base rate
    p_default = 1 / (1 + np.exp(-base))
    default = (rng.random(n) < p_default).astype(int)

    X = np.column_stack([income, score, employment, amount])
    names = ["income", "credit_score", "employment_years", "loan_amount"]
    return {
        "X": X, "y": 1 - default, "group": group, "feature_names": names,
        "group_names": ["A", "B"],
        "card": {
            "name": "synthetic loan approval",
            "n": n, "seed": seed, "licence": "CC0-1.0",
            "features": names,
            "label": "approved (1) / not approved (0)",
            "bias_mechanism": "base-rate difference plus 70/30 sampling imbalance",
            "intended_use": "teaching disparity metrics and threshold trade-offs",
            "known_limits": ["income and score are correlated by construction",
                             "no real credit history", "no intersectional analysis"],
        },
    }


def raw_disparity(data: dict) -> dict:
    """Selection rate per group in the labels themselves, before any model."""
    y, g = data["y"], data["group"]
    out = {}
    for name in data["group_names"]:
        mask = g == name
        out[name] = {"n": int(mask.sum()), "positive_rate": float(y[mask].mean())}
    rates = [v["positive_rate"] for v in out.values()]
    out["ratio"] = float(min(rates) / max(rates))
    out["difference"] = float(abs(rates[0] - rates[1]))
    return out


def save_datasets(path: Path | None = None) -> Path:
    """Write the three datasets and their cards as .npz + .json for the labs."""
    path = path or HERE / "data"
    path.mkdir(parents=True, exist_ok=True)
    bundle = {}
    cards = []
    for name, fn in (("recruitment", recruitment), ("student", student), ("loans", loans)):
        d = fn()
        bundle[f"{name}_X"] = d["X"]
        bundle[f"{name}_y"] = d["y"]
        bundle[f"{name}_group"] = d["group"]
        cards.append(d["card"])
    np.savez_compressed(path / "rai_datasets.npz", **bundle)
    (path / "dataset_cards.json").write_text(json.dumps(cards, indent=2), encoding="utf-8")
    return path


def main() -> None:
    print("=" * 78)
    print("Dataset cards and raw label disparity")
    print("=" * 78)
    for name, fn in (("recruitment", recruitment), ("student", student), ("loans", loans)):
        d = fn()
        card = d["card"]
        print(f"\n{name}: {card['n']} rows, {len(card['features'])} features, "
              f"licence {card['licence']}")
        print(f"  label            : {card['label']}")
        print(f"  bias mechanism   : {card['bias_mechanism']}")
        print(f"  positive rate    : {d['y'].mean():.3f}")
        disp = raw_disparity(d)
        for g in d["group_names"]:
            print(f"    group {g}: n={disp[g]['n']:5d} positive rate {disp[g]['positive_rate']:.3f}")
        print(f"  ratio {disp['ratio']:.3f}   difference {disp['difference']:.3f}")
        print("  feature means by group:")
        for j, fname in enumerate(card["features"]):
            a = d["X"][d["group"] == d["group_names"][0], j].mean()
            b = d["X"][d["group"] == d["group_names"][1], j].mean()
            print(f"    {fname:20s} {a:9.3f} vs {b:9.3f}")
    print("\nsaved:", save_datasets())


if __name__ == "__main__":
    main()
