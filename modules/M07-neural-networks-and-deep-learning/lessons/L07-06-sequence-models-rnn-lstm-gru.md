# L07-06 — Sequence Models: RNN, LSTM and GRU

[← Previous: ? Lesson](L07-05-convolutional-neural-networks.md) · [Module home](../README.md) · [Next: ? Lesson →](L07-07-attention-and-transformers.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Forecasting with an LSTM](#4-the-procedure-forecasting-with-an-lstm)
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

> **Module M07** · Lesson 6 of 8 · ~95 minutes · Level 300
> **Prerequisites:** L07-02 to L07-05

[Previous: L07-05](L07-05-convolutional-neural-networks.md) · [Module overview](../README.md) · [Next: L07-07 →](L07-07-attention-and-transformers.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Explain** why sequences break the fixed-input assumption of an MLP and what a recurrent
   connection adds.
2. **Unroll** an RNN over time and compute a forward pass by hand.
3. **Describe** backpropagation through time and why gradients vanish or explode over long
   sequences.
4. **Derive** the LSTM gates and the cell-state update, and explain what each gate controls.
5. **Compare** LSTM and GRU in cost and behaviour, and choose between them.
6. **Train** an LSTM forecaster and compare it with a naive baseline.
7. **State** when a 1D convolution or a transformer is a better choice than a recurrent network.

## 2. Prerequisite Knowledge

Matrix multiplication, tanh and sigmoid, and the idea of a hidden state. Nothing about sequences is
assumed.

## 3. Conceptual Explanation

### 3.1 Why sequences need a different model

An MLP maps a fixed-size vector to an output. Text, audio and sensor streams have variable length
and, more importantly, **order matters**: "dog bites man" and "man bites dog" contain the same
words. A model needs some memory of what it has seen.

A recurrent network keeps a hidden state that is updated at every step:

$$
\mathbf{h}_t = \tanh\big(\mathbf{W}_x\mathbf{x}_t + \mathbf{W}_h\mathbf{h}_{t-1} + \mathbf{b}\big),
\qquad
\hat{\mathbf{y}}_t = \mathbf{W}_y\mathbf{h}_t.
$$

The same weights are used at every step — weight sharing across time, exactly as a convolution
shares across space.

### 3.2 Unrolling and backpropagation through time

Unrolling the recurrence for $T$ steps produces a deep network with $T$ layers that all share
weights:

```text
x1 → h1 → h2 → h3 → ... → hT → loss
      ↑    ↑    ↑          ↑
      └────┴────┴──────────┘  same W_h
```

Backpropagation through time (BPTT) is ordinary backprop on this unrolled graph. The gradient with
respect to $h_0$ contains a product of $T$ Jacobians, each involving $\mathbf{W}_h^\top$ and the
tanh derivative (≤ 1). If the largest singular value of $\mathbf{W}_h$ is below 1, the product
decays exponentially; above 1, it explodes. This is the same vanishing-gradient mechanism as deep
feedforward stacks, but worse because the same matrix is multiplied repeatedly.

Practical responses: gradient clipping (cap the norm at 1–5), gated architectures (LSTM/GRU),
truncated BPTT (backpropagate only $k$ steps), and — in modern practice — attention.

### 3.3 LSTM

The long short-term memory cell (Hochreiter & Schmidhuber, 1997) adds a **cell state**
$\mathbf{c}_t$ that runs through time with only elementwise operations, plus three gates:

$$
\mathbf{f}_t=\sigma(\mathbf{W}_f[\mathbf{h}_{t-1},\mathbf{x}_t]+\mathbf{b}_f)
\quad\text{(forget)}
$$
$$
\mathbf{i}_t=\sigma(\mathbf{W}_i[\mathbf{h}_{t-1},\mathbf{x}_t]+\mathbf{b}_i)
\quad\text{(input)}
$$
$$
\tilde{\mathbf{c}}_t=\tanh(\mathbf{W}_c[\mathbf{h}_{t-1},\mathbf{x}_t]+\mathbf{b}_c)
\quad\text{(candidate)}
$$
$$
\mathbf{c}_t=\mathbf{f}_t\odot\mathbf{c}_{t-1}+\mathbf{i}_t\odot\tilde{\mathbf{c}}_t
$$
$$
\mathbf{o}_t=\sigma(\mathbf{W}_o[\mathbf{h}_{t-1},\mathbf{x}_t]+\mathbf{b}_o),
\qquad
\mathbf{h}_t=\mathbf{o}_t\odot\tanh(\mathbf{c}_t).
$$

Read the cell update as a leaky integrator: the forget gate decides what to keep, the input gate
what to add. When $\mathbf{f}_t\approx1$, the gradient can flow through many steps without being
multiplied by a weight matrix — the "constant error carousel". That is the architectural fix for
vanishing gradients, not a hyperparameter.

### 3.4 GRU

The gated recurrent unit (Cho et al., 2014) merges the cell state and hidden state and uses two
gates:

$$
\mathbf{z}_t=\sigma(\mathbf{W}_z[\mathbf{h}_{t-1},\mathbf{x}_t])
\quad\text{(update)},
\qquad
\mathbf{r}_t=\sigma(\mathbf{W}_r[\mathbf{h}_{t-1},\mathbf{x}_t])
\quad\text{(reset)},
$$
$$
\tilde{\mathbf{h}}_t=\tanh(\mathbf{W}_h[\mathbf{r}_t\odot\mathbf{h}_{t-1},\mathbf{x}_t]),
\qquad
\mathbf{h}_t=(1-\mathbf{z}_t)\odot\mathbf{h}_{t-1}+\mathbf{z}_t\odot\tilde{\mathbf{h}}_t.
$$

Fewer parameters (three weight blocks instead of four), often similar accuracy. Choose GRU for
smaller data or tighter latency; LSTM when long-range dependencies matter and you can afford it.
Both are superseded by attention for most text tasks, but remain strong for small sensor and
time-series problems where data are limited.

### 3.5 Output heads

| Task | Head |
| :--- | :--- |
| Sequence classification | take the last hidden state, or mean-pool over time |
| Many-to-many (tagging) | a linear layer at every step |
| Forecasting | linear layer on the last state, predicting one or more future values |
| Sequence-to-sequence | encoder-decoder, often with attention |

### 3.6 Limitations

- **Sequential computation**: step $t$ cannot start before $t-1$ finishes, so training does not
  parallelise over time the way a transformer does.
- **Long-range memory** is finite even with gates; 500-step dependencies remain hard.
- **Fixed hidden size** compresses the whole past into one vector.
- They are still the right tool for small, streaming, low-latency sequence problems.

## 4. The Procedure: Forecasting with an LSTM

1. Build windows: a fixed-length input and the value(s) to predict.
2. Split **chronologically**, never randomly.
3. Standardise using training statistics only.
4. Start with a one-layer LSTM of 16–64 units; add a linear head.
5. Train with MSE/MAE and early stopping on validation loss.
6. Compare with a naive baseline: predict the last value, or the seasonal mean.
7. Plot predictions against actuals for a held-out stretch, not just the loss.
8. Inspect residuals for drift and for missed peaks.

## 5. Worked Examples

### Example 1 — An RNN step by hand

Scalar RNN with $W_x=1$, $W_h=0.5$, $b=0$, $h_0=0$, input sequence $(1,-1,0.5)$:

$$
h_1=\tanh(1+0)=0.7616,
$$
$$
h_2=\tanh(-1+0.5(0.7616))=\tanh(-0.6192)=-0.5506,
$$
$$
h_3=\tanh(0.5+0.5(-0.5506))=\tanh(0.2247)=0.2210.
$$

Each output depends on the entire prefix; the same three numbers appear at every step with
different inputs.

### Example 2 — LSTM on a synthetic series

800 windows of length 24 from a two-sinusoid series, 640 train / 160 validation, 25 epochs:

```text
LSTM final validation MSE: 0.0459
naive "repeat last value" baseline MSE: 0.5372
```

The LSTM captures the periodic structure and beats the naive baseline, but the margin is not
infinite: most of the signal is a smooth sinusoid that a seasonal baseline handles well. A model
that cannot beat "repeat the last value" has not learned anything useful.

### Example 3 — Gate behaviour, interpreted

If the forget gate saturates near 1 and the input gate near 0, the cell state is preserved and the
network is ignoring the input — a sign of over-training or of an uninformative sequence. If the
forget gate is near 0 everywhere, the model has no memory beyond one step. Inspecting gate
activations is a legitimate diagnostic, not just a curiosity.

## 6. Mathematical Formulation

**RNN**: as in §3.1, with parameter count
$|\mathbf{W}_x|+|\mathbf{W}_h|+|\mathbf{b}| = d\,h + h^2 + h$.

**LSTM** parameter count per layer in PyTorch: $4\big((d+h)h+2h\big)$ — four weight blocks, each
with an input bias and a recurrent bias. For $d=1$, $h=32$ that is 4,480, plus 33 for the linear
head, giving 4,513.

**GRU**: $3\big((d+h)h+2h\big)$.

**Gradient through time**:

$$
\frac{\partial L}{\partial \mathbf{h}_0}
= \sum_{t=1}^{T}\frac{\partial L_t}{\partial \mathbf{h}_t}
\prod_{k=1}^{t}\frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}},
$$

and each factor is $\text{diag}(1-\tanh^2)\mathbf{W}_h^\top$. The product is the vanishing-gradient
problem in one line.

**Gradient clipping**: if $\lVert g\rVert>c$, set $g\leftarrow c\,g/\lVert g\rVert$.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import torch.nn as nn
import deep_data as dd
from torch_utils import LSTMRegressor, Trainer, make_loader, count_parameters

X, y = dd.series_windows(800, seed=0)
train_loader = make_loader(X[:640], y[:640], 32, seed=0)
val_loader = make_loader(X[640:], y[640:], 64, shuffle=False)

model = LSTMRegressor(hidden_size=32)
print("parameters:", count_parameters(model))
trainer = Trainer(model, criterion=nn.MSELoss(), patience=8)
history = trainer.fit(train_loader, val_loader, epochs=25, lr=0.01)
loss, _, preds, _ = trainer.evaluate(val_loader)
print("validation MSE:", round(loss, 4))
print("first five predictions:", [round(float(v), 3) for v in preds[:5]])
```

```text
parameters: 4513
validation MSE: 0.0459
```

The naive baseline, for comparison:

```python
import numpy as np
print("repeat-last baseline MSE:", round(float(np.mean((y[640:] - X[640:, -1, 0]) ** 2)), 4))
```

## 8. Practical Applications

- **Energy and demand forecasting** — hourly load, weather features, LSTM or GRU per meter.
- ** Predictive maintenance** — sensor sequences; a GRU is often enough.
- **Speech recognition** — historically LSTM/CTC; now transformers.
- **Clinical time series** — irregular sampling is the hard part, not the architecture.
- **Text classification with small data** — a bidirectional GRU is a strong, cheap baseline.

## 9. Common Mistakes

1. **Random splits on time series.** Shuffling leaks the future; split chronologically.
2. **Standardising before the split.** Use training statistics only.
3. **Comparing with no baseline.** Always report "repeat last value" or the seasonal mean.
4. **Feeding padded sequences without a mask** and averaging over padding.
5. **Forgetting gradient clipping** on long sequences, then blaming the architecture for NaN.
6. **Assuming LSTM beats a 1D CNN** on short windows; often it does not.
7. **Reporting MSE** without the target's scale or a plot.

## 10. Practical Exercises

1. Compute three RNN steps by hand with $W_x=0.5$, $W_h=-0.8$, inputs $(1,2,-1)$.
2. Count LSTM and GRU parameters for input 1, hidden 32, one layer. Verify with PyTorch.
3. Train the LSTM with and without gradient clipping on a 100-step window. Compare.
4. Replace the LSTM with a GRU and compare validation MSE and training time.
5. Plot predictions versus actuals over the whole validation split and describe where the model
   fails.
6. Train on a shuffled split and report the inflated score. Explain why it is meaningless.

## 11. Self-Assessment

**Multiple choice**

1. An RNN shares weights
   a) across layers only. b) across time steps. c) across batches. d) never.
2. BPTT gradients vanish when
   a) the learning rate is low. b) the product of Jacobians has norm below 1.
   c) the batch is small. d) the loss is MSE.
3. The LSTM cell state is updated
   a) by a convolution. b) with elementwise gating. c) by attention. d) by pooling.
4. A GRU has
   a) more parameters than an LSTM. b) fewer gates than an LSTM. c) no hidden state.
   d) no nonlinearity.

**Short answer**

5. Why does the LSTM's cell state help gradients?
6. Give one situation where a 1D CNN is preferable to an LSTM.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. Its update is additive and elementwise, so gradients can flow through many steps without
   repeated multiplication by a weight matrix.
6. Short, fixed-length windows with local patterns and a need for parallel computation — a 1D
   convolution trains faster and often matches accuracy.

</details>

## 12. Key Terms

**Sequence**, **recurrence**, **hidden state**, **unrolling**, **backpropagation through time**,
**truncated BPTT**, **vanishing gradient**, **exploding gradient**, **gradient clipping**,
**LSTM**, **forget gate**, **input gate**, **output gate**, **cell state**, **GRU**, **reset gate**,
**update gate**, **teacher forcing**, **sequence-to-sequence**.

## 13. Further Reading

- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory*. Neural Computation.
- Cho, K. et al. (2014). *Learning Phrase Representations using RNN Encoder–Decoder* (GRU). EMNLP.
- Pascanu, Mikolov & Bengio (2013). *On the Difficulty of Training Recurrent Neural Networks*. ICML.

## What to Do Next

1. Run `python torch_utils.py` and read the LSTM line.
2. Do exercises 1–3.
3. Continue to [L07-07 — Attention and Transformers](L07-07-attention-and-transformers.md).

---

**Navigation:** [← Previous: ? Lesson](L07-05-convolutional-neural-networks.md) · [Module home](../README.md) · [Next: ? Lesson →](L07-07-attention-and-transformers.md)
