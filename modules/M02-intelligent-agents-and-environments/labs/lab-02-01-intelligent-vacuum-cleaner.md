# LAB-02-01 — The Intelligent Vacuum Cleaner

| | |
| :--- | :--- |
| Module | M02 · Intelligent Agents and Environments |
| Time | 2.5 hours |
| Level | 200 |
| Pairs with | L02-04, L02-05 |
| Code | [`code/agents.py`](../code/agents.py), [`code/environments.py`](../code/environments.py) |

[Module home](../README.md) · [Lab 2](lab-02-02-campus-navigation-agent.md) · [Notebook](../notebooks/nb-02-01-agent-loop-gridworld.ipynb)

## Scenario

A facilities company buys a hundred robot vacuums for an office floor. The supplier's firmware is a
simple reflex controller: *if the current cell is dirty, clean it; otherwise follow a fixed cycle*.
On the demo floor it works. On the real floor — partial sensors, furniture, two rooms — the robots clean
one corner repeatedly, exhaust their batteries, and the company refuses delivery.

You have one week to specify and demonstrate a better controller, and to explain to a non-technical
manager why the reflex controller was predictable rather than unlucky.

## Problem statement

Build and compare agent controllers for the same environment, and recommend one with evidence.

## Environment definition

`environments.GridWorld(width, height, dirt, seed)`:

| Property | Value |
| :--- | :--- |
| State | robot position, set of dirty cells, obstacle set |
| Actions | `up`, `down`, `left`, `right`, `suck`, `noop` |
| Percepts | **local**: `("local", (x,y), dirty, walls, bump)` or **full**: `("full", pos, dirt, obstacles)` |
| Transition | deterministic; walls block movement (`bump` reports it) |
| Reward | `+1` per cleaned cell, small step penalty; `performance` accumulates it |
| Episode | ends when all dirt is cleaned, or at the step limit |

Classified on the L02-03 dimensions: partially observable (local percept), deterministic, sequential,
static, discrete, single-agent, model partially known.

## Agent requirements

- **R1** A reflex controller that is *complete*: every percept maps to an action, with no unmatched case.
- **R2** A model-based controller that maintains a belief map from local percepts only.
- **R3** A goal-based controller that plans to the nearest known dirt with an explicit goal test.
- **R4** A utility-based controller whose utility function is written down and justified.
- **R5** At least three measured runs per controller on at least three floor layouts, reported as steps, cells cleaned and score.
- **R6** One page explaining the reflex controller's failure to a manager, without jargon.

## Implementation tasks

1. **Baseline** (20 min). Run `python code/agents.py`; record the five architectures' numbers.
2. **Local-percept world** (30 min). Instantiate `GridWorld` with the local percept and confirm the reflex agent's partial failure.
3. **Belief map** (40 min). Extend or re-implement `ModelBasedAgent` so bumps are learned and never retried; measure the step reduction.
4. **Planner** (30 min). Make the goal-based agent clean the nearest known dirt, then re-plan when dirt disappears.
5. **Utility** (30 min). Add a battery term (each move costs 0.5, cleaning returns 1) and show a case where the utility agent and the goal agent diverge.
6. **Report** (20 min). Table of results plus the manager page.

## Starter code

```python
from environments import GridWorld
from agents import ReflexAgent, ModelBasedAgent, GoalBasedAgent, UtilityBasedAgent, run_episode

LAYOUTS = [{(1, 1), (3, 2)}, {(0, 3), (2, 0), (3, 3)}, {(2, 2)}]
for dirt in LAYOUTS:
    for factory in (ReflexAgent, ModelBasedAgent, GoalBasedAgent, UtilityBasedAgent):
        world = GridWorld(width=4, height=4, dirt=set(dirt), seed=1)
        world.reset(dirt=set(dirt))
        print(dirt, run_episode(factory(), world, max_steps=60))
```

## Expected behaviour

- Reflex: cleans at most one cell on the two-room layouts; score negative; never terminates early.
- Model-based: cleans every cell on all three layouts; more steps than the planner.
- Goal-based: fewer steps than model-based on every layout; equal or better score.
- Utility-based: matches or beats goal-based once the battery term is in, and never enters a cell that costs more than it gains.

## Testing

| Test | Expected |
| :--- | :--- |
| Reflex completeness | every local percept produces a valid action |
| Belief correctness | after visiting a cell, the map agrees with the world |
| Bump handling | a wall learned once is not attempted again |
| Goal test | episode ends in fewer than 60 steps on all layouts |
| Determinism | same seed, same result, twice |
| Utility sanity | a move with negative utility is never chosen |

## Deliverables

| File | Contents |
| :--- | :--- |
| `vacuum_agents.py` | Your controllers |
| `results.md` | Table of runs, three layouts, four architectures |
| `manager_note.md` | ≤ 300 words, no jargon |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Correctness | 30% | all layouts cleaned; belief map correct | most layouts | one layout |
| Comparison | 25% | measured table, three architectures, explained | numbers only | no measurement |
| Design | 20% | clean separation of percept, state, decision | works | tangled |
| Testing | 15% | tests above, all passing | partial | none |
| Communication | 10% | manager can act on the note | understandable | jargon |

## Extension challenges

1. Add a second robot and a simple coordination rule; measure duplicate cleaning.
2. Make the environment stochastic (10% slip) and compare all controllers again.
3. Replace the hand-written utility with one learned from episodes; compare policy quality.
4. Add battery management as a hard constraint rather than a cost, and describe what changes.

## Reflection

1. Which requirement of the manager's problem did the reflex controller violate, in one sentence?
2. Your best controller uses more code. What did the extra code buy, measured?
3. Where would you put a learning element, and what reward would you give it?

---

[Module home](../README.md) · [Lab 2](lab-02-02-campus-navigation-agent.md) · [Notebook](../notebooks/nb-02-01-agent-loop-gridworld.ipynb)
