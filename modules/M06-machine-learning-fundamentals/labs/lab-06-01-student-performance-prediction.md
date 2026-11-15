# LAB-06-01 — Tabular Prediction End-to-End: Student Performance and House Prices

> **Module M06** · Lab 1 of 4 · ~150 minutes · Level 300
> **Scenarios:** 1 (student academic performance) and 2 (house price prediction)
> **Prerequisites:** L06-01 to L06-06 · **Pairs with:** NB-06-01

[Module overview](../README.md) · [Lesson 1](../lessons/L06-01-what-machine-learning-is.md) · [Next lab: LAB-06-02 →](lab-06-02-model-comparison-spam-and-loans.md)

Two regression problems, one workflow. The first is a small, clean, four-feature dataset where
you can check every number by hand. The second has an impossible value and six planted outliers,
so the preparation step decides the result. Do them in order: the second is only instructive once
you have seen what a clean baseline looks like.

---

## Scenario 1 — Student academic performance

### Problem description

Predict a student's final score (0–100) from study habits, attendance, prior grade and sleep, and
separately predict whether the student passes (score ≥ 55). Both targets exist in the dataset, so
you will build a regression and a classifier from the same features and compare what each can
tell an adviser.

### Business context

A university advising office can contact a limited number of students each term. A regression
gives an expected score and a ranking; a classifier gives a yes/no flag. The office wants to know
which one to use, at what threshold, and what the errors cost. This is a decision-support exercise,
not an automated grading system — the model must never be used to assign a grade.

### Dataset source and licence

- **In this lab:** `code/datasets.students(n=600, seed=0)` — synthetic, generated in-script, no
  licence restrictions, deterministic.
- **Real counterpart:** UCI Machine Learning Repository, *Student Performance* (Cortez & Silva,
  2008), licensed CC BY 4.0. Download `student-por.csv` or `student-mat.csv` and map the columns:
  `studytime` (ordinal 1–4), `absences`, `G1`/`G2` (prior grades), `G3` (final grade).
- If you use the real file, cite the dataset and keep the licence notice with your submission. Do
  not report synthetic results as if they came from the real data.

### Dataset description

600 rows, 9 columns.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| study_hours | float | hours per week, 0–21 |
| attendance_pct | float | percentage, 45.6–100, **21 missing** |
| prior_grade | float | previous assessment, 0–100 |
| sleep_hours | float | per night, 3.8–10.2, **14 missing** |
| part_time_job | categorical | yes/no |
| parental_education | categorical | none/school/university |
| internet_at_home | categorical | yes/no |
| final_score | float | target for regression, 34.6–84.5 |
| passed | int | target for classification, score ≥ 55, rate 0.728 |

The correlations with the target are: study hours 0.56, prior grade 0.42, attendance 0.14,
sleep 0.13. Two features carry most of the signal; that is normal in tabular data and worth
noticing before you add complexity.

### Learning objectives

- Build a leakage-free train/test split with missing-value imputation inside a pipeline.
- Fit and interpret OLS coefficients with units.
- Compare MAE, RMSE and R² and justify which one the advising office should quote.
- Convert a regression into a classification with a threshold and compare the two framings.
- Write a baseline and prove the model beats it.

### Tasks

1. Profile the data with `describe_frame`. Record dtypes, missing counts and ranges.
2. Split 75/25 with `seed=0`. Report the number of rows in each set.
3. Fit `LinearRegression` on the four numeric features after median imputation. Report the
   coefficients with units, the intercept, and test MAE/RMSE/R².
4. Compute the mean baseline (predict the training mean) and its MAE and R². Compare.
5. Fit a second model adding one-hot `part_time_job`, `parental_education` and
   `internet_at_home`. Does test R² improve by more than the CV spread? Report both.
6. Add polynomial terms of degree 2 and 3. Tabulate train and test R². Identify the degree at
   which test performance starts to fall.
7. Build the classifier for `passed` with logistic regression on the same features. Report the
   confusion matrix, precision and recall for the "will fail" class (0) **and** the "will pass"
   class (1).
8. Choose a threshold for the advising office if a missed at-risk student costs 5 and an
   unnecessary call costs 1. Justify the number.
9. Write a 150-word recommendation: regression or classification, which metric, which threshold,
   and what the model must not be used for.

### Expected results

- OLS with four features: coefficients approximately `study_hours 1.28`, `attendance 0.098`,
  `prior_grade 0.257`, `sleep 0.897`, intercept ≈ 18.4 (they shift slightly if you impute
  differently).
- Test MAE around 4.5 points, RMSE around 5.5, R² between 0.50 and 0.56.
- Mean baseline MAE around 6.8 and R² near 0.
- Degree 2 does not improve test R² materially; degree 3+ degrades it. If your degree-5 test R² is
  positive and large, check for leakage.
- Classifier accuracy around 0.80–0.85, with much lower recall for the failing class than for the
  passing class.

### Evaluation metrics

Primary: **MAE** (points of final score) for regression, because the advising office thinks in
points, not squared points. Secondary: RMSE and R². For classification: recall for the at-risk
class at the chosen threshold, with precision, F1 and the confusion matrix reported alongside.

### Deliverables

- A notebook or script that runs end to end from `datasets.students()` to the final metrics.
- A results table with train and test values for every model tried.
- The 150-word recommendation.
- A paragraph naming the two features you would try to collect next and why.

### Extension challenges

1. Replace median imputation with a model-based imputer and measure the change in test MAE.
2. Add a missing-indicator for `attendance_pct` and test whether missingness predicts the score.
3. Fit the same model on the 480 training rows with 5-fold CV and compare the CV mean to the
   single holdout score. Which is more trustworthy, and why?
4. Calibrate the classifier and plot predicted probability against observed pass rate in deciles.
5. Try to beat the linear model with a random forest. If you cannot, explain why the extra
   capacity did not pay.

---

## Scenario 2 — House price prediction

### Problem description

Predict a house's sale price in thousands from size, rooms, age, distance to the centre, garage and
neighbourhood — with one impossible living area (12,000 sqft) and six luxury prices in the data.
Your job is to decide what to do about them and to show the effect with numbers.

### Business context

An estate agency wants a first-pass valuation to prioritise which properties get a full
appraisal. A model that is 35 thousand off on average is useful for triage; one that is 74
thousand off is not. The agency also needs to know when the model should refuse: a 12,000 sqft
property is outside the training distribution.

### Dataset source and licence

- **In this lab:** `code/datasets.houses(n=800, seed=0)` — synthetic, generated in-script.
- **Real counterpart:** *Ames Housing* data (De Cock, 2011), distributed through Kaggle's "House
  Prices — Advanced Regression Techniques" competition. Kaggle's competition terms apply; check
  them before redistributing. The UCI *Real Estate Valuation* dataset (CC BY 4.0) is a smaller
  alternative if you want a permissive licence.

### Dataset description

800 rows, 9 columns.

| Column | Type | Range / levels |
| :--- | :--- | :--- |
| living_area_sqft | float | 600–4,200 typical; one row at 12,000 |
| bedrooms | int | 1–6 |
| bathrooms | float | 1.0–4.0 |
| age_years | float | 0–120 |
| distance_to_centre_km | float | 0.2–40 |
| garage | int | 0/1 |
| neighbourhood | categorical | north/east/south/west |
| condition | categorical | fair/good/excellent |
| price_thousands | float | target; 89–1,263, mean 351 |

Six prices are roughly three times the local norm — planted luxury outliers, not errors. The
12,000 sqft area is an error.

### Learning objectives

- Distinguish an impossible value from a legitimate outlier.
- Quantify the effect of clipping with the IQR rule on test R² and RMSE.
- Encode categorical features and interpret the resulting coefficients.
- Recognise when a prediction is an extrapolation and refuse it.

### Tasks

1. Profile the data. Find the impossible area and the six price outliers. Report the rows.
2. Fit OLS on all rows with the numeric features. Record test RMSE, MAE and R².
3. Clip `price_thousands` and `living_area_sqft` with the IQR rule (k = 1.5), recording the
   bounds and how many rows changed.
4. Refit and compare. Report the improvement in RMSE and R².
5. One-hot encode `neighbourhood` and `condition`; fit again. Interpret one coefficient in
   thousands of pounds.
6. Fit with `k = 3.0` clipping instead of 1.5. Which do you defend in the report, and why?
7. Predict the price of a 12,000 sqft house with your final model. Compare it with the observed
   luxury prices and explain why the number is not usable.
8. Produce a residual plot against fitted price and describe the pattern.

### Expected results

- Raw fit: RMSE ≈ 74, MAE ≈ 35, R² ≈ 0.38.
- After clipping: RMSE ≈ 35, MAE ≈ 24, R² ≈ 0.75.
- Clip bounds: price ≈ 155–540 thousand, area ≈ 381–3,207 sqft; 7 rows change.
- The 12,000 sqft prediction is far outside the observed price range — a clear extrapolation.
- Residuals widen at higher prices (heteroscedasticity), which is expected for prices.

### Evaluation metrics

**RMSE** as the headline (large errors are the ones that hurt a valuation), with MAE for the
typical error and R² for the variance explained. Report all three before and after preparation —
the delta is the finding.

### Deliverables

- A preparation log: every change, the rule used, the rows affected.
- A before/after table (RMSE, MAE, R²).
- The final model, with one coefficient interpreted in business units.
- A one-paragraph "when to refuse" policy for out-of-range properties.

### Extension challenges

1. Model `log(price)` instead of price and compare RMSE on the original scale after
   back-transformation. Does the log fit the multiplicative structure better?
2. Add an interaction `living_area × neighbourhood` and test whether it earns its place.
3. Fit ridge with several alphas and plot test RMSE against alpha. Is the model variance-limited?
4. Build a simple refusal rule based on the Mahalanobis distance of the features and quantify how
   many test rows it would refuse.
5. Compare a random forest with the linear model. Which handles the luxury outliers better without
   clipping?

---

## Shared requirements

- **No test-set tuning.** All choices come from training data or cross-validation.
- **Report the baseline.** A model that does not beat the mean predictor has not earned a report.
- **Seed everything.** Use `seed=0` unless an exercise says otherwise, and record the seed.
- **Every number in your report must come from a run you can reproduce.**
- **Code quality:** functions, no copy-paste blocks, comments explaining *why*.

## Evaluation criteria

| Criterion | Weight | What earns full marks |
| :--- | ---: | :--- |
| Correctness of pipeline | 30% | split before preprocessing, no leakage, reproducible |
| Preparation judgement | 25% | outliers handled with a stated rule, effect quantified |
| Metric choice and interpretation | 20% | metric tied to the decision, baseline shown |
| Communication | 15% | results table, units, honest limitations |
| Code quality | 10% | readable, modular, commented |

## Hints

- `prep.describe_frame` finds the impossible value quickly; `prep.clip_outliers_iqr` returns the
  bounds, so you can report them.
- If your R² is suspiciously high, check whether `final_score` (scenario 1) or any price-derived
  column (scenario 2) is in the feature matrix.
- `LinearRegression.score` returns R²; use `linreg.regression_report` for the full set.

## Reflection

1. In scenario 1, which mattered more: the model or the choice of metric? Justify with numbers.
2. In scenario 2, did outlier handling change the ranking of features or only the scale of the
   errors?
3. Which of the two problems would you refuse to ship without more data, and why?

## Time budget

| Task | Time |
| :--- | ---: |
| Scenario 1, tasks 1–6 | 60 min |
| Scenario 1, tasks 7–9 | 25 min |
| Scenario 2, tasks 1–6 | 45 min |
| Scenario 2, tasks 7–8 | 15 min |
| Write-up | 15 min |

Next: [LAB-06-02 — Model Comparison: Spam and Loan Approval](lab-06-02-model-comparison-spam-and-loans.md).

## Starter material

The guided notebook [`nb-06-01-data-preparation-workbench.ipynb`](../notebooks/nb-06-01-data-preparation-workbench.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
