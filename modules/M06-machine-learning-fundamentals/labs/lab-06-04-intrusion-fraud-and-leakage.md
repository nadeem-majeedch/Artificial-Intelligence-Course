# LAB-06-04 — Intrusion, Fraud and the Leakage Hunt

> **Module M06** · Lab 4 of 4 · ~150 minutes · Level 300
> **Scenarios:** 6 (network intrusion), 8 (credit-card anomaly detection), plus the leakage audit
> **Prerequisites:** L06-02, L06-08, L06-09 · **Pairs with:** NB-06-04

[Previous lab: LAB-06-03](lab-06-03-customer-segmentation-and-attrition.md) · [Module overview](../README.md) · [Next: QUIZ-06 →](../quizzes/quiz-06.md)

Two detection problems where positives are rare, and one audit that decides whether any of your
earlier results can be trusted. Do the audit first: a detection model built on a leaking pipeline
is a story, not a result.

---

## Part A — The leakage hunt

### Problem description

You are given four pipelines that all report excellent scores. At least two of them leak. Find the
leak in each, explain the mechanism, fix it, and quantify the drop.

### Business context

A model that scores 1.000 in a notebook and 0.70 in production is worse than a model that scores
0.78 in both. The audit is the step that prevents the first from ever being deployed, and it is the
step most often skipped when a deadline is close.

### What you are given

- The student dataset, where `passed` is derived from `final_score`.
- A house dataset with a planted impossible value and six luxury outliers.
- `prep.Pipeline`, `SimpleImputer`, `StandardScaler`, `OneHotEncoder`.
- Four broken pipelines below, described rather than implemented so you must build each yourself.

| Pipeline | Reported score | Suspicion |
| :--- | ---: | :--- |
| A: predicts `passed` using `final_score` as a feature | test accuracy 1.000 | ? |
| B: imputes and scales on all rows, then cross-validates | CV accuracy slightly above the honest run | ? |
| C: random 80/20 split of transactions ordered by time | test AUC much higher than a time-ordered split | ? |
| D: splits patient visits randomly, with several visits per patient | test AUC inflated | ? |

### Learning objectives

- Apply the four-leakage taxonomy (target, preprocessing, temporal, group) to concrete code.
- Quantify the optimism each leak creates.
- Rebuild each pipeline so that `fit` touches training rows only.
- Write a reusable audit checklist.

### Tasks

1. Reproduce pipeline A. Report test accuracy. Remove the leaking column and re-run. Report both
   numbers and the difference.
2. Build the honest and dishonest versions of pipeline B (scaler fitted on all rows versus inside
   the fold) and compare 5-fold CV accuracy. The difference is small — explain why it is still a
   defect.
3. For pipeline C, sort the transaction data by `hour` (a proxy for time), make a random split and
   a time-ordered split, and compare test AUC.
4. For pipeline D, simulate repeated entities by duplicating 20% of rows with jittered features,
   then compare a random split with a group split.
5. For each of the four, write one sentence naming the mechanism and one sentence naming the fix.
6. Produce a checklist of six checks you would run on any tabular pipeline before believing its
   score.

### Expected results

```text
pipeline A with final_score : test accuracy 1.000
pipeline A without          : test accuracy 0.827
pipeline B                  : difference of a few tenths of a point (real but small)
pipeline C                  : random split AUC materially higher than time-ordered
pipeline D                  : random split AUC inflated by the duplicated entity
```

The A gap (17 points) is the loud leak. B is the quiet one: small enough to survive review, which
is exactly why it needs a rule rather than vigilance.

### Evaluation metrics

The **gap** between the reported and honest score, and whether the student can explain the
mechanism. No model performance is being assessed here.

### Deliverables

- The four repaired pipelines, each with a comment naming the leak it removes.
- A before/after table of reported versus honest scores.
- The six-item checklist.

---

## Scenario 6 — Network intrusion detection

### Problem description

Classify a network connection record as normal or an attack from flow features, then break the
errors down by attack family. This is the scenario where aggregate accuracy is most misleading:
99% of the traffic is normal, and the attacks you care about are the rare families.

### Business context

A security operations centre can investigate a limited number of alerts per shift. Missing a
denial-of-service burst is expensive; investigating benign traffic burns the analysts' attention.
The centre needs recall by attack family at a fixed alert budget, not a single accuracy figure.

### Dataset source and licence

- **In this lab:** `code/datasets.intrusion(n=3000, seed=0)` — synthetic features named after
  NSL-KDD, with three attack families.
- **Real counterpart:** *NSL-KDD* (Tavallaee, Bagheri, Lu & Ghorbani, 2009), a cleaned version of
  KDD Cup 99, made available for research. Cite the paper, and check the hosting page's current
  terms before redistributing. Load it with `pd.read_csv` after downloading; the 41 original
  columns include `protocol_type`, `src_bytes`, `dst_bytes`, `serror_rate`, `num_failed_logins`
  and the `attack_type` label you must collapse to binary.
- The synthetic generator is a teaching stand-in, not a substitute for the real benchmark. Results
  on it do not transfer.

### Dataset description

3,000 rows, 11 columns.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| duration | float | connection seconds |
| src_bytes / dst_bytes | float | bytes sent / received |
| count / srv_count | int | connections to the same host / service |
| serror_rate | float | fraction of SYN errors, 0–1 |
| num_failed_logins | int | failed login attempts |
| logged_in | int | 0/1 |
| protocol_type | categorical | tcp/udp/icmp |
| attack_family | categorical | normal/probing/dos/r2l |
| is_attack | int | target, 21.1% positive |

Family counts: normal 2,366, probing 281, dos 232, r2l 121. The r2l family is the smallest and the
hardest.

### Learning objectives

- Handle heavily skewed byte counts with a log transform and explain why.
- Report precision, recall and AUC overall **and per attack family**.
- Read feature importance critically.
- Choose an alert budget and compute recall at that budget.

### Tasks

1. Split 75/25 stratified. Apply `log1p` to `duration`, `src_bytes`, `dst_bytes`; scale; fit a
   random forest.
2. Report accuracy, precision, recall and AUC. Compare with the majority baseline (0.789).
3. Compute recall **per attack family** on the test set. Which family is worst, and by how much?
4. Report the confusion matrix and the number of false positives per 1,000 connections.
5. Rank features by importance. Which single feature dominates, and why is that plausible for this
   synthetic generator?
6. Sweep the threshold and report precision/recall at 100, 200 and 400 alerts.
7. Remove `serror_rate` and refit. Report the AUC change. Is the model still usable?
8. Fit logistic regression and compare. Does the tree-based model's advantage justify its extra
   complexity?
9. Write a 150-word note to the SOC lead: expected alert volume, expected true attacks caught, and
   the family you cannot currently detect well.

### Expected results

```text
random forest: accuracy 0.979  precision 0.961  recall 0.937  AUC 0.996
majority baseline accuracy: 0.789
feature importance: serror_rate 0.428, dst_bytes 0.232, num_failed_logins 0.142,
                    duration 0.125, logged_in 0.044, src_bytes 0.016
```

- Recall for r2l is markedly lower than for dos — the small, subtle family is the hard one.
- Removing `serror_rate` costs several points of AUC; the model leans on one strong signal.
- At 100 alerts, precision should stay high; recall falls as the budget tightens.

### Evaluation metrics

**Recall per attack family at a fixed alert budget**, with precision at that budget. AUC for
ranking. Accuracy only beside the baseline.

### Deliverables

- The overall and per-family metric table.
- The alert-budget table.
- Feature importance with a critical note.
- The SOC note.

### Extension challenges

1. Rebalance with class weights or resampling and measure the effect on r2l recall.
2. Build a one-vs-rest model per family and compare with the binary model's per-family recall.
3. Add a cost matrix (missed dos vs missed r2l) and compute the cost-optimal threshold.
4. Train on the first 70% by row order and test on the last 30%. Does performance hold? What does
   that suggest about temporal drift?
5. Use `evaluation.learning_curve` to see whether more attack examples would fix the r2l gap.

---

## Scenario 8 — Credit-card transaction anomaly detection

### Problem description

Flag fraudulent card transactions when fraud is 0.8% of rows. Treat it first as unsupervised
anomaly detection (no labels at training time) and then as supervised classification, and compare
what each buys at a fixed review capacity.

### Business context

A fraud team can review 30 alerts per day out of thousands of transactions. The operating question
is not "what is the accuracy?" but "of the 30 alerts I can review, how many are real fraud?" A
model with 99.2% accuracy that flags nothing is worthless; a ranking that puts 20 real frauds in
the top 30 is a product.

### Dataset source and licence

- **In this lab:** `code/datasets.transactions(n=5000, seed=0)` — synthetic, 0.8% fraud, 39
  positives.
- **Real counterpart:** *Credit Card Fraud Detection* (Dal Pozzolo, Caelen, Johnson & Bontempi,
  2015), ULB Machine Learning Group, distributed via Kaggle under DbCL / ODbL. It has 284,807
  transactions, 492 frauds, and 28 anonymised PCA features plus `Time` and `Amount`.
- The real dataset is extremely imbalanced (0.172%). Any result on this synthetic sample must be
  labelled as a teaching result.

### Dataset description

5,000 rows, 8 columns.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| amount | float | transaction value, heavy-tailed |
| hour | int | 0–23 |
| distance_from_home_km | float | heavy-tailed |
| ratio_to_median_spend | float | relative to the cardholder's median |
| foreign_transaction | int | 0/1 |
| merchant_category | categorical | six levels |
| attempts_last_hour | int | velocity feature |
| is_fraud | int | target, 0.78% positive |

### Learning objectives

- Compute precision and recall at a fixed alert budget rather than at a default threshold.
- Compare z-score, IQR and Mahalanobis anomaly scores on the same data.
- Show why per-feature rules over-flag skewed amounts.
- Train a supervised model with and without class weighting and compare with the unsupervised
  ranking.
- Explain the operational trade between alert volume and precision.

### Tasks

1. Report the fraud rate and the majority-class accuracy (≈ 0.992). Confirm that a constant
   "normal" predictor achieves it.
2. `log1p`-transform the four numeric features and standardise them.
3. Flag anomalies with z > 3 on any feature. Report the number of flags, precision and recall.
4. Flag with the IQR rule (k = 1.5) on the raw features. Report the same. Explain the difference.
5. Compute Mahalanobis scores and report precision/recall at budgets 25, 50 and 100.
6. Fit logistic regression and a random forest with `class_weight="balanced"`. Report AUC, average
   precision, and precision/recall at the 30-alert budget.
7. Compare the unsupervised ranking with the supervised ranking. Which would you ship if labels
   arrived only after 60 days?
8. Build the alert list for a 30-alert day: how many are real, and what is the review cost per true
   fraud?
9. Write a 150-word memo: method, alert budget, expected precision, and the main caveat.

### Expected results

```text
fraud rate 0.0078 (39 of 5,000); "predict normal" accuracy 0.992
z > 3       73 flags   precision 0.438   recall 0.821
IQR k=1.5  932 flags   precision 0.042   recall 1.000
Mahalanobis top 25   precision 0.920   recall 0.590
Mahalanobis top 50   precision 0.680   recall 0.872
Mahalanobis top 100  precision 0.370   recall 0.949
```

- The IQR rule's recall of 1.000 is worthless: 932 alerts at 4% precision.
- Supervised models should beat Mahalanobis on AUC; the interesting comparison is precision at 30.
- At 30 alerts, the best method should deliver roughly 20 true frauds.

### Evaluation metrics

**Precision at the alert budget** (primary), **recall at the budget**, average precision and AUC.
Never accuracy.

### Deliverables

- The method comparison table at budgets 25/50/100.
- The 30-alert list with true positives marked.
- A note on which method to ship before labels are available, and why.
- The memo.

### Extension challenges

1. Fit an isolation-forest-style score (random splits, path length) and compare at the same budget.
2. Add the `merchant_category` one-hot features and measure whether precision at 30 improves.
3. Simulate label delay: train on the first 3,000 rows and test on the last 2,000, then reverse the
   order. Does the ranking hold?
4. Compute the expected daily cost for a 30-alert budget given a fraud loss of £500 and a review
   cost of £8.
5. Use PCA reconstruction error as the anomaly score and compare with Mahalanobis.

---

## Shared requirements

- **Rare positives change the metric.** Every table must include counts, not only ratios.
- **The audit comes first.** Any detection result produced by a leaking pipeline is void.
- **State the alert budget** before comparing methods.
- **Distinguish synthetic from real.** Do not present these results as benchmarks against NSL-KDD
  or the ULB dataset.
- **No accuracy headlines** unless the majority baseline is printed beside them.

## Evaluation criteria

| Criterion | Weight | What earns full marks |
| :--- | ---: | :--- |
| Leakage audit | 30% | four leaks identified, quantified and repaired |
| Detection evaluation | 30% | budget-aware precision/recall, per-family analysis |
| Interpretation | 20% | explains why methods differ, not just which wins |
| Communication | 20% | memo states method, budget, expected outcome, caveat |

## Hints

- `np.argsort(-scores)[:budget]` gives the top-N ranking directly.
- `evaluation.precision` and `evaluation.recall` work on hard labels; threshold the score at the
  budget's cut-off to use them, or compute the counts directly.
- `log1p` before standardising makes heavy-tailed byte counts and amounts behave.
- Mahalanobis uses the inverse covariance; `np.linalg.pinv` is safer than `inv` on near-singular
  matrices.

## Reflection

1. Which of the four leaks would have survived your previous review process, and why?
2. In the fraud scenario, would you rather have 92% precision at 25 alerts or 68% at 50? State the
   assumption behind your choice.
3. What would you need to measure to know the intrusion model still works six months after
   deployment?

## Time budget

| Task | Time |
| :--- | ---: |
| Part A, tasks 1–6 | 40 min |
| Scenario 6, tasks 1–9 | 55 min |
| Scenario 8, tasks 1–9 | 45 min |
| Write-up | 10 min |

Next: [QUIZ-06](../quizzes/quiz-06.md), then [ASG-06](../assignments/asg-06-complete-ml-pipeline.md) and
[MP-06](../projects/mp-06-prediction-challenge.md).

## Starter material

The guided notebook [`nb-06-04-clustering-pca-and-anomalies.ipynb`](../notebooks/nb-06-04-clustering-pca-and-anomalies.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
