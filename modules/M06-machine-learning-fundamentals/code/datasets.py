"""Deterministic synthetic datasets for M06.

Every generator is seeded and returns a pandas DataFrame with exactly the columns
documented in DATASETS. The module exists so the module's lessons, notebooks and labs
run offline, on any machine, with no downloads and no licence questions.

Each dataset mirrors the schema of a real public dataset named in DATASETS, so a
student can swap in the real file (see the labs) without rewriting the code. The
synthetic rows are *not* the real data and must never be reported as such.

Run `python datasets.py` for a summary table.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "students",
    "houses",
    "emails",
    "customers",
    "loans",
    "intrusion",
    "attrition",
    "transactions",
    "DATASETS",
    "summary",
]


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def _clip01(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 1.0)


def _calibrated_intercept(logit: np.ndarray, u: np.ndarray, target_rate: float) -> float:
    """Bisect the intercept so that mean(u < sigmoid(logit + b)) hits target_rate.

    Used to keep class imbalance realistic and documented rather than accidental.
    """
    lo, hi = -40.0, 40.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        rate = float(np.mean(u < 1.0 / (1.0 + np.exp(-(logit + mid)))))
        if rate < target_rate:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# 1. Student academic performance (regression + classification)
# ---------------------------------------------------------------------------
def students(n: int = 600, seed: int = 0) -> pd.DataFrame:
    """Predict a final score (0-100) from study habits and background.

    Mirrors UCI Student Performance (Cortez & Silva, 2008): grades, study time,
    absences and family background. Missing values are injected into two columns so
    the imputation lesson has something to impute.
    """
    rng = _rng(seed)
    study_hours = np.clip(rng.normal(9.0, 4.0, n), 0.0, 30.0)
    attendance = np.clip(rng.normal(84.0, 12.0, n), 40.0, 100.0)
    prior_grade = np.clip(rng.normal(62.0, 14.0, n), 0.0, 100.0)
    sleep_hours = np.clip(rng.normal(7.0, 1.2, n), 3.0, 11.0)
    part_time = rng.random(n) < 0.28
    parental = rng.choice(["none", "school", "university"], n, p=[0.18, 0.47, 0.35])
    internet = rng.choice(["yes", "no"], n, p=[0.86, 0.14])

    parental_bonus = pd.Series(parental).map(
        {"none": -2.0, "school": 0.0, "university": 2.5}
    ).to_numpy()

    score = (
        13.0
        + 1.25 * study_hours
        + 0.15 * attendance
        + 0.26 * prior_grade
        + 0.85 * sleep_hours
        - 3.0 * part_time
        + parental_bonus
        + 1.8 * (internet == "yes")
        + rng.normal(0.0, 5.5, n)
    )
    score = np.clip(score, 0.0, 100.0)

    df = pd.DataFrame(
        {
            "study_hours": study_hours.round(2),
            "attendance_pct": attendance.round(1),
            "prior_grade": prior_grade.round(1),
            "sleep_hours": sleep_hours.round(2),
            "part_time_job": np.where(part_time, "yes", "no"),
            "parental_education": parental,
            "internet_at_home": internet,
            "final_score": score.round(2),
        }
    )
    df["passed"] = (df["final_score"] >= 55).astype(int)

    # Missing at random, roughly 4% and 2%.
    df.loc[rng.random(n) < 0.04, "attendance_pct"] = np.nan
    df.loc[rng.random(n) < 0.02, "sleep_hours"] = np.nan
    return df


# ---------------------------------------------------------------------------
# 2. House prices (regression)
# ---------------------------------------------------------------------------
def houses(n: int = 800, seed: int = 0) -> pd.DataFrame:
    """Predict sale price in thousands from size, age, location and condition.

    Mirrors the Ames Housing schema (De Cock, 2011) in miniature. A few extreme
    prices and one implausible living area are included so outlier handling has a
    target.
    """
    rng = _rng(seed)
    living_area = np.clip(rng.normal(1800, 520, n), 600, 4200)
    bedrooms = np.clip(np.round(rng.normal(3.2, 0.9, n)), 1, 6).astype(int)
    bathrooms = np.clip(np.round(rng.normal(2.1, 0.7, n) * 2) / 2, 1, 4)
    age = np.clip(rng.gamma(3.0, 12.0, n), 0, 120)
    distance_km = np.clip(rng.gamma(2.2, 3.1, n), 0.2, 40)
    garage = (rng.random(n) < 0.68).astype(int)
    neighbourhood = rng.choice(["north", "east", "south", "west"], n, p=[0.3, 0.25, 0.2, 0.25])
    condition = rng.choice(["fair", "good", "excellent"], n, p=[0.2, 0.6, 0.2])

    nb_bonus = pd.Series(neighbourhood).map(
        {"north": 32.0, "east": 8.0, "south": -12.0, "west": 3.0}
    ).to_numpy()
    cond_bonus = pd.Series(condition).map({"fair": -14.0, "good": 0.0, "excellent": 21.0}).to_numpy()

    price = (
        62.0
        + 0.118 * living_area
        + 13.0 * bedrooms
        + 17.0 * bathrooms
        - 0.42 * age
        - 1.35 * distance_km
        + 11.0 * garage
        + nb_bonus
        + cond_bonus
        + rng.normal(0.0, 22.0, n)
    )
    price = np.clip(price, 45.0, None)

    df = pd.DataFrame(
        {
            "living_area_sqft": living_area.round(0),
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "age_years": age.round(1),
            "distance_to_centre_km": distance_km.round(2),
            "garage": garage,
            "neighbourhood": neighbourhood,
            "condition": condition,
            "price_thousands": price.round(1),
        }
    )

    # Two planted problems: an impossible area and a handful of luxury outliers.
    df.loc[7, "living_area_sqft"] = 12000.0
    luxury = rng.choice(n, 6, replace=False)
    df.loc[luxury, "price_thousands"] = (df.loc[luxury, "price_thousands"] * 3.1).round(1)
    return df


# ---------------------------------------------------------------------------
# 3. Email spam (binary classification, imbalanced)
# ---------------------------------------------------------------------------
def emails(n: int = 1200, seed: int = 0) -> pd.DataFrame:
    """Classify an email as spam (1) or ham (0).

    Mirrors the UCI SMS Spam Collection (Almeida et al., 2011) in spirit: short text
    reduced to a handful of numeric and count features, with a realistic 17% spam
    rate. The features are the kind you would extract with a bag-of-words model.
    """
    rng = _rng(seed)
    spam = rng.random(n) < 0.17
    word_count = np.where(spam, rng.gamma(6.0, 22.0, n), rng.gamma(5.0, 18.0, n)).round(0)
    num_links = np.where(spam, rng.poisson(1.6, n), rng.poisson(0.25, n))
    uppercase_words = np.where(spam, rng.poisson(3.4, n), rng.poisson(0.4, n))
    exclamations = np.where(spam, rng.poisson(1.9, n), rng.poisson(0.3, n))
    has_attachment = np.where(spam, rng.random(n) < 0.22, rng.random(n) < 0.41).astype(int)
    sender_known = np.where(spam, rng.random(n) < 0.18, rng.random(n) < 0.83).astype(int)
    hour_sent = rng.integers(0, 24, n)
    contains_free = np.where(spam, rng.random(n) < 0.46, rng.random(n) < 0.07).astype(int)

    df = pd.DataFrame(
        {
            "word_count": word_count.astype(int),
            "num_links": num_links,
            "uppercase_words": uppercase_words,
            "exclamation_marks": exclamations,
            "has_attachment": has_attachment,
            "sender_known": sender_known,
            "hour_sent": hour_sent,
            "contains_free": contains_free,
            "is_spam": spam.astype(int),
        }
    )
    return df


# ---------------------------------------------------------------------------
# 4. Customer segmentation (clustering)
# ---------------------------------------------------------------------------
def customers(n: int = 500, seed: int = 0) -> pd.DataFrame:
    """Segment customers by value and engagement, with four planted groups.

    Mirrors the RFM features of UCI Online Retail II (Chen, 2012): recency,
    frequency, monetary value, plus tenure and a survey-style spending score.
    """
    rng = _rng(seed)
    # Four latent segments, deliberately unequal in size.
    sizes = [170, 140, 110, 80]
    centres = [
        # income, spending, recency, frequency, monetary, tenure
        (88.0, 82.0, 12.0, 22.0, 4200.0, 62.0),   # premium loyalists
        (66.0, 58.0, 30.0, 12.0, 2100.0, 40.0),   # steady regulars
        (34.0, 24.0, 95.0, 3.0, 420.0, 14.0),     # lapsing low-value
        (55.0, 12.0, 55.0, 6.0, 900.0, 26.0),     # high income, low spend
    ]
    rows = []
    for size, c in zip(sizes, centres):
        income = np.clip(rng.normal(c[0], 8.0, size), 12, 120)
        spending = np.clip(rng.normal(c[1], 9.0, size), 1, 100)
        recency = np.clip(rng.normal(c[2], 9.0, size), 1, 200)
        frequency = np.clip(rng.normal(c[3], 3.0, size), 1, 60)
        monetary = np.clip(rng.normal(c[4], 380.0, size), 40, 9000)
        tenure = np.clip(rng.normal(c[5], 10.0, size), 1, 96)
        rows.append(
            np.column_stack([income, spending, recency, frequency, monetary, tenure])
        )
    data = np.vstack(rows)
    rng.shuffle(data)
    df = pd.DataFrame(
        data,
        columns=[
            "annual_income_k",
            "spending_score",
            "recency_days",
            "purchase_frequency",
            "monetary_value",
            "tenure_months",
        ],
    )
    df["annual_income_k"] = df["annual_income_k"].round(1)
    df["spending_score"] = df["spending_score"].round(0)
    df["recency_days"] = df["recency_days"].round(0)
    df["purchase_frequency"] = df["purchase_frequency"].round(0)
    df["monetary_value"] = df["monetary_value"].round(0)
    df["tenure_months"] = df["tenure_months"].round(0)
    return df


# ---------------------------------------------------------------------------
# 5. Loan approval (binary classification, imbalanced)
# ---------------------------------------------------------------------------
def loans(n: int = 1500, seed: int = 0) -> pd.DataFrame:
    """Predict whether a loan application is approved.

    Mirrors UCI Statlog German Credit (Hofmann, 1994): income, amount, credit
    history, employment and purpose. About 30% of applications are approved, so
    accuracy is a trap.
    """
    rng = _rng(seed)
    income_k = np.clip(rng.lognormal(3.35, 0.45, n), 8, 120)
    loan_amount_k = np.clip(rng.lognormal(2.7, 0.55, n), 1, 90)
    credit_score = np.clip(rng.normal(640, 75, n), 350, 850)
    employment_years = np.clip(rng.gamma(2.5, 2.6, n), 0, 40)
    debt_ratio = np.clip(rng.beta(2.2, 3.4, n), 0.01, 0.95)
    default_history = (rng.random(n) < 0.13).astype(int)
    purpose = rng.choice(
        ["car", "business", "education", "home", "other"], n, p=[0.28, 0.18, 0.17, 0.24, 0.13]
    )

    logit = (
        0.052 * income_k
        - 0.061 * loan_amount_k
        + 0.0105 * credit_score
        + 0.052 * employment_years
        - 2.55 * debt_ratio
        - 1.65 * default_history
        + pd.Series(purpose).map(
            {"car": 0.15, "business": -0.35, "education": 0.3, "home": 0.55, "other": -0.5}
        ).to_numpy()
    )
    u = rng.random(n)
    intercept = _calibrated_intercept(logit, u, 0.30)
    approved = (u < 1.0 / (1.0 + np.exp(-(logit + intercept)))).astype(int)

    df = pd.DataFrame(
        {
            "annual_income_k": income_k.round(1),
            "loan_amount_k": loan_amount_k.round(1),
            "credit_score": credit_score.round(0),
            "employment_years": employment_years.round(1),
            "debt_ratio": debt_ratio.round(3),
            "default_history": default_history,
            "purpose": purpose,
            "approved": approved,
        }
    )
    df.loc[rng.random(n) < 0.03, "credit_score"] = np.nan
    return df


# ---------------------------------------------------------------------------
# 6. Network intrusion (binary classification, imbalanced)
# ---------------------------------------------------------------------------
def intrusion(n: int = 3000, seed: int = 0) -> pd.DataFrame:
    """Flag a connection record as an attack (1) or normal traffic (0).

    Feature names follow NSL-KDD (Tavallaee et al., 2009): duration, byte counts,
    error rates, failed logins and protocol. Roughly one record in five is an
    attack, spread over three attack families so error analysis has structure.
    """
    rng = _rng(seed)
    attack = rng.choice([0, 1, 2, 3], n, p=[0.79, 0.09, 0.08, 0.04])  # 0 = normal
    is_attack = (attack > 0).astype(int)
    kind = np.where(attack == 0, "normal", np.where(attack == 1, "probing", np.where(attack == 2, "dos", "r2l")))

    base_duration = np.where(is_attack == 1, rng.gamma(1.4, 4.0, n), rng.gamma(2.2, 9.0, n))
    src_bytes = np.where(is_attack == 1, rng.lognormal(6.2, 2.0, n), rng.lognormal(7.0, 1.6, n))
    dst_bytes = np.where(is_attack == 1, rng.lognormal(5.0, 2.2, n), rng.lognormal(8.0, 1.4, n))
    count = rng.integers(1, 512, n)
    srv_count = np.clip(count + rng.integers(-20, 21, n), 1, 512)
    serror_rate = np.where(is_attack == 1, rng.beta(2.4, 3.0, n), rng.beta(1.3, 14.0, n))
    num_failed_logins = np.where(is_attack == 1, rng.poisson(1.1, n), rng.poisson(0.06, n))
    logged_in = np.where(is_attack == 1, rng.random(n) < 0.42, rng.random(n) < 0.83).astype(int)
    protocol = rng.choice(["tcp", "udp", "icmp"], n, p=[0.72, 0.19, 0.09])

    df = pd.DataFrame(
        {
            "duration": base_duration.round(2),
            "src_bytes": src_bytes.round(0),
            "dst_bytes": dst_bytes.round(0),
            "count": count,
            "srv_count": srv_count,
            "serror_rate": serror_rate.round(3),
            "num_failed_logins": num_failed_logins,
            "logged_in": logged_in,
            "protocol_type": protocol,
            "attack_family": kind,
            "is_attack": is_attack,
        }
    )
    return df


# ---------------------------------------------------------------------------
# 7. Employee attrition (binary classification, imbalanced)
# ---------------------------------------------------------------------------
def attrition(n: int = 1400, seed: int = 0) -> pd.DataFrame:
    """Predict whether an employee leaves within the year.

    Mirrors the IBM HR Analytics Attrition sample: age, income, tenure, overtime,
    satisfaction and distance from home. About 16% leave.
    """
    rng = _rng(seed)
    age = np.clip(rng.normal(36, 8.5, n), 18, 60).round(0)
    monthly_income = np.clip(rng.lognormal(3.5, 0.32, n), 1.2, 20.0)
    years_at_company = np.clip(rng.gamma(2.0, 3.2, n), 0, 30)
    job_satisfaction = rng.integers(1, 5, n)
    overtime = (rng.random(n) < 0.29).astype(int)
    distance_from_home = np.clip(rng.gamma(2.0, 5.5, n), 1, 60)
    num_companies = np.clip(rng.poisson(2.6, n), 0, 9)
    environment_satisfaction = rng.integers(1, 5, n)
    job_level = rng.choice([1, 2, 3, 4, 5], n, p=[0.36, 0.31, 0.18, 0.10, 0.05])

    logit = (
        -0.028 * age
        + 0.28 * monthly_income
        - 0.062 * years_at_company
        - 0.52 * job_satisfaction
        + 1.18 * overtime
        + 0.032 * distance_from_home
        + 0.19 * num_companies
        - 0.34 * environment_satisfaction
        - 0.42 * job_level
    )
    u = rng.random(n)
    intercept = _calibrated_intercept(logit, u, 0.16)
    left = (u < 1.0 / (1.0 + np.exp(-(logit + intercept)))).astype(int)

    df = pd.DataFrame(
        {
            "age": age.astype(int),
            "monthly_income_k": monthly_income.round(1),
            "years_at_company": years_at_company.round(1),
            "job_satisfaction": job_satisfaction,
            "overtime": overtime,
            "distance_from_home_km": distance_from_home.round(1),
            "num_companies_worked": num_companies,
            "environment_satisfaction": environment_satisfaction,
            "job_level": job_level,
            "attrition": left,
        }
    )
    return df


# ---------------------------------------------------------------------------
# 8. Credit-card transactions (anomaly detection)
# ---------------------------------------------------------------------------
def transactions(n: int = 5000, seed: int = 0) -> pd.DataFrame:
    """Flag fraudulent card transactions; fraud is about 0.8% of rows.

    Mirrors the ULB Credit Card Fraud dataset (Dal Pozzolo et al., 2015) in shape:
    amount, time, distance, and a few anonymised-looking behavioural features.
    The fraud rate is deliberately realistic, so a "predict everything normal"
    baseline scores over 99% accuracy and is useless.
    """
    rng = _rng(seed)
    fraud = rng.random(n) < 0.008
    amount = np.where(fraud, rng.lognormal(3.6, 1.2, n), rng.lognormal(3.2, 1.0, n))
    hour = rng.integers(0, 24, n)
    distance_from_home = np.where(fraud, rng.lognormal(4.1, 1.1, n), rng.lognormal(2.3, 1.0, n))
    ratio_to_median = np.where(fraud, rng.lognormal(2.6, 0.9, n), rng.lognormal(0.35, 0.6, n))
    foreign = np.where(fraud, rng.random(n) < 0.62, rng.random(n) < 0.08).astype(int)
    merchant = rng.choice(
        ["grocery", "fuel", "online", "restaurant", "travel", "electronics"],
        n,
        p=[0.3, 0.18, 0.24, 0.15, 0.06, 0.07],
    )
    attempts_last_hour = np.where(fraud, rng.poisson(3.1, n), rng.poisson(1.05, n))

    df = pd.DataFrame(
        {
            "amount": amount.round(2),
            "hour": hour,
            "distance_from_home_km": distance_from_home.round(1),
            "ratio_to_median_spend": ratio_to_median.round(2),
            "foreign_transaction": foreign,
            "merchant_category": merchant,
            "attempts_last_hour": attempts_last_hour,
            "is_fraud": fraud.astype(int),
        }
    )
    return df


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
DATASETS = {
    "students": {
        "title": "Student academic performance",
        "task": "regression (final_score) and binary classification (passed)",
        "target": "final_score / passed",
        "target_col": "passed",
        "classification": True,
        "real_counterpart": "UCI Student Performance (Cortez & Silva, 2008), CC BY 4.0",
        "notes": "12% missing attendance, 2% missing sleep; 600 rows.",
    },
    "houses": {
        "title": "House price prediction",
        "task": "regression",
        "target": "price_thousands",
        "target_col": "price_thousands",
        "classification": False,
        "real_counterpart": "Ames Housing (De Cock, 2011), distributed via Kaggle",
        "notes": "One impossible area (12,000 sqft) and six luxury outliers.",
    },
    "emails": {
        "title": "Email spam detection",
        "task": "binary classification, imbalanced",
        "target": "is_spam",
        "target_col": "is_spam",
        "classification": True,
        "real_counterpart": "UCI SMS Spam Collection (Almeida et al., 2011), CC BY 4.0",
        "notes": "17% positive class; 1,200 rows.",
    },
    "customers": {
        "title": "Customer segmentation",
        "task": "clustering",
        "target": "none (four latent segments)",
        "target_col": None,
        "classification": False,
        "real_counterpart": "UCI Online Retail II (Chen, 2012), CC BY 4.0",
        "notes": "500 rows, four unequal segments.",
    },
    "loans": {
        "title": "Bank loan approval",
        "task": "binary classification, imbalanced",
        "target": "approved",
        "target_col": "approved",
        "classification": True,
        "real_counterpart": "UCI Statlog German Credit (Hofmann, 1994), CC BY 4.0",
        "notes": "About 30% approved; 3% missing credit score.",
    },
    "intrusion": {
        "title": "Network intrusion detection",
        "task": "binary classification, imbalanced",
        "target": "is_attack",
        "target_col": "is_attack",
        "classification": True,
        "real_counterpart": "NSL-KDD (Tavallaee et al., 2009), research use",
        "notes": "21% attacks across three families; 3,000 rows.",
    },
    "attrition": {
        "title": "Employee attrition",
        "task": "binary classification, imbalanced",
        "target": "attrition",
        "target_col": "attrition",
        "classification": True,
        "real_counterpart": "IBM HR Analytics Attrition sample (IBM, via Kaggle)",
        "notes": "About 16% attrition; 1,400 rows.",
    },
    "transactions": {
        "title": "Credit-card fraud detection",
        "task": "anomaly detection / binary classification",
        "target": "is_fraud",
        "target_col": "is_fraud",
        "classification": True,
        "real_counterpart": "ULB Credit Card Fraud Detection (Dal Pozzolo et al., 2015), DbCL/ODbL",
        "notes": "0.8% fraud; 5,000 rows.",
    },
}


def summary() -> pd.DataFrame:
    rows = []
    for name, meta in DATASETS.items():
        df = globals()[name]()
        col = meta["target_col"]
        rows.append(
            {
                "dataset": name,
                "rows": len(df),
                "columns": df.shape[1],
                "task": meta["task"].split(",")[0],
                "target": meta["target"],
                "positive_rate": (
                    round(float(df[col].mean()), 3)
                    if col and meta["classification"]
                    else "-"
                ),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(summary().to_string(index=False))
    print()
    for name in DATASETS:
        frame = globals()[name]()
        print(f"{name:12s} {frame.shape[0]:5d} rows x {frame.shape[1]:2d} cols  "
              f"missing={int(frame.isna().sum().sum())}")
