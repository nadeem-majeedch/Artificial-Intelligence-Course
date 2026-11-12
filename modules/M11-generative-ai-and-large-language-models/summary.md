# M11 — One-Page Summary

[Module home](README.md) · [Course home](../../README.md) · [Quiz](quizzes/quiz-11.md)

## The pipeline

```text
documents -> ingest -> chunk -> embed (+ BM25) -> fuse -> rerank -> pack context
          -> prompt (role, evidence, refusal path, format) -> model -> answer + sources
          -> evaluate: retrieval / answer / grounding / behaviour / cost
```

The five stages people confuse, and what each one is actually for:

| Stage | Changes | Fixes | Does not fix |
| :--- | :--- | :--- | :--- |
| Prompt engineering | conditioning only | format, tone, refusal behaviour | missing knowledge |
| RAG | the context | facts, provenance, freshness | style, weak reasoning |
| SFT / LoRA | weights (or adapters) | format, task behaviour | facts that change |
| Preference tuning | weights | tone, refusal calibration | truthfulness |
| Quantisation | weight precision | size, memory | accuracy (usually costs some) |

## Formulas

$$
p(x_{1:T})=\prod_t p(x_t\mid x_{<t}),
\qquad
\mathcal L=-\frac1T\sum_t\log p(x_t\mid x_{<t}),
\qquad
\text{PPL}=\exp\!\left(-\frac1T\sum_t\log p(x_t\mid x_{<t})\right).
$$

$$
\text{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V,
\qquad
\text{MultiHead}=\mathrm{Concat}(\text{head}_1,\dots,\text{head}_h)W_O .
$$

$$
\mathcal L_{\text{ELBO}}=\mathbb E_q[\log p(x\mid z)]-D_{\mathrm{KL}}(q(z\mid x)\|p(z)),
\qquad
D_{\mathrm{KL}}=\tfrac12\textstyle\sum_j(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2).
$$

$$
\min_G\max_D\;\mathbb E_{x}[\log D(x)]+\mathbb E_z[\log(1-D(G(z)))],
\qquad
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon .
$$

$$
W'=W+\frac{\alpha}{r}BA,
\qquad
\text{BM25}=\sum_t\text{IDF}(t)\frac{f_{td}(k_1+1)}{f_{td}+k_1(1-b+b|d|/\text{avgdl})},
\qquad
\text{MaxSim}=\sum_{i\in q}\max_{j\in d}\cos(e_i,e_j).
$$

$$
\text{Recall@}k=\frac{|\text{rel}\cap\text{top}_k|}{|\text{rel}|},
\qquad
\text{MRR}=\frac1{|Q|}\sum_q\frac1{\text{rank}_q},
\qquad
\kappa=\frac{p_o-p_e}{1-p_e}.
$$

## Verified numbers from this module

Run the scripts and you should see these figures (CPU, seed 0, cached models):

| Experiment | Result |
| :--- | :--- |
| Corpus | 24 documents, 1,895 words, 11,608 characters, 79 words/doc |
| PDF round-trip | 4 pages, 15,293 bytes, 12,471 characters extracted |
| Tokenisation (one sentence) | 66 chars / 8 words / 13 tokens; 5.08 chars per token |
| Corpus tokenisation | 2,281 tokens, 1.204 tokens per word, 871 distinct ids |
| Tokeniser probes | `HELLO` 3, `1234567890` 4, `2026-11-11` 6, `9,250` 3 tokens |
| Context arithmetic | window 1024, prompt 900, reserve 200 → 0 available, 76 over |
| Attention saturation, $d_k=256$ | unscaled max weight 1.0000, entropy 0.000; scaled 0.5815, 1.5017 |
| distilgpt2 attention, 13 tokens | entropy 1.180 → 0.644 (layer 0 → 4), look-back 2.618 → 5.202 |
| Next-token mass | top-5 = 0.3516 for "The library opens at" |
| VAE | 30 epochs, 12.4 s, recon 24.23, KL 1.67, recon MSE 0.0539, 7/8 active latents |
| VAE samples | NN-MSE 1.8006, 10/10 classes, max share 0.24, diversity 1.8203 |
| GAN | 1,500 steps, 30.0 s, D loss 0.351, G loss 2.555 |
| GAN samples | NN-MSE 5.4135, **3/10 classes**, max share 0.68 — mode collapse |
| DDPM | 1,500 steps, 15.9 s, final noise MSE 0.2152; 200 samples in 0.7 s |
| DDPM samples | NN-MSE 3.0519, 10/10 classes, diversity 5.9105 |
| Real data reference | NN-MSE 1.1082, max class share 0.10, diversity 9.3918 |
| Perplexity (distilgpt2) | 46.35 / 59.26 / 131.97 on three handbook sections |
| Sampling | greedy entropy 0.000; T=1.0 3.630; T=1.5 7.619; top-p 0.9 0.766 |
| Grounded vs closed book (15 q) | EM 0.60 vs 0.00; F1 0.78 vs 0.03; latency 0.28 vs 0.17 s |
| Unanswerable refusal | 0.00 grounded, 0.00 closed book; 1/8 had unsupported numbers |
| Templates (12 q) | zero-shot 0.67/0.80; few-shot 0.50/0.74; CoT 0.00/0.18; JSON 0/6 valid |
| Prompt tokens | zero-shot 135, few-shot 258 (569 vs 1,079 characters) |
| Injection | naive 0.00, defended 0.00 — inconclusive at this model size |
| Quantisation | 307.8 MB → 65.9 MB; 0.159 s → 0.423 s; EM 1.00 → 0.50 |
| KV cache | 24 tokens: 2.06 s → 1.87 s (1.1×) |
| RAG index | 24 docs → 48 chunks, 384-dim, FAISS, 44.9 s build |
| Retrieval R@1 | dense 0.90, BM25 0.97, hybrid 1.00, hybrid+rerank 1.00 |
| Retrieval MRR | dense 0.944, BM25 0.983, hybrid 1.000 |
| RAG end-to-end (12 q) | EM 0.75, F1 0.85, support 1.00, latency 1.84 s, refusals 0/12 |
| RAG unanswerable | refusal 0.00; answers `'15 working days'`, `'1'`, `'John C.'`, `'40 GBP'` |
| Chunk sweep | 40/10: 69 chunks, R@1 0.93, EM 0.67; 60/15: 48, 1.00, 0.75; 100/25: 24, 0.93, 0.75 |
| LoRA budget (r=8) | 24 layers, 589,824 trainable = 0.715%, adapter 2.4 MB |
| LoRA training | 40 steps, 12.4 s, held-out 4.956 → 3.005 |
| LoRA merge | 24 layers, max logit difference 6.87e-05, 0 trainable left |
| Judge reliability | 80% agreement κ=0.600; 60% agreement κ=0.200 |
| Latency/cost | p50 0.55 s, p95 2.10 s; 8.00 USD per 1,000 queries at 0.50/1.50 prices |

## Decision table

| You need | Do this first | Then | Evidence required |
| :--- | :--- | :--- | :--- |
| Facts from documents | RAG with citations | reranking, query rewriting | recall@k, EM, refusal rate |
| A different answer format | prompt | SFT / LoRA | EM, length, refusal rate |
| Lower latency | smaller model, cache | quantisation (measure!) | p50/p95, quality delta |
| Per-tenant behaviour | LoRA adapters | QLoRA | held-out loss, task metric |
| Trust | evaluation harness | human review of samples | κ, slice analysis |

## Diagnostics cheat sheet

| Symptom | Likely cause | First thing to try |
| :--- | :--- | :--- |
| Fluent but wrong answers | ungrounded generation | add context + refusal path |
| Right document, wrong span | generation selection | extractive prompt, shorter context |
| Answer missing entirely | retrieval or chunking | recall@k, chunk size, overlap |
| Never says "I don't know" | no refusal path, no threshold | refusal instruction, score threshold |
| Repetitive output | low temperature or greedy | top-p + temperature + repetition penalty |
| Garbled structured output | decoding not constrained | schema validation with retries |
| Loss falls, quality does not | overfitting small data | fewer steps, held-out metric |
| Size down, quality down | quantisation | re-evaluate; consider adapter-aware quantisation |
| Slow tail (p95) | retrieval or long context | measure stages separately |

## What to do next

- [M12 — AI Agents and Agentic AI Systems](../README.md#m12) builds on tool use and evaluation.
- [M13 — Responsible, Explainable and Secure AI](../README.md#m13) covers safety and governance in depth.
- Re-run your evaluation harness before shipping any prompt or index change.
