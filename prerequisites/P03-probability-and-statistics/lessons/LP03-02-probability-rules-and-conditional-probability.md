# LP03-02 — Probability Rules and Conditional Probability

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Study time | 75 minutes |
| Prerequisites | [LP03-01](LP03-01-descriptive-statistics.md) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) |
| Lab | [LAB-P03-01](../labs/lab-p03-01-exam-score-report.md) |

[← Previous: Descriptive Statistics](LP03-01-descriptive-statistics.md) · [P03 home](../README.md) · [Next: Bayes' Theorem →](LP03-03-bayes-theorem.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Use** the three axioms and the complement rule to compute probabilities of simple events.
- **Apply** the addition rule for non-disjoint events without double-counting.
- **Compute** conditional probabilities from a two-way table, in both directions.
- **Distinguish** independent events from mutually exclusive events, and explain why confusing them is
  the most common error in this unit.

## 2. Prerequisite Knowledge

- Descriptive statistics and basic arithmetic: [LP03-01](LP03-01-descriptive-statistics.md).

## 3. Conceptual Explanation

### 3.1 Vocabulary that pays for itself

- **Experiment:** a procedure with an uncertain outcome (send an email, classify an image).
- **Sample space** $\Omega$: every possible outcome.
- **Event** $A$: a subset of $\Omega$; we ask for $P(A)$.

### 3.2 The axioms, and what follows

1. $P(A) \ge 0$.
2. $P(\Omega) = 1$.
3. For disjoint events, $P(A \cup B) = P(A) + P(B)$.

Everything else is derived:

$$
P(A^c) = 1 - P(A)
\qquad
P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

The subtraction in the second rule is not decoration: if $A$ and $B$ overlap, adding their
probabilities counts the overlap twice. When $A$ and $B$ are **disjoint** ($A \cap B = \emptyset$), the
subtracted term is zero and the axiom applies directly.

### 3.3 Conditional probability

$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) > 0
$$

Read it as "restrict the sample space to $B$, then ask what fraction of it is also $A$". Rearranged,
it gives the **multiplication rule**:

$$
P(A \cap B) = P(A \mid B)\,P(B) = P(B \mid A)\,P(A)
$$

Both forms are used constantly: the left when you know a conditional rate, the right when you have a
joint count and want the conditional.

### 3.4 Independence is a statement about conditionals

$A$ and $B$ are **independent** when knowing one tells you nothing about the other:

$$
P(A \mid B) = P(A)
\quad\Longleftrightarrow\quad
P(A \cap B) = P(A)P(B)
$$

Independence is a modelling assumption, not a default. Two coin flips are independent; two emails from
the same sender are not; two pixels in an image are definitely not.

**Disjoint is not independent.** Disjoint events are maximally *dependent*: if $A$ happened, $B$ cannot
have. The two ideas are almost opposites, and exam questions exploit the confusion.

### 3.5 Total probability

If $B_1, \dots, B_k$ partition the sample space (disjoint and covering everything), then

$$
P(A) = \sum_{i=1}^{k} P(A \mid B_i)\,P(B_i)
$$

This is how you compute an overall rate from subgroup rates — and it is the first half of Bayes'
theorem, which the next lesson completes.

## 4. Worked Examples

### Example 1 — a two-way table, both directions

200 emails, classified by whether they are spam and whether they contain the word "free":

| | Contains "free" | No "free" | Total |
| :--- | ---: | ---: | ---: |
| Spam | 54 | 6 | 60 |
| Not spam | 14 | 126 | 140 |
| **Total** | **68** | **132** | **200** |

$$
P(\text{spam}) = \frac{60}{200} = 0.30, \qquad
P(\text{free}) = \frac{68}{200} = 0.34
$$

$$
P(\text{spam} \mid \text{free}) = \frac{54}{68} \approx 0.794
\qquad
P(\text{free} \mid \text{spam}) = \frac{54}{60} = 0.90
$$

The two conditionals differ (0.794 vs 0.90) because they condition on different things. A spam filter
needs the first: given that a message contains "free", how likely is it spam? Reversing them is the
error that Bayes' theorem exists to correct.

Check the addition rule: $P(\text{spam} \cup \text{free}) = 0.30 + 0.34 - 0.27 = 0.37$, and counting
directly: $(60 + 68 - 54)/200 = 74/200 = 0.37$ ✓.

### Example 2 — independence, tested rather than assumed

From the table, $P(\text{spam}) \times P(\text{free}) = 0.30 \times 0.34 = 0.102$, while
$P(\text{spam} \cap \text{free}) = 0.27$. Since $0.27 \ne 0.102$, the events are **not** independent —
which is exactly why the word is a useful feature.

### Example 3 — total probability in a quality check

Two machines produce 60% and 40% of a factory's output; 2% and 5% respectively are defective.

$$
P(\text{defect}) = 0.6 \times 0.02 + 0.4 \times 0.05 = 0.012 + 0.020 = 0.032
$$

3.2% of all items are defective, a figure neither machine's rate predicts alone.

```python
p_defect = 0.6 * 0.02 + 0.4 * 0.05
print(round(p_defect, 4))
print(round(0.6 * 0.02 / p_defect, 3))   # share of defects from machine 1
```

```text
0.032
0.375
```

The second line is Bayes in action: only 37.5% of defects come from the machine with the lower defect
rate but the larger output.

## 5. Visual Explanation

```text
        Ω ┌───────────────────────────┐
          │   A ∩ B                   │
          │   ┌───────────┐           │
          │   │   54      │  A only 6 │
          │   └───────────┘           │
          │   B only 14  │  neither 126│
          └───────────────────────────┘

P(A|B) = area(A ∩ B) / area(B)
```

*Text description of the diagram:* the rectangle is the sample space, split into four cells by the two
questions. Conditioning on $B$ means keeping only the $B$ column and renormalising by its total (68), so
$P(A \mid B)$ is the 54 cell divided by 68 — not by 200.

## 6. Mathematical Formulation

$$
P(A^c) = 1 - P(A)
$$
$$
P(A \cup B) = P(A) + P(B) - P(A\cap B)
$$
$$
P(A \mid B) = \frac{P(A\cap B)}{P(B)}
$$
$$
A \perp B \iff P(A\cap B) = P(A)P(B)
$$
$$
P(A) = \sum_i P(A\mid B_i)P(B_i) \quad \text{for a partition } \{B_i\}
$$

Note the asymmetry of the conditional: $P(A\mid B) \ne P(B\mid A)$ in general, even though the joint
probability $P(A\cap B)$ is symmetric. That single asymmetry accounts for a large share of real-world
reasoning errors, from medical screening to legal testimony.

## 7. Python Implementation

```python
"""Conditional probabilities from counts — always compute from the table, not from memory."""
import numpy as np

# rows: spam, not spam; columns: contains "free", no "free"
counts = np.array([[54, 6],
                   [14, 126]])

total = counts.sum()
joint = counts / total

p_spam = joint[0].sum()
p_free = joint[:, 0].sum()

print("P(spam)          =", round(p_spam, 3))
print("P(free)          =", round(p_free, 3))
print("P(spam and free) =", round(joint[0, 0], 3))
print("P(spam | free)   =", round(joint[0, 0] / p_free, 3))
print("P(free | spam)   =", round(joint[0, 0] / p_spam, 3))
print("independent?     ", np.isclose(joint[0, 0], p_spam * p_free))
```

**Output**

```text
P(spam)          = 0.3
P(free)          = 0.34
P(spam and free) = 0.27
P(spam | free)   = 0.794
P(free | spam)   = 0.9
independent?      False
```

Dividing the joint table by its total and then slicing is the safest habit: every marginal and
conditional can be read off one array, and no count is retyped.

## 8. Practical Applications

- **Classifier metrics.** Precision is $P(\text{true positive} \mid \text{predicted positive})$; recall
  is $P(\text{predicted positive} \mid \text{true positive})$. They are the two conditionals of Example
  1 with different labels, and they are not interchangeable.
- **Reliability.** System failure rates combine component failure rates through the total probability
  rule, weighted by usage.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Adding probabilities of overlapping events | Sum above 1 | Double-counted intersection | Subtract $P(A\cap B)$ |
| Swapping $P(A\mid B)$ and $P(B\mid A)$ | Wildly wrong conclusion | Conditionals are asymmetric | Use Bayes (next lesson) |
| Calling disjoint events independent | Contradiction | Confusing exclusive with unrelated | Check $P(A\cap B)=P(A)P(B)$ |
| Conditioning on a zero-probability event | `ZeroDivisionError` | $P(B)=0$ | The conditional is undefined |

## 10. Self-Assessment

**1.** $P(A) = 0.5$, $P(B) = 0.4$, $P(A \cap B) = 0.2$. Are $A$ and $B$ independent? What is
$P(A \cup B)$?
<details><summary>Show answer</summary>

$P(A)P(B) = 0.2 = P(A\cap B)$, so they are independent. $P(A\cup B) = 0.5 + 0.4 - 0.2 = 0.7$.
</details>

**2.** A test is positive for 90% of sick people and 8% of healthy people. Does that mean a positive
test implies a 90% chance of illness?
<details><summary>Show answer</summary>

No. 0.90 is $P(\text{positive}\mid\text{sick})$; the question asks for
$P(\text{sick}\mid\text{positive})$, which also depends on how common the illness is. That is Bayes'
theorem, next lesson.
</details>

**3.** Two events have $P(A\cap B) = 0$. Can they be independent?
<details><summary>Show answer</summary>

Only if $P(A) = 0$ or $P(B) = 0$. Otherwise $P(A)P(B) > 0 \ne 0$, so they are dependent — indeed
maximally so.
</details>

**4.** A patient has a 30% chance of needing test A, and if so a 40% chance of needing test B; if not,
a 10% chance. What is the overall probability of needing B?
<details><summary>Show answer</summary>

$0.3 \times 0.4 + 0.7 \times 0.1 = 0.12 + 0.07 = 0.19$. Total probability, with the two cases as the
partition.
</details>

## 11. Further Reading

- [Seeing Theory, Ch. 1–2](https://seeing-theory.brown.edu/) — interactive probability, including conditional probability.
- [OpenStax Introductory Statistics 2e, Ch. 3](https://openstax.org/books/introductory-statistics-2e/pages/3-introduction) — two-way tables and the rules used here.

## Mini-Lab

Build a two-way table of 300 records for two binary attributes of your choice (for example, "studied
more than 5 hours" and "passed"). Compute both conditionals and test independence. Then change ten
counts so that the attributes become independent and confirm that $P(A\cap B) = P(A)P(B)$ holds to
rounding.

## What to Do Next

Continue to [LP03-03 Bayes' Theorem](LP03-03-bayes-theorem.md).
