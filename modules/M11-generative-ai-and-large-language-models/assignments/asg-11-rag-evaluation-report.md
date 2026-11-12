# ASG-11 — A RAG System with an Evaluation Report

| Module | M11 · Generative AI and Large Language Models |
| :--- | :--- |
| Type | Individual assignment |
| Effort | ~1.5 hours core (up to 6 hours with the extensions) |
| Submit | Code, evaluation harness, results file and report |
| Covers | L11-04, L11-05, L11-07 |

[← Module home](../README.md) · [Labs](../labs/lab-11-02-build-a-retrieval-augmented-assistant.md) · [Quiz](../quizzes/quiz-11.md)

## Brief

Build a retrieval-augmented assistant over a document set of your choice, then **prove** how
well it works at each stage. The deliverable is not the chatbot; it is the evidence.

A submission that says "it works well" earns nothing. A submission that says "recall@3 is
0.93, exact match is 0.58, refusal rate on unanswerable questions is 0.25, and here are the
four failures I could not fix" earns full marks for evidence.

## Requirements

1. **Corpus.** At least 20 documents, at least 3,000 words, with a stated licence and
   provenance. Use the module handbook, your own notes, or a public-domain source. Do not
   redistribute copyrighted material.
2. **Pipeline.** Ingestion, chunking with recorded parameters, dense and lexical indexes,
   fusion, context packing, grounded generation with a refusal path.
3. **Evaluation set.** At least **40 questions**: 30 answerable (including 5 that need two
   documents) and 10 that the corpus cannot answer. Each has a gold answer and, for
   answerable items, a gold document id.
4. **Metrics.** Retrieval (recall@1, recall@3, MRR), answers (exact match, token F1), grounding
   (support rate, unsupported numbers), behaviour (refusal rate on unanswerable items),
   operations (p50/p95 latency).
5. **Ablation.** One factor changed at a time, three configurations minimum: chunk size,
   hybrid weight $\alpha$, or reranking on/off. Report the delta and whether it exceeds the
   noise of your sample.
6. **Error analysis.** At least six inspected failures, classified as retrieval miss, wrong
   span, unsupported claim, or unnecessary refusal. Quote the question, the retrieved
   documents and the answer.
7. **Report.** Eight sections, two pages of prose plus tables and figures.

## Suggested structure

| Section | Content | Length |
| :--- | :--- | :--- |
| 1. Question | What the assistant is for and who uses it | 2–3 lines |
| 2. Corpus | Documents, licence, size, chunking parameters | 1 paragraph |
| 3. Pipeline | Index types, fusion, context budget, model, prompt | 1 paragraph + diagram |
| 4. Evaluation set | Construction, slices, gold sources | 1 paragraph |
| 5. Results | Tables by stage | Tables |
| 6. Ablation | One factor, three configurations, deltas | Table + 2 paragraphs |
| 7. Error analysis | Six failures with quoted evidence | Bullets |
| 8. Limitations | Sample size, synthetic corpus, CPU model, cost | 1 paragraph |

## Worked example of the results table

Numbers from the module's own 24-document handbook corpus, 30 questions — use them as a
format model, not as your results:

| Stage | Metric | Value |
| :--- | :--- | ---: |
| Retrieval | recall@1, hybrid | 1.00 |
| Retrieval | MRR, hybrid | 1.000 |
| Answers (12 q) | exact match | 0.75 |
| Answers (12 q) | token F1 | 0.85 |
| Grounding | mean support rate | 1.00 |
| Behaviour | refusal rate, 8 unanswerable | 0.00 |
| Operations | mean latency | 1.84 s |

The row that matters most is the refusal rate. A system that answers everything with grounded
text looks excellent on three metrics and fails the one test that matters for trust.

## Marking rubric

| Criterion | Weight | What full marks looks like |
| :--- | ---: | :--- |
| Working, reproducible pipeline | 20% | One command builds the index and runs the harness |
| Evaluation set quality | 20% | 40+ items, gold documents, unanswerable slice, stated provenance |
| Metrics reported per stage | 20% | All five families, with $n$ and intervals |
| Ablation discipline | 15% | One factor, three configurations, deltas compared with noise |
| Error analysis | 15% | Six classified failures with quoted evidence |
| Report quality | 10% | Reproducible commands, figures labelled, claims bounded by evidence |

## Submission checklist

- [ ] `python evaluate.py` runs end to end on CPU in under 15 minutes.
- [ ] `results.csv` contains one row per configuration × question.
- [ ] Report states the corpus licence and the model's licence.
- [ ] No claim of improvement without a measured baseline on the same question set.
- [ ] The unanswerable slice is reported separately, never averaged into the main score.

## Extensions (optional, not graded)

- Add query rewriting or HyDE and measure the delta on the two-document questions.
- Replace MaxSim reranking with a cross-encoder and compare nDCG and latency.
- Add a score threshold calibrated on the unanswerable set and report the new refusal and
  over-refusal rates.
- Compare flan-t5-small with a larger local model and report quality, latency and memory.

## Common pitfalls

- Tuning the prompt on the same 40 questions you report on.
- Reporting precision@3 with one relevant document and interpreting it as a quality signal.
- Quoting a single run and no interval.
- Averaging unanswerable questions into exact match, which hides the failure mode entirely.
- Forgetting to say which chunk size produced the reported numbers.
