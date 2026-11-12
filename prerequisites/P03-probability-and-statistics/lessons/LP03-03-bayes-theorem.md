# LP03-03 — Bayes' Theorem

| Unit | P03 · Probability and Statistics |
| :--- | :--- |
| Level | 100 |
| Study time | 75 minutes |
| Prerequisites | [LP03-02](LP03-02-probability-rules-and-conditional-probability.md) |
| Notebook | [NB-P03-01](../notebooks/nb-p03-01-probability-and-statistics.ipynb) |
| Lab | [LAB-P03-01](../labs/lab-p03-01-exam-score-report.md) |

[← Previous: Probability Rules](LP03-02-probability-rules-and-conditional-probability.md) · [P03 home](../README.md) · [Next: Random Variables and Distributions →](LP03-04-random-variables-and-distributions.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **State** Bayes' theorem and name each of its four terms: prior, likelihood, evidence, posterior.
- **Compute** a posterior probability from a base rate and a test's sensitivity and specificity.
- **Explain** the base-rate fallacy, with numbers, in one paragraph.
- **Update** a belief sequentially as new evidence arrives, and see why the order does not matter.

## 2. Prerequisite Knowledge

- Conditional probability, the multiplication rule and total probability:
  [LP03-02](LP03-02-probability-rules-and-conditional-probability.md).

## 3. Conceptual Explanation

### 3.1 The theorem is just the multiplication rule, twice

Since $P(A\cap B) = P(A\mid B)P(B) = P(B\mid A)P(A)$, dividing by $P(B)$ gives

$$
P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}
$$

With a partition $\{A, A^c\}$ and the total probability rule,
$P(B) = P(B\mid A)P(A) + P(B\mid A^c)P(A^c)$, so the fully explicit form is

$$
P(A \mid B) = \frac{P(B\mid A)\,P(A)}
{P(B\mid A)\,P(A) + P(B\mid A^c)\,P(A^c)}
$$

There is no new mathematics here. What is new is the *habit*: the probability you have is usually
$P(\text{evidence}\mid\text{hypothesis})$, and the probability you want is
$P(\text{hypothesis}\mid\text{evidence})$. They are different, and only Bayes converts one into the
other.

### 3.2 The four terms

| Term | Symbol | Meaning |
| :--- | :--- | :--- |
| Prior | $P(A)$ | What you believed before seeing the evidence |
| Likelihood | $P(B\mid A)$ | How well the hypothesis predicts the evidence |
| Evidence | $P(B)$ | How common the evidence is overall |
| Posterior | $P(A\mid B)$ | What you believe after |

The posterior is proportional to prior × likelihood; the evidence is only a normalising constant. In
machine learning, "prior" is the class balance, "likelihood" is the model's per-class score, and the
posterior is what a calibrated classifier should output.

### 3.3 The base-rate fallacy

A rare condition with a fairly accurate test produces mostly false positives, because there are so
many healthy people. This is not a paradox and not a flaw in the test: it is arithmetic. If you forget
the base rate, you will over-estimate the posterior dramatically — the classic error in screening
programmes, fraud alerts, and intrusion detection.

### 3.4 Sequential updating

Evidence can be applied one item at a time: today's posterior becomes tomorrow's prior. Because
multiplication is commutative, the final belief is the same whatever order the evidence arrives in —
a property that makes online learning and streaming filters possible.

Naive Bayes classifiers use exactly this: assume features are conditionally independent given the
class, multiply their likelihoods, and pick the class with the largest posterior. The independence
assumption is usually false, and the classifier still works well — worth remembering as evidence that
a model can be useful without being true.

## 4. Worked Examples

### Example 1 — a screening test, with the base rate

A disease affects 1% of a population. A test detects 99% of cases (sensitivity) and correctly clears
95% of healthy people (specificity, so the false-positive rate is 5%).

Let $D$ be "has the disease" and $+$ be "tests positive".

$$
P(D) = 0.01, \quad P(+\mid D) = 0.99, \quad P(+\mid D^c) = 0.05
$$

$$
P(+) = 0.99 \times 0.01 + 0.05 \times 0.99 = 0.0099 + 0.0495 = 0.0594
$$

$$
P(D \mid +) = \frac{0.0099}{0.0594} \approx 0.1667
$$

So a positive result means about a **17%** chance of disease, not 99%. Of 10 000 people: 100 are sick,
99 of them test positive; 9 900 are healthy, 495 of them test positive. Among 594 positives, 99 are
true — one in six.

```python
prior, sens, fpr = 0.01, 0.99, 0.05
evidence = sens * prior + fpr * (1 - prior)
posterior = sens * prior / evidence
print(round(evidence, 4), round(posterior, 4))
```

```text
0.0594 0.1667
```

### Example 2 — a second, independent test

The posterior 0.1667 becomes the new prior. A second positive result:

$$
P(D\mid +,+)=\frac{0.99 \times 0.1667}{0.99 \times 0.1667 + 0.05 \times 0.8333}
= \frac{0.165}{0.2067} \approx 0.798
$$

Now the chance is about 80%. One test was weak evidence; two are strong. This is how evidence
accumulates, and why a single screening result is rarely a diagnosis.

```python
post1 = posterior
post2 = sens * post1 / (sens * post1 + fpr * (1 - post1))
print(round(post2, 3))
```

```text
0.798
```

### Example 3 — odds form, which is easier to reason with

$$
\underbrace{\frac{P(D\mid +)}{P(D^c\mid +)}}_{\text{posterior odds}}
= \underbrace{\frac{P(D)}{P(D^c)}}_{\text{prior odds}}
\times \underbrace{\frac{P(+\mid D)}{P(+\mid D^c)}}_{\text{likelihood ratio}}
$$

Prior odds $= 0.01/0.99 \approx 0.0101$; likelihood ratio $= 0.99/0.05 = 19.8$; posterior odds
$\approx 0.2$, i.e. $0.2/(1+0.2) \approx 0.167$ ✓. Multiplying odds is often faster than computing the
evidence term, and it makes clear that a likelihood ratio of 20 cannot rescue a prior odds of 1:100.

## 5. Visual Explanation

```text
10 000 people
├── 100 sick ──────── 99 test +      ← true positives
│                      1 test −
└── 9 900 healthy ── 495 test +      ← false positives
                   9 405 test −

            99 true positives
P(sick|+) = ─────────────────── = 0.167
            99 + 495 positives
```

*Text description of the diagram:* the population splits by disease status, then each branch splits by
test result. The posterior is the ratio of the true-positive branch to all positives. The visual makes
the base rate impossible to ignore: the huge healthy branch generates five times as many positives as
the small sick branch.

## 6. Mathematical Formulation

$$
P(A\mid B) = \frac{P(B\mid A)P(A)}{P(B)},
\qquad
P(B) = \sum_{i} P(B\mid A_i)P(A_i)
$$

In log form, which is how it is implemented to avoid underflow when many likelihoods multiply:

$$
\log P(A\mid B) = \log P(B\mid A) + \log P(A) - \log P(B)
$$

The $-\log P(B)$ is the same for every hypothesis, so classification can skip it entirely: compare
$\log P(B\mid A_i) + \log P(A_i)$ and take the largest. That is a naive Bayes classifier in one line.

## 7. Python Implementation

```python
"""Bayes update as a reusable function, with a small sensitivity sweep."""
def posterior(prior: float, sensitivity: float, false_positive: float) -> float:
    """Return P(disease | positive test)."""
    evidence = sensitivity * prior + false_positive * (1 - prior)
    return sensitivity * prior / evidence


print("prevalence sweep for a 99%/5% test:")
for prevalence in (0.001, 0.01, 0.05, 0.20, 0.50):
    print(f"  prior={prevalence:>5.1%}  posterior={posterior(prevalence, 0.99, 0.05):.3f}")

print("\ntwo sequential positives, prior 1%:")
p = 0.01
for i in range(3):
    p = posterior(p, 0.99, 0.05)
    print(f"  after test {i + 1}: {p:.3f}")
```

**Output**

```text
prevalence sweep for a 99%/5% test:
  prior= 0.1%  posterior=0.019
  prior= 1.0%  posterior=0.167
  prior= 5.0%  posterior=0.510
  prior=20.0%  posterior=0.832
  prior=50.0%  posterior=0.952

two sequential positives, prior 1%:
  after test 1: 0.167
  after test 2: 0.798
  after test 3: 0.987
```

The sweep is the lesson: the same test, the same numbers, and the posterior ranges from 2% to 95%
depending solely on how common the condition is. Any claim about a test's meaning that omits the base
rate is incomplete.

## 8. Practical Applications

- **Spam and fraud filters.** Every incoming message updates a posterior; the prior is your base rate
  of spam, the likelihood comes from word frequencies.
- **Model calibration.** A classifier's raw score is a likelihood; a calibrated output is a posterior.
  Knowing the difference is what stops you from deploying a model that is "90% accurate" on a task
  where 90% of cases are negative.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Reporting sensitivity as the answer | 99% instead of 17% | Ignoring the base rate | Compute the evidence term |
| Forgetting to update the prior | Second test adds nothing | Using the original prior again | Posterior becomes the new prior |
| Treating tests as independent when they are not | Over-confident posterior | Same underlying signal | Use one combined likelihood |
| Probabilities above 1 or below 0 | Impossible output | Arithmetic slip in the evidence | Check that $P(B) \ge P(A\cap B)$ |

## 10. Self-Assessment

**1.** Prevalence 2%, sensitivity 90%, false-positive rate 10%. What is $P(\text{disease}\mid+)$?
<details><summary>Show answer</summary>

$P(+) = 0.9\times0.02 + 0.1\times0.98 = 0.018 + 0.098 = 0.116$;
$P(D\mid+) = 0.018/0.116 \approx 0.155$, about 15.5%.
</details>

**2.** Why does a second positive test raise the posterior so much more than the first?
<details><summary>Show answer</summary>

Because the first test moves the prior from 1% to 17%, and the second multiplies by the same likelihood
ratio of about 20 again. Each independent test multiplies the odds, so evidence compounds
multiplicatively while the prior moves toward 1.
</details>

**3.** A test has sensitivity 99% and specificity 99%, and the condition affects 1 in 10 000. Estimate
the posterior for a positive result.
<details><summary>Show answer</summary>

$P(+) \approx 0.99\times0.0001 + 0.01\times0.9999 \approx 0.000099 + 0.009999 \approx 0.0101$;
posterior $\approx 0.000099/0.0101 \approx 0.0098$, about 1%. Even a very good test on a very rare
condition mostly produces false positives.
</details>

**4.** In naive Bayes, why can the evidence term be dropped at prediction time?
<details><summary>Show answer</summary>

Because $P(B)$ is the same for every candidate class, so it does not change which class has the largest
posterior. Only the ranking matters for a decision.
</details>

## 11. Further Reading

- [Seeing Theory, Ch. 2: Conditional Probability](https://seeing-theory.brown.edu/basic-probability/index.html) — interactive Bayes updates.
- [3Blue1Brown: Bayes' theorem, with the medical test example](https://www.3blue1brown.com/lessons/bayes-theorem) — the tree diagram in motion.

## Mini-Lab

Write `posterior(prior, sensitivity, fpr)` and use it to answer: a factory's defect detector flags 8%
of good parts (false positives) and misses 5% of bad ones. If 3% of parts are bad, what fraction of
flagged parts are actually bad? Then find the prior at which a flag becomes more likely right than
wrong, and explain in one sentence why that number matters for deciding whether to deploy the detector.

## What to Do Next

Continue to [LP03-04 Random Variables and Distributions](LP03-04-random-variables-and-distributions.md).
