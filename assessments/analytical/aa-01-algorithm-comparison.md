# AA-01 — Choosing a Search Algorithm for a Real Constraint

| | |
| :--- | :--- |
| Assignment | 01 |
| Difficulty | Intermediate |
| Estimated time | 2 hours |
| Prerequisites | M03 |
| Format | Written analysis, no code required |
| Covers | algorithm comparison, complexity, assumptions |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

Algorithm choice is usually taught as a table of complexities. In practice the decision is driven by
three things the table omits: what the cost model actually is, how large the frontier gets in memory,
and whether the heuristic is trustworthy.

## Problem scenario

A delivery company plans routes over 5,000 stops with travel times that vary by hour. They propose
A\* with straight-line distance as the heuristic. Evaluate the proposal.

## Learning outcomes

1. Compare BFS, UCS, greedy best-first and A\* on stated criteria.
2. Reason about admissibility when edge costs are time-dependent.
3. Estimate memory requirements from branching factor and depth.
4. Recommend an approach with its assumptions made explicit.

## Tasks

1. **Cost model.** State whether straight-line distance is admissible for time-dependent costs, and
   what it would take to make it so.
2. **Comparison table.** For each algorithm: optimality, completeness, time, space, and the assumption
   it needs.
3. **Memory estimate.** With average branching factor 8 and depth 6, estimate frontier size and
   compare with available memory.
4. **Alternatives.** Describe one approach suited to time-dependent costs (e.g. time-dependent
   Dijkstra, contraction hierarchies) and its trade-offs.
5. **Recommendation.** One paragraph, with the conditions under which you would change your mind.

## Constraints

- No more than 900 words plus one table.
- State every assumption explicitly; do not assume a static graph silently.
- Cite at least two sources.

## Expected deliverables

A written report with the comparison table and the recommendation.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Cost-model analysis | 30% | admissibility question answered correctly |
| Comparison | 25% | criteria complete, assumptions named |
| Quantitative estimate | 20% | memory arithmetic correct and interpreted |
| Recommendation | 15% | conditional, defensible |
| Writing | 10% | clear, cited, within length |

## Bonus challenges

- Estimate the effect of a 20% error in travel-time estimates on route optimality.
- Discuss whether a learned heuristic could be admissible and what that would require.

---

[Assessment index](../README.md) · [AA-02](aa-02-complexity-analysis.md)
