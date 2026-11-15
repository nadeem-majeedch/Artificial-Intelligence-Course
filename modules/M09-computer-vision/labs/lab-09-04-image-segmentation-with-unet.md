# LAB-09-04 — Image Segmentation Using U-Net

| | |
| :--- | :--- |
| Module | M09 · Computer Vision |
| Level | 300 |
| Time | 3.5 hours |
| Prerequisites | [L09-05](../lessons/L09-05-image-segmentation.md), LAB-09-02 |
| Dataset | synthetic road scenes with exact pixel masks |
| Code | `code/vision_core.py` |

[← LAB-09-03](lab-09-03-object-detection.md) · [Module home](../README.md)

## 1. Learning objectives

- **Distinguish** semantic, instance and panoptic segmentation on a concrete scene.
- **Train** a small U-Net on pixel labels and read its learning curve.
- **Diagnose** the class-collapse failure caused by unweighted cross-entropy on imbalanced masks.
- **Evaluate** with Dice and per-class IoU, and explain why pixel accuracy misleads.
- **State** the limits of a model trained on synthetic scenes.

## 2. Scenario

An autonomous-cart prototype needs to know which pixels are road, which are sky and which are obstacles.
The team cannot collect real labelled footage yet, so it generated 64×64 synthetic road scenes with exact
masks: road, sky, and a small brown obstacle. Obstacles occupy roughly **1.4% of pixels** — the number
that decides whether this lab succeeds or quietly fails.

You are asked to train a segmenter and, more importantly, to prove it does not ignore the obstacle class.

## 3. Problem statement

1. build the colour-rule baseline and measure it;
2. train a small U-Net with cross-entropy plus Dice loss;
3. show what happens **without** class weighting;
4. evaluate with mean IoU and per-class Dice on held-out scenes;
5. compare against the baseline and state the honest conclusion;
6. list the conditions under which this model must not be used.

## 4. Background concepts

- Encoder–decoder with skip connections: the bottleneck carries *what*, the skips carry *where*.
- Upsampling: nearest, bilinear, or transposed convolution; each has artefacts.
- Losses: cross-entropy (class-frequency sensitive), Dice (overlap), combined (both).
- Metrics: $\mathrm{Dice}_c = 2|P_c\cap G_c|/(|P_c|+|G_c|)$,
  $\mathrm{IoU}_c = |P_c\cap G_c|/|P_c\cup G_c|$, $\mathrm{Dice} = 2\,\mathrm{IoU}/(1+\mathrm{IoU})$.
- Pixel accuracy is dominated by the largest class and must never be reported alone.

## 5. Dataset information and licensing

`make_road_scene(seed=…)` and `make_road_dataset(n=…)` generate scenes and masks in code. The images are
course-authored synthetic data with no third-party licence. They are not photographs and the model trained
on them has learned the generator's colour statistics, not road physics. **No safety claim of any kind may
be attached to a model trained in this lab.**

## 6. Software requirements

Python 3.10+, NumPy, PyTorch (CPU), Matplotlib. No downloads, no pretrained weights, no GPU. The reference
run below takes about 30 seconds on a laptop CPU.

## 7. Step-by-step tasks

1. Generate 60 scenes at 64×64 and print the class fractions. Confirm obstacles are about 1.4% of pixels.
2. Baseline: predict sky where blue > 150, road elsewhere. Report pixel accuracy, mean IoU and obstacle
   Dice. Explain the three numbers together.
3. Better rule: add "brown" (R − B > 40) as obstacle. Report the same three numbers.
4. Train the U-Net for 15 epochs with the default settings; print loss and training mIoU per epoch.
5. Evaluate on 15 scenes you did **not** train on (generate with seeds 1000+). Report mean IoU and
   per-class Dice.
6. Retrain with `weights` disabled (edit a copy of the training function to drop the class weights) and
   describe the collapse: what does the model predict, and what does pixel accuracy say about it?
7. Compare baseline and learned model in one table. State which is better, on what metric, and whether the
   difference is meaningful at this data scale.
8. Write the "must not be used for" list: at least four conditions.

## 8. Starter code

```python
import numpy as np
import vision_core as v

train_x, train_y = v.make_road_dataset(n=60, size=64, seed=0)
test_x, test_y = v.make_road_dataset(n=15, size=64, seed=1000)
print("class fractions:", {c: round(float((train_y == c).mean()), 4) for c in (0, 1, 2)})

# baseline
predicted = np.zeros_like(train_y)
predicted[train_x[:, :, :, 2] > 150] = 1
print("baseline pixel accuracy:", round(float((predicted == train_y).mean()), 3))
print("baseline mIoU:", round(float(np.mean([v.mean_iou(predicted[i], train_y[i])
                                             for i in range(len(train_y))])), 3))
print("baseline obstacle Dice:", round(float(np.mean([v.dice(predicted[i], train_y[i], 2)
                                                      for i in range(len(train_y))])), 3))

# learned model
model, history = v.train_segmenter(train_x, train_y, epochs=15, seed=0)
print([(h["epoch"], round(h["loss"], 2), round(h["train_miou"], 3)) for h in history])

masks = v.predict_masks(model, test_x)
print("test mIoU:", round(float(np.mean([v.mean_iou(masks[i], test_y[i])
                                         for i in range(len(test_y))])), 3))
for label in (0, 1, 2):
    print(label, "Dice:", round(float(np.mean([v.dice(masks[i], test_y[i], label)
                                               for i in range(len(test_y))])), 3))
```

## 9. Expected behaviour

- The colour-rule baseline reaches about **0.65 mean IoU** and **0.00 obstacle Dice** — it never predicts
  the class that matters, while pixel accuracy stays above 0.95.
- The weighted U-Net reaches a training mIoU of about **0.95** within 15 epochs on 60 scenes. Held-out
  scenes score lower (typically 0.85–0.95) because the generator varies obstacle placement and horizon.
- Without class weights the model collapses to "road everywhere": mIoU around 0.20, obstacle Dice 0.00,
  pixel accuracy still high. This is the single most important observation in the lab.

Report your measured numbers; expect variation of a few points between runs and machines.

## 10. Evaluation metrics

| Metric | Definition | What it hides |
| :--- | :--- | :--- |
| Pixel accuracy | correct pixels / all pixels | rare-class failure |
| Mean IoU | mean over present classes | boundary error severity |
| Per-class Dice | overlap for one class | which class failed |
| Training mIoU curve | learning progress | generalisation |

## 11. Testing instructions

- Assert masks contain only `{0, 1, 2}` and match the image shape.
- Assert Dice is in `[0, 1]` and equals 1.0 for a mask compared with itself.
- Confirm the identity $\mathrm{Dice} = 2\mathrm{IoU}/(1+\mathrm{IoU})$ on one class.
- Check that train and test seeds do not overlap.
- Re-run training with `seed=1`; if test mIoU moves by more than 0.1, increase the number of scenes before
  drawing conclusions.
- Confirm `python code/vision_core.py` prints `vision_core self-test: True`.

## 12. Submission requirements

Code, the baseline table, the training curve, held-out metrics per class, the collapse experiment, and the
"must not be used for" list. State epochs, scene counts, seeds and hardware.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Baseline and metrics | 20% | three numbers interpreted together, not separately |
| Training and reproducibility | 25% | seeds, epochs and split documented; curve shown |
| Collapse diagnosis | 25% | unweighted run explained with evidence from predictions |
| Held-out evaluation | 20% | per-class Dice reported, limitations stated |
| Communication | 10% | claims bounded by the evidence |

## 14. Extension challenges

1. **Dice-only loss.** Train with Dice and no cross-entropy; compare convergence speed and final mIoU.
2. **Resolution study.** Train at 32×32 and 96×96 and compare boundary error. Which size is worth the
   compute?
3. **Hard negatives.** Add a grey obstacle colour so the brown rule fails; retrain and report whether the
   learned model generalises.
4. **Panoptic view.** Post-process the predicted mask into connected components and count obstacles —
   turning semantic output into instances.

## Reflection

The lesson is not that U-Net works; it is that a 1.4%-of-pixels class can be invisible to every default.
Class weights, Dice and per-class reports are three different defences against the same failure, and a
report that shows only pixel accuracy has none of them.
