# LAB-09-03 — Object Detection

| | |
| :--- | :--- |
| Module | M09 · Computer Vision |
| Level | 300 |
| Time | 2.5 hours |
| Prerequisites | [L09-04](../lessons/L09-04-object-detection.md) |
| Dataset | synthetic road scenes with exact ground-truth boxes |
| Code | `code/vision_core.py` |

[← LAB-09-02](lab-09-02-image-classification-with-cnns.md) · [Next lab: LAB-09-04 →](lab-09-04-image-segmentation-with-unet.md)

## 1. Learning objectives

- **Compute** IoU between boxes and explain its role as the matching rule.
- **Implement** greedy non-maximum suppression and measure its effect.
- **Match** predictions to ground truth and compute precision, recall and AP.
- **Diagnose** failure modes: duplicates, missed objects, localisation error.
- **Choose** an operating point from evidence rather than from a default.

## 2. Scenario

A traffic-monitoring pilot needs vehicle counts per frame. Counting is a detection problem: a classifier
per frame answers "is there a vehicle?", which is useless for a count. Your team generated scenes with
exact boxes so the counting logic can be validated before any real annotation exists.

## 3. Problem statement

Build the measurement half of a detector:

1. generate scenes and print the ground-truth boxes;
2. implement IoU and verify two hand-computed values;
3. implement greedy NMS and show it removes a deliberate duplicate;
4. simulate detectors with three error profiles — perfect, shifted, and duplicate-heavy;
5. compute precision, recall and 11-point AP for each at IoU 0.5;
6. sweep the NMS threshold and report how the counts and AP change;
7. state which operating point you would use for counting, and why counting prefers recall.

## 4. Background concepts

- Box conventions: `(x, y, w, h)` versus `(x0, y0, x1, y1)`; `x` is a column, `y` a row.
- $\mathrm{IoU} = |A\cap B| / |A\cup B|$; a prediction is a true positive if it matches an unused truth
  box at IoU ≥ threshold.
- NMS keeps the best box and suppresses overlapping ones above a threshold.
- AP is the area under the precision-recall curve; the 11-point interpolation is the PASCAL VOC variant.
- Counting errors compound: one duplicate per frame is a systematic overcount.

## 5. Dataset information and licensing

`make_detection_scene(seed=…)` generates a 96×96 road scene with zero to three vehicles and returns exact
`(x, y, w, h, label)` boxes. The scenes are course-authored synthetic data, free to use within this
repository; no third-party dataset or annotation licence is involved. Because ground truth is exact,
every metric below is checkable by hand — which is the point.

## 6. Software requirements

Python 3.10+, NumPy, Matplotlib. No PyTorch, no downloads. Everything is CPU and takes under a second per
scene.

## 7. Step-by-step tasks

1. Generate scenes with seeds 7, 11, 12 and print the number of objects in each. Note that some scenes
   have none — handle that case without dividing by zero.
2. Verify by hand: `iou((0,0,10,10), (0,0,10,10)) == 1.0` and `iou((0,0,10,10), (5,0,10,10)) == 1/3`.
3. Build a duplicate prediction set (truth plus a copy of the first box at a slightly lower score) and
   show the kept indices from `v.nms` at thresholds 0.3 and 0.7.
4. Perfect detector: pass the truth boxes with descending scores; AP must be 1.0.
5. Shifted detector: move every box by 2 px in x and 1 px in y; compute AP and the matched counts.
6. Duplicate-heavy detector: append a copy of every box; compute AP with and without NMS.
7. For seeds 7, 11, 12 accumulate true positives, false positives and false negatives at IoU 0.5 and
   report micro precision and recall.
8. Write the operating-point paragraph from task 7.

## 8. Starter code

```python
import numpy as np
import vision_core as v

scenes = {seed: v.make_detection_scene(seed=seed) for seed in (7, 11, 12)}
for seed, (image, boxes) in scenes.items():
    print(seed, "objects:", len(boxes), boxes)

image, boxes = scenes[7]
truth = [b[:4] for b in boxes]
scores = [0.9, 0.8, 0.7][:len(truth)]

print("perfect AP:", v.average_precision(truth, scores, truth, 0.5))

shifted = [(x + 2, y + 1, w, h) for x, y, w, h in truth]
print("shifted AP:", v.average_precision(shifted, scores, truth, 0.5))
print("shifted match (tp, fp, fn):", v.match_boxes(shifted, scores, truth, 0.5))

duplicated = truth + [truth[0]]
dup_scores = scores + [0.85]
keep = v.nms(duplicated, dup_scores, 0.4)
print("NMS keeps:", keep)
print("AP with duplicates, no NMS:", v.average_precision(duplicated, dup_scores, truth, 0.5))
```

## 9. Expected behaviour

- The perfect detector scores **AP 1.0** at IoU 0.5.
- A 2-pixel shift on a 20×15 box keeps IoU above 0.5, so AP stays **1.0** — localisation error that small
  is invisible to the metric. That is a finding to report, not a success.
- The duplicate-heavy detector scores **below 1.0 without NMS** and returns to **1.0 with NMS** at a
  threshold of 0.4, because the copy overlaps the original almost completely.
- Scenes with no objects must produce a defined result (AP 0 with predictions, 1 with none) rather than a
  `ZeroDivisionError`.

## 10. Evaluation metrics

| Metric | Definition | What it exposes |
| :--- | :--- | :--- |
| IoU | overlap / union | localisation quality |
| TP / FP / FN | matched / spurious / missed | the three error types |
| Precision | TP/(TP+FP) | overcounting |
| Recall | TP/(TP+FN) | undercounting |
| AP @ 0.5 | area under PR curve | ranking quality at a fixed IoU |

## 11. Testing instructions

- Assert IoU against your two hand computations to 1e-12.
- Assert AP is in `[0, 1]` for every detector and that the perfect detector is exactly 1.0.
- Assert NMS keeps indices in descending score order and never returns a duplicate above threshold.
- Assert `tp + fn == len(truth)` for every matched set.
- Run `python code/vision_core.py` and confirm the self-test passes.

## 12. Submission requirements

A script or notebook with all four detector profiles, a table of precision/recall/AP per seed, the NMS
sweep, and the operating-point paragraph. Include the scene seeds so the numbers are reproducible.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| IoU and matching | 25% | hand-checked, edge cases handled |
| NMS implementation | 20% | correct ordering, threshold effect measured |
| Metric computation | 25% | AP computed and interpreted, per-seed aggregation |
| Diagnosis | 20% | failure modes named with the metric that reveals them |
| Decision | 10% | operating point justified by the counting task |

## 14. Extension challenges

1. **Per-class AP.** Compute AP separately for cars and vans. Does one class dominate the mean?
2. **Soft-NMS.** Replace suppression with score decay and show the effect on two heavily overlapping
   objects.
3. **IoU sweep.** Recompute AP at IoU 0.3, 0.5 and 0.75 and plot the curve. What does the slope tell you
   about localisation quality?
4. **Tiny detector.** Train a one-layer convnet to regress box centres on these scenes (fixed two boxes
   per scene) and compare its AP with the simulated profiles.

## Reflection

Detection metrics are easy to compute and easy to misread. The shifted-box result — AP 1.0 with every box
wrong by two pixels — is the lesson: a threshold hides the error it was designed to tolerate. Always
report the IoU you used, the NMS threshold, and the per-class breakdown.
