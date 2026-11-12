# QUIZ-M11 — Solutions and Explanations

[Quiz](quiz-m11.md) · [Assessment index](../README.md)

---

## Part A

**Q11.1 — B.** $\text{PPL}=\exp\!\left(-\frac1T\sum_t\log p(x_t)\right)$, the geometric mean
inverse probability per token. Option A is the negative log-likelihood, not its exponential.

**Q11.2 — B.** LoRA freezes $W$ and learns $BA$ with $B\in\mathbb R^{d\times r}$,
$A\in\mathbb R^{r\times k}$, adding $r(d+k)$ parameters instead of $dk$.

**Q11.3 — A.** Dividing logits by $T>1$ flattens the distribution: low-probability tokens become
relatively more likely. $T\to0$ approaches greedy decoding.

**Q11.4 — B.** Retrieval supplies facts and provenance in the context window. It does not add
reasoning capacity, which is why multi-step inference errors survive it.

## Part B

**Q11.5 — False.** Retrieval reduces fabrication about the retrieved content, but the model can
still misread sources, combine them incorrectly, or answer from memory when retrieval fails. It also
cannot reason beyond what the sources support. Grounding must be measured, not assumed.

## Part C

**Q11.6 — Model answer.** Perplexity is per token, and tokenisers split text differently, so the
same text yields different token counts and different per-token likelihoods. Comparing perplexities
across tokenisers (or across vocabularies) compares normalisations that are not equivalent; compare
bits-per-character or run the same tokeniser.

**Q11.7 — Model answer.** Multi-step reasoning or arithmetic: retrieval can put the correct facts in
context and the model can still compute the wrong answer. Retrieval changes what is available, not
what the model can do with it.

## Part D

**Q11.8 —** $\text{PPL}=e^{1.5}\approx4.48$.

**Q11.9 —** $r(d+k)=8(512+512)=8{,}192$ parameters. The full matrix has $512^2=262{,}144$, so the
adapter is about 3.1% of it.

## Part E

**Q11.10 —** Greedy decoding picks index 0 (logit 2.0). Raising $T$ to 10 divides the logits by 10;
the argmax is unchanged, but the probabilities become much closer, so sampling becomes far more
random. Temperature does not change the ranking, only the spread.

## Part F

**Q11.11 —** `[0.659 0.242 0.099] 0`

Softmax of $[2.0,1.0,0.1]$: $e^2=7.389$, $e^1=2.718$, $e^{0.1}=1.105$; total $11.212$, giving
$0.659$, $0.242$, $0.099$. The argmax is index 0.

---

[Quiz](quiz-m11.md) · [Assessment index](../README.md) · [Next solutions](quiz-m12.md)
