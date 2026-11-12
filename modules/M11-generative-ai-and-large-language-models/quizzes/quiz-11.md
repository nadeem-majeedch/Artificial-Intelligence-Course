# QUIZ-11 — Generative AI and Large Language Models self-check

| Module | M11 · Generative AI and Large Language Models |
| :--- | :--- |
| Questions | 20 multiple choice + 6 numerical + 4 short answer + 3 programming |
| Time | 60 minutes (Part C open-book) |
| Covers | [L11-01](../lessons/L11-01-the-generative-modelling-landscape.md) … [L11-07](../lessons/L11-07-evaluating-llm-systems.md) |
| Pass mark | 15 / 20 on Part A, plus 4 / 6 on Part B |

[← Module home](../README.md) · [Course home](../../../README.md)

## How to use this quiz

Parts A and B are closed-book; a calculator is allowed, code is not. Part C is open-book and
expects you to run code. Mark yourself against the worked answers, then use the revision map
at the end. An answer you get right by elimination still counts, but reread the explanation.

## Part A — Multiple choice (20 marks)

**Q11.01** A discriminative model learns
- A. $p(x)$
- B. $p(y\mid x)$
- C. the latent prior
- D. the noise schedule

**Q11.02** The ELBO is a lower bound on
- A. the reconstruction loss
- B. $\log p(x)$
- C. the KL divergence to the prior
- D. the adversarial loss

**Q11.03** The reparameterisation trick $z=\mu+\sigma\odot\epsilon$ exists so that
- A. sampling is deterministic
- B. gradients can pass through the sampling step
- C. the latent space is discrete
- D. the decoder is invertible

**Q11.04** In DDPM the network is trained to predict
- A. the clean data
- B. the class label
- C. the noise added at step $t$
- D. the reverse schedule

**Q11.05** Mode collapse is best detected by
- A. the generator loss
- B. the discriminator loss
- C. class coverage and diversity of samples
- D. training wall-clock

**Q11.06** A tokeniser that maps a rare word to several subword pieces is
- A. character-level
- B. BPE-style subword
- C. word-level
- D. byte-level only

**Q11.07** The $\sqrt{d_k}$ divisor in attention prevents
- A. overfitting
- B. saturated softmax and vanishing gradients
- C. padding leakage
- D. quadratic cost

**Q11.08** A causal mask ensures position $t$ attends
- A. to all positions
- B. only to positions $\le t$
- C. only to position $t$
- D. to no positions

**Q11.09** The context window limits
- A. the vocabulary
- B. prompt tokens plus generated tokens
- C. the number of layers
- D. only the output length

**Q11.10** Instruction tuning primarily changes
- A. factual knowledge
- B. response format and behaviour
- C. the tokeniser
- D. the attention mechanism

**Q11.11** DPO differs from RLHF in that it
- A. needs no reference model
- B. needs no reward model
- C. needs no preference data
- D. trains from scratch

**Q11.12** LoRA with rank $r$ trains approximately
- A. $d^2$ parameters per layer
- B. $r(d+k)$ parameters per wrapped projection
- C. only embeddings
- D. the full model at low precision

**Q11.13** Dynamic int8 quantisation of a small model typically
- A. always reduces latency
- B. reduces size and may increase latency
- C. improves accuracy
- D. changes the tokeniser

**Q11.14** Chain-of-thought prompting is least useful when
- A. the task needs serial arithmetic
- B. the model is too small to reason
- C. the task is multi-hop
- D. the answer must be explained

**Q11.15** The safest way to obtain structured output is
- A. asking for JSON
- B. regex extraction
- C. schema validation with retries or constrained decoding
- D. lowering the temperature

**Q11.16** A prompt-injection attack works because
- A. models are slow
- B. instructions and data share one channel
- C. JSON is hard to parse
- D. temperature is above 1

**Q11.17** BM25 outperforms dense retrieval mainly on
- A. paraphrases
- B. rare exact terms
- C. images
- D. long documents only

**Q11.18** Hybrid retrieval requires
- A. a GPU
- B. score normalisation before fusion
- C. a reranker
- D. no index

**Q11.19** An end-to-end score of 0.75 with recall@1 = 1.00 and refusal rate 0.00 suggests
- A. retrieval is broken
- B. generation selects wrong spans and never declines
- C. the tokeniser is wrong
- D. the model is too small

**Q11.20** Cohen's κ is used because
- A. it is faster than accuracy
- B. it corrects agreement for chance
- C. it needs no labels
- D. it measures latency

## Part B — Numerical (6 marks)

**Q11.21** Compute the KL contribution of one latent dimension with $\mu=0.5$ and
$\log\sigma^2=-1.0$. (Answer in nats, three decimals.)

**Q11.22** With window 1,024, prompt 900 and 200 reserved output tokens, how many tokens are
available for context, and how many overflow?

**Q11.23** A corpus of 1,895 words tokenises to 2,281 tokens. Compute tokens per word and
characters per token given 11,608 characters.

**Q11.24** A sentence of 66 characters becomes 13 tokens. Compute the mean token length and
the cost multiplier versus a tokeniser averaging 4 characters per token.

**Q11.25** At 10 prompt tokens and 2 completion tokens per query, with prices 0.50 USD and
1.50 USD per million tokens, compute the cost per 1,000 queries.

**Q11.26** Rank-8 LoRA wraps 24 projections and trains 589,824 parameters of an 82,502,400
parameter model. Compute the trainable share as a percentage.

## Part C — Short answer (4 marks)

**Q11.27** Explain why fine-tuning is the wrong tool for facts that change monthly.

**Q11.28** Give two reasons a RAG system can have perfect retrieval and still answer wrongly.

**Q11.29** Why is few-shot prompting not "learning"? Refer to the measured template table.

**Q11.30** State one thing the grounding score cannot detect, with an example from this module.

## Part D — Programming (3 tasks, open-book)

**Q11.31** Write a function that takes a list of (prediction, gold) pairs and returns exact
match, token F1 and ROUGE-L. Validate it on the pairs `("08:00","08:00")`,
`("8:00","08:00")` and `("I don't know","08:00")`.

**Q11.32** Implement top-p (nucleus) filtering for a logit vector and verify that the retained
tokens' probabilities sum to at least $p$ and that removing the last retained token drops the
sum below $p$.

**Q11.33** Implement chunking with overlap and demonstrate on a 200-token document that every
token appears in at least one chunk when overlap is at least the window minus the stride.

---

## Answer key

### Part A

| Q | Answer | Note |
| :--- | :--- | :--- |
| 11.01 | B | generative models learn $p(x)$, discriminative learn $p(y\mid x)$ |
| 11.02 | B | the gap is the KL between approximate and true posterior |
| 11.03 | B | moves randomness out of the differentiated path |
| 11.04 | C | denoising objective $\|\epsilon-\epsilon_\theta\|^2$ |
| 11.05 | C | losses looked fine at 3/10 classes |
| 11.06 | B | BPE splits rare words into frequent pieces |
| 11.07 | B | measured: unscaled softmax at $d_k=256$ has entropy 0.000 |
| 11.08 | B | lower-triangular weight matrix |
| 11.09 | B | prompt + output share the window |
| 11.10 | B | 0.00 → 0.60 exact match came from *context*, not tuning |
| 11.11 | B | DPO removes the reward model but keeps the reference |
| 11.12 | B | $r(d+k)$ per wrapped projection |
| 11.13 | B | 307.8 → 65.9 MB but 0.159 → 0.423 s |
| 11.14 | B | measured EM 0.00 for the 77M model |
| 11.15 | C | 0/6 raw JSON valid here |
| 11.16 | B | retrieved text and instructions are the same channel |
| 11.17 | B | policy numbers, error codes, names |
| 11.18 | B | scales differ by orders of magnitude |
| 11.19 | B | wrong span selection, zero refusals |
| 11.20 | B | judge B looked 60% right and was κ = 0.200 |

### Part B

**11.21** $\tfrac12(\mu^2+\sigma^2-1-\log\sigma^2)=\tfrac12(0.25+0.3679-1+1)=0.3090$ nats.

**11.22** $1024-900-200=-76$: 0 tokens available, 76 overflow.

**11.23** $2281/1895=1.204$ tokens per word; $11608/2281=5.089$ characters per token.

**11.24** $66/13=5.08$ characters per token; versus 4.0 that is $5.08/4.0=1.27$, so about 27%
fewer tokens (and 27% lower cost) than the 4-characters-per-token baseline.

**11.25** $(10\times0.5+2\times1.5)/10^6\times1000=(5+3)/1000=0.008$ USD per query, so
**8.00 USD per 1,000 queries**.

**11.26** $589{,}824/82{,}502{,}400=0.00715$, i.e. **0.715%**.

### Part C

**11.27** Weights encode a snapshot of the training distribution and are expensive to update
and to re-evaluate; retrieval can be re-indexed in minutes, keeps provenance, and can be
audited. Fine-tuning also risks teaching the model to assert stale facts confidently.

**11.28** (i) The model selects a span from the correct document that answers a different
question — measured: "20:00" for the weekday opening time, and "15 October" for the January
instalment. (ii) The chunk containing the right document omits the sentence with the answer,
so the answer is assembled from adjacent-but-wrong text.

**11.29** Weights are unchanged; the examples shift the conditional distribution at inference.
Measured on 12 questions, few-shot scored *worse* than zero-shot (EM 0.50 vs 0.67) while
costing 258 versus 135 prompt tokens.

**11.30** It cannot detect a wrong-but-grounded span. Every content word of "20:00" appears in
the library document, so support is 1.00, yet the answer contradicts the question. Only
comparison with a gold answer catches it.

### Part D marking notes

**11.31** Expect a normalisation step, multiset token overlap, and an LCS. Reference output:
`EM 0.333, F1 0.667, ROUGE-L 0.667` for the three pairs.

**11.32** Sort descending, cumsum, keep until the cumulative mass reaches $p$ inclusive;
verify the two properties. A common bug is dropping the token that crosses $p$.

**11.33** The invariant holds when `stride <= window - overlap`; test by collecting the set of
covered indices.

---

## Revision map

| If you missed | Reread |
| :--- | :--- |
| 11.01–11.05 | [L11-01](../lessons/L11-01-the-generative-modelling-landscape.md) |
| 11.06–11.09 | [L11-02](../lessons/L11-02-inside-a-large-language-model.md) |
| 11.10–11.13 | [L11-03](../lessons/L11-03-pretraining-instruction-tuning-and-alignment.md) |
| 11.14–11.16 | [L11-04](../lessons/L11-04-prompt-engineering-and-in-context-learning.md) |
| 11.17–11.19 | [L11-05](../lessons/L11-05-retrieval-augmented-generation.md), [L11-07](../lessons/L11-07-evaluating-llm-systems.md) |
| 11.20 | [L11-07](../lessons/L11-07-evaluating-llm-systems.md) |
| Numerical | the worked examples in L11-01, L11-02, L11-06 and the [summary](../summary.md) |
