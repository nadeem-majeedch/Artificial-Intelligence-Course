# LP04-04 — Visualisation and Exploratory Data Analysis

| Unit | P04 · Data Preparation and Visualisation |
| :--- | :--- |
| Level | 100 |
| Study time | 90 minutes |
| Prerequisites | [LP04-03](LP04-03-outliers-normalization-and-standardization.md) |
| Notebook | [NB-P04-01](../notebooks/nb-p04-01-data-preparation.ipynb) |
| Lab | [LAB-P04-01](../labs/lab-p04-01-messy-survey-cleanup.md) |

[← Previous: Outliers and Scaling](LP04-03-outliers-normalization-and-standardization.md) · [P04 home](../README.md) · [Next: Diagnostic →](../../diagnostic.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Choose** a chart type from the question you are asking, not from habit.
- **Build** a labelled multi-panel figure with Matplotlib and a grouped plot with Seaborn.
- **Run** a structured exploratory analysis: shape, types, missingness, univariate, bivariate,
  multivariate.
- **Recognise** the four common ways a chart misleads: truncated axes, overplotting, wrong aggregation
  and missing context.

## 2. Prerequisite Knowledge

- Matplotlib/Seaborn basics: [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md).
- Descriptive statistics and correlation: [LP03-01](../../P03-probability-and-statistics/lessons/LP03-01-descriptive-statistics.md),
  [LP03-05](../../P03-probability-and-statistics/lessons/LP03-05-sampling-correlation-and-covariance.md).

## 3. Conceptual Explanation

### 3.1 Chart choice follows the question

| Question | Chart | Why |
| :--- | :--- | :--- |
| How is one variable distributed? | Histogram, KDE, ECDF | Shows shape, skew, modes |
| How do groups compare? | Boxplot, violin, bar with error bars | Shows centre *and* spread |
| Are two variables related? | Scatter | Reveals non-linearity that $r$ hides |
| How does something change over time? | Line | Order matters |
| How do many variables co-vary? | Correlation heatmap, pair plot | Overview before detail |
| Where is the mass concentrated? | Hexbin, 2-D density | Avoids overplotting |

A bar chart summarises; a boxplot shows the summary *and* the spread; a scatter shows everything. When
in doubt, plot the raw points — aggregation is a decision you cannot undo once the chart is published.

### 3.2 The anatomy of a Matplotlib figure

- **Figure** — the whole canvas.
- **Axes** — one plotting area (most figures have several).
- **Artists** — lines, patches, text inside an axes.

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
axes[0, 0].hist(df["hours"], bins=20)
axes[0, 0].set_title("Study hours")
```

Working with `fig`/`axes` explicitly, rather than the implicit `plt.` state machine, is what makes
multi-panel figures and reusable plotting functions possible. Seaborn's `relplot`, `displot` and
`catplot` return a figure with facets; `scatterplot` and `boxplot` accept `ax=` so they compose into a
layout you control.

### 3.3 A structured exploration

1. **Shape and types** — rows, columns, dtypes; any column that should be numeric but is text?
2. **Missingness** — count and fraction per column; is it concentrated in a few rows?
3. **Univariate** — histogram and five-number summary per numeric column; value counts for categorical.
4. **Bivariate** — scatter against the target; grouped summaries by category.
5. **Multivariate** — correlation matrix, pair plot, and one interaction you suspect.
6. **Record hypotheses** — each one a sentence you could test, not a chart you happened to like.

### 3.4 Four ways a chart lies

1. **Truncated axis on a bar chart.** Bars encode length, so starting the axis at 90 instead of 0
   exaggerates a 2% difference into a visual landslide. Line charts may truncate; bars may not.
2. **Overplotting.** Ten thousand points in a small scatter become a blob; use transparency, hexbin, or
   a sample.
3. **Wrong aggregation.** A mean of already-averaged groups is not the overall mean unless the group
   sizes are equal.
4. **Missing context.** No units, no $n$, no date range. A chart without these cannot be checked.

## 4. Worked Examples

### Example 1 — a distribution, two ways

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(seed=2)
hours = rng.gamma(shape=2.0, scale=2.0, size=300)

fig, axes = plt.subplots(1, 2, figsize=(9, 3))
axes[0].hist(hours, bins=25, edgecolor="white")
axes[0].set_title("Histogram")
axes[1].boxplot(hours, vert=False)
axes[1].set_title("Boxplot")
for ax in axes:
    ax.set_xlabel("Hours per week")
fig.tight_layout()
plt.close(fig)
```

The histogram shows the right skew (gamma with shape 2), the boxplot shows the same skew through the
median sitting left of centre and a longer right whisker. Neither is wrong; they answer different
questions. Read the histogram for shape, the boxplot for quartiles and outliers.

### Example 2 — a grouped comparison

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Lahore", "Karachi", "Lahore", "Islamabad", "Karachi", "Lahore"],
    "score": [78, 91, 64, 85, 72, 88],
})
print(df.groupby("city")["score"].agg(["count", "mean"]).round(1).to_string())
```

```text
           count  mean
city
Islamabad      1  85.0
Karachi        2  81.5
Lahore         3  76.7
```

A bar chart of these means would hide that Islamabad's 85 comes from a single student. Always plot the
count alongside the mean, or use a boxplot, which makes small groups visibly thin.

### Example 3 — the correlation heatmap and what it hides

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=4)
x = rng.normal(size=200)
data = pd.DataFrame({
    "x": x,
    "linear": 2 * x + rng.normal(scale=0.5, size=200),
    "quadratic": x**2 + rng.normal(scale=0.5, size=200),
})
print(data.corr().round(2).to_string())
```

```text
              x  linear  quadratic
x          1.00    0.97      -0.04
linear     0.97    1.00      -0.03
quadratic -0.04   -0.03       1.00
```

The `quadratic` column is a *deterministic* function of `x`, yet its correlation is $-0.04$ — the
heatmap would tell you there is nothing there. Pearson correlation measures linear association only, which is
why the scatter plot in the notebook, not the heatmap alone, is the diagnostic.

## 5. Visual Explanation

```text
  misleading (truncated)            honest (zero baseline)
  100┤   █  █                       100┤
   98┤   █  █                        50┤  █  █
   96┤   █  █                         0└──█──█──
        A  B                             A  B
   "B is twice A!"                  "B is slightly taller"
```

*Text description of the diagram:* the same two values drawn on two axes. On the left the axis starts
near the values, so a small difference fills the panel; on the right it starts at zero and the
difference is visibly small. Bars encode magnitude by length, so the baseline is part of the data.

## 6. Mathematical Formulation

A histogram estimates the density by counting observations per bin of width $h$:

$$
\hat{f}(x) = \frac{1}{nh}\sum_{i=1}^{n}\mathbf{1}\{x_i \in B(x)\}
$$

The bin width is a modelling choice: too wide hides structure, too narrow shows noise. A useful default
is Sturges' rule, $k = \lceil \log_2 n\rceil + 1$ bins, or Freedman–Diaconis,
$h = 2\,\text{IQR}\,n^{-1/3}$, which adapts to spread and is robust to outliers.

An **ECDF** avoids the choice entirely:

$$
\hat{F}(x) = \frac{1}{n}\sum_{i=1}^{n}\mathbf{1}\{x_i \le x\}
$$

It is the empirical CDF, and reading a quantile off it is a one-line lookup — which is why it is the
best plot for "what fraction is below this threshold?" questions.

## 7. Python Implementation

```python
"""One exploratory pass: shapes, groups, relationship, and a four-panel figure."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=12)
n = 240
hours = rng.uniform(1, 12, n).round(1)
city = rng.choice(["Lahore", "Karachi", "Islamabad"], size=n)
bonus = pd.Series(city).map({"Lahore": 0, "Karachi": 4, "Islamabad": 2}).to_numpy()

df = pd.DataFrame({
    "hours": hours,
    "city": city,
    "score": (40 + 3 * hours + bonus + rng.normal(scale=4, size=n)).round(1),
})

print("shape:", df.shape)
print(df.groupby("city")["score"].agg(["count", "mean"]).round(1).to_string())
print("r(hours, score) =", round(float(df["hours"].corr(df["score"])), 2))

fig, axes = plt.subplots(2, 2, figsize=(10, 7))

axes[0, 0].hist(df["hours"], bins=20, edgecolor="white", color="#4c72b0")
axes[0, 0].set_title("Distribution of study hours")
axes[0, 0].set_xlabel("Hours per week")
axes[0, 0].set_ylabel("Students")

df.boxplot(column="score", by="city", ax=axes[0, 1], grid=False)
axes[0, 1].set_title("Score by city")
axes[0, 1].set_xlabel("")
axes[0, 1].set_ylabel("Score")

axes[1, 0].scatter(df["hours"], df["score"], s=18, alpha=0.6)
axes[1, 0].set_title("Score against study hours")
axes[1, 0].set_xlabel("Hours per week")
axes[1, 0].set_ylabel("Score")

df["city"].value_counts().plot(kind="bar", ax=axes[1, 1], color="#55a868")
axes[1, 1].set_title("Students per city")
axes[1, 1].set_xlabel("")
axes[1, 1].set_ylabel("Count")

fig.suptitle("Exploratory overview of a student survey", fontsize=12)
fig.tight_layout()
fig.savefig("eda_overview.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

**Output**

```text
shape: (240, 3)
           count  mean
city
Islamabad     94  60.7
Karachi       77  64.0
Lahore        69  60.6
r(hours, score) = 0.92
```

Read the pass in order: 240 rows and three columns, group sizes fairly balanced (69–94, so the means
are comparable), the city effect visible as a 3.4-mark gap between Karachi and Lahore, and a strong
linear relationship with hours ($r = 0.92$) that the scatter confirms is not curved. That is four questions answered before any model
is fitted — and the `count` column is what makes the group comparison trustworthy.

## 8. Practical Applications

- **Before modelling.** EDA decides which features exist, which need transforming, and whether the task
  is plausible at all. Skipping it is the most common cause of a model that scores well and is useless.
- **Communicating results.** A single well-labelled figure survives being screenshotted into a slide; a
  table of numbers rarely does. Design for that use.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Truncated bar axis | Exaggerated differences | Zooming in on values | Start bars at zero |
| Histogram with 5 bins | Featureless blob | Default `bins=10` on wide data | Use 20–50, or Freedman–Diaconis |
| Scatter with opaque points | Solid blob | Overplotting | `alpha`, smaller `s`, or hexbin |
| Sorting a pie chart by value | Unreadable | Too many slices | Bar chart, sorted |
| Unlabelled axes | Nobody can read it | Defaults | `set_xlabel`, units, `n` in the title |

## 10. Self-Assessment

**1.** You want to compare the spread of scores across four cities. Which chart, and why not a bar chart
of means?
<details><summary>Show answer</summary>

A boxplot (or violin) per city: it shows median, quartiles and outliers, so differences in spread and
small groups are visible. A bar of means hides spread entirely and can make a group of three students
look as solid as a group of three hundred.
</details>

**2.** Why is a truncated y-axis acceptable on a line chart but not on a bar chart?
<details><summary>Show answer</summary>

Bars encode value by length from the baseline, so changing the baseline falsifies the encoding. A line
encodes value by position, and readers interpret slopes; truncation is still worth flagging, but it does
not misrepresent the quantity itself.
</details>

**3.** A pair plot shows two clusters that the correlation matrix calls uncorrelated. Which do you
believe?
<details><summary>Show answer</summary>

The plot. Pearson correlation is a single number summarising linear association; two well-separated
clusters can produce $r \approx 0$ while being strongly structured. Always inspect the scatter.
</details>

**4.** Your histogram of income has one bar reaching 60% and a long flat tail. What do you do?
<details><summary>Show answer</summary>

Plot on a log scale, or plot the log of income, and report the median and IQR. The raw histogram is
accurate but uninformative; the transform reveals the structure in the tail without discarding it.
</details>

## 11. Further Reading

- [Matplotlib: Anatomy of a figure](https://matplotlib.org/stable/gallery/showcase/anatomy.html) — every element named and located.
- [Seaborn: An introduction](https://seaborn.pydata.org/tutorial/introduction.html) — figure-level versus axes-level functions.
- [Data-to-Viz](https://www.data-to-viz.com/) — a decision tree from question to chart type.

## Mini-Lab

Take the 240-row survey frame from §7, add a `passed` column (score ≥ 60), and produce a figure with:
a histogram of score split by `passed`, a boxplot of hours by city, and a scatter of hours against
score coloured by city. Report the pass rate per city as a table. Which city has the highest pass rate,
and does it also have the highest mean score? If the two answers differ, explain why in one sentence.

## What to Do Next

You have finished P04. Take the [prerequisite diagnostic](../../diagnostic.md) to check all four
sections, then continue to [Module 01](../../../modules/README.md#m01).
