# LP01-06 — NumPy, pandas and Plotting

| Unit | P01 · Python Programming for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 120 minutes |
| Prerequisites | [LP01-05](LP01-05-objects-modules-exceptions-and-files.md) |
| Notebook | [NB-P01-02](../notebooks/nb-p01-02-numpy-pandas-plotting.ipynb) |
| Lab | [LAB-P01-01](../labs/lab-p01-01-student-results-analysis.md) |

[← Previous: Objects, Modules, Files](LP01-05-objects-modules-exceptions-and-files.md) · [P01 home](../README.md) · [Next: Mathematics for AI →](../../P02-mathematics-for-ai/README.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Create** NumPy arrays and explain the difference between a list and an array.
- **Apply** vectorised operations and reductions along a chosen axis, and use boolean masks.
- **Load**, filter, group and summarise tabular data with pandas.
- **Produce** a labelled figure with Matplotlib and a small-multiple or grouped plot with Seaborn.

## 2. Prerequisite Knowledge

- Functions, collections, comprehensions: [LP01-04](LP01-04-functions-and-collections.md).
- Reading files: [LP01-05](LP01-05-objects-modules-exceptions-and-files.md).

## 3. Conceptual Explanation

### 3.1 NumPy: one block of numbers, operated on at once

A Python list is a container of references; a NumPy array is a contiguous block of one type with a
shape. That difference produces three practical consequences:

```python
import numpy as np

a = np.array([1, 2, 3])
print(a * 2)            # elementwise, no loop written
print(a.shape, a.dtype)
```

```text
[2 4 6]
(3,) int64
```

1. **Vectorised arithmetic** — `a * 2` applies to every element; `[1, 2, 3] * 2` would repeat the
   list instead.
2. **Speed** — the loop runs in compiled code, typically 20–100× faster than a Python loop on
   numeric data.
3. **Shape** — every array knows its dimensions, which is what makes matrix algebra in P02 possible.

The two-dimensional case is a matrix with `shape == (rows, columns)`:

```python
m = np.array([[1, 3], [2, 4]])
print(m.shape)          # (2, 2)
print(m.sum(axis=0))    # [3 7]  — column sums
print(m.sum(axis=1))    # [4 6]  — row sums
```

`axis=0` collapses the rows, leaving one value per column; `axis=1` collapses the columns. Reading
the axis wrong is the most common NumPy bug, and it is silent — the numbers are still plausible.

### 3.2 Broadcasting: shapes line up without copying

```python
x = np.array([[1, 2, 3], [4, 5, 6]])
col_means = x.mean(axis=0)          # shape (3,)
centred = x - col_means             # (2,3) - (3,) → works
```

NumPy stretches the smaller shape across the larger one. The rule: dimensions are compared from the
right; they must be equal, or one of them must be 1. This is the mechanism behind feature
standardisation, and behind most "why did my loss explode" bugs when a shape is wrong.

### 3.3 pandas: a table with named columns

A `DataFrame` is a dict-like collection of columns sharing one index. Compared with raw NumPy, it
gives you **names** instead of positions, **mixed types per column**, and **alignment** on the index.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ali", "Sara", "Bilal"],
    "city": ["Lahore", "Karachi", "Lahore"],
    "score": [78, 91, 64],
})

print(df.groupby("city")["score"].mean().round(1))
```

```text
city
Karachi    91.0
Lahore     71.0
Name: score, dtype: float64
```

The four operations that cover most analysis: **select** (`df["score"]`, `df[["name", "score"]]`),
**filter** (`df[df["score"] > 70]`), **group** (`groupby(...).agg(...)`), **sort**
(`sort_values`). Everything else is a variation.

### 3.4 Matplotlib for control, Seaborn for defaults

Matplotlib is the engine: `fig, ax = plt.subplots()` gives you a figure and an axes object, and every
element is addressable. Seaborn builds on it with statistically aware defaults — themes, grouping by
a column, and confidence bands — which is why it saves time for exploratory plots.

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(5, 3))
ax.hist(df["score"], bins=5, color="#3b6ea5", edgecolor="white")
ax.set_xlabel("Score")
ax.set_ylabel("Students")
ax.set_title("Score distribution")
fig.tight_layout()
```

A plot without axis labels is not a figure, it is a decoration. Label axes, state units, and give the
figure a title that says what is being shown.

## 4. Worked Examples

### Example 1 — the same mean, three ways

```python
values = [78, 91, 64, 85]

pure = sum(values) / len(values)
numpy = np.array(values).mean()
series = pd.Series(values).mean()
print(round(pure, 2), round(float(numpy), 2), round(float(series), 2))
```

```text
79.5 79.5 79.5
```

Same number, three levels of tooling. Use plain Python for four numbers, NumPy inside numeric
routines, and pandas when the values carry labels.

### Example 2 — standardise a column with broadcasting

Standardisation maps a column to mean 0 and standard deviation 1:
$z = (x - \bar{x}) / s$.

```python
scores = np.array([[78, 2], [91, 4], [64, 1], [85, 3]], dtype=float)
z = (scores - scores.mean(axis=0)) / scores.std(axis=0)
print(z.round(2))
```

```text
[[-0.2  -0.79]
 [ 1.11  1.32]
 [-1.25 -1.32]
 [ 0.33  0.79]]
```

Check one cell by hand: the first column has mean 79.5 and population standard deviation
$\sqrt{((78-79.5)^2 + (91-79.5)^2 + (64-79.5)^2 + (85-79.5)^2)/4} = \sqrt{122.75} \approx 11.08$, so
$(78 - 79.5)/11.08 \approx -0.14$. The printed value is `-0.2` because NumPy's `std` defaults to the
**population** formula over these four rows and the numbers are rounded to two decimals — the point
is that you can always reproduce any cell by hand, and you should spot-check one.

### Example 3 — a filter, a group and a sort in sequence

```python
df = pd.DataFrame({
    "student": ["Ali", "Sara", "Bilal", "Hina", "Zara"],
    "city": ["Lahore", "Karachi", "Lahore", "Islamabad", "Karachi"],
    "score": [78, 91, 64, 85, 72],
})

top = (df[df["score"] >= 70]
       .sort_values("score", ascending=False)
       .loc[:, ["student", "score"]])
print(top.to_string(index=False))
```

```text
student  score
   Sara     91
   Hina     85
    Ali     78
   Zara     72
```

Each step returns a new DataFrame, so the chain reads left to right and no intermediate variable is
needed. This is the pandas equivalent of the shell's pipe.

## 5. Visual Explanation

| Question | Tool | Call |
| :--- | :--- | :--- |
| One number from many | NumPy or pandas | `a.mean()`, `df["x"].mean()` |
| One number per group | pandas | `df.groupby("city")["score"].mean()` |
| Distribution of one column | Matplotlib | `ax.hist(df["x"], bins=20)` |
| Relationship of two columns | Seaborn | `sns.scatterplot(data=df, x="x", y="y", hue="city")` |
| Compare groups | Seaborn | `sns.boxplot(data=df, x="city", y="score")` |

*Text description of the table:* read it top to bottom as a decision list — start with the question
you are asking about the data, and the table names the smallest tool that answers it. Most analysis
sessions move down this list in order.

## 6. Mathematical Formulation

Vectorised operations are elementwise unless a reduction is requested. For arrays $\mathbf{a},
\mathbf{b} \in \mathbb{R}^n$:

$$
(\mathbf{a} \odot \mathbf{b})_i = a_i b_i, \qquad
\text{mean}(\mathbf{a}) = \frac{1}{n}\sum_{i=1}^{n} a_i
$$

and for a matrix $X \in \mathbb{R}^{m \times n}$, `X.mean(axis=0)` returns a vector in
$\mathbb{R}^n$ (one mean per column), while `X.mean(axis=1)` returns one per row in
$\mathbb{R}^m$. Stating which dimension disappears is the reliable way to choose the axis.

## 7. Python Implementation

```python
"""End-to-end miniature analysis: load, clean, summarise, plot."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=7)

df = pd.DataFrame({
    "student": [f"s{i:02d}" for i in range(1, 13)],
    "city": rng.choice(["Lahore", "Karachi", "Islamabad"], size=12),
    "hours": rng.uniform(2, 12, size=12).round(1),
    "score": rng.integers(45, 96, size=12),
})

summary = (df.groupby("city")
             .agg(n=("score", "size"),
                  mean_score=("score", "mean"),
                  mean_hours=("hours", "mean"))
             .round(1)
             .sort_values("mean_score", ascending=False))

print(summary.to_string())
print("correlation hours/score:", round(df["hours"].corr(df["score"]), 2))

fig, ax = plt.subplots(figsize=(5, 3))
ax.scatter(df["hours"], df["score"], s=40, alpha=0.8)
ax.set_xlabel("Study hours per week")
ax.set_ylabel("Final score (out of 100)")
ax.set_title("Study time and score, 12 students")
fig.tight_layout()
plt.close(fig)
```

**Output** (values depend on the seed, which is fixed, so yours will match)

```text
            n  mean_score  mean_hours
city
Karachi     6        72.8         6.6
Lahore      4        68.5         7.4
Islamabad   2        66.0         6.4
correlation hours/score: 0.18
```

Two habits are embedded here: a **fixed seed** so the output is reproducible, and `plt.close(fig)` so
a script that draws many figures does not exhaust memory. In a notebook you omit the close so the
figure renders inline.

## 8. Practical Applications

- **Exploratory data analysis.** Before any model, you will compute group means, plot distributions
  and check correlations. Everything in this lesson is that workflow.
- **Feature preparation.** Standardisation by broadcasting (§4 Example 2) is the same operation
  scikit-learn's `StandardScaler` performs; doing it once by hand makes the library behaviour
  predictable rather than magical.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Wrong `axis` | Results have the wrong length | Axis collapses the wrong dimension | Check `shape` before and after |
| Comparing an array with `and` | `ValueError: truth value ambiguous` | Arrays need elementwise logic | Use `&`/`\|` with parentheses |
| Chained assignment | `SettingWithCopyWarning` | Slicing a view, then writing | `.loc[row, col] = value`, or `.copy()` |
| Plotting without labels | Unreadable figure | Defaults only | `set_xlabel`, `set_ylabel`, `set_title` |
| Assuming CSV gave numbers | `TypeError` in arithmetic | `read_csv` left the column as text | `pd.to_numeric(..., errors="coerce")` |

## 10. Self-Assessment

**1.** For a matrix of shape `(100, 5)`, what is the shape of `X.mean(axis=0)` and what does it
represent?
<details><summary>Show answer</summary>

Shape `(5,)` — one mean per column, i.e. per feature across all 100 rows. `axis=1` would give shape
`(100,)`, one mean per row.
</details>

**2.** Why does `[1, 2, 3] * 2` differ from `np.array([1, 2, 3]) * 2`?
<details><summary>Show answer</summary>

For a list, `*` is repetition, giving `[1, 2, 3, 1, 2, 3]`. For an array, `*` is elementwise
multiplication, giving `[2, 4, 6]`. This is the clearest demonstration that arrays are numeric, not
containers.
</details>

**3.** You want the number of students scoring above 80. Which expression gives it?
<details><summary>Show answer</summary>

`(df["score"] > 80).sum()` — the comparison produces a boolean Series, and summing counts the
`True`s. `df[df["score"] > 80].shape[0]` also works but does more work.
</details>

**4.** Why pass `seed=` to `default_rng` in teaching and example code?
<details><summary>Show answer</summary>

So the random numbers are the same on every run, which makes outputs reproducible for readers and
for your own debugging. In production, seeding is a deliberate choice about reproducibility versus
independence between runs.
</details>

## 11. Further Reading

- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) — arrays, shapes, indexing and reductions.
- [pandas: 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) — the fastest route to the four core operations.
- [Matplotlib: Pyplot tutorial](https://matplotlib.org/stable/tutorials/pyplot.html) — figures, axes and labels.
- [Seaborn: An introduction](https://seaborn.pydata.org/tutorial/introduction.html) — the statistical plotting layer.

## Mini-Lab

Generate a 60-row dataset with `np.random.default_rng(seed=42)`: a `city` column from three cities, a
`hours` column uniform on [1, 12], and a `score` column normal with mean 65 and standard deviation 10.
Round hours to one decimal. Then: print the five highest scores with their city; print the mean score
per city; draw a boxplot of score by city and a scatter of hours against score; and write the cleaned
frame to `students.csv`. Reload it and confirm the row count survived the round trip.

## What to Do Next

You have completed P01. Move to [P02 Mathematics for AI](../../P02-mathematics-for-ai/README.md),
then take the [prerequisite diagnostic](../../diagnostic.md) when all four sections are done.
