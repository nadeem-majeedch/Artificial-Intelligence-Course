# L04-02 — Propositional Logic: Syntax, Operators and Truth Tables

| Module | M04 · Knowledge Representation and Logical Reasoning |
| :--- | :--- |
| Level | 200 |
| Study time | 75 minutes |
| Prerequisites | [L04-01](L04-01-knowledge-representation-fundamentals.md) |
| Notebook | [NB-04-01 Propositional Logic Workbench](../notebooks/nb-04-01-propositional-logic-workbench.ipynb) |
| Lab | LAB-04-01 Diagnostic Rule Engine |

[← Previous: L04-01 Knowledge Representation and Knowledge-Based Systems](L04-01-knowledge-representation-fundamentals.md) · [Module home](../README.md) · [Next: L04-03 Inference Rules and Logical Equivalence →](L04-03-inference-rules-and-equivalence.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. Procedure: building and reading a truth table](#4-procedure-building-and-reading-a-truth-table)
- [5. Worked Examples](#5-worked-examples)
- [6. Complexity](#6-complexity)
- [7. Python Implementation](#7-python-implementation)
- [8. Visual Explanation — the implication lattice](#8-visual-explanation--the-implication-lattice)
- [9. Real-World Application](#9-real-world-application)
- [10. Common Misconceptions](#10-common-misconceptions)
- [11. Exercises](#11-exercises)
- [12. Self-Assessment](#12-self-assessment)
- [13. Key Terms](#13-key-terms)
- [14. Further Reading](#14-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Write** a propositional sentence for a stated fact pattern, using the five operators correctly.
- **Build** a truth table from a formula and read off its models.
- **Explain** why `p → q` is true when `p` is false, without hand-waving.
- **Convert** an English conditional into a formula and say what the formula does *not* claim.
- **Read** a formula's models as the set of worlds it allows.

## 2. Prerequisite Knowledge

You need the KR vocabulary from [L04-01](L04-01-knowledge-representation-fundamentals.md), specifically *syntax*, *semantics* and *model*. You also need to be comfortable with Python booleans and `and`/`or`/`not`.

## 3. Conceptual Explanation

### 3.1 The idea in one paragraph

Propositional logic is the logic of whole statements. Each **atomic proposition** — `rain`, `wet`, `indoors` — is either true or false in a given world, and nothing else. Compound sentences are built with five operators. A sentence's **meaning** is the set of worlds in which it is true; a truth table simply lists them. That is the entire theory, and it is enough to build a working inference engine, as you will see in [L04-03](L04-03-inference-rules-and-equivalence.md) and [L04-06](L04-06-resolution-and-automated-reasoning.md).

### 3.2 Syntax

A formula is either:

- an atom — a lowercase symbol such as `rain`;
- `¬φ` (negation);
- `(φ ∧ ψ)` (conjunction), `(φ ∨ ψ)` (disjunction);
- `(φ → ψ)` (implication), `(φ ↔ ψ)` (biconditional).

Precedence, when parentheses are omitted: `¬` binds tightest, then `∧`, then `∨`, then `→`, then `↔`. Write the parentheses anyway. Almost every error in student proofs is a precedence error, and no marker will give you the benefit of the doubt.

### 3.3 Semantics: the five operators

| `p` | `q` | `¬p` | `p ∧ q` | `p ∨ q` | `p → q` | `p ↔ q` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| F | F | T | F | F | **T** | T |
| F | T | T | F | T | **T** | F |
| T | F | F | F | T | **F** | F |
| T | T | F | T | T | T | T |

Two rows deserve attention.

**Implication is not causation.** `p → q` means "it is not the case that `p` is true and `q` is false". When `p` is false, the implication is true regardless of `q`. This is called *vacuous truth* and it is not a quirk to memorise away: it is what makes "all unicorns are pink" true in a world with no unicorns, which is exactly what a universal claim in [L04-04](L04-04-first-order-logic-and-quantifiers.md) needs.

**Inclusive or.** `∨` allows both. English "or" sometimes means exclusive-or; logic does not. If you need exclusive-or, write `(p ∨ q) ∧ ¬(p ∧ q)`.

### 3.4 Models, validity, satisfiability

A **model** of a formula is an assignment of truth values to its atoms that makes it true. Three properties follow:

- **Valid** (tautology): true in *every* model. Example: `p ∨ ¬p`.
- **Satisfiable**: true in *at least one* model. Example: `p ∧ q`.
- **Unsatisfiable** (contradiction): true in no model. Example: `p ∧ ¬p`.

The connection to reasoning: a set of sentences $KB$ entails $\alpha$ exactly when $KB \wedge \neg\alpha$ is unsatisfiable. That single equivalence is the engine behind resolution, and it is the reason [L04-06](L04-06-resolution-and-automated-reasoning.md) spends its effort on proving contradictions.

### 3.5 Translating English honestly

| English | Formula | What it does **not** say |
| :--- | :--- | :--- |
| "If it rains, the ground is wet" | `rain → wet` | that rain caused it, or that wet implies rain |
| "It rains only if the ground is wet" | `rain → wet` | that rain happens |
| "It rains if the ground is wet" | `wet → rain` | that rain happens |
| "The ground is wet if and only if it rained" | `wet ↔ rain` | that either happened |
| "Either the alarm rings or the door opens" | `alarm ∨ door` | that both cannot happen |

"Only if" is the trap. `p only if q` is `p → q`, not `q → p`. Test it with the contrapositive: `p → q` says "no `p` without `q`", which is what "only if" means in English.

## 4. Procedure: building and reading a truth table

```text
1. List the atoms in alphabetical order: a, b, c, ...
2. There are 2^n rows; enumerate every combination (standard order: F...F first).
3. Evaluate innermost parentheses outward, one column per subformula.
4. Mark the rows where the whole formula is true: these are its models.
5. Classify: all rows true -> valid; some row true -> satisfiable; no row true -> contradiction.
```

Step 3 is where marks are lost. Write one column per subformula and never evaluate two operators in your head at once.

## 5. Worked Examples

### Example 1 — a full truth table for `(rain → wet) → indoors`

The code in §7 produces, for the simpler formula `rain → wet`:

```text
rain | wet | (rain -> wet)
F | F | T
F | T | T
T | F | F
T | T | T
```

Read the three `T` rows as the models: everything except the world where it rains and nothing gets wet. One row is enough to falsify an implication, which is why implications are cheap to test and expensive to trust.

### Example 2 — step by step, `(p → q) ∧ (q → r)`

Atoms `p`, `q`, `r`: eight rows.

| `p` | `q` | `r` | `p→q` | `q→r` | conjunction |
| :---: | :---: | :---: | :---: | :---: | :---: |
| F | F | F | T | T | T |
| F | F | T | T | T | T |
| F | T | F | T | F | F |
| F | T | T | T | T | T |
| T | F | F | F | T | F |
| T | F | T | F | T | F |
| T | T | F | T | F | F |
| T | T | T | T | T | T |

Four models out of eight. The formula is satisfiable but not valid — a chain of implications is not a tautology, because the chain can start with `p` true and end with `r` false.

### Example 3 — a sentence whose meaning is easy to get wrong

"Students who pass both labs may take the exam" over two students:

```text
(pass_lab1_ali ∧ pass_lab2_ali → may_sit_ali) ∧ (pass_lab1_bea ∧ pass_lab2_bea → may_sit_bea)
```

Now ask: what does the formula say about a student who failed a lab? Nothing — the conjunction is vacuously true for them. A rule base that treats "not eligible" as "forbidden" is adding the closed-world assumption; the logic itself is silent. [L04-07](L04-07-rule-based-and-expert-systems.md) returns to this, because it is the single most common source of unfair automated decisions.

## 6. Complexity

| Task | Cost | Note |
| :--- | :--- | :--- |
| Truth table for $n$ atoms | $2^n$ rows, $O(2^n \cdot \lvert\phi\rvert)$ time | $n{=}20$: 1,048,576 rows |
| Validity check | same | must inspect every row |
| Satisfiability | same by enumeration | the general problem is NP-complete |
| Checking one model | $O(\lvert\phi\rvert)$ | cheap: this is why testing is easy |

The asymmetry matters: verifying a claimed model is linear, finding one may be exponential. Every practical SAT-based tool lives off that gap.

## 7. Python Implementation

```python
from itertools import product


def evaluate(formula: str, assignment: dict[str, bool]) -> bool:
    """Evaluate a formula written with Python operators: and, or, not, <=, ==."""
    return bool(eval(formula, {"__builtins__": {}}, dict(assignment)))


def truth_table(atoms: list[str], formula: str) -> None:
    print(" | ".join(atoms + [formula]))
    for values in product([False, True], repeat=len(atoms)):
        assignment = dict(zip(atoms, values))
        row = ["T" if v else "F" for v in values]
        row.append("T" if evaluate(formula, assignment) else "F")
        print(" | ".join(row))


truth_table(["rain", "wet"], "rain and not wet")   # the only falsifying world
truth_table(["p", "q", "r"], "(p <= q) and (q <= r) and p and not r")
```

**Output**

```text
rain | wet | rain and not wet
F | F | F
F | T | F
T | F | T
T | T | F
p | q | r | (p <= q) and (q <= r) and p and not r
F | F | F | F
F | F | T | F
F | T | F | F
F | T | T | F
T | F | F | F
T | F | T | F
T | T | F | F
T | T | T | F
```

`<=` is Python's implication for booleans (`p <= q` is `not p or q`), and `==` is the biconditional. The second formula is unsatisfiable, which is why every row is `F`: it asks for a chain `p → q → r` while also asserting `p` and `¬r`. Spotting that from the table, rather than from the formula, is the skill the table is for. Using `eval` is acceptable in a teaching notebook with a restricted namespace; never do it on untrusted input, because it is arbitrary code execution.

The serious implementation — an AST, CNF conversion and resolution — is [`code/prop_logic.py`](../code/prop_logic.py). Its self-check prints:

```text
== CNF ==
cnf of (rain -> wet) -> indoors: ((rain or indoors) and (not wet or indoors))
clauses: ['indoors or rain', 'indoors or not wet']
```

That conversion is what [L04-06](L04-06-resolution-and-automated-reasoning.md) consumes.

## 8. Visual Explanation — the implication lattice

```text
        p -> q  is FALSE only here
        +-------------------+
   q=T  | T            T    |
        |                   |
   q=F  | T            F    |  <- p=T, q=F
        +-------------------+
          p=F          p=T
```

*Text description:* a 2×2 grid of worlds. The implication `p → q` excludes exactly the bottom-right corner: `p` true and `q` false. Everything else is allowed. When students say "if it rains the ground is wet, and it did not rain, so I cannot tell whether the ground is wet" — the grid agrees, and marks both no-rain rows as consistent with the rule.

## 9. Real-World Application

**Configuration and access control.** "If a user has role `editor` and the document is `locked`, then `write` is denied" is a propositional rule over flags. Systems with tens of such rules are checked for contradictions by SAT solvers before deployment: if `deny ∧ allow` is satisfiable for the same request, two rules can fire at once, and the deploy is blocked. The truth table is the concept; the SAT solver is the production tool.

**Circuit design.** Gates are propositional connectives, and equivalence checking of two circuits is a validity check. Your laptop's processor was verified this way.

## 10. Common Misconceptions

| Misconception | Correction |
| :--- | :--- |
| "`p → q` means `p` causes `q`." | It is a truth-functional constraint, nothing more. Causation needs a stronger language. |
| "If `p` is false, the implication is neither true nor false." | Classical logic is two-valued: it is true. |
| "`p → q` and `q → p` are the same rule." | They are converses. Confusing them is the most common modelling error in rule bases. |
| "`p ∨ q` excludes both being true." | That is exclusive-or; write it explicitly if you need it. |
| "A formula with no false rows is uninformative." | Tautologies are the theorems of the logic; `p ∨ ¬p` is what makes case analysis valid. |

## 11. Exercises

1. **Fill the table.** Construct the truth table for `(p → q) ∨ (q → p)` and classify it. What does the result tell you about implication in general?
2. **Translate.** Write formulas for: (a) "the alarm sounds only if the door is open"; (b) "the door is open but the alarm is silent"; (c) "either the alarm sounds or the door is closed, but not both".
3. **Count models.** How many of the eight rows satisfy `(p → q) ∧ (q → r)`? Confirm with code.
4. **Exclusive or.** Express `p ⊕ q` using only `¬`, `∧`, `∨`, and verify by truth table that your expression matches the intended meaning.
5. **Spot the error.** A classmate writes `rain → wet` for "the ground is wet whenever it rains, and it is raining". What is missing, and what formula do they actually need?

## 12. Self-Assessment

**1.** Why is `p → q` true when `p` is false? Give the semantic argument, not a rule to memorise.
<details><summary>Show answer</summary>

`p → q` asserts that there is no world in which `p` holds and `q` fails. If `p` is false, that situation cannot arise, so the assertion is not violated and the sentence is true in that world. Semantically, the implication's model set is everything except `{p=T, q=F}`.

</details>

**2.** A formula has 5 atoms. How many rows does its truth table have, and how many models does it have if it is a tautology?
<details><summary>Show answer</summary>

$2^5 = 32$ rows. A tautology is true in every model, so all 32 rows are models. By contrast, a contradiction has zero models and a contingent formula has between 1 and 31.

</details>

**3.** Translate "you may graduate only if you pass the capstone" and its converse. Which one is the actual rule?
<details><summary>Show answer</summary>

Rule: `graduate → pass_capstone` (no graduation without the capstone). Converse: `pass_capstone → graduate`, which claims that passing guarantees graduation — false if there are other requirements. The word "only if" always produces the first form.

</details>

**4.** Why does entailment reduce to unsatisfiability of `KB ∧ ¬α`?
<details><summary>Show answer</summary>

$KB \models \alpha$ means every model of $KB$ satisfies $\alpha$. If some model satisfied $KB$ but not $\alpha$, it would satisfy $KB \wedge \neg\alpha$. So no model of $KB \wedge \neg\alpha$ exists exactly when the entailment holds. This lets a refutation procedure prove positive results by deriving a contradiction.

</details>

**5.** Give a formula that is satisfiable but not valid, and one that is valid but not a tautology in the strict sense of having no atoms.
<details><summary>Show answer</summary>

Satisfiable not valid: `p ∧ q` (true in one row, false in three). Valid: `p ∨ ¬p`. The phrase "valid but not a tautology" is a trick — in propositional logic validity *is* tautologyhood, since a formula is valid iff true under all assignments. (In first-order logic the two come apart, which is why the distinction is taught there.)

</details>

## 13. Key Terms

- **Atomic proposition** — an indivisible statement symbol.
- **Connective** — an operator that builds compound formulas.
- **Model** — an assignment making a formula true.
- **Tautology / validity** — true under every assignment.
- **Satisfiable / unsatisfiable** — has at least one model / has none.
- **Vacuous truth** — an implication true because its antecedent is false.
- **Converse** — `q → p` for `p → q`.

## 14. Further Reading

- Russell & Norvig (2021), *AIMA* 4th ed., §7.4–7.5. — Truth tables and entailment, with the same terminology.
- Enderton, H. (2001). *A Mathematical Introduction to Logic*, 2nd ed., Chapter 1. — The precise semantics, for readers who want the formal version.
- Biere, A. et al. (2021). *Handbook of Satisfiability*, 2nd ed., Chapter 1. — Where truth tables end and SAT solving begins.

## What to Do Next

Work through [NB-04-01](../notebooks/nb-04-01-propositional-logic-workbench.ipynb) until you can predict a table before running it, then continue to [L04-03 — Inference Rules and Logical Equivalence](L04-03-inference-rules-and-equivalence.md).

---

**Navigation:** [← Previous: L04-01 Knowledge Representation and Knowledge-Based Systems](L04-01-knowledge-representation-fundamentals.md) · [Module home](../README.md) · [Next: L04-03 Inference Rules and Logical Equivalence →](L04-03-inference-rules-and-equivalence.md)
