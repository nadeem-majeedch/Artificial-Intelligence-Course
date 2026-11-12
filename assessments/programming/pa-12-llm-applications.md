# PA-12 — A Grounded Question-Answering Application

| | |
| :--- | :--- |
| Assignment | 12 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M11 (L11-05, L11-07), PA-08 |
| Covers | retrieval, prompt construction, grounding, refusal, evaluation harness |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

An assistant that answers from a document set must do three things: retrieve the right passage, answer
only from it, and refuse when the answer is absent. Each is measurable, and most demos measure none.

## Problem scenario

Given 30 documents and 40 questions (30 answerable, 10 not), build a retrieval-augmented answerer and
an evaluation harness that reports retrieval and answer quality separately.

## Learning outcomes

1. Build a retrieval index and measure recall@k.
2. Construct prompts that delimit evidence and specify a refusal path.
3. Score groundedness and refusal, not only answer similarity.
4. Separate retrieval failures from generation failures.

## Tasks

1. **Index.** Chunk with overlap; report chunk count and recall@5 for BM25.
2. **Answer.** Answer with citations; refuse when no passage supports an answer.
3. **Harness.** Per question: retrieved passages, answer, citation, grounded (yes/no), correct (yes/no).
4. **Attribution.** Classify each error as retrieval, generation, or evaluation ambiguity; report counts.
5. **Unanswerable set.** Report refusal rate and false-answer rate.
6. **Iteration.** Make one change (chunk size or k) and report the metric change.

## Constraints

- No hosted APIs; a local model or a template answerer is acceptable if labelled.
- Fixed question set and seeds.
- Delimit documents; never place untrusted text as instructions.

## Expected deliverables

`rag.py`, `eval_set.jsonl`, `results.md`, and a failure table with ten examples.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Retrieval | 20% | recall@5 measured with chunk statistics |
| Grounding | 25% | answers cite; unsupported answers counted |
| Refusal | 20% | unanswerable set handled and reported |
| Error attribution | 25% | retrieval vs generation separated |
| Reproducibility | 10% | one command regenerates results |

## Bonus challenges

- Compare dense, lexical and hybrid retrieval on the same 40 questions.
- Add a confidence band and test whether it predicts correctness.

---

[Assessment index](../README.md) · [PA-11](pa-11-generative-ai.md) · [PA-13](pa-13-ai-agents.md)
