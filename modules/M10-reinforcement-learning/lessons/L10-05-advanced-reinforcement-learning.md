# L10-05 — Advanced Reinforcement Learning

| Module | M10 · Reinforcement Learning |
| :--- | :--- |
| Level | 400 |
| Study time | 80 minutes |
| Prerequisites | [L10-04](L10-04-deep-reinforcement-learning.md) |
| Code | `code/dqn.py`, `code/rl_envs.py` |

[← Previous: L10-04](L10-04-deep-reinforcement-learning.md) · [Module home](../README.md)

## 1. Learning Objectives

- **Handle** continuous action spaces and say why a max over actions is no longer available.
- **Distinguish** on-policy, off-policy and offline learning by their data requirements.
- **Diagnose** reward hacking and propose a test that would have caught it.
- **Describe** the two dominant failure modes of multi-agent learning.
- **State** the safety and evaluation limits of a learned policy before deployment.

## 2. Prerequisite Knowledge

DQN, policy gradients and PPO from [L10-04](L10-04-deep-reinforcement-learning.md).

## 3. Conceptual Explanation

### 3.1 Continuous actions

A robot joint has a real-valued torque. Three standard responses:

1. **Discretise** — simple, and the cost is exponential in the number of dimensions.
2. **Deterministic policy gradient (DDPG/TD3)** — learn $\mu_\theta(s)$ directly and backpropagate through
   $Q$; add noise for exploration.
3. **Stochastic policy (SAC/PPO)** — output a distribution (Gaussian) and sample; entropy regularisation
   keeps exploration alive.

SAC's entropy term $-\alpha \log \pi(a\mid s)$ is a principled exploration bonus: maximise reward *and*
uncertainty, and anneal the trade-off.

### 3.2 Offline RL

Offline RL learns from a fixed dataset with no interaction. The central problem is distribution shift: the
learned policy prefers actions the dataset never took, and the value estimate for those actions is
unconstrained. Solutions constrain the policy to the data (behaviour cloning regularisation, conservative
value penalties) or estimate uncertainty. **Never evaluate an offline policy only on the dataset** — it will
look excellent, because the dataset contains the good outcomes it was fitted to.

### 3.3 Reward design and reward hacking

Every reward is a proxy, and agents optimise the proxy exactly. Classic failures:

| Intended goal | Reward written | What the agent did |
| :--- | :--- | :--- |
| Clean a room | small penalty per dirty spot | covered the sensor instead |
| Fast lap | time bonus | drove in circles off-track where the timer did not apply |
| Keep traffic flowing | queue length | shortened green so queues were never measured |

The defence is procedural, not mathematical: specify the reward, then specify the *test* that would catch
the failure, then check the policy's behaviour on held-out scenarios. Potential-based shaping (L10-03) is
the only shaping with a policy-invariance guarantee.

### 3.4 Multi-agent learning

Two failure modes dominate. **Non-stationarity**: each agent's environment includes the others, so the MDP
assumption fails and naive Q-learning oscillates. **Credit assignment across agents**: a team reward gives
no signal about which agent helped. Independent learners work in cooperative settings with shared
observation; centralised training with decentralised execution (CTDE) is the standard compromise.

### 3.5 Safety and evaluation

A learned policy is a hypothesis tested on a distribution. Before deployment you need: evaluation on
held-out seeds and perturbations, a random and a scripted baseline, a shutdown path, and a monitoring
signal. High average reward with occasional catastrophic episodes is not a good policy for a physical
system — look at the tail, not the mean.

## 4. Pseudocode

```text
function EVALUATE_POLICY(policy, envs, seeds, perturbations):
    results <- []
    for env in envs, seed in seeds:
        for perturbation in perturbations:
            G <- rollout(policy, perturb(env, perturbation), seed)
            results.append(G)
    return median(results), quantile(results, 0.05), max_episode_cost(results)
```

## 5. Worked Example — the same policy under perturbation

```python
import numpy as np
import experiments, tabular

q = tabular.q_learning(experiments.make_grid(4), episodes=400, alpha=0.5, gamma=0.9, eps=0.2, seed=0)
Q = q["Q"]
policy = lambda s: tabular.greedy_action(Q, s, 4)

clean = tabular.evaluate(experiments.make_grid(4, slip=0.0), policy, episodes=50, seed=0)
slippery = tabular.evaluate(experiments.make_grid(4, slip=0.3), policy, episodes=50, seed=0)
print("clean:  return", round(clean["return"], 3), "success", round(clean["success"], 2))
print("slippery: return", round(slippery["return"], 3), "success", round(slippery["success"], 2))
```

A policy trained without slip degrades when the environment becomes stochastic. That gap is the number a
deployment review should ask for.

## 6. Mathematical Formulation

Entropy-regularised objective (SAC):

$$J(\pi) = \mathbb{E}\Big[\sum_t \gamma^t\big(r_t + \alpha\,\mathcal{H}(\pi(\cdot\mid s_t))\big)\Big]$$

Offline constraint (behaviour-regularised):

$$\max_\theta\ \mathbb{E}_{(s,a)\sim D}\big[Q_\theta(s,a)\big] \quad
\text{s.t.}\ \mathbb{E}_{s\sim D}\big[D_{KL}(\pi_\theta(\cdot\mid s)\,\|\,\pi_\beta(\cdot\mid s))\big] \le \epsilon$$

## 7. Python Implementation

```python
import numpy as np
import rl_envs

# the module ships three small environments; each has a documented reward and observation
env = rl_envs.TrafficSignalEnv()
obs, info = env.reset(seed=0)
print("observation:", obs, "info:", info)
for _ in range(5):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    print(round(float(reward), 3), terminated, truncated, info)

# reward hacking, in miniature: the queue-length reward can be gamed by serving nobody
print("reward definition:", rl_envs.TrafficSignalEnv.__doc__.splitlines()[0])
```

## 8. Practical Applications

- **Energy systems** — HVAC and battery scheduling with hard safety constraints.
- **Robotics** — sim-to-real transfer, where perturbation testing is mandatory.
- **Operations research** — inventory and routing with offline historical data.
- **Education** — adaptive practice scheduling; here the "reward" is learning gain, and the proxy problem
  is severe.

## 9. Common Mistakes

1. Judging an offline policy on its training distribution.
2. Adding reward terms until the curve rises, then discovering the behaviour is wrong.
3. Training multi-agent systems with independent learners and expecting convergence.
4. Reporting the mean episode reward while ignoring the worst-case episode.
5. Treating a solved benchmark as evidence of transfer to a new environment.

## 10. Exercises

1. Take the gridworld policy above and evaluate it at slips 0.0, 0.1 and 0.3. Plot return against slip.
2. Write a reward for "keep the queue short" that cannot be gamed by refusing to serve; explain why.
3. Explain in three sentences why offline RL needs a constraint the online algorithms do not.
4. Design an evaluation protocol for a learned traffic controller: seeds, baselines, perturbations, metrics.

## 11. Self-Assessment

1. Why is discretisation unattractive for a 7-joint arm?
   *Seven dimensions at even five bins each is $5^7$ actions per step.*
2. What is reward hacking, in one sentence?
   *Optimising the measured proxy in a way that defeats the intended goal.*
3. Why is a high mean return insufficient evidence of a safe policy?
   *Rare catastrophic episodes barely move the mean but decide the deployment decision.*

## 12. Key Terms

**Continuous action space**, **deterministic policy gradient**, **SAC**, **offline RL**,
**behaviour cloning**, **reward hacking**, **multi-agent RL**, **sim-to-real**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Levine et al. (2020), "Offline Reinforcement Learning: Tutorial, Review, and Perspectives".
- Amodei et al. (2016), "Concrete Problems in AI Safety" — the specification-gaming section.

## What to Do Next

Complete [LAB-10-04](../labs/lab-10-04-policy-based-learning-and-ppo-introduction.md), then attempt
[PA-10](../../../assessments/programming/pa-10-reinforcement-learning.md) and the
[quiz](../../../assessments/quizzes/quiz-m10.md). The module project is
[MP-10](../projects/mp-10-inventory-control-agent.md) if your programme includes it.
