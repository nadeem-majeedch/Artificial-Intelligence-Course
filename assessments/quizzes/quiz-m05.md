# QUIZ-M05 — Uncertainty, Bayesian Reasoning and Fuzzy Logic

| | |
| :--- | :--- |
| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| Questions | 11 (20 marks) |
| Time | 35 minutes |
| Covers | L05-01 … L05-06 (including L05-06, variable elimination) |
| Pass mark | 12 / 20 |

> **Availability.** This module's lessons, notebook and lab are published in this repository; sit this paper after finishing them.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m05.md)

Calculator allowed. Show the formula before substituting numbers.

---

## Part A — Multiple choice (4 marks)

**Q5.1** $P(A\mid B)$ is defined as

- A. $P(A)P(B)$
- B. $P(A \cap B)/P(B)$
- C. $P(B\mid A)$
- D. $P(A \cup B)/P(B)$

**Q5.2** A Bayesian network's compactness comes from

- A. discretising variables
- B. conditional independence encoded by the graph structure
- C. assuming all variables are independent
- D. pruning low-probability states

**Q5.3** In an HMM, the Markov assumption applies to

- A. observations only
- B. hidden states only
- C. both, independently
- D. neither

**Q5.4** Expected utility of an action is

- A. the maximum utility among its outcomes
- B. the probability-weighted average of its outcomes' utilities
- C. the utility of the most likely outcome
- D. the sum of its outcomes' utilities

## Part B — True or false, with a reason (2 marks)

**Q5.5** "A fuzzy membership value of 0.7 means the proposition is true with probability 0.7."

## Part C — Conceptual (4 marks)

**Q5.6** (2 marks) Why can a network with 20 binary variables be represented with far fewer than
$2^{20}$ numbers, and what assumption makes that possible?

**Q5.7** (2 marks) Explain the difference between aleatoric and epistemic uncertainty, with one
example of each.

## Part D — Numerical (6 marks)

**Q5.8** (3 marks) A disease affects 1% of a population. A test has sensitivity 0.99 and a
false-positive rate of 0.05. Compute the probability that a person who tests positive has the
disease. Show the denominator.

**Q5.9** (3 marks) A decision has two actions. Action A yields 100 with probability 0.6 and 0 with
probability 0.4. Action B yields 60 for certain. Which has higher expected utility, and what is
the difference?

## Part E — Tracing (2 marks)

**Q5.10** For $P(A)=0.4$, $P(B\mid A)=0.5$, $P(B\mid \neg A)=0.25$, compute $P(B)$ and then
$P(A\mid B)$.

## Part F — Python output (2 marks)

**Q5.11** What does this print?

```python
import numpy as np

posterior = np.array([0.0099, 0.0495])
print(np.round(posterior / posterior.sum(), 3))
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m05.md) · [Next quiz](quiz-m06.md)
