# L07-04 — Regularisation, Dropout and Diagnosing a Deep Network

[← Previous: ? Lesson](L07-03-training-in-practice.md) · [Module home](../README.md) · [Next: ? Lesson →](L07-05-convolutional-neural-networks.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: A Regularisation Ablation](#4-the-procedure-a-regularisation-ablation)
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

> **Module M07** · Lesson 4 of 8 · ~90 minutes · Level 300
> **Prerequisites:** L07-03, M06 L06-06 (bias–variance)

[Previous: L07-03](L07-03-training-in-practice.md) · [Module overview](../README.md) · [Next: L07-05 →](L07-05-convolutional-neural-networks.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** dropout as training-time masking with inverted scaling, and why inference needs no
   mask.
2. **Apply** weight decay, early stopping, data augmentation and label smoothing, and say which
   failure each addresses.
3. **Describe** batch normalisation's forward computation, its train/eval difference, and its
   contested explanation.
4. **Diagnose** overfitting, underfitting, label noise and optimisation failure from loss curves and
   gradient norms.
5. **Run** an ablation that keeps every other variable fixed, and report what it establishes.
6. **Analyse** errors by class, confidence and slice instead of quoting one accuracy.

## 2. Prerequisite Knowledge

The bias–variance decomposition and the regularisation ideas from
[L06-06](../../M06-machine-learning-fundamentals/lessons/L06-06-bias-variance-and-regularisation.md),
plus the training loop from L07-03.

## 3. Conceptual Explanation

### 3.1 What regularisation is for

A network with enough parameters can fit random labels. Regularisation is any constraint that
makes fitting the training set harder in a way that helps on unseen data. It is not a single
technique but a family:

| Technique | Mechanism | Best against |
| :--- | :--- | :--- |
| Weight decay (L2) | penalise large weights | high variance, many parameters |
| Dropout | random unit masking | co-adaptation, small datasets |
| Early stopping | stop at best validation loss | over-training |
| Data augmentation | enlarge the effective dataset | small datasets, vision/audio |
| Label smoothing | soften targets | overconfidence, noisy labels |
| Smaller model | fewer parameters | high variance |
| Batch norm | rescale activations | optimisation instability |

### 3.2 Dropout

During training, each hidden unit is kept with probability $q$ and zeroed otherwise. With
**inverted dropout**, survivors are divided by $q$:

$$
\tilde h_i = \frac{m_i}{q}h_i, \qquad m_i\sim\text{Bernoulli}(q).
$$

Then $\mathbb{E}[\tilde h_i]=h_i$, so no rescaling is needed at inference. The original formulation
instead scaled by $q$ at test time; both are equivalent in expectation, but inverted dropout keeps
inference identical to a normal forward pass.

Two useful readings:

- **Ensemble view**: each mask defines a different sub-network; dropout trains many of them
  implicitly and averages at test time.
- **Noise view**: it stops a unit from relying on a specific partner unit, which is what
  "co-adaptation" means.

Dropout is applied to hidden activations, not to the output layer, and is disabled in `eval()`.
On convolutional networks, spatial dropout (dropping whole channels) is usually better than
dropping individual pixels.

### 3.3 Weight decay

Add $\lambda\lVert\theta\rVert_2^2$ to the loss, or equivalently multiply weights by
$(1-\eta\lambda)$ each step. It keeps the function smoother and prevents any single weight from
dominating. In Adam, "AdamW" decouples the decay from the adaptive scaling; the difference matters
at scale but is a refinement, not a different idea.

### 3.4 Early stopping

Track validation loss each epoch, keep the best state dict, and stop after `patience` epochs without
improvement. It is free, requires no gradient change, and is the regulariser most often omitted.
Its weakness: the validation set is now used for model selection, so the test set must stay
untouched.

### 3.5 Batch normalisation

For a mini-batch, standardise each channel/feature, then apply a learned scale and shift:

$$
\hat x = \frac{x-\mu_B}{\sqrt{\sigma_B^2+\epsilon}},
\qquad
y = \gamma\hat x+\beta.
$$

- **Training**: $\mu_B,\sigma_B$ from the current batch; running averages are updated for inference.
- **Evaluation**: use the running averages, not the current batch. This is why `model.eval()`
  matters and why a batch of one behaves differently in train mode.
- **Why it helps**: originally explained as reducing "internal covariate shift"; later work showed
  the main benefit is a smoother optimisation landscape, allowing larger learning rates.
- **Caveats**: it interacts badly with very small batches, adds a train/test discrepancy, and is
  often replaced by LayerNorm outside vision.

### 3.6 Data augmentation and label smoothing

Augmentation encodes known invariances: small translations, flips, crops, colour jitter for
images; time warping and masking for audio; token deletion for text. It is the highest-value
regulariser when data are scarce, because it adds information rather than restricting the model.

Label smoothing replaces a one-hot target with

$$
y_k^{\text{smoothed}} = (1-\epsilon)y_k + \frac{\epsilon}{K},
$$

which stops the network from driving logits to infinity and improves calibration. With genuinely
noisy labels, smoothing or robust losses (Huber, symmetric cross-entropy) are appropriate.

### 3.7 Diagnosis from curves

```text
train ↓  val ↓  small gap      → healthy; stop when val flattens
train ↓  val ↑                 → overfitting; regularise or add data
both flat and high             → underfitting or a bug
train stuck at chance          → check labels, loss, learning rate, gradients
val better than train          → augmentation is active in train, or leakage
```

Always look at both curves and at the gap, not at a single final number. A model at 0.99 train /
0.70 val is a different product from 0.75 / 0.73.

### 3.8 Error analysis

1. Confusion matrix by class.
2. Accuracy as a function of confidence (are the wrong ones confident?).
3. Slices: class, subgroup, acquisition source, difficulty.
4. Inspect individual failures. In image tasks, ask whether a human could label them.
5. Check for label errors; in small datasets they are common and they cap achievable accuracy.

### 3.9 Class imbalance in deep learning

Same tools as classical ML, plus two more: class-weighted cross-entropy and focal loss, which
down-weights easy examples. Report per-class recall, not accuracy.

## 4. The Procedure: A Regularisation Ablation

1. Fix the split, the seed, the architecture and the optimiser.
2. Establish the unregularised baseline and its train/validation gap.
3. Change **one** thing: dropout, weight decay, augmentation or capacity.
4. Train with early stopping; record best validation loss and the epoch it occurred.
5. Repeat for three seeds and report mean ± spread. A single run cannot distinguish a real effect
   from seed noise.
6. Keep the change only if the improvement exceeds the seed spread.
7. Report the test score once, for the chosen configuration.

## 5. Worked Examples

### Example 1 — Label noise makes regularisation visible

300 training images, 30% of labels randomly flipped, 60 epochs, MLP 64–128–10:

```text
config        train acc  val acc
base             0.760    0.870
dropout 0.5      0.710    0.890
weight decay     0.703    0.874
hidden 32        0.680    0.853
```

The ceiling is about 0.90 because 30% of the training labels are wrong; the network cannot fit
noise and truth simultaneously. Dropout gains two points over the base, weight decay less, and
shrinking the model costs accuracy. On a clean dataset these differences would be within seed
noise — which is the lesson: **regularisation only helps when there is something to regularise.**

### Example 2 — Reading a gap

A run reports train 1.000, validation 0.870, and validation loss rising after epoch 12. The
diagnosis is overfitting with early stopping already available: keep the epoch-12 weights. Adding
dropout might raise the ceiling, but first ask whether the training set is simply too small.

### Example 3 — Batch norm at inference

A model trained with batch norm and batch size 64 is evaluated one image at a time. In `train()`
mode, each single-image batch has zero variance, so the normalisation divides by $\epsilon$ and the
predictions are nonsense. In `eval()` mode the running statistics are used and the predictions are
correct. Forgetting `model.eval()` is the most common cause of "the model works in the notebook but
not in deployment".

## 6. Mathematical Formulation

**Dropout expectation**: with mask $m_i\sim\text{Bernoulli}(q)$ and scaling $1/q$,
$\mathbb{E}[\tilde h_i]=h_i$.

**L2 regularised objective**:
$L_{\text{reg}}=L(\theta)+\frac{\lambda}{2}\lVert\theta\rVert_2^2$, with gradient
$\nabla L+\lambda\theta$.

**Batch norm** as in §3.5, with running estimates
$\mu_{\text{run}}\leftarrow(1-\alpha)\mu_{\text{run}}+\alpha\mu_B$.

**Label smoothing** cross-entropy:
$L=-(1-\epsilon)\log p_y-\frac{\epsilon}{K}\sum_k\log p_k$.

**Focal loss**: $L=-\alpha_t(1-p_t)^\gamma\log p_t$, which reduces the contribution of
well-classified examples.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import numpy as np
import deep_data as dd
from torch_utils import MLP, Trainer, make_loader, set_seed

X, y = dd.digit_images(1600, seed=0)
rng = np.random.default_rng(1)
noisy = y[:300].copy()
flip = rng.random(300) < 0.30
noisy[flip] = (noisy[flip] + rng.integers(1, 10, flip.sum())) % 10

train_loader = make_loader(X[:300], noisy, 32, seed=0)
val_loader = make_loader(X[300:], y[300:], 256, shuffle=False)

for name, model, kwargs in [
    ("base", MLP(64, (128,), 10), {}),
    ("dropout 0.5", MLP(64, (128,), 10, dropout=0.5), {}),
    ("weight decay", MLP(64, (128,), 10), {"weight_decay": 1e-2}),
    ("hidden 32", MLP(64, (32,), 10), {}),
]:
    set_seed(0)
    trainer = Trainer(model, patience=15)
    trainer.fit(train_loader, val_loader, epochs=60, lr=1e-3, **kwargs)
    _, val_acc, _, _ = trainer.evaluate(val_loader)
    _, train_acc, _, _ = trainer.evaluate(train_loader)
    print(f"{name:14s} train {train_acc:.3f} val {val_acc:.3f}")
```

```text
base           train 0.760 val 0.870
dropout 0.5    train 0.710 val 0.890
weight decay   train 0.703 val 0.874
hidden 32      train 0.680 val 0.853
```

Batch norm and dropout in one model, and the train/eval trap:

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Flatten(), nn.Linear(64, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.5),
    nn.Linear(64, 10),
)
x = torch.as_tensor(X[:1])
model.train()
print("train-mode logits:", model(x).detach().numpy().round(3))
model.eval()
print("eval-mode logits: ", model(x).detach().numpy().round(3))
```

The two lines differ because batch norm uses batch statistics in train mode and running statistics
in eval mode, and dropout is active only in train mode. Neither output is "wrong"; they answer
different questions.

## 8. Practical Applications

- **Medical imaging** — augmentation (rotations, flips with anatomical care), strong early stopping,
  and per-subgroup error reporting.
- **Speech** — SpecAugment masks time and frequency bands; it is often worth more than a larger
  model.
- **Recommendation** — dropout on embeddings prevents memorising individual users.
- **Fine-tuning** — small learning rates plus early stopping are the main defence against
  catastrophic forgetting (L07-08).

## 9. Common Mistakes

1. Leaving dropout on at inference (`model.train()` during evaluation).
2. Applying dropout to the output layer.
3. Using batch norm with batch size 1 in train mode.
4. Adding regularisation before checking for label noise or a broken pipeline.
5. Comparing single runs with different seeds and calling the difference an effect.
6. Augmenting with transformations that change the label (flipping digits, mirroring text).
7. Reporting accuracy on imbalanced classes.

## 10. Practical Exercises

1. Reproduce the ablation table at three seeds and report mean ± spread.
2. Increase label noise to 50% and re-run. At what noise level does dropout stop helping?
3. Train with and without batch norm at learning rate $10^{-2}$; compare stability.
4. Add random translations of ±2 pixels as augmentation and measure validation accuracy on clean
   digits.
5. Build a confusion matrix for the best model and identify the two most confused classes.

## 11. Self-Assessment

**Multiple choice**

1. Inverted dropout scales surviving activations by
   a) $q$. b) $1/q$. c) $1-q$. d) nothing.
2. Batch norm uses running statistics
   a) in training. b) at evaluation. c) never. d) only with dropout.
3. Early stopping is a form of
   a) data augmentation. b) regularisation. c) initialisation. d) normalisation.
4. Label smoothing primarily improves
   a) training speed. b) calibration and overconfidence. c) batch norm. d) gradient clipping.

**Short answer**

5. Why is "val better than train" usually a sign of augmentation or leakage rather than skill?
6. Your model has train 0.99 and val 0.62. Give two fixes and one thing you would check first.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Training applies augmentation and dropout (harder task), while validation does not; if neither is
   active, the split is probably leaking.
6. Add regularisation or data, reduce capacity; first check the split and label quality.

</details>

## 12. Key Terms

**Regularisation**, **dropout**, **inverted dropout**, **co-adaptation**, **weight decay**,
**early stopping**, **patience**, **batch normalisation**, **running statistics**, **layer
normalisation**, **data augmentation**, **label smoothing**, **focal loss**, **ablation study**,
**error analysis**, **calibration**.

## 13. Further Reading

- Srivastava, N. et al. (2014). *Dropout: A Simple Way to Prevent Neural Networks from
  Overfitting*. JMLR.
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization*. ICML; and Santurkar et al. (2018),
  *How Does Batch Normalization Help Optimization?* NeurIPS.
- Müller, R., Kornblith, S. & Hinton, G. (2019). *When Does Label Smoothing Help?* NeurIPS.

## What to Do Next

1. Run the ablation script and compare with §5.
2. Do exercises 1–3.
3. Continue to [L07-05 — Convolutional Neural Networks](L07-05-convolutional-neural-networks.md).

---

**Navigation:** [← Previous: ? Lesson](L07-03-training-in-practice.md) · [Module home](../README.md) · [Next: ? Lesson →](L07-05-convolutional-neural-networks.md)
