# PA-10 — Q-Learning, Then DQN, on the Same Task

| | |
| :--- | :--- |
| Assignment | 10 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M10 (L10-02 … L10-07), PA-07 |
| Covers | MDPs, tabular Q-learning, function approximation, learning curves, reward design |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

Tabular Q-learning is easy to get working on a gridworld and easy to break when the state space grows.
This assignment makes you solve the same task twice — once with a table, once with a network — and
report where the second one fails and why.

## Problem scenario

A 6×6 gridworld with a goal, a pit and a wall. Reward: −0.01 per step, +1 goal, −1 pit, episode ends
after 100 steps. Part 2 uses a continuous-state variant (position plus velocity) that makes a table
impractical.

## Learning outcomes

1. Implement Q-learning with ε-greedy exploration and a decaying schedule.
2. Diagnose instability in function approximation.
3. Design and critique a reward function.
4. Report learning curves over seeds, not single runs.

## Tasks

1. **Tabular.** Q-learning on the discrete grid; report the greedy policy and steps-to-goal.
2. **Seeds.** Five seeds; plot mean and range of episode return.
3. **Sensitivity.** Vary α, γ and the ε schedule; report which matters most and why.
4. **Reward design.** Add a shaping term for moving toward the goal; report the policy change and
   whether it is desirable.
5. **DQN.** Function approximation on the continuous variant; report stability problems you observe.
6. **Diagnosis.** Explain one failure mechanistically (e.g. moving-target instability).

## Constraints

- No RL libraries; implement the update yourself.
- Fixed environment seeds across algorithms.
- Report compute time.

## Expected deliverables

`qlearning.py`, `dqn.py`, `curves.png`, `results.md`, and a short reward-design critique.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Tabular implementation | 25% | correct update, converges, policy sensible |
| Experimental discipline | 25% | five seeds, ranges shown |
| Hyperparameter study | 20% | effects measured, not listed |
| DQN and diagnosis | 20% | failure identified mechanistically |
| Reward critique | 10% | shaping analysed for unintended policy |

## Bonus challenges

- Implement double Q-learning and report the overestimation change.
- Compare ε-greedy with Boltzmann exploration at equal compute.

---

[Assessment index](../README.md) · [PA-09](pa-09-computer-vision.md) · [PA-11](pa-11-generative-ai.md)
