# QUIZ-M03 — Solutions and Explanations

> **Availability.** M03 (Problem Solving and Search) is not published in this repository yet. This paper is
> included so the assessment set is complete; it cannot be attempted until the module's
> lessons and labs are available.

[Quiz](quiz-m03.md) · [Assessment index](../README.md)

---

## Part A

**Q3.1 — B.** BFS keeps every generated node in the frontier, so memory is exponential in depth:
$O(b^d)$. Time is also $O(b^d)$; $O(bd)$ is the path length, not the frontier. Option D is the
complexity of a balanced-tree operation, not of search.

**Q3.2 — A.** Admissible means never overestimating the true remaining cost: $h(n) \le h^*(n)$ for
all $n$. Option B describes a heuristic that is optimistic in the wrong direction (an
overestimate), which can make A\* miss the optimal path. Option C is stronger than admissibility
and implies it, not the reverse.

**Q3.3 — B.** Alpha–beta returns exactly the minimax value; it only skips branches that cannot
affect it. If your pruned search returns a different value, there is a bug in the bounds.

## Part B

**Q3.4 — False.** Admissibility alone guarantees optimality for *tree* search. Under graph search,
an inconsistent heuristic can close a node reached by a suboptimal path; without reopening, the
optimal path may be discarded. Consistency (monotonicity) is the condition that makes graph-search
A\* optimal without reopening.

## Part C

**Q3.5 — Model answer.** Admissibility is a global bound: $h(n)$ never exceeds the true cost to the
goal. Consistency is a local condition: $h(n) \le c(n,n') + h(n')$ for every edge, which implies
admissibility. Tree-search A\* needs admissibility; graph-search A\* needs consistency, or
reopening of closed nodes.

**Q3.6 — Model answer.** Hill climbing keeps only the current state and moves to a better
neighbour, so it can stop at a local maximum and never backtrack. BFS keeps a frontier of
alternatives and is therefore complete. The memory saving is exactly what removes the ability to
escape a local optimum.

## Part D

**Q3.7 —** Total nodes in a complete binary tree of depth 3: $1 + 2 + 4 + 8 = 15$. Worst-case
expansions before reaching a goal at depth 3: 15 (all nodes at depths 0–2 must be expanded, and in
the worst case every depth-3 node is generated but only the goal is recognised on generation).
Award the mark for 15 with either interpretation clearly stated.

**Q3.8 —** Both have $f = 5$. A tie; A\* may expand either. The tie shows the heuristic is
uninformative between these two nodes — and in the worst case an uninformative heuristic degrades
A\* to uniform-cost search. (1 mark for identifying the tie, 1 for expanding either with the
reason, 1 for the consequence.)

## Part E

**Q3.9 —** Minimax: left MIN = min(3,5) = 3; right MIN = min(6,9) = 6; root MAX = 6.

Alpha–beta, left to right: root starts $\alpha=-\infty$. Left subtree evaluates 3, then 5, giving 3;
root $\alpha=3$. Right subtree: first leaf 6 $\ge \alpha=3$, so the MIN node can never fall below
3 and cannot improve the root — the remaining leaf 9 is pruned. Leaves evaluated: **3**
(3, 5, 6). Value returned: 6, unchanged.

## Part F

**Q3.10 —** `1 [2, 3]`

`deque([1])` starts with one element; two appends add 2 and 3 at the right; `popleft()` returns 1
and removes it, leaving `[2, 3]`. The list is printed after the pop because arguments are evaluated
left to right before `print` runs.

## Part G

**Q3.11 — Model answer.** Any problem with non-uniform step costs: a road network with different
travel times, or a planner where actions have different prices. BFS minimises the *number* of
steps, so it can return a five-step path that costs more than a two-step path. UCS expands by
cumulative cost and returns the cheapest.

**Q3.12 — Model answer.** True when the heuristic is admissible and informative: A\* with a good
$h$ expands fewer nodes than Dijkstra, which is A\* with $h=0$. False when the heuristic is weak or
misleading — with $h \equiv 0$ the two algorithms are identical, and with a badly scaled but still
admissible $h$ the overhead of computing it can make A\* slower in wall-clock terms despite fewer
expansions.

---

[Quiz](quiz-m03.md) · [Previous solutions](quiz-m02.md) · [Assessment index](../README.md)
