# A-12 — Secure AI Agent with Runtime Monitoring

**Level** Advanced · **Time** 14 h capstone · **Prerequisites** M13 (L13-04), M12, L14-03

## Problem statement

Build a tool-using agent with runtime guardrails, then attack it with a fixed adversarial suite
and report both the guardrail effectiveness and the drift/abuse monitoring around it.

## Motivation

Agent security is not a prompt problem: it is a capability problem (M13 measured injection success
falling from 0.83 to 0.17 with an allowlist, while a content-only attack still succeeded). This
project builds the controls and the monitoring, and evaluates both against a published suite.

## Scope

**In:** a local agent with 3–4 tools, a 20-case adversarial suite, in-process evaluation.
**Out:** attacking real services, deployment, any offensive tooling.

## Objectives

1. Implement default-deny tool permissions with an approval gate.
2. Build a 20-case suite: direct injection, indirect injection, tool abuse, data exfiltration.
3. Measure unsafe-action rate with and without guardrails.
4. Add monitoring: action logs, anomaly rules, and a drift check on request distribution.

## Required knowledge

M13 L13-04, M12 agent loop. You will need to learn logging/tracing design; the fallback is
structured JSON logs.

## Suggested architecture

```text
request -> sanitiser -> planner -> tool call (allowlist + approval gate)
        -> audit log -> monitor (rules + distribution check) -> response
        -> evaluate: unsafe action rate, false denial rate, detection latency
```

## Dataset recommendations

Synthetic documents and a toy tool registry (send, read, delete) — see M13's `llm_security.py` for
a model of the harness. No real credentials, recipients or data.

## Suggested technologies

Python; a deterministic simulator is acceptable and must be labelled. If you use a hosted model,
keep the key in an environment variable.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | agent with default-deny, 20-case suite |
| M3 | guardrail results, monitoring rules |
| M4 | residual-risk analysis, report |

## Evaluation metrics

Primary: unsafe action rate on the adversarial suite. Supporting: false denial rate on a benign
suite, detection latency, log completeness. Baseline: no guardrails.

## Expected deliverables

Agent, suite, logs, monitoring rules, report with residual risk.

## Challenges

1. **False denials.** Guardrails that block everything score well on unsafe actions and badly on
   usability. Measure both suites.
2. **Detection ≠ boundary.** A detector is a signal; say what the boundary actually is.
3. **Simulator honesty.** If you use one, state that the results are about orchestration.

## Possible extensions

- Add a rate limiter and measure the effect on extraction-style abuse.
- Compare a classifier-based action gate against the allowlist.

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
