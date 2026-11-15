# LAB-12-02 — Agent Security and Evaluation

| | |
| :--- | :--- |
| Module | M12 · AI Agents and Agentic AI Systems |
| Time | 2 hours |
| Level | 400 |
| Pairs with | L12-05, L12-06 |

[Module home](../README.md) · [Lab 12-01](lab-12-01-tool-using-agent.md) · [Project](../projects/mp-12-multi-tool-agent.md)

## Scenario

Before the support agent from LAB-12-01 goes live, the security team runs a red-team exercise. Your
job is to attack your own agent and report what you found — including the attacks that failed,
because "we could not break it" is only evidence if you say what you tried.

The second half is evaluation: the support lead wants a number they can defend to the board, and a
board does not accept "it works well".

## Your role

You are both the attacker and the evaluator. Two artefacts, one honest report.

## What you are given

| Item | Details |
| :--- | :--- |
| Target | your LAB-12-01 agent |
| Attack surface | ticket text, order notes, tool outputs, retrieved policy snippets |
| Evaluation set | 40 tickets from `code/agent_data.py` |
| Reference | `code/guardrails.py`, [L13-04](../../M13-responsible-explainable-secure-ai/lessons/L13-04-security-adversarial-examples-and-prompt-injection.md) |

## Starter material

The guided notebook [`nb-12-01-agentic-ai-workbench.ipynb`](../notebooks/nb-12-01-agentic-ai-workbench.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).

## Requirements

- **R1** Write eight attacks across three classes: direct injection, indirect injection, tool-output manipulation.
- **R2** Run each attack three times; report success rate, not a single run.
- **R3** For every successful attack, state which layer failed.
- **R4** Evaluate the agent on the 40-task set with four metrics and confidence intervals.
- **R5** Propose one architectural fix per successful attack class.

## Tasks

1. **Threat model** (20 min). Assets, entry points, trust boundaries — one page.
2. **Attacks** (40 min). Eight attempts; record prompt, channel, outcome.
3. **Layered fixes** (25 min). Apply structured extraction, allowlists, approval binding; re-run the attacks.
4. **Evaluation** (25 min). Four metrics, intervals, and a per-category breakdown.
5. **Report** (20 min). Findings ranked by severity with evidence.

## Expected results

- Direct injection succeeds against a prompt-only defence in at least one of three runs.
- Structured extraction reduces indirect-injection success to zero on this task set — and you should
  say explicitly that this is not a general proof.
- Approval binding rejects an approval whose arguments were modified.
- Task success between 0.70 and 0.90 with a wide interval at $n = 40$.

## Deliverables

| File | Contents |
| :--- | :--- |
| `redteam.py` | Attack harness with seeds |
| `security_report.md` | Threat model, eight attacks, layer that failed, fixes |
| `evaluation.md` | Four metrics, intervals, per-category table |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Attack quality | 30% | eight credible attacks across three classes, repeated | fewer classes | one prompt |
| Analysis | 25% | names the failing layer; distinguishes mitigation from proof | partial | "blocked" with no mechanism |
| Evaluation | 25% | four metrics, intervals, categories | accuracy only | no measurement |
| Reporting | 20% | severity-ranked with evidence | descriptive | missing negative results |

## Extension challenges

1. Add an MCP-style tool server and attack the trust boundary between host and server.
2. Measure the cost of the security layers in latency and tool calls.
3. Build a regression suite from your attacks and run it on every change.

## Reflection

1. Which attack succeeded, and would a better prompt have stopped it? Why does that matter?
2. What does "0 of 3 attacks succeeded" actually establish?
3. Which metric would you show the board, and which would you show the engineers?

---

[Module home](../README.md) · [Lab 12-01](lab-12-01-tool-using-agent.md) · [Project](../projects/mp-12-multi-tool-agent.md)
