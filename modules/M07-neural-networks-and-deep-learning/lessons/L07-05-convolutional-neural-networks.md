# L07-05 — Convolutional Neural Networks

[← Previous: L07-04](L07-04-regularisation-and-diagnosis.md) · [Module home](../README.md) · [Next: L07-06 →](L07-06-sequence-models-rnn-lstm-gru.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Designing a Small CNN](#4-the-procedure-designing-a-small-cnn)
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

> **Module M07** · Lesson 5 of 8 · ~90 minutes · Level 300
> **Prerequisites:** L07-02 to L07-04

[Previous: L07-04](L07-04-regularisation-and-diagnosis.md) · [Module overview](../README.md) · [Next: L07-06 →](L07-06-sequence-models-rnn-lstm-gru.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Compute** a 2D convolution by hand and state the output shape for any kernel, padding and
   stride.
2. **Explain** weight sharing, locality and translation equivariance, and what each one buys.
3. **Add** pooling and understand its effect on the receptive field and on spatial precision.
4. **Draw** a small CNN and count its parameters.
5. **Compare** MLP and CNN on the same images with accuracy, parameters and training time.
6. **Recognise** the design ideas in LeNet, VGG, ResNet and Inception, including residual
   connections and 1×1 convolutions.
7. **State** the limitations: fixed input size assumptions, cost, lack of rotation invariance,
   texture bias.

## 2. Prerequisite Knowledge

Matrix multiplication, the idea of a sliding window, and the training loop from L07-03. No prior
computer vision is assumed.

## 3. Conceptual Explanation

### 3.1 Why not a fully connected network?

An 8×8 grayscale image has 64 inputs, and an MLP handles that. A 256×256 RGB image has 196,608
inputs; one fully connected layer of 1,000 units would have 196 million parameters. Worse, the
network would have to learn that a cat in the top-left and a cat in the bottom-right are the same
thing, separately for every position.

Convolutions impose two priors:

- **Locality**: nearby pixels are more informative together than distant ones.
- **Weight sharing**: the same feature detector is applied at every position.

The result is far fewer parameters, translation equivariance (a shifted input produces a shifted
feature map), and better sample efficiency for images.

### 3.2 The convolution operation

For a single-channel image $I$ and kernel $K$ of size $k\times k$:

$$
(I * K)[i,j] = \sum_{u=0}^{k-1}\sum_{v=0}^{k-1} I[i+u,\,j+v]\,K[u,v].
$$

This is *cross-correlation* in signal-processing terms; deep-learning libraries call it
convolution and skip the kernel flip. With multiple input channels, the kernel has the same depth
and the products are summed over channels:

$$
\text{out}_c[i,j] = b_c + \sum_{c'}\sum_{u,v} X[c', i+u, j+v]\,K[c, c', u, v].
$$

**Output size** for input $W$, kernel $k$, padding $p$, stride $s$:

$$
W_{\text{out}} = \left\lfloor\frac{W + 2p - k}{s}\right\rfloor + 1.
$$

For an 8×8 input, 3×3 kernel, padding 1, stride 1: $(8+2-3)/1+1 = 8$ — "same" padding preserves
size. A 2×2 max pool with stride 2 halves it to 4.

**Parameter count** for a conv layer with $C_{\text{in}}$ inputs, $C_{\text{out}}$ filters, kernel
$k$: $C_{\text{out}}(C_{\text{in}}k^2+1)$. A 1→16 3×3 layer has $16(9+1)=160$ parameters, not
thousands.

### 3.3 Padding and stride

- **Valid** (no padding) shrinks the map and loses border information.
- **Same** padding keeps the size; standard in modern CNNs.
- **Stride > 1** downsamples inside the convolution instead of a separate pooling layer, which is
  common in modern architectures.

Padding matters because a corner pixel participates in one window while a centre pixel participates
in nine; without padding, border features are systematically under-represented.

### 3.4 Pooling

Max pooling takes the maximum in each window; average pooling takes the mean.

- Reduces spatial size and compute.
- Adds a small amount of translation invariance.
- Increases the **receptive field** of later layers: after two 2×2 pools, one unit sees roughly a
  4× larger region.
- Discards location information, which hurts tasks needing precise localisation (segmentation).

### 3.5 Receptive field

The receptive field is the region of the input that affects one output unit. With 3×3
convolutions and 2×2 pooling, it grows roughly as:

```text
conv3x3 → 3x3
pool2   → 4x4
conv3x3 → 8x8
pool2   → 10x10
```

Deep stacks see the whole image; early layers see edges. This hierarchy — edges, textures, parts,
objects — is what makes CNNs work, and it is learned, not programmed.

### 3.6 Architecture families

| Architecture | Year | Idea that lasted |
| :--- | ---: | :--- |
| LeNet-5 | 1998 | conv → pool → conv → pool → dense; the template |
| AlexNet | 2012 | ReLU, dropout, GPU training, data augmentation at scale |
| VGG | 2014 | stacks of 3×3 convolutions; depth with simplicity |
| Inception | 2014 | parallel filter sizes in one block; 1×1 convolutions for channel reduction |
| ResNet | 2015 | residual connections $y=x+F(x)$, enabling very deep networks |
| EfficientNet | 2019 | compound scaling of depth, width and resolution |

**Residual connections** deserve emphasis. A plain 50-layer network trains worse than a 20-layer
one, not because it lacks capacity but because optimisation degrades. Adding $x$ to the output gives
the gradient an identity path, so signals do not have to survive 50 multiplications. Every modern
architecture uses them.

**1×1 convolutions** mix channels without looking at neighbouring pixels — a learned linear
projection per position, used to reduce or expand channel counts cheaply.

### 3.7 What CNNs do not give you

- **Rotation invariance** is not built in; it must be learned or augmented.
- **Scale invariance** is partial.
- **Global context** requires depth or attention; a convolution is local by construction.
- **Texture bias**: CNNs often classify by texture rather than shape, which differs from human
  behaviour and matters for robustness.
- **Fixed-size assumptions** in the classifier head; adaptive pooling removes this but changes the
  model.

## 4. The Procedure: Designing a Small CNN

1. Input shape `(C, H, W)`; normalise pixels to [0,1] or standardise.
2. Block 1: Conv(3×3, same) → BatchNorm → ReLU → MaxPool(2).
3. Block 2: Conv(3×3) with double the channels → BatchNorm → ReLU → MaxPool(2).
4. Flatten → Linear(64) → ReLU → Dropout → Linear(classes).
5. Count parameters and compare with the dataset size.
6. Train with Adam 1e-3 and early stopping; plot curves.
7. Inspect the confusion matrix and misclassified images.
8. Only then add depth or width.

## 5. Worked Examples

### Example 1 — Convolution by hand

$$
I=\begin{bmatrix}1&2&0\\0&1&3\\2&1&0\end{bmatrix},
\qquad
K=\begin{bmatrix}1&0\\0&-1\end{bmatrix}.
$$

Valid convolution (stride 1):

- $(0,0)$: $1(1)+2(0)+0(0)+1(-1)=0$
- $(0,1)$: $2(1)+0(0)+1(0)+3(-1)=-1$
- $(1,0)$: $0(1)+1(0)+2(0)+1(-1)=-1$
- $(1,1)$: $1(1)+3(0)+1(0)+0(-1)=1$

$$
I*K=\begin{bmatrix}0&-1\\-1&1\end{bmatrix}.
$$

The kernel is a diagonal edge detector: it responds positively where the top-left is bright and the
bottom-right is dark, and negatively in the opposite case.

### Example 2 — Same images, two models

From `torch_utils.py`, five epochs, CPU, 1,800 training / 600 validation synthetic digits:

```text
model                    params  val acc  seconds
MLP 64-32                  2410    0.920     3.05
CNN width 16              13802    1.000     1.75
```

The CNN has six times the parameters but is faster per epoch here because the convolutions are
cheap at 8×8 and the model converges in fewer effective steps. The honest summary: for tiny images
the MLP is competitive and simpler; the gap grows with image size and with the need for translation
robustness.

### Example 3 — Parameter count, by hand

The CNN: Conv(1→16, 3×3) = 160; BatchNorm 32; Conv(16→32, 3×3) = 4,640; BatchNorm 64; Linear
(32×2×2=128 → 64) = 8,256; Linear(64→10) = 650. Total ≈ 13,802, matching `count_parameters`. Two
convolution layers account for a third of the weights; the dense head accounts for most of the
rest. At 32×32 input the dense head would dominate far more, which is why global average pooling
replaced it in modern designs.

## 6. Mathematical Formulation

Cross-correlation as in §3.2. With padding $p$ and stride $s$, output size as in §3.2.

**Receptive field** recurrence: $r_l = r_{l-1} + (k_l-1)\prod_{i<l}s_i$, starting from $r_0=1$.

**Max pool**: $\text{out}[i,j]=\max_{u,v} X[i\cdot s+u, j\cdot s+v]$.

**Residual block**: $y = f(x) + x$, requiring matching shapes (a 1×1 convolution adjusts channels
when they differ). Gradient: $\partial y/\partial x = \partial f/\partial x + I$, so the identity
term prevents the product of Jacobians from vanishing.

**Global average pooling**: $\text{out}_c=\frac{1}{HW}\sum_{i,j}X[c,i,j]$, which removes the
fixed-size dense head.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import torch
from torch import nn
from torch_utils import SmallCNN, Trainer, make_loader, count_parameters
import deep_data as dd

images, labels = dd.digit_images(2400, seed=0)
train_loader = make_loader(images[:1800], labels[:1800], 64, seed=0)
val_loader = make_loader(images[1800:], labels[1800:], 256, shuffle=False)

model = SmallCNN(in_channels=1, n_classes=10, width=16, image_size=8)
print([type(layer).__name__ for layer in model.features])
print([type(layer).__name__ for layer in model.classifier])
print("parameters:", count_parameters(model))

trainer = Trainer(model, patience=5)
trainer.fit(train_loader, val_loader, epochs=5, lr=1e-3)
loss, acc, preds, true = trainer.evaluate(val_loader)
print("validation accuracy:", round(acc, 3))
```

```text
['Conv2d', 'BatchNorm2d', 'ReLU', 'MaxPool2d', 'Conv2d', 'BatchNorm2d', 'ReLU', 'MaxPool2d']
['Flatten', 'Linear', 'ReLU', 'Dropout', 'Linear']
parameters: 13802
validation accuracy: 1.0
```

An output-shape check, which is worth doing before any long run:

```python
x = torch.randn(2, 1, 8, 8)
print("after features:", model.features(x).shape)   # (2, 32, 2, 2)
print("logits:", model(x).shape)                      # (2, 10)
```

## 8. Practical Applications

- **Medical imaging** — lesion detection; augmentation must respect anatomy (no vertical flips).
- **Manufacturing inspection** — defect segmentation on production lines.
- **Remote sensing** — land-cover classification from satellite tiles.
- **Agriculture** — plant-disease classification from leaf photographs (the lab scenario).
- **Audio** — spectrograms are images; the same blocks apply.

## 9. Common Mistakes

1. Forgetting the channel dimension: `(N, H, W)` instead of `(N, C, H, W)`.
2. Mismatched shapes in the dense head after pooling — compute the output size explicitly.
3. Using a large kernel where three 3×3 convolutions would do the same job with fewer parameters
   and more nonlinearity.
4. Applying dropout after every convolution; it often hurts in vision.
5. Augmenting with transformations that change the label (flipping digits 6 and 9).
6. Reporting accuracy on a balanced test set when deployment is imbalanced.
7. Training from scratch on 600 images and expecting transfer-learning performance.

## 10. Practical Exercises

1. Compute the output size for 32×32 input, 5×5 kernel, padding 2, stride 1; then stride 2.
2. Count the parameters of Conv(3→32, 5×5) and compare with Conv(3→32, 3×3) stacked twice.
3. Convolve a 4×4 image with a vertical-edge kernel and describe the response.
4. Train the CNN with and without batch norm at learning rate 1e-2. Compare stability.
5. Replace max pooling with average pooling and report the accuracy change.
6. Break the input shape deliberately and read the error message; write down what it tells you.

## 11. Self-Assessment

**Multiple choice**

1. Weight sharing in a convolution gives
   a) rotation invariance. b) translation equivariance and fewer parameters. c) larger inputs.
   d) better calibration.
2. A 3×3 convolution with padding 1 and stride 1 on a 16×16 input produces
   a) 14×14. b) 16×16. c) 18×18. d) 8×8.
3. Max pooling
   a) increases spatial resolution. b) reduces spatial size and increases the receptive field.
   c) adds parameters. d) replaces batch norm.
4. Residual connections mainly help
   a) regularisation. b) optimisation of deep networks. c) data augmentation. d) calibration.

**Short answer**

5. Why does a 1×1 convolution have parameters at all?
6. Give one task where pooling is a bad idea and explain why.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. It mixes channels: a 1×1 convolution with $C_{\text{in}}$ inputs and $C_{\text{out}}$ outputs has
   $C_{\text{out}}(C_{\text{in}}+1)$ parameters.
6. Semantic segmentation or keypoint detection: pooling discards the spatial precision those tasks
   need.

</details>

## 12. Key Terms

**Convolution**, **kernel/filter**, **stride**, **padding**, **feature map**, **channel**,
**pooling**, **receptive field**, **weight sharing**, **translation equivariance**, **residual
connection**, **1×1 convolution**, **global average pooling**, **LeNet**, **VGG**, **ResNet**,
**Inception**.

## 13. Further Reading

- LeCun, Y. et al. (1998). *Gradient-Based Learning Applied to Document Recognition*. Proceedings
  of the IEEE.
- Krizhevsky, Sutskever & Hinton (2012). *ImageNet Classification with Deep CNNs*. NeurIPS.
- He, K. et al. (2016). *Deep Residual Learning for Image Recognition*. CVPR.
- Dumoulin, V. & Visin, F. (2016). *A Guide to Convolution Arithmetic for Deep Learning*.

## What to Do Next

1. Run `python torch_utils.py` and compare the two model rows.
2. Do exercises 1–3.
3. Continue to [L07-06 — Sequence Models](L07-06-sequence-models-rnn-lstm-gru.md).

---

**Navigation:** [← Previous: L07-04](L07-04-regularisation-and-diagnosis.md) · [Module home](../README.md) · [Next: L07-06 →](L07-06-sequence-models-rnn-lstm-gru.md)
