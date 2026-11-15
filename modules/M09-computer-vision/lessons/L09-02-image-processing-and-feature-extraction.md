# L09-02 — Image Processing and Feature Extraction

| Module | M09 · Computer Vision |
| :--- | :--- |
| Level | 300 |
| Study time | 75 minutes |
| Prerequisites | [L09-01](L09-01-introduction-to-computer-vision.md) |
| Code | `code/vision_core.py` |

[← Previous: L09-01](L09-01-introduction-to-computer-vision.md) · [Next: L09-03 CNNs →](L09-03-image-classification-and-cnns.md)

## 1. Learning Objectives

- **Implement** 2-D convolution and predict output shapes for `same` and `valid` padding.
- **Explain** what a blur, a sharpen and a Sobel kernel each compute.
- **Apply** Otsu thresholding and morphological opening to isolate objects.
- **Compute** a HOG descriptor by hand for a small cell grid and state its dimensionality.
- **Choose** between classical features and a learned model for a given data budget.

## 2. Prerequisite Knowledge

Array slicing, and the idea that a small matrix can be slid over a larger one. No calculus is needed:
every operation here is a weighted sum of neighbours.

## 3. Conceptual Explanation

### 3.1 Convolution is a weighted sum of neighbours

A kernel $K$ of size $k \times k$ is placed over each pixel; the output is $\sum K_{uv} I_{i+u,j+v}$.
Formally this is *cross-correlation*; deep-learning frameworks call it convolution and flip nothing.
The distinction matters only when you compare against a signal-processing textbook.

Output size for an input of size $n$, kernel $k$, padding $p$ and stride $s$:

$$n_{out} = \left\lfloor \frac{n + 2p - k}{s} \right\rfloor + 1$$

With `same` padding ($p = \lfloor k/2 \rfloor$, $s=1$) the output matches the input; with `valid`
padding ($p=0$) it shrinks by $k-1$.

### 3.2 Three kernels you must recognise

| Kernel | Effect | Why |
| :--- | :--- | :--- |
| $\frac{1}{9}$ of all-ones (3×3) | blur | local average, removes high frequency |
| centre 5, neighbours −1 | sharpen | original minus a blurred copy |
| Sobel $G_x$, $G_y$ | vertical / horizontal edges | discrete derivative |

Edge magnitude is $\sqrt{G_x^2 + G_y^2}$; direction is $\arctan(G_y/G_x)$. The magnitude image is what
most classical pipelines threshold.

### 3.3 Thresholding and morphology

Otsu's method chooses the threshold $t$ that maximises the between-class variance of the two intensity
groups — no parameter to tune, which is why it is the default for bimodal images and a poor choice for
anything else. Morphological **erosion** removes isolated pixels, **dilation** fills gaps, **opening**
(erode then dilate) removes specks, **closing** (dilate then erode) fills holes.

Segmentation fundamentals follow: threshold → clean with morphology → label connected components →
measure area and shape. That pipeline is a legitimate baseline, and every learned segmentation model
should be compared against it.

### 3.4 Classical descriptors

A descriptor turns a patch into a fixed-length vector that survives small changes.

- **HOG** — gradients binned by orientation over cells; length $= (H/c)\,(W/c)\,b$ for cell size $c$ and
  $b$ bins. For a 96×96 image with 8-pixel cells and 9 bins: $12 \cdot 12 \cdot 9 = 1{,}296$ numbers.
- **SIFT / ORB** — keypoints with scale and rotation invariance; ORB is the fast, patent-free choice.
- **Colour histograms** — cheap, robust to translation, blind to shape.

Their weakness is the same: they encode what the designer thought mattered. A CNN learns the same
thing end to end, given the data to do it.

## 4. Pseudocode

```text
function EDGE_PIPELINE(image):
    gray  <- luma(image)
    blur  <- convolve(gray, gaussian(5, 1.0))
    mag   <- hypot(convolve(blur, sobel_x), convolve(blur, sobel_y))
    t     <- otsu(mag)
    mask  <- mag > t
    mask  <- closing(opening(mask, 3), 3)
    return mask

function HOG(gray, cell, bins):
    gx, gy <- sobel(gray)
    angle  <- atan2(gy, gx) mod 180 degrees
    hist   <- weighted bincount per cell
    return flatten(normalise_each_cell(hist))
```

## 5. Worked Example — a synthetic road scene

`make_road_scene` returns an image and an exact three-class mask (road, sky, obstacle). A baseline of
"blue channel above 150 means sky" scores **mean IoU 0.65** and **Dice 0.00 for the obstacle class** —
it never predicts an obstacle at all, because obstacles are brownish and sky is blue. That single number
is the argument for LAB-09-04: a rule that looks reasonable leaves an entire class undetected, and
per-class metrics are what expose it.

## 6. Mathematical Formulation

Convolution as a sum:

$$(I * K)_{ij} = \sum_{u=0}^{k-1}\sum_{v=0}^{k-1} K_{uv}\, I_{i+u-p,\, j+v-p}$$

Otsu maximises

$$\sigma_b^2(t) = \omega_0(t)\,\omega_1(t)\,\big(\mu_0(t) - \mu_1(t)\big)^2$$

over thresholds $t$, where $\omega$ are class proportions and $\mu$ class means.

Dice and IoU for a mask $A$ against truth $B$:

$$\mathrm{Dice} = \frac{2|A \cap B|}{|A| + |B|}, \qquad \mathrm{IoU} = \frac{|A \cap B|}{|A \cup B|}$$

## 7. Python Implementation

```python
import numpy as np
import vision_core as v

image, mask = v.make_road_scene(seed=3)
gray = v.to_gray(image)

blurred = v.convolve2d(gray, v.gaussian_kernel(5, 1.0))
edges = v.sobel_magnitude(blurred)

# 1. convolution preserves shape with 'same' and shrinks with 'valid'
print(v.convolve2d(gray, np.ones((3, 3)) / 9).shape, v.convolve2d(gray, np.ones((3, 3)) / 9, "valid").shape)
print("edge max:", round(float(edges.max()), 1))

# 2. threshold + morphology
threshold = v.otsu_threshold(gray)
binary = gray > threshold
opened = v.dilate(v.erode(binary, 3), 3)
print("threshold:", threshold, "| pixels kept:", int(opened.sum()))

# 3. HOG dimensionality
descriptor = v.hog_descriptor(gray, cell=8, bins=9)
print("HOG length:", descriptor.size, "expected:", (gray.shape[0] // 8) * (gray.shape[1] // 8) * 9)

# 4. the baseline and its per-class failure
predicted = np.where(image[:, :, 2] > 150, 1, 0).astype(np.uint8)
print("mIoU:", round(v.mean_iou(predicted, mask), 3), "| obstacle Dice:", round(v.dice(predicted, mask, 2), 3))
```

## 8. Practical Applications

- **Industrial inspection**: edge + morphology finds missing parts under controlled lighting, in
  microseconds, with no training data.
- **Document analysis**: deskew, binarise, then OCR — the classical pipeline still ships.
- **Preprocessing for networks**: normalisation and augmentation are image processing, and they decide
  whether the network sees a stable distribution.
- **Annotation assistance**: an edge or HOG detector proposes regions for a human to accept.

## 9. Common Mistakes

1. Convolving a `uint8` array, so every negative kernel weight wraps around modulo 256.
2. Forgetting that a blur and a resize are not the same operation, then blaming the model for aliasing.
3. Tuning a threshold on the test image and reporting the score.
4. Reporting accuracy for segmentation when one class occupies 90% of the pixels.
5. Using HOG with a cell size that does not divide the image, and silently dropping the remainder.

## 10. Exercises

1. Convolve a 10×10 array with a 3×3 kernel under `same` and `valid`; confirm the shapes from the
   formula, then from the code.
2. Build a sharpening kernel and apply it to a blurred leaf image. Measure the variance before and
   after — why does sharpening increase it?
3. Replace the sky rule with a rule for obstacles (brown: R > G > B). Compute the obstacle Dice and
   explain what improved and what got worse.
4. Compute HOG for cell sizes 4, 8 and 16 and report the three vector lengths. Which loses the most
   information, and what evidence supports your answer?

## 11. Self-Assessment

1. Why does `padding='same'` require the kernel size to be odd in this implementation?
   *So the padding can be split evenly; an even kernel has no unique centre and shifts the output by
   half a pixel.*
2. What does an opening operation remove that a closing does not?
   *Small isolated bright specks; closing fills small dark holes instead.*
3. Why is Otsu a poor choice for a natural photograph?
   *Its two-class assumption fails when the histogram is not bimodal, so the threshold lands somewhere
   arbitrary.*

## 12. Key Terms

**Kernel**, **convolution**, **cross-correlation**, **padding**, **stride**, **Sobel operator**,
**Otsu threshold**, **morphology**, **opening**, **closing**, **HOG**, **descriptor**, **connected
components**. Definitions: [glossary](../../../resources/glossary.md).

## 13. Further Reading

- Szeliski, ch. 3 (image processing) and ch. 7 (feature detection).
- Dalal and Triggs (2005), "Histograms of Oriented Gradients for Human Detection" — the original HOG paper.

## What to Do Next

Continue to [L09-03 Image Classification and CNNs](L09-03-image-classification-and-cnns.md), and run
[LAB-09-01](../labs/lab-09-01-image-processing-and-feature-extraction.md) to implement the pipeline
above on the leaf dataset.
