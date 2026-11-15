# L02-02 — Rational Agents and PEAS Descriptions

| Module | M02 · Intelligent Agents and Environments |
| :--- | :--- |
| Level | 200 |
| Study time | 80 minutes |
| Prerequisites | [L02-01](L02-01-agents-percepts-actions.md) · [LP01-05](../../../prerequisites/P01-python-programming/lessons/LP01-05-objects-modules-exceptions-and-files.md) |
| Code | [`code/agents.py`](../code/agents.py) — agent architectures; [`code/environments.py`](../code/environments.py) — worlds |

[← Previous: L02-01](L02-01-agents-percepts-actions.md) · [Next: L02-03 Task Environments →](L02-03-task-environments-and-properties.md)

## 1. Learning Objectives

- **Define** rationality as expected performance given the percept sequence and the agent's knowledge.
- **Write** a PEAS description whose performance measure is measurable, not aspirational.
- **Distinguish** rationality from omniscience, and explain why a rational agent can still fail.
- **Diagnose** a performance measure that rewards the wrong behaviour.

## 2. Prerequisite Knowledge

Percepts, actions, agent function and the agent–environment boundary —
[L02-01](L02-01-agents-percepts-actions.md). You will write small classes, so
[LP01-05](../../../prerequisites/P01-python-programming/lessons/LP01-05-objects-modules-exceptions-and-files.md)
is assumed.

## 3. Conceptual Explanation

### 3.1 Rationality, precisely

A rational agent chooses the action expected to maximise its performance measure, given

1. the percept sequence so far,
2. whatever built-in knowledge it has,
3. the actions available.

"Expected" is doing the work. Rationality is not correctness and not success: a rational agent that
buys a lottery ticket can lose, and an irrational one can win.

### 3.2 Omniscience is impossible, and not required

An omniscient agent knows the actual outcome of its actions. No real agent does. Rationality asks
only for the best *expected* choice given what can be known — which is why **information gathering**
is a rational action: paying for a sensor can be worth more than acting blind.

### 3.3 PEAS

| Letter | Question | Bad answer | Good answer |
| :--- | :--- | :--- | :--- |
| **P**erformance | How is success measured? | "customer satisfaction" | median resolution time; reopen rate |
| **E**nvironment | What does it act in? | "the internet" | ticket queue, order database, email |
| **A**ctuators | How does it act? | "replies to customers" | send_email, update_order, escalate |
| **S**ensors | What does it perceive? | "the situation" | ticket text, order status, SLA clock |

The performance measure is the specification. Everything else in the design is downstream of it, and
almost every "the AI behaved badly" story is a performance-measure story.

### 3.4 Autonomy

An agent is autonomous to the extent its behaviour is determined by its own experience rather than
only by built-in knowledge. A thermostat with a fixed rule has low autonomy; a system that adjusts its
own thresholds from outcomes has more. Autonomy is a dial, not a badge.

## 4. Pseudocode

```text
function RATIONAL-AGENT(percept_sequence) -> action:
    beliefs <- UPDATE(beliefs, percept_sequence)
    candidates <- ACTIONS(state)
    return argmax over a in candidates of E[performance | a, beliefs]
```

## 5. Worked Example — two PEAS descriptions

**A. Hospital triage assistant**

- Performance: patients seen within target time; harm events; clinician override rate (lower is better *if* the advice is good).
- Environment: emergency department queue, vitals, triage notes.
- Actuators: set priority, page clinician, request test.
- Sensors: vitals monitor, notes, waiting-room count.

Note the third performance component: without it, a system that always says "urgent" scores well on
time-to-treatment and destroys the department.

**B. Warehouse picking robot**

- Performance: items picked per hour, mis-picks per 1,000, collision count.
- Environment: aisles, shelves, other robots, humans.
- Actuators: wheels, lift, arm, status light.
- Sensors: lidar, camera, weight sensor, fleet messages.

Design consequence: mis-picks and collisions are in the measure, so the agent cannot trade safety for
speed without the measure noticing.

## 6. Mathematical Formulation

$$a^\* = \arg\max_{a \in A} \sum_{o} P(o \mid a, \text{beliefs})\,U(o)$$

If the agent's utility is linear in two objectives with a trade-off weight $\lambda$:

$$U = \text{throughput} - \lambda \cdot \text{errors}$$

$\lambda$ is a policy decision, not a technical one. Write it down, and say who chose it.

## 7. Python Implementation

The module's runnable agents are in [`code/agents.py`](../code/agents.py); the snippet below is the
performance-measure half of the idea — a scoring function you can inspect and argue with.

```python
from dataclasses import dataclass


@dataclass
class PEAS:
    performance: str
    environment: str
    actuators: list
    sensors: list

    def is_complete(self):
        return bool(self.performance and self.environment
                    and self.actuators and self.sensors)


def evaluate(measure, trace):
    """Score an agent's run with an explicit, inspectable measure."""
    picked = sum(1 for step in trace if step["action"] == "pick" and step["ok"])
    mispicks = sum(1 for step in trace if step["action"] == "pick" and not step["ok"])
    collisions = sum(1 for step in trace if step["event"] == "collision")
    return {"picked": picked, "mispicks": mispicks,
            "score": picked - 10 * mispicks - 50 * collisions,
            "measure": measure}


trace = [{"action": "pick", "ok": True}, {"action": "pick", "ok": False},
         {"action": "move", "event": "collision"}]
print(evaluate("picked - 10*mispicks - 50*collisions", trace))
```

```text
{'picked': 1, 'mispicks': 1, 'score': -59, 'measure': 'picked - 10*mispicks - 50*collisions'}
```

The weights are visible and arguable — which is the point of writing the measure as code.

## 8. Practical Applications

- **Support automation** — resolution time plus reopen rate plus escalation accuracy.
- **Recommendation** — click-through plus retention; CTR alone rewards clickbait.
- **Industrial control** — throughput plus defect rate plus safety interlocks.
- **Research assistants** — answer acceptance plus citation correctness.

## 9. Common Mistakes

- Naming a performance measure that nobody can compute, so it is never checked.
- Rewarding a proxy and being surprised at the proxy's optimum (clicks, minutes, keystrokes).
- Assuming rationality implies success, then blaming the algorithm for bad luck.
- Omitting safety or quality terms, so the agent trades them away optimally.
- Writing PEAS for the algorithm instead of for the environment the algorithm will meet.

## 10. Exercises

1. Write a PEAS description for a lift controller, then for the same building's fire-evacuation system; identify which measure dominates.
2. Take a deployed system you use and write the performance measure its behaviour implies (not the one its documentation claims).
3. Add a third objective to the warehouse measure and show how $\lambda$ changes the chosen action in a two-action example.
4. Find a case where information gathering is the rational action, and say what the sensor must cost to change the decision.

## 11. Self-Assessment

1. Define rationality without using the word "success".
2. Why is information gathering sometimes the rational action?
3. What does a PEAS description miss if the performance measure is vague?
4. Give an example of a proxy measure that is easier to compute and worse to want.

## 12. Key Terms

**Rationality**, **performance measure**, **PEAS**, **omniscience**, **autonomy**, **information gathering**, **proxy measure**, **utility trade-off**.

## 13. Further Reading

- Russell & Norvig, chapter 2 §2.2–2.3.
- Goodhart (1975) on measures that cease to be good measures when used as targets.

## What to Do Next

[L02-03](L02-03-task-environments-and-properties.md) classifies the environment your agent will face;
the classification decides which architecture can work at all.
