# AA-06 — Auditing a Dataset Before Modelling

| | |
| :--- | :--- |
| Assignment | 06 |
| Difficulty | Intermediate |
| Estimated time | 2 hours |
| Prerequisites | M06, M13 (L13-01, L13-02) |
| Format | Dataset audit |
| Covers | sampling bias, label bias, proxies, measurement validity |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

Bias enters before the model exists: in who is sampled, how labels were produced, and which column
stands in for the thing you actually care about. A model can be fair by every metric and still be
built on a target that measures the wrong construct.

## Problem scenario

A hiring dataset has 12,000 historical decisions with: applicant gender, years of experience, degree
institution tier, interview score, and `hired`. The stated goal is "predict who will succeed in the
role". The positive label is a past hiring decision, not a performance measure.

## Learning outcomes

1. Distinguish the construct you want from the label you have.
2. Identify sampling and label-generation mechanisms that create disparity.
3. Reason about proxy variables and their legal/ethical status.
4. Specify a data collection change, not only a modelling one.

## Tasks

1. **Construct validity.** Explain why `hired` is not `will succeed`, and what label would be better.
2. **Mechanism.** Name two mechanisms by which the historical process produces disparate labels.
3. **Measurement.** For each column, state what it measures and whether it is a proxy for a protected
   attribute.
4. **Detection.** Propose two quantitative checks on the dataset (before modelling) and the result
   that would trigger action.
5. **Remediation.** One data change and one modelling change, each with its cost.
6. **Boundary.** State one decision this dataset cannot support at all.

## Constraints

- No model training required.
- Do not propose dropping protected attributes as a fairness fix without argument.
- Cite at least two sources on construct validity or label bias.

## Expected deliverables

A written audit of at most 900 words with a column-by-column table.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Construct validity | 25% | label vs goal argued precisely |
| Mechanisms | 25% | two mechanisms, correctly described |
| Column analysis | 20% | proxies identified with reasoning |
| Checks and remediation | 20% | concrete, costed, trigger-based |
| Boundary | 10% | a clear "cannot support" claim |

## Bonus challenges

- Sketch the label you would collect and the study needed to collect it.
- Discuss whether reweighing can fix label bias in this dataset, with evidence.

---

[Assessment index](../README.md) · [AA-05](aa-05-error-analysis.md) · [AA-07](aa-07-research-paper-analysis.md)
