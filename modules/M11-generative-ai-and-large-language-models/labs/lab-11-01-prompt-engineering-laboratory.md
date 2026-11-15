# LAB-11-01 — Prompt Engineering Laboratory

> **Module M11** · Lab 1 of 3 · ~150 minutes · Level 400
> **Covers:** L11-04 · **Pairs with:** NB-11-02 · **Scenarios:** university FAQ chatbot, text generation

[Module overview](../README.md) · [Next lab: LAB-11-02 →](lab-11-02-build-a-retrieval-augmented-assistant.md)

Prompt engineering is a measurement discipline. This lab makes you build a miniature
evaluation harness, run seven templates, and then explain why most of the differences you
observe are not real.

---

## Scenario — the university FAQ chatbot's prompt

### Problem description

A university wants an assistant that answers student questions from its handbook. You are not
being asked to build the whole system today (that is LAB-11-02); you are asked to answer one
question with evidence: **which prompt should the assistant use, and how would you know?**

### Business context

Every template change is a deployed change. A template that shortens answers can raise exact
match and lower user satisfaction; a template that invites explanation triples the token bill.
The lab's deliverable is a decision, with the evidence that supports it.

### Data and licence

- 24 handbook documents and 30 gold questions from `code/gen_data.py`, authored for this
  module under **CC0-1.0**.
- The model is `google/flan-t5-small` (**Apache-2.0**), 77M parameters, run locally on CPU.

### Tasks

1. **Prompt inventory.** Read `code/prompts.py` and write down, for each of the seven
   templates, which of the six prompt parts (role, task, context, constraints, format,
   examples) it contains and which it omits.
2. **Baseline.** Run `python prompts.py`. Record the table: exact match, token F1, mean answer
   length, refusal rate and latency for all seven templates.
3. **Confidence intervals.** For every exact-match value, compute the 95% interval with
   $n=12$. State which template differences are larger than the interval.
4. **Extend the sample.** Build a 40-question evaluation set of your own from the handbook
   (30 answerable, 10 unanswerable), and re-run zero-shot, few-shot and extractive on it.
   Report the new table with $n=40$.
5. **Structured output.** Ask for JSON on six questions. Report how many outputs parse raw,
   how many parse after regex extraction, and what a retry loop with the validation error
   achieves in three attempts.
6. **Chain-of-thought.** Run the CoT template on four questions. Classify each output as
   correct, correct-but-unparseable, or wrong. Explain the EM of 0.00 in those terms.
7. **Injection.** Use the poisoned document in `prompts.py`. Report the attack success rate
   for the naive and defended prompts, and state explicitly whether the experiment is
   informative for this model. Then describe what evidence would be needed with a capable
   model.
8. **Token economics.** Compute prompt tokens for zero-shot and few-shot, and the daily cost
   difference at 10,000 queries for a price of 0.50 USD per million tokens.
9. **Decision.** Write a one-page recommendation: which template, which guardrails, which
   metric you will monitor, and what you would measure next.

### Expected results (measured here)

```text
template              EM    F1  chars  refuse   sec
zero-shot           0.67  0.80   11.9    0.00  0.25
one-shot            0.50  0.74   10.2    0.00  0.24
few-shot            0.50  0.74   10.2    0.00  0.30
role                0.67  0.80   11.9    0.00  0.28
extractive          0.58  0.77   13.8    0.00  0.27
chain-of-thought    0.00  0.18  130.1    0.00  1.01
structured-json     0.58  0.77   12.7    0.00  0.27

valid JSON objects: 0/6     recovered by extraction: 0/6
injection: naive 0.00, defended 0.00 (inconclusive: the model does not follow the injection)
zero-shot 569 chars / 135 tokens; few-shot 1079 chars / 258 tokens
```

At $n=12$ the interval around 0.67 is roughly ±0.28, so **none of the differences between
zero-shot, role and one-shot is significant**. CoT's drop to 0.00 is larger than the interval
and is a real, reproducible effect for this model on this task.

### Metrics summary

| Stage | Metric | Why |
| :--- | :--- | :--- |
| Answer | exact match, token F1 | does the answer match the gold span |
| Behaviour | refusal rate | does it decline when it should |
| Format | parse rate | can a program consume the output |
| Operations | tokens, latency | what each template costs |

## Deliverables

1. `prompt_lab.py` — your harness, parameterised by template and question set.
2. `results.csv` — one row per template × question.
3. `lab-11-01-report.md` — the two tables, the intervals, the JSON and injection findings and
   the one-page decision.
4. A short note on what you would change about the 12-question set.

## Extensions

- Add a template with an explicit "answer with a number only" instruction and measure EM on
  numeric questions only.
- Compare greedy with sampling at temperature 0.3 on the same set (five seeds).
- Add a periodic self-check template ("before answering, list the sentences you used") and
  measure whether it changes EM or length.
- Try a larger local model and repeat the table; report which findings replicate.

## Common pitfalls

- Concluding "few-shot is worse" from 12 questions without an interval.
- Reporting exact match without answer length, so a template that emits one word looks best.
- Treating 0/6 JSON as a model property rather than a prompt-plus-decoder property.
- Claiming a defence against injection when the model was simply too weak to comply.
- Changing the question set between templates.

## Marking guide

| Criterion | Weight |
| :--- | ---: |
| Working harness with fixed question set and metrics | 25% |
| Correct intervals and honest significance claims | 20% |
| Structured-output analysis including retries | 20% |
| Injection discussion, including the inconclusive case | 15% |
| Decision memo with a monitoring plan | 20% |

## Starter material

The guided notebook [`nb-11-01-tokens-attention-and-generative-models.ipynb`](../notebooks/nb-11-01-tokens-attention-and-generative-models.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
