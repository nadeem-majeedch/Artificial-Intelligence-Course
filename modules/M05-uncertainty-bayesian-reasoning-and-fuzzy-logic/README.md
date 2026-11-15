# M05 — Uncertainty, Bayesian Reasoning and Fuzzy Logic

| Level | 300 |
| :--- | :--- |
| Study time | 20.6 hours — guided 8.8 · practical 7.0 · assessment 4.8 · project 0.0 |
| Lessons | 6 |
| Course outcome | CLO6 — reason and decide under uncertainty, using probability or fuzzy logic as appropriate |
| Prerequisites | [P03 Probability and Statistics](../../prerequisites/P03-probability-and-statistics/README.md), [M04](../M04-knowledge-representation-and-logical-reasoning/README.md) |

[← Previous module: M04](../M04-knowledge-representation-and-logical-reasoning/README.md) · [Course home](../../README.md) · [All modules](../README.md) · [Next module: M06](../M06-machine-learning-fundamentals/README.md)

## Overview

Logic handles what is certainly true. Real problems are rarely certain in either sense: the outcome
may be random (will it rain?), or the category may be vague (is this email aggressive?). This module
treats both, and keeps them apart. Probability and Bayesian networks handle randomness; fuzzy sets
handle vagueness. Confusing the two is the most common conceptual error in the module.

Everything is computed by hand first and then in Python, so the numbers in the lessons can be
reproduced exactly.

## Learning outcomes

1. **Apply** Bayes' theorem and explain why the base rate dominates rare-event evidence.
2. **Build** a Bayesian network, read independence from the graph, and compute a posterior by enumeration.
3. **Implement** naive Bayes with smoothing and evaluate it beyond accuracy.
4. **Model** a linguistic variable with membership functions and justify the operators chosen.
5. **Design** a Mamdani or Sugeno controller and defuzzify it defensibly.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L05-01 | Probability, Conditional Probability and Bayes' Theorem | Lesson | 85 m | [Read](lessons/L05-01-probability-conditional-probability-and-bayes-theorem.md) |
| L05-02 | Bayesian Networks, Conditional Independence and Inference | Lesson | 100 m | [Read](lessons/L05-02-bayesian-networks-independence-and-inference.md) |
| L05-03 | Naive Bayes and Text Classification | Lesson | 80 m | [Read](lessons/L05-03-naive-bayes-and-text-classification.md) |
| L05-04 | Fuzzy Sets, Membership Functions and Fuzzy Operations | Lesson | 80 m | [Read](lessons/L05-04-fuzzy-sets-membership-functions-and-operations.md) |
| L05-05 | Fuzzy Inference: Mamdani, Sugeno and Defuzzification | Lesson | 90 m | [Read](lessons/L05-05-fuzzy-inference-mamdani-sugeno-and-defuzzification.md) |
| L05-06 | Variable Elimination and Factor Algebra | Lesson | 95 m | [Read](lessons/L05-06-variable-elimination-and-factor-algebra.md) |
| NB-05-01 | Uncertainty Workbench | Notebook | 60 m | [Open](notebooks/nb-05-01-uncertainty-workbench.ipynb) |
| NB-05-02 | Variable Elimination | Notebook | 60 m | [Open](notebooks/nb-05-02-variable-elimination.ipynb) |
| LAB-05-01 | A Bayesian and Fuzzy Decision System | Lab | 3 h | [Start](labs/lab-05-01-bayesian-and-fuzzy-decision-system.md) |
| LAB-05-02 | Bayesian Network Inference and Intelligent Diagnosis | Lab | 3 h | [Start](labs/lab-05-02-bayesian-network-inference-and-diagnosis.md) |
| QUIZ-05 | Module self-check | Quiz | 25 m | [Take](../../assessments/quizzes/quiz-m05.md) |

## Reference code

| File | What it contains |
| :--- | :--- |
| [`alarm_network.py`](code/alarm_network.py) | Alarm network, full CPTs, enumeration and self-tests |
| [`variable_elimination.py`](code/variable_elimination.py) | Generic factors, VE with configurable ordering, cross-checks against enumeration and brute force |

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L05-01, NB-05-01 cells 1–4 | 2.5 h |
| 2 | L05-02, finish NB-05-01 | 3 h |
| 3 | L05-03, start LAB-05-01 | 2.5 h |
| 4 | L05-04, L05-05 | 3 h |
| 5 | L05-06, NB-05-02 | 2.5 h |
| 6 | Finish LAB-05-01 | 1.5 h |

## Assessment for this module

| Component | Weight |
| :--- | ---: |
| LAB-05-01 (Bayesian and fuzzy components, evaluation, explanation) | 60% |
| QUIZ-05 | 25% |
| Notebook exercises | 15% |

## Key terms

**Prior**, **likelihood**, **posterior**, **conditional independence**, **collapsing**, **fuzzy
set**, **membership function**, **defuzzification**. Definitions:
[glossary](../../resources/glossary.md).

## Navigation

[← Previous: M04](../M04-knowledge-representation-and-logical-reasoning/README.md) · [Course home](../../README.md) ·
[Next module: M06 →](../M06-machine-learning-fundamentals/README.md)

## Assignment

[PA-05 — Bayesian Diagnosis with a Small Network](../../assessments/programming/pa-05-bayesian-reasoning.md)
