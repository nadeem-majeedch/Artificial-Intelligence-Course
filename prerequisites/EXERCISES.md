# Prerequisite Exercises

Practice for the four prerequisite sections and the nine topics they cover. Every topic has **three
graded exercises** (warm-up → standard → stretch), **one guided exercise** with its expected output, and
**one independent challenge**. Hints are separated from answers on purpose: read the hint, try again, and
only then check the validation criteria.

**Course home:** [README](../README.md) · **Prerequisites:** [prerequisites/README.md](README.md) ·
**Diagnostic:** [diagnostic.md](diagnostic.md) · **Glossary:** [glossary.md](../resources/glossary.md)

Everything runs on CPU in a few seconds. No downloads, no datasets beyond what you type yourself.

**How to use this page.** Do the warm-up for the topic you are on. If it takes more than five minutes,
read the lesson again before continuing — this page is a check, not a course.

---

## 1. Python fundamentals
*Lesson: [LP01-02](P01-python-programming/lessons/LP01-02-variables-types-and-operators.md) ·
[LP01-03](P01-python-programming/lessons/LP01-03-conditionals-loops-and-comprehensions.md)*

**Warm-up 1.1.** Print the result and type of `17 // 5`, `17 % 5`, `17 / 5`, and `2 ** 10`.
**Standard 1.2.** Given `marks = [72, 45, 88, 91, 60]`, print the names of the marks that are above the
mean, using a comprehension and `zip` with `["Ali", "Sara", "Zain", "Hina", "Omar"]`.
**Stretch 1.3.** Write a loop that prints the first 10 Fibonacci numbers and stops early with `break` if
any value exceeds 100.

**Guided exercise.** Convert this to a single comprehension and explain the difference:

```python
squares = []
for n in range(1, 11):
    squares.append(n * n)
```

Run your version and confirm the output starts `[1, 4, 9, 16, 25]`.

**Independent challenge.** FizzBuzz with a twist: multiples of 3 print `Fizz`, of 5 `Buzz`, of 7 `Bang`,
and combinations concatenate (`FizzBang` for 21). Do it for 1–30 with one loop and no `if` chain longer
than three branches.

**Validation.** You are done when: 1.2 prints five names, 1.3 stops at `144 > 100`, and the challenge
prints `FizzBang` at 21 and `FizzBuzzBang` nowhere in 1–30 (why not?).

**Hints.** Use `statistics.mean` or `sum(marks)/len(marks)`. For the challenge, build a string and append
conditionally instead of branching on every combination.

---

## 2. Functions and data structures
*Lesson: [LP01-04](P01-python-programming/lessons/LP01-04-functions-and-collections.md)*

**Warm-up 2.1.** Write `is_even(n)` returning a boolean, and call it in a comprehension that keeps the
even numbers from 1–20.
**Standard 2.2.** Write `word_counts(text)` returning a dictionary of word → count for
`"the cat and the hat and the bat"`. Sort the result by count descending.
**Stretch 2.3.** Write `group_by_length(words)` returning a dict of length → list of words, then print
the longest group.

**Guided exercise.** Trace this function on paper, then run it:

```python
def add_item(basket, item, items=None):
    if items is None:
        items = []
    items.append(item)
    basket[item] = len(items)
    return basket

print(add_item({}, "apple"))
print(add_item({}, "pear"))
```

Explain why the second call prints `1` item rather than `2`, and what would happen with a mutable
default argument.

**Independent challenge.** Build a tiny inventory: a list of dicts, each with `sku`, `qty` and `price`.
Write three functions — `total_value`, `low_stock(threshold)`, `apply_discount(pct)` — that do not mutate
their input, and show that calling them twice gives the same answer.

**Validation.** `total_value` returns a number; `low_stock(5)` returns only rows below the threshold;
`apply_discount(10)` leaves the original list unchanged.

**Hints.** Copy with `[dict(row) for row in rows]`. For 2.2 use `collections.Counter` and compare with
your own loop.

---

## 3. NumPy
*Lesson: [LP01-06](P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md) ·
[LP02-02](P02-mathematics-for-ai/lessons/LP02-02-matrix-operations-and-multiplication.md)*

**Warm-up 3.1.** Create `np.arange(12).reshape(3, 4)`; print its shape, dtype and the second row.
**Standard 3.2.** Compute the column means of that array, then subtract them (broadcasting) and verify
each column now has mean ≈ 0.
**Stretch 3.3.** Given a 5×3 matrix of integers, return the rows whose sum is above the median row sum,
without a Python loop over rows.

**Guided exercise.** Multiply `A = np.array([[1, 2], [3, 4]])` by `B = np.array([[0, 1], [1, 0]])` using
`A @ B`, `A * B` and `np.outer(A[0], B[0])`. Which two results are the same shape, and why do the values
differ?

**Independent challenge.** Implement a single-layer linear model by hand: `y = X @ w + b` for a 100×4
`X`, then compute mean squared error against a target vector, and the gradient of the loss with respect
to `w`. Check your gradient with a numerical approximation (perturb one weight by 1e-4).

**Validation.** Column means after centring are within 1e-12 of zero; your analytic gradient matches the
numerical one to 1e-6.

**Hints.** `A.mean(axis=0)` reduces rows, not columns. For the gradient: `X.T @ (y_hat - y) * 2 / n`.

---

## 4. Pandas
*Lesson: [LP01-06](P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md) ·
[LP04-01](P04-data-preparation-and-visualization/lessons/LP04-01-dataset-structures-csv-and-json.md)*

**Warm-up 4.1.** Build a DataFrame with `name`, `age`, `score` for five people; print the rows where
`age > 25` and the mean score.
**Standard 4.2.** Add a column `passed = score >= 60`; then group by `passed` and report the count and
mean age.
**Stretch 4.3.** Sort by score, take the top three, and reset the index — showing before and after.

**Guided exercise.** With a `price` column stored as text (`"1,200"`, `"950"`, `"n/a"`), convert it to
numbers with `pd.to_numeric(..., errors="coerce")` after removing the comma. Print how many values became
missing and why that is better than a crash.

**Independent challenge.** Two frames — `students(name, id)` and `marks(id, subject, score)` — are joined
on `id`. Produce a table of mean score per student, keeping students with no marks (as `NaN`) and
reporting how many there are.

**Validation.** 4.2 reports two groups; the join keeps every student; you can state how many rows have
`NaN` and why.

**Hints.** `how="left"` keeps unmatched left rows. `groupby(...).agg(["count", "mean"])` gives both
numbers at once.

---

## 5. Data visualisation
*Lesson: [LP04-04](P04-data-preparation-and-visualization/lessons/LP04-04-visualization-and-exploratory-data-analysis.md)*

**Warm-up 5.1.** Plot a line of `[3, 5, 4, 8]` with labelled axes; save it to a file and reopen it.
**Standard 5.2.** Given 200 samples from a normal distribution (fixed seed), draw a histogram with 20 bins
and overlay the theoretical density.
**Stretch 5.3.** Draw a scatter of two correlated variables and add the line of best fit using the
least-squares slope you compute yourself.

**Guided exercise.** Make a bar chart of four category counts where one bar is much larger than the
others. Then switch the y-axis to a log scale and describe what became visible and what became misleading.

**Independent challenge.** Build a four-panel figure (2×2): histogram, box plot, scatter, and a cumulative
distribution. One sentence per panel saying what question it answers.

**Validation.** Every axis is labelled with units; the log-scale panel states its caveat; the file is
written and re-readable.

**Hints.** `fig, axes = plt.subplots(2, 2)`; index panels with `axes[0, 0]`. Use
`fig.savefig(..., dpi=150, bbox_inches="tight")`.

---

## 6. Linear algebra
*Lessons: [LP02-01](P02-mathematics-for-ai/lessons/LP02-01-scalars-vectors-matrices-and-tensors.md) ·
[LP02-02](P02-mathematics-for-ai/lessons/LP02-02-matrix-operations-and-multiplication.md) ·
[LP02-03](P02-mathematics-for-ai/lessons/LP02-03-transpose-inverse-and-eigenvalues.md)*

**Warm-up 6.1.** Compute the dot product of (1, 2, 3) and (4, 5, 6) by hand, then in NumPy, and state
what the sign means.
**Standard 6.2.** For `A = [[2, 0], [0, 3]]`, compute `A.T`, `A⁻¹` and the eigenvalues; verify
`A @ A⁻¹ = I`.
**Stretch 6.3.** Show that multiplying a vector by a matrix can change its direction but not the direction
of an eigenvector; demonstrate with one eigenvector of `A`.

**Guided exercise.** Compute the determinant of `[[4, 7], [2, 6]]` by hand, interpret it geometrically,
then invert the matrix and verify the product.

**Independent challenge.** Solve `Ax = b` for a 3×3 system three ways — `np.linalg.solve`, matrix inverse,
and elimination by hand — and report the largest disagreement.

**Validation.** `A @ A⁻¹` is identity to 1e-12; the eigenvector check shows parallel vectors; all three
solutions agree to 1e-10.

**Hints.** `np.linalg.eig` returns eigenvalues and eigenvectors as columns. Prefer `solve` over `inv` in
code: fewer operations, better conditioning.

---

## 7. Probability and statistics
*Lessons: [LP03-02](P03-probability-and-statistics/lessons/LP03-02-probability-rules-and-conditional-probability.md) ·
[LP03-03](P03-probability-and-statistics/lessons/LP03-03-bayes-theorem.md) ·
[LP03-04](P03-probability-and-statistics/lessons/LP03-04-random-variables-and-distributions.md)*

**Warm-up 7.1.** Two fair dice: compute `P(sum = 7)` and `P(sum = 7 | first die is 3)` by enumeration.
**Standard 7.2.** A test has 95% sensitivity and 90% specificity at 2% prevalence. Compute the posterior
and the number of false positives per 1,000 tests.
**Stretch 7.3.** Simulate 10,000 draws from that test, estimate the posterior empirically, and compare
with your analytic answer.

**Guided exercise.** With `random.seed(0)`, draw 500 samples from a normal distribution with mean 10 and
standard deviation 2. Report mean, standard deviation and the 90th percentile; compare with the
theoretical 90th percentile (10 + 2·1.2816).

**Independent challenge.** Estimate the standard error of the mean from a sample of 30, then show how it
shrinks when you take 300. State the relationship in one sentence.

**Validation.** 7.1 gives 6/36 and 1/6; 7.2 gives a posterior near 0.16 and about 98 false positives;
your simulation lands within 0.02 of the analytic value.

**Hints.** Prevalence × sensitivity is the true-positive mass; add (1−prevalence) × (1−specificity) for
false positives. Standard error is `s / sqrt(n)`.

---

## 8. Calculus and optimisation fundamentals
*Lessons: [LP02-04](P02-mathematics-for-ai/lessons/LP02-04-derivatives-partial-derivatives-and-gradients.md) ·
[LP02-05](P02-mathematics-for-ai/lessons/LP02-05-optimization-fundamentals.md)*

**Warm-up 8.1.** Differentiate `f(x) = 3x² + 2x − 5` and find where the slope is zero.
**Standard 8.2.** Implement gradient descent on that function from `x = 4` with learning rate 0.1 for 20
steps; print the first and last values.
**Stretch 8.3.** Repeat with learning rate 1.1 and explain the divergence in terms of the second
derivative.

**Guided exercise.** For `f(x, y) = x² + 3y²`, compute the gradient at (2, 1), take one step of size
0.1, and show the function value decreased.

**Independent challenge.** Minimise the same function by hand for three step sizes and plot
value-versus-step for each on one axis. State which step size you would choose and why.

**Validation.** 8.2 converges near `x = −1/3`; the divergent run grows without bound; your plot shows one
curve flattening and one rising.

**Hints.** The update is `x ← x − η f'(x)`. Divergence happens when `η > 2/L` where `L` is the curvature
(here 6).

---

## 9. Data preparation
*Lessons: [LP04-01](P04-data-preparation-and-visualization/lessons/LP04-01-dataset-structures-csv-and-json.md) ·
[LP04-02](P04-data-preparation-and-visualization/lessons/LP04-02-missing-values-and-duplicates.md) ·
[LP04-03](P04-data-preparation-and-visualization/lessons/LP04-03-outliers-normalization-and-standardization.md)*

**Warm-up 9.1.** Load a small CSV you write yourself with one missing value; report `isna().sum()`.
**Standard 9.2.** Remove duplicate rows, fill numeric missing values with the median, and print the shape
before and after each step.
**Stretch 9.3.** Standardise one column with z-scores, then verify mean ≈ 0 and standard deviation ≈ 1.

**Guided exercise.** Take `[10, 12, 11, 13, 12, 90]`. Compute the mean and median, identify the outlier
by the 1.5×IQR rule, and state which statistic you would report to a manager and why.

**Independent challenge.** Build a five-step cleaning pipeline as functions (load → dedupe → coerce types
→ handle missing → scale), each returning a new frame. Prove with `assert` that the output has no
duplicates, no missing values in required columns, and that row order is preserved.

**Validation.** 9.2 prints three shapes that differ only where expected; the IQR rule flags 90 only; your
pipeline asserts pass on a frame with deliberately inserted problems.

**Hints.** `df.duplicated().sum()` counts duplicates. For IQR: compute Q1/Q3 with `.quantile([0.25, 0.75])`
and flag outside `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`.

---

## Where this fits

These exercises are checks, not a curriculum. The main sequence is the four prerequisite sections, then
[M01](../modules/M01-introduction-and-foundations/README.md). If a topic here takes you more than fifteen
minutes per exercise, revisit its lesson before continuing — the modules assume these operations are
automatic.

**Navigation:** [Prerequisites](README.md) · [Diagnostic](diagnostic.md) · [Learning paths](../docs/learning-path.md) ·
[Course home](../README.md)
