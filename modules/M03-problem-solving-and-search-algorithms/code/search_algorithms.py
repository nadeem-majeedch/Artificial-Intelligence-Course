"""Reference implementations for M03: uninformed, informed, local and adversarial search.

Every function is deterministic given a seed, runs on the standard library plus numpy, and is
used by the module notebook and both labs.
"""

from __future__ import annotations

import heapq
import math
import random
from collections import deque


# --------------------------------------------------------------------------- uninformed

def bfs(neighbours, start, goal):
    """Breadth-first search. Returns (path, nodes_expanded) or (None, n)."""
    frontier = deque([[start]])
    seen = {start}
    expanded = 0
    while frontier:
        path = frontier.popleft()
        node = path[-1]
        if node == goal:
            return path, expanded
        expanded += 1
        for nxt, _cost in neighbours(node):
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(path + [nxt])
    return None, expanded


def dfs(neighbours, start, goal):
    frontier = [[start]]
    seen = set()
    expanded = 0
    while frontier:
        path = frontier.pop()
        node = path[-1]
        if node == goal:
            return path, expanded
        if node in seen:
            continue
        seen.add(node)
        expanded += 1
        for nxt, _cost in reversed(list(neighbours(node))):
            frontier.append(path + [nxt])
    return None, expanded


def depth_limited(neighbours, node, goal, limit, path=None):
    path = path or [node]
    if node == goal:
        return path
    if limit <= 0:
        return None
    for nxt, _cost in neighbours(node):
        if nxt not in path:
            found = depth_limited(neighbours, nxt, goal, limit - 1, path + [nxt])
            if found:
                return found
    return None


def ids(neighbours, start, goal, max_depth=25):
    expanded = 0
    for limit in range(max_depth + 1):
        found = depth_limited(neighbours, start, goal, limit)
        expanded += limit + 1
        if found:
            return found, limit, expanded
    return None, max_depth, expanded


def uniform_cost(neighbours, start, goal):
    frontier = [(0.0, 0, start, [start])]
    best = {start: 0.0}
    expanded = 0
    tie = 1
    while frontier:
        g, _t, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, g, expanded
        if g > best.get(node, math.inf):
            continue
        expanded += 1
        for nxt, cost in neighbours(node):
            ng = g + cost
            if ng < best.get(nxt, math.inf):
                best[nxt] = ng
                heapq.heappush(frontier, (ng, tie, nxt, path + [nxt]))
                tie += 1
    return None, math.inf, expanded


# --------------------------------------------------------------------------- informed

def astar(neighbours, start, goal, h):
    frontier = [(h(start), 0.0, 0, start, [start])]
    best = {start: 0.0}
    expanded = 0
    tie = 1
    while frontier:
        _f, g, _t, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, g, expanded
        if g > best.get(node, math.inf):
            continue
        expanded += 1
        for nxt, cost in neighbours(node):
            ng = g + cost
            if ng < best.get(nxt, math.inf):
                best[nxt] = ng
                heapq.heappush(frontier, (ng + h(nxt), ng, tie, nxt, path + [nxt]))
                tie += 1
    return None, math.inf, expanded


def greedy(neighbours, start, goal, h):
    frontier = [(h(start), 0, start, [start])]
    seen = set()
    expanded = 0
    tie = 1
    while frontier:
        _hv, _t, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, expanded
        if node in seen:
            continue
        seen.add(node)
        expanded += 1
        for nxt, _cost in neighbours(node):
            if nxt not in seen:
                heapq.heappush(frontier, (h(nxt), tie, nxt, path + [nxt]))
                tie += 1
    return None, expanded


# --------------------------------------------------------------------------- local search

def eight_queens_conflicts(state):
    """Number of attacking pairs for one queen per column."""
    total = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                total += 1
    return total


def hill_climb(state, rng, max_steps=200):
    state = list(state)
    for _ in range(max_steps):
        current = eight_queens_conflicts(state)
        best_cost, best_state = current, None
        for col in range(len(state)):
            for row in range(len(state)):
                if row == state[col]:
                    continue
                trial = state[:]
                trial[col] = row
                c = eight_queens_conflicts(trial)
                if c < best_cost:
                    best_cost, best_state = c, trial
        if best_state is None:
            return state, current
        state = best_state
    return state, eight_queens_conflicts(state)


def anneal(state, rng, steps=4000, t0=2.0, alpha=0.999):
    state = list(state)
    best_cost, best_state = eight_queens_conflicts(state), state[:]
    temp = t0
    for _ in range(steps):
        col = rng.randrange(len(state))
        trial = state[:]
        trial[col] = rng.randrange(len(state))
        delta = eight_queens_conflicts(trial) - eight_queens_conflicts(state)
        if delta <= 0 or rng.random() < math.exp(-delta / temp):
            state = trial
            cost = eight_queens_conflicts(state)
            if cost < best_cost:
                best_cost, best_state = cost, state[:]
        temp *= alpha
    return best_state, best_cost


# --------------------------------------------------------------------------- adversarial

def minimax(state, depth, maximising, children, evaluate, terminal):
    if terminal(state) or depth == 0:
        return evaluate(state)
    values = [minimax(c, depth - 1, not maximising, children, evaluate, terminal)
              for c in children(state)]
    return max(values) if maximising else min(values)


def alphabeta(state, depth, alpha, beta, maximising, children, evaluate, terminal, counter):
    counter[0] += 1
    if terminal(state) or depth == 0:
        return evaluate(state)
    if maximising:
        value = -math.inf
        for child in children(state):
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False,
                                         children, evaluate, terminal, counter))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    value = math.inf
    for child in children(state):
        value = min(value, alphabeta(child, depth - 1, alpha, beta, True,
                                     children, evaluate, terminal, counter))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value


# --------------------------------------------------------------------------- CSP

def solve_csp(variables, domains, edges):
    """Backtracking with MRV and forward checking for binary inequality constraints."""
    assignment = {}

    def consistent(var, value):
        for a, b in edges:
            if a == var and assignment.get(b) == value:
                return False
            if b == var and assignment.get(a) == value:
                return False
        return True

    def backtrack():
        if len(assignment) == len(variables):
            return dict(assignment)
        unassigned = [v for v in variables if v not in assignment]
        var = min(unassigned, key=lambda v: sum(1 for x in domains[v] if consistent(v, x)))
        for value in domains[var]:
            if not consistent(var, value):
                continue
            assignment[var] = value
            ok = True
            for other in unassigned:
                if other == var:
                    continue
                if not any(consistent(other, x) for x in domains[other]):
                    ok = False
                    break
            if ok:
                found = backtrack()
                if found:
                    return found
            del assignment[var]
        return None

    return backtrack()


# --------------------------------------------------------------------------- demos

def grid_neighbours(width=6, height=6, wall=()):
    wall = set(wall)

    def neighbours(node):
        x, y = node
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in wall:
                yield (nx, ny), 1.0
    return neighbours


def run_comparison(seed=0):
    rng = random.Random(seed)
    wall = {(2, 1), (2, 2), (2, 3), (4, 4)}
    nb = grid_neighbours(wall=wall)
    start, goal = (0, 0), (5, 5)
    h = lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1])
    rows = []
    path, exp = bfs(nb, start, goal)
    rows.append(("BFS", exp, float(len(path) - 1), len(path)))
    path, exp = dfs(nb, start, goal)
    rows.append(("DFS", exp, float(len(path) - 1), len(path)))
    path, cost, exp = uniform_cost(nb, start, goal)
    rows.append(("UCS", exp, cost, len(path)))
    path, cost, exp = astar(nb, start, goal, h)
    rows.append(("A*", exp, cost, len(path)))
    path, exp = greedy(nb, start, goal, h)
    rows.append(("Greedy", exp, float(len(path) - 1), len(path)))
    state = [rng.randrange(8) for _ in range(8)]
    _, hc = hill_climb(state, rng)
    _, sa = anneal(state, rng)
    csp = solve_csp(["A", "B", "C", "D", "E"], {v: ["R", "G", "B"] for v in "ABCDE"},
                    [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E")])
    return rows, hc, sa, csp


if __name__ == "__main__":
    rows, hc, sa, csp = run_comparison()
    for name, expanded, cost, length in rows:
        print(f"{name:7s} expanded={expanded:3d} cost={cost} path_len={length}")
    print("hill climb conflicts:", hc)
    print("annealing conflicts:", sa)
    print("csp:", csp)
