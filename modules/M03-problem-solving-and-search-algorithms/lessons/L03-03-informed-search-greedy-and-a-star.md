# L03-03 — Informed Search: Greedy Best-First, A* and Heuristic Design

| Module | M03 · Problem Solving and Search Algorithms |
| :--- | :--- |
| Level | 200 |
| Study time | 100 minutes |
| Prerequisites | [L03-02](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md) · [LP02-02](../../../prerequisites/P02-mathematics-for-ai/lessons/LP02-02-matrix-operations-and-multiplication.md) |
| Notebook | NB-03-01 Search Workbench |

[← Previous: L03-02 Uninformed](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md) · [Next: L03-04 Local Search →](L03-04-local-search-hill-climbing-annealing-genetic.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Implement** greedy best-first and A\* search and explain the difference in one sentence.
- **Design** a heuristic for a grid or puzzle domain and prove it admissible.
- **Distinguish** admissibility from consistency and say what each guarantees.
- **Measure** the effect of heuristic quality on nodes expanded, not just on runtime.

## 2. Prerequisite Knowledge

- BFS, UCS and iterative deepening — [L03-02](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md).
- Euclidean and Manhattan distance — [LP02-01](../../../prerequisites/P02-mathematics-for-ai/lessons/LP02-01-scalars-vectors-matrices-and-tensors.md).

## 3. Conceptual Explanation

### 3.1 The idea: add an estimate of the remaining cost

Uninformed search treats every direction as equally promising. A **heuristic** $h(n)$ estimates
the cost from node $n$ to the goal. Greedy best-first expands the smallest $h$; A\* expands the
smallest $f = g + h$, where $g$ is the cost already paid.

Greedy is fast and can be badly wrong: it follows the heuristic and ignores cost, so it is not
optimal. A\* balances the two and is optimal when $h$ never overestimates.

### 3.2 Admissibility versus consistency

- **Admissible:** $h(n) \le h^*(n)$ for every node — never optimistic by more than reality. This is enough for A\* to be optimal on a tree, with a graph-search caveat.
- **Consistent (monotone):** $h(n) \le c(n, n') + h(n')$ for every edge. This implies admissibility, and it means $f$ never decreases along a path, so A\* never needs to reopen a closed node.

Manhattan distance on a 4-connected grid is consistent, hence admissible. Euclidean distance is
admissible for 8-connected grids but not consistent when diagonal moves cost 1 — a distinction
that shows up as extra re-expansions, not as a wrong answer.

### 3.3 Heuristic quality is measurable

The **effective branching factor** $b^*$ solves $N = 1 + b^* + (b^*)^2 + \cdots + (b^*)^d$ for the
number of nodes expanded $N$. Two heuristics on the same problem can differ by an order of
magnitude in $N$; measuring $b^*$ is how you compare them without arguing.

## 4. Pseudocode

```text
function A_STAR(problem, h):
    frontier <- min-heap by f = g + h, containing root
    best_g <- {root.state: 0}
    while frontier not empty:
        node <- frontier.pop_min()
        if goal(node.state): return node
        for child in expand(node):
            if child.g < best_g.get(child.state, infinity):
                best_g[child.state] <- child.g
                frontier.push(child)
```

## 5. Worked Example — A\* on a grid

Grid, 4-connected, unit costs. Start (0,0), goal (3,0), one wall at (1,1).

| Node | $g$ | $h$ (Manhattan) | $f$ |
| :--- | ---: | ---: | ---: |
| (0,0) | 0 | 3 | 3 |
| (1,0) | 1 | 2 | 3 |
| (2,0) | 2 | 1 | 3 |
| (3,0) | 3 | 0 | 3 |

A\* expands only the four nodes on the shortest path because every node on it has $f = 3$ and
nothing off it has a smaller value. BFS would also expand (0,1), (0,2), (0,3) and their children —
about a dozen nodes for the same answer.

**Worked example with a bad heuristic.** Set $h = 0$: A\* becomes UCS and expands the whole
distance-3 diamond. Set $h = 2 \times$ Manhattan: still finds *a* path, but it may not be the
shortest, because the heuristic now overestimates and can discard the optimal route.

## 6. Mathematical Formulation

$$f(n) = g(n) + h(n), \qquad h(n) \le h^*(n) \;\Rightarrow\; \text{A}^* \text{ is optimal}$$

Node expansion order is by $f$; ties are broken arbitrarily but consistently. With a consistent
heuristic, the first time a state is expanded its $g$ is optimal:

$$h(n) - h(n') \le c(n, n') \;\Rightarrow\; f \text{ is non-decreasing along any path}$$

## 7. Python Implementation

```python
import heapq


def a_star(graph, start, goal, h):
    frontier = [(h(start), 0, start, [start])]
    best = {start: 0}
    expanded = 0
    while frontier:
        f, g, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, g, expanded
        expanded += 1
        for nxt, cost in graph[node]:
            ng = g + cost
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(frontier, (ng + h(nxt), ng, nxt, path + [nxt]))
    return None, None, expanded


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def grid_graph(width=5, height=5, wall={(1, 1)}):
    g = {}
    for x in range(width):
        for y in range(height):
            if (x, y) in wall:
                continue
            g[(x, y)] = [((x + dx, y + dy), 1)
                         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                         if 0 <= x + dx < width and 0 <= y + dy < height
                         and (x + dx, y + dy) not in wall]
    return g


G = grid_graph()
goal = (4, 4)
for name, hfn in (("manhattan", lambda n: manhattan(n, goal)),
                  ("zero (UCS)", lambda n: 0),
                  ("double manhattan", lambda n: 2 * manhattan(n, goal))):
    path, cost, expanded = a_star(G, (0, 0), goal, hfn)
    print(f"{name:16s} cost={cost} nodes={expanded} len={len(path)}")
```

```text
manhattan        cost=8 nodes=9 len=9
zero (UCS)       cost=8 nodes=25 len=9
double manhattan cost=8 nodes=8 len=9
```

The doubled heuristic expands fewer nodes here and still returns cost 8 — this instance does not
punish it. That is the trap: an inadmissible heuristic fails only on the instances where it
matters, which is why admissibility is proved, not sampled.

## 8. Practical Applications

- **Road routing** — A\* with travel-time heuristics is the basis of production routing engines.
- **Puzzle solvers** — Manhattan and linear-conflict heuristics are the standard comparison.
- **Game pathfinding** — A\* on navmeshes; consistency avoids reopening nodes every frame.
- **Planning** — heuristic search over state spaces (FF, LM-cut) uses the same $f = g + h$ frame.

## 9. Common Mistakes

- Using a heuristic that overestimates (e.g., Euclidean distance with unit diagonal costs) and assuming optimality anyway.
- Forgetting to scale the heuristic when edge costs are not unit.
- Comparing heuristics by runtime on one instance rather than by nodes expanded across a sample.
- Reopening closed nodes unnecessarily when the heuristic is consistent.
- Reporting that A\* is "always faster" — with $h = 0$ it is UCS.

## 10. Exercises

1. Prove that Manhattan distance is admissible for the 8-puzzle.
2. Implement greedy best-first and compare its node count with A\* on ten random grids.
3. Construct a grid where doubling the heuristic returns a path that is not shortest.
4. Compute the effective branching factor for both heuristics in §7 and state the ratio.

## 11. Self-Assessment

1. What does admissibility guarantee, and on which kind of graph search?
2. Why does consistency imply admissibility but not the reverse?
3. What happens to A\* if $h$ is negative?
4. Give a domain where greedy best-first is a reasonable production choice.

## 12. Key Terms

**Heuristic**, **admissible**, **consistent**, **$f = g + h$**, **effective branching factor**, **greedy best-first**, **A\***.

## 13. Further Reading

- Hart, Nilsson & Raphael (1968) — the original A\* paper.
- Russell & Norvig, chapter 3, section 3.5–3.6.

## What to Do Next

[L03-04 Local Search](L03-04-local-search-hill-climbing-annealing-genetic.md) drops the path
entirely and asks a different question: which state is best, regardless of how you got there.
