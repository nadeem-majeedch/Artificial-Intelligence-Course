# Glossary — Generative AI (M11)

Generative models, language models, prompting, retrieval and adaptation. Back to the
[glossary index](README.md).

## A

### Autoregressive model
**Abbreviation.** AR · **Module.** M11
**Simple definition.** A model that generates a sequence one element at a time, each conditioned
on what it has already produced.
**Detailed explanation.** Factorising a joint distribution into a chain of conditional
probabilities makes exact likelihood computable and generation sequential. The cost is that
errors compound and generation cannot be parallelised across positions.
**Mathematics.** $p(x_1,\dots,x_T) = \prod_{t=1}^{T} p(x_t \mid x_{<t})$
**Practical example.** A 7-billion-parameter language model writing a 200-token answer performs
200 forward passes, each conditioning on all previous tokens.
**Related.** [Temperature](#temperature), [Perplexity](#perplexity), [Instruction tuning](#instruction-tuning)
**Where it is taught.** [L11-02 Inside a large language model](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-02-inside-a-large-language-model.md)

## C

### Chain-of-thought prompting
**Abbreviation.** CoT · **Module.** M11
**Simple definition.** Asking a model to write intermediate reasoning steps before its answer.
**Detailed explanation.** Intermediate tokens give the model more computation and a scratchpad,
which helps on multi-step arithmetic and logic. It hurts when the task is extraction or the
answer must be short, and the reasoning shown is not guaranteed to be the reasoning used.
**Mathematics.** —
**Practical example.** On a three-step word problem, plain prompting answers 0.52 correct;
"show your steps" raises it to 0.81 but triples output tokens.
**Related.** [Prompt engineering](#prompt-engineering), [In-context learning](#in-context-learning), [Hallucination](#hallucination)
**Where it is taught.** [L11-04 Prompt engineering and in-context learning](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md)

### Chunking
**Abbreviation.** — · **Module.** M11
**Simple definition.** Splitting documents into passages small enough to retrieve and fit into a
prompt.
**Detailed explanation.** Chunk size trades context against precision: large chunks carry more
context but dilute the embedding and waste tokens; small chunks retrieve precisely but lose the
surrounding meaning. Overlap and structure-aware splitting (headings, sentences) reduce
mid-thought cuts.
**Mathematics.** —
**Practical example.** A 40-page handbook split into 300-word chunks with 50-word overlap yields
210 passages; a question about one clause retrieves the right 3.
**Related.** [Retrieval-augmented generation](#retrieval-augmented-generation), [Vector index](#vector-index)
**Where it is taught.** [L11-05 Retrieval-augmented generation](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-05-retrieval-augmented-generation.md)

## D

### Diffusion model
**Abbreviation.** DDPM · **Module.** M11
**Simple definition.** A generative model that learns to reverse a gradual noising process.
**Detailed explanation.** Training adds noise to data and learns to predict it; sampling starts
from noise and denoises step by step. Diffusion produces higher-quality images than GANs and
trains stably, at the cost of many sampling steps.
**Mathematics.** $q(x_t \mid x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}\,x_{t-1}, \beta_t I)$; learn $\epsilon_\theta(x_t, t)$.
**Practical example.** An 8×8 toy diffusion model trained in the M11 notebook generates digit-like
patterns after 300 denoising steps, and its loss curve is the diagnostic.
**Related.** [Variational autoencoder](#variational-autoencoder), [Generative adversarial network](#generative-adversarial-network), [Latent space](#latent-space)
**Where it is taught.** [L11-01 The generative modelling landscape](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-01-the-generative-modelling-landscape.md)

## G

### Generative adversarial network
**Abbreviation.** GAN · **Module.** M11
**Simple definition.** Two networks trained against each other: a generator that makes samples
and a discriminator that judges them.
**Detailed explanation.** The generator learns to fool the discriminator, which learns to tell
real from fake; at equilibrium the generator matches the data distribution. Training is unstable
and can collapse to a few modes, which is why the loss curve alone is not evidence of quality.
**Mathematics.** $\min_G \max_D \mathbb{E}_{x\sim p_{data}}[\log D(x)] + \mathbb{E}_{z}[\log(1 - D(G(z)))]$
**Practical example.** In the M11 notebook the GAN's loss looks healthy while its samples cover
only three of ten classes — mode collapse invisible in the numbers.
**Related.** [Diffusion model](#diffusion-model), [Variational autoencoder](#variational-autoencoder), [Latent space](#latent-space)
**Where it is taught.** [L11-01 The generative modelling landscape](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-01-the-generative-modelling-landscape.md)

## H

### Hallucination
**Abbreviation.** — · **Module.** M11
**Simple definition.** Fluent output that is not supported by the model's evidence or the source.
**Detailed explanation.** A language model optimises plausibility, not truth, so it fills gaps with
confident invention — especially citations, numbers and names. Retrieval reduces but does not
remove it; grounded evaluation (does the answer follow from the retrieved passages?) is the only
reliable check.
**Mathematics.** —
**Practical example.** Asked for a paper on a niche topic, a model invents a plausible title,
author and year; the DOI resolves to nothing.
**Related.** [Retrieval-augmented generation](#retrieval-augmented-generation), [Perplexity](#perplexity), [Chain-of-thought prompting](#chain-of-thought-prompting)
**Where it is taught.** [L11-07 Evaluating LLM systems](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-07-evaluating-llm-systems.md)

## I

### In-context learning
**Abbreviation.** ICL · **Module.** M11
**Simple definition.** Learning a task from examples placed in the prompt, with no weight update.
**Detailed explanation.** The model conditions on demonstrations and infers the pattern. Performance
depends on example order, label balance and formatting, which is why prompt evaluation needs
multiple orderings rather than one lucky run.
**Mathematics.** $p(y \mid x, \text{demos})$ with parameters frozen.
**Practical example.** Five labelled sentiment examples in the prompt move a classifier from 0.61
to 0.84 accuracy; shuffling the same five examples changes it to 0.79.
**Related.** [Prompt engineering](#prompt-engineering), [Chain-of-thought prompting](#chain-of-thought-prompting), [Instruction tuning](#instruction-tuning)
**Where it is taught.** [L11-04 Prompt engineering and in-context learning](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md)

### Instruction tuning
**Abbreviation.** SFT · **Module.** M11
**Simple definition.** Fine-tuning a pretrained model on demonstrations of following instructions.
**Detailed explanation.** Pretraining teaches next-token prediction; instruction tuning teaches the
format of helpful response. It changes behaviour far more than knowledge, and it is the step
between a base model and an assistant.
**Mathematics.** $\max_\theta \sum_{(x,y)} \log p_\theta(y \mid x)$
**Practical example.** A base model completes "Summarise this:" with more text; after 5,000
instruction pairs it produces a summary in the requested length.
**Related.** [RLHF](#rlhf-reinforcement-learning-from-human-feedback), [LoRA](#lora), [In-context learning](#in-context-learning)
**Where it is taught.** [L11-03 Pretraining, instruction tuning and alignment](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-03-pretraining-instruction-tuning-and-alignment.md)

## L

### Latent space
**Abbreviation.** — · **Module.** M11
**Simple definition.** A compressed representation space in which a generative model operates.
**Detailed explanation.** Encoders map data into a lower-dimensional space where structure is
smooth, and decoders map back. Interpolation and sampling happen in the latent space, so its
geometry determines whether generated samples are coherent.
**Mathematics.** $z = E(x)$, $\hat{x} = D(z)$, with $\dim z \ll \dim x$.
**Practical example.** Interpolating between the latents of "3" and "8" produces intermediate
digits that look like neither, revealing gaps in the learned manifold.
**Related.** [Variational autoencoder](#variational-autoencoder), [Diffusion model](#diffusion-model)
**Where it is taught.** [L11-01 The generative modelling landscape](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-01-the-generative-modelling-landscape.md)

### LoRA
**Abbreviation.** LoRA · **Module.** M11
**Simple definition.** Fine-tuning a frozen model by training two small low-rank matrices per
layer.
**Detailed explanation.** The weight update is constrained to a low-rank factorisation, cutting
trainable parameters by orders of magnitude and letting one base model serve many adapters. It
trades a little quality for a lot of memory.
**Mathematics.** $W' = W + \frac{\alpha}{r}BA$, with $B \in \mathbb{R}^{d\times r}$, $A \in \mathbb{R}^{r\times k}$, $r \ll d,k$.
**Practical example.** For a 512×512 projection with rank 8, LoRA trains $8(512+512) = 8{,}192$
parameters instead of $262{,}144$ — 3% of the original.
**Related.** [Instruction tuning](#instruction-tuning), [RLHF](#rlhf-reinforcement-learning-from-human-feedback)
**Where it is taught.** [L11-06 Fine-tuning and parameter-efficient adaptation](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-06-fine-tuning-and-parameter-efficient-adaptation.md)

## P

### Perplexity
**Abbreviation.** PPL · **Module.** M11
**Simple definition.** The exponentiated average negative log-likelihood per token — how surprised
the model is by the text.
**Detailed explanation.** Lower is better, and it is comparable only across models with the same
tokeniser and the same test set. It measures fluency-like fit, not correctness or usefulness.
**Mathematics.** $\text{PPL} = \exp\!\left(-\frac{1}{N}\sum_{i=1}^{N}\log p(x_i \mid x_{<i})\right)$
**Practical example.** A mean negative log-likelihood of 1.5 nats gives $\text{PPL} = e^{1.5} = 4.48$;
a model at 2.0 gives 7.39.
**Related.** [Autoregressive model](#autoregressive-model), [Temperature](#temperature), [Hallucination](#hallucination)
**Where it is taught.** [L11-07 Evaluating LLM systems](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-07-evaluating-llm-systems.md)

### Prompt engineering
**Abbreviation.** — · **Module.** M11
**Simple definition.** Designing the instructions and context given to a model to obtain a
reliable output.
**Detailed explanation.** Prompts specify task, format, constraints and examples; small wording
changes produce large behavioural changes. It is a design discipline with tests, not a bag of
incantations — the same prompt must be evaluated across paraphrases and edge cases.
**Mathematics.** —
**Practical example.** Adding an output schema and one counter-example reduces a model's invalid
JSON responses from 18% to 2%.
**Related.** [In-context learning](#in-context-learning), [Chain-of-thought prompting](#chain-of-thought-prompting), [Retrieval-augmented generation](#retrieval-augmented-generation)
**Where it is taught.** [L11-04 Prompt engineering and in-context learning](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md)

## R

### Retrieval-augmented generation
**Abbreviation.** RAG · **Module.** M11
**Simple definition.** Retrieving relevant passages and putting them in the prompt so the model
answers from evidence rather than memory.
**Detailed explanation.** Retrieval supplies facts the model lacks or has outdated, and grounding
makes attribution possible. Quality is bounded by retrieval: if the right passage is not
retrieved, generation cannot fix it, which is why retrieval is evaluated separately from answers.
**Mathematics.** $p(y \mid x) \approx p(y \mid x, \text{top-}k(q))$
**Practical example.** A handbook assistant retrieves three passages and answers with citations;
removing one retrieval step drops answer accuracy from 0.78 to 0.41.
**Related.** [Chunking](#chunking), [Vector index](#vector-index), [Hallucination](#hallucination)
**Where it is taught.** [L11-05 Retrieval-augmented generation](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-05-retrieval-augmented-generation.md)

### RLHF (reinforcement learning from human feedback)
**Abbreviation.** RLHF · **Module.** M11
**Simple definition.** Training a model to prefer outputs that human raters prefer, using a
learned reward model.
**Detailed explanation.** Raters rank outputs, a reward model learns the ranking, and the policy
is optimised against it with a constraint that keeps it close to the original. It aligns style
and refusal behaviour, not factual accuracy, and it can be gamed.
**Mathematics.** $\max_\pi \mathbb{E}[r_\phi(x,y)] - \beta\, D_{KL}(\pi \,\|\, \pi_{ref})$
**Practical example.** A model fine-tuned this way stops producing unsafe completions while
losing two points on a factual benchmark — the trade-off is measurable.
**Related.** [Instruction tuning](#instruction-tuning), [Hallucination](#hallucination)
**Where it is taught.** [L11-03 Pretraining, instruction tuning and alignment](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-03-pretraining-instruction-tuning-and-alignment.md)

## T

### Temperature
**Abbreviation.** $T$ · **Module.** M11
**Simple definition.** A divisor on logits that controls how random the sampling is.
**Detailed explanation.** Low temperature sharpens the distribution toward the most likely token;
high temperature flattens it. Temperature 0 (greedy) is deterministic but can loop; the setting
is a product decision about creativity versus consistency.
**Mathematics.** $p_i = \dfrac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}$
**Practical example.** With logits 3.0 and 1.5, $T = 1$ gives probabilities 0.82/0.18; $T = 2$
gives 0.68/0.32 — the same model, very different outputs.
**Related.** [Autoregressive model](#autoregressive-model), [Perplexity](#perplexity)
**Where it is taught.** [L11-02 Inside a large language model](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-02-inside-a-large-language-model.md)

## V

### Variational autoencoder
**Abbreviation.** VAE · **Module.** M11
**Simple definition.** An autoencoder whose latent code is a probability distribution, trained by
maximising a lower bound on likelihood.
**Detailed explanation.** The encoder outputs a mean and variance; sampling from that distribution
keeps the latent space smooth and makes generation possible. The reconstruction term fights the
KL term, which is why VAE samples are blurrier than GAN or diffusion samples.
**Mathematics.** $\mathcal{L} = \mathbb{E}_{q}[\log p(x \mid z)] - D_{KL}(q(z\mid x)\,\|\,p(z))$
**Practical example.** A VAE on 8×8 digits reconstructs shapes well but its samples are soft —
the blur is the KL term doing its job.
**Related.** [Latent space](#latent-space), [Generative adversarial network](#generative-adversarial-network), [Diffusion model](#diffusion-model)
**Where it is taught.** [L11-01 The generative modelling landscape](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-01-the-generative-modelling-landscape.md)

### Vector index
**Abbreviation.** — · **Module.** M11
**Simple definition.** A data structure that finds the nearest vectors to a query quickly.
**Detailed explanation.** Exact search is linear in the corpus, so approximate nearest-neighbour
indexes trade a little recall for large speed gains. Retrieval quality depends on the embedding
model, the chunking and the index parameters together.
**Mathematics.** $\text{top-}k = \arg\max_{d} \cos(q, e_d)$ over indexed documents $d$.
**Practical example.** An index over 210 handbook chunks returns the right passage in the top 3
for 82% of test questions; the two failures are questions whose wording never appears in the text.
**Related.** [Retrieval-augmented generation](#retrieval-augmented-generation), [Chunking](#chunking)
**Where it is taught.** [L11-05 Retrieval-augmented generation](../../modules/M11-generative-ai-and-large-language-models/lessons/L11-05-retrieval-augmented-generation.md)

---

[Glossary index](README.md) · [Reinforcement learning](reinforcement-learning.md) · [Agents](agents.md) · [Quick reference](../glossary.md)
