# QUIZ-M03 — Problem Solving and Search Algorithms

| | |
| :--- | :--- |
| Module | M03 · Problem Solving and Search Algorithms |
| Questions | 12 (20 marks) |
| Time | 40 minutes |
| Covers | L03-01 … L03-07 |
| Pass mark | 12 / 20 |

> **Availability.** This module's lessons, notebook and lab are published in this repository; sit this paper after finishing them.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m03.md) · [Module](../../modules/README.md#m03)

Closed book, calculator allowed. Part E requires drawing the tree.

---

## Part A — Multiple choice (3 marks)

**Q3.1** Breadth-first search is complete and optimal for unit step costs, but its memory use is

- A. $O(bd)$
- B. $O(b^d)$
- C. $O(d)$
- D. $O(b \log d)$

**Q3.2** A heuristic $h$ is admissible when

- A. $h(n) \le h^*(n)$ for every node
- B. $h(n) \ge h^*(n)$ for every node
- C. $h$ is consistent
- D. $h(\text{goal}) = 0$ only

**Q3.3** Alpha–beta pruning can change

- A. the value returned by minimax
- B. the number of nodes examined, not the value
- C. the branching factor of the game
- D. the depth of the tree

## Part B — True or false, with a reason (2 marks)

**Q3.4** "A\* with an admissible but inconsistent heuristic is optimal under graph search without
reopening closed nodes."

## Part C — Conceptual (4 marks)

**Q3.5** (2 marks) Explain the difference between admissibility and consistency, and which one is
required for tree-search A\* optimality.

**Q3.6** (2 marks) Why can hill climbing fail on a problem where breadth-first search succeeds,
even though hill climbing uses less memory?

## Part D — Numerical (6 marks)

**Q3.7** (3 marks) A tree has branching factor 2 and uniform depth 3 (root at depth 0). How many
nodes are generated in total (including the root)? How many does breadth-first search expand
before reaching a goal at depth 3 in the worst case?

**Q3.8** (3 marks) Two frontier nodes have $f = g + h$: node A with $g = 3$, $h = 2$; node B with
$g = 1$, $h = 4$. Which does A\* expand first, and what does the tie tell you about the heuristic?

## Part E — Tracing (3 marks)

**Q3.9** A root MAX node has two MIN children. The leaves, left to right, are
`3, 5` under the first MIN and `6, 9` under the second. Trace minimax, then alpha–beta with
left-to-right order, and report how many leaves are evaluated under pruning.

## Part F — Python output (2 marks)

**Q3.10** What does this print?

```python
from collections import deque

q = deque([1])
q.append(2)
q.append(3)
print(q.popleft(), list(q))
```

## Part G — Short answer (4 marks)

**Q3.11** (2 marks) Give one problem where uniform-cost search is necessary and breadth-first
search is wrong, and say why.

**Q3.12** (2 marks) A colleague claims "A\* is always faster than Dijkstra". State the condition
under which that is true and the case where it is false.

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m03.md) · [Next quiz](quiz-m04.md)
