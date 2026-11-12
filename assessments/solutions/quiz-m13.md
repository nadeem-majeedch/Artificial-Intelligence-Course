# QUIZ-M13 — Solutions and Explanations

[Quiz](quiz-m13.md) · [Assessment index](../README.md)

---

## Part A

**Q13.1 — B.** Demographic parity compares selection rates. Equal TPR is equal opportunity; equal
precision is predictive parity. These can conflict when base rates differ.

**Q13.2 — B.** Efficiency is $\sum_j\phi_j=f(x)-\mathbb E[f]$. If the sum does not match, the
coalition sampling or background distribution is wrong, whatever else the implementation claims.

**Q13.3 — B.** $\varepsilon$ bounds the perturbation in the input space; $\varepsilon=0.2$ on
$[0,1]$ pixels is a small change that can flip the prediction. It is not a training-set attack
(C is poisoning) nor an inference attack (D).

**Q13.4 — B.** A fairness section must name the definition, give a measured gap with sample sizes,
and state the threshold that triggers action. "Designed fairly" is unfalsifiable.

## Part B

**Q13.5 — False.** Reweighing balances the marginal label distribution $P(Y\mid G)$; it cannot
correct a labelling policy that treats equally qualified people differently. Measured in M13: every
metric was unchanged to three decimals after reweighing.

## Part C

**Q13.6 — Model answer.** Accuracy aggregates over people, so a model can be right about most
applicants while allocating positive decisions unevenly. The recruitment model was 0.947 accurate
with a disparate impact ratio of 0.557 and an equal-opportunity gap of 0.176. Accuracy answers "how
often right", not "who bears the errors".

**Q13.7 — Model answer.** An attribution measures sensitivity — how much the output moves when a
feature changes. The binding constraint is the rule or threshold that actually decided the case. In
M13 the policy limit was income, but integrated gradients ranked savings first and income last,
because savings had more leverage on the model's probability. A reason for a decision must name the
binding constraint.

## Part D

**Q13.8 —** $\text{DI}=0.096/0.172=0.558$. Below 0.80, so it fails the 80% screening rule and
invites scrutiny — but the rule is a heuristic, not a proof of discrimination or of its absence.

**Q13.9 —** AUC 0.513 is essentially chance: the attack cannot distinguish members from non-members.
The confidence gap of 0.009 explains why — there is almost no overfitting signal to exploit. Both
numbers should appear in the model card as a tested negative result.

## Part E

**Q13.10 —** $x'=\operatorname{clip}(x+0.1\cdot[+1,-1])=[0.5,0.6]$, already inside $[0,1]$.

## Part F

**Q13.11 —** `0.558 True`

$0.096/0.172=0.5581$, printed to three decimals, and the comparison to 0.8 is `True`.

---

[Quiz](quiz-m13.md) · [Previous solutions](quiz-m12.md) · [Assessment index](../README.md)
