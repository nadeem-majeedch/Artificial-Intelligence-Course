# Artificial Intelligence — A Comprehensive Course

**A university-level, beginner-to-advanced course in artificial intelligence, designed for
self-study and adaptable for classroom teaching.**

This course progresses from the foundations of intelligent agents through classical AI, machine
learning, deep learning and modern generative and agentic systems, and ends with a scoped capstone
project. It combines explanatory lessons, hand-worked mathematics, runnable Python notebooks,
practical laboratories, quizzes, assignments and project-based learning. Every module states what
it assumes, what it contains and what a student should be able to do afterwards.

**Instructor:** Engr. Dr. Muhammad Nadeem Majeed  
Professor  
Department of Data Science (PUCIT)  
University of the Punjab, Lahore, Pakistan.

**Start here:** [Learning paths](docs/learning-path.md) · [Prerequisites](prerequisites/README.md) ·
[All modules](modules/README.md) · [FAQ](docs/faq.md)

---

## Contents

- [1. Course description](#1-course-description)
- [2. Learning outcomes](#2-learning-outcomes)
- [3. Prerequisites](#3-prerequisites)
- [4. Course roadmap](#4-course-roadmap)
- [5. Course structure](#5-course-structure)
- [6. Study workload](#6-study-workload)
- [7. How to use the course](#7-how-to-use-the-course)
- [8. Software requirements](#8-software-requirements)
- [9. Licensing and attribution](#9-licensing-and-attribution)
- [10. Academic disclaimer](#10-academic-disclaimer)
- [11. Contribution and feedback](#11-contribution-and-feedback)

---

## 1. Course description

Artificial Intelligence is broad: it includes search and planning, knowledge representation,
reasoning under uncertainty, machine learning, perception, language, reinforcement learning,
generative models and multi-agent systems. This course teaches that breadth in a deliberate order,
so that each idea arrives with the background it needs.

The course is written for a reader who does not have an instructor in the room. Lessons begin with
intuition, work through examples by hand, and then implement the idea in Python. Laboratories place
the idea in a realistic scenario with requirements, a deliverable and a rubric. The capstone asks
the student to scope, build, evaluate and defend a complete AI project.

It is suitable for undergraduate and postgraduate students, working developers moving into AI,
researchers from other fields, teachers adapting course material, and self-taught programmers who
want the foundations that tutorials often omit.

## 2. Learning outcomes

On completing the course, a student should be able to:

| ID | Outcome |
| :--- | :--- |
| CLO1 | Explain what AI is, how the field evolved, and how agents perceive, decide and act in an environment. |
| CLO2 | Formulate a problem as a search or constraint problem and justify a search strategy with its complexity trade-offs. |
| CLO3 | Represent knowledge in propositional and first-order logic and derive conclusions by sound inference. |
| CLO4 | Quantify uncertainty with probability, build and query Bayesian networks, and design a fuzzy inference system. |
| CLO5 | Run a leakage-free machine-learning workflow and evaluate models with appropriate metrics. |
| CLO6 | Build, train, debug and evaluate neural networks for tabular, text and image data. |
| CLO7 | Implement reinforcement-learning and generative systems, and assemble a tool-using AI agent. |
| CLO8 | Audit an AI system for fairness, explainability, privacy and security, and deliver a documented capstone project. |

The detailed outcome-to-module mapping is in the [curriculum map](docs/CURRICULUM-MAP.md).

## 3. Prerequisites

The course has a four-section prerequisite track. It is part of the course, not an entrance exam:

| Section | Topic | Hours | Use |
| :--- | :--- | ---: | :--- |
| [P01](prerequisites/P01-python-programming/README.md) | Python programming for AI | 14 | Essential if you have not programmed before |
| [P02](prerequisites/P02-mathematics-for-ai/README.md) | Vectors, matrices, calculus and optimisation | 24 | Essential before M03, M06 and M07 |
| [P03](prerequisites/P03-probability-and-statistics/README.md) | Probability and statistics | 10 | Essential before M05 and M06 |
| [P04](prerequisites/P04-data-preparation-and-visualization/README.md) | Data preparation and visualisation | 8 | Recommended before M06, M08 and M09 |

**Essential knowledge.**

- **Python programming:** variables, control flow, functions, lists and dictionaries. Complete P01
  if these are unfamiliar.
- **Basic mathematics:** algebra and functions. P02 supplies the rest.
- **Linear algebra:** vectors, matrices and matrix multiplication, needed from M06 onwards.
- **Probability and statistics:** conditional probability, distributions and summary statistics,
  needed from M05 onwards.
- **Basic data structures:** lists, dictionaries, stacks, queues and graphs. These can be learned
  alongside M01–M03; the early modules use them with explanation.

**Can be learned alongside the course.** Calculus is introduced in P02 and revisited where it is
used. Data preparation and visualisation can be studied immediately before M06. A GPU, paid API or
prior AI experience is not required.

A readiness diagnostic and alternative entry points are on the
[learning paths](docs/learning-path.md) and [prerequisites](prerequisites/README.md) pages.

## 4. Course roadmap

The 14 modules are listed in their intended learning sequence. Each title links to its module
landing page, which lists every lesson, notebook, laboratory and assessment.

| # | Module | Short description | Workload |
| ---: | :--- | :--- | ---: |
| M01 | [Introduction and Foundations of Artificial Intelligence](modules/M01-introduction-and-foundations/README.md) | AI as a field, agents, environments, capability claims and study method | 12.8 h |
| M02 | [Intelligent Agents and Environments](modules/M02-intelligent-agents-and-environments/README.md) | Percepts, actions, rationality, PEAS descriptions and agent architectures | 17.9 h |
| M03 | [Problem Solving and Search Algorithms](modules/M03-problem-solving-and-search-algorithms/README.md) | Uninformed and informed search, local search, minimax, alpha–beta and CSPs | 19.9 h |
| M04 | [Knowledge Representation and Logical Reasoning](modules/M04-knowledge-representation-and-logical-reasoning/README.md) | Propositional and first-order logic, inference, unification and resolution | 31.6 h |
| M05 | [Uncertainty, Bayesian Reasoning and Fuzzy Logic](modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/README.md) | Bayes' rule, Bayesian networks, naive Bayes, fuzzy inference and variable elimination | 20.6 h |
| M06 | [Machine Learning Fundamentals and Algorithms](modules/M06-machine-learning-fundamentals/README.md) | Leakage-free workflows, regression, classification, metrics, trees, SVM and clustering | 31.4 h |
| M07 | [Artificial Neural Networks and Deep Learning](modules/M07-neural-networks-and-deep-learning/README.md) | Backpropagation, training, regularisation, CNNs, RNNs, attention and transfer learning | 24.9 h |
| M08 | [Natural Language Processing](modules/M08-natural-language-processing/README.md) | Text processing, TF-IDF, embeddings, classification, NER and sequence models | 24.3 h |
| M09 | [Computer Vision](modules/M09-computer-vision/README.md) | Image processing, features, CNNs, object detection, segmentation and evaluation | 26.8 h |
| M10 | [Reinforcement Learning](modules/M10-reinforcement-learning/README.md) | MDPs, value iteration, Q-learning, SARSA, deep RL and reward design | 34.1 h |
| M11 | [Generative AI and Large Language Models](modules/M11-generative-ai-and-large-language-models/README.md) | Tokens and attention, pretraining, prompting, RAG, PEFT and evaluation | 23.3 h |
| M12 | [AI Agents and Agentic AI Systems](modules/M12-ai-agents-and-agentic-systems/README.md) | Tool calling, planning, memory, multi-agent systems, MCP and security | 27.8 h |
| M13 | [Responsible, Explainable and Secure AI](modules/M13-responsible-explainable-secure-ai/README.md) | Fairness, explainability, privacy, adversarial security, governance and auditing | 22.4 h |
| M14 | [Advanced AI Applications and Capstone Projects](modules/M14-advanced-ai-applications-and-capstone/README.md) | Applied systems, MLOps, monitoring, research reproduction and the capstone studio | 32.9 h |

The prerequisite track precedes or runs alongside this sequence. Recommended routes — core,
core plus deep learning, full programme and three specialisations — are described in
[learning paths](docs/learning-path.md).

## 5. Course structure

The current repository contains:

| Component | Inventory |
| :--- | :--- |
| Modules | 14, each with a landing page, outcomes, prerequisites, module map and study plan |
| Lessons | 89 module lessons and 21 prerequisite lessons |
| Jupyter notebooks | 35 course notebooks (29 module, 6 prerequisite), executed during release validation |
| Practical laboratories | 38 module laboratories and 5 prerequisite laboratories, with scenarios, deliverables and marking guidance |
| Assignments | 22 (14 programming and 8 analytical), with specifications and rubrics |
| Quizzes | 14 module quizzes with explained answer keys |
| Self-assessment | 14 module self-assessment sets, plus lesson-level self-checks |
| Projects | 8 module projects and 12 capstone briefs |
| Capstone | Proposal, four milestones, rubric, report template and defence guidance |
| Reference material | Glossary, concept maps, 95 annotated books and papers, and official library documentation |

Every module follows the same structure: learning outcomes, prerequisites, a readiness check, a
sequenced module map with time estimates, lessons, notebooks, laboratories, assessment and
navigation to neighbouring modules.

## 6. Study workload

The workload figures use the reconciliation documented in
[curriculum map §3.1](docs/CURRICULUM-MAP.md#31-how-the-hour-totals-are-calculated).

| Route | Estimated workload |
| :--- | ---: |
| Module content | 350.7 hours |
| Prerequisite track | 56 hours |
| **Full programme** | **406.7 hours (≈ 407 hours)** |
| Core path (P01, essentials of P02–P04, M01–M06) | ≈ 169 hours |
| Core plus deep learning (core path plus M07) | ≈ 194 hours |
| NLP and generative AI specialisation | ≈ 270 hours |
| Vision specialisation | ≈ 243 hours |
| Decision-systems specialisation | ≈ 256 hours |
| Responsible-AI specialisation | ≈ 268 hours |

The full programme is designed for two semesters at roughly 10–15 hours per week. These are
planning estimates, not guaranteed completion times; prior experience and study pace change them
substantially. The prerequisite share assumes 50% of P02–P04 on the core path, a planning
assumption rather than a measurement.

## 7. How to use the course

1. **Begin with the prerequisites.** Take the readiness diagnostic and complete P01–P04 as needed.
2. **Follow the module sequence.** M01–M07 establish the common foundation; M08–M14 build on it.
3. **Study each lesson actively.** Read the objectives, work the examples with the solutions
   covered, and answer the self-check before opening its answer.
4. **Execute its notebook.** Restart and run all cells, then change one parameter and predict the
   effect before running it again.
5. **Complete the associated laboratory.** State the decision, build a baseline, evaluate against
   the stated criteria, and report one failure case.
6. **Attempt the quiz and assignment.** Mark yourself with the provided key or rubric before moving
   on.
7. **Complete the module project and, at the end, the capstone.** The capstone is scoped through a
   proposal and four milestones.
8. **Review the self-assessment.** Revisit the named lessons for any outcome you cannot yet
   demonstrate.

Detailed study routines, weekly schedules and pacing options are in
[learning paths](docs/learning-path.md) and the [FAQ](docs/faq.md).

## 8. Software requirements

**Essential.**

| Tool | Purpose | Notes |
| :--- | :--- | :--- |
| Python 3.11 or newer | Course language | 3.11 or 3.12 is the safest choice; release validation used Python 3.14.7 |
| Jupyter Notebook, JupyterLab or VS Code | Running `.ipynb` practicals | Google Colab or Kaggle also work |
| NumPy, pandas, Matplotlib | Numerical work, data handling and plots | Required from P01 onwards |
| scikit-learn | Classical machine learning and evaluation | Required from M06 |
| PyTorch (CPU build) | Neural networks | Required from M07 |

**Optional or module-specific.**

| Tool | Purpose |
| :--- | :--- |
| Hugging Face `transformers` and `sentence-transformers` | Pretrained-model demonstrations in M08 and M11 |
| Gymnasium | Optional CartPole and FrozenLake benchmarks in M10; bundled environments cover the same labs |
| NetworkX | Optional graph inspection in M14 |
| GPU | Convenience for larger M07/M11 experiments; never required for an exercise or assessment |

Everything runs on a CPU. Most notebooks finish in seconds; the longest take about 1–1.5 minutes
on the release-audit machine. Datasets are included or generated locally, but **internet access is
needed once** for the two M11 notebooks that download small pretrained weights (`distilgpt2` and
`all-MiniLM-L6-v2`); they run offline after the models are cached. Optional M08 pretrained-model
demonstrations may also download weights. No paid API account is required for any lesson, lab,
assignment or project.

## 9. Licensing and attribution

This repository contains four licensing layers. There is **no single repository-wide licence**.

| Material | Licence | Details |
| :--- | :--- | :--- |
| Original source code | **MIT License** | Python, tests, audit scripts and notebook code cells. See [LICENSE](LICENSE). |
| Original educational content | **CC BY 4.0** | Lessons, labs, assignments, quizzes, documentation and notebook prose. Reuse and adaptation, including commercial use, are permitted with attribution and an indication of changes. See [CONTENT-LICENSE.md](CONTENT-LICENSE.md). |
| Original synthetic datasets | **CC0 1.0** | Datasets generated by course code. See [DATASET-LICENSE.md](DATASET-LICENSE.md). |
| Third-party material | **Upstream terms** | Software, external datasets, model weights, papers and quotations are not relicensed here. See [THIRD-PARTY-ATTRIBUTIONS.md](THIRD-PARTY-ATTRIBUTIONS.md). |

Canonical licence references:

- MIT: <https://opensource.org/license/mit>
- CC BY 4.0: <https://creativecommons.org/licenses/by/4.0/>
- CC0 1.0: <https://creativecommons.org/publicdomain/zero/1.0/>

Suggested attribution for reused course material:

> Adapted from *Artificial Intelligence — A Comprehensive Course* by Muhammad Nadeem Majeed
> (University of the Punjab, PUCIT), licensed under CC BY 4.0. Changes: [describe changes]. Source:
> https://github.com/nadeem-majeedch/Artificial-Intelligence-Course

The per-category ownership record is in [LICENSING-INVENTORY.md](LICENSING-INVENTORY.md), and the
citation metadata is in [CITATION.cff](CITATION.cff). Third-party material remains subject to its
own terms; the course's licences do not override them.

## 10. Academic disclaimer

This material is provided for educational purposes. It is not professional, legal, medical or
financial advice, and it does not constitute a legal review of third-party material. Students
should verify external references, datasets, model licences and software requirements before
relying on them. Results in notebooks and laboratories are measurements on the stated data and
environment, not guarantees of performance elsewhere. Third-party resources remain subject to
their own terms.

## 11. Contribution and feedback

Errors found by students and instructors improve the course. Please open an issue on the
[repository issue tracker](https://github.com/nadeem-majeedch/Artificial-Intelligence-Course/issues)
and include:

- the module, lesson or file;
- the exact sentence, result or command;
- what you expected instead and, where relevant, the environment and error output.

For licensing concerns, identify the file and the material in question. Reports are treated as
priority corrections, and content may be removed while a claim is investigated.

---

**Course home:** this page · **Modules:** [modules/README.md](modules/README.md) ·
**Prerequisites:** [prerequisites/README.md](prerequisites/README.md) ·
**Documentation index:** [docs/index.md](docs/index.md) ·
**FAQ:** [docs/faq.md](docs/faq.md)
