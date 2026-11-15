"""LAB-03-02 starter — a game agent, then a timetable solver.

Part A gives you a complete tic-tac-toe tree search. Part B gives you the CSP
encoding harness with one constraint implemented and two left to you.

Run:  python lab-03-02_starter.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "code"))

import search_algorithms as sa  # noqa: E402

# --------------------------------------------------------------- Part A: game
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
         (0, 4, 8), (2, 4, 6)]


def winner(board):
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def terminal(board):
    return winner(board) is not None or "." not in board


def children(board):
    out = []
    for i, cell in enumerate(board):
        if cell == ".":
            nxt = list(board)
            nxt[i] = "X" if board.count("X") == board.count("O") else "O"
            out.append(tuple(nxt))
    return out


def evaluate(board):
    """Score from X's point of view; deeper wins are NOT discounted here."""
    result = winner(board)
    if result == "X":
        return 1
    if result == "O":
        return -1
    return 0


def best_move(board, depth=9):
    maximizing = board.count("X") == board.count("O")
    scored = [(sa.minimax(child, depth - 1, not maximizing, children, evaluate, terminal), child)
              for child in children(board)]
    if not scored:
        return None
    value = max(score for score, _ in scored) if maximizing else min(score for score, _ in scored)
    # TODO: prefer the fastest win / slowest loss by scoring depth, not just the result
    return value, [child for score, child in scored if score == value][0]


# ---------------------------------------------------------- Part B: timetable
SLOTS = ["Mon-9", "Mon-11", "Tue-9", "Tue-11", "Wed-9"]
COURSES = ["AI", "DB", "OS", "NET"]
ROOMS = ["R1", "R2"]


def build_domains():
    """Each course picks one (slot, room) pair."""
    return {course: [(slot, room) for slot in SLOTS for room in ROOMS] for course in COURSES}


def same_slot_conflict(_a, _b):
    """Two different courses may not share a slot, in any room."""
    return lambda slot_a, slot_b: slot_a[0] != slot_b[0]


def room_capacity(_a, _b):
    # TODO: replace with "same slot implies different rooms" and see whether the
    # five-slot, four-course instance stays feasible.
    return lambda slot_a, slot_b: True


def main():
    board = tuple(".........")
    value, move = best_move(board)
    print("empty board: minimax value", value, "-> play", move)
    print("this is a draw with perfect play; your task is to make the agent prove it\n")

    variables = list(build_domains())
    edges = {}
    for i, a in enumerate(variables):
        for b in variables[i + 1:]:
            edges[(a, b)] = same_slot_conflict(a, b)
    solution = sa.solve_csp(variables, build_domains(), edges)
    print("timetable:", solution)
    # TODO: add the room constraint, then report whether a solution still exists.


if __name__ == "__main__":
    main()
