# L05-01 — Probability, Conditional Probability and Bayes' Theorem

| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| :--- | :--- |
| Level | 300 |
| Study time | 85 minutes |
| Prerequisites | [LP03-02](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-02-probability-rules-and-conditional-probability.md) · [LP03-03](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-03-bayes-theorem.md) |
| Notebook | NB-05-01 Uncertainty Workbench |

[← Module start](../README.md) · [Next: L05-02 Bayesian Networks →](L05-02-bayesian-networks-independence-and-inference.md)

## 1. Learning Objectives

- **Apply** the product and sum rules to compute joint, marginal and conditional probabilities.
- **Update** a belief with evidence using Bayes' theorem, and explain why the base rate dominates.
- **Distinguish** $P(A\mid B)$ from $P(B\mid A)$ in a case where confusing them changes a decision.
- **Implement** Bayesian updating over a discrete hypothesis space.

## 2. Prerequisite Knowledge

Sample spaces, independence, and the definition of conditional probability —
[LP03-02](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-02-probability-rules-and-conditional-probability.md).
If Bayes' theorem is new, read [LP03-03](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-03-bayes-theorem.md) first.

## 3. Conceptual Explanation

### 3.1 Why probability in an AI course

Rule-based systems fail on incomplete information; probability is the calculus for acting anyway.
Two rules generate everything else:

- **Product rule:** $P(A \wedge B) = P(A\mid B)P(B)$.
- **Sum rule (marginalisation):** $P(A) = \sum_b P(A \wedge B=b)$.

### 3.2 Bayes' theorem is bookkeeping

$$P(H\mid E) = \frac{P(E\mid H)P(H)}{P(E)}$$

The posterior is proportional to likelihood times prior. Every "the test is 99% accurate" claim is
incomplete until the prior is known: at 1% prevalence, a 99%-specific test still produces mostly
false positives.

### 3.3 Conditional independence is the escape hatch

The joint distribution over $n$ binary variables needs $2^n - 1$ numbers. Conditional independence
lets a model factor it into small pieces, which is the whole reason Bayesian networks (L05-02) exist.

## 4. Worked Example — spam and the base rate

Prior: 30% of mail is spam. Likelihoods: $P(\text{"free"}\mid\text{spam}) = 0.6$,
$P(\text{"free"}\mid\text{ham}) = 0.05$.

$$P(\text{spam}\mid\text{free}) = \frac{0.6 \times 0.3}{0.6\times0.3 + 0.05\times0.7}
= \frac{0.18}{0.215} \approx 0.837$$

Now change the prior to 2% spam: posterior $= \frac{0.012}{0.012+0.049} \approx 0.197$. Same word,
same likelihoods, opposite decision — the prior did the work.

**Medical version.** 1% prevalence, 99% sensitivity, 99% specificity:
$P(D\mid +) = \frac{0.0099}{0.0099+0.0099} = 0.5$. Half the positives are false.

## 5. Mathematical Formulation

Sequential updating is repeated Bayes:

$$P(H\mid E_1,E_2) \propto P(E_2\mid H,E_1)\,P(E_1\mid H)\,P(H)$$

With conditional independence of the evidence given $H$, the middle factor simplifies to
$P(E_2\mid H)$, which is what makes naive Bayes (L05-03) cheap.

## 6. Python Implementation

```python
from fractions import Fraction


def bayes(prior, likelihood_h, likelihood_not_h):
    joint = prior * likelihood_h
    evidence = joint + (1 - prior) * likelihood_not_h
    return joint / evidence


print(round(bayes(0.30, 0.60, 0.05), 3))   # 0.837
print(round(bayes(0.02, 0.60, 0.05), 3))   # 0.197
print(round(bayes(0.01, 0.99, 0.01), 3))   # 0.5


def update(prior, likelihoods):
    """Posterior over hypotheses given one observation."""
    unnorm = {h: prior[h] * likelihoods[h] for h in prior}
    z = sum(unnorm.values())
    return {h: v / z for h, v in unnorm.items()}


print(update({"spam": 0.3, "ham": 0.7}, {"spam": 0.6, "ham": 0.05}))
```

## 7. Practical Applications

- **Spam filtering** — posterior over classes given token evidence.
- **Medical screening** — the base-rate argument that decides screening policy.
- **Fault diagnosis** — posterior over causes given symptoms.
- **A/B testing** — posterior over conversion rates rather than a p-value alone.

## 8. Common Mistakes

- Confusing $P(E\mid H)$ with $P(H\mid E)$ — the prosecutor's fallacy.
- Dropping the prior because "we want to be objective"; that is a prior of 0.5.
- Multiplying likelihoods without conditional independence.
- Reporting a posterior without the evidence base used to compute it.
- Treating a 99% accurate test as a 99% chance of disease.

## 9. Exercises

1. A test has 95% sensitivity and 90% specificity at 2% prevalence. Compute the posterior and the number of false positives per 1,000 tests.
2. Update the spam posterior sequentially for two independent words and compare with the joint computation.
3. Build a table showing how the posterior changes as prevalence moves from 0.1% to 10%.
4. Find a real accuracy claim and write the missing prior it implies.

## 10. Self-Assessment

1. State the product rule and the sum rule.
2. Why does the base rate dominate a rare-event test?
3. When may likelihoods be multiplied directly?
4. What is the posterior if the prior is 0 or 1?

## 11. Key Terms

**Prior**, **likelihood**, **posterior**, **evidence**, **marginalisation**, **conditional probability**, **base rate**, **conditional independence**.

## 12. Further Reading

- Russell & Norvig, chapter 13.
- Kahneman & Tversky (1973) on base-rate neglect — the psychology behind the error.

## What to Do Next

[L05-02](L05-02-bayesian-networks-independence-and-inference.md) scales this from two variables to a
graph of many.
