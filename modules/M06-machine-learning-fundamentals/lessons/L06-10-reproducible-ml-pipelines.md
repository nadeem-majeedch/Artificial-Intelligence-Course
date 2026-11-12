# L06-10 — Building a Reproducible Machine-Learning Pipeline

[← Previous: ? Lesson](L06-09-unsupervised-learning-and-dimensionality-reduction.md) · [Module end](../README.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: From Notebook to Pipeline](#4-the-procedure-from-notebook-to-pipeline)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Python Implementation](#7-python-implementation)
- [8. Practical Applications](#8-practical-applications)
- [9. Common Mistakes](#9-common-mistakes)
- [10. Practical Exercises](#10-practical-exercises)
- [11. Self-Assessment](#11-self-assessment)
- [12. Key Terms](#12-key-terms)
- [13. Further Reading](#13-further-reading)
- [What to Do Next](#what-to-do-next)

> **Module M06** · Lesson 10 of 10 · ~90 minutes · Level 300
> **Prerequisites:** L06-02 to L06-09

[Previous: L06-09](L06-09-unsupervised-learning-and-dimensionality-reduction.md) · [Module overview](../README.md) · [Next: LAB-06-01 →](../labs/lab-06-01-student-performance-prediction.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Assemble** a leakage-free pipeline as a single object with `fit` and `predict`.
2. **Control** randomness: seeds, split reproducibility, deterministic ordering.
3. **Record** an experiment so that another person can reproduce the number: data version,
   parameters, code state, metric, seed, environment.
4. **Write** a model card that states intended use, population, metrics, limitations and the
   monitoring plan.
5. **Perform** error analysis that finds a subgroup or data-quality problem rather than a decimal
   place.
6. **Plan** deployment: batch versus online, latency budget, drift detection, retraining triggers
   and the feedback loop that can poison the model.

## 2. Prerequisite Knowledge

Everything before this lesson. The pipeline in §3.1 uses `prep.Pipeline`, imputation, scaling and
logistic regression.

## 3. Conceptual Explanation

### 3.1 The pipeline as the unit of work

```python
from prep import Pipeline, SimpleImputer, StandardScaler
from classifiers import LogisticRegressionGD

model = Pipeline([
    ("impute", SimpleImputer("median")),
    ("scale", StandardScaler()),
    ("model", LogisticRegressionGD(lr=0.5, epochs=800)),
])
model.fit(X_train, y_train)          # every statistic comes from the training rows
model.predict(X_test)
```

Why this matters beyond tidiness:

- **Leakage becomes structurally impossible** for the preprocessing steps in the pipeline, because
  `fit` is only ever called on training data.
- **Train and serving preprocessing cannot drift apart**, because there is one implementation.
- **Cross-validation is honest**, because each fold fits a fresh copy.

The failure mode this prevents is the most expensive bug in applied ML: training used one
scaling, serving used another, and nobody noticed for six months.

### 3.2 Reproducibility

Four kinds of state:

| State | Where it lives | How to capture it |
| :--- | :--- | :--- |
| Data | files, database, snapshot | hash or version tag; record the query |
| Code | repository | commit hash; keep notebooks executable |
| Parameters | script, config | explicit values in a config file, not in your head |
| Randomness | RNG | explicit seed for every split, model and shuffle |

Rules that work in practice:

- **One seed, passed down.** Do not rely on global RNG state; the order of calls changes it.
- **Sort before you shuffle** when order should not matter, so ties resolve deterministically.
- **Never edit data by hand in a notebook** without writing the transformation into code.
- **Re-run the whole pipeline from raw data** before reporting. If that takes an hour, automate it;
  if it takes a day, automate it anyway.
- **Pin versions** for the packages that affect numbers (NumPy, pandas, scikit-learn). Floating
  point results can differ across versions.

### 3.3 What to log for every experiment

```text
experiment_id : 2026-11-10-loan-logreg-v3
data          : loans.csv sha256=... rows=1500, seed=0 split 75/25 stratified
params        : lr=0.5 epochs=800 l2=0.0 class_weight=balanced
metrics       : cv_acc 0.7853 +/- 0.0185, test_acc 0.7834, auc 0.7976, ap 0.6684
baseline      : majority 0.701
code          : commit 4f2c1a9, python 3.14, numpy 2.5.3, pandas 3.0.6
notes         : threshold 0.5; review team capacity not considered
```

A results table without the data hash and the seed is an anecdote. This is not bureaucracy: it is
the difference between "the model got 78%" and "this pipeline, on this data, with this seed, gets
78%, and here is how to check".

### 3.4 The model card

One page, written for someone who will not read the code:

- **Purpose and intended users.**
- **Training data**: source, collection period, population, known gaps.
- **Features**: what each one means, and which are unavailable at prediction time.
- **Metrics**: on what split, with what baseline and interval.
- **Subgroup performance**: where it is worse, and by how much.
- **Limitations**: what it must not be used for.
- **Monitoring**: what is checked, how often, and who acts.
- **Retraining policy**: trigger and cadence.

### 3.5 Error analysis

A single metric hides the failure pattern. The workflow:

1. Take the wrong predictions on the validation set.
2. Slice by every feature you have (age band, region, income quartile, time period).
3. Look for a slice where the error rate is double the average.
4. Look at individual rows: is the label wrong? Is the feature missing? Is the case genuinely
   ambiguous?
5. Fix the cause — data, label definition, feature, or model — and re-measure.

On the loan model, the overall accuracy is 0.783 but recall for approvals is 0.527. Slicing by
`default_history` would show whether the misses concentrate among applicants with thin credit
files; that finding is worth more than another 0.005 of accuracy.

### 3.6 Deployment and drift

- **Batch scoring**: nightly job, predictions written to a table. Simplest, and adequate for most
  tabular problems.
- **Online scoring**: a service with a latency budget (often <100 ms), model and preprocessing
  packaged together, feature computation on the request path.
- **Drift**: the input distribution changes (`P(X)`), or the relationship changes (`P(y|X)`).
  Monitor feature means, missing rates, prediction distribution, and — when labels arrive — the
  metrics.
- **Label delay**: fraud chargebacks arrive weeks later; churn labels after a quarter. Plan the
  evaluation lag into the monitoring.
- **Feedback loops**: if the model decides who gets a retention call, the labels for those who
  were not called are missing. The next model is trained on a censored sample. This is a
  first-class design problem, not a footnote.

### 3.7 The reproducibility checklist

- [ ] Data loaded by code, not by hand.
- [ ] Split reproducible and stratified/time-ordered as appropriate.
- [ ] All preprocessing inside the pipeline, fitted on training data.
- [ ] Every random source seeded.
- [ ] Baseline computed and reported.
- [ ] Metric chosen from the decision, with an interval.
- [ ] Test set touched once.
- [ ] Confusion matrix and error slices recorded.
- [ ] Model card written.
- [ ] Monitoring plan and retraining trigger written.
- [ ] Whole pipeline re-run from raw data end to end.

## 4. The Procedure: From Notebook to Pipeline

1. Write the pipeline object first; keep every transformation inside it.
2. Put the config (paths, seed, hyperparameters, thresholds) in one dictionary at the top.
3. Split once; save the split indices so every model sees the same rows.
4. Cross-validate on train; choose hyperparameters; record the table.
5. Fit on train+validation; evaluate on test once; record the confusion matrix.
6. Run error analysis on validation (not test) to avoid overfitting the test set.
7. Write the model card from the recorded numbers, not from memory.
8. Package: pipeline + config + model card + requirements.
9. Re-run from raw data on a clean environment; compare the metric. A difference means hidden
   state.

## 5. Worked Examples

### Example 1 — The same pipeline, honestly cross-validated

```text
make_pipeline() → impute(median) → scale → logistic(lr=0.5, epochs=600)

5-fold stratified CV accuracy: [0.7933 0.7567 0.8133 0.7833 0.7800]
mean 0.7853   std 0.0185
```

The spread is 5.7 percentage points between the best and worst fold. Two models whose means
differ by less than about two points are not distinguishable on this dataset. Reporting "78.5%"
without the spread invites a false comparison.

### Example 2 — A model card, filled in

```text
Purpose        : flag loan applications for manual review before approval
Training data  : synthetic German-Credit-shaped sample, 1,500 rows, generated in-script
Features       : income, loan amount, credit score, employment years, debt ratio, default history
Target         : approved (30%)
Model          : logistic regression, standardised, threshold 0.5
Metrics        : test accuracy 0.783, AUC 0.798, AP 0.668, recall(approved) 0.527
Baseline       : majority class 0.701
Subgroups      : not evaluated — required before any real use
Limitations    : synthetic data; no protected attributes; threshold not cost-tuned
Monitoring     : monthly AUC and approval-rate check; drift trigger at 5% shift
Retraining     : quarterly, or when AUC falls below 0.75
```

The "not evaluated" line is the most important one. A model card that hides its gaps is
marketing.

### Example 3 — Error analysis that changes the plan

Suppose slicing the loan errors shows that recall for applicants with `employment_years < 1` is
0.18 while the overall is 0.53. Two responses:

- **Model**: add an interaction or a separate model for thin-file applicants.
- **Data**: the label for that group is delayed or noisy, so the model is learning a corrupted
  target.

The second is more common than students expect, and no amount of hyperparameter tuning finds it.

## 6. Mathematical Formulation

**Pipeline as a composed function.** With preprocessing $T_\theta$ fitted on training data and
estimator $f_\phi$,

$$
\hat y(x) = f_\phi\big(T_\theta(x)\big),
\qquad
(\theta,\phi) \text{ estimated on } \mathcal{D}_{train} \text{ only}.
$$

**Cross-validated estimate with spread**:

$$
\bar R = \frac{1}{k}\sum_{i=1}^{k}R_i,
\qquad
s = \sqrt{\frac{1}{k-1}\sum_{i=1}^{k}(R_i-\bar R)^2}.
$$

**Paired comparison** of two models on the same folds uses the differences
$d_i = R_i^{(A)} - R_i^{(B)}$, with standard error $s_d/\sqrt{k}$. If $|d|$ is smaller than about
two standard errors, the ranking is not established — the same logic as a paired t-test, applied
as a sanity check rather than a ritual.

**Drift** can be monitored with a two-sample statistic on features, e.g. the population stability
index

$$
\text{PSI} = \sum_b (p_b^{new} - p_b^{ref})\ln\frac{p_b^{new}}{p_b^{ref}},
$$

binned over a feature; values above ~0.2 are conventionally treated as material.

## 7. Python Implementation

```python
# run from modules/M06-machine-learning-fundamentals/code
import json
import numpy as np
import datasets as ds
import evaluation as ev
from prep import Pipeline, SimpleImputer, StandardScaler, train_test_split
from classifiers import LogisticRegressionGD

frame = ds.loans()
cols = ["annual_income_k", "loan_amount_k", "credit_score",
        "employment_years", "debt_ratio", "default_history"]
X = frame[cols].fillna(frame[cols].median()).to_numpy()
y = frame["approved"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)

config = {"lr": 0.5, "epochs": 800, "threshold": 0.5, "seed": 0}

def make_pipeline(cfg=config):
    return Pipeline([
        ("impute", SimpleImputer("median")),
        ("scale", StandardScaler()),
        ("model", LogisticRegressionGD(lr=cfg["lr"], epochs=cfg["epochs"])),
    ])

cv = ev.cross_val_score(make_pipeline, X_train, y_train, k=5, stratified=True)
model = make_pipeline().fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
pred = (proba >= config["threshold"]).astype(int)

record = {
    "config": config,
    "cv": {"mean": round(float(cv.mean()), 4), "std": round(float(cv.std()), 4)},
    "test": {
        "accuracy": round(ev.accuracy(y_test, pred), 4),
        "auc": round(ev.roc_auc_score(y_test, proba), 4),
        "average_precision": round(ev.average_precision(y_test, proba), 4),
        "confusion": ev.confusion_matrix(y_test, pred).tolist(),
    },
}
print(json.dumps(record, indent=1))
```

```text
{
 "config": {"lr": 0.5, "epochs": 800, "threshold": 0.5, "seed": 0},
 "cv": {"mean": 0.7772, "std": 0.033},
 "test": {"accuracy": 0.7834, "auc": 0.7976, "average_precision": 0.6684,
          "confusion": [[234, 28], [53, 59]]}
}
```

(The CV here is computed on the training split only, which is why it is lower and more variable
than the full-data cross-validation in Example 1 — the folds are smaller and the model never sees
the test rows.)

Saving and loading the whole pipeline, so serving uses the same transformations:

```python
import pickle

with open("loan_model.pkl", "wb") as handle:
    pickle.dump({"pipeline": model, "config": config, "features": cols}, handle)

with open("loan_model.pkl", "rb") as handle:
    bundle = pickle.load(handle)

print("reloaded predictions identical:",
      np.allclose(bundle["pipeline"].predict_proba(X_test)[:, 1], proba))
```

Pickling is fine for a course and for small tabular models. In production, prefer a format with a
schema and a version (ONNX, or the library's own versioned format) and never load a pickle from an
untrusted source — unpickling executes code.

### Scratch versus scikit-learn

The module implements its own estimators so the arithmetic is visible; the same models from
scikit-learn should agree, and where they do not, the difference should be explainable. Run
`python sklearn_compare.py`:

```text
model                  scratch acc sklearn acc scratch AUC sklearn AUC
logistic regression          0.783       0.783       0.798       0.798
k-nearest neighbours         0.743       0.743       0.766       0.766
decision tree (d=5)          0.717       0.717       0.696       0.696
random forest                0.762       0.773       0.802       0.801

k-means inertia  scratch 211.6   sklearn 211.6
k-means silhouette scratch 0.539 sklearn 0.539
PCA explained ratio scratch [0.87  0.066]
PCA explained ratio sklearn [0.87  0.066]
PCA loadings agree up to sign: True
```

Logistic regression, k-NN and the tree match exactly because they have little hidden state. The
forest differs by a point because the two implementations draw bootstrap samples and feature
subsets differently — same algorithm, different random stream. That is the useful outcome of the
exercise: agreement where the maths is identical, an explainable difference where the randomness
is not.

Writing this comparison is also how the module's own k-means inertia bug was found: the scratch
number disagreed with scikit-learn by a factor of eight because the wrong axis was reduced.
Checking your implementation against a trusted one is not cheating; it is testing.

## 8. Practical Applications

- **Bank model risk** — model documentation, validation and monitoring are regulatory
  requirements, not extras.
- **Clinical deployment** — the model card records the population, the label definition and the
  subgroup gaps; silent updates are prohibited.
- **Retail demand** — nightly batch scoring, drift monitored per store, retraining weekly.
- **Fraud** — online scoring with a latency budget; a feedback loop where blocked transactions
  have no chargeback label.

## 9. Common Mistakes

1. Preprocessing outside the pipeline. The most common production bug in the field.
2. Reporting a score with no seed and no data version.
3. Tuning on the test set "just once more".
4. Saving the model but not the preprocessing; serving then uses different scaling.
5. Monitoring only accuracy, which hides a change in prevalence.
6. Retraining on data the model itself selected (the feedback loop).
7. Writing a model card that lists only the good numbers.

## 10. Practical Exercises

1. Assemble the loan pipeline, log the JSON record, and re-run with seed 1. Which numbers change?
2. Deliberately move the scaler outside the pipeline and fit it on all rows. Measure the CV
   difference. Explain why it is small here and why that makes it dangerous.
3. Write a one-page model card for your LAB-06-01 model, including the "not evaluated" section.
4. Implement a simple PSI check for `credit_score` between train and test.
5. Design a monitoring plan for a churn model where labels arrive 90 days late: what do you check
   weekly, and what triggers retraining?

## 11. Self-Assessment

**Multiple choice**

1. A pipeline's main reproducibility benefit is that
   a) it trains faster. b) every preprocessing statistic is fitted on training data only.
   c) it removes the need for a test set. d) it improves accuracy.
2. Two models score 0.785 ± 0.019 and 0.774 ± 0.017 on the same folds. You should
   a) declare the first better. b) treat them as indistinguishable without a paired comparison.
   c) retrain both. d) use the second because it is simpler.
3. Concept drift means
   a) the code changed. b) the relationship between features and target changed.
   c) the model is overfitted. d) the labels are missing.
4. Pickling a model is risky because
   a) it is slow. b) unpickling can execute arbitrary code. c) it cannot store arrays.
   d) it loses precision.

**Short answer**

5. List four things you must record to make a reported metric reproducible.
6. Why can a feedback loop make the next model worse even though it is trained on more data?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Data version/hash, code version, parameters, seed (and package versions).
6. The new data are censored by the previous model's decisions: outcomes are observed only for the
   cases it selected, so the training sample no longer represents the population.

</details>

## 12. Key Terms

**Pipeline**, **fit/transform contract**, **reproducibility**, **seed**, **config**, **experiment
log**, **model card**, **error analysis**, **slice**, **batch scoring**, **online scoring**,
**latency budget**, **data drift**, **concept drift**, **label delay**, **feedback loop**,
**population stability index**, **retraining trigger**.

## 13. Further Reading

- Sculley, D. et al. (2015). *Hidden Technical Debt in Machine Learning Systems*. NeurIPS.
- Mitchell, M. et al. (2019). *Model Cards for Model Reporting*. FAT*.
- Gebru, T. et al. (2021). *Datasheets for Datasets*. CACM.
- Pineau, J. et al. (2021). *Improving Reproducibility in Machine Learning Research*. JMLR.

## What to Do Next

1. Run the §7 script and save the JSON record.
2. Do exercises 1–2; both are part of the LAB-06-04 leakage audit.
3. Start [LAB-06-01 — Student Performance Prediction](../labs/lab-06-01-student-performance-prediction.md).

---

**Navigation:** [← Previous: ? Lesson](L06-09-unsupervised-learning-and-dimensionality-reduction.md) · [Module end](../README.md)
