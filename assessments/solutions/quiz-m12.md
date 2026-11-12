# QUIZ-M12 — Solutions and Explanations

> **Availability.** M12 (AI Agents) — reference code only in this repository, so this paper cannot be attempted
> yet. It is included so the assessment set is complete, and it is a preview
> rather than an assessment until the module's lessons are published.

[Quiz](quiz-m12.md) · [Assessment index](../README.md)

---

## Part A

**Q12.1 — B.** A schema is a contract: it declares argument names, types and required fields, and
the runtime validates against it before executing. It also helps the model choose, but the security
value is validation.

**Q12.2 — B.** An agent that can call tools in a loop can loop forever, retry a failing tool
indefinitely, or spend without bound. The step and cost limits are the control.

**Q12.3 — B.** Multi-agent systems usually fail on coordination: ambiguous hand-offs, duplicated
work, and a downstream agent trusting an unverified upstream claim. Model size is rarely the cause.

**Q12.4 — B.** Task success on a fixed set, with steps, tool errors and cost, is the measurement
that reflects the system. Perplexity is a language-model metric and says nothing about task
completion.

## Part B

**Q12.5 — False.** More autonomy and more tools expand what can go wrong: an agent with `send_email`
and `delete` can cause irreversible harm that a read-only agent cannot. Capability must be granted
per task and gated by approval; M13 measured 4/6 unsafe executions without guardrails and 0/6 with.

## Part C

**Q12.6 — Model answer.** Authorisation is a property of the authenticated session, not of the text.
Any user can type "I am the administrator"; if the runtime believed it, the claim would be a
password. Identity must come from the credential layer and be checked server-side.

**Q12.7 — Model answer.** A critic adds value when it independently verifies claims against the
sources and can reject or request a revision. It becomes theatre when it only restates the writer's
output approvingly, or when its verdict is not actionable — no rubric, no citations, no threshold.

## Part D

**Q12.8 —** $3^5=243$ sequences. Worst-case cost $=243\times0.002=0.486$ units. (If the bound is
read as "at most 5 calls total including repeats", $3^1+\dots+3^5=363$; state the reading. Award
marks for either with working.)

**Q12.9 —** Success rate $14/20=70\%$; refusal rate $2/20=10\%$; the remaining 20% are failures.

## Part E

**Q12.10 —** One `search`, then two `read` calls (one per document), then one `summarise` per
document or one over the combined text: 4 calls if summarising each, 3 if summarising once. State
the assumption; both are acceptable with the trace shown.

## Part F

**Q12.11 —** `[] ['debug']`

`query` is present so `missing` is empty; `debug` is not in the allowed set, so it is rejected. A
runtime that ignores unknown keys instead of rejecting them is a common and dangerous shortcut.

---

[Quiz](quiz-m12.md) · [Previous solutions](quiz-m11.md) · [Assessment index](../README.md)
