# L02-04 — Simple Reflex and Model-Based Agents

| Module | M02 · Intelligent Agents and Environments |
| :--- | :--- |
| Level | 200 |
| Study time | 85 minutes |
| Prerequisites | [L02-03](L02-03-task-environments-and-properties.md) · [LP01-05](../../../prerequisites/P01-python-programming/lessons/LP01-05-objects-modules-exceptions-and-files.md) |
| Code | [`code/agents.py`](../code/agents.py) (`ReflexAgent`, `ModelBasedAgent`) · [`code/environments.py`](../code/environments.py) |

[← Previous: L02-03](L02-03-task-environments-and-properties.md) · [Next: L02-05 Goal, Utility and Learning Agents →](L02-05-goal-utility-and-learning-agents.md)

## 1. Learning Objectives

- **Implement** a simple reflex agent as condition–action rules and state its two failure conditions.
- **Implement** a model-based reflex agent that maintains belief state from percepts.
- **Explain** what internal state buys, in terms of the environment property that forces it.
- **Measure** the difference between the two agents on the same world.

## 2. Prerequisite Knowledge

Environment properties — [L02-03](L02-03-task-environments-and-properties.md) — and classes in Python
([LP01-05](../../../prerequisites/P01-python-programming/lessons/LP01-05-objects-modules-exceptions-and-files.md)).

## 3. Conceptual Explanation

### 3.1 Simple reflex agents

```text
percept ──▶ [ condition–action rules ] ──▶ action
```

The agent looks up the rule whose condition matches the current percept. It has no memory, so:

- it **fails under partial observability** — the percept does not contain the information the rule
  would need;
- it **loops** in environments where the same percept recurs without progress (two cells, alternating
  moves, forever).

Rules must be *complete* over percepts: an unmatched percept leaves the agent with no action, which is
a bug, not a fallback.

### 3.2 Model-based reflex agents

```text
percept ──▶ [ state update: how the world evolves + what my actions do ] ──▶ belief state
belief  ──▶ [ condition–action rules ] ──▶ action
```

The agent keeps *how the world evolves* (a transition model) and *what its actions do*, folds each
percept into a belief state, and applies rules to the belief rather than the raw percept. This is what
partial observability forces: the answer is not in the current percept.

The cost is **belief maintenance**. Every update can be wrong, and a wrong belief persists and compounds.
A model-based agent that mis-maps a wall will keep bumping into it.

### 3.3 The comparison the module measures

The module's `GridWorld` gives a *local* percept (my cell, is it dirty, walls, bumped?) and a *full*
percept (position, all dirt, all obstacles). With the local percept:

- `ReflexAgent` can clean the cell it is in, but cannot know where it has been → it sweeps a fixed
  cycle and cleans whatever it meets.
- `ModelBasedAgent` remembers visited cells, builds a wall map, and heads for the nearest unvisited
  cell by breadth-first search over its *believed* map.

## 4. Pseudocode

```text
function REFLEX-AGENT(percept):
    for rule in RULES:
        if rule.condition(percept): return rule.action

function MODEL-BASED-AGENT(percept):
    state <- UPDATE-STATE(state, action_last, percept, model)
    for rule in RULES:
        if rule.condition(state): return rule.action
```

## 5. Worked Example — four steps in a 4×4 world

Local percept format: `("local", (x, y), dirty, walls, bump)`.

| Step | Percept | Reflex | Model-based |
| ---: | :--- | :--- | :--- |
| 1 | (0,0) clean, no walls | `right` (cycle) | goal unknown → nearest unvisited: `right` |
| 2 | (1,0) dirty | `suck` | `suck` |
| 3 | (1,0) clean | `down` (cycle) | nearest unvisited: `down` |
| 4 | (1,1) clean, bumped earlier | `left` | `right` (unvisited cell east) |

Both clean dirt they stand on. They diverge as soon as the question becomes "where have I not been?" —
which is exactly the question a reflex agent cannot represent.

## 6. Mathematical Formulation

Belief update is a deterministic special case of the Bayes filter:

$$b'(s') = \eta \, O(o \mid s', a) \sum_{s} T(s' \mid s, a)\, b(s)$$

With a deterministic, fully observed cell and a known map, $O$ is an indicator and $b'$ is a point
mass — the map the agent carries. Cost per step is $O(1)$ for the reflex rule and $O(|S|)$ for the
belief update, plus $O(|S|)$ for the BFS planning step.

## 7. Python Implementation

```python
# The module's implementations, abridged. Full versions: code/agents.py
from environments import GridWorld, ACTIONS
from agents import ReflexAgent, ModelBasedAgent, run_episode

world = GridWorld(width=4, height=4, dirt={(1, 1), (3, 2)}, seed=1)
for factory in (ReflexAgent, ModelBasedAgent):
    world.reset(dirt={(1, 1), (3, 2)})
    print(run_episode(factory(), world))
```

```text
{'agent': 'reflex', 'steps': 60, 'cleaned': 1, 'performance': -49}
{'agent': 'model-based', 'steps': 15, 'cleaned': 2, 'performance': 7}
```

Measured on this repository (`python code/agents.py`, seed 1). The reflex agent runs out of steps
having cleaned one of the two dirt cells: its fixed cycle meets the dirt at (1,1) but never reaches
(3,2) systematically. The model-based agent finishes the task in 15 steps. For reference, the random
baseline scores −34 after 60 steps with one cell cleaned.

## 8. Practical Applications

- **Reflex** — thermostats, over-temperature trips, spam keyword blocks, safety interlocks.
- **Model-based** — robot vacuum mapping a room, a vehicle tracking its pose, a service that tracks
  which alerts it has already acknowledged.

A useful engineering rule: start reflex, and move to model-based only when you can name the state the
percept omits.

## 9. Common Mistakes

- Giving the reflex agent a rule that depends on a variable it cannot perceive (e.g. "if this cell was
  cleaned before").
- Letting the model-based agent's map grow forever, then discovering the memory cost.
- Treating a bump percept as an error rather than as information about the world.
- Re-planning from scratch every step when the map has not changed.
- Assuming a model-based agent is automatically better; it is better *if the model is right*.

## 10. Exercises

1. Write a reflex agent that solves the 4×4 world with two dirt cells using only local percepts. Explain why it cannot generalise to a random layout.
2. Add bump handling to `ModelBasedAgent` so that a wall learned once is never re-tried; measure the step reduction.
3. Instrument both agents to count "wasted" steps (no dirt cleaned, no new cell visited).
4. Give the reflex agent an explicit loop detector and show what it does instead of cycling.

## 11. Self-Assessment

1. What are the two conditions under which a simple reflex agent fails?
2. What two things does the internal state of a model-based agent model?
3. Why is the belief state a probability distribution in general?
4. When is a reflex agent the better engineering choice?

## 12. Key Terms

**Condition–action rule**, **internal state**, **belief state**, **transition model**, **state update**, **bump percept**, **exploration policy**.

## 13. Further Reading

- Russell & Norvig, sections 2.4.1–2.4.3.
- Thrun, Burgard & Fox, *Probabilistic Robotics*, chapter 2 — belief state in practice.

## What to Do Next

[L02-05](L02-05-goal-utility-and-learning-agents.md) adds goals, utilities and the ability to improve
from experience.
