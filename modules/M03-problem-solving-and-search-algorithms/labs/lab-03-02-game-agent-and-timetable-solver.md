# LAB-03-02 — A Game Agent and a Timetable Solver

| | |
| :--- | :--- |
| Module | M03 · Problem Solving and Search Algorithms |
| Time | 2.5 hours |
| Level | 300 |
| Pairs with | L03-04, L03-05, L03-06 |

[Module home](../README.md) · [Lab 03-01](lab-03-01-route-planning-under-constraints.md) · [Quiz](../../../assessments/quizzes/quiz-m03.md)

## Scenario

A small college timetables 24 courses into 12 slots across 4 rooms. Two constraints are hard: a
teacher cannot be in two rooms at once, and a student group cannot attend two courses at once.
Everything else — preferring mornings, avoiding the last slot on Friday — is a preference, not a
rule.

Separately, the computing club wants a Connect Four opponent that is not embarrassing: it should
beat a random player, and it should not take longer than a second per move.

You are the one person who knows what a search algorithm is.

## Your role

You deliver two artefacts to two different stakeholders: a timetable the registrar can publish, and
a game agent the club can run on a laptop.

## What you are given

| Item | Details |
| :--- | :--- |
| Timetable data | 24 courses, 8 teachers, 6 student groups, 12 slots, 4 rooms (in the task) |
| Reference code | `code/search_algorithms.py` — hill climbing, annealing, minimax, alpha–beta, CSP solver |
| Game | Connect Four, 7×6, standard rules |

## Starter material

A runnable starter is provided: [`starters/lab-03-02_starter.py`](starters/lab-03-02_starter.py).
It loads the lab's data, prints a baseline you can compare against, and
marks the parts left for you with `TODO`. Run it before you write anything.

Module reference code: [`../code/`](../code/).

## Requirements

- **R1** Model the timetable as a CSP: variables, domains, hard constraints, soft preferences.
- **R2** Solve it with backtracking + forward checking; report nodes visited and whether it backtracks.
- **R3** Improve the solution with local search over soft preferences; report the penalty before and after.
- **R4** Implement minimax and alpha–beta for Connect Four with a stated evaluation function.
- **R5** Report nodes visited by both, at depths 4 and 6, and the win rate against a random player over 50 games.

## Tasks

1. **CSP model** (30 min). Write the variables, domains and constraints in the report before coding.
2. **Solve** (30 min). Run `solve_csp` on a reduced instance (8 courses) and then the full 24.
3. **Repair** (25 min). Use hill climbing on the soft penalty, keeping hard constraints satisfied.
4. **Game agent** (40 min). Implement the evaluation function (three-in-a-row counts, centre control) and both search variants.
5. **Measure** (20 min). Fill the node-count and win-rate tables.
6. **Recommend** (15 min). Which solver would you ship, and what would you monitor?

## Expected results

- The 8-course instance solves with fewer than 40 nodes; the full instance backtracks at least once.
- Local search reduces the soft penalty by at least 30% from the first solution.
- Alpha–beta visits roughly 40–60% of minimax's nodes at depth 6 with this evaluation.
- The agent beats a random player in at least 45 of 50 games.

## Deliverables

| File | Contents |
| :--- | :--- |
| `timetable.py` | CSP model, solver call, local-search repair |
| `connect4.py` | Game state, evaluation, minimax, alpha–beta |
| `report.md` | Model, node counts, penalty improvement, win rate, recommendation |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Model quality | 30% | hard and soft constraints clearly separated and justified | mostly clear | constraints conflated |
| Correctness | 25% | both solvers correct; pruning provably preserves value | minor bug | wrong results |
| Measurement | 20% | node counts and win rates reproducible with seeds | some numbers | no measurements |
| Recommendation | 15% | specific, with a monitoring plan | generic | absent |
| Code quality | 10% | clean interfaces, deterministic | runs | does not run |

## Extension challenges

1. Add a 13th slot and show how the search cost changes.
2. Add iterative deepening to the game agent and report the depth reached in one second.
3. Replace the hand-written evaluation with a small learned model trained on self-play.

## Reflection

1. The registrar wants a timetable that "feels fair". How did you turn that into a soft constraint,
   and what did the transformation lose?
2. Alpha–beta returns the same value as minimax. Why does that matter when you are debugging?
3. Which of the two artefacts would you trust in production, and why?

---

[Module home](../README.md) · [Lab 03-01](lab-03-01-route-planning-under-constraints.md) · [Quiz](../../../assessments/quizzes/quiz-m03.md)
