# LAB-02-02 — Intelligent Campus Navigation Agent

| | |
| :--- | :--- |
| Module | M02 · Intelligent Agents and Environments |
| Time | 3 hours |
| Level | 200 |
| Pairs with | L02-03, L02-05 |
| Code | [`code/agents.py`](../code/agents.py), [`code/environments.py`](../code/environments.py) |

[Module home](../README.md) · [Lab 1](lab-02-01-intelligent-vacuum-cleaner.md)

## Scenario

A university wants a phone assistant that walks a new student from the main gate to a room, then to
the library, then back to the gate. The campus map is incomplete: corridors are known, but doors,
closures and lifts are not. The assistant has GPS (noisy), a camera (sees signs), and the student's
own description ("I'm near the café").

You must specify the agent, then implement the decision layer against the module's grid abstraction so
the behaviour is testable without a phone.

## Problem statement

Design an agent that navigates an unknown, partially observable campus grid with multiple sequential
goals, and demonstrate that it degrades sensibly when the environment misbehaves.

## Environment definition

| Property | Value |
| :--- | :--- |
| Grid | up to 12×12, walls = closed corridors, obstacles = furniture |
| Percepts | local (cell, sign text, walls, bump) or full (position, goals, obstacles) |
| Actions | four moves, `noop`, `suck` unused |
| Transition | deterministic by default; option to add 10% slip |
| Reward | `+10` per goal reached, `-0.1` per step, `-1` per bump |
| Episode | ends when all goals are visited, or the step limit |

Classification: partially observable, deterministic or stochastic, sequential, dynamic in the real
deployment, discrete, multi-agent in reality (other students), unknown map.

## Agent requirements

- **R1** A `PEAS` description as a table, with a measurable performance measure.
- **R2** A goal-based controller that navigates to each goal in order and re-plans when a wall is discovered.
- **R3** A utility-based controller that prefers the shorter of two known routes and avoids revisiting.
- **R4** An explicit handling of a failed move (bump): what the agent knows afterwards, and what it does next.
- **R5** A report of behaviour under the deterministic and the 10%-slip environment.
- **R6** A stated failure mode: one scenario in which your agent should ask the human for help, and how it detects that it is in one.

## Implementation tasks

1. **Model** (25 min). Write the PEAS table and the environment classification with justifications.
2. **Map** (40 min). Represent the known map; update it from percepts and bumps.
3. **Multi-goal planner** (50 min). Plan to the next unvisited goal; re-plan after each discovery.
4. **Utility layer** (35 min). Add step cost and bump cost; show the chosen route for two layouts.
5. **Robustness** (30 min). Add slip; measure success rate over 20 episodes and the effect on re-planning.
6. **Help-seeking** (20 min). Define the condition ("no known route to the next goal and no unexplored reachable cell") and demonstrate it.

## Starter code

```python
from environments import GridWorld
from agents import GoalBasedAgent, UtilityBasedAgent, run_episode

world = GridWorld(width=8, height=8, dirt={(7, 7), (0, 7)}, seed=3)   # goals stand in for rooms
world.reset(dirt={(7, 7), (0, 7)})
print(run_episode(GoalBasedAgent(width=8, height=8), world, max_steps=200))
```

The vacuum abstraction is reused deliberately: a "dirty" cell is a goal to be visited, so the existing
goal-based agent is the baseline your agent must beat on steps.

## Expected behaviour

- Deterministic: all goals visited in a single episode; steps within ~20% of the shortest tour.
- With 10% slip: occasional re-planning; success rate above 0.9 over 20 episodes, with the failures reported rather than hidden.
- On a closed corridor: the agent marks it unusable and routes around it, or triggers the help condition.
- No episode revisits a cell more than twice when a shorter route is known.

## Testing

| Test | Expected |
| :--- | :--- |
| Map consistency | known map ⊆ true map after every step |
| Multi-goal order | goals visited in the specified order |
| Re-planning | a newly discovered wall changes the next action within 2 steps |
| Slip robustness | ≥ 18 of 20 episodes succeed at 10% slip |
| Help condition | triggers on a fully enclosed goal, not on a reachable one |
| Determinism | same seed → same trace |

## Deliverables

| File | Contents |
| :--- | :--- |
| `campus_agent.py` | Controllers plus map |
| `peas.md` | The PEAS table and classification |
| `results.md` | Deterministic and slip measurements, success rates, one trace |
| `handover.md` | ≤ 400 words: what it does, when it asks for help |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Environment model | 25% | classification justified, measure measurable | listed | vague |
| Navigation | 30% | goals in order, re-plans, near-shortest | reaches goals | wanders |
| Robustness | 20% | slip measured, failures reported | runs | crashes |
| Help condition | 15% | precise, tested both ways | stated | absent |
| Documentation | 10% | handover usable | readable | missing |

## Extension challenges

1. Add a second student agent and a corridor with capacity one; describe the deadlock and a rule that breaks it.
2. Make GPS noisy (percept position wrong 10% of the time) and show how belief maintenance copes.
3. Add an unknown "lift" action that moves between floors; classify the new environment.
4. Compare goal-based and utility-based controllers over 20 random layouts and report where they differ.

## Reflection

1. Which environment property made a reflex controller impossible here?
2. Your agent asks for help when it cannot find a route. Is that a failure or a feature?
3. What would you need to add to make this a learning agent?

---

[Module home](../README.md) · [Lab 1](lab-02-01-intelligent-vacuum-cleaner.md)
