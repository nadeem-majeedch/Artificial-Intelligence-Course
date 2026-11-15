# Course Modules

Fourteen modules, from "what is AI" to a defended capstone project. This page is the index: each
module has its own section below describing what it covers, what you will be able to do afterwards,
and what it assumes you already know. Every section links to the module's own landing page, which
lists every lesson, notebook, lab and assessment in reading order.

**Course home:** [README](../README.md) · **Prerequisites:** [P01–P04](../prerequisites/README.md) ·
**Sequence:** [learning paths](../docs/learning-path.md) · [roadmap](../docs/course-roadmap.md)

## Module index

| Module | Title | Level | Hours | Course outcome |
| :--- | :--- | :--- | ---: | :--- |
| [M01](#m01) | Introduction and Foundations of Artificial Intelligence | 100 | 12.8 | CLO1 |
| [M02](#m02) | Intelligent Agents and Environments | 200 | 17.9 | CLO1 |
| [M03](#m03) | Problem Solving and Search Algorithms | 200 | 19.9 | CLO2 |
| [M04](#m04) | Knowledge Representation and Logical Reasoning | 200 | 31.6 | CLO3 |
| [M05](#m05) | Uncertainty, Bayesian Reasoning and Fuzzy Logic | 300 | 20.6 | CLO4 |
| [M06](#m06) | Machine Learning Fundamentals and Algorithms | 300 | 31.4 | CLO5 |
| [M07](#m07) | Artificial Neural Networks and Deep Learning | 300 | 24.9 | CLO6 |
| [M08](#m08) | Natural Language Processing | 300 | 24.3 | CLO6, CLO7 |
| [M09](#m09) | Computer Vision | 300 | 26.8 | CLO6 |
| [M10](#m10) | Reinforcement Learning | 400 | 34.1 | CLO7 |
| [M11](#m11) | Generative AI and Large Language Models | 400 | 23.3 | CLO7 |
| [M12](#m12) | AI Agents and Agentic AI Systems | 400 | 27.8 | CLO7 |
| [M13](#m13) | Responsible, Explainable and Secure AI | 300 | 22.4 | CLO8 |
| [M14](#m14) | Advanced AI Applications and Capstone Projects | 400 | 32.9 | CLO8 |

**Levels.** 100 assumes no AI background; 200 assumes programming and basic mathematics; 300
assumes linear algebra and probability; 400 assumes the modules named in its prerequisites.
**Hours** are total study effort: lessons, notebooks, labs, assignments, quizzes and mini-projects.

**How each module page is organised:** overview, learning outcomes, prerequisites with a readiness
self-check, a table of every lesson, notebook, lab, assignment, quiz and mini-project with links
and time estimates, a suggested seven-day study plan, and navigation to the neighbouring modules.

**Content status.** All fourteen modules are complete. Every module page states its current
inventory, and every relative link on this page resolves to a file in the repository.

---

<a id="m01"></a>
## M01: Introduction and Foundations of Artificial Intelligence

| | |
| :--- | :--- |
| **Level** | 100 |
| **Study time** | 12.8 hours |
| **Course outcome** | CLO1 — explain what AI is, how the field evolved, and how agents act in an environment |
| **Prerequisites** | None |

**Overview.** Before writing a single algorithm, you need an accurate mental model of the field.
This module separates the three meanings of "AI" that beginners conflate — a goal, a set of
techniques, and a marketing label — and traces how the ideas developed from symbolic reasoning
through the statistical turn to today's generative systems. It also sets the working habits the
rest of the course depends on: how to read a lesson, when to run code, and how to check yourself.

**What you will be able to do.** Define AI precisely enough to argue about it; explain what the
"AI winters" were and why they happened; distinguish symbolic, statistical and generative
approaches and say what each is good at; recognise claims that AI cannot currently support; set up
your study environment and run your first notebook.

**Planned components.** 5 lessons · 1 notebook · 1 lab · 1 quiz · 1 mini-project.

**Content status:** complete — 5 lessons, a notebook, 2 labs, a quiz, a mini-project and reference code.

**Start here:** [M01 module page](M01-introduction-and-foundations/README.md) · [L01-01 What Is Artificial Intelligence?](M01-introduction-and-foundations/lessons/L01-01-what-is-artificial-intelligence.md)

---

<a id="m02"></a>
## M02: Intelligent Agents and Environments

| | |
| :--- | :--- |
| **Level** | 200 |
| **Study time** | 17.9 hours |
| **Course outcome** | CLO1 |
| **Prerequisites** | P01 (Python) |

**Overview.** "Agent" is the organising abstraction of the whole field: something that perceives an
environment, decides, and acts. This module gives you the vocabulary to describe any AI system
precisely — percepts, actions, rationality, PEAS descriptions, and the properties of environments
(observable or not, deterministic or stochastic, static or dynamic). Every later module is, in
effect, a different way of choosing the agent function.

**What you will be able to do.** Write a PEAS description for a system you know; classify an
environment and predict which algorithm families will work in it; implement simple reflex,
model-based, goal-based and utility-based agents; explain why learning agents need a performance
standard rather than a fixed rule.

**Planned components.** 5 lessons · 2 notebooks · 2 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 5 lessons, 1 executed notebook, 2 labs and a quiz are published.

**Start here:** [M02 module page](M02-intelligent-agents-and-environments/README.md) · [L02-01 Agents, Percepts, Actions](M02-intelligent-agents-and-environments/lessons/L02-01-agents-percepts-actions.md)

---

<a id="m03"></a>
## M03: Problem Solving and Search Algorithms

| | |
| :--- | :--- |
| **Level** | 200 |
| **Study time** | 19.9 hours |
| **Course outcome** | CLO2 |
| **Prerequisites** | P01 (Python), P02 (vectors and matrices) |

**Overview.** The largest module in the classical half of the course, and the one that teaches the
habit of thinking in terms of states, actions and costs. You start by turning a described problem
into a search problem, then work through uninformed search, heuristics, A\*, local search,
adversarial search and constraint satisfaction. Along the way you learn the analysis that makes
the difference between an algorithm that finishes and one that does not: branching factor, depth,
and why an admissible heuristic is worth the trouble.

**What you will be able to do.** Formulate a real problem as a state space; choose between BFS,
DFS, uniform-cost and A\* with a reasoned argument rather than a guess; design a heuristic and prove
it admissible; implement minimax with alpha–beta pruning; model a scheduling problem as a
constraint satisfaction problem and solve it.

**Planned components.** 8 lessons · 3 notebooks · 3 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 7 lessons, 1 executed notebook, 2 labs and a quiz are published.
point at which self-study stalls; the labs are designed to prevent that.

---

<a id="m04"></a>
## M04: Knowledge Representation and Logical Reasoning

| | |
| :--- | :--- |
| **Level** | 200 |
| **Study time** | 31.6 hours |
| **Course outcome** | CLO3 |
| **Prerequisites** | P02 (vectors and matrices) |

**Overview.** Machine learning is not the only way to make a system know something. This module
covers the symbolic tradition: representing facts and rules in propositional and first-order logic,
and deriving new facts by sound inference. These ideas still run scheduling engines, eligibility
systems, database constraints and knowledge graphs — and they teach a discipline that statistical
methods lack: the ability to say exactly what follows from what.

**What you will be able to do.** Translate a domain into propositions and predicates; evaluate
entailment with truth tables, forward and backward chaining, and resolution; use quantifiers and
unification correctly; explain what a knowledge graph or ontology provides; recognise the limits
of rule-based systems, including where uncertainty forces a different approach.

**Planned components.** 7 lessons · 2 notebooks · 2 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 7 lessons, 2 executed notebooks, 3 labs, a mini-project and a quiz are published.

**Start here:** [M04 module page](M04-knowledge-representation-and-logical-reasoning/README.md) · [L04-01 Knowledge Representation](M04-knowledge-representation-and-logical-reasoning/lessons/L04-01-knowledge-representation-fundamentals.md)

---

<a id="m05"></a>
## M05: Uncertainty, Bayesian Reasoning and Fuzzy Logic

| | |
| :--- | :--- |
| **Level** | 300 |
| **Study time** | 20.6 hours |
| **Course outcome** | CLO4 |
| **Prerequisites** | P03 (probability) |

**Overview.** Real systems never have complete information. This module turns "probably" into
mathematics: conditional probability, Bayes' rule, Bayesian networks and inference over them, then
reasoning over time with Markov chains and hidden Markov models. It closes with fuzzy logic, which
handles vagueness rather than randomness — a distinction that matters in control systems and in
any domain where "warm" and "tall" are real categories.

**What you will be able to do.** Apply Bayes' rule to update a belief with evidence; build a
Bayesian network for a domain and compute a posterior by hand and by code; explain conditional
independence and why it makes inference tractable; design a small fuzzy inference system; choose
between probabilistic and fuzzy representations for a given problem.

**Planned components.** 7 lessons · 3 notebooks · 3 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 6 lessons, 2 executed notebooks, 2 labs and a quiz are published.
foundation for M10.

---

<a id="m06"></a>
## M06: Machine Learning Fundamentals and Algorithms

| | |
| :--- | :--- |
| **Level** | 300 |
| **Study time** | 31.4 hours |
| **Course outcome** | CLO5 |
| **Prerequisites** | P02 (matrices and gradients), P03 (probability), P04 (data preparation) |

**Overview.** The module where most self-study courses begin and most of them go wrong. You will
learn regression, classification, the classical algorithm family (k-NN, naïve Bayes, trees,
ensembles, k-means, PCA) *and* the part tutorials skip: validation design, leakage, baselines,
metric choice, bias–variance and honest error analysis. The aim is not to know many algorithms; it
is to be able to defend a model.

**What you will be able to do.** Split data without leaking; justify a metric for an imbalanced
problem; fit and regularise linear and logistic models; compare tree and ensemble methods with
evidence; build a reproducible pipeline and explain every choice in it; diagnose overfitting and
underfitting from learning curves.

**Components.** 10 lessons · 4 notebooks · 4 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete, including all eight practical scenarios (student performance, house
prices, spam, customer segmentation, loan approval, intrusion detection, attrition and credit-card
anomalies) and a four-part leakage audit. Every dataset is generated in-script with fixed seeds,
and each mirrors the schema of a named public dataset so the real file can be substituted.

**Start here:** [M06 module page](M06-machine-learning-fundamentals/README.md) ·
[L06-01 What Machine Learning Is](M06-machine-learning-fundamentals/lessons/L06-01-what-machine-learning-is.md) ·
[summary](M06-machine-learning-fundamentals/summary.md)

This module is the hard prerequisite for everything from M07 onwards; do not compress it.

---

<a id="m07"></a>
## M07: Artificial Neural Networks and Deep Learning

| | |
| :--- | :--- |
| **Level** | 300 |
| **Study time** | 24.9 hours |
| **Course outcome** | CLO6 |
| **Prerequisites** | M06, P02 (gradients) |

**Overview.** From the perceptron to the transformer, with the mathematics done properly once.
You implement a network and one epoch of backpropagation by hand — the single most clarifying
exercise in the course — then learn the engineering that makes training work: initialisation,
optimisers, regularisation, and how to tell a learning-rate problem from a data problem. It closes
with attention and with transfer learning — the two ideas that make modern pretrained models usable
on small datasets, and the bridge to M08, M09 and M11.

**What you will be able to do.** Derive and implement backpropagation; verify gradients numerically;
train and debug a network without guessing; explain what convolution does and why it suits images;
describe how an LSTM carries state and why attention replaced it in most language tasks; fine-tune a
pretrained model.

**Components.** 8 lessons · 3 notebooks · 3 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete. Covers the perceptron through Transformers with NumPy and PyTorch
implementations, and all seven scenarios (logic gates, digits, fashion textures, plant disease,
sentiment, LSTM forecasting and transfer learning). Every dataset is generated in-script with fixed
seeds; each mirrors a named public dataset so the real file can be substituted. No torchvision or
TensorFlow is required — TensorFlow/Keras appears only as annotated comparative snippets.

**Start here:** [M07 module page](M07-neural-networks-and-deep-learning/README.md) ·
[L07-01 From the Perceptron to the MLP](M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md) ·
[summary](M07-neural-networks-and-deep-learning/summary.md)

---

<a id="m08"></a>
## M08: Natural Language Processing

| | |
| :--- | :--- |
| **Level** | 300 |
| **Study time** | 24.3 hours |
| **Course outcome** | CLO6, CLO7 |
| **Prerequisites** | M07 |

**Overview.** Language is the domain where modern AI is most visible and least understood. This
module starts with the unglamorous foundations — normalisation, tokenisation, subwords, TF-IDF —
because they explain what a model actually sees, then moves through embeddings to transformer-based
fine-tuning. The evaluation lesson is deliberately as long as the modelling one: text models fail
in ways that aggregate accuracy hides.

**What you will be able to do.** Prepare text without destroying information; explain what a
subword token is and why vocabulary size matters; train and compare classical and neural text
classifiers; fine-tune an encoder for classification or entity recognition; analyse errors by class,
length and domain; audit a text pipeline for bias.

**Planned components.** 6 lessons · 2 notebooks · 2 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 6 lessons, 3 executed notebooks, 3 labs and a quiz are published.

**Start here:** [M08 code overview](M08-natural-language-processing/README.md)

---

<a id="m09"></a>
## M09: Computer Vision

| | |
| :--- | :--- |
| **Level** | 300 |
| **Study time** | 26.8 hours |
| **Course outcome** | CLO6 |
| **Prerequisites** | M07 |

**Overview.** Images are arrays, and most confusion about vision disappears once you accept that.
The module builds from pixels and convolution through classical feature methods to modern CNN
architectures, detection and segmentation. You will also test robustness: what happens to accuracy
under blur, brightness change, rotation and compression — questions that decide whether a model is
usable outside a benchmark.

**What you will be able to do.** Implement convolution and filtering from scratch; explain what a
CNN learns layer by layer; fine-tune a pretrained vision model on a small dataset; distinguish
classification, detection and segmentation tasks and their metrics; run an augmentation and
robustness study and report what you find.

**Planned components.** 6 lessons · 2 notebooks · 2 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 6 lessons, 4 executed notebooks, 4 labs, a quiz and an assignment are published.

---

<a id="m10"></a>
## M10: Reinforcement Learning

| | |
| :--- | :--- |
| **Level** | 400 |
| **Study time** | 34.1 hours |
| **Course outcome** | CLO7 |
| **Prerequisites** | M06, M05 (MDP section), P02, P03 |

**Overview.** Learning from consequences rather than labels. The module formalises the interaction
loop as a Markov decision process, solves small problems exactly with dynamic programming, then
removes the model: Monte Carlo, temporal-difference learning, SARSA and Q-learning. It closes with
function approximation and policy gradients, and with the engineering reality that reward design
decides what your agent actually learns — including the failures you did not intend.

**What you will be able to do.** Write down an MDP for a real decision problem; compute optimal
values by policy and value iteration; implement tabular Q-learning and explain its convergence
conditions; train a DQN on a small control task; recognise reward hacking and diagnose it from
learning curves.

**Planned components.** 7 lessons · 3 notebooks · 3 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 5 lessons, 3 executed notebooks, 4 labs, a mini-project and a quiz are published.

**Start here:** [M10 code overview](M10-reinforcement-learning/README.md)

---

<a id="m11"></a>
## M11: Generative AI and Large Language Models

| | |
| :--- | :--- |
| **Level** | 400 |
| **Study time** | 23.3 hours |
| **Course outcome** | CLO7 |
| **Prerequisites** | M07 (attention), M08 |

**Overview.** What is actually happening inside a large language model, and how do you build a
reliable system around one? The module covers the generative modelling landscape, tokenisation and
next-token prediction, pretraining and alignment, prompt engineering as an engineering discipline,
retrieval-augmented generation, parameter-efficient fine-tuning, and evaluation — faithfulness,
hallucination, cost and latency. Everything runs locally on CPU with small Apache-2.0 models; hosted
APIs appear only as optional comparisons, so no exercise or assessment needs a paid account.

**What you will be able to do.** Explain autoregressive generation and why it hallucinates; design
prompts and measure their effect rather than guessing; build a retrieval-augmented question
answering system with citations; apply parameter-efficient fine-tuning; build an evaluation harness
that reports quality, cost and failure modes together.

**Components.** 7 lessons · 2 notebooks · 3 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete. Four cached Apache-2.0 models (distilgpt2, flan-t5-small,
all-MiniLM-L6-v2, distilbert-SST-2) run offline on CPU, with a 24-document CC0-1.0 handbook corpus
authored for the module. Every number quoted in the lessons and labs comes from the module's own
scripts: tokenisation and attention measurements, VAE/GAN/diffusion training with a shared sample
metric (the GAN collapses to 3 of 10 classes), seven decoding strategies, grounded versus
closed-book answering, hybrid retrieval over FAISS and BM25 with MaxSim reranking, LoRA from
scratch with merge verification, int8 quantisation, and an evaluation harness reporting retrieval,
answer, grounding, refusal, latency and cost separately.

**Start here:** [M11 module page](M11-generative-ai-and-large-language-models/README.md) ·
[L11-01 The Generative Modelling Landscape](M11-generative-ai-and-large-language-models/lessons/L11-01-the-generative-modelling-landscape.md) ·
[L11-05 Retrieval-Augmented Generation](M11-generative-ai-and-large-language-models/lessons/L11-05-retrieval-augmented-generation.md) ·
[summary](M11-generative-ai-and-large-language-models/summary.md)

---

<a id="m12"></a>
## M12: AI Agents and Agentic AI Systems

| | |
| :--- | :--- |
| **Level** | 400 |
| **Study time** | 27.8 hours |
| **Course outcome** | CLO7 |
| **Prerequisites** | M11, M02 |

**Overview.** A language model answers; an agent acts. This module turns a model into a system that
uses tools, keeps memory, plans across steps and coordinates with other agents — then spends equal
effort on the new risks that creates: runaway loops, injected instructions, over-broad permissions
and untraceable failures. The engineering discipline here is closer to distributed systems than to
machine learning.

**What you will be able to do.** Build a tool-using agent with a bounded loop; define and validate
structured tool interfaces; add planning and memory without making behaviour unpredictable; apply
sandboxing, permission limits and logging; red-team your own agent and report what you found;
evaluate an agent on tasks rather than on vibes.

**Planned components.** 6 lessons · 1 notebook · 2 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete — 6 lessons, 1 executed notebook, 2 labs, an integrated project and a quiz are published.

**Start here:** [M12 code overview](M12-ai-agents-and-agentic-systems/README.md)

---

<a id="m13"></a>
## M13: Responsible, Explainable and Secure AI

| | |
| :--- | :--- |
| **Level** | 300 |
| **Study time** | 22.4 hours |
| **Course outcome** | CLO8 |
| **Prerequisites** | M06 |

**Overview.** Not an ethics appendix — an engineering module. You will measure bias in a model you
built, explain its decisions with tools and with inherently interpretable alternatives, examine
what a model memorises about individuals, and attack it: adversarial inputs, data poisoning and
prompt injection. The module ends with a practical audit checklist and a model card you can reuse
for the rest of your career.

**What you will be able to do.** Measure disparity across groups and say what the measurement does
and does not show; choose between post-hoc explanation and an interpretable model; apply privacy
protections and recognise their limits; demonstrate an adversarial or injection attack; write a
model card and a short audit report.

**Planned components.** 6 lessons · 1 notebook · 2 labs · 1 assignment · 1 quiz · 1 mini-project.

**Content status:** complete. Read the [module page](M13-responsible-explainable-secure-ai/README.md)
for the timetable, the code map and the licences.

**Start here:** [M13 module page](M13-responsible-explainable-secure-ai/README.md) ·
[L13-01 Responsible AI, Fairness and Bias](M13-responsible-explainable-secure-ai/lessons/L13-01-responsible-ai-fairness-and-bias.md) ·
[L13-02 Explainability](M13-responsible-explainable-secure-ai/lessons/L13-02-explainability-from-importance-to-counterfactuals.md) ·
[LAB-13-01 Fairness Audit](M13-responsible-explainable-secure-ai/labs/lab-13-01-fairness-audit.md) ·
[summary](M13-responsible-explainable-secure-ai/summary.md)

All lessons are measurement-first: every number quoted comes from a script in
[`code/`](M13-responsible-explainable-secure-ai/code/), including the results that contradict
the standard advice (reweighing changed nothing; the backdoored model scored higher clean
accuracy than the baseline; membership inference failed at AUC 0.513).

---

<a id="m14"></a>
## M14: Advanced AI Applications and Capstone Projects

| | |
| :--- | :--- |
| **Level** | 400 |
| **Study time** | 32.9 hours (14.0 of them project work) |
| **Course outcome** | CLO8 |
| **Prerequisites** | M13, plus the modules named by your chosen brief |

**Overview.** The course turns outward: how AI systems work in health, education, finance and
agriculture; what it takes to serve a model and keep it working as data drifts; how to read and
reproduce a research result; and how to scope a project you can actually finish. Most of the module
is your capstone, run in milestones with feedback points rather than a single deadline.

**What you will be able to do.** Evaluate a published AI system's claims critically; describe the
serving and monitoring lifecycle of a model; reproduce a small published result; scope a capstone
with a realistic evaluation plan; present and defend your project, including its limitations.

**Planned components.** 5 lessons · 1 assignment (proposal) · 1 quiz · capstone briefs, milestone
guides and rubric.

**Content status:** complete. Read the [module page](M14-advanced-ai-applications-and-capstone/README.md)
for the timetable, the code map and the capstone studio.

**Start here:** [M14 module page](M14-advanced-ai-applications-and-capstone/README.md) ·
[L14-01 AI in Practice](M14-advanced-ai-applications-and-capstone/lessons/L14-01-ai-in-practice-case-studies-and-hybrid-systems.md) ·
[L14-05 Capstone Studio](M14-advanced-ai-applications-and-capstone/lessons/L14-05-capstone-studio.md) ·
[capstone briefs](M14-advanced-ai-applications-and-capstone/capstone/README.md) ·
[summary](M14-advanced-ai-applications-and-capstone/summary.md)

The module is measurement-first like M13: every number comes from `code/`, including results that
contradict standard advice (distillation gained nothing, int8 was 1.6–2.4x slower in release
validation, a GNN lost 0.131 accuracy at low homophily).

---

## Choosing What to Study Next

1. **Have you finished a module?** Take its quiz. Below 60%, revisit the lessons it points to
   before moving on.
2. **Unsure between two modules?** Follow the dependency order in the
   [roadmap](../docs/course-roadmap.md); it always beats curiosity-driven jumping in the early
   stages.
3. **Short on time?** The [learning paths](../docs/learning-path.md) page defines a core path that
   covers the essential lessons of each module in about 169 hours.

**Navigation:** [Course home](../README.md) · [Prerequisites](../prerequisites/README.md) ·
[Learning paths](../docs/learning-path.md) · [Course roadmap](../docs/course-roadmap.md) ·
[Glossary](../resources/glossary.md) · [FAQ](../docs/faq.md)
