# L10-02 — Value-Based Reinforcement Learning

| Module | M10 · Reinforcement Learning |
| :--- | :--- |
| Level | 400 |
| Study time | 80 minutes |
| Prerequisites | [L10-01](L10-01-foundations-of-reinforcement-learning.md) |
| Code | `code/dp.py`, `code/tabular.py` |

[← Previous: L10-01](L10-01-foundations-of-reinforcement-learning.md) · [Next: L10-03 TD Learning →](L10-03-temporal-difference-learning.md)

## 1. Learning Objectives

- **Define** $V^\pi$, $Q^\pi$, $V^*$ and $Q^*$ and state the relationship between them.
- **Apply** the Bellman expectation and optimality backups by hand on a two-state MDP.
- **Implement** policy evaluation, policy iteration and value iteration.
- **Explain** why dynamic programming needs a model and what that costs.
- **Estimate** values by Monte Carlo and say why its variance is higher than DP's.

## 2. Prerequisite Knowledge

Returns and discounts from [L10-01](L10-01-foundations-of-reinforcement-learning.md), and the expectation
notation from P03. Every line of code below is one of the two Bellman equations, so read them again before
starting.

## 3. Conceptual Explanation

### 3.1 Two functions, four symbols

- $V^\pi(s)$ — expected return starting in $s$ and following $\pi$.
- $Q^\pi(s,a)$ — expected return starting in $s$, taking $a$, then following $\pi$.
- $V^*(s) = \max_\pi V^\pi(s)$ and $Q^*(s,a) = \max_\pi Q^\pi(s,a)$ — the best achievable.

Given $Q^*$, the optimal policy is one line: $\pi^*(s) = \arg\max_a Q^*(s,a)$. That is why action values are
the working object in control.

### 3.2 Dynamic programming: the model is the price

Policy evaluation iterates the expectation backup until values stop moving. Policy iteration alternates
evaluation with greedy improvement. Value iteration folds both into one sweep of the optimality backup.
All three require $P(s'\mid s,a)$ and $R$ — the model. In a gridworld you have it; in the real world you
usually do not, which is why L10-03 exists.

### 3.3 Monte Carlo: sample instead of enumerate

Monte Carlo evaluation runs episodes, observes returns, and averages them per state. No model needed. The
cost is variance: a single long episode can be far from the mean, and every estimate waits for the episode
to end. The bias is zero, though, which is why MC is the reference against which TD is judged.

### 3.4 What convergence actually requires

- **Policy evaluation** converges for $\gamma < 1$ because the Bellman operator is a contraction.
- **Policy iteration** terminates in a finite number of steps for finite MDPs.
- **Value iteration** converges to $V^*$ at a geometric rate governed by $\gamma$.

If $\gamma = 1$ and the task is continuing, none of these statements holds without extra conditions.

## 4. Pseudocode

```text
function POLICY_EVALUATION(mdp, policy, gamma, theta):
    V <- zeros
    repeat:
        delta <- 0
        for s in states:
            v <- sum over a, s' of pi(a|s) P(s'|s,a) [R + gamma V(s')]
            delta <- max(delta, |v - V(s)|); V(s) <- v
    until delta < theta
    return V

function VALUE_ITERATION(mdp, gamma, theta):
    V <- zeros
    repeat:
        for s in states: V(s) <- max over a of sum over s' P(s'|s,a)[R + gamma V(s')]
    until max change < theta
    return V, greedy_policy(V)
```

## 5. Worked Example — the 5×5 gridworld

```python
import dp, rl_envs

mdp = rl_envs.make_gridworld("open", step_cost=-0.04)
vi = dp.value_iteration(mdp, gamma=0.9)
pi = dp.policy_iteration(mdp, gamma=0.9)
print("value iteration sweeps:", vi["sweeps"], "| start value:", round(float(vi["V"][0]), 4))
print("policy iteration rounds:", pi["rounds"], "| start value:", round(float(pi["V"][0]), 4))
print("same policy:", (vi["policy"] == pi["policy"]).all())
print(dp.format_policy(mdp, vi["policy"]))
```

Both algorithms agree, as they must: they are solving the same fixed point. Value iteration needs more
sweeps but each sweep is cheaper; policy iteration needs fewer but each requires a full evaluation.

## 6. Mathematical Formulation

Bellman expectation backup:

$$V_{k+1}(s) \leftarrow \sum_a \pi(a\mid s)\sum_{s'} P(s'\mid s,a)\big[R(s,a,s') + \gamma V_k(s')\big]$$

Bellman optimality backup:

$$V_{k+1}(s) \leftarrow \max_a \sum_{s'} P(s'\mid s,a)\big[R(s,a,s') + \gamma V_k(s')\big]$$

Monte Carlo estimate: $\hat{V}(s) = \frac{1}{N(s)}\sum_{i=1}^{N(s)} G_i(s)$, unbiased but high variance.

## 7. Python Implementation

```python
import numpy as np
import dp, rl_envs, tabular

mdp = rl_envs.make_gridworld("open", step_cost=-0.04)
vi = dp.value_iteration(mdp, gamma=0.9)
print("V* grid:")
print(dp.format_grid(mdp, vi["V"]))

# exact policy evaluation of a random policy, for contrast with the optimal one
policy = dp.random_policy(mdp, seed=0)
V_pi = dp.exact_policy_value(mdp, policy, gamma=0.9)
print("random policy start value:", round(float(V_pi[0]), 4))
print("optimal start value:", round(float(vi["V"][0]), 4))

# Monte Carlo prediction on the same MDP, via the gym-style adapter
env = rl_envs.MDPAdapter(mdp)
mc = tabular.mc_prediction(env, lambda s: 0, episodes=200, gamma=0.9, seed=0)
print("MC estimates (first three states):", {k: round(float(v), 3) for k, v in list(mc.items())[:3]})
```

## 8. Practical Applications

- **Scheduling and inventory** — DP is the right tool when a small model is available (MP-10).
- **Evaluation baselines** — every learned agent should be compared against a DP solution on a toy version
  of the task.
- **Reward debugging** — an unexpected optimal policy is usually a modelling error, visible in $V^*$.
- **Teaching intuition** — value grids make the effect of a discount or a step cost visible in one picture.

## 9. Common Mistakes

1. Forgetting to skip terminal states in the backup, so values leak past the goal.
2. Mixing up $V$ and $Q$ indices when computing a greedy policy.
3. Using too large a $\theta$ and calling the result optimal.
4. Comparing DP sweeps with MC episodes as if they were the same unit of work.
5. Assuming a converged $V$ means a good policy — check the induced policy, not just the numbers.

## 10. Exercises

1. Hand-compute one Bellman backup for a two-state MDP with known transitions and $\gamma = 0.5$.
2. Run value iteration at $\gamma \in \{0.5, 0.9, 0.99\}$ and tabulate sweeps and start values.
3. Compare policy iteration and value iteration on the maze gridworld: sweeps, policies, wall-clock.
4. Estimate $V^\pi$ by Monte Carlo with 50, 200 and 1000 episodes and plot the error against the exact value.

## 11. Self-Assessment

1. Why does a greedy policy with respect to $V^\pi$ require the model, while with $Q^\pi$ it does not?
   *Because the one-step lookahead needs $P$ and $R$; $Q$ already contains their expectation.*
2. What is the contraction argument for value iteration in one sentence?
   *The Bellman optimality operator is a $\gamma$-contraction in the max norm, so repeated application has a
   unique fixed point.*
3. Why does Monte Carlo have higher variance than DP for the same MDP?
   *It estimates from sampled returns, which include all the randomness of the trajectory.*

## 12. Key Terms

**State value**, **action value**, **Bellman equation**, **policy evaluation**, **policy iteration**,
**value iteration**, **dynamic programming**, **Monte Carlo prediction**, **contraction**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Sutton and Barto, ch. 4 (dynamic programming) and ch. 5 (Monte Carlo).

## What to Do Next

Continue to [L10-03 Temporal Difference Learning](L10-03-temporal-difference-learning.md), and complete
[NB-10-01](../notebooks/nb-10-01-mdps-and-dynamic-programming.ipynb).
