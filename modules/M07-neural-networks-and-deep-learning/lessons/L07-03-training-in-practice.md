# L07-03 — Training in Practice: Frameworks, Optimisers and Learning Rates

[← Previous: L07-02](L07-02-backpropagation-the-mathematics-of-learning.md) · [Module home](../README.md) · [Next: L07-04 →](L07-04-regularisation-and-diagnosis.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: A Training Run You Can Defend](#4-the-procedure-a-training-run-you-can-defend)
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

> **Module M07** · Lesson 3 of 8 · ~90 minutes · Level 300
> **Prerequisites:** L07-02

[Previous: L07-02](L07-02-backpropagation-the-mathematics-of-learning.md) · [Module overview](../README.md) · [Next: L07-04 →](L07-04-regularisation-and-diagnosis.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Use** PyTorch tensors, autograd, `Dataset`/`DataLoader` and an `nn.Module` to build and train
   a network.
2. **Write** a training loop with a validation pass, early stopping and history.
3. **Save** and **load** a model correctly, and identify what must be saved besides the weights.
4. **Compare** SGD, Momentum, RMSProp and Adam, with their update equations and failure modes.
5. **Choose** a learning rate and a schedule, and diagnose "too high" versus "too low" from the
   loss curve.
6. **Explain** what changes with a GPU, and what stays identical.
7. **Read** an equivalent Keras program and map each line to its PyTorch counterpart.

## 2. Prerequisite Knowledge

Backpropagation (L07-02), mini-batch gradient descent, and enough Python to read a class with a
`forward` method.

## 3. Conceptual Explanation

### 3.1 Tensors

A tensor is an n-dimensional array with two additions: it can live on a device (CPU or GPU) and it
can record the operations applied to it. Shapes matter as much as values in deep learning:

```python
x = torch.randn(32, 1, 8, 8)   # batch 32, 1 channel, 8x8 image
print(x.shape)                 # torch.Size([32, 1, 8, 8])
```

A convolution expects `(batch, channels, height, width)`; a linear layer expects
`(batch, features)`. Most shape errors are a missing `flatten` or a channel dimension in the wrong
place.

### 3.2 Autograd

```python
w = torch.tensor([2.0], requires_grad=True)
loss = (w * 3 - 1) ** 2
loss.backward()
print(w.grad)          # dloss/dw = 2*(3w-1)*3 = 30
```

PyTorch records the graph during the forward computation and traverses it backwards on
`.backward()`. Two habits prevent most autograd bugs:

- **Zero the gradients** (`optimizer.zero_grad()`) each step; they accumulate by default.
- **Wrap evaluation in `torch.no_grad()`** so validation does not build a graph.

### 3.3 Datasets and loaders

A `DataLoader` does four things: batching, shuffling, collation and (optionally) parallel loading.
The module's `make_loader` wraps NumPy arrays; for real data you subclass `torch.utils.data.Dataset`
and implement `__len__` and `__getitem__`.

```python
from torch_utils import make_loader
train_loader = make_loader(X_train, y_train, batch_size=64, shuffle=True)
val_loader = make_loader(X_val, y_val, batch_size=256, shuffle=False)
```

Shuffle the training set every epoch; never shuffle the validation set (the metric does not care,
but reproducibility and error inspection do).

### 3.4 Model construction

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(64, 32), nn.ReLU(), nn.Dropout(0.1),
    nn.Linear(32, 10),
)
```

Subclassing `nn.Module` is needed when the forward pass is not a straight line (residual
connections, attention masks, multiple inputs). The rule: define layers in `__init__`, use them in
`forward`, never create parameters inside `forward`.

### 3.5 The training loop

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(epochs):
    model.train()
    for xb, yb in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        # compute validation loss and accuracy
        ...
```

Five lines do the work: zero, forward, loss, backward, step. Everything else is measurement.
`Trainer` in `torch_utils.py` packages this with early stopping and history.

### 3.6 Optimisers

| Optimiser | Update | Strength | Weakness |
| :--- | :--- | :--- | :--- |
| SGD | $w \leftarrow w-\eta g$ | simple, generalises well with tuning | slow in ravines |
| Momentum | $v\leftarrow\beta v+g$; $w\leftarrow w-\eta v$ | faster, damps oscillation | extra hyperparameter |
| RMSProp | $s\leftarrow\beta s+(1-\beta)g^2$; $w\leftarrow w-\eta g/\sqrt{s}$ | per-parameter scaling | can be noisy |
| Adam | momentum + RMSProp + bias correction | robust default | sometimes worse final generalisation than tuned SGD |

Five epochs on the synthetic digits, batch 64, NumPy MLP:

```text
sgd       loss 1.715 train acc 0.639
momentum  loss 0.524 train acc 0.977
rmsprop   loss 1.420 train acc 0.803
adam      loss 1.450 train acc 0.804
```

Momentum's advantage here is a learning-rate effect as much as an algorithmic one: its effective
step is larger. That is exactly why optimiser comparisons must state the learning rate — an
optimiser is not a model, it is a policy for using gradients.

### 3.7 Learning rate

- **Too high**: loss oscillates or grows; accuracy collapses after a good start.
- **Too low**: loss falls smoothly but far too slowly; early stopping triggers before progress.
- **Schedules**: step decay (×0.1 at milestones), cosine annealing, one-cycle, warmup then decay.
  Warmup avoids early instability in transformers.
- **Rule of thumb**: start at $10^{-3}$ for Adam, $10^{-1}$–$10^{-2}$ for SGD, then sweep by
  factors of 3 and plot loss against epochs.

### 3.8 Epochs and batches

- **Batch size** trades gradient noise against throughput and memory. Smaller batches add noise
  that can help generalisation and hurt speed.
- **Epochs** are a budget, not a target; early stopping decides when to stop.
- Doubling the batch size usually allows roughly doubling the learning rate; that is a heuristic,
  not a law.

### 3.9 Initialisation

- **Xavier/Glorot** ($\text{Var}=1/n_{\text{in}}$) for tanh/sigmoid.
- **He** ($\text{Var}=2/n_{\text{in}}$) for ReLU.
- **Zero init** is a disaster: every neuron in a layer computes the same thing and receives the
  same gradient, so they stay identical forever (symmetry breaking requires randomness).

### 3.10 Saving and loading

```python
torch.save({"state_dict": model.state_dict(), "config": config}, "model.pt")
bundle = torch.load("model.pt", weights_only=False)
model.load_state_dict(bundle["state_dict"])
```

Save the **state dict**, not the model object, and record the architecture and preprocessing
alongside it. A checkpoint without its config is a puzzle, not a model.

### 3.11 GPU acceleration

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
xb, yb = xb.to(device), yb.to(device)
```

On CPU everything above is identical; only speed changes. Practical notes: larger batches amortise
transfer overhead, `pin_memory=True` helps with `num_workers>0`, and moving data to the device
inside the loop (as above) is the simplest correct pattern. The module's code never assumes CUDA —
`get_device()` returns CPU on this machine.

### 3.12 Keras, comparatively

Keras hides the loop behind `compile`/`fit`. The mapping is direct:

```python
# Keras (not executed in this course environment; TensorFlow is not installed)
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(8, 8)),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.1),
    keras.layers.Dense(10, activation="softmax"),
])
model.compile(optimizer=keras.optimizers.Adam(1e-3),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=5, batch_size=64,
                    validation_data=(X_val, y_val))
```

| Keras | PyTorch |
| :--- | :--- |
| `Sequential([...])` | `nn.Sequential(...)` |
| `compile(optimizer, loss)` | optimizer + loss function objects |
| `fit(...)` | the training loop |
| `history.history["val_loss"]` | `Trainer.history["val_loss"]` |
| `model.save("m.keras")` | `state_dict` + config |
| `model.predict(X)` | `model.eval()` + `no_grad` |

Keras is shorter; PyTorch makes the loop explicit. For research and custom losses, the explicit
loop is usually easier to modify; for standard supervised training, Keras is faster to write.

## 4. The Procedure: A Training Run You Can Defend

1. Seed everything (`set_seed`), choose the device, record both.
2. Build train/validation/test splits before any preprocessing.
3. Define the model, count its parameters and compare with the dataset size.
4. Pick loss from the task, optimiser Adam at $10^{-3}$, batch size 32–128.
5. Train with validation every epoch and early stopping on validation loss.
6. Plot train and validation loss; diagnose before tuning.
7. Save the best state dict plus config; record the history.
8. Report test metrics once, with a baseline.
9. Write down what you did **not** try.

## 5. Worked Examples

### Example 1 — MLP versus CNN on synthetic digits

From `torch_utils.py`, five epochs, CPU:

```text
model                    params  val acc  seconds
MLP 64-32                  2410    0.920     3.05
CNN width 16              13802    1.000     1.75
```

The CNN has six times the parameters and trains faster per epoch here, because convolutions share
weights. Accuracy is not the only column that matters: the MLP at 0.920 is already usable, and if
latency or interpretability mattered it could win.

### Example 2 — Reading a loss curve

| Pattern | Diagnosis | First response |
| :--- | :--- | :--- |
| train ↓, val ↓, small gap | healthy | stop when val flattens |
| train ↓, val ↑ | overfitting | dropout, weight decay, more data, early stop |
| train flat, val flat, both high | underfitting or bug | larger model, check labels and learning rate |
| loss NaN | learning rate too high or log(0) | lower lr, check loss implementation |
| val much lower than train | leakage or a lucky split | audit the split |

### Example 3 — A learning-rate sweep

Train the same MLP at $10^{-4}$, $10^{-3}$, $10^{-2}$ for three epochs and record final training
loss. On this data, $10^{-4}$ barely moves, $10^{-3}$ falls steadily, $10^{-2}$ is unstable. The
sweep costs three short runs and is more informative than any amount of guessing.

## 6. Mathematical Formulation

Mini-batch loss for batch $B$: $L_B = \frac{1}{|B|}\sum_{i\in B}\ell(f(x_i),y_i)$.

**Adam**, with $g_t$ the batch gradient:

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,
$$
$$
\hat m_t=\frac{m_t}{1-\beta_1^t},\qquad
\hat v_t=\frac{v_t}{1-\beta_2^t},\qquad
\theta_t=\theta_{t-1}-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
$$

**Cosine annealing**: $\eta_t=\eta_{\min}+\tfrac12(\eta_{\max}-\eta_{\min})
(1+\cos(\pi t/T))$.

**Effective learning rate with momentum**: steady-state step size is approximately
$\eta/(1-\beta)$ along a consistent direction.

## 7. Python Implementation

```python
# run from modules/M07-neural-networks-and-deep-learning/code
import torch
from torch import nn
from torch_utils import MLP, Trainer, make_loader, set_seed, get_device, count_parameters
import deep_data as dd

set_seed(0)
device = get_device()
images, labels = dd.digit_images(2400, seed=0)
train_loader = make_loader(images[:1800], labels[:1800], 64, seed=0)
val_loader = make_loader(images[1800:], labels[1800:], 256, shuffle=False)

model = MLP(64, hidden=(32,), n_classes=10)
trainer = Trainer(model, device=device, patience=5)
history = trainer.fit(train_loader, val_loader, epochs=5, lr=1e-3, verbose=True)
loss, acc, preds, labels_true = trainer.evaluate(val_loader)
print("params:", count_parameters(model), "val acc:", round(acc, 3))
print("history keys:", list(history))
```

```text
params: 2410 val acc: 0.92
history keys: ['train_loss', 'val_loss', 'train_acc', 'val_acc']
```

Saving and reloading:

```python
from torch_utils import save_checkpoint, load_checkpoint

save_checkpoint(model, "digits_mlp.pt", config={"hidden": (32,), "lr": 1e-3})
reloaded, config = load_checkpoint(MLP(64, hidden=(32,), n_classes=10), "digits_mlp.pt")
print("config:", config)

with torch.no_grad():
    before = model.eval()(torch.as_tensor(images[1800:1810]))
    after = reloaded.eval()(torch.as_tensor(images[1800:1810]))
print("same predictions:", bool(torch.allclose(before, after)))
```

```text
config: {'hidden': (32,), 'lr': 0.001}
same predictions: True
```

## 8. Practical Applications

- **Tabular deep models** rarely beat gradient boosting, but they scale to huge categorical inputs
  with embeddings.
- **Vision and audio** are where PyTorch's explicit loops and ecosystem pay off.
- **Research** needs custom losses and schedules, which is why the explicit loop matters.
- **Production** needs the saved artefact plus preprocessing, not just the weights.

## 9. Common Mistakes

1. Forgetting `optimizer.zero_grad()`: gradients accumulate across batches.
2. Evaluating without `model.eval()`: dropout and batch norm behave differently in training mode.
3. Comparing optimisers at different effective learning rates.
4. Saving the whole model object and losing the class definition.
5. Shuffling the validation set, then reporting a score you cannot reproduce.
6. Ignoring parameter count relative to dataset size.
7. Blaming the optimiser when the data pipeline is wrong.

## 10. Practical Exercises

1. Run the MLP at three learning rates and plot the training loss curves.
2. Replace Adam with plain SGD at $\eta=0.1$ and momentum 0.9. Compare epochs to reach 0.85
   validation accuracy.
3. Deliberately set `model.train()` during validation and report how the accuracy changes with
   dropout 0.5.
4. Save a checkpoint, reload it in a fresh process, and compare predictions on ten rows.
5. Translate the Keras `fit` example into the PyTorch loop, line by line, in a comment block.

## 11. Self-Assessment

**Multiple choice**

1. `optimizer.zero_grad()` exists because PyTorch
   a) stores gradients in the model. b) accumulates gradients by default. c) uses SGD.
   d) requires it for autograd to work.
2. `model.eval()` matters because
   a) it speeds up training. b) dropout and batch norm change behaviour at inference.
   c) it frees memory. d) it zeroes gradients.
3. Adam's bias correction exists because
   a) gradients are noisy. b) $m$ and $v$ start at zero and are biased early.
   c) learning rates decay. d) batches are small.
4. He initialisation is designed for
   a) sigmoid. b) ReLU. c) softmax. d) linear outputs.

**Short answer**

5. Why should the state dict, not the model object, be the saved artefact?
6. A run's training loss is flat from epoch 1. Name two possible causes and the check for each.

<details>
<summary>Answers</summary>

1. **b**. 2. **b**. 3. **b**. 4. **b**.
5. It is portable across code refactors and does not require the class definition at load time; the
   config records the architecture.
6. Learning rate too low (check a larger value) or gradients not flowing (check `requires_grad`,
   loss, and gradient norms); also a frozen model or all-zero inputs.

</details>

## 12. Key Terms

**Tensor**, **autograd**, **requires_grad**, **state dict**, **DataLoader**, **Dataset**,
**collate**, **optimiser**, **momentum**, **RMSProp**, **Adam**, **bias correction**,
**learning-rate schedule**, **warmup**, **early stopping**, **He initialisation**,
**Xavier initialisation**, **GPU**, **mixed precision**.

## 13. Further Reading

- Kingma, D. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR.
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR.
- PyTorch documentation, *Autograd mechanics* and *Optimizing model parameters*.

## What to Do Next

1. Run `python torch_utils.py` and `python nn_numpy.py`.
2. Do exercises 1–3.
3. Continue to [L07-04 — Regularisation and Diagnosis](L07-04-regularisation-and-diagnosis.md).

---

**Navigation:** [← Previous: L07-02](L07-02-backpropagation-the-mathematics-of-learning.md) · [Module home](../README.md) · [Next: L07-04 →](L07-04-regularisation-and-diagnosis.md)
