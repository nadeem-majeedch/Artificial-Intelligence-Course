# LAB-10-03 — CartPole Using Deep Q-Networks

| | |
| :--- | :--- |
| Module | M10 · Reinforcement Learning |
| Level | 400 |
| Time | 3 hours |
| Prerequisites | [L10-04](../lessons/L10-04-deep-reinforcement-learning.md) |
| Environment | `CartPole-v1` (Gymnasium) with a bundled fallback |
| Code | `code/dqn.py`, `code/rl_envs.py` |

[← LAB-10-02](lab-10-02-compare-sarsa-and-q-learning.md) · [Next lab: LAB-10-04 →](lab-10-04-policy-based-learning-and-ppo-introduction.md)

## 1. Learning objectives

- **Replace** a Q table with a neural network and state what breaks.
- **Implement** experience replay and a target network, and ablate each.
- **Read** a noisy learning curve: smoothing, seeds, tail means, random baseline.
- **Diagnose** instability from evidence rather than from intuition.
- **Report** a run that did not solve the task as a finding, not a failure of effort.

## 2. Scenario

A control team wants to balance an inverted pendulum. The state is four continuous numbers, so a table is
out of the question. The team's question is not "can DQN solve CartPole?" — it is "which of the two
stabilisers is doing the work, and how would we know if it stopped working?"

## 3. Problem statement

1. inspect the environment and print one transition;
2. train a DQN for a short budget and record the return curve;
3. ablate the target network and describe the difference;
4. ablate replay (train on consecutive transitions) and describe the difference;
5. compare against a random-policy floor and a scripted baseline;
6. state the budget at which your run would be credible, and what you would change to reach it.

## 4. Background concepts

- DQN loss: Huber between $Q_\theta(s,a)$ and $r + \gamma\max_{a'}Q_{\theta^-}(s',a')$, with terminal
  masking.
- Replay decorrelates samples; the target network freezes the bootstrap target.
- $\varepsilon$ decay from 1.0 to 0.05 over a few thousand environment steps.
- CartPole-v1 returns +1 per step, episode ends at 500 steps or when the pole falls.

## 5. Dataset information and licensing

CartPole is part of Gymnasium (MIT licence) and generates its own episodes; no data is downloaded. If
Gymnasium is unavailable or the environment cannot be created, use the bundled `rl_envs.RobotNavEnv`, which
has the same `reset`/`step` contract and runs without any external package. Record which environment you
used.

## 6. Software requirements

Python 3.10+, NumPy, PyTorch (CPU), Gymnasium 0.29+ (optional but recommended), Matplotlib. A short DQN run
is a few minutes on a laptop CPU; a full solve is longer. No GPU, no downloads beyond the package itself.

## 7. Step-by-step tasks

1. Create the environment; assert `observation_space.shape == (4,)` and `action_space.n == 2`.
2. Print one transition and the reward for a random step.
3. Train with `dqn.train_dqn(episodes=60, seed=0)`; plot the raw and 20-episode-smoothed returns.
4. Repeat with seeds 1 and 2 on the same budget and plot all three.
5. Ablate the target network by editing a copy of the training loop to use `Q` in the target; describe the
   curve.
6. Ablate replay by sampling the last transition instead of a random minibatch; describe the curve.
7. Report the random-policy mean return and the scripted "push in the direction of the pole angle" baseline.
8. Write the credibility paragraph: how many episodes and seeds would you need before claiming a solve?

## 8. Starter code

```python
import numpy as np
import dqn

env_id = "CartPole-v1"
result = dqn.train_dqn(env_id=env_id, episodes=60, seed=0)
returns = np.asarray(result["returns"])
print("episodes:", len(returns))
print("first 10 mean:", round(float(returns[:10].mean()), 1))
print("last 10 mean: ", round(float(returns[-10:].mean()), 1))
print("smoothed tail:", np.round(dqn.smooth(returns, 20)[-5:], 1))

print("epsilon schedule:", [round(dqn.epsilon_schedule(s), 3) for s in (0, 500, 2000, 5000)])
print("network parameters:", sum(p.numel() for p in dqn.QNet(4, 2).parameters()))
```

## 9. Expected behaviour

- The return curve rises but stays noisy: on 60 episodes expect the last-ten mean to be above the first-ten
  mean but far below the 500-step ceiling. A short run demonstrates the machinery, not a solution.
- Removing the target network typically produces a curve that oscillates or collapses; removing replay
  produces slow, high-variance learning. Both effects are visible within a short budget even if the run
  never solves the task.
- The random floor is around 20 steps per episode; a scripted angle-based policy is far higher. Any claim
  must beat both.

State your measured numbers. If your run does not improve on random, report that — it usually means the
budget is too small or `learn_start` is too high for the number of steps taken.

## 10. Evaluation metrics

| Metric | Meaning |
| :--- | :--- |
| Mean episode return (tail) | performance |
| Episodes-to-threshold (e.g. 195) | sample efficiency |
| Seed spread | reliability |
| Ablation deltas | which component matters |

## 11. Testing instructions

- Assert returns are finite and episode lengths never exceed the environment limit.
- Assert the buffer grows and that a minibatch has the expected shapes.
- Confirm the target network is a separate object: `Q_target is not Q`.
- Re-run with three seeds; report the median, not the best.
- If CartPole cannot be created, switch to `rl_envs.RobotNavEnv`, record the substitution and continue.

## 12. Submission requirements

Curves for three seeds, the two ablations, the baseline comparison, and the credibility paragraph. State
environment, version, episodes, seeds, wall-clock and hardware.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Correct DQN implementation | 25% | terminal masking, target sync, replay used correctly |
| Ablations | 25% | each stabiliser isolated with evidence |
| Measurement | 20% | seeds, smoothing, baselines stated |
| Interpretation | 20% | instability diagnosed from the curve |
| Honesty | 10% | short-budget limits stated plainly |

## 14. Extension challenges

1. **Double DQN.** Enable `double=True` and compare sample efficiency.
2. **Reward scaling.** Multiply rewards by 0.1 and describe the effect on learning rate sensitivity.
3. **Replay size.** Compare capacities 1,000 and 50,000; which matters more, capacity or freshness?
4. **Frame stacking.** Replace the state with a two-frame stack on a pixel-free variant and discuss why this
   is the standard fix for partial observability.

## Reflection

DQN is Q-learning with two engineering fixes. The lab is designed so that removing either fix produces a
visible failure, which is the only way to understand why the fixes exist rather than memorising their names.
