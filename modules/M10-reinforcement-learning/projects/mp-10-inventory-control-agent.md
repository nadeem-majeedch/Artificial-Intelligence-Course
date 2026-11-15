# MP-10 — Inventory-Control Agent

| | |
| :--- | :--- |
| Module | M10 · Reinforcement Learning |
| Level | 400 |
| Time | 8–10 hours |
| Prerequisites | LAB-10-01, LAB-10-02 |
| Code | `code/rl_envs.py`, `code/tabular.py` |

[← Module](../README.md)

## 1. Problem statement

A shop stocks one product. Each day it chooses how many units to order; demand is random and unmet demand
is lost. Ordering too much costs storage, too little costs margin. This is a classic stochastic inventory
problem, and it is small enough to solve exactly *and* learn, which makes it the right vehicle for an
honest comparison.

Build an agent that chooses daily order quantities, then answer: **how close does learning get to the
optimal policy, and what does it cost to get there?**

## 2. Environment specification

- **State**: stock on hand (0–20) and units arriving tomorrow (0–10) — 231 states.
- **Action**: order 0–5 units; each order arrives next day.
- **Demand**: Poisson with mean 4, truncated at 12; unmet demand is lost.
- **Reward**: $2 per unit sold − 1 per unit stored − 0.5 per unit ordered.
- **Horizon**: 365 days, discounted at 0.95, or continuing with average reward.
- **Constraint**: stock capacity 20; overflow is discarded at a cost.

Document any deviation from these numbers in your report. The specification is part of the experiment.

## 3. Requirements

1. Implement the environment with a seeded `reset`/`step`, matching the Gymnasium contract.
2. Compute a baseline: always order the mean demand (4 units).
3. Solve exactly with value iteration on the finite state space.
4. Learn with tabular Q-learning; report the tail mean reward and the number of episodes to within 5% of
   the exact optimum.
5. Compare policies day by day on a fixed demand trace: where do they differ, and what does it cost?
6. Test robustness: demand mean 6 instead of 4. Which policy degrades less, and why?
7. Report the gap between learning and optimality in reward per day, not in percentage of an arbitrary max.

## 4. Suggested architecture

```text
inventory_env.py    environment: state, transitions, reward, seeding
baselines.py        fixed-order policy and a reorder-point policy
solve_exact.py      value iteration over 231 states
learn.py            Q-learning with decayed epsilon
compare.py          tables, plots, demand-trace comparison
report.md           results, gap analysis, robustness
```

## 5. Starter code

```python
import numpy as np

class InventoryEnv:
    def __init__(self, demand_mean=4.0, capacity=20, max_order=5, seed=0):
        self.demand_mean = demand_mean
        self.capacity = capacity
        self.max_order = max_order
        self.rng = np.random.default_rng(seed)
        self.reset()

    def reset(self, seed=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.stock, self.incoming, self.day = 10, 0, 0
        return (self.stock, self.incoming), {}

    def step(self, order):
        demand = int(self.rng.poisson(self.demand_mean))
        available = self.stock + self.incoming
        sold = min(available, demand)
        lost = demand - sold
        self.stock = min(self.capacity, available - sold)
        self.incoming = int(order)
        reward = 2.0 * sold - 1.0 * self.stock - 0.5 * order
        self.day += 1
        done = self.day >= 365
        return (self.stock, self.incoming), reward, done, False, {"lost": lost}

env = InventoryEnv(seed=0)
state, _ = env.reset()
total = 0.0
for _ in range(10):
    state, reward, done, truncated, info = env.step(4)
    total += reward
print("ten days, fixed order of 4:", round(total, 2), "state:", state, "last info:", info)
```

## 6. Development milestones

| Milestone | Deliverable | Time |
| :--- | :--- | ---: |
| M1 | environment + fixed-order baseline | 2 h |
| M2 | exact value iteration and optimal policy table | 2 h |
| M3 | Q-learning and learning curve | 2 h |
| M4 | policy comparison on a shared demand trace | 1.5 h |
| M5 | robustness run at demand mean 6 | 1 h |
| M6 | report with gap analysis | 1.5 h |

## 7. Expected functionality

- `python solve_exact.py` prints the optimal order for each stock level and the optimal daily reward.
- `python learn.py` prints tail reward and episodes to within 5% of optimal.
- `python compare.py` prints a table of daily reward for fixed, reorder-point and learned policies.
- The learned policy is close to the exact one in most states and visibly different where ties exist —
  ties are expected, and reporting them as errors would be wrong.

## 8. Evaluation criteria

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Environment correctness | 20% | transitions, capacity and rewards match the spec, seeded |
| Exact solution | 20% | value iteration converges; policy is interpretable |
| Learning | 25% | curve, tail metrics, episodes-to-threshold, comparison with exact |
| Robustness | 15% | demand shift tested, degradation quantified |
| Reporting | 20% | gap stated in reward/day, ties explained, limits named |

## 9. Extension challenges

1. **Lead time.** Make orders arrive after two days and report how the state space grows.
2. **Continuing task.** Switch to average reward and compare with the discounted solution.
3. **Function approximation.** Replace the table with a linear value function on (stock, incoming) and
   measure the loss in reward.
4. **Reward hacking.** Add a bonus for "service level" (fraction of demand met) and show a policy that
   games it by over-ordering.

## 10. Scope and honesty

This is a synthetic single-product model, not a retail system. Demand is Poisson and stationary; real
demand has seasonality and promotions. State that limitation in the report, and do not present the learned
policy as operational advice.
