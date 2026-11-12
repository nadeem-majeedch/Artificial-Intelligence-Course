# M07 — Artificial Neural Networks and Deep Learning

| Level | 300 |
| :--- | :--- |
| Study time | 27 hours |
| Lessons | 8 |
| Course outcome | CLO6 — build, train, evaluate and debug a neural network, and explain why it works |
| Prerequisites | P02 (matrices, gradients), M06 (essential) |

[Course home](../../README.md) · [All modules](../README.md) · [Previous module: M06](../M06-machine-learning-fundamentals/README.md) · [Next module: M08](../README.md#m08)

## Overview

This module takes you from a single neuron to a working deep-learning workflow. It is built on two
convictions: that the mathematics is worth doing once, properly, by hand; and that most deep-learning
failures are evaluation failures — a missing baseline, a leaked split, a single seed, a metric that
does not match the decision.

You will implement a perceptron, a multilayer network and one full backward pass in NumPy, verify the
gradients numerically, and then rebuild the same ideas in PyTorch. From there: convolution, recurrence,
attention, and transfer. Every lesson ends with the failure modes of the method it taught.

The seven practical scenarios are spread across the three labs:

| Scenario | Task | Where |
| :--- | :--- | :--- |
| 1 | AND/OR/XOR with a perceptron and an MLP | [LAB-07-01](labs/lab-07-01-neural-network-from-scratch.md) |
| 2 | Handwritten digit classification | [LAB-07-02](labs/lab-07-02-digital-fashion-and-plant-classifiers.md) |
| 3 | Garment/texture classification | [LAB-07-02](labs/lab-07-02-digital-fashion-and-plant-classifiers.md) |
| 4 | Plant disease classification | [LAB-07-02](labs/lab-07-02-digital-fashion-and-plant-classifiers.md) |
| 5 | Review sentiment classification | [LAB-07-03](labs/lab-07-03-sentiment-forecasting-and-transfer.md) |
| 6 | Demand forecasting with an LSTM | [LAB-07-03](labs/lab-07-03-sentiment-forecasting-and-transfer.md) |
| 7 | Transfer learning with 60 labels | [LAB-07-03](labs/lab-07-03-sentiment-forecasting-and-transfer.md) |

## Data and licences

All datasets are **synthetic, generated in-script with fixed seeds**, so every number in these
lessons reproduces offline on a CPU. Each mirrors the shape of a named public dataset so you can swap
the real files in:

| Synthetic generator | Mirrors | Licence of the real dataset |
| :--- | :--- | :--- |
| `digit_images` | MNIST | CC BY-SA 3.0 |
| `pattern_images` | Fashion-MNIST | MIT |
| `plant_images` | PlantVillage | CC BY-SA 3.0 |
| `sentiment_data` | IMDB Large Movie Review | research use — check terms |
| `series_windows` | generic seasonal demand series | n/a |

`deep_data.load_idx_images` reads the original IDX files for MNIST or Fashion-MNIST, so the labs can
run against the real data by changing one loader call. Synthetic results are teaching results; never
report them as benchmarks. Pretrained weights carry their own licence, separate from any dataset.

**No torchvision and no TensorFlow are required.** The module uses `torch` (CPU) and NumPy only.
TensorFlow/Keras equivalents appear as annotated comparative snippets marked *not executed*.

## Before you start

You need to be able to write and debug Python functions, use NumPy arrays, read a derivative, and
explain train/validation/test splits. The prerequisite lessons:

- **Matrices and gradients** — [P02](../../prerequisites/P02-mathematics-for-ai/README.md)
- **Machine learning workflow, evaluation, leakage** — [M06](../M06-machine-learning-fundamentals/README.md)

**Readiness self-check.** If you cannot do three of these, review the prerequisites first:

1. Differentiate $f(w)=(wx-y)^2$ with respect to $w$.
2. Multiply a $3\times2$ matrix by a $2\times4$ matrix by hand.
3. Explain why you must not tune on the test set.
4. Compute softmax of $(1, 2, 3)$ to two decimals.
5. Explain what a learning rate does in one sentence.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L07-01 | From the Perceptron to the Multilayer Perceptron | Lesson | 75 m | [Read](lessons/L07-01-from-perceptron-to-mlp.md) |
| L07-02 | Backpropagation: The Mathematics of Learning | Lesson | 90 m | [Read](lessons/L07-02-backpropagation-the-mathematics-of-learning.md) |
| L07-03 | Training in Practice: Initialisation, Optimisers, Learning Rates | Lesson | 90 m | [Read](lessons/L07-03-training-in-practice.md) |
| L07-04 | Regularisation, Dropout and Diagnosing a Deep Network | Lesson | 90 m | [Read](lessons/L07-04-regularisation-and-diagnosis.md) |
| L07-05 | Convolutional Neural Networks | Lesson | 90 m | [Read](lessons/L07-05-convolutional-neural-networks.md) |
| L07-06 | Sequence Models: RNN, LSTM and GRU | Lesson | 95 m | [Read](lessons/L07-06-sequence-models-rnn-lstm-gru.md) |
| L07-07 | Attention and the Transformer Architecture | Lesson | 90 m | [Read](lessons/L07-07-attention-and-transformers.md) |
| L07-08 | Transfer Learning, Fine-Tuning and Autoencoders | Lesson | 90 m | [Read](lessons/L07-08-transfer-learning-and-autoencoders.md) |
| NB-07-01 | Neural Network Fundamentals Workbench | Notebook | 60 m | [Open](notebooks/nb-07-01-neural-network-fundamentals.ipynb) |
| NB-07-02 | PyTorch Image Classification Workbench | Notebook | 60 m | [Open](notebooks/nb-07-02-pytorch-image-classification.ipynb) |
| NB-07-03 | Sequences, Attention and Transfer Workbench | Notebook | 60 m | [Open](notebooks/nb-07-03-sequences-attention-transfer.ipynb) |
| LAB-07-01 | A Neural Network From Scratch | Lab | 2.5 h | [Start](labs/lab-07-01-neural-network-from-scratch.md) |
| LAB-07-02 | Digits, Fashion and Plant Disease Classifiers | Lab | 2.5 h | [Start](labs/lab-07-02-digital-fashion-and-plant-classifiers.md) |
| LAB-07-03 | Sentiment, Forecasting and Transfer Learning | Lab | 2.5 h | [Start](labs/lab-07-03-sentiment-forecasting-and-transfer.md) |
| ASG-07 | A Deep Model with an Ablation Study | Assignment | 2 h | [Start](assignments/asg-07-ablation-study.md) |
| QUIZ-07 | Module self-check | Quiz | 30 m | [Take](quizzes/quiz-07.md) |
| MP-07 | Image Classifier Sprint | Mini-project | 2 h | [Start](projects/mp-07-image-classifier-sprint.md) |

Total: 12 h lessons + 3 h notebooks + 7.5 h labs + 2 h assignment + 0.5 h quiz + 2 h mini-project
= **27 hours**.

Supporting code lives in [`code/`](code/):

| File | Contents |
| :--- | :--- |
| `deep_data.py` | seven seeded dataset generators plus an IDX loader |
| `nn_numpy.py` | perceptron rule, MLP, backpropagation, SGD/Momentum/RMSProp/Adam, gradient check |
| `torch_utils.py` | `Trainer`, `MLP`, `SmallCNN`, `LSTMRegressor`, `TinyTransformerClassifier`, `AutoEncoder`, checkpointing, freeze/unfreeze |
| `transfer.py` | pretraining, head swap, frozen/fine-tuned sweep, autoencoder anomaly experiment |

Every module runs standalone: `python deep_data.py`, `python nn_numpy.py`, `python torch_utils.py`,
`python transfer.py`.

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L07-01, L07-02 | 3 h |
| 2 | NB-07-01, LAB-07-01 (start) | 2.5 h |
| 3 | LAB-07-01 (finish), L07-03 | 2.5 h |
| 4 | L07-04, NB-07-02 | 2.5 h |
| 5 | L07-05, LAB-07-02 (start) | 2.5 h |
| 6 | LAB-07-02 (finish) | 2.5 h |
| 7 | L07-06, L07-07 | 3 h |
| 8 | NB-07-03, L07-08 | 3 h |
| 9 | LAB-07-03 | 2.5 h |
| 10 | QUIZ-07, ASG-07 | 2.5 h |
| 11 | MP-07, revision | 2 h |

Eleven days at roughly 2.5 hours. If time is short, keep the labs and the backpropagation exercise in
LAB-07-01; drop the notebooks only after reproducing their headline numbers yourself.

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-07-01 | From-scratch implementation, gradient check, experiment discipline | 10% |
| LAB-07-02 | Three image pipelines, matched comparisons, cue-dependence analysis | 10% |
| LAB-07-03 | Baselines, threshold reasoning, seed sweeps, transfer judgement | 10% |
| QUIZ-07 | Conceptual and numerical grasp | 10% |
| ASG-07 | Ablation design, statistical honesty, error analysis | 25% |
| MP-07 | Working classifier, reproducibility, model card | 35% |

The assessment dimensions are described in the
[curriculum map](../../docs/CURRICULUM-MAP.md#8-assessment-model).

## Key terms introduced

**Perceptron**, **activation function**, **sigmoid**, **tanh**, **ReLU**, **Leaky ReLU**,
**softmax**, **hidden layer**, **feedforward**, **forward propagation**, **loss function**,
**gradient descent**, **backpropagation**, **chain rule**, **learning rate**, **epoch**, **batch**,
**momentum**, **RMSProp**, **Adam**, **weight decay**, **dropout**, **batch normalisation**,
**vanishing gradient**, **exploding gradient**, **convolution**, **kernel**, **padding**, **stride**,
**pooling**, **feature map**, **recurrent network**, **LSTM**, **GRU**, **cell state**, **attention**,
**query/key/value**, **multi-head attention**, **positional encoding**, **transformer**,
**transfer learning**, **fine-tuning**, **frozen backbone**, **autoencoder**, **latent code**,
**reconstruction error**.

All are defined in the [glossary](../../resources/glossary.md). The one-page recap is in
[summary.md](summary.md).

## Resources

- Goodfellow, Bengio & Courville (2016), *Deep Learning* — free online; chapters 6–10 cover this
  module's theory.
- Prince (2023), *Understanding Deep Learning* — free online, excellent on attention and training.
- PyTorch tutorials, "Learn the Basics" — the API reference for NB-07-02 and beyond.
- Nielsen (2015), *Neural Networks and Deep Learning* — the clearest treatment of backpropagation
  for a first encounter.
- The module's [summary](summary.md) — formulas and verified numbers for revision.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) ·
[Prerequisites](../../prerequisites/README.md) · [Next module: M08](../README.md#m08)
