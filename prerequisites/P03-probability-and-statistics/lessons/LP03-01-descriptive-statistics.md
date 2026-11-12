# LP03-01 — Descriptive Statistics

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Study time | 75 minutes |
| Prerequisites | [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) |
| Lab | [LAB-P03-01](../labs/lab-p03-01-exam-score-report.md) |

[← Previous unit: P02](../../P02-mathematics-for-ai/README.md) · [P03 home](../README.md) · [Next: Probability Rules →](LP03-02-probability-rules-and-conditional-probability.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Compute** mean, median, mode, variance and standard deviation by hand and in code.
- **Choose** the right centre measurement for skewed data, and justify the choice.
- **Distinguish** population from sample formulas, and say when each applies.
- **Read** a five-number summary and detect skew from the comparison of mean and median.

## 2. Prerequisite Knowledge

- NumPy and pandas basics, including `mean`, `std` and `describe`:
  [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md).

## 3. Conceptual Explanation

### 3.1 Two questions, five numbers

Descriptive statistics answer two questions about a column of data: **where is the centre?** and **how
spread out is it?** Almost every summary you will read — and every model diagnostic — is a variation
on those two.

### 3.2 Centre: mean, median, mode

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
\qquad\text{(mean)}
$$

The **median** is the middle value once the data is sorted (the average of the two middle values when
$n$ is even). The **mode** is the most frequent value — the only sensible centre for categorical data.

The choice matters when the data is skewed:

- The mean uses every value, so a single extreme observation moves it.
- The median depends only on position, so extremes barely move it.

Household income is the classic case: a few very large incomes raise the mean well above the median,
and a report that quotes only the mean overstates what a typical household earns.

### 3.3 Spread: variance and standard deviation

Variance is the average squared distance from the mean:

$$
\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2
\qquad\text{(population)}
$$

$$
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2
\qquad\text{(sample)}
$$

Squaring makes deviations positive but also changes units — grams become grams squared. The **standard
deviation** is the square root, which returns to the original units: "typically about 2 marks away from
the mean" is intelligible in a way that "variance 4 marks²" is not.

Why $n-1$? Because $\bar{x}$ is itself estimated from the data, so deviations from it are slightly too
small; dividing by $n-1$ corrects the bias. With $n=8$ the difference is about 7%, which is enough to
change a reported figure.

### 3.4 Shape: skew and the five-number summary

The five-number summary is minimum, first quartile $Q_1$, median, third quartile $Q_3$, maximum. The
interquartile range $\text{IQR} = Q_3 - Q_1$ covers the middle half of the data and, like the median,
is resistant to extremes.

- **mean > median** → right (positive) skew: a long tail of large values.
- **mean < median** → left (negative) skew.
- **mean ≈ median** → roughly symmetric.

## 4. Worked Examples

### Example 1 — a small dataset, fully described

Data: $2, 4, 4, 4, 5, 5, 7, 9$ ($n = 8$).

Mean: $\sum x_i = 40$, so $\bar{x} = 5$.

Median: the 4th and 5th sorted values are 4 and 5, so median $= 4.5$.

Mode: 4, occurring three times.

Deviations from 5: $-3, -1, -1, -1, 0, 0, 2, 4$. Squares: $9, 1, 1, 1, 0, 0, 4, 16$; sum $= 32$.

$$
\sigma^2 = 32/8 = 4,\quad \sigma = 2;
\qquad s^2 = 32/7 \approx 4.571,\quad s \approx 2.138
$$

```python
import numpy as np

data = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print(data.mean(), np.median(data), data.std(), data.std(ddof=1).round(3))
```

```text
5.0 4.5 2.0 2.138
```

`ddof=1` selects the sample formula. NumPy defaults to the population version, pandas' `Series.std`
defaults to the sample version — a discrepancy that has produced more than one wrong table in a
report.

### Example 2 — skew in one line

```python
skewed = np.array([1, 1, 2, 2, 3, 50])
print(skewed.mean().round(2), np.median(skewed))
```

```text
9.83 2.0
```

Mean 9.83, median 2.0. Six values, one of them 50 — and the mean is now describing a person who does
not exist in the data. The median 2 is a fair summary; the mean is a fair summary of the *total*
divided by six. Report both, and say which question you are answering.

### Example 3 — quartiles and the IQR

```python
q1, q3 = np.percentile(data, [25, 75])
print(q1, q3, q3 - q1)
```

```text
4.0 5.5 1.5
```

Half the observations lie between 4.0 and 5.5. The IQR of 1.5 is the width of the box in a boxplot,
and $1.5 \times \text{IQR}$ beyond the quartiles is the conventional outlier fence that P04 uses.

## 5. Visual Explanation

```text
 symmetric            right-skewed           left-skewed
   ▁▃█▇▃▁               ▁█▇▃▂▁▁•              •▁▁▂▃▇█▁
   mean = median        mean > median          mean < median
```

*Text description of the diagram:* three small histograms. The symmetric one has matching tails and
mean equal to median. The right-skewed one has a long tail to the right, which pulls the mean right of
the median. The left-skewed one has the long tail on the left, pulling the mean left of the median.
The tail is always where the mean moves.

## 6. Mathematical Formulation

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i,
\qquad
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2,
\qquad
s = \sqrt{s^2}
$$

An equivalent, less numerically delicate form used by streaming algorithms:

$$
s^2 = \frac{1}{n-1}\left(\sum_i x_i^2 - n\bar{x}^2\right)
$$

It is algebraically identical but subtracts two large numbers, so with values around $10^8$ it loses
precision — which is why libraries use a two-pass or Welford update instead.

Standardisation, which P04 builds on:

$$
z_i = \frac{x_i - \bar{x}}{s}
$$

has mean 0 and standard deviation 1, making variables measured in different units comparable.

## 7. Python Implementation

```python
"""A description table you can reuse for any numeric column."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=0)
scores = pd.Series(rng.normal(loc=68, scale=9, size=200).round(0))

summary = {
    "n": scores.size,
    "mean": scores.mean(),
    "median": scores.median(),
    "std": scores.std(),              # sample std by default in pandas
    "min": scores.min(),
    "q1": scores.quantile(0.25),
    "q3": scores.quantile(0.75),
    "max": scores.max(),
    "iqr": scores.quantile(0.75) - scores.quantile(0.25),
}
for key, value in summary.items():
    print(f"{key:7s} {value:8.2f}")

print("skew-ish:", "right" if summary["mean"] > summary["median"] else "left/even")
```

**Output**

```text
n         200.00
mean       68.14
median     68.00
std         8.68
min        46.00
q1         62.00
q3         74.00
max        86.00
iqr        12.00
skew-ish: right
```

The printed `n` is a float because it went through the same format string; the content is what matters.
The true distribution is symmetric, so the mean sits only 0.14 above the median — sampling noise at
$n = 200$, not evidence of skew. With 20 000 draws the gap would shrink to a few hundredths. Read the
`skew-ish` line as a hint to look at a histogram, never as a conclusion.

## 8. Practical Applications

- **Reporting.** Any table of results should state n, a centre and a spread — and say which centre.
- **Model inputs.** Standardisation uses the mean and standard deviation; robust scaling uses the
  median and IQR precisely because they ignore outliers.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Using the mean on skewed data | A "typical" value no one has | Mean is pulled by tails | Report median too |
| Mixing `ddof` | Two tools disagree | NumPy defaults to population | State `ddof=1` explicitly |
| Treating mode as a number | Wrong for continuous data | Continuous values rarely repeat | Bin the data first |
| Comparing standard deviations across units | Meaningless ratio | SD carries units | Compare coefficients of variation $s/\bar{x}$ |

## 10. Self-Assessment

**1.** Data: $3, 5, 5, 7, 20$. Compute the mean and median. Which better describes a typical value, and
why?
<details><summary>Show answer</summary>

Mean $= 40/5 = 8$; median $= 5$. The single value 20 pulls the mean upward; the median 5 describes the
typical observation. Report the median for skewed data and mention the extreme.
</details>

**2.** A column has standard deviation 0. What does that tell you about the column?
<details><summary>Show answer</summary>

Every value is identical (equal to the mean), so all deviations are zero. Such a column carries no
information for a model and is usually dropped.
</details>

**3.** Why does the sample variance divide by $n-1$ rather than $n$?
<details><summary>Show answer</summary>

Because deviations are measured from the sample mean, which is itself fitted to the data and sits
slightly closer to the points than the true mean does. Dividing by $n-1$ corrects that downward bias,
making $s^2$ an unbiased estimator of $\sigma^2$.
</details>

**4.** Mean 50, median 61. Which way is the data skewed, and what kind of values would you look for?
<details><summary>Show answer</summary>

Left-skewed — a tail of small values pulls the mean below the median. Look for a cluster of unusually
low observations, which may be data-entry errors or a genuine minority group.
</details>

## 11. Further Reading

- [pandas: Descriptive statistics](https://pandas.pydata.org/docs/user_guide/basics.html#descriptive-statistics) — `describe`, `quantile`, `std` and their defaults.
- [NIST/SEMATECH e-Handbook, Measures of Scale](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm) — variance and standard deviation with worked examples.

## Mini-Lab

Generate two columns with `np.random.default_rng(seed=1)`: 500 draws from a normal distribution with
mean 60 and standard deviation 8, and 500 draws from an exponential distribution scaled by 8. For each,
report mean, median, standard deviation, IQR and the difference between mean and median. Draw a
histogram of each. Which column shows the skew you predicted, and how far apart are the two centres?

## What to Do Next

Continue to [LP03-02 Probability Rules and Conditional Probability](LP03-02-probability-rules-and-conditional-probability.md).
