# L04-06 — Resolution and Automated Reasoning

| Module | M04 · Knowledge Representation and Logical Reasoning |
| :--- | :--- |
| Level | 200 |
| Study time | 75 minutes |
| Prerequisites | [L04-05](L04-05-unification-and-chaining.md) |
| Notebook | [NB-04-02 First-Order Inference and Unification](../notebooks/nb-04-02-first-order-inference-and-unification.ipynb) |
| Lab | LAB-04-01 Diagnostic Rule Engine |

[← Previous: L04-05 Unification, Forward Chaining and Backward Chaining](L04-05-unification-and-chaining.md) · [Module home](../README.md) · [Next: L04-07 Semantic Networks, Frames, Ontologies and Expert Systems →](L04-07-rule-based-and-expert-systems.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. Procedure: a resolution refutation by hand](#4-procedure-a-resolution-refutation-by-hand)
- [5. Worked Examples](#5-worked-examples)
- [6. Complexity](#6-complexity)
- [7. Python Implementation](#7-python-implementation)
- [8. Visual Explanation — the resolution lattice](#8-visual-explanation--the-resolution-lattice)
- [9. Real-World Application](#9-real-world-application)
- [10. Common Misconceptions](#10-common-misconceptions)
- [11. Exercises](#11-exercises)
- [12. Self-Assessment](#12-self-assessment)
- [13. Key Terms](#13-key-terms)
- [14. Further Reading](#14-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Convert** a formula to clause form, naming each of the seven steps.
- **Run** a resolution refutation by hand on a three-clause example.
- **Explain** why resolution proves entailment by deriving the empty clause.
- **Apply** unification inside resolution, and say why factoring matters in principle.
- **Judge** when resolution is the right tool and when its blind search is too expensive.

## 2. Prerequisite Knowledge

Clauses, CNF and unification from [L04-02](L04-02-propositional-logic.md) and [L04-05](L04-05-unification-and-chaining.md). You should be able to negate a formula until `¬` touches only predicates.

## 3. Conceptual Explanation

### 3.1 One rule instead of nine

Chaining needs a different rule for each pattern. Resolution needs one:

$$
\frac{p \lor q \qquad \neg p \lor r}{q \lor r}
$$

Read it as cancellation: a literal and its negation disappear, and the remaining literals are joined. In first-order form, the two occurrences of `p` need not be syntactically identical — they only need to **unify**, and the unifier is applied to the resolvent.

One rule is enough because every propositional formula can be rewritten into clauses, and every first-order formula can too (with skolemisation). That is the whole architecture of automated theorem proving.

### 3.2 Refutation, not construction

Resolution does not build the query; it assumes the query is **false** and derives a contradiction:

$$
KB \models \alpha \quad\equiv\quad KB \wedge \neg\alpha \text{ is unsatisfiable.}
$$

So the procedure is: add `¬α` to the clauses, resolve until the **empty clause** `□` appears. `□` is unsatisfiable, so the assumption `¬α` must be false, so `α` follows from the KB.

This is why a resolution proof of `mortal(socrates)` starts by adding `¬mortal(socrates)`. Students who forget the negation get a proof of nothing.

### 3.3 Clause form in seven steps

| Step | Operation | Example |
| ---: | :--- | :--- |
| 1 | Eliminate `↔` | `p ↔ q` → `(p→q) ∧ (q→p)` |
| 2 | Eliminate `→` | `p → q` → `¬p ∨ q` |
| 3 | Push negations inward (De Morgan, quantifier laws) | `¬∀x p(x)` → `∃x ¬p(x)` |
| 4 | Standardise variables apart | rename each quantifier's variable uniquely |
| 5 | Skolemise: replace each `∃` by a fresh constant or function of the enclosing `∀`s | `∀x ∃y parent(y,x)` → `parent(sk0(x), x)` |
| 6 | Drop universal quantifiers | all variables are implicitly universal |
| 7 | Distribute `∨` over `∧`, producing a set of clauses | `(a∧b) ∨ c` → `(a∨c) ∧ (b∨c)` |

The engine prints the results of steps 4–7:

```text
== universal rule in clause form ==
ancestor(x_1, y_1) or not parent(x_1, y_1)
== negation of query as clauses ==
not ancestor(ann, dan)
== exists skolemisation ==
parent(ann, sk0)
```

`sk0` is a skolem constant: "somebody, we do not know who". If the existential sat inside a universal, it would be a function of that universal's variable (`sk0(x)`), because the witness may depend on `x`.

### 3.4 A propositional refutation, step by step

KB: `rain → wet`, `wet → ¬indoors`, `rain`. Query: `¬indoors`.

Clauses: `¬rain ∨ wet`, `¬wet ∨ ¬indoors`, `rain`, and the negated query `indoors`.

| Step | Clause | From |
| ---: | :--- | :--- |
| 1 | `¬rain ∨ wet` | KB |
| 2 | `¬wet ∨ ¬indoors` | KB |
| 3 | `rain` | KB |
| 4 | `indoors` | negated query |
| 5 | `wet` | resolve 1, 3 |
| 6 | `¬indoors` | resolve 2, 5 |
| 7 | `□` | resolve 4, 6 |

Seven clauses, two resolutions, one contradiction. The engine's own trace agrees (renaming aside):

```text
start: 4 clauses
resolve not rain or wet with not indoors or not wet -> not indoors or not rain
resolve not rain or wet with rain -> wet
resolve not indoors or not wet with indoors -> not wet
resolve not rain or wet with not wet -> not rain
resolve not indoors or not wet with wet -> not indoors
resolve wet with not wet -> empty clause
```

The engine tries pairs in a fixed order, so its route is longer than the hand proof. Both are valid; a proof is not required to be shortest, only correct.

### 3.5 Resolution with unification

For FOL, two literals resolve when their atoms unify:

```text
clause 1:  ancestor(x, y) ∨ ¬parent(x, y)
clause 2:  parent(ann, bob)
resolvent: ancestor(ann, bob)        with θ = {x↦ann, y↦bob}
```

The engine's proof of `mortal(socrates)` from "all humans are mortal" and "Socrates is human":

```text
given: mortal(x_0) or not human(x_0)
given: human(socrates)
given: not mortal(socrates)
resolve mortal(x_0) or not human(x_0) with human(socrates) -> mortal(socrates)
resolve mortal(x_0) or not human(x_0) with not mortal(socrates) -> not human(socrates)
resolve human(socrates) with not human(socrates) -> empty clause
```

Note the renaming `x_0`: the same clause can be reused with fresh variables, which is how one universally quantified clause serves many instances.

### 3.6 Why naive resolution is not enough

Completeness says a refutation exists; it does not say you will find it soon. On the four-person ancestor KB (two rules, three facts, one negated query) the engine starts with six clauses and takes this many lines to close:

```text
proved True trace lines 274
```

Six clauses in, 274 trace lines out — most of them clauses that no human would generate. Add a fourth generation of people, or a rule with five literals, and the count grows faster than the family tree. This is why real provers add **strategies**:

| Strategy | Idea | Effect |
| :--- | :--- | :--- |
| Unit preference | resolve with single-literal clauses first | short clauses, quick progress |
| Set of support | only resolve clauses descended from the negated query | ignores irrelevant KB parts |
| Subsumption | delete a clause implied by a more general one | shrinks the search space |
| Ordering / selection | fix which literal is resolved on | makes search deterministic |
| Hyperresolution | resolve a nucleus against a set of electrons at once | suits Horn clauses |

The engine in this module implements none of them, deliberately: you can read all of it, and its inefficiency is the lesson.

## 4. Procedure: a resolution refutation by hand

```text
1. Write the KB and the NEGATED query.
2. Convert everything to clauses (the seven steps).
3. Number the clauses.
4. Pick two clauses containing complementary literals; unify them if needed.
5. Write the resolvent, and record the parents and the unifier.
6. Repeat. Stop at the empty clause (proved) or when no new clauses appear (not proved).
```

Step 6 has two stopping conditions and they mean different things. `□` means the query is entailed. Exhaustion without `□` means no refutation exists — but only for a *complete* strategy, and only if the clause set is finite.

## 5. Worked Examples

### Example 1 — a two-step FOL refutation

KB: `∀x (student(x) → passed(x, cs101))`, `student(ali)`. Query: `passed(ali, cs101)`.

| Step | Clause | Justification |
| ---: | :--- | :--- |
| 1 | `¬student(x) ∨ passed(x, cs101)` | KB, clause form |
| 2 | `student(ali)` | KB |
| 3 | `¬passed(ali, cs101)` | negated query |
| 4 | `passed(ali, cs101)` | resolve 1, 2 with `{x↦ali}` |
| 5 | `□` | resolve 3, 4 |

### Example 2 — skolemisation that matters

"Every student has an advisor" and "no student is their own advisor" should *not* entail a contradiction. Formalised:

```text
∀x (student(x) → ∃y (advisor(y, x) ∧ y ≠ x))
```

Skolemising gives `advisor(sk0(x), x)` — the advisor depends on the student, which is correct. If you wrongly used a single constant `advisor(c, x)`, the formula would claim one global advisor for everyone, a stronger and false statement. The dependency structure of the skolem term is the whole content of the quantifier order.

### Example 3 — resolution proves non-entailment by failing, sometimes

Query `wet → rain` against the rain KB: the negation adds `wet ∧ ¬rain`, which is consistent, so no refutation exists and the engine reports failure. That failure is informative only because the clause set is finite. In FOL with function symbols, failure to close may simply mean the loop has not finished — the semi-decidability from [L04-04](L04-04-first-order-logic-and-quantifiers.md) showing up as a runtime property.

## 6. Complexity

| Problem | Worst case |
| :--- | :--- |
| Propositional resolution | exponential in the number of clauses |
| First-order resolution | semi-decidable; no bound on proof length |
| Horn-clause resolution (SLD) | linear in proof length, exponential in depth |
| Unit propagation on Horn clauses | linear in the KB size |

The gap between the first two rows and the last is why Datalog engines are fast and general theorem provers are not.

## 7. Python Implementation

The core loop is short; the work is in clause form.

```python
def resolve(ci, cj):
    """All binary resolvents of two clauses of (positive?, atom) literals."""
    out = []
    for pi, ai in ci:
        for pj, aj in cj:
            if pi == pj:
                continue
            theta = unify_atoms(ai, aj)
            if theta is None:
                continue
            merged = {(p, apply(a, theta)) for p, a in ci if (p, a) != (pi, ai)}
            merged |= {(p, apply(a, theta)) for p, a in cj if (p, a) != (pj, aj)}
            out.append(frozenset(merged))
    return out


def refute(clauses, max_steps=200):
    seen = set(clauses)
    for _ in range(max_steps):
        new = []
        for i, ci in enumerate(clauses):
            for cj in clauses[i + 1:]:
                for r in resolve(ci, cj):
                    if not r:                 # empty clause
                        return True
                    if r not in seen:
                        seen.add(r)
                        new.append(r)
        if not new:
            return False
        clauses = clauses + new
    return False
```

The full version with clause conversion, skolemisation and a readable trace is [`code/fol_core.py`](../code/fol_core.py) (`to_clauses`, `resolve_clauses`, `fol_resolution`); the propositional variant is [`code/prop_logic.py`](../code/prop_logic.py) (`clauses`, `resolution_refutation`).

## 8. Visual Explanation — the resolution lattice

```text
   ¬rain ∨ wet        rain          ¬wet ∨ ¬indoors      indoors
        \              /                    \               /
          \          /                       \             /
             wet                              ¬indoors
                \                              /
                 \                            /
                        □  (empty clause)
```

*Text description:* two independent chains of cancellation that meet at the empty clause. Each arrow is one resolution step; the empty clause is the proof. In FOL the arrows also carry a unifier, and the diagram becomes a tree whose leaves are the input clauses.

## 9. Real-World Application

**SMT solvers in software engineering.** Modern verifiers (Dafny, Kani, TLA+ tools) translate program properties to clauses and let an SMT solver refute the negation. The solver is a resolution engine with theories (arithmetic, arrays) bolted on; the loop above is its skeleton.

**Knowledge-graph query answering.** Conjunctive queries over ontologies can be answered by resolution with the ontology's clauses, which is how OWL reasoners answer "is this individual a member of that class?" and why the choice of fragment (EL, RL, QL) decides whether the answer arrives in milliseconds or never.

## 10. Common Misconceptions

| Misconception | Correction |
| :--- | :--- |
| "Resolution proves the query directly." | It refutes the negation; the empty clause is the proof. |
| "Any two clauses can be resolved." | They need complementary literals, and the atoms must unify — otherwise the "resolvent" is unsound. |
| "Skolem constants are ordinary individuals." | They are witnesses with no name; using one where a function is needed changes the meaning. |
| "More steps means a worse proof." | Search strategy affects length; correctness does not depend on finding the shortest. |
| "Failure to find `□` proves the query false." | Only for a complete strategy on a finite clause set; otherwise it may mean "not finished". |

## 11. Exercises

1. **Convert.** Take `∀x (p(x) → (q(x) ↔ r(x)))` to clause form, showing each of the seven steps.
2. **Refute.** Prove `q` from `{p ∨ q, ¬p ∨ r, ¬r}` by resolution, numbering clauses and resolvents.
3. **Unify inside resolution.** Resolve `¬parent(x, y) ∨ ancestor(x, y)` with `parent(ann, bob)` and with `parent(bob, cid)` separately. What differs?
4. **Skolemise.** Convert `∀x ∃y ∀z (p(x, y) ∧ q(y, z))` to clause form and explain the arity of the skolem function.
5. **Count the explosion.** For 10 clauses, how many pairs must a naive round examine? What does the ancestor example's 274-line trace suggest about the practical limit?

## 12. Self-Assessment

**1.** Why does the empty clause prove the query, rather than proving the KB inconsistent?
<details><summary>Show answer</summary>

The empty clause is derived from `KB ∧ ¬α`. If that set is unsatisfiable, no model makes the KB true and `α` false, so every model of the KB satisfies `α` — that is entailment. The KB itself may well be satisfiable; it is the KB *plus the negated query* that has no model.

</details>

**2.** What is the difference between a skolem constant and a skolem function, and what determines which you get?
<details><summary>Show answer</summary>

An existential with no enclosing universal becomes a fresh constant (one witness). An existential inside universals becomes a function of those universals' variables, because the witness may depend on them. The nesting of quantifiers determines the arity.

</details>

**3.** Resolution is complete, yet the engine may fail to prove a true entailment. How can both be true?
<details><summary>Show answer</summary>

Completeness is a property of the *calculus*: if a refutation exists, some sequence of resolution steps finds it. The engine searches with a fixed order under a step limit, and in FOL the search space may be infinite, so it can stop early. Completeness guarantees the existence of a proof, not that a bounded search finds it.

</details>

**4.** Give a clause pair with complementary literals that must *not* be resolved, and explain the error.
<details><summary>Show answer</summary>

`p(x) ∨ q(x)` and `¬p(a) ∨ r(a)`: resolving on `p` with `{x↦a}` gives `q(a) ∨ r(a)`, which is correct. A bad pair is `p(x)` and `¬p(y)` where the same variable name is reused across clauses without standardising apart — after renaming it is fine, but if you unify `x` with itself incorrectly you may drop a literal you needed. More directly: resolving on `p(a)` and `¬p(a)` when other literals share variables requires applying the unifier to *all* remaining literals; forgetting that produces an unsound resolvent.

</details>

**5.** Why do practical systems restrict resolution instead of using full FOL?
<details><summary>Show answer</summary>

Because full FOL refutation search has no termination guarantee and explodes combinatorially. Restricting to Horn clauses (SLD) or function-free clauses (Datalog) gives polynomial or linear behaviour with predictable termination, at the cost of expressiveness — a trade every deployed rule engine makes explicitly.

</details>

## 13. Key Terms

- **Clause** — a disjunction of literals.
- **Clause form (CNF)** — a conjunction of clauses.
- **Skolemisation** — replacing existentials with fresh constants/functions.
- **Refutation** — deriving the empty clause from KB plus negated query.
- **Empty clause (`□`)** — unsatisfiable; the goal of a refutation.
- **Factoring** — merging two literals of one clause that unify.
- **Set of support** — restricting resolution to clauses descended from the query.

## 14. Further Reading

- Robinson, J. A. (1965). "A Machine-Oriented Logic Based on the Resolution Principle." *JACM* 12(1). — The original paper; still readable.
- Russell & Norvig (2021), *AIMA* 4th ed., §9.5. — Clause form, skolemisation and resolution with the same conventions.
- de Moura, L. & Bjørner, N. (2011). "Satisfiability Modulo Theories: Introduction and Applications." *CACM* 54(9). — Where resolution meets arithmetic in industrial tools.

## What to Do Next

Read [L04-07 — Frames, Ontologies and Expert Systems](L04-07-rule-based-and-expert-systems.md) to see the representations that won in practice, and why they are less logical than this lesson and more usable.

---

**Navigation:** [← Previous: L04-05 Unification, Forward Chaining and Backward Chaining](L04-05-unification-and-chaining.md) · [Module home](../README.md) · [Next: L04-07 Semantic Networks, Frames, Ontologies and Expert Systems →](L04-07-rule-based-and-expert-systems.md)
