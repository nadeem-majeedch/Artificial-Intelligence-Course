# MP-11 — Domain Question-Answering Assistant

| Module | M11 · Generative AI and Large Language Models |
| :--- | :--- |
| Type | Mini-project (individual or pairs) |
| Effort | ~2 hours core, up to 10 hours with the production extras |
| Deliverables | Repository, short report, five-minute demo |
| Covers | L11-02 to L11-07 |

[← Module home](../README.md) · [Assignment](../assignments/asg-11-rag-evaluation-report.md) · [Summary](../summary.md)

## The brief

Ship a question-answering assistant for a real, narrow domain, with sources, a refusal path,
and an evaluation you can defend. This is the module's capstone: it combines retrieval,
prompting, generation and measurement.

Choose a domain you can legitimately use:

| Track | Corpus | Why it is interesting |
| :--- | :--- | :--- |
| A — Handbook / policy | the module corpus, or your institution's public policy pages | exact answers, dates and numbers, refusal matters |
| B — Course notes | your own notes from two or three modules | messy structure, formulas, inconsistent naming |
| C — Open documentation | a public-domain or permissively licensed manual | long documents, code identifiers, chunking pressure |
| D — Your own writing | essays, reports, notes you own | small corpus, style variation, licence certainty |

Track C is the best choice if you want to test chunking and hybrid retrieval seriously.
Track A is the best choice if you have limited time and want a clean baseline.

## Required work

1. **Corpus card.** Source, licence, size in words and documents, date collected, known gaps.
2. **Pipeline.** Chunking parameters, dense and lexical indexes, fusion, reranking (or a stated
   reason not to), context packing with an explicit token budget.
3. **Prompt.** Role, evidence boundary, refusal path and output contract, versioned.
4. **Interface.** Streamlit app or CLI; show the retrieved sources next to every answer.
5. **Evaluation.** 40 questions (30 answerable, 5 multi-document, 10 unanswerable), metrics at
   each stage, latency percentiles, and the model's licence.
6. **Error analysis.** Six failures, classified by stage, with quoted evidence.
7. **Demo.** Five minutes: the problem, the baseline, the system, the evidence, the caveat.

## Milestones

| Time | Milestone | Exit criterion |
| :--- | :--- | :--- |
| 0:00–0:20 | Choose domain, collect corpus, write corpus card | 20+ documents, licence recorded |
| 0:20–0:50 | Ingest, chunk, index, retrieve | Three queries return sensible chunks |
| 0:50–1:10 | Prompt with refusal path, end-to-end answers | Five answers with sources |
| 1:10–1:40 | Evaluation set and harness | Metrics for every stage |
| 1:40–2:00 | Error analysis, interface, demo prep | Six failures classified, app runs |

## Repository layout

```text
mp11/
  README.md            # five commands to run it
  data/                # corpus + LICENCE + corpus-card.md
  pipeline.py          # ingest, chunk, index, retrieve
  prompts.py           # versioned prompt templates
  answer.py            # CLI and Streamlit entry point
  evaluate.py          # harness: metrics, slices, results.csv
  results/             # results.csv, figures, sample outputs
  REPORT.md            # methods, results, error analysis, limitations
```

## Reproducibility requirements

- One command builds the index; one command runs the evaluation.
- No downloads at import time; models named explicitly with their licence.
- Seeds fixed where sampling is used; greedy decoding for the evaluation.
- `results.csv` records every question × configuration.
- The corpus is either redistributable or excluded from the repository with a fetch script.

## Licensing and compute (state these in the report)

| Component | Licence | Note |
| :--- | :--- | :--- |
| `all-MiniLM-L6-v2` | Apache-2.0 | 384-dim embeddings, 22M parameters |
| `google/flan-t5-small` | Apache-2.0 | 77M parameters, seq2seq |
| `distilgpt2` | Apache-2.0 | 82M parameters, decoder |
| your corpus | yours to state | check before publishing the index |

CPU-only is sufficient: this module's full pipeline builds in about 45 s and answers in about
2 s per question. A GPU shortens generation, not retrieval design.

## Grading

| Criterion | Weight |
| :--- | :--- |
| Working system with sources and refusal path | 25% |
| Evaluation set and per-stage metrics | 25% |
| Error analysis quality | 20% |
| Reproducibility and documentation | 15% |
| Licence and compute honesty | 10% |
| Demo clarity | 5% |

## Stretch goals

- Add query rewriting or HyDE and measure the effect on multi-document questions.
- Calibrate a retrieval-score threshold and report the refusal/over-refusal trade-off.
- Add a LoRA adapter trained on 50 domain Q/A pairs and compare it with the prompt baseline on
  the same evaluation set.
- Quantise the generator and report size, latency and quality on your set.
- Add caching and measure the hit rate and cost saving.
- Write a one-page incident runbook: what to check when an answer is wrong.

## Anti-goals

These do not earn marks: a demo with no evaluation; a corpus you may not redistribute; metrics
without $n$; "it is accurate" without a refusal test; a Streamlit app that hides its sources;
claims of improvement from a 12-question comparison.

## Presentation questions you should be able to answer

1. What decision does this assistant support, and what does a wrong answer cost?
2. Which stage fails most often in your error analysis, and how do you know?
3. What is your refusal rate on unanswerable questions, and is it where you want it?
4. What is the p95 latency, and what dominates it?
5. What would you measure first if users reported hallucinations next week?
