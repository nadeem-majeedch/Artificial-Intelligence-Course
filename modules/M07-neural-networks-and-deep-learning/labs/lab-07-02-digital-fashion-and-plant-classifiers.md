# LAB-07-02 — Image Classifiers: Digits, Fashion and Plant Disease

> **Module M07** · Lab 2 of 3 · ~150 minutes · Level 300
> **Scenarios:** 2 (handwritten digits), 3 (fashion/garment classification), 4 (plant disease)
> **Prerequisites:** L07-03, L07-04, L07-05 · **Pairs with:** NB-07-02

[Module overview](../README.md) · [Previous lab: LAB-07-01](lab-07-01-neural-network-from-scratch.md) · [Next lab: LAB-07-03 →](lab-07-03-sentiment-forecasting-and-transfer.md)

Three image classification problems with the same pipeline and three different lessons: digits
teach the mechanics, fashion teaches confusion between similar classes, and plant disease teaches
that a model exploiting the wrong cue can look excellent in the lab and fail in the field.

---

## Scenario 2 — Handwritten digit recognition

### Problem description

Classify 8×8 grayscale digit images into ten classes. Establish a dense baseline, then a
convolutional model, and quantify what the spatial inductive bias is worth.

### Business context

Automated reading of handwritten amounts, postcodes and forms. The cost asymmetry matters: a
misread digit on a cheque is expensive, so per-class recall matters more than overall accuracy.

### Dataset source and licence

- **In this lab:** `code/deep_data.digit_images(n=2400, size=8, seed=0)` — synthetic glyphs rendered
  from a built-in 7×5 bitmap font with jitter, intensity variation and noise. Generated in-script,
  dedicated to CC0 1.0, deterministic.
- **Real counterpart:** MNIST (LeCun, Cortes & Burges), **CC BY-SA 3.0**. Load the original IDX files
  with `code/deep_data.load_idx_images("train-images-idx3-ubyte.gz")`; the array convention
  `(n, 1, 28, 28)` in `[0, 1]` matches, so only the model's `image_size` and input width change.
- Report synthetic numbers as synthetic. Do not present them as MNIST benchmarks.

### Dataset description

2,400 images, shape `(2400, 1, 8, 8)`, labels 0–9 roughly balanced (222–267 per class). Pixel
intensities in `[0, 1]`. Default split: 1,800 train / 600 test.

### Tasks

1. **Baseline.** Train `MLP(64, hidden=(32,), n_classes=10)` for 8 epochs with Adam at `1e-3`,
   patience 5. Report parameters, validation accuracy and wall-clock seconds.
2. **CNN.** Train `SmallCNN(in_channels=1, n_classes=10, width=16, image_size=8)` under the same
   budget. Compare parameters and accuracy.
3. **Curves.** Plot train and validation loss and validation accuracy for both. Identify the epoch
   where the MLP starts to overfit.
4. **Confusion matrix.** Build the 10×10 matrix for the CNN, report per-class recall, and inspect the
   misclassified images.
5. **Regularisation ablation.** Re-run the CNN with `dropout=0.0` and `dropout=0.3`; report the
   train/validation gap.
6. **Checkpoint.** Save the trained model with `save_checkpoint`, reload into a fresh model and
   confirm identical accuracy.

### Expected results

```text
MLP 64-32   params   2410   val acc 0.988   2.31 s
CNN w16     params  13802   val acc 0.998   1.36 s
per-class recall: [1. 1. 1. 1. 1. 1. 0.983 1. 1. 1.]
confusions: [(6, 1, 1)]
misclassified: 1 of 600
```

The CNN needs six times the parameters but five times fewer operations per image than the dense
model would need at full resolution — and it wins by a point. On this toy task both models are
already near ceiling; the point is the mechanism, not the margin.

---

## Scenario 3 — Garment and texture classification

### Problem description

Classify 16×16 texture images into ten classes. Compare a dense network with a CNN, and analyse
which classes are confused and why.

### Business context

Catalogue tagging and automated quality control: a garment or material classifier that confuses
"shirt" with "pullover" is tolerable in search, expensive in inventory. The confusion structure tells
you where human review should be inserted.

### Dataset source and licence

- **In this lab:** `code/deep_data.pattern_images(n=2400, size=16, seed=0)` — ten procedural texture
  families (stripes, checkerboard, rings, gradients, noise). Generated in-script.
- **Real counterpart:** Fashion-MNIST (Xiao, Rasul & Vollgraf, 2017), **MIT licence**. IDX files load
  with `load_idx_images`; images are 28×28 grayscale with ten garment classes.
- These synthetic images are **textures, not garments**. Do not label them as clothing in the report.

### Dataset description

2,400 images, `(2400, 1, 16, 16)`, ten balanced classes. Default split 1,800 / 600.

### Tasks

1. Train `SmallCNN(1, 10, width=16, image_size=16)` for 8 epochs; record accuracy and parameters.
2. Train `MLP(256, hidden=(64,), n_classes=10)` for the same budget. Compare.
3. Build the confusion matrix. Identify the most-confused pair and explain it in terms of the
   generating patterns (look at the images).
4. Visualise the first convolutional layer's 16 filters and the feature maps for one image.
5. Ablation: width 8 vs 16 vs 32. Plot accuracy against parameters.
6. Add random horizontal flips as data augmentation (flip the NumPy arrays before batching) and
   measure the effect.

### Expected results

```text
patterns CNN  params 38378  val acc 1.000
patterns MLP  params 17098  val acc 1.000
```

Both models saturate: the ten texture families are perfectly separable. That is a useful negative
result — if the task is too easy, no architecture comparison is informative, and you should say so
rather than manufacture a difference. The filter visualisations still show that the CNN learns
oriented edge detectors.

---

## Scenario 4 — Plant disease classification

### Problem description

Classify 16×16 RGB leaf images into healthy, rust and powdery mildew. Then deliberately remove
colour (average the channels) and repeat: the accuracy drop measures how much the model relies on
colour rather than lesion shape.

### Business context

A phone-based crop-disease assistant. A model trained on one farm's camera may latch onto lighting
or background colour instead of lesions and fail on a different device. Quantifying cue dependence
is a prerequisite for deployment, and the grayscale ablation is the cheapest way to do it.

### Dataset source and licence

- **In this lab:** `code/deep_data.plant_images(n=600, size=16, seed=0)` — three synthetic leaf
  classes with colour-coded disease patterns. Generated in-script.
- **Real counterpart:** PlantVillage (Hughes & Salathé, 2015), **CC BY-SA 3.0**. It contains
  ~54,000 leaf images across 38 classes, with strong background/lab-condition biases — read
  Mohanty et al. (2016) before trusting high accuracy on it.
- Licence note: CC BY-SA requires attribution and share-alike for derived datasets; a trained model
  is generally not a derivative work, but check before commercial use.

### Dataset description

600 images, `(600, 3, 16, 16)`, three classes roughly balanced, RGB in `[0, 1]`. Default split
450 / 150.

### Tasks

1. Train `SmallCNN(in_channels=3, n_classes=3, width=16, image_size=16)` for 12 epochs; report
   accuracy on the held-out 150.
2. Convert to grayscale (`images.mean(axis=1, keepdims=True)`) and train the 1-channel model.
   Report the accuracy difference.
3. Inspect the errors of the grayscale model: which class collapses, and does that match the
   generator's colour scheme?
4. Add a colour-jitter augmentation (multiply each channel by a random factor in `[0.8, 1.2]`) and
   see whether the RGB model's accuracy survives on a jittered test set.
5. Write a short deployment memo: what would you check before shipping this model to farmers?

### Expected results

```text
plants RGB  CNN  params 38211  val acc 1.000
plants gray CNN  params 37923  val acc 0.813
```

Colour alone carries most of the signal in this synthetic dataset. The 0.19 gap is the quantified
cue dependence — and the reason the real PlantVillage accuracy claims need a background-controlled
test set before they mean anything.

---

## Metrics summary

| Scenario | Primary metric | Secondary | Error analysis |
| :--- | :--- | :--- | :--- |
| Digits | accuracy, per-class recall | params, train time | misclassified images |
| Fashion/texture | accuracy, macro F1 | params | confusion matrix |
| Plant disease | accuracy | RGB vs grayscale gap | per-class recall, cue dependence |

Report all three, with the split sizes and seed, in one table.

## Deliverables

1. `digits_baseline.py`, `textures_cnn.py`, `plants_ablation.py`.
2. Figures: learning curves, confusion matrices, filter visualisations, misclassified examples.
3. `lab-07-02-report.md` — the comparison table, the three error analyses and the deployment memo.
4. A model card for the plant classifier: intended use, training data, licence, known failure modes.

## Extensions

- Replace the synthetic digit generator with real MNIST and repeat scenario 2.
- Add batch normalisation to the CNN and compare convergence speed.
- Fine-tune a model trained on digits for the plant task and report whether transfer helps (L07-08).
- Quantise the plant model to `float16` and measure the accuracy and size change.

## Common pitfalls

- Reporting a 1.000 on a synthetic dataset as if it demonstrated real-world capability.
- Using the test split for early stopping — that is validation leaking into the test estimate.
- Forgetting `nn.BatchNorm2d` behaves differently in `train()` and `eval()`.
- Comparing models trained for different numbers of epochs or different learning rates.

## Marking guide

| Criterion | Weight |
| :--- | ---: |
| All three pipelines run and reproduce expected ranges | 25% |
| Correct baseline-versus-CNN comparison with matched budgets | 20% |
| Error analysis: confusion matrix and image inspection | 20% |
| Grayscale/cue-dependence ablation and its interpretation | 20% |
| Report and model card quality | 15% |

## Starter material

The guided notebook [`nb-07-02-pytorch-image-classification.ipynb`](../notebooks/nb-07-02-pytorch-image-classification.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
