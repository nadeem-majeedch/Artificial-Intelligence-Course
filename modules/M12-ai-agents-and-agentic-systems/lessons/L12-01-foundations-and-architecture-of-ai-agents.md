# L12-01 — Foundations and Architecture of AI Agents

| Module | M12 · AI Agents and Agentic AI Systems |
| :--- | :--- |
| Level | 400 |
| Study time | 75 minutes |
| Prerequisites | [L02-01](../../M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md) · [L11-04](../../M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md) |
| Code | `code/agent_core.py`, `code/agent_data.py` |

[← Module start](../README.md) · [Next: L12-02 Tool Calling →](L12-02-llm-agents-tool-calling-and-structured-outputs.md)

## 1. Learning Objectives

- **Distinguish** a model call from an agent: the loop, the state, the tools and the stopping rule.
- **Draw** the architecture of an agent as four components and name the failure mode of each.
- **Implement** a bounded loop with a logged termination reason.
- **Explain** why "agent" is an engineering claim about control flow, not about intelligence.

## 2. Prerequisite Knowledge

The agent vocabulary from [L02-01](../../M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)
(percept, action, environment type) and prompting from
[L11-04](../../M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md).

## 3. Conceptual Explanation

### 3.1 What makes a system agentic

A single model call maps input to output. An agent adds three things: a **loop** (it acts, observes,
decides again), **tools** (it affects or inspects the world), and a **stopping rule** (a budget, a
goal test, or a human decision). Remove any of the three and you have a pipeline, not an agent.

### 3.2 The four components

| Component | Job | Typical failure |
| :--- | :--- | :--- |
| Policy | choose the next action | loops, or chooses an action it cannot justify |
| Tools | execute actions with schemas | malformed arguments, unauthorised effect |
| State | remember what happened | grows unbounded, contradicts itself |
| Controller | enforce budget, permissions, termination | never stops, or stops before the goal |

### 3.3 The loop is the risk

Every extra iteration multiplies cost and the chance of an unrecoverable action. Production agents
are therefore designed around **bounded** loops: a maximum step count, a token budget, a wall-clock
timeout, and a termination reason that is logged. "It stopped eventually" is not a termination
policy.

### 3.4 Determinism first

The reference code in this module uses a deterministic stand-in for the model, so every behaviour
in the lessons is reproducible. That is not a shortcut: it is how you test an agent's control flow
before introducing a stochastic policy.

## 4. Pseudocode

```text
function RUN(goal, tools, budget):
    state <- {goal: goal, history: []}
    for step in 1..budget.max_steps:
        action <- policy(state, tools)
        if action.type == "finish": return finish(action, "goal")
        observation <- execute(action, tools)     # validated, permissioned
        state.history.append((action, observation))
    return finish(None, "budget_exhausted")
```

## 5. Worked Example — a two-tool agent

Goal: "what is the status of order 4471?" Tools: `lookup_order(id)`, `check_stock(sku)`.

| Step | Action | Observation |
| ---: | :--- | :--- |
| 1 | `lookup_order("4471")` | `{status: "delayed", sku: "A-12"}` |
| 2 | `check_stock("A-12")` | `{available: 0, restock_days: 6}` |
| 3 | finish | answer: delayed, restock in 6 days |

Three steps, two tools, one termination reason. The agent never needed to "reason" beyond choosing
the next tool; the value came from the loop and the schemas.

## 6. Mathematical Formulation

An agent is a policy over histories with a budget:

$$\pi: (S \times A \times O)^* \to A, \qquad \text{stop} \iff t \ge T_{\max} \lor g(s_t) \lor u(s_t) < \tau$$

where $u$ is the remaining budget (steps, tokens or seconds). Boundedness is a property of the
controller, not of the model.

## 7. Python Implementation

```python
from dataclasses import dataclass, field


@dataclass
class Agent:
    tools: dict
    max_steps: int = 8
    history: list = field(default_factory=list)

    def run(self, goal, policy):
        for step in range(self.max_steps):
            action = policy(goal, self.history)
            if action["type"] == "finish":
                return {"answer": action["answer"], "steps": step,
                        "reason": "goal", "history": self.history}
            name = action["name"]
            if name not in self.tools:
                self.history.append((action, {"error": "unknown tool"}))
                continue
            result = self.tools[name](**action["args"])
            self.history.append((action, result))
        return {"answer": None, "steps": self.max_steps,
                "reason": "budget_exhausted", "history": self.history}
```

The important line is the `max_steps` loop bound: it turns an open-ended process into a system with
a predictable worst case.

## 8. Practical Applications

- **Support triage** — look up order, check policy, draft reply, escalate if uncertain.
- **Data collection** — search, fetch, validate, store, with a step budget per record.
- **Build and deploy assistants** — read logs, propose a fix, request approval, apply.
- **Research helpers** — plan queries, retrieve, synthesise, cite.

## 9. Common Mistakes

- No step budget, so a failing agent spends the monthly API allowance overnight.
- Tools with free-text arguments instead of schemas, so the model invents parameter names.
- Storing the whole transcript as state until the context window overflows.
- Treating "the model said it is done" as a goal test.
- Giving the agent write access before read access has been tested.

## 10. Exercises

1. Add a token budget alongside the step budget and terminate on whichever is exhausted first.
2. Log a termination reason for every path and write a test that forces each one.
3. Replace the policy with a scripted one that deliberately calls an unknown tool; verify the agent recovers.
4. Draw the four-component architecture for a system you use at work.

## 11. Self-Assessment

1. Which three properties make a system agentic?
2. Why must the controller, not the model, enforce the budget?
3. What is the failure mode of an unbounded state?
4. Why does the module use a deterministic stand-in model?

## 12. Key Terms

**Agent loop**, **policy**, **tool**, **state**, **controller**, **termination reason**, **step budget**.

## 13. Further Reading

- Russell & Norvig, chapter 2 (agent architectures).
- Yao et al. (2022), ReAct — reasoning and acting in one loop.

## What to Do Next

[L12-02](L12-02-llm-agents-tool-calling-and-structured-outputs.md) makes the policy a language model
and the tools structured functions.
