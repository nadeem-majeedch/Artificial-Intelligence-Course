# Glossary — Agents (M12)

M12 has reference code but no published lessons, so entries link to the module page and are
marked **module page only**. Back to the [glossary index](README.md).

## A

### Agent loop
**Abbreviation.** ReAct · **Module.** M12
**Simple definition.** The cycle of reasoning, acting, observing the result and deciding again.
**Detailed explanation.** A language model that can call tools needs a controller: it proposes an
action, executes it, reads the observation and repeats until a stopping condition. The loop is
where most agent failures occur — runaway iterations, ignored errors, premature termination.
**Mathematics.** $s_{t+1} = \text{env}(a_t)$, $a_t \sim \pi(\cdot \mid s_{\le t})$
**Practical example.** A ticket agent searches, reads the top result, notices the customer ID is
missing, asks for it, then closes — four iterations, with a hard cap of eight.
**Related.** [Tool use](#tool-use), [Guardrail](#guardrail), [Planning](#planning-agent)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

## G

### Guardrail
**Abbreviation.** — · **Module.** M12
**Simple definition.** A deterministic check that blocks or rewrites an agent action before it
takes effect.
**Detailed explanation.** Guardrails are deliberately outside the model: allowlists, schema
validation, spend limits, human approval for irreversible actions. A prompt instruction is not a
guardrail because a prompt can be overridden.
**Mathematics.** —
**Practical example.** An agent may draft a refund but the payment API rejects any amount above
the customer's last order, whatever the model requested.
**Related.** [Tool use](#tool-use), [Human-in-the-loop](#human-in-the-loop), [Agent loop](#agent-loop)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

## H

### Human-in-the-loop
**Abbreviation.** HITL · **Module.** M12
**Simple definition.** A design in which a person approves or reviews consequential agent actions.
**Detailed explanation.** HITL is a risk control, not a courtesy: it bounds the damage of a wrong
action at the cost of latency and attention. Its effectiveness depends on the reviewer actually
checking, which is why automation bias is measured rather than assumed.
**Mathematics.** —
**Practical example.** A contract agent extracts clauses automatically but routes any redline to
a lawyer; approval latency rises by 20 minutes and error cost falls to near zero.
**Related.** [Guardrail](#guardrail), [Multi-agent system](#multi-agent-system)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

## M

### Memory (agent)
**Abbreviation.** — · **Module.** M12
**Simple definition.** Stored state an agent carries between steps or sessions.
**Detailed explanation.** Short-term memory is the context window; long-term memory is an external
store retrieved on demand. Without memory an agent repeats work; with unmanaged memory it grows
cost and contradicts itself.
**Mathematics.** —
**Practical example.** A support agent stores the customer's plan and previous ticket IDs, so a
follow-up message does not re-ask for them.
**Related.** [Agent loop](#agent-loop), [Tool use](#tool-use)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

### Multi-agent system
**Abbreviation.** MAS · **Module.** M12
**Simple definition.** Several agents that divide a task and coordinate their outputs.
**Detailed explanation.** Specialisation can beat one general agent on wide tasks, but every
hand-off adds a failure mode and a cost. Coordination protocols (shared state, message passing,
supervisor delegation) matter more than the number of agents.
**Mathematics.** —
**Practical example.** A research system with a planner, a retriever and a writer produces better
reports than one agent, but only when the planner's output is schema-validated before hand-off.
**Related.** [Orchestration](#orchestration), [Agent loop](#agent-loop)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

## O

### Orchestration
**Abbreviation.** — · **Module.** M12
**Simple definition.** The component that decides which agent or tool runs next, and with what
input.
**Detailed explanation.** Orchestration is ordinary distributed-systems work wearing new clothes:
retries, timeouts, idempotency, tracing. Agents make it harder because steps are chosen at
runtime, so observability is the difference between a debuggable system and a mystery.
**Mathematics.** —
**Practical example.** A supervisor assigns subtasks, enforces a global token budget and logs every
tool call with its latency; when a run fails, the trace shows which step.
**Related.** [Multi-agent system](#multi-agent-system), [Planning](#planning-agent), [Guardrail](#guardrail)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

## P

### Planning (agent)
**Abbreviation.** — · **Module.** M12
**Simple definition.** Decomposing a goal into ordered steps before acting.
**Detailed explanation.** Planning separates "what to do" from "how to do it", which makes
progress checkable and failures locatable. Plans must be revisable: an agent that cannot update
its plan after an error will repeat it.
**Mathematics.** —
**Practical example.** "Prepare the quarterly report" becomes retrieve sales, compute variance,
draft, verify numbers, send for review — each step verifiable.
**Related.** [Agent loop](#agent-loop), [Orchestration](#orchestration)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

## T

### Tool use
**Abbreviation.** Function calling · **Module.** M12
**Simple definition.** Letting a model call an external function with structured arguments and
read the result.
**Detailed explanation.** Tools extend a model beyond its weights: calculators, databases, search,
APIs. The model proposes arguments; the host validates and executes them, which is the security
boundary that makes tool use safe or catastrophic.
**Mathematics.** $a = \text{model}(s) \to \text{tool}(a.\text{name}, a.\text{args}) \to o$
**Practical example.** A model asked for a square root calls a calculator tool rather than
guessing, and the answer is exact because the host computed it.
**Related.** [Guardrail](#guardrail), [Agent loop](#agent-loop), [Orchestration](#orchestration)
**Where it is taught.** Module page only — [M12 AI Agents](../../modules/M12-ai-agents-and-agentic-systems/README.md)

---

[Glossary index](README.md) · [Generative AI](generative-ai.md) · [Responsible AI](responsible-ai.md) · [Quick reference](../glossary.md)
