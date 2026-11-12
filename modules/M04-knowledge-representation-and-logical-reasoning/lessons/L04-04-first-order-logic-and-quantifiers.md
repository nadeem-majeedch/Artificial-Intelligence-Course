# L04-04 — First-Order Logic: Predicates, Terms and Quantifiers

| Module | M04 · Knowledge Representation and Logical Reasoning |
| :--- | :--- |
| Level | 200 |
| Study time | 75 minutes |
| Prerequisites | [L04-03](L04-03-inference-rules-and-equivalence.md) |
| Notebook | [NB-04-02 First-Order Inference and Unification](../notebooks/nb-04-02-first-order-inference-and-unification.ipynb) |
| Lab | LAB-04-02 Advising and Family Knowledge Bases |

[← Previous: L04-03 Inference Rules and Logical Equivalence](L04-03-inference-rules-and-equivalence.md) · [Module home](../README.md) · [Next: L04-05 Unification, Forward Chaining and Backward Chaining →](L04-05-unification-and-chaining.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. Procedure: translating a paragraph](#4-procedure-translating-a-paragraph)
- [5. Worked Examples](#5-worked-examples)
- [6. Complexity](#6-complexity)
- [7. Python Implementation](#7-python-implementation)
- [8. Visual Explanation — the syntax tree](#8-visual-explanation--the-syntax-tree)
- [9. Real-World Application](#9-real-world-application)
- [10. Common Misconceptions](#10-common-misconceptions)
- [11. Exercises](#11-exercises)
- [12. Self-Assessment](#12-self-assessment)
- [13. Key Terms](#13-key-terms)
- [14. Further Reading](#14-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Decompose** an English statement into predicates, terms, variables and quantifiers.
- **Distinguish** terms from formulas, and bound from free variables.
- **Apply** the two translation templates: `∀` with `→`, `∃` with `∧`.
- **Negate** quantified statements correctly using the quantifier De Morgan laws.
- **Explain** why "all students" cannot be expressed in propositional logic without one sentence per student.

## 2. Prerequisite Knowledge

Propositional syntax and semantics, plus the inference rules, from [L04-02](L04-02-propositional-logic.md) and [L04-03](L04-03-inference-rules-and-equivalence.md). You should be comfortable with functions taking arguments, since predicates look like them.

## 3. Conceptual Explanation

### 3.1 The limitation being fixed

Propositional logic has no internal structure. To say "Ann is a parent of Bob" you need a symbol `ann_parent_bob`. For four people you need dozens of symbols; for a university, thousands. Worse, "everyone has a parent" cannot be written at all, because the number of people is open.

**First-order logic (FOL)** fixes this by looking inside the statement:

```text
parent(ann, bob)        predicate + two terms
parent(x, y)            variables instead of names
∀x ∃y parent(y, x)      quantified, one sentence for every person
```

Now a single sentence covers an unbounded domain. That is the entire reason FOL exists.

### 3.2 Syntax, layer by layer

| Layer | What it is | Examples |
| :--- | :--- | :--- |
| **Constant** | a named individual | `ann`, `bob`, `socrates` |
| **Variable** | a placeholder ranging over individuals | `x`, `y`, `z` |
| **Function** | maps individuals to individuals | `mother(x)`, `age(ann)` |
| **Term** | a constant, variable, or function applied to terms | `mother(bob)`, `x` |
| **Predicate** | maps individuals to truth values | `parent(ann, bob)`, `older(x, y)` |
| **Formula** | predicates combined with connectives and quantifiers | `∀x (human(x) → mortal(x))` |

Two distinctions carry most of the marks:

- **Term vs formula.** `mother(bob)` is a *thing* (a person); `parent(bob, cid)` is a *claim*. You cannot write `parent(mother(bob))` — a predicate needs the right number of arguments, and `mother(bob)` is one term, not two.
- **Function vs predicate.** A function returns an individual; a predicate returns a truth value. `age(x)` is a number; `adult(x)` is a claim.

### 3.3 Quantifiers and scope

`∀x φ` means φ holds for every individual; `∃x φ` means it holds for at least one. The **scope** of the quantifier is the formula it governs, and a variable is **bound** inside that scope, **free** outside it.

```text
∀x (human(x) → mortal(x))          x bound throughout
human(x) → mortal(x)               x free: not a sentence, a pattern
∀x parent(x, y)                    x bound, y free
```

Only sentences (no free variables) have truth values. A formula with a free variable is a template waiting for a substitution — which is exactly what [L04-05](L04-05-unification-and-chaining.md) does with it.

### 3.4 The two translation templates

Beginners mirror English word order and get both wrong. Learn the templates:

| English | Correct | Wrong | Why the wrong one fails |
| :--- | :--- | :--- | :--- |
| "All students work hard" | `∀x (student(x) → hardworking(x))` | `∀x (student(x) ∧ hardworking(x))` | says *everything* is a hardworking student |
| "Some students work hard" | `∃x (student(x) ∧ hardworking(x))` | `∃x (student(x) → hardworking(x))` | true if anything is not a student |
| "No student cheats" | `∀x (student(x) → ¬cheats(x))` | `¬∃x (student(x) ∧ cheats(x))` (also correct) | these two are equivalent |
| "Only students may enter" | `∀x (enters(x) → student(x))` | `∀x (student(x) → enters(x))` | converse: "everyone enters" |

The rule of thumb: **`∀` pairs with `→`, `∃` pairs with `∧`**. Every deviation should be deliberate and justified.

### 3.5 Quantifier De Morgan

$$
\neg\forall x\,\phi \equiv \exists x\,\neg\phi
\qquad
\neg\exists x\,\phi \equiv \forall x\,\neg\phi
$$

These let you push negation inward until it touches a predicate, which is the normal form every prover needs. In words: "not everyone passes" is "someone fails", and "nobody passes" is "everyone fails". The engine prints the first equivalence directly:

```text
de morgan:  not forall x human(x) == exists x not human(x)
```

### 3.6 Equality and counting

Equality (`=`) is built into standard FOL and lets you say "at most one", "exactly two":

```text
∃x ∃y (parent(ann, x) ∧ parent(ann, y) ∧ x ≠ y)      ann has at least two children
```

Counting without equality is not expressible, which is why the family KB in LAB-04-02 adds explicit `different` facts: definite clauses have no inequality, so the pairs are enumerated. This is the sort of representational patch you should learn to recognise, because every restricted language forces some.

## 4. Procedure: translating a paragraph

```text
1. Underline the nouns that name individuals -> constants or variables.
2. Underline the verbs/adjectives that make claims -> predicates.
3. Decide the quantifier for each claim: "all/every" -> forall; "some/a" -> exists.
4. Choose connective by the template: forall+->, exists+and.
5. Check arity: every predicate has a fixed number of arguments.
6. Check scope: no accidental free variable; no variable captured by the wrong quantifier.
7. Read the sentence back in English. If it says more than the original, fix it.
```

Step 7 catches most errors, because over-claiming is audible: "all students are hardworking" when you meant "all hardworking people are students" sounds different out loud.

## 5. Worked Examples

### Example 1 — family relations

Domain: people. Facts: `parent(ann, bob)`, `parent(bob, cid)`.

- "Ann is Bob's parent": `parent(ann, bob)`.
- "Everyone has a parent": `∀x ∃y parent(y, x)`.
- "Ann is an ancestor of Cid": derived, not stated — see [L04-05](L04-05-unification-and-chaining.md).
- "Bob is Ann's only child": needs counting and negation; state it as `parent(ann, bob) ∧ ∀x (parent(ann, x) → x = bob)`.

### Example 2 — instantiation, step by step

The universal rule is `∀x (human(x) → mortal(x))`. To use it for Socrates you do **not** substitute inside the scope; you *drop* the quantifier and then substitute:

| Step | Formula | Rule |
| ---: | :--- | :--- |
| 1 | `∀x (human(x) → mortal(x))` | premise |
| 2 | `human(x) → mortal(x)` | universal instantiation (drop `∀`) |
| 3 | `human(socrates) → mortal(x){x↦socrates}` | substitute `x := socrates` |
| 4 | `human(socrates) → mortal(socrates)` | result |

The engine shows the same move:

```text
rule:           forall x (human(x) -> mortal(x))
body:           (human(x) -> mortal(x))
instantiated:   (human(socrates) -> mortal(socrates))
variables:      ['x']
```

Substituting into the *whole quantified formula* changes nothing, because the bound variable is not free there — the earlier attempt to do so printed the rule back unchanged. That is the correct behaviour, and a good check on whether you understand scope.

### Example 3 — a nested quantifier whose order matters

"Everyone loves someone" is not "someone is loved by everyone":

```text
∀x ∃y loves(x, y)      every person loves at least one person
∃y ∀x loves(x, y)      there is one person whom everyone loves
```

The second entails the first; the first does not entail the second. Reading order aloud is the reliable test: "for each person, there is someone" versus "there is someone, for all people".

## 6. Complexity

| Problem | Complexity |
| :--- | :--- |
| Checking a formula in a finite model | polynomial in domain size and formula length |
| Satisfiability of FOL | undecidable (Church–Turing) |
| Entailment in FOL | semi-decidable: a proof is found if one exists, but non-entailment may loop |
| Entailment in Horn clauses (no functions) | polynomial in the number of facts |
| Entailment in description logics (e.g. OWL 2 EL) | polynomial |

The practical moral: full FOL is a specification language, not a runtime. Systems that must answer quickly restrict the language until entailment is decidable — Datalog, Horn clauses, description logics — and accept the expressiveness they lose.

## 7. Python Implementation

```python
from fol_core import (
    Const, Forall, ImpliesF, NotF, Exists, Var, func, pred,
    substitute_formula, unify, variables_in, plain,
)

x, y = Var("x"), Var("y")
human = lambda t: pred("human", t)
mortal = lambda t: pred("mortal", t)
loves = lambda a, b: pred("loves", a, b)

rule = Forall(x, ImpliesF(human(x), mortal(x)))
print("rule:          ", plain(str(rule)))
print("body:          ", plain(str(rule.body)))
print("instantiated:  ", plain(str(substitute_formula(rule.body, {"x": Const("socrates")}))))
print("variables:     ", sorted(variables_in(rule)))
print("exists form:   ", plain(str(Exists(y, loves(Const("ann"), y)))))
print("de morgan:     ", plain(str(NotF(Forall(x, human(x)))), "==",
                               str(Exists(x, NotF(human(x))))))
print("nested unify:  ", unify(func("f", x, Const("c")), func("f", Const("a"), y)))
print("occurs check:  ", unify(x, func("f", x)))
```

**Output**

```text
rule:           forall x (human(x) -> mortal(x))
body:           (human(x) -> mortal(x))
instantiated:   (human(socrates) -> mortal(socrates))
variables:      ['x']
exists form:    exists y loves(ann, y)
de morgan:      not forall x human(x) == exists x not human(x)
nested unify:   {'x': Const(name='a'), 'y': Const(name='c')}
occurs check:   None
```

The last line is the **occurs check**: `x` cannot be unified with `f(x)`, because no finite term equals a term containing itself. Without that check, a prover would build an infinite term and hang — one of the classic implementation traps.

## 8. Visual Explanation — the syntax tree

```text
                 ∀x
                  |
              implies
             /       \
        human(x)     mortal(x)
           |             |
        predicate     predicate
           |             |
        variable      variable
```

*Text description:* quantifier at the root, connective below it, predicates at the leaves with terms as their arguments. Reading a tree is easier than reading a formula: the quantifier's scope is its subtree, and any variable appearing outside its own quantifier's subtree is free. When a formula confuses you, draw this and mark each variable's binder.

## 9. Real-World Application

**SQL and relational queries.** A `SELECT ... WHERE` is a restricted first-order query: rows are individuals, columns are predicates, `WHERE` is a formula. `NOT EXISTS` is a negated existential, and the classic interview question "find students with no failing grade" is exactly `¬∃`.

**Ontologies and the semantic web.** OWL is a description logic: a decidable fragment of FOL designed so that classifiers can answer "is this class satisfiable?" in reasonable time. The restriction to decidable fragments is not academic tidiness — it is what makes an ontology usable at runtime.

**Program specification.** Loop invariants and pre/postconditions are FOL formulas. Tools that verify them (Dafny, Why3) rely on the same semantics and the same restriction: they hand the formula to an SMT solver only after it has been reduced to a decidable theory.

## 10. Common Misconceptions

| Misconception | Correction |
| :--- | :--- |
| "`∀x (student(x) ∧ hardworking(x))` says all students are hardworking." | It says everything in the domain is a hardworking student. Use `→` under `∀`. |
| "Quantifier order does not matter." | `∀x∃y` and `∃y∀x` differ in strength; the second implies the first, never the reverse. |
| "A free variable is a wildcard." | It is an unbound placeholder; the formula is not a sentence and has no truth value until substitution or closure. |
| "First-order logic can express anything." | It cannot express counting without equality, nor second-order claims like "every property that holds of Ann…". |
| "If the prover does not find a proof, the claim is false." | FOL entailment is semi-decidable: failure to find a proof may mean "not entailed" or "not finished". |

## 11. Exercises

1. **Translate.** Domain: people and courses. Write FOL for: (a) every student takes some course; (b) no student takes every course; (c) only students take courses; (d) exactly one student takes CS201 (use equality).
2. **Fix the translation.** A classmate writes `∃x (student(x) → passed(x, cs101))`. Give a world that makes it true when no student passed, and repair it.
3. **Negate.** Negate `∀x (student(x) → ∃y (course(y) ∧ takes(x, y)))` and simplify until negation sits on atomic predicates only.
4. **Scope.** In `∀x (p(x) → ∃x q(x))`, which `x` does `q(x)` refer to? Rename to make the formula unambiguous.
5. **Terms and formulas.** Classify each as term or formula: `mother(bob)`, `parent(bob, cid)`, `age(ann)`, `older(ann, bob)`, `x`.

## 12. Self-Assessment

**1.** Why does `∃x (student(x) → passed(x))` fail as a translation of "some student passed"?
<details><summary>Show answer</summary>

The implication is true for any individual who is not a student, so a world with no students (or one non-student) satisfies it. The existential is then satisfied by a non-student, which is not the intended claim. Use `∃x (student(x) ∧ passed(x))`.

</details>

**2.** Show that `∀x∃y loves(x, y)` does not entail `∃y∀x loves(x, y)` with a two-person countermodel.
<details><summary>Show answer</summary>

Domain `{a, b}` with `loves(a,b)` and `loves(b,a)` true, `loves(a,a)` and `loves(b,b)` false. Every person loves someone, so the first holds; no single person is loved by everyone, so the second fails.

</details>

**3.** What does the occurs check prevent, and what would happen without it?
<details><summary>Show answer</summary>

It prevents binding a variable to a term containing that variable, e.g. `x := f(x)`. Without it, substitution would expand forever (`f(f(f(...)))`), so the unifier would build an infinite term and the prover would not terminate. In finite Herbrand terms no such unifier exists, so rejecting it is correct.

</details>

**4.** Why is full FOL entailment only semi-decidable, and what practical consequence does that have for a rule engine?
<details><summary>Show answer</summary>

Because a proof of entailment can be enumerated (sound and complete calculi exist), but there is no general procedure that always terminates with "not entailed" — FOL satisfiability is undecidable. Practically, an engine may loop on a false query, so production systems restrict the language (Horn clauses, no function symbols) or impose depth/step limits and report "unknown".

</details>

**5.** Translate "every course has a prerequisite that is not itself" and explain why it needs inequality.
<details><summary>Show answer</summary>

`∀c (course(c) → ∃p (prereq(c, p) ∧ p ≠ c))`. Without `≠`, the formula is satisfied by any course that is its own prerequisite, which is the opposite of the intended constraint. With only positive Horn clauses, you approximate `≠` by listing the distinct pairs, as the family KB does.

</details>

## 13. Key Terms

- **Predicate** — a relation over individuals, returning true or false.
- **Term** — an expression denoting an individual: constant, variable or function application.
- **Quantifier** — `∀` (all) or `∃` (some).
- **Bound / free variable** — inside / outside the scope of its quantifier.
- **Sentence** — a formula with no free variables.
- **Universal instantiation** — dropping `∀` and substituting a term.
- **Occurs check** — rejecting `x := f(x)` during unification.

## 14. Further Reading

- Russell & Norvig (2021), *AIMA* 4th ed., Chapter 8. — Syntax, semantics and quantifier nesting, with the same templates.
- Enderton (2001), *A Mathematical Introduction to Logic*, Chapter 2. — The model theory behind entailment in FOL.
- Baader et al. (2017), *The Description Logic Handbook*, Chapter 2. — What FOL looks like when restricted until it is decidable.

## What to Do Next

Continue to [L04-05 — Unification and Chaining](L04-05-unification-and-chaining.md), where quantified rules meet facts and the engine starts producing new sentences without being told them.

---

**Navigation:** [← Previous: L04-03 Inference Rules and Logical Equivalence](L04-03-inference-rules-and-equivalence.md) · [Module home](../README.md) · [Next: L04-05 Unification, Forward Chaining and Backward Chaining →](L04-05-unification-and-chaining.md)
