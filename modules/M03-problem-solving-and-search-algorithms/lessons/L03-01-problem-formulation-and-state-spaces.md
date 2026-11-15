# L03-01 — Problem Formulation and State-Space Representation

| Module | M03 · Problem Solving and Search Algorithms |
| :--- | :--- |
| Level | 200 |
| Study time | 75 minutes |
| Prerequisites | [LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md) · [LP02-01](../../../prerequisites/P02-mathematics-for-ai/lessons/LP02-01-scalars-vectors-matrices-and-tensors.md) |
| Notebook | NB-03-01 Search Workbench |

[← Module start](../README.md) · [Next: L03-02 Uninformed Search →](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Formulate** a described problem as a state space: initial state, actions, transition function, goal test and path cost.
- **Distinguish** a state from a node, and explain why the distinction prevents two classic bugs.
- **Estimate** the size of a search space from branching factor and depth, and use the estimate to rule out an approach before coding it.
- **Draw** the search tree for a small problem by hand.

## 2. Prerequisite Knowledge

- Python functions, lists, tuples and dictionaries — [LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md).
- Sets and the idea of a tuple as an immutable key — [LP01-05](../../../prerequisites/P01-python-programming/lessons/LP01-05-objects-modules-exceptions-and-files.md).
- No AI background is assumed.

## 3. Conceptual Explanation

### 3.1 Why formulation decides the outcome

Every search algorithm in this module takes the *same* input: a state space. The algorithm is
rarely the hard part. What decides whether a problem is solvable in seconds or not at all is the
representation — which objects are states, which details are abstracted away, and how large the
resulting space is.

A delivery-routing problem can be modelled with states as *street intersections* (a few thousand
states) or as *every position to the metre* (effectively infinite). The first is solvable; the
second is not. Both are "the same problem" until you write the state down.

### 3.2 The five components

| Component | Question it answers | Robot vacuum example |
| :--- | :--- | :--- |
| Initial state | Where does the agent start? | Position (0,0), no dirt collected |
| Actions | What can it do? | Up, down, left, right, suck |
| Transition model | What does an action do? | Moving changes position; walls block |
| Goal test | Is this a goal? | All rooms clean |
| Path cost | How expensive is a solution? | One per move, three per suck |

A **state** is a configuration of the world. A **node** is a bookkeeping record: a state plus the
parent that reached it, the action taken, and the cost so far. Two different paths can reach the
same state; the state is the same, the nodes are not. Mixing them up causes infinite loops (you
revisit states forever) or lost paths (you cannot reconstruct the route).

### 3.3 Abstraction is a promise you have to keep

Removing detail is what makes search possible, but every abstraction makes a promise: *the removed
detail does not change the answer*. Ignoring traffic makes routing tractable and makes the answer
wrong at 8 a.m. Good formulation states the promise explicitly so it can be tested.

### 3.4 Measuring the space before you search it

Two numbers decide feasibility:

- **Branching factor** $b$: how many actions are available on average.
- **Solution depth** $d$: how many steps a solution takes.

A binary tree of depth 20 has about a million nodes; depth 40 has a trillion. This is why the
choice of algorithm in L03-02 matters more than the choice of language or hardware.

## 4. Pseudocode

```text
function SEARCH(problem, strategy):
    frontier <- {make_node(problem.initial_state)}
    explored <- {}
    loop:
        if frontier is empty: return failure
        node <- strategy.remove_choice(frontier)
        if problem.goal_test(node.state): return solution(node)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child <- make_node(problem.result(node.state, action), parent=node)
            if child.state not in explored and child.state not in frontier:
                frontier.add(child)
```

Every algorithm in this module is this loop with a different `remove_choice`.

## 5. Worked Example — the 8-puzzle

The 8-puzzle has a 3×3 board with one blank. States are permutations of nine tiles; actions slide a
tile into the blank.

- **States:** $9! = 362{,}880$ arrangements, of which half are reachable from a given start.
- **Branching factor:** 2 (corner blank), 3 (edge), 4 (centre); average ≈ 3.
- **Typical solution depth:** about 22 moves.

So a breadth-first search may expand on the order of $3^{22} \approx 3\times10^{10}$ nodes. That
number, not the code, is why the 8-puzzle chapter exists: the same problem is trivial with a good
heuristic (L03-03) and hopeless without one.

**Worked trace.** Start `[[1,2,3],[4,0,5],[6,7,8]]`, goal `[[1,2,3],[4,5,6],[7,8,0]]`.

| Step | Node state (blank position) | Action | $g$ |
| ---: | :--- | :--- | ---: |
| 0 | `1 2 3 / 4 0 5 / 6 7 8` (centre) | — | 0 |
| 1 | `1 2 3 / 4 5 0 / 6 7 8` (middle right) | slide 5 right | 1 |
| 2 | `1 2 3 / 4 5 6 / 6 7 8`? | invalid: two 6s | — |

The second row shows the most common formulation bug: the transition function must move the blank,
not overwrite a tile. A correct implementation moves the blank and swaps.

## 6. Mathematical Formulation

A search problem is a five-tuple:

$$\mathcal{P} = \langle S,\ s_0,\ A,\ T,\ G,\ c \rangle$$

with $T: S \times A \to S$ the transition function, $G \subseteq S$ the goal set, and
$c: S \times A \times S \to \mathbb{R}_{\ge 0}$ the step cost. A solution is a path
$s_0 \xrightarrow{a_1} s_1 \cdots \xrightarrow{a_k} s_k$ with $s_k \in G$, and its cost is
$\sum_i c(s_{i-1}, a_i, s_i)$.

The size of the reachable space is bounded by $b^{d+1}$ for uniform branching; the exact count
matters when it is small, and the bound is what matters when it is large.

## 7. Python Implementation

```python
from dataclasses import dataclass, field
from typing import Callable, Hashable


@dataclass(frozen=True)
class Puzzle:
    """8-puzzle state: a tuple of nine ints, 0 is the blank."""
    tiles: tuple

    def blank(self):
        return self.tiles.index(0)

    def neighbours(self):
        i = self.blank()
        r, c = divmod(i, 3)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                j = nr * 3 + nc
                t = list(self.tiles)
                t[i], t[j] = t[j], t[i]
                yield Puzzle(tuple(t)), f"slide {t[i]}"


START = Puzzle((1, 2, 3, 4, 0, 5, 6, 7, 8))
for child, action in list(START.neighbours())[:2]:
    print(action, "->", child.tiles)
```

```text
slide 4 -> (1, 2, 3, 0, 4, 5, 6, 7, 8)
slide 2 -> (1, 0, 3, 4, 2, 5, 6, 7, 8)
```

**Why `frozen=True` matters.** Hashable states can go in a `set`, which is the only cheap way to
enforce the "explored" rule. A mutable dataclass silently breaks deduplication.

## 8. Practical Applications

- **Route planning** — states are intersections, cost is travel time, abstraction drops lane-level detail.
- **Packing and scheduling** — states are partial assignments; formulation decides whether the space is thousands or billions.
- **Puzzle and game AI** — the formulation is the algorithm's only input; a bad heuristic cannot rescue a bad state space.
- **Compiler optimisation** — instruction selection is a shortest-path problem over program states.

## 9. Common Mistakes

- Treating a node as a state and re-expanding duplicates, or the reverse and losing the path.
- Forgetting that costs must be non-negative for Dijkstra-style reasoning.
- Modelling too much detail ("position to the millimetre") and making the problem unsolvable.
- Modelling too little detail and reporting a route that ignores a one-way street.
- Testing the goal when a node is *generated* rather than when it is *expanded* — this changes optimality guarantees.

## 10. Exercises

1. Formulate the water-jug problem (3-litre and 5-litre jugs, target 4 litres) as a five-tuple. How many states are reachable?
2. Write `is_solvable(tiles)` for the 8-puzzle using inversion parity, and test it on two random states.
3. Add diagonal moves to the grid-world formulation. What happens to $b$, and to the number of states?
4. Take a problem from your own work. Write its state, actions, goal test and cost, then state one abstraction promise you are making.

## 11. Self-Assessment

1. Why can two distinct nodes share one state?
2. A problem has $b = 4$ and $d = 12$. Roughly how many nodes in the full tree?
3. What breaks if the transition function allows a zero-cost cycle?
4. Give one abstraction that is appropriate for a planning demo and one that is not appropriate for production.

## 12. Key Terms

**State**, **node**, **state space**, **branching factor**, **depth**, **transition model**, **goal test**, **path cost**, **abstraction**.

## 13. Further Reading

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*, chapter 3 — the canonical formulation.
- Hart, Nilsson & Raphael (1968), "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" — where the cost model is made precise.

## What to Do Next

Continue to [L03-02 Uninformed Search](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md), where the
same five-tuple is searched four different ways.
