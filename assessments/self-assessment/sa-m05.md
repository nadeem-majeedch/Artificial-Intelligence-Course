# SA-M05 — Self-Assessment: Reasoning Under Uncertainty

Module M05 · [Module](../../docs/CURRICULUM-MAP.md) · [Quiz](../quizzes/quiz-m05.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Apply Bayes' rule with a base rate and explain the result
- [ ] Define conditional independence and test for it
- [ ] Read a Bayesian network's factorisation from its graph
- [ ] Perform exact inference by enumeration on a small network
- [ ] Explain what a CPT encodes and what it assumes
- [ ] Describe why naive Bayes is "naive" and what that costs

## Knowledge-check questions

1. A test has 99% sensitivity and a 5% false-positive rate; prevalence is 1%. Compute $P(D\mid T+)$.
2. Why does a high-sensitivity test still produce mostly false positives at low prevalence?
3. Write the factorisation for a chain $A\to B\to C$ and for a fork $A\leftarrow B\to C$.
4. Are two symptoms independent given the disease in a naive Bayes model? Is that realistic?
5. What does $d$-separation tell you, in one sentence?

## Practical competency checklist

- [ ] Compute a posterior by hand and with code, and get the same answer
- [ ] Build a small network and verify CPT rows sum to 1
- [ ] Validate exact inference against simulation
- [ ] Explain a result in plain language for a non-specialist

## Suggested revision topics

Conditional probability · Bayes' rule · base-rate fallacy · independence · network factorisation ·
enumeration · naive Bayes assumptions · simulation as a check.

## Readiness test for M06

Without notes:

1. Compute a posterior from sensitivity, specificity and prevalence.
2. Draw a three-node network and write its joint distribution.
3. Explain why "the test is 99% accurate" is not a statement about $P(D\mid T+)$.

If any is shaky, revisit L05-02 and L05-04 before M06.
