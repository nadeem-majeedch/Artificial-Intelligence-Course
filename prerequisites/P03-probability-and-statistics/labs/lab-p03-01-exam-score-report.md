# LAB-P03-01 — Exam Score Report

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Effort | 1.5 hours, suggested split: session 1 = tasks 1–3, session 2 = tasks 4–6 |
| Lessons covered | [LP03-01](../lessons/LP03-01-descriptive-statistics.md) … [LP03-06](../lessons/LP03-06-hypothesis-testing-fundamentals.md) |
| Dataset | generated in the lab (fixed seed) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) — support for the simulations |

[← Unit home](../README.md) · [Prerequisites home](../../README.md)

## Scenario

A department ran an optional tutorial before the mid-term. Thirty students attended, thirty did not, and
the tutorial coordinator, Dr. Farhan, wants to know whether it helped. He is under pressure from a
colleague who says "the tutorial group averaged four marks more, so it works" — and from a student
representative who says "the tutorial group was self-selected, so it proves nothing". He needs a report
that takes both objections seriously and states what the data can and cannot support.

## Your role

You are the analyst writing that report. You report to Dr. Farhan and you will be judged on **honesty of
inference**: a conclusion that survives a skeptical reader, with the uncertainty visible.

## What you are given

| Item | Location | Notes |
| :--- | :--- | :--- |
| Scores | generated in Task 1 | two groups of 30, plus attendance percentage |
| Starter code | none | NumPy, pandas, Matplotlib |
| Constraints | — | no SciPy; use the formulas from the lessons |

**Not provided:** the correct answer to "did it work", a p-value, or a confidence interval. You compute
them and then decide what to say.

## Requirements

**Functional**

- R1 — Generate two groups of 30 scores, the tutorial group with a mean about 4 marks higher, and an
  attendance percentage correlated with score.
- R2 — Report per group: count, mean, median, standard deviation and IQR.
- R3 — Build a 95% confidence interval for each group mean using the standard error, and state the
  margin of error in marks.
- R4 — Compute the standardised effect size between groups and a permutation p-value for the difference
  in means.
- R5 — Report the correlation between attendance and score with a scatter plot, and say what it implies
  about the self-selection objection.

**Non-functional**

- N1 — Runs in under 10 seconds, including 10 000 permutations.
- N2 — Fixed seed, identical output on every run.
- N3 — Every number in the report is printed by the code.

## Tasks

1. **Generate.** Draw the control group from $\mathcal{N}(62, 8)$ and the tutorial group from
   $\mathcal{N}(66, 8)$, rounded to one decimal, with a fixed seed. *(success: `df.groupby("group").size()`
   is 30 and 30)*
2. **Describe.** Print the five-number-style summary per group and draw overlaid histograms with 10 bins.
   *(success: you can say which group is more variable, not only which is higher)*
3. **Quantify uncertainty.** Compute each mean's standard error and 95% interval, and report both
   intervals in marks. *(success: the intervals are roughly one mark wide on each side)*
4. **Test.** Run a two-sample permutation test on the difference in means with 10 000 shuffles, and
   compute Cohen's $d$. *(success: p-value and effect size both reported, with the direction stated)*
5. **Address self-selection.** Plot attendance against score and report $r$; then explain in three
   sentences why a correlation between attendance and score weakens the causal claim. *(success: the
   explanation names a plausible confounder rather than repeating "correlation is not causation")*
6. **Recommend.** Write five sentences to Dr. Farhan: the estimated gain, its uncertainty, whether the
   evidence supports running the tutorial again, and what would settle the question properly.

## Deliverables

| File | Contents |
| :--- | :--- |
| `lab_p03_01.py` | Runnable script implementing R1–R5 |
| `groups.png` | Overlaid histograms and a boxplot of the two groups |
| `attendance.png` | Scatter of attendance against score, with $r$ in the title |
| `report.md` | ≤ 500 words: summary table, intervals, test result, causal caveat, recommendation |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Correct statistics | 35% | Intervals, effect size and p-value all correct and consistent | One computed with a slip | Several wrong or missing |
| Interpretation | 30% | Distinguishes evidence for a difference from evidence for a cause | Reports result without caveat | Over-claims |
| Visualisation | 20% | Plots labelled, show spread not just means | Labelled, minimal | Unlabelled or misleading |
| Communication | 15% | Recommendation is actionable and hedged appropriately | Understandable | No recommendation |

## Extension challenges

1. **Power.** Simulate the experiment 500 times with the same effect and report the fraction of runs
   where p < 0.05. What does that say about a single study of this size?
2. **Unequal variance.** Regenerate the tutorial group with standard deviation 14 and repeat the test.
   Does the conclusion change?
3. **Bayesian view.** Treat the difference as a normal posterior with a flat prior and report a 95%
   credible interval; compare it with the frequentist interval.

## Hints

<details><summary>Hint 1 — getting started</summary>

Compute the difference in means once, then build the permutation loop around a single pooled array. The
observed difference never changes inside the loop; only the labels do.

</details>

<details><summary>Hint 2 — the likely sticking point</summary>

The confidence interval uses the standard error $s/\sqrt{n}$, not the standard deviation — with $n = 30$
they differ by a factor of about 5.5, which is exactly the size of the mistake that makes an interval
look far tighter than the data support.

</details>

<details><summary>Hint 3 — checking your work</summary>

The permutation p-value should be close to what the $t$ statistic suggests; if the two disagree wildly,
check whether you shuffled the pooled values or only one group, and whether the test was one- or
two-sided.

</details>

## Reflection

1. The colleague says "four marks more, so it works". What is missing from that sentence?
2. What design would let the department answer the causal question properly, and what would it cost?
3. If the p-value were 0.06 rather than 0.03, what would you write to Dr. Farhan — and why is that not
   the same as "no effect"?

## Time budget

| Session | Tasks | Time |
| :--- | :--- | ---: |
| 1 | 1–3 | 45 min |
| 2 | 4–6 | 45 min |
