# L06-02 — Data Preparation, Splitting and Leakage

[← Previous: L06-01](L06-01-what-machine-learning-is.md) · [Module home](../README.md) · [Next: L06-03 →](L06-03-linear-regression-from-first-principles.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: A Leakage-Free Pipeline](#4-the-procedure-a-leakage-free-pipeline)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Practical Applications](#7-practical-applications)
- [8. Common Mistakes](#8-common-mistakes)
- [9. Practical Exercises](#9-practical-exercises)
- [10. Self-Assessment](#10-self-assessment)
- [11. Key Terms](#11-key-terms)
- [12. Further Reading](#12-further-reading)
- [What to Do Next](#what-to-do-next)

> **Module M06** · Lesson 2 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-01, P04 (data preparation)

[Previous: L06-01](L06-01-what-machine-learning-is.md) · [Module overview](../README.md) · [Next: L06-03 →](L06-03-linear-regression-from-first-principles.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Profile** a dataset before modelling it: dtypes, missingness, impossible values,
   duplicates, class balance.
2. **Choose** a missing-value strategy and justify it from the mechanism (MCAR, MAR, MNAR).
3. **Handle** outliers deliberately — clip, keep or model — instead of deleting rows by reflex.
4. **Encode** categorical variables and explain when one-hot, ordinal or target encoding is
   appropriate, and where target encoding leaks.
5. **Scale** features, and know which model families do not need it.
6. **Split** data into train/validation/test, stratified or time-ordered as the problem demands.
7. **Detect** the four common leakages — target, preprocessing, temporal, group — and build a
   pipeline whose `fit` touches only training rows.
8. **Run** k-fold cross-validation and report a mean with a spread rather than a single number.

## 2. Prerequisite Knowledge

You need L06-01's vocabulary and enough pandas to select columns and compute summary
statistics. The module's `prep.py` uses NumPy arrays; read it once before running the code.

## 3. Conceptual Explanation

### 3.1 Profiling before touching anything

Four questions, in this order:

1. **What is one row?** A student, a loan application, a transaction, a customer. If you cannot
   say, you cannot split, join or interpret anything.
2. **What is the target, and when is it known?** The answer determines which features are legal.
3. **What is missing, and why?** Missingness has a mechanism, and the mechanism decides the fix.
4. **What is impossible?** Negative ages, 12,000 sqft houses, prices of zero. Impossible values
   are usually data-entry or unit errors, not outliers to be modelled.

`prep.describe_frame` gives the first pass:

```python
import datasets as ds
from prep import describe_frame

print(describe_frame(ds.students()).to_string(index=False))
```

```text
            column  dtype  missing  unique    min    max
       study_hours float64        0     469    0.0  21.26
    attendance_pct float64       21     286   45.6  100.0
       prior_grade float64        0     369   18.4  100.0
       sleep_hours float64       14     329    3.81  10.19
     part_time_job     str        0       2      -      -
parental_education     str        0       3      -      -
  internet_at_home     str        0       2      -      -
       final_score float64        0     552  34.58  84.51
            passed     int64        0       2      0      1
```

### 3.2 Missing values: the mechanism decides the method

| Mechanism | Meaning | Example | Reasonable strategy |
| :--- | :--- | :--- | :--- |
| MCAR | missingness independent of everything | a sensor dropped a packet at random | mean/median imputation, drop rows if few |
| MAR | depends on observed variables | older applicants skip a survey question | model-based imputation using other columns |
| MNAR | depends on the missing value itself | high earners refuse to state income | impute **and** add a "was missing" indicator |

Rules that save you from most mistakes:

- **Impute inside the pipeline, fitted on training data.** The median of the test set is
  information you are not allowed to have at prediction time.
- **Add a missing-indicator column** when the missingness itself is informative. "Income not
  stated" often predicts default better than income does.
- **Never impute the target.** Drop those rows or reframe the problem.
- Constant imputation shrinks variance and biases correlations toward zero; state that in your
  report rather than pretending the filled values are observed.

### 3.3 Outliers: an outlier is not automatically an error

Three responses, in order of preference:

1. **Fix it** if it is impossible (12,000 sqft house in a dataset whose maximum should be
   ~4,000) — correct or drop with a documented reason.
2. **Clip it** (winsorise) at the IQR fence if it is extreme but plausible. Keeps the row, limits
   its leverage.
3. **Keep it and use a model that tolerates it** — trees split on order, so a huge value costs
   little; linear regression and k-NN are sensitive.

The effect is not subtle. On the house data, one impossible area and six luxury prices give:

```text
raw test     : mse 5490.69  rmse 74.10  mae 35.49  r2 0.38
clipped test : mse 1248.74  rmse 35.34  mae 24.18  r2 0.75
clip bounds  : price 155.4 to 540.1 thousand; area 381 to 3207 sqft
rows changed : 7
```

Same model, same split, R² 0.38 → 0.75. Outlier handling was worth more than any
hyperparameter search on this dataset.

### 3.4 Encoding categorical variables

- **One-hot** for unordered categories with few levels. Safe, sparse, no implied order.
- **Ordinal** only when the order is real: "fair < good < excellent". Never for
  "north/east/south/west".
- **Target/mean encoding** replaces a category with its mean target. Powerful for
  high-cardinality features, and a leakage machine unless computed out-of-fold on training data
  only.
- **Hashing / frequency encoding** for very high cardinality. Mentioned, not built here.

### 3.5 Scaling: standardisation, normalisation, and when neither matters

$$
z = \frac{x - \mu}{\sigma}
\qquad\text{(standardisation, unbounded)}
$$

$$
x' = \frac{x - \min}{\max - \min}
\qquad\text{(min–max normalisation, }[0,1]\text{)}
$$

- **Needs scaling:** gradient descent (logistic regression, linear regression by GD, SVMs,
  neural networks), distance-based methods (k-NN, k-means, DBSCAN), PCA.
- **Does not need scaling:** decision trees, random forests, gradient boosting — they split on
  order, which is invariant to monotone transforms.
- **Fit the scaler on training data only.** A scaler fitted on all rows has seen the test set's
  mean and standard deviation. The effect is usually small, which is exactly why it survives
  review.

### 3.6 Feature engineering and selection

Engineering creates informative columns: ratios (`loan / income`), aggregates (spend per month),
calendar features (is the transaction at 3 a.m.?), interactions when you have a reason.
Selection removes columns that add noise: correlation with the target, mutual information,
recursive feature elimination, or L1 regularisation (L06-06).

Feature selection is a **supervised** step. Doing it on all rows before splitting leaks the
target's distribution into your feature set, and on small datasets it can inflate a score by
several points.

### 3.7 Splitting

| Split | Purpose | Typical size |
| :--- | :--- | :--- |
| Train | fit parameters | 60–80% |
| Validation | choose model and hyperparameters, early stopping | 10–20% |
| Test | report once, at the end | 10–20% |

- **Stratify** classification splits so each set keeps the class ratio. With 0.8% positives,
  an unstratified test set can contain no positives at all.
- **Time-ordered splits** for anything with a time dimension. A random split on last year's
  transactions teaches the model the future.
- **Group splits** when rows repeat per entity (multiple visits per patient): keep an entity
  entirely in one split. Otherwise the model memorises the patient, not the disease.

### 3.8 Cross-validation

k-fold CV rotates the validation block:

```text
fold 1: [val][train][train][train][train]
fold 2: [train][val][train][train][train]
...
```

Report the mean **and** the standard deviation. On the loan data, five-fold accuracy is
`0.785 ± 0.019`. Quoting only "78.5%" hides that a different fold gives 75.7%, and it hides
that a competing model at 77.4% is inside the noise.

Stratified k-fold keeps the class ratio in each fold; time-series CV uses expanding or sliding
windows and never shuffles.

### 3.9 The four leakages

| Leakage | What happens | Detection |
| :--- | :--- | :--- |
| **Target** | a feature is derived from the label | accuracy near 1.0; check construction of every column |
| **Preprocessing** | imputer/scaler/selector fitted on all rows | fit only on train; compare scores |
| **Temporal** | random split on time-ordered data | sort by date, split at a cut-off |
| **Group** | the same entity appears in train and test | group-aware split, check ID overlap |

The signature of leakage is a test score too good to be true — treat it as a bug report, not a
result. On the student data, including `final_score` when predicting `passed` gives **1.000**
test accuracy; dropping it gives **0.827**. Nothing about the algorithm changed.

## 4. The Procedure: A Leakage-Free Pipeline

1. Load and profile (`describe_frame`): dtypes, missing, min/max, class balance.
2. Fix impossible values; document every row changed or dropped.
3. Split first — train / validation / test, stratified or time-ordered as appropriate.
4. Build a `Pipeline`: imputer → encoder → scaler → model, **fitted on the training fold**.
5. Impute (median for skewed numeric, mode for categorical) and add indicators if missingness
   is informative.
6. Encode categoricals (one-hot unless order is real).
7. Scale if the model needs it.
8. Select features using training folds only, or skip selection and regularise.
9. Cross-validate on the training set to choose hyperparameters.
10. Fit once on train+validation, evaluate once on test, report the metric with a CI.
11. Write down what you fitted on what, with seeds. LAB-06-04 audits the result.

## 5. Worked Examples

### Example 1 — Impute, scale, encode

```python
import datasets as ds
from prep import StandardScaler, SimpleImputer, OneHotEncoder, train_test_split

frame = ds.students()
cols = ["study_hours", "attendance_pct", "prior_grade", "sleep_hours"]
X, y = frame[cols].to_numpy(), frame["final_score"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.2, seed=0)
print("rows:", len(X_train), len(X_test))

imputer = SimpleImputer("median").fit(X_train)
X_train = imputer.transform(X_train)
print("missing after imputation:", int((X_train != X_train).sum()))

scaler = StandardScaler().fit(X_train)
scaled = scaler.transform(X_train)
print("means:", scaled.mean(axis=0).round(6), "stds:", scaled.std(axis=0).round(3))

onehot = OneHotEncoder().fit(frame[["part_time_job"]].iloc[:480])
print("one-hot columns:", onehot.get_feature_names())
```

```text
rows: 480 120
missing after imputation: 0
means: [ 0. -0. -0.  0.] stds: [1. 1. 1. 1.]
one-hot columns: ['col0_no', 'col0_yes']
```

### Example 2 — Stratification when positives are rare

The transaction dataset is 0.8% fraud — 39 positives in 5,000 rows. An unstratified 20% test
split can easily hold 4 or 5 of them; a stratified one reliably holds about 8. The stratified
version makes the test metric far less noisy, and `stratified_indices` guarantees at least one
positive in each split when the count allows it.

### Example 3 — Reading a CV table

```text
logistic   [0.7933 0.7567 0.8133 0.7833 0.7800]  mean 0.7853  std 0.0185
tree d4    [0.7300 0.7333 0.7733 0.7500 0.7000]  mean 0.7373  std 0.0242
forest 40  [0.7633 0.7667 0.8067 0.7700 0.7633]  mean 0.7740  std 0.0165
```

Logistic regression wins on the mean, but fold 3 gives the forest 0.8067 against logistic's
0.8133 and fold 1 gives the forest 0.7633 against 0.7567 — the ordering flips inside folds. The
honest conclusion is "logistic is about one point better on average, with fold-level noise of
about two points", not "logistic is the best model".

## 6. Mathematical Formulation

**Standardisation** is an affine map per feature: $z_j = (x_j - \mu_j)/\sigma_j$, with $\mu_j$
and $\sigma_j$ estimated on the training set.

**IQR fence:** with $Q_1$ and $Q_3$ the first and third quartiles,
$\text{IQR} = Q_3 - Q_1$, and values outside

$$
[\,Q_1 - k\,\text{IQR},\; Q_3 + k\,\text{IQR}\,], \quad k = 1.5 \text{ (Tukey)}
$$

are flagged. On the house prices this gives $[155.4,\ 540.1]$ thousand and changes 7 rows.

**Cross-validated risk** is the average of held-out risks:

$$
\widehat{R}_{CV} = \frac{1}{k}\sum_{i=1}^{k} \frac{1}{|V_i|}\sum_{(x,y)\in V_i} \ell\big(f^{(-i)}(x), y\big),
$$

where $f^{(-i)}$ is trained without fold $V_i$. The standard deviation across folds is a crude
but useful uncertainty estimate; for a proper interval, bootstrap the metric (L06-05).

## 7. Practical Applications

- **Clinical tabular data** — missingness is MNAR ("not measured because the patient was too
  unwell"), so missing indicators are mandatory and imputation must be discussed with clinicians.
- **Credit applications** — group splits by applicant, time-ordered by application date, and
  target encoding computed out-of-fold.
- **IoT sensor streams** — MCAR gaps from dropped packets; forward-fill is common but biases
  variance, so record the gap length as a feature.
- **Retail demand** — calendar and holiday features matter more than model choice.

## 8. Common Mistakes

1. Scaling or imputing before the split. Small, real, and hard to notice.
2. Dropping every row with a missing value. On the student data that removes 35 rows for two
   columns — often a biased subset.
3. One-hot encoding a 5,000-level ID column. Use frequency or target encoding, or drop it.
4. Random splits on time series.
5. Choosing k in CV and then reporting that same CV score as the test score.
6. Treating a clipped outlier as if it were observed. Clipping changes the target's distribution;
   say so.
7. Deleting rows because a model dislikes them. That is fitting the data to the model.

## 9. Practical Exercises

1. Profile `datasets.loans()`. How many rows have a missing credit score? What strategy and why?
2. Clip `price_thousands` in `datasets.houses()` with $k=1.5$ and $k=3.0$. How many rows change
   in each case, and which would you defend in a report?
3. Build a pipeline that imputes, scales and fits logistic regression on the loan data. Report
   5-fold stratified CV mean and std.
4. Compute target-encoded `neighbourhood` for house prices on the training split only, then again
   on all rows. Compare test R². Explain the difference.
5. Write a one-page leakage audit for a dataset of your choice: target timing, preprocessing,
   temporal order, group structure.

## 10. Self-Assessment

**Multiple choice**

1. Mean imputation of a feature that is 40% missing will most likely
   a) preserve variance. b) shrink variance and bias correlations toward zero.
   c) improve the target distribution. d) create leakage.
2. Which model does **not** require feature scaling?
   a) k-NN. b) logistic regression by gradient descent. c) random forest. d) PCA.
3. You standardise before splitting. The consequence is
   a) a training error. b) optimistic test scores. c) a shape mismatch. d) nothing at all.
4. With 1% positives, an unstratified 20% test split risks
   a) too many positives. b) a test set with no positives. c) leakage. d) duplicate rows.

**Short answer**

5. Give one example each of target, temporal and group leakage.
6. Why is a single cross-validation number not enough to compare two models?

<details>
<summary>Answers</summary>

1. **b**. 2. **c**. 3. **b** — the scaler has seen test statistics. 4. **b**.
5. Target: `final_score` predicting `passed`. Temporal: random split of 2019–2024 sales to predict
   2024 prices. Group: the same patient's visits in both train and test.
6. Fold-to-fold variation is often as large as the difference between models; report mean and
   spread, and prefer a paired comparison on the same folds.

</details>

## 11. Key Terms

**MCAR / MAR / MNAR**, **imputation**, **missing indicator**, **winsorising**, **IQR fence**,
**one-hot encoding**, **ordinal encoding**, **target encoding**, **standardisation**,
**min–max normalisation**, **feature engineering**, **feature selection**, **stratified split**,
**group split**, **time-ordered split**, **k-fold cross-validation**, **leakage**, **pipeline**.

## 12. Further Reading

- Van den Broeck, J. et al. (2005). *Data Cleaning: Detecting, Diagnosing and Editing Data
  Abnormalities*. PLoS Medicine. — Practical, clinical, honest about missingness.
- Kaufman, S. et al. (2012). *Leakage in Data Mining: Formulation, Detection and Avoidance*.
  — The paper that named the problem.
- scikit-learn user guide, *Preprocessing* and *Cross-validation*. — The API this module's
  classes imitate.

## What to Do Next

1. Run `python prep.py`.
2. Do exercises 1–4 and keep the numbers for LAB-06-04.
3. Continue to [L06-03 — Linear Regression from First Principles](L06-03-linear-regression-from-first-principles.md).

---

**Navigation:** [← Previous: L06-01](L06-01-what-machine-learning-is.md) · [Module home](../README.md) · [Next: L06-03 →](L06-03-linear-regression-from-first-principles.md)
