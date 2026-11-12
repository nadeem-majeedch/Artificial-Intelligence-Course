# SA-M10 — Self-Assessment: Reinforcement Learning

Module M10 · [Module](../../docs/CURRICULUM-MAP.md) · [Quiz](../quizzes/quiz-m10.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Define the agent–environment loop with states, actions, rewards and transitions
- [ ] Write the return and explain the discount factor
- [ ] State the Bellman expectation and optimality equations
- [ ] Distinguish policy evaluation from policy improvement
- [ ] Explain on-policy vs off-policy with an example
- [ ] Describe the exploration–exploitation trade-off
- [ ] Explain why reward shaping can change the optimal policy

## Knowledge-check questions

1. Compute $G_0$ for rewards $[2,0,1]$ with $\gamma=0.5$.
2. Why does Q-learning converge to the optimal policy while following an exploratory one?
3. What goes wrong if $\gamma=0$ in a task with delayed reward?
4. Why is a high average reward compatible with a bad policy?
5. What is the moving-target problem in DQN?

## Practical competency checklist

- [ ] Implement and debug a tabular Q-learning agent
- [ ] Plot learning curves over multiple seeds
- [ ] Diagnose non-learning (reward scale, exploration, bug) systematically
- [ ] Write a reward function and state its failure modes

## Suggested revision topics

MDPs · returns and discounting · Bellman equations · dynamic programming · Monte Carlo vs TD ·
Q-learning and SARSA · function approximation · reward design.

## Readiness test for M11

Without notes:

1. Perform one Bellman backup on a two-action state.
2. Compute a Q-learning update with given α, γ, r and max Q.
3. Explain why an agent can be optimal and still look erratic while learning.

If any is shaky, revisit L10-03 and L10-05 before M11.
