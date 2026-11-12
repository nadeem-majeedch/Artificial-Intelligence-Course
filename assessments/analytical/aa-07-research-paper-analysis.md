# AA-07 — Reading a Paper Critically

| | |
| :--- | :--- |
| Assignment | 07 |
| Difficulty | Advanced |
| Estimated time | 3 hours |
| Prerequisites | M06 or M08 or M11; any completed module |
| Format | Structured paper review |
| Covers | claims, evidence, ablations, baselines, reproducibility |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

A paper's abstract states a claim; its experiments support a narrower one. The skill is stating
exactly what was shown, on what data, against what baseline, and what would have to be true for it to
transfer.

## Problem scenario

Choose one paper from the course reading list (or an approved alternative) reporting an accuracy or
quality improvement on a benchmark. Review it with the structure below. Length is limited deliberately:
precision is the point.

## Learning outcomes

1. Separate claim, method and evidence.
2. Identify the baseline and judge whether it is strong.
3. Evaluate ablations: does each component earn its place?
4. State the conditions under which the result would not transfer.

## Tasks

1. **Claim.** One sentence: what the paper claims, on which task and dataset.
2. **Method.** Three sentences, no equations unless essential.
3. **Baselines.** What was compared, and what was omitted that a reviewer would expect.
4. **Evidence table.** For the headline result: metric, dataset size, variance across seeds, and
   whether an interval is reported.
5. **Ablation.** Which component contributed most, and is the ablation complete?
6. **Threats to validity.** Three, each with the specific result it would undermine.
7. **Verdict.** Would you build on it? Under what conditions?

## Constraints

- One paper, at most 800 words, plus the evidence table.
- No summarising the related-work section.
- Quote numbers exactly as reported; do not round.

## Expected deliverables

A structured review following the seven sections.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Claim precision | 20% | claim bounded to what was tested |
| Baseline judgement | 20% | omissions identified |
| Evidence table | 25% | metrics, sizes, seeds, intervals |
| Ablation reading | 20% | contribution assessed |
| Threats and verdict | 15% | specific, not generic |

## Bonus challenges

- Reproduce one table or figure from the paper's released code, or state why you could not.
- Write the reviewer paragraph you would submit, in 120 words.

---

[Assessment index](../README.md) · [AA-06](aa-06-dataset-bias-analysis.md) · [AA-08](aa-08-system-architecture-evaluation.md)
