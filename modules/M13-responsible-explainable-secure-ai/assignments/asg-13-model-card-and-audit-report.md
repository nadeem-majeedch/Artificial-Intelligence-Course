# ASG-13 — Model Card and Audit Report

| | |
| :--- | :--- |
| Time | 1.5 hours |
| Weight | 25% of the module |
| Prerequisites | L13-01 to L13-06, LAB-13-01, LAB-13-02 |
| Deliverables | model card (1 page), audit report (≤1,500 words), risk register extract |

[Module home](../README.md) · [Mini-project](../projects/mp-13-ethics-review-board.md)

## Brief

You are the internal auditor for a system that is about to be deployed. Choose **one** of the
three systems you built:

| System | Evidence you already have |
| :--- | :--- |
| Recruitment screening | `fairness.py` recruitment tables; L13-01 |
| Student pass prediction | `fairness.py` student tables; `explain.py` explanations |
| Loan prioritisation | `fairness.py` loans tables, calibration by group |

Your job is not to improve the model. It is to state, with evidence, what it does, for whom it
fails, and whether it should ship.

## Deliverable 1 — Model card

Use `code/governance.py` as the starting template (`model_card()` writes
`outputs/model-card.md`). Fill every field. Rules:

- Every number must be reproducible by a command in this repository; cite the command.
- Report at least one metric per group, with $n$ per group.
- State the fairness definition you chose **and why**, and the gap you measured.
- Include an explainability section with a fidelity or stability number.
- Include a security/privacy section, even if the answer is "not applicable, because…".
- List limitations as things that are true, not hedges.

An incomplete card scores zero on completeness, regardless of prose quality.

## Deliverable 2 — Audit report

Structure:

### 1. Scope and context of use (150 words)

The decision the system supports, who is affected, what a human does with the output, and what
"harm" means here.

### 2. Evidence reviewed (150 words)

Files, scripts, seeds, sample sizes. A stranger must be able to rerun it.

### 3. Findings (700 words)

Four to six findings in this exact format:

```text
F-01 — <short title>
Observation: <what the artefact says>
Evidence: <file, number, command>
Risk: <who is harmed and how>
Severity: critical / high / medium / low
Action: <specific, owned, dated>
```

At least one finding must come from the subgroup table, one from explainability or calibration,
and one from security or privacy.

### 4. Residual risk (200 words)

The two risks you would accept, with justification, and the two you would not.

### 5. Recommendation (150 words)

Release, conditional release, or do not release — with conditions, owners and dates if
conditional.

## Deliverable 3 — Risk register extract

Five to eight rows in `governance.py` format: id, category, description, likelihood, impact,
controls, residual. At least one row must have a residual in the high band, and it must be
justified by a measurement from your own runs.

## Worked example of a good finding

```text
F-02 — Recall gap concentrated in one group
Observation: model-card.md reports overall accuracy 0.798; the subgroup table shows TPR
0.985 (group C) vs 0.963 (group D), and PPV 0.885 vs 0.734.
Evidence: python fairness.py, section 2, 30% holdout, n=900 (447/453), random_state=0.
Risk: a qualified applicant in group D is rejected more often, and a positive prediction for
group D is less likely to be correct — so both the applicant and the reviewer bear a cost.
Severity: high.
Action: report the subgroup table in the card; review the threshold at 0.45 for group D;
owner: modelling lead; due: 10 working days.
```

Note that it names the split, the seed, the sample sizes, the direction of harm and a concrete
action. That is the standard.

## Constraints

- Synthetic data only. Do not introduce real personal records.
- Do not deploy anything, and do not commit or push.
- If you cannot evidence a claim, write "not measured" and say what it would take. Inventing a
  number is a fail, and it is also the exact failure this module is about.

## Marking criteria

| Criterion | Weight | Excellent | Adequate | Weak |
| :--- | ---: | :--- | :--- | :--- |
| Model card completeness | 25% | all fields, traceable numbers | most fields | placeholders remain |
| Findings quality | 30% | specific, evidenced, severity justified | mostly specific | vague observations |
| Fairness and explainability analysis | 20% | definition chosen and defended; fidelity reported | metrics reported | single metric, no interpretation |
| Security/privacy | 10% | attacks named with results | mentioned | absent |
| Recommendation | 10% | conditions, owners, dates | recommendation given | no decision |
| Reproducibility | 5% | commands and seeds | partial | none |

## Reflection questions

Answer briefly at the end of the report.

1. Which finding was hardest to evidence, and why?
2. Did any measurement contradict what you expected before running it?
3. If you had one more hour, which single measurement would you add, and what decision would
   it change?
4. Would you sign this audit under your own name? What would you need first?

---

[Module home](../README.md) · [Quiz](../quizzes/quiz-13.md) ·
[Mini-project](../projects/mp-13-ethics-review-board.md)
