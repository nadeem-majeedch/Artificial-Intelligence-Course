# ASG-14 — Capstone Proposal

| | |
| :--- | :--- |
| Time | 2 hours |
| Weight | 15% of the module |
| Prerequisites | L14-01 to L14-05 |
| Deliverable | 2-page proposal plus a one-page evaluation plan |

[Module home](../README.md) · [Rubric](../capstone/rubric.md) · [Milestones](../capstone/milestones.md)

## Brief

Choose one of the twelve briefs in [`capstone/briefs/`](../capstone/briefs/) — or propose your
own, subject to approval. Write the proposal a supervisor would approve without a meeting.

The proposal is assessed on whether the project is **falsifiable, resourced and finished before
the deadline**, not on whether the idea is ambitious.

## Required sections

### 1. Problem statement (200 words)

The decision the system supports, who is affected by it, and what currently happens without it.
Not "AI for education" — "flag students at risk of failing week 6 so an advisor can intervene,
where currently nobody reviews engagement until the exam".

### 2. Motivation (150 words)

Why this problem, why now, and why a learned approach rather than a rule. Cite at least one
source. If a rule would do, say why it would not.

### 3. Objectives (5 bullets)

Each objective must be checkable. "Build a model" is not an objective; "achieve macro F1 ≥ 0.80
on the held-out field set, with a per-class table" is.

### 4. Scope (200 words)

**In scope**, and explicitly **out of scope**. The out-of-scope list is the more important one:
it is what stops the project from expanding. Include deployment, real users, and any domain where
you will not claim validation.

### 5. Required knowledge (bullets)

Name the modules and specific techniques you will use, and honestly list the one you will have to
learn. State the fallback if learning it takes too long.

### 6. Architecture (diagram + 150 words)

A block diagram of the pipeline: data → preprocessing → model(s) → evaluation → output. Mark
where a human is involved and where the system abstains.

### 7. Dataset (200 words)

Name, source URL, licence, size, features, target, known gaps, and how you will obtain it **this
week**. If the data requires approval, say when it will arrive and what you will do if it does
not.

Use the datasheet fields from M13 where relevant: provenance, collection, preprocessing, known
bias.

### 8. Technologies

Libraries, framework, hardware. State whether it runs on CPU. A proposal that requires a GPU you
do not have is not resourced.

### 9. Milestones (table)

| Milestone | Date | Artefact |
| :--- | :--- | :--- |
| M1 proposal approved | | this document |
| M2 data + baseline | | pipeline, baseline number |
| M3 model + evaluation | | main result, per-class table |
| M4 report + demo | | report, 10-minute defence |

Dates must be real dates, not "week 3".

### 10. Evaluation metrics

| | |
| :--- | :--- |
| Primary metric | tied to the decision |
| Supporting metrics | at least two |
| Split | how, and why it matches deployment |
| Baselines | one trivial, one standard |
| Uncertainty | intervals, repeats, or a stated sample-size caveat |
| Subgroup table | which slices, and why those |

### 11. Expected deliverables

Code (runnable, seeded), model card, report, demo, and the reproduction command. One line each.

### 12. Challenges (3, with mitigations)

The three most likely reasons the project fails, and what you will do about each. "Time" is not a
challenge unless you say what you will cut.

### 13. Possible extensions

Two, each a sentence. Extensions are not part of the plan and you will not be penalised for not
doing them.

### 14. Failure condition

The single most important section: **what result would mean the project did not succeed, and how
you would report it.** A project with no failure condition cannot produce a finding.

### 15. Ethics and data protection

Personal data (yes/no), licence compliance, intended-use limits, and the sentence you will put in
the report stating that the prototype is not validated for high-stakes use.

## Worked example (excerpt)

```text
Problem: 2,300 students enrol in the introductory programming module each year. Advisors
review engagement only after the mid-term exam, by which time the failure is decided.
Goal: flag at-risk students at week 6 with precision >= 0.5 at recall >= 0.6, so advisors
can offer support while it can still change the outcome.
Data: institutional LMS logs, 3 years, anonymised export approved by the teaching office
(no names, no demographic attributes beyond programme code).
Baseline: logistic regression on attendance and prior grade.
Primary metric: recall at fixed precision 0.5, on the most recent year held out.
Failure: if precision at recall 0.6 is below 0.3, report that engagement signals are too
weak at week 6 and quantify how much later data would be needed.
Out of scope: any automated action, any use in grading, deployment to students.
```

Note that the failure condition is a *useful* result: it tells the institution when to measure
instead of what to build.

## Constraints

- Synthetic or appropriately licensed data only.
- No deployment, no commit, no push.
- Do not propose a project whose data you cannot obtain within one week.

## Marking criteria

| Criterion | Weight | Excellent |
| :--- | ---: | :--- |
| Problem and motivation | 20% | specific decision, named beneficiary, cited evidence |
| Scope and failure condition | 25% | tight scope, explicit out-of-scope, real failure condition |
| Data and feasibility | 20% | dataset secured, licence stated, fallback named |
| Evaluation plan | 25% | primary metric, baselines, split, uncertainty, subgroup table |
| Milestones and risks | 10% | dated artefacts, three real risks with mitigations |

## Reflection questions

Answer in three sentences each.

1. What would you have to believe for this project to be worth doing?
2. Which part of your plan depends on someone else, and what happens if they are slow?
3. If your main result came out 10 points worse, would the report still be worth writing?

---

[Module home](../README.md) · [Rubric](../capstone/rubric.md) ·
[Briefs](../capstone/briefs/)
