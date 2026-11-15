# LAB-14-02 — Efficient Serving: Compression, Latency and Drift

| | |
| :--- | :--- |
| Time | 2.5 hours |
| Level | 400 |
| Prerequisites | L14-02, L14-03 |
| Code | `code/efficiency.py`, `code/timeseries_monitor.py` |

[Module home](../README.md) · [Lab 14-01](lab-14-01-multimodal-and-graph-systems.md) · [Rubric](../capstone/rubric.md)

## Purpose

Take a model from "it trains" to "it could be served": compress it, measure the real cost of each
compression, define a latency budget, and build a drift monitor that fires before the error metric
does.

**Deliverable.** A serving note (≤900 words) with the four-column compression table, a latency
budget, and a monitoring plan with thresholds and an owner.

---

## 1. Setup

```bash
cd modules/M14-advanced-ai-applications-and-capstone/code
python efficiency.py          # ~30–60 s on the audit machine
python timeseries_monitor.py  # ~20 s
```

## 2. Part A — Compression, measured honestly (60 minutes)

### A1. The four columns

Record accuracy, size, parameters and latency for all five rows. Then:

- Which row is Pareto-optimal on (accuracy, size)? On (accuracy, latency)?
- Which row would you ship for a 50 MB memory budget and a 20 ms inference budget? Justify.

### A2. Why int8 was slower

In release validation the quantised model was 1.61–2.35× slower than the float student (median
1.68×) and 5.2 KB vs 18.8 KB. An earlier single unrecorded run reported 2.62×; your own ratio will
depend on CPU, thread count, load and whether int8 kernels are available.

- Look at `Int8Linear.forward`. Which operation costs time on every call?
- Precompute the dequantised weight once and cache it. Re-measure. Report the change and explain
  why this is not a fair test of quantisation in general.
- Name two deployment conditions where int8 would be faster.

### A3. Distillation gained nothing

The gain over scratch training is −0.004.

- Why can a teacher add nothing on an easy task?
- Look at the temperature sweep: which setting is worst, and what does over-smoothing the soft
  targets do?
- Construct (in words) a task where distillation would help, and say what you would measure to
  prove it.

### A4. Pruning

50% of weights are zero, size unchanged, latency ratio 0.80–1.30× across release-validation runs
(median 1.01×) — no reliable speed change. An earlier single run reported 1.45× worse.

- Explain why dense arithmetic does not benefit from zero weights.
- What would make pruning pay? Name the structural change.

### A5. Batch throughput

Measure per-example latency at batch sizes 1, 8, 32, 128. Report examples/second for each. At
what batch size does throughput stop improving, and why does per-request latency still rise?

## 3. Part B — Latency budget (30 minutes)

Assume a request budget of 200 ms and a measured inference cost equal to your chosen model's
per-example latency (convert µs to ms).

- Build the budget: network, feature fetch, inference, post-processing, headroom.
- How much headroom is left? If it is negative, what do you cut?
- What is your fallback if inference exceeds the budget at runtime?

Write the budget as a table with a number in every row.

## 4. Part C — Drift monitoring (60 minutes)

### C1. Backtest and coverage

Record MAE, 80% coverage and mean width for the three forecasters.

- Boosting has the narrowest intervals and 0.66 coverage. Why is that worse than wide intervals?
- Which model would you deploy, and what do you tell the stakeholder about its intervals?

### C2. Detection

After a level shift at day 560, the worst PSI is 3.777 at lag 28.

- Why does PSI detect the change before MAE does?
- Which lag would you monitor to catch this shift earliest? Run `drift_report` with a few
  different lags to find out.
- Lower the drift magnitude (change `+18` to `+6`) and re-measure PSI. At what magnitude does it
  fall below the 0.25 alert threshold?

### C3. Retrain or investigate?

MAE after drift: naive +1.58, ridge +1.94, boosting +1.49.

- The best model degrades most. Explain why.
- Write the decision rule you would use in production: what combination of drift and error
  triggers a retrain rather than an investigation?

## 5. Part D — Write the plan (20 minutes)

Complete this table for a model you would actually ship:

| Part | Your answer |
| :--- | :--- |
| Metric | |
| Threshold | |
| Cadence | |
| Owner | |
| Action | |

Then state the one alert you would delete as noise, and why.

## 6. Reflection questions

1. Three compressions, three trades, none free. Which trade would you refuse to make for a
   medical triage model, and which would you accept for a mobile photo filter?
2. The int8 result contradicts a widely repeated claim. What is the general lesson about
   benchmark claims from other people's hardware?
3. Your monitor fires at PSI 3.777 but the error metric lags. What would you do in the first hour
   after the alert, before retraining?
4. State precisely what your serving note does **not** establish about the model in production.

## 7. Marking criteria

| Criterion | Weight | Strong |
| :--- | ---: | :--- |
| Measurement | 30% | all four columns, repeated runs stated |
| Explanation of surprises | 25% | int8 slowdown and null distillation explained mechanistically |
| Latency budget | 20% | every row has a number; fallback defined |
| Monitoring plan | 25% | thresholds justified, owner and action named |

---

[Module home](../README.md) · [Lab 14-01](lab-14-01-multimodal-and-graph-systems.md) ·
[Summary](../summary.md)

## Starter material

A runnable starter is provided: [`starters/lab-14-02_starter.py`](starters/lab-14-02_starter.py).
It loads the lab's data, prints a baseline you can compare against, and
marks the parts left for you with `TODO`. Run it before you write anything.

Module reference code: [`../code/`](../code/).

## Extension challenges (optional)

Optional, and closer to production engineering than the rest of M14.

1. **Latency budget.** Derive the p95 latency budget from a stated user requirement (for
   example 200 ms end to end with 50 ms for the model), then measure whether your serving
   path meets it at the target batch size. Report the gap, not just the mean.
2. **Quantisation sweep.** Compare float32, int8 dynamic and int8 static quantisation on
   accuracy, model size and p95 latency. Which combination would you ship, and what
   monitoring would tell you it had gone wrong?
3. **Rollback drill.** Write the rollback runbook: trigger metric, threshold, who is
   paged, what is reverted, and how you verify the rollback worked. Keep it under one page.
