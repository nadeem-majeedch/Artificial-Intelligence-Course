# L02-03 — Task Environments and Their Properties

| Module | M02 · Intelligent Agents and Environments |
| :--- | :--- |
| Level | 200 |
| Study time | 80 minutes |
| Prerequisites | [L02-02](L02-02-rational-agents-and-peas.md) |
| Code | [`code/environments.py`](../code/environments.py), [`code/agents.py`](../code/agents.py) |

[← Previous: L02-02](L02-02-rational-agents-and-peas.md) · [Next: L02-04 Reflex and Model-Based Agents →](L02-04-simple-reflex-and-model-based-agents.md)

## 1. Learning Objectives

- **Classify** an environment on the standard dimensions and justify each classification.
- **Predict** which algorithm families fit an environment from its properties.
- **Explain** why partial observability forces an internal state, and why stochasticity forces expected values.
- **Identify** the property that most changes a design decision in a given system.

## 2. Prerequisite Knowledge

PEAS and rationality — [L02-02](L02-02-rational-agents-and-peas.md).

## 3. Conceptual Explanation

### 3.1 The dimensions

| Property | Question | Consequence |
| :--- | :--- | :--- |
| Fully / partially observable | do the sensors see the whole state? | partial ⇒ internal state estimate |
| Deterministic / stochastic | is the outcome of an action certain? | stochastic ⇒ expected values, risk |
| Episodic / sequential | does this decision affect later ones? | sequential ⇒ planning, long horizon |
| Static / dynamic | does the world change while deciding? | dynamic ⇒ deadlines, anytime algorithms |
| Discrete / continuous | are states and actions countable? | continuous ⇒ optimisation, not enumeration |
| Single / multi-agent | are there other decision makers? | multi ⇒ game theory, coordination |
| Known / unknown | is the transition model known? | unknown ⇒ learning, exploration |

### 3.2 The two that matter most

**Partial observability** is what turns a lookup table into a model-based agent: the agent must
remember what it has seen because the current percept does not contain the answer.

**Stochasticity** is what turns a plan into a policy: with certain outcomes you choose a sequence;
with uncertain outcomes you choose a decision rule that can respond to what happens.

### 3.3 Chess and taxi driving

| | Chess | Taxi driving |
| :--- | :--- | :--- |
| Observable | fully | partially |
| Deterministic | yes (rules) | no (traffic, pedestrians) |
| Episodic | sequential | sequential |
| Static | yes | dynamic |
| Discrete | yes | continuous |
| Agents | two | many |

Chess admits exhaustive search with a perfect model. Driving admits none of that, which is why the two
subfields developed different methods — the environment, not the ambition, chose them.

## 4. Pseudocode — the loop that respects the environment

```text
function RUN(agent, env, steps):
    percept <- env.observe()
    total <- 0
    for t in 1..steps:
        action <- agent.act(percept)
        outcome <- env.step(action)        # may be stochastic
        percept <- outcome.percept
        total <- total + outcome.reward
        if outcome.done: break
    return total
```

## 5. Worked Example — classifying a warehouse robot

- **Partially observable**: a pallet behind a shelf is unseen, so the robot keeps a map.
- **Stochastic**: wheels slip; an action "move forward" lands with probability 0.9.
- **Sequential**: today's route changes tomorrow's battery state.
- **Dynamic**: humans move while the robot plans, so plans are re-evaluated frequently.
- **Continuous**: positions are real numbers.
- **Multi-agent**: other robots share aisles.
- **Known model**: aisle geometry is mapped; slip probability is measured.

Consequence: model-based, replanning, risk-aware — and never a pure lookup agent.

## 6. Mathematical Formulation

A stochastic, sequential environment is a Markov decision process
$(\mathcal{S}, \mathcal{A}, T, R, \gamma)$ with

$$T(s,a,s') = P(s' \mid s,a), \qquad
V^\pi(s) = \mathbb{E}\left[\sum_{t} \gamma^t R(s_t, \pi(s_t)) \,\middle|\, s_0 = s\right]$$

If the environment is also partially observable the agent maintains a belief
$b(s)$; a deterministic fully observable environment is the special case where $T$ is a point mass.

## 7. Python Implementation

```python
class GridWorld:
    """Fully/partially observable grid with optional slip."""

    def __init__(self, size=5, slip=0.0, observable=True, seed=0):
        import random
        self.size, self.slip, self.observable = size, slip, observable
        self.random = random.Random(seed)
        self.position = (0, 0)
        self.goal = (size - 1, size - 1)

    def observe(self):
        if self.observable:
            return {"position": self.position, "goal": self.goal}
        return {"bump": self.position[0] == 0}

    def step(self, action):
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        if self.random.random() < self.slip:                 # action fails: stay put
            pass
        else:
            dr, dc = moves[action]
            self.position = (min(max(self.position[0] + dr, 0), self.size - 1),
                             min(max(self.position[1] + dc, 0), self.size - 1))
        done = self.position == self.goal
        return {"percept": self.observe(), "reward": 1.0 if done else -0.01, "done": done}


env = GridWorld(size=3, slip=0.2)
print(env.observe(), env.step("right"))
```

## 8. Practical Applications

- **Autonomous vehicles** — partial, stochastic, dynamic, multi-agent, continuous.
- **Warehouse and factory robots** — partial, mildly stochastic, sequential, multi-agent.
- **Recommendation** — partially observable user state, stochastic response, sequential.
- **Medical decision support** — partial, stochastic, sequential, high stakes.

## 9. Common Mistakes

- Calling an environment deterministic because the rules are; sensor noise makes it stochastic.
- Ignoring the multi-agent property, then being surprised by congestion or oscillation.
- Treating a dynamic environment as static and shipping plans that are already stale.
- Labelling an unknown environment as stochastic — exploration is a different problem.
- Classifying the environment once and never revisiting it as the system grows.

## 10. Exercises

1. Classify three systems you use on all seven dimensions, and name the property that most affects the design.
2. Modify `GridWorld` to be partially observable and observable, and show which agent method must change.
3. Set `slip=0.5` and explain what a plan-based agent does wrong that a policy-based agent handles.
4. Add a second robot to the grid and describe the coordination failure you can produce in ten steps.

## 11. Self-Assessment

1. Which property forces an internal state estimate, and why?
2. Which property turns a plan into a policy?
3. Why does chess allow exhaustive search but driving not?
4. What is the difference between unknown and stochastic?

## 12. Key Terms

**Fully/partially observable**, **deterministic/stochastic**, **episodic/sequential**, **static/dynamic**, **discrete/continuous**, **single/multi-agent**, **known/unknown**, **MDP**, **belief state**.

## 13. Further Reading

- Russell & Norvig, section 2.3 — the environment-property table.
- Sutton & Barto, chapter 3 — MDPs as the formalisation of a stochastic environment.

## What to Do Next

[L02-04](L02-04-simple-reflex-and-model-based-agents.md) builds the two architectures that partial
observability separates.
