# AA-04 — Evaluating a Reported Result

| | |
| :--- | :--- |
| Assignment | 04 |
| Difficulty | Intermediate |
| Estimated time | 2 hours |
| Prerequisites | M06, M13 (L13-01) |
| Format | Critical evaluation |
| Covers | metric choice, baselines, intervals, subgroup reporting |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

A vendor reports: "Our triage model reaches 94% accuracy, outperforming clinicians, and is ready for
deployment." The numbers may be true and the conclusion still unsupported. Your job is to separate
them.

## Problem scenario

The vendor's summary reports accuracy on a balanced research cohort of 2,000 cases (50% positive),
a 94% figure, and "no significant difference between subgroups". The deployment population has 4%
prevalence. No confidence intervals are given.

## Learning outcomes

1. Convert accuracy claims into the metrics that matter at deployment prevalence.
2. Identify what a balanced cohort hides.
3. Specify the evidence a deployment claim requires.
4. Write a short, fair critique that separates measurement from inference.

## Tasks

1. **Prevalence.** Assuming sensitivity 0.94 and specificity 0.94, compute precision and NPV at 4%
   prevalence. Show the arithmetic.
2. **Baseline.** What comparison would establish "outperforming clinicians"? State the design.
3. **Subgroups.** Why is "no significant difference" uninformative without subgroup sizes and
   intervals?
4. **Missing evidence.** List four artefacts required before deployment and say what each would show.
5. **Verdict.** Write 200 words a regulator could act on: what is supported, what is not, and the
   single most important missing measurement.

## Constraints

- No more than 900 words.
- Do not speculate about the vendor's motives; critique the evidence.
- Every numerical claim you make must be computed or cited.

## Expected deliverables

A written evaluation with the prevalence table and the verdict.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Prevalence arithmetic | 30% | correct precision/NPV with working |
| Baseline critique | 20% | comparison design specified |
| Subgroup reasoning | 20% | intervals and sizes discussed |
| Evidence list | 20% | four relevant artefacts, correctly motivated |
| Verdict | 10% | fair, actionable, bounded |

## Bonus challenges

- Recompute precision if prevalence is 1% and 20%, and plot the curve.
- Describe the prospective study that would justify the deployment claim.

---

[Assessment index](../README.md) · [AA-03](aa-03-mathematical-derivation.md) · [AA-05](aa-05-error-analysis.md)
