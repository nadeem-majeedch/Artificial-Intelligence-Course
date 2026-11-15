"""Reproducible RL experiments for M10.

The algorithms live in ``dp.py``, ``tabular.py`` and ``dqn.py``; this file wires them to the
environments in ``rl_envs.py`` so that a lesson, lab or notebook can say "run the comparison" without
repeating twenty lines of setup. Everything is seeded, so the numbers in the lessons are reproducible
on any machine.

Contents
--------
make_cliff()                     : the 4×12 cliff-walking MDP wrapped as a gym-style environment
make_grid()                      : a small 4×4 gridworld, wrapped the same way
compare_sarsa_qlearning(...)     : the on-policy / off-policy comparison on the cliff
random_baseline(env, ...)        : the floor any learner must beat
run_tests()                      : asserts the claims the lessons make
"""

from __future__ import annotations

import numpy as np

import dp
import rl_envs
import tabular


def make_cliff():
    """Cliff walking as a gymnasium-style environment (``reset``/``step``)."""
    return rl_envs.MDPAdapter(rl_envs.cliff_walk())


def make_grid(size: int = 4, slip: float = 0.0):
    """A small empty gridworld with a goal in the bottom-right corner."""
    grid = ["S" + "." * (size - 1)] + ["." * size] * (size - 2) + ["." * (size - 1) + "G"]
    mdp = rl_envs.GridMDP(grid, slip=slip, step_cost=-0.04, goal_reward=1.0, name=f"grid-{size}")
    return rl_envs.MDPAdapter(mdp)


def mean_tail(values, window: int = 50) -> float:
    """Mean of the last ``window`` episodes — the standard way to quote a learning curve."""
    values = np.asarray(values, dtype=float)
    return float(values[-window:].mean()) if len(values) else float("nan")


def random_baseline(env, episodes: int = 100, seed: int = 0, max_steps: int = 200) -> dict:
    """Uniform-random policy returns: the number a learner has to beat to claim it learned."""
    rng = np.random.default_rng(seed)
    n_actions = tabular._n_actions(env)
    returns = []
    for _ in range(episodes):
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        total = 0.0
        for _ in range(max_steps):
            obs, reward, terminated, truncated, _ = env.step(int(rng.integers(n_actions)))
            total += float(reward)
            if terminated or truncated:
                break
        returns.append(total)
    return {"returns": np.array(returns), "mean": float(np.mean(returns))}


def compare_sarsa_qlearning(episodes: int = 400, seeds=(0, 1, 2), alpha: float = 0.5,
                            gamma: float = 0.95, eps: float = 0.1) -> dict:
    """Run SARSA and Q-learning on cliff walking for each seed and summarise the tails.

    Returns mean tail returns, the full curves, and the greedy action-value table of the last run so
    a lab can print the policy difference rather than only the numbers.
    """
    rows = {"sarsa": [], "q_learning": []}
    curves = {"sarsa": [], "q_learning": []}
    last = {}
    for seed in seeds:
        s = tabular.sarsa(make_cliff(), episodes=episodes, alpha=alpha, gamma=gamma,
                          eps=eps, seed=seed)
        q = tabular.q_learning(make_cliff(), episodes=episodes, alpha=alpha, gamma=gamma,
                               eps=eps, seed=seed)
        rows["sarsa"].append(mean_tail(s["returns"]))
        rows["q_learning"].append(mean_tail(q["returns"]))
        curves["sarsa"].append(s["returns"])
        curves["q_learning"].append(q["returns"])
        last = {"sarsa_Q": s["Q"], "q_learning_Q": q["Q"]}
    return {
        "episodes": episodes,
        "seeds": list(seeds),
        "sarsa_tail": float(np.mean(rows["sarsa"])),
        "q_learning_tail": float(np.mean(rows["q_learning"])),
        "tail_per_seed": rows,
        "curves": curves,
        "last": last,
    }


def value_iteration_solution(size: int = 4, gamma: float = 0.9) -> dict:
    """Exact solution of the small gridworld, for comparison with learned values."""
    grid = ["S" + "." * (size - 1)] + ["." * size] * (size - 2) + ["." * (size - 1) + "G"]
    mdp = rl_envs.GridMDP(grid, slip=0.0, step_cost=-0.04, goal_reward=1.0, name=f"grid-{size}")
    return dp.value_iteration(mdp, gamma=gamma)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def run_tests() -> bool:
    """Check the claims the module makes about its own experiments."""
    env = make_grid()
    baseline = random_baseline(env, episodes=60, seed=0)
    assert baseline["mean"] < 1.0, baseline["mean"]

    learned = tabular.q_learning(env, episodes=300, alpha=0.5, gamma=0.9, eps=0.2, seed=0)
    tail = mean_tail(learned["returns"], 50)
    assert tail > baseline["mean"] + 0.3, (tail, baseline["mean"])

    exact = value_iteration_solution()
    assert exact["sweeps"] > 0 and exact["V"].max() > 0.5
    # the exact optimal policy reaches the goal from the start corner
    small = rl_envs.GridMDP(["S..", "...", "..G"], slip=0.0, step_cost=-0.04,
                            goal_reward=1.0, name="grid-3")
    small_exact = dp.value_iteration(small, gamma=0.9)
    path = dp.greedy_path(small, small_exact["policy"])
    assert len(path) >= 1 and path[-1] == small.n_states - 1, path

    result = compare_sarsa_qlearning(episodes=300, seeds=(0, 1))
    assert result["episodes"] == 300
    # Sutton & Barto figure 6.4: online, SARSA's safe path earns more than Q-learning's optimal-but-
    # risky path, because epsilon-greedy exploration walks Q-learning off the cliff.
    assert result["sarsa_tail"] > result["q_learning_tail"], result["tail_per_seed"]
    # both still beat a uniform-random policy on the same task
    floor = random_baseline(make_cliff(), episodes=20, seed=0)["mean"]
    assert result["q_learning_tail"] > floor and result["sarsa_tail"] > floor, floor
    return True


if __name__ == "__main__":
    print("experiments self-test:", run_tests())
    result = compare_sarsa_qlearning(episodes=300)
    print("SARSA tail:", round(result["sarsa_tail"], 2),
          "| Q-learning tail:", round(result["q_learning_tail"], 2))
