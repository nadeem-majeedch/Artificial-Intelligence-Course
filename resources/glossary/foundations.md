# Glossary — Foundations (M01, M02)

Terms for what AI is, how the field developed, and what an agent is. Back to the
[glossary index](README.md).

## A

### Actuator
**Abbreviation.** — · **Module.** M02
**Simple definition.** The part of an agent that changes the environment.
**Detailed explanation.** Sensors convert the world into percepts; actuators convert the agent's
decisions back into effects on the world. In software agents the actuator is an API call, a
database write or a message sent to another service, which is why "action" and "side effect"
are the same idea seen from two sides.
**Mathematics.** —
**Practical example.** A support-ticket agent reads the queue with an API (sensor) and applies a
label with a second API call (actuator); if the label call fails, the agent has perceived but not
acted.
**Related.** [Agent](#agent), [Percept](#percept), [Environment (task environment)](#environment-task-environment)
**Where it is taught.** [L02-01 Agents, percepts and actions](../../modules/M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

### Agent
**Abbreviation.** — · **Module.** M02
**Simple definition.** Anything that perceives its environment and acts on it to achieve a goal.
**Detailed explanation.** The agent abstraction separates *what* a system decides from *how* it
is implemented: a thermostat, a chess engine and a large language model are all agents if they
map percepts to actions. The abstraction is useful because it lets one analysis (rationality,
environment type, observability) apply to all of them.
**Mathematics.** $f: P^* \to A$ — the agent function maps a percept history to an action.
**Practical example.** A trading bot receives prices every second (percepts) and places or cancels
orders (actions); its environment is partially observable and stochastic, which is why a rule
that works in backtests can fail live.
**Related.** [Rational agent](#rational-agent), [Percept](#percept), [Environment (task environment)](#environment-task-environment)
**Where it is taught.** [L02-01 Agents, percepts and actions](../../modules/M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

### AI winter
**Abbreviation.** — · **Module.** M01
**Simple definition.** A period when funding and interest in AI collapsed after promises
outran results.
**Detailed explanation.** The term covers two episodes: the late-1970s reaction to the limits of
perceptrons and machine translation, and the late-1980s collapse of the expert-system market.
Both followed the same pattern — a capability gap hidden by demos, then withdrawal. The lesson
is about incentives rather than technology: a field that reports only successes will be
punished when the failures surface.
**Mathematics.** —
**Practical example.** The LISP-machine market collapsed in 1987 when cheaper workstations
matched its performance; the technical capability had improved while the business case
disappeared.
**Related.** [Symbolic AI](#symbolic-ai), [Connectionist AI](#connectionist-ai), [Narrow AI](#narrow-ai)
**Where it is taught.** [L01-02 A brief history of AI and the AI winters](../../modules/M01-introduction-and-foundations/lessons/L01-02-history-and-ai-winters.md)

## C

### Connectionist AI
**Abbreviation.** — · **Module.** M01
**Simple definition.** The approach that builds intelligence from many simple learned units
rather than explicit rules.
**Detailed explanation.** Connectionism distributes knowledge across weights instead of storing
it in symbols. It won the last decade because gradient-based training on large data beats
hand-written rules wherever data is plentiful, but it gives up inspectability: a weight matrix
has no sentence-length explanation.
**Mathematics.** $y = \sigma(W_2\,\sigma(W_1 x + b_1) + b_2)$ — knowledge lives in $W_1, W_2$.
**Practical example.** A spam filter learned from 200,000 labelled emails generalises to wording
nobody wrote a rule for, but cannot tell you *why* one email was blocked.
**Related.** [Symbolic AI](#symbolic-ai), [Narrow AI](#narrow-ai)
**Where it is taught.** [L01-03 The many faces of AI](../../modules/M01-introduction-and-foundations/lessons/L01-03-symbolic-statistical-generative.md)

## E

### Environment (task environment)
**Abbreviation.** — · **Module.** M02
**Simple definition.** The problem an agent operates in, described by its observability,
determinism, episodicity, dynamics and number of agents.
**Detailed explanation.** These five properties decide which techniques are even applicable:
a fully observable, deterministic environment permits search and planning, while a partially
observable, stochastic one requires beliefs and learning. Naming the environment type before
choosing an algorithm prevents the most common design error in the course.
**Mathematics.** —
**Practical example.** Chess is fully observable, deterministic and sequential; a cancer-screening
decision is partially observable, stochastic and episodic — the same tree-search instinct does not
transfer.
**Related.** [Agent](#agent), [Percept](#percept), [Rational agent](#rational-agent)
**Where it is taught.** [L02-01 Agents, percepts and actions](../../modules/M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

## G

### General AI
**Abbreviation.** AGI · **Module.** M01
**Simple definition.** A system that can perform any intellectual task a person can, including
transferring skill to unfamiliar problems.
**Detailed explanation.** Generality is a claim about *breadth of transfer*, not about scale or
fluency. Current systems are narrow in the precise sense that their competence is bounded by
their training distribution, even when their outputs sound general. The term is worth using
carefully because marketing uses it loosely.
**Mathematics.** —
**Practical example.** A model that writes code in forty languages still fails a task requiring a
new tool it has never seen combined with a constraint it has never been given — narrowness
appears at composition, not at syntax.
**Related.** [Narrow AI](#narrow-ai), [Turing test](#turing-test), [Connectionist AI](#connectionist-ai)
**Where it is taught.** [L01-01 What is artificial intelligence?](../../modules/M01-introduction-and-foundations/lessons/L01-01-what-is-artificial-intelligence.md)

## H

### Hybrid AI
**Abbreviation.** — · **Module.** M01
**Simple definition.** A system that combines learned components with explicit rules, search or
symbolic structure.
**Detailed explanation.** Hybrids exist because the two paradigms fail differently: learning
handles perception and ambiguity, symbols handle constraints and auditability. The practical
pattern is to let a model propose and a deterministic component dispose — the rule layer can
refuse an action the model cannot be trusted to refuse.
**Mathematics.** —
**Practical example.** A loan system scores with a gradient-boosted model but applies a hard
regulatory cap in code, so no model output can exceed the legal limit.
**Related.** [Symbolic AI](#symbolic-ai), [Connectionist AI](#connectionist-ai), [Agent](#agent)
**Where it is taught.** [L14-01 AI in practice: case studies and hybrid systems](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-01-ai-in-practice-case-studies-and-hybrid-systems.md)

## N

### Narrow AI
**Abbreviation.** — · **Module.** M01
**Simple definition.** A system that performs one task or a narrow family of tasks well.
**Detailed explanation.** Narrowness is about the scope of the competence, not the size of the
model. A 70-billion-parameter model that answers questions is narrow because its competence does
not extend to tasks outside its training objective without new data or tools.
**Mathematics.** —
**Practical example.** A model tuned for radiology reports degrades sharply on legal contracts
even though both are English text — the distribution, not the language, defines the boundary.
**Related.** [General AI](#general-ai), [Connectionist AI](#connectionist-ai)
**Where it is taught.** [L01-01 What is artificial intelligence?](../../modules/M01-introduction-and-foundations/lessons/L01-01-what-is-artificial-intelligence.md)

## P

### PEAS
**Abbreviation.** PEAS · **Module.** M02
**Simple definition.** Performance measure, Environment, Actuators, Sensors — the four-part
description of an agent's task.
**Detailed explanation.** PEAS forces the designer to state what "good" means before choosing an
algorithm. The performance measure is the part most often left vague, and it is the part that
determines whether the agent is rational.
**Mathematics.** —
**Practical example.** For an automated vacuum: performance = dirt cleaned per hour with battery
constraints; environment = floors, furniture, pets; actuators = wheels, brushes, suction;
sensors = bump, dirt, camera.
**Related.** [Agent](#agent), [Rational agent](#rational-agent), [Environment (task environment)](#environment-task-environment)
**Where it is taught.** [L02-01 Agents, percepts and actions](../../modules/M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

### Percept
**Abbreviation.** — · **Module.** M02
**Simple definition.** One unit of sensory input an agent receives at a moment in time.
**Detailed explanation.** A percept is not the environment; it is what the sensors report, which
may be incomplete, noisy or delayed. The percept *sequence* is what the agent function consumes,
which is why memory matters in partially observable settings.
**Mathematics.** $p_t \in P$ at time $t$; the agent sees $p_1, \dots, p_t$.
**Practical example.** A robot's camera returns a frame with a glare patch; the frame is the
percept, the room is the environment, and the glare is why the agent's belief can be wrong.
**Related.** [Agent](#agent), [Actuator](#actuator), [Environment (task environment)](#environment-task-environment)
**Where it is taught.** [L02-01 Agents, percepts and actions](../../modules/M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

## R

### Rational agent
**Abbreviation.** — · **Module.** M02
**Simple definition.** An agent that chooses the action expected to maximise its performance
measure given what it knows.
**Detailed explanation.** Rationality is relative to the percept sequence and built-in knowledge,
so it is not omniscience: a rational agent can make a mistake because its information was
incomplete. The definition is useful because it separates "bad outcome" from "bad decision".
**Mathematics.** $a^* = \arg\max_{a} \mathbb{E}[U \mid p_{1:t}, a]$
**Practical example.** A routing agent chooses the fastest expected route and still arrives late
after an accident; the decision was rational, the outcome was not.
**Related.** [Agent](#agent), [PEAS](#peas), [Environment (task environment)](#environment-task-environment)
**Where it is taught.** [L02-01 Agents, percepts and actions](../../modules/M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

## S

### Symbolic AI
**Abbreviation.** GOFAI · **Module.** M01
**Simple definition.** The approach that represents knowledge as explicit symbols and manipulates
them with rules.
**Detailed explanation.** Symbolic systems are inspectable and composable — a proof step can be
explained — but brittle outside their rule set, because every exception must be written down.
The knowledge-acquisition bottleneck is the reason expert systems stalled.
**Mathematics.** $KB \models \alpha$ — entailment between a knowledge base and a sentence.
**Practical example.** A tax engine that encodes statute as rules can justify every line of a
return, but a new regulation requires a developer, not a retraining run.
**Related.** [Connectionist AI](#connectionist-ai), [Hybrid AI](#hybrid-ai), [AI winter](#ai-winter)
**Where it is taught.** [L01-03 The many faces of AI](../../modules/M01-introduction-and-foundations/lessons/L01-03-symbolic-statistical-generative.md)

## T

### Turing test
**Abbreviation.** — · **Module.** M01
**Simple definition.** A behavioural test of machine intelligence: a human judge cannot tell the
machine's conversation from a person's.
**Detailed explanation.** The test measures indistinguishability in text, not understanding,
and it is easy to game with fluent evasion. Its lasting contribution is the operational framing —
define intelligence by observable behaviour — and its lasting problem is that behaviour can be
imitated without the competence being present.
**Mathematics.** —
**Practical example.** A 2023-era chatbot passes a five-minute text comparison while failing a
calculation a child can do; the test's verdict and the capability diverge.
**Related.** [General AI](#general-ai), [Narrow AI](#narrow-ai)
**Where it is taught.** [L01-01 What is artificial intelligence?](../../modules/M01-introduction-and-foundations/lessons/L01-01-what-is-artificial-intelligence.md)

---

[Glossary index](README.md) · [Classical AI terms](classical-ai.md) · [Quick reference](../glossary.md)
