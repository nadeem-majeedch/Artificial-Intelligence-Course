# L03-05 — Adversarial Search: Minimax and Alpha–Beta Pruning

| Module | M03 · Problem Solving and Search Algorithms |
| :--- | :--- |
| Level | 300 |
| Study time | 85 minutes |
| Prerequisites | [L03-04](L03-04-local-search-hill-climbing-annealing-genetic.md) · [LP01-03](../../../prerequisites/P01-python-programming/lessons/LP01-03-conditionals-loops-and-comprehensions.md) |
| Notebook | NB-03-01 Search Workbench |

[← Previous: L03-04 Local Search](L03-04-local-search-hill-climbing-annealing-genetic.md) · [Next: L03-06 Constraints →](L03-06-constraint-satisfaction-problems.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Implement** minimax for a two-player zero-sum game.
- **Apply** alpha–beta pruning and prove it returns the same value as plain minimax.
- **Measure** the node reduction from move ordering.
- **Explain** why evaluation functions make deep search approximate, not exact.

## 2. Prerequisite Knowledge

- Recursion and tree traversal — [LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md).
- The state/node distinction — [L03-01](L03-01-problem-formulation-and-state-spaces.md).

## 3. Conceptual Explanation

### 3.1 The setting

Two players, alternating turns, zero-sum: one player's gain is the other's loss. The game tree
alternates **max** nodes (our turn) and **min** nodes (opponent's turn), with terminal values from
our perspective.

### 3.2 Minimax

Minimax computes the value of a position assuming both players play optimally:
$V(s) = \max_a V(\text{result}(s,a))$ at our turn, $\min$ at theirs. It is exact only if the tree
is searched to terminal states.

### 3.3 Alpha–beta: prune what cannot matter

Maintain $\alpha$ (best value we can already guarantee) and $\beta$ (best the opponent can
guarantee). If $\alpha \ge \beta$ at a node, the remaining children cannot influence the result and
are skipped. The returned value is identical to minimax — pruning changes work, not the answer.

With perfect ordering the search examines about $b^{d/2}$ nodes instead of $b^d$: at $b = 10$,
depth 8, that is roughly 10,000 instead of 100,000,000.

### 3.4 Depth limits and evaluation functions

Real games are too deep, so search stops at a horizon and applies an evaluation function. The
value is then an estimate, and horizon effects appear: a position can look excellent one ply before
a forced loss. Quiescence search (extend until the position is "quiet") is the standard mitigation.

## 4. Pseudocode

```text
function MINIMAX(state, depth, maximising):
    if terminal(state) or depth == 0: return evaluate(state)
    if maximising: return max over children of MINIMAX(child, depth-1, False)
    else:          return min over children of MINIMAX(child, depth-1, True)

function ALPHA_BETA(state, depth, alpha, beta, maximising):
    if terminal(state) or depth == 0: return evaluate(state)
    if maximising:
        value <- -infinity
        for child in children(state):
            value <- max(value, ALPHA_BETA(child, depth-1, alpha, beta, False))
            if value >= beta: break          # beta cut-off
            alpha <- max(alpha, value)
        return value
    else:
        value <- +infinity
        for child in children(state):
            value <- min(value, ALPHA_BETA(child, depth-1, alpha, beta, True))
            if value <= alpha: break         # alpha cut-off
            beta <- min(beta, value)
        return value
```

## 5. Worked Example — a two-ply tree

Leaves, left to right: `3, 12, 8 | 2, 4, 6 | 14, 5, 2`.

Plain minimax: left group max = 12, middle max = 6, right max = 14; root min = 6.

Alpha–beta trace:

1. Left group: 12 found, $\alpha = 12$ at root after the first child? No — root is min, so $\beta$ starts at $\infty$; after left child value 12, $\beta = 12$.
2. Middle group: first leaf 2; at that max node, value ≥ 2. Since 2 < 12 it cannot raise the min's value above 12? It can only produce a value ≤ 12, which could still be lower — continue. Leaves 2, 4, 6 give 6; $\beta = 6$.
3. Right group: first leaf 14. The max node will return ≥ 14, which is worse for the min player than 6, so the remaining two leaves are pruned. Two nodes saved out of nine, with a suboptimal ordering.

With best-first ordering the saving is much larger, which is why move ordering (captures first,
killer moves) is worth more than a deeper search.

## 6. Mathematical Formulation

$$\text{Minimax}(s) = \begin{cases} \text{Utility}(s) & s \text{ terminal} \\ \max_{a} \text{Minimax}(T(s,a)) & \text{our turn} \\ \min_{a} \text{Minimax}(T(s,a)) & \text{their turn} \end{cases}$$

Best-case node count with pruning: $O(b^{d/2})$, i.e. the same answer for an effective doubling of
search depth.

## 7. Python Implementation

```python
def minimax(state, depth, maximising, children, evaluate, terminal):
    if terminal(state) or depth == 0:
        return evaluate(state)
    values = [minimax(c, depth - 1, not maximising, children, evaluate, terminal)
              for c in children(state)]
    return max(values) if maximising else min(values)


def alphabeta(state, depth, alpha, beta, maximising, children, evaluate, terminal, counter):
    counter[0] += 1
    if terminal(state) or depth == 0:
        return evaluate(state)
    if maximising:
        value = float("-inf")
        for c in children(state):
            value = max(value, alphabeta(c, depth - 1, alpha, beta, False,
                                         children, evaluate, terminal, counter))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    value = float("inf")
    for c in children(state):
        value = min(value, alphabeta(c, depth - 1, alpha, beta, True,
                                     children, evaluate, terminal, counter))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value


LEAVES = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]


def children(node):
    depth, index = node
    if depth == 2:
        return []
    return [(depth + 1, index * 3 + k) for k in range(3)]


def evaluate(node):
    depth, index = node
    return LEAVES[depth][index] if depth == 2 and index < 3 else 0


counter = [0]
print("plain value:", minimax((0, 0), 2, True, children, evaluate,
                              lambda n: n[0] == 2))
print("pruned value:", alphabeta((0, 0), 2, float("-inf"), float("inf"), True,
                                 children, evaluate, lambda n: n[0] == 2, counter),
      "nodes:", counter[0])
```

Both calls return the same value; the second visits fewer nodes.

## 8. Practical Applications

- **Board games** — chess, checkers, Go (with Monte Carlo tree search where branching is huge).
- **Adversarial planning** — security games, red-team/blue-team simulation.
- **Auction and negotiation agents** — minimax over bids with a utility model.
- **Automated verification** — game-theoretic check of a protocol against an adversary.

## 9. Common Mistakes

- Sign errors: evaluating from one player's perspective and negating inconsistently.
- Pruning with an incorrect bound comparison ($>$ vs $\ge$), which can change the value.
- Searching deeper with a bad evaluation function and trusting the result more.
- Ignoring horizon effects and reporting a "win" that is a forced loss two plies later.
- Assuming alpha–beta reduces the worst case without good move ordering.

## 10. Exercises

1. Instrument both functions on a random tree of depth 4, branching 4, and report nodes visited.
2. Reorder the leaves in §5 to maximise pruning and count saved nodes.
3. Add a move-ordering heuristic (captures first) to a small chess-like game and measure the reduction.
4. Explain why alpha–beta returns the minimax value even though entire subtrees are never examined.

## 11. Self-Assessment

1. What is the complexity of minimax without pruning, and with perfect ordering?
2. What do $\alpha$ and $\beta$ represent?
3. Why does a deeper search with a poor evaluation function not guarantee better play?
4. Give one domain outside games where minimax is the right model.

## 12. Key Terms

**Zero-sum game**, **minimax**, **alpha**, **beta**, **cut-off**, **evaluation function**, **horizon effect**, **quiescence search**, **move ordering**.

## 13. Further Reading

- Russell & Norvig, chapter 5.
- Knuth & Moore (1975), "An Analysis of Alpha-Beta Pruning".

## What to Do Next

[L03-06 Constraint Satisfaction](L03-06-constraint-satisfaction-problems.md) replaces adversarial
opponents with hard constraints — a different structure with its own algorithms.
