"""Tests for M03 search algorithms.

Reference calculations are independent of the implementation: Dijkstra is written here,
heuristics are derived from its distances, and game-tree values are enumerated by hand
for a small tree.
"""

import heapq
import math
import random

import pytest

import search_algorithms as sa


def dijkstra(adj, start):
    dist = {start: 0.0}
    queue = [(0.0, start)]
    while queue:
        d, u = heapq.heappop(queue)
        if d > dist.get(u, math.inf):
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, math.inf):
                dist[v] = d + w
                heapq.heappush(queue, (d + w, v))
    return dist


def random_graph(seed, n=10, p=0.4):
    rng = random.Random(seed)
    return {i: [(j, rng.randint(1, 9)) for j in range(n) if j != i and rng.random() < p]
            for i in range(n)}


def weighted_cost(adj, path):
    return sum(w for a, b in zip(path, path[1:]) for nb, w in adj[a] if nb == b)


@pytest.mark.parametrize("seed", range(8))
def test_uniform_cost_is_optimal(seed):
    adj = random_graph(seed)
    dist = dijkstra(adj, 0)
    goal = max(dist, key=dist.get)
    path, cost, _expanded = sa.uniform_cost(lambda u: adj[u], 0, goal)
    assert path[0] == 0 and path[-1] == goal
    assert cost == pytest.approx(dist[goal])
    assert weighted_cost(adj, path) == pytest.approx(cost)


@pytest.mark.parametrize("seed", range(8))
def test_astar_with_admissible_heuristic_matches_ucs(seed):
    adj = random_graph(seed)
    dist = dijkstra(adj, 0)
    goal = max(dist, key=dist.get)
    h = lambda u: abs(dist.get(u, 1e9) - dist[goal])  # noqa: E731
    _path, cost, _n = sa.astar(lambda u: adj[u], 0, goal, h)
    assert cost == pytest.approx(dist[goal])


def test_astar_with_zero_heuristic_equals_uniform_cost():
    adj = random_graph(3)
    dist = dijkstra(adj, 0)
    goal = max(dist, key=dist.get)
    _p, cost_zero, _ = sa.astar(lambda u: adj[u], 0, goal, lambda u: 0.0)
    _p, cost_ucs, _ = sa.uniform_cost(lambda u: adj[u], 0, goal)
    assert cost_zero == pytest.approx(cost_ucs)


def test_bfs_returns_a_shortest_path_in_steps_on_an_unweighted_grid():
    nb = sa.grid_neighbours(width=5, height=5)
    path, _expanded = sa.bfs(nb, (0, 0), (4, 4))
    assert len(path) - 1 == 8  # manhattan distance on an empty grid


def test_dfs_finds_a_path_but_not_necessarily_the_shortest():
    nb = sa.grid_neighbours(width=5, height=5)
    path, _expanded = sa.dfs(nb, (0, 0), (4, 4))
    assert path[0] == (0, 0) and path[-1] == (4, 4)
    assert len(path) - 1 >= 8


def test_iterative_deepening_agrees_with_bfs_cost():
    nb = sa.grid_neighbours(width=4, height=4, wall={(1, 1)})
    bfs_path, _ = sa.bfs(nb, (0, 0), (3, 3))
    ids_path, limit, _expanded = sa.ids(nb, (0, 0), (3, 3))
    assert limit == len(bfs_path) - 1
    assert len(ids_path) - 1 == limit


def test_manhattan_is_consistent_on_a_walled_grid():
    nb = sa.grid_neighbours(width=6, height=6, wall={(2, y) for y in range(4)})
    goal = (5, 5)
    h = lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1])  # noqa: E731
    for x in range(6):
        for y in range(6):
            for nxt, cost in nb((x, y)):
                assert h((x, y)) - cost - h(nxt) <= 0


def test_unreachable_goal_reports_failure():
    nb = sa.grid_neighbours(width=3, height=3, wall={(1, 0), (1, 1), (1, 2)})
    assert sa.bfs(nb, (0, 0), (2, 2))[0] is None
    assert sa.uniform_cost(nb, (0, 0), (2, 2))[0] is None


def test_eight_queens_conflicts_known_values():
    assert sa.eight_queens_conflicts([3, 5, 7, 1, 6, 0, 2, 4]) == 0
    assert sa.eight_queens_conflicts([0] * 8) == 28
    assert sa.eight_queens_conflicts([0, 1]) == 1


def test_alpha_beta_returns_the_minimax_value_with_fewer_evaluations():
    tree = {0: [1, 2], 1: [3, 4], 2: [5, 6]}
    leaves = {3: 3, 4: 5, 5: 2, 6: 9}
    children = lambda s: tree.get(s, [])  # noqa: E731
    terminal = lambda s: s not in tree  # noqa: E731
    evaluate = lambda s: leaves[s]  # noqa: E731
    counter = [0]
    best_plain = sa.minimax(0, 2, True, children, evaluate, terminal)
    best_pruned = sa.alphabeta(0, 2, -math.inf, math.inf, True, children, evaluate, terminal, counter)
    # root max(min(3, 5), min(2, 9)) = max(3, 2) = 3
    assert best_plain == best_pruned == 3
    assert counter[0] <= 6


def test_csp_solution_satisfies_every_edge():
    variables = ["a", "b", "c"]
    domains = {v: [1, 2, 3] for v in variables}
    edges = {("a", "b"): lambda x, y: x != y, ("b", "c"): lambda x, y: x != y,
             ("a", "c"): lambda x, y: x != y}
    solution = sa.solve_csp(variables, domains, edges)
    assert solution is not None and set(solution) == set(variables)
    for (u, v), ok in edges.items():
        assert ok(solution[u], solution[v])
