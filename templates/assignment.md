# ASG-«MM» — «Assignment title»

| Module | M«MM» · «Module title» |
| :--- | :--- |
| Weight | «within the module's assessment» |
| Effort | «4–6 hours» |
| Individual / pair | «Individual» |
| Due | «set by your instructor; no date is fixed in the repository» |
| Lessons covered | `L«MM»-«NN»`, «…» |

[← Module home](../README.md) · `[Course home](../README.md)`

<!--
AUTHOR NOTES (delete before publishing)
• State the interface exactly (function names, file names, CLI). Ambiguity here produces
  unmarkable submissions.
• The starter materials must not contain the answer.
• For a mini-project, keep the same structure but replace "Specification" with "Brief" and
  shorten the rubric to three criteria.
-->

## Context

«Why this task exists and where it sits in the module. Two or three sentences — a student
should understand the purpose without reading the whole module again.»

## Objective

«One sentence naming the deliverable: "Implement and evaluate X, and report which configuration
you would ship and why."»

## Specification

**Inputs**

- «Format, size, where it comes from (`datasets/«slug»/`), edge cases present.»

**Outputs / interface**

| Item | Required form |
| :--- | :--- |
| `«function_or_class»` | `def «name»(«args») -> «type»` — «contract, including error behaviour» |
| `«output_file»` | «columns, types, sorting, precision» |
| `«report.md»` | «required sections» |

**Constraints**

- «No external libraries beyond the course's core tier; CPU only; runtime ≤ «n» s; deterministic
  with the given seed.»

## Starter materials

| Item | Path | What it does |
| :--- | :--- | :--- |
| «Skeleton» | `«path»` | «Signatures only; raises NotImplementedError» |
| «Data» | `«path»` | «…» |
| «Tests» | `«path»` | «Public tests covering «what»; hidden tests will cover «what»» |

## Tasks

1. «Implement the core method.»
2. «Validate it against «a hand-computed case / the reference implementation».»
3. «Run the experiment described in Task 3 and record the results table.»
4. «Analyse: where does it fail, and why?»
5. «Write the report with the required sections.»

## Deliverables

| File | Contents | Marked on |
| :--- | :--- | :--- |
| `«file»` | «…» | Correctness, code quality |
| `«report.md»` | «…» | Understanding, evaluation, communication |
| `«figure»` | «…» | Communication |

## Rubric

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Correctness against spec | 35% | «All tests pass, edge cases handled» | «Most pass» | «Core fails» |
| Understanding | 25% | «Explains the mechanism and the mathematics» | «Describes steps» | «Copied code, no explanation» |
| Evaluation and analysis | 20% | «Baseline, right metric, error analysis with causes» | «Metric only» | «No evaluation» |
| Code quality and reproducibility | 15% | «Modular, typed, seeded, one command to run» | «Runs with effort» | «Does not run» |
| Communication | 5% | «Report a stakeholder could act on» | «Readable» | «Unclear» |

## Submission checklist

- [ ] Code runs from a clean checkout with the documented command
- [ ] Random seeds fixed; two runs produce identical results
- [ ] No data files modified in place; no absolute paths
- [ ] Report states the metric, the baseline, one failure case and one limitation
- [ ] All figures labelled with axis names and units
- [ ] Sources cited for any code or idea that is not yours

## Academic integrity

«State the module's policy: discussion is encouraged, sharing code is not; cite every external
source; generated code must be understood and disclosed; the report must be your own words.»

## Estimated effort

| Stage | Time |
| :--- | ---: |
| Reading and planning | «45» min |
| Implementation | ««2–3» h» |
| Experiments | ««1–1.5» h» |
| Report | ««45–60» min» |

## Extensions (optional, unmarked)

1. «A harder variant that a strong student can attempt.»
2. «A production consideration: latency, memory, monitoring.»
