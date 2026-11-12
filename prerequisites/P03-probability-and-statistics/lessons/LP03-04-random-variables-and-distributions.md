# LP03-04 — Random Variables and Distributions

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Study time | 75 minutes |
| Prerequisites | [LP03-03](LP03-03-bayes-theorem.md) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) |
| Lab | [LAB-P03-01](../labs/lab-p03-01-exam-score-report.md) |

[← Previous: Bayes' Theorem](LP03-03-bayes-theorem.md) · [P03 home](../README.md) · [Next: Sampling and Correlation →](LP03-05-sampling-correlation-and-covariance.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Distinguish** discrete from continuous random variables, and PMF from PDF.
- **Compute** expectation and variance from a small probability table.
- **Use** the binomial formula for a count of successes, and state its assumptions.
- **Convert** any normal variable to a standard normal, and use the empirical rule to answer questions.

## 2. Prerequisite Knowledge

- Probability rules and conditional probability: [LP03-02](LP03-02-probability-rules-and-conditional-probability.md).
- Descriptive statistics, especially mean and variance: [LP03-01](LP03-01-descriptive-statistics.md).

## 3. Conceptual Explanation

### 3.1 A random variable is a number produced by chance

A random variable $X$ maps outcomes to numbers: the number of heads in 10 flips, the height of a
random student, tomorrow's temperature. It is **discrete** if its values can be listed (counts) and
**continuous** if they lie on a continuum (measurements).

- **PMF** (discrete): $p(x) = P(X = x)$, with $\sum_x p(x) = 1$.
- **PDF** (continuous): $f(x) \ge 0$ with $\int f(x)\,dx = 1$; probabilities are **areas**,
  $P(a \le X \le b) = \int_a^b f(x)\,dx$. For a continuous variable $P(X = x) = 0$ for every $x$ — a
  single point has no width.
- **CDF**, both cases: $F(x) = P(X \le x)$, non-decreasing, from 0 to 1. This is what a library's
  `cdf` function returns, and what you read off a table.

### 3.2 Expectation and variance

$$
\mathbb{E}[X] = \sum_x x\,p(x)
\qquad\text{(discrete)}
$$

$$
\operatorname{Var}(X) = \mathbb{E}\left[(X - \mathbb{E}[X])^2\right] = \mathbb{E}[X^2] - \left(\mathbb{E}[X]\right)^2
$$

Expectation is the long-run average, not a prediction about any single trial. The variance identity on
the right is the one to use in code: it needs one pass and no second loop.

For a linear transformation, $\mathbb{E}[aX + b] = a\mathbb{E}[X] + b$ and
$\operatorname{Var}(aX+b) = a^2\operatorname{Var}(X)$ — shifting does not change spread, scaling by $a$
multiplies the standard deviation by $|a|$. This is precisely how standardisation works.

### 3.3 The binomial distribution

$X \sim \text{Binomial}(n, p)$ counts successes in $n$ independent trials with the same success
probability $p$:

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k},
\qquad
\mathbb{E}[X] = np,
\qquad
\operatorname{Var}(X) = np(1-p)
$$

The four assumptions matter and are frequently violated: fixed $n$, independent trials, constant $p$,
two outcomes per trial. If the trials are not independent (students copying in a class), the variance
is larger than $np(1-p)$.

### 3.4 The normal distribution

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

Written $X \sim \mathcal{N}(\mu, \sigma^2)$. It is symmetric about $\mu$, with inflection points at
$\mu \pm \sigma$. Standardising with $z = (x-\mu)/\sigma$ gives $\mathcal{N}(0,1)$, the only table you
ever need:

$$
P(X \le x) = \Phi\!\left(\frac{x-\mu}{\sigma}\right)
$$

**Empirical rule:** about 68% of values lie within $1\sigma$, 95% within $2\sigma$, 99.7% within
$3\sigma$. That is where the "$3\sigma$ event" language in quality control and anomaly detection comes
from.

Why is the normal everywhere? Because of the central limit theorem, which LP03-05 covers: sums and
averages of many independent quantities tend toward normality regardless of the underlying
distribution.

## 4. Worked Examples

### Example 1 — expectation and variance from a table

A loaded die has $P(1)=0.1$, $P(2)=0.2$, $P(3)=0.2$, $P(4)=0.2$, $P(5)=0.2$, $P(6)=0.1$.

$$
\mathbb{E}[X] = 1(0.1)+2(0.2)+3(0.2)+4(0.2)+5(0.2)+6(0.1) = 0.1+0.4+0.6+0.8+1.0+0.6 = 3.5
$$

$\mathbb{E}[X^2] = 1(0.1)+4(0.2)+9(0.2)+16(0.2)+25(0.2)+36(0.1) = 0.1+0.8+1.8+3.2+5.0+3.6 = 14.5$

$$
\operatorname{Var}(X) = 14.5 - 3.5^2 = 14.5 - 12.25 = 2.25,
\qquad \sigma = 1.5
$$

```python
import numpy as np

x = np.arange(1, 7)
p = np.array([0.1, 0.2, 0.2, 0.2, 0.2, 0.1])
mean = (x * p).sum()
var = (x**2 * p).sum() - mean**2
print(round(mean, 4), round(var, 4), round(float(np.sqrt(var)), 4))
```

```text
3.5 2.25 1.5
```

The mean is the fair-die value 3.5 — the loading is symmetric, so it does not shift the centre, only
the spread compared with a fair die's $35/12 \approx 2.92$.

### Example 2 — binomial by hand

Ten independent questions, each with success probability 0.3. What is $P(X = 3)$?

$$
P(X=3) = \binom{10}{3}(0.3)^3(0.7)^7 = 120 \times 0.027 \times 0.08235 \approx 0.2668
$$

```python
from math import comb

n, p, k = 10, 0.3, 3
pr = comb(n, k) * p**k * (1 - p) ** (n - k)
print(round(pr, 4), round(n * p, 1), round(n * p * (1 - p), 2))
```

```text
0.2668 3.0 2.1
```

About 27% chance of exactly three successes, with an expected 3 and variance 2.1 ($\sigma \approx
1.45$). Note the distinction between "expected" and "most likely": the expectation is exactly 3 here,
and 3 *is* the mode for this $p$, but that coincidence is not a rule.

### Example 3 — a normal probability via the empirical rule and via $\Phi$

Scores are $X \sim \mathcal{N}(68, 9^2)$. What fraction score below 70?

$$
z = \frac{70-68}{9} = 0.222, \qquad P(X \le 70) = \Phi(0.222) \approx 0.588
$$

```python
from math import erf, sqrt

def phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))

print(round(phi((70 - 68) / 9), 3))
```

```text
0.588
```

So about 59% score below 70 — and by the empirical rule, roughly 68% lie between 59 and 77, which is
consistent. If you have no table to hand, the rule gives a serviceable estimate; the exact value needs
$\Phi$.

## 5. Visual Explanation

```text
  PMF (discrete)                  PDF (continuous)
  p(x)                            f(x)
   │      ▂▄▆▄▂                    │        ▄▆█▆▄
   │    ▂▄█████▄▂                  │      ▄███████▄
   └──┬──┬──┬──┬──┬── x             └────┬───┬───┬──── x
      0  1  2  3  4                    µ-σ  µ  µ+σ

  bars: height = probability      curve: area = probability
```

*Text description of the diagram:* on the left, discrete probabilities are bar heights that sum to 1 —
you read $P(X = k)$ directly. On the right, a continuous density has no probability at a point; you read
the area under the curve between two values. The shaded band between $\mu-\sigma$ and $\mu+\sigma$
covers about 68% of the area, which is the empirical rule in a picture.

## 6. Mathematical Formulation

$$
\mathbb{E}[X] = \sum_x x\,p(x), \qquad
\operatorname{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2
$$

$$
X \sim \text{Bin}(n,p): \quad P(X=k) = \binom{n}{k}p^k(1-p)^{n-k}, \quad \mathbb{E}[X]=np, \quad \operatorname{Var}(X)=np(1-p)
$$

$$
X \sim \mathcal{N}(\mu,\sigma^2): \quad Z = \frac{X-\mu}{\sigma} \sim \mathcal{N}(0,1), \quad P(a \le X \le b) = \Phi\!\left(\frac{b-\mu}{\sigma}\right) - \Phi\!\left(\frac{a-\mu}{\sigma}\right)
$$

Two conventions to watch: the normal is written $\mathcal{N}(\mu, \sigma^2)$ in mathematics but
`normal(loc=mu, scale=sigma)` in code. Passing the variance where the standard deviation is expected
is a quiet, common error that changes every downstream number.

## 7. Python Implementation

```python
"""Simulate, then compare with the theoretical formulas."""
import numpy as np

rng = np.random.default_rng(seed=42)

# Binomial: 10 trials, p = 0.3, 20 000 repetitions
draws = rng.binomial(n=10, p=0.3, size=20_000)
print("simulated mean/var:", draws.mean().round(3), draws.var().round(3))
print("theoretical       :", 10 * 0.3, round(10 * 0.3 * 0.7, 3))

# Normal: mean 68, sd 9
x = rng.normal(loc=68, scale=9, size=20_000)
within1 = np.mean(np.abs(x - 68) <= 9)
within2 = np.mean(np.abs(x - 68) <= 18)
print("within 1 sd:", round(float(within1), 3), " within 2 sd:", round(float(within2), 3))
```

**Output**

```text
simulated mean/var: 3.003 2.109
theoretical       : 3.0 2.1
within 1 sd: 0.677  within 2 sd: 0.953
```

Simulation is the cheapest way to check that you have understood a formula: if the simulated mean and
variance do not match $np$ and $np(1-p)$, either the simulation or your understanding is wrong, and the
disagreement tells you which numbers to inspect.

## 8. Practical Applications

- **Anomaly detection.** Flag values beyond $3\sigma$ (or a robust equivalent) and you have the simplest
  detector that works — with a known false-positive rate under normality.
- **Model outputs.** A classifier's logits can be turned into probabilities with a softmax or sigmoid,
  which is a distribution over classes; understanding PMFs is what makes those outputs interpretable.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Using a density as a probability | Values above 1 | $f(x)$ is not $P(X=x)$ | Integrate over an interval |
| Passing variance as `scale` | Absurdly wide/narrow spread | Convention mix-up | `scale=sigma` |
| Applying the binomial to dependent trials | Variance too small | Independence violated | Use a different model |
| Expecting the mean to be a likely value | "Nobody scores 3.5" | Mean is a long-run average | Report a distribution, not one number |

## 10. Self-Assessment

**1.** $X$ takes values 0, 1, 2 with probabilities 0.5, 0.3, 0.2. Compute $\mathbb{E}[X]$ and
$\operatorname{Var}(X)$.
<details><summary>Show answer</summary>

$\mathbb{E}[X] = 0 + 0.3 + 0.4 = 0.7$. $\mathbb{E}[X^2] = 0 + 0.3 + 0.8 = 1.1$. So
$\operatorname{Var}(X) = 1.1 - 0.49 = 0.61$.
</details>

**2.** Why is $P(X = 5)$ zero for a continuous random variable?
<details><summary>Show answer</summary>

Because probability is area under the density, and a single point has zero width. Only intervals have
positive probability; this is why continuous distributions are described by densities and CDFs.
</details>

**3.** A binomial experiment has $n=20$, $p=0.1$. What are the mean and standard deviation?
<details><summary>Show answer</summary>

Mean $= 2$; variance $= 20 \times 0.1 \times 0.9 = 1.8$; standard deviation $\approx 1.34$.
</details>

**4.** Scores are normal with mean 500 and standard deviation 100. What fraction lie between 400 and
700?
<details><summary>Show answer</summary>

$z$ from $-1$ to $+2$, so $\Phi(2) - \Phi(-1) \approx 0.977 - 0.159 = 0.818$, about 82%. The empirical
rule alone would suggest roughly $68/2 + 95/2 = 81.5\%$ — close, but the exact value needs $\Phi$.
</details>

## 11. Further Reading

- [Seeing Theory, Ch. 3: Probability Distributions](https://seeing-theory.brown.edu/probability-distributions/index.html) — interactive binomial and normal.
- [OpenStax Introductory Statistics 2e, Ch. 4 and 6](https://openstax.org/books/introductory-statistics-2e/pages/4-introduction) — discrete and normal distributions with tables.

## Mini-Lab

Simulate 10 000 draws from $\text{Binomial}(20, 0.4)$ and 10 000 from $\mathcal{N}(20\times0.4, 20\times0.4\times0.6)$.
Plot both histograms with the same bins and compare their shapes. Then compute the fraction of
binomial draws within one standard deviation of the mean and compare it with the normal's 68%. How
close are they, and would you expect them to be closer with $n = 100$?

## What to Do Next

Continue to [LP03-05 Sampling, Correlation and Covariance](LP03-05-sampling-correlation-and-covariance.md).
