# A-10 — Multi-Agent Research Assistant

**Level** Advanced · **Time** 14 h capstone · **Prerequisites** M12, M11, M13

## Problem statement

Build a small multi-agent system that plans a research question, retrieves sources, drafts an
answer and critiques it — and evaluate it on tasks rather than on impressions.

## Motivation

Agent systems are easy to demo and hard to evaluate. The contribution of this project is the
evaluation: task success, step counts, tool errors, cost and failure modes, on a fixed task set
that you publish alongside the code.

## Scope

**In:** 3–4 agents (planner, retriever, writer, critic), a fixed corpus, 15–20 tasks, offline
evaluation.
**Out:** open-web browsing at scale, deployment, any claim of research quality comparable to a
human.

## Objectives

1. Implement a bounded agent loop with per-agent tool permissions.
2. Build a 15-task evaluation set with reference answers and rubrics.
3. Measure task success, steps, tool errors and latency.
4. Compare single-agent against multi-agent on the same tasks.

## Required knowledge

M12 agent patterns, M11 retrieval, L14-04 evaluation discipline. You will need to learn tracing;
the fallback is structured logging.

## Suggested architecture

```text
question -> planner (decompose) -> retriever (documents) -> writer (draft)
         -> critic (checks claims against sources) -> final answer + citations
         -> evaluate: task success (rubric), steps, tool errors, refusals, latency
```

## Dataset recommendations

- The M11 Northfield corpus (CC0-1.0) or another permissively licensed document set.
- 15 questions answerable from the corpus plus 5 that are not.
- If you use a hosted model, keep keys in environment variables and never commit them.

## Suggested technologies

Python; the M12 `agent_core.py` pattern (bounded loop, tool registry, logging). A deterministic
simulated model is acceptable for the harness if clearly labelled — but then your evaluation is of
the orchestration, not of a language model, and must say so.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | single-agent baseline with logging |
| M3 | multi-agent system, task-set results |
| M4 | failure taxonomy, cost analysis, report |

## Evaluation metrics

Primary: task success rate by rubric on 20 tasks. Supporting: mean steps, tool-error rate,
citation correctness, latency, and refusal behaviour on unanswerable tasks. Baselines:
single-agent, and a no-retrieval variant.

## Expected deliverables

Agent code, task set with rubrics, traces, report.

## Challenges

1. **Evaluation subjectivity.** Write the rubric before running the system, and score blind to
   which system produced the answer where possible.
2. **Runaway loops.** Bound steps and record terminations. Report how often the bound was hit.
3. **Agent collusion.** A critic that trusts the writer adds nothing; make it check sources.

## Possible extensions

- Add a tool-abuse evaluation (M13's harness) and report unsafe-action attempts.
- Compare two orchestration topologies on the same task set.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
