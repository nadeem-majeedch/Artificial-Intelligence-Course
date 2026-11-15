# L03-07 — Choosing and Combining Search Strategies

| Module | M03 · Problem Solving and Search Algorithms |
| :--- | :--- |
| Level | 300 |
| Study time | 60 minutes |
| Prerequisites | L03-01 … L03-06 |
| Notebook | NB-03-01 Search Workbench |

[← Previous: L03-06 Constraints](L03-06-constraint-satisfaction-problems.md) · [Module home](../README.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Select** a search strategy from the structure of a problem, with a stated justification.
- **Combine** techniques: heuristic search inside a CSP, local search over a heuristic's weights, pruning inside a game tree.
- **Recognise** the four situations where search is the wrong tool.
- **Estimate** cost before implementation, and abandon an approach on evidence.

## 2. Prerequisite Knowledge

All six preceding lessons. If any complexity table is not familiar, revisit
[L03-02](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md) §3.1 before continuing.

## 3. Conceptual Explanation

### 3.1 A decision procedure

Ask these questions in order:

1. **Is the path part of the answer?** If yes, use graph search (L03-02, L03-03). If only the final
   configuration matters, use local search (L03-04) or a CSP (L03-06).
2. **Is there an adversary?** Then minimax with pruning (L03-05), not single-agent search.
3. **Are costs uniform?** Uniform → BFS or IDS. Non-uniform → UCS or A\*.
4. **Is a good heuristic available?** If yes, A\*; if no, IDS is the safe default.
5. **Is memory the constraint?** IDS or DFS with a depth limit; never BFS.
6. **Are there hard constraints on the answer?** Model it as a CSP and let propagation work.

### 3.2 Combination is normal

Production systems mix these: a route planner uses A\* over a graph whose edge costs come from a
learned model; a scheduler uses a CSP with local search to repair violated soft constraints; a game
engine uses alpha–beta with a neural evaluation function. The exam question "which algorithm?" is a
teaching simplification; the engineering question is "which decomposition?".

### 3.3 When not to search

- The answer is computable directly (shortest path on a DAG, sorting, dynamic programming with
  optimal substructure).
- The state space is continuous and differentiable — use gradient-based optimisation.
- The objective is unknown until execution — use online learning or bandits (M10).
- The problem is actually a data problem — a learned model beats hand-written search rules (M06).

## 4. Pseudocode

```text
CHOOSE(problem):
    if problem.has_adversary:        return ALPHA_BETA_WITH_EVALUATION
    if problem.is_assignment:        return BACKTRACKING_WITH_PROPAGATION
    if problem.costs_uniform:        return ITERATIVE_DEEPENING
    if problem.has_admissible_h:     return A_STAR
    return UNIFORM_COST_SEARCH
```

## 5. Worked Example — three problems, three answers

| Problem | Structure | Choice | Why |
| :--- | :--- | :--- | :--- |
| Delivery routing, 5,000 intersections | Graph, non-uniform costs, heuristic available | A\* with travel-time lower bound | Optimal, expands a fraction of the graph |
| Exam timetabling, 400 exams | Assignment with hard conflicts | CSP + local search repair | No path; constraints dominate |
| Connect Four | Adversarial, perfect information | Alpha–beta, depth 8, evaluation | Opponent chooses; pruning makes depth feasible |

## 6. Mathematical Formulation

Expected nodes before a solution, for A\* with heuristic error $\epsilon$ uniformly bounded:

$$N \le b^{\,\epsilon d}\, N_{\text{exact}}$$

An admissible but weak heuristic degrades gracefully toward UCS; an inadmissible one can lose
optimality entirely. This is the quantitative version of "a heuristic is a promise".

## 7. Python Implementation

```python
from .search_algorithms import astar, bfs, ids, backtracking_csp  # see module code

def choose(problem):
    if problem.get("adversary"):
        return "alpha-beta with evaluation function"
    if problem.get("constraints"):
        return "backtracking CSP with forward checking"
    if problem.get("uniform_cost"):
        return "iterative deepening"
    if problem.get("heuristic"):
        return "A*"
    return "uniform-cost search"
```

The module's `search_algorithms.py` contains the implementations these strategies refer to; the
notebook runs each on the same graph so their node counts can be compared directly.

## 8. Practical Applications

- **Logistics** — A\* for routing, CSP for loading constraints, local search for schedule repair.
- **Game AI** — alpha–beta at shallow depth plus a learned evaluator.
- **Compilers** — shortest-path instruction selection, CSP-style register allocation.
- **Resource planning** — constraint solvers over shifts, with soft preferences.

## 9. Common Mistakes

- Choosing A\* with a heuristic that is not admissible and calling the result optimal.
- Using local search for a problem whose constraints are hard and non-negotiable.
- Implementing BFS on a graph with 10 million nodes and running out of memory at depth 4.
- Treating a CSP as a sequence-search problem and losing the commutativity gain.
- Benchmarking on one instance and generalising.

## 10. Exercises

1. Take three problems from your own domain and run the decision procedure, writing the answer and the reason.
2. Build a table of node counts for BFS, IDS and A\* on one grid, and compute each algorithm's memory peak.
3. Find a problem where local search beats A\* and explain the structural reason.
4. Write the one-paragraph justification you would give a reviewer for your choice in exercise 1.

## 11. Self-Assessment

1. Name the two questions that eliminate most algorithms immediately.
2. Why is IDS the safe default when no heuristic exists?
3. What does an inadmissible heuristic cost you?
4. When is a CSP formulation strictly better than state-space search?

## 12. Key Terms

**Strategy selection**, **decomposition**, **admissible heuristic**, **propagation**, **memory bound**, **hybrid system**.

## 13. Further Reading

- Russell & Norvig, chapter 3 summary and chapter 6.
- Likhachev, Gordon & Thrun (2003), "ARA\*" — anytime search when the budget is uncertain.

## What to Do Next

Work the [notebook](../notebooks/nb-03-01-search-workbench.ipynb) and then
[LAB-03-01](../labs/lab-03-01-route-planning-under-constraints.md), which applies this decision
procedure to a real routing scenario.
