# L07-02 — Backpropagation: The Mathematics of Learning

[← Previous: L07-01](L07-01-from-perceptron-to-mlp.md) · [Module home](../README.md) · [Next: L07-03 →](L07-03-training-in-practice.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Deriving Backprop for a New Layer](#4-the-procedure-deriving-backprop-for-a-new-layer)
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

> **Module M07** · Lesson 2 of 8 · ~90 minutes · Level 300
> **Prerequisites:** L07-01, P02 (chain rule)

[Previous: L07-01](L07-01-from-perceptron-to-mlp.md) · [Module overview](../README.md) · [Next: L07-03 →](L07-03-training-in-practice.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Draw** the computation graph of a small network and label every intermediate value.
2. **Derive** the backward pass with the chain rule, for one unit and in matrix form.
3. **Compute** a full forward and backward pass by hand for a 2–2–1 network.
4. **Explain** why softmax with cross-entropy has the gradient $p-y$, and why that is convenient.
5. **Implement** backpropagation in NumPy and check it against finite differences.
6. **Diagnose** vanishing and exploding gradients from the product of Jacobians.

## 2. Prerequisite Knowledge

You need the chain rule for composed functions, the derivative of sigmoid and tanh, and matrix
multiplication shapes. The whole of backpropagation is the chain rule applied systematically; if
the chain rule is shaky, nothing below will feel obvious.

## 3. Conceptual Explanation

### 3.1 The problem

Training minimises a loss $L(\theta)$ over all parameters $\theta$. Gradient descent needs
$\partial L/\partial \theta$ for every parameter. A network may have millions of parameters and
dozens of layers. Numerical differentiation would cost two forward passes per parameter —
impossible. Backpropagation computes **all** gradients in roughly the cost of one forward pass,
by reusing intermediate results.

### 3.2 The computation graph

For a two-layer network:

```text
x ──► z1 = W1ᵀx + b1 ──► h = f(z1) ──► z2 = W2ᵀh + b2 ──► a = softmax(z2) ──► L(a, y)
```

Each node is a simple function; each edge carries a value forward. Backpropagation walks the
graph backwards, computing "how much does $L$ change if this node changes?" — the **local
gradient** — and multiplies by the gradient flowing in from the right.

### 3.3 The chain rule, written for a network

Define the error signal at layer $l$ as

$$
\boldsymbol{\delta}^{(l)} = \frac{\partial L}{\partial \mathbf{z}^{(l)}}.
$$

Then, for a softmax/cross-entropy output,

$$
\boldsymbol{\delta}^{(L)} = \mathbf{p} - \mathbf{y},
$$

and for earlier layers,

$$
\boldsymbol{\delta}^{(l)} = \big(\mathbf{W}^{(l+1)\top}\boldsymbol{\delta}^{(l+1)}\big)
\odot f'(\mathbf{z}^{(l)}),
$$

where $\odot$ is elementwise multiplication. The parameter gradients are

$$
\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \mathbf{a}^{(l-1)}\,\boldsymbol{\delta}^{(l)\top},
\qquad
\frac{\partial L}{\partial \mathbf{b}^{(l)}} = \boldsymbol{\delta}^{(l)}.
$$

That is the whole algorithm. Everything else is bookkeeping.

### 3.4 Why softmax + cross-entropy simplifies

For one example with logits $z_k$,

$$
p_k = \frac{e^{z_k}}{\sum_j e^{z_j}},
\qquad
L = -\log p_y.
$$

Differentiating gives

$$
\frac{\partial L}{\partial z_k} = p_k - \mathbb{1}[k=y].
$$

The softmax Jacobian and the log cancel. This is not luck: cross-entropy is the negative
log-likelihood of a categorical distribution, and softmax is its canonical link. Using MSE with
softmax instead leaves a factor of $p_k(1-p_k)$ in the gradient, which is small exactly when the
model is confidently wrong — the worst possible time to learn slowly.

### 3.5 Vanishing and exploding gradients

The backward pass multiplies a Jacobian at every layer. If each factor has norm below 1, the
product decays exponentially with depth; above 1, it explodes.

- Sigmoid derivative ≤ 0.25, so a 20-layer sigmoid stack multiplies by at most $0.25^{20}\approx
  10^{-12}$. Early layers barely learn.
- ReLU keeps the derivative at 1 for active units, which is why it replaced sigmoid.
- Large weights or deep recurrent unrolls produce exploding gradients; gradient clipping caps the
  norm.
- Residual connections (L07-05 onwards) give gradients a short path to earlier layers.
- Batch normalisation rescales activations, which conditions the Jacobians.

### 3.6 Loss functions

| Loss | Formula | Task |
| :--- | :--- | :--- |
| MSE | $\frac1n\sum(\hat y-y)^2$ | regression |
| MAE | $\frac1n\sum\lvert\hat y-y\rvert$ | regression, outlier-robust |
| Binary cross-entropy | $-\frac1n\sum[y\log p+(1-y)\log(1-p)]$ | binary |
| Cross-entropy | $-\frac1n\sum\log p_{y_i}$ | multiclass |
| Huber | quadratic near 0, linear beyond | regression with outliers |

### 3.7 Gradient checking

Replace each analytic derivative with a central difference:

$$
\frac{\partial L}{\partial \theta_i} \approx \frac{L(\theta_i+\epsilon)-L(\theta_i-\epsilon)}{2\epsilon},
\quad \epsilon\approx10^{-6}.
$$

The relative error should be below $10^{-6}$ for float64. A value around $10^{-2}$ means a bug in
the backward pass. The module's check reports **1.18e-08**, which is as close as floating point
allows.

## 4. The Procedure: Deriving Backprop for a New Layer

1. Write the forward function and the shapes of every intermediate.
2. Write the local derivative of the layer's output with respect to its input and parameters.
3. Receive $\partial L/\partial \text{output}$ from the layer above.
4. Multiply: $\partial L/\partial \text{input} = (\partial \text{output}/\partial \text{input})^\top
   \partial L/\partial \text{output}$.
5. Accumulate parameter gradients over the batch.
6. Check numerically on a small batch before training anything.
7. Only then optimise.

## 5. Worked Examples

### Example 1 — Full forward and backward pass, by hand

Network: 2 inputs, 2 sigmoid hidden units, 1 sigmoid output, MSE loss.

$$
\mathbf{x}=(1,0.5),\quad
\mathbf{W}_1=\begin{bmatrix}0.2&-0.1\\0.4&0.3\end{bmatrix},\quad
\mathbf{b}_1=(0.1,-0.2),
$$
$$
\mathbf{W}_2=(0.5,-0.6),\quad b_2=0.05,\quad y=1.
$$

**Forward**

$$
\mathbf{z}_1=(0.5,\,-0.15),\quad
\mathbf{h}=(0.622459,\,0.462570),
$$
$$
z_2 = 0.5(0.622459)-0.6(0.462570)+0.05 = 0.083688,
\quad a=\sigma(z_2)=0.520910,
$$
$$
L=\tfrac12(a-y)^2 = \tfrac12(-0.479090)^2 = 0.114764.
$$

**Backward**

$$
\frac{\partial L}{\partial a}=a-y=-0.479090,
\qquad
\frac{\partial L}{\partial z_2}=(-0.479090)(0.520910)(0.479090)=-0.119563.
$$

So $\partial L/\partial W_2 = (-0.119563)(0.622459,\ 0.462570) = (-0.074423,\ -0.055306)$ and
$\partial L/\partial b_2=-0.119563$.

Into the hidden layer:

$$
\frac{\partial L}{\partial \mathbf{h}} = (-0.119563)(0.5,\,-0.6) = (-0.059782,\ 0.071738),
$$
$$
\frac{\partial L}{\partial \mathbf{z}_1} = (-0.059782,\ 0.071738)\odot(0.235003,\ 0.248604)
= (-0.014049,\ 0.017834).
$$

Finally

$$
\frac{\partial L}{\partial \mathbf{W}_1}
= \mathbf{x}\,\boldsymbol{\delta}_1^\top
= \begin{bmatrix}-0.014049&0.017834\\-0.007024&0.008917\end{bmatrix},
\qquad
\frac{\partial L}{\partial \mathbf{b}_1}=(-0.014049,\ 0.017834).
$$

Every number can be recomputed with a calculator, which is the point: backpropagation is
arithmetic, not magic.

### Example 2 — What the signs mean

The gradient for $W_2[1]$ is negative, so a gradient-descent step *increases* the first output
weight. Increasing it raises $z_2$, which raises $a$ toward the target 1, which lowers the loss. The
sign is checkable by reasoning about the forward pass, and doing so is a good way to catch a
transposed matrix.

### Example 3 — Gradient check catches the classic bug

If you forget to transpose $W^{(l+1)}$ in the backward pass, the shapes may still broadcast on a
square matrix and training may even appear to work for a while. The gradient check does not care
about plausibility: the analytic and numerical values disagree by orders of magnitude, and it
fails immediately.

```text
gradient check (max relative error): 1.18e-08
```

## 6. Mathematical Formulation

For a layer $l$ with activation $f$ and batch size $n$:

$$
\mathbf{Z}^{(l)} = \mathbf{A}^{(l-1)}\mathbf{W}^{(l)} + \mathbf{1}\mathbf{b}^{(l)\top},
\qquad
\mathbf{A}^{(l)} = f(\mathbf{Z}^{(l)}).
$$

Backward, with $\boldsymbol{\Delta}^{(l)} = \partial L/\partial \mathbf{Z}^{(l)}$:

$$
\boldsymbol{\Delta}^{(L)} = \frac{1}{n}(\mathbf{P}-\mathbf{Y}),
\qquad
\boldsymbol{\Delta}^{(l)} = \big(\boldsymbol{\Delta}^{(l+1)}\mathbf{W}^{(l+1)\top}\big)\odot
f'(\mathbf{Z}^{(l)}),
$$
$$
\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \mathbf{A}^{(l-1)\top}\boldsymbol{\Delta}^{(l)},
\qquad
\frac{\partial L}{\partial \mathbf{b}^{(l)}} = \sum_i \boldsymbol{\Delta}^{(l)}_i.
$$

**Complexity.** One forward pass costs $O(\sum_l n_{l-1}n_l)$; the backward pass costs a constant
factor more. Memory stores every intermediate activation, which is why large models are
memory-bound and why checkpointing exists.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import numpy as np
from nn_numpy import MLP, gradient_check
import deep_data as dd

X, y = dd.digit_images(200)
X = X.reshape(len(X), -1)
net = MLP([64, 32, 10], seed=0)
print("max relative gradient error:", f"{gradient_check(net, X[:32], y[:32]):.2e}")
```

```text
max relative gradient error: 1.18e-08
```

The same gradient with PyTorch's autograd:

```python
import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(2, 4), nn.Tanh(), nn.Linear(4, 2))
x = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
target = torch.tensor([0, 1, 1, 0])

loss_fn = nn.CrossEntropyLoss()
output = model(x)
loss = loss_fn(output, target)
loss.backward()
print("loss:", round(loss.item(), 4))
print("dL/dW1:", model[0].weight.grad.numpy().round(4))
```

```text
loss: 0.7111
dL/dW1: [[-0.0081  0.0031]
 [-0.0300 -0.0293]
 [-0.0018  0.0007]
 [ 0.0040 -0.0012]]
```

PyTorch builds the graph during the forward call and replays it backwards. The numbers are the
same chain rule you applied by hand; `.backward()` is the loop in §3.3, written by someone else.

## 8. Practical Applications

- **Every deep model** uses this algorithm; there is no alternative at scale.
- **Custom layers** require a correct backward pass, which is why gradient checking is part of the
  development loop, not an academic exercise.
- **Scientific computing** uses the same reverse-mode differentiation for sensitivity analysis.
- **Debugging training** often means inspecting gradient norms per layer; a layer whose gradient is
  $10^{-9}$ is not learning.

## 9. Common Mistakes

1. **Forgetting the transpose** in $\mathbf{W}^\top\boldsymbol{\delta}$. Shapes may broadcast;
   gradients will be wrong.
2. **Applying the derivative of the output activation twice.** With softmax + cross-entropy, the
   combined gradient is already $p-y$.
3. **Not zeroing gradients** between steps in a framework. PyTorch accumulates by default.
4. **Using float32 for a gradient check.** The tolerance is too tight; use float64.
5. **Treating a small loss as proof of correctness.** A model can fit the wrong labels perfectly.
6. **Ignoring gradient norms.** Vanishing gradients look like "the model stopped learning" with no
   error message.

## 10. Practical Exercises

1. Reproduce Example 1 with a script and confirm every gradient to six decimals.
2. Change the loss to MSE on the sigmoid output and re-derive $\partial L/\partial z_2$. Compare
   the gradient magnitude with the cross-entropy version.
3. Break the transpose in your NumPy implementation deliberately and report the gradient-check
   value.
4. Build a 10-layer sigmoid network and a 10-layer ReLU network. Compare the gradient norm at the
   first layer after one backward pass.
5. Derive the backward pass for a mean-pooling layer (average of a 2×2 block).

## 11. Self-Assessment

**Multiple choice**

1. Backpropagation computes gradients
   a) approximately. b) in about the cost of one forward pass. c) with finite differences.
   d) only for convex losses.
2. With softmax and cross-entropy, $\partial L/\partial z$ equals
   a) $p-y$. b) $p(1-p)(p-y)$. c) $y-p$. d) $p$.
3. A vanishing gradient is caused by
   a) too small a batch. b) repeated multiplication by Jacobians with norm below 1.
   c) too few epochs. d) a large learning rate.
4. PyTorch accumulates gradients unless you
   a) call `.backward()`. b) zero them. c) use a scheduler. d) freeze layers.

**Short answer**

5. Why is the backward pass roughly the same cost as the forward pass?
6. Your gradient check reports 0.03 relative error. What do you do?

<details>
<summary>Answers</summary>

1. **b**. 2. **a**. 3. **b**. 4. **b**.
5. Each node's local derivative is reused for all parameters that share it, so every parameter is
   visited once per pass.
6. Stop training and find the bug: compare one layer's analytic gradient with its numerical value,
   check transposes and activation derivatives.

</details>

## 12. Key Terms

**Backpropagation**, **computation graph**, **chain rule**, **error signal**, **local gradient**,
**Jacobian**, **cross-entropy**, **softmax gradient**, **vanishing gradient**, **exploding
gradient**, **gradient clipping**, **gradient check**, **reverse-mode differentiation**.

## 13. Further Reading

- Rumelhart, Hinton & Williams (1986). *Learning Representations by Back-Propagating Errors*.
  Nature. — The paper that made it mainstream.
- Goodfellow, Bengio & Courville (2016). *Deep Learning*, Chapter 6.5.
- Baydin, Pearlmutter, Radul & Siskind (2018). *Automatic Differentiation in Machine Learning: A
  Survey*. JMLR.

## What to Do Next

1. Run `python nn_numpy.py` and read the gradient-check line.
2. Do exercises 1 and 3 — breaking it on purpose teaches more than fixing it.
3. Continue to [L07-03 — Training in Practice](L07-03-training-in-practice.md).

---

**Navigation:** [← Previous: L07-01](L07-01-from-perceptron-to-mlp.md) · [Module home](../README.md) · [Next: L07-03 →](L07-03-training-in-practice.md)
