# L07-01 — From the Perceptron to the Multilayer Perceptron

[← Module start](../README.md) · [Next: ? Lesson →](L07-02-backpropagation-the-mathematics-of-learning.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Building a First Network](#4-the-procedure-building-a-first-network)
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

> **Module M07** · Lesson 1 of 8 · ~75 minutes · Level 300
> **Prerequisites:** P02 (vectors, derivatives), M06 (linear and logistic models)

[Module overview](../README.md) · [Next: L07-02 →](L07-02-backpropagation-the-mathematics-of-learning.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Describe** the artificial neuron as a weighted sum plus a nonlinearity, and map each part to
   its biological namesake without over-claiming the analogy.
2. **Train** a perceptron by its historical learning rule and explain why it converges on AND/OR
   but not on XOR.
3. **Compare** step, sigmoid, tanh, ReLU, Leaky ReLU and softmax, with range, derivative and the
   failure each one addresses.
4. **Stack** neurons into a multilayer perceptron and compute a forward pass by hand.
5. **Explain** why depth plus a nonlinear activation can represent XOR, and what the universal
   approximation theorem does and does not promise.
6. **Choose** an output activation and loss pair for regression, binary and multiclass tasks.

## 2. Prerequisite Knowledge

The dot product, the chain rule, and logistic regression from
[L06-04](../../M06-machine-learning-fundamentals/lessons/L06-04-classification-with-logistic-regression.md).
A neuron is logistic regression with a different activation and a different training signal; if
that sentence is unclear, revise the logistic lesson first.

## 3. Conceptual Explanation

### 3.1 Biological inspiration, honestly stated

A biological neuron receives signals through dendrites, integrates them in the cell body, and
emits a spike along its axon when the integrated signal crosses a threshold. An artificial neuron
does something structurally similar:

```text
inputs x1..xd → multiply by weights w1..wd → add bias b → activation f → output a
```

The analogy stops there. Real neurons are time-dependent, chemically modulated, recurrent and
not organised in tidy layers. "Inspired by the brain" is a historical remark, not an argument that
the model works the way a brain does. The useful content is the computation, not the metaphor.

### 3.2 The artificial neuron

$$
z = \sum_{j=1}^{d} w_j x_j + b = \mathbf{w}^\top\mathbf{x} + b,
\qquad
a = f(z).
$$

- **Weights** say how much each input matters.
- **Bias** shifts the threshold: a large negative bias means the neuron fires only for strong
  evidence.
- **Activation** $f$ makes the unit nonlinear. Without it, stacking layers collapses to one linear
  map — a fact worth proving to yourself once: $W_2(W_1x) = (W_2W_1)x$.

### 3.3 The perceptron and its learning rule

Rosenblatt's perceptron (1958) used a step activation and this update for each misclassified
example:

$$
\mathbf{w} \leftarrow \mathbf{w} + \eta\,(y - \hat y)\,\mathbf{x},
\qquad
b \leftarrow b + \eta\,(y - \hat y).
$$

If the prediction is correct, nothing changes. If the true label is 1 and the output 0, the weight
vector moves toward the input; if the reverse, it moves away. The **perceptron convergence
theorem** guarantees termination in finite steps *if the data are linearly separable*.

The module's demo, 20 epochs on the four examples:

```text
AND  errors per epoch: [1, 3, 3, 2, 1, 0] ... final acc 1.00
OR   errors per epoch: [1, 2, 1, 0, 0, 0] ... final acc 1.00
XOR  errors per epoch: [2, 3, 4, 4, 4, 4] ... final acc 0.50
```

XOR's error count never reaches zero because no straight line separates $\{(0,0),(1,1)\}$ from
$\{(0,1),(1,0)\}$. The 1969 book *Perceptrons* made this limitation famous and is a large part of
why neural-network research stalled for a decade. The fix is not a better perceptron; it is a
hidden layer.

### 3.4 Activation functions

| Function | Formula | Range | Derivative | Use |
| :--- | :--- | :--- | :--- | :--- |
| step | $\mathbb{1}[z>0]$ | {0,1} | 0 almost everywhere | historical only |
| sigmoid | $1/(1+e^{-z})$ | (0,1) | $a(1-a)$ | binary output, gates |
| tanh | $(e^z-e^{-z})/(e^z+e^{-z})$ | (−1,1) | $1-a^2$ | small hidden layers |
| ReLU | $\max(0,z)$ | [0,∞) | 0 or 1 | default for hidden layers |
| Leaky ReLU | $\max(\alpha z,z)$ | (−∞,∞) | 1 or $\alpha$ | avoids dead units |
| softmax | $e^{z_k}/\sum_j e^{z_j}$ | (0,1), sums to 1 | see L07-02 | multiclass output |

Why ReLU became the default: its derivative is exactly 1 for positive inputs, so gradients do not
shrink as they pass through many layers. Sigmoid's derivative is at most 0.25, and a product of
many such terms vanishes — the subject of L07-02. ReLU's weakness is the "dead unit": a neuron
whose pre-activation is always negative receives zero gradient forever. Leaky ReLU gives it a small
slope as an escape.

Softmax is different in kind: it turns a vector of scores into a probability distribution, so it
belongs at the output of a multiclass classifier, not in hidden layers.

### 3.5 From one neuron to a network

A **multilayer perceptron** (MLP) arranges neurons in layers:

```text
input (d) → hidden 1 (h1) → hidden 2 (h2) → ... → output (k)
```

Each layer computes

$$
\mathbf{a}^{(l)} = f\big(\mathbf{W}^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}\big),
$$

which is a matrix multiplication followed by an elementwise nonlinearity. **Forward propagation**
is just evaluating that composition from the input to the output.

For XOR, two hidden units suffice. Take

$$
h_1 = \mathbb{1}[x_1 + x_2 - 0.5 > 0] \quad (\text{OR}),
\qquad
h_2 = \mathbb{1}[x_1 + x_2 - 1.5 > 0] \quad (\text{AND}),
$$

then

$$
\hat y = \mathbb{1}[h_1 - h_2 - 0.5 > 0],
$$

which is 1 only when OR is true and AND is false — exactly XOR. Two straight lines, combined,
produce a non-linear region. That is the geometric meaning of a hidden layer.

### 3.6 Depth and the universal approximation theorem

A network with one sufficiently wide hidden layer can approximate any continuous function on a
compact domain to arbitrary accuracy (Cybenko 1989, Hornik 1991). Read the fine print:

- "Sufficiently wide" can mean exponentially many units; the theorem is about existence, not
  about learnability from finite data.
- It says nothing about whether gradient descent will find the approximation.
- Depth is usually more parameter-efficient than width for the same function, which is why modern
  architectures are deep.

### 3.7 Outputs and losses

| Task | Output activation | Loss |
| :--- | :--- | :--- |
| Regression | none (linear) | MSE / MAE |
| Binary classification | sigmoid, one unit | binary cross-entropy |
| Multiclass, one label | softmax, k units | cross-entropy |
| Multilabel | sigmoid per label | binary cross-entropy per label |

Matching the output to the loss is not cosmetic: softmax with MSE trains slowly and calibrates
badly, because the gradient loses the probability structure.

## 4. The Procedure: Building a First Network

1. Flatten or encode the input into a fixed-length vector.
2. Choose the output unit and loss from the task (§3.7).
3. Start with one hidden layer of 32–128 units and ReLU.
4. Initialise weights with He scaling (ReLU) or Xavier (tanh).
5. Train with a small batch size and Adam at $10^{-3}$ as a first attempt.
6. Watch training loss first: if it does not fall, the bug is in the model or the data, not the
   regularisation.
7. Only then add capacity, dropout, or a scheduler.
8. Compare with a linear baseline before claiming the network is necessary.

## 5. Worked Examples

### Example 1 — One neuron by hand

Inputs $x=(1,2)$, weights $w=(0.5,-0.25)$, bias $b=0.1$:

$$
z = 0.5(1) - 0.25(2) + 0.1 = 0.1,
\qquad
a = \sigma(0.1) = 0.525.
$$

With ReLU instead, $a = 0.1$. With a step, $a = 1$. The same weighted sum, three different
decisions about how to fire.

### Example 2 — XOR with a hidden layer

Using the construction in §3.5 on $(1,0)$: OR $= \mathbb{1}[1-0.5>0]=1$, AND
$=\mathbb{1}[1-1.5>0]=0$, so $\hat y = \mathbb{1}[1-0-0.5>0]=1$. On $(1,1)$: OR 1, AND 1, so
$\hat y=\mathbb{1}[1-1-0.5>0]=0$. The network gets all four rows right with four parameters in the
hidden layer.

### Example 3 — A trained network

```text
MLP [2, 4, 2] on XOR, tanh, Adam(0.05), 2000 epochs
final loss 6e-05   accuracy 1.0
probabilities: [[1.0, 0.0], [0.0, 1.0], [0.0, 1.0], [1.0, 0.0]]
```

The probabilities are saturated because the loss is tiny. On a real dataset that saturation would
be a calibration warning; on a four-row logic problem it is simply convergence.

## 6. Mathematical Formulation

Layer $l$ with $n_{l-1}$ inputs and $n_l$ units:

$$
\mathbf{z}^{(l)} = \mathbf{W}^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)},
\qquad
\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)}),
$$

with $\mathbf{W}^{(l)}\in\mathbb{R}^{n_l\times n_{l-1}}$. The parameter count is
$\sum_l (n_{l-1}n_l + n_l)$.

Sigmoid derivative: $\sigma'(z)=\sigma(z)(1-\sigma(z))$. Tanh derivative: $1-\tanh^2(z)$.
ReLU derivative: $\mathbb{1}[z>0]$. Softmax with cross-entropy has the convenient gradient
$\partial L/\partial z_k = p_k - y_k$ (derived in L07-02).

Universal approximation (Cybenko): for any continuous $f$ on $[0,1]^d$ and $\epsilon>0$ there
exist $N$ and parameters such that a one-hidden-layer network with $N$ units satisfies
$\sup_x |F(x)-f(x)|<\epsilon$.

## 7. Python Implementation

The perceptron rule, then an MLP, both from scratch:

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import numpy as np
import deep_data as dd
from nn_numpy import MLP, train, Adam, perceptron_rule

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
for name, y in [("AND", np.array([0, 0, 0, 1])),
                ("OR", np.array([0, 1, 1, 1])),
                ("XOR", np.array([0, 1, 1, 0]))]:
    w, b, errors = perceptron_rule(X, y, epochs=20)
    preds = ((X @ w + b) > 0).astype(int)
    print(name, "errors:", errors[:6], "accuracy:", np.mean(preds == y))

Xx, yx = dd.xor_data()
net = MLP([2, 4, 2], activation="tanh", seed=1)
history = train(net, Xx, yx.ravel().astype(int), epochs=2000, batch_size=4,
                optimizer=Adam(0.05), seed=1)
print("XOR MLP loss:", round(history["loss"][-1], 6), "accuracy:", history["accuracy"][-1])
```

```text
AND errors: [1, 3, 3, 2, 1, 0] accuracy: 1.0
OR errors: [1, 2, 1, 0, 0, 0] accuracy: 1.0
XOR errors: [2, 3, 4, 4, 4, 4] accuracy: 0.5
XOR MLP loss: 6e-05 accuracy: 1.0
```

The same network on 2,000 synthetic digit images (64 inputs, 32 hidden, 10 outputs, 15 epochs):
training accuracy 0.995, test accuracy 0.995. The task is easy on purpose — the point is the
pipeline, not the score.

## 8. Practical Applications

- **Tabular credit scoring** — an MLP on engineered features can match gradient boosting, but
  usually needs more tuning and offers less interpretability.
- **Handwritten digit recognition** — the historical proving ground; now solved by CNNs.
- **Function approximation in control** — a small MLP represents a policy or value function.
- **Embedding heads** — the final layers of large models are MLPs.

## 9. Common Mistakes

1. **Forgetting the nonlinearity.** Two linear layers in a row are one linear layer.
2. **Using sigmoid in every hidden layer.** Gradients vanish; use ReLU or tanh.
3. **Softmax with MSE.** Match the output activation to the loss.
4. **Expecting a perceptron to learn XOR.** It cannot, by theorem, not by tuning.
5. **Judging a network by training loss alone.** A model that memorises has low training loss.
6. **Treating the brain analogy as evidence.** It is motivation, not validation.

## 10. Practical Exercises

1. Compute one forward pass for $x=(0.5,-1)$, $W=[[1,2],[-1,0.5]]$, $b=(0,1)$ with ReLU.
2. Show algebraically that two linear layers without activation compose into one linear map.
3. Train the perceptron on AND with $\eta=0.01$ and $\eta=10$. How do the error sequences differ?
4. Build the XOR network from §3.5 by hand and verify all four rows.
5. Add a second hidden layer to the XOR MLP. Does it learn faster, slower, or the same? Report
   epochs to loss < 0.01 for three seeds.

## 11. Self-Assessment

**Multiple choice**

1. Without activation functions, a deep network is
   a) more expressive. b) a single linear map. c) a kernel machine. d) non-convex.
2. The perceptron convergence theorem requires
   a) a hidden layer. b) linearly separable data. c) a sigmoid output. d) mini-batches.
3. ReLU's derivative for negative inputs is
   a) 1. b) 0. c) 0.01 always. d) undefined.
4. Softmax is used to
   a) speed up training. b) produce a probability distribution over classes.
   c) prevent overfitting. d) initialise weights.

**Short answer**

5. Why does XOR require a hidden layer?
6. State one thing the universal approximation theorem does **not** guarantee.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b** (for ReLU; Leaky ReLU uses 0.01). 4. **b**.
5. XOR is not linearly separable; a hidden layer maps it into a space where the output unit can
   separate the classes.
6. That gradient descent will find the approximating parameters, or that the required width is
   practical.

</details>

## 12. Key Terms

**Artificial neuron**, **weight**, **bias**, **activation function**, **perceptron**,
**perceptron learning rule**, **linear separability**, **multilayer perceptron**,
**hidden layer**, **feedforward**, **forward propagation**, **ReLU**, **softmax**,
**universal approximation**.

## 13. Further Reading

- Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for Information Storage and
  Organization in the Brain*. Psychological Review.
- Minsky, M. & Papert, S. (1969). *Perceptrons*. — The XOR limitation and its consequences.
- Goodfellow, Bengio & Courville (2016). *Deep Learning*, Chapter 6. — Units, activations,
  architecture design.

## What to Do Next

1. Run `python nn_numpy.py` and read the perceptron block.
2. Do exercises 1–4.
3. Continue to [L07-02 — Backpropagation](L07-02-backpropagation-the-mathematics-of-learning.md).

---

**Navigation:** [← Module start](../README.md) · [Next: ? Lesson →](L07-02-backpropagation-the-mathematics-of-learning.md)
