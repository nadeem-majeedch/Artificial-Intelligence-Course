# L09-01 — Introduction to Computer Vision

| Module | M09 · Computer Vision |
| :--- | :--- |
| Level | 300 |
| Study time | 60 minutes |
| Prerequisites | [P01 NumPy](../../../prerequisites/P01-python-programming/README.md) · [L07-01](../../M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md) (helpful) |
| Code | `code/vision_core.py` |

[← Module start](../README.md) · [Next: L09-02 Image Processing →](L09-02-image-processing-and-feature-extraction.md)

## 1. Learning Objectives

- **Describe** an image as a numeric array: shape, dtype, value range and channel order.
- **Convert** between colour representations and explain when greyscale is enough.
- **Distinguish** computer vision from image processing, with an example of each.
- **Explain** what acquisition decisions (resolution, exposure, lens, compression) cost downstream.
- **Inspect** a real array and predict what a model can and cannot recover from it.

## 2. Prerequisite Knowledge

Indexing and slicing in NumPy, array shapes, and the idea of a matrix product. If `arr[0:2, 1:3]`
is unfamiliar, read [P01 NumPy](../../../prerequisites/P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md)
first — every operation in this module is array arithmetic.

## 3. Conceptual Explanation

### 3.1 An image is an array, and nothing else

A greyscale image of height `H` and width `W` is an array of shape `(H, W)`. A colour image adds a
channel axis: `(H, W, 3)` in RGB order. Each element is a brightness sample, usually `uint8` in
`[0, 255]` for display or `float32` in `[0, 1]` for a network.

Three facts follow from that, and they explain most beginner bugs:

1. **Shape order is (rows, columns, channels).** A `(32, 32, 3)` image is 3,072 numbers, not 32.
2. **Coordinates are (y, x), not (x, y).** Every box, crop and annotation format disagrees about this;
   the mismatch is the single most common detection bug.
3. **The dtype carries meaning.** Dividing a `uint8` image by 255 in-place truncates to 0 and 1.

### 3.2 Colour spaces

| Space | Channels | Useful for | Watch out |
| :--- | :--- | :--- | :--- |
| RGB | R, G, B | display, most networks | channels are correlated |
| Greyscale | luma | shape, edges, most classical features | throws away colour that may be the signal |
| HSV | hue, saturation, value | colour thresholding, lighting robustness | hue is circular, so distances need care |
| Lab | lightness, a, b | perceptual difference, colour constancy | less familiar, more arithmetic |

Luma is a weighted sum, not an average, because the eye is more sensitive to green:

$$Y = 0.299R + 0.587G + 0.114B$$

An average of the three channels is a different (and worse) greyscale. `vision_core.to_gray`
implements the weighted version.

### 3.3 Acquisition decides the ceiling

A model cannot recover information the sensor never recorded. Four decisions dominate:

- **Resolution** — small objects need pixels; downsampling to 32×32 destroys text on a sign.
- **Exposure** — clipping at 0 or 255 is irreversible: two different bright surfaces become identical.
- **Optics** — blur is convolution with a point-spread function; deblurring amplifies noise.
- **Compression** — JPEG discards high-frequency detail, which is exactly what fine textures are.

### 3.4 Computer vision versus image processing

*Image processing* transforms an image into another image: denoise, sharpen, resize, colour-correct.
*Computer vision* extracts a decision: a class, a box, a mask, a trajectory. The two are not rivals —
every vision pipeline starts with processing, and the interesting engineering question is how much
processing to do before a learned model takes over.

### 3.5 The three tasks this module builds

| Task | Output | Metric | Lab |
| :--- | :--- | :--- | :--- |
| Classification | one label per image | accuracy, per-class recall | LAB-09-02 |
| Detection | boxes + labels | IoU, precision/recall, mAP | LAB-09-03 |
| Segmentation | one label per pixel | IoU, Dice | LAB-09-04 |

## 4. Pseudocode

```text
function INSPECT(image):
    print shape, dtype, min, max
    gray <- 0.299R + 0.587G + 0.114B
    print gray.mean(), gray.std()
    return summary

function NORMALISE(image):
    float <- image.astype(float32) / 255.0     # divide before, not after, casting
    return (float - mean) / std
```

## 5. Worked Example — reading a synthetic leaf image

The module's images are generated, so every number below is reproducible:

```python
import vision_core as v

images, labels, names = v.make_leaf_images(n_per_class=2, size=32, seed=0)
print(images.shape, images.dtype)          # (6, 32, 32, 3) uint8
print(names, labels)                       # ['healthy','spot','blight'] [..]
image = images[0]
gray = v.to_gray(image)
print(round(gray.mean(), 2), round(gray.std(), 2))
```

The shape tells you the tensor a model receives; the mean and standard deviation tell you whether the
image is bright, dark or flat. A flat image (std near zero) carries no information no matter how deep
the network.

## 6. Mathematical Formulation

For an $H \times W \times 3$ image $I$:

- memory in bytes: $H \cdot W \cdot 3 \cdot \text{bytes per element}$ (1 for `uint8`, 4 for `float32`);
- luma: $Y_{ij} = 0.299 I_{ij1} + 0.587 I_{ij2} + 0.114 I_{ij3}$;
- bilinear resize from $(H,W)$ to $(H',W')$: each output pixel is a weighted sum of the four nearest
  input pixels, with weights from the fractional coordinates.

Downsampling by a factor $k$ without smoothing aliases: two distinct textures can collapse onto the
same samples. That is why a resize is usually *blur then subsample*, not subsample alone.

## 7. Python Implementation

```python
import numpy as np
import vision_core as v

images, labels, names = v.make_sign_images(n_per_class=4, size=32, seed=1)
print("batch:", images.shape, images.dtype, images.min(), images.max())

gray = v.to_gray(images[0])
print("gray stats:", round(gray.mean(), 1), round(gray.std(), 1))

# a cheap colour feature: mean and standard deviation per channel
features = np.concatenate([images.reshape(len(images), -1, 3).mean(1),
                           images.reshape(len(images), -1, 3).std(1)], axis=1)
print("feature matrix:", features.shape)

# class balance is part of inspecting a dataset
unique, counts = np.unique(labels, return_counts=True)
print(dict(zip([names[u] for u in unique], counts)))
```

## 8. Practical Applications

- **Agriculture** — leaf disease screening from phone photos (LAB-09-01, LAB-09-02).
- **Transport** — traffic-sign recognition and vehicle detection (LAB-09-02, LAB-09-03).
- **Robotics** — road-scene segmentation for free-space estimation (LAB-09-04).
- **Education** — segmentation of annotated medical images for teaching; never a clinical claim.
- **Quality control** — defect detection on production lines, where lighting is controlled.

## 9. Common Mistakes

1. **Confusing (x, y) and (row, column).** Draw one box by hand before trusting any annotation code.
2. **Normalising with `uint8` arithmetic**, which silently clips.
3. **Splitting a dataset after augmentation**, so near-duplicates of test images leak into training.
4. **Reporting accuracy on a balanced synthetic set and calling it field performance.**
5. **Assuming a greyscale conversion is lossless.** Colour is often the class signal.

## 10. Exercises

1. Generate 5 images per class and print shape, dtype and per-channel mean for each. Which channel
   separates `stop` from `mandatory` signs best, and why?
2. Compute luma two ways — weighted and plain mean — and report the maximum absolute difference.
   Which produces a darker image for a mostly green leaf?
3. Downsample a 32×32 image to 16×16 and back to 32×32 with nearest-neighbour sampling, and describe
   exactly what was lost.
4. Write `to_hsv` for a single pixel using the standard formula, and check it against `cv2.cvtColor`.

## 11. Self-Assessment

1. Why is an image's dtype part of its meaning?
   *Because the same numbers mean different brightnesses at different scales; `uint8` and `float32`
   pipelines are not interchangeable without an explicit conversion.*
2. When is greyscale preferable to colour?
   *When shape or texture carries the signal and colour is a nuisance variable (lighting, white
   balance), or when compute is tight.*
3. What does a `(32, 32, 3)` array contain?
   *32 rows × 32 columns × 3 colour channels = 3,072 samples.*

## 12. Key Terms

**Pixel**, **channel**, **luma**, **colour space**, **resolution**, **aliasing**, **point-spread
function**, **image processing**, **computer vision**. Definitions: [glossary](../../../resources/glossary.md).

## 13. Further Reading

- Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed., ch. 1–2 (free PDF from the author).
- OpenCV documentation, "Getting Started with Images" — the practical reference for I/O and colour conversion.

## What to Do Next

Continue to [L09-02 Image Processing and Feature Extraction](L09-02-image-processing-and-feature-extraction.md),
then run [NB-09-01](../notebooks/nb-09-01-image-processing.ipynb) before starting
[LAB-09-01](../labs/lab-09-01-image-processing-and-feature-extraction.md).
