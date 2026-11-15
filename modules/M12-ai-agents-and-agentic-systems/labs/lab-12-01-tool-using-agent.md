# LAB-12-01 — A Tool-Using Support Agent

| | |
| :--- | :--- |
| Module | M12 · AI Agents and Agentic AI Systems |
| Time | 2.5 hours |
| Level | 400 |
| Pairs with | L12-01, L12-02, L12-04 |

[Module home](../README.md) · [Lab 12-02](lab-12-02-agent-security-and-evaluation.md) · [Project](../projects/mp-12-multi-tool-agent.md)

## Scenario

An online retailer's support queue handles 900 tickets a day. Sixty per cent are three questions:
where is my order, can I change the address, can I get a refund. The support lead wants an agent that
**answers the first two and drafts the third for a human**, with a hard rule: it may never issue a
refund itself.

You are the engineer. The lead cares about two numbers: how many tickets are resolved without a
human, and how often the agent says something false.

## Your role

You report to the support lead and to the finance controller, who has one requirement: no money
moves without a human. You will be judged on whether the agent's failure modes are known.

## What you are given

| Item | Details |
| :--- | :--- |
| Reference code | `code/agent_core.py` (loop, termination), `code/tools.py` (schemas), `code/guardrails.py` (permissions) |
| Task set | `code/agent_data.py` — 40 tickets with expected outcomes |
| Tools available | `lookup_order`, `check_stock`, `update_address`, `draft_refund` |
| Forbidden | any tool that issues a payment |

## Starter material

The guided notebook [`nb-12-01-agentic-ai-workbench.ipynb`](../notebooks/nb-12-01-agentic-ai-workbench.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).

## Requirements

- **R1** Implement the loop with a step budget and a logged termination reason for every run.
- **R2** Define each tool with a schema; reject malformed arguments before execution.
- **R3** Enforce the permission boundary: refunds are drafted, never issued.
- **R4** Run the 40-ticket task set and report success, steps, tool-error rate and cost.
- **R5** List every failure in the task set by category, not just a count.

## Tasks

1. **Tools** (30 min). Write the four schemas and validators; unit-test each rejection path.
2. **Loop** (30 min). Wrap the deterministic policy from `agent_data.py` and log steps.
3. **Permissions** (20 min). Attempt to call a forbidden payment tool and verify refusal plus no retry.
4. **Evaluate** (40 min). Run all 40 tickets; produce the four metrics with a confidence interval.
5. **Failure analysis** (30 min). Categorise failures: wrong tool, missing argument, bad answer, loop.
6. **Recommendation** (20 min). State a rollout condition and one monitoring metric.

## Expected results

- 30–34 of 40 tickets resolved correctly by the deterministic policy.
- At least one ticket fails with a missing argument and one with a tool error.
- The forbidden call is refused and does not appear twice in the trace.
- Step counts between 1 and 4 for resolved tickets; no run hits the budget on the sample.

## Deliverables

| File | Contents |
| :--- | :--- |
| `support_agent.py` | Tools, schemas, loop, permission checks |
| `evaluation.md` | Four metrics, confidence interval, failure taxonomy |
| `rollout.md` | ≤ 300 words: conditions, monitoring, escalation |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Safety | 30% | forbidden action impossible by construction | blocked at runtime | reachable |
| Correctness | 25% | 30+ correct; failures explained | 20+ | under 20 or unexplained |
| Measurement | 20% | four metrics, interval, reproducible seeds | metrics only | single accuracy number |
| Engineering | 15% | clean schemas, trace, tests | runs | fragile |
| Communication | 10% | rollout conditions a manager can apply | vague | absent |

## Extension challenges

1. Add a fifth tool that reads a policy document, and show that its output is treated as data.
2. Add a bounded repair attempt for malformed calls and measure the recovery rate.
3. Simulate an injected instruction inside an order note and prove it cannot trigger a refund.

## Reflection

1. Which requirement would you keep if you had to drop everything else, and why?
2. The agent resolves 34 of 40 tickets. What does the other 6 cost the business?
3. Where would you put the human approval, and what exactly would they approve?

---

[Module home](../README.md) · [Lab 12-02](lab-12-02-agent-security-and-evaluation.md) · [Project](../projects/mp-12-multi-tool-agent.md)
