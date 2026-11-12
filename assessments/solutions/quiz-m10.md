# QUIZ-M10 — Solutions and Explanations

> **Availability.** M10 (Reinforcement Learning) — reference code only in this repository, so this paper cannot be attempted
> yet. It is included so the assessment set is complete, and it is a preview
> rather than an assessment until the module's lessons are published.

[Quiz](quiz-m10.md) · [Assessment index](../README.md)

---

## Part A

**Q10.1 — B.** $\gamma\to1$ means future rewards are discounted very little, so the agent is
far-sighted. $\gamma\to0$ gives a myopic agent (A). Discounting does not control exploration.

**Q10.2 — B.** Q-learning updates toward $\max_{a'}Q(s',a')$ regardless of the behaviour policy, so
it learns the optimal policy off-policy. SARSA, which uses the action actually taken, is on-policy.

**Q10.3 — B.** The agent cannot know an action's value without trying it, but trying costs reward.
The trade-off is about information, not about unknown rewards per se.

**Q10.4 — B.** A poorly designed shaping term can make a different policy optimal — the agent
optimises the shaped reward, not your intention. Classic example: a bonus for visiting a location
creates a policy that circles it forever.

## Part B

**Q10.5 — False.** A converged Q-function already encodes the best action at each state, so a
greedy policy is optimal *for that Q*. Exploration is needed during learning; after convergence,
greedy behaviour is the point. (Caveat worth a mark: in a non-stationary environment the Q-function
does not stay converged.)

## Part C

**Q10.6 — Model answer.** In a maze the agent may wander for many steps before the goal reward
arrives. Assigning credit for that reward to the actions that actually helped, rather than to the
hundreds of irrelevant steps, is the credit-assignment problem. Discounting, eligibility traces and
bootstrapping (TD) are the mechanisms that spread credit backwards.

**Q10.7 — Model answer.** Mechanism: the replay buffer fills with highly correlated, early
experiences and the target network lags, so the Q-function overshoots and then collapses
(catastrophic forgetting of earlier states). Mitigation: a target network updated slowly, gradient
clipping, or a larger, more diverse replay buffer.

## Part D

**Q10.8 —** $G_0=1+0.9(0)+0.9^2(2)=1+0+1.62=2.62$.

**Q10.9 —** Target $=r+\gamma\max_{a'}Q(s',a')=1+0.9(4)=4.6$. Update
$Q\leftarrow2+0.5(4.6-2)=2+1.3=3.3$.

## Part E

**Q10.10 —** One backup compares $Q(A)=1+0.9(0)=1$ with $Q(B)=0+0.9(5)=4.5$. Action B is chosen.
This is the key insight of dynamic programming: an action with no immediate reward can be optimal
because of where it leads.

---

[Quiz](quiz-m10.md) · [Previous solutions](quiz-m09.md) · [Assessment index](../README.md)
