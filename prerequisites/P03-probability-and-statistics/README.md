# P03 — Probability and Statistics

**Level 100 · 10 hours · 6 lessons, 1 notebook, 1 lab**

[← Previous unit: P02](../P02-mathematics-for-ai/README.md) · [Next unit: P04 Data Preparation →](../P04-data-preparation-and-visualization/README.md)

How to describe data, reason about uncertainty, and decide whether a difference is real. The emphasis
is on the handful of ideas that appear in every machine-learning paper — variance, conditional
probability, Bayes' theorem, the normal and binomial distributions, standard error, correlation, and
the meaning of a p-value — each introduced with a worked number rather than a derivation.

## Who this unit is for

- **No statistics background:** read in order; the lessons assume only arithmetic and the mean.
- **Some statistics, no probability:** LP03-02 to LP03-04 are the parts that get used most in modelling.
- **Comfortable with both:** read LP03-05 and LP03-06 closely and then do the lab; the sampling and
  error material is where practical mistakes concentrate.

## Learning outcomes

By the end of P03 you can:

1. Summarise a column with the right centre and spread, and justify the choice for skewed data.
2. Compute conditional probabilities from a table and state the difference between
   $P(A\mid B)$ and $P(B\mid A)$.
3. Apply Bayes' theorem to a screening problem and explain the base-rate fallacy with numbers.
4. Use the binomial and normal distributions, including standardisation and the empirical rule.
5. Compute a standard error, build a confidence interval, and interpret a p-value and an effect size
   without over-claiming.

These outcomes support **M05, M06 and M10** (classification metrics, model evaluation, probabilistic
reasoning) and every discussion of uncertainty later in the programme.

## Lessons

| ID | Lesson | Time | Focus |
| :--- | :--- | ---: | :--- |
| [LP03-01](lessons/LP03-01-descriptive-statistics.md) | Descriptive Statistics | 75 min | Mean, median, mode, variance, IQR, skew |
| [LP03-02](lessons/LP03-02-probability-rules-and-conditional-probability.md) | Probability Rules and Conditional Probability | 75 min | Axioms, addition rule, independence, two-way tables |
| [LP03-03](lessons/LP03-03-bayes-theorem.md) | Bayes' Theorem | 75 min | Prior, likelihood, posterior, base rates, sequential updates |
| [LP03-04](lessons/LP03-04-random-variables-and-distributions.md) | Random Variables and Distributions | 75 min | Expectation, variance, binomial, normal, $\Phi$ |
| [LP03-05](lessons/LP03-05-sampling-correlation-and-covariance.md) | Sampling, Covariance and Correlation | 60 min | Standard error, central limit theorem, $r$, sampling bias |
| [LP03-06](lessons/LP03-06-hypothesis-testing-fundamentals.md) | Hypothesis Testing Fundamentals | 60 min | $t$ statistic, p-values, error types, power, effect size |

## Notebook

[NB-P03-01 — Probability and Statistics](notebooks/nb-p03-01-probability-and-statistics.ipynb) pairs with
all six lessons: descriptive summaries and histograms, simulated dice and conditional counts, a Bayes
update table, binomial and normal simulations, sampling distributions, and a permutation test. Every
simulation uses a fixed seed so the printed numbers match the lesson.

## Lab

[LAB-P03-01 — Exam Score Report](labs/lab-p03-01-exam-score-report.md) (1.5 h) turns a small score table
into a defensible report: summary statistics with the right centre, a distribution plot, a group
comparison, and a significance test whose conclusion is stated with its uncertainty.

## Time budget

| Activity | Hours |
| :--- | ---: |
| Six lessons | 7.0 |
| Notebook | 1.5 |
| Lab | 1.5 |
| **Total** | **10.0** |

This is the shortest unit and the one most often rushed. Read LP03-03 and LP03-06 twice: the base-rate
error and the misreading of p-values are the two mistakes that survive into professional work.

## How to check yourself

The self-assessment questions are numeric wherever possible, because the concepts are easy to nod along
to and harder to compute. If you can reproduce the worked examples without looking — the 17% posterior,
the 10 000-person table, the $t = 1.875$ — you have the unit.

## Common sticking points

- **Population versus sample formulas.** `ddof=0` in NumPy, `ddof=1` in pandas. Say which you used.
- **Conditional direction.** Precision and recall are the two conditionals of the same table; neither
  substitutes for the other.
- **p-value meaning.** It is $P(\text{data} \mid H_0)$, not $P(H_0 \mid \text{data})$.
- **Correlation of a curve.** $r \approx 0$ does not mean no relationship; plot before concluding.

## Next

Continue to [P04 — Data Preparation and Visualisation](../P04-data-preparation-and-visualization/README.md).
