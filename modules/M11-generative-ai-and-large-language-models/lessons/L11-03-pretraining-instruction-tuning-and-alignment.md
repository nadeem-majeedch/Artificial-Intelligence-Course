# L11-03 — Pretraining, Instruction Tuning and Preference Alignment

[← Previous: L11-02](L11-02-inside-a-large-language-model.md) · [Module home](../README.md) · [Next: L11-04 →](L11-04-prompt-engineering-and-in-context-learning.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Choosing a Stage](#4-the-procedure-choosing-a-stage)
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

> **Module M11** · Lesson 3 of 7 · ~90 minutes · Level 400
> **Prerequisites:** L11-02, M07 (training)

[Previous: L11-02](L11-02-inside-a-large-language-model.md) · [Module overview](../README.md) · [Next: L11-04 →](L11-04-prompt-engineering-and-in-context-learning.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Distinguish** pretraining, supervised fine-tuning, preference optimisation and inference — what each changes and what it costs.
2. **Explain** the pretraining objective, data pipeline and scaling behaviour.
3. **Describe** instruction tuning and why a base model cannot follow instructions.
4. **Contrast** RLHF with DPO and state what each optimises.
5. **Explain** LoRA, QLoRA and quantisation, and choose between them under a hardware budget.
6. **Measure** the size, latency and quality cost of int8 quantisation.
7. **Explain** hallucination and context limits as consequences of the training objective, not bugs.

## 2. Prerequisite Knowledge

Cross-entropy, gradient descent, and the attention stack from L11-02. No new mathematics
beyond one preference loss; the difficulty here is keeping four stages of a pipeline
conceptually separate.

## 3. Conceptual Explanation

### 3.1 The four stages, kept separate

| Stage | Objective | Data | What changes | Typical cost |
| :--- | :--- | :--- | :--- | :--- |
| Pretraining | next-token cross-entropy | trillions of tokens of raw text | all weights; world knowledge, grammar, style | millions of GPU-hours |
| Supervised fine-tuning (SFT) | next-token cross-entropy on demonstrations | thousands to millions of prompt→response pairs | all weights (or adapters); behaviour | GPU-hours |
| Preference optimisation (RLHF/DPO) | maximise preference margin | tens of thousands of ranked pairs | weights; politeness, refusal, helpfulness | GPU-days |
| Inference | none | user prompt | nothing | per-token compute |

Most "the model got worse" reports come from confusing these stages: a behaviour change
after SFT is not a knowledge change, and a refusal after preference tuning is not a
capability regression.

### 3.2 Pretraining

The model reads text and predicts the next token, billions of times. Nothing is labelled;
every position supplies a target. What emerges is a compressed statistical model of language
that also encodes facts, because facts are useful for prediction.

Three practical facts:

- **The corpus is the ceiling.** A model cannot reliably know what it never saw; distilgpt2
  puts 0.0421 probability on ` 9` after "The library opens at" because it has seen clocks,
  not this handbook.
- **Data quality beats data quantity** past a point; deduplication and filtering are the
  highest-leverage steps in the pipeline.
- **Compute is the constraint.** Pretraining a 7B model on 2T tokens is roughly
  $6\times7\times10^9\times2\times10^{12}\approx8.4\times10^{22}$ FLOPs — thousands of
  GPU-months. This is why the module fine-tunes and retrieves instead.

### 3.3 Base models cannot follow instructions

A base model continues text. Prompt it with "Summarise this paragraph" and the most likely
continuation may be *another instruction*, because that is what the pretraining data looks
like. Instruction tuning fixes this by training on (instruction, response) pairs — the same
cross-entropy loss on a curated distribution. It teaches a **format**, not new knowledge.

### 3.4 Preference optimisation

Human raters rank two responses to the same prompt. RLHF fits a reward model to those
preferences, then optimises the policy against it with a KL penalty to the SFT model so it
does not drift into reward hacking:

$$
\max_\pi\;\mathbb E_{x,\,y\sim\pi}[r_\phi(x,y)]-\beta\,D_{\mathrm{KL}}\!\left(\pi\,\|\,\pi_{\text{SFT}}\right).
$$

**DPO** removes the separate reward model. With $\pi_\theta$ the policy, $\pi_{\text{ref}}$
the frozen reference, and $\sigma$ the logistic function, the loss on a preferred/rejected
pair $(y_w,y_l)$ is

$$
\mathcal L_{\text{DPO}}=-\log\sigma\!\left(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\text{ref}}(y_w\mid x)}
-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\text{ref}}(y_l\mid x)}\right).
$$

Both methods reward the preferred answer *relative to* the reference model. Both can make a
model confidently wrong in a more agreeable tone if the preference data rewards confidence
over accuracy — which is exactly the mechanism behind sycophancy.

### 3.5 LoRA and QLoRA

Full fine-tuning updates every weight and needs optimizer state for all of them. **LoRA**
freezes the base and learns a low-rank update $W'=W+\frac{\alpha}{r}BA$ on selected
projections, with $r\ll d$. Trainable parameters scale with $r$, not with the model:

| rank | layers wrapped | trainable parameters | share of model |
| ---: | ---: | ---: | ---: |
| 4 | 24 | 294,912 | 0.359% |
| 8 | 24 | 589,824 | 0.715% |
| 16 | 24 | 1,179,648 | 1.420% |

**QLoRA** quantises the frozen base to 4-bit and trains LoRA adapters in higher precision on
top. The base shrinks roughly 7× against fp32 while the adapters stay small — the standard
way to fine-tune a 7B model on a single consumer GPU.

### 3.6 Quantisation

Post-training quantisation stores weights in fewer bits. Dynamic int8 quantisation of
flan-t5-small, measured here:

| variant | size | mean latency (4 questions) | exact match |
| :--- | ---: | ---: | ---: |
| fp32 | 307.8 MB | 0.159 s | 1.00 |
| int8 dynamic | 65.9 MB | 0.423 s | 0.50 |

Two lessons, both uncomfortable. The size win is real (4.7×). The latency *loss* is real
too: for tiny models, dequantisation overhead outweighs the arithmetic saved. And quality
fell by half on a four-question set — small samples are noisy, but the direction is what
matters: **always re-run your evaluation after quantising.**

### 3.7 Inference

At inference the model does one forward pass per generated token. The **key/value cache**
stores past attention keys and values so they are not recomputed; without it, generating
$n$ tokens costs $O(n^2)$ attention work redundantly. Measured on this CPU for 24 tokens:
2.06 s without the cache versus 1.87 s with it (1.1×). The gap grows with output length and
shrinks for short generations, where per-step Python and matmul overhead dominates.

Compute per token is roughly $2N$ FLOPs for a model with $N$ parameters, so a 77M-parameter
model costs about 154 MFLOPs per token — trivial arithmetic, dominated in practice by memory
bandwidth.

### 3.8 Decoding parameters

The model produces logits; decoding turns them into text.

- **Temperature** $\tau$: $p\propto\exp(z/\tau)$. Low $\tau$ → deterministic; high → creative and incoherent.
- **Top-k**: keep the $k$ highest-probability tokens.
- **Top-p (nucleus)**: keep the smallest set whose cumulative probability reaches $p$.
- **Repetition penalty**: down-weight tokens already generated.

Measured on the prompt "The library opens at", 24 tokens, seed 0:

| strategy | mean entropy (nats) | distinct-2 | repetition rate | text |
| :--- | ---: | ---: | ---: | :--- |
| greedy | 0.000 | 0.30 | 0.20 | `' the end of the day.'` + blank lines |
| T = 0.7 | 0.685 | 0.22 | 0.00 | `' a new time.'` + blank lines |
| T = 1.0 | 3.630 | 1.00 | 0.17 | `' a button seven times a second...'` |
| T = 1.5 | 7.619 | 1.00 | 0.05 | `' a button seven times a second... is "tr'` |
| top-k 40 | 1.985 | 0.85 | 0.00 | `' a new time.'` … |
| top-p 0.9 | 0.766 | 0.17 | 0.00 | `' a button:'` + blank lines |
| top-p 0.9, T 1.2, rep 1.3 | 5.610 | 1.00 | 0.00 | `' a button seven times each second... is '` |

Greedy and low temperature collapse into newline spam, because the model's most probable
continuation after a time expression is a line break. The combination of nucleus sampling,
higher temperature and a repetition penalty produced the only varied, non-repetitive output.
**This is an empirical result about one small model; it is not a universal recipe.**

### 3.9 Hallucination and context limits

A language model optimises plausibility, not truth. With no context, flan-t5-small answered
"what is the daily overdue charge?" with `'$9.00'` and "how many items can an undergraduate
borrow?" with `'ten'` — fluent, confident, wrong. With the correct context in the prompt,
its exact match on 15 questions rose from **0.00 to 0.60** (token F1 0.03 → 0.78).

Context limits compound the problem: when the needed text is truncated the model does not
know it is missing, so it fills the gap. Grounding plus a refusal instruction is the
mitigation; measurement (L11-07) is how you know whether it worked.

## 4. The Procedure: Choosing a Stage

1. **Can a prompt plus retrieval answer it?** Try that first — it is reversible and cheap (L11-04, L11-05).
2. **Is the failure stylistic or behavioural?** SFT with a few hundred demonstrations, or LoRA on a CPU.
3. **Is the failure a matter of preference (tone, refusal, format)?** Preference optimisation, with ranked data you actually have.
4. **Is the failure knowledge?** Retrieval, not fine-tuning: facts change, and weights are expensive to update.
5. **Is it latency or memory?** Quantisation, smaller model, or a cached answer.

## 5. Worked Examples

### Example 1 — what SFT does and does not do

Fine-tuning distilgpt2 with LoRA for 40 steps on 34 handbook question/answer pairs dropped
held-out loss from **4.956 to 3.005** (trainable parameters 0.715%). A generation after
training begins `'Answer: 08:00 to 09:00 on weekdays'` — the *format* changed. It also
produced `'15 GBP per year for a student accommodation accommodation accommodation'`, which
is fluent-shaped but wrong: **SFT teaches shape, not facts.**

### Example 2 — the cost of a KL penalty

If the policy's log-probability ratio for a preferred answer is +0.8 and for the rejected
answer −0.4, the DPO margin is $0.8-(-0.4)=1.2$; with $\beta=0.1$ the scaled margin is 0.12
and the loss is $-\log\sigma(0.12)=0.686$. Training pushes the margin up, but the reference
term pins the model near its starting distribution, which is what stops it degrading into
one-word answers that always "win" the preference comparison.

### Example 3 — memory arithmetic for QLoRA

A 7B model in fp32 needs 28 GB for weights, plus ~112 GB of Adam state for full fine-tuning.
In 4-bit it needs ~3.5 GB, and LoRA with $r=16$ adds ~40 MB of trainable parameters plus
activations. That is the difference between a cluster and a laptop with a 8–12 GB GPU.

## 6. Mathematical Formulation

RLHF objective and DPO loss in §3.4; LoRA update $W'=W+\frac{\alpha}{r}BA$ in §3.5;
temperature scaling in §3.8. SFT is the same cross-entropy as pretraining, restricted to
response tokens:

$$
\mathcal L_{\text{SFT}}=-\sum_{(x,y)\in\mathcal D}\sum_{t}\log\pi_\theta(y_t\mid x,y_{<t}).
$$

Masking the prompt tokens out of the loss is a detail that materially changes behaviour: if
you train on the prompt too, the model learns to generate questions.

## 7. Python Implementation

```python
# run from modules/M11-generative-ai-and-large-language-models/code
from llm_gen import quantization_report, kv_cache_timing, sample_text, perplexity

qr = quantization_report()
print("fp32 ", round(qr["fp32"]["size_mb"], 1), "MB",
      round(qr["fp32"]["mean_latency_s"], 3), "s", qr["fp32"]["em"])
print("int8 ", round(qr["int8"]["size_mb"], 1), "MB",
      round(qr["int8"]["mean_latency_s"], 3), "s", qr["int8"]["em"])
print(kv_cache_timing("The Hartley Library is open from 08:00 to 23:00", 24))
print(perplexity("The wellbeing service offers free, confidential counselling."))
```

```text
fp32  307.8 MB 0.159 s 1.0
int8  65.9 MB 0.423 s 0.5
{'no_cache': 2.06, 'with_cache': 1.87, 'speedup': 1.1}
{'tokens': 16, 'nll_per_token': 4.19, 'perplexity': 66.1}
```

LoRA training is in `lora.py` (L11-06 walks through it). The important discipline is the
same in every stage: change one thing, evaluate on a fixed set, and report the baseline.

## 8. Practical Applications

- **Domain assistants** — SFT or LoRA on a few thousand examples, then retrieval for facts.
- **Tone and refusal behaviour** — preference tuning with genuinely ranked data.
- **Edge deployment** — quantisation plus a smaller model; measure latency on the target device, not on a server.
- **Cost control** — caching, shorter outputs, smaller models, batching; quantify tokens per request.

## 9. Common Mistakes

1. Fine-tuning to add facts that change monthly; retrieval is the right tool.
2. Training on prompt tokens and then wondering why the model emits questions.
3. Reporting training loss as evidence of quality; report held-out loss and a task metric.
4. Quantising and shipping without re-running evaluation.
5. Assuming the KV cache is always a large win; measure the actual generation length.
6. Treating RLHF as a truthfulness mechanism; it optimises what raters preferred.
7. Forgetting that adapters and base weights carry different licences.

## 10. Practical Exercises

**Beginner**

1. Reproduce the quantisation table. Explain why latency got worse while size got better.
2. Write down, for your own use case, which of the four stages you would use and why.

**Intermediate**

3. Run `sample_text` at temperatures 0.5, 0.9 and 1.2 with `top_p=0.95` and tabulate distinct-2 and repetition rate.
4. Measure KV-cache speedup at 8, 24 and 64 generated tokens. Where does the cache start to pay?

**Advanced**

5. Implement DPO's loss in NumPy for a single pair and verify the gradient sign pushes the preferred log-ratio up.
6. Quantise only the decoder layers and compare quality against quantising everything.
7. Estimate the FLOPs and wall-clock for pretraining a 124M model on 10B tokens on your hardware; compare with this module's 40-step LoRA run.

## 11. Self-Assessment

**Multiple choice**

1. Instruction tuning primarily changes
   a) world knowledge. b) response format and behaviour. c) the tokeniser. d) the context window.
2. DPO differs from RLHF by
   a) removing the reward model. b) removing the reference model. c) using no data. d) training from scratch.
3. LoRA with rank $r$ trains
   a) all weights. b) a low-rank update on selected projections. c) only embeddings. d) only the output head.
4. Dynamic int8 quantisation of a small model typically
   a) always speeds it up. b) shrinks it and may slow it down. c) improves accuracy. d) changes the tokeniser.

**Short answer**

5. Why can fine-tuning make a model *more* confidently wrong?
6. What does the KL term in RLHF protect against?

<details>
<summary>Answers</summary>

1. **b**. 2. **a**. 3. **b**. 4. **b**.
5. SFT and preference tuning reward fluent, assertive answers in the training distribution; if the data rewards confidence, the model learns confidence independent of correctness.
6. Drift away from the SFT policy into reward hacking — degenerate outputs that score well on the reward model but are useless to users.

</details>

## 12. Key Terms

**Pretraining**, **supervised fine-tuning**, **instruction tuning**, **preference optimisation**,
**RLHF**, **reward model**, **DPO**, **reference model**, **LoRA**, **QLoRA**, **quantisation**,
**int8**, **KV cache**, **temperature**, **top-k**, **top-p**, **hallucination**, **context limit**,
**sycophancy**.

## 13. Further Reading

- Ouyang et al. (2022). *Training Language Models to Follow Instructions with Human Feedback* (InstructGPT).
- Rafailov et al. (2023). *Direct Preference Optimization*.
- Hu et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*.
- Dettmers et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*.
- Bender et al. (2021). *On the Dangers of Stochastic Parrots* — the data-side critique.

## What to Do Next

1. Run the quantisation and KV-cache measurements yourself.
2. Do exercises 1–3.
3. Continue to [L11-04 — Prompt Engineering and In-Context Learning](L11-04-prompt-engineering-and-in-context-learning.md).

---

**Navigation:** [← Previous: L11-02](L11-02-inside-a-large-language-model.md) · [Module home](../README.md) · [Next: L11-04 →](L11-04-prompt-engineering-and-in-context-learning.md)
