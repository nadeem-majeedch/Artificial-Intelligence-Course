# LP03-06 — Hypothesis Testing Fundamentals

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Study time | 60 minutes |
| Prerequisites | [LP03-05](LP03-05-sampling-correlation-and-covariance.md) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) |
| Lab | [LAB-P03-01](../labs/lab-p03-01-exam-score-report.md) |

[← Previous: Sampling and Correlation](LP03-05-sampling-correlation-and-covariance.md) · [P03 home](../README.md) · [Next: Data Preparation and Visualisation →](../../P04-data-preparation-and-visualization/README.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **State** a null and alternative hypothesis, and choose a one- or two-sided test deliberately.
- **Compute** a test statistic and compare it with a critical value, or interpret a p-value correctly.
- **Distinguish** Type I from Type II error, and explain what statistical power is.
- **Report** an effect size alongside a p-value, and explain why "significant" is not "important".

## 2. Prerequisite Knowledge

- Sampling distributions, standard error and confidence intervals:
  [LP03-05](LP03-05-sampling-correlation-and-covariance.md).

## 3. Conceptual Explanation

### 3.1 The logic of a significance test

1. **State $H_0$** — the boring hypothesis: no effect, no difference, $\mu = 68$.
2. **State $H_1$** — what you would report if $H_0$ fails: $\mu \ne 68$, $\mu > 68$, etc.
3. **Choose $\alpha$** — the false-positive rate you are willing to accept, usually 0.05.
4. **Compute a statistic** from the data and see how far it is from what $H_0$ predicts.
5. **Decide**: if the statistic is more extreme than the critical value, reject $H_0$.

The logic is **proof by contradiction with uncertainty**: assume $H_0$, show the data would be unlikely,
and conclude $H_0$ is a poor explanation — never that it is proven false.

### 3.2 The one-sample t statistic

$$
t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}
$$

The numerator is the observed effect; the denominator is the standard error. So $t$ is "the effect
measured in units of its own noise" — a signal-to-noise ratio. That is why the same formula works for
almost every test you will meet: only the standard error changes.

Compare $|t|$ with a critical value from the $t$ distribution with $n-1$ degrees of freedom, or compute
the p-value.

### 3.3 What a p-value is, and is not

> The p-value is the probability of observing data at least as extreme as ours, **assuming $H_0$ is
> true**.

It is **not** the probability that $H_0$ is true, and $1 - p$ is **not** the probability that your
hypothesis is right. A small p-value says: this data would be surprising under the null. That is all.

Two-sided tests are the default because a surprise in either direction is worth reporting; one-sided
tests must be justified before looking at the data, not after.

### 3.4 Errors, power and effect size

| | $H_0$ true | $H_0$ false |
| :--- | :--- | :--- |
| **Reject $H_0$** | Type I error ($\alpha$) | Correct (power $= 1-\beta$) |
| **Fail to reject** | Correct | Type II error ($\beta$) |

Lowering $\alpha$ reduces false positives but raises false negatives. Power grows with larger $n$,
larger effects, and less noise — which is why underpowered studies produce a literature of exaggerated
findings.

**Effect size** answers a different question: how big is the difference, in meaningful units? Cohen's
$d = (\bar{x} - \mu_0)/s$ is the standard version. With $n = 10\,000$, a difference of 0.1 marks can be
"highly significant" and completely irrelevant; with $n = 12$, a difference of 10 marks can fail to
reach significance. Report both.

## 4. Worked Examples

### Example 1 — one-sample test by hand

A class of $n = 25$ scores has mean 71 and standard deviation 8. The historical average is 68. Is the
class different?

$$
t = \frac{71 - 68}{8/\sqrt{25}} = \frac{3}{1.6} = 1.875
$$

With $df = 24$, the two-sided critical value at $\alpha = 0.05$ is about 2.064. Since
$1.875 < 2.064$, we **fail to reject** $H_0$. The corresponding p-value is about 0.073 — suggestive, but
not below 0.05.

Effect size: $d = 3/8 = 0.375$, a small-to-moderate difference. Both statements belong in the report:
"not statistically significant at the 5% level, with a small-to-moderate effect; a larger sample would
be needed to decide."

### Example 2 — the same effect with more data

If the same mean and standard deviation came from $n = 100$:

$$
t = \frac{3}{8/10} = 3.75, \qquad df = 99
$$

The critical value is about 1.984, so now we reject $H_0$ (p ≈ 0.0003). Nothing about the class changed
— only the amount of evidence. This is the clearest demonstration that "significant" is a statement
about evidence, not about importance.

### Example 3 — a paired permutation test, which needs no distributional formula

Eight students are measured before and after a workshop. Under $H_0$ the workshop does nothing, so each
difference is equally likely to have either sign. Flipping random signs therefore generates the null
distribution directly.

```python
import numpy as np

before = np.array([62, 58, 71, 65, 60, 67, 55, 70])
after = np.array([68, 61, 74, 66, 66, 70, 58, 73])
diff = after - before
observed = diff.mean()

rng = np.random.default_rng(seed=0)
count = 0
for _ in range(10_000):
    signs = rng.choice([-1, 1], size=diff.size)
    if abs((signs * diff).mean()) >= abs(observed):
        count += 1

print(round(float(observed), 3), round(count / 10_000, 4))
```

```text
3.5 0.008
```

The mean gain is 3.5 marks, and only 0.8% of sign-flipped versions are that large — stronger evidence
than the conventional threshold. Note the pairing: every student is compared with themselves, so the
large between-student variation drops out. Treating the two groups as independent instead would ignore
that pairing and lose most of the signal.

## 5. Visual Explanation

```text
        null distribution of t (df = 24)
                    ▄▆█▆▄
                 ▄███████▄
              ▄█████████████▄
        ────┬──────┬──────┬────┴────
          -2.064   0   +2.064
              ▲            ▲
        reject │            │ reject
                       t = 1.875  ← observed, inside: fail to reject
```

*Text description of the diagram:* the curve is what $t$ would look like if $H_0$ were true. The shaded
tails beyond $\pm 2.064$ together hold 5% of the area. Our observed 1.875 sits inside the middle region,
so it is not unusual enough to reject — even though it is on the side we expected.

## 6. Mathematical Formulation

$$
t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}, \qquad df = n - 1
$$

For two independent samples (Welch's version, the safe default):

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}}}
$$

Effect size and the relation to power:

$$
d = \frac{\bar{x} - \mu_0}{s},
\qquad
\text{power} \approx \Phi\!\left(\frac{|d|\sqrt{n}}{2} - z_{1-\alpha}\right)
\quad \text{(rough)}
$$

The second formula is approximate but revealing: power depends on $|d|\sqrt{n}$, so doubling the effect
size is equivalent to quadrupling the sample. Design a study around the effect you care about, then
compute the $n$ you need — not the other way round.

## 7. Python Implementation

```python
"""A t statistic plus a bootstrap confidence interval for the mean difference."""
import numpy as np

before = np.array([62, 58, 71, 65, 60, 67, 55, 70])
after = np.array([68, 61, 74, 66, 66, 70, 58, 73])

diff = after - before
n = diff.size
t_stat = diff.mean() / (diff.std(ddof=1) / np.sqrt(n))
d_effect = diff.mean() / diff.std(ddof=1)
print(f"mean gain = {diff.mean():.2f}, t({n-1}) = {t_stat:.3f}, d = {d_effect:.2f}")

rng = np.random.default_rng(seed=1)
boots = [rng.choice(diff, size=n, replace=True).mean() for _ in range(5000)]
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"95% bootstrap CI for the gain: ({lo:.2f}, {hi:.2f})")
```

**Output**

```text
mean gain = 3.50, t(7) = 5.857, d = 2.07
95% bootstrap CI for the gain: (2.50, 4.62)
```

$t = 5.857$ is far beyond the two-sided critical value of 2.365 at $df = 7$, and the bootstrap interval
lies entirely above zero — three different procedures agreeing, which is what a robust finding looks
like. The effect size $d = 2.07$ says the gain is about two standard deviations of the individual
differences: large, but with only eight students the interval is still wide, from 2.5 to 4.6 marks.

## 8. Practical Applications

- **A/B testing.** Comparing two variants is a two-sample test; the effect size and confidence interval
  matter more than the p-value, because a launch decision depends on how large the gain is.
- **Model comparison.** Reporting that model A beats model B requires a test over paired folds or
  seeds; without it, a 0.3% difference is indistinguishable from noise.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Reading $p$ as $P(H_0)$ | "There is a 5% chance the null is true" | Misreading the conditional | $p$ conditions on $H_0$, not the reverse |
| Testing many hypotheses at $\alpha = 0.05$ | One "significant" result in 20 | Multiple comparisons | Correct, or pre-register |
| Choosing a one-sided test after seeing the data | Convenient significance | Post-hoc direction | Decide the test in advance |
| Reporting significance without size | Trivial differences called findings | $n$ inflates significance | Report effect size and CI |

## 10. Self-Assessment

**1.** $n = 36$, $\bar{x} = 52$, $s = 6$, $H_0: \mu = 50$. Compute $t$.
<details><summary>Show answer</summary>

$t = (52-50)/(6/6) = 2/1 = 2.0$ with $df = 35$. The two-sided 5% critical value is about 2.03, so this
is borderline — a good reminder to report the interval as well as the verdict.
</details>

**2.** What does a p-value of 0.03 mean, in one sentence?
<details><summary>Show answer</summary>

If the null hypothesis were true, data at least as extreme as ours would occur about 3% of the time. It
is a statement about the data given the hypothesis, not about the hypothesis given the data.
</details>

**3.** You lower $\alpha$ from 0.05 to 0.01. What happens to Type I and Type II error rates?
<details><summary>Show answer</summary>

Type I error falls to 1%, but Type II error rises — the test becomes more conservative, so real effects
are missed more often unless the sample grows.
</details>

**4.** A study with 50 000 users finds a 0.2% improvement, p < 0.001. What else must be reported?
<details><summary>Show answer</summary>

The effect size and a confidence interval. A 0.2% gain may be statistically detectable yet commercially
irrelevant, and the interval shows how precisely it was estimated.
</details>

## 11. Further Reading

- [OpenStax Introductory Statistics 2e, Ch. 9](https://openstax.org/books/introductory-statistics-2e/pages/9-introduction) — hypothesis testing with worked examples.
- [ASA Statement on p-Values (2016)](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108) — the six principles every reader of results should know.

## Mini-Lab

Take two groups of 15 measurements each (generate them with `np.random.default_rng(seed=9)`, means 60
and 63, standard deviation 8). Run a permutation test for the difference in means, and compute the
standardised effect size. Then repeat the whole experiment with 150 per group and record how the
p-value and the effect size changed. Which one moved, and why?

## What to Do Next

P03 is complete. Continue to [P04 Data Preparation and Visualisation](../../P04-data-preparation-and-visualization/README.md),
then take the [diagnostic](../../diagnostic.md).
