# Capstone Milestones

Four gates. Each one ends in an artefact, not a status report. The gates are self-checked; the
rubric is applied at M4.

## M1 — Proposal approved (after ASG-14)

| | |
| :--- | :--- |
| Input | the brief, your draft proposal |
| Output | approved 2-page proposal plus evaluation plan |
| Time | 2 hours |

**Checklist**

- [ ] One-sentence goal, no more than two "and"s
- [ ] Data confirmed available this week, licence stated
- [ ] Baseline named and trivially runnable
- [ ] Primary metric tied to the decision
- [ ] Split strategy justified (random, temporal, by site)
- [ ] Failure condition written
- [ ] Out-of-scope list written
- [ ] Four dated milestones

**Gate question.** "If I gave this proposal to another student, could they start tomorrow without
asking me anything?" If not, it is not approved.

**Common failure.** Scope so broad that the failure condition is unfalsifiable. Cut until the
failure condition is a number.

## M2 — Data and baseline (week 2)

| | |
| :--- | :--- |
| Input | approved proposal |
| Output | working pipeline, baseline number, data note |
| Time | 4 hours |

**Checklist**

- [ ] Data loads from a script, not a notebook cell with a local path
- [ ] Split implemented and printed (sizes, class balance)
- [ ] Leakage check: no test information in preprocessing or feature selection
- [ ] Baseline trained and evaluated; number recorded
- [ ] Data note: provenance, licence, rows per class, known gaps
- [ ] Environment file (requirements) exists

**Gate question.** "Can you beat this baseline?" If you cannot, that is a finding — report it.

**Common failure.** Spending the week on cleaning without a baseline. A rough baseline on dirty
data tells you more than a perfect pipeline with no number.

## M3 — Model and evaluation (week 3–4)

| | |
| :--- | :--- |
| Input | pipeline, baseline |
| Output | main result, per-class or subgroup table, error analysis |
| Time | 5 hours |

**Checklist**

- [ ] Model trained with at least two seeds, or a stated reason why not
- [ ] Primary metric reported on the held-out split
- [ ] Two baselines in the same table
- [ ] Per-class or subgroup table with n per cell
- [ ] Uncertainty: intervals, repeated runs, or an explicit sample-size caveat
- [ ] Three concrete failures inspected and explained
- [ ] One ablation: which component actually mattered

**Gate question.** "What is the smallest change to the data that would break this?" Answer it with
an experiment, not an opinion.

**Common failure.** Tuning on the test split. Fix: a validation split, and a note in the report
saying which split was used for what.

## M4 — Report, demo and defence (final week)

| | |
| :--- | :--- |
| Input | all previous artefacts |
| Output | report (6 pages), model card, 5-slide defence, reproduction command |
| Time | 3 hours |

**Checklist**

- [ ] Report follows the template; every number traceable to a command
- [ ] Abstract states the result and the main limitation
- [ ] Model card complete (including the security and privacy lines, even if "not applicable")
- [ ] Reproduction: one command, seeds fixed, environment pinned
- [ ] Demo shows the main result **and** one failure
- [ ] Limitations in the abstract, not buried at the end
- [ ] Prototype boundary stated for any high-stakes domain
- [ ] Self-score on the rubric with evidence per criterion

**Gate question.** "Which of your claims would survive if the main result were 5 points worse?"

**Common failure.** A polished demo and a thin evaluation. The rubric weights evaluation at 15 and
demonstration at 5 for a reason.

## Weekly evidence rule

Every week, produce one artefact a supervisor can look at in under a minute:

| Week | Artefact |
| ---: | :--- |
| 1 | proposal, dataset note |
| 2 | baseline table |
| 3 | first model result against baseline |
| 4 | per-class table, error analysis |
| 5 | report draft, model card |
| 6 | final report, demo, defence |

If a week produces nothing you can point at, the project is drifting. Say so early.

## When things go wrong

| Situation | What to do |
| :--- | :--- |
| Data never arrives | switch to a public dataset from the same domain; document the substitution |
| Model cannot beat baseline | report it; analyse why; the negative result is the finding |
| Results are unstable across seeds | report the spread; reduce model capacity; check the split |
| Scope creep | cut a feature, never the evaluation |
| Time runs out | submit M3 evidence plus a partial report; a documented partial result beats an undocumented demo |

---

[Capstone home](README.md) · [Rubric](rubric.md) · [Report template](report-template.md)
