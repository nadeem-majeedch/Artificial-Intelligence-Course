# LP04-02 — Missing Values and Duplicates

| Unit | P04 · Data Preparation and Visualisation |
| :--- | :--- |
| Level | 100 |
| Study time | 90 minutes |
| Prerequisites | [LP04-01](LP04-01-dataset-structures-csv-and-json.md) |
| Notebook | [NB-P04-01](../notebooks/nb-p04-01-data-preparation.ipynb) |
| Lab | [LAB-P04-01](../labs/lab-p04-01-messy-survey-cleanup.md) |

[← Previous: Dataset Structures](LP04-01-dataset-structures-csv-and-json.md) · [P04 home](../README.md) · [Next: Outliers and Scaling →](LP04-03-outliers-normalization-and-standardization.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Quantify** missingness per column and per row, and decide between dropping and imputing.
- **Distinguish** MCAR, MAR and MNAR, and explain why the distinction changes what you can conclude.
- **Impute** with mean, median or mode — and add an indicator column when missingness itself is
  informative.
- **Detect** exact and near-duplicate records, and remove them without destroying legitimate repeats.

## 2. Prerequisite Knowledge

- Loading and inspecting tables: [LP04-01](LP04-01-dataset-structures-csv-and-json.md).
- Mean, median and mode: [LP03-01](../../P03-probability-and-statistics/lessons/LP03-01-descriptive-statistics.md).

## 3. Conceptual Explanation

### 3.1 Three mechanisms of missingness

| Mechanism | Meaning | Example | Consequence |
| :--- | :--- | :--- | :--- |
| **MCAR** | Missing completely at random | A sensor's packet was dropped | Dropping rows is unbiased, just wasteful |
| **MAR** | Missing depends on observed variables | Older respondents skip the income question | Imputation using other columns is defensible |
| **MNAR** | Missing depends on the missing value itself | High earners refuse to state income | Any imputation biases the result; say so |

You cannot test MNAR from the data alone — it requires knowing the collection process. The honest move
is to state which mechanism you assume and what would change if it were wrong.

### 3.2 The decision, in order

1. **How much is missing?** A column that is 80% empty is usually dropped; a handful of gaps in a key
   column can be dropped as rows.
2. **Is the missingness informative?** If the fact of absence predicts the target, keep it as a feature:
   `df["income_missing"] = df["income"].isna()`. In credit scoring this flag is often more predictive
   than the imputed value.
3. **What is the cost of a wrong value?** Mean imputation shrinks variance and weakens correlations;
   it is a convenience, not a repair.
4. **Where does the statistic come from?** The imputation value must be computed on the **training**
   data only, then applied to test data. Computing it on everything leaks information and inflates
   measured performance.

### 3.3 Imputation choices, ranked by honesty

- **Drop the row** — unbiased under MCAR, and transparent.
- **Median** — robust to skew; the safe default for numeric columns.
- **Mean** — fine for symmetric data, distorted by outliers.
- **Mode** — the only option for categorical columns.
- **Model-based** (regression, k-NN) — better under MAR, but more machinery and more ways to leak.
- **Forward fill** — correct for time series where the last known value persists; wrong for independent
  observations.

Never impute the target column. A model trained on invented outcomes learns the invention.

### 3.4 Duplicates come in two kinds

- **Exact duplicates** — every column identical. Usually a double write; remove with
  `drop_duplicates()`.
- **Near duplicates** — the same entity recorded twice with a typo, trailing space, or different case
  (`"Ali "` vs `"ali"`). Removing these requires deciding on a **key** and normalising it first.

A duplicate is only a duplicate relative to a key. Two transactions of the same amount on the same day
may be two genuine purchases. Decide what identifies a record before deleting anything.

## 4. Worked Examples

### Example 1 — quantify, then decide

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "student": ["Ali", "Sara", "Bilal", "Hina", "Zara"],
    "score": [78, np.nan, 64, 85, np.nan],
    "city": ["Lahore", "Karachi", None, "Lahore", "Karachi"],
})
print(df.isna().sum().to_dict())
print(df.isna().sum(axis=1).tolist())
```

```text
{'student': 0, 'score': 2, 'city': 1}
[0, 1, 1, 0, 1]
```

Two of five scores missing (40%) is too many to drop without losing most of the table, and the gaps are
scattered, so per-column imputation is the reasonable route. Per-row counts show no row is entirely
empty.

### Example 2 — median imputation with an indicator

```python
df["score_missing"] = df["score"].isna()
df["score"] = df["score"].fillna(df["score"].median())
print(df["score"].tolist())
print(round(df["score"].mean(), 2))
```

```text
[78.0, 78.0, 64.0, 85.0, 78.0]
76.6
```

The median of the three observed scores $(64, 78, 85)$ is 78, which fills both gaps. The observed mean
was 75.67 and the imputed mean is 76.6 — the two invented values sit exactly at 78, so they add no
spread, which is the variance shrink described in §3.2. The `score_missing` column preserves the fact
that two values were invented, so a model can learn from it.

### Example 3 — exact and near duplicates

```python
raw = pd.DataFrame({
    "name": ["Ali", "Sara", "Ali", "ali ", "Sara"],
    "score": [78, 91, 78, 78, 88],
})
print("exact rows:", raw.duplicated().sum())

clean = raw.assign(name=raw["name"].str.strip().str.lower())
print("rows sharing a key:", clean.duplicated(subset=["name"]).sum())
print(clean.loc[clean.duplicated(subset=["name"], keep=False)].to_string(index=False))
print(clean.drop_duplicates(subset=["name", "score"]).to_string(index=False))
```

```text
exact rows: 1
rows sharing a key: 3
name  score
 ali     78
sara     91
 ali     78
 ali     78
sara     88
name  score
 ali     78
sara     91
sara     88
```

Row 2 duplicates row 0 exactly, hence one exact duplicate. After trimming and lowercasing, three rows
share a name key — and the middle block shows why deletion needs judgement: the three `ali` rows carry
the **same** score, so they are genuine duplicates, but the two `sara` rows carry **different** scores
(91 and 88). Those are a conflict that needs a rule, not a deletion.

Deduplicating on `["name", "score"]` therefore removes only the two redundant `ali` rows and leaves
both Sara measurements for review. The habit: choose and normalise a key, inspect every row that shares
it, and only then decide what to drop.

## 5. Visual Explanation

```text
  missingness by column            decision
  student  ██████████ 0%           keep
  score    ██████     40%          impute + indicator
  city     ████████   20%          mode, or drop rows
  notes    ██         80%          drop the column
```

*Text description of the diagram:* a bar per column showing the fraction of missing cells. The bands on
the right are the usual thresholds: below about 5% dropping rows is harmless, 20–50% needs imputation
with an indicator, and above roughly 80% the column rarely earns its keep. These are conventions, not
laws — the mechanism matters more than the percentage.

## 6. Mathematical Formulation

Mean imputation replaces missing $x_i$ with $\bar{x}_{\text{obs}}$ and, in doing so, reduces the sample
variance:

$$
s^2_{\text{imputed}} = \frac{(n_{\text{obs}} - 1)s^2_{\text{obs}}}{n - 1}
< s^2_{\text{obs}}
$$

because the imputed values sit exactly at the mean and contribute zero deviation. The variance is
under-estimated by a factor of roughly $(n_{\text{obs}}-1)/(n-1)$. Similarly, correlation with other
variables is attenuated toward zero, since the imputed column carries no genuine covariation.

Under MAR, multiple imputation addresses this by drawing $m$ plausible values from a predictive
distribution and pooling the results — the standard remedy when the analysis must be defensible rather
than merely convenient.

## 7. Python Implementation

```python
"""A small, explicit cleaning function with a report of what changed."""
import numpy as np
import pandas as pd

raw = pd.DataFrame({
    "id": [1, 2, 3, 4, 4, 5],
    "score": [78.0, np.nan, 64.0, 85.0, 85.0, 90.0],
    "city": ["Lahore", "karachi", "Lahore", "Lahore", "Lahore", None],
})


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    report = {}
    df = df.drop_duplicates(subset=["id"]).copy()
    report["duplicate ids removed"] = raw.shape[0] - df.shape[0]

    df["city"] = df["city"].str.strip().str.title()
    df["city"] = df["city"].fillna(df["city"].mode().iloc[0])

    df["score_missing"] = df["score"].isna()
    report["scores imputed"] = int(df["score_missing"].sum())
    df["score"] = df["score"].fillna(df["score"].median())

    report["remaining missing"] = int(df.isna().sum().sum())
    return df, report


cleaned, report = clean(raw)
print(cleaned.to_string(index=False))
print(report)
```

**Output**

```text
 id  score    city  score_missing
  1   78.0  Lahore          False
  2   81.5 Karachi           True
  3   64.0  Lahore          False
  4   85.0  Lahore          False
  5   90.0  Lahore          False
{'duplicate ids removed': 1, 'scores imputed': 1, 'remaining missing': 0}
```

The report dictionary is the part most pipelines omit and every reviewer asks for: what was removed,
what was invented, and what is still unknown. Returning it alongside the frame makes the cleaning
auditable — the same discipline M13's evaluation work will demand.

## 8. Practical Applications

- **Surveys and clinical data.** Missingness is the norm; documenting the mechanism is often more
  important than the imputation method.
- **Joins and merges.** A left join that produces `NaN`s is telling you the key did not match — inspect
  those rows before imputing them away.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Imputing before splitting train/test | Test performance too good | Statistic saw the test data | Fit on train, transform test |
| Imputing the target | Model predicts the imputation | Invented outcomes | Drop target-missing rows |
| Dropping duplicates on all columns | Near duplicates remain | Key not normalised | Trim, lowercase, then compare |
| Treating `""` as missing automatically | Empty strings counted as data | Not `NaN` | `df.replace("", np.nan)` |

## 10. Self-Assessment

**1.** A column is 60% missing. What are the three options, and which do you choose first?
<details><summary>Show answer</summary>

Drop the column, drop the affected rows, or impute with an indicator. First check whether missingness
predicts the target — if it does, keep the column with an indicator; if not, and the column is
peripheral, dropping it is simplest and most honest.
</details>

**2.** Why is mean imputation worse for a skewed column?
<details><summary>Show answer</summary>

Because the mean is itself pulled by the tail, so imputed values are placed in a region where few real
observations lie, and the column's spread is understated. The median places them where data actually
cluster.
</details>

**3.** Two rows share an `id` but differ in `score`. Are they duplicates?
<details><summary>Show answer</summary>

They are a **conflict**: the same key with different measurements. Deleting one silently discards data.
Decide a rule — keep the latest by timestamp, keep the maximum, or flag for review — and record it.
</details>

**4.** You impute `income` with the median of the whole dataset, then split into train and test. What is
wrong?
<details><summary>Show answer</summary>

The median was computed using test values, so information from the test set leaked into training. The
median must come from the training split only, then be applied to both.
</details>

## 11. Further Reading

- [pandas: Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) — `isna`, `fillna`, `dropna` and their options.
- [pandas: Duplicated values](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html) — subset and keep semantics.

## Mini-Lab

Build a 30-row dataset with `np.random.default_rng(seed=4)` containing `id`, `score` (10% missing) and
`city` (three spellings of two cities, some with trailing spaces, 5% missing). Write `clean(df)` that
normalises city spellings, imputes missing city by mode, imputes score by median with an indicator,
and removes duplicate ids. Return the frame plus a report dictionary, and assert that no `NaN` remains.

## What to Do Next

Continue to [LP04-03 Outliers, Normalisation and Standardisation](LP04-03-outliers-normalization-and-standardization.md).
