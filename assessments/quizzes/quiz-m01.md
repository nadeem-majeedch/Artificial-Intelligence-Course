# QUIZ-M01 — Introduction and Foundations of AI

| | |
| :--- | :--- |
| Module | M01 · Introduction and Foundations of AI |
| Questions | 12 (20 marks) |
| Time | 30 minutes |
| Covers | L01-01 … L01-05 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m01.md) · [Module](../../modules/M01-introduction-and-foundations/README.md)

**How to use this.** Answer everything on paper first, without notes. Then mark against the
solutions file, which explains each answer and the wrong options. A question you got right by
elimination still deserves a reread.

Marks are shown per question. Part A is multiple choice (1 mark each), Part B true/false with a
reason (2), Part C conceptual (2 each), Part D numerical (3 each), Part E tracing (3), Part F
Python output (2), Part G short answer (2 each).

---

## Part A — Multiple choice (3 marks)

**Q1.1** Which clause is **not** part of this course's working definition of AI?

- A. Perceiving an environment
- B. Selecting actions among alternatives
- C. Being implemented with a neural network
- D. Pursuing a goal under uncertainty

**Q1.2** The "AI effect" describes which phenomenon?

- A. Models get slower as they get larger
- B. Once a capability works reliably, it stops being called AI
- C. Accuracy improves as data grows
- D. Research funding collapses after a winter

**Q1.3** A chess engine that evaluates positions with hand-written rules and never learns is best
described as

- A. machine learning
- B. symbolic AI with hand-written knowledge
- C. generative AI
- D. not AI at all, because it does not learn

## Part B — True or false, with a one-sentence reason (2 marks)

**Q1.4** "A system that is entirely rule-based cannot be considered AI, because AI requires
learning from data."

## Part C — Conceptual (4 marks)

**Q1.5** (2 marks) Explain the difference between *automation* and *AI* in terms of what the system
does when the situation is not anticipated by its designer.

**Q1.6** (2 marks) Give one reason the symbolic and statistical traditions are complementary rather
than competing, using an example of a task where each is stronger.

## Part D — Numerical (6 marks)

**Q1.7** (3 marks) A teaching rubric scores a system on three capabilities, each 0 or 1, with
weights 3, 2 and 3 for *perceives*, *decides* and *adapts*. Compute the capability score for:

- (a) a thermostat: perceives 1, decides 1, adapts 0
- (b) a spam filter retrained monthly: perceives 1, decides 1, adapts 1
- (c) a lookup table with no sensing and no decisions: 0, 0, 0

**Q1.8** (3 marks) A model is right on 873 of 1,000 test cases. Express its accuracy as a
proportion, a percentage to one decimal place, and as an error rate in cases per 1,000.

## Part E — Tracing (3 marks)

**Q1.9** Place these five events in chronological order and state which two are separated by the
longest gap:

1. transformer architecture
2. first AI winter
3. deep learning wins ImageNet
4. Dartmouth workshop
5. expert systems boom

## Part F — Python output (2 marks)

**Q1.10** What does this print?

```python
scores = {"perceives": 1, "decides": 1, "adapts": 0}
total = 3 * scores["perceives"] + 2 * scores["decides"] + 3 * scores["adapts"]
print(total, f"{total / 8:.3f}")
```

## Part G — Short answer (4 marks)

**Q1.11** (2 marks) Name two claims about AI capability that are commonly made and are **not**
supported by a benchmark result. Explain what evidence would support each.

**Q1.12** (2 marks) The module argues that "AI" is a family of methods rather than one technology.
Give two consequences of that framing for how you should choose a technique for a new problem.

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m01.md) ·
[Next quiz](quiz-m02.md)
