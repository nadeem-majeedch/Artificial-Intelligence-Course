# L10-04 — Deep Reinforcement Learning

| Module | M10 · Reinforcement Learning |
| :--- | :--- |
| Level | 400 |
| Study time | 90 minutes |
| Prerequisites | [L10-03](L10-03-temporal-difference-learning.md) · [M07 L07-02](../../M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md) |
| Code | `code/dqn.py` |

[← Previous: L10-03](L10-03-temporal-difference-learning.md) · [Next: L10-05 Advanced RL →](L10-05-advanced-reinforcement-learning.md)

## 1. Learning Objectives

- **Explain** why tabular methods fail as soon as states are continuous.
- **Describe** the two stabilisers that made DQN work: replay and target networks.
- **Derive** the policy-gradient update from the log-derivative trick.
- **Compare** value-based and policy-based methods on what they can and cannot represent.
- **Read** a learning curve and distinguish instability from slow learning.

## 2. Prerequisite Knowledge

TD control from [L10-03](L10-03-temporal-difference-learning.md), plus backpropagation and the training
loop from M07. The networks here are small MLPs; nothing about them is special except that the data is not
i.i.d.

## 3. Conceptual Explanation

### 3.1 Why tables stop working

CartPole's observation is four floats. A gridworld with 0.01 resolution would need $100^4$ entries per
action. Function approximation replaces the table with a parameterised $Q_\theta(s,a)$ and generalises
between nearby states — and immediately breaks two assumptions that tabular TD relied on.

### 3.2 Two assumptions, two fixes

1. **Samples are correlated.** Consecutive transitions are near-duplicates, so gradient descent on them
   chases its own tail. *Experience replay* stores transitions and samples minibatches uniformly,
   decorrelating them.
2. **The target moves.** The bootstrap target depends on the same weights being updated, so the agent
   chases a moving goal. A *target network* — a frozen copy refreshed every few hundred steps — holds the
   target still.

DQN is Q-learning plus those two fixes plus a Huber loss for robustness to large TD errors. Remove either
fix and CartPole training usually fails or becomes wildly unstable — which is exactly what the lab asks you
to reproduce.

### 3.3 Policy gradients

Instead of learning values and deriving a policy, parameterise the policy $\pi_\theta(a\mid s)$ and ascend
the expected return. The log-derivative trick gives

$$\nabla_\theta J = \mathbb{E}\big[\nabla_\theta \log \pi_\theta(a\mid s)\,G_t\big]$$

REINFORCE uses the Monte Carlo return $G_t$: unbiased, high variance. Subtracting a baseline $b(s)$ (often
$V_\theta(s)$) leaves the gradient unchanged in expectation and cuts variance.

### 3.4 Actor–critic and PPO

Actor–critic learns a policy (actor) and a value (critic) together; the critic supplies the baseline and
the advantage $A = r + \gamma V(s') - V(s)$. PPO clips the policy ratio so a single batch cannot move the
policy too far:

$$L^{clip} = \mathbb{E}\Big[\min\big(\rho A,\ \mathrm{clip}(\rho, 1-\epsilon, 1+\epsilon)A\big)\Big],
\qquad \rho = \frac{\pi_\theta(a\mid s)}{\pi_{\theta_{old}}(a\mid s)}$$

The clip is a trust region in disguise: cheap to compute, stable in practice, which is why PPO became the
default baseline for continuous control.

### 3.5 Reading a curve honestly

Averaging over seeds is mandatory: single-run curves in RL are anecdotes. Report the median and the spread,
smooth with a window and state the window, and compare against a random baseline. "It learned" means the
tail return is above the random floor across seeds — not that one run reached a high score.

## 4. Pseudocode

```text
function DQN(env, episodes):
    Q <- network(); Q_target <- copy(Q); buffer <- replay memory
    for episode in 1..episodes:
        s <- reset()
        repeat:
            a <- epsilon_greedy(Q(s), eps)
            s', r, done <- step(a); buffer.add(s, a, r, s', done)
            if len(buffer) > learn_start:
                batch <- sample(buffer)
                target <- r + gamma * max_a' Q_target(s', a') * (1 - done)
                loss <- huber(Q(s, a), target); update Q
            if steps % target_update == 0: Q_target <- copy(Q)
        until done
```

## 5. Worked Example — CartPole, and what it costs

`dqn.py` contains `train_dqn`, `reinforce`, `actor_critic` and `ppo`, all CPU-capable. A short run is enough
to see the shape of the curve; do not expect a solved CartPole in under a couple of minutes on a laptop.

```python
import dqn

# a deliberately short run: enough to see the curve rise, not enough to solve the task
result = dqn.train_dqn(env_id="CartPole-v1", episodes=60, seed=0)
print("episodes:", len(result["returns"]))
print("first 10 mean:", round(float(result["returns"][:10].mean()), 1))
print("last 10 mean:", round(float(result["returns"][-10:].mean()), 1))
```

If the last-ten mean is not clearly above the first-ten mean, that is a finding: on 60 episodes DQN has
barely started. State it as such rather than tuning until the picture looks good.

## 6. Mathematical Formulation

DQN loss with Huber:

$$L(\theta) = \mathbb{E}_{(s,a,r,s')\sim D}\Big[\mathrm{Huber}\big(r + \gamma\max_{a'}Q_{\theta^-}(s',a') - Q_\theta(s,a)\big)\Big]$$

Advantage and actor–critic gradient:

$$A(s,a) = Q(s,a) - V(s), \qquad \nabla_\theta J \approx \mathbb{E}\big[\nabla_\theta\log\pi_\theta(a\mid s)A(s,a)\big]$$

## 7. Python Implementation

```python
import numpy as np
import dqn, rl_envs

# the network and buffer are ordinary PyTorch pieces
net = dqn.QNet(obs_dim=4, n_actions=2)
print("parameters:", sum(p.numel() for p in net.parameters()))

buffer = dqn.ReplayBuffer(capacity=1000)
for i in range(10):
    buffer.add(np.zeros(4), 0, 1.0, np.ones(4), False)
print("buffer size:", buffer.size)

print("epsilon at step 0:", dqn.epsilon_schedule(0))
print("epsilon at step 2000:", round(dqn.epsilon_schedule(2000), 3))
```

## 8. Practical Applications

- **Continuous control** — PPO is the workhorse for locomotion and manipulation.
- **Game playing** — DQN's replay-and-target recipe generalised across Atari.
- **Recommender systems** — policy gradients for sequential engagement, with careful offline evaluation.
- **Simulation-based optimisation** — HVAC and datacentre control, where a simulator is the environment.

## 9. Common Mistakes

1. No target network, then interpreting divergence as "DQN is unstable".
2. Replay buffer with too few samples, so batches are effectively one trajectory.
3. Reporting a single seed's best run.
4. Forgetting `(1 - done)` in the target, so terminal states bootstrap forever.
5. Comparing wall-clock across implementations instead of environment steps.

## 10. Exercises

1. Remove the target network from `train_dqn` (use `Q` instead of `Q_target`) and describe the curve.
2. Compute the parameter count for `QNet(4, 2)` by hand and check it.
3. Derive REINFORCE's gradient for a two-action softmax policy in three lines.
4. Explain in two sentences why PPO's clip prevents a destructive update.

## 11. Self-Assessment

1. Why does replay decorrelate samples?
   *It replaces consecutive transitions with a random sample from history, approximating i.i.d. draws.*
2. What does the critic provide the actor?
   *A state-dependent baseline, which reduces gradient variance without adding bias.*
3. Why is a single-seed learning curve not evidence?
   *RL variance across seeds is large; one run cannot distinguish a good algorithm from a lucky one.*

## 12. Key Terms

**Function approximation**, **Deep Q-Network**, **experience replay**, **target network**, **policy
gradient**, **REINFORCE**, **actor–critic**, **advantage**, **PPO**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Mnih et al. (2015), "Human-level control through deep reinforcement learning".
- Schulman et al. (2017), "Proximal Policy Optimization Algorithms".

## What to Do Next

Continue to [L10-05 Advanced Reinforcement Learning](L10-05-advanced-reinforcement-learning.md), and complete
[LAB-10-03](../labs/lab-10-03-cartpole-with-deep-q-networks.md).
