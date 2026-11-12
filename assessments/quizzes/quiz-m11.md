# QUIZ-M11 — Generative AI and Large Language Models

| | |
| :--- | :--- |
| Module | M11 · Generative AI and Large Language Models |
| Questions | 11 (20 marks) |
| Time | 35 minutes |
| Covers | L11-01 … L11-07 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m11.md)

---

## Part A — Multiple choice (4 marks)

**Q11.1** Perplexity is

- A. the mean log-likelihood per token
- B. the exponential of mean negative log-likelihood per token
- C. the accuracy of next-token prediction
- D. the number of tokens in the vocabulary

**Q11.2** LoRA reduces trainable parameters by

- A. quantising the base weights
- B. adding low-rank matrices whose product approximates a weight update
- C. pruning attention heads
- D. freezing the embedding layer only

**Q11.3** Raising the sampling temperature

- A. makes the distribution flatter and output more random
- B. makes the distribution sharper
- C. increases the context window
- D. reduces perplexity

**Q11.4** Retrieval-augmented generation primarily improves

- A. reasoning depth
- B. access to facts not in the parameters, with provenance
- C. decoding speed
- D. tokeniser coverage

## Part B — True or false, with a reason (2 marks)

**Q11.5** "Adding retrieval removes hallucination, because the model can no longer invent facts."

## Part C — Conceptual (4 marks)

**Q11.6** (2 marks) Why are perplexities from models with different tokenisers not comparable?

**Q11.7** (2 marks) Give one failure that retrieval cannot fix and explain why.

## Part D — Numerical (6 marks)

**Q11.8** (3 marks) A model achieves mean negative log-likelihood 1.5 nats per token on a held-out
set. Compute its perplexity to two decimal places.

**Q11.9** (3 marks) A LoRA adapter is applied to a $512\times512$ weight matrix with rank $r=8$ and
no bias. How many trainable parameters does the adapter add?

## Part E — Tracing (2 marks)

**Q11.10** Logits are $[2.0, 1.0, 0.1]$. After a temperature of $T=1$, which token is sampled under
greedy decoding, and what happens to the argmax at $T=10$?

## Part F — Python output (2 marks)

**Q11.11** What does this print?

```python
import numpy as np

logits = np.array([2.0, 1.0, 0.1])
p = np.exp(logits) / np.exp(logits).sum()
print(np.round(p, 3), int(p.argmax()))
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m11.md) · [Next quiz](quiz-m12.md)
