# L10-03 — Temporal Difference Learning

| Module | M10 · Reinforcement Learning |
| :--- | :--- |
| Level | 400 |
| Study time | 80 minutes |
| Prerequisites | [L10-02](L10-02-value-based-reinforcement-learning.md) |
| Code | `code/tabular.py` |

[← Previous: L10-02](L10-02-value-based-reinforcement-learning.md) · [Next: L10-04 Deep RL →](L10-04-deep-reinforcement-learning.md)

## 1. Learning Objectives

- **Derive** the TD(0) update as a sampled Bellman backup.
- **Implement** SARSA and Q-learning and state precisely how their targets differ.
- **Explain** on-policy versus off-policy with the cliff-walking result as evidence.
- **Tune** $\alpha$ and $\varepsilon$ and describe what each controls.
- **Detect** reward shaping that changes the optimal policy rather than accelerating learning.

## 2. Prerequisite Knowledge

Bellman backups from [L10-02](L10-02-value-based-reinforcement-learning.md) and $\varepsilon$-greedy
exploration from [L10-01](L10-01-foundations-of-reinforcement-learning.md).

## 3. Conceptual Explanation

### 3.1 From enumeration to sampling

DP needs the model; MC needs a whole episode. TD combines the two: bootstrap from an estimate after one
step, using the reward you actually observed.

$$V(s) \leftarrow V(s) + \alpha\big[\underbrace{r + \gamma V(s')}_{\text{TD target}} - V(s)\big]$$

The bracket is the **TD error**. TD is biased (it trusts an estimate) and much lower variance than MC (one
step of randomness, not a whole trajectory). That trade is the reason tabular TD learns faster per episode
in most gridworlds.

### 3.2 Two control algorithms, one difference

| Algorithm | Target | Behaviour | Consequence |
| :--- | :--- | :--- | :--- |
| SARSA | $r + \gamma Q(s',a')$ | on-policy: $a'$ is what the policy will take | learns the value of the exploration policy |
| Q-learning | $r + \gamma \max_{a'} Q(s',a')$ | off-policy: assumes greedy next action | learns the optimal policy while exploring |

On the cliff-walking task with $\varepsilon = 0.1$, SARSA learns a path that stays away from the edge and
earns more *online* reward; Q-learning learns the shortest path along the edge and falls in more often
while exploring. Q-learning's greedy policy is better; SARSA's behaviour is safer. Both statements are
true, and which you want depends on whether you will deploy the greedy policy or the exploring one.

Measured in this module (`experiments.compare_sarsa_qlearning`, 300 episodes, $\alpha=0.5$,
$\varepsilon=0.1$, seeds 0 and 1): SARSA tail return ≈ **−32**, Q-learning tail ≈ **−36**. The gap is the
cost of exploration on a risky path, not a bug.

### 3.3 Learning rate and exploration

- $\alpha$ controls how much of each new sample you believe. Too small: the agent forgets faster than it
  learns. Too large: values oscillate and can diverge.
- $\varepsilon$ controls how much you deviate from the current best guess. Decay it too fast and the agent
  locks into the first path it found; too slowly and it never exploits.

Robbins–Monro conditions ($\sum \alpha_t = \infty$, $\sum \alpha_t^2 < \infty$) are the formal requirement
for convergence with sampled updates; a constant $\alpha$ converges to a neighbourhood, not a point.

### 3.4 Reward shaping has a correctness condition

Adding a potential-based term $F(s,s') = \gamma\Phi(s') - \Phi(s)$ preserves the optimal policy (Ng,
Harada and Russell, 1999). Anything else may not. A shaping term that pays for "moving right" will make the
agent move right forever if the task ever ends. Test shaping by comparing the optimal policy before and
after, not by looking at the learning curve.

## 4. Pseudocode

```text
function Q_LEARNING(env, episodes, alpha, gamma, eps):
    Q <- zeros
    for episode in 1..episodes:
        s <- reset()
        repeat:
            a <- epsilon_greedy(Q[s], eps)
            s', r, done <- step(a)
            target <- r + (0 if done else gamma * max(Q[s']))
            Q[s][a] += alpha * (target - Q[s][a])
            s <- s'
        until done

function SARSA(env, episodes, alpha, gamma, eps):
    # identical except the target uses the action actually chosen next
```

## 5. Worked Example — cliff walking

```python
import experiments, tabular

result = experiments.compare_sarsa_qlearning(episodes=300)
print("SARSA tail:", round(result["sarsa_tail"], 2))
print("Q-learning tail:", round(result["q_learning_tail"], 2))
print("per seed:", {k: [round(x, 1) for x in v] for k, v in result["tail_per_seed"].items()})

env = experiments.make_cliff()
q = tabular.q_learning(env, episodes=500, alpha=0.5, eps=0.1, seed=0)
path = tabular.greedy_path_from_q(env, q["Q"], start=36)
print("greedy path length:", len(path), "first steps:", path[:6])
```

The greedy path from Q-learning hugs the cliff. That is the optimal policy for the MDP — and the reason the
online curve is worse than SARSA's.

## 6. Mathematical Formulation

TD error and update:

$$\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t), \qquad V(s_t) \leftarrow V(s_t) + \alpha\delta_t$$

Q-learning (off-policy):

$$Q(s,a) \leftarrow Q(s,a) + \alpha\big[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\big]$$

SARSA (on-policy):

$$Q(s,a) \leftarrow Q(s,a) + \alpha\big[r + \gamma Q(s',a') - Q(s,a)\big]$$

Expected SARSA replaces $Q(s',a')$ with $\sum_{a'}\pi(a'\mid s')Q(s',a')$, cutting variance at the cost of
one extra sum.

## 7. Python Implementation

```python
import numpy as np
import experiments, tabular

env = experiments.make_cliff()

for eps in (0.01, 0.1, 0.3):
    run = tabular.q_learning(env, episodes=300, alpha=0.5, eps=eps, seed=0)
    print(f"eps={eps}: tail return {experiments.mean_tail(run['returns']):.2f}, "
          f"mean steps {run['lengths'][-50:].mean():.1f}")

# optimistic initialisation as an exploration strategy
optimistic = tabular.q_learning(env, episodes=300, alpha=0.5, eps=0.0, q_init=0.0, seed=0)
print("greedy-only tail:", round(experiments.mean_tail(optimistic["returns"]), 2))
```

Greedy-only Q-learning stalls: with no exploration it never discovers the goal. That is the cleanest
demonstration that $\varepsilon$ is not decoration.

## 8. Practical Applications

- **Adaptive control** — signal timing, where online reward is the deployment metric.
- **Inventory** — tabular Q-learning on discretised stock levels (MP-10).
- **Game agents** — TD learning beat human players at backgammon decades before deep RL.
- **Simulation calibration** — TD errors reveal where a simulator disagrees with reality.

## 9. Common Mistakes

1. Using the max in SARSA or the behaviour action in Q-learning, then wondering why results differ.
2. Forgetting `done` in the target, so terminal states bootstrap from nothing.
3. Decaying $\varepsilon$ before the agent has seen the goal.
4. Reporting the best episode instead of the tail mean.
5. Adding reward shaping without checking policy invariance.

## 10. Exercises

1. Derive the TD(0) update from the Bellman expectation equation in three lines.
2. Sweep $\alpha \in \{0.05, 0.2, 0.5, 0.9\}$ on cliff walking and plot tail return. Where does it destabilise?
3. Run SARSA and Q-learning at $\varepsilon = 0.01$ and $0.3$; does the ordering of their returns change?
4. Design a potential function $\Phi$ for the gridworld and verify that shaping leaves the optimal policy
   unchanged.

## 11. Self-Assessment

1. Why is Q-learning off-policy?
   *Its target uses the greedy action regardless of what the behaviour policy actually did.*
2. Why does SARSA perform better online on the cliff?
   *It values the exploring policy, so it learns to keep away from the cliff that exploration would fall off.*
3. What does a constant learning rate converge to?
   *A neighbourhood of the optimum whose size scales with the learning rate.*

## 12. Key Terms

**Temporal-difference learning**, **TD error**, **bootstrapping**, **SARSA**, **Q-learning**,
**on-policy**, **off-policy**, **epsilon-greedy**, **reward shaping**, **potential function**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Sutton and Barto, ch. 6.
- Ng, Harada and Russell (1999), "Policy Invariance Under Reward Transformations".

## What to Do Next

Continue to [L10-04 Deep Reinforcement Learning](L10-04-deep-reinforcement-learning.md), and complete
[LAB-10-02](../labs/lab-10-02-compare-sarsa-and-q-learning.md).
