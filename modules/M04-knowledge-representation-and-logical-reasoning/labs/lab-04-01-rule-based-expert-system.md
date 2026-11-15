# LAB-04-01 — Rule-Based Expert System

| | |
| :--- | :--- |
| Module | M04 · Knowledge Representation and Logical Reasoning |
| Level | 200 |
| Time | 2.5 hours |
| Prerequisites | [L04-01](../lessons/L04-01-knowledge-representation-fundamentals.md), [L04-03](../lessons/L04-03-inference-rules-and-equivalence.md), [L04-07](../lessons/L04-07-rule-based-and-expert-systems.md) |
| Code | `code/expert_system.py` |

[← Module](../README.md) · [Next lab: LAB-04-02 →](lab-04-02-logic-based-reasoning-and-inference.md)

## 1. Learning objectives

- **Design** a small knowledge base as facts and rules with stable identifiers.
- **Implement** forward chaining that terminates and records why each fact was derived.
- **Explain** a conclusion by replaying its derivation, not by paraphrasing it.
- **Test** a rule base against cases that should and should not fire.
- **Identify** the maintenance problem that rule bases create at scale.

## 2. Scenario

A university's academic office wants a first-pass eligibility checker for a scholarship programme. Staff
currently read applications by hand and apply five policies from a handbook. The office wants the same
policies encoded so that decisions are consistent and every answer comes with its reason.

This is a **teaching simulation**. It is not an official admission or scholarship service, and no real
student record is used anywhere in this lab.

## 3. Problem statement

Encode the policy as a knowledge base and answer queries with explanations:

1. represent facts as tuples `(predicate, value…)` and rules as `if_all → then`;
2. run forward chaining and print the derivation order;
3. explain a conclusion as a proof tree;
4. test four applicant profiles, including one that must **not** qualify;
5. add one policy and show that no unrelated conclusion changed.

## 4. Background concepts

- A rule base separates **what** is known (facts) from **how** to conclude (rules).
- Forward chaining is data-driven: it fires rules whose premises hold, adding conclusions until closure.
- Termination needs monotonicity: never remove facts, never fire the same rule with the same binding twice.
- An explanation is a stored derivation, not a sentence generated afterwards.
- The frame problem, conflict resolution and rule interaction are the maintenance costs of this design.

## 5. Dataset information and licensing

No dataset. Applicant profiles are synthetic values written in the lab; `advising_kb()` in
`code/expert_system.py` encodes the synthetic policy. Both are course-authored: the lab text is
covered by CC BY 4.0, and the synthetic profiles are dedicated to the public domain under CC0 1.0
(see `DATASET-LICENSE.md`). The rules are invented for teaching and must not be presented as
institutional policy.

## 6. Software requirements

Python 3.10+ and the module's `expert_system.py`. No third-party packages, no network access.

## 7. Step-by-step tasks

1. Read `advising_kb()` and list its ten rules in a table: id, premises, conclusion, note.
2. Create a knowledge base, add `("gpa", "high")` and `("english", "passed")`, and run forward chaining.
   Print the derivations in order.
3. Print `kb.explain(("scholarship", "automatic"))`. Draw the tree by hand and check it against the code.
4. Profile A: GPA high, English passed → expect honours + scholarship.
   Profile B: GPA mid, English passed → expect standard admission, no scholarship.
   Profile C: GPA low, English not passed → expect a probation meeting, no admission.
   Profile D: GPA high, English not passed → expect **no** admission (the language rule blocks it).
5. Add a rule for a "deferral" outcome and confirm profiles A–D are unchanged.
6. Write the five-sentence maintenance paragraph: what breaks first if the policy grows to 200 rules?

## 8. Starter code

```python
import expert_system as es

kb = es.advising_kb()
kb.add_fact("gpa", "high")
kb.add_fact("english", "passed")
derived = kb.forward_chain()
print("derived facts:", len(derived))
for d in derived:
    print(f"  {es.fmt(d.conclusion):40s} by {d.rule.id} from {[es.fmt(p) for p in d.premises]}")

print()
print(kb.explain(("scholarship", "automatic")))

print()
proof = kb.backward_chain(("admit", "honours_programme"))
print(es.proof_text(proof))
```

## 9. Expected behaviour

- Profile A derives `eligible(honours)`, `satisfies(language_requirement)`,
  `admit(honours_programme)` and `scholarship(automatic)` — four derivations, in that order.
- The explanation prints a tree in which `scholarship(automatic)` is justified by R7, which depends on R5,
  which depends on R1 and R4, each resting on a given fact.
- Profile D produces **no** admission fact. That negative case is the important one: a rule base that only
  ever says yes has not been tested.
- Backward chaining proves the same goal from the same facts and returns `None` for an unsupported one.

## 10. Evaluation metrics

| Check | Pass condition |
| :--- | :--- |
| Soundness | every derived fact has all premises present |
| Completeness on the test set | the four profiles yield the documented outcomes |
| Explanation | the printed tree matches the rule ids used in the derivation |
| Termination | forward chaining stops without a bound in the loop |
| Idempotence | running chaining twice adds no new facts |

## 11. Testing instructions

- Assert the four profile outcomes exactly (including the negative case).
- Assert `len(kb.forward_chain()) == 0` on a second call.
- Assert every derivation's premises are in `kb.facts`.
- Assert `kb.backward_chain(("admit", "standard_programme"))` is `None` for Profile A.
- Run `python code/expert_system.py`; it must print `expert_system self-test: True`.

## 12. Submission requirements

The rule table, the derivation trace for Profile A, the four profile outcomes with explanations for two of
them, and the maintenance paragraph. No real student data.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Knowledge base design | 25% | rules are atomic, named, and non-overlapping where possible |
| Inference implementation | 25% | sound, terminating, order recorded |
| Explanations | 20% | tree printed and correctly interpreted |
| Testing | 20% | negative cases included, idempotence checked |
| Reflection | 10% | maintenance cost named with a concrete example |

## 14. Extension challenges

1. **Conflict resolution.** Add two rules that can conclude different outcomes and define a priority scheme.
2. **Certainty factors.** Attach a confidence to each rule and propagate it — then note where it stops being
   logic.
3. **Backward-only mode.** Answer "why is this applicant eligible?" without running forward chaining first.
4. **Rule explosion.** Add five more policies and measure how many rules interact; report the count of
   rule pairs that can fire on the same fact.

## Reflection

An expert system's value is its auditability: every answer has a proof. Its cost is that the proof must be
maintained by hand, and rule interactions grow faster than rules do. That trade-off — explainability bought
with maintenance — is why this design survives in regulated domains and disappears elsewhere.
