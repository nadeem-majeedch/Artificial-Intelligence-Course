# M06 — Machine Learning Fundamentals and Algorithms

| Level | 300 |
| :--- | :--- |
| Study time | 31.4 hours — guided 10.0 · practical 12.0 · assessment 5.9 · project 3.5 |
| Lessons | 10 |
| Course outcome | CLO5 — build, evaluate and defend a machine-learning model on tabular data |
| Prerequisites | P02 (matrices, gradients), P03 (probability), P04 (data preparation); M05 recommended |

[Course home](../../README.md) · [All modules](../README.md) · [Next module: M07 Neural Networks →](../README.md#m07)

## Overview

This is the module the rest of the applied course depends on. It covers the classical algorithm
family — linear and logistic regression, k-NN, naïve Bayes, trees, forests, boosting, SVMs, k-means,
GMM, PCA — and the part most tutorials skip: validation design, leakage, baselines, metric choice,
calibration, bias–variance and honest error analysis.

The organising question is not "which algorithm is best?" but "what evidence would justify
shipping this model?". Every lesson therefore ends with the failure modes of the method it just
taught.

All datasets are **synthetic and generated in-script with fixed seeds**, so every number in the
lessons, notebooks and labs reproduces offline. Each mirrors the schema of a named public dataset
(UCI Student Performance, Ames Housing, SMS Spam Collection, Online Retail II, German Credit,
NSL-KDD, IBM HR Attrition, ULB Credit Card Fraud) so the labs can swap in the real file. Results on
the synthetic data are teaching results and must not be reported as benchmarks.

## Learning outcomes

By the end of this module you will be able to:

1. **Frame** a tabular problem: decision, label, prediction time, cost asymmetry, baseline, metric.
2. **Prepare** data without leakage: split first, impute/encode/scale inside a pipeline, handle
   outliers with a stated rule.
3. **Fit** linear, logistic, k-NN, naïve Bayes, tree, forest, boosting and SVM models, and explain
   what each one assumes.
4. **Evaluate** with confusion matrices, precision/recall/F1, ROC-AUC, average precision, MAE, RMSE
   and R², choosing the metric from the decision.
5. **Diagnose** overfitting and underfitting from learning curves and close the gap with
   regularisation, capacity control or more data.
6. **Cluster and compress** with k-means, hierarchical clustering, DBSCAN, GMM and PCA, and validate
   without labels.
7. **Detect** anomalies at a fixed alert budget and report precision/recall there.
8. **Deliver** a reproducible pipeline, a results record and a model card.

## Before you start

You need to be able to write and debug a Python function, use NumPy arrays and pandas DataFrames,
and read a derivative. The prerequisite lessons:

- **Matrices and gradients** — [P02](../../prerequisites/P02-mathematics-for-ai/README.md)
- **Probability and Bayes** — [P03](../../prerequisites/P03-probability-and-statistics/README.md)
- **Dataframes, missing values, plots** — [P04](../../prerequisites/P04-data-preparation-and-visualization/README.md)

**Readiness self-check.** If you cannot do three of these, spend a few hours in the prerequisites:

1. Multiply a $3\times4$ matrix by a $4\times1$ vector by hand.
2. Compute a conditional probability from a two-way table.
3. Load a CSV into pandas and report the missing count per column.
4. Explain what a derivative measures, in one sentence.
5. Compute the mean and standard deviation of five numbers.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L06-01 | What Machine Learning Is, and What It Is Not | Lesson | 75 m | [Read](lessons/L06-01-what-machine-learning-is.md) |
| L06-02 | Data Preparation, Splitting and Leakage | Lesson | 75 m | [Read](lessons/L06-02-data-splitting-leakage-and-cross-validation.md) |
| L06-03 | Linear Regression from First Principles | Lesson | 75 m | [Read](lessons/L06-03-linear-regression-from-first-principles.md) |
| L06-04 | Classification with Logistic Regression | Lesson | 75 m | [Read](lessons/L06-04-classification-with-logistic-regression.md) |
| L06-05 | Model Evaluation: Metrics, Confusion Matrices and ROC | Lesson | 75 m | [Read](lessons/L06-05-model-evaluation-metrics-and-roc.md) |
| L06-06 | Bias, Variance, Regularisation and Generalisation | Lesson | 75 m | [Read](lessons/L06-06-bias-variance-and-regularisation.md) |
| L06-07 | k-Nearest Neighbours and Naïve Bayes | Lesson | 75 m | [Read](lessons/L06-07-k-nearest-neighbours-and-naive-bayes.md) |
| L06-08 | Decision Trees, Random Forests, Boosting and SVMs | Lesson | 75 m | [Read](lessons/L06-08-trees-forests-boosting-and-svm.md) |
| L06-09 | Unsupervised Learning and Dimensionality Reduction | Lesson | 75 m | [Read](lessons/L06-09-unsupervised-learning-and-dimensionality-reduction.md) |
| L06-10 | Building a Reproducible ML Pipeline | Lesson | 75 m | [Read](lessons/L06-10-reproducible-ml-pipelines.md) |
| NB-06-01 | Data Preparation Workbench | Notebook | 60 m | [Open](notebooks/nb-06-01-data-preparation-workbench.ipynb) |
| NB-06-02 | Regression and Classification Workbench | Notebook | 60 m | [Open](notebooks/nb-06-02-regression-and-classification-workbench.ipynb) |
| NB-06-03 | Model Comparison and Ensembles | Notebook | 60 m | [Open](notebooks/nb-06-03-model-comparison-and-ensembles.ipynb) |
| NB-06-04 | Clustering, PCA and Anomalies | Notebook | 60 m | [Open](notebooks/nb-06-04-clustering-pca-and-anomalies.ipynb) |
| LAB-06-01 | Student Performance and House Prices | Lab | 2.5 h | [Start](labs/lab-06-01-student-performance-prediction.md) |
| LAB-06-02 | Model Comparison: Spam and Loans | Lab | 2.5 h | [Start](labs/lab-06-02-model-comparison-spam-and-loans.md) |
| LAB-06-03 | Customer Segmentation and Attrition | Lab | 2.5 h | [Start](labs/lab-06-03-customer-segmentation-and-attrition.md) |
| LAB-06-04 | Intrusion, Fraud and the Leakage Hunt | Lab | 2.5 h | [Start](labs/lab-06-04-intrusion-fraud-and-leakage.md) |
| ASG-06 | Complete ML Pipeline with Report | Assignment | 2 h | [Start](assignments/asg-06-complete-ml-pipeline.md) |
| QUIZ-06 | Module self-check | Quiz | 30 m | [Take](quizzes/quiz-06.md) |
| MP-06 | Prediction Challenge | Mini-project | 2 h | [Start](projects/mp-06-prediction-challenge.md) |

**Total published:** 10.0 h guided study + 12.0 h practical + 5.9 h assessment + 3.5 h mini-project = **31.4 hours**.

Supporting code lives in [`code/`](code/): `datasets.py` (eight seeded generators), `prep.py`
(splitting, imputation, encoding, scaling, pipeline), `linreg.py` (OLS, gradient descent,
polynomials, ridge, lasso, regression metrics), `classifiers.py` (logistic, k-NN, Gaussian and
multinomial NB, CART, random forest, gradient boosting, linear SVM), `unsupervised.py` (k-means,
hierarchical, DBSCAN, GMM, PCA, anomaly scores), `evaluation.py` (confusion matrix, metrics, ROC/PR,
CV, grid search, learning curves, bootstrap), and `sklearn_compare.py` (the same models fitted with
scikit-learn, side by side). Every module runs standalone: `python prep.py`, and so on.

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L06-01, L06-02 | 2.5 h |
| 2 | L06-03, NB-06-01 | 2.5 h |
| 3 | L06-04, L06-05 | 2.5 h |
| 4 | NB-06-02, LAB-06-01 (start) | 2.5 h |
| 5 | LAB-06-01 (finish), L06-06 | 2.5 h |
| 6 | L06-07, NB-06-03 | 2.5 h |
| 7 | L06-08, LAB-06-02 | 3 h |
| 8 | L06-09, NB-06-04 | 2.5 h |
| 9 | LAB-06-03 | 2.5 h |
| 10 | L06-10, LAB-06-04 | 3 h |
| 11 | QUIZ-06, ASG-06 | 2.5 h |
| 12 | MP-06, revision | 2 h |

Thirteen study days at roughly 2.5 hours. If you have less time, keep the labs and drop the
notebooks only after you have reproduced their numbers by hand; never drop LAB-06-04, because the
leakage audit is the skill that transfers to every later module.

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-06-01 | Regression workflow, prep judgement, baseline | 10% |
| LAB-06-02 | Comparison discipline, threshold reasoning, error analysis | 10% |
| LAB-06-03 | Clustering validation, imbalance handling, communication | 10% |
| LAB-06-04 | Leakage audit, budget-aware detection metrics | 10% |
| QUIZ-06 | Conceptual and numerical grasp | 10% |
| ASG-06 | Complete pipeline, reproducibility, model card | 25% |
| MP-06 | Best honest model under fixed rules, error analysis | 25% |

The six assessment dimensions are described in the
[curriculum map](../../docs/CURRICULUM-MAP.md#8-assessment-model).

## Key terms introduced

**Supervised/unsupervised/self-supervised/reinforcement learning**, **baseline**, **leakage**,
**imputation**, **one-hot encoding**, **standardisation**, **cross-validation**, **bias**,
**variance**, **regularisation**, **ridge**, **lasso**, **log-odds**, **cross-entropy**,
**confusion matrix**, **precision**, **recall**, **F1**, **ROC**, **AUC**, **average precision**,
**class weight**, **bagging**, **boosting**, **margin**, **kernel**, **inertia**, **silhouette**,
**DBSCAN**, **GMM**, **PCA**, **anomaly score**, **model card**, **drift**.

All are defined in the [glossary](../../resources/glossary.md). The one-page recap is in
[summary.md](summary.md).

## Resources

- scikit-learn user guide — the reference API these lessons imitate; read the sections for the
  model you are using.
- Hastie, Tibshirani & Friedman (2009), *The Elements of Statistical Learning* — free online, the
  canonical treatment of everything in L06-03 to L06-09.
- Géron (2022), *Hands-On Machine Learning* — the practical companion for the labs.
- The module's [summary](summary.md) — formulas and numbers for revision.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) ·
[Prerequisites](../../prerequisites/README.md) · [Next module: M07 Neural Networks →](../README.md#m07)

## Assignment

[PA-06 — A Leakage-Free Prediction Pipeline](../../assessments/programming/pa-06-machine-learning.md)
