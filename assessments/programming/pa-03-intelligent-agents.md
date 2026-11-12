# PA-03 — An Agent for a Partly Observable Environment

| | |
| :--- | :--- |
| Assignment | 03 |
| Difficulty | Intermediate |
| Estimated time | 4 hours |
| Prerequisites | M02 (L02-01 … L02-05), P01 |
| Covers | PEAS, agent architectures, state estimation, environment simulation |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

A cleaning robot must decide where to go using only local sensors: it sees the current cell, not the
building. The assignment asks you to build the environment, four agents, and the measurement that
distinguishes them — because an agent that "looks smarter" is not necessarily better.

## Problem scenario

A 5×5 building with dirt in random cells and a charging station. The robot's percept is
`(cell_dirty, wall_north, wall_east, wall_south, wall_west, battery)`. It acts: `suck`, `move(dir)`,
`charge`. Dirt accumulates slowly. The episode ends after 200 steps.

## Learning outcomes

1. Write a PEAS description that names a measurable performance measure.
2. Implement reflex, model-based, goal-based and utility-based agents against one interface.
3. Implement state estimation under partial observability.
4. Compare agents on the same seeds and report the distribution of outcomes.

## Tasks

1. **Environment.** Implement the simulator with seeded dirt placement and a step limit.
2. **PEAS.** Write the description; the performance measure must be a single number per episode.
3. **Agents.** Implement four: simple reflex, model-based (internal map), goal-based (return to
   charger when battery < 20%), utility-based (expected utility over dirt, battery and distance).
4. **Comparison.** Run each agent on 100 seeds; report mean, median and interquartile range of the
   performance measure.
5. **Failure analysis.** For the worst seed of the best agent, print a trace and explain the failure.
6. **Ablation.** Remove the internal map from the model-based agent and report the change.

## Constraints

- No reinforcement learning; this is about architecture, not training.
- Seeded randomness; the same seed set for every agent.
- One interface: `act(percept) -> action`.

## Expected deliverables

`env.py`, `agents.py`, `run_experiment.py`, `results.md` with the comparison table and one trace,
and a README with the PEAS description.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Environment and PEAS | 20% | measure is single-valued and fits the task |
| Architectures | 30% | four agents implement the stated designs, not aliases |
| Comparison | 25% | same seeds, distribution reported, not just the mean |
| Failure analysis | 15% | one trace explained mechanistically |
| Code quality | 10% | interface respected, no duplicated simulator logic |

## Bonus challenges

- Add a second dirt type that requires two `suck` actions and report which agent adapts with no code
  change.
- Measure how performance degrades as sensor noise increases from 0% to 20%.

---

[Assessment index](../README.md) · [PA-02](pa-02-search-algorithms.md) · [PA-04](pa-04-knowledge-based-systems.md)
