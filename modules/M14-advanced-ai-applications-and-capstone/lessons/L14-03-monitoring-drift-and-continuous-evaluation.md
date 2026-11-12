# L14-03 — Monitoring, Drift and Continuous Evaluation

| | |
| :--- | :--- |
| Level | 400 |
| Study time | 90 minutes |
| Prerequisites | L14-02, M06 (metrics), M13 (monitoring) |
| Code | `code/timeseries_monitor.py` |

[← Previous: L14-02 From Model to Product: Serving, Compression and MLOps](L14-02-from-model-to-product-mlops-and-serving.md) · [Module home](../README.md) · [Next: L14-04 Reading and Reproducing AI Research →](L14-04-reading-and-reproducing-ai-research.md)

## Why this lesson exists

A model is a snapshot of a relationship that keeps moving. Prices shift, user behaviour changes,
a supplier renames a product, a pandemic changes everything. None of those events raises an
exception; the model simply gets worse, quietly, while every test still passes.

This lesson uses forecasting as the concrete case because time is explicit there: you can
backtest honestly, watch a series drift, and see the error move after the inputs do. The
discipline transfers to any monitored model.

## What you will be able to do

1. Backtest a forecaster with rolling origins and report error with interval coverage.
2. Choose a baseline that a complex model must beat.
3. Compute a population stability index and set alert thresholds.
4. Explain why input drift is detectable before output error is.
5. Write a monitoring plan with metrics, thresholds, cadence and an owner.

---

## 1. Time-series intelligence

Three properties separate time series from ordinary tabular problems:

- **Order matters.** A random split leaks the future into the training set and inflates every
  metric. Split by time, always.
- **The target is autocorrelated**, so a naive "predict the last value" baseline is strong. Any
  model that cannot beat it is not adding value.
- **Stationarity is an assumption, not a fact.** Trends and seasonality that persist in training
  can change in deployment, and that is exactly what drift monitoring is for.

### Baselines, in increasing order of effort

| Baseline | Rule | Why it is the right first comparison |
| :--- | :--- | :--- |
| Last value | $\hat y_{t+1}=y_t$ | cheapest, strong for random walks |
| Seasonal naive | $\hat y_{t+h}=y_{t+h-7}$ | captures weekly structure with no fitting |
| Moving average | mean of last $k$ | smooths noise, lags turning points |
| Linear on lags | ridge regression | captures autocorrelation and trend |
| Nonlinear on lags | gradient boosting | captures interactions, overfits more |

### Measured: 8 rolling origins, 14-day horizon

`timeseries_monitor.py` builds 760 days with trend, weekly and yearly seasonality, then
backtests:

```text
model                MAE   80% coverage  mean width
seasonal naive      4.78           0.85       17.82
ridge               3.79           0.84       13.81
boosting            4.27           0.66       11.16
```

Three results worth keeping:

1. **The linear model wins.** Ridge on 28 lags beats gradient boosting (3.79 vs 4.27). With a
   mostly additive generating process, the extra flexibility buys variance, not signal. Always
   run the simple model.
2. **Coverage is a separate claim from accuracy.** Boosting has the narrowest intervals (11.16)
   and the worst coverage (0.66): its 80% intervals contain the truth two-thirds of the time, not
   80%. An interval that is too narrow is worse than no interval, because people act on it.
3. **Seasonal naive is not a straw man.** MAE 4.78 with correct coverage (0.85) is a real
   baseline; the ridge gain is 21%, not an order of magnitude.

**Interval coverage** is the metric most often omitted and most often wrong:

$$
\text{coverage}=\frac1n\sum_t \mathbb 1\{y_t \in [\ell_t,u_t]\}.
$$

A nominal 80% interval that covers 66% of outcomes is mis-specified, and the fix is usually a
residual distribution computed out-of-sample rather than in-sample.

## 2. Drift

**Drift** is a change in the joint distribution $P(X,y)$; **covariate shift** is a change in
$P(X)$ alone; **concept drift** is a change in $P(y\mid X)$. They need different responses:

| Change | Detected by | Response |
| :--- | :--- | :--- |
| Covariate shift | input distribution monitors | investigate the data source; often retrain |
| Concept drift | error against labels, when they arrive | relabel, retrain, or change the model |
| Label shift | base-rate monitor | recalibrate thresholds |

The practical problem is that labels arrive late — often weeks later, sometimes never. By the
time the error metric moves, users have been affected for a while. **Input monitoring is the
early-warning system; output monitoring is the confirmation.**

### Population stability index

PSI compares the distribution of a feature in a reference sample with a current sample, over
bins:

$$
\text{PSI}=\sum_{b}\left(q_b-p_b\right)\ln\frac{q_b}{p_b},
$$

where $p_b$ and $q_b$ are the bin proportions. Conventional reading: below 0.10 stable,
0.10–0.25 worth watching, above 0.25 alert. The thresholds are conventions, not laws — set them
from your own false-alarm rate.

Measured on this series, after a deliberate level shift at day 560:

```text
after the level shift  worst PSI  3.777 at lag 28  -> alert
```

3.777 is far past 0.25, as it should be for an 18-point level change in a series with standard
deviation around 4. The monitor fires immediately; the error metric takes a full window to move.

### What the error metric does after the drift

```text
model             MAE before  MAE after   change
seasonal naive          4.63       6.21    +1.58
ridge                   3.54       5.48    +1.94
boosting                4.13       5.62    +1.49
```

Every model degrades; the best model degrades most in absolute terms (+1.94), because it was
fitted most tightly to the old distribution. This is the argument for retraining as a *response*
to evidence rather than a schedule: the drift monitor says the inputs changed, the error metric
says it matters, and only then is retraining justified.

Retraining on a schedule has a specific failure mode: it hides drift. A model retrained every
night on drifted data will look fine and will have silently accepted the new regime.

## 3. Continuous evaluation

Monitoring is not a dashboard. A monitoring system is complete only when it has all five parts:

| Part | Question | Example |
| :--- | :--- | :--- |
| Metric | what is measured? | PSI per feature, rolling MAE, coverage |
| Threshold | when is it a problem? | PSI > 0.25, MAE 20% above baseline |
| Cadence | how often? | hourly features, weekly drift, monthly review |
| Owner | who is paged? | named role, not a team |
| Action | what happens? | rollback, retrain, investigate the source |

Missing the last two is the common failure: alerts that nobody owns and no one acts on become
noise, and then they are muted.

### Metrics by model type

| Model type | Leading indicator | Lagging indicator |
| :--- | :--- | :--- |
| Tabular classifier | feature PSI, missingness, subgroup selection rate | accuracy, calibration by group |
| Forecaster | residual autocorrelation, interval coverage | MAE/MAPE on realised values |
| Recommender | catalogue coverage, embedding drift | click-through, retention |
| LLM application | prompt length, retrieval hit rate, refusal rate | groundedness, task success, cost per request |
| Vision | image brightness/blur statistics, class prior | per-class accuracy on labelled sample |

The leading indicator is the one you can compute today. Invest there.

## 4. A monitoring plan you can defend

```text
Model: daily demand forecaster v3.2
Leading: PSI on 28 lag features, daily; alert >0.25 on any feature, >0.10 on three
Lagging: rolling 14-day MAE against seasonal-naive baseline, weekly
Quality: 80% interval coverage, monthly (target 0.80 +/- 0.05)
Owner: demand planning lead; paged by the on-call data engineer
Action: PSI alert -> check upstream feeds; MAE breach -> shadow a retrained model
Review: monthly, with the drift and error series plotted together
```

Note that the action distinguishes between "the data changed" and "the model got worse". Those
are different findings and they lead to different fixes.

## Common mistakes

| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Random train/test split on time series | leaks the future, inflated metrics | split by time |
| No naive baseline | complexity unjustified | report seasonal naive first |
| Intervals without coverage measurement | false confidence | report coverage and width |
| Only monitoring output error | late detection | monitor inputs too |
| Retraining on a schedule | silently accepts drift | retrain on evidence |
| Alerts with no owner | muted within a month | name the owner and the action |

## Exercises

**Beginner.** Run `python timeseries_monitor.py`. Copy the backtest table and say which model you
would deploy, with the coverage caveat stated.

**Beginner.** Change `HORIZON` to 7 and 28 and rerun. How does the ranking and the coverage
change as the horizon grows?

**Intermediate.** Replace the in-sample residual quantiles with out-of-sample ones from the
previous fold, and report the coverage change. Does boosting improve?

**Intermediate.** Add a second drift event (a weekly-seasonality change) and report which PSI
feature detects it first. Is it the same feature as the level shift?

**Advanced.** Implement a simple concept-drift detector (e.g. Page–Hinkley on residuals) and
compare its detection delay with the PSI monitor on the same stream.

**Advanced.** Design the monitoring plan for one of the capstone briefs in
[`capstone/briefs/`](../capstone/briefs/), including thresholds you can justify.

## Self-check

1. Why does a random split inflate time-series metrics?
2. What does interval coverage measure that MAE does not?
3. Give one reason input drift is detectable earlier than output error.
4. What are the five parts of a complete monitoring system?
5. Why can scheduled retraining hide drift?

## Key terms

**Rolling-origin backtest**, **seasonal naive**, **prediction interval**, **coverage**,
**covariate shift**, **concept drift**, **label shift**, **PSI**, **leading indicator**,
**lagging indicator**, **retraining trigger**, **shadow deployment**.

## Further reading

- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice* — backtesting and intervals.
- Gama et al. (2014). *A Survey on Concept Drift Adaptation*.
- Sculley et al. (2015). *Hidden Technical Debt in Machine Learning Systems*.
- NannyML and Evidently documentation — open-source drift tooling worth reading for metric
  definitions.

---

[Previous: L14-02](L14-02-from-model-to-product-mlops-and-serving.md) · [Module home](../README.md) ·

---

**Navigation:** [← Previous: L14-02 From Model to Product: Serving, Compression and MLOps](L14-02-from-model-to-product-mlops-and-serving.md) · [Module home](../README.md) · [Next: L14-04 Reading and Reproducing AI Research →](L14-04-reading-and-reproducing-ai-research.md)
