# QUIZ-M01 — Solutions and Explanations

[Quiz](quiz-m01.md) · [Assessment index](../README.md)

**Marking.** Part A 1 mark each; B 2 (1 for the verdict, 1 for the reason); C 2 each; D 3 each;
E 3; F 2; G 2 each. Total 20.

---

## Part A

**Q1.1 — C.** The definition is about goal-directed behaviour in an uncertain environment, not
about implementation. A rule-based planner satisfies it; a neural network that makes no decisions
does not. A, B and D are the three clauses the module uses.

**Q1.2 — B.** The AI effect is the boundary moving: once a capability is reliable it is
reclassified as "just software". Chess engines, OCR and route planning all moved across that
line. Distractor D describes an AI winter, which is a funding phenomenon, not a definitional one.

**Q1.3 — B.** Hand-written evaluation with no learning is symbolic AI. Option D is the common
error: learning is one route to AI, not the definition. Option A requires fitting from data;
option C requires generation.

## Part B

**Q1.4 — False.** Learning is one way to achieve goal-directed behaviour, not a requirement. A
rule-based system that perceives, decides and acts in an uncertain environment is AI under the
course definition; the question is capability, not mechanism. (1 mark for "false", 1 for the
reason.)

## Part C

**Q1.5 — Model answer.** Automation executes a fixed procedure and fails, visibly, when the
situation is outside what the designer anticipated. AI is the attempt to handle the unanticipated
case: it perceives an uncertain situation and selects among alternatives rather than following one
path. The practical test is what happens at the edge of the specification: automation stops or does
the wrong thing silently; an AI system is expected to degrade, abstain, or generalise.

**Q1.6 — Model answer.** Symbolic methods are stronger where the rules are known and must be
audited — tax calculation, eligibility policy, a game with explicit legal moves. Statistical
methods are stronger where the rule is unknown but examples are plentiful — recognising a cat,
transcribing speech. They are complementary because a deployed system often needs both: a learned
component to handle perception and a symbolic boundary to guarantee compliance (M14 measures this
directly: a model alone produced 100 policy violations, a rule gate reduced that to zero).

## Part D

**Q1.7 — (3 marks, 1 each).** Score $= 3p + 2d + 3a$ out of 8.

- (a) $3(1) + 2(1) + 3(0) = 5$
- (b) $3 + 2 + 3 = 8$
- (c) $0$

The maximum is 8, so (b) is the only system using the full capability set as defined here.

**Q1.8 — (3 marks).**

- proportion: $873/1000 = 0.873$ (1)
- percentage to one decimal: $87.3\%$ (1)
- error rate: $127$ per 1,000 (1)

Note the third is not $0.127\%$ — it is 127 cases per thousand, i.e. 12.7%.

## Part E

**Q1.9 — (3 marks).** Order: Dartmouth workshop (1956) → expert systems boom (late 1970s–1980s) →
first AI winter (late 1980s) → deep learning wins ImageNet (2012) → transformer architecture
(2017). 2 marks for the correct order; 1 mark for identifying the longest gap, expert systems to
ImageNet (roughly 25 years), or Dartmouth to expert systems if you date the boom from the
mid-1970s.

## Part F

**Q1.10 —** `5 0.625`

The score is 5; $5/8 = 0.625$ and `.3f` prints three decimals. `print` with two arguments separates
them with a single space. (Students who write `0.63` have rounded when the format did not ask for
rounding.)

## Part G

**Q1.11 — Model answer (2 marks, 1 per claim).** Two common unsupported claims: "the model
understands" — a benchmark measures task accuracy, not understanding, and would need
counterfactual or compositional tests; "the model is safe for clinical use" — a held-out accuracy
figure says nothing about prevalence shift, subgroup error or prospective validation. Other
acceptable answers: "human-level", "general", "will replace X", each with the specific evidence
that would be needed.

**Q1.12 — Model answer (2 marks).** Two consequences: (i) you choose a technique by the structure
of the problem — known rules suggest symbolic, unknown mapping with data suggests statistical —
rather than by fashion; (ii) you accept hybrid designs, since a perception component and a
compliance rule answer different questions. A third acceptable consequence: benchmarks from one
paradigm do not transfer as evidence to another.

---

[Quiz](quiz-m01.md) · [Next solutions](quiz-m02.md) · [Assessment index](../README.md)
