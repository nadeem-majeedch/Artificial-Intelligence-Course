# M01 — Introduction and Foundations of Artificial Intelligence

| Level | 100 |
| :--- | :--- |
| Study time | 10 hours |
| Lessons | 5 |
| Course outcome | CLO1 — explain what AI is, how the field evolved, and how agents act in an environment |
| Prerequisites | None (P01 recommended if you have never programmed) |

[Course home](../../README.md) · [All modules](../README.md) · [Next module: M02 Intelligent Agents →](../M02-intelligent-agents-and-environments/README.md)

## Overview

This module gives you an accurate mental model of the field before you write an algorithm. It
separates the three meanings of "AI" that beginners conflate — a goal, a set of techniques, and a
marketing label — and traces how the ideas developed from symbolic reasoning through the statistical
turn to today's generative systems. It also establishes the working habits the rest of the course
depends on: how to read a lesson, when to run code, and how to check yourself.

By the end you will be able to describe any AI system by its mechanism, classify its environment and
its limitations, and audit a capability claim rather than repeat it.

## Learning outcomes

By the end of this module you will be able to:

1. **Define** AI precisely enough to argue about a specific system, and separate narrow/general from
   weak/strong without conflating the two axes.
2. **Explain** the two AI winters as consequences of an expectation–capability gap, and name the
   mechanism behind each.
3. **Classify** a system as symbolic, learned or hybrid, and place AI, machine learning and deep
   learning correctly in a containment diagram.
4. **Audit** a capability claim: task family, dataset, metric, base rate, tail behaviour and feedback
   loop, with unknown fields marked as unknown.
5. **Compute** the operational consequences of an error rate, the calibration of a confidence score,
   and the compounded failure probability of a multi-step plan.

## Before you start

You need no AI background, but you do need to be able to read and modify a short Python program.

- **Run Python and a notebook** — [LP01-01](../../prerequisites/P01-python-programming/lessons/LP01-01-setting-up-python-and-jupyter.md)
- **Use variables, loops and functions** — [LP01-04](../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md)
- **Read a formatted print and a list comprehension** — [LP01-03](../../prerequisites/P01-python-programming/lessons/LP01-03-conditionals-loops-and-comprehensions.md)

**Readiness self-check.** If you cannot answer three of these, spend an hour in P01 first:

1. Can you run a Python file and a notebook cell on your own machine?
2. Can you write a function that takes a list and returns a filtered list?
3. Can you explain what a variable name refers to in Python?
4. Can you read a traceback and find the line that failed?

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L01-01 | What Is Artificial Intelligence? Definitions, Goals and Myths | Lesson | 60 m | [Read](lessons/L01-01-what-is-artificial-intelligence.md) |
| L01-02 | A Brief History of AI and the AI Winters | Lesson | 60 m | [Read](lessons/L01-02-history-and-ai-winters.md) |
| L01-03 | The Many Faces of AI: Symbolic, Statistical and Generative | Lesson | 60 m | [Read](lessons/L01-03-symbolic-statistical-generative.md) |
| L01-04 | What AI Can and Cannot Do Today | Lesson | 50 m | [Read](lessons/L01-04-ai-capabilities-and-limitations.md) |
| L01-05 | How This Course Works: Tools, Workflow and Study Habits | Lesson | 40 m | [Read](lessons/L01-05-course-workflow-and-study-habits.md) |
| NB-01-01 | Capability Test Bench | Notebook | 60 m | [Open](notebooks/nb-01-01-capability-test-bench.ipynb) |
| LAB-01-01 | Claim Audit: Does the Enquiry Assistant Really Work? | Lab | 60 m | [Start](labs/lab-01-01-claim-audit.md) |
| LAB-01-02 | Build a Turing-Test-Style Conversational System | Lab | 60 m | [Start](labs/lab-01-02-turing-test-conversation.md) |
| QUIZ-01 | Module self-check | Quiz | 30 m | [Take](quizzes/quiz-01.md) |
| MP-01 | AI-in-Your-Field Use-Case Audit | Mini-project | 2 h | [Start](projects/mp-01-ai-in-your-field-audit.md) |

Total: 4.5 h lessons + 1 h notebook + 2 h labs + 0.5 h quiz + 2 h mini-project = **10 hours**.

Supporting code: [`code/capability_check.py`](code/capability_check.py) (capability scoring) and
[`code/eliza_lite.py`](code/eliza_lite.py) (the conversational system used in LAB-01-02). Both are
standard-library only and run from the command line.

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L01-01, L01-02 | 2 h |
| 2 | L01-03, start NB-01-01 | 2 h |
| 3 | Finish NB-01-01, LAB-01-01 | 2 h |
| 4 | L01-04 | 1 h |
| 5 | LAB-01-02 | 1 h |
| 6 | L01-05, QUIZ-01 | 1 h |
| 7 | MP-01 | 1 h |

If you have only four days, keep the lab and notebook days and merge the reading. Never drop the
labs to save time: they are where the definitions become usable.

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-01-01 | Evidence discipline: baseline, per-class metrics, calibration, error cost | 25% |
| LAB-01-02 | Fair protocol, reproducibility, honest limits of a behavioural test | 25% |
| QUIZ-01 | Conceptual grasp of definitions, history and limits | 20% |
| MP-01 | Independent judgement on a real system in your field | 30% |

Each artefact carries its own rubric. The six assessment dimensions are described in the
[curriculum map](../../docs/CURRICULUM-MAP.md#8-assessment-model).

## Key terms introduced

**Artificial intelligence**, **narrow AI**, **general AI**, **superintelligence**, **weak AI**,
**strong AI**, **Turing Test**, **AI winter**, **symbolic AI**, **connectionist AI**, **expert
system**, **knowledge acquisition bottleneck**, **combinatorial explosion**, **inductive bias**,
**calibration**, **distribution shift**, **precision**, **recall**, **base rate**.

All are defined in the [glossary](../../resources/glossary.md). The module's one-page recap is in
[summary.md](summary.md).

## Resources

- [AIMA chapter 1](https://aima.cs.berkeley.edu/) — the standard definition and compressed history; the
  best single chapter to read alongside L01-01 and L01-02.
- [`code/eliza_lite.py`](code/eliza_lite.py) — read the rule list before LAB-01-02; it is short enough to
  understand completely, which is the point.
- [Glossary](../../resources/glossary.md) — check unknown terms here before continuing; the module uses
  precise vocabulary deliberately.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) ·
[Prerequisites](../../prerequisites/README.md) ·
[Next module: M02 Intelligent Agents →](../M02-intelligent-agents-and-environments/README.md)
