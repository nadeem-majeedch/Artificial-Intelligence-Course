# L12-05 — Multi-Agent Systems and Collaboration

| Module | M12 · AI Agents and Agentic AI Systems |
| :--- | :--- |
| Level | 400 |
| Study time | 75 minutes |
| Prerequisites | [L12-04](L12-04-agent-frameworks-and-practical-implementation.md) |
| Code | `code/multi_agent.py`, `code/protocols.py` |

[← Previous: L12-04](L12-04-agent-frameworks-and-practical-implementation.md) · [Next: L12-06 Security and Evaluation →](L12-06-mcp-security-evaluation-and-reliable-execution.md)

## 1. Learning Objectives

- **Identify** the three coordination patterns: supervisor, pipeline and peer negotiation.
- **Justify** multi-agent decomposition with a cost argument, not an intuition.
- **Implement** a supervisor that validates hand-offs against a schema.
- **Diagnose** the four multi-agent failure modes: duplication, contradiction, deadlock, cost blow-up.

## 2. Prerequisite Knowledge

Single-agent loop, tools and tracing from L12-01…L12-04.

## 3. Conceptual Explanation

### 3.1 Why split into agents

Three defensible reasons: **context isolation** (each agent sees only what it needs),
**specialisation** (different tools and prompts), and **independent verification** (a checker that
did not produce the work). "More agents are smarter" is not one of them — specialisation without a
measured gain is cost.

### 3.2 Coordination patterns

| Pattern | Structure | Good for | Failure |
| :--- | :--- | :--- | :--- |
| Supervisor | one planner delegates to workers | decomposable tasks | supervisor becomes the bottleneck |
| Pipeline | fixed sequence, each stage refines | document processing | error propagation |
| Peer negotiation | agents critique each other | review, verification | loops, no termination |

### 3.3 Hand-offs are the new interface

Every hand-off needs a schema and a postcondition: what the worker receives, what it must return,
and how the supervisor validates it. Free-text hand-offs are where duplication and contradiction
enter — two workers solve the same subtask because neither could tell it was already done.

### 3.4 Cost is multiplicative

If each agent has a 90% success rate and a task requires five sequential agents, end-to-end success
is $0.9^5 \approx 0.59$. Multi-agent systems must therefore include per-agent budgets and a
supervisor that can abandon a branch.

## 4. Pseudocode

```text
function SUPERVISE(goal, workers, budget):
    subtasks <- decompose(goal)
    results <- {}
    for task in subtasks:
        worker <- choose_worker(task)
        out <- worker.run(task, budget.share())
        if not validates(out, task.schema): return blocked(task, "schema")
        results[task.id] <- out
    return combine(results)
```

## 5. Worked Example — research assistant

Goal: a 300-word brief on a policy question.

| Role | Tools | Output schema |
| :--- | :--- | :--- |
| Planner | none | list of 4 questions |
| Retriever | search, fetch | passages with URLs |
| Writer | none | draft with citations |
| Checker | none | claims vs sources, verdict per claim |

Sequential success at 0.92 per stage: $0.92^4 = 0.72$. Adding a bounded retry on the checker
raises end-to-end success to 0.86 in the module's task set — measured, not assumed.

## 6. Mathematical Formulation

End-to-end success for $n$ independent stages with per-stage success $s$:

$$S = s^n \quad\Rightarrow\quad n = \frac{\log S}{\log s}$$

To keep $S \ge 0.9$ at $s = 0.95$, you can afford three stages. This arithmetic is the argument
against gratuitous decomposition.

## 7. Python Implementation

```python
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    run: object
    schema_keys: tuple


class Supervisor:
    def __init__(self, workers, budget=6):
        self.workers = {w.name: w for w in workers}
        self.budget = budget
        self.log = []

    def run(self, tasks):
        results = {}
        for task in tasks:
            worker = self.workers[task["worker"]]
            out = worker.run(task["input"])
            missing = [k for k in worker.schema_keys if k not in out]
            self.log.append((worker.name, task["id"], "ok" if not missing else missing))
            if missing:
                return {"status": "blocked", "at": task["id"], "missing": missing}
            results[task["id"]] = out
            self.budget -= 1
            if self.budget <= 0:
                return {"status": "budget", "results": results}
        return {"status": "ok", "results": results}
```

## 8. Practical Applications

- **Document review** — extractor, validator, summariser, with a checker that sees only sources.
- **Software maintenance** — planner, patcher, test-runner; the test-runner is the independent verifier.
- **Customer operations** — triage, resolver, escalation, with shared state and one owner per ticket.
- **Analysis pipelines** — collector, analyst, critic, each with a bounded scope.

## 9. Common Mistakes

- Adding agents to look sophisticated, then paying 3× cost for the same accuracy.
- Free-text hand-offs, so the supervisor cannot detect an incomplete result.
- No shared state, so two workers duplicate the same subtask.
- Peer critique without a termination rule, producing infinite politeness.
- Ignoring the multiplicative success arithmetic.

## 10. Exercises

1. Implement the supervisor above with three workers and one schema violation; verify it blocks at the right task.
2. Measure end-to-end success for 2, 3 and 4 stages at 0.9 per stage and compare with the formula.
3. Add a checker worker and measure whether it improves the final answer on ten tasks.
4. Design a shared-state schema that prevents duplicate work.

## 11. Self-Assessment

1. Give one good and one bad reason to split a task across agents.
2. What must every hand-off include?
3. Why does success decay multiplicatively?
4. What is the supervisor's job when a worker returns an invalid result?

## 12. Key Terms

**Supervisor**, **worker**, **hand-off**, **pipeline**, **peer review**, **shared state**, **end-to-end success**.

## 13. Further Reading

- Wu et al. (2023), AutoGen — multi-agent conversation patterns.
- Hong et al. (2023), MetaGPT — role-based decomposition with schemas.

## What to Do Next

[L12-06](L12-06-mcp-security-evaluation-and-reliable-execution.md) closes the module with the
security and evaluation discipline that multi-agent systems make urgent.
