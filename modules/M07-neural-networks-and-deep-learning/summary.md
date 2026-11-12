# M07 — One-Page Summary

[Module home](README.md) · [Course home](../../README.md) · [Quiz](quizzes/quiz-07.md)

## The workflow

```text
frame the task → fix the split → baseline → train → validate → test once
              → error analysis → ablations with seeds → model card → monitor
```

The three rules that prevent most deep-learning disasters:

1. **A baseline or it didn't happen.** Majority class for classification, repeat-last for forecasting.
2. **One factor at a time, three seeds minimum.** A difference smaller than the seed spread is noise.
3. **The test split is touched once.** Early stopping belongs on validation.

## The pieces

| Layer | What it does | Formula |
| :--- | :--- | :--- |
| Neuron | weighted sum, then activation | $z=w^\top x+b$ |
| Sigmoid | squashes to (0,1) | $\sigma(z)=1/(1+e^{-z})$ |
| tanh | squashes to (−1,1) | $\tanh(z)$ |
| ReLU | keeps positives | $\max(0,z)$ |
| Leaky ReLU | keeps a small negative slope | $\max(0.01z,z)$ |
| Softmax | turns scores into a distribution | $e^{z_i}/\sum_j e^{z_j}$ |
| Cross-entropy | classification loss | $-\sum_i y_i\log p_i$ |
| MSE | regression/reconstruction loss | $\frac1n\sum(y-\hat y)^2$ |

## Backpropagation, in one line per step

$$
\delta^{L}=p-y,\qquad
\delta^{l}=\left(W^{l+1\top}\delta^{l+1}\right)\odot f'(z^{l}),\qquad
\frac{\partial L}{\partial W^{l}}=a^{l-1\top}\delta^{l}.
$$

Numerical check: $\frac{L(\theta+\epsilon)-L(\theta-\epsilon)}{2\epsilon}$ must match the analytic
gradient to a relative error below $10^{-6}$.

## Optimisers

| Rule | Update |
| :--- | :--- |
| SGD | $w \leftarrow w-\eta g$ |
| Momentum | $v\leftarrow\beta v+g$; $w\leftarrow w-\eta v$ |
| RMSProp | $s\leftarrow\beta s+(1-\beta)g^2$; $w\leftarrow w-\eta g/(\sqrt{s}+\epsilon)$ |
| Adam | momentum + RMSProp, both bias-corrected |

## Convolution arithmetic

$$
\text{out}=\left\lfloor\frac{W+2P-K}{S}\right\rfloor+1,
\qquad
\text{params}=(K\cdot K\cdot C_{\text{in}}+1)\cdot C_{\text{out}}.
$$

Pooling has no parameters. Weight sharing is why a CNN needs far fewer parameters than a dense
network on the same image.

## Sequences and attention

RNN state: $h_t=\tanh(W_xx_t+W_hh_{t-1}+b)$. LSTM adds input, forget and output gates around a cell
state; GRU merges them into reset and update gates.

$$
\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V .
$$

Multi-head attention runs $h$ of these with different projections; positional encodings restore order;
cost is $O(n^2)$ per layer.

## Transfer and autoencoders

- Feature extraction: freeze the backbone, train a new head.
- Fine-tuning: unfreeze at 10–100× smaller learning rate.
- Transfer helps most when labels are scarce; check the licence of the weights, not just the data.
- Autoencoder loss: $\lVert x-\hat x\rVert^2$; anomaly score = reconstruction error; threshold at a
  chosen quantile of normal error and report false-alarm rate with recall.

## Verified numbers from this module

Run these and you should see the same figures (CPU, seed 0):

| Experiment | Result |
| :--- | :--- |
| Perceptron, AND / OR / XOR, 6 epochs | errors `[1,3,3,2,1,0]` / `[1,2,1,0,0,0]` / `[2,3,4,4,4,4]`; XOR accuracy 0.50 |
| MLP 2-4-2 on XOR | loss 5.95e-05, accuracy 1.000 |
| Gradient check, 64-5-3 network | max relative error 1.22e-08 |
| Digits MLP 64-32 | 2,410 params, val accuracy 0.988 |
| Digits CNN width 16 | 13,802 params, val accuracy 0.998 |
| Textures CNN / MLP | 1.000 / 1.000 — task too easy to separate architectures |
| Plants RGB vs grayscale CNN | 1.000 vs 0.813 — colour carries most of the signal |
| LSTM forecast (800 windows) | MSE 0.0249 vs repeat-last 0.5372 |
| Tiny transformer sentiment | 9,922 params, accuracy 0.990 vs majority 0.578 |
| Transfer, 60 labels | scratch 0.502, frozen 0.756, fine-tuned 0.769 |
| Transfer, 150 labels | scratch 0.938, frozen 0.836, fine-tuned 0.947 |
| Autoencoder anomaly detector | error 0.0187 normal vs 0.0417 unseen; 5% false alarms, 70.7% recall |

## Diagnostics cheat sheet

| Symptom | Likely cause | First thing to try |
| :--- | :--- | :--- |
| Loss flat from the start | learning rate too small, or dead ReLU units | raise lr 10×; check activation statistics |
| Loss explodes | learning rate too large, or no input scaling | lower lr; normalise inputs |
| Train accuracy high, val low | overfitting | dropout, weight decay, more data, early stopping |
| Both low | underfitting or broken labels | bigger model, check label balance, verify data pipeline |
| Val loss rising while train falls | overfitting has started | restore the best checkpoint |
| Accuracy stuck at majority rate | class imbalance or labels swapped | confusion matrix; check the label mapping |
| Gradients near zero everywhere | vanishing gradients, saturating activations | ReLU, batch norm, residual connections |

## What to do next

- [M08 — Natural Language Processing](../README.md#m08) applies attention to text properly.
- [M09 — Computer Vision](../README.md#m09) goes deeper on convolution and detection.
- [M11 — Generative AI and LLMs](../README.md#m11) scales the transformer.
