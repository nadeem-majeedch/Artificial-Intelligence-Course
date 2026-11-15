# L02-05 — Goal-Based, Utility-Based and Learning Agents

| Module | M02 · Intelligent Agents and Environments |
| :--- | :--- |
| Level | 200 |
| Study time | 90 minutes |
| Prerequisites | [L02-04](L02-04-simple-reflex-and-model-based-agents.md) · [L03-03](../../M03-problem-solving-and-search-algorithms/lessons/L03-03-informed-search-greedy-and-a-star.md) |
| Code | [`code/agents.py`](../code/agents.py) (`GoalBasedAgent`, `UtilityBasedAgent`, `LearningAgent`) |

[← Previous: L02-04](L02-04-simple-reflex-and-model-based-agents.md) · [Module home](../README.md) · [Lab 1](../labs/lab-02-01-intelligent-vacuum-cleaner.md)

## 1. Learning Objectives

- **Implement** a goal-based agent that plans a path to a subgoal and **explain** what planning adds.
- **Implement** a utility-based agent with an explicit, arguable utility function.
- **Implement** a learning agent with a performance element and a learning element.
- **Compare** five architectures on one task and justify a choice with measurements.

## 2. Prerequisite Knowledge

Belief state and the reflex/model-based distinction — [L02-04](L02-04-simple-reflex-and-model-based-agents.md)
— and best-first search, because a goal-based agent plans with it
([L03-03](../../M03-problem-solving-and-search-algorithms/lessons/L03-03-informed-search-greedy-and-a-star.md)).

## 3. Conceptual Explanation

### 3.1 Goal-based agents: add a destination

A model-based agent explores; a goal-based agent has a *subgoal* and searches for a path to it. The
module's `GoalBasedAgent` targets the nearest known dirty cell, using breadth-first search over the
believed map. Goal information changes the question from "what is unvisited?" to "what is the shortest
route to the objective?" — and it is the first architecture that needs a search algorithm at all.

Limitation: a goal is binary. Two goals reachable in 3 and 30 steps are both "achievable", and a
goal-based agent has no way to prefer the nearer one when both satisfy the goal.

### 3.2 Utility-based agents: add a ranking

A utility function maps outcomes to numbers, so any two worlds can be compared — including worlds where
the goal is met with different cost, risk or side effects. `UtilityBasedAgent` scores each neighbour as

$$U(\text{move}) = \underbrace{10 \cdot \mathbb{1}[\text{cell is dirty}]}_{\text{reward}} -
\underbrace{0.4 \cdot d(\text{cell, nearest dirt})}_{\text{travel cost}}$$

and takes the maximum. With uncertain outcomes the same expression uses expected utility, which is
exactly L02-03's MDP objective.

Two notes that matter more than the formula: the weights are a **policy choice**, and a utility-based
agent with a badly chosen utility is a very efficient optimiser of the wrong thing.

### 3.3 Learning agents: add improvement

| Element | Job |
| :--- | :--- |
| Performance element | choose actions (any architecture above) |
| Critic | convert the percept sequence into a reward signal |
| Learning element | revise the policy from that signal |
| Problem generator | propose exploratory actions |

`LearningAgent` keeps a Q-table over compact state keys and updates it after each step:

$$Q(s,a) \leftarrow Q(s,a) + \alpha\left[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\right]$$

The critic is the environment's reward, the learning element is the update, and $\epsilon$-greedy
exploration is the problem generator. Remove any of the four and learning stops working — the most
common failure is a missing critic, i.e. no reward signal to learn from.

### 3.4 Choosing an architecture

| Architecture | Adds | Needs | Fails when |
| :--- | :--- | :--- | :--- |
| Reflex | nothing | full observability, no loops | hidden state, cycles |
| Model-based | belief state | a transition model | the model is wrong |
| Goal-based | search to a subgoal | an explicit goal test | goals need ranking |
| Utility-based | ranking, risk | a utility function | utility is misspecified |
| Learning | improvement | reward, exploration | reward is sparse or gamed |

## 4. Pseudocode

```text
function GOAL-AGENT(belief):
    if goal_test(belief): return DONE
    return first_action_of(BFS(belief, nearest_subgoal))

function UTILITY-AGENT(belief):
    return argmax over a of U(outcome(a, belief))

function LEARNING-AGENT(percept, reward):
    critic: r <- reward
    learning element: Q[s,a] += alpha * (r + gamma * max Q[s'] - Q[s,a])
    performance element: return argmax Q[s] (epsilon-greedy)
```

## 5. Worked Example — one world, five agents

`GridWorld(4, 4, dirt={(1,1),(3,2)}, seed=1)`, 60-step limit, measured with `python code/agents.py`
and the notebook. The percept setting decides what the planner can do, so both are shown.

**Local percept** (`observable="local"`, the realistic setting):

| Agent | What it does | Steps | Cleaned | Score |
| :--- | :--- | ---: | ---: | ---: |
| Random | ignores percepts | 60 | 1 | −34 |
| Reflex | suck-if-dirty, else cycle | 60 | 1 | −49 |
| Model-based | explores unvisited cells | 15 | 2 | 7 |
| Goal-based | explores: no visible goal | 15 | 2 | 7 |
| Utility-based | explores: no scored target | 15 | 2 | 7 |

**Full percept** (`observable="full"`): model-based 15 steps, goal-based **7** steps, score 15. Planning
only pays when the goal is observable — a precise demonstration of L02-03's point that the environment
chooses the architecture.

Under the local percept, 20 learning episodes with `epsilon=0.2` give a mean of −16.6 over the first five
and −0.8 over the last five: improvement, not convergence, exactly as the theory predicts for this
budget. Under the full percept the same experiment gives −13.4 and +5.0.

## 6. Mathematical Formulation

Utility with a travel penalty, and the Q-learning update used by `LearningAgent`
($\alpha$ learning rate, $\gamma$ discount, $\epsilon$ exploration):

$$U(s,a) = R(s,a) - c \cdot d(s'), \qquad
Q(s,a) \leftarrow (1-\alpha)Q(s,a) + \alpha\left[r + \gamma\max_{a'}Q(s',a')\right]$$

Convergence requires every state–action pair to be visited infinitely often (with probability 1) and a
decaying learning rate — neither holds in a 60-step episode, which is why the learning agent *improves*
rather than converges.

## 7. Python Implementation

```python
from environments import GridWorld
from agents import GoalBasedAgent, UtilityBasedAgent, LearningAgent, run_episode

world = GridWorld(width=4, height=4, dirt={(1, 1), (3, 2)}, seed=1)
for factory in (GoalBasedAgent, UtilityBasedAgent):
    world.reset(dirt={(1, 1), (3, 2)})
    print(run_episode(factory(), world))

learner = LearningAgent(epsilon=0.2, seed=0)
scores = []
for episode in range(20):
    world.reset(dirt={(1, 1), (3, 2)})
    scores.append(run_episode(learner, world, learn=True)["performance"])
print("first five:", scores[:5])
print("last five: ", scores[-5:])
```

## 8. Practical Applications

- **Goal-based** — route planners, task bots ("file the report"), test runners with a target state.
- **Utility-based** — dispatch with cost/risk trade-offs, ad ranking, energy-aware HVAC.
- **Learning** — recommendation, robot manipulation, any system with a repeatable reward.

## 9. Common Mistakes

- Giving a goal-based agent a goal it cannot test (no `goal_test`, so "done" is a guess).
- Writing a utility function with hidden units: throughput in items and delay in seconds added directly.
- Learning with no exploration, so the table locks onto the first policy tried.
- Letting the learning element update on the wrong state key, so experience does not transfer.
- Believing more architecture is more capability: each layer must earn its complexity in measurement.

## 10. Exercises

1. Add a second dirt cell to the utility agent's world and show a case where the goal-based route is longer than the utility-based one.
2. Give `LearningAgent` `epsilon=0` from the start and explain the result.
3. Change the travel cost from 0.4 to 2.0 and describe the new behaviour in words before running it.
4. Write the four-element table (performance, critic, learning, problem generator) for a recommendation system.

## 11. Self-Assessment

1. What does a goal-based agent add to a model-based one?
2. Why can a goal-based agent not rank two achievable goals?
3. Name the four components of a learning agent and what breaks without each.
4. When would you deliberately choose a reflex agent over a learning one?

## 12. Key Terms

**Goal test**, **subgoal**, **utility function**, **expected utility**, **performance element**, **critic**, **learning element**, **problem generator**, **Q-learning**, **exploration**.

## 13. Further Reading

- Russell & Norvig, sections 2.4.4–2.4.6 and chapter 22.
- Sutton & Barto, chapter 6 — temporal-difference learning.

## What to Do Next

Work [LAB-02-01](../labs/lab-02-01-intelligent-vacuum-cleaner.md), then
[LAB-02-02](../labs/lab-02-02-campus-navigation-agent.md).
