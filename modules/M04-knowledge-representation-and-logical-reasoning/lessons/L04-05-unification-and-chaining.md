# L04-05 — Unification, Forward Chaining and Backward Chaining

| Module | M04 · Knowledge Representation and Logical Reasoning |
| :--- | :--- |
| Level | 200 |
| Study time | 75 minutes |
| Prerequisites | [L04-04](L04-04-first-order-logic-and-quantifiers.md) |
| Notebook | [NB-04-02 First-Order Inference and Unification](../notebooks/nb-04-02-first-order-inference-and-unification.ipynb) |
| Lab | LAB-04-01 Diagnostic Rule Engine |

[← Previous: L04-04 First-Order Logic: Predicates, Terms and Quantifiers](L04-04-first-order-logic-and-quantifiers.md) · [Module home](../README.md) · [Next: L04-06 Resolution and Automated Reasoning →](L04-06-resolution-and-automated-reasoning.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. Procedure: tracing a chain](#4-procedure-tracing-a-chain)
- [5. Worked Examples](#5-worked-examples)
- [6. Complexity](#6-complexity)
- [7. Python Implementation](#7-python-implementation)
- [8. Visual Explanation — chaining directions](#8-visual-explanation--chaining-directions)
- [9. Real-World Application](#9-real-world-application)
- [10. Common Misconceptions](#10-common-misconceptions)
- [11. Exercises](#11-exercises)
- [12. Self-Assessment](#12-self-assessment)
- [13. Key Terms](#13-key-terms)
- [14. Further Reading](#14-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Define** a substitution, a unifier and the most general unifier (MGU).
- **Compute** an MGU by hand for two atoms, and say when none exists.
- **Explain** why rules must be standardised apart before matching, and what goes wrong if they are not.
- **Trace** a forward chain and a backward chain over the same knowledge base.
- **Choose** forward or backward chaining for a described application, with a cost argument.

## 2. Prerequisite Knowledge

Terms, predicates, quantifiers and scope from [L04-04](L04-04-first-order-logic-and-quantifiers.md), and modus ponens from [L04-03](L04-03-inference-rules-and-equivalence.md). You should be able to read a rule with variables aloud as a pattern.

## 3. Conceptual Explanation

### 3.1 Why matching is not enough

Propositional rules match exactly: `rain` matches `rain`. First-order rules contain variables, so `parent(ann, x)` must match `parent(ann, bob)` by binding `x`. That binding is a **substitution**, written `θ = {x ↦ bob}`.

A **unifier** of two atoms is a substitution making them identical. The **most general unifier** is the least committal one: it binds only what must be bound. `{x ↦ bob}` unifies `parent(ann, x)` with `parent(ann, bob)`; `{x ↦ bob, y ↦ cid}` also unifies them but is less general, because it commits to a value for `y` that nothing required.

MGUs matter because any other unifier is an instance of the MGU. Using the MGU loses no solutions and produces no redundant ones — which is exactly what a complete inference procedure needs.

### 3.2 The algorithm, in words

```
unify(x, y, θ):
  1. Apply θ to both sides (follow existing bindings).
  2. If they are identical, return θ.
  3. If one is a variable v, and v does not occur in the other (occurs check),
     return θ ∪ {v ↦ other}.
  4. If both are functions/predicates with the same name and arity,
     unify their arguments pairwise, threading θ through.
  5. Otherwise, fail.
```

Three details do all the work:

- **Walk before compare.** `{x ↦ y, y ↦ bob}` must resolve `x` to `bob`. Forgetting to follow binding chains is the classic bug.
- **Occurs check.** `x` cannot unify with `f(x)`; no finite term equals a term containing itself.
- **Thread the substitution.** After unifying the first argument pair, the binding must be visible when unifying the second. Unifying arguments independently gives wrong answers on shared variables.

### 3.3 Standardising apart

Two rules both use `x`, and their meanings are unrelated:

```text
rule 1:  parent(x, y) → ancestor(x, y)
rule 2:  parent(x, y) ∧ ancestor(y, z) → ancestor(x, z)
```

If you fire rule 2 with a fact that binds `x`, then fire rule 1 with the *same* `x`, the rules interfere: a variable in one has silently become bound by the other. The fix is mechanical: rename every variable in a rule to a fresh name each time it is used (`x_1`, `x_2`, …). The engine's `_fresh` does this, and every trace you see with names like `x_0` is the result.

This is not a cosmetic detail. Without standardising apart, forward chaining derives fewer facts than it should, and the bug is invisible until a case happens to share a variable name.

### 3.4 Forward chaining

Start from facts, find rules whose premises are all satisfied under some substitution, add the instantiated conclusion, repeat until nothing new appears.

```text
forward_chain(rules, facts):
    known <- facts
    REPEAT
        new <- {}
        FOR each rule, each MGU of its premises against known:
            new <- new + instantiate(head, MGU)
        IF new ⊆ known: RETURN known
        known <- known ∪ new
```

Termination: for definite clauses without function symbols, the set of derivable ground atoms is finite (the Herbrand base), so the loop halts. With function symbols, `p(x) → p(f(x))` generates infinitely many atoms and the loop never stops — a concrete reason production systems ban functions.

### 3.5 Backward chaining

Start from the goal and work back: find rules whose head unifies with the goal, then recursively prove their premises.

```text
prove(goal, θ):
    FOR each fact: if unify(goal, fact, θ) succeeds: yield θ
    FOR each rule with head h:
        if unify(goal, h, θ) succeeds:
            prove premises left to right, then yield
```

This is SLD resolution restricted to definite clauses. It is goal-directed, so it ignores facts no query needs — the opposite trade from forward chaining.

### 3.6 The same KB, both directions

The family KB in [`code/knowledge_bases.py`](../code/knowledge_bases.py) has six people, five `parent` facts and three rules. Forward chaining computes the whole closure; backward chaining answers one question.

Forward (real output):

```text
seed facts: 35
iter 1: ancestor(ann, bob) from rule 'a parent is an ancestor'
iter 1: ancestor(ann, cid) from rule 'a parent is an ancestor'
iter 1: ancestor(bob, dan) from rule 'a parent is an ancestor'
iter 1: ancestor(bob, eve) from rule 'a parent is an ancestor'
iter 1: ancestor(cid, finn) from rule 'a parent is an ancestor'
iter 1: sibling(bob, cid) from rule 'children of a common parent are siblings'
iter 1: sibling(cid, bob) from rule 'children of a common parent are siblings'
iter 1: sibling(dan, eve) from rule 'children of a common parent are siblings'
iter 1: sibling(eve, dan) from rule 'children of a common parent are siblings'
iter 2: ancestor(ann, dan) from rule 'an ancestor of a child is an ancestor'
iter 2: ancestor(ann, eve) from rule 'an ancestor of a child is an ancestor'
iter 2: ancestor(ann, finn) from rule 'an ancestor of a child is an ancestor'
fixpoint after 3 iteration(s)
```

Backward (real output):

```text
== family: who is an ancestor of dan? ==
   bob
   ann
```

Three iterations and 47 atoms in the closure, versus one focused search for a single query. The 35 seed facts include the 30 `different` pairs, which is why the count is high — another visible cost of encoding inequality as data. Now the advising KB, where the same engine answers a different question shape:

```text
== advising: eligible courses (forward chaining) ==
   eligible(ali, cs201)
   eligible(ali, ds201)
   eligible(bea, cs201)
   eligible(bea, cs301)
   eligible(bea, ds201)
   eligible(chen, cs201)
   eligible(chen, cs301)
   eligible(chen, ds201)

== advising: what blocks chen from cap400? ==
   missing: ['cs301']
   chen eligible for cap400? []
```

Note the empty list from backward chaining: `cap400` needs `cs301` and `ds201`; Chen has `ds201` but not `cs301`, so no substitution is found. The procedural `missing_prerequisites` routine reports *why* — the logic alone can only say "not derivable". That division of labour (logic for entailment, code for absence) is the standard design.

## 4. Procedure: tracing a chain

```text
Forward:
1. Write the facts. These are iteration 0.
2. For each rule, match every premise against the current set, standardising apart.
3. Record each new conclusion with the rule and binding that produced it.
4. Repeat until an iteration adds nothing.

Backward:
1. Write the goal with its variables.
2. Find rules or facts whose head unifies with it; show the binding.
3. Replace the goal by the rule's premises, applying the binding.
4. Recurse leftmost-first; report the final binding, or "no proof".
```

## 5. Worked Examples

### Example 1 — an MGU by hand

Unify `ancestor(x, finn)` with `ancestor(ann, y)`:

| Step | Pair | Binding added |
| ---: | :--- | :--- |
| 1 | `ancestor(x, finn)` vs `ancestor(ann, y)` | names match, arity 2 |
| 2 | `x` vs `ann` | `{x ↦ ann}` |
| 3 | `finn` vs `y` | `{x ↦ ann, y ↦ finn}` |

MGU: `{x ↦ ann, y ↦ finn}`. Check by applying it to both: `ancestor(ann, finn)` on each side.

### Example 2 — two failures

| Pair | Result | Reason |
| :--- | :--- | :--- |
| `f(x, b)` vs `f(a, y)` | `{x↦a, y↦b}` | succeeds |
| `f(x, x)` vs `f(a, b)` | fail | `x` would need to be both `a` and `b` |
| `x` vs `f(x)` | fail | occurs check |
| `parent(x, y)` vs `sibling(x, y)` | fail | predicate names differ |

The third row is subtle: `x = f(x)` has no finite solution. The engine confirms with `None` in [L04-04](L04-04-first-order-logic-and-quantifiers.md)'s output.

### Example 3 — a derivation with bindings

KB: `parent(ann, bob)`, `parent(bob, cid)`, and the two ancestor rules. Query `ancestor(ann, cid)`.

| Step | Goal | Rule applied | Binding |
| ---: | :--- | :--- | :--- |
| 1 | `ancestor(ann, cid)` | recursive ancestor rule | `{x↦ann, z↦cid}` |
| 2 | `parent(ann, y)`, `ancestor(y, cid)` | fact `parent(ann, bob)` | `{y↦bob}` |
| 3 | `ancestor(bob, cid)` | base ancestor rule | `{x↦bob, y↦cid}` |
| 4 | `parent(bob, cid)` | fact | ✓ |

The proof is a tree whose leaves are facts. Every internal node is one rule application with one MGU — which is why unification is the engine of every logic-based system you will meet.

## 6. Complexity

| Operation | Cost |
| :--- | :--- |
| One unification | $O(\lvert t_1 \rvert + \lvert t_2 \rvert)$ with the occurs check |
| Forward chain, $n$ atoms, $m$ rules, $k$ iterations | $O(k \cdot m \cdot \text{cost of join})$ |
| Backward chain, branching $b$, depth $d$ | $O(b^d)$ without memoisation |
| Datalog entailment (no functions, safe rules) | polynomial in the data size |

The join in forward chaining is the expensive part: matching a two-premise rule is a nested loop over facts, and a five-premise rule is five nested loops. Real engines use the Rete algorithm to share that matching across iterations, which is why they can handle thousands of rules at interactive speed.

## 7. Python Implementation

The complete engine is [`code/fol_core.py`](../code/fol_core.py); this is the core of it, stripped to what you need to read.

```python
def unify(x, y, subst=None):
    """Most general unifier of two terms, or None."""
    if subst is None:
        subst = {}
    x, y = walk(x, subst), walk(y, subst)      # follow existing bindings
    if x == y:
        return subst
    if isinstance(x, Var):
        if occurs(x, y):
            return None
        return {**subst, x.name: y}
    if isinstance(y, Var):
        if occurs(y, x):
            return None
        return {**subst, y.name: x}
    if isinstance(x, Func) and isinstance(y, Func) and x.name == y.name \
            and len(x.args) == len(y.args):
        for a, b in zip(x.args, y.args):
            subst = unify(a, b, subst)        # thread the substitution
            if subst is None:
                return None
        return subst
    return None


def forward_chain(rules, facts, max_iterations=50):
    known, log = set(facts), []
    for iteration in range(1, max_iterations + 1):
        added = set()
        for rule in rules:
            fresh = rename_apart(rule, iteration)      # x -> x_<iteration>
            for subst in match_all(fresh.body, known):
                added.add(instantiate(fresh.head, subst))
        if not added:
            return known, log
        known |= added
    return known, log
```

Running the family KB through it produces the closure in §3.6. The two functions you should be able to write from memory are `walk` (follow binding chains) and `match_all` (join premises against facts); everything else is bookkeeping.

## 8. Visual Explanation — chaining directions

```text
facts:   parent(ann,bob)  parent(bob,cid)  parent(cid,finn)
            |                 |                |
            v                 v                v
         ancestor         ancestor          ancestor        (iteration 1)
            \                |               /
             \               v              /
              +------> ancestor <----------+                 (iteration 2, 3)

goal:    ancestor(ann, finn)?
             ^
             |  rule needs parent(ann,y) and ancestor(y,finn)
        y=bob -> parent(ann,bob) ok, ancestor(bob,finn)?
                    y=cid -> parent(bob,cid) ok, ancestor(cid,finn)?
                                fact, done
```

*Text description:* forward chaining fills the triangle from the facts upward; backward chaining walks down one branch of the same tree. Same KB, same conclusions, opposite order of work.

## 9. Real-World Application

**Fraud and eligibility rules.** A bank's transaction monitoring forward-chains over facts such as `transfer(u, v, amount)`, deriving `suspicious(u)` and attaching the rule chain as an explanation. Forward chaining suits it because new facts arrive continuously and many alerts must be evaluated.

**Clinical alerts and configuration.** Backward chaining suits "why is this order blocked?" because the query drives the search: prove `blocked(order)`, then walk the premises. The explanation is the proof tree, printed for the clinician.

**Datalog in production.** Cloud security tools (e.g. policy analysis of IAM rules) and program-analysis frameworks use Datalog: Horn clauses without function symbols, so entailment is polynomial and queries terminate. The restriction is the point.

## 10. Common Misconceptions

| Misconception | Correction |
| :--- | :--- |
| "Unification is equality." | Unification *finds* a substitution that makes two terms equal; equality is a predicate inside the logic. |
| "Any unifier will do." | A non-MGU unifier can miss solutions and duplicate work; completeness depends on using the MGU. |
| "Rules can share variable names safely." | Only after standardising apart. Shared names cause silent cross-talk between rules. |
| "Forward chaining is always slower." | It derives everything once; if you need many queries, that is cheaper than re-searching per query. |
| "Backward chaining fails means false." | It means not derivable from the KB. Under the closed-world assumption you may report false, but that is an extra assumption. |

## 11. Exercises

1. **Compute MGUs.** (a) `p(x, f(y))` vs `p(a, f(b))`; (b) `p(x, x)` vs `p(y, b)`; (c) `p(f(x))` vs `p(x)`.
2. **Standardise.** Write the two ancestor rules with all variables renamed to unique names, then say which bindings the first firing produces.
3. **Trace forward.** Starting from three `parent` facts of your choice, list every atom derived in each iteration.
4. **Trace backward.** For goal `sibling(dan, eve)`, draw the proof tree and mark each binding.
5. **Design the direction.** For each system, choose chaining direction and justify: (a) a tax calculator answering one question per user; (b) a network monitor evaluating every packet; (c) a course catalogue answering thousands of student queries per hour.

## 12. Self-Assessment

**1.** Why must a complete inference procedure use the most general unifier rather than any unifier?
<details><summary>Show answer</summary>

Every other unifier is an instance of the MGU, so any conclusion reachable with a more specific substitution is also reachable, later, from the MGU's conclusion by further instantiation. Using a non-general unifier can therefore miss solutions (if it over-commits) or duplicate them (if several specifics are tried), breaking completeness or efficiency.

</details>

**2.** What breaks if you forget to standardise rules apart?
<details><summary>Show answer</summary>

Variables with the same name in different rules become accidentally shared. A binding made while firing one rule then constrains the other, so some legitimate matches fail and the closure is incomplete. The bug is intermittent, which is what makes it dangerous; renaming per use removes it entirely.

</details>

**3.** Give a rule set where forward chaining does not terminate, and explain the cause precisely.
<details><summary>Show answer</summary>

`p(x) → p(f(x))` with fact `p(a)` derives `p(f(a))`, `p(f(f(a)))`, … Each conclusion is a new atom, so the fixpoint is never reached: the Herbrand universe is infinite because function symbols build unboundedly nested terms. Banning function symbols (Datalog) makes the Herbrand base finite and guarantees termination.

</details>

**4.** A backward-chaining engine returns no proof for `eligible(chen, cap400)`. List two different reasons this could be true and how you would distinguish them.
<details><summary>Show answer</summary>

(a) A required fact is genuinely absent — Chen has not passed `cs301`, which the procedural checker confirms. (b) The search was cut off by a depth or step limit, or the rule was never fired because a premise is underivable due to a modelling gap. Distinguish by running forward chaining to fixpoint (does the atom appear?) and by inspecting the failed goals, or by checking the prerequisite list directly.

</details>

**5.** Why does the advising KB need a Python function to report missing prerequisites, when it already has a rule engine?
<details><summary>Show answer</summary>

Because definite clauses express only positive conclusions. "Chen lacks cs301" is a negative fact, and without negation as failure the engine cannot derive it. The procedural check supplies the closed-world assumption explicitly, and states which prerequisite is missing — information the logic does not represent at all.

</details>

## 13. Key Terms

- **Substitution** — a mapping from variables to terms.
- **Unifier / MGU** — a substitution making two expressions identical / the most general such.
- **Occurs check** — rejecting self-referential bindings.
- **Standardising apart** — renaming a rule's variables on each use.
- **Forward chaining** — data-driven rule application to a fixpoint.
- **Backward chaining** — goal-driven proof search.
- **Datalog** — Horn clauses without function symbols; polynomial entailment.

## 14. Further Reading

- Russell & Norvig (2021), *AIMA* 4th ed., §9.2 and §9.4. — Unification and the two chaining algorithms, with pseudocode close to this lesson's.
- Ceri, S., Gottlob, G. & Tanca, L. (1989). "What You Always Wanted to Know About Datalog." *IEEE TKDE* 1(1). — The classic survey of the tractable fragment.
- Forgy (1982), "Rete." — How forward-chaining engines make repeated matching cheap.

## What to Do Next

Work [NB-04-02](../notebooks/nb-04-02-first-order-inference-and-unification.ipynb) until you can predict each binding, then read [L04-06 — Resolution and Automated Reasoning](L04-06-resolution-and-automated-reasoning.md), which replaces chaining with a single complete rule.

---

**Navigation:** [← Previous: L04-04 First-Order Logic: Predicates, Terms and Quantifiers](L04-04-first-order-logic-and-quantifiers.md) · [Module home](../README.md) · [Next: L04-06 Resolution and Automated Reasoning →](L04-06-resolution-and-automated-reasoning.md)
