# LAB-11-03 — An Evaluation Harness for LLM Systems

> **Module M11** · Lab 3 of 3 · ~150 minutes · Level 400
> **Covers:** L11-06, L11-07 · **Pairs with:** NB-11-02
> **Scenarios:** sentiment analysis with an LLM, local LLM chatbot, domain assistant, fine-tuning comparison

[Module overview](../README.md) · [Previous lab: LAB-11-02](lab-11-02-build-a-retrieval-augmented-assistant.md)

The last lab is the one that makes the previous two trustworthy. You will build a harness that
scores retrieval, answers, grounding, behaviour, cost and an adapter against a fixed set.

---

## Scenario A — sentiment analysis with an LLM

### Problem description

Classify 40 labelled sentences with a prompted model, then decide whether the prompt is worth
using compared with a trivial baseline.

### Data and licence

`code/gen_data.SENTENCES` — 40 sentences authored for this module (CC0-1.0), 22 positive and
18 negative, deliberately containing negation, contrast and sarcasm. The model is
`distilbert-base-uncased-finetuned-sst-2-english` (**Apache-2.0**), a 67M-parameter classifier
already cached locally.

### Tasks

1. **Baseline.** Count positive/negative predictions from the SST-2 classifier on all 40
   sentences. Report accuracy and the confusion matrix.
2. **Prompt baseline.** Ask flan-t5-small to answer positive/negative for the same 40
   sentences with a one-line prompt. Report accuracy.
3. **Slice analysis.** Split the sentences into "plain", "negation", "sarcasm" and
   "contrast". Report accuracy per slice for both systems. Which slice breaks which system?
4. **Agreement.** Compute percent agreement and Cohen's κ between the two systems.
5. **Cost.** Report tokens per request and the mean latency for each system.

### Expected results

The classifier is the stronger baseline and the prompt is worse on sarcasm; the exact numbers
you get will differ from any published figure because the sentence set is authored here, so
**report your own**. What must be true for full marks: the confusion matrix, the per-slice
table, and a statement that 40 items gives a 95% interval of roughly ±0.15.

---

## Scenario B — the local chatbot's refusal behaviour

### Problem description

Measure whether a local assistant refuses what it should and answers what it should, using
both out-of-corpus questions and benign in-corpus questions.

### Tasks

1. Use the eight unanswerable questions from `gen_data.UNANSWERABLE` plus ten answerable ones.
2. Run `RAGSystem().answer(...)` for each. Record answer, grounding score and refusal flag.
3. Report: refusal rate on unanswerable items, refusal rate on answerable items
   (over-refusal), and mean grounding score on each slice.
4. Add a retrieval-score threshold. Sweep it over five values and plot refusal rate against
   threshold for both slices. Choose a threshold and justify it.
5. Write a two-paragraph incident note: what the metric cannot see.

### Expected results

Measured with the module's default prompt: refusal rate **0.00** on unanswerable questions and
**0.00** on answerable ones, with wrong-but-grounded answers such as `'15 working days'` and
`'40 GBP'`. The threshold sweep is the deliverable that turns this into a decision.

---

## Scenario C — adapter versus prompt, on one evaluation set

### Problem description

Train a LoRA adapter (L11-06) and compare it with the base model on the same 40 questions.
This is the lab's central discipline: **one evaluation set, two systems, same metric.**

### Tasks

1. Train `train_lora(steps=40, r=8)`. Record trainable parameters (589,824, 0.715%), held-out
   loss (4.956 → 3.005) and training seconds (12.4 s).
2. Evaluate base and adapter on the 30 answerable handbook questions: exact match, token F1,
   mean answer length.
3. Evaluate both on the eight unanswerable questions: refusal rate.
4. Merge the adapter and re-run three generations; confirm the output is unchanged
   (measured maximum logit difference 6.87e-05).
5. **Quantisation.** Run `quantization_report()`. Report size, latency and exact match for
   fp32 and int8 (measured: 307.8 → 65.9 MB, 0.159 → 0.423 s, EM 1.00 → 0.50 on four items).
6. Decision memo: for this task, which of prompt, adapter or quantisation would you ship, and
   what evidence supports it?

### Expected results

```text
adapter: 0.715% trainable, held-out 4.956 -> 3.005, 12.4 s, 2.4 MB
generation after 40 steps: 'Answer: 08:00 to 09:00 on weekdays'  (format learned, facts not)
quantisation: 307.8 -> 65.9 MB, latency worse, EM 1.00 -> 0.50 on four questions
merge: 24 layers, max logit difference 6.87e-05, zero trainable parameters remaining
```

The adapter likely **does not** beat the base model on exact match after 40 steps. Reporting
that honestly, with the numbers, is worth more than a cherry-picked generation.

---

## Scenario D — cost and latency budget

### Tasks

1. Measure p50 and p95 latency over 20 questions for: retrieval only, retrieval plus
   generation, and generation with a 2× longer context.
2. Compute cost per 1,000 queries at 10 prompt and 2 completion tokens, and at 900 prompt and
   60 completion tokens, for two price points.
3. Identify the dominant term in each case and state one design change that would cut it.

## Metrics summary

| Scenario | Primary | Secondary |
| :--- | :--- | :--- |
| Sentiment | accuracy per slice | κ, latency |
| Refusal | refusal rates on two slices | grounding score, threshold curve |
| Adapter | EM base vs adapter | trainable params, merge equivalence |
| Cost | p50/p95 latency, cost per 1,000 | token counts |

## Deliverables

1. `harness.py` — loads a question set, runs any system, writes `results.csv`.
2. `plots.py` — refusal-vs-threshold curve, latency histogram, adapter comparison bar chart.
3. `lab-11-03-report.md` — four scenarios, tables with $n$ and intervals, one decision memo.
4. `results.csv` with one row per system × question.

## Extensions

- Add a second judge (a different prompt or model) and report κ between the two judges.
- Add an entailment-based hallucination check and compare its flags with the number-support check.
- Run the harness with three seeds on any sampled decoding and report variance.
- Make the harness fail a CI check when recall@3 drops below a threshold.

## Common pitfalls

- Evaluating the adapter on its own training questions.
- Reporting accuracy over the unanswerable slice as if it were a quality score.
- Using mean latency only, hiding the tail.
- Comparing fp32 and int8 at different context lengths.
- Claiming significance from 12 questions.

## Marking guide

| Criterion | Weight |
| :--- | ---: |
| Harness works for multiple systems and writes results | 25% |
| Metrics per stage, with $n$ and intervals | 20% |
| Refusal threshold curve and justification | 20% |
| Adapter comparison and merge verification | 20% |
| Cost/latency analysis and decision memo | 15% |
