# LAB-10-01 — Grid-World Navigation Using Q-Learning

| | |
| :--- | :--- |
| Module | M10 · Reinforcement Learning |
| Level | 400 |
| Time | 2.5 hours |
| Prerequisites | [L10-01](../lessons/L10-01-foundations-of-reinforcement-learning.md), [L10-03](../lessons/L10-03-temporal-difference-learning.md) |
| Environment | the module's bundled gridworlds (no Gymnasium required) |
| Code | `code/rl_envs.py`, `code/tabular.py`, `code/experiments.py` |

[← Module](../README.md) · [Next lab: LAB-10-02 →](lab-10-02-compare-sarsa-and-q-learning.md)

## 1. Learning objectives

- **Formulate** a grid navigation task as an MDP with an explicit reward.
- **Implement** tabular Q-learning and verify it against a dynamic-programming solution.
- **Interpret** a learning curve and a $Q$ table as diagnostics.
- **Quantify** the effect of the exploration rate on final performance.
- **Report** results with seeds, tail means and a random baseline.

## 2. Scenario

A warehouse robot moves on a 4×4 grid from a charging bay to a pick station. It must learn the route from
trial and error, because the floor plan changes between deployments and no labelled trajectories exist.
Every step costs energy; reaching the goal pays 1.0.

You are asked to prove the agent learns a route, not merely that the code runs.

## 3. Problem statement

1. build the 4×4 environment and print its states, actions and rewards;
2. solve it exactly with value iteration (the reference);
3. learn it with tabular Q-learning;
4. compare $Q^*$ from DP with $Q$ learned from experience;
5. sweep $\varepsilon$ over three values and report tail returns;
6. show what greedy-only learning does;
7. state the route the deployed policy takes and its cost.

## 4. Background concepts

- Q-learning target $r + \gamma \max_{a'}Q(s',a')$; terminal states do not bootstrap.
- $\varepsilon$-greedy exploration with a decay schedule.
- Tail mean over the last 50 episodes as the performance measure; the best episode is not a measurement.
- Random-policy return as the floor a learner must beat.

## 5. Dataset information and licensing

No dataset: the environment is generated in code (`experiments.make_grid`, `rl_envs.make_gridworld`). The
gridworlds are course-authored and use no third-party asset. Gymnasium is installed but not required for
this lab; `MDPAdapter` exposes the same `reset`/`step` interface so the code transfers.

## 6. Software requirements

Python 3.10+, NumPy, Matplotlib. CPU only, seconds of compute. No downloads.

## 7. Step-by-step tasks

1. `env = experiments.make_grid(4)`; print `env.reset()` output and `env.step(0)`.
2. Solve exactly: `experiments.value_iteration_solution()`; print the value grid and the greedy policy.
3. Learn: `tabular.q_learning(env, episodes=300, alpha=0.5, gamma=0.9, eps=0.2, seed=0)`.
4. Compare: print the tail return, the greedy path length, and the random baseline.
5. Sweep $\varepsilon \in \{0.01, 0.1, 0.3\}$ at 300 episodes and tabulate tail returns.
6. Run greedy-only ($\varepsilon = 0$) and describe what the agent does instead of learning.
7. Change the step cost from −0.04 to −0.5 and re-learn. Does the route change? Why?
8. Report: the policy, its cost, and the evidence that learning, not luck, produced it.

## 8. Starter code

```python
import numpy as np
import experiments, tabular

env = experiments.make_grid(4)
obs, info = env.reset(seed=0)
print("start observation:", obs, info)

# exact reference
exact = experiments.value_iteration_solution()
print("sweeps to converge:", exact["sweeps"])

# learned agent
run = tabular.q_learning(env, episodes=300, alpha=0.5, gamma=0.9, eps=0.2, seed=0)
print("tail return:", round(experiments.mean_tail(run["returns"]), 3))
print("first 20 returns:", np.round(run["returns"][:20], 2))

path = tabular.greedy_path_from_q(env, run["Q"], start=0)
print("greedy path:", path)

floor = experiments.random_baseline(env, episodes=30, seed=0)["mean"]
print("random baseline:", round(floor, 3))
```

## 9. Expected behaviour

- Value iteration converges in a handful of sweeps on 16 states; the optimal value at the start corner is
  positive and the greedy path reaches the goal.
- Q-learning reaches a tail return of roughly **0.8** (the reachable optimum is 1.0 minus step costs along
  the shortest route) within 300 episodes at $\alpha=0.5$, $\gamma=0.9$, $\varepsilon=0.2$.
- The random baseline is **negative** — it rarely reaches the goal before the step limit.
- $\varepsilon = 0$ learns nothing useful: with no exploration the agent never discovers the goal, and the
  tail return stays at the random floor.

Report your own numbers; expect small variation with library versions and seeds.

## 10. Evaluation metrics

| Metric | Meaning |
| :--- | :--- |
| Tail return (last 50 episodes) | final performance |
| Episode length | route efficiency |
| Random baseline | the floor that proves learning |
| Greedy path length | policy quality, independent of exploration noise |

## 11. Testing instructions

- Assert every return is finite and every episode terminates within the step limit.
- Assert the greedy path ends at the goal state and visits no state twice.
- Re-run with `seed=1`; if the tail return moves by more than 0.15, run more episodes before concluding.
- Confirm `python code/experiments.py` prints `experiments self-test: True`.
- Check that `q["Q"]` has at least one entry per visited state.

## 12. Submission requirements

Code, the value grid, the learned policy as arrows, the $\varepsilon$ sweep table, and a paragraph
explaining why the greedy-only run fails. State seeds, episode counts and the tail window.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| MDP formulation | 20% | states, actions, rewards and discount stated explicitly |
| Implementation | 25% | correct terminal handling, reproducible seeds |
| Comparison with DP | 20% | learned values checked against the exact solution |
| Experimentation | 20% | $\varepsilon$ sweep, baseline, tail means, seed check |
| Explanation | 15% | greedy-only failure diagnosed, not just reported |

## 14. Extension challenges

1. **Optimistic initialisation.** Set `q_init` above the best possible return and run with $\varepsilon=0$.
   Does exploration emerge? Why?
2. **Reward shaping.** Add a small penalty for revisiting a state and check whether the optimal route changes.
3. **State aliasing.** Remove the row coordinate from the observation and describe the failure.
4. **Bigger grid.** Try 8×8 and report how episodes-to-converge scales.

## Reflection

Q-learning is four lines of arithmetic. The lab's value is in the comparison: against DP for correctness,
against random for evidence, and against a second seed for honesty.
