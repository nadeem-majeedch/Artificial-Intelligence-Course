# LAB-09-02 — Image Classification Using CNNs

| | |
| :--- | :--- |
| Module | M09 · Computer Vision |
| Level | 300 |
| Time | 3 hours |
| Prerequisites | [L09-03](../lessons/L09-03-image-classification-and-cnns.md), LAB-09-01 |
| Dataset | synthetic traffic signs and leaf images (`vision_core.py`) |
| Code | `code/vision_core.py` |

[← LAB-09-01](lab-09-01-image-processing-and-feature-extraction.md) · [Next lab: LAB-09-03 →](lab-09-03-object-detection.md)

## 1. Learning objectives

- **Build** a CNN classifier pipeline with a reproducible train/test split.
- **Compute** convolution output sizes and parameter counts before running the model.
- **Train** with and without augmentation and compare the outcomes honestly.
- **Read** a learning curve and a confusion matrix as diagnostics.
- **Defend** a model choice against a classical baseline rather than against nothing.

## 2. Scenario

A city transport authority is piloting automatic traffic-sign logging from dash-cams. The prototype must
classify three sign families — stop (red octagon), warning (yellow triangle) and mandatory (blue disc) —
before it is worth collecting real footage. Your team built a synthetic generator so the pipeline can be
validated end to end before a single real image is annotated.

## 3. Problem statement

Train a small convolutional network on the synthetic sign dataset and evaluate it properly:

1. split 75/25, stratified, with a fixed seed;
2. compute the parameter count of both convolution layers by hand;
3. train for three epochs and record loss and training accuracy per epoch;
4. evaluate on the held-out 25% and produce a confusion matrix;
5. repeat with augmentation and with the HOG baseline from LAB-09-01;
6. decide — with evidence — which pipeline you would ship to the pilot, and what you would measure next.

## 4. Background concepts

- Output size: $\lfloor (n + 2p - k)/s \rfloor + 1$; parameters: $C_{out}(C_{in}k^2 + 1)$.
- Pooling halves spatial dimensions and discards within-window position.
- Cross-entropy on logits; softmax probabilities sum to one.
- Augmentation is a prior: it must not change the label.
- A confusion matrix with 30 test images is a diagnostic, not a statistic.

## 5. Dataset information and licensing

Both datasets are **generated in code** (`make_sign_images`, `make_leaf_images`) and are course-authored
synthetic data; nothing is redistributed, and the data is dedicated to CC0 1.0. Sizes: 40 images per class at 32×32×3
for signs (120 total), 60 per class for leaves (180 total). Class balance is exact by construction, which
is convenient for learning and unrealistic for deployment — say so in your report.

## 6. Software requirements

Python 3.10+, NumPy, PyTorch (CPU is enough), scikit-learn and Matplotlib for the baseline and plots.
No GPU, no downloads, no pretrained weights. `torchvision` is **not** required.

## 7. Step-by-step tasks

1. Generate the sign dataset with `seed=0`; print the shape, dtype and class counts.
2. Compute by hand: parameters of `Conv2d(3,8,3)`, of `Conv2d(8,16,3)`, and the flatten size after two
   2×2 pools on 32×32 input. Verify with `model.parameters()`.
3. Train three epochs at the default learning rate; print the history.
4. Evaluate: test accuracy and confusion matrix. Which class, if any, is confused?
5. Train again with `use_augmentation=True` and compare. State whether augmentation helped, hurt, or made
   no measurable difference, and why on this data.
6. Repeat tasks 3–5 on the leaf dataset with 8 epochs and report the training/test gap.
7. Run the HOG + logistic-regression baseline on both datasets.
8. Write a recommendation: which pipeline, which metric to monitor in the pilot, and which data you would
   collect first.

## 8. Starter code

```python
import numpy as np
import vision_core as v

images, labels, names = v.make_sign_images(n_per_class=40, size=32, seed=0)
cut = int(len(labels) * 0.75)

# parameters by hand
print("conv1:", 8 * (3 * 3 * 3 + 1), "conv2:", 16 * (8 * 3 * 3 + 1))
print("flatten:", 16 * (32 // 4) * (32 // 4))

model, history = v.train_classifier(images[:cut], labels[:cut], epochs=3, seed=0)
print([(h["epoch"], round(h["loss"], 3), round(h["train_accuracy"], 3)) for h in history])

predicted = v.predict(model, images[cut:])
print("test accuracy:", round(float((predicted == labels[cut:]).mean()), 3))
print(v.confusion_matrix(predicted, labels[cut:], 3))

aug_model, aug_history = v.train_classifier(images[:cut], labels[:cut], epochs=3, seed=0,
                                            use_augmentation=True)
print("augmented test accuracy:",
      round(float((v.predict(aug_model, images[cut:]) == labels[cut:]).mean()), 3))
```

## 9. Expected behaviour

On the sign dataset the model reaches about **0.88 training accuracy by epoch 3** and **1.00 test
accuracy**; with only 30 test images that means "no errors on this sample", not "perfect in the field".
On leaves (8 epochs, 140/40 split) training accuracy is about **0.76** and test about **0.95**.

The important expected result is the comparison: **HOG + logistic regression also scores 1.00 on signs
and about 0.95 on leaves**. On tiny, easy, synthetic data the classical baseline is competitive. Your
report must contain that comparison, because a model that is only compared with itself has not been
evaluated.

## 10. Evaluation metrics

| Metric | Use |
| :--- | :--- |
| Training accuracy | detect underfitting (low) and overfitting (gap to test) |
| Test accuracy | headline, with the test-set size stated |
| Per-class recall | expose a collapsed class |
| Parameter count | the deployment cost argument |
| Wall-clock per epoch | the practical cost of the extra complexity |

## 11. Testing instructions

- Assert `len(history) == epochs` and that accuracy is in `[0, 1]`.
- Assert the confusion matrix sums to the test-set size.
- Re-run with `seed=1`; if sign test accuracy drops below 0.9, your conclusion about "perfect" was wrong.
- Check that augmentation changes the training set: `augment` must alter pixels, not just return a copy.
- Confirm `python code/vision_core.py` prints `vision_core self-test: True`.

## 12. Submission requirements

Code, the three histories, both confusion matrices, the baseline comparison table, and a recommendation of
at most 200 words. State seeds, epochs, split sizes and the machine you ran on.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Correct implementation | 20% | shapes and parameter counts verified before training |
| Experimental discipline | 25% | fixed seeds, stated splits, no test-set tuning |
| Diagnostics | 25% | history and confusion matrix interpreted, not just printed |
| Honest comparison | 20% | baseline included, conclusion limited by the evidence |
| Communication | 10% | recommendation is specific and measurable |

## 14. Extension challenges

1. **Class imbalance.** Drop 80% of the `stop` images and report accuracy versus per-class recall. Which
   number hides the problem?
2. **Label-changing augmentation.** Add horizontal flipping and measure the effect on `warning` (triangle)
   versus `mandatory` (disc). Explain the asymmetry.
3. **Depth versus data.** Add a third convolution block and retrain on the same 90 images. Does more
   capacity help, hurt, or merely overfit faster?
4. **Corruption study.** Apply Gaussian noise, blur and brightness shifts to the test set at increasing
   severity and plot accuracy against severity — the beginning of PA-09.

## Reflection

The network is not the interesting part of this lab; the comparison is. Any pipeline that reaches 1.00 on
30 easy images is unproven, and the classical baseline reaching the same number tells you the dataset is
the limiting factor, not the architecture. That conclusion is only available if you run both.
