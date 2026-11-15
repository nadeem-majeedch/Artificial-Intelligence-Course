# LAB-10-04 — Policy-Based Learning and PPO Introduction

| | |
| :--- | :--- |
| Module | M10 · Reinforcement Learning |
| Level | 400 |
| Time | 3 hours |
| Prerequisites | [L10-04](../lessons/L10-04-deep-reinforcement-learning.md), LAB-10-03 |
| Environment | `CartPole-v1` or the bundled `RobotNavEnv` |
| Code | `code/dqn.py` (`reinforce`, `actor_critic`, `ppo`) |

[← LAB-10-03](lab-10-03-cartpole-with-deep-q-networks.md) · [Module home](../README.md)

## 1. Learning objectives

- **Derive** the REINFORCE gradient and implement it without a value function.
- **Add** a baseline and show the variance reduction empirically.
- **Implement** an actor–critic update with an advantage.
- **Explain** PPO's clip as a trust region and observe its effect on update size.
- **Compare** value-based and policy-based learning on the same task with the same budget.

## 2. Scenario

The control team from LAB-10-03 now needs a policy that can be extended to continuous actions. Value-based
methods require a max over actions, which is awkward for a real-valued torque. A policy network outputs the
action distribution directly.

Your task is to see what that buys and what it costs in variance.

## 3. Problem statement

1. train REINFORCE and record the return curve and the gradient-norm proxy (mean return variance);
2. add a learned baseline (actor–critic) and compare curves;
3. run PPO with the same budget and compare sample efficiency;
4. measure how far the policy moves per update (KL or ratio spread);
5. compare against DQN from LAB-10-03 on the same environment and budget;
6. state which method you would choose for a continuous-action task, and why.

## 4. Background concepts

- $\nabla_\theta J = \mathbb{E}[\nabla_\theta\log\pi_\theta(a\mid s)G_t]$ — REINFORCE.
- Baseline subtraction leaves the gradient unbiased and reduces variance.
- Advantage $A = r + \gamma V(s') - V(s)$; actor–critic trains both heads.
- PPO clips the importance ratio $\rho$ to $[1-\epsilon, 1+\epsilon]$ so one batch cannot move the policy far.
- Entropy bonus keeps early exploration alive.

## 5. Dataset information and licensing

Same as LAB-10-03: Gymnasium's CartPole (MIT) generates episodes; nothing is downloaded. The bundled
`RobotNavEnv` is a fallback with the same interface. Record which environment you used and its version.

## 6. Software requirements

Python 3.10+, NumPy, PyTorch (CPU), Matplotlib, Gymnasium (optional). REINFORCE on CartPole needs a few
hundred episodes; keep budgets identical across methods or the comparison is meaningless.

## 7. Step-by-step tasks

1. Read `dqn.reinforce` and identify where the return is computed and where the baseline would enter.
2. Train REINFORCE for a fixed budget; plot the curve and the per-episode return variance.
3. Train `dqn.actor_critic` on the same budget; compare smoothed curves and variance.
4. Train `dqn.ppo` on the same budget; record episodes-to-threshold if it reaches one.
5. Compute the mean absolute policy-ratio deviation per PPO update (or a KL proxy) and describe what the
   clip is preventing.
6. Put DQN, REINFORCE, actor–critic and PPO in one table: budget, tail return, seed spread, wall-clock.
7. Write the recommendation for a continuous-action task in five sentences, citing your table.

## 8. Starter code

```python
import numpy as np
import dqn

result = dqn.reinforce(env_id="CartPole-v1", episodes=120, seed=0)
returns = np.asarray(result["returns"])
print("REINFORCE first/last 20:", round(float(returns[:20].mean()), 1),
      round(float(returns[-20:].mean()), 1))
print("return std (last 20):", round(float(returns[-20:].std()), 1))

ac = dqn.actor_critic(env_id="CartPole-v1", episodes=120, seed=0)
print("actor-critic last 20:", round(float(np.asarray(ac["returns"])[-20:].mean()), 1))

ppo = dqn.ppo(env_id="CartPole-v1", episodes=120, seed=0)
print("PPO last 20:", round(float(np.asarray(ppo["returns"])[-20:].mean()), 1))
```

## 9. Expected behaviour

- REINFORCE improves slowly and noisily: the last-20 mean should exceed the first-20 mean, with a large
  standard deviation.
- Actor–critic is usually smoother at the same budget because the baseline removes return-scale variance.
- PPO typically reaches a higher tail return than REINFORCE within the same number of episodes, though on a
  short budget the difference can be inside the seed noise — report the spread, not just the mean.
- If any method fails to beat the random floor, that is the result: state the budget and what you would
  change.

Do not copy numbers from this page into your report. Run it.

## 10. Evaluation metrics

| Metric | Meaning |
| :--- | :--- |
| Tail return | performance at the budget |
| Return standard deviation | stability |
| Episodes-to-threshold | sample efficiency |
| Ratio spread / KL proxy | how far each update moves the policy |

## 11. Testing instructions

- Assert all runs return arrays with one value per episode.
- Assert log-probabilities and entropies have matching shapes in your own implementation.
- Use identical budgets and seeds across methods; note any deviation.
- Check that PPO's clip is active: log the fraction of ratios outside $[1-\epsilon, 1+\epsilon]$.
- If CartPole cannot be created, use `rl_envs.RobotNavEnv` and record the substitution.

## 12. Submission requirements

Four curves on one axis, the comparison table with seed spread, the ratio/clip diagnostic, and the
recommendation. State budgets, seeds, versions and hardware.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Correct policy-gradient implementation | 25% | return and baseline handled correctly |
| Controlled comparison | 25% | identical budgets and seeds |
| Diagnostic evidence | 25% | clip/KL measured, variance quantified |
| Interpretation | 15% | recommendations grounded in the table |
| Reproducibility | 10% | exact commands and versions given |

## 14. Extension challenges

1. **Entropy coefficient.** Sweep it on PPO and describe the exploration/performance trade-off.
2. **Continuous actions.** Replace the categorical head with a Gaussian and run on `Pendulum-v1`.
3. **Reward normalisation.** Scale returns before the policy-gradient update and measure stability.
4. **Off-policy check.** Feed PPO data collected by a different policy and show why the ratio correction
   matters.

## Reflection

Policy gradients optimise what you deploy — the policy — instead of deriving it from values. The price is
variance, and the lab's numbers are the receipt: baselines and clipping are not refinements, they are what
make the method usable.
