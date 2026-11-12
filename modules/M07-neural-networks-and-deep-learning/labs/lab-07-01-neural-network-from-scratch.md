# LAB-07-01 — A Neural Network From Scratch: Logic Gates and Backpropagation

> **Module M07** · Lab 1 of 3 · ~150 minutes · Level 300
> **Scenario:** 1 — AND/OR/XOR with a perceptron, then a multilayer network
> **Prerequisites:** L07-01, L07-02, L07-03 · **Pairs with:** NB-07-01

[Module overview](../README.md) · [Lesson 1](../lessons/L07-01-from-perceptron-to-mlp.md) · [Next lab: LAB-07-02 →](lab-07-02-digital-fashion-and-plant-classifiers.md)

You will build a neural network with NumPy only — no autograd, no framework — and prove it is
correct. The problem is deliberately tiny so that every gradient can be checked numerically and
every failure is your own mistake rather than a library's.

---

## Scenario 1 — Logic gates: the perceptron's limits and the MLP's fix

### Problem description

Four input pairs, two classes. AND and OR are linearly separable; XOR is not. Implement Rosenblatt's
perceptron and show, with the error counts, that it converges on the first two and never on the
third. Then add a hidden layer, train with backpropagation, and solve XOR.

### Business context

Every classification system in production is a composition of units like these, and every
"why doesn't my network learn?" question has a geometric answer. A team that has seen a single
neuron fail on XOR knows why depth exists and will not waste weeks adding regularisation to a model
that is simply too shallow.

### Dataset source and licence

- **In this lab:** the four-point XOR truth table, constructed in code. No licence, no download.
- **Real counterpart:** none needed. If you want a real binary toy dataset later, the UCI *Iris*
  subset (two classes, two features) is CC BY 4.0.

### Learning objectives

1. Implement a perceptron learning rule and an MLP forward pass in NumPy.
2. Derive and implement the backward pass for softmax + cross-entropy.
3. Validate gradients numerically with a relative-error check below $10^{-6}$.
4. Compare step, sigmoid, tanh, ReLU and Leaky ReLU hidden activations on XOR.
5. Measure how learning rate, batch size and epochs change convergence.
6. Explain why a hidden layer changes the representable function class.

### Background

The perceptron updates $w \leftarrow w + \eta\,(y-\hat y)x$ for each mistake. It converges in finite
steps when the classes are linearly separable and provably does not when they are not. A hidden
layer maps the four points into a space where the classes *are* separable — with four hidden units,
XOR becomes two linear cuts.

Softmax + cross-entropy gives the clean gradient $\partial L/\partial z = (p-y)/n$, which is why the
backward pass below is short.

### Tasks

**Task 1 — Perceptron on three gates (25 min)**

```python
import numpy as np
import deep_data as dd
from nn_numpy import perceptron_rule, accuracy

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
for name, labels in {"AND": [0, 0, 0, 1], "OR": [0, 1, 1, 1], "XOR": [0, 1, 1, 0]}.items():
    w, b, errors = perceptron_rule(X, np.array(labels), epochs=6, lr=1.0)
    preds = ((X @ w + b) > 0).astype(int)
    print(name, errors, round(accuracy(labels, preds), 2))
```

Record the per-epoch error counts. Plot them for all three gates on one axis.

**Task 2 — Forward and backward by hand (35 min)**

Write your own `forward` and `backward` for a 2-4-2 network, without looking at `nn_numpy.py`,
then compare against it numerically. Your backward pass must start from
`dZ = (p - onehot)/n`.

**Task 3 — Gradient check (20 min)**

```python
from nn_numpy import MLP, gradient_check
model = MLP([2, 4, 2], activation="tanh", seed=0)
Xxor, yxor = dd.xor_data()
worst = gradient_check(model, Xxor, yxor.ravel().astype(int), epsilon=1e-6)
print(f"{worst:.2e}")
```

The check must pass below $10^{-6}$. If it does not, the usual causes are a missing division by the
batch size, the activation derivative evaluated at the wrong pre-activation, or transposed weight
matrices.

**Task 4 — Activation sweep (30 min)**

Train the same 2-4-2 network on XOR for 2,000 epochs with each activation in
`step, sigmoid, tanh, relu, leaky_relu`. Report final loss, epochs to reach loss < 0.05, and whether
it converged at all. Use the same seed.

**Task 5 — Learning rate and batch size (25 min)**

For lr in `0.001, 0.01, 0.05, 0.5, 5.0` and batch size in `1, 2, 4`, record final loss after 500
epochs. Identify the region where training is unstable and explain it in terms of the step size
relative to the curvature of the loss surface.

**Task 6 — Depth versus width (15 min)**

Compare `[2, 4, 2]`, `[2, 2, 2, 2]` and `[2, 16, 2]` on XOR. Which configurations can represent XOR,
and which merely happen to fit these four points?

### Expected results

Perceptron error counts with `lr=1.0`, six epochs:

```text
AND [1, 3, 3, 2, 1, 0] -> accuracy 1.00
OR  [1, 2, 1, 0, 0, 0] -> accuracy 1.00
XOR [2, 3, 4, 4, 4, 4] -> accuracy 0.50
```

The XOR count oscillates and never reaches zero: that is the proof, not an implementation bug.

MLP on XOR, `[2, 4, 2]`, tanh, Adam(0.05), 2,000 epochs:

```text
final loss: 5.95e-05   accuracy: 1.000   predictions: [0 1 1 0]
```

Gradient check on a 64-5-3 network: maximum relative error `1.22e-08` — a passing implementation.

### Metrics

- Final cross-entropy loss and accuracy on all four XOR inputs.
- Maximum relative gradient error (must be $<10^{-6}$).
- Epochs to convergence at each learning rate (a proxy for optimisation efficiency).

### Deliverables

1. `perceptron_gates.py` — Task 1, with the plot.
2. `backprop_xor.py` — Tasks 2–4, including your own backward implementation.
3. `lab-07-01-report.md` — a one-page report with the error-count table, the gradient-check result,
   the activation sweep and the learning-rate table, plus two paragraphs explaining the geometry.

### Extensions

- Add momentum to the perceptron and check whether XOR still fails (it does — momentum changes the
  path, not the function class).
- Replace softmax cross-entropy with mean squared error on one-hot targets and compare convergence.
- Implement mini-batch shuffling and measure the variance of the final loss across ten seeds.

### Common pitfalls

- Labelling XOR with `0/1` in one place and `-1/+1` in another.
- Forgetting to zero the gradient accumulators between batches.
- Using a ReLU network with too few epochs and concluding ReLU cannot do XOR.
- Checking gradients with dropout enabled — the stochastic mask makes finite differences meaningless.

### Marking guide

| Criterion | Weight |
| :--- | ---: |
| Perceptron implementation and correct error counts | 20% |
| Own forward/backward pass, gradient check passing | 30% |
| Activation and learning-rate experiments, correctly interpreted | 25% |
| Report clarity, including the geometry explanation | 15% |
| Code quality: seeds, reproducibility, no dead code | 10% |
