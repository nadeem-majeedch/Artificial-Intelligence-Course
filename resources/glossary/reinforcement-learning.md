# Glossary — Reinforcement Learning (M10)

M10 has reference code but no published lessons, so entries link to the module page and are
marked **module page only**. Back to the [glossary index](README.md).

## A

### Action value
**Abbreviation.** $Q(s,a)$ · **Module.** M10
**Simple definition.** The expected return from taking action $a$ in state $s$ and then acting
well.
**Detailed explanation.** The action-value function is what an agent needs to choose: it ranks
actions within a state. Q-learning estimates it directly, while actor–critic methods learn it as
a critic to reduce the variance of policy gradients.
**Mathematics.** $Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a]$
**Practical example.** In a grid world, $Q(\text{start}, \text{right}) = 2.62$ versus
$Q(\text{start}, \text{down}) = 1.9$ makes the first move preferable before any exploration.
**Related.** [Q-learning](#q-learning), [Policy](#policy), [Return](#return)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## D

### Discount factor
**Abbreviation.** $\gamma$ · **Module.** M10
**Simple definition.** How much future rewards are worth relative to immediate ones.
**Detailed explanation.** With $\gamma < 1$ the return is finite and the agent prefers sooner
rewards; $\gamma = 1$ is used for episodic tasks with guaranteed termination. The value is a
design choice about patience, not a property of the world.
**Mathematics.** $G_t = \sum_{k=0}^{\infty}\gamma^k R_{t+k+1}$
**Practical example.** At $\gamma = 0.9$, a reward 10 steps away is worth $0.35$ of the same
reward now; at $\gamma = 0.99$ it is worth $0.90$.
**Related.** [Return](#return), [Markov decision process](classical-ai.md#markov-decision-process)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## E

### Exploration–exploitation
**Abbreviation.** — · **Module.** M10
**Simple definition.** The choice between trying unknown actions and using the best known one.
**Detailed explanation.** Exploiting only what is known locks in a suboptimal policy; exploring
forever never profits. $\epsilon$-greedy is the simplest schedule, UCB is principled, and
Thompson sampling is usually strongest in bandits.
**Mathematics.** $\epsilon$-greedy: with probability $1-\epsilon$ take $\arg\max_a Q(s,a)$, else random.
**Practical example.** A recommender that always shows the current best article never discovers
that a new article would retain better; $\epsilon = 0.1$ costs 10% of clicks to learn.
**Related.** [Multi-armed bandit](#multi-armed-bandit), [Policy](#policy), [Q-learning](#q-learning)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## M

### Multi-armed bandit
**Abbreviation.** MAB · **Module.** M10
**Simple definition.** A one-state decision problem: choose among actions with unknown reward
distributions to maximise total reward.
**Detailed explanation.** The bandit strips away state, leaving only the exploration problem.
It is the right model for A/B tests, ad allocation and pricing, where actions do not change the
world.
**Mathematics.** Regret $= T\mu^* - \sum_{t=1}^{T}\mu_{a_t}$; UCB regret grows as $O(\log T)$.
**Practical example.** Three checkout layouts with true conversion 4.1%, 4.4% and 4.6%; a
Thompson-sampling policy loses about a third less traffic than a fixed 50/50 test.
**Related.** [Exploration–exploitation](#explorationexploitation), [Policy](#policy)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## P

### Policy
**Abbreviation.** $\pi$ · **Module.** M10
**Simple definition.** The rule an agent follows to choose actions in each state.
**Detailed explanation.** A policy can be a lookup table, a function approximator or a
distribution. Policy-gradient methods optimise it directly; value-based methods derive it from
estimated values. The distinction matters because direct policy optimisation handles continuous
actions and stochastic optimal policies.
**Mathematics.** $\pi(a \mid s) = P(A_t = a \mid S_t = s)$
**Practical example.** A warehouse robot policy maps 400 sensor states to 4 movements; training
raises mean episode reward from 12 to 87.
**Related.** [Action value](#action-value), [Q-learning](#q-learning), [Exploration–exploitation](#explorationexploitation)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## Q

### Q-learning
**Abbreviation.** — · **Module.** M10
**Simple definition.** An off-policy method that learns action values by bootstrapping from the
best next action.
**Detailed explanation.** Q-learning updates toward the maximum over next actions regardless of
what the agent actually did, so it can learn the optimal policy while exploring. It converges in
tabular settings given sufficient visitation; function approximation can diverge.
**Mathematics.** $Q(s,a) \leftarrow Q(s,a) + \alpha\left[r + \gamma\max_{a'}Q(s',a') - Q(s,a)\right]$
**Practical example.** With $Q = 2$, reward 1, $\gamma = 0.9$ and $\max_{a'}Q(s',a') = 4$, the
target is $1 + 3.6 = 4.6$; at $\alpha = 0.5$ the new value is 3.3.
**Related.** [Action value](#action-value), [Policy](#policy), [Temporal difference](#temporal-difference)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## R

### Return
**Abbreviation.** $G_t$ · **Module.** M10
**Simple definition.** The discounted sum of rewards from a time step onward.
**Detailed explanation.** The return is what the agent maximises; it makes the trade-off between
immediate and future reward explicit through $\gamma$. Value functions are expectations of it.
**Mathematics.** $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots$
**Practical example.** Rewards 1, 0, 2 at $\gamma = 0.9$ give $G = 1 + 0 + 1.62 = 2.62$.
**Related.** [Discount factor](#discount-factor), [Action value](#action-value)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## T

### Temporal difference
**Abbreviation.** TD · **Module.** M10
**Simple definition.** Learning a value estimate from a later value estimate instead of waiting
for the true return.
**Detailed explanation.** TD bootstraps: it updates toward $r + \gamma V(s')$, trading the
variance of Monte Carlo returns for the bias of an imperfect estimate. TD(0) is the simplest
form and the basis of Q-learning.
**Mathematics.** $V(s) \leftarrow V(s) + \alpha[r + \gamma V(s') - V(s)]$
**Practical example.** A grid-world agent updates values after every step, learning a usable
policy in 200 episodes where Monte Carlo needs 2,000.
**Related.** [Q-learning](#q-learning), [Action value](#action-value)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

## V

### Value function
**Abbreviation.** $V(s)$ · **Module.** M10
**Simple definition.** The expected return from being in a state and following a policy.
**Detailed explanation.** Values summarise the future in one number per state, which is what makes
planning tractable. Policy evaluation computes $V^\pi$; policy iteration alternates evaluation and
improvement.
**Mathematics.** $V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$
**Practical example.** A maintenance MDP values "serviced last month" at 2.6 and "overdue" at
−1.4, so the optimal action changes with state alone.
**Related.** [Action value](#action-value), [Policy](#policy), [Markov decision process](classical-ai.md#markov-decision-process)
**Where it is taught.** Module page only — [M10 Reinforcement Learning](../../modules/M10-reinforcement-learning/README.md)

---

[Glossary index](README.md) · [NLP and vision](nlp-and-vision.md) · [Generative AI](generative-ai.md) · [Quick reference](../glossary.md)
