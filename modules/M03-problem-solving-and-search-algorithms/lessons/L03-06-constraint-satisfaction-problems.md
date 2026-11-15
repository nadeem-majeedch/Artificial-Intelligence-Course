# L03-06 — Constraint Satisfaction Problems

| Module | M03 · Problem Solving and Search Algorithms |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | [L03-02](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md) · [LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md) |
| Notebook | NB-03-01 Search Workbench |

[← Previous: L03-05 Adversarial](L03-05-adversarial-search-minimax-and-alpha-beta.md) · [Module home](../README.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Model** a scheduling or assignment problem as a CSP: variables, domains, constraints.
- **Implement** backtracking search with forward checking and MRV ordering.
- **Explain** why constraint propagation removes work that search would otherwise repeat.
- **Recognise** when a CSP formulation is better than a state-space search.

## 2. Prerequisite Knowledge

- Depth-first search and backtracking — [L03-02](L03-02-uninformed-search-bfs-dfs-ucs-dls-ids.md).
- Sets and dictionaries — [LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md).

## 3. Conceptual Explanation

### 3.1 Structure instead of sequence

A CSP is defined by variables, their domains, and constraints over subsets of variables. The
solution is an assignment, not a path, so the branching factor is the domain size and every leaf at
depth $n$ is a candidate solution.

Three ideas make CSPs dramatically easier than blind search:

- **Commutativity:** the order of assignments does not matter, so fix a variable order and never
  revisit it. BFS on such a space would be pointless.
- **Propagation:** once a variable is assigned, values inconsistent with it can be deleted from
  neighbours' domains immediately (forward checking), or further with arc consistency.
- **Heuristics:** choose the variable with the fewest remaining values (MRV) and the value that
  constrains others least (LCV).

### 3.2 The standard example

Map colouring: colour regions with three colours so neighbours differ. Variables are regions,
domains are colours, constraints are inequality on each edge. Backtracking with MRV solves
Australia in a handful of assignments where plain DFS tries many dead ends.

### 3.3 Where CSPs stop being easy

NP-completeness does not disappear: worst cases remain exponential. The practical gain comes from
propagation and ordering, and it is large enough that CSP solvers (SAT, CP-SAT, MiniZinc) are used
in production scheduling.

## 4. Pseudocode

```text
function BACKTRACKING(csp):
    return RECURSIVE({}, csp)

function RECURSIVE(assignment, csp):
    if complete(assignment): return assignment
    var <- SELECT_UNASSIGNED_VARIABLE(csp, assignment)   # MRV
    for value in ORDER_DOMAIN_VALUES(var, assignment):   # LCV
        if consistent(value, var, assignment):
            assignment[var] <- value
            if FORWARD_CHECK(assignment, csp):
                result <- RECURSIVE(assignment, csp)
                if result is not failure: return result
            remove assignment[var]
    return failure
```

## 5. Worked Example — map colouring

Regions: A–B, A–C, B–C, B–D, C–E, D–E. Colours {R, G, B}.

1. MRV ties everywhere at the start; pick A = R.
2. Forward check removes R from B and C. B domain {G, B}, C domain {G, B}.
3. Pick B (2 values) = G; removes G from C and D. C domain {B}, D domain {R, B}.
4. Pick C (1 value) = B; removes B from E (E domain {R, G}).
5. Pick D = R; removes R from E, leaving E = G. Complete.

Total: 5 assignments, 0 backtracking. Without forward checking, the same instance backtracks
several times because conflicts at E are discovered late.

## 6. Mathematical Formulation

A CSP is $\langle X, D, C \rangle$ with $X = \{X_1,\dots,X_n\}$, domains $D_i$, and constraints
$C_j = \langle \text{scope}, R_j \rangle$ where $R_j$ is the allowed tuple set.

Arc consistency for constraint $(X_i, X_j)$:

$$\forall a \in D_i,\ \exists b \in D_j \text{ such that } (a,b) \in R_{ij}$$

AC-3 repeatedly enforces this until no domain changes, in $O(ed^3)$ for $e$ arcs and domain size $d$.

## 7. Python Implementation

```python
def solve_csp(variables, domains, constraints, order=None):
    assignment = {}

    def consistent(var, value):
        for (v1, v2) in constraints:
            other = None
            if v1 == var:
                other = v2
            elif v2 == var:
                other = v1
            if other in assignment and assignment[other] == value:
                return False
        return True

    def backtrack():
        if len(assignment) == len(variables):
            return dict(assignment)
        unassigned = [v for v in variables if v not in assignment]
        # MRV: fewest legal values first
        var = min(unassigned,
                  key=lambda v: sum(1 for val in domains[v] if consistent(v, val)))
        for value in domains[var]:
            if not consistent(var, value):
                continue
            assignment[var] = value
            # forward check: every unassigned neighbour must keep at least one value
            ok = True
            for nxt in unassigned:
                if nxt == var:
                    continue
                if not any(consistent(nxt, val) for val in domains[nxt]):
                    ok = False
                    break
            if ok:
                result = backtrack()
                if result:
                    return result
            del assignment[var]
        return None

    return backtrack()


variables = ["A", "B", "C", "D", "E"]
domains = {v: ["R", "G", "B"] for v in variables}
edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E")]
print(solve_csp(variables, domains, edges))
```

```text
{'A': 'R', 'B': 'G', 'C': 'B', 'D': 'R', 'E': 'G'}
```

Check by hand: A–B R/G, A–C R/B, B–C G/B, B–D G/R, C–E B/G, D–E R/G — all differ. The solution is
valid, though not unique.

## 8. Practical Applications

- **Timetabling** — rooms, teachers and slots as variables with overlap constraints.
- **Nurse rostering** — coverage constraints plus fairness preferences as soft constraints.
- **Frequency assignment** — interference graph colouring for radio spectrum.
- **Sudoku and puzzles** — the canonical teaching instance; solvers handle 9×9 instantly.

## 9. Common Mistakes

- Forgetting the commutativity argument and searching assignments in all orders.
- Propagating only after a full assignment instead of incrementally.
- Using MRV when a variable has zero legal values — detect failure first.
- Modelling soft preferences as hard constraints and making the problem infeasible.
- Reporting the first solution as "the" solution when the problem is under-constrained.

## 10. Exercises

1. Add arc consistency (AC-3) and compare node counts with forward checking on 20 random 3-colouring instances.
2. Model a 4×4 Sudoku as a CSP and solve it with the code above.
3. Add a soft constraint (preferred colour) with a penalty and minimise total penalty.
4. Construct an instance where forward checking still backtracks heavily and explain why.

## 11. Self-Assessment

1. What three structural properties make CSPs easier than generic search?
2. What does MRV stand for, and why does it help?
3. What is the difference between forward checking and arc consistency?
4. Why is a CSP solution not a path?

## 12. Key Terms

**CSP**, **variable**, **domain**, **constraint**, **backtracking**, **forward checking**, **arc consistency**, **MRV**, **LCV**, **soft constraint**.

## 13. Further Reading

- Russell & Norvig, chapter 6.
- Dechter (2003), *Constraint Processing* — the systematic treatment.

## What to Do Next

You have finished the search lessons. Continue to the
[module page](../README.md) for the notebook and labs, then
[L04-01 Knowledge Representation](../../M04-knowledge-representation-and-logical-reasoning/lessons/L04-01-knowledge-representation-fundamentals.md).
