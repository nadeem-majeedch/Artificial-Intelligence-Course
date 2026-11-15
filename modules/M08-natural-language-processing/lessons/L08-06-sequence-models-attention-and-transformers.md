# L08-06 — Sequence Models, Attention and Transformer Foundations

| Module | M08 · Natural Language Processing |
| :--- | :--- |
| Level | 300 |
| Study time | 110 minutes |
| Prerequisites | [L08-05](L08-05-text-classification-sentiment-and-ner.md) · [L07-03](../../M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md) |
| Code | [`code/seq_models.py`](../code/seq_models.py) · Notebook `nb-08-03` |

[← Previous: L08-05](L08-05-text-classification-sentiment-and-ner.md) · [Module home](../README.md)

## 1. Learning Objectives

- **Write** the recurrence and explain why it struggles with long-range dependencies.
- **Compute** scaled dot-product attention by hand and in NumPy.
- **Describe** a transformer block: attention, residual, layer norm, feed-forward.
- **Decide** whether a task needs a transformer or a TF-IDF baseline, with a cost argument.

## 2. Prerequisite Knowledge

Sequence modelling and transfer learning — [L07-03](../../M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md).

## 3. Conceptual Explanation

### 3.1 Recurrence

$$h_t = \tanh(W_h h_{t-1} + W_x x_t + b), \qquad y_t = \mathrm{softmax}(W_y h_t)$$

Information from step $t-k$ reaches step $t$ through $k$ multiplications by $W_h$. If the largest
singular value is below 1 the contribution decays (vanishing); above 1 it explodes. LSTMs and GRUs add
gates that create a shorter gradient path, which helps but does not remove the sequential bottleneck:
step $t$ cannot be computed before step $t-1$.

### 3.2 Attention in one equation

$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Every position can look at every other position in one step. The $\sqrt{d_k}$ keeps the logits from
growing with dimension, which would saturate the softmax. Cost is $O(n^2 d)$ — quadratic in sequence
length, the reason long-document NLP is expensive.

**Multi-head** attention runs $h$ of these in parallel with $d_k = d/h$ and concatenates: different
heads learn different relations (adjacency, agreement, coreference), in principle.

### 3.3 A transformer block

```text
x -> LayerNorm -> multi-head attention -> + x   (residual)
  -> LayerNorm -> feed-forward (2 layers) -> + x
```

Residual connections make deep stacks trainable; layer norm stabilises; the feed-forward layer does the
per-position transformation. **Positional encodings** are added because attention alone is
permutation-invariant — without them, word order disappears.

### 3.4 Pre-train, then fine-tune

A pre-trained encoder is trained on unlabelled text (masked prediction) and then fine-tuned on your
labelled task. This is why 500 labelled examples can beat a from-scratch model trained on 50,000 — and
also why your results depend on the pre-training corpus, which you did not choose.

**Availability warning.** `transformers` and CPU `torch` are installed in this environment, but every
pre-trained model is a download. Nothing in this module's executed notebooks requires one, and no claim
is made here about the quality of any Urdu checkpoint: if you use one, verify that it downloads, record
its name and revision, and evaluate it on your own labelled Urdu data before quoting a number.

## 4. Worked Example — attention by hand

Sequence `["the", "cat", "sat"]`, $d_k = 2$, one head, simplified $Q=K=V$ embeddings:

| token | vector |
| :--- | :--- |
| the | (1, 0) |
| cat | (0.9, 0.1) |
| sat | (0.7, 0.7) |

$QK^\top$ for "cat" against all: $(0.9, 0.1)\cdot(1,0) = 0.9$; against itself $0.82$; against "sat"
$0.70$. Divide by $\sqrt{2} = 1.414$: 0.636, 0.580, 0.495. Softmax: 0.355, 0.336, 0.309 — "cat"
attends most to "the", then to itself, then to "sat". With real weights these attention maps are what the
diagrams in papers show; here you can check the arithmetic.

## 5. Mathematical Formulation

Full block with residual and normalisation:

$$A = \mathrm{softmax}(QK^\top/\sqrt{d_k}), \quad
H = \mathrm{LN}(x + A V), \quad
y = \mathrm{LN}(H + \mathrm{FFN}(H))$$

Complexity per layer: attention $O(n^2 d)$, feed-forward $O(n d^2)$; memory $O(n^2)$ for the attention
matrix, which is what limits batch size on a long document.

## 6. Python Implementation

```python
import numpy as np


def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def attention(Q, K, V, mask=None):
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    if mask is not None:
        scores = np.where(mask, scores, -1e9)
    weights = softmax(scores)
    return weights @ V, weights


X = np.array([[1.0, 0.0], [0.9, 0.1], [0.7, 0.7]])   # the, cat, sat
out, weights = attention(X, X, X)
print("weights:\n", np.round(weights, 3))
print("row sums:", np.round(weights.sum(axis=1), 6))
print("output:\n", np.round(out, 3))
```

```text
weights:
 [[0.455 0.312 0.233]
  [0.373 0.354 0.273]
  [0.331 0.333 0.336]]
row sums: [1. 1. 1.]
output:
 [[0.874 0.194]
  [0.873 0.194]
  [0.867 0.267]]
```

Every row sums to 1: attention is a weighted average of value vectors, which is why it cannot invent a
token and why it is stable to train.

A causal mask (for language modelling) is `np.tril(np.ones((n, n), dtype=bool))`; apply it before the
softmax, as the `mask` argument does.

## 7. Practical Applications

- **Classification with limited labels** — fine-tune a small encoder, or start with TF-IDF and only
  escalate if the gap pays for the compute.
- **NER** — token classification with a pre-trained encoder is the standard strong baseline.
- **Translation and summarisation** — encoder–decoder transformers.
- **Retrieval** — sentence embeddings, with attention maps usable as a rough explanation.

## 8. Common Mistakes

- Claiming a transformer "understands" order without positional encodings.
- Forgetting the $\sqrt{d_k}$ scaling, then blaming the learning rate for saturated softmax.
- Fine-tuning on 200 examples without a held-out set and reporting the training loss.
- Using a model whose pre-training corpus you cannot name, then being surprised by domain failure.
- Assuming an Urdu checkpoint works because the model card lists `ur` among 100 languages.

## 9. Exercises

1. Reproduce the attention table in §4 and confirm each row sums to 1.
2. Add a causal mask and show how the output for "the" changes.
3. Compute the attention cost for $n = 128$ and $n = 1024$ with $d = 64$ and compare with the feed-forward cost.
4. Train TF-IDF + logistic regression on a small labelled set, then state what evidence would justify moving to a transformer.

## 10. Self-Assessment

1. Why do recurrent networks struggle with long dependencies?
2. What does the $\sqrt{d_k}$ do?
3. What would break if positional encodings were removed?
4. Give one cost argument for staying with a TF-IDF baseline.

## 11. Key Terms

**Recurrence**, **vanishing gradient**, **attention**, **query/key/value**, **scaled dot-product**, **multi-head**, **residual connection**, **layer norm**, **positional encoding**, **pre-training**, **fine-tuning**.

## 12. Further Reading

- Vaswani et al. (2017), "Attention is All You Need".
- Jurafsky & Martin, chapter 9; Jay Alammar's illustrated transformer for the diagrams.

## What to Do Next

Work [LAB-08-03](../labs/lab-08-03-urdu-and-english-sentiment-and-ner.md), then compare a TF-IDF and an
encoder baseline on the same split and report the cost difference honestly.
