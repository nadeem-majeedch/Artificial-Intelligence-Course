# PA-05 — Bayesian Diagnosis with a Small Network

| | |
| :--- | :--- |
| Assignment | 05 |
| Difficulty | Intermediate |
| Estimated time | 4 hours |
| Prerequisites | M05 (L05-02 … L05-04), P03 |
| Covers | conditional probability, Bayes' rule, Bayesian networks, exact inference |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

A clinic screens for a condition with a 1% prevalence. The test is good — sensitivity 0.99, false
positive rate 0.05 — and yet most positives are false. Clinicians find this counter-intuitive, and
so does almost everyone the first time. The assignment builds the arithmetic, then a small network
with three symptoms, then an exact inference routine, and checks all three against each other.

## Problem scenario

Variables: `D` (condition), `T` (test), `S1`, `S2` (symptoms), with a stated graph and CPTs. You must
compute posteriors by enumeration, by a second method, and validate both against a simulation.

## Learning outcomes

1. Apply Bayes' rule and explain base-rate effects numerically.
2. Represent a domain as a Bayesian network with correct factorisation.
3. Implement exact inference by enumeration.
4. Validate analytic results against Monte Carlo simulation.

## Tasks

1. **Base rate.** Compute $P(D\mid T{+})$ from the numbers above; show the denominator.
2. **Network.** Build a five-node network (add a second test `T2` conditionally dependent on `D`),
   write the CPTs, and state the factorisation the graph implies.
3. **Enumeration.** Implement exact inference for any query given evidence, from the CPTs.
4. **Validation.** Simulate 200,000 draws and compare the empirical posterior with the exact value;
   report the difference and a 95% interval.
5. **Sensitivity.** Vary prevalence from 0.1% to 10% and plot $P(D\mid T{+})$; explain the shape.
6. **Independence.** Show numerically what happens if you incorrectly assume `T` and `T2` independent
   given `D` when they are not.

## Constraints

- No probabilistic programming libraries; implement the enumeration.
- Seeded simulation; report the seed.
- Every probability in the report printed to four decimals.

## Expected deliverables

`bayes.py`, `network.json` (graph and CPTs), `results.md` with tables and the sensitivity plot, and a
short discussion of the base-rate result.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Bayes computation | 20% | correct posterior with the denominator shown |
| Network and factorisation | 25% | CPTs consistent, factorisation matches the graph |
| Inference implementation | 30% | exact posteriors for several evidence sets |
| Validation | 15% | simulation agrees within the stated interval |
| Discussion | 10% | base-rate and independence results interpreted |

## Bonus challenges

- Implement variable elimination and compare runtime with enumeration on the same queries.
- Add a decision node and compute the expected utility of testing versus not testing.

---

[Assessment index](../README.md) · [PA-04](pa-04-knowledge-based-systems.md) · [PA-06](pa-06-machine-learning.md)
