# Prerequisite Diagnostic

**Time: 90 minutes · 40 questions · closed book, calculator allowed**

[← Prerequisites home](README.md) · [Course home](../README.md)

This diagnostic checks whether you are ready for Module 01. It is not graded and nothing is submitted.
Work through it without notes; the point is to find out what you actually know, not what you can look up.

**How to use it**

1. Answer all 40 questions on paper, writing your reasoning, not only the final number.
2. Mark your answers against the key in §Answers, one point per question.
3. Read §What your score means and follow the recommendation for your weakest section.
4. Revisit only the sections you missed — do not reread all four units.

Questions are grouped by section, and each group links back to the lessons that cover it. Ten questions
per section means a weak section is visible immediately.

## Section A — Python Programming (10 points)

Covers [P01](P01-python-programming/README.md).

**A1.** What does `17 // 5` return, and what does `17 % 5` return?

**A2.** Why is `0.1 + 0.2 == 0.3` false, and what should you use instead?

**A3.** `values = [3, 1, 2]`. Write a one-line expression that returns the same list sorted, without
modifying `values`.

**A4.** What does this print, and why?

```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add(1), add(2))
```

**A5.** Rewrite as a list comprehension: a loop over `range(10)` that appends `x**2` only when `x` is
odd.

**A6.** For `a = np.array([1, 2, 3])`, what is `a * 2`? What would `[1, 2, 3] * 2` give instead?

**A7.** A DataFrame has 100 rows and 5 columns. What is the shape of `df.mean(axis=0)`? What does it
represent?

**A8.** You read a CSV and `int(df.loc[0, "score"])` raises `ValueError`. Name two likely causes.

**A9.** What does `with open(path, encoding="utf-8") as f:` guarantee that `f = open(path)` does not?

**A10.** Why is `except Exception: pass` a bad habit, in one sentence?

## Section B — Mathematics for AI (10 points)

Covers [P02](P02-mathematics-for-ai/README.md).

**B1.** What is the shape of a batch of 8 colour images of 32×32 pixels? How many scalars does it hold?

**B2.** $\mathbf{a} = (1, 2)$, $\mathbf{b} = (2, 1)$. Compute $\mathbf{a}\cdot\mathbf{b}$ and the cosine of
the angle between them.

**B3.** $A$ is $3\times4$, $B$ is $4\times2$. Give the shapes of $AB$ and $BA$, or say which is undefined.

**B4.** Compute $AB$ for $A = \begin{bmatrix}1&2\\3&4\end{bmatrix}$, $B = \begin{bmatrix}5&6\\7&8\end{bmatrix}$.

**B5.** For $A = \begin{bmatrix}4&7\\2&6\end{bmatrix}$, compute the determinant and the inverse.

**B6.** Find the eigenvalues of $\begin{bmatrix}2&1\\1&2\end{bmatrix}$ and verify the trace identity.

**B7.** $f(x,y) = x^2y + 3y$. Write $\nabla f$ and evaluate it at $(2, 1)$.

**B8.** Differentiate $h(x) = (3x+1)^2$ with the chain rule and evaluate at $x = 1$.

**B9.** In gradient descent, why do we subtract the gradient rather than add it?

**B10.** For $f(x) = x^2$ with $\eta = 1.5$ starting at $x_0 = 4$, compute $x_1$ and $x_2$. Does the
sequence converge?

## Section C — Probability and Statistics (10 points)

Covers [P03](P03-probability-and-statistics/README.md).

**C1.** Data: $3, 5, 5, 7, 20$. Compute the mean and the median. Which better describes a typical value?

**C2.** Why does the sample variance divide by $n-1$ rather than $n$?

**C3.** $P(A) = 0.5$, $P(B) = 0.4$, $P(A\cap B) = 0.2$. Compute $P(A\cup B)$ and decide whether $A$ and
$B$ are independent.

**C4.** Write the definition of $P(A\mid B)$ and explain why it differs from $P(B\mid A)$.

**C5.** A disease affects 2% of a population. A test has sensitivity 90% and a false-positive rate of
10%. Compute $P(\text{disease}\mid\text{positive})$.

**C6.** $X$ takes values 0, 1, 2 with probabilities 0.5, 0.3, 0.2. Compute $\mathbb{E}[X]$ and
$\operatorname{Var}(X)$.

**C7.** $X \sim \text{Binomial}(20, 0.1)$. Give $\mathbb{E}[X]$ and the standard deviation.

**C8.** Scores are $\mathcal{N}(500, 100^2)$. What fraction lie between 400 and 700? Use $\Phi(2)\approx
0.977$ and $\Phi(-1) \approx 0.159$.

**C9.** A sample of 400 has standard deviation 20. Compute the standard error of the mean. What sample
size would halve it?

**C10.** A test reports p = 0.03. State what that means and one thing it does not mean.

## Section D — Data Preparation and Visualisation (10 points)

Covers [P04](P04-data-preparation-and-visualization/README.md).

**D1.** State the three rules of tidy data.

**D2.** A table has columns `id, jan, feb, mar`. Is it tidy? What would you do?

**D3.** Name two reasons a numeric-looking CSV column loads as text.

**D4.** Distinguish MCAR, MAR and MNAR with one example each.

**D5.** Why must an imputation statistic be computed on the training split only?

**D6.** Two rows share an `id` but have different scores. Are they duplicates? What do you do?

**D7.** Data: $4, 5, 6, 7, 8, 9, 40$. Compute $Q_1$, $Q_3$, the IQR and the upper fence. Is 40 flagged?

**D8.** Explain why one extreme value can hide itself from the z-score rule.

**D9.** Give the formulas for min-max scaling and standardisation, and one situation where each is
preferred.

**D10.** You want to compare the spread of scores across four cities. Which chart, and why not a bar
chart of means?

## Answers

Mark one point per correct answer; partial credit is not the point here.

### Section A

1. `3` and `2`. Since $17 = 5\times3 + 2$.
2. Binary floating point cannot represent 0.1 exactly, so the sum carries a small error. Use
   `math.isclose(a, b)` or compare with a tolerance.
3. `sorted(values)` — `values.sort()` would modify the list in place and return `None`.
4. `[1, 2] [1, 2]`. The default list is created once at definition time and shared across calls.
5. `[x**2 for x in range(10) if x % 2 == 1]`.
6. `array([2, 4, 6])` — elementwise. The list gives `[1, 2, 3, 1, 2, 3]` because `*` repeats.
7. Shape `(5,)`: one mean per column, i.e. per feature across the 100 rows.
8. Whitespace or a thousands separator, and a missing-value marker such as `""` or `"NA"`.
9. It closes the file even if an exception occurs, and it applies UTF-8 explicitly rather than the
   platform default.
10. It turns every failure — including typos and logic errors — into silent continuation, destroying the
    traceback that would have explained it.

### Section B

1. `(8, 32, 32, 3)`, containing $8 \times 32 \times 32 \times 3 = 24\,576$ scalars.
2. $\mathbf{a}\cdot\mathbf{b} = 1\cdot2 + 2\cdot1 = 4$; $\cos\theta = 4/(\sqrt5\sqrt5) = 0.8$.
3. $AB$ is $3\times2$; $BA$ is undefined (inner dimensions 2 and 3 do not match).
4. $\begin{bmatrix}19&22\\43&50\end{bmatrix}$.
5. $\det = 24 - 14 = 10$; $A^{-1} = \begin{bmatrix}0.6&-0.7\\-0.2&0.4\end{bmatrix}$.
6. $\lambda = 3$ and $\lambda = 1$; $3 + 1 = 4 = \operatorname{trace}$.
7. $\nabla f = (2xy,\ x^2+3)$, which is $(4, 7)$ at $(2,1)$.
8. $6(3x+1) = 18x + 6$, so 24 at $x = 1$.
9. Because the gradient points in the direction of steepest *increase*; subtracting moves downhill.
10. $x_1 = 4 - 1.5\cdot8 = -8$; $x_2 = -8 - 1.5\cdot(-16) = 16$. The sequence diverges ($\eta$ exceeds
    $2/L = 1$).

### Section C

1. Mean $= 40/5 = 8$; median $= 5$. The median, because the single 20 pulls the mean.
2. Because deviations are measured from the sample mean, which is fitted to the data; the $n-1$
   denominator corrects the resulting downward bias.
3. $P(A\cup B) = 0.5 + 0.4 - 0.2 = 0.7$. Independent, since $P(A)P(B) = 0.2 = P(A\cap B)$.
4. $P(A\mid B) = P(A\cap B)/P(B)$. Conditioning on a different event restricts the sample space
   differently, so the two conditionals are generally unequal.
5. $P(+) = 0.9\times0.02 + 0.1\times0.98 = 0.018 + 0.098 = 0.116$; posterior $= 0.018/0.116 \approx
   0.155$.
6. $\mathbb{E}[X] = 0.7$; $\mathbb{E}[X^2] = 1.1$; $\operatorname{Var} = 1.1 - 0.49 = 0.61$.
7. Mean $= 2$; standard deviation $= \sqrt{20\times0.1\times0.9} = \sqrt{1.8} \approx 1.34$.
8. $\Phi(2) - \Phi(-1) = 0.977 - 0.159 = 0.818$, about 82%.
9. $20/\sqrt{400} = 1.0$; to halve it, $n = 1600$.
10. If $H_0$ were true, data at least as extreme would occur 3% of the time. It is **not** the
    probability that $H_0$ is true, and not the probability that your hypothesis is right.

### Section D

1. Each row one observation, each column one variable, each cell one value.
2. No — the month is a variable stored in column names. Melt to `id, month, value`.
3. A thousands separator (`"1,200"`), a percent sign or other unit, or a missing marker that stops
   numeric inference.
4. **MCAR:** a sensor packet was dropped, unrelated to any variable. **MAR:** older respondents skip the
   income question, so missingness depends on an observed variable. **MNAR:** high earners refuse to
   state income, so missingness depends on the unobserved value itself.
5. Otherwise test information enters the statistic, so measured performance is optimistic — the classic
   silent leak.
6. Not duplicates: a conflict. Keep both, or apply a stated rule (latest timestamp, highest value) and
   record it.
7. $Q_1 = 5$, $Q_3 = 9$, IQR $= 4$, upper fence $= 15$. Yes, 40 is flagged.
8. Because the standard deviation is computed including the extreme value, so the denominator grows and
   every z-score — including the outlier's — shrinks.
9. Min-max: $(x - x_{\min})/(x_{\max} - x_{\min})$; standardise: $(x-\bar{x})/s$. Min-max for bounded
   inputs such as pixel intensities; standardisation for distance- and gradient-based models.
10. A boxplot per city: it shows median, quartiles and spread, so small groups are visibly thin. A bar of
    means hides spread and makes a group of three look as solid as a group of three hundred.

## What your score means

| Score | Reading | What to do |
| :--- | :--- | :--- |
| 36–40 | Ready | Start [Module 01](../modules/README.md#m01). Keep this sheet for reference. |
| 30–35 | Ready with gaps | Start M01, but redo the lessons behind every missed question in the first two weeks. |
| 20–29 | Not yet | Revisit the section where you lost the most points, then retake the diagnostic after the unit's lab. |
| Below 20 | Foundation needed | Work through the two weakest units in full, including notebooks and labs, before starting M01. |

**Section-level rule.** Regardless of total score, if you score **below 6 of 10** in any one section,
complete that unit's lab before Module 02. Module 02 assumes all four.

## Where to go next

| Weakest section | Go to |
| :--- | :--- |
| A — Python | [P01](P01-python-programming/README.md) · [LP01-04](P01-python-programming/lessons/LP01-04-functions-and-collections.md) · [NB-P01-02](P01-python-programming/notebooks/nb-p01-02-numpy-pandas-plotting.ipynb) |
| B — Mathematics | [P02](P02-mathematics-for-ai/README.md) · [LP02-04](P02-mathematics-for-ai/lessons/LP02-04-derivatives-partial-derivatives-and-gradients.md) · [LAB-P02-02](P02-mathematics-for-ai/labs/lab-p02-02-gradient-descent-by-hand.md) |
| C — Probability | [P03](P03-probability-and-statistics/README.md) · [LP03-03](P03-probability-and-statistics/lessons/LP03-03-bayes-theorem.md) · [LAB-P03-01](P03-probability-and-statistics/labs/lab-p03-01-exam-score-report.md) |
| D — Data preparation | [P04](P04-data-preparation-and-visualization/README.md) · [LP04-02](P04-data-preparation-and-visualization/lessons/LP04-02-missing-values-and-duplicates.md) · [LAB-P04-01](P04-data-preparation-and-visualization/labs/lab-p04-01-messy-survey-cleanup.md) |

A score of 40/40 means you know the material; it does not mean you can skip the labs. The labs are where
the material becomes a habit.
