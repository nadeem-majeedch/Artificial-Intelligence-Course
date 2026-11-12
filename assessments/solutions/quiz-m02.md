# QUIZ-M02 — Solutions and Explanations

> **Availability.** M02 (Intelligent Agents) — 1 of 5 lessons published in this repository, so this paper cannot be attempted
> yet. It is included so the assessment set is complete, and it is a preview
> rather than an assessment until the module's lessons are published.

[Quiz](quiz-m02.md) · [Assessment index](../README.md)

---

## Part A

**Q2.1 — C.** Rationality is a property of the agent given its percepts and prior knowledge; the
environment's properties constrain what is achievable but do not determine whether the agent is
rational. Observability (A), determinism (B) and dynamism (D) are all environment properties the
percept design reveals.

**Q2.2 — B.** A model-based reflex agent keeps internal state to track the part of the world it
cannot currently see. A simple reflex agent maps the current percept to an action with no memory;
a table-driven agent is a special case of that. A stateless classifier has no state by definition.

**Q2.3 — A.** Profit with risk limits is the performance measure — the thing we judge the agent by.
The market is the environment; orders are actuators; prices and news are sensors. A common error
is to place "profit" under environment because it is external; the PEAS performance measure is
specifically the external criterion.

## Part B

**Q2.4 — False.** Rationality is judged on *expected* performance given the information available
at decision time, not on the outcome after the fact. An agent that buys a lottery ticket with
positive expected value is rational even when the ticket loses; an agent that gambles the
institution's reserves on a hunch is not, even if it happens to win.

## Part C

**Q2.5 — Model answer.** A reflex agent conditions only on the current percept. In a partially
observable environment the same percept is consistent with several world states, so any fixed
percept→action rule must be wrong in some of them. Rationality requires distinguishing those
states, which needs memory (state) or information gathering.

**Q2.6 — Model answer.** Static: a puzzle or a route-planning problem where the world does not
change while the agent deliberates. Dynamic: driving, trading, or any task where the world changes
during computation. Design consequence: in a dynamic environment the agent needs anytime
behaviour — a usable answer within a deadline — and must re-perceive rather than plan once and
execute a long sequence blindly.

## Part D

**Q2.7 —** Percepts: $2^3 = 8$. Sequences of length 3: $8^3 = 512$. Table entries: 8 (one action
per percept). Marks: 1 each.

## Part E

**Q2.8 —** Branching factor 4. Nodes at depth 2: $4^2 = 16$ generated; with duplicates included,
$4 + 16 = 20$ nodes generated in total (root plus depth 1 plus depth 2). If the question is read
as "children at depth 2 only", 16 is correct; both readings are accepted with the working shown.

## Part F

**Q2.9 —** Actions: `Suck` (A dirty) → `Move right` (A clean) → `Suck` (B dirty).

Tracing rule: the agent uses the *current* percept only; after sucking at A, the next percept is
(A, clean), which triggers "move right". No state is carried, which is exactly why the third input
at B is handled without any memory of having visited A.

## Part G

**Q2.10 —** `['suck', 'no-op', 'right']`

`dict.get(key, default)` returns the default for the missing key `("dirty", "B")` rather than
raising `KeyError`. Students who answer with an exception have confused `d[...]` with `.get(...)`.

## Part H

**Q2.11 — Model answer (2 marks, 1 per property).** Partly observable → internal state or
information-gathering actions. Stochastic → reason over outcomes and expected utility rather than
a single predicted next state. Dynamic → deadline-aware deliberation and re-planning.

**Q2.12 — Model answer.** PEAS forces you to name the performance measure and the sensors before
writing code, which exposes mismatches early. One failure it prevents: optimising a proxy that is
easy to measure (clicks) rather than the actual objective (retention), discovered only after
deployment. Another: designing actuators the environment cannot accept.

---

[Quiz](quiz-m02.md) · [Previous solutions](quiz-m01.md) · [Assessment index](../README.md)
