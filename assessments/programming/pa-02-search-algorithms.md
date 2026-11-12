# PA-02 — Search Algorithms on a Real Grid

| | |
| :--- | :--- |
| Assignment | 02 |
| Difficulty | Intermediate |
| Estimated time | 4 hours |
| Prerequisites | M03 (L03-01 … L03-06), P01 |
| Covers | BFS, DFS, IDDFS, UCS, A\*, heuristics, measured comparisons |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

Warehouse robots move on a grid with obstacles and variable floor friction: some cells cost 1 to
enter, others 3. Breadth-first search finds the fewest *steps*, which is not the cheapest route.
The assignment is to implement four algorithms on the same problem and report what each one
actually costs in nodes expanded, path cost and wall-clock time.

## Problem scenario

A 40×40 grid map is provided as text (`#` wall, `.` floor cost 1, `~` floor cost 3, `S` start,
`G` goal). You must return a path and the numbers that justify the algorithm choice.

## Learning outcomes

1. Formulate a grid problem as states, actions, costs and a goal test.
2. Implement BFS, UCS and A\* with a consistent interface.
3. Design an admissible heuristic and prove it is admissible for this cost model.
4. Compare algorithms on measured metrics rather than on asymptotic claims alone.

## Tasks

1. **Model.** Define the state, successors and step costs; document them in the README.
2. **Implement.** BFS, DFS with a depth limit, iterative deepening, UCS, and A\* with Manhattan
   distance scaled by the minimum cell cost.
3. **Verify optimality.** For 20 random maps, check that UCS and A\* return the same path cost.
4. **Measure.** For each algorithm and map: nodes expanded, frontier size, path cost, runtime.
   Tabulate means and ranges.
5. **Stress.** Run on a map with no path; every algorithm must terminate and say so.
6. **Heuristic study.** Compare A\* with Manhattan distance against A\* with $h=0$ (which is UCS)
   and against an inadmissible heuristic ($2\times$ Manhattan). Report the cost of inadmissibility.

## Constraints

- Standard library plus NumPy; no search libraries.
- Deterministic tie-breaking (document the order).
- A\* must not reopen nodes unless you justify it.

## Expected deliverables

`search.py`, `maps/` (at least 5 maps including one unsolvable), `results.md` with the tables, and a
README stating the heuristic's admissibility argument.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Correctness | 30% | all algorithms solve the maps; UCS and A\* agree on cost |
| Heuristic argument | 20% | admissibility proved for this cost model |
| Measurement | 25% | nodes, frontier, time reported for each |
| Robustness | 15% | unsolvable maps, tie-breaking, no crashes |
| Documentation | 10% | model and interface documented |

## Bonus challenges

- Add weighted A\* ($f=g+w\cdot h$) and plot cost against nodes expanded for several $w$.
- Implement a bidirectional search and compare its frontier size with UCS.

---

[Assessment index](../README.md) · [PA-01](pa-01-python-and-numpy.md) · [PA-03](pa-03-intelligent-agents.md)
