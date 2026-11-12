# PA-13 — A Tool-Using Agent with a Bounded Loop

| | |
| :--- | :--- |
| Assignment | 13 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M12, M13 (L13-04), PA-12 |
| Covers | tool schemas, planning, memory, guardrails, agent evaluation |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

An agent is a loop around a model with tools attached. Most of the engineering is in the loop: what
the tools accept, what happens when one fails, when to stop, and what is logged. This assignment
builds that loop and evaluates it on tasks rather than on impressions.

## Problem scenario

Build an agent that answers questions over a document collection using three tools: `search`,
`read_document` and `summarise`. It may take at most 6 steps. A small adversarial set tests whether
the agent can be induced to call a non-existent tool or exceed its permissions.

## Learning outcomes

1. Define tool schemas and validate arguments before execution.
2. Bound the loop by steps and cost, with a logged termination reason.
3. Add default-deny permissions and an approval gate for destructive actions.
4. Evaluate task success, steps and tool errors on a fixed task set.

## Tasks

1. **Tools.** Implement the three tools with JSON schemas and argument validation.
2. **Loop.** Planner → tool call → observation → repeat, capped at 6 steps.
3. **Robustness.** Handle a tool that raises, a tool that returns nothing, and an unknown tool name.
4. **Guardrails.** Deny unknown tools; require approval for anything destructive; log every attempt.
5. **Evaluation.** 15 tasks (10 answerable, 5 not); report success, mean steps, tool-error rate.
6. **Adversarial set.** 6 cases attempting tool abuse; report unsafe-attempt rate with and without the
   gate.

## Constraints

- No live external services; a deterministic simulator is acceptable if labelled.
- Every run produces a structured log.
- No credentials in code.

## Expected deliverables

`agent.py`, `tools.py`, `tasks.jsonl`, `logs/` (sample), `results.md`.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Tool design | 20% | schemas validated, errors handled |
| Loop control | 20% | bound enforced, termination logged |
| Guardrails | 25% | default deny, approval, audit log |
| Evaluation | 25% | fixed task set, steps and errors reported |
| Honesty | 10% | simulator labelled; limits stated |

## Bonus challenges

- Add a cost budget and report the trade with task success.
- Compare a single-agent loop with a planner/executor split on the same tasks.

---

[Assessment index](../README.md) · [PA-12](pa-12-llm-applications.md) · [PA-14](pa-14-explainable-and-secure-ai.md)
