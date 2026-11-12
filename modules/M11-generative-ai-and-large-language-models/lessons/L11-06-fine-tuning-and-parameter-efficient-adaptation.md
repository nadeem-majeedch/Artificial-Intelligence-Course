# L11-06 — Fine-Tuning and Parameter-Efficient Adaptation

[← Previous: ? Lesson](L11-05-retrieval-augmented-generation.md) · [Module home](../README.md) · [Next: ? Lesson →](L11-07-evaluating-llm-systems.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: A CPU Fine-Tuning Run](#4-the-procedure-a-cpu-fine-tuning-run)
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

> **Module M11** · Lesson 6 of 7 · ~90 minutes · Level 400
> **Prerequisites:** L11-03, M07 (training loops)

[Previous: L11-05](L11-05-retrieval-augmented-generation.md) · [Module overview](../README.md) · [Next: L11-07 →](L11-07-evaluating-llm-systems.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Decide** between prompting, RAG and fine-tuning for a stated failure.
2. **Implement** a LoRA layer and apply it to a pretrained transformer.
3. **Compute** the trainable-parameter budget for a given rank.
4. **Train** an adapter on CPU and report held-out loss before and after.
5. **Merge** an adapter into base weights and verify numerical equivalence.
6. **Explain** QLoRA and quantisation trade-offs with measured evidence.
7. **Evaluate** an adapter against its base model on a fixed set.

## 2. Prerequisite Knowledge

Backpropagation and optimisers (M07), the four-stage pipeline (L11-03), and prompt evaluation
discipline (L11-04).

## 3. Conceptual Explanation

### 3.1 First, decide whether to fine-tune at all

| Symptom | Right tool | Why |
| :--- | :--- | :--- |
| Missing or stale facts | RAG | weights are expensive to update; documents are not |
| Wrong tone, format, or verbosity | prompt, then SFT/LoRA | behaviour is learnable from a few hundred examples |
| Task-specific vocabulary | LoRA or RAG | both work; RAG is auditable |
| Needs a new capability (legal drafting) | more pretraining or a bigger model | adapters cannot add knowledge reliably |
| Too slow or too large | quantisation, distillation | adaptation does not help latency |

Fine-tuning is the most expensive and least reversible option. Try the two cheaper ones
first, and write down what you expect fine-tuning to fix.

### 3.2 Full fine-tuning versus adapters

Full fine-tuning updates $W\in\mathbb R^{d\times k}$ with gradients and keeps an optimizer
state for each parameter (Adam: two extra tensors, so ~12 bytes per parameter). For a 7B
model that is ~84 GB before activations. **LoRA** freezes $W$ and learns $BA$ with
$B\in\mathbb R^{r\times k}$, $A\in\mathbb R^{d\times r}$:

$$
W'=W+\frac{\alpha}{r}BA,\qquad \text{trainable}=r(d+k).
$$

$A$ is initialised randomly and $B$ at zero, so the model starts exactly at the base
behaviour — an important property: step 0 is a no-op, and any degradation is your data.

### 3.3 Measured parameter budget on distilgpt2

Twenty-four projections wrapped (`c_attn`, `c_proj`, `c_fc` in all six blocks):

| rank | trainable parameters | share of 82M | adapter size (fp32) |
| ---: | ---: | ---: | ---: |
| 4 | 294,912 | 0.359% | 1.2 MB |
| 8 | 589,824 | 0.715% | 2.4 MB |
| 16 | 1,179,648 | 1.420% | 4.7 MB |

The base model is 328 MB in fp32. An adapter is **2.4 MB for rank 8** — small enough to keep
one per customer, per task, or per language.

### 3.4 QLoRA

QLoRA stores the frozen base in 4-bit (NF4) and computes in bf16 through dequantisation on
the fly, with paged optimizers to survive memory spikes. Relative to full fine-tuning:

- weights: ~7× smaller;
- optimizer state: only for adapters, so ~1000× smaller;
- quality: close to 16-bit LoRA on most instruction tasks, but always re-measure.

Dynamic int8 quantisation of flan-t5-small measured in this module: **307.8 MB → 65.9 MB**
(4.7×), latency **0.159 s → 0.423 s** (worse, because these matmuls are tiny), exact match
**1.00 → 0.50** on four questions. Quantisation is not free, and small-model latency often
gets worse.

### 3.5 Training an adapter: what to watch

1. **Loss on response tokens only.** Mask the prompt with `-100`; otherwise you teach the
   model to write questions.
2. **Held-out loss.** Training loss falling is necessary, not sufficient.
3. **Learning rate.** Adapters tolerate 1e-4 to 1e-3; much higher and the adapter overfits
   the small dataset within a few dozen steps.
4. **Steps, not epochs.** With tiny data, an "epoch" is a handful of steps; report steps.
5. **A task metric.** Held-out loss is a proxy; exact match or human rating is the goal.

### 3.6 Catastrophic forgetting and the reference model

Adapting on a narrow dataset degrades unrelated behaviour. Mitigations: mix in a slice of
general data, keep the learning rate low, use few steps, and evaluate on a general benchmark
before and after. In preference optimisation the reference model plays this role explicitly;
in LoRA you are the one who must check.

### 3.7 Merging

At inference you can either keep the adapter separate (two matmuls, easy to swap) or merge
$BA$ into $W$ (one matmul, no runtime cost). Merging is exact up to floating-point error:
measured maximum logit difference **6.87e-05**, with the parameter count returning to
81,912,576 and zero trainable parameters. Keep the unmerged adapter for reproducibility; ship
the merged weights for speed.

## 4. The Procedure: A CPU Fine-Tuning Run

1. Collect 30–500 examples of the exact input/output format you need.
2. Hold out 15% and never train on it.
3. Freeze the base; wrap 3–5 projection types with LoRA ($r=8$, $\alpha=16$).
4. Tokenise with the base model's own tokeniser; mask prompt tokens in the labels.
5. Train with AdamW at 1e-3 for tens of steps, checking held-out loss every 10.
6. Evaluate: held-out loss, task metric, and a general-capability sanity check.
7. Merge, save, and record the base model, licence, data provenance and hyperparameters.

## 5. Worked Examples

### Example 1 — the measured run

Forty steps, batch 2, learning rate 1e-3, rank 8, on 34 handbook question/answer pairs:

```text
trainable parameters  : 589,824 (0.715% of 82,502,400)
held-out loss         : base 4.956 -> before 4.956 -> after 3.005
training loss         : first 4.477  first-5 mean 4.445  last-5 mean 1.874
wall clock            : 12.4 s training, 18.4 s total
```

The held-out loss fell by 39%, and trainable parameters were under 1% of the model. The
adapter is 2.4 MB against a 328 MB base: a 137× reduction in what you must store per task.

### Example 2 — what changed in the output

```text
prompt: Question: What is the accommodation deposit?
  base  -> 'Answer: The deposit is a deposit of money in the form of a'
  LoRA  -> 'Answer: 15 GBP per year for a student accommodation accommodation accommodation'
```

The adapter learned the answer *format* and the domain's shape, then hallucinated a figure and
degenerated into repetition — 40 steps on 34 examples is nowhere near enough to teach facts.
This is the single most important observation in the lesson: **fine-tuning teaches form;
retrieval supplies facts.**

### Example 3 — budget arithmetic

For a 7B model with $d=k=4096$, rank 16, on all query/key/value/output projections of 32
layers: trainable $=4\times32\times16\times(4096+4096)\approx16.8\text{M}$ — 0.24% of the
model. In fp32 that is 67 MB of adapter, versus 28 GB of weights and 56 GB of Adam state for
full fine-tuning.

## 6. Mathematical Formulation

LoRA update and parameter count above; the training objective is cross-entropy on response
tokens:

$$
\mathcal L=-\sum_{t\in\text{response}}\log\pi_{\theta+\Delta\theta}(y_t\mid x,y_{<t}),
\qquad \Delta\theta=\{A,B\}.
$$

Merging computes $W\leftarrow W+\frac{\alpha}{r}BA$ exactly; since both are linear, the
merged model computes the same function as the unmerged one, up to float error.

## 7. Python Implementation

```python
# run from modules/M11-generative-ai-and-large-language-models/code
from lora import train_lora, merge_lora, qa_pairs

res = train_lora(steps=40, r=8)
print(res["layers_replaced"], res["trainable"], round(res["trainable_pct"], 3))
print(round(res["before_loss"], 3), "->", round(res["after_loss"], 3))
print(len(qa_pairs(40)), "examples,", round(res["seconds"], 1), "s")

merged = merge_lora(res["model"])
print("merged layers", merged,
      "trainable now", sum(p.numel() for p in res["model"].parameters() if p.requires_grad))
```

```text
24 589824 0.715
4.956 -> 3.005
40 examples, 12.4 s
merged layers 24 trainable now 0
```

The full script also verifies that merged and unmerged logits agree (`6.87e-05` maximum
difference) and that `YAML`-free JSON metadata is saved alongside the adapter.

## 8. Practical Applications

- **Per-tenant style adapters** — small, swappable, auditable.
- **Domain jargon** — legal, medical, internal product names; pair with RAG for facts.
- **Low-resource languages** — adapters on a multilingual base.
- **Edge deployment** — merged adapter plus int8 quantisation, with measured latency.

## 9. Common Mistakes

1. Fine-tuning to add facts that retrieval could supply.
2. Training on prompt tokens.
3. Reporting training loss instead of held-out loss and a task metric.
4. Choosing a learning rate for full fine-tuning (too high for adapters on small data).
5. Evaluating on the training set, then being surprised in production.
6. Forgetting the base model's licence and the data's licence.
7. Merging without verifying outputs, then debugging a "different model".

## 10. Practical Exercises

**Beginner**

1. Reproduce the rank table; compute the adapter size for rank 32 by hand and check it.
2. Run the 40-step adapter and record held-out loss at steps 0, 10, 20, 40.

**Intermediate**

3. Train with 10, 20 and 40 examples; plot held-out loss against dataset size.
4. Apply LoRA only to `c_attn` and compare held-out loss with the all-projection run.
5. Merge and compare 20 generated outputs before and after merging; report any differences.

**Advanced**

6. Add a general-domain held-out set (e.g. three handbook documents from a different section) and measure forgetting.
7. Implement 4-bit quantised base weights with adapters and compare memory and quality.
8. Write an adapter card: base model, licence, data provenance, steps, rank, metrics, known failure modes.

## 11. Self-Assessment

**Multiple choice**

1. LoRA trains
   a) all weights. b) two low-rank matrices per wrapped projection. c) only the embeddings. d) the tokeniser.
2. The B matrix is initialised to zero so that
   a) training is faster. b) the model starts at base behaviour. c) gradients vanish. d) merging is impossible.
3. QLoRA quantises
   a) the adapters. b) the frozen base weights. c) the activations only. d) the dataset.
4. Merging an adapter
   a) changes the function. b) preserves it up to float error. c) doubles parameters. d) requires retraining.

**Short answer**

5. Why must prompt tokens be masked out of the loss?
6. Why is held-out loss not enough to ship an adapter?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Otherwise the model is trained to generate the prompt, which teaches question-writing and wastes capacity.
6. It measures next-token fit, not task success; an adapter can lower loss while producing degenerate or incorrect answers, as the deposit example shows.

</details>

## 12. Key Terms

**Fine-tuning**, **adapter**, **LoRA**, **rank**, **alpha**, **QLoRA**, **NF4**, **quantisation**,
**catastrophic forgetting**, **reference model**, **merge**, **trainable parameters**,
**adapter card**, **held-out loss**.

## 13. Further Reading

- Hu et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*.
- Dettmers et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*.
- Houlsby et al. (2019). *Parameter-Efficient Transfer Learning for NLP*.
- Biderman et al. (2024). *LoRA Learns Less and Forgets Less* — the forgetting trade-off.

## What to Do Next

1. Run `python lora.py`; keep the held-out numbers.
2. Do exercises 1–3, then LAB-11-03.
3. Continue to [L11-07 — Evaluating LLM Systems](L11-07-evaluating-llm-systems.md).

---

**Navigation:** [← Previous: ? Lesson](L11-05-retrieval-augmented-generation.md) · [Module home](../README.md) · [Next: ? Lesson →](L11-07-evaluating-llm-systems.md)
