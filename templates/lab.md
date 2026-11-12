# LAB-«MM»-«NN» — «Scenario title»

| Module | M«MM» · «Module title» |
| :--- | :--- |
| Level | «200» |
| Effort | «2–3 hours», suggested split: «session 1 = tasks 1–3, session 2 = tasks 4–6» |
| Lessons covered | ```[L«MM»-«NN»](../lessons/L«MM»-«NN»-«slug».md)```, ```[L«MM»-«NN»](../lessons/L«MM»-«NN»-«slug».md)``` |
| Dataset / assets | `«dataset-slug»`, «or: generated in the lab» |
| Notebook | `NB-«MM»-«NN»` — «optional support» |

[← Module home](../README.md) · `[Course home](../README.md)`

<!--
AUTHOR NOTES (delete before publishing)
• The scenario must contain a real decision and a stakeholder — not "apply the algorithm to
  another dataset".
• Every task names an observable success condition.
• Hints are progressive. The lab must never ship a full solution.
-->

## Scenario

«Three to five sentences of situation. Name the organisation, the person who will use the
result, and the decision they have to make. Example: "The campus transport office must reroute
two shuttle buses before the new term. The officer has a map, a list of stops, and one working
day. She needs routes she can defend to students who will complain about longer walks."»

## Your role

«You are the «job title» on this task. You report to «stakeholder» and you will be judged on
«what matters — accuracy, cost, interpretability, time».»

## What you are given

| Item | Location | Notes |
| :--- | :--- | :--- |
| «Dataset / map / logs» | `«relative path»` | «rows, columns, known quirks» |
| «Starter code» | `«relative path or "none"»` | «what it already does» |
| «Constraints» | — | «runtime limit, no GPU, interpretability requirement» |

**Not provided:** «say explicitly what the student must not expect to be handed, e.g. a cleaned
dataset, tuned hyperparameters, a reference implementation».

## Requirements

**Functional**

- R1 — «The system must … for input …»
- R2 — «It must report … in this form …»
- R3 — «It must handle «edge case» without crashing.»

**Non-functional**

- N1 — «Runs in under «n» seconds on a CPU laptop.»
- N2 — «Results are reproducible: same seed → same output.»
- N3 — «Every reported number is produced by committed code, not typed by hand.»

## Tasks

1. **«Load and inspect»** — «produce X» *(success: you can state «the fact they should discover»)*
2. **«Implement the baseline»** — «produce X» *(success: «metric» is at least «value»)*
3. **«Apply the module technique»** — «produce X»
4. **«Evaluate and compare»** — «produce a table with …»
5. **«Diagnose a failure»** — «find one case where the method fails and explain the mechanism»
6. **«Recommend»** — «write three sentences to the stakeholder, including one limitation»

## Deliverables

| File | Contents |
| :--- | :--- |
| `«solution.py»` or `«notebook.ipynb»` | «Working implementation, runnable top to bottom» |
| `«report.md»` | «≤ 600 words: approach, results table, failure analysis, recommendation» |
| `«figure.png»` | «One clearly labelled figure: «what it must show»» |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Correctness | 30% | «All requirements met, edge case handled» | «Core works, edge case fails» | «Outputs do not match the spec» |
| Method justification | 25% | «Choice justified against an alternative, with evidence» | «Method named, weakly justified» | «Method applied without reason» |
| Evaluation | 20% | «Right metric, baseline, honest error analysis» | «Metric reported, no baseline» | «Single number, no context» |
| Code quality | 15% | «Readable, modular, reproducible» | «Works, hard to follow» | «Does not run» |
| Communication | 10% | «Stakeholder could act on the report» | «Understandable» | «Unclear or missing» |

## Extension challenges

1. **«Harder variant»** — «e.g. make the environment stochastic and keep the guarantee».
2. **«Scale or robustness»** — «e.g. 100× more nodes; what breaks first?»
3. **«Different objective»** — «e.g. optimise for worst case instead of average».

## Hints

<details><summary>Hint 1 — getting started</summary>

«A nudge about where to begin, not a solution.»

</details>

<details><summary>Hint 2 — the likely sticking point</summary>

«Name the conceptual trap and the question to ask yourself.»

</details>

<details><summary>Hint 3 — checking your work</summary>

«A sanity check the student can run: the expected order of magnitude, or an invariant.»

</details>

## Reflection

1. «Which requirement was hardest to satisfy, and what does that tell you about the method?»
2. «What would you do differently with «twice the data / more time / a GPU»?»
3. «Where could this system cause harm, and what would you monitor?»

## Time budget

| Session | Tasks | Time |
| :--- | :--- | ---: |
| 1 | 1–3 | ««60–90» min» |
| 2 | 4–6 | ««60–90» min» |
