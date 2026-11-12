# L04-03 — Inference Rules and Logical Equivalence

| Module | M04 · Knowledge Representation and Logical Reasoning |
| :--- | :--- |
| Level | 200 |
| Study time | 75 minutes |
| Prerequisites | [L04-02](L04-02-propositional-logic.md) |
| Notebook | [NB-04-01 Propositional Logic Workbench](../notebooks/nb-04-01-propositional-logic-workbench.ipynb) |
| Lab | LAB-04-01 Diagnostic Rule Engine |

[← Previous: L04-02 Propositional Logic: Syntax, Operators and Truth Tables](L04-02-propositional-logic.md) · [Module home](../README.md) · [Next: L04-04 First-Order Logic: Predicates, Terms and Quantifiers →](L04-04-first-order-logic-and-quantifiers.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. Procedure: writing a derivation](#4-procedure-writing-a-derivation)
- [5. Worked Example — a four-line proof](#5-worked-example--a-four-line-proof)
- [6. Complexity](#6-complexity)
- [7. Python Implementation — a proof engine with justifications](#7-python-implementation--a-proof-engine-with-justifications)
- [8. Visual Explanation — forward versus backward](#8-visual-explanation--forward-versus-backward)
- [9. Real-World Application](#9-real-world-application)
- [10. Common Misconceptions](#10-common-misconceptions)
- [11. Exercises](#11-exercises)
- [12. Self-Assessment](#12-self-assessment)
- [13. Key Terms](#13-key-terms)
- [14. Further Reading](#14-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Name and apply** the standard inference rules, and say what each one licenses.
- **Rewrite** a formula using the equivalence laws, one step at a time, with the law named.
- **Prove** a short entailment by a numbered derivation, citing a rule at each line.
- **Distinguish** an equivalence from an inference: `↔` versus `⊨`.
- **Recognise** the two classic fallacies (affirming the consequent, denying the antecedent) in an argument someone presents as valid.

## 2. Prerequisite Knowledge

Truth tables and the five operators from [L04-02](L04-02-propositional-logic.md). You should be able to check any candidate law by table before trusting it — that habit is the whole of §5.

## 3. Conceptual Explanation

### 3.1 Two different jobs

Students conflate these constantly, so separate them at the start.

- An **equivalence** says two formulas have the same truth value in every world: `¬(p ∧ q) ≡ ¬p ∨ ¬q`. You may *replace* one with the other anywhere inside a larger formula.
- An **inference rule** says: from formulas of this shape, you may *add* a formula of that shape. Modus ponens takes `p` and `p → q` and adds `q`.

Equivalence is a statement *about* formulas; inference is an action *on* a set of formulas. A proof is a sequence of actions, each justified by a rule.

### 3.2 The equivalence laws you will use

| Law | Form |
| :--- | :--- |
| Commutativity | `p ∧ q ≡ q ∧ p`, `p ∨ q ≡ q ∨ p` |
| Associativity | `(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)` |
| Distribution | `p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)`; dually for `∨` over `∧` |
| De Morgan | `¬(p ∧ q) ≡ ¬p ∨ ¬q`; `¬(p ∨ q) ≡ ¬p ∧ ¬q` |
| Double negation | `¬¬p ≡ p` |
| Contraposition | `p → q ≡ ¬q → ¬p` |
| Implication elimination | `p → q ≡ ¬p ∨ q` |
| Absorption | `p ∨ (p ∧ q) ≡ p` |
| Exportation | `(p ∧ q) → r ≡ p → (q → r)` |
| Distribution of implication | `p → (q ∧ r) ≡ (p → q) ∧ (p → r)` |

Every row is checkable by truth table, and the module's engine does exactly that:

```text
commutativity (and)          True
commutativity (or)           True
associativity (and)          True
distribution (and over or)   True
De Morgan (and)              True
De Morgan (or)               True
double negation              True
contraposition               True
implication elimination      True
absorption                   True
exportation                  True
distribution of implies      True
not a law: False
```

The last line is the converse `q → p` for `p → q`. It is *not* a law, which is why "the ground is wet, so it rained" is invalid reasoning.

### 3.3 The inference rules

| Rule | From | Infer | Nickname |
| :--- | :--- | :--- | :--- |
| Modus ponens | `p`, `p → q` | `q` | affirming the antecedent |
| Modus tollens | `¬q`, `p → q` | `¬p` | denying the consequent |
| Hypothetical syllogism | `p → q`, `q → r` | `p → r` | chaining |
| And-elimination | `p ∧ q` | `p` (or `q`) | simplification |
| And-introduction | `p`, `q` | `p ∧ q` | conjunction |
| Or-introduction | `p` | `p ∨ q` | addition |
| Disjunctive syllogism | `p ∨ q`, `¬p` | `q` | unit resolution |
| Resolution | `p ∨ q`, `¬p ∨ r` | `q ∨ r` | the workhorse |
| Constructive dilemma | `p → q`, `r → s`, `p ∨ r` | `q ∨ s` | case analysis |

Each rule is **sound**: if the premises are true in a world, the conclusion is true in that same world. You can verify any of them by checking that `premises → conclusion` is a tautology.

### 3.4 Sound is not the same as equivalent

Here is the trap, verified by the engine:

```text
resolution as an equivalence: False
resolution as an inference:   True
```

`(p ∨ q) ∧ (¬p ∨ r)` does **not** have the same truth value as `q ∨ r`: when `p` is false and `q` is false, the premise is false and the resolvent is true. But every model of the premise is a model of the resolvent, so the *inference* is valid. An inference may throw information away; an equivalence may not.

This is why resolution proofs are refutations. You cannot replace the KB by its resolvents and keep meaning; you can only add consequences and look for a contradiction.

### 3.5 Proofs as search

A derivation is a search problem in the M03 sense: states are sets of formulas, actions are rule applications, the goal is the query. The branching factor is the number of rules times the number of matching formula pairs, which is why naive proof search explodes and why [L04-06](L04-06-resolution-and-automated-reasoning.md) imposes a normal form.

Two control strategies:

- **Forward chaining** — start from facts, apply rules, stop when the goal appears. Data-driven; good when there are few facts and many possible queries.
- **Backward chaining** — start from the goal, find rules that conclude it, recurse on their premises. Goal-driven; good when there are many facts and one query.

Both are sound. Neither is complete without loop checking on cyclic rules.

## 4. Procedure: writing a derivation

```text
1. Number every premise.
2. State the goal.
3. At each step, write the new formula, the lines it came from, and the rule name.
4. Never apply a rule to a formula that is not on an earlier line.
5. Stop when the goal appears; the derivation is the proof.
```

Marks are lost for unlabelled steps. A derivation that reaches the right answer by an unnamed transformation is not a proof; it is a claim.

## 5. Worked Example — a four-line proof

Premises:

1. `rain → wet`
2. `wet → slippery`
3. `rain`

Goal: `slippery`.

| Line | Formula | Justification |
| ---: | :--- | :--- |
| 1 | `rain → wet` | premise |
| 2 | `wet → slippery` | premise |
| 3 | `rain` | premise |
| 4 | `wet` | modus ponens, 1 and 3 |
| 5 | `slippery` | modus ponens, 2 and 4 |

Five lines, two rule applications. Now the same KB with `¬slippery` added and the goal `¬rain`:

| Line | Formula | Justification |
| ---: | :--- | :--- |
| 1 | `rain → wet` | premise |
| 2 | `wet → slippery` | premise |
| 3 | `¬slippery` | premise |
| 4 | `¬wet` | modus tollens, 2 and 3 |
| 5 | `¬rain` | modus tollens, 1 and 4 |

Same two rules, opposite direction. Modus tollens is not a new law of logic; it is contraposition plus modus ponens, which is worth showing once:

`p → q ≡ ¬q → ¬p` (contraposition), then `¬q` and `¬q → ¬p` give `¬p` by modus ponens.

### The fallacies, for contrast

| Argument | Form | Why it fails |
| :--- | :--- | :--- |
| "If it rained, the ground is wet. The ground is wet. So it rained." | `p → q`, `q` ⊢ `p` | sprinklers exist; the converse is not entailed |
| "If it rained, the ground is wet. It did not rain. So the ground is dry." | `p → q`, `¬p` ⊢ `¬q` | the rule says nothing about no-rain worlds |

Both are common in bad rule bases: a rule is written for one direction and then queried in the other.

## 6. Complexity

| Task | Cost |
| :--- | :--- |
| Check one rule application | $O(\lvert\phi\rvert)$ matching |
| Forward chain to fixpoint, $n$ atoms, $m$ rules | $O(n \cdot m)$ rule firings in the worst case |
| Backward chain, depth $d$, branching $b$ | $O(b^d)$ without memoisation |
| Propositional proof search in general | co-NP-complete |

The last row is the honest headline: deciding entailment is as hard as deciding unsatisfiability, so every practical prover trades completeness or generality for speed.

## 7. Python Implementation — a proof engine with justifications

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    premises: tuple[str, ...]
    conclusion: str
    name: str


def forward_chain(facts: set[str], rules: list[Rule]) -> list[tuple[str, str]]:
    """Return (fact, justification) pairs in the order they were derived."""
    known = set(facts)
    proof: list[tuple[str, str]] = [(f, "premise") for f in sorted(facts)]
    changed = True
    while changed:
        changed = False
        for rule in rules:
            if all(p in known for p in rule.premises) and rule.conclusion not in known:
                known.add(rule.conclusion)
                proof.append((rule.conclusion, f"{rule.name} from {', '.join(rule.premises)}"))
                changed = True
    return proof


rules = [
    Rule(("rain", "rain -> wet"), "wet", "modus ponens"),
    Rule(("wet", "wet -> slippery"), "slippery", "modus ponens"),
]
for fact, why in forward_chain({"rain", "rain -> wet", "wet -> slippery"}, rules):
    print(f"{fact:12s} <- {why}")
```

**Output**

```text
rain         <- premise
rain -> wet  <- premise
wet          <- modus ponens from rain, rain -> wet
wet -> slippery <- premise
slippery     <- modus ponens from wet, wet -> slippery
```

The facts are strings beginning with `->` because the engine is deliberately simple: it matches symbols, not structure. [L04-04](L04-04-first-order-logic-and-quantifiers.md) replaces strings with terms and predicates, and [L04-05](L04-05-unification-and-chaining.md) replaces exact matching with unification.

## 8. Visual Explanation — forward versus backward

```text
forward:  facts ──▶ rules ──▶ rules ──▶ ... ──▶ goal?
           rain      wet      slippery            yes

backward: goal ◀── which rules conclude it? ◀── premises ◀── facts
          slippery    wet → slippery           wet      rain
```

*Text description:* forward chaining fans out from what is known; backward chaining narrows from what is asked. Draw both for the same KB and count the formulas touched. With three premises the difference is invisible; with three thousand, it decides whether the query returns at all.

## 9. Real-World Application

**Business rule engines** (insurance underwriting, loan eligibility, fraud triage) are forward-chaining engines over propositional or simple first-order rules, and every derived decision carries the rule names that produced it. That justification trail is not a nice-to-have: in regulated domains the explanation *is* the deliverable, and a model that cannot produce one cannot be deployed, however accurate.

**Hardware verification** uses the same rules in a different notation: equivalence checking between two circuit descriptions is a sequence of Boolean rewrites, each one a law from the table in §3.2.

## 10. Common Misconceptions

| Misconception | Correction |
| :--- | :--- |
| "Modus tollens is the same as denying the antecedent." | Tollens denies the *consequent* and concludes `¬p`; denying the antecedent concludes `¬q` and is invalid. |
| "If the premises entail the conclusion, they are equivalent." | Entailment is one-directional; equivalence needs both directions. |
| "`↔` is just a strong `→`." | It is a conjunction of two implications; `p ↔ q` entails both `p → q` and `q → p`. |
| "A longer proof is a better proof." | A proof is judged by validity and clarity, not length. Short proofs are easier to audit. |
| "Forward and backward chaining give different answers." | On a definite-clause KB they compute the same closure; they differ in cost, not in result. |

## 11. Exercises

1. **Name the rule.** For each: (a) from `p ∧ q` infer `q`; (b) from `p` infer `p ∨ r`; (c) from `p → q` and `¬q` infer `¬p`; (d) from `p ∨ q` and `¬p` infer `q`.
2. **Prove it.** Give a derivation of `¬r` from `{p → q, q → r, ¬r → ¬q, p}` or explain why none exists.
3. **Break a fallacy.** Write the truth table showing `{p → q, q} ⊭ p`, and identify the row that is a countermodel.
4. **Rewrite.** Simplify `¬(p ∧ ¬q) ∨ (p ∧ q)` using the laws, naming each step.
5. **Count the work.** For 10 atoms and 20 binary rules, estimate how many rule-premise pairs a forward chain must check per iteration.

## 12. Self-Assessment

**1.** Why is resolution sound but not an equivalence?
<details><summary>Show answer</summary>

Every model of `p ∨ q` and `¬p ∨ r` satisfies `q ∨ r` — if `p` is true then `r` must hold, and if `p` is false then `q` must hold. So the inference preserves truth. But the premise can be false while the resolvent is true (`p=F, q=F`), so the two formulas are not equivalent and one cannot be substituted for the other.

</details>

**2.** State modus tollens and derive it from modus ponens in two steps.
<details><summary>Show answer</summary>

From `p → q` and `¬q`, infer `¬p`. Derivation: contraposition gives `¬q → ¬p`; with `¬q`, modus ponens gives `¬p`.

</details>

**3.** A rule base contains "if the alarm is armed and the door opens, then notify". A user asks: "the door opened and there was no notification — was the alarm armed?" Which rule answers, and what does the answer rely on?
<details><summary>Show answer</summary>

Modus tollens on `(armed ∧ opened) → notify` with `¬notify` gives `¬(armed ∧ opened)`, i.e. `¬armed ∨ ¬opened`. With `opened` true, disjunctive syllogism yields `¬armed`. The answer relies on the rule being the *only* cause of notification — a closed-world assumption, not a logical one.

</details>

**4.** Why does backward chaining suit a query-heavy, fact-heavy system?
<details><summary>Show answer</summary>

It touches only the rules that can conclude the goal and their supporting premises, ignoring unrelated facts. Forward chaining would derive the entire closure, most of which no query needs. With many facts and few queries per session, backward chaining's focused search wins.

</details>

**5.** Give a KB where forward chaining terminates but naive backward chaining does not, and say how to fix it.
<details><summary>Show answer</summary>

`p → q` and `q → p` with goal `p`: backward chaining recurses `p → q → p → …` forever. Forward chaining reaches a fixpoint because no new atoms appear. Fixes: a depth limit, a set of (goal, depth) pairs already explored, or tabling/memoisation as in Datalog.

</details>

## 13. Key Terms

- **Inference rule** — a licensed step from premises to conclusion.
- **Equivalence law** — a schema whose two sides have identical truth values.
- **Derivation / proof** — a numbered sequence of licensed steps.
- **Modus ponens / modus tollens** — affirming the antecedent / denying the consequent.
- **Resolution** — from `p ∨ q` and `¬p ∨ r` infer `q ∨ r`.
- **Forward / backward chaining** — data-driven / goal-driven rule application.

## 14. Further Reading

- Russell & Norvig (2021), *AIMA* 4th ed., §7.5. — Inference rules and equivalence, with the same tables.
- Prawitz, D. (2006). *Natural Deduction: A Proof-Theoretical Study*. — Where these rules come from and why they are the ones chosen.
- Forgy, C. (1982). "Rete: A Fast Algorithm for the Many Pattern/Many Object Pattern Match Problem." *Artificial Intelligence* 19(1). — How forward-chaining engines match thousands of rules quickly.

## What to Do Next

Run the derivation in §7 yourself, then continue to [L04-04 — First-Order Logic and Quantifiers](L04-04-first-order-logic-and-quantifiers.md), where symbols acquire arguments and rules acquire variables.

---

**Navigation:** [← Previous: L04-02 Propositional Logic: Syntax, Operators and Truth Tables](L04-02-propositional-logic.md) · [Module home](../README.md) · [Next: L04-04 First-Order Logic: Predicates, Terms and Quantifiers →](L04-04-first-order-logic-and-quantifiers.md)
