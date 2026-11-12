# L11-01 — The Generative Modelling Landscape

[← Module start](../README.md) · [Next: ? Lesson →](L11-02-inside-a-large-language-model.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. Choosing a Family: A Decision Procedure](#4-choosing-a-family-a-decision-procedure)
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

> **Module M11** · Lesson 1 of 7 · ~90 minutes · Level 400
> **Prerequisites:** M07 (neural networks, training), M08 (text processing)

[Module overview](../README.md) · [Next: L11-02 →](L11-02-inside-a-large-language-model.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Distinguish** discriminative from generative modelling, and say which one a task needs.
2. **Name** the four dominant generative families and the objective each one optimises.
3. **Derive** the evidence lower bound and explain why the VAE needs it.
4. **Explain** the GAN minimax objective and recognise mode collapse from a metric.
5. **Describe** the forward and reverse processes of a diffusion model.
6. **Write** the autoregressive factorisation and relate it to perplexity.
7. **Choose** a family for text, image, audio and video, and state its costs.

## 2. Prerequisite Knowledge

You need: neural network training with gradients (M07), the chain rule, conditional
probability, and the difference between a likelihood and a loss. The variational bound is
the only new derivation; it is done line by line in §3.5.

## 3. Conceptual Explanation

### 3.1 What "generative AI" actually means

A generative model learns the probability distribution of data, $p(x)$, or a conditional
distribution $p(x\mid c)$ for a context $c$. Once you have that distribution you can do
three things a classifier cannot:

- **sample** new data points $x\sim p(x)$;
- **score** existing points, which gives you likelihood, anomaly detection and compression;
- **condition** the sample on an input — a prompt, an image, a class label.

Everything else in this module — tokens, attention, RAG, fine-tuning — is engineering
built on top of that one idea: model the distribution, then sample from it usefully.

### 3.2 Discriminative versus generative

| | Discriminative | Generative |
| :--- | :--- | :--- |
| Learns | $p(y\mid x)$ | $p(x)$ or $p(x,y)$ |
| Question answered | "which class?" | "what does this data look like?" |
| Typical loss | cross-entropy on labels | negative log-likelihood, adversarial, ELBO |
| Sample from it | no | yes |
| Data efficiency on classification | usually better | usually worse |
| Failure mode | confident wrong labels | confident wrong *content* (hallucination) |

A spam filter is discriminative; a model that writes plausible emails is generative. They
are not rivals: a generative model can be turned into a classifier with Bayes' rule, and a
classifier's features are often reused inside generative systems (this module's reranker is
exactly that).

### 3.3 The probability distributions involved

For a sequence $x_{1:T}$ the joint distribution factorises by the chain rule:

$$
p(x_{1:T})=\prod_{t=1}^{T}p(x_t\mid x_{<t}).
$$

That single identity is the whole basis of autoregressive language modelling. Two other
objects appear constantly:

- **Marginal likelihood** $p(x)=\int p(x\mid z)p(z)\,dz$ — intractable when the latent $z$
  is high-dimensional, which is why VAEs use a bound.
- **Conditional likelihood with a temperature** $p_\tau(x_t)\propto \exp(z_t/\tau)$ — the
  knob that turns a sharp next-token distribution into a creative one (L11-02).

### 3.4 The families

| Family | Objective | Strength | Weakness |
| :--- | :--- | :--- | :--- |
| Autoregressive | $\sum_t\log p(x_t\mid x_{<t})$ | exact likelihood, strong at text | sequential sampling, slow |
| VAE | ELBO: reconstruction + KL | fast sampling, smooth latent space | blurry samples, posterior gap |
| GAN | $\min_G\max_D$ adversarial loss | sharp samples, one-step sampling | unstable, mode collapse |
| Diffusion | denoising score matching | stable training, excellent quality | many sampling steps |
| Flows / energy-based | exact likelihood or unnormalised density | invertibility / flexibility | architectural constraints |

### 3.5 Latent variable models and the ELBO

Assume data is generated from a latent $z$: $p(x)=\int p(x\mid z)p(z)\,dz$. The integral
has no closed form for a neural decoder, and sampling $z$ from the true posterior is also
hard. Introduce an approximate posterior $q(z\mid x)$ and use Jensen's inequality:

$$
\log p(x)=\log\mathbb{E}_{q}\!\left[\frac{p(x,z)}{q(z\mid x)}\right]
\;\ge\;\mathbb{E}_{q}\!\left[\log p(x\mid z)\right]-D_{\mathrm{KL}}\!\left(q(z\mid x)\,\|\,p(z)\right).
$$

The right-hand side is the **evidence lower bound**. The gap between it and $\log p(x)$ is
exactly $D_{\mathrm{KL}}(q(z\mid x)\|p(z\mid x))$: the better your approximate posterior,
the tighter the bound. Training maximises the bound, which means reconstructing well while
staying close to the prior.

### 3.6 Variational autoencoders

The encoder outputs $\mu$ and $\log\sigma^2$; sampling is pushed through the
**reparameterisation trick** $z=\mu+\sigma\odot\epsilon$ with $\epsilon\sim\mathcal N(0,I)$,
so gradients flow through the sampling step. The per-dimension KL against a standard normal
has a closed form:

$$
D_{\mathrm{KL}}=\tfrac12\sum_j\left(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2\right).
$$

**Worked numbers.** A latent dimension with $\mu=0.5$ and $\log\sigma^2=-1.0$ (so
$\sigma^2=0.3679$):

$$
D_{\mathrm{KL}}=\tfrac12\left(0.25+0.3679-1-(-1)\right)=\tfrac12(0.6179)=0.3090\ \text{nats}.
$$

A second dimension with $\mu=0,\ \log\sigma^2=0$ contributes exactly zero — the prior
already. This is why a trained VAE's per-dimension KL tells you which latents are actually
used. In this module's model, 7 of 8 latent dimensions have posterior standard deviation
above 0.1; the eighth has 0.091 and carries almost nothing.

### 3.7 Generative adversarial networks

A generator $G$ maps noise to data; a discriminator $D$ scores realism. The objective is

$$
\min_G\max_D\;\mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)]+\mathbb{E}_{z}[\log(1-D(G(z)))].
$$

At the optimum $D(x)=\tfrac12$ everywhere and the loss is
$\log\tfrac12+\log\tfrac12=-1.386$ nats. In practice you never reach it, and the failure to
watch for is **mode collapse**: the generator finds a few outputs that fool $D$ and stops
covering the distribution.

**Measured here.** 1,500 steps on 8×8 digits produced samples covering **3 of 10 classes**
with 68% of samples in one class, against 10 of 10 for the VAE. The discriminator ended at
0.87 on real data and 0.13 on fakes: it was still winning, and $G$ had collapsed into a
safe corner.

### 3.8 Diffusion models

Diffusion destroys data with a fixed noise schedule and learns to reverse it. With
$\beta_t\in(0,1)$, $\alpha_t=1-\beta_t$ and $\bar\alpha_t=\prod_{s\le t}\alpha_s$:

$$
q(x_t\mid x_0)=\mathcal N\!\left(\sqrt{\bar\alpha_t}\,x_0,\ (1-\bar\alpha_t)I\right),
\qquad
x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon .
$$

Training regresses the injected noise: $\mathcal L=\mathbb E\|\epsilon-\epsilon_\theta(x_t,t)\|^2$.
Sampling runs the reverse step

$$
x_{t-1}=\frac{1}{\sqrt{\alpha_t}}\left(x_t-\frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\,\epsilon_\theta(x_t,t)\right)+\sigma_t z .
$$

**Worked step.** Take $x_0=0.8$, $\bar\alpha_t=0.5$, $\epsilon=0.3$. Then
$x_t=0.7071(0.8)+0.7071(0.3)=0.5657+0.2121=0.7778$. With $\alpha_t=0.98$ and a perfect
predictor $\hat\epsilon=0.3$:

$$
x_{t-1}=\frac{0.7778-\frac{0.02}{0.7071}(0.3)}{0.98995}
=\frac{0.7778-0.00849}{0.98995}=0.7773 .
$$

One step barely moves the sample: the information is spread across all $T$ steps, which is
why diffusion is stable to train and expensive to sample.

### 3.9 Autoregressive models

Text models use the chain rule directly: one network, one token at a time, trained with
cross-entropy on every position (teacher forcing). Nothing about the architecture is
sequential — a transformer scores all positions in parallel during training — only sampling
is sequential.

**Perplexity** is the exponential of mean negative log-likelihood:
$\text{PPL}=\exp(-\frac1T\sum_t\log p(x_t\mid x_{<t}))$. Measured on three handbook
sections with distilgpt2: **46.35**, **59.26** and **131.97**. The last section ("laboratory
and workshop safety") is the hardest because its vocabulary — chemicals, defibrillators,
technicians — is rare in distilgpt2's web-text training data. A perplexity of 59.26 means
4.082 nats per token, i.e. an average per-token probability of $e^{-4.082}=0.0169$; a
ten-token sentence therefore has probability about $1.9\times10^{-18}$ under the model.
Large numbers of tiny probabilities are normal — that is what a joint distribution over
sequences looks like.

### 3.10 Modalities

| Modality | Usual representation | Dominant family | Note |
| :--- | :--- | :--- | :--- |
| Text | subword token ids | autoregressive transformer | discrete, exact likelihood |
| Image | VQ tokens or continuous latents | diffusion (quality), GAN (speed) | latent diffusion is the compromise |
| Audio | spectrogram frames or codec tokens | diffusion, autoregressive codecs | sample rate dominates cost |
| Video | space-time tokens | diffusion + temporal attention | compute-bound, evaluation weak |

## 4. Choosing a Family: A Decision Procedure

1. **Discrete or continuous output?** Discrete sequential data → autoregressive. Images and
   audio → diffusion is the default; GAN only if latency is the binding constraint.
2. **Do you need likelihoods?** Then autoregressive or flows; diffusion and GAN give scores
   only indirectly.
3. **What is the latency budget?** GAN: one pass. Diffusion: 20–1,000 passes. Autoregressive:
   one pass per token.
4. **How much data and compute?** VAEs and diffusion train reliably from small data; GANs
   need careful tuning at any scale.
5. **What does failure cost?** Blurry (VAE) is safer than confidently wrong (GAN/LLM).

## 5. Worked Examples

### Example 1 — the same task, two objectives

Given 8×8 digit images, a discriminative model learns $p(\text{digit}\mid\text{pixels})$ and
reaches high accuracy; it cannot produce a digit. The generative models in this module learn
$p(\text{pixels})$ and can sample, but their classification accuracy through Bayes' rule is
worse. The measured comparison of the three families, all trained on the same 1,797 images:

| Model | Training time | NN-MSE to real (lower is closer) | Classes covered | Max class share | Pairwise diversity |
| :--- | ---: | ---: | ---: | ---: | ---: |
| real data (reference) | — | 1.1082 | 10 | 0.10 | 9.3918 |
| VAE (30 epochs) | 12.4 s | 1.8006 | 10 | 0.24 | 1.8203 |
| GAN (1,500 steps) | 30.0 s | 5.4135 | 3 | 0.68 | 0.9635 |
| DDPM (1,500 steps) | 15.9 s | 3.0519 | 10 | 0.24 | 5.9105 |

Read this table the way you would read three students' coursework. The VAE produces
recognisable but averaged digits (low diversity, good coverage). The GAN produces sharp but
repetitive digits and misses seven classes — the classic collapse signature. The diffusion
model has the closest-to-real nearest-neighbour distance and the best diversity, at the cost
of 200 sequential sampling steps (0.7 s for 200 samples, so 3.5 ms per image on this CPU).

### Example 2 — an ELBO computed by hand

One image, one latent dimension. Reconstruction term $-3.2$ nats (a poor fit), KL $0.3090$.
The bound is $-3.2-0.309=-3.509$; the loss minimised in code is the negative of that,
$3.509$. The KL is small relative to reconstruction early in training, so the model first
learns to copy; as reconstruction improves, the KL term starts to bind and the latent space
organises itself. In the real run the final split was reconstruction **24.23** nats versus KL
**1.67** nats per image — the KL is deliberately small because $\beta=1$ weights it that way.

### Example 3 — what a GAN's losses do and do not tell you

At step 1,500: $D$ loss 0.351, $G$ loss 2.555, $D(\text{real})=0.870$, $D(\text{fake})=0.130$.
Both losses look "fine" — neither diverged — yet the samples cover three classes. The
metric that caught it was class coverage, not the loss. **Always report a coverage or
diversity metric alongside the adversarial loss.**

## 6. Mathematical Formulation

Autoregressive likelihood, ELBO, adversarial objective, diffusion forward/reverse and the
DDPM loss are stated in §3.3–3.9. Two practical additions:

**Temperature-scaled sampling.** With logits $z$ and temperature $\tau$:
$p_\tau=\mathrm{softmax}(z/\tau)$. As $\tau\to0$ it becomes argmax; as $\tau\to\infty$ it
becomes uniform. Measured on the same prompt, mean predictive entropy went from **0.00**
(greedy) through **3.63** ($\tau=1.0$) to **7.62** ($\tau=1.5$).

**Parameter count of a small VAE.** Encoder $64\to128\to128\to(8,8)$, decoder
$8\to128\to128\to64$: roughly $2\times(64\cdot128+128^2)+128\cdot16+128\cdot64\approx
58{,}000$ parameters. The whole module's generative experiments fit in a few seconds of CPU
because the data is 64-dimensional, not because the ideas are small.

## 7. Python Implementation

```python
# run from modules/M11-generative-ai-and-large-language-models/code
import torch
from gen_models import train_vae, vae_samples, train_gan, train_diffusion, sample_metrics, digits

X, y = digits(0)
v = train_vae()
print("VAE final loss", round(v["history"]["loss"][-1], 2),
      "recon", round(v["history"]["recon"][-1], 2),
      "KL", round(v["history"]["kl"][-1], 2))
s = vae_samples(v["model"], 300)
print("VAE samples", {k: round(val, 3) if isinstance(val, float) else val
                      for k, val in sample_metrics(s, X, y).items()})
```

```text
VAE final loss 25.9 recon 24.23 KL 1.67
VAE samples {'nn_mse': 1.8, 'nn_mse_median': 1.62, 'classes_seen': 10,
 'class_entropy': 2.19, 'max_class_share': 0.24, 'pairwise_mse': 1.82,
 'sample_mean': 0.302, 'real_mean': 0.305}
```

The GAN and diffusion models are trained by `train_gan()` and `train_diffusion()` with the
same interface; `sample_metrics` is the common judge. That shared metric is the reason the
comparison in Example 1 is fair.

## 8. Practical Applications

- **Text** — assistants, summarisation, code completion (autoregressive; the rest of this module).
- **Images** — product photography, medical augmentation, texture synthesis (diffusion; GAN where latency matters).
- **Audio** — speech synthesis and enhancement (diffusion and autoregressive codecs).
- **Tabular** — synthetic data for testing pipelines, with a privacy caveat: a generative model can memorise rows.
- **Science** — molecule and protein generation, where likelihood matters and evaluation is hard.

## 9. Common Mistakes

1. **Judging a generator by its loss.** GAN and diffusion losses are diagnostics, not quality.
2. **Sampling once and declaring victory.** Report coverage, diversity and nearest-neighbour distance.
3. **Comparing models trained on different data or budgets.** The table above uses one dataset, one split, one metric set.
4. **Forgetting the likelihood gap.** The ELBO is a bound; a high bound does not prove a good sampler.
5. **Ignoring memorisation.** Nearest-neighbour distance near zero means the model reproduced training data.
6. **Treating images and text as the same problem.** Discrete likelihoods and continuous densities are not interchangeable.
7. **Believing "generative" implies "truthful".** A model samples from what it learned, including the errors.

## 10. Practical Exercises

**Beginner**

1. Run `python gen_models.py` and copy the comparison table. Which model has the best class coverage per second of training?
2. Compute by hand the KL contribution of a latent dimension with $\mu=0$, $\log\sigma^2=1.0$.
3. For $\bar\alpha_t=0.25$ and $x_0=1.0$, compute $x_t$ with $\epsilon=-0.5$.

**Intermediate**

4. Train the VAE with `beta=4.0`. Report reconstruction MSE and how many latents stay active. Explain the trade-off.
5. Run the GAN for 4,000 steps and re-measure class coverage. Does collapse persist, and does the discriminator loss change?
6. Change the diffusion schedule to `beta_end=0.05` and report the sampling time and nearest-neighbour distance.

**Advanced**

7. Add a `sample_metrics` check to the GAN training loop every 200 steps and plot coverage against step. At which step does the generator commit to its first class?
8. Compute the FID-style distance between real and generated pixel statistics (mean and covariance) and compare it with the nearest-neighbour metric. Which is more sensitive to collapse?
9. Derive the DDPM reverse mean from the Gaussian posterior $q(x_{t-1}\mid x_t,x_0)$ and show it matches §3.8.

## 11. Self-Assessment

**Multiple choice**

1. A model that outputs $p(y\mid x)$ is
   a) generative. b) discriminative. c) a latent variable model. d) a diffusion model.
2. The ELBO is a lower bound on
   a) the reconstruction loss. b) $\log p(x)$. c) the KL divergence. d) the GAN objective.
3. The reparameterisation trick exists so that
   a) sampling is faster. b) gradients pass through a stochastic node. c) the prior is Gaussian. d) the decoder is linear.
4. Mode collapse is best detected by
   a) the discriminator loss. b) the generator loss. c) class coverage or diversity metrics. d) training time.
5. In DDPM, the network predicts
   a) the clean image. b) the added noise. c) the class label. d) the reverse schedule.

**Short answer**

6. Why does a diffusion model need many sampling steps while a GAN needs one?
7. State one reason a VAE's samples look blurrier than a GAN's.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **c**. 5. **b**.
6. Diffusion reverses a gradual noising process, so information is recovered a little at each of $T$ steps; a GAN learns a direct mapping from noise to data.
7. The VAE's Gaussian likelihood plus a KL to a broad prior averages over uncertainty, producing mean-looking outputs; the adversarial loss rewards sharpness instead.

</details>

## 12. Key Terms

**Generative model**, **discriminative model**, **joint distribution**, **marginal likelihood**,
**latent variable**, **evidence lower bound (ELBO)**, **KL divergence**, **reparameterisation
trick**, **variational autoencoder**, **generative adversarial network**, **minimax objective**,
**mode collapse**, **diffusion model**, **noise schedule**, **denoising**, **autoregressive
model**, **teacher forcing**, **perplexity**, **multimodal generation**.

## 13. Further Reading

- Kingma & Welling (2014). *Auto-Encoding Variational Bayes*. ICLR.
- Goodfellow et al. (2014). *Generative Adversarial Nets*. NeurIPS.
- Ho, Jain & Abbeel (2020). *Denoising Diffusion Probabilistic Models*. NeurIPS.
- Sohl-Dickstein et al. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*. ICML.
- Bengio, Courville & Vincent (2013). *Representation Learning: A Review and New Perspectives* — the clearest account of why generative modelling matters.

## What to Do Next

1. Run `python gen_models.py`; keep the table, you will reuse it in LAB-11-03.
2. Do exercises 1–3.
3. Continue to [L11-02 — Inside a Large Language Model](L11-02-inside-a-large-language-model.md).

---

**Navigation:** [← Module start](../README.md) · [Next: ? Lesson →](L11-02-inside-a-large-language-model.md)
