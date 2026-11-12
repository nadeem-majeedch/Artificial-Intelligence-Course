# L11-02 — Inside a Large Language Model: Tokens, Attention, Next-Token Prediction

[← Previous: ? Lesson](L11-01-the-generative-modelling-landscape.md) · [Module home](../README.md) · [Next: ? Lesson →](L11-03-pretraining-instruction-tuning-and-alignment.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: From Text to a Predicted Token](#4-the-procedure-from-text-to-a-predicted-token)
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

> **Module M11** · Lesson 2 of 7 · ~90 minutes · Level 400
> **Prerequisites:** L11-01, M07 (attention)

[Previous: L11-01](L11-01-the-generative-modelling-landscape.md) · [Module overview](../README.md) · [Next: L11-03 →](L11-03-pretraining-instruction-tuning-and-alignment.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** sequence modelling as next-token prediction and write the training loss.
2. **Derive** scaled dot-product attention and compute a head by hand.
3. **Describe** self-attention, causal masking and multi-head attention.
4. **Justify** the $\sqrt{d_k}$ scaling with a measured saturation experiment.
5. **Explain** positional encoding, and why attention alone is order-blind.
6. **Compare** encoder, decoder and encoder–decoder stacks.
7. **Trace** a sentence through tokenisation, embeddings, attention and a next-token distribution.
8. **Do** context-window arithmetic and predict where truncation will bite.

## 2. Prerequisite Knowledge

Matrix multiplication, softmax, and the transformer block from M07/L07-07. This lesson
repeats the mechanics only where a measurement adds something the previous lesson could not
show.

## 3. Conceptual Explanation

### 3.1 Sequence modelling

A language model assigns a probability to every sequence:

$$
p(x_{1:T})=\prod_{t=1}^{T}p_\theta(x_t\mid x_{<t}).
$$

Training minimises the mean negative log-likelihood over all positions at once:

$$
\mathcal L(\theta)=-\frac1T\sum_{t=1}^{T}\log p_\theta(x_t\mid x_{<t}).
$$

Every position is a training example — a 500-token document yields 500 prediction problems
from one forward pass. That is why pretraining scales: the supervision is free.

### 3.2 Why attention

A recurrent model squeezes the past into one vector; the further back the information, the
more it degrades. Attention lets position $t$ read any earlier position directly:

$$
\text{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V .
$$

$Q$ rows are queries (what each position wants), $K$ rows are keys (what each position
offers), $V$ rows are values (what is actually passed on). $M$ is an additive mask:
$-\infty$ where attention is forbidden.

### 3.3 The $\sqrt{d_k}$ divisor, measured

Dot products of $d_k$-dimensional random vectors have variance proportional to $d_k$, so
unscaled logits grow with width and the softmax saturates. Measured over 10 random keys:

| $d_k$ | raw logit range | raw max weight | scaled max weight | raw entropy | scaled entropy | max entropy |
| ---: | :--- | ---: | ---: | ---: | ---: | ---: |
| 4 | −1.14 … 0.82 | 0.2049 | 0.1497 | 2.1344 | 2.2557 | 2.3026 |
| 16 | −8.40 … 5.22 | 0.7853 | 0.2690 | 0.8048 | 2.0389 | 2.3026 |
| 64 | −11.63 … 8.70 | 0.9297 | 0.3075 | 0.2608 | 1.9633 | 2.3026 |
| 256 | −14.22 … 45.73 | 1.0000 | 0.5815 | 0.0000 | 1.5017 | 2.3026 |

At $d_k=256$ the unscaled softmax puts all mass on one key and its gradient is
effectively zero; the scaled version still has entropy 1.50 nats. This is not a cosmetic
detail — without the divisor, deep attention layers stop learning.

### 3.4 Self-attention, causal masks and multi-head attention

**Self-attention** is attention where $Q,K,V$ all come from the same sequence. For a decoder
you also need a **causal mask**: position $t$ may only attend to positions $\le t$.
With four tokens the weight matrix is lower-triangular, and row 0 has a single 1.0 —
verified by `causal_mask(4)` in `attention_lab.py`.

**Multi-head attention** runs $h$ attention operations on projected subspaces and
concatenates:

$$
\text{MHA}(X)=\mathrm{Concat}(\text{head}_1,\dots,\text{head}_h)W_O .
$$

Measured on a 6-token, 12-dimensional input with 3 heads: head entropies 1.621, 1.572 and
1.650 nats, mean maximum weight 0.486, 0.520 and 0.531 — different heads, different
distributions, which is the point.

**Padding masks** are the other half of the story: batched sequences are padded, and padded
keys must receive zero weight. The test in `attention_lab.py` confirms it exactly
(`allclose(w[1,2:], 0.0)` is true).

### 3.5 Positional encoding

Attention is permutation-equivariant: shuffle the input and every output shuffles with it.
Order must be injected. Sinusoidal encodings use

$$
PE_{(pos,2i)}=\sin\!\left(pos/10000^{2i/d}\right),\qquad
PE_{(pos,2i+1)}=\cos\!\left(pos/10000^{2i/d}\right).
$$

For $d=16$ the adjacent-position dot product is 7.5 for every neighbouring pair — a smooth,
slowly changing code. Learned position embeddings are the alternative and are what GPT-2
uses.

### 3.6 Encoder, decoder, encoder–decoder

| Configuration | Masking | Cross-attention | Example use |
| :--- | :--- | :--- | :--- |
| Encoder only | bidirectional | none | classification, sentence embeddings |
| Decoder only | causal | none | GPT-style generation, this module's distilgpt2 |
| Encoder–decoder | causal decoder | yes | translation, T5 question answering |

A decoder-only model is an encoder with the mask switched on, trained on the same objective;
that economy is why the architecture won.

### 3.7 Tokenisation

Text becomes integers before any network sees it.

- **Word-level**: unbounded vocabulary, no way to handle a novel word.
- **Character-level**: tiny vocabulary, very long sequences.
- **Subword (BPE)**: frequent strings become one token, rare words split into pieces.

BPE learns merges greedily. On this module's handbook, 18 merges on a 37-symbol alphabet
produced 55 symbols and split words as `library -> l | i | b | r | ar | y</w>` and
`mitigating -> m | i | ti | g | a | t | in | g | </w>`. Real tokenisers do this 50,000
times and keep the merges.

**Measured with the GPT-2 tokenizer.** The sentence

> Northfield University charges 9,250 GBP for undergraduate tuition.

is 66 characters, 8 words, 66 UTF-8 bytes and **13 tokens** (5.08 characters per token,
0.62 words per token):

```text
['North', 'field', ' University', ' charges', ' 9', ',', '250', ' GB', 'P', ' for',
 ' undergraduate', ' tuition', '.']
```

Notice that a leading space is part of the token, that `9,250` splits into three tokens, and
that `GBP` splits into `GB` + `P`. Across the whole corpus: 2,281 tokens for 1,895 words
(**1.204 tokens per word**), 5.089 characters per token, 871 distinct token ids used, and the
longest document is 111 tokens. The uppercase probe is instructive: `hello` is one token,
`Hello` is one, `HELLO` is three (`HE`,`LL`,`O`). Numeric probes: `1234` → 2 tokens,
`1234567890` → 4, `2026-11-11` → 6, `don't` → 2, `cafe` → 2.

### 3.8 Embeddings

Token ids index an embedding matrix $E\in\mathbb R^{V\times d}$. GPT-2 small has
$V=50{,}257$ and $d=768$, so the embedding table alone is 38.6M parameters of the model's
82M. Embeddings are learned, not looked up from a dictionary — "library" and "libraries"
end up close because they predict similar continuations, not because a linguist said so.

### 3.9 The context window

The window is a hard limit on `prompt + output`. With a 1,024-token window, a 300-token
prompt and 200 reserved output tokens, 524 tokens remain for retrieved context. With a
900-token prompt the same arithmetic gives **−76**: the request does not fit at all. This is
the calculation a RAG system must perform *before* it calls the model, not after.

Chunking interacts with it: an 88-token document chunked at 120 tokens yields one chunk; at
60 tokens with 10-token overlap it yields two chunks of 60 and 38 tokens.

### 3.10 Next-token prediction in practice

For the prompt `"The library opens at"` the model's top five continuations were:

| token | probability |
| :--- | ---: |
| ` the` | 0.1565 |
| ` 10` | 0.0536 |
| ` 7` | 0.0510 |
| ` 6` | 0.0484 |
| ` 9` | 0.0421 |

Top-5 mass: 0.3516. For `"The capital of France is"` the mass is 0.3348 and the top token is
` the` (0.1177), not "Paris" — a small model trained on web text has no reliable factual
head. **The distribution is broad, and everything in L11-04 about decoding is a policy for
choosing from it.**

## 4. The Procedure: From Text to a Predicted Token

1. Normalise text (whitespace, unicode) — tokeniser-specific.
2. Tokenise to ids; check the length against the window.
3. Embed ids and add positional information.
4. Apply $L$ transformer blocks: layer norm → attention → residual → layer norm →
   feedforward → residual.
5. Project the final hidden state to vocabulary logits.
6. Softmax (with temperature) → a distribution over the next token.
7. Choose a token (greedy, top-k, nucleus), append, repeat.

## 5. Worked Examples

### Example 1 — one attention head by hand

$Q=(1,0)$, $K=I_2$, $V=\begin{bmatrix}10&0\\0&20\end{bmatrix}$, $d_k=2$.

Scores $QK^\top=(1,0)$; scaled by $\sqrt2$: $(0.7071,0)$; softmax: $e^{0.7071}=2.028$,
$e^0=1$, total 3.028 → weights $(0.670,0.330)$; output
$0.670(10,0)+0.330(0,20)=(6.70,6.60)$. Softmax never returns a one-hot vector, and that
softness is what makes the operation differentiable.

### Example 2 — a real 13-token sentence

`"The library opens at eight and closes at eleven on weekdays."` tokenises to 13 tokens:
`['The',' library',' opens',' at',' eight',' and',' closes',' at',' eleven',' on',' week','days','.']`.
distilgpt2's attention, layer by layer (12 heads), measured here:

| layer | mean entropy (nats) | max possible (ln 13) | mass on self | mean \|i−j\| |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1.180 | 2.565 | 0.386 | 2.618 |
| 1 | 1.117 | 2.565 | 0.163 | 3.324 |
| 2 | 0.859 | 2.565 | 0.166 | 3.668 |
| 3 | 0.744 | 2.565 | 0.116 | 4.739 |
| 4 | 0.644 | 2.565 | 0.110 | 5.202 |
| 5 | 0.774 | 2.565 | 0.132 | 4.975 |

Two real trends: attention sharpens with depth (entropy falls from 1.18 to 0.64 before
rising slightly), and the effective look-back distance grows (2.6 → 5.2 tokens), so deeper
layers integrate more context. Layer 0's head entropies `[1.529, 0.179, 1.514, 0.356, ...]`
show that some heads are almost one-hot while others are nearly uniform — heads specialise.

### Example 3 — the cost of attention

For $n$ tokens, $h$ heads and head width $d_k$, the score tensor is $h\times n\times n$.
At $n=512$, $h=8$: 2.1M entries per layer. At $n=4{,}096$: 134M. That is why the context
window is a product decision with a price.

## 6. Mathematical Formulation

Scaled dot-product attention, multi-head projection, sinusoidal encoding and the
cross-entropy objective are given in §3.2–3.7. Parameter counts for one block of width $d$
and feedforward width $4d$: attention projections $4d^2$, feedforward $8d^2$, layer norms
$4d$, total $\approx 12d^2$ per block. GPT-2 small ($d=768$, 12 blocks) is therefore about
85M parameters before embeddings — the same order as its published 82M after weight tying.

## 7. Python Implementation

```python
# run from modules/M11-generative-ai-and-large-language-models/code
from tokenizers_lab import compare_granularities, token_report, context_budget
from attention_lab import attention_profile, next_token_report
from gen_data import HANDBOOK

s = "Northfield University charges 9,250 GBP for undergraduate tuition."
g = compare_granularities(s)
print({k: g[k] for k in ("characters", "words", "subword_tokens", "chars_per_token")})
print(g["subword_pieces"])

profile = attention_profile("The library opens at eight and closes at eleven on weekdays.")
for layer in profile["layers"]:
    print(layer["layer"], round(layer["mean_entropy"], 3), round(layer["mean_distance"], 3))

print(context_budget(900, 1024, 200))
print(next_token_report("The library opens at"))
```

```text
{'characters': 66, 'words': 8, 'subword_tokens': 13, 'chars_per_token': 5.076923076923077}
['North', 'field', ' University', ' charges', ' 9', ',', '250', ' GB', 'P', ' for',
 ' undergraduate', ' tuition', '.']
0 1.18 2.618
1 1.117 3.324
2 0.859 3.668
3 0.744 4.739
4 0.644 5.202
5 0.774 4.975
{'window': 1024, 'prompt': 900, 'reserved_output': 200,
 'available_for_context': 0, 'overflow': 76}
```

## 8. Practical Applications

- **Prompt budgeting.** Count tokens before you send; truncation is silent at the API boundary.
- **Cost estimation.** Price is per token, so tokeniser choice changes the bill. `GBP` costing two tokens is a real cost multiplier on a corpus of currency amounts.
- **Chunking.** Chunk in tokens, not characters, or your overlap will not mean what you think.
- **Model selection.** Window size and vocabulary are architectural facts, not settings.

## 9. Common Mistakes

1. Counting words when the limit is tokens (1.204 tokens per word here, worse for code and non-English text).
2. Forgetting reserved output tokens when computing available context.
3. Assuming attention weights are explanations; they show where mass went, not why.
4. Training without the $\sqrt{d_k}$ divisor and blaming the optimiser.
5. Omitting the causal mask and leaking the answer into the input during training.
6. Padding batches without a padding mask, then wondering why short sequences behave oddly.
7. Treating the tokeniser as fixed across models; every model has its own vocabulary.

## 10. Practical Exercises

**Beginner**

1. Tokenise five sentences of your own and compute characters per token. Compare with 5.09.
2. Compute the available context for window 2,048, prompt 1,800 and 300 reserved output tokens.

**Intermediate**

3. Implement `causal_mask` and verify that row $t$ has exactly $t+1$ non-zero entries.
4. Measure attention entropy for a 40-token sentence and compare it with the 13-token result at layer 5.
5. Change `maxsim`-style pooling to mean pooling over heads and re-measure entropy.

**Advanced**

6. Train a 2-layer character-level transformer on the handbook and compare its perplexity per character with distilgpt2's 59.26 per token.
7. Show numerically that removing the $\sqrt{d_k}$ divisor increases gradient magnitude variance across layers.
8. Implement sliding-window attention and measure the memory saved at $n=1{,}024$.

## 11. Self-Assessment

**Multiple choice**

1. The next-token training loss is
   a) MSE. b) cross-entropy over the vocabulary. c) KL to a uniform distribution. d) adversarial.
2. The causal mask prevents
   a) padding. b) attending to future tokens. c) gradient flow. d) tokenisation errors.
3. Multi-head attention is used because
   a) it is cheaper. b) heads can capture different relations. c) it removes positions. d) it avoids softmax.
4. With a 1,024-token window, 900-token prompt and 200 reserved output tokens, you have
   a) 124 tokens spare. b) 0 available and 76 over. c) 200 tokens. d) no limit.

**Short answer**

5. Why does a tokeniser make `9,250` cost three tokens, and why does that matter commercially?
6. Give one measured reason a decoder-only model can serve as an encoder.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. BPE merges frequent strings; `9`, `,` and `250` are separately frequent, so they stay separate. Tokens are the billing and context unit, so numeric-heavy text costs more.
6. A decoder-only model is an encoder with a causal mask; masking is a choice, and with the mask removed the same weights produce bidirectional representations.

</details>

## 12. Key Terms

**Sequence model**, **next-token prediction**, **scaled dot-product attention**, **query/key/value**,
**self-attention**, **causal mask**, **padding mask**, **multi-head attention**, **positional
encoding**, **encoder**, **decoder**, **encoder–decoder**, **cross-attention**, **BPE**,
**vocabulary**, **embedding**, **context window**, **logits**, **teacher forcing**.

## 13. Further Reading

- Vaswani et al. (2017). *Attention Is All You Need*.
- Radford et al. (2019). *Language Models are Unsupervised Multitask Learners* (GPT-2).
- Sennrich, Haddow & Birch (2016). *Neural Machine Translation of Rare Words with Subword Units*.
- Phuong & Hutter (2022). *Formal Algorithms for Transformers* — the best short reference for exact tensor shapes.

## What to Do Next

1. Run `python tokenizers_lab.py` and `python attention_lab.py`.
2. Do exercises 1–3.
3. Continue to [L11-03 — Pretraining, Instruction Tuning and Alignment](L11-03-pretraining-instruction-tuning-and-alignment.md).

---

**Navigation:** [← Previous: ? Lesson](L11-01-the-generative-modelling-landscape.md) · [Module home](../README.md) · [Next: ? Lesson →](L11-03-pretraining-instruction-tuning-and-alignment.md)
