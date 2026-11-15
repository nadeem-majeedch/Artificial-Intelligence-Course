# PROJECT-04-01 — Intelligent University Advisory Expert System

| | |
| :--- | :--- |
| Module | M04 · Knowledge Representation and Logical Reasoning |
| Level | 200 |
| Time | 8–10 hours |
| Prerequisites | LAB-04-01, LAB-04-02, LAB-04-03 |
| Code | `code/expert_system.py` |

[← Module](../README.md) · [All projects](../../README.md)

## 1. Problem statement

Build a small advisory system that answers student questions about module choice, eligibility and
progression, using a hand-written knowledge base, forward and backward chaining, a query interface and
explanations. Then evaluate it honestly: where does it give confident nonsense?

**This is a teaching artefact**, not a university service. Use only synthetic student records, and say so in
your submission.

## 2. Requirements

The system must:

1. **Represent knowledge** — at least 25 facts and 15 rules, each rule with an identifier and a one-line
   rationale;
2. **Forward-chain** to closure, recording every derivation;
3. **Backward-chain** a single goal and return a proof tree;
4. **Process queries** in both directions: "what follows from these facts?" and "what would make this true?";
5. **Explain** any conclusion as a rendered proof, not prose;
6. **Test** at least eight scenarios, including three negative ones;
7. **Report** the limitations, including at least two places where logic is the wrong tool.

## 3. Suggested architecture

```text
data/facts.txt      synthetic student records and module facts
kb/rules.py         Rule objects: id, if_all, then, rationale
engine.py           KnowledgeBase (forward + backward chaining, explanations)
queries.py          query parsing and both directions of inference
report.md           test scenarios, results, limitations
```

Keep the engine free of domain knowledge: rules live in `rules.py`, the engine stays generic. That
separation is the difference between a system you can extend and one you cannot.

## 4. Starter code

```python
from expert_system import KnowledgeBase, Rule, fmt, proof_text

kb = KnowledgeBase(rules=[
    Rule("R1", [("passed", "?m", "CS201")], ("eligible", "?m", "CS301"), "CS301 requires CS201"),
    Rule("R2", [("eligible", "?s", "CS301"), ("gpa_above", "?s", 3.0)],
         ("recommend", "?s", "CS301"), "recommend only with a GPA above 3.0"),
    Rule("R3", [("failed", "?s", "?m"), ("required", "?m")],
         ("must", "?s", "retake"), "a failed required module must be retaken"),
])

kb.add_fact("passed", "sara", "CS201")
kb.add_fact("gpa_above", "sara", 3.4)
kb.forward_chain()
print(kb.explain(("recommend", "sara", "CS301")))
print(proof_text(kb.backward_chain(("recommend", "sara", "CS301"))))
```

Note what the engine does *not* do: it does not know what "recommend" means, it cannot weigh a 3.01 against
a 3.4, and it cannot say "probably". Those gaps are your report's content.

## 5. Development milestones

| Milestone | Deliverable | Time |
| :--- | :--- | ---: |
| M1 | rules and facts covering module prerequisites and progression | 2 h |
| M2 | forward chaining with derivation log | 1.5 h |
| M3 | backward chaining with proof tree and cycle guard | 1.5 h |
| M4 | query interface, both directions | 1.5 h |
| M5 | eight test scenarios with expected outcomes | 1.5 h |
| M6 | report: results, limitations, what a probabilistic model would add | 2 h |

## 6. Expected functionality

- `python engine.py --forward facts.txt` prints every derived fact with its rule id.
- `python engine.py --why "recommend sara CS301"` prints the proof tree.
- `python engine.py --what-if "gpa_above sara 2.9"` reports which conclusions disappear.
- A scenario file with eight cases runs as a test suite and prints pass/fail per case.
- The system refuses to answer when the goal is unprovable, rather than guessing.

## 7. Evaluation criteria

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Knowledge representation | 20% | 15+ atomic rules, rationales, no domain logic in the engine |
| Inference | 25% | forward and backward agree, recursion bounded, order preserved |
| Explanations | 20% | proof trees correct and readable |
| Testing | 20% | 8+ scenarios including 3 negatives, all executed |
| Critical evaluation | 15% | limitations specific, with a concrete example of each |

## 8. Extension challenges

1. **Certainty factors.** Attach confidences and propagate them; state precisely where the result stops being
   a probability.
2. **Rule priority.** Add conflict resolution and show a case where priority changes the answer.
3. **Consistency check.** Detect a rule set that derives both a fact and its negation.
4. **Hybrid.** Replace one rule with a Bayesian posterior from LAB-04-03 and argue for the split.
5. **Scale test.** Generate a 200-rule synthetic base and measure forward-chaining time; plot rules against
   time.

## 9. Academic integrity and scope

Use synthetic records only. Do not present the system as an official advising tool, do not encode real
policies without citing them, and state in the report that the knowledge base is a teaching construction.
