# PA-07 — A Neural Network From Scratch, Then in PyTorch

| | |
| :--- | :--- |
| Assignment | 07 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M07 (L07-01 … L07-05), P02 |
| Covers | forward pass, backpropagation, training loop, overfitting diagnosis |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

You can call `loss.backward()` without understanding it, and many people do. This assignment makes
you write the backward pass by hand for a two-layer network, verify it against numerical gradients,
and then reproduce the same model in PyTorch and confirm the results agree.

## Problem scenario

Classify 8×8 handwritten digits (scikit-learn `load_digits`) with a 64→32→10 network. Implement
NumPy forward and backward passes, then compare against a PyTorch implementation with identical
initialisation.

## Learning outcomes

1. Derive and implement gradients for a two-layer network with ReLU and softmax cross-entropy.
2. Verify gradients numerically before trusting a training run.
3. Diagnose underfitting and overfitting from learning curves.
4. Explain what the framework does for you, using your own implementation as the reference.

## Tasks

1. **Forward.** Implement the forward pass from parameters, returning logits and a cache.
2. **Backward.** Implement gradients by hand; no autograd.
3. **Gradient check.** Compare analytic and numerical gradients on a small batch; report the maximum
   relative error.
4. **Train.** Mini-batch SGD with a learning-rate sweep; report accuracy vs epochs for three rates.
5. **PyTorch parity.** Reproduce with identical initial weights; report the difference in final loss.
6. **Diagnosis.** Produce one underfitting and one overfitting run, with the curves and the evidence.
7. **Report.** Include the gradient-check table and both parity numbers.

## Constraints

- NumPy only for Part 1; PyTorch only for Part 5.
- Seeded initialisation; the seed must be in the report.
- No `nn.Linear` in your own implementation.

## Expected deliverables

`numpy_net.py`, `torch_net.py`, `results.md` with gradient-check and parity tables, and learning-curve
figures.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Forward/backward correctness | 30% | gradient check passes (relative error < 1e-6) |
| Training | 20% | sensible accuracy with a justified learning rate |
| Parity with PyTorch | 20% | same initialisation, comparable loss |
| Diagnosis | 20% | under/overfitting runs identified from curves |
| Explanation | 10% | states what the framework automates |

## Bonus challenges

- Add momentum and compare convergence at the same learning rate.
- Add dropout and report both train and validation curves, explaining the divergence.

---

[Assessment index](../README.md) · [PA-06](pa-06-machine-learning.md) · [PA-08](pa-08-nlp.md)
