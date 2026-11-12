# SA-M03 — Self-Assessment: Search

Module M03 · [Module](../../docs/CURRICULUM-MAP.md) · [Quiz](../quizzes/quiz-m03.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Formulate a problem as states, actions, transition, cost, goal test
- [ ] Trace BFS, DFS, UCS and A\* on a small graph
- [ ] State completeness, optimality, time and space for each
- [ ] Define admissibility and consistency, and give an example of each failing
- [ ] Explain why A\* with an admissible heuristic is optimal
- [ ] Describe iterative deepening and what it trades

## Knowledge-check questions

1. Why does BFS fail to find the cheapest path when step costs differ?
2. Construct a heuristic that is admissible but inconsistent, and show the consequence.
3. What is expanded first in UCS, and why does that guarantee optimality?
4. Give a case where greedy best-first search expands fewer nodes but returns a worse path.
5. Why does IDDFS use less memory than BFS at the same depth?

## Practical competency checklist

- [ ] Implement BFS and UCS with one interface
- [ ] Design an admissible heuristic and argue for it
- [ ] Report nodes expanded, frontier size and path cost, not just the path
- [ ] Handle unsolvable instances without crashing

## Suggested revision topics

Problem formulation · frontier and explored sets · UCS vs BFS · A\* and heuristics · admissibility
vs consistency · IDDFS · memory vs time trade-offs.

## Readiness test for M04

Without notes:

1. Trace UCS and A\* on a 6-node weighted graph and give the expansion order.
2. Prove or disprove admissibility of a given heuristic.
3. Explain the memory cost of BFS at branching factor 10 and depth 8.

If any is shaky, revisit L03-04 and L03-06 before M04.
