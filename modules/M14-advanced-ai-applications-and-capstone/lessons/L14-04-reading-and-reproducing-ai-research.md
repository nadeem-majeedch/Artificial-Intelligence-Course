# L14-04 — Reading and Reproducing AI Research

| | |
| :--- | :--- |
| Level | 400 |
| Study time | 90 minutes |
| Prerequisites | L14-01 to L14-03 |
| Code | `code/multimodal.py`, `code/graphs.py`, `code/federated.py` |

[← Previous: L14-03 Monitoring, Drift and Continuous Evaluation](L14-03-monitoring-drift-and-continuous-evaluation.md) · [Module home](../README.md) · [Next: L14-05 Capstone Studio: Scoping, Milestones and Defence →](L14-05-capstone-studio.md)

## On this page

- [Why this lesson exists](#why-this-lesson-exists)
- [What you will be able to do](#what-you-will-be-able-to-do)
- [1. How to read an applied AI paper](#1-how-to-read-an-applied-ai-paper)
- [2. Reproduction one: a contrastive vision-language model](#2-reproduction-one-a-contrastive-vision-language-model)
- [3. Reproduction two: a graph neural network](#3-reproduction-two-a-graph-neural-network)
- [4. Reproduction three: federated averaging](#4-reproduction-three-federated-averaging)
- [5. Emerging directions worth tracking](#5-emerging-directions-worth-tracking)
- [Common mistakes](#common-mistakes)
- [Exercises](#exercises)
- [Self-check](#self-check)
- [Key terms](#key-terms)
- [Further reading](#further-reading)

## Why this lesson exists

The advanced topics in this module — multimodal models, graph networks, federated learning,
speech, efficient inference — are moving faster than any textbook. The durable skill is not
knowing the current state of the art; it is being able to read a claim, reproduce a small
version of it, and notice when the reproduction disagrees.

This lesson reproduces three results at toy scale: a contrastive vision-language model, a graph
neural network, and federated averaging. Each reproduction is small enough to run in seconds and
honest enough to fail — and two of them *do* fail to reproduce the expected effect.

## What you will be able to do

1. Read a research claim and extract the smallest experiment that would test it.
2. Reproduce a contrastive vision-language model and evaluate it with the right metric.
3. Show when a graph network helps and when it hurts, using measured homophily.
4. Compare federated learning against centralised training and per-client baselines.
5. Describe the mechanism and evaluation of speech recognition and synthesis.
6. Say honestly what a toy reproduction does and does not establish.

---

## 1. How to read an applied AI paper

A paper makes four kinds of claim, and they need different evidence:

| Claim type | Example | What would support it |
| :--- | :--- | :--- |
| Existence | "this architecture can do X" | one worked example, a benchmark |
| Comparative | "better than the baseline" | same data, same budget, seeds, intervals |
| Mechanistic | "it works because of Y" | an ablation that removes Y |
| Generality | "works across domains" | multiple datasets, including one that fails |

Most papers establish existence and comparative claims. The generality claim is the one
practitioners need and the one least often tested.

**A reading checklist** (use it on the next paper you open):

1. What is the baseline, and is it tuned as hard as the proposed method?
2. What is the evaluation sample, and is it the deployment distribution?
3. Are there error bars, seeds, or repeated runs?
4. Which ablation isolates the claimed mechanism?
5. What does the limitations section actually concede?
6. Could you reproduce the headline number with the released code and data? If not, why not?

## 2. Reproduction one: a contrastive vision-language model

**The claim.** Two encoders trained on paired data, with a contrastive objective, learn a shared
space in which an image retrieves its caption and supports zero-shot classification of classes
never seen as labels.

**The smallest test.** 8×8 digits with templated captions, a bag-of-words text tower and a small
image tower; symmetric InfoNCE with temperature 0.07; 300 steps at batch 128.

**Measured.**

```text
  images 1,797, captions 1,797, vocabulary 22 words
  before training: i2t R@1 0.006, zero-shot accuracy 0.152
  after 300 steps: i2t R@1 0.024, i2t R@5 0.098, t2i R@1 0.019
  zero-shot digit accuracy: 0.904
  digit-level retrieval accuracy: 0.961 (worst class 8 at 0.87)
```

**What reproduced.** Zero-shot classification: 0.152 → 0.904 with no digit label ever supplied
to the text tower. The mechanism is exactly the paper's: the caption names the digit, and the
image tower inherits the class through the pairing.

**What did not reproduce — and why the metric was wrong.** Instance-level image-to-text R@1 is
0.024 against a chance level of about 0.028 (roughly 36 captions per digit in the test set). It
is *at chance*. The instinct is to call the model broken. The correct reading is that instance
retrieval is the wrong question for this data: dozens of captions describe the same digit, so
"retrieve the exact paired caption" is nearly impossible by construction. Digit-level retrieval,
0.961, is the meaningful measure.

**The lesson.** When a reproduction fails, first check whether the metric matches the data. A
metric whose ceiling is set by label ambiguity will make a working model look broken.

**What this does not establish.** Nothing about real images, open vocabulary, multiple objects,
or scale. It establishes the training signal, not the capability.

### Speech recognition and synthesis, briefly and accurately

The same encoder/decoder logic underlies the speech systems in this space, and the evaluation
vocabulary is worth knowing:

| Task | Architecture family | Standard metrics |
| :--- | :--- | :--- |
| Speech recognition (ASR) | acoustic encoder + CTC or attention decoder | word error rate (WER), character error rate (CER) |
| Text to speech (TTS) | text encoder + acoustic model + vocoder | mean opinion score (MOS), real-time factor (RTF) |
| Speech translation | ASR + MT, or end-to-end | BLEU plus WER on the transcript |

Two honest observations. First, WER is sensitive to normalisation (punctuation, casing, numbers),
so comparisons across papers are often not like-for-like. Second, MOS is a human rating with
wide variance; a TTS claim of "naturalness" with n=10 raters is a demonstration, not a result.

This module does not ship an ASR or TTS demo: audio dependencies are not part of the course
environment, and a toy vocoder would teach less than reading one paper's evaluation section
carefully. That is a scope decision, stated rather than hidden.

## 3. Reproduction two: a graph neural network

**The claim.** Message passing over a graph improves node classification over feature-only
models when neighbours are informative.

**Measured** (200 nodes, 5 classes, 12 noisy features, measured edge homophily **0.825**):

```text
  MLP (features only)      0.600
  GCN, 2 layers            1.000
  GCN, 4 layers            1.000
  GCN, 8 layers            0.250
```

The graph gain is +0.400. The 8-layer collapse to 0.250 is **oversmoothing**: repeated
neighbour averaging converges every node's representation toward the same vector, and the
classifier loses the ability to separate classes. Depth in a GNN is not free.

**The assumption, tested.** Homophily sweep, same generator, five graphs:

```text
   homophily     MLP   GCN-2    gain
         0.1   0.550   0.340  -0.210
         0.3   0.550   0.500  -0.050
         0.5   0.550   0.880  +0.330
         0.7   0.550   1.000  +0.450
         0.9   0.550   1.000  +0.450
```

Below roughly 0.5 the GNN is *worse* than ignoring the graph, because averaging over neighbours
mixes classes. The paper's claim is conditional on homophily; the condition is measurable, and
you should measure it before choosing the architecture.

## 4. Reproduction three: federated averaging

**The claim.** Averaging locally trained weights converges to a useful global model without
centralising data.

**Setup.** Ten clients, each holding two of ten digit classes (deliberately non-IID), five local
epochs per round, 50 rounds.

```text
  centralised (pooled)      0.917
  local only, mean          0.176 (min 0.131, max 0.202)
  FedAvg                    0.898 at round 50 (round 5: 0.276, round 25: 0.896)
  FedAvg + DP (sigma 0.02)  0.844 at round 50
```

**What reproduced.** FedAvg reaches 0.898 against 0.917 centralised, from clients that each see
20% of the label space and score 0.176 alone. The mechanism works.

**What the average hides.** Per-class accuracy of the federated model:

```text
  0:1.00  1:0.64  2:0.92  3:0.87  4:0.87  5:0.84  6:0.98  7:1.00  8:0.65  9:0.83
  spread: 0.364
```

A 0.36 spread across classes. The headline number is the mean; the harm is in the tail. Any
federated deployment should report per-client (or per-class) outcomes, not just the global
average — the clients with unusual data are the ones who paid for the average.

**On the DP variant.** Clipping at 1.0 and adding noise at sigma 0.02 costs 0.054 accuracy. That
is the only number in this reproduction that is a *cost* claim; there is no epsilon here, because
computing one requires a privacy accountant over the sampling process. Reporting "differentially
private" without an epsilon is a claim, not a guarantee.

## 5. Emerging directions worth tracking

Not a hype list — each entry names the open problem that would decide whether it matters.

| Direction | The open problem |
| :--- | :--- |
| Multimodal agents | grounding actions in perception, and evaluating them |
| Long-context models | whether attention over 1M tokens beats retrieval |
| Test-time compute | when more inference beats a bigger model |
| Mechanistic interpretability | whether features generalise across models |
| Federated + DP at scale | privacy budgets that survive many rounds |
| On-device learning | updating without catastrophic forgetting |
| Neuro-symbolic verification | guarantees that scale beyond toy policies |
| Data attribution | proving which training data caused an output |

A useful habit: for each, ask "what measurement would change my mind?" If nothing would, it is
marketing.

## Common mistakes

| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Reproducing the headline number only | misses the conditional claims | reproduce the ablation too |
| Trusting a metric whose ceiling is ambiguous | calls a working model broken | check the chance level |
| Assuming a GNN helps | measured −0.210 at low homophily | measure homophily first |
| Reporting only the federated average | hides a 0.36 per-class spread | report per-client results |
| Claiming DP without epsilon | unfalsifiable privacy claim | use an accountant |
| Reproducing at toy scale and generalising | overclaiming | state what the scale licenses |

## Exercises

**Beginner.** Run `python multimodal.py`. Record zero-shot accuracy before and after training,
and explain in one sentence why the text tower never sees a label.

**Beginner.** Run `python graphs.py`. Copy the homophily sweep and identify the crossover point.

**Intermediate.** In `graphs.py`, add a GraphSAGE-style mean aggregator without self-loops and
compare it against the GCN at homophily 0.1. Does the negative result persist?

**Intermediate.** In `federated.py`, change the client split so each client has five classes and
report the accuracy change. Is the gain from federation larger or smaller, and why?

**Advanced.** Reproduce one result from a recent paper at toy scale and write a 300-word
reproduction note: claim, smallest test, measured result, what reproduced, what did not, and
what the scale does not license.

**Advanced.** Design an evaluation for a speech interface in your capstone domain: which metric
(WER, MOS, task success), measured on what sample, with what acceptance threshold?

## Self-check

1. Name the four kinds of research claim and the evidence each needs.
2. Why was instance-level retrieval the wrong metric here?
3. What is oversmoothing, and at what depth did it appear?
4. Why should a federated system report per-client accuracy?
5. What is missing from a "differentially private" claim with no epsilon?

## Key terms

**Reproduction**, **ablation**, **contrastive learning**, **InfoNCE**, **zero-shot
classification**, **modality gap**, **message passing**, **homophily**, **oversmoothing**,
**FedAvg**, **non-IID**, **per-client fairness**, **WER**, **MOS**, **real-time factor**.

## Further reading

- Radford et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision*
  (CLIP).
- Kipf & Welling (2017). *Semi-Supervised Classification with Graph Convolutional Networks*.
- McMahan et al. (2017). *Communication-Efficient Learning of Deep Networks from Decentralized
  Data*.
- Li et al. (2020). *On the Convergence of FedAvg on Non-IID Data*.
- Pineau et al. (2021). *Improving Reproducibility in Machine Learning Research*.

---

[Previous: L14-03](L14-03-monitoring-drift-and-continuous-evaluation.md) · [Module home](../README.md) ·

---

**Navigation:** [← Previous: L14-03 Monitoring, Drift and Continuous Evaluation](L14-03-monitoring-drift-and-continuous-evaluation.md) · [Module home](../README.md) · [Next: L14-05 Capstone Studio: Scoping, Milestones and Defence →](L14-05-capstone-studio.md)
