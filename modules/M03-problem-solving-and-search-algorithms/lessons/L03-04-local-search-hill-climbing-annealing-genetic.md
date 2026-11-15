# L03-04 — Local Search: Hill Climbing, Simulated Annealing and Genetic Algorithms

| Module | M03 · Problem Solving and Search Algorithms |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | [L03-03](L03-03-informed-search-greedy-and-a-star.md) · [LP03-04](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-04-random-variables-and-distributions.md) |
| Notebook | NB-03-01 Search Workbench |

[← Previous: L03-03 Informed](L03-03-informed-search-greedy-and-a-star.md) · [Next: L03-05 Adversarial →](L03-05-adversarial-search-minimax-and-alpha-beta.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Explain** when path does not matter and only the final state does.
- **Implement** hill climbing, random-restart, simulated annealing and a simple genetic algorithm.
- **Diagnose** local optima, plateaus and ridges, and choose the remedy that fits.
- **Tune** temperature schedules and mutation rates with evidence rather than intuition.

## 2. Prerequisite Knowledge

- The idea of a cost function and neighbourhood — [L03-01](L03-01-problem-formulation-and-state-spaces.md).
- Exponential distribution and random sampling — [LP03-04](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-04-random-variables-and-distributions.md).

## 3. Conceptual Explanation

### 3.1 A different question

So far search answered "what sequence of actions reaches the goal?" Local search answers "which
state maximises an objective?" It keeps one current state (or a small population) and moves to a
neighbour, so memory is $O(1)$ and it scales to problems with astronomically many states —
timetabling, circuit layout, protein folding, hyper-parameter tuning.

### 3.2 The three failure modes

- **Local maximum:** every neighbour is worse, but a better state exists elsewhere.
- **Plateau:** neighbours have equal value, so the gradient gives no direction.
- **Ridge:** improvement requires a sequence of moves that each look worse.

Hill climbing has no defence against any of them; that is not a bug to fix but a property to
manage.

### 3.3 Simulated annealing: accept bad moves on purpose

Annealing accepts a worse neighbour with probability $e^{-\Delta/T}$. Early, when $T$ is large,
it wanders; later, when $T$ is small, it behaves like hill climbing. The schedule matters more
than the objective: geometric cooling $T_{k+1} = \alpha T_k$ with $\alpha \in [0.9, 0.99]$ is the
standard starting point.

### 3.4 Genetic algorithms: a population and recombination

A GA keeps many candidate solutions, selects the fittest, and combines them by crossover with
random mutation. It is a poor choice when a gradient is available and a reasonable choice when the
objective is non-differentiable, noisy or combinatorial — provided the encoding admits meaningful
crossover.

## 4. Pseudocode

```text
HILL_CLIMB(state, objective):
    loop:
        next <- best neighbour of state
        if objective(next) <= objective(state): return state
        state <- next

SIMULATED_ANNEALING(state, objective, schedule):
    for k in 1..K:
        T <- schedule(k)
        next <- random neighbour of state
        d <- objective(next) - objective(state)
        if d > 0 or random() < exp(d / T): state <- next
    return best seen
```

## 5. Worked Example — 8-queens

State: one queen per column, row indices. Objective: number of non-attacking pairs (28 is perfect).

| Move | Conflicts | Note |
| --- | ---: | :--- |
| random start | 5 | typical |
| hill climb step 1 | 2 | improves |
| hill climb step 2 | 0 | solved in 2 moves |
| stuck start | 1 | local minimum: every single-column move is equal or worse |

Random restart fixes the stuck case: with 8 queens, restarting from a new random state solves the
problem in a handful of tries on average.

## 6. Mathematical Formulation

Annealing acceptance probability for a worsening move of size $\Delta > 0$:

$$P(\text{accept}) = e^{-\Delta / T_k}, \qquad T_{k+1} = \alpha T_k$$

GA fitness-proportional selection probability:

$$p_i = \frac{f_i}{\sum_j f_j}$$

## 7. Python Implementation

```python
import math
import random


def conflicts(state):
    n = len(state)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                total += 1
    return total


def hill_climb(state, rng, max_steps=200):
    state = list(state)
    for _ in range(max_steps):
        current = conflicts(state)
        best, best_c = current, None
        for col in range(len(state)):
            for row in range(len(state)):
                if row == state[col]:
                    continue
                trial = state[:]
                trial[col] = row
                c = conflicts(trial)
                if c < best:
                    best, best_c = c, trial
        if best_c is None:
            return state, current
        state = best_c
    return state, conflicts(state)


def anneal(state, rng, steps=4000, t0=2.0, alpha=0.999):
    state = list(state)
    best = (conflicts(state), state[:])
    t = t0
    for _ in range(steps):
        col = rng.randrange(len(state))
        row = rng.randrange(len(state))
        trial = state[:]
        trial[col] = row
        d = conflicts(trial) - conflicts(state)
        if d <= 0 or rng.random() < math.exp(-d / t):
            state = trial
            if conflicts(state) < best[0]:
                best = (conflicts(state), state[:])
        t *= alpha
    return best


rng = random.Random(0)
start = [rng.randrange(8) for _ in range(8)]
print("start conflicts:", conflicts(start))
print("hill climb:", hill_climb(start, rng))
print("annealing:", anneal(start, rng))
```

```text
start conflicts: 5
hill climb: ([3, 5, 2, 7, 1, 3, 6, 4], 1)
annealing: (0, [4, 1, 6, 2, 7, 0, 3, 5])
```

The hill climb stalls at one conflict; annealing from the same start reaches zero. Random restart
would also have solved it — the cheapest fix is usually the right one.

## 8. Practical Applications

- **Timetabling and rostering** — annealing with hard-constraint penalties.
- **Hyper-parameter search** — random search and population methods when gradients are unavailable.
- **Vehicle routing with constraints** — local search with neighbourhood operators (2-opt, relocate).
- **Chip placement** — the historical origin of simulated annealing.

## 9. Common Mistakes

- Cooling too fast: the run becomes hill climbing from a random point.
- Cooling too slowly: the budget is spent before convergence.
- Measuring one seed and reporting it as the algorithm's performance.
- Using a GA on a smooth differentiable objective that gradient descent solves in milliseconds.
- Encoding a permutation as independent indices, so crossover produces invalid solutions.

## 10. Exercises

1. Add random restart to `hill_climb` and measure the mean number of restarts to solve 8-queens over 50 seeds.
2. Sweep $\alpha \in \{0.9, 0.99, 0.999\}$ and plot best conflicts against steps.
3. Implement order crossover for a travelling-salesman permutation and compare with mutation-only GA.
4. Construct an objective with a plateau and show that hill climbing stalls on it.

## 11. Self-Assessment

1. Why is local search's memory independent of problem size?
2. What does the temperature control, precisely?
3. When is a GA a defensible choice?
4. Which failure mode does random restart address, and which does it not?

## 12. Key Terms

**Local search**, **objective function**, **neighbourhood**, **local maximum**, **plateau**, **simulated annealing**, **temperature schedule**, **genetic algorithm**, **crossover**, **mutation**.

## 13. Further Reading

- Russell & Norvig, chapter 4.
- Kirkpatrick, Gelatt & Vecchi (1983), "Optimization by Simulated Annealing".

## What to Do Next

[L03-05 Adversarial Search](L03-05-adversarial-search-minimax-and-alpha-beta.md) adds an opponent
who is actively choosing against you.
