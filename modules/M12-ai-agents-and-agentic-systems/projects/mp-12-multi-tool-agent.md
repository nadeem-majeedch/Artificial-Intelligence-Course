# MP-12 — Multi-Tool Agent for a Realistic Task

| | |
| :--- | :--- |
| Module | M12 · AI Agents and Agentic AI Systems |
| Effort | 8–10 hours |
| Level | 400 |
| Type | Integrated project |

[Module home](../README.md) · [LAB-12-01](../labs/lab-12-01-tool-using-agent.md) · [LAB-12-02](../labs/lab-12-02-agent-security-and-evaluation.md)

## Scenario

A small logistics company receives supplier invoices as PDFs, checks them against purchase orders in
a spreadsheet, and pays the ones that match. Two people do this manually for about three hours a
day. They want an agent that does the reading, checking and drafting, and a human who approves
payment.

Your agent must use **at least four tools**, handle failures without losing the task, and produce an
audit trail a finance auditor would accept.

## Your role

You are the engineer delivering a working prototype, its evaluation, and a short handover document.
There is no paid API: the model is replaced by a deterministic policy or a local model, and the
grading is on the system, not on the language model's eloquence.

## Requirements

- **R1** Four tools minimum: extract invoice fields, look up purchase order, compare, draft payment.
- **R2** A bounded loop with a logged termination reason for every run.
- **R3** Schema validation on every tool call, and a refusal path that does not retry permission errors.
- **R4** Human approval bound to the exact payment (amount, supplier, reference).
- **R5** Persistence: a run can be resumed after an interruption without redoing completed steps.
- **R6** Evaluation on at least 20 invoices, reporting task success, steps, tool errors and cost.

## Suggested build order

1. **Corpus** — generate 20 synthetic invoices with deliberate defects: wrong amount, unknown PO,
   duplicate, unreadable field. Store expected outcomes alongside.
2. **Tools** — four functions with schemas and validators; unit-test each rejection path.
3. **Loop** — bounded steps, per-step trace, resumable state file.
4. **Approval** — a preview plus an approval token bound to the arguments.
5. **Evaluation** — run the set, report four metrics with intervals, and a failure taxonomy.
6. **Handover** — a one-page document for the finance team.

## Deliverables

| File | Contents |
| :--- | :--- |
| `agent.py` | Loop, tools, guardrails, persistence |
| `tools.py` | Schemas and implementations |
| `evaluate.py` | Runs the corpus and writes metrics |
| `RESULTS.md` | Metrics, failure taxonomy, limitations |
| `HANDOVER.md` | ≤ 600 words for the finance team |

## Marking scheme

| Criterion | Weight | What a strong submission shows |
| :--- | ---: | :--- |
| Architecture | 25% | loop, tools, state and approval clearly separated |
| Safety | 20% | irreversible action impossible without bound approval; injection tested |
| Reliability | 20% | resumption works; errors classified; no runaway runs |
| Evaluation | 20% | four metrics, intervals, honest failure taxonomy |
| Handover | 15% | a non-engineer can operate and escalate it |

## Extensions

1. Add a second agent that independently verifies the match, and measure whether end-to-end success improves.
2. Add an MCP server exposing the purchase-order lookup, and document the trust boundary.
3. Replace the deterministic policy with a local model and compare success, steps and cost.

## What "done" looks like

A run of 20 invoices finishes in under two minutes on CPU, every payment requires an approval that
names the amount, the trace explains any failure, and `RESULTS.md` states what the system cannot do.
