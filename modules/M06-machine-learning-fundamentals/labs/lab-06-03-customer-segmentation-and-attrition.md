# LAB-06-03 — Customer Segmentation and Employee Attrition

> **Module M06** · Lab 3 of 4 · ~150 minutes · Level 300
> **Scenarios:** 4 (customer segmentation) and 7 (employee attrition)
> **Prerequisites:** L06-05, L06-06, L06-09 · **Pairs with:** NB-06-03

[Previous lab: LAB-06-02](lab-06-02-model-comparison-spam-and-loans.md) · [Module overview](../README.md) · [Next lab: LAB-06-04 →](lab-06-04-intrusion-fraud-and-leakage.md)

Two problems where the *human* interpretation is the deliverable. Clusters without names are not a
segmentation, and an attrition model with 84% accuracy that catches 13% of leavers is not a
retention tool.

---

## Scenario 4 — Customer segmentation

### Problem description

Group 500 customers by value and engagement so that marketing can treat each group differently.
There is no label: the answer is the grouping, plus a defensible name and action for each group.

### Business context

A retailer has limited campaign budget. Sending the same offer to everyone wastes money on
customers who would have bought anyway and on customers who will never return. Four actionable
segments — premium loyalists, steady regulars, lapsing low-value, high-income low-spend — allow
different offers, different channels and different frequencies. The clustering is a means; the
campaign plan is the end.

### Dataset source and licence

- **In this lab:** `code/datasets.customers(n=500, seed=0)` — synthetic RFM-shaped data with four
  planted segments.
- **Real counterpart:** UCI *Online Retail II* (Chen, 2012), CC BY 4.0 — transactional data from a
  UK online retailer. You compute recency, frequency and monetary value per customer, then cluster
  those three features. The licence permits reuse with attribution.

### Dataset description

500 rows, 6 columns.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| annual_income_k | float | 12–120 |
| spending_score | float | 1–100, survey-style |
| recency_days | float | days since last purchase |
| purchase_frequency | float | purchases in the period |
| monetary_value | float | total spend |
| tenure_months | float | months as a customer |

Four latent groups of sizes 170, 140, 110, 80. The features are correlated within groups, which is
why the first principal component explains 87% of the variance.

### Learning objectives

- Standardise features before distance-based clustering and show why.
- Choose k using inertia, silhouette and domain sense, and explain a disagreement between them.
- Profile clusters and name them in business language.
- Compare k-means, hierarchical clustering, DBSCAN and a Gaussian mixture.
- Use PCA to visualise and to compress, and read the explained-variance ratios.

### Tasks

1. Standardise the six features. Report the mean and standard deviation of each column before and
   after.
2. Run k-means for k = 2…6. Record inertia and silhouette for each.
3. Choose k. Explain the choice when silhouette prefers a different value from the one that
   produces actionable segments.
4. For your chosen k, report cluster sizes and the mean of every feature per cluster.
5. Name each cluster and write one campaign action for it.
6. Repeat with hierarchical clustering (average linkage) on a 150-customer subsample at the same k.
   Compare the assignments qualitatively.
7. Run DBSCAN with `eps` = 0.4, 0.5 and 0.8. Report the noise count and cluster sizes. Explain why
   the largest `eps` is useless.
8. Fit a Gaussian mixture with k = 2…5. Report BIC and the soft membership of the two most
   ambiguous customers.
9. Fit PCA. Report the explained-variance ratios, the number of components for 90% and 95%, and
   the reconstruction error with two components.
10. Produce a two-component scatter coloured by your k-means labels. Label the axes with their
    loadings and note what the first component means.

### Expected results

```text
k  inertia  silhouette
2    620.6       0.580
3    350.3       0.520
4    211.6       0.539
5    194.8       0.405
6    184.3       0.330

k=4 sizes [80, 170, 110, 140]
c0: income 55.3  spending 11.9  recency 53.7  frequency  6.2
c1: income 88.3  spending 80.8  recency 12.7  frequency 21.9
c2: income 32.2  spending 23.9  recency 94.8  frequency  3.4
c3: income 66.4  spending 58.1  recency 31.5  frequency 12.0

PCA ratios [0.870 0.066 0.035 0.028]; 2 components keep 0.937
GMM BIC: k=2 3027.8, k=3 2891.1, k=4 2812.9, k=5 2871.9
DBSCAN eps=0.4: 66 noise; eps=0.5: 20 noise; eps=0.8: 0 noise
```

Silhouette chooses k=2; k=4 recovers the planted segments. That disagreement is the exercise.

### Evaluation metrics

**Silhouette** as an internal index, **stability** across seeds, and **business interpretability**.
There is no accuracy. A segmentation that cannot be named fails, regardless of its silhouette.

### Deliverables

- The k table with inertia and silhouette.
- A cluster profile table with business names and one action per segment.
- The DBSCAN and GMM comparisons, including the noise fraction.
- The PCA variance table and the two-component plot.
- A 150-word memo to the marketing lead: which segments to prioritise, and what you are unsure
  about.

### Extension challenges

1. Re-run k-means with seeds 0–9 at your chosen k. Report the range of cluster sizes. Is the
   solution stable?
2. Add a derived `avg_order_value = monetary_value / frequency` and re-cluster. Does the
   segmentation improve or fragment?
3. Cluster on the first two principal components instead of the raw features. Compare the
   assignments with the full-feature solution.
4. Use the silhouette per sample to identify customers who sit between segments, and propose how
   marketing should treat them.
5. Estimate a monetary value per segment and compute which segment justifies a 10% discount
   campaign.

---

## Scenario 7 — Employee attrition prediction

### Problem description

Predict which employees will leave within the year, so HR can intervene. Attrition is 16%, and the
cost of losing a trained employee is far higher than the cost of an unnecessary retention
conversation — a cost asymmetry that accuracy completely hides.

### Business context

HR has capacity for roughly 100 conversations per year. A model that flags 300 people at 30%
precision wastes 200 conversations; one that flags 90 at 55% precision uses the budget well. The
department also needs to know which factors are associated with leaving, with the explicit caveat
that association is not causation.

### Dataset source and licence

- **In this lab:** `code/datasets.attrition(n=1400, seed=0)` — synthetic, 15.9% attrition.
- **Real counterpart:** *IBM HR Analytics Employee Attrition & Performance* sample dataset,
  distributed via Kaggle. IBM's sample is widely used for teaching; check the Kaggle dataset page
  for the current terms before redistributing.

### Dataset description

1,400 rows, 10 columns.

| Column | Type | Meaning |
| :--- | :--- | :--- |
| age | int | 18–60 |
| monthly_income_k | float | thousands |
| years_at_company | float | 0–30 |
| job_satisfaction | int | 1–4 |
| overtime | int | 0/1 |
| distance_from_home_km | float | 1–60 |
| num_companies_worked | int | 0–9 |
| environment_satisfaction | int | 1–4 |
| job_level | int | 1–5 |
| attrition | int | target, 15.9% positive |

### Learning objectives

- Show that class weighting and threshold choice change the product more than model choice does.
- Interpret logistic coefficients on a rare-event problem without over-claiming.
- Report precision/recall at a fixed review capacity (100 conversations).
- Build a confusion matrix that a non-technical stakeholder can read.
- State the causal limitation explicitly.

### Tasks

1. Split 75/25 stratified. Fit logistic regression with and without `class_weight="balanced"`.
2. Report accuracy, precision, recall and F1 for both. Explain the accuracy drop in the balanced
   model in business terms.
3. Compute the majority baseline accuracy (≈ 0.84) and its recall for leavers (0).
4. Choose a threshold that produces at most 100 flags on the test set. Report the precision,
   recall and number of true leavers caught.
5. Fit a random forest and a gradient boosting model. Compare all three on 5-fold stratified CV
   with mean ± std.
6. Interpret the five largest logistic coefficients in odds terms. Mark which are plausibly
   actionable (overtime, satisfaction) and which are descriptive (age, tenure).
7. Produce a decile lift table: sort by predicted probability, split into ten groups, and report
   the observed attrition rate per decile. What does the top decile tell HR?
8. Write a 200-word memo: whom to contact, what to change, and what the model cannot tell you.

### Expected results

```text
no class weights : accuracy 0.843  precision 0.538  recall 0.125
balanced weights : accuracy 0.680  precision 0.306  recall 0.786
majority baseline: accuracy ≈ 0.841, recall 0
attrition rate   : 0.159
```

- The balanced model catches roughly six times as many leavers at half the precision.
- Coefficients: overtime positive and large, job satisfaction negative, years at company negative,
  distance positive — the synthetic generator's structure, not a finding about the world.
- Lift is steep at the top: the first decile should show a much higher attrition rate than 16%.

### Evaluation metrics

**Recall at a fixed alert budget** (100 conversations) and **precision at that budget**, with lift
by decile. Accuracy is reported only next to the baseline, and AUC as a secondary ranking measure.

### Deliverables

- The two-model comparison table with cost interpretation.
- The threshold/capacity table and the selected operating point.
- The decile lift table.
- Coefficient interpretation with an explicit "association, not causation" caveat.
- The 200-word memo.

### Extension challenges

1. Compute the expected cost of your operating point for a stated cost of a departure and a cost
   per conversation. Compare with the balanced model.
2. Add interaction terms (`overtime × job_satisfaction`) and test whether CV improves.
3. Build a "reason code" for each flagged employee using the top three contributing features, and
   discuss the ethical risk of acting on them.
4. Remove `job_level` and see whether performance drops. If it does not, discuss whether the
   feature should have been collected at all.
5. Simulate a retention campaign that saves 30% of those contacted. Estimate the number of
   departures avoided at your operating point.

---

## Shared requirements

- **Clustering has no test set.** Use stability and domain validation instead, and say so.
- **Supervised work uses one split**; thresholds are chosen on validation/CV, never on test.
- **Name every cluster and every threshold decision** in business language.
- **No causal claims.** Write the sentence "this is an association in the training data" where it
  belongs.
- **Report counts as well as ratios**: 100 conversations, 23 leavers, not just "recall 0.79".

## Evaluation criteria

| Criterion | Weight | What earns full marks |
| :--- | ---: | :--- |
| Clustering method and validation | 30% | scaling, k justification, stability, profiles |
| Supervised evaluation | 25% | imbalance handled honestly, capacity-aware threshold |
| Interpretation | 25% | segments and coefficients translated into actions |
| Communication | 20% | memo a manager could act on; limitations stated |

## Hints

- `unsupervised.silhouette_score` is O(n²); it is fine at 500 rows, not at 50,000.
- `evaluation.threshold_sweep` gives you precision/recall per threshold; convert to counts by
  multiplying by the test size.
- The GMM's `predict_proba` gives soft membership — use it to find the ambiguous customers.
- For lift, sort by probability descending and cut into ten equal groups with `np.array_split`.

## Reflection

1. Did the silhouette pick the segmentation you would present to marketing? If not, what does that
   say about internal indices?
2. In the attrition problem, which changed the product more: the model or the weight/threshold
   choice?
3. Which of these two analyses would you be more comfortable defending to a sceptical manager, and
   why?

## Time budget

| Task | Time |
| :--- | ---: |
| Scenario 4, tasks 1–5 | 55 min |
| Scenario 4, tasks 6–10 | 35 min |
| Scenario 7, tasks 1–4 | 35 min |
| Scenario 7, tasks 5–8 | 35 min |
| Write-up | 20 min |

Next: [LAB-06-04 — Intrusion, Fraud and the Leakage Hunt](lab-06-04-intrusion-fraud-and-leakage.md).

## Starter material

The guided notebook [`nb-06-03-model-comparison-and-ensembles.ipynb`](../notebooks/nb-06-03-model-comparison-and-ensembles.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
