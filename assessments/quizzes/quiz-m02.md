# QUIZ-M02 — Intelligent Agents and Environments

| | |
| :--- | :--- |
| Module | M02 · Intelligent Agents and Environments |
| Questions | 12 (20 marks) |
| Time | 30 minutes |
| Covers | L02-01 … L02-05 |
| Pass mark | 12 / 20 |

> **Availability.** This module's lessons, notebooks and labs are published in this repository; sit this paper after finishing them.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m02.md) · [Module](../../modules/README.md#m02)

Answer on paper first. Part D needs arithmetic you can do by hand; Part E needs a table.

---

## Part A — Multiple choice (3 marks)

**Q2.1** A vacuum robot's percept is (floor state, current position). Which environment property
does this **not** determine?

- A. Whether the environment is fully observable
- B. Whether the environment is deterministic
- C. Whether the agent is rational
- D. Whether the environment is static

**Q2.2** Which architecture must maintain internal state?

- A. Simple reflex agent
- B. Model-based reflex agent
- C. Table-driven agent
- D. A stateless classifier

**Q2.3** In a PEAS description for an automated trading agent, "profit after costs and risk limits"
belongs under

- A. Performance measure
- B. Environment
- C. Actuators
- D. Sensors

## Part B — True or false, with a reason (2 marks)

**Q2.4** "A rational agent always chooses the action that turns out to have the best outcome."

## Part C — Conceptual (4 marks)

**Q2.5** (2 marks) Explain why a simple reflex agent cannot be rational in a partially observable
environment, even with a perfect rule table.

**Q2.6** (2 marks) Give one concrete task environment that is *static* and one that is *dynamic*,
and say what changes for the agent's design.

## Part D — Numerical (6 marks)

**Q2.7** (3 marks) An agent has three binary sensors and four actions. How many distinct percepts
exist? How many distinct percept sequences of length 3? If a table-driven agent stores one action
per percept, how many entries does its table need?

**Q2.8** (3 marks) A grid has 25 cells, the agent can move in 4 directions with no obstacles, and
bumping into a wall leaves it in place. What is the branching factor, and how many nodes are
generated at depth 2 (including duplicates)?

## Part E — Tracing (3 marks)

**Q2.9** Trace this reflex agent for three percepts and give the sequence of actions:

| Percept (location, status) | Rule |
| :--- | :--- |
| (A, dirty) | Suck |
| (A, clean) | Move right |
| (B, dirty) | Suck |
| (B, clean) | Move left |

Inputs: (A, dirty), (A, clean), (B, dirty).

## Part F — Python output (2 marks)

**Q2.10** What does this print?

```python
rules = {("dirty", "A"): "suck", ("clean", "A"): "right"}
percepts = [("dirty", "A"), ("dirty", "B"), ("clean", "A")]
print([rules.get(p, "no-op") for p in percepts])
```

## Part G — Short answer (4 marks)

**Q2.11** (2 marks) A delivery robot's environment is partly observable, stochastic and dynamic.
Name one design change each property forces on the agent.

**Q2.12** (2 marks) Why is the PEAS description useful *before* any code is written? Give one
failure that a PEAS exercise prevents.

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m02.md) · [Next quiz](quiz-m03.md)
