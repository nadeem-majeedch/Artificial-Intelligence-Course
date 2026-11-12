"""dp.py -- exact dynamic programming on a tabular MDP (M10, lessons L10-02/L10-03).

Everything here assumes the transition model is known, which is what separates
*planning* (this file) from *learning* (``tabular.py``).

Contents
--------
policy_evaluation      iterative Bellman expectation backup
action_values          Q(s, a) from V and the model
improve_policy         greedy policy improvement
policy_iteration       evaluate -> improve until stable
value_iteration        Bellman optimality backup until the value function settles
exact_policy_value     closed-form V_pi via a linear solve (I - gamma P)^-1 r
expected_episode_length closed-form expected steps to termination
greedy_path            follow a deterministic policy from the start
bellman_residual       max |V - T V| for the optimality operator
format_grid            pretty-print a state-indexed array as a grid

Run ``python dp.py`` to reproduce every DP number quoted in the lessons.
"""

from __future__ import annotations

import numpy as np

from rl_envs import ACTION_NAMES, ACTIONS, GridMDP, make_gridworld


# ---------------------------------------------------------------------------
# Prediction: policy evaluation
# ---------------------------------------------------------------------------

def policy_evaluation(
    mdp: GridMDP,
    policy: np.ndarray,
    gamma: float = 0.9,
    theta: float = 1e-8,
    max_sweeps: int = 10_000,
) -> tuple[np.ndarray, int, list[float]]:
    """Iterative policy evaluation.

    Repeat ``V(s) <- sum_{s'} p(s'|s,a) [r + gamma V(s')]`` for every non-terminal
    state, in place (Gauss-Seidel), until the largest change in a sweep is below
    ``theta``. Returns the value function, the number of sweeps and the delta
    history (useful for the convergence plot).
    """
    V = np.zeros(mdp.n_states)
    deltas: list[float] = []
    for sweep in range(1, max_sweeps + 1):
        delta = 0.0
        for s in range(mdp.n_states):
            if mdp.is_terminal(s):
                continue
            a = int(policy[s])
            v_new = 0.0
            for s2, p in mdp.transitions(s, a).items():
                v_new += p * (mdp.reward(s, a, s2) + gamma * V[s2])
            delta = max(delta, abs(v_new - V[s]))
            V[s] = v_new
        deltas.append(delta)
        if delta < theta:
            return V, sweep, deltas
    return V, max_sweeps, deltas


def action_values(mdp: GridMDP, V: np.ndarray, gamma: float = 0.9) -> np.ndarray:
    """One-step lookahead: ``Q(s,a) = sum p (r + gamma V(s'))``."""
    Q = np.full((mdp.n_states, mdp.n_actions), -np.inf)
    for s in range(mdp.n_states):
        if mdp.is_terminal(s):
            continue
        for a in range(mdp.n_actions):
            Q[s, a] = sum(p * (mdp.reward(s, a, s2) + gamma * V[s2])
                          for s2, p in mdp.transitions(s, a).items())
    return Q


def greedy_from_values(mdp: GridMDP, V: np.ndarray, gamma: float = 0.9) -> np.ndarray:
    """Greedy policy with respect to V; ties broken by the lowest action index."""
    Q = action_values(mdp, V, gamma)
    policy = np.zeros(mdp.n_states, dtype=int)
    for s in range(mdp.n_states):
        if not mdp.is_terminal(s):
            policy[s] = int(np.argmax(Q[s]))
    return policy


# ---------------------------------------------------------------------------
# Control: policy iteration and value iteration
# ---------------------------------------------------------------------------

def policy_iteration(
    mdp: GridMDP,
    gamma: float = 0.9,
    theta: float = 1e-8,
) -> dict:
    """Alternate full policy evaluation with greedy improvement until the policy is stable."""
    policy = np.zeros(mdp.n_states, dtype=int)
    history = []
    rounds = 0
    while True:
        rounds += 1
        V, sweeps, deltas = policy_evaluation(mdp, policy, gamma, theta)
        Q = action_values(mdp, V, gamma)
        new_policy = policy.copy()
        changes = 0
        for s in range(mdp.n_states):
            if mdp.is_terminal(s):
                continue
            best = int(np.argmax(Q[s]))
            if best != policy[s]:
                new_policy[s] = best
                changes += 1
        history.append({
            "round": rounds,
            "sweeps": sweeps,
            "changes": changes,
            "v_start": float(V[mdp.start_state()]),
            "delta": float(deltas[-1]) if deltas else 0.0,
        })
        policy = new_policy
        if changes == 0:
            break
        if rounds >= 100:
            break
    return {"V": V, "policy": policy, "rounds": rounds, "history": history}


def value_iteration(
    mdp: GridMDP,
    gamma: float = 0.9,
    theta: float = 1e-8,
    max_sweeps: int = 10_000,
) -> dict:
    """Bellman optimality backup until ``max_s |V - T*V| < theta``."""
    V = np.zeros(mdp.n_states)
    deltas: list[float] = []
    for sweep in range(1, max_sweeps + 1):
        delta = 0.0
        for s in range(mdp.n_states):
            if mdp.is_terminal(s):
                continue
            v_new = max(
                sum(p * (mdp.reward(s, a, s2) + gamma * V[s2])
                    for s2, p in mdp.transitions(s, a).items())
                for a in range(mdp.n_actions)
            )
            delta = max(delta, abs(v_new - V[s]))
            V[s] = v_new
        deltas.append(delta)
        if delta < theta:
            break
    return {
        "V": V,
        "policy": greedy_from_values(mdp, V, gamma),
        "sweeps": sweep,
        "deltas": deltas,
    }


def bellman_residual(mdp: GridMDP, V: np.ndarray, gamma: float = 0.9) -> float:
    """``max_s |V(s) - max_a Q(s,a)|`` over non-terminal states."""
    Q = action_values(mdp, V, gamma)
    residuals = [abs(V[s] - np.max(Q[s])) for s in range(mdp.n_states)
                 if not mdp.is_terminal(s)]
    return float(max(residuals)) if residuals else 0.0


# ---------------------------------------------------------------------------
# Exact quantities for a fixed deterministic policy
# ---------------------------------------------------------------------------

def _policy_matrices(mdp: GridMDP, policy: np.ndarray, gamma: float):
    """Build P (n x n) and r (n) for the non-terminal block of a policy."""
    free = [s for s in range(mdp.n_states) if not mdp.is_terminal(s)]
    pos = {s: i for i, s in enumerate(free)}
    n = len(free)
    P = np.zeros((n, n))
    r = np.zeros(n)
    for s in free:
        a = int(policy[s])
        for s2, p in mdp.transitions(s, a).items():
            r[pos[s]] += p * mdp.reward(s, a, s2)
            if s2 in pos:
                P[pos[s], pos[s2]] += p
    return P, r, free, pos


def exact_policy_value(mdp: GridMDP, policy: np.ndarray, gamma: float = 0.9) -> np.ndarray:
    """Solve ``(I - gamma P) V = r`` exactly; terminal states keep value 0."""
    P, r, free, pos = _policy_matrices(mdp, policy, gamma)
    V = np.zeros(mdp.n_states)
    if free:
        V_free = np.linalg.solve(np.eye(len(free)) - gamma * P, r)
        for s in free:
            V[s] = V_free[pos[s]]
    return V


def expected_episode_length(mdp: GridMDP, policy: np.ndarray) -> float:
    """Expected steps until a terminal state; ``inf`` if the policy can loop forever."""
    P, _, free, pos = _policy_matrices(mdp, policy, 0.0)
    if not free:
        return 0.0
    lengths = np.linalg.solve(np.eye(len(free)) - P, np.ones(len(free)))
    value = float(lengths[pos[mdp.start_state()]])
    if not np.isfinite(value) or value < 0 or value > 1e6:
        return float("inf")
    return value


def greedy_path(mdp: GridMDP, policy: np.ndarray) -> list[int]:
    """Follow the policy from the start state until a terminal state or a repeat."""
    s = mdp.start_state()
    path = [s]
    for _ in range(2 * mdp.n_states):
        if mdp.is_terminal(s):
            break
        s2 = next(iter(mdp.transitions(s, int(policy[s]))))
        if s2 in path:
            path.append(s2)
            break
        path.append(s2)
        s = s2
    return path


def describe_path(mdp: GridMDP, path: list[int], limit: int = 12) -> str:
    """Short human-readable path; non-terminating policies are labelled, not printed in full."""
    coords = [mdp.state_coord(s) for s in path]
    if not mdp.is_terminal(path[-1]):
        head = coords[:6]
        return f"does not terminate (starts {head}{' ...' if len(coords) > 6 else ''})"
    shown = coords[:limit]
    return str(shown) + (" ..." if len(coords) > limit else "")


# ---------------------------------------------------------------------------
# Printing helpers
# ---------------------------------------------------------------------------

def format_grid(mdp: GridMDP, values: np.ndarray, fmt: str = "{:+.2f}") -> str:
    """Render a state-indexed array as a grid, walls as ``#####``."""
    width = max(len(fmt.format(0.0)), 5)
    lines = []
    for r, row in enumerate(mdp.grid):
        cells = []
        for c in range(len(row)):
            if (r, c) not in mdp.index:
                cells.append("#" * width)
            else:
                cells.append(fmt.format(values[mdp.index[(r, c)]]).rjust(width))
        lines.append(" ".join(cells))
    return "\n".join(lines)


def format_policy(mdp: GridMDP, policy: np.ndarray) -> str:
    lines = []
    for r, row in enumerate(mdp.grid):
        cells = []
        for c in range(len(row)):
            if (r, c) not in mdp.index:
                cells.append("#")
            else:
                s = mdp.index[(r, c)]
                cells.append(mdp.cells[(r, c)] if mdp.is_terminal(s)
                             else ACTIONS[int(policy[s])][2])
        lines.append(" ".join(cells))
    return "\n".join(lines)


def random_policy(mdp: GridMDP, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.integers(0, mdp.n_actions, size=mdp.n_states)


# ---------------------------------------------------------------------------
# Demo: every DP number in the lessons
# ---------------------------------------------------------------------------

def main() -> None:
    gamma = 0.9

    print("=" * 72)
    print("1. Policy evaluation on the 5x5 open grid (slip=0.1, step cost=-0.04)")
    print("=" * 72)
    mdp = make_gridworld("open", slip=0.1, step_cost=-0.04)
    uniform = np.zeros(mdp.n_states, dtype=int)  # always "up"
    V_up, sweeps, deltas = policy_evaluation(mdp, uniform, gamma)
    print(f"always-up policy: sweeps={sweeps} last delta={deltas[-1]:.2e} "
          f"V(start)={V_up[mdp.start_state()]:+.4f}")
    print("first six deltas:", [round(d, 4) for d in deltas[:6]])
    print(format_grid(mdp, V_up))

    print("\nExact linear solve for the same policy:")
    V_exact = exact_policy_value(mdp, uniform, gamma)
    print(f"  max |iterative - exact| = {np.max(np.abs(V_up - V_exact)):.2e}")

    print("\n" + "=" * 72)
    print("2. Policy iteration vs value iteration")
    print("=" * 72)
    pi = policy_iteration(mdp, gamma)
    vi = value_iteration(mdp, gamma)
    print(f"policy iteration : rounds={pi['rounds']}  sweeps per round="
          f"{[h['sweeps'] for h in pi['history']]}  changes={[h['changes'] for h in pi['history']]}")
    print(f"value iteration  : sweeps={vi['sweeps']}  V(start)={vi['V'][mdp.start_state()]:+.4f}")
    print(f"max |V_pi - V_vi| = {np.max(np.abs(pi['V'] - vi['V'])):.2e}")
    print(f"policies identical: {np.array_equal(pi['policy'], vi['policy'])}")
    print(f"Bellman residual of V_vi: {bellman_residual(mdp, vi['V'], gamma):.2e}")
    print("\noptimal values:\n" + format_grid(mdp, vi["V"]))
    print("\noptimal policy:\n" + format_policy(mdp, vi["policy"]))
    path = greedy_path(mdp, vi["policy"])
    print(f"greedy path from start: {describe_path(mdp, path)}")
    print(f"expected episode length: {expected_episode_length(mdp, vi['policy']):.2f} steps")

    print("\n" + "=" * 72)
    print("3. Policy comparison: exact expected return from the start state")
    print("=" * 72)
    policies = {
        "optimal": vi["policy"],
        "always-up": np.zeros(mdp.n_states, dtype=int),
        "always-right": np.ones(mdp.n_states, dtype=int),
        "random seed 0": random_policy(mdp, 0),
        "random seed 1": random_policy(mdp, 1),
        "random seed 2": random_policy(mdp, 2),
    }
    for name, pol in policies.items():
        V_pol = exact_policy_value(mdp, pol, gamma)
        steps = expected_episode_length(mdp, pol)
        steps_txt = f"{steps:6.2f}" if np.isfinite(steps) else "   inf"
        print(f"{name:14s} V(start)={V_pol[mdp.start_state()]:+8.4f} steps={steps_txt} "
              f"path={describe_path(mdp, greedy_path(mdp, pol))}")

    print("\n" + "=" * 72)
    print("4. Deterministic world (slip=0): does the optimal path change?")
    print("=" * 72)
    det = make_gridworld("open", slip=0.0, step_cost=-0.04)
    det_vi = value_iteration(det, gamma)
    print(f"sweeps={det_vi['sweeps']} V(start)={det_vi['V'][det.start_state()]:+.4f}")
    print("optimal policy:\n" + format_policy(det, det_vi["policy"]))
    print(f"path={describe_path(det, greedy_path(det, det_vi['policy']))}")

    print("\n" + "=" * 72)
    print("5. Discount sweep")
    print("=" * 72)
    print(f"{'gamma':>6} {'sweeps':>7} {'V(start)':>10} {'policy?':>18} {'steps':>7}")
    base = None
    for g in (0.0, 0.5, 0.8, 0.9, 0.95, 0.99):
        res = value_iteration(mdp, g)
        key = tuple(res["policy"])
        if base is None:
            base = key
        same = "same as gamma=0" if key == base else "differs"
        steps = expected_episode_length(mdp, res["policy"])
        steps_txt = f"{steps:7.2f}" if np.isfinite(steps) else "    inf"
        print(f"{g:6.2f} {res['sweeps']:7d} {res['V'][mdp.start_state()]:10.4f} "
              f"{same:>18} {steps_txt}")

    print("\n" + "=" * 72)
    print("6. Cost of slipping: same task, three slip levels")
    print("=" * 72)
    for slip in (0.0, 0.1, 0.3):
        m = make_gridworld("open", slip=slip, step_cost=-0.04)
        r = value_iteration(m, gamma)
        print(f"slip={slip:4.1f}  V(start)={r['V'][m.start_state()]:+8.4f}  "
              f"steps={expected_episode_length(m, r['policy']):6.2f}  "
              f"path_len={len(greedy_path(m, r['policy'])) - 1}")


if __name__ == "__main__":
    main()
