# L09-04 — Object Detection

| Module | M09 · Computer Vision |
| :--- | :--- |
| Level | 300 |
| Study time | 80 minutes |
| Prerequisites | [L09-03](L09-03-image-classification-and-cnns.md) |
| Code | `code/vision_core.py` |

[← Previous: L09-03](L09-03-image-classification-and-cnns.md) · [Next: L09-05 Segmentation →](L09-05-image-segmentation.md)

## 1. Learning Objectives

- **Distinguish** classification, localisation and detection by their outputs.
- **Convert** between box conventions and compute IoU by hand.
- **Implement** greedy non-maximum suppression and explain the threshold's effect.
- **Describe** the R-CNN → YOLO progression in terms of what became faster.
- **Compute** precision, recall and AP from a ranked list of predictions.

## 2. Prerequisite Knowledge

Classification from [L09-03](L09-03-image-classification-and-cnns.md), and the idea of a ranking
metric. No deep-learning internals are needed for the metrics half of this lesson.

## 3. Conceptual Explanation

### 3.1 Three different questions

| Task | Output | Example |
| :--- | :--- | :--- |
| Classification | one label | "this crop is a stop sign" |
| Localisation | one label + one box | "stop sign at (12, 40, 20, 18)" |
| Detection | a *variable-length list* of boxes and labels | "two cars left, one van right" |

The variable-length output is what makes detection hard to train and hard to score: a model that
predicts three boxes when the truth has two must be penalised for the extra *and* the missing one.

### 3.2 Box conventions

Four numbers describe a box: `(x, y, w, h)` (corner + size), `(x0, y0, x1, y1)` (two corners), or
`(cx, cy, w, h)` (centre + size, what anchors predict). All are equivalent; mixing them silently is a
classic bug. In this module boxes are `(x, y, w, h)` with `x` as column and `y` as row — the opposite of
array indexing, which is why L09-01 insisted on it.

### 3.3 Intersection over Union

$$\mathrm{IoU}(A,B) = \frac{|A \cap B|}{|A \cup B|}$$

IoU is 1 for identical boxes, 0 for disjoint ones, and 0.5 when a prediction covers half of the union.
It is the matching rule for every detection metric, and it is scale-free — which is why a small box and
a large box at the same IoU are treated as equally good, a known weakness of the metric.

### 3.4 Non-maximum suppression

A detector proposes many overlapping boxes for the same object. NMS keeps the highest-scoring box,
deletes everything overlapping it above a threshold, and repeats. With `iou_threshold = 0.4` two boxes
covering the same car are merged; with 0.9 they both survive. Too low a threshold deletes genuine
neighbours in a crowd; too high a threshold leaves duplicates. This is a real tuning decision, not a
detail.

### 3.5 Anchor-based and anchor-free

- **Two-stage (R-CNN family)** — propose regions, then classify and refine each. Accurate, slower.
- **One-stage anchor-based (YOLO v2–v5, SSD)** — predict offsets from a grid of anchor boxes in one pass.
- **Anchor-free (FCOS, YOLOv8+)** — predict centre distance or keypoints directly, removing anchor
  hyperparameters entirely.

The progression is a sequence of removing bottlenecks: region proposals → shared features → anchors →
anchors again. YOLO's contribution was framing detection as a single regression over a grid, which made
real-time detection possible.

### 3.6 Metrics from a ranked list

Sort predictions by confidence. Each is a true positive if it matches an unmatched ground-truth box at
IoU ≥ threshold. Precision $= TP/(TP+FP)$, recall $= TP/(TP+FN)$. Average precision is the area under
the precision-recall curve; mean AP averages it over classes. **A single AP number hides which class
failed**, so always report per class.

## 4. Pseudocode

```text
function NMS(boxes, scores, threshold):
    keep <- []
    while boxes not empty:
        best <- argmax(scores)
        keep.append(best)
        remove every box with IoU(best, box) > threshold
    return keep

function AP(predictions, truth, iou_threshold):
    sort predictions by score descending
    for each prediction: match to an unused truth box at IoU >= threshold
    accumulate precision and recall after each prediction
    interpolate and average precision over recall levels 0..1
```

## 5. Worked Example — a scene with exact boxes

```python
import vision_core as v

image, boxes = v.make_detection_scene(seed=7)
print(boxes)                     # [(6, 79, 20, 15, 1), (34, 80, 14, 12, 1), (62, 83, 22, 11, 0)]
truth = [b[:4] for b in boxes]

# a perfect detector: same boxes, descending scores
print("AP at IoU 0.5:", v.average_precision(truth, [0.9, 0.8, 0.7], truth, 0.5))   # 1.0

# a duplicated detector: NMS decides what survives
duplicated = truth + [truth[0]]
scores = [0.9, 0.8, 0.7, 0.85]
keep = v.nms(duplicated, scores, 0.4)
print("kept:", keep, "-> no duplicate of box 0")
```

With a duplicate at score 0.85, NMS keeps the 0.90 original and drops the copy. Without NMS the
duplicate becomes a false positive and AP falls — which is why the lab asks you to measure it.

## 6. Mathematical Formulation

For boxes $A=(x_a, y_a, w_a, h_a)$ and $B$:

$$|A \cap B| = \max(0, \min(x_a+w_a, x_b+w_b) - \max(x_a, x_b)) \cdot
\max(0, \min(y_a+h_a, y_b+h_b) - \max(y_a, y_b))$$

$$\mathrm{AP} = \frac{1}{11}\sum_{r \in \{0, 0.1, \dots, 1\}} \max_{\tilde r \ge r} p(\tilde r)$$

The 11-point interpolation is the PASCAL VOC definition; COCO uses 101 points and IoU averaged from
0.5 to 0.95. State which one you report.

## 7. Python Implementation

```python
import numpy as np
import vision_core as v

image, boxes = v.make_detection_scene(seed=11)
truth = [b[:4] for b in boxes]
print("objects:", len(truth))

# IoU by hand for two boxes
print("IoU:", round(v.iou(truth[0], truth[0]), 3) if truth else "no objects")

# a noisy detector: shift each box by a few pixels
noisy = [(x + 2, y + 1, w, h) for x, y, w, h in truth]
scores = [0.9 - 0.1 * i for i in range(len(noisy))]
if truth:
    print("AP with 2px shift:", round(v.average_precision(noisy, scores, truth, 0.5), 3))
    print("matched:", v.match_boxes(noisy, scores, truth, 0.5))
```

## 8. Practical Applications

- **Vehicle and pedestrian detection** for traffic analysis (LAB-09-03).
- **Retail shelf auditing** — count facings, detect gaps.
- **Agriculture** — count fruit or diseased plants per row.
- **Safety** — helmet and vest detection on sites, where a missed detection costs more than a false one,
  so the operating point is chosen for recall.

## 9. Common Mistakes

1. Mixing `(x, y, w, h)` and `(x0, y0, x1, y1)` between annotation and code.
2. Clipping boxes to the image *after* computing IoU, so scores disagree with visuals.
3. Reporting mAP without per-class AP, hiding a class with 0.0.
4. Matching one ground-truth box to several predictions (double counting true positives).
5. Choosing the NMS threshold on the test set.

## 10. Exercises

1. Compute IoU for `(0,0,10,10)` and `(5,0,10,10)` by hand and check with `v.iou` (answer: 1/3).
2. Build five predictions for one object with scores 0.9, 0.8, 0.7, 0.6, 0.5 and IoU 0.6 between
   neighbours; run NMS at 0.3 and 0.7 and explain the different counts.
3. Given predictions where the highest-score box is a false positive, compute the 11-point AP and say
   why the first precision value matters so much.
4. Explain in three sentences why anchor-free detectors removed a hyperparameter but not a design choice.

## 11. Self-Assessment

1. Why can a detector with high precision have low recall?
   *It only predicts boxes it is confident about, so it misses objects it never proposes.*
2. What does an IoU threshold of 0.5 mean for a small object?
   *A prediction may be substantially offset or mis-sized and still count; small objects need stricter
   thresholds in practice.*
3. What does NMS do when two genuine objects overlap heavily?
   *It deletes one of them — the failure mode that motivates soft-NMS and learned suppression.*

## 12. Key Terms

**Bounding box**, **IoU**, **non-maximum suppression**, **anchor**, **one-stage detector**, **two-stage
detector**, **precision**, **recall**, **average precision**, **mAP**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Redmon et al. (2016), "You Only Look Once" — the single-pass framing.
- Ren et al. (2015), "Faster R-CNN" — region proposal networks.
- Everingham et al., PASCAL VOC devkit — the AP definition this lesson uses.

## What to Do Next

Continue to [L09-05 Image Segmentation](L09-05-image-segmentation.md), and complete
[LAB-09-03](../labs/lab-09-03-object-detection.md).
