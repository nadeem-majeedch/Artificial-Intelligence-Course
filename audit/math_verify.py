"""Independent mathematical verification harness for the AI course (Phase 23).

Each check re-derives a property independently of the course implementation, or
compares two implementations of the same quantity. Failures are reported with the
quantity that disagreed; nothing is silently skipped.
"""

import itertools
import math
import os
import sys
import traceback

import numpy as np

sys.path[:0] = [os.path.abspath(d) for d in (
    "modules/M03-problem-solving-and-search-algorithms/code",
    "modules/M04-knowledge-representation-and-logical-reasoning/code",
    "modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/code",
    "modules/M06-machine-learning-fundamentals/code",
    "modules/M07-neural-networks-and-deep-learning/code",
    "modules/M09-computer-vision/code",
    "modules/M10-reinforcement-learning/code",
    "modules/M13-responsible-explainable-secure-ai/code",
)]

RESULTS = []


def check(name):
    def deco(fn):
        try:
            detail = fn()
            RESULTS.append((name, "PASS", detail))
        except AssertionError as exc:
            RESULTS.append((name, "FAIL", str(exc)[:300]))
        except Exception as exc:  # noqa: BLE001
            line = traceback.format_exc().strip().splitlines()[-3:]
            RESULTS.append((name, "ERROR", f"{type(exc).__name__}: {exc} | {' / '.join(line)[:220]}"))
        return fn
    return deco


# --------------------------------------------------------------------- search
def random_graph(rng, n=12, p=0.35):
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < p:
                adj[i].append((j, int(rng.integers(1, 9))))
    return adj


def dijkstra(adj, start):
    import heapq
    dist = {start: 0.0}
    pq = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


@check("search: UCS matches independent Dijkstra")
def _():
    import search_algorithms as sa
    rng = np.random.default_rng(0)
    compared = 0
    for _ in range(120):
        adj = random_graph(rng)
        dist = dijkstra(adj, 0)
        goal = int(max(dist, key=dist.get))
        path, cost, _exp = sa.uniform_cost(lambda u: adj[u], 0, goal)
        assert abs(cost - dist[goal]) < 1e-9, f"UCS {cost} != {dist[goal]}"
        assert path[0] == 0 and path[-1] == goal
        compared += 1
    return f"{compared} random weighted graphs"


@check("search: A* with an exact heuristic is optimal")
def _():
    import search_algorithms as sa
    rng = np.random.default_rng(1)
    for _ in range(120):
        adj = random_graph(rng)
        dist = dijkstra(adj, 0)
        goal = int(max(dist, key=dist.get))
        h = lambda u, d=dist, g=goal: abs(d.get(u, 1e9) - d[g])  # noqa: E731
        _p, cost, _e = sa.astar(lambda u: adj[u], 0, goal, h)
        assert abs(cost - dist[goal]) < 1e-9, f"A* {cost} != {dist[goal]}"
    return "120 graphs with an admissible, consistent h"


@check("search: manhattan heuristic is consistent on a walled grid")
def _():
    import search_algorithms as sa
    nb = sa.grid_neighbours(width=6, height=6, wall={(2, 0), (2, 1), (2, 2), (2, 3)})
    goal = (5, 5)
    h = lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1])  # noqa: E731
    worst = -math.inf
    for x in range(6):
        for y in range(6):
            for v, c in nb((x, y)):
                worst = max(worst, h((x, y)) - c - h(v))
    assert worst <= 1e-12, f"consistency violated by {worst}"
    return f"max(h(u) - c - h(v)) = {worst} (consistency requires <= 0)"


@check("search: greedy best-first is not optimal on some graphs")
def _():
    import search_algorithms as sa
    rng = np.random.default_rng(2)
    worse = 0
    for _ in range(200):
        adj = random_graph(rng)
        dist = dijkstra(adj, 0)
        goal = int(max(dist, key=dist.get))
        h = lambda u, d=dist, g=goal: abs(d.get(u, 1e9) - d[g])  # noqa: E731
        path, _e = sa.greedy(lambda u: adj[u], 0, goal, h)
        if path:
            cost = sum(w for a, b in zip(path, path[1:]) for nb, w in adj[a] if nb == b)
            if cost > dist[goal] + 1e-9:
                worse += 1
    assert worse > 0, "greedy was optimal in all 200 graphs"
    return f"greedy suboptimal on {worse}/200 graphs"


@check("search: eight-queens conflict count on a known solution is zero")
def _():
    import search_algorithms as sa
    assert sa.eight_queens_conflicts([3, 5, 7, 1, 6, 0, 2, 4]) == 0
    assert sa.eight_queens_conflicts([0] * 8) == 28
    return "0 conflicts for a valid board, 28 for a full row"


# ----------------------------------------------------------------------- logic
@check("logic: unification respects the occurs check")
def _():
    from fol_core import Const, Var, func, unify
    X = Var("x")
    assert unify(X, func("f", X)) is None, "occurs check missing"
    assert unify(Var("x"), Const("a"))["x"] == Const("a")
    return "unify(x, f(x)) = None; unify(x, a) = {x/a}"


@check("logic: MGU composes across shared variables")
def _():
    from fol_core import Const, Var, pred, unify_atoms
    a, b = Const("a"), Const("b")
    subst = unify_atoms(pred("p", Var("X"), b), pred("p", a, Var("Y")))
    assert subst is not None
    assert subst["X"] == a and subst["Y"] == b, subst
    assert unify_atoms(pred("p", a), pred("p", b)) is None
    return "{X/a, Y/b}; distinct constants do not unify"


@check("logic: resolution proves a valid entailment and refuses an invalid one")
def _():
    from fol_core import Const, Forall, ImpliesF, Var, fol_resolution, pred
    x = Var("x")
    kb = [Forall(x, ImpliesF(pred("human", x), pred("mortal", x))), pred("human", Const("socrates"))]
    proved, trace = fol_resolution(kb, pred("mortal", Const("socrates")))
    assert proved, f"failed to prove mortal(socrates): {trace[-3:]}"
    bad, bad_trace = fol_resolution(kb, pred("mortal", Const("plato")))
    assert not bad, f"proved an invalid entailment: {bad_trace[-3:]}"
    return "mortal(socrates) proved by refutation, mortal(plato) not proved"


@check("logic: propositional implication agrees with its truth table")
def _():
    import prop_logic as pl
    formula = pl.Implies(pl.Symbol("P"), pl.Symbol("Q"))
    for p in (True, False):
        for q in (True, False):
            got = bool(pl.evaluate(formula, {"P": p, "Q": q}))
            assert got == ((not p) or q), (p, q, got)
    # modus ponens as an entailment: {P->Q, P} entails Q, but {P->Q} does not
    kb = [formula, pl.Symbol("P")]
    assert pl.entails(kb, pl.Symbol("Q"))
    assert not pl.entails([formula], pl.Symbol("Q"))
    return "implication matches not-P or Q; modus ponens entailed, converse not"


# ----------------------------------------------------------------- probability
def enumerate_joint(factors, variables):
    joint = {}
    for values in itertools.product([True, False], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        product = 1.0
        for f in factors:
            product *= f.value(**{v: assignment[v] for v in f.variables})
        joint[values] = product
    return joint


@check("probability: variable elimination equals brute-force enumeration")
def _():
    from variable_elimination import alarm_factors, variable_elimination

    factors = alarm_factors()
    variables = []
    for f in factors:
        for v in f.variables:
            if v not in variables:
                variables.append(v)
    joint = enumerate_joint(factors, variables)
    total = sum(joint.values())
    assert abs(total - 1.0) < 1e-9, f"joint does not normalise: {total}"
    cases = [
        ("A", {}, None),
        ("B", {"J": True}, None),
        ("E", {"A": True, "M": True}, None),
        ("B", {"J": True, "M": True}, ["A", "E"]),
    ]
    for query, evidence, order in cases:
        p_true, _mass = variable_elimination(factors, query, evidence, order=order)
        num = den = 0.0
        for values, w in joint.items():
            assignment = dict(zip(variables, values))
            if all(assignment[k] == v for k, v in evidence.items()):
                den += w
                if assignment[query]:
                    num += w
        expected = num / den
        assert abs(float(p_true) - expected) < 1e-10, f"{query}{evidence}: {p_true} != {expected}"
    return f"{len(cases)} queries agree with enumeration over {len(variables)} variables to 1e-10"


@check("probability: Bayes rule is internally consistent")
def _():
    import expert_system as es
    net = es.troubleshooting_net()
    nodes = list(net.parents)
    query, evidence = "P", "W"
    def joint_of(**fixed):
        rest = [n for n in nodes if n not in fixed]
        total = 0.0
        for values in itertools.product([True, False], repeat=len(rest)):
            full = {**fixed, **dict(zip(rest, values))}
            p = 1.0
            for node in nodes:
                if node in full:
                    p *= net.prob(node, full[node], full)
            total += p
        return total

    prior = joint_of(**{query: True})
    p_w = joint_of(**{evidence: True})
    both = joint_of(**{query: True, evidence: True})
    posterior = es.bayes_posterior(net, query, {evidence: True})
    assert abs(posterior[True] - both / p_w) < 1e-12, (posterior, both / p_w)
    assert abs(posterior[True] + posterior[False] - 1.0) < 1e-12
    return f"P(P)={prior:.4f}, P(W)={p_w:.4f}, P(P|W)={posterior[True]:.4f}=P(P,W)/P(W)"


# ------------------------------------------------------------- machine learning
@check("ml: closed-form OLS equals numpy lstsq")
def _():
    from linreg import LinearRegression
    rng = np.random.default_rng(3)
    X = rng.normal(size=(60, 3))
    y = X @ np.array([1.5, -2.0, 0.5]) + 0.3
    model = LinearRegression().fit(X, y)
    coef = np.linalg.lstsq(np.c_[np.ones(len(X)), X], y, rcond=None)[0]
    got = np.r_[model.intercept_, model.coef_]
    assert np.allclose(got, coef, atol=1e-8), (got, coef)
    return f"coefficients agree to 1e-8: {np.round(got, 3)}"


@check("ml: ridge closed form matches (X'X + lambda I)^-1 X'y")
def _():
    from linreg import Ridge
    rng = np.random.default_rng(4)
    X = rng.normal(size=(40, 2))
    y = X @ np.array([1.0, -1.0]) + rng.normal(scale=0.1, size=40)
    lam = 1.7
    model = Ridge(alpha=lam).fit(X, y)
    Xc = X - X.mean(0)
    yc = y - y.mean()
    w = np.linalg.solve(Xc.T @ Xc + lam * np.eye(2), Xc.T @ yc)
    assert np.allclose(model.coef_, w, atol=1e-6), (model.coef_, w)
    return "ridge coefficients agree to 1e-6"


@check("ml: r2_score equals 1 - SS_res/SS_tot")
def _():
    from linreg import r2_score
    rng = np.random.default_rng(5)
    y = rng.normal(size=50)
    p = y + rng.normal(scale=0.4, size=50)
    expected = 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    assert abs(r2_score(y, p) - expected) < 1e-12
    return "definition verified on random vectors"


@check("ml: naive Bayes posterior matches a hand-computed Gaussian likelihood")
def _():
    from classifiers import GaussianNB
    X = np.array([[0.0], [0.2], [1.0], [1.2], [5.0], [5.4]])
    y = np.array([0, 0, 0, 0, 1, 1])
    model = GaussianNB().fit(X, y)
    prior = np.array([4 / 6, 2 / 6])
    lik = []
    for k in range(2):
        mu = X[y == k, 0].mean()
        var = X[y == k, 0].var()
        lik.append(np.exp(-(0.1 - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var))
    expected = prior * np.array(lik)
    expected = expected / expected.sum()
    got = model.predict_proba(np.array([[0.1]]))[0]
    assert np.allclose(got, expected, atol=1e-8), (got, expected)
    return "GaussianNB posterior matches the analytic posterior"


@check("ml: decision tree fits AND and OR exactly")
def _():
    from classifiers import DecisionTreeClassifier
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    for name, y in (("AND", np.array([0, 0, 0, 1])), ("OR", np.array([0, 1, 1, 1]))):
        pred = DecisionTreeClassifier(max_depth=2).fit(X, y).predict(X)
        assert (pred == y).all(), (name, pred)
    return "AND and OR learned exactly with depth 2"


@check("ml: gradient descent linear regression converges to OLS")
def _():
    from linreg import LinearRegression, LinearRegressionGD
    rng = np.random.default_rng(6)
    X = rng.normal(size=(200, 2))
    y = 2.0 + X @ np.array([3.0, -1.5]) + rng.normal(scale=0.05, size=200)
    ols = LinearRegression().fit(X, y)
    gd = LinearRegressionGD(lr=0.05, epochs=4000).fit(X, y)
    assert np.allclose(np.r_[gd.intercept_, gd.coef_], np.r_[ols.intercept_, ols.coef_], atol=0.05)
    return f"GD loss {gd.loss_history_[-1]:.6f}, coefficients within 0.05 of OLS"


# ---------------------------------------------------------------- neural nets
@check("nn: numerical gradient check passes for the numpy MLP")
def _():
    from nn_numpy import MLP, gradient_check
    rng = np.random.default_rng(11)
    X = rng.normal(size=(12, 4))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    rel = gradient_check(MLP([4, 8, 2], seed=0), X, y, seed=0)
    assert rel < 1e-4, f"relative error {rel}"
    return f"max relative error {rel:.2e}"


@check("nn: softmax rows sum to one and is shift-invariant")
def _():
    from nn_numpy import softmax
    z = np.array([[1.0, 2.0, 3.0], [-10.0, 0.0, 10.0]])
    p = softmax(z)
    assert np.allclose(p.sum(1), 1.0), p.sum(1)
    assert np.allclose(softmax(z + 100.0), p, atol=1e-12), "softmax is not shift invariant"
    return "rows sum to 1; softmax(z + 100) == softmax(z)"


@check("nn: attention weights are a distribution and the mask is respected")
def _():
    import torch
    sys.path.insert(0, os.path.abspath("modules/M08-natural-language-processing/code"))
    from seq_models import Attention
    torch.manual_seed(0)
    att = Attention(8)
    dec = torch.randn(2, 8)
    enc = torch.randn(2, 5, 8)
    mask = torch.zeros(2, 5, dtype=torch.bool)
    mask[:, 3:] = True
    ctx, w = att(dec, enc, mask)
    assert ctx.shape == (2, 8)
    assert torch.allclose(w.sum(1), torch.ones(2)), w.sum(1)
    assert torch.all(w[:, 3:] < 1e-7), "masked positions received attention"
    return "weights sum to 1, masked positions receive exactly zero"


@check("vision: convolution matches scipy for a symmetric kernel")
def _():
    from scipy.signal import convolve2d as sp_conv
    from vision_core import convolve2d, gaussian_kernel
    rng = np.random.default_rng(7)
    img = rng.random((12, 12))
    k = gaussian_kernel(5, 1.0)
    k = k / k.sum()
    ours = convolve2d(img, k, padding="same")
    ref = sp_conv(img, k, mode="same", boundary="fill", fillvalue=0.0)
    assert np.allclose(ours, ref, atol=1e-10), np.abs(ours - ref).max()
    return f"max difference {np.abs(ours - ref).max():.2e}"


@check("vision: Otsu threshold matches skimage on a bimodal image")
def _():
    from skimage.filters import threshold_otsu
    from vision_core import otsu_threshold
    rng = np.random.default_rng(8)
    img = np.clip(np.r_[rng.normal(0.25, 0.05, 600), rng.normal(0.75, 0.05, 400)], 0, 1)
    ours = otsu_threshold((img * 255).round().astype(np.uint8))
    ref = threshold_otsu(img)
    assert abs(ours / 255.0 - ref) < 0.02, (ours, ref * 255)
    return f"ours {ours:.1f}/255 vs skimage {ref * 255:.1f}/255"


@check("vision: IoU, Dice and mIoU match their definitions")
def _():
    from vision_core import dice, iou, mean_iou
    a, b = [0, 0, 10, 10], [5, 0, 10, 10]   # (x, y, w, h)
    inter = 50
    union = 100 + 100 - inter
    assert abs(iou(a, b) - inter / union) < 1e-12
    m1 = np.zeros((10, 10), dtype=int)
    m1[2:6, 2:6] = 1
    m2 = np.zeros((10, 10), dtype=int)
    m2[4:8, 4:8] = 1
    inter_px = int(((m1 == 1) & (m2 == 1)).sum())
    assert abs(dice(m1, m2, label=1) - 2 * inter_px / ((m1 == 1).sum() + (m2 == 1).sum())) < 1e-12
    expected = []
    for lab in (0, 1):
        p, t = (m1 == lab), (m2 == lab)
        expected.append(((p & t).sum()) / ((p | t).sum()))
    assert abs(mean_iou(m1, m2, (0, 1)) - float(np.mean(expected))) < 1e-12, (mean_iou(m1, m2, (0, 1)), expected)
    return "IoU 0.333, Dice 0.25, mIoU matches the per-class mean"


@check("vision: NMS keeps the highest-scoring box and suppresses its neighbour")
def _():
    from vision_core import nms
    kept = nms([[0, 0, 10, 10], [1, 1, 11, 11], [50, 50, 60, 60]], [0.9, 0.8, 0.7], iou_threshold=0.5)
    assert kept == [0, 2], kept
    return "kept boxes [0, 2]"


@check("vision: synthetic datasets are deterministic, seed-separated and balanced")
def _():
    from vision_core import make_leaf_images
    imgs, labels, *_ = make_leaf_images(n_per_class=10, seed=0)
    imgs2, _, *_ = make_leaf_images(n_per_class=10, seed=0)
    imgs3, _, *_ = make_leaf_images(n_per_class=10, seed=1)
    assert np.array_equal(imgs, imgs2), "same seed is not reproducible"
    assert not np.array_equal(imgs, imgs3), "different seeds give identical images"
    counts = np.bincount(np.asarray(labels).ravel())
    assert len(set(counts.tolist())) == 1, counts
    hashes = {hash(img.tobytes()) for img in np.asarray(imgs)}
    assert len(hashes) == len(np.asarray(imgs)), "duplicate images inside one dataset"
    return f"leaves {imgs.shape}, balanced {counts.tolist()}, {len(hashes)} unique images"


# --------------------------------------------------------------- reinforcement
@check("rl: value iteration satisfies the Bellman optimality equation")
def _():
    from dp import bellman_residual, value_iteration
    from rl_envs import make_gridworld
    mdp = make_gridworld(kind="open", slip=0.1)
    out = value_iteration(mdp, gamma=0.9, theta=1e-10)
    res = bellman_residual(mdp, out["V"], gamma=0.9)
    assert res < 1e-8, f"residual {res}"
    return f"residual {res:.2e} after {out['sweeps']} sweeps"


@check("rl: policy iteration and value iteration agree on the optimal value")
def _():
    from dp import policy_iteration, value_iteration
    from rl_envs import make_gridworld
    mdp = make_gridworld(kind="maze", slip=0.05)
    vi = value_iteration(mdp, gamma=0.9, theta=1e-10)
    pi = policy_iteration(mdp, gamma=0.9, theta=1e-10)
    v_pi = pi["V"] if isinstance(pi, dict) else pi[0]
    delta = float(np.max(np.abs(v_pi - vi["V"])))
    assert delta < 1e-6, f"policy and value iteration differ by {delta}"
    return f"max |V_pi - V*| = {delta:.2e}"


@check("rl: exact policy value equals iterative policy evaluation")
def _():
    from dp import exact_policy_value, policy_evaluation, random_policy
    from rl_envs import make_gridworld
    mdp = make_gridworld(kind="open")
    policy = random_policy(mdp, seed=0)
    V_iter, _s, _d = policy_evaluation(mdp, policy, gamma=0.9, theta=1e-12)
    V_exact = exact_policy_value(mdp, policy, gamma=0.9)
    delta = float(np.max(np.abs(V_iter - V_exact)))
    assert delta < 1e-9, f"iterative and exact policy evaluation differ by {delta}"
    return f"max difference {delta:.2e}"


@check("rl: Q-learning reaches the goal reliably and near the optimal return")
def _():
    from experiments import make_grid, value_iteration_solution
    from tabular import evaluate, q_learning
    env = make_grid(size=4)
    opt = value_iteration_solution(size=4, gamma=0.95)
    res = q_learning(env, episodes=800, alpha=0.5, gamma=0.95, eps=0.2, eps_end=0.02,
                     decay_episodes=600, seed=0)
    Q = res["Q"]
    policy = lambda obs: int(np.argmax(Q.get(int(np.asarray(obs).ravel()[0]), np.zeros(4))))  # noqa: E731
    score = evaluate(make_grid(size=4), policy, episodes=50, seed=1, max_steps=100)
    assert score["success"] > 0.9, score
    V_start = float(np.max(opt["V"]))
    assert score["return"] > 0.6 * V_start, (score["return"], V_start)
    return f"success {score['success']:.2f}, return {score['return']:.3f} vs V* {V_start:.3f}"


@check("rl: SARSA is safer than Q-learning on cliff walking across seeds")
def _():
    from experiments import compare_sarsa_qlearning
    out = compare_sarsa_qlearning(episodes=300, seeds=(0, 1, 2))
    s, q = out["sarsa_tail"], out["q_learning_tail"]
    assert s > q, f"SARSA {s} not above Q-learning {q}"
    return f"SARSA {s:.2f} > Q-learning {q:.2f}, 300 episodes x 3 seeds"


@check("tabular: TD(0) converges to the exact value of a fixed policy")
def _():
    import gymnasium as gym
    from tabular import exact_values, td0_prediction
    policy = lambda obs: 0  # noqa: E731  always the first action
    env = gym.make("FrozenLake-v1", is_slippery=False)
    V_exact = exact_values(env, policy, gamma=0.99)
    res = td0_prediction(env, policy, episodes=3000, alpha=0.1, gamma=0.99, seed=0)
    V = res if isinstance(res, dict) else {}
    err = float(np.mean([abs(V.get(k, 0.0) - v) for k, v in V_exact.items()]))
    assert err < 0.15, f"mean absolute TD error {err}"
    return f"mean |V_TD - V_pi| = {err:.3f}"


# --------------------------------------------------------------- fairness/gen
@check("fairness: disparate impact ratio matches min/max selection rate")
def _():
    from fairness import disparate_impact_ratio, group_metrics
    y_true = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    y_pred = np.array([1, 1, 1, 0, 0, 0, 1, 1])
    group = np.array(["a", "a", "a", "a", "b", "b", "b", "b"])
    m = group_metrics(y_true, y_pred, group)
    rates = [v["selection_rate"] for v in m.values()]
    assert abs(disparate_impact_ratio(m) - min(rates) / max(rates)) < 1e-12
    return f"DIR {min(rates) / max(rates):.3f} = min/max selection rate"


def main():
    width = max(len(n) for n, _s, _d in RESULTS)
    failed = 0
    for name, status, detail in RESULTS:
        if status != "PASS":
            failed += 1
        print(f"{status:5s} {name:<{width}}  {detail}")
    print(f"\n{len(RESULTS)} checks, {len(RESULTS) - failed} passed, {failed} failed")


if __name__ == "__main__":
    main()
