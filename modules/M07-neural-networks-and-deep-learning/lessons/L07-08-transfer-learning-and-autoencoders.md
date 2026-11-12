# L07-08 — Transfer Learning, Fine-Tuning and Autoencoders

[← Previous: ? Lesson](L07-07-attention-and-transformers.md) · [Module end](../README.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Transfer in Eight Steps](#4-the-procedure-transfer-in-eight-steps)
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

> **Module M07** · Lesson 8 of 8 · ~90 minutes · Level 300
> **Prerequisites:** L07-03, L07-05, L07-07

[Previous: L07-07](L07-07-attention-and-transformers.md) · [Module overview](../README.md) · [Back to Lesson 1](L07-01-from-perceptron-to-mlp.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** why features learned on one task transfer to another.
2. **Distinguish** feature extraction (frozen backbone) from fine-tuning.
3. **Implement** a head swap, freeze/unfreeze, and a discriminative learning rate.
4. **Measure** whether transfer actually helps, with seeds and a matched baseline.
5. **Recognise** catastrophic forgetting and negative transfer.
6. **Explain** autoencoders, the bottleneck, and reconstruction loss.
7. **Use** an autoencoder for anomaly detection and as a representation learner.

## 2. Prerequisite Knowledge

Convolutional layers and their parameter shapes (L07-05), the training loop (L07-03), and
train/validation/test discipline (M06). No new mathematics: transfer learning is a workflow, not a
formula.

## 3. Conceptual Explanation

### 3.1 Why transfer works

The first layers of a CNN learn edges, colour blobs and simple textures. Those features are useful
for leaves, cats and circuit boards alike — they are properties of natural images, not of the label
set. Later layers combine them into task-specific parts. So a network trained on 1.2 million
ImageNet photographs contains a great deal of reusable machinery for a 300-image plant-disease
problem.

The deeper the layer, the more task-specific its features. That single fact explains every
practical decision below: freeze early layers, adapt late ones gently.

### 3.2 The three workflows

| Workflow | What you train | When |
| :--- | :--- | :--- |
| **Train from scratch** | everything | plenty of labelled data, or no suitable pretrained model |
| **Feature extraction** | new head only, backbone frozen | small dataset, target similar to source |
| **Fine-tuning** | head + some/all backbone at a small learning rate | small-to-medium dataset, target close to source |

A fourth case exists: **domain-specific pretraining** — pretrain on unlabelled data from your own
domain (self-supervised), then fine-tune. This is what modern medical and remote-sensing models do
when ImageNet features are a poor match.

### 3.3 The mechanics

1. **Load** the pretrained weights into an architecture with the same backbone shapes.
2. **Replace the head**: the old head outputs 1,000 ImageNet classes; yours outputs 3.
   `load_state_dict(..., strict=False)` deliberately leaves the head's parameters at their random
   initialisation — they are the only ones that must change shape.
3. **Freeze** the backbone: `requires_grad = False` for its parameters.
4. **Train the head** for a few epochs. The features are fixed, so this is a linear (or shallow)
   probe.
5. **Unfreeze** and fine-tune everything at a learning rate 10–100× smaller than the head's, so the
   pretrained weights are nudged rather than destroyed.
6. Optionally unfreeze progressively, layer by layer, from the top down.

**Discriminative learning rates** — head at $10^{-3}$, backbone at $10^{-4}$ — are the standard way
to express step 5 in one optimizer. PyTorch takes parameter groups:

```python
optimizer = torch.optim.Adam([
    {"params": model.classifier.parameters(), "lr": 1e-3},
    {"params": model.features.parameters(), "lr": 1e-4},
])
```

### 3.4 What can go wrong

- **Negative transfer**: features from a distant domain hurt. Medical X-rays and ImageNet photos
  share little; a randomly initialised network can beat a badly matched pretrained one.
- **Catastrophic forgetting**: fine-tuning at a large learning rate overwrites the useful features.
  The symptom is a first-epoch collapse in validation accuracy.
- **Pretraining leakage**: if the pretraining corpus contains your test images (or near duplicates),
  your reported accuracy is inflated. Always check overlap and provenance.
- **Batch-norm statistics**: frozen backbones still update running statistics in `train()` mode.
  Either call `.eval()` on the frozen part, or leave the whole model in eval until you unfreeze.
- **Licence mismatch**: model weights carry their own licence, separate from the dataset's. A
  research-only checkpoint cannot ship in a commercial product.

### 3.5 Measuring whether transfer helped

A transfer-learning claim is only credible with three things:

1. **A matched baseline**: identical architecture, data, epochs and evaluation.
2. **Several seeds**: with 60 labels, one seed can swing accuracy by 40 points.
3. **A data-size sweep**: transfer should help most where labels are scarce, and its advantage
   should shrink as labels grow.

The experiment in §7 does exactly this, and the result is the lesson's main finding.

### 3.6 Autoencoders

An autoencoder learns to reconstruct its input through a narrow bottleneck:

$$
\mathcal{L}=\frac{1}{n}\sum_i\lVert x_i-\text{decoder}(\text{encoder}(x_i))\rVert^2 .
$$

The bottleneck forces the network to keep only what is needed to rebuild the input. There is no
label and no target other than the input itself, so this is **self-supervised** learning.

Three uses:

- **Compression / denoising**: 64 pixels → 8 numbers → 64 pixels.
- **Representation learning**: the 8-dimensional code can feed a classifier, a nearest-neighbour
  search or a visualisation.
- **Anomaly detection**: train on normal data only. Novel structure compresses badly, so the
  reconstruction error is a score. Pick a threshold from the normal-error distribution — for
  example its 95th percentile — and flag anything above it.

**Denoising autoencoders** corrupt the input (noise, masking) but reconstruct the clean version,
which forces robust features. **Variational autoencoders** (VAEs) additionally make the latent space
smooth and generative by predicting a distribution instead of a point; that is a separate lesson's
worth of material, but the bottleneck idea is the same.

## 4. The Procedure: Transfer in Eight Steps

1. Define the target task and split the data **before** touching any pretrained model.
2. Choose a source model whose input size, channel count and domain are compatible.
3. Check the licence of both the data and the weights.
4. Load the backbone with `strict=False` and confirm only the head is missing.
5. Freeze, train the head, record validation accuracy.
6. Unfreeze at a small learning rate; keep the best checkpoint by validation loss.
7. Compare against a scratch baseline with the same budget, averaged over ≥3 seeds.
8. Write down where transfer helped and where it did not.

## 5. Worked Examples

### Example 1 — Head swap

```python
state = torch.load("backbone.pt")
state = {k: v for k, v in state.items() if not k.startswith("classifier.4")}
model = SmallCNN(in_channels=1, n_classes=3, width=16, image_size=16)
missing, unexpected = model.load_state_dict(state, strict=False)
```

`missing` contains exactly the two head parameters (`classifier.4.weight`,
`classifier.4.bias`) and `unexpected` is empty. If `missing` lists convolutional weights, your
architectures do not match and nothing will transfer.

### Example 2 — Does transfer help? A data-size sweep

Pretrain on 3,000 synthetic texture images (ten classes, 16×16), then adapt to 3-class leaf images
with grayscale input. Accuracy on the held-out leaves, averaged over three seeds:

| Labelled leaves | From scratch | Frozen backbone | Fine-tuned |
| ---: | ---: | ---: | ---: |
| 60 | 0.502 | 0.756 | **0.769** |
| 150 | **0.938** | 0.836 | 0.947 |

Read the table carefully, because it is the honest version of the usual claim:

- With **60 labels** (20 per class), scratch training is unstable and averages 0.502, while the
  frozen and fine-tuned models reach 0.756 and 0.769. Per-seed scratch scores were 0.704, 0.315 and
  0.493 — one lucky run and two poor ones.
- With **150 labels**, scratch training catches up (0.938). Transfer no longer buys much.
- Fine-tuning beats freezing everywhere, but only slightly: with 60 labels the head is the
  bottleneck, not the features.

Transfer is a **data-efficiency** technique. Its value falls as labels accumulate.

### Example 3 — Autoencoder as an anomaly detector

Train on digits 0–7 only (1,920 images), then score all 2,400 images including unseen 8s and 9s:

```text
AE params: 4744
reconstruction error: normal 0.0187 unseen 0.0417
threshold 0.0316 flag rate on normal 0.05 recall on unseen 0.707
```

The unseen digits reconstruct about twice as badly. At a 95th-percentile threshold the detector
flags 5% of normal inputs (by construction) and catches 70.7% of the unseen class. That trade-off
is the whole design problem: lower the threshold and recall rises while false alarms rise too.

## 6. Mathematical Formulation

**Reconstruction loss** as in §3.6; the latent code is $z=\text{encoder}(x)\in\mathbb{R}^{k}$ with
$k\ll d$.

**Anomaly score** $s(x)=\lVert x-\hat{x}\rVert^2/d$, threshold $\tau=Q_{0.95}(s_{\text{normal}})$.

**Evaluation** of the detector at $\tau$: flag rate on normal data $=\alpha$ by construction;
recall on anomalies is measured, and precision is
$\frac{\text{TP}}{\text{TP}+\text{FP}}$ — which depends on the anomaly prevalence in deployment, not
on the training set. Report prevalence alongside.

**Fine-tuning objective** is the same cross-entropy as before but with an initialisation
$\theta_0=\theta_{\text{pretrained}}$ instead of random $\theta_0$, and a smaller step size.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
python transfer.py
```

The script (`transfer.py`) contains four reusable functions:

| Function | Purpose |
| :--- | :--- |
| `pretrain_on_textures` | train the source model, return weights without the head |
| `adapt` | build a 3-class model carrying those weights |
| `run_experiment` | one training run in `scratch` / `frozen` / `finetune` mode |
| `train_autoencoder` | train the bottleneck model on digits 0–7 |

Verified output:

```text
pretrained on textures: acc 1.0 params 38378
labels  scratch   frozen  finetune
    60    0.502    0.756     0.769
   150    0.938    0.836     0.947
AE params: 4744
reconstruction error: normal 0.0187 unseen 0.0417
threshold 0.0316 flag rate on normal 0.05 recall on unseen 0.707
```

Using the latent code as a feature vector:

```python
import numpy as np
import torch
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from transfer import train_autoencoder

model, flat, labels, normal = train_autoencoder(latent=8, epochs=20, seed=0)
with torch.no_grad():
    codes = model.encode(torch.as_tensor(flat)).numpy()
print("latent shape:", codes.shape)
print("1-NN on 8 latent numbers:", round(cross_val_score(KNeighborsClassifier(1), codes, labels, cv=3).mean(), 3))
print("1-NN on 64 pixels:      ", round(cross_val_score(KNeighborsClassifier(1), flat, labels, cv=3).mean(), 3))
```

```text
latent shape: (2400, 8)
1-NN on 8 latent numbers: 0.996
1-NN on 64 pixels:       1.0
```

Eight numbers instead of 64 preserve almost all of the neighbourhood structure (the same experiment
in `NB-07-03` reports 0.994 — retraining shifts the last digit), which is what a useful
representation means.

## 8. Practical Applications

- **Medical imaging** — pretrained backbones with a few hundred labelled scans.
- **Manufacturing inspection** — autoencoders on normal parts; reconstruction error flags defects.
- **Retail and fashion** — fine-tuned classifiers for catalogue attributes.
- **Audio and speech** — pretrained encoders fine-tuned for keyword spotting.
- **Tabular anomaly detection** — autoencoders or isolation forests over transaction features.

## 9. Common Mistakes

1. Reporting a single-seed transfer win when the baseline was simply unlucky.
2. Forgetting to re-initialise the head, so the model starts with 1,000-class weights.
3. Fine-tuning at the head's learning rate and destroying the features.
4. Loading weights with `strict=True` and "fixing" the error by renaming layers.
5. Leaving a frozen batch-norm layer in training mode so its statistics drift.
6. Pretraining on data that overlaps the test set.
7. Using an autoencoder threshold on a dataset whose anomaly prevalence differs from deployment and
   quoting precision without prevalence.
8. Ignoring the model-weights licence.

## 10. Practical Exercises

1. Run the sweep with 30 labelled leaves. How large is the transfer gain? How large is the seed
   variance?
2. Fine-tune at `lr=1e-2` and describe the first-epoch validation behaviour. Is it catastrophic
   forgetting?
3. Change the source task from textures to digits (`dd.digit_images(2000, size=16)`) and re-run.
   Does transfer still help? This is negative transfer in action.
4. Train the autoencoder with `latent=2` and plot the codes coloured by digit. Which digits collide?
5. Lower the anomaly threshold to the 80th percentile and recompute flag rate and recall.
6. Add Gaussian noise to the autoencoder's input while keeping clean targets. Does the 1-NN score
   on latent codes improve?

## 11. Self-Assessment

**Multiple choice**

1. Freezing the backbone means
   a) deleting its weights. b) setting `requires_grad = False`. c) using a smaller batch size.
   d) removing batch norm.
2. Transfer learning helps most when
   a) labels are plentiful. b) labels are scarce. c) source and target domains are unrelated.
   d) the head is randomly initialised and left untrained.
3. An autoencoder is trained with
   a) cross-entropy against labels. b) reconstruction loss against its own input. c) a contrastive
   loss only. d) no loss at all.
4. A 95th-percentile threshold on normal reconstruction error flags
   a) 5% of anomalies. b) 5% of normal inputs. c) exactly all anomalies. d) nothing.

**Short answer**

5. Give one reason a frozen backbone can outperform fine-tuning on a small dataset.
6. Why must you check for overlap between pretraining data and test data?

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Fine-tuning has many parameters and few labels, so it overfits or drifts; a frozen backbone plus a
   simple head has far less capacity to overfit.
6. Overlap leaks test information into the pretrained weights and inflates the measured accuracy;
   the model has effectively seen the test set.

</details>

## 12. Key Terms

**Transfer learning**, **feature extraction**, **fine-tuning**, **backbone**, **head**, **frozen
parameters**, **discriminative learning rate**, **negative transfer**, **catastrophic forgetting**,
**domain shift**, **autoencoder**, **bottleneck**, **latent code**, **reconstruction error**,
**denoising autoencoder**, **variational autoencoder**, **anomaly score**.

## 13. Further Reading

- Yosinski, J. et al. (2014). *How transferable are features in deep neural networks?* NeurIPS.
- Zhuang, F. et al. (2021). *A Comprehensive Survey on Transfer Learning*. Proceedings of the IEEE.
- Hinton, G. & Salakhutdinov, R. (2006). *Reducing the Dimensionality of Data with Neural Networks*.
  Science. — The autoencoder paper that restarted deep learning.
- Kingma, D. & Welling, M. (2014). *Auto-Encoding Variational Bayes*. ICLR.

## What to Do Next

1. Run `python transfer.py` and reproduce the table.
2. Do exercises 1–3; they are the ones that build judgement about transfer claims.
3. Continue to [LAB-07-03](../labs/lab-07-03-sentiment-forecasting-and-transfer.md), which combines
   sentiment classification, forecasting and transfer learning in one workflow.
4. Close the module with the [assignment](../assignments/asg-07-ablation-study.md) and
   [mini-project](../projects/mp-07-image-classifier-sprint.md).

---

**Navigation:** [← Previous: ? Lesson](L07-07-attention-and-transformers.md) · [Module end](../README.md)
