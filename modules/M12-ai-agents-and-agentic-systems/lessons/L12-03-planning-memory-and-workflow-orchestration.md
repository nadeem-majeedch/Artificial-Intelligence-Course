# L12-03 — Planning, Memory and Workflow Orchestration

| Module | M12 · AI Agents and Agentic AI Systems |
| :--- | :--- |
| Level | 400 |
| Study time | 80 minutes |
| Prerequisites | [L12-02](L12-02-llm-agents-tool-calling-and-structured-outputs.md) · [L03-01](../../M03-problem-solving-and-search-algorithms/lessons/L03-01-problem-formulation-and-state-spaces.md) |
| Code | `code/agent_core.py`, `code/protocols.py` |

[← Previous: L12-02](L12-02-llm-agents-tool-calling-and-structured-outputs.md) · [Next: L12-04 Frameworks →](L12-04-agent-frameworks-and-practical-implementation.md)

## 1. Learning Objectives

- **Decompose** a goal into verifiable steps, and revise the plan when a step fails.
- **Choose** between a fixed workflow and a dynamic plan, with a stated criterion.
- **Design** memory as two tiers: bounded context and external store.
- **Diagnose** the three classic orchestration failures: replanning loops, stale memory, lost state.

## 2. Prerequisite Knowledge

The loop and tool boundary from L12-01/L12-02, and state-space thinking from
[L03-01](../../M03-problem-solving-and-search-algorithms/lessons/L03-01-problem-formulation-and-state-spaces.md).

## 3. Conceptual Explanation

### 3.1 Workflow or agent?

A **workflow** has steps fixed by the developer; the model fills in content. An **agent** chooses
the steps at runtime. Workflows are cheaper, testable and easier to audit; agents handle tasks whose
step count is unknown in advance. The engineering rule: use the least dynamic structure that solves
the problem.

### 3.2 Planning that survives failure

A plan is a list of steps, each with a checkable postcondition. When a step fails, the agent must be
able to (a) retry once, (b) replan the remaining steps, or (c) stop and report. Agents that cannot
distinguish these three enter replanning loops: they retry a step that can never succeed.

### 3.3 Memory in two tiers

- **Context memory:** the conversation and recent observations. Bounded by the context window, so it
  must be summarised or pruned, not simply appended.
- **External memory:** a store queried on demand (files, database, vector index). Authoritative,
  but only as good as the retrieval query.

The failure mode is treating context as a database: it grows, costs tokens, and eventually
contradicts itself because old and new observations coexist without precedence.

### 3.4 State, not transcript

Persist the *task state* — goal, completed steps, open questions, artifacts — rather than the raw
transcript. A resume from state is reliable; a resume from a truncated transcript is guesswork.

## 4. Pseudocode

```text
function STEP(plan, state):
    step <- next_unfinished(plan)
    if step is None: return finish(state)
    result <- attempt(step)                  # bounded retries inside
    if result.ok:
        state.completed.add(step.id)
    else if result.retryable and step.attempts < 2:
        step.attempts += 1
    else:
        plan <- replan(plan, state, result)  # may drop or replace steps
        if plan is None: return finish(state, reason="blocked")
```

## 5. Worked Example — invoice reconciliation

Goal: reconcile 40 invoices against payments.

| Step | Postcondition | Failure handling |
| ---: | :--- | :--- |
| 1 | invoices loaded | retry once on timeout |
| 2 | payments loaded | retry once, then stop: no data means no task |
| 3 | matches computed | deterministic, no retry needed |
| 4 | 7 unmatched flagged | if > 10 unmatched, stop and ask a human |

Step 4's threshold is the interesting design decision: an agent that "fixes" unmatched invoices
automatically is an agent that can approve payments it does not understand.

## 6. Mathematical Formulation

Expected cost of a plan with step costs $c_i$ and retry probability $p$:

$$\mathbb{E}[C] = \sum_i c_i \left(1 + p_i + p_i^2\right) \quad \text{(two retries)}$$

Replanning adds a full extra pass; the budget must therefore be allocated per step, not per run.

## 7. Python Implementation

```python
from dataclasses import dataclass, field


@dataclass
class Step:
    id: str
    action: str
    done: bool = False
    attempts: int = 0


@dataclass
class Plan:
    steps: list
    max_attempts: int = 2

    def next_open(self):
        return next((s for s in self.steps if not s.done), None)

    def record(self, step, ok, retryable=True):
        if ok:
            step.done = True
            return "advanced"
        step.attempts += 1
        if retryable and step.attempts < self.max_attempts:
            return "retry"
        return "replan"


plan = Plan([Step("load", "load_invoices"), Step("match", "compute_matches")])
step = plan.next_open()
print(plan.record(step, ok=False))   # retry
print(plan.record(step, ok=False))   # replan
```

## 8. Practical Applications

- **Document processing** — extract, validate, route, with a human threshold on low confidence.
- **Incident response** — gather signals, propose remediation, require approval to act.
- **E-commerce operations** — check stock, price, fraud, then fulfil; each step has a postcondition.
- **Research assistants** — plan queries, retrieve, synthesise, cite; replan on empty results.

## 9. Common Mistakes

- Appending every observation to context until the window overflows mid-task.
- Retrying a step whose failure is permanent (missing permission, absent record).
- Persisting the transcript instead of the task state, so resumption loses the goal.
- Letting the agent modify its own plan without a log, which makes failures untraceable.
- Using an agent where a five-step workflow would be cheaper and testable.

## 10. Exercises

1. Add a postcondition check to each step in the invoice example and a test that fails it.
2. Implement summarisation of context memory at a token threshold; measure tokens before and after.
3. Persist the plan to JSON and resume a run from it.
4. Compare a fixed workflow and an agent on the same task: steps, cost, failure modes.

## 11. Self-Assessment

1. What distinguishes a workflow from an agent?
2. Name the three responses to a failed step and when each is correct.
3. Why is the transcript the wrong thing to persist?
4. What is the danger of automatic repair of unmatched records?

## 12. Key Terms

**Plan**, **postcondition**, **replanning**, **context memory**, **external memory**, **task state**, **resume**.

## 13. Further Reading

- Wei et al. (2022), chain-of-thought; Yao et al. (2023), Tree of Thoughts.
- Anthropic (2024), "Building effective agents" — workflow-versus-agent trade-offs.

## What to Do Next

[L12-04](L12-04-agent-frameworks-and-practical-implementation.md) puts these pieces into a runnable
system and compares frameworks with a plain loop.
