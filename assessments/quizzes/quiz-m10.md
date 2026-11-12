# QUIZ-M10 — Reinforcement Learning

| | |
| :--- | :--- |
| Module | M10 · Reinforcement Learning |
| Questions | 10 (20 marks) |
| Time | 40 minutes |
| Covers | L10-01 … L10-07 |
| Pass mark | 12 / 20 |

> **Availability.** M10 (Reinforcement Learning) — reference code only in this repository, so this paper cannot be attempted
> yet. It is included so the assessment set is complete, and it is a preview
> rather than an assessment until the module's lessons are published.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m10.md)

---

## Part A — Multiple choice (4 marks)

**Q10.1** A discount factor $\gamma$ close to 1 makes the agent

- A. ignore future rewards
- B. value future rewards almost as much as immediate ones
- C. explore more
- D. converge faster in all cases

**Q10.2** Q-learning is

- A. on-policy
- B. off-policy
- C. a policy-gradient method
- D. model-based

**Q10.3** The exploration–exploitation trade-off exists because

- A. the reward function is unknown
- B. the agent must gather information about actions whose value it does not know
- C. environments are non-stationary
- D. the state space is continuous

**Q10.4** Reward shaping risks

- A. slowing convergence only
- B. changing the optimal policy away from the intended one
- C. increasing the state space
- D. removing the need for exploration

## Part B — True or false, with a reason (2 marks)

**Q10.5** "A policy that is greedy with respect to a converged Q-function still needs exploration."

## Part C — Conceptual (4 marks)

**Q10.6** (2 marks) Explain the credit-assignment problem in one paragraph, with the maze example.

**Q10.7** (2 marks) Why can a DQN's learning curve rise and then collapse? Name one mechanism and
one mitigation.

## Part D — Numerical (6 marks)

**Q10.8** (3 marks) Rewards $r_0=1$, $r_1=0$, $r_2=2$ with $\gamma=0.9$. Compute the return
$G_0$.

**Q10.9** (3 marks) Q-learning update with $\alpha=0.5$, $\gamma=0.9$, current $Q(s,a)=2$, reward
$r=1$, and $\max_{a'}Q(s',a')=4$. Compute the new $Q(s,a)$.

## Part E — Tracing (2 marks)

**Q10.10** Value iteration for one state with two actions: action A leads to reward 1 and a
terminal state; action B leads to reward 0 and a state whose value is 5. With $\gamma=0.9$, which
action does one Bellman backup choose?

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m10.md) · [Next quiz](quiz-m11.md)
