# LAB-09-01 — Image Processing and Feature Extraction

| | |
| :--- | :--- |
| Module | M09 · Computer Vision |
| Level | 300 |
| Time | 2.5 hours |
| Prerequisites | [L09-01](../lessons/L09-01-introduction-to-computer-vision.md), [L09-02](../lessons/L09-02-image-processing-and-feature-extraction.md) |
| Dataset | synthetic leaf images from `code/vision_core.py` |
| Code | `code/vision_core.py` |

[← Module](../README.md) · [Next lab: LAB-09-02 →](lab-09-02-image-classification-with-cnns.md)

## 1. Learning objectives

- **Inspect** an image dataset as arrays: shape, dtype, value range, class balance.
- **Implement** convolution, Sobel edge detection, Otsu thresholding and morphology from scratch.
- **Build** a classical feature pipeline (HOG + linear classifier) and report per-class results.
- **Diagnose** failures of hand-designed rules using per-class metrics rather than accuracy.
- **Report** a comparison between two feature representations without overstating either.

## 2. Scenario

An agricultural technology company wants a cheap first-pass screen for leaf disease on low-power
devices: a phone photograph arrives, and the device must flag "healthy", "spot" or "blight". Before
anyone trains a network, the engineering team asks a simpler question: **how far do classical image
processing and hand-designed features get us?**

You are the engineer answering that question.

## 3. Problem statement

Using the synthetic leaf dataset (three classes, 32×32 RGB), build and evaluate a classical pipeline:

1. inspect the data and report its statistics;
2. implement filtering, edge detection and morphology on one example;
3. extract HOG descriptors for all images;
4. train a linear classifier on those descriptors;
5. report accuracy **and** per-class recall, and explain any failure.

## 4. Background concepts

- Convolution as a weighted sum of neighbours; `same` versus `valid` output sizes.
- Luma conversion: $Y = 0.299R + 0.587G + 0.114B$.
- Otsu thresholding maximises between-class variance.
- HOG length for cell size $c$ and $b$ bins: $(H/c)(W/c)b$; at 32×32, $c=8$, $b=9$ → 144 features.
- Per-class recall $= TP_c / (TP_c + FN_c)$ — the metric that exposes a collapsed classifier.

## 5. Dataset information and licensing

`vision_core.make_leaf_images` **generates** the images procedurally: a leaf disc, veins, then
class-specific lesions (dark specks for *spot*, brown patches plus a yellowing tint for *blight*). No
photographs are redistributed, so there is no dataset licence to honour: the images are course-authored
synthetic data, free to use and modify within this repository. They are **not** a substitute for a real
plant-disease dataset, and no result here transfers to field accuracy.

## 6. Software requirements

Python 3.10+, NumPy, scikit-learn, Matplotlib. PyTorch is **not** required for this lab. No network
access is needed and nothing is downloaded.

## 7. Step-by-step tasks

1. **Inspect.** Generate 40 images per class (`seed=0`). Print the array shape, dtype, min/max, and the
   class counts. Convert the first image to luma and print its mean and standard deviation.
2. **Filter.** Convolve luma with a 5×5 Gaussian ($\sigma=1$) and with a sharpening kernel. Report the
   variance of each result and explain both signs of the change.
3. **Edges.** Compute the Sobel magnitude of the blurred image. Threshold it at the Otsu value and apply
   an opening (erode then dilate) with a 3×3 element. Count surviving pixels.
4. **Features.** Extract a HOG descriptor for every image with `cell=8, bins=9`. Confirm the length
   matches the formula.
5. **Classify.** Split 75/25 with `stratify=labels`, train logistic regression, and report test
   accuracy plus per-class recall from the confusion matrix.
6. **Stress the features.** Repeat with `cell=16` and with grayscale replaced by the raw RGB means, and
   report the three accuracies side by side.
7. **Explain.** Write five sentences: which class is hardest, which feature choice hurt most, and what
   you would collect or engineer next.

## 8. Starter code

```python
import numpy as np
import vision_core as v
from sklearn.linear_model import LogisticRegression

images, labels, names = v.make_leaf_images(n_per_class=40, size=32, seed=0)
cut = int(len(labels) * 0.75)

# 1. inspect
print(images.shape, images.dtype, images.min(), images.max())
print(dict(zip(names, np.bincount(labels))))

# 2-3. filtering, edges, morphology on one image
gray = v.to_gray(images[0])
blurred = v.convolve2d(gray, v.gaussian_kernel(5, 1.0))
print("variance:", round(float(gray.var()), 1), "->", round(float(blurred.var()), 1))
edges = v.sobel_magnitude(blurred)
threshold = v.otsu_threshold(edges)
mask = v.dilate(v.erode(edges > threshold, 3), 3)
print("threshold:", threshold, "| kept pixels:", int(mask.sum()))

# 4. HOG features
features = np.stack([v.hog_descriptor(v.to_gray(img), cell=8, bins=9) for img in images])
print("feature length:", features.shape)

# 5. classify and evaluate per class
model = LogisticRegression(max_iter=1000).fit(features[:cut], labels[:cut])
predicted = model.predict(features[cut:])
print("accuracy:", round(float((predicted == labels[cut:]).mean()), 3))
print(v.confusion_matrix(predicted, labels[cut:], 3))
```

## 9. Expected behaviour

With the settings above the pipeline runs in a few seconds and reaches **about 0.95 test accuracy**
(HOG + logistic regression on 140 training images). The confusion matrix should be near-diagonal with
occasional `spot`/`healthy` swaps. A `cell=16` descriptor carries a quarter of the features and typically
loses a few points; RGB means instead of luma usually lose more, because the texture signal is
high-frequency and colour averages wash it out.

Exact numbers vary slightly with library versions — report **your** measured values, not these.

## 10. Evaluation metrics

| Metric | What it tells you |
| :--- | :--- |
| Test accuracy | overall correctness on held-out images |
| Per-class recall | whether one class is systematically missed |
| Confusion matrix | which pair of classes collides |
| Feature length | the cost of the descriptor, for the device budget |

## 11. Testing instructions

- Assert that every HOG vector has length `(32//8)*(32//8)*9 = 144`.
- Assert that the confusion matrix row sums equal the per-class test counts.
- Re-run with `seed=1` and confirm the accuracy moves by less than five points; if it moves more, your
  split is too small and your conclusion is too strong.
- Run `python code/vision_core.py` and confirm `vision_core self-test: True`.

## 12. Submission requirements

A notebook or script that reproduces every number, plus a one-page report containing: the data
statistics, the three feature variants and their accuracies, the confusion matrix, and the five-sentence
explanation from task 7. Include the exact seed values you used.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Correct image/array handling | 20% | dtype and range handled explicitly, no silent clipping |
| Processing pipeline | 25% | convolution, Otsu and morphology implemented and explained |
| Feature extraction | 20% | HOG length verified, variants compared fairly |
| Evaluation | 20% | per-class recall reported, split justified, seed sensitivity checked |
| Explanation | 15% | failure diagnosed with evidence, not adjectives |

## 14. Extension challenges

1. **Rotation invariance.** Augment the test set with 90° rotations and measure the accuracy drop. Should
   HOG be invariant to them? Why not?
2. **Colour spaces.** Convert to HSV and build a hue/saturation histogram descriptor; compare with HOG.
3. **Tiny device budget.** Compress the descriptor to 32 dimensions with PCA and find the smallest size
   that keeps accuracy within two points.
4. **Rule-based baseline.** Ignore learning: count dark pixels and threshold twice. How far does a
   three-line rule get, and what does that say about the dataset?

## Reflection

Hand-designed features encode what the designer believed mattered. That is a strength — you can explain
every number — and a limit: when the signal is a texture nobody anticipated, no amount of tuning the
descriptor helps. The next lab replaces the descriptor with a learned one and asks whether it actually
buys anything at this data scale.
