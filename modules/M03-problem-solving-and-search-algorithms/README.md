# M03 — Problem Solving and Search Algorithms

| Level | 200 |
| :--- | :--- |
| Study time | 19.9 hours — guided 10.0 · practical 5.0 · assessment 4.9 · project 0.0 |
| Lessons | 7 |
| Course outcome | CLO2 — formulate a problem as a state space and choose a search strategy with a justification |
| Prerequisites | [P01 Python](../../prerequisites/P01-python-programming/README.md), [P02 Mathematics](../../prerequisites/P02-mathematics-for-ai/README.md) |

[Course home](../../README.md) · [All modules](../README.md) · [Previous module: M02](../M02-intelligent-agents-and-environments/README.md) · [Next module: M04](../M04-knowledge-representation-and-logical-reasoning/README.md)

## Overview

Search is where AI stops being a definition and becomes an algorithm. This module teaches the habit
that decides whether a problem is solvable at all: writing down states, actions, costs and a goal
test *before* choosing a method. You then work through the classical families — uninformed,
informed, local, adversarial and constraint-based — and learn the analysis that separates an
algorithm that finishes from one that does not.

Every algorithm is implemented in Python against one shared interface, so the comparison is
measured rather than asserted: node counts, memory peaks and solution costs on the same problems.

## Learning outcomes

By the end of this module you will be able to:

1. **Formulate** a described problem as a five-tuple state space and justify the abstraction.
2. **Select** BFS, DFS, uniform-cost, iterative deepening or A\* from the problem's structure, with complexity evidence.
3. **Design** a heuristic and prove it admissible or consistent.
4. **Apply** local search where only the final state matters, and diagnose local optima.
5. **Implement** minimax with alpha–beta pruning and measure the pruning gain.
6. **Model** a scheduling problem as a CSP and solve it with propagation.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L03-01 | Problem Formulation and State Spaces | Lesson | 75 m | [Read](lessons/L03-01-problem-formulation-and-state-spaces.md) |
| L03-02 | Uninformed Search: BFS, DFS, UCS, DLS, IDS | Lesson | 100 m | [Read](lessons/L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md) |
| L03-03 | Informed Search: Greedy, A\* and Heuristics | Lesson | 100 m | [Read](lessons/L03-03-informed-search-greedy-and-a-star.md) |
| L03-04 | Local Search: Hill Climbing, Annealing, Genetic | Lesson | 90 m | [Read](lessons/L03-04-local-search-hill-climbing-annealing-genetic.md) |
| L03-05 | Adversarial Search: Minimax and Alpha–Beta | Lesson | 85 m | [Read](lessons/L03-05-adversarial-search-minimax-and-alpha-beta.md) |
| L03-06 | Constraint Satisfaction Problems | Lesson | 90 m | [Read](lessons/L03-06-constraint-satisfaction-problems.md) |
| L03-07 | Choosing and Combining Search Strategies | Lesson | 60 m | [Read](lessons/L03-07-choosing-and-combining-search-strategies.md) |
| NB-03-01 | Search Workbench | Notebook | 60 m | [Open](notebooks/nb-03-01-search-workbench.ipynb) |
| LAB-03-01 | Route Planning Under Real Constraints | Lab | 2 h | [Start](labs/lab-03-01-route-planning-under-constraints.md) |
| LAB-03-02 | A Game Agent and a Timetable Solver | Lab | 2.5 h | [Start](labs/lab-03-02-game-agent-and-timetable-solver.md) |
| QUIZ-03 | Module self-check | Quiz | 40 m | [Take](../../assessments/quizzes/quiz-m03.md) |
| PA-02 | Search Algorithms | Assignment | 4 h | [Start](../../assessments/programming/pa-02-search-algorithms.md) |

Supporting code: [`code/search_algorithms.py`](code/search_algorithms.py) — every algorithm in the
module, standard library only, used by the notebook and both labs.

## Before you start

You need Python functions and loops, and you should be comfortable with the idea of a cost. Refresh
with [LP01-04](../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md)
and [LP02-02](../../prerequisites/P02-mathematics-for-ai/lessons/LP02-02-matrix-operations-and-multiplication.md).

**Readiness self-check.** If you cannot answer three of these, spend an hour in P01 first:

1. Can you write a function that takes a graph as a dictionary and returns a list?
2. Can you explain what a stack and a queue are, and which one DFS uses?
3. Can you compute $3^4$ and say why $b^d$ matters for search?
4. Can you read a traceback and find the line that failed?

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L03-01, start NB-03-01 | 2.5 h |
| 2 | L03-02, finish NB-03-01 | 3 h |
| 3 | L03-03, LAB-03-01 tasks 1–3 | 3 h |
| 4 | LAB-03-01 complete | 2 h |
| 5 | L03-04, L03-05 | 3 h |
| 6 | L03-06, L03-07 | 2.5 h |
| 7 | LAB-03-02, QUIZ-03 | 3 h |

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-03-01 | Correct search implementations, admissibility argument, communication | 30% |
| LAB-03-02 | CSP model, pruning measurement, recommendation | 30% |
| QUIZ-03 | Complexity, optimality, heuristic reasoning | 20% |
| PA-02 | Independent implementation with benchmarks | 20% |

## Key terms introduced

**State space**, **branching factor**, **frontier**, **completeness**, **optimality**, **admissible
heuristic**, **consistency**, **local optimum**, **alpha–beta pruning**, **CSP**, **arc consistency**.
All are defined in the [glossary](../../resources/glossary/classical-ai.md).

## Resources

- [AIMA chapter 3](https://aima.cs.berkeley.edu/) — the standard treatment of search.
- [`code/search_algorithms.py`](code/search_algorithms.py) — read `astar` before writing your own.
- [Concept map: search algorithms](../../docs/CONCEPT-MAPS.md#3-search-algorithms) — the family tree.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) ·
[Previous module: M02](../M02-intelligent-agents-and-environments/README.md) ·
[Next module: M04 Knowledge Representation →](../M04-knowledge-representation-and-logical-reasoning/README.md)
