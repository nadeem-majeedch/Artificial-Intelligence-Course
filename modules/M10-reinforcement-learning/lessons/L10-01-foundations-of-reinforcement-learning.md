# L10-01 — Foundations of Reinforcement Learning

| Module | M10 · Reinforcement Learning |
| :--- | :--- |
| Level | 400 |
| Study time | 75 minutes |
| Prerequisites | [M05 L05-01](../../M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-01-probability-conditional-probability-and-bayes-theorem.md) · [P03 Probability](../../../prerequisites/P03-probability-and-statistics/README.md) |
| Code | `code/rl_envs.py` |

[← Module start](../README.md) · [Next: L10-02 Value-Based RL →](L10-02-value-based-reinforcement-learning.md)

## 1. Learning Objectives

- **Write down** an MDP: states, actions, transitions, rewards, discount.
- **Explain** the difference between supervised labels and scalar reward.
- **Compute** a return and show how the discount factor changes it.
- **Distinguish** episodic from continuing tasks and state why it matters for evaluation.
- **Describe** the exploration–exploitation trade-off with a concrete failure of each extreme.

## 2. Prerequisite Knowledge

Conditional probability and expectation (P03), plus the MDP vocabulary from
[L05-05](../../M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-01-probability-conditional-probability-and-bayes-theorem.md).
If "expectation of a sum of random variables" is not automatic, revisit that lesson first: every RL update
is an expectation estimate.

## 3. Conceptual Explanation

### 3.1 Learning from consequences

Supervised learning is told the answer. Reinforcement learning is told a number, later, and must work out
which of its many actions caused it. That single difference produces every difficulty in the module:
credit assignment, delayed reward, non-stationary data (the policy changes the distribution it learns
from), and the need to explore.

### 3.2 The interaction loop

```text
state s_t → action a_t → reward r_{t+1}, next state s_{t+1} → ...
```

The agent's *policy* $\pi(a \mid s)$ maps states to action distributions. The *return* is what it is trying
to maximise:

$$G_t = r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + \dots = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}$$

With $\gamma = 0$ the agent is myopic; with $\gamma \to 1$ it cares about the distant future. The discount
is not a technicality: it is the only reason a continuing task has a finite objective.

### 3.3 The Markov property

A state is Markov if it summarises everything about the past that affects the future. A gridworld position
is Markov; a single camera frame usually is not (velocity is missing), which is why real systems stack
frames or use recurrent state. When the property fails, no amount of tuning fixes the agent — the
information is simply absent.

### 3.4 Episodic versus continuing

An episodic task terminates (a game, a delivery). A continuing task never does (a traffic controller), and
must be evaluated on average reward per step rather than per episode. Mixing the two produces meaningless
comparisons: an agent that survives by never finishing scores beautifully on "return per episode".

### 3.5 Exploration versus exploitation

- **Pure exploitation** — a gridworld agent finds a small reward, then camps on it forever.
- **Pure exploration** — the agent never repeats a good action, so it never accumulates reward.

$\varepsilon$-greedy is the simplest compromise: with probability $\varepsilon$ act randomly, otherwise act
greedily. Decaying $\varepsilon$ over time is standard; the schedule is a hyperparameter with a real effect
on the final policy.

## 4. Pseudocode

```text
function EPISODE(env, policy, gamma):
    s <- env.reset()
    G <- 0; discount <- 1
    repeat:
        a <- policy(s)
        s', r, done <- env.step(a)
        G <- G + discount * r
        discount <- discount * gamma
        s <- s'
    until done
    return G
```

## 5. Worked Example — the same grid, two discounts

```python
import rl_envs, dp

mdp = rl_envs.make_gridworld("open", step_cost=-0.04)
for gamma in (0.5, 0.9, 0.99):
    result = dp.value_iteration(mdp, gamma=gamma)
    path = dp.greedy_path(mdp, result["policy"])
    print(f"gamma={gamma}: sweeps={result['sweeps']}, path length={len(path)}, V(start)={result['V'][0]:.3f}")
```

The value of the start state falls as the discount rises, because the step cost is paid over more steps
before the goal. A larger discount makes the agent patient; it does not make the task easier.

## 6. Mathematical Formulation

The Bellman expectation equation for a fixed policy:

$$V^\pi(s) = \sum_a \pi(a\mid s) \sum_{s'} P(s'\mid s,a)\big[R(s,a,s') + \gamma V^\pi(s')\big]$$

The optimality equation replaces the average over actions with a maximum:

$$V^*(s) = \max_a \sum_{s'} P(s'\mid s,a)\big[R(s,a,s') + \gamma V^*(s')\big]$$

Everything in L10-02 is a way of solving one of these two equations.

## 7. Python Implementation

```python
import numpy as np
import dp, rl_envs

mdp = rl_envs.make_gridworld("open", step_cost=-0.04)
print("states:", mdp.n_states, "actions:", mdp.n_actions)
print(dp.format_grid(mdp, np.zeros(mdp.n_states)))

# one rollout: the loop, the discounted return and the episode length
env = rl_envs.MDPAdapter(mdp)
obs, _ = env.reset(seed=0)
total, discount = 0.0, 1.0
for step in range(20):
    obs, reward, terminated, truncated, _ = env.step(step % mdp.n_actions)
    total += discount * reward
    discount *= 0.9
    if terminated or truncated:
        break
print("return:", round(total, 3), "steps:", step + 1)
```

## 8. Practical Applications

- **Inventory control** — order quantities with stochastic demand (MP-10).
- **Traffic signals** — phase timing with a continuing objective.
- **Robotics** — locomotion and manipulation where labels do not exist.
- **Recommendation** — sequential choice under delayed engagement signals.

## 9. Common Mistakes

1. Treating reward as a loss to minimise without flipping the sign consistently.
2. Comparing episodic returns across tasks with different episode lengths.
3. Forgetting that the discount changes the optimal policy, not just the scale of value.
4. Using a non-Markov state and blaming the algorithm.
5. Evaluating on the training episodes only.

## 10. Exercises

1. Compute $G_0$ for rewards `[1, 1, 1]` with $\gamma = 0.9$ and with $\gamma = 1$.
2. Run value iteration on the `open` gridworld at three discounts and tabulate start-state values.
3. Construct a state representation that is *not* Markov for a cart-pole and say what is missing.
4. Give one example each where $\varepsilon = 0$ and $\varepsilon = 1$ fail catastrophically.

## 11. Self-Assessment

1. Why does a discount factor of 0 produce a greedy-but-blind policy?
   *It values only the immediate reward, so any future consequence is invisible.*
2. What makes a state Markov?
   *It contains all information from the past needed to predict the future distribution of rewards and
   next states.*
3. Why is average reward the right objective for continuing tasks?
   *Because the episode never ends, so a total return is unbounded and cannot rank policies.*

## 12. Key Terms

**Agent**, **environment**, **state**, **action**, **reward**, **policy**, **return**, **discount factor**,
**episode**, **Markov decision process**, **exploration**, **exploitation**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed., ch. 3
  ([free PDF](http://incompleteideas.net/book/the-book-2nd.html)).

## What to Do Next

Continue to [L10-02 Value-Based Reinforcement Learning](L10-02-value-based-reinforcement-learning.md), and
run [NB-10-01](../notebooks/nb-10-01-mdps-and-dynamic-programming.ipynb).
