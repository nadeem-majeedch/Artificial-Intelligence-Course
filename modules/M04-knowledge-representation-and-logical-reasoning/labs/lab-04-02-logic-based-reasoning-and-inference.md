# LAB-04-02 — Logic-Based Reasoning and Inference

| | |
| :--- | :--- |
| Module | M04 · Knowledge Representation and Logical Reasoning |
| Level | 200 |
| Time | 2.5 hours |
| Prerequisites | [L04-04](../lessons/L04-04-first-order-logic-and-quantifiers.md), [L04-05](../lessons/L04-05-unification-and-chaining.md) |
| Code | `code/expert_system.py` |

[← LAB-04-01](lab-04-01-rule-based-expert-system.md) · [Next lab: LAB-04-03 →](lab-04-03-bayesian-and-knowledge-based-decision-support.md)

## 1. Learning objectives

- **Represent** relationships as ground facts and rules with variables.
- **Unify** a rule head with a query and instantiate the premises correctly.
- **Run** forward and backward chaining on a recursive rule and explain why recursion terminates.
- **Distinguish** what first-order logic can prove from what it cannot.
- **Diagnose** an over-general rule by reading the derived facts.

## 2. Scenario

A genealogy teaching dataset encodes five generations of a fictional family. Students ask questions such as
"is Ali an ancestor of Ayesha?", "who are Zain's aunts?" and "is siblinghood symmetric in this encoding?".
The dataset is deliberately small so every proof can be checked by hand.

All names are fictional. No real personal data is used.

## 3. Problem statement

1. load `family_kb()` and list its facts and rules;
2. run forward chaining and print the derived relations;
3. query ancestor, sibling, aunt/uncle and relative;
4. prove `ancestor(ali, ayesha)` backward and print the proof tree;
5. add a rule that is wrong (for example, sibling without the `different` condition) and describe the damage;
6. explain why `ancestor` needs a depth guard and what would happen without it.

## 4. Background concepts

- Ground facts versus rules with variables; `?x` is a variable, everything else a constant.
- Unification binds variables so a pattern matches a fact; failure is a `None`, not an exception.
- Forward chaining closes over the rule set; backward chaining proves one goal and returns a tree.
- Recursion plus symmetry produces cycles: termination needs a visited set or a depth bound.
- Logic proves truth, not likelihood: it cannot say "probably an ancestor".

## 5. Dataset information and licensing

The family graph is synthetic and course-authored (`family_kb()`), with five parent facts and a
`different` relation. No third-party genealogy data is used; the synthetic graph is dedicated to the
public domain under CC0 1.0 and the lab text is CC BY 4.0. Names are placeholders.

## 6. Software requirements

Python 3.10+ and `code/expert_system.py`. No packages, no network.

## 7. Step-by-step tasks

1. Print the facts and rules; draw the family tree on paper.
2. Forward-chain and list every derived `ancestor`, `sibling`, `uncle_or_aunt` and `relative` fact.
3. Verify by hand that `uncle_or_aunt(sara, omar)` follows from `parent(hina, omar)` and
   `sibling(sara, hina)` — and that the rule's variable order matters.
4. Backward-chain `ancestor(ali, ayesha)` and print the proof; count the recursion depth.
5. Remove `different(?x, ?y)` from rule F3 and re-run. How many spurious siblings appear?
6. Add a rule `ancestor(?x, ?x)` and explain why the depth guard is now load-bearing.
7. Write four sentences on the difference between what this lab computes and what a probabilistic model
   (LAB-04-03) computes.

## 8. Starter code

```python
import expert_system as es

kb = es.family_kb()
kb.forward_chain()

for fact in sorted(kb.facts):
    if fact[0] in ("ancestor", "sibling", "uncle_or_aunt"):
        print(es.fmt(fact))

print()
print(es.proof_text(kb.backward_chain(("ancestor", "ali", "ayesha"))))

print()
print(kb.explain(("uncle_or_aunt", "sara", "omar")))
```

## 9. Expected behaviour

- Forward chaining derives `ancestor(ali, ayesha)` through three generations, plus the symmetric sibling
  facts and two aunt/uncle facts (`sara` of `omar`, `hina` of `zain`).
- The backward proof shows the recursive rule F2 applied twice, with each level justified by a `parent`
  fact.
- Removing `different` from F3 makes every person their own sibling and then inflates `uncle_or_aunt` —
  the clearest demonstration in the module that a missing constraint is not a detail.
- Without the depth guard, `ancestor(?x, ?x)` and symmetric rules can recurse until Python's limit.

## 10. Evaluation metrics

| Check | Pass condition |
| :--- | :--- |
| Derived set | matches the hand-drawn tree exactly |
| Proof tree | depth and rule ids are correct |
| Negative cases | `ancestor(ayesha, ali)` is not derived |
| Robustness | bounded recursion, no `RecursionError` |
| Explanation | the effect of removing `different` is quantified |

## 11. Testing instructions

- Assert the nine expected ancestor facts (count them by hand first).
- Assert `("ancestor", "ayesha", "ali") not in kb.facts`.
- Assert `kb.backward_chain(("relative", "ayesha", "ali")) is None`.
- Time the forward chain: it must finish in well under a second on this graph.
- Run `python code/expert_system.py` and confirm the self-test passes.

## 12. Submission requirements

The tree drawing, the derived-fact table, the proof tree, the "removed constraint" experiment with counts,
and the four-sentence comparison with probabilistic reasoning.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Representation | 20% | facts and rules chosen to make the tree explicit |
| Inference | 25% | forward and backward agree; recursion bounded |
| Diagnosis | 25% | over-general rule quantified by derived facts |
| Testing | 20% | negative cases and counts checked |
| Comparison | 10% | logic vs probability stated precisely |

## 14. Extension challenges

1. **Cousin rule.** Add `cousin(?x, ?y)` and verify it against the drawn tree.
2. **Closed-world test.** Add a negation-as-failure rule and discuss why it is not classical negation.
3. **Scale.** Generate a 50-person synthetic tree and measure forward-chaining time.
4. **Consistency.** Insert a fact that contradicts a rule and describe how your engine behaves.

## Reflection

First-order rules compress a family tree into a handful of lines and prove any relationship in it. They also
make over-generalisation cheap: one missing condition turns every person into their own sibling. Logic gives
you exactness and no sense of proportion — which is precisely the gap the next lab fills with probability.
