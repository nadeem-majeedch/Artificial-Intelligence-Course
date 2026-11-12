# LP04-03 — Outliers, Normalisation and Standardisation

| Unit | P04 · Data Preparation and Visualisation |
| :--- | :--- |
| Level | 100 |
| Study time | 90 minutes |
| Prerequisites | [LP04-02](LP04-02-missing-values-and-duplicates.md) |
| Notebook | [NB-P04-01](../notebooks/nb-p04-01-data-preparation.ipynb) |
| Lab | [LAB-P04-01](../labs/lab-p04-01-messy-survey-cleanup.md) |

[← Previous: Missing Values](LP04-02-missing-values-and-duplicates.md) · [P04 home](../README.md) · [Next: Visualisation and EDA →](LP04-04-visualization-and-exploratory-data-analysis.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Detect** outliers with the IQR fence and the z-score, and explain the masking effect that makes
  the z-score unreliable on small samples.
- **Choose** deliberately between keeping, capping, correcting and removing an extreme value.
- **Apply** min-max scaling, standardisation and robust scaling, and predict what each does to a
  column.
- **Avoid** the scaling leakage that makes a model look better in testing than it is.

## 2. Prerequisite Knowledge

- Quantiles and standard deviation: [LP03-01](../../P03-probability-and-statistics/lessons/LP03-01-descriptive-statistics.md).
- pandas filtering: [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md).

## 3. Conceptual Explanation

### 3.1 An outlier is a value far from the bulk — not necessarily an error

A single late delivery is an outlier in delivery times, and also the most important observation in the
dataset if the task is predicting delays. Before doing anything with an extreme value, answer: **is it
a measurement error, a different population, or a genuine rare event?**

- **Error** (typo, unit mix-up, sensor fault) → correct or remove.
- **Different population** (an adult in a child-height dataset) → split the analysis, or exclude with a
  stated rule.
- **Genuine rare event** (fraud, failure) → keep it, and be careful that your metric does not ignore it.

### 3.2 Two detection methods, with different assumptions

**IQR fence** (distribution-free):

$$
\text{outlier if } x < Q_1 - 1.5\,\text{IQR} \quad\text{or}\quad x > Q_3 + 1.5\,\text{IQR}
$$

With roughly normal data this flags about 0.7% of points; it makes no normality assumption and is
barely affected by the extreme value itself, because quartiles are positional.

**z-score** (assumes approximate normality and a reliable mean/sd):

$$
z = \frac{x - \bar{x}}{s}, \qquad \text{outlier if } |z| > 3
$$

The weakness is **masking**: one huge value inflates $s$, which shrinks every z-score including its own.
With $n = 7$ and one extreme point, the outlier typically scores below 3 and hides. Robust alternatives
use the median and the median absolute deviation:

$$
M = \frac{0.6745\,(x - \text{median})}{\text{MAD}},
\qquad \text{MAD} = \text{median}(|x - \text{median}|)
$$

with $|M| > 3.5$ as the conventional threshold.

### 3.3 Scaling: what each transform does

| Transform | Formula | Output range | Preserves | Use when |
| :--- | :--- | :--- | :--- | :--- |
| Min–max | $x' = \dfrac{x - x_{\min}}{x_{\max} - x_{\min}}$ | $[0,1]$ | Shape, relative distances | Bounded inputs, neural nets, images |
| Standardise | $z = \dfrac{x - \bar{x}}{s}$ | mean 0, sd 1 | Shape, relative distances | Distance- and gradient-based models |
| Robust scale | $\dfrac{x - \text{median}}{\text{IQR}}$ | median 0 | Shape, ignores extremes | Data with outliers |

None of them makes data normal. A histogram that was skewed before standardisation is still skewed
after: the transform shifts and stretches, it does not change shape. For skew, apply $\log$ or a square
root **first**, then standardise.

### 3.4 Why scaling matters at all

Euclidean distance sums squared differences, so a feature measured in thousands dominates one measured
in single digits:

$$
d(\mathbf{a},\mathbf{b}) = \sqrt{\sum_j (a_j - b_j)^2}
$$

If $a_1 - b_1 = 1000$ and $a_2 - b_2 = 1$, the second feature is invisible. Standardising puts every
feature on the same footing, which changes what "nearest" means — usually for the better, and always
deliberately. Tree-based models split one feature at a time and are indifferent to scale; $k$-NN, SVM,
PCA and gradient descent are not.

**Leakage:** the mean, standard deviation, minimum and maximum are estimated from data. Estimate them on
the training split only, then apply the same numbers to validation and test sets. Scaling the whole
dataset before splitting is the classic silent leak — it rarely looks wrong, and it always flatters the
model.

## 4. Worked Examples

### Example 1 — one extreme value, two verdicts

Data: $10, 12, 13, 14, 15, 16, 100$.

Mean $= 180/7 \approx 25.71$, $s \approx 32.8$, so for 100:

$$
z = \frac{100 - 25.71}{32.8} \approx 2.26
$$

Below the 3 threshold — the outlier has hidden itself by inflating the standard deviation.

Quartiles: $Q_1 = 12.5$, $Q_3 = 15.5$, $\text{IQR} = 3$, so the upper fence is
$15.5 + 4.5 = 20$. The value 100 is flagged immediately.

```python
import numpy as np

x = np.array([10, 12, 13, 14, 15, 16, 100], dtype=float)
z = (x - x.mean()) / x.std(ddof=1)
q1, q3 = np.percentile(x, [25, 75])
print(z.round(2).tolist())
print(q1, q3, q3 + 1.5 * (q3 - q1))
```

```text
[-0.48, -0.42, -0.39, -0.36, -0.33, -0.3, 2.26]
[12.5 15.5 20.0]
```

Every z-score is squeezed toward zero by the inflated standard deviation, while the fence stays sharp.
That is the practical argument for the IQR rule on small samples.

### Example 2 — the three scalings side by side

For the value 100 in the same data, median 14 and IQR 3:

$$
\text{min-max} = \frac{100-10}{100-10} = 1.0,
\qquad
z \approx 2.26,
\qquad
\text{robust} = \frac{100-14}{3} \approx 28.67
$$

```python
minmax = (x - x.min()) / (x.max() - x.min())
z = (x - x.mean()) / x.std(ddof=1)
q1, q3 = np.percentile(x, [25, 75])
robust = (x - np.median(x)) / (q3 - q1)
print([round(float(v[-1]), 2) for v in (minmax, z, robust)])
```

```text
[1.0, 2.26, 28.67]
```

The robust score of 28.67 is the honest signal that this point is extraordinary; the z-score of 2.26
understates it. Report which measure you used, because the three disagree by an order of magnitude.
Note also that min-max scaling maps the outlier to exactly 1.0 and squashes everything else into
$[0, 0.07]$ — which is why it is the worst choice when extremes are present.

### Example 3 — capping versus removing

Suppose the values are monthly incomes and 100 is a data-entry error for 10.0. Correcting it is
obviously right. But suppose they are genuine incomes: capping at the 95th percentile keeps the row's
other columns usable, while removing the row discards them. If the task is predicting the *mean*
income, neither capping nor removal is neutral — both bias it downward — so the correct action is to
report the median and keep the data.

The decision table:

| Situation | Action |
| :--- | :--- |
| Provably an error (impossible value, unit mix) | Correct or remove |
| Genuine but rare, and the model must handle it | Keep |
| Genuine, extreme, and distorting a linear model | Cap (winsorise) and say so |
| Different population | Split the analysis by group |

## 5. Visual Explanation

```text
   IQR fence view
   ├────┬───────┬──────┬──────────────→
      Q1      median   Q3
   |←1.5IQR→|        |←1.5IQR→|
                                  ● 100  ← beyond the fence
```

*Text description of the diagram:* the box spans the middle half of the data from $Q_1$ to $Q_3$; the
whiskers extend 1.5 IQR beyond each hinge, and anything past them is plotted as an individual point.
This is exactly the boxplot you will draw in the next lesson, so the rule and the picture are the same
object.

## 6. Mathematical Formulation

$$
x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}} \in [0,1]
\qquad
z = \frac{x - \bar{x}}{s}, \quad \bar{z} = 0,\ s_z = 1
$$

For an affine transform $x' = ax + b$: mean becomes $a\bar{x} + b$ and standard deviation becomes
$|a|s$. Both min-max and standardisation are affine, which is why they preserve shape exactly —
correlation, skew and the ordering of values are untouched.

Distance distortion, quantitatively: if features have standard deviations $s_j$, the expected squared
Euclidean distance between two random points is $2\sum_j s_j^2$. A feature with $s = 100$ contributes
$10\,000$ times as much as one with $s = 1$, which is the entire case for standardising before any
distance-based method.

## 7. Python Implementation

```python
"""Fit scalers on training data only, then apply them everywhere."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=8)
df = pd.DataFrame({
    "income": rng.normal(60_000, 12_000, 200).round(-2),
    "age": rng.integers(18, 65, 200),
})
df.loc[0, "income"] = 5_000_000          # injected outlier

train, test = df.iloc[:150], df.iloc[150:]


def fit_scaler(frame: pd.DataFrame) -> dict:
    return {
        "median": frame.median(),
        "iqr": frame.quantile(0.75) - frame.quantile(0.25),
    }


def apply_scaler(frame: pd.DataFrame, stats: dict) -> pd.DataFrame:
    return (frame - stats["median"]) / stats["iqr"]


stats = fit_scaler(train)
print(apply_scaler(df, stats).describe().loc[["mean", "std"]].round(2).to_string())
print("max robust score:", round(float(apply_scaler(df, stats)["income"].max()), 1))
```

**Output**

```text
      income    age
mean    1.45  -0.08
std    19.72   0.56
max robust score: 278.7
```

The injected 5 000 000 produces a robust score near 279, while the rest of the column sits near zero —
the transform isolates the anomaly instead of hiding it. Two details matter more than the numbers: the
statistics came from `train` only, and the same `stats` dictionary is applied to both frames, so no
information crossed the split.

## 8. Practical Applications

- **Anomaly detection.** Robust scores, not z-scores, are the baseline detector for fraud and sensor
  faults, precisely because the anomalies you seek would otherwise inflate the scale.
- **Model pipelines.** `StandardScaler` inside a `Pipeline` is fitted per training fold; doing it outside
  is the most common cause of optimistic cross-validation scores.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Deleting every flagged value | Loss of the rare cases you care about | Treating the fence as an error detector | Inspect each flagged row |
| Using z-scores on small samples | Outlier not flagged | Masking by inflated $s$ | Use IQR or MAD |
| Scaling before splitting | Test score too good | Leakage | Fit on train only |
| Expecting scaling to fix skew | Still skewed | Affine transforms preserve shape | Log transform first |
| Min-max on a column with one huge value | Everything squashed near 0 | Range set by the extreme | Robust scale, or cap first |

## 10. Self-Assessment

**1.** Data: $4, 5, 6, 7, 8, 9, 40$. Compute $Q_1$, $Q_3$, IQR and the upper fence. Is 40 an outlier by
this rule?
<details><summary>Show answer</summary>

$Q_1 = 5$, $Q_3 = 9$, IQR $= 4$, upper fence $= 9 + 6 = 15$. Yes, 40 is well beyond it.
</details>

**2.** Why does a single extreme value reduce the z-score of that same value?
<details><summary>Show answer</summary>

Because $s$ is computed from the data including the extreme point; a large deviation increases the
standard deviation, which increases the denominator of every z-score. This is masking, and it is why
the z-rule fails on small samples.
</details>

**3.** A feature ranges from 0.001 to 0.002. Why standardise it rather than min-max scale it?
<details><summary>Show answer</summary>

Either is fine mathematically, but standardisation is preferable for gradient-based models because the
values are centred and on a predictable scale regardless of the raw units; min-max would leave a range of
width 1 but centred at 0.5. Standardisation also handles a changing range between train and test better.
</details>

**4.** You standardise using the mean of the full dataset, then split. What is the consequence, and how
large can it be?
<details><summary>Show answer</summary>

Test information enters the scaling statistics, so test performance is optimistic. With large samples the
effect is small; with a few hundred rows and a skewed feature it can shift results noticeably. The fix is
to fit the scaler on the training split.
</details>

## 11. Further Reading

- [scikit-learn: Preprocessing data](https://scikit-learn.org/stable/modules/preprocessing.html) — the reference for scalers and their leakage-safe use in pipelines.
- [NIST/SEMATECH: Detection of Outliers](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm) — IQR, z-score and MAD with worked examples.

## Mini-Lab

Generate a column of 500 values from a normal distribution with mean 50 and standard deviation 5, then
inject three values at 150, 200 and −100. Apply the IQR fence, the z-score with threshold 3, and the
modified z-score, and report how many values each method flags and which ones they miss. Then compare
min-max, standard, and robust scaling on the same column, reporting the range of each transformed
column.

## What to Do Next

Continue to [LP04-04 Visualisation and Exploratory Data Analysis](LP04-04-visualization-and-exploratory-data-analysis.md).
