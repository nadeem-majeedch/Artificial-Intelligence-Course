# L05-04 — Fuzzy Sets, Membership Functions and Fuzzy Operations

| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| :--- | :--- |
| Level | 300 |
| Study time | 80 minutes |
| Prerequisites | [L05-01](L05-01-probability-conditional-probability-and-bayes-theorem.md) |
| Notebook | NB-05-01 Uncertainty Workbench |

[← Previous: L05-03](L05-03-naive-bayes-and-text-classification.md) · [Next: L05-05 Fuzzy Inference →](L05-05-fuzzy-inference-mamdani-sugeno-and-defuzzification.md)

## 1. Learning Objectives

- **Distinguish** vagueness (fuzzy) from randomness (probability) and say when each applies.
- **Define** triangular, trapezoidal and Gaussian membership functions.
- **Compute** $\min$/$\max$ and algebraic fuzzy operators, and explain why the choice matters.
- **Implement** a membership function library and plot a variable's linguistic terms.

## 2. Prerequisite Knowledge

Sets, functions, and the notion of a truth value from
[L05-01](L05-01-probability-conditional-probability-and-bayes-theorem.md) (probability is a different
kind of uncertainty — this lesson is about vagueness).

## 3. Conceptual Explanation

### 3.1 Two different uncertainties

"I will roll a six" is random: the event is crisp, the outcome is not known. "The room is warm" is
vague: the boundary of the set *warm rooms* is not defined. Probability theory handles the first;
fuzzy set theory handles the second. Mixing them up produces either a model that cannot express
"warm" or a probability that is really a preference.

### 3.2 Membership

A fuzzy set $A$ on universe $X$ is a map $\mu_A: X \to [0,1]$. A temperature of 24 °C can be
*warm* to degree 0.6 and *hot* to degree 0.1 — both statements, simultaneously.

| Shape | Parameters | Use |
| :--- | :--- | :--- |
| Triangular | $(a,b,c)$ | most control variables |
| Trapezoidal | $(a,b,c,d)$ | saturated ranges |
| Gaussian | $(\mu,\sigma)$ | smooth, differentiable |

### 3.3 Operations

For $x \in X$:

- Union: $\mu_{A\cup B} = \max(\mu_A,\mu_B)$
- Intersection: $\mu_{A\cap B} = \min(\mu_A,\mu_B)$
- Complement: $\mu_{\bar A} = 1 - \mu_A$

Algebraic alternatives ($ab$, $a+b-ab$) are smoother and matter when the output must be continuous.
$\min$/$\max$ are the Zadeh operators; they are idempotent, which algebraic ones are not.

## 4. Worked Example — temperature terms

Universe 0–40 °C. Cold = triangle (0, 0, 18); Warm = triangle (10, 20, 30); Hot = triangle (22, 40, 40).

At 24 °C: cold 0, warm $1 - |24-20|/10 = 0.6$, hot $(24-22)/18 = 0.11$.

At 18 °C: cold $1 - 18/18 = 0$? — using (0,0,18) the right edge gives 0 at exactly 18, warm 0.8, hot 0.
Note the boundary behaviour: overlapping terms must sum sensibly or the control surface has holes.

## 5. Mathematical Formulation

Triangle: $\mu(x) = \max\left(0, \min\left(\frac{x-a}{b-a}, \frac{c-x}{c-b}\right)\right)$

Trapezoid: $\mu(x) = \max\left(0, \min\left(\frac{x-a}{b-a}, 1, \frac{d-x}{d-c}\right)\right)$

Gaussian: $\mu(x) = \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$

## 6. Python Implementation

```python
import math


def tri(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    return (x - a) / (b - a) if x <= b else (c - x) / (c - b)


def trap(x, a, b, c, d):
    return max(0.0, min((x - a) / (b - a) if b != a else 1.0,
                        1.0,
                        (d - x) / (d - c) if d != c else 1.0))


def gauss(x, mu, sigma):
    return math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


cold, warm, hot = lambda x: tri(x, 0, 0, 18), lambda x: tri(x, 10, 20, 30), lambda x: tri(x, 22, 40, 40)
for t in (8, 18, 24, 33):
    print(t, round(cold(t), 2), round(warm(t), 2), round(hot(t), 2))

print("warm AND hot at 24:", min(warm(24), hot(24)))
print("warm OR hot at 24:", max(warm(24), hot(24)))
print("NOT warm at 24:", round(1 - warm(24), 2))
```

## 7. Practical Applications

- **Control** — fan speed, valve position, braking force (L05-05).
- **Decision support** — risk categories with soft boundaries.
- **Image processing** — edge and region membership.
- **Consumer products** — washing machines, cameras, rice cookers.

## 8. Common Mistakes

- Using membership 0.7 as "70% probability".
- Terms that do not overlap, leaving gaps where no rule fires.
- Terms that all peak at one point, so every input is "medium".
- Choosing $\min$/$\max$ and then differentiating the output.
- Normalising memberships when the application needs absolute values.

## 9. Exercises

1. Plot the three temperature terms and mark where warm and hot cross.
2. Add a "very" hedge ($\mu^2$) and a "somewhat" hedge ($\sqrt{\mu}$); compare at 24 °C.
3. Show a case where $\min$ and the algebraic product give different rule strengths.
4. Design terms for humidity and check coverage over 0–100%.

## 10. Self-Assessment

1. Give one phenomenon that is vague but not random.
2. Why must adjacent terms overlap?
3. What does $\mu_A(x)=0.6$ mean, precisely?
4. Which operator would you choose if the output must be differentiable, and why?

## 11. Key Terms

**Fuzzy set**, **membership function**, **universe of discourse**, **linguistic variable**, **Zadeh operators**, **hedge**.

## 12. Further Reading

- Zadeh (1965), "Fuzzy sets".
- Ross, *Fuzzy Logic with Engineering Applications*, chapters 2–3.

## What to Do Next

[L05-05](L05-05-fuzzy-inference-mamdani-sugeno-and-defuzzification.md) turns memberships into
control actions.
