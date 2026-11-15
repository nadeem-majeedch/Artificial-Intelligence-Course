# L07-07 — Attention Mechanisms and the Transformer

[← Previous: L07-06](L07-06-sequence-models-rnn-lstm-gru.md) · [Module home](../README.md) · [Next: L07-08 →](L07-08-transfer-learning-and-autoencoders.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Using a Transformer Classifier](#4-the-procedure-using-a-transformer-classifier)
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

> **Module M07** · Lesson 7 of 8 · ~90 minutes · Level 300
> **Prerequisites:** L07-06

[Previous: L07-06](L07-06-sequence-models-rnn-lstm-gru.md) · [Module overview](../README.md) · [Next: L07-08 →](L07-08-transfer-learning-and-autoencoders.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** attention as a soft, learned lookup, and derive scaled dot-product attention.
2. **Compute** one attention head by hand for a small example.
3. **Describe** multi-head attention and why several heads beat one.
4. **Explain** positional encoding, residual connections and layer normalisation in a transformer
   block.
5. **Distinguish** encoder, decoder and encoder–decoder configurations.
6. **Train** a tiny transformer classifier and compare it with an RNN baseline.
7. **State** attention's quadratic cost, its data appetite, and when not to use it.

## 2. Prerequisite Knowledge

Softmax, matrix multiplication, and the sequence-model vocabulary from L07-06. The scaled
dot-product formula is the only new mathematics.

## 3. Conceptual Explanation

### 3.1 The problem attention solves

A recurrent network compresses the entire past into one hidden vector. For a 40-word sentence, the
information about word 3 must survive 37 updates before it is needed. Attention removes that
bottleneck: every position can look directly at every other position, and the model learns *what*
to look at.

The mental model is a dictionary lookup. A query is compared with a set of keys; the best matches
retrieve their values. Attention makes the lookup soft: instead of retrieving one value, it
retrieves a weighted average of all values, with weights from the softmax of query–key similarity.

### 3.2 Scaled dot-product attention

$$
\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
$$

- $Q\in\mathbb{R}^{n\times d_k}$: one query per position.
- $K\in\mathbb{R}^{m\times d_k}$: keys for the positions being attended to.
- $V\in\mathbb{R}^{m\times d_v}$: their values.
- The output is $n\times d_v$: one weighted summary per query.

The $\sqrt{d_k}$ divisor matters: dot products of $d_k$-dimensional random vectors have variance
proportional to $d_k$, so without scaling the softmax saturates, gradients vanish, and training
stalls. Dividing by $\sqrt{d_k}$ keeps the logits at a sane scale.

**Causal masking** (for language generation) sets the upper triangle of $QK^\top$ to $-\infty$
before the softmax, so position $t$ cannot attend to positions after $t$.

### 3.3 Multi-head attention

One attention head can only express one weighted average. Multi-head attention runs $h$ heads in
parallel with different learned projections, then concatenates and projects:

$$
\text{MultiHead}(Q,K,V)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)W_O,
\qquad
\text{head}_i=\text{Attention}(QW_i^Q,KW_i^K,VW_i^V).
$$

Different heads learn different relations in practice: one tracks syntactic dependencies, another
coreference, another local adjacency. This is an empirical observation, not a guarantee, but the
diversity is the point.

### 3.4 Positional information

Attention is permutation-invariant: shuffling the input shuffles the output and changes nothing
else. Word order must therefore be injected explicitly, either with sinusoidal encodings

$$
PE_{(pos,2i)}=\sin\!\left(\frac{pos}{10000^{2i/d}}\right),
\qquad
PE_{(pos,2i+1)}=\cos\!\left(\frac{pos}{10000^{2i/d}}\right),
$$

or with learned position embeddings (as in this module's tiny model). Both work; learned embeddings
are simpler, sinusoids extrapolate a little better in principle.

### 3.5 The transformer block

```text
x → LayerNorm → Multi-Head Attention → + x  (residual)
  → LayerNorm → Feedforward (Linear → ReLU/GELU → Linear) → + x
```

Every sub-layer is wrapped in a residual connection and a layer norm. The feedforward block is
position-wise: the same two-layer MLP is applied independently at every position, which is where
most of the parameters live.

Two orderings exist: **post-norm** (original paper) and **pre-norm** (modern default, more stable
for deep stacks). PyTorch's `TransformerEncoderLayer` defaults to post-norm unless
`norm_first=True`.

### 3.6 Encoder, decoder, encoder–decoder

| Configuration | Attention | Typical use |
| :--- | :--- | :--- |
| Encoder only | bidirectional (no mask) | classification, embeddings (BERT) |
| Decoder only | causal mask | generation (GPT) |
| Encoder–decoder | encoder bidirectional + decoder causal + cross-attention | translation, summarisation (T5) |

Cross-attention lets the decoder query the encoder's output: $Q$ from the decoder, $K$ and $V$ from
the encoder.

### 3.7 Why it replaced recurrence

- **Parallelism over positions**: all queries are computed at once, so GPUs are fully used. An RNN
  cannot parallelise across time.
- **Short gradient paths**: any two positions are one attention step apart, so long-range
  dependencies are easier to learn.
- **Scaling laws**: performance improves predictably with data, parameters and compute.

The cost: attention is $O(n^2)$ in sequence length for both time and memory. A 4,096-token sequence
needs 16 million score entries per head. This is why long-context models use sparse, sliding-window
or linear attention variants.

### 3.8 Data appetite and limitations

A transformer has little built-in inductive bias: no locality prior, no recurrence. It therefore
needs more data (or pretraining) than a CNN or RNN to reach the same accuracy. On 1,500 synthetic
sentences it can still learn the task, but a similarly sized GRU often matches it — which is the
honest comparison to run in the lab.

## 4. The Procedure: Using a Transformer Classifier

1. Tokenise, build a vocabulary, encode to integer ids, pad to a fixed length.
2. Embed tokens and add positional information.
3. One or more encoder layers with multi-head self-attention.
4. Pool: take the first token's state (BERT-style) or mean-pool over non-padding positions.
5. Linear classification head; cross-entropy loss.
6. Mask padding in attention and in pooling.
7. Train with Adam at $10^{-4}$–$10^{-3}$ and warmup if the model is deep.
8. Compare with a GRU and with a bag-of-words baseline before claiming a transformer win.

## 5. Worked Examples

### Example 1 — One head by hand

$$
Q=\begin{bmatrix}1&0\end{bmatrix},\quad
K=\begin{bmatrix}1&0\\0&1\end{bmatrix},\quad
V=\begin{bmatrix}10&0\\0&20\end{bmatrix},\quad d_k=2.
$$

Scores: $QK^\top=(1,0)$. Scale by $\sqrt{2}$: $(0.707,0)$. Softmax:
$e^{0.707}=2.028$, $e^{0}=1$, total $3.028$, so weights $(0.670,0.330)$.

Output: $0.670(10,0)+0.330(0,20)=(6.70,6.60)$.

The query matched the first key, so the output is mostly the first value — but not entirely, because
softmax always spreads some mass. That softness is what makes attention differentiable.

### Example 2 — A tiny transformer on sentiment

1,500 synthetic sentences, vocabulary 28, max length 12, one encoder layer, $d_{\text{model}}=32$,
4 heads:

```text
parameters: 9922
validation accuracy: 0.990
majority-class baseline: 0.578
```

The model learned the polarity words. On real IMDB reviews the same architecture from scratch
would be far worse — 25,000-word vocabularies and subtle negation need pretraining, which is the
subject of L07-08.

### Example 3 — Quadratic cost, concretely

Sequence length 512, 8 heads, $d_k=64$: the score tensor is $8\times512\times512$, about 2.1
million floats per layer per batch item. At 4,096 tokens it is 134 million — the reason
long-context inference is memory-bound.

## 6. Mathematical Formulation

Scaled dot-product attention and multi-head attention as in §3.2–3.3.

**Parameter count** per encoder layer with $d$ model width:

- $Q,K,V,O$ projections: $4d^2$ (plus biases).
- Feedforward: $2\times d\times d_{ff}$ with $d_{ff}=4d$ by convention.
- Layer norms: $2\times 2d$.

For $d=32$, $d_{ff}=64$: $4(1024)+2(2048)+128\approx8{,}320$ plus embeddings, matching the 9,922
reported when the embedding table (29×32), positions (12×32) and head are included.

**Positional encoding** as in §3.4; the wavelengths form a geometric progression from $2\pi$ to
$10000\cdot2\pi$, so each dimension oscillates at a different frequency.

**Complexity**: $O(n^2d)$ time and $O(n^2+nd)$ memory per layer.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import numpy as np
import torch
import deep_data as dd
from torch_utils import TinyTransformerClassifier, Trainer, make_loader, count_parameters, set_seed

set_seed(0)
texts, labels, vocab = dd.sentiment_data(1500, seed=0)
X = dd.encode_sentiment(texts, vocab, max_len=12)
print("vocab size:", len(vocab), "encoded shape:", X.shape)

model = TinyTransformerClassifier(vocab_size=len(vocab) + 1, max_len=12)
print("parameters:", count_parameters(model))

trainer = Trainer(model, patience=6)
trainer.fit(
    make_loader(X[:1100], labels[:1100], 64, seed=0),
    make_loader(X[1100:], labels[1100:], 256, shuffle=False),
    epochs=12, lr=1e-3,
)
_, acc, preds, true = trainer.evaluate(make_loader(X[1100:], labels[1100:], 256, shuffle=False))
print("validation accuracy:", round(acc, 3))
print("majority baseline:", round(max(np.mean(labels[1100:]), 1 - np.mean(labels[1100:])), 3))
```

```text
vocab size: 28 encoded shape: (1500, 12)
parameters: 9922
validation accuracy: 0.99
majority baseline: 0.578
```

The same formula, one head, by hand in PyTorch — this is Example 1 reproduced by code:

```python
import torch
q = torch.tensor([[1., 0.]])
k = torch.eye(2)
v = torch.tensor([[10., 0.], [0., 20.]])
scores = q @ k.T / (2 ** 0.5)
weights = scores.softmax(dim=-1)
print(scores.numpy().round(3), weights.numpy().round(3), (weights @ v).numpy().round(2))
```

```text
[[0.707 0.   ]] [[0.67 0.33]] [[6.7 6.6]]
```

Rows of the weight matrix sum to 1 because each query distributes one unit of attention across the
keys. Inside the trained model the padding mask zeroes the columns of padded positions before the
softmax, so padding tokens receive no attention.

## 8. Practical Applications

- **Language models** — GPT-style decoders; every modern LLM is a stack of these blocks.
- **Translation and summarisation** — encoder–decoder with cross-attention.
- **Vision transformers** — images split into patches, treated as tokens.
- **Time series** — attention over sensor windows, especially with irregular sampling.
- **Recommenders** — self-attention over a user's history.

## 9. Common Mistakes

1. Forgetting positional information: the model becomes a bag of tokens.
2. Omitting the $\sqrt{d_k}$ scaling, then wondering why training is unstable.
3. Masking padding in the embedding but not in attention or pooling.
4. Using a causal mask when the task is classification over the whole input.
5. Training a transformer from scratch on a small dataset and concluding transformers are worse.
6. Ignoring memory: doubling sequence length quadruples attention cost.
7. Reporting accuracy without a bag-of-words or GRU baseline.

## 10. Practical Exercises

1. Compute attention by hand for $Q=(0,1)$, $K=I_2$, $V=[[1,2],[3,4]]$, $d_k=2$.
2. Show that permuting the input rows of $K$ and $V$ permutes the output, and explain why positional
   encodings are therefore necessary.
3. Count the parameters of a two-layer encoder with $d=64$, $h=4$, $d_{ff}=128$.
4. Train the tiny transformer with `max_len=6` and compare accuracy with `max_len=12`.
5. Replace mean pooling with the first token's state and compare.
6. Add a causal mask and describe what changes in the training objective.

## 11. Self-Assessment

**Multiple choice**

1. Attention weights are produced by
   a) a convolution. b) softmax over scaled query–key scores. c) a recurrent update.
   d) max pooling.
2. The $\sqrt{d_k}$ factor prevents
   a) overfitting. b) saturated softmax and vanishing gradients. c) padding. d) masking.
3. Multi-head attention is useful because
   a) it is cheaper. b) heads can learn different relations. c) it removes the need for positions.
   d) it avoids layer norm.
4. Attention costs, per layer,
   a) $O(n)$. b) $O(n\log n)$. c) $O(n^2)$ in sequence length. d) $O(1)$.

**Short answer**

5. Why can a transformer train faster per epoch than an RNN on the same data?
6. Give one reason a small dataset may favour a GRU over a transformer.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **c**.
5. All positions are processed in parallel; the RNN must step sequentially through time.
6. The transformer has weaker inductive bias and needs more data (or pretraining) to learn
   locality and order; a GRU's recurrence encodes order for free.

</details>

## 12. Key Terms

**Attention**, **query**, **key**, **value**, **scaled dot-product attention**, **multi-head
attention**, **causal mask**, **padding mask**, **positional encoding**, **transformer block**,
**residual connection**, **layer normalisation**, **encoder**, **decoder**, **cross-attention**,
**self-attention**, **quadratic complexity**.

## 13. Further Reading

- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS.
- Bahdanau, Cho & Bengio (2015). *Neural Machine Translation by Jointly Learning to Align and
  Translate*. ICLR. — Attention before the transformer.
- Phuong, M. & Hutter, M. (2022). *Formal Algorithms for Transformers*. — A precise, short
  reference for the mechanics.

## What to Do Next

1. Run the transformer script and inspect the attention matrix.
2. Do exercises 1–3.
3. Continue to [L07-08 — Transfer Learning and Autoencoders](L07-08-transfer-learning-and-autoencoders.md).

---

**Navigation:** [← Previous: L07-06](L07-06-sequence-models-rnn-lstm-gru.md) · [Module home](../README.md) · [Next: L07-08 →](L07-08-transfer-learning-and-autoencoders.md)
