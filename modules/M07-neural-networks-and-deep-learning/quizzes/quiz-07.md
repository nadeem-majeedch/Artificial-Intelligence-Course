# QUIZ-07 — Neural Networks and Deep Learning self-check

| Module | M07 · Artificial Neural Networks and Deep Learning |
| :--- | :--- |
| Questions | 20 multiple choice + 6 numerical + 4 short answer + 3 programming |
| Time | 90 minutes |
| Covers | [L07-01](../lessons/L07-01-from-perceptron-to-mlp.md) … [L07-08](../lessons/L07-08-transfer-learning-and-autoencoders.md) |
| Pass mark | 16 / 20 on Part A, plus 4 / 6 on Part B |

[← Module home](../README.md) · [Course home](../../../README.md)

## How to use this quiz

Parts A and B are closed-book; a calculator is allowed, code is not. Part C is open-book. Mark
yourself against the worked answers, then use the revision map at the end. An answer you get right by
elimination still counts, but reread the explanation.

## Part A — Multiple choice (20 marks)

**Q07.01** A single perceptron cannot solve XOR because
- A. the learning rate is too small
- B. XOR is not linearly separable
- C. the step activation is not differentiable
- D. there are too few training examples

**Q07.02** The derivative of the sigmoid $\sigma(z)=1/(1+e^{-z})$ is
- A. $\sigma(z)$
- B. $\sigma(z)(1-\sigma(z))$
- C. $1-\sigma(z)^2$
- D. $\max(0,1)$

**Q07.03** ReLU is preferred over sigmoid in deep hidden layers mainly because
- A. it is bounded
- B. its gradient does not saturate for positive inputs
- C. it is differentiable everywhere
- D. it reduces the parameter count

**Q07.04** The "dying ReLU" problem refers to
- A. units whose gradient is permanently zero because their pre-activation stays negative
- B. units that explode to infinity
- C. overfitting to the training set
- D. batch norm instability

**Q07.05** For softmax plus cross-entropy, $\partial L/\partial z$ equals
- A. $p-y$
- B. $y-p$
- C. $p(1-p)$
- D. $2(p-y)$

**Q07.06** Backpropagation computes
- A. the global minimum directly
- B. gradients by the chain rule, layer by layer
- C. the Hessian
- D. the loss without gradients

**Q07.07** A learning rate that is too large typically causes
- A. slow but stable convergence
- B. divergence or oscillation of the loss
- C. vanishing gradients
- D. guaranteed overfitting

**Q07.08** Adam differs from plain SGD because it
- A. uses second-order derivatives
- B. keeps per-parameter momentum and adaptive scaling with bias correction
- C. requires no learning rate
- D. cannot overfit

**Q07.09** Dropout at training time
- A. removes units permanently
- B. randomly zeroes activations, with scaling so inference is unchanged
- C. averages the weights across epochs
- D. normalises the batch

**Q07.10** Batch normalisation normalises using
- A. the whole-dataset statistics in both training and inference
- B. batch statistics in training, running estimates at inference
- C. per-parameter gradients
- D. the target distribution

**Q07.11** A convolution layer with kernel 3, padding 1, stride 2 applied to a 28×28 input produces
- A. 28×28
- B. 27×27
- C. 14×14
- D. 13×13

**Q07.12** Weight sharing in a CNN means
- A. every layer has the same number of filters
- B. the same kernel is applied at every spatial position
- C. all images share the same label
- D. gradients are shared between batches

**Q07.13** Max pooling mainly provides
- A. translation robustness and downsampling
- B. more parameters
- C. a non-linear loss
- D. longer training

**Q07.14** An LSTM addresses the vanishing-gradient problem with
- A. a larger learning rate
- B. gated cell state carrying information across time
- C. batch normalisation
- D. convolution over time only

**Q07.15** In a GRU, compared with an LSTM,
- A. there are more gates
- B. there are fewer gates (reset and update, no separate output gate)
- C. there is no hidden state
- D. recurrence is removed

**Q07.16** The $\sqrt{d_k}$ in scaled dot-product attention exists to
- A. normalise the values
- B. prevent large dot products from saturating the softmax
- C. mask the future
- D. reduce the parameter count

**Q07.17** Positional encodings are necessary because self-attention
- A. is too slow
- B. is permutation-invariant
- C. cannot handle embeddings
- D. requires masking

**Q07.18** Freezing a pretrained backbone means
- A. deleting its weights
- B. setting `requires_grad = False` for its parameters
- C. removing batch norm
- D. training at a larger learning rate

**Q07.19** An autoencoder's training objective is
- A. cross-entropy against labels
- B. reconstruction of its own input
- C. a contrastive triplet loss only
- D. maximising the latent dimension

**Q07.20** A reconstruction-error anomaly detector trained on normal data should be evaluated
- A. on the training set only
- B. on held-out normal data plus labelled anomalies, reporting false-alarm rate and recall
- C. by its training loss
- D. by the number of parameters

## Part B — Numerical (6 marks)

**Q07.21** Scaled dot-product attention with
$Q=(1,0)$, $K=I_2$, $V=\begin{bmatrix}10&0\\0&20\end{bmatrix}$, $d_k=2$.
Give the attention weights and the output vector to two decimals.

**Q07.22** How many trainable parameters in a dense network `64 → 32 → 10` with biases?

**Q07.23** A convolutional layer has kernel size 3, padding 1, stride 2, and receives a 32×32 map.
What is the output spatial size?

**Q07.24** Inverted dropout with drop probability 0.5 leaves an activation of 4.0 alive. What value
does the network use for that unit during training?

**Q07.25** Momentum with $\beta=0.9$, previous velocity 0.3, current gradient 0.5, learning rate 0.1,
weight $w=1.0$. Give the new velocity and the new weight.

**Q07.26** A reconstruction-error detector is thresholded at the 95th percentile of normal training
error and tested on 1,000 normal items and 200 anomalies, catching 70% of the anomalies. What is
precision?

## Part C — Short answer (4 marks)

**Q07.27** Explain in three sentences why a deep network with all-linear activations is equivalent to
a single linear layer.

**Q07.28** Give two reasons validation loss can rise while training loss falls, and one remedy for
each.

**Q07.29** Why does a transformer need more data than a CNN to reach the same accuracy on images?

**Q07.30** A colleague reports 0.97 accuracy from a model fine-tuned on 50 labelled images, without a
baseline. Name three checks you would require before believing the number.

## Part D — Programming (3 tasks, open book)

**Q07.31** Implement a `train_one_epoch(model, loader, optimizer, criterion)` that returns mean loss
and accuracy, works on CPU, and sets train/eval mode correctly.

**Q07.32** Write a function `attention(Q, K, V, mask=None)` implementing scaled dot-product
attention with an optional boolean mask, and test it against the hand computation in Q07.21.

**Q07.33** Write `ablation_table(configs, run_fn, seeds)` that runs each configuration over several
seeds and returns mean and standard deviation of the metric, sorted descending by mean.

---

## Answers

### Part A

| Q | Answer | Why |
| :--- | :--- | :--- |
| 01 | B | XOR needs two lines; one neuron gives one. |
| 02 | B | $\sigma' = \sigma(1-\sigma)$. |
| 03 | B | ReLU's gradient is 1 for positive inputs, so it does not saturate. |
| 04 | A | A large negative bias keeps the unit off and its gradient zero. |
| 05 | A | With one-hot $y$ and softmax $p$, the gradient simplifies to $p-y$. |
| 06 | B | Reverse-mode chain rule over the computation graph. |
| 07 | B | Steps overshoot the minimum; the loss oscillates or diverges. |
| 08 | B | First and second moment estimates with bias correction. |
| 09 | B | Inverted dropout scales survivors by $1/(1-p)$. |
| 10 | B | Batch statistics while training, running estimates afterwards. |
| 11 | C | $\lfloor(28+2-3)/2\rfloor+1 = 14$. |
| 12 | B | One kernel slides over all positions. |
| 13 | A | Local translation invariance plus a smaller map. |
| 14 | B | The cell state is updated additively through gates. |
| 15 | B | Reset and update gates only. |
| 16 | B | Dot-product variance grows with $d_k$; scaling keeps logits usable. |
| 17 | B | Without positions, attention cannot distinguish order. |
| 18 | B | Gradients are not computed for frozen parameters. |
| 19 | B | The target is the input itself. |
| 20 | B | False-alarm rate and recall on held-out data, at a stated threshold. |

### Part B

**Q07.21** Scores $QK^\top=(1,0)$; scaled by $\sqrt2$: $(0.707,0)$. Softmax gives
$(0.670, 0.330)$. Output $=0.670(10,0)+0.330(0,20)=(6.70,6.60)$.

**Q07.22** $(64\cdot32+32)+(32\cdot10+10)=2048+32+320+10=\mathbf{2410}$.

**Q07.23** $\lfloor(32+2-3)/2\rfloor+1 = 16$, so **16×16**.

**Q07.24** Inverted dropout scales by $1/(1-0.5)=2$, so the unit contributes **8.0**.

**Q07.25** $v=0.9(0.3)+0.5=0.77$; $w=1.0-0.1(0.77)=\mathbf{0.923}$.

**Q07.26** Threshold at the 95th percentile flags 5% of 1,000 normal items = 50 false positives;
true positives $=0.7\times200=140$. Precision $=140/190\approx\mathbf{0.74}$.

### Part C

**Q07.27** A linear layer followed by another linear layer is still a linear map, since
$W_2(W_1x+b_1)+b_2=(W_2W_1)x+(W_2b_1+b_2)$. Any depth of linear layers collapses to one matrix,
so the network cannot represent a non-linear function such as XOR. Non-linear activations between
layers are what create the extra representational power.

**Q07.28** (1) Overfitting: the model memorises training noise — remedy: more data or stronger
regularisation (dropout, weight decay, early stopping). (2) Distribution shift between training and
validation splits — remedy: check how the split was made and whether the validation set is
representative. A third cause is a learning-rate schedule that is too aggressive late in training.

**Q07.29** A CNN encodes locality and translation equivariance in its architecture, so it needs fewer
examples to learn that nearby pixels are related. A transformer has to learn spatial relationships
from data via positional encodings and attention, which requires either more labelled data or
pretraining on a large corpus.

**Q07.30** A matched baseline (scratch training on the same 50 labels, same budget); multiple seeds
with the spread reported; and a check that the pretraining data does not overlap the test images —
plus, ideally, a held-out test split that was never used for early stopping.

### Part D — sketch answers

**Q07.31**

```python
import torch

def train_one_epoch(model, loader, optimizer, criterion):
    model.train()
    total_loss, correct, seen = 0.0, 0, 0
    for xb, yb in loader:
        optimizer.zero_grad()
        outputs = model(xb)
        loss = criterion(outputs, yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(xb)
        correct += (outputs.argmax(dim=1) == yb).sum().item()
        seen += len(xb)
    return total_loss / seen, correct / seen
```

**Q07.32**

```python
import math
import torch

def attention(Q, K, V, mask=None):
    scores = Q @ K.transpose(-2, -1) / math.sqrt(Q.shape[-1])
    if mask is not None:
        scores = scores.masked_fill(mask, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    return weights @ V, weights

Q = torch.tensor([[1.0, 0.0]])
K = torch.eye(2)
V = torch.tensor([[10.0, 0.0], [0.0, 20.0]])
out, w = attention(Q, K, V)
print(w.round(3), out.round(2))   # [[0.670, 0.330]] [[6.70, 6.60]]
```

**Q07.33**

```python
import numpy as np

def ablation_table(configs, run_fn, seeds=(0, 1, 2)):
    rows = []
    for name, config in configs.items():
        scores = [run_fn(**config, seed=s) for s in seeds]
        rows.append((name, float(np.mean(scores)), float(np.std(scores))))
    return sorted(rows, key=lambda r: -r[1])
```

## Revision map

| If you missed | Reread |
| :--- | :--- |
| Q01–Q04 | [L07-01](../lessons/L07-01-from-perceptron-to-mlp.md) |
| Q05–Q08 | [L07-02](../lessons/L07-02-backpropagation-the-mathematics-of-learning.md), [L07-03](../lessons/L07-03-training-in-practice.md) |
| Q09–Q10 | [L07-04](../lessons/L07-04-regularisation-and-diagnosis.md) |
| Q11–Q13 | [L07-05](../lessons/L07-05-convolutional-neural-networks.md) |
| Q14–Q15 | [L07-06](../lessons/L07-06-sequence-models-rnn-lstm-gru.md) |
| Q16–Q17 | [L07-07](../lessons/L07-07-attention-and-transformers.md) |
| Q18–Q20 | [L07-08](../lessons/L07-08-transfer-learning-and-autoencoders.md) |

Marking: 1 mark per Part A question, 1 per Part B question, 1 per Part C question. Part D is
ungraded self-check; run the sketches.
