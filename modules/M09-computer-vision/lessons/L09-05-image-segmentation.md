# L09-05 — Image Segmentation

| Module | M09 · Computer Vision |
| :--- | :--- |
| Level | 300 |
| Study time | 80 minutes |
| Prerequisites | [L09-04](L09-04-object-detection.md) |
| Code | `code/vision_core.py` |

[← Previous: L09-04](L09-04-object-detection.md) · [Next: L09-06 Advanced Vision →](L09-06-advanced-computer-vision.md)

## 1. Learning Objectives

- **Distinguish** semantic, instance and panoptic segmentation by their outputs.
- **Draw** an encoder–decoder with skip connections and explain why the skips exist.
- **Compute** Dice and IoU for a mask and explain when they disagree with pixel accuracy.
- **Choose** a loss for class-imbalanced masks and justify it.
- **State** the practical limits of an educational segmentation model.

## 2. Prerequisite Knowledge

Convolution and pooling (L09-03), and per-class metrics (L09-04). The decoder is the same arithmetic as
the encoder, run in the other direction.

## 3. Conceptual Explanation

### 3.1 Three flavours

| Variant | Output | Question answered |
| :--- | :--- | :--- |
| Semantic | one label per pixel | "which pixels are road?" |
| Instance | one mask per object | "which pixels are *this* car?" |
| Panoptic | semantic + instances | "every pixel, with countable objects separated" |

A semantic model cannot tell two adjacent cars apart; an instance model does not label the sky. Panoptic
segmentation is the union, and it is what a driving stack actually needs.

### 3.2 Encoder–decoder and skip connections

The encoder downsamples: resolution falls, semantic meaning rises. The decoder upsamples back to the
input size. Plain upsampling loses precisely the fine boundaries that segmentation is judged on, so
**U-Net** concatenates encoder features into the decoder at each resolution. The skips carry *where*;
the bottleneck carries *what*. That is the whole idea, and it is why U-Net remains the default baseline
a decade later.

Upsampling is usually nearest-neighbour or bilinear followed by a convolution, or a transposed
convolution — each has different checkerboard artefacts.

### 3.3 Losses

- **Pixel-wise cross-entropy** — treats each pixel as a classification. Dominated by the largest class.
- **Dice loss** $1 - \frac{2|A\cap B|}{|A|+|B|}$ — optimises overlap directly, insensitive to class size.
- **Focal loss** — down-weights easy pixels, focusing capacity on hard ones.
- **Combined CE + Dice** — stable gradients early, overlap pressure late. The usual practical choice.

On the synthetic road scenes here, obstacles are about **1.4% of pixels**. A model that predicts "road or
sky" and never says "obstacle" reaches 98.6% pixel accuracy and has Dice 0 for the class that matters.
That is the argument for Dice and per-class IoU.

### 3.4 Metrics

$$\mathrm{IoU}_c = \frac{|P_c \cap G_c|}{|P_c \cup G_c|}, \qquad
\mathrm{Dice}_c = \frac{2|P_c \cap G_c|}{|P_c| + |G_c|}$$

$\mathrm{Dice} = 2\,\mathrm{IoU}/(1+\mathrm{IoU})$: they rank models the same way, so report one and say
which. Mean IoU averages over classes; a class absent from both prediction and truth is skipped, not
counted as 1.0.

### 3.5 Practical limitations

Segmentation fails at boundaries, on rare classes, under domain shift (rain, night), and when annotation
rules are inconsistent. An educational model trained on synthetic scenes has learned the generator, not
the world — this module says so in every lab, and it never claims clinical or safety certification.

## 4. Pseudocode

```text
function UNET_FORWARD(x):
    e1 <- conv_block(x)          # H x W
    e2 <- conv_block(pool(e1))   # H/2
    e3 <- conv_block(pool(e2))   # H/4
    b  <- conv_block(pool(e3))   # H/8 bottleneck
    d3 <- conv_block(cat(upsample(b), e3))
    d2 <- conv_block(cat(upsample(d3), e2))
    d1 <- conv_block(cat(upsample(d2), e1))
    return softmax(conv1x1(d1))
```

## 5. Worked Example — a baseline and its blind spot

```python
import numpy as np
import vision_core as v

image, truth = v.make_road_scene(seed=3)
print("class fractions:", {c: round(float((truth == c).mean()), 3) for c in (0, 1, 2)})
print("obstacle share:", round(float((truth == 2).mean()), 3))       # ~0.014

# baseline: blue means sky, everything else road, obstacles never predicted
baseline = np.where(image[:, :, 2] > 150, 1, 0).astype(np.uint8)
print("pixel accuracy:", round(float((baseline == truth).mean()), 3))   # high
print("mIoU:", round(v.mean_iou(baseline, truth), 3))                   # ~0.65
print("obstacle Dice:", round(v.dice(baseline, truth, 2), 3))           # 0.0
```

Three numbers, one story: 98%+ pixel accuracy, mediocre mIoU, zero recall on the class that matters.

## 6. Mathematical Formulation

Soft Dice for class $c$ with prediction probabilities $p_i$ and targets $y_i$:

$$\mathcal{L}_{Dice} = 1 - \frac{2\sum_i p_i y_i + \epsilon}{\sum_i p_i + \sum_i y_i + \epsilon}$$

The $\epsilon$ prevents division by zero when a class is absent from a batch — omit it and training
produces NaNs on exactly the batches you care about.

## 7. Python Implementation

```python
import numpy as np
import vision_core as v

image, truth = v.make_road_scene(seed=5)

# a slightly better rule: obstacles are brown (red clearly above blue)
predicted = np.zeros_like(truth)
predicted[image[:, :, 2] > 150] = 1                       # sky
brown = (image[:, :, 0].astype(int) - image[:, :, 2].astype(int)) > 40
predicted[brown] = 2                                      # obstacle
print("mIoU:", round(v.mean_iou(predicted, truth), 3))
for label in (0, 1, 2):
    print(label, "Dice:", round(v.dice(predicted, truth, label), 3))

# how a boundary error costs: shift the prediction by one pixel
shifted = np.roll(predicted, 1, axis=1)
print("shifted mIoU:", round(v.mean_iou(shifted, truth), 3))
```

## 8. Practical Applications

- **Road-scene understanding** — free space, drivable area, obstacles (LAB-09-04).
- **Medical imaging education** — organ or lesion outlines on public teaching datasets; never a diagnosis.
- **Agriculture** — plot boundaries and canopy coverage from drone imagery.
- **Document layout** — text blocks, tables and figures for OCR pipelines.

## 9. Common Mistakes

1. Reporting pixel accuracy on class-imbalanced masks.
2. Counting absent classes as perfect (mIoU inflated to 1.0).
3. Forgetting `epsilon` in a Dice loss, then debugging NaNs.
4. Comparing a model trained on 64×64 masks against one evaluated at full resolution.
5. Using bilinear upsampling without a final convolution, producing blocky boundaries.

## 10. Exercises

1. Compute Dice and IoU for one class from a 4×4 toy mask pair and verify the identity
   $\mathrm{Dice} = 2\mathrm{IoU}/(1+\mathrm{IoU})$.
2. Extend the brown-obstacle rule with a size filter (drop regions under 20 pixels) and report the
   change in obstacle Dice.
3. Explain why a skip connection helps boundaries but increases memory, in two sentences.
4. Design a loss for a dataset where obstacles are 1% of pixels, and state what could go wrong with it.

## 11. Self-Assessment

1. What does the bottleneck of a U-Net represent?
   *The most downsampled, most semantic feature map — what is present, with little location information.*
2. Why are skip connections concatenations rather than additions in U-Net?
   *Concatenation keeps fine and coarse features separate for the next convolution to weight; addition
   forces them into one channel budget.*
3. When is Dice preferable to pixel accuracy?
   *Whenever the interesting class is small: Dice ignores the true negatives that inflate accuracy.*

## 12. Key Terms

**Semantic segmentation**, **instance segmentation**, **panoptic segmentation**, **encoder–decoder**,
**skip connection**, **U-Net**, **Dice coefficient**, **focal loss**, **upsampling**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Ronneberger, Fischer and Brox (2015), "U-Net: Convolutional Networks for Biomedical Image Segmentation".
- Sudre et al. (2017), "Generalised Dice Overlap as a Deep Learning Loss Function".

## What to Do Next

Continue to [L09-06 Advanced Computer Vision](L09-06-advanced-computer-vision.md), and complete
[LAB-09-04](../labs/lab-09-04-image-segmentation-with-unet.md).
