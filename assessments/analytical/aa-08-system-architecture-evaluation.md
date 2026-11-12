# AA-08 — Evaluating an AI System Architecture

| | |
| :--- | :--- |
| Assignment | 08 |
| Difficulty | Advanced |
| Estimated time | 3 hours |
| Prerequisites | M11–M14, PA-12 or PA-13 |
| Format | Architecture review |
| Covers | components, failure modes, cost, latency, security, operability |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

Architecture diagrams show boxes and arrows; production failures happen at the seams — between
retrieval and generation, between the agent and its tools, between the model and its data. A useful
review asks what happens when each component is slow, wrong, or unavailable.

## Problem scenario

Review this proposed system: a document assistant with a vector index, a hosted LLM, an agent loop with
`search`, `read`, `email`, a Postgres record of conversations, and a nightly re-index. Users are
internal staff; documents include HR records. Traffic is 200 requests/hour, peak 40/minute.

## Learning outcomes

1. Map a system into components with explicit contracts.
2. Analyse failure modes and their propagation.
3. Estimate cost and latency budgets per request.
4. Identify security and privacy risks specific to the design.
5. Recommend a revised architecture with trade-offs stated.

## Tasks

1. **Component table.** Each component: responsibility, input, output, failure behaviour.
2. **Failure analysis.** Three failure modes with propagation and user-visible effect.
3. **Budget.** Allocate a 6-second p95 latency budget and a per-request cost budget; show the
   arithmetic and the assumption behind each number.
4. **Security.** Identify two risks (one injection, one access-control) and a control for each.
5. **Operability.** What must be logged and alerted to detect degradation within a day?
6. **Revision.** One architectural change with its benefit, cost and new risk.

## Constraints

- At most 1,000 words plus two tables.
- Every estimate labelled as an estimate with its basis.
- Do not assume the LLM is trustworthy; do not assume it is useless.

## Expected deliverables

The review document with the component and budget tables.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Component contracts | 20% | responsibilities and failure behaviour |
| Failure analysis | 25% | propagation traced, not listed |
| Budgets | 20% | arithmetic coherent, assumptions stated |
| Security | 20% | two concrete risks with controls |
| Revision | 15% | trade-off explicit, new risk named |

## Bonus challenges

- Add a fallback path when the LLM is unavailable and estimate its quality cost.
- Estimate the cost of the nightly re-index at 10× the document volume.

---

[Assessment index](../README.md) · [AA-07](aa-07-research-paper-analysis.md) · [Self-assessment](../self-assessment/README.md)
