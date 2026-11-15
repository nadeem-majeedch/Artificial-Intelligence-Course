# L09-03 — Image Classification and CNNs

| Module | M09 · Computer Vision |
| :--- | :--- |
| Level | 300 |
| Study time | 80 minutes |
| Prerequisites | [L09-02](L09-02-image-processing-and-feature-extraction.md) · [L07-03](../../M07-neural-networks-and-deep-learning/lessons/L07-05-convolutional-neural-networks.md) |
| Code | `code/vision_core.py` |

[← Previous: L09-02](L09-02-image-processing-and-feature-extraction.md) · [Next: L09-04 Object Detection →](L09-04-object-detection.md)

## 1. Learning Objectives

- **Draw** the classification pipeline from pixels to a predicted label and a loss.
- **Compute** convolution output sizes and parameter counts for a small CNN.
- **Explain** what pooling buys and what it destroys.
- **Train** a CNN, read its learning curve, and detect overfitting from the gap.
- **Justify** augmentation as a prior, not a trick.

## 2. Prerequisite Knowledge

The convolution arithmetic from [L09-02](L09-02-image-processing-and-feature-extraction.md), and the
training loop — forward pass, loss, gradient, update — from
[L07-02](../../M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md).

## 3. Conceptual Explanation

### 3.1 The pipeline

```text
image → resize/normalise → [conv → activation → pool] × n → flatten → linear → softmax → loss
```

Classification assigns **one label to the whole image**. Everything else (detection, segmentation)
adds a spatial output on top of this backbone.

### 3.2 Why convolution instead of a dense layer

A dense layer on a 32×32×3 image already has 3,072 inputs per unit and no notion of locality. A
convolution shares one small filter across all positions, which gives two properties that matter:

- **Translation equivariance** — a leaf spot detected at the top-left is detected anywhere.
- **Parameter efficiency** — a 3×3×3 filter has 27 weights regardless of image size.

### 3.3 Counting what a layer costs

For a convolution with $C_{in}$ input channels, $C_{out}$ filters of size $k \times k$:

$$\text{params} = C_{out}\,(C_{in} k^2 + 1), \qquad
\text{output size} = \left\lfloor \frac{n + 2p - k}{s}\right\rfloor + 1$$

`TinyCNN` in `vision_core.py` is `Conv2d(3,8,3)` → pool → `Conv2d(8,16,3)` → pool → dense(32) →
dense(3). The first layer has $8(3 \cdot 9 + 1) = 224$ parameters; the second has
$16(8 \cdot 9 + 1) = 1{,}168$. The whole model is a few thousand parameters — small enough to train on
a CPU in seconds, large enough to learn colour and texture statistics.

### 3.4 Pooling

Max-pooling by 2 halves each spatial dimension, so a 32×32 feature map becomes 16×16, then 8×8. It
buys translation tolerance and compute, and it destroys the precise location of what it kept. That is
exactly the trade-off that makes pooling fine for classification and a problem for segmentation.

### 3.5 Training, and the gap that matters

The loop is ordinary supervised learning: cross-entropy on the logits, Adam, mini-batches. What is
specific to vision is the gap between training and validation accuracy. On the synthetic sign set
(40 images per class, 75/25 split, 3 epochs) the tiny CNN reaches **0.878 training accuracy** and
**1.000 test accuracy** — the data is easy and the split is small. On the leaf set (60 per class,
8 epochs) it reaches about **0.76 training** and **0.95 test**. Neither number means much alone:
the same HOG + logistic-regression baseline also scores 1.00 on signs and 0.95 on leaves. The lesson is
not "CNNs are better"; it is that **on small, easy, synthetic data a classical baseline is competitive,
and you owe the reader that comparison**.

### 3.6 Augmentation as a prior

Flipping, small rotations and brightness jitter encode beliefs: the label should not change under these
transformations. Augment only with transformations that preserve the label. A horizontal flip turns a
left-turn sign into a right-turn sign, so flipping is wrong for that class — and no amount of epochs
fixes a corrupted prior.

## 4. Pseudocode

```text
function TRAIN(images, labels, epochs):
    model <- TinyCNN()
    for epoch in 1..epochs:
        for batch in shuffle(images):
            logits <- model(batch / 255)
            loss   <- cross_entropy(logits, labels)
            loss.backward(); optimiser.step(); optimiser.zero_grad()
        record(train_loss, train_accuracy)
    return model
```

## 5. Worked Example — three sign families

```python
import numpy as np
import vision_core as v

images, labels, names = v.make_sign_images(n_per_class=40, size=32, seed=0)
cut = int(len(labels) * 0.75)
model, history = v.train_classifier(images[:cut], labels[:cut], epochs=3, seed=0)
print([(h["epoch"], round(h["train_accuracy"], 3)) for h in history])

predicted = v.predict(model, images[cut:])
print("test accuracy:", round(float((predicted == labels[cut:]).mean()), 3))
print(v.confusion_matrix(predicted, labels[cut:], 3))   # rows truth, columns prediction
```

A confusion matrix on nine test images is a diagnostic, not a statistic: it tells you *which* classes
collide, which is what you need before collecting more data.

## 6. Mathematical Formulation

Cross-entropy for $C$ classes with logits $z$ and true class $y$:

$$\mathcal{L} = -\log\frac{e^{z_y}}{\sum_{c} e^{z_c}} = -z_y + \log\sum_c e^{z_c}$$

Gradient with respect to the logits is $\hat{p} - \text{onehot}(y)$ — the softmax probability minus the
truth. Every classification loss in this module reduces to that.

## 7. Python Implementation

```python
import numpy as np
import vision_core as v

# parameter count by hand, then by the model
print("conv1 params:", 8 * (3 * 3 * 3 + 1))    # 224
print("conv2 params:", 16 * (8 * 3 * 3 + 1))   # 1168

images, labels, names = v.make_leaf_images(n_per_class=60, size=32, seed=1)
cut = 140
model, history = v.train_classifier(images[:cut], labels[:cut], epochs=8, seed=0)
print("final train accuracy:", round(history[-1]["train_accuracy"], 3))
print("test accuracy:", round(float((v.predict(model, images[cut:]) == labels[cut:]).mean()), 3))

# augmentation as a prior: it changes what the model sees, not the labels
rng = np.random.default_rng(0)
augmented = np.stack([v.augment(img, rng) for img in images[:6]])
print("augmented batch:", augmented.shape, augmented.dtype)
```

## 8. Practical Applications

- **Plant disease triage** — three-way classification of leaf images, with a per-class recall report.
- **Traffic-sign recognition** — the classic small-image benchmark; augmentation matters more than depth.
- **Defect detection** — controlled lighting makes a small CNN beat a large pretrained one.
- **Feature extraction** — a trained backbone's penultimate layer is a useful embedding (L09-06).

## 9. Common Mistakes

1. Reporting test accuracy from a split made before augmentation, leaking near-duplicates.
2. Dividing by 255 after casting to `uint8`.
3. Using accuracy on imbalanced classes; per-class recall exposes the collapse.
4. Augmenting with label-changing transforms (flips for directional signs).
5. Comparing a CNN against no baseline at all.

## 10. Exercises

1. Compute the parameter count of a `Conv2d(16, 32, 5, padding=2)` layer and verify it in PyTorch.
2. Train with and without augmentation on the leaf set and report both test accuracies. If they are
   equal, explain why augmentation bought nothing here.
3. Build a confusion matrix for the leaf classifier and identify the most confused pair.
4. Freeze the first convolution (set `requires_grad=False`) and retrain; how much accuracy do you lose?

## 11. Self-Assessment

1. Why does a 3×3 convolution with `padding=1` preserve spatial size?
   *It adds one ring of zeros, so each output position sees a full 3×3 window: $(n + 2 - 3)/1 + 1 = n$.*
2. What information does max-pooling discard?
   *The position of the maximum within each window; only the strongest response survives.*
3. Why is a training accuracy of 0.99 with test accuracy of 0.55 a problem, and what is the first thing
   to check?
   *It is overfitting or leakage; check the split and augmentation order before adding regularisation.*

## 12. Key Terms

**Feature map**, **stride**, **padding**, **pooling**, **receptive field**, **parameter sharing**,
**cross-entropy**, **augmentation**, **overfitting**, **baseline**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- LeCun, Bengio and Hinton (2015), "Deep Learning", *Nature* 521 — the canonical short survey.
- PyTorch tutorial "Training a Classifier" — the reference implementation pattern.

## What to Do Next

Continue to [L09-04 Object Detection](L09-04-object-detection.md), and complete
[LAB-09-02](../labs/lab-09-02-image-classification-with-cnns.md).
