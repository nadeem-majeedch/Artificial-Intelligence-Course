# LP03-05 — Sampling, Covariance and Correlation

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Study time | 60 minutes |
| Prerequisites | [LP03-04](LP03-04-random-variables-and-distributions.md) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) |
| Lab | [LAB-P03-01](../labs/lab-p03-01-exam-score-report.md) |

[← Previous: Random Variables](LP03-04-random-variables-and-distributions.md) · [P03 home](../README.md) · [Next: Hypothesis Testing →](LP03-06-hypothesis-testing-fundamentals.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Explain** why a sample mean is itself a random variable, and compute its standard error.
- **Describe** the central limit theorem and use it to build a confidence interval.
- **Compute** covariance and correlation, and interpret the sign, magnitude and limitations of $r$.
- **Identify** the sampling biases that make a large sample useless.

## 2. Prerequisite Knowledge

- Expectation, variance and the normal distribution: [LP03-04](LP03-04-random-variables-and-distributions.md).

## 3. Conceptual Explanation

### 3.1 Population and sample

The **population** is everything you care about; the **sample** is what you measured. A statistic is a
number computed from the sample (e.g. $\bar{x}$); a parameter is the corresponding unknown population
quantity (e.g. $\mu$). Every inference in this unit is an attempt to say something about the parameter
using the statistic.

### 3.2 How you sample changes everything

| Method | How it works | Failure mode |
| :--- | :--- | :--- |
| Simple random | Every unit equally likely | Needs a complete list of the population |
| Stratified | Sample within subgroups, then combine | Weights must match population shares |
| Systematic | Every $k$-th unit | Periodicity in the list can alias |
| Convenience | Whoever is available | Systematic bias, regardless of size |

Bias does not shrink with $n$. A million voluntary online responses can be further from the truth than
a well-drawn sample of a thousand — this is the single most important sentence in the lesson.

### 3.3 The sampling distribution and standard error

Draw a sample of size $n$, compute $\bar{x}$; repeat. Those means have their own distribution, with

$$
\mathbb{E}[\bar{X}] = \mu,
\qquad
\operatorname{SE}(\bar{X}) = \frac{\sigma}{\sqrt{n}}
\approx \frac{s}{\sqrt{n}}
$$

The $\sqrt{n}$ is the reason precision improves slowly: to halve the standard error you need **four
times** the data. This is why "just collect more" has diminishing returns, and why a study with
$n = 10\,000$ is only about three times more precise than one with $n = 1\,000$.

### 3.4 Central limit theorem

For independent observations with finite variance, the distribution of $\bar{X}$ approaches a normal
with mean $\mu$ and standard error $\sigma/\sqrt{n}$ as $n$ grows — *whatever* the shape of the original
distribution. In practice $n \ge 30$ is usually enough for moderately skewed data; heavily skewed data
needs more.

This is the theorem that licenses the confidence interval:

$$
\bar{x} \pm z_{1-\alpha/2}\,\frac{s}{\sqrt{n}}
\approx \bar{x} \pm 1.96\,\frac{s}{\sqrt{n}}
\quad \text{for } 95\%
$$

Interpretation, stated carefully: if we repeated the whole procedure many times, about 95% of the
intervals so constructed would contain $\mu$. It is a statement about the procedure, not a 95% chance
that this particular interval contains $\mu$.

### 3.5 Covariance and correlation

$$
\operatorname{Cov}(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y}),
\qquad
r = \frac{\operatorname{Cov}(X,Y)}{s_x s_y}
$$

Covariance's sign says whether the variables move together, but its magnitude depends on units — a
covariance in "marks × minutes" is not comparable with one in "metres × kilograms". Dividing by both
standard deviations removes the units, giving the Pearson correlation $r \in [-1, 1]$.

What $r$ does and does not say:

- $r = 0$ means no **linear** association; a strong curved relationship can still have $r \approx 0$.
- $r$ is sensitive to outliers, because it is built from squared deviations.
- Correlation is not causation: a third variable can drive both, and the direction of influence can be
  reversed.

## 4. Worked Examples

### Example 1 — covariance and correlation by hand

$x = (1, 2, 3, 4)$, $y = (2, 4, 5, 4)$. Means: $\bar{x} = 2.5$, $\bar{y} = 3.75$.

| $x_i$ | $y_i$ | $x_i - \bar{x}$ | $y_i - \bar{y}$ | product |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | $-1.5$ | $-1.75$ | $2.625$ |
| 2 | 4 | $-0.5$ | $0.25$ | $-0.125$ |
| 3 | 5 | $0.5$ | $1.25$ | $0.625$ |
| 4 | 4 | $1.5$ | $0.25$ | $0.375$ |

Sum of products $= 3.5$, so $\operatorname{Cov} = 3.5/3 \approx 1.167$.

$s_x^2 = 5/3 \approx 1.667 \Rightarrow s_x \approx 1.291$;
$s_y^2 = 4.75/3 \approx 1.583 \Rightarrow s_y \approx 1.258$.

$$
r = \frac{1.167}{1.291 \times 1.258} \approx 0.718
$$

```python
import numpy as np

x = np.array([1, 2, 3, 4], dtype=float)
y = np.array([2, 4, 5, 4], dtype=float)
print(np.cov(x, y, ddof=1)[0, 1].round(3))
print(np.corrcoef(x, y)[0, 1].round(3))
```

```text
1.167
0.718
```

A moderately strong positive linear relationship — but with four points, treat the number as a hint, not
a finding.

### Example 2 — standard error and a confidence interval

A sample of $n = 100$ scores has mean 68 and standard deviation 9.

$$
\operatorname{SE} = \frac{9}{\sqrt{100}} = 0.9,
\qquad
95\%\ \text{CI} = 68 \pm 1.96(0.9) = (66.24,\ 69.76)
$$

```python
from math import sqrt

n, mean, s = 100, 68, 9
se = s / sqrt(n)
print(round(se, 3), (round(mean - 1.96 * se, 2), round(mean + 1.96 * se, 2)))
```

```text
0.9 (66.24, 69.76)
```

A margin of error under two marks from a hundred observations is the kind of precision that makes a
survey worth running; note it came from $\sqrt{100} = 10$, not from a clever formula.

### Example 3 — the central limit theorem, demonstrated

```python
import numpy as np

rng = np.random.default_rng(seed=3)
means = [rng.exponential(scale=2.0, size=40).mean() for _ in range(2000)]
print(round(float(np.mean(means)), 3), round(float(np.std(means, ddof=1)), 3))
```

```text
2.004 0.318
```

The exponential distribution is strongly right-skewed, yet the 2 000 sample means are symmetric around
2.004 with a spread of 0.318 — close to the theoretical $\sigma/\sqrt{n} = 2/\sqrt{40} \approx 0.316$.
That is the central limit theorem doing its work.

## 5. Visual Explanation

```text
  population (skewed)          distribution of x̄ (n=40)
     ██                              ▄▆█▆▄
     ███                           ▄███████▄
     ████                        ▄███████████▄
  ───┴─────── x                ──────┴─────── x̄
   wide, asymmetric            narrower, symmetric, centred on μ
```

*Text description of the diagram:* averaging compresses the horizontal axis by $\sqrt{n}$ and, by the
central limit theorem, symmetrises the shape. The population's long right tail does not survive
averaging: the sample mean's distribution is symmetric even though the data are not.

## 6. Mathematical Formulation

$$
\operatorname{SE}(\bar{X}) = \frac{\sigma}{\sqrt{n}},
\qquad
\operatorname{Cov}(X,Y) = \frac{1}{n-1}\sum_i (x_i-\bar{x})(y_i-\bar{y})
$$

$$
r = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i (x_i-\bar{x})^2}\sqrt{\sum_i (y_i-\bar{y})^2}},
\qquad -1 \le r \le 1
$$

An identity worth knowing: $r$ is the covariance of the **standardised** variables,

$$
r = \frac{1}{n-1}\sum_i z^x_i z^y_i
$$

so correlation is an average product of $z$-scores. That is why $|r| \le 1$: each product is at most 1
in magnitude in a specific sense, and the average cannot exceed it.

## 7. Python Implementation

```python
"""Sampling behaviour: watch the standard error shrink as sqrt(n)."""
import numpy as np

rng = np.random.default_rng(seed=11)

print(" n    mean of means   SE observed   SE predicted")
for n in (10, 40, 160, 640):
    means = rng.normal(loc=50, scale=12, size=(500, n)).mean(axis=1)
    print(f"{n:>4} {means.mean():>12.3f} {means.std(ddof=1):>13.3f} {12 / np.sqrt(n):>14.3f}")

X = rng.normal(size=500)
Y = 0.6 * X + rng.normal(scale=0.8, size=500)
print("\ncorr(X, Y) =", round(float(np.corrcoef(X, Y)[0, 1]), 3))
```

**Output**

```text
 n    mean of means   SE observed   SE predicted
  10       50.098         3.936          3.795
  40       49.997         1.900          1.897
 160       49.984         0.989          0.949
 640       50.005         0.475          0.474

corr(X, Y) = 0.594
```

Predicted and observed agree to within sampling noise at every size, and quadrupling $n$ halves the
spread each time — the $\sqrt{n}$ law, visible in a table. The correlation of 0.594 is the population
value $0.6/\sqrt{0.6^2 + 0.8^2} = 0.6$ up to sampling error, which is a reminder that $r$ from 500
points still wobbles in the second decimal.

## 8. Practical Applications

- **Model evaluation.** A test-set accuracy is a sample mean; its standard error tells you whether the
  difference between two models is real or noise. Reporting accuracy without it is reporting a number
  without its uncertainty.
- **Feature selection.** Correlation matrices are the first thing to inspect before modelling, both to
  find useful signal and to spot near-duplicate features that destabilise linear models.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Treating a convenience sample as representative | Confident, wrong conclusions | Selection bias | Describe the sampling frame |
| Reading $r = 0$ as independence | Missed relationship | Only linear association measured | Plot the data |
| Comparing covariances across units | Meaningless ranking | Units are inside the number | Use correlation |
| Interpreting a CI as a probability for $\mu$ | "95% chance $\mu$ is here" | Frequentist interval is about the procedure | State the repeated-sampling meaning |

## 10. Self-Assessment

**1.** A sample of 400 has standard deviation 20. What is the standard error of the mean?
<details><summary>Show answer</summary>

$20/\sqrt{400} = 20/20 = 1.0$. To halve it to 0.5 you would need $n = 1600$.
</details>

**2.** $r = -0.85$ between study hours and error rate. Describe the relationship and one thing it does
not prove.
<details><summary>Show answer</summary>

A strong negative linear association: more study hours are associated with lower error. It does not
prove that studying causes the reduction — a third factor (prior knowledge, motivation) could drive
both.
</details>

**3.** Why can a huge sample still give a badly wrong estimate?
<details><summary>Show answer</summary>

Because bias is not reduced by sample size. If the sampling procedure systematically excludes part of
the population, more data just estimates the wrong quantity more precisely.
</details>

**4.** Data have $r = 0.02$ but the scatter plot shows a clear U-shape. What happened?
<details><summary>Show answer</summary>

Correlation measures only linear association. A symmetric curve has positive products on one side and
negative on the other, which cancel to near zero. Always plot before trusting a single coefficient.
</details>

## 11. Further Reading

- [Seeing Theory, Ch. 5: Sampling](https://seeing-theory.brown.edu/frequentist-inference/index.html) — the sampling distribution, interactively.
- [The Datasaurus Dozen](https://www.autodesk.com/research/publications/same-stats-different-graphs) — twelve datasets with identical summary statistics and very different shapes; the definitive argument for plotting.

## Mini-Lab

Generate a population of 10 000 values from a lognormal distribution with `np.random.default_rng(seed=5)`.
Draw 500 samples of size 30, record each mean, and plot the histogram of means alongside the population
histogram. Report the observed standard deviation of the means and compare it with $s/\sqrt{30}$.
Then repeat with a deliberately biased "sample": only the largest 30% of the population. How far is the
mean of that sample from the true mean?

## What to Do Next

Continue to [LP03-06 Hypothesis Testing Fundamentals](LP03-06-hypothesis-testing-fundamentals.md).
