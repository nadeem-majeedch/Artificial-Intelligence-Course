# L11-07 — Evaluating LLM Systems: Quality, Hallucination, Cost and Safety

[← Previous: L11-06](L11-06-fine-tuning-and-parameter-efficient-adaptation.md) · [Module end](../README.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: An Evaluation Harness](#4-the-procedure-an-evaluation-harness)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Python Implementation](#7-python-implementation)
- [8. Practical Applications](#8-practical-applications)
- [9. Common Mistakes](#9-common-mistakes)
- [10. Practical Exercises](#10-practical-exercises)
- [11. Self-Assessment](#11-self-assessment)
- [12. Key Terms](#12-key-terms)
- [13. Further Reading](#13-further-reading)
- [What to Do Next](#what-to-do-next)

> **Module M11** · Lesson 7 of 7 · ~90 minutes · Level 400
> **Prerequisites:** L11-04, L11-05

[Previous: L11-06](L11-06-fine-tuning-and-parameter-efficient-adaptation.md) · [Module overview](../README.md) · [Summary](../summary.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Evaluate** a RAG or prompt system at retrieval, answer and grounding levels separately.
2. **Compute** exact match, token F1 and ROUGE-L, and explain when each misleads.
3. **Compute** recall@k, MRR and nDCG@k for retrieval.
4. **Detect** hallucination with grounding and number-support checks.
5. **Judge** answer quality with an LLM rubric and quantify the judge's reliability.
6. **Report** latency percentiles and cost per thousand queries.
7. **Design** an evaluation set with slices, sample sizes and significance in mind.

## 2. Prerequisite Knowledge

Precision/recall (M06), L11-05's architecture, and the metrics module `llm_eval.py`.

## 3. Conceptual Explanation

### 3.1 Evaluate the parts, not just the answer

An end-to-end score of 0.75 hides four different failures:

| Level | Question | Metric | Failure looks like |
| :--- | :--- | :--- | :--- |
| Retrieval | was the right text found? | recall@k, MRR, nDCG | answer missing, or citing the wrong document |
| Answer | does it match the gold answer? | EM, token F1, ROUGE-L | right document, wrong span |
| Grounding | is it supported by the context? | support rate, unsupported numbers | confident invention |
| Operations | what does it cost? | p50/p95 latency, tokens, cost | slow tail, surprise bill |

### 3.2 Exact match, token F1 and ROUGE-L

- **EM** is 1 only if normalised strings are identical. Normalisation (lowercase, strip
  punctuation and articles) is what makes `"08:00"` and `"08:00."` agree — but not `"8:00"`.
- **Token F1** gives partial credit for overlapping tokens; it cannot distinguish a correct
  short answer from a long one containing it.
- **ROUGE-L** uses longest-common-subsequence F1, so it rewards word order.

Measured on hand-checked pairs: prediction `"8:00"` against gold `"08:00"` scores EM 0.00
and F1 1.00 (the colon splits the token, but the token sets differ), while
`"The library opens at 08:00."` scores EM 0.00 and F1 0.71. **EM punishes verbosity, which
is why refusal-rate and length must be reported alongside it.**

### 3.3 Retrieval metrics

$$
\text{Recall@}k=\frac{|\text{rel}\cap\text{top}_k|}{|\text{rel}|},\quad
\text{MRR}=\frac1{|Q|}\sum_q\frac{1}{\text{rank}_q},\quad
\text{nDCG@}k=\frac{\text{DCG@}k}{\text{IDCG@}k}.
$$

Report at least recall@k and MRR. Precision@k caps at $1/k$ when one document is relevant, so
it is uninformative without stating the number of relevant documents.

### 3.4 Hallucination

Three complementary checks, all cheap:

1. **Refusal behaviour** on questions the corpus cannot answer — measured refusal rate 0.00
   in this module, i.e. the model never said "I don't know".
2. **Grounding / support rate** — the share of answer content words present in the retrieved
   context. 1.00 is not proof of correctness (a wrong span is still grounded), but a low
   score is a strong warning.
3. **Unsupported numbers** — numbers in the answer that do not appear in the context. One of
   eight unanswerable answers contained such a number.

A production stack adds: entailment scoring by a second model, citation verification, and
human review of sampled traffic.

### 3.5 Response quality and LLM-as-judge

Rubric judging (1–5 on relevance, completeness, faithfulness, tone) scales better than human
review, but the judge must be validated. Agreement measured here between a judge and ten human
labels: **80% agreement, Cohen's κ = 0.600** for one judge and **60%, κ = 0.200** for another.
The second judge looks acceptable by raw agreement and is barely better than chance once base
rates are accounted for — which is why κ (or another chance-corrected statistic) is mandatory.

Rules for LLM judges: fix the rubric, use a reference answer where possible, randomise order,
report κ against a human-labelled subset, and never let the judge see the system you are
comparing.

### 3.6 Cost and latency

Latency is a distribution, not a mean: measured on eight requests, mean 0.802 s, p50 0.55 s,
p95 2.10 s. The tail is what users complain about. Cost arithmetic:

$$
\text{cost per 1000}=\frac{(\text{prompt tokens}\cdot p_{\text{in}}+
\text{completion tokens}\cdot p_{\text{out}})}{10^6}\times1000 .
$$

At 10 prompt and 2 completion tokens per query with prices 0.50/1.50 USD per million, that is
**8.00 USD per 1,000 queries**; at 0.15/0.60 prices, **2.70 USD**. The formula matters more
than the price list, which changes.

### 3.7 Safety and red-teaming

Evaluate refusals on harmful requests, leakage of the system prompt, prompt injection (L11-04),
PII in outputs, and over-refusal on benign questions. Over-refusal is a quality metric too: a
system that refuses everything scores 0% on harmful compliance and is useless.

### 3.8 Sample size

With $n=12$ questions, a proportion near 0.67 has a 95% interval of roughly ±0.28. With
$n=200$, about ±0.065. Most "improvements" reported in blog posts are inside the noise floor
of their own evaluation set. State $n$, the interval, and the exact question set.

## 4. The Procedure: An Evaluation Harness

1. Freeze a question set: answerable, multi-document, unanswerable, plus slices (short/long,
   numeric/date/prose).
2. Run the system once, log every prompt, context, answer, latency and token count.
3. Score retrieval, answer and grounding separately.
4. Compute refusal rates on each slice.
5. Validate any LLM judge against 30+ human labels with κ.
6. Report latency percentiles and cost per 1,000 queries.
7. Keep the harness in the repository and run it before every prompt or index change.

## 5. Worked Examples

### Example 1 — reading the module's own results

| Measure | Value | What it means |
| :--- | ---: | :--- |
| Retrieval recall@1 (hybrid) | 1.00 | the right document is first for all 30 questions |
| End-to-end EM (12 questions) | 0.75 | nine of twelve answers match exactly |
| Token F1 | 0.85 | partial credit is high; wrong answers are close but wrong |
| Grounding score | 1.00 | every content word appears in the context |
| Refusal rate on unanswerable | 0.00 | the system never declines |
| p95 latency | ~2.1 s | tail dominated by retrieval and generation |

The pattern — perfect retrieval, perfect grounding, zero refusals — is the signature of a
system that answers from *something* rather than from *the right thing*. Grounding alone does
not detect it; only the unanswerable slice does.

### Example 2 — why κ matters

Judge A: 8/10 agreement, κ = 0.600 — moderate. Judge B: 6/10 agreement, κ = 0.200 — the
labels carry almost no information beyond chance. If you had reported only agreement, Judge B
would look "60% as good as a human" and you would ship it.

### Example 3 — cost at scale

100,000 queries/day, 900 prompt tokens (RAG context) and 60 completion tokens, at
0.50/1.50 USD per million: $100{,}000\times(900\times0.5+60\times1.5)/10^6=100{,}000\times
0.00054=54$ USD/day. Halving the retrieved context to 450 tokens drops it to 36 USD/day — a
33% saving for a change you can measure against recall.

## 6. Mathematical Formulation

All metrics above. Two additions used in reporting:

$$
\text{95\% CI for a proportion}\approx\hat p\pm1.96\sqrt{\frac{\hat p(1-\hat p)}{n}},
\qquad
\kappa=\frac{p_o-p_e}{1-p_e}.
$$

## 7. Python Implementation

```python
# run from modules/M11-generative-ai-and-large-language-models/code
from llm_eval import (answer_report, retrieval_report, support_rate, unsupported_numbers,
                      is_refusal, refusal_rate, cohen_kappa, latency_report)
from gen_data import QA, UNANSWERABLE

print(answer_report([("08:00", "08:00"), ("8:00", "08:00"), ("I don't know", "08:00")]))
print(retrieval_report([(["hb-01", "hb-03"], ["hb-01"]), (["hb-03", "hb-01"], ["hb-01"])]))
ctx = "The library opens at 08:00 and closes at 23:00."
print(support_rate("The library opens at 07:00.", ctx),
      unsupported_numbers("The library opens at 07:00.", ctx))
print(cohen_kappa([1,1,0,0,1,0,1,1,0,0], [1,1,0,0,1,0,0,1,0,1]))
print(latency_report([0.42, 0.51, 0.47, 1.30, 0.55, 0.49, 2.10, 0.58]))
```

```text
{'n': 3, 'exact_match': 0.333, 'token_f1': 0.667, 'rouge_l': 0.667}
{'recall@1': 0.5, 'precision@1': 0.5, 'ndcg@1': 0.5, 'recall@3': 1.0, ...}
0.2 ['07']
0.6
{'n': 8, 'mean_s': 0.802, 'p50_s': 0.55, 'p95_s': 2.1, 'max_s': 2.1}
```

## 8. Practical Applications

- **Release gates** — block a deploy if recall@5 or refusal-on-unanswerable regresses.
- **A/B testing prompts** — same set, same metric, one change, with intervals.
- **Incident review** — slice logs by failure level to find whether retrieval or generation broke.
- **Procurement** — cost per 1,000 queries at your own token profile, not the vendor's example.

## 9. Common Mistakes

1. Reporting one end-to-end number with no stage breakdown.
2. Omitting the unanswerable slice, so hallucination is invisible.
3. Using raw agreement for an LLM judge.
4. Comparing systems on different question sets.
5. Quoting p50 latency while users experience p95.
6. Ignoring output length in cost, which is usually the smaller term in RAG.
7. Testing on the questions used to tune the prompt.

## 10. Practical Exercises

**Beginner**

1. Compute EM, F1 and ROUGE-L for five of your own answer pairs.
2. Compute the 95% interval for 0.75 at $n=12$ and $n=100$.

**Intermediate**

3. Build a 40-question set with 10 unanswerable items and measure your LAB-11-02 system's refusal rate.
4. Compute κ between two judges on 20 labelled answers.

**Advanced**

5. Add an entailment check using a second model and compare its hallucination flags with the number-support check.
6. Measure p50/p95 latency for dense, hybrid and reranked retrieval separately.
7. Design a release gate: which metrics, which thresholds, and what evidence justifies each threshold.

## 11. Self-Assessment

**Multiple choice**

1. A system with perfect grounding can still be wrong because
   a) grounding is unmeasurable. b) it may use a real but incorrect span. c) retrieval is exact. d) EM is broken.
2. κ is preferred over raw agreement because it
   a) is faster. b) corrects for chance. c) needs no labels. d) measures latency.
3. The most informative hallucination test is
   a) average answer length. b) refusal rate on unanswerable questions. c) p50 latency. d) token count.
4. Precision@3 with one relevant document cannot exceed
   a) 1.0. b) 0.333. c) 0.5. d) it is unbounded.

**Short answer**

5. Why must retrieval and generation be scored separately?
6. What makes an evaluation set "frozen", and why does it matter?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Different failures need different fixes; a retrieval miss cannot be fixed by prompting, and a wrong span cannot be fixed by better chunking.
6. Its questions, gold answers and gold sources are versioned and never tuned against, so improvements reflect the system, not familiarity with the test.

</details>

## 12. Key Terms

**Exact match**, **token F1**, **ROUGE-L**, **recall@k**, **MRR**, **nDCG**, **grounding score**,
**support rate**, **hallucination**, **refusal rate**, **LLM-as-judge**, **Cohen's κ**,
**percentile latency**, **cost per query**, **evaluation harness**, **slice**, **confidence
interval**.

## 13. Further Reading

- Raji et al. (2021). *AI and the Everything in the Whole Wide World Benchmark* — on what benchmarks measure.
- Zheng et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* — judge biases.
- Es et al. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*.
- Liang et al. (2023). *Holistic Evaluation of Language Models (HELM)*.

## What to Do Next

1. Run `python llm_eval.py`; then LAB-11-03.
2. Build your own 40-question evaluation set for the mini-project.
3. Read the [module summary](../summary.md) before the quiz.

---

**Navigation:** [← Previous: L11-06](L11-06-fine-tuning-and-parameter-efficient-adaptation.md) · [Module end](../README.md)
