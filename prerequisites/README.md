# Prerequisites

Four preparation sections: **Python programming**, **mathematics for AI**, **probability and statistics**,
and **data preparation and visualisation**. Together they take about **56 hours**, and they exist
because every module assumes them without apology.

This is not gatekeeping. Each idea here reappears within the first ten minutes of the module that needs
it, and the course would rather spend an hour on it now than lose you in M06.

**Course home:** [README](../README.md) · **Learning paths:** [learning-path.md](../docs/learning-path.md) ·
**Modules:** [modules/README.md](../modules/README.md) · **Diagnostic:** [diagnostic.md](diagnostic.md) ·
**Practice exercises:** [EXERCISES.md](EXERCISES.md)

## The four sections

| Section | Hours | Lessons | Notebooks | Lab | Start here if |
| :--- | ---: | ---: | ---: | :--- | :--- |
| [P01 — Python Programming](P01-python-programming/README.md) | 14 | 6 | 2 | [LAB-P01-01](P01-python-programming/labs/lab-p01-01-student-results-analysis.md) | You have never written code |
| [P02 — Mathematics for AI](P02-mathematics-for-ai/README.md) | 24 | 5 | 2 | 2 labs | Matrices or derivatives are unfamiliar |
| [P03 — Probability and Statistics](P03-probability-and-statistics/README.md) | 10 | 6 | 1 | [LAB-P03-01](P03-probability-and-statistics/labs/lab-p03-01-exam-score-report.md) | You have not studied probability |
| [P04 — Data Preparation and Visualisation](P04-data-preparation-and-visualization/README.md) | 8 | 4 | 1 | [LAB-P04-01](P04-data-preparation-and-visualization/labs/lab-p04-01-messy-survey-cleanup.md) | You have not cleaned a dataset |
| **Total** | **56** | **21** | **6** | **5** | |

Each section follows the same shape: lessons you read and work through, a notebook you run, a lab you
build. The lessons are written to be read in order, and every one ends with self-assessment questions
and a small lab scenario.

## Are you ready? A ten-question self-check

Answer on paper, without looking anything up. Then open the answers. This is a warm-up; the real check
is the [diagnostic](diagnostic.md) at the end of the four sections.

**1.** What does `17 // 5` evaluate to, and what does `17 % 5` evaluate to?
<details><summary>Answer</summary>

`3` and `2` — floor division and remainder, two halves of the identity $17 = 5\times3 + 2$.
</details>

**2.** When would you use a dictionary rather than a list?
<details><summary>Answer</summary>

When you look something up *by name* rather than by position: `{"student": "Ali", "marks": 87}`.
Dictionaries give fast lookup by key; lists give ordered access by index.
</details>

**3.** Compute $\begin{bmatrix}1 & 2\\3 & 4\end{bmatrix}\begin{bmatrix}1\\0\end{bmatrix}$.
<details><summary>Answer</summary>

$\begin{bmatrix}1\\3\end{bmatrix}$ — each output entry is a row of the matrix dotted with the column.
</details>

**4.** What is the dot product of $(1, 2)$ and $(3, 4)$, and what does its sign tell you?
<details><summary>Answer</summary>

$1\cdot3 + 2\cdot4 = 11$. It is positive, so the angle between the vectors is acute — they point roughly
the same way.
</details>

**5.** A test is 90% sensitive and the disease affects 1% of people; the false-positive rate is 10%.
What is $P(\text{disease}\mid\text{positive})$?
<details><summary>Answer</summary>

About **8.3%**. Of 1 000 people, 10 have the disease and 9 of them test positive; 990 do not, and 99 of
them test positive. So 9 of 108 positives are true — 8.3%. Base rates dominate.
</details>

**6.** Differentiate $f(x) = x^3 + 2x$.
<details><summary>Answer</summary>

$f'(x) = 3x^2 + 2$ — the slope, i.e. how much the output changes per unit change of the input.
</details>

**7.** If a function's derivative at a point is positive, which direction decreases the function?
<details><summary>Answer</summary>

The negative direction — step against the gradient. That is the whole of gradient descent.
</details>

**8.** In pandas, how do you select the rows of `df` where `age` is greater than 30?
<details><summary>Answer</summary>

`df[df["age"] > 30]` — a boolean mask applied to the frame.
</details>

**9.** What does a standard deviation of 0 tell you about a set of numbers?
<details><summary>Answer</summary>

That every value is identical: there is no spread around the mean.
</details>

**10.** A CSV column of prices loads as text. Name one likely cause and the function you would use to
convert it.
<details><summary>Answer</summary>

A thousands separator or a currency symbol, e.g. `"1,200"`. Remove the character and apply
`pd.to_numeric(..., errors="coerce")` so unconvertible values become missing rather than raising.
</details>

**Scoring.** Eight or more correct: skim the sections and take the [diagnostic](diagnostic.md). Five to
seven: work through the sections covering your misses. Four or fewer: start at
[P01](P01-python-programming/README.md) and work in order — the sections build on each other.

## Suggested orders

| Your background | Order |
| :--- | :--- |
| Complete beginner | P01 → P02 → P03 → P04, with each notebook as you finish its lessons |
| Programmer, weak mathematics | P01 (skim) → P02 → P03 → P04 |
| Strong mathematics, new to Python | P01 → P02 (skim) → P04, then P03 |
| Some statistics, no data work | P04 → P03 → P01 (skim) → P02 |

The [diagnostic](diagnostic.md) is designed to be taken **after** all four sections. If you believe you
already know the material, take it first — it will tell you which sections to skip, and which to read
anyway.

## How to study mathematics without suffering

1. **Do not read mathematics; write it.** Copy each symbol table and each worked example by hand.
   Notation becomes familiar through production, not exposure.
2. **Say the formula in words.** "$f'(x) = 3x^2 + 2$" is "the slope is three times the square of x, plus
   two". If you cannot say it, you do not have it.
3. **Use small numbers.** Verify every matrix operation on 2×2 examples before trusting code.
4. **Implement it in NumPy immediately.** Ten lines of code make a definition concrete in a way another
   paragraph cannot.
5. **Accept partial understanding and move on.** Mathematics is learned in layers; the second pass is
   always easier, and it needs the first pass to have happened.

## If you already know some of it

Skip on evidence, not optimism. Take the [diagnostic](diagnostic.md); if a section scores 8 or better,
you may skip its lessons but still do its lab — the lab is where knowledge becomes a habit. If a section
scores below 6, work through it in full, including the notebook.

What you should not skip even if you are confident: **the chain rule** in
[LP02-04](P02-mathematics-for-ai/lessons/LP02-04-derivatives-partial-derivatives-and-gradients.md), and
**the base-rate lesson** in
[LP03-03](P03-probability-and-statistics/lessons/LP03-03-bayes-theorem.md). M06 and M07 use both
constantly.

## Where to go next

- **Finished all four sections?** Take the [diagnostic](diagnostic.md), then start
  [M01: Introduction and Foundations](../modules/README.md#m01).
- **Want a schedule?** [Learning paths](../docs/learning-path.md)
- **Unfamiliar term?** [Glossary](../resources/glossary.md)
- **Need a textbook?** [Books](../resources/books.md) — including free online texts for every section

**Navigation:** [Course home](../README.md) · [Learning paths](../docs/learning-path.md) ·
[Modules](../modules/README.md) · [Course roadmap](../docs/course-roadmap.md) ·
[Glossary](../resources/glossary.md) · [FAQ](../docs/faq.md)
