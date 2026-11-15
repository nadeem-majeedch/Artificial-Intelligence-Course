# LAB-10-02 — Compare SARSA and Q-Learning

| | |
| :--- | :--- |
| Module | M10 · Reinforcement Learning |
| Level | 400 |
| Time | 2.5 hours |
| Prerequisites | [L10-03](../lessons/L10-03-temporal-difference-learning.md) |
| Environment | cliff walking (Sutton & Barto figure 6.4) |
| Code | `code/tabular.py`, `code/experiments.py` |

[← LAB-10-01](lab-10-01-grid-world-navigation-using-q-learning.md) · [Next lab: LAB-10-03 →](lab-10-03-cartpole-with-deep-q-networks.md)

## 1. Learning objectives

- **Implement** SARSA and Q-learning from the same skeleton and name the single line that differs.
- **Measure** the on-policy / off-policy difference on a task designed to expose it.
- **Explain** why the better *online* return is not the better *greedy* policy.
- **Use** multi-seed averages and tail windows rather than single runs.
- **Choose** an algorithm from deployment conditions, not from a leaderboard.

## 2. Scenario

A delivery robot crosses a warehouse aisle with a loading pit along one edge. Falling in costs a day of
downtime; every step costs a little. The robot will keep exploring while it runs, so the policy that
maximises reward *while exploring* may differ from the shortest path.

That is exactly the cliff-walking trade-off, and it is the lab.

## 3. Problem statement

1. run both algorithms for 300 episodes at $\alpha = 0.5$, $\gamma = 0.95$, $\varepsilon = 0.1$;
2. report tail returns per seed and their mean;
3. extract the greedy path each algorithm learned and compare their routes;
4. sweep $\varepsilon \in \{0.01, 0.1, 0.3\}$ and show how the ordering behaves;
5. explain when you would deploy each algorithm;
6. state the limitation of a 300-episode comparison.

## 4. Background concepts

- SARSA target: $r + \gamma Q(s',a')$ with $a'$ sampled from the behaviour policy.
- Q-learning target: $r + \gamma\max_{a'}Q(s',a')$.
- Online return measures the behaviour policy; greedy evaluation measures the target policy. They are
  different questions.
- Cliff walking: 4×12 grid, −1 per step, −100 and episode end on the cliff, goal at bottom-right.

## 5. Dataset information and licensing

No dataset; the environment is generated in code. The task reproduces Sutton and Barto's figure 6.4 for
teaching purposes, with the same reward structure. No third-party asset is used.

## 6. Software requirements

Python 3.10+, NumPy, Matplotlib. CPU only; both algorithms finish 300 episodes in a few seconds. No
downloads, no Gymnasium requirement.

## 7. Step-by-step tasks

1. Print the cliff environment's reward structure by stepping into the cliff deliberately.
2. Run `experiments.compare_sarsa_qlearning(episodes=300, seeds=(0,1,2))` and record the tails.
3. Plot both learning curves on one axis (smoothed with a 20-episode window) and note where they separate.
4. Extract `greedy_path_from_q` for each algorithm's final $Q$ and compare route lengths and proximity to
   the cliff.
5. Sweep $\varepsilon$ and repeat step 2 at each value. Does the ordering change at $\varepsilon=0.01$?
6. Write the deployment recommendation: which algorithm for a robot that explores at runtime, which for a
   system that acts greedily after training.
7. State what 300 episodes cannot tell you.

## 8. Starter code

```python
import numpy as np
import experiments, tabular

result = experiments.compare_sarsa_qlearning(episodes=300, seeds=(0, 1, 2))
print("SARSA tail:      ", round(result["sarsa_tail"], 2))
print("Q-learning tail: ", round(result["q_learning_tail"], 2))
print("per seed:", {k: [round(v, 1) for v in vals] for k, vals in result["tail_per_seed"].items()})

env = experiments.make_cliff()
for name in ("sarsa_Q", "q_learning_Q"):
    path = tabular.greedy_path_from_q(env, result["last"][name], start=36)
    print(name, "path length:", len(path), "steps:", path[:8])

# one episode of each, to see the behaviour difference directly
for algorithm in (tabular.sarsa, tabular.q_learning):
    run = algorithm(env, episodes=1, alpha=0.5, eps=0.1, seed=0)
    print(algorithm.__name__, "first episode return:", float(run["returns"][0]))
```

## 9. Expected behaviour

- SARSA's tail return is higher: about **−32** versus **−36** for Q-learning at 300 episodes, averaged over
  three seeds. The gap is exploration falling into the cliff on the risky path.
- Q-learning's greedy path hugs the bottom row; SARSA's keeps one row away. Both reach the goal.
- At very low $\varepsilon$ the gap narrows, because exploration no longer visits the cliff often enough to
  punish the risky path.
- Single-seed runs can invert the ordering. That is not a bug in the algorithms; it is why the lab requires
  three seeds.

## 10. Evaluation metrics

| Metric | Measures |
| :--- | :--- |
| Tail return per seed | behaviour-policy performance |
| Mean over seeds | stability of the comparison |
| Greedy path shape | target-policy quality |
| Steps per episode | efficiency under exploration |

## 11. Testing instructions

- Assert both runs return arrays of length `episodes`.
- Assert every Q-table has entries for the start state.
- Confirm the greedy paths end at the goal index and are acyclic.
- Re-run with seeds 3–5; if the ordering flips, report it rather than hiding it.
- Confirm `python code/experiments.py` prints `experiments self-test: True`.

## 12. Submission requirements

Curves, tail table with all seeds, the two routes drawn on the grid, the $\varepsilon$ sweep, and the
deployment recommendation. Include the exact command that reproduces your numbers.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Correct implementations | 25% | the one-line difference identified and tested |
| Measurement discipline | 25% | seeds, tail window, smoothing stated |
| Interpretation | 25% | online vs greedy distinction explained with evidence |
| Experiment design | 15% | $\varepsilon$ sweep and route comparison |
| Communication | 10% | recommendation tied to deployment conditions |

## 14. Extension challenges

1. **Expected SARSA.** Add it to the comparison; does its variance reduction narrow the gap?
2. **Double Q-learning.** Implement it and test whether it removes the maximisation bias on this task.
3. **Safe exploration.** Add a penalty for stepping adjacent to the cliff and see how both algorithms adapt.
4. **Episodic vs continuing.** Truncate episodes at 50 steps and describe what changes in the comparison.

## Reflection

The two algorithms differ by one line, and that line changes which question they answer. The lab's real
skill is stating the question first: "best behaviour while learning" and "best policy after learning" have
different answers, and both are legitimate.
