# AA-05 — Error Analysis of a Deployed Classifier

| | |
| :--- | :--- |
| Assignment | 05 |
| Difficulty | Intermediate |
| Estimated time | 2 hours |
| Prerequisites | M06, PA-06 |
| Format | Data analysis on a supplied error dump |
| Covers | taxonomy, prioritisation, base rates, remediation |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

"Our model is 91% accurate" says nothing about which 9% fail or what fixing them is worth. Error
analysis turns a rate into a plan: a taxonomy, counts, and a ranking by expected gain.

## Problem scenario

You are given 300 misclassified rows from a five-class classifier with per-class support: 1,200,
900, 300, 250 and 150. Each row has the true label, predicted label, confidence and a short text
field. The product owner can fund exactly one fix.

## Learning outcomes

1. Build a mutually exclusive error taxonomy from examples.
2. Compute per-class error rates and identify the worst class correctly.
3. Estimate the gain from each candidate fix.
4. Recommend one fix and state what would falsify it.

## Tasks

1. **Per-class table.** Errors and error rate per class, with support; identify the worst class by rate
   and by count (they may differ, and say why that matters).
2. **Taxonomy.** At least five categories, mutually exclusive, with counts and two examples each.
3. **Confusion.** Which class pair dominates? Give counts and one explanation.
4. **Gain estimate.** For two candidate fixes, estimate the accuracy change using the counts; state the
   assumption each estimate rests on.
5. **Recommendation.** One fix, the expected gain, the cost, and the measurement that would show you
   were wrong.
6. **Caveat.** Name one reason the error dump may not represent production.

## Constraints

- Work only from the supplied dump; no new data collection.
- Category counts must sum to 300.
- Distinguish rate from count explicitly.

## Expected deliverables

`analysis.md` with the tables, plus a short appendix of the taxonomy definition.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Per-class analysis | 25% | rates and counts, difference explained |
| Taxonomy | 30% | exclusive, complete, evidenced |
| Gain estimates | 25% | arithmetic shown, assumptions named |
| Recommendation | 20% | ranked, falsifiable, cost-aware |

## Bonus challenges

- Add a confidence-stratified analysis and test whether abstention would help.
- Estimate the label-noise share and how it bounds achievable accuracy.

---

[Assessment index](../README.md) · [AA-04](aa-04-model-evaluation.md) · [AA-06](aa-06-dataset-bias-analysis.md)
