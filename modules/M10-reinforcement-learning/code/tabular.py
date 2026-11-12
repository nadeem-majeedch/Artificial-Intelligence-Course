"""tabular.py -- model-free reinforcement learning on tabular problems (M10, L10-04).

Every algorithm here learns from sampled transitions only: no transition model is
used. The code works with any Gymnasium-style environment (``reset`` -> obs, info;
``step`` -> obs, reward, terminated, truncated, info) and with ``rl_envs.MDPAdapter``.

Contents
--------
epsilon_greedy          exploration rule used by every control algorithm
mc_control              every-visit Monte Carlo control (epsilon-greedy)
sarsa                   on-policy temporal-difference control
expected_sarsa          SARSA with the expectation over next actions
q_learning              off-policy temporal-difference control
double_q_learning       two Q-tables to remove maximisation bias
td0_prediction          TD(0) state-value prediction for a fixed policy
mc_prediction           Monte Carlo state-value prediction for a fixed policy
exact_values            ground-truth V_pi from the environment's own model
evaluate                run a greedy policy and report return / success / steps
moving_average          smoothing for learning curves
greedy_path_from_q      follow argmax Q from a start state
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _key(obs):
    """Hashable state key: tuples for array observations, the object itself otherwise."""
    if isinstance(obs, np.ndarray):
        return tuple(np.round(obs.ravel(), 6).tolist())
    return obs


def _n_actions(env) -> int:
    return int(env.action_space.n)


def epsilon_greedy(q: np.ndarray, n_actions: int, eps: float, rng: np.random.Generator) -> int:
    if rng.random() < eps:
        return int(rng.integers(n_actions))
    return int(np.argmax(q))


def moving_average(x, window: int = 20) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if len(x) < window:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="valid")


def _eps_at(episode: int, eps: float, eps_end: float, decay_episodes: int) -> float:
    if decay_episodes <= 0 or episode >= decay_episodes:
        return float(eps_end)
    frac = episode / decay_episodes
    return float(eps + frac * (eps_end - eps))


def _rollout(env, policy, seed: int, max_steps: int):
    """Run one episode under ``policy``; return the list of (s, a, r, s2, terminated)."""
    obs, _ = env.reset(seed=seed)
    s = _key(obs)
    traj = []
    for _ in range(max_steps):
        a = policy(s)
        obs, r, terminated, truncated, info = env.step(a)
        s2 = _key(obs)
        traj.append((s, a, float(r), s2, terminated))
        s = s2
        if terminated or truncated:
            break
    return traj


def _step(env, action):
    """Step an environment and normalise legacy 4-tuple returns."""
    out = env.step(action)
    if len(out) == 4:  # (s2, r, done, info)
        s2, r, done, info = out
        return s2, r, bool(done), False, info
    return out


# ---------------------------------------------------------------------------
# Prediction: Monte Carlo vs temporal difference
# ---------------------------------------------------------------------------

def mc_prediction(env, policy, episodes: int = 1000, gamma: float = 0.99,
                  seed: int = 0, max_steps: int = 200, every_visit: bool = True):
    """Monte Carlo estimate of V_pi: average the observed discounted returns."""
    rng = np.random.default_rng(seed)
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        traj = _rollout(env, policy, seed=int(rng.integers(1 << 30)), max_steps=max_steps)
        returns = []
        G = 0.0
        for _, _, r, _, _ in reversed(traj):
            G = r + gamma * G
            returns.append(G)
        returns.reverse()
        seen = set()
        for i, (s, _, _, _, _) in enumerate(traj):
            if not every_visit and s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (returns[i] - V[s]) / counts[s]
    return dict(V)


def td0_prediction(env, policy, episodes: int = 1000, alpha: float = 0.05,
                   gamma: float = 0.99, seed: int = 0, max_steps: int = 200):
    """TD(0): update V(s) toward r + gamma V(s') after every step."""
    rng = np.random.default_rng(seed)
    V = defaultdict(float)
    for _ in range(episodes):
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        s = _key(obs)
        for _ in range(max_steps):
            a = policy(s)
            obs, r, terminated, truncated, _ = env.step(a)
            s2 = _key(obs)
            target = float(r) + (0.0 if terminated else gamma * V[s2])
            V[s] += alpha * (target - V[s])
            s = s2
            if terminated or truncated:
                break
    return dict(V)


def exact_values(env, policy, gamma: float = 0.99) -> dict:
    """Solve for V_pi exactly from the environment's transition model (``env.unwrapped.P``)."""
    P = env.unwrapped.P
    states = sorted(P.keys(), key=repr)
    pos = {s: i for i, s in enumerate(states)}
    A = np.eye(len(states))
    b = np.zeros(len(states))
    for s in states:
        a = policy(s)
        for prob, s2, r, terminated in P[s][a]:
            b[pos[s]] += prob * r
            if not terminated and s2 in pos:
                A[pos[s], pos[s2]] -= prob * gamma
    return dict(zip(states, np.linalg.solve(A, b)))


# ---------------------------------------------------------------------------
# Control
# ---------------------------------------------------------------------------

def q_learning(env, episodes: int = 500, alpha: float = 0.5, gamma: float = 0.95,
               eps: float = 0.1, eps_end: float | None = None,
               decay_episodes: int = 0, seed: int = 0, max_steps: int = 200,
               q_init: float = 0.0) -> dict:
    """Off-policy TD control: the target uses ``max_a Q(s', a)`` regardless of behaviour.

    ``q_init`` sets the initial action value of every unvisited state. A value above
    the best possible return makes the agent optimistic under uncertainty, which is
    itself an exploration strategy (see the demo and L10-04).
    """
    rng = np.random.default_rng(seed)
    n_actions = _n_actions(env)
    eps_end = eps if eps_end is None else eps_end
    Q = defaultdict(lambda: np.full(n_actions, float(q_init)))
    returns, epsilons, lengths = [], [], []
    for ep in range(episodes):
        e = _eps_at(ep, eps, eps_end, decay_episodes)
        epsilons.append(e)
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        s = _key(obs)
        total = 0.0
        step = 0
        for step in range(1, max_steps + 1):
            a = epsilon_greedy(Q[s], n_actions, e, rng)
            obs, r, terminated, truncated, _ = env.step(a)
            s2 = _key(obs)
            target = r + (0.0 if terminated else gamma * np.max(Q[s2]))
            Q[s][a] += alpha * (target - Q[s][a])
            total += float(r)
            s = s2
            if terminated or truncated:
                break
        returns.append(total)
        lengths.append(step)
    return {"Q": dict(Q), "returns": np.array(returns), "eps": np.array(epsilons),
            "lengths": np.array(lengths)}


def sarsa(env, episodes: int = 500, alpha: float = 0.5, gamma: float = 0.95,
          eps: float = 0.1, eps_end: float | None = None,
          decay_episodes: int = 0, seed: int = 0, max_steps: int = 200) -> dict:
    """On-policy TD control: the target uses the action the agent will actually take."""
    rng = np.random.default_rng(seed)
    n_actions = _n_actions(env)
    eps_end = eps if eps_end is None else eps_end
    Q = defaultdict(lambda: np.zeros(n_actions))
    returns, epsilons = [], []
    for ep in range(episodes):
        e = _eps_at(ep, eps, eps_end, decay_episodes)
        epsilons.append(e)
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        s = _key(obs)
        a = epsilon_greedy(Q[s], n_actions, e, rng)
        total = 0.0
        for _ in range(max_steps):
            obs, r, terminated, truncated, _ = env.step(a)
            s2 = _key(obs)
            a2 = epsilon_greedy(Q[s2], n_actions, e, rng)
            target = r + (0.0 if terminated else gamma * Q[s2][a2])
            Q[s][a] += alpha * (target - Q[s][a])
            total += float(r)
            s, a = s2, a2
            if terminated or truncated:
                break
        returns.append(total)
    return {"Q": dict(Q), "returns": np.array(returns), "eps": np.array(epsilons)}


def expected_sarsa(env, episodes: int = 500, alpha: float = 0.5, gamma: float = 0.95,
                   eps: float = 0.1, eps_end: float | None = None,
                   decay_episodes: int = 0, seed: int = 0, max_steps: int = 200) -> dict:
    """On-policy TD control whose target averages over the epsilon-greedy policy."""
    rng = np.random.default_rng(seed)
    n_actions = _n_actions(env)
    eps_end = eps if eps_end is None else eps_end
    Q = defaultdict(lambda: np.zeros(n_actions))
    returns = []
    for ep in range(episodes):
        e = _eps_at(ep, eps, eps_end, decay_episodes)
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        s = _key(obs)
        total = 0.0
        for _ in range(max_steps):
            a = epsilon_greedy(Q[s], n_actions, e, rng)
            obs, r, terminated, truncated, _ = env.step(a)
            s2 = _key(obs)
            if terminated:
                target = r
            else:
                q2 = Q[s2]
                greedy = int(np.argmax(q2))
                expect = (1 - e) * q2[greedy] + e * q2.mean()
                target = r + gamma * expect
            Q[s][a] += alpha * (target - Q[s][a])
            total += float(r)
            s = s2
            if terminated or truncated:
                break
        returns.append(total)
    return {"Q": dict(Q), "returns": np.array(returns)}


def double_q_learning(env, episodes: int = 500, alpha: float = 0.5, gamma: float = 0.95,
                      eps: float = 0.1, eps_end: float | None = None,
                      decay_episodes: int = 0, seed: int = 0, max_steps: int = 200) -> dict:
    """Double Q-learning: select the best action with one table, evaluate it with the other."""
    rng = np.random.default_rng(seed)
    n_actions = _n_actions(env)
    eps_end = eps if eps_end is None else eps_end
    Q1 = defaultdict(lambda: np.zeros(n_actions))
    Q2 = defaultdict(lambda: np.zeros(n_actions))
    returns = []
    for ep in range(episodes):
        e = _eps_at(ep, eps, eps_end, decay_episodes)
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        s = _key(obs)
        total = 0.0
        for _ in range(max_steps):
            a = epsilon_greedy(Q1[s] + Q2[s], n_actions, e, rng)
            obs, r, terminated, truncated, _ = env.step(a)
            s2 = _key(obs)
            if terminated:
                target = r
            elif rng.random() < 0.5:
                best = int(np.argmax(Q1[s2]))
                target = r + gamma * Q2[s2][best]
            else:
                best = int(np.argmax(Q2[s2]))
                target = r + gamma * Q1[s2][best]
            table = Q1 if rng.random() < 0.5 else Q2
            table[s][a] += alpha * (target - table[s][a])
            total += float(r)
            s = s2
            if terminated or truncated:
                break
        returns.append(total)
    Q = {k: Q1[k] + Q2[k] for k in set(Q1) | set(Q2)}
    return {"Q": Q, "returns": np.array(returns)}


def mc_control(env, episodes: int = 2000, gamma: float = 0.99, eps: float = 0.2,
               eps_end: float = 0.05, decay_episodes: int = 1500, seed: int = 0,
               max_steps: int = 200) -> dict:
    """Every-visit Monte Carlo control with an epsilon-greedy behaviour policy."""
    rng = np.random.default_rng(seed)
    n_actions = _n_actions(env)
    Q = defaultdict(lambda: np.zeros(n_actions))
    N = defaultdict(lambda: np.zeros(n_actions))
    returns = []
    for ep in range(episodes):
        e = _eps_at(ep, eps, eps_end, decay_episodes)
        traj = _rollout(env, lambda s: epsilon_greedy(Q[s], n_actions, e, rng),
                        seed=int(rng.integers(1 << 30)), max_steps=max_steps)
        G = 0.0
        returns.append(sum(t[2] for t in traj))
        for s, a, r, _, _ in reversed(traj):
            G = r + gamma * G
            N[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / N[s][a]
    return {"Q": dict(Q), "returns": np.array(returns)}


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def greedy_action(Q, s, n_actions: int) -> int:
    return int(np.argmax(Q.get(s, np.zeros(n_actions))))


def evaluate(env, policy, episodes: int = 100, seed: int = 0, max_steps: int = 200) -> dict:
    """Run a policy greedily; report mean return, success rate and mean length."""
    rng = np.random.default_rng(seed)
    totals, successes, lengths = [], [], []
    for _ in range(episodes):
        obs, _ = env.reset(seed=int(rng.integers(1 << 30)))
        s = _key(obs)
        total = 0.0
        step = 0
        info = {}
        for step in range(1, max_steps + 1):
            s2, r, terminated, truncated, info = _step(env, policy(s))
            total += float(r)
            s = _key(s2)
            if terminated or truncated:
                break
        totals.append(total)
        lengths.append(step)
        successes.append(bool(info.get("success", total > 0)))
    return {
        "return": float(np.mean(totals)),
        "success": float(np.mean(successes)),
        "steps": float(np.mean(lengths)),
        "episodes": episodes,
    }


def greedy_path_from_q(env, Q, start, max_steps: int = 60) -> list:
    """Deterministic argmax path; stops on termination, repeat or step limit.

    Works on ``rl_envs.MDPAdapter``, which exposes ``env.mdp.is_terminal``.
    """
    n_actions = _n_actions(env)
    mdp = getattr(env, "mdp", None)
    if hasattr(env, "reset"):
        env.reset(seed=0)
    s = start
    path = [s]
    for _ in range(max_steps):
        if mdp is not None and mdp.is_terminal(s):
            break
        a = greedy_action(Q, s, n_actions)
        s2, _, terminated, truncated, _ = _step(env, a)
        s2 = _key(s2)
        path.append(s2)
        if terminated or truncated or s2 in path[:-1]:
            break
        s = s2
    return path


def action_values_table(Q: dict, states: list, n_actions: int) -> np.ndarray:
    """Dense Q array for printing or plotting."""
    out = np.zeros((len(states), n_actions))
    for i, s in enumerate(states):
        if s in Q:
            out[i] = Q[s]
    return out


# ---------------------------------------------------------------------------
# Demo: the model-free numbers quoted in L10-04 and the labs
# ---------------------------------------------------------------------------

def _summarise(name: str, returns: np.ndarray, tail: int = 100) -> str:
    return (f"{name:16s} first-100={returns[:100].mean():8.2f}  "
            f"last-{tail}={returns[-tail:].mean():8.2f}  "
            f"best-20={np.max(moving_average(returns, 20)):8.2f}")


def main() -> None:
    import gymnasium as gym

    from rl_envs import MDPAdapter, cliff_walk, make_gridworld

    print("=" * 78)
    print("1. Cliff walking: SARSA (safe) vs Q-learning (optimal but risky)")
    print("=" * 78)
    env = MDPAdapter(cliff_walk(), max_steps=200)
    runs = {"SARSA": [], "Q-learning": []}
    for seed in range(5):
        runs["SARSA"].append(sarsa(env, episodes=500, alpha=0.5, gamma=1.0, eps=0.1,
                                   seed=seed)["returns"])
        runs["Q-learning"].append(q_learning(env, episodes=500, alpha=0.5, gamma=1.0,
                                             eps=0.1, seed=seed)["returns"])
    mdp = cliff_walk()
    for name, curves in runs.items():
        stack = np.vstack(curves)
        print(_summarise(name, stack.mean(axis=0)))
        print(f"   per-seed last-100 mean: "
              f"{[round(float(c[-100:].mean()), 1) for c in curves]}")
    Q_sarsa = sarsa(env, episodes=500, alpha=0.5, gamma=1.0, eps=0.1, seed=0)["Q"]
    Q_q = q_learning(env, episodes=500, alpha=0.5, gamma=1.0, eps=0.1, seed=0)["Q"]
    start = mdp.start_state()
    for name, Q in (("SARSA", Q_sarsa), ("Q-learning", Q_q)):
        path = greedy_path_from_q(env, Q, start)
        coords = [mdp.state_coord(s) for s in path]
        rows = [rc[0] for rc in coords]
        print(f"{name:10s} greedy path length={len(path) - 1:2d} "
              f"rows={sorted(set(rows))} columns={[rc[1] for rc in coords]}")
        print(f"{'':10s} bottom-row steps={sum(1 for r in rows if r == 3)}  "
              f"greedy return="
              f"{evaluate(env, lambda s, Q=Q: greedy_action(Q, s, 4), episodes=50)['return']:.1f}")

    print("\n" + "=" * 78)
    print("2. Deterministic 5x5 gridworld: epsilon sweep under two initial values")
    print("   10 seeds x 300 episodes, and the same sweep with pessimistic Q init (-1)")
    print("=" * 78)
    gmdp = make_gridworld("open", slip=0.0, step_cost=-0.04)
    genv = MDPAdapter(gmdp, max_steps=100)
    for q_init in (0.0, -1.0):
        label = "optimistic (Q init 0, above the -0.4 a bad policy earns)" if q_init == 0.0 \
            else "pessimistic (Q init -1, below every achievable return)"
        print(f"\nq_init={q_init:+.0f}  {label}")
        print(f"{'eps':>5} {'train last-50':>14} {'greedy return':>14} {'success':>8} {'steps':>7}")
        for eps in (0.0, 0.05, 0.1, 0.3, 0.5):
            curves, evals = [], []
            for seed in range(10):
                res = q_learning(genv, episodes=300, alpha=0.5, gamma=0.9, eps=eps,
                                 seed=seed, max_steps=100, q_init=q_init)
                curves.append(res["returns"])
                Q = res["Q"]
                evals.append(evaluate(genv, lambda s, Q=Q: greedy_action(Q, s, 4),
                                      episodes=30, seed=1000 + seed))
            curve = np.vstack(curves).mean(axis=0)
            print(f"{eps:5.2f} {curve[-50:].mean():14.2f} "
                  f"{np.mean([e['return'] for e in evals]):14.3f} "
                  f"{np.mean([e['success'] for e in evals]):8.2f} "
                  f"{np.mean([e['steps'] for e in evals]):7.2f}")

    print("\n" + "=" * 78)
    print("3. FrozenLake-v1 (slippery): Q-learning vs Monte Carlo control")
    print("=" * 78)
    lake = gym.make("FrozenLake-v1", is_slippery=True, max_episode_steps=100)
    # Sparse rewards: without a genuinely exploratory start (eps=1.0) none of these
    # algorithms finds the goal often enough to bootstrap. See the note in L10-04.
    settings = [("Q-learning", q_learning, True), ("SARSA", sarsa, True),
                ("Expected SARSA", expected_sarsa, True), ("Double Q", double_q_learning, True),
                ("MC control", mc_control, False)]
    for name, fn, uses_alpha in settings:
        evals = []
        for seed in range(5):
            extra = {"alpha": 0.1} if uses_alpha else {}
            res = fn(lake, episodes=3000, gamma=0.99, eps=1.0, eps_end=0.05,
                     decay_episodes=2500, seed=seed, max_steps=100, **extra)
            Q = res["Q"]
            evals.append(evaluate(lake, lambda s, Q=Q: greedy_action(Q, s, 4),
                                  episodes=100, seed=500 + seed, max_steps=100))
        print(f"{name:16s} success={np.mean([e['success'] for e in evals]):.3f} "
              f"(sd {np.std([e['success'] for e in evals]):.3f})  "
              f"return={np.mean([e['return'] for e in evals]):.3f}  "
              f"steps={np.mean([e['steps'] for e in evals]):5.1f}")

    rng = np.random.default_rng(0)
    print("\nRandom policy on FrozenLake (baseline):",
          f"{evaluate(lake, lambda s: int(rng.integers(4)), episodes=200, seed=7)['success']:.3f}"
          " success")

    print("\n" + "=" * 78)
    print("4. Monte Carlo vs TD(0) prediction on FrozenLake")
    print("=" * 78)
    lake2 = gym.make("FrozenLake-v1", is_slippery=True, max_episode_steps=100)
    eval_policy = lambda s: 2  # always "right"
    truth = exact_values(lake2, eval_policy, gamma=0.99)

    def rmse(V):
        errs = [abs(V.get(s, 0.0) - truth[s]) for s in truth]
        return float(np.sqrt(np.mean(np.square(errs))))

    for episodes in (50, 200, 1000):
        mc = mc_prediction(lake2, eval_policy, episodes=episodes, gamma=0.99, seed=1,
                           max_steps=100)
        td = td0_prediction(lake2, eval_policy, episodes=episodes, alpha=0.05, gamma=0.99,
                            seed=1, max_steps=100)
        print(f"episodes={episodes:5d}  MC RMSE={rmse(mc):.4f}  TD RMSE={rmse(td):.4f}  "
              f"V(start) MC={mc.get(0, 0.0):+.3f} TD={td.get(0, 0.0):+.3f} "
              f"exact={truth[0]:+.3f}")

    print("\n" + "=" * 78)
    print("5. Blackjack-v1: a game-playing agent from tabular Q-learning")
    print("=" * 78)
    bj = gym.make("Blackjack-v1", sab=True)
    results = [q_learning(bj, episodes=40_000, alpha=0.02, gamma=0.99, eps=0.2,
                          eps_end=0.02, decay_episodes=30_000, seed=seed, max_steps=40)
               for seed in range(3)]
    evals = [evaluate(bj, lambda s, Q=res["Q"]: greedy_action(Q, s, 2),
                      episodes=5000, seed=99, max_steps=40) for res in results]
    print(f"greedy win rate={np.mean([e['success'] for e in evals]):.3f} "
          f"(per seed {[round(float(e['success']), 3) for e in evals]})")
    print(f"mean return={np.mean([e['return'] for e in evals]):+.4f} "
          f"(a win pays +1, a loss -1)")
    Q = results[0]["Q"]
    for st in [(16, 10, False), (20, 10, False), (12, 4, False), (18, 9, True)]:
        q = Q.get(st, np.zeros(2))
        print(f"state={st}  Q(stick)={q[0]:+.3f}  Q(hit)={q[1]:+.3f}  "
              f"action={'stick' if q[0] >= q[1] else 'hit'}")
    print("\nRules note: gymnasium's Blackjack pays +1 for a win and -1 for a loss; draws pay 0.")


if __name__ == "__main__":
    main()
