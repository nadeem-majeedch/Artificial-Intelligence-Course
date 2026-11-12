# QUIZ-M05 — Solutions and Explanations

> **Availability.** M05 (Reasoning Under Uncertainty) is not published in this repository yet. This paper is
> included so the assessment set is complete; it cannot be attempted until the module's
> lessons and labs are available.

[Quiz](quiz-m05.md) · [Assessment index](../README.md)

---

## Part A

**Q5.1 — B.** By definition $P(A\mid B)=P(A\cap B)/P(B)$ for $P(B)>0$. Option C is the common
confusion with Bayes' rule; $P(B\mid A)$ is not equal to $P(A\mid B)$ in general.

**Q5.2 — B.** The graph encodes conditional independences, so each variable needs a table over its
parents only. A fully connected network would need the full joint.

**Q5.3 — B.** The Markov property is that the next hidden state depends only on the current hidden
state; observations are conditionally independent given the state. Option A would be an
observation-only Markov chain, which is a different model.

**Q5.4 — B.** Expected utility is $\sum_o P(o\mid a)U(o)$ — a probability-weighted average, not a
maximum and not a sum of utilities.

## Part B

**Q5.5 — False.** Fuzzy membership is a degree of belonging to a set, not a probability over
outcomes. The two formalisms answer different questions: "how much is this a tall person" versus
"how likely is it that this person is over 1.8 m". Treating a membership value as a probability
leads to invalid arithmetic (memberships do not have to sum to 1).

## Part C

**Q5.6 — Model answer.** A full joint over 20 binary variables needs $2^{20}-1$ numbers. A Bayesian
network stores one conditional table per variable given its parents, so the total is
$\sum_i 2^{|\text{parents}(i)|}$, which is small when the graph is sparse. The enabling assumption
is conditional independence: each variable is independent of its non-descendants given its parents.

**Q5.7 — Model answer.** Aleatoric uncertainty is irreducible randomness in the process — the
outcome of a fair coin, or sensor noise. Epistemic uncertainty is ignorance about the model or
parameters, reducible with more data — an unobserved region of feature space. Distinguishing them
matters because collecting data reduces only the second.

## Part D

**Q5.8 —** $P(D)=0.01$, $P(+|D)=0.99$, $P(+|\neg D)=0.05$.

$$
P(D\mid +)=\frac{0.01\times 0.99}{0.01\times 0.99 + 0.99\times 0.05}
=\frac{0.0099}{0.0099+0.0495}=\frac{0.0099}{0.0594}\approx 0.167 .
$$

About **16.7%**. The denominator is the total probability of a positive test, and the base rate
dominates: most positives are false positives because the disease is rare.

**Q5.9 —** $EU(A)=0.6\times100+0.4\times0=60$; $EU(B)=60$. They tie exactly. The lesson is that a
certain 60 and a 60% chance of 100 have the same expected value but very different risk; expected
utility alone does not decide for a risk-averse decision maker.

## Part E

**Q5.10 —** $P(B)=P(B\mid A)P(A)+P(B\mid \neg A)P(\neg A)=0.5(0.4)+0.25(0.6)=0.20+0.15=0.35$.

$P(A\mid B)=P(B\mid A)P(A)/P(B)=0.20/0.35\approx0.571$.

## Part F

**Q5.11 —** `[0.167 0.833]`

The array is normalised by its sum ($0.0594$), giving $0.0099/0.0594\approx0.1667$ and
$0.0495/0.0594=0.8333$, rounded to three decimals. The first entry is the posterior probability of
the disease from Q5.8.

---

[Quiz](quiz-m05.md) · [Previous solutions](quiz-m04.md) · [Assessment index](../README.md)
