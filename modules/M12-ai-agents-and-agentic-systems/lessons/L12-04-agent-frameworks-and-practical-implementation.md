# L12-04 — Agent Frameworks and Practical Implementation

| Module | M12 · AI Agents and Agentic AI Systems |
| :--- | :--- |
| Level | 400 |
| Study time | 80 minutes |
| Prerequisites | [L12-03](L12-03-planning-memory-and-workflow-orchestration.md) |
| Code | `code/agent_core.py`, `code/tools.py`, `code/agent_data.py` |

[← Previous: L12-03](L12-03-planning-memory-and-workflow-orchestration.md) · [Next: L12-05 Multi-agent →](L12-05-multi-agent-systems-and-collaboration.md)

## 1. Learning Objectives

- **Build** a working agent with a plain loop, then map that loop onto a framework's abstractions.
- **Choose** between a framework and 200 lines of your own code using explicit criteria.
- **Add** logging, tracing and replay to an agent so failures are debuggable.
- **Identify** which framework features are load-bearing and which are decoration.

## 2. Prerequisite Knowledge

The loop, tool schema and planner from L12-01…L12-03.

## 3. Conceptual Explanation

### 3.1 What frameworks actually provide

| Feature | Why it matters | Can you write it yourself? |
| :--- | :--- | :--- |
| Tool schema + dispatch | the safety boundary | yes, ~60 lines |
| Retries with backoff | reliability | yes |
| Tracing of steps | debuggability | yes, but tedious |
| Persistence / resumption | long tasks | yes, with a state file |
| Multi-agent orchestration | specialisation | often premature |

Frameworks earn their place when you need tracing, persistence and a team's shared vocabulary. They
cost you an abstraction you must debug when behaviour surprises you. The module's recommendation:
build the plain loop first, then adopt a framework when you can name the feature you need.

### 3.2 The runnable stack in this module

`agent_core.py` provides the loop and termination reasons; `tools.py` the schemas and validation;
`guardrails.py` permissions and refusal paths; `protocols.py` message formats; `multi_agent.py`
supervisor delegation; `agent_data.py` a task set with expected outcomes. It runs offline with a
deterministic policy, so every experiment is reproducible.

### 3.3 Tracing is the feature you will miss

Record for every step: input state hash, chosen action, arguments, validation result, tool output
summary, latency, tokens, and termination reason. Without this, an agent that "sometimes fails" is
unfixable; with it, the failure is a specific step with a specific observation.

### 3.4 Error handling policy

Classify errors before choosing a response:

| Error class | Example | Response |
| :--- | :--- | :--- |
| Transient | timeout, 429 | retry with backoff, bounded |
| Invalid input | schema violation | return validation detail, one repair attempt |
| Permission | forbidden tool | stop; do not retry |
| Semantic | tool succeeded but result useless | replan |
| Fatal | corrupted state | stop and surface |

## 4. Pseudocode

```text
function RUN_TRACED(goal, tools, budget, trace):
    while steps < budget:
        action <- policy(goal, state)
        trace.record(state_digest(state), action)
        outcome <- try: execute(action) catch e: classify(e)
        trace.record(outcome)
        if outcome.terminal: return finish(outcome)
```

## 5. Worked Example — one task, three structures

Task: "find the cheapest in-stock supplier for part P-88 and draft an order".

- **Workflow:** lookup → filter stock → sort price → draft. Four fixed steps, no model.
- **Agent:** the model decides which suppliers to query and when to stop.
- **Framework agent:** the same loop with tracing and retries supplied.

Measured on the module task set: workflow 4 steps, agent 6–9 steps, framework agent 6–9 steps plus
persistence. The workflow is cheaper and sufficient; the agent is justified only if the supplier set
changes shape per request.

## 6. Mathematical Formulation

Cost per successful task with retry probability $p$ and retry cost $c_r$:

$$C = c_{\text{base}} + \frac{p}{1-p}\,c_r$$

At $p = 0.2$, retries add 25% to the base cost — the number to compare against a workflow's
deterministic cost.

## 7. Python Implementation

```python
import time


class Trace:
    def __init__(self):
        self.events = []

    def record(self, kind, **fields):
        self.events.append({"t": round(time.time(), 3), "kind": kind, **fields})

    def summary(self):
        from collections import Counter
        return Counter(e["kind"] for e in self.events)


trace = Trace()
trace.record("action", name="lookup_order", args={"order_id": "4471"})
trace.record("observation", ok=True, rows=1)
trace.record("terminate", reason="goal")
print(trace.summary())
```

```text
Counter({'action': 1, 'observation': 1, 'terminate': 1})
```

## 8. Practical Applications

- **Internal tooling** — a traced loop over your own APIs is usually enough.
- **Customer support** — framework persistence lets a conversation resume across sessions.
- **Data operations** — workflows with one agent step where judgement is needed.
- **Research prototypes** — frameworks for speed, with the plain loop kept as a reference.

## 9. Common Mistakes

- Adopting a framework before knowing which feature you need.
- Logging only the final answer, so failures cannot be replayed.
- Treating every exception as retryable.
- Hiding the loop behind three layers of abstraction, then debugging the abstraction.
- Benchmarking frameworks on one task and generalising.

## 10. Exercises

1. Implement `Trace` and run the module's task set; produce a failure taxonomy from the trace.
2. Add a replay mode that re-executes a trace against recorded tool outputs.
3. Compare the plain loop and a framework on the same task: lines of code, steps, latency.
4. Write the criterion you would use to justify adopting a framework to a reviewer.

## 11. Self-Assessment

1. Which framework feature is hardest to retrofit later?
2. Why is "retry on exception" a bug?
3. What belongs in a trace record?
4. When is a workflow the better engineering choice?

## 12. Key Terms

**Framework**, **trace**, **replay**, **retry policy**, **error classification**, **persistence**.

## 13. Further Reading

- Anthropic (2024), "Building effective agents".
- LangGraph and OpenAI Agents SDK documentation, read as design documents rather than tutorials.

## What to Do Next

[L12-05](L12-05-multi-agent-systems-and-collaboration.md) adds more than one agent — and more than
one way to fail.
