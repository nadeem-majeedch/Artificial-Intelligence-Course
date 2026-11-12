# PA-04 — A Rule-Based Eligibility Adviser

| | |
| :--- | :--- |
| Assignment | 04 |
| Difficulty | Intermediate |
| Estimated time | 4 hours |
| Prerequisites | M04 (L04-02 … L04-07), P01 |
| Covers | propositional logic, forward chaining, rule bases, explanation, limits |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

A scholarship office applies a published policy: twelve rules over income, household size, enrolment
status and prior award. Staff apply them inconsistently, and applicants cannot see why they were
refused. The assignment is to encode the policy, run inference, and produce an audit trail — then
show where a rule base stops being the right tool.

## Problem scenario

Facts are supplied per applicant as a dictionary. The rule base must derive `eligible` or
`ineligible`, and explain which rules fired. One rule is deliberately ambiguous; you must resolve it
by writing the resolution down, not by guessing.

## Learning outcomes

1. Encode a policy as Horn-style rules and test it against worked cases.
2. Implement forward chaining with a derivation trace.
3. Detect and report conflicts and unreachable rules.
4. Explain when a rule base should be replaced by a learned model, and vice versa.

## Tasks

1. **Formalise.** Convert the twelve policy rules to implications; state the atomic propositions.
2. **Inference.** Implement forward chaining returning the derived conclusion and the rule chain.
3. **Cases.** Build 25 test applicants covering each rule, including two deliberate conflicts.
4. **Explanation.** For each case print: conclusion, the rules that fired, the facts that triggered
   them, and any rule that could have fired but did not.
5. **Static checks.** Report rules that can never fire given the others, and any pair that can derive
   contradictory conclusions.
6. **Limits.** Add a fuzzy threshold case ("income approximately below 30,000") and explain, in the
   report, why the rule base now needs a different formalism or a learned component.

## Constraints

- No probabilistic inference and no ML.
- The derivation trace must be machine-generated, not hand-written.
- The policy text is the source of truth; where it is ambiguous, document your reading.

## Expected deliverables

`rules.py`, `infer.py`, `cases.csv` with expected and actual conclusions, `explanations.md`, and a
report section on the ambiguity and the limits.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Formalisation | 25% | rules faithful to policy; atoms defined |
| Inference correctness | 30% | all 25 cases match expected, including conflicts |
| Explanation | 20% | trace names rules and triggering facts |
| Static analysis | 15% | unreachable rules and conflicts reported |
| Discussion of limits | 10% | the fuzzy case is analysed, not hand-waved |

## Bonus challenges

- Implement backward chaining and confirm it derives the same conclusions with fewer rule firings.
- Add a simple truth-maintenance scheme so retracting a fact also retracts conclusions that depended
  on it.

---

[Assessment index](../README.md) · [PA-03](pa-03-intelligent-agents.md) · [PA-05](pa-05-bayesian-reasoning.md)
