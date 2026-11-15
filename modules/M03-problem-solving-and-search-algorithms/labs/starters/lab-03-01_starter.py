"""LAB-03-01 starter — route planning on a 12x12 street grid.

What this gives you
-------------------
* the grid, the blocked streets and the nine benchmark pairs from the lab sheet;
* a working comparison of BFS, UCS and A* with a Manhattan heuristic;
* a printed table you can paste into your report.

What is missing (your work)
---------------------------
1. One-way streets. ``one_way`` below is empty; make ``neighbours`` respect it.
2. Greedy best-first and DFS columns, using the same signature.
3. The route-sheet cost comparison described in task 4.

Run:  python lab-03-01_starter.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "code"))

import search_algorithms as sa  # noqa: E402

SIZE = 12
BLOCKED = {(3, 4), (3, 5), (4, 4), (7, 8), (8, 8), (8, 9), (9, 2), (9, 3), (10, 2)}
ONE_WAY = {}          # TODO: map (from_node, to_node) -> False to forbid that direction
BENCHMARKS = [((0, 0), (11, 11)), ((0, 6), (11, 0)), ((5, 0), (5, 11)),
              ((2, 2), (10, 10)), ((0, 11), (11, 5)), ((6, 6), (0, 0)),
              ((11, 0), (0, 11)), ((4, 9), (9, 4)), ((1, 1), (1, 10))]


def neighbours(node):
    """Yield (neighbour, cost) for a 4-connected street grid."""
    x, y = node
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nxt = (x + dx, y + dy)
        if not (0 <= nxt[0] < SIZE and 0 <= nxt[1] < SIZE):
            continue
        if nxt in BLOCKED:
            continue
        if ONE_WAY.get((node, nxt)) is False:      # one-way rule, if you add one
            continue
        yield nxt, 1.0


def manhattan(goal):
    return lambda node: abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def main():
    print(f"{'start':>8} {'goal':>8} {'BFS':>6} {'UCS':>6} {'A*':>6} {'A* expanded':>12}")
    for start, goal in BENCHMARKS:
        bfs_path, _ = sa.bfs(neighbours, start, goal)
        _ucs_path, ucs_cost, _ = sa.uniform_cost(neighbours, start, goal)
        _astar_path, astar_cost, expanded = sa.astar(neighbours, start, goal, manhattan(goal))
        print(f"{str(start):>8} {str(goal):>8} {len(bfs_path) - 1:>6} {ucs_cost:>6.0f} "
              f"{astar_cost:>6.0f} {expanded:>12}")

    # TODO: add greedy and DFS rows; explain in one sentence why greedy can be longer
    # than UCS on this grid, using an actual pair from the table.


if __name__ == "__main__":
    main()
