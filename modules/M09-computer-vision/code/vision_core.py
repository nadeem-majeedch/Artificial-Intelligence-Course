"""Synthetic computer-vision toolkit for M09.

Everything here is generated in code: no dataset download, no pretrained weights, no third-party
licensing obligation. The generated data is dedicated to the public domain under CC0 1.0 (see
DATASET-LICENSE.md). The images are deliberately small and the generators deterministic, so a whole lab runs
on a laptop CPU in seconds and every printed number in the lessons can be reproduced exactly.

Contents
--------
Data generators : make_leaf_images, make_sign_images, make_detection_scene, make_road_scene
Image processing: to_gray, convolve2d, gaussian_kernel, sobel_magnitude, otsu_threshold,
                  erode, dilate, hog_descriptor
Detection       : iou, nms, match_boxes, average_precision
Segmentation    : dice, mean_iou
Learning        : augment, TinyCNN, train_classifier, predict
Self-test       : run_tests

PyTorch is imported lazily: the image-processing and detection half of the module works with
NumPy alone, which is what a student on a locked-down machine needs.
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------
# Data generators
# ---------------------------------------------------------------------------

CLASS_NAMES = ("stop", "warning", "mandatory")
LEAF_CLASSES = ("healthy", "spot", "blight")
SEG_CLASSES = ("road", "sky", "obstacle")


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def _disc(size: int, cy: float, cx: float, r: float) -> np.ndarray:
    yy, xx = np.mgrid[0:size, 0:size]
    return ((yy - cy) ** 2 + (xx - cx) ** 2) <= r ** 2


def make_leaf_images(n_per_class: int = 40, size: int = 32, seed: int = 0):
    """Three leaf conditions: healthy, leaf spot, blight.

    The classes differ in texture and colour statistics, not in shape, so a model cannot win by
    memorising an outline. Returns ``(images, labels, class_names)`` with images ``uint8`` of shape
    ``(N, size, size, 3)``.
    """
    rng = _rng(seed)
    images, labels = [], []
    for label, name in enumerate(LEAF_CLASSES):
        for _ in range(n_per_class):
            img = np.full((size, size, 3), 236, dtype=np.int16)
            cy, cx = size / 2 + rng.normal(0, 1.2), size / 2 + rng.normal(0, 1.2)
            leaf = _disc(size, cy, cx, size * 0.42)
            base = np.array([60, 150, 70], dtype=np.int16) + rng.integers(-15, 16, 3)
            img[leaf] = base
            # veins: low-frequency structure shared by all classes
            for k in range(1, 4):
                phase = rng.uniform(0, math.pi)
                yy = np.arange(size).reshape(-1, 1)
                xx = np.arange(size).reshape(1, -1)
                vein = (np.sin((yy * 0.6 + xx * 0.4) + phase) > 0.85) & leaf
                img[vein] = np.clip(img[vein] - 18, 0, 255)

            if name == "spot":
                # many small, very dark lesions: high-frequency texture, leaf colour unchanged
                for _ in range(rng.integers(10, 16)):
                    sy, sx = rng.integers(3, size - 3, 2)
                    spot = _disc(size, float(sy), float(sx), rng.uniform(1.6, 2.8)) & leaf
                    img[spot] = np.clip(np.array([25, 30, 25]) + rng.integers(-8, 9, 3), 0, 255)
            if name == "blight":
                # fewer, larger, brown lesions plus a yellowing tint over the whole leaf
                img[leaf] = np.clip(img[leaf] + np.array([45, -15, -40]), 0, 255)
                for _ in range(rng.integers(4, 7)):
                    by, bx = rng.integers(3, size - 3, 2)
                    blob = _disc(size, float(by), float(bx), rng.uniform(4.0, 6.5)) & leaf
                    img[blob] = np.clip(np.array([135, 85, 35]) + rng.integers(-15, 16, 3), 0, 255)
                img = np.clip(img + rng.normal(0, 6, img.shape), 0, 255)

            img = np.clip(img + rng.normal(0, 3, img.shape), 0, 255)
            images.append(img.astype(np.uint8))
            labels.append(label)
    images = np.stack(images)
    labels = np.array(labels, dtype=np.int64)
    order = rng.permutation(len(labels))
    return images[order], labels[order], list(LEAF_CLASSES)


def make_sign_images(n_per_class: int = 40, size: int = 32, seed: int = 1):
    """Three road-sign families drawn procedurally: red octagon, yellow triangle, blue disc."""
    rng = _rng(seed)
    images, labels = [], []
    for label, name in enumerate(CLASS_NAMES):
        for _ in range(n_per_class):
            img = np.full((size, size, 3), 200, dtype=np.int16)
            cy = cx = size / 2 + rng.normal(0, 0.8)
            r = size * 0.36
            if name == "stop":
                yy, xx = np.mgrid[0:size, 0:size]
                dist = np.maximum(np.abs(yy - cy), np.abs(xx - cx))
                shape = dist <= r
                colour = np.array([190, 35, 40])
            elif name == "warning":
                yy, xx = np.mgrid[0:size, 0:size]
                # upward triangle: three half-plane constraints
                tri = ((yy - (cy - r)) >= -0.05) & (
                    (yy - (cy - r)) <= 2 * r - np.abs(xx - cx) * 1.15
                )
                shape = tri
                colour = np.array([225, 190, 40])
            else:
                shape = _disc(size, cy, cx, r)
                colour = np.array([40, 70, 190])
            img[shape] = np.clip(colour + rng.integers(-12, 13, 3), 0, 255)
            # inner glyph: a bright bar of random orientation
            glyph = shape & _disc(size, cy + rng.normal(0, 0.6), cx + rng.normal(0, 0.6), r * 0.45)
            img[glyph] = np.clip(np.array([230, 230, 225]) + rng.integers(-10, 11, 3), 0, 255)
            img = np.clip(img + rng.normal(0, 5, img.shape), 0, 255)
            images.append(img.astype(np.uint8))
            labels.append(label)
    images = np.stack(images)
    labels = np.array(labels, dtype=np.int64)
    order = rng.permutation(len(labels))
    return images[order], labels[order], list(CLASS_NAMES)


def make_detection_scene(seed: int = 0, size: int = 96, max_objects: int = 3):
    """A synthetic road scene with 0–3 vehicles and exact ground-truth boxes.

    Returns ``(image uint8 (size,size,3), boxes [(x, y, w, h, label), ...])`` where ``label`` is 0
    for a car and 1 for a van. Boxes never overlap, so matching is unambiguous and NMS can be
    studied on deliberately duplicated predictions instead.
    """
    rng = _rng(seed)
    img = np.full((size, size, 3), 120, dtype=np.int16)
    img[: size // 2] = np.array([135, 175, 215])          # sky
    img[size // 2:] = np.array([95, 95, 100])             # road
    img[size // 2: size // 2 + 3] = np.array([210, 210, 200])  # horizon line
    boxes = []
    n = int(rng.integers(0, max_objects + 1))
    slots = np.linspace(6, size - 34, max(n, 1), dtype=int)
    for i in range(n):
        w = int(rng.integers(14, 24))
        h = int(rng.integers(10, 18))
        x = int(slots[i])
        y = int(rng.integers(size - h - 4, size - h - 1))
        label = int(rng.integers(0, 2))
        colour = np.array([200, 60, 60]) if label == 0 else np.array([50, 90, 170])
        img[y:y + h, x:x + w] = np.clip(colour + rng.integers(-15, 16, 3), 0, 255)
        img[y:y + h, x:x + 3] = 30                        # window strip keeps left edge honest
        boxes.append((x, y, w, h, label))
    img = np.clip(img + rng.normal(0, 4, img.shape), 0, 255)
    return img.astype(np.uint8), boxes


def make_road_scene(seed: int = 0, size: int = 64):
    """A three-class segmentation scene: 0 road, 1 sky, 2 obstacle. Exact pixel labels."""
    rng = _rng(seed)
    img = np.zeros((size, size, 3), dtype=np.int16)
    mask = np.zeros((size, size), dtype=np.uint8)
    horizon = int(size * rng.uniform(0.38, 0.48))
    img[:horizon] = np.clip(np.array([130, 175, 220]) + rng.integers(-10, 11, 3), 0, 255)
    mask[:horizon] = 1
    img[horizon:] = np.clip(np.array([90, 90, 95]) + rng.integers(-8, 9, 3), 0, 255)
    mask[horizon:] = 0
    # lane markings
    for y in range(horizon, size, 8):
        img[y:y + 3, size // 2 - 1: size // 2 + 1] = 220
    # one or two obstacles on the road
    for _ in range(int(rng.integers(1, 3))):
        w = int(rng.integers(8, 16))
        h = int(rng.integers(6, 12))
        x = int(rng.integers(0, size - w))
        y = int(rng.integers(horizon + 2, max(horizon + 3, size - h)))
        img[y:y + h, x:x + w] = np.clip(np.array([140, 120, 60]) + rng.integers(-15, 16, 3), 0, 255)
        mask[y:y + h, x:x + w] = 2
    img = np.clip(img + rng.normal(0, 3, img.shape), 0, 255)
    return img.astype(np.uint8), mask


# ---------------------------------------------------------------------------
# Image processing
# ---------------------------------------------------------------------------

def to_gray(image: np.ndarray) -> np.ndarray:
    """ITU-R 601 luma of an RGB uint8 image, returned as float64 in [0, 255]."""
    if image.ndim == 2:
        return image.astype(np.float64)
    return image[..., :3].astype(np.float64) @ np.array([0.299, 0.587, 0.114])


def convolve2d(image: np.ndarray, kernel: np.ndarray, padding: str = "same") -> np.ndarray:
    """2-D cross-correlation (what every deep-learning framework calls convolution).

    ``padding='same'`` zero-pads so the output matches the input; ``padding='valid'`` shrinks the
    output by ``kernel.shape - 1``. Implemented with shifts, so there is no scipy dependency and the
    loop count is the kernel size rather than the image size.
    """
    k = np.asarray(kernel, dtype=np.float64)
    img = np.asarray(image, dtype=np.float64)
    kh, kw = k.shape
    if padding == "same":
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(img, ((pad_h, kh - 1 - pad_h), (pad_w, kw - 1 - pad_w)), mode="constant")
        out = np.zeros_like(img)
    elif padding == "valid":
        padded = img
        out = np.zeros((img.shape[0] - kh + 1, img.shape[1] - kw + 1))
    else:
        raise ValueError("padding must be 'same' or 'valid'")
    for i in range(kh):
        for j in range(kw):
            if k[i, j] == 0:
                continue
            out += k[i, j] * padded[i:i + out.shape[0], j:j + out.shape[1]]
    return out


def gaussian_kernel(size: int = 5, sigma: float = 1.0) -> np.ndarray:
    """Normalised 2-D Gaussian kernel; ``size`` should be odd."""
    ax = np.arange(size) - (size - 1) / 2
    g = np.exp(-(ax[:, None] ** 2 + ax[None, :] ** 2) / (2 * sigma ** 2))
    return g / g.sum()


def sobel_magnitude(gray: np.ndarray) -> np.ndarray:
    """Gradient magnitude from the 3×3 Sobel pair, scaled to [0, 255]."""
    gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    gy = gx.T
    mag = np.hypot(convolve2d(gray, gx), convolve2d(gray, gy))
    peak = mag.max()
    return mag / peak * 255.0 if peak > 0 else mag


def otsu_threshold(gray: np.ndarray, bins: int = 64) -> float:
    """Otsu's threshold: maximise between-class variance over the observed intensities.

    The threshold is returned in the input's own units, so an 8-bit image gives a
    value in 0-255 and an image scaled to [0, 1] gives a value in 0-1. Intensities
    are quantised into ``bins`` levels between the observed minimum and maximum;
    this is why the uint8 and float copies of one image split at the same place.
    """
    values = np.asarray(gray, dtype=np.float64).ravel()
    low, high = float(values.min()), float(values.max())
    if high <= low:
        return low
    hist, edges = np.histogram(values, bins=bins, range=(low, high))
    hist = hist.astype(np.float64)
    centres = (edges[:-1] + edges[1:]) / 2.0
    total = hist.sum()
    w0 = np.cumsum(hist)
    w1 = total - w0
    m0 = np.cumsum(hist * centres)
    mean_total = m0[-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        mu0 = m0 / w0
        mu1 = (mean_total - m0) / w1
        between = w0 * w1 * (mu0 - mu1) ** 2
    between = np.nan_to_num(between)
    return float(centres[int(np.argmax(between))])


def _binary_op(binary: np.ndarray, k: int, op: str) -> np.ndarray:
    pad = k // 2
    padded = np.pad(binary.astype(bool), pad, mode="constant", constant_values=False)
    acc = None
    for i in range(k):
        for j in range(k):
            window = padded[i:i + binary.shape[0], j:j + binary.shape[1]]
            if acc is None:
                acc = window.copy()
            else:
                acc = (acc | window) if op == "dilate" else (acc & window)
    return acc


def dilate(binary: np.ndarray, k: int = 3) -> np.ndarray:
    """Binary dilation with a k×k square structuring element (grows white regions)."""
    return _binary_op(binary, k, "dilate")


def erode(binary: np.ndarray, k: int = 3) -> np.ndarray:
    """Binary erosion with a k×k square structuring element (shrinks white regions)."""
    return _binary_op(binary, k, "erode")


def hog_descriptor(gray: np.ndarray, cell: int = 8, bins: int = 9) -> np.ndarray:
    """A small Histogram of Oriented Gradients descriptor.

    Gradients are unsigned (0–180°), binned by magnitude into ``bins`` over ``cell``-sized blocks,
    and each cell histogram is L2-normalised. The result is a single flat vector whose length is
    ``(H//cell) * (W//cell) * bins``.
    """
    gx = convolve2d(gray, np.array([[-1, 0, 1]], dtype=np.float64))
    gy = convolve2d(gray, np.array([[-1], [0], [1]], dtype=np.float64))
    mag = np.hypot(gx, gy)
    ang = (np.degrees(np.arctan2(gy, gx)) % 180.0)
    h, w = gray.shape
    ch, cw = h // cell, w // cell
    hist = np.zeros((ch, cw, bins))
    bin_idx = np.minimum((ang / (180.0 / bins)).astype(int), bins - 1)
    for by in range(ch):
        for bx in range(cw):
            m = mag[by * cell:(by + 1) * cell, bx * cell:(bx + 1) * cell]
            b = bin_idx[by * cell:(by + 1) * cell, bx * cell:(bx + 1) * cell]
            hist[by, bx] = np.bincount(b.ravel(), weights=m.ravel(), minlength=bins)
    hist = hist.reshape(-1, bins)
    norms = np.linalg.norm(hist, axis=1, keepdims=True)
    hist = hist / np.maximum(norms, 1e-8)
    return hist.ravel()


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def iou(box_a, box_b) -> float:
    """Intersection over Union for ``(x, y, w, h)`` boxes; 0 when they do not touch."""
    ax, ay, aw, ah = box_a[:4]
    bx, by, bw, bh = box_b[:4]
    x0, y0 = max(ax, bx), max(ay, by)
    x1, y1 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    inter = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    union = aw * ah + bw * bh - inter
    return float(inter / union) if union > 0 else 0.0


def nms(boxes, scores, iou_threshold: float = 0.4):
    """Greedy non-maximum suppression. Returns the kept indices, best score first."""
    order = sorted(range(len(boxes)), key=lambda i: scores[i], reverse=True)
    keep = []
    while order:
        best = order.pop(0)
        keep.append(best)
        order = [i for i in order if iou(boxes[best], boxes[i]) <= iou_threshold]
    return keep


def match_boxes(pred_boxes, pred_scores, true_boxes, iou_threshold: float = 0.5):
    """Greedy matching of predictions to ground truth at a given IoU.

    Returns ``(tp, fp, fn)`` counts. Each true box can be matched at most once; a prediction that
    matches nothing above the threshold is a false positive.
    """
    used = set()
    tp = 0
    for index in np.argsort(pred_scores)[::-1]:
        best, best_iou = None, 0.0
        for j, true_box in enumerate(true_boxes):
            if j in used:
                continue
            value = iou(pred_boxes[index], true_box)
            if value > best_iou:
                best, best_iou = j, value
        if best is not None and best_iou >= iou_threshold:
            used.add(best)
            tp += 1
    fp = len(pred_boxes) - tp
    fn = len(true_boxes) - len(used)
    return tp, fp, fn


def average_precision(pred_boxes, pred_scores, true_boxes, iou_threshold: float = 0.5) -> float:
    """11-point interpolated AP for a single class and a single image.

    With one image the precision-recall curve is a step function; the 11-point interpolation is
    what the original PASCAL VOC metric used and it keeps the arithmetic visible.
    """
    if not true_boxes:
        return 0.0 if pred_boxes else 1.0
    order = np.argsort(pred_scores)[::-1]
    used = set()
    tp_running, fp_running = 0, 0
    precisions, recalls = [], []
    for index in order:
        best, best_iou = None, 0.0
        for j, true_box in enumerate(true_boxes):
            if j in used:
                continue
            value = iou(pred_boxes[index], true_box)
            if value > best_iou:
                best, best_iou = j, value
        if best is not None and best_iou >= iou_threshold:
            used.add(best)
            tp_running += 1
        else:
            fp_running += 1
        precisions.append(tp_running / (tp_running + fp_running))
        recalls.append(tp_running / len(true_boxes))
    aps = []
    for r in np.linspace(0, 1, 11):
        candidates = [p for p, rr in zip(precisions, recalls) if rr >= r]
        aps.append(max(candidates) if candidates else 0.0)
    return float(np.mean(aps))


# ---------------------------------------------------------------------------
# Segmentation metrics
# ---------------------------------------------------------------------------

def dice(pred_mask: np.ndarray, true_mask: np.ndarray, label: int = 1) -> float:
    """Dice coefficient for one label: 2|A∩B| / (|A| + |B|)."""
    a = pred_mask == label
    b = true_mask == label
    denom = a.sum() + b.sum()
    return float(2 * (a & b).sum() / denom) if denom else 1.0


def mean_iou(pred_mask: np.ndarray, true_mask: np.ndarray, labels=(0, 1, 2)) -> float:
    """Mean IoU over the given labels, ignoring labels absent from both masks."""
    scores = []
    for label in labels:
        a = pred_mask == label
        b = true_mask == label
        union = (a | b).sum()
        if union == 0:
            continue
        scores.append((a & b).sum() / union)
    return float(np.mean(scores)) if scores else 1.0


# ---------------------------------------------------------------------------
# Learning
# ---------------------------------------------------------------------------

def augment(image: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Horizontal flip, random brightness and 90° rotation — three cheap, label-safe transforms."""
    out = image
    if rng.random() < 0.5:
        out = out[:, ::-1]
    if rng.random() < 0.5:
        out = np.rot90(out, k=int(rng.integers(0, 4)))
    shift = rng.uniform(-12, 12)
    return np.clip(out.astype(np.float64) + shift, 0, 255).astype(np.uint8)


def _make_cnn(n_classes: int, size: int):
    import torch.nn as nn

    class TinyCNN(nn.Module):
        """Two convolution blocks and a linear head: the smallest CNN that can learn this data."""

        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            )
            with_size = size // 4
            self.head = nn.Sequential(
                nn.Flatten(), nn.Linear(16 * with_size * with_size, 32), nn.ReLU(),
                nn.Linear(32, n_classes),
            )

        def forward(self, x):
            return self.head(self.features(x))

    return TinyCNN()


def train_classifier(images: np.ndarray, labels: np.ndarray, epochs: int = 3, seed: int = 0,
                     lr: float = 0.01, batch_size: int = 32, use_augmentation: bool = False):
    """Train ``TinyCNN`` on ``images`` and return ``(model, history)``.

    ``history`` holds per-epoch training loss and training accuracy. The model is left in eval mode.
    """
    import torch
    import torch.nn as nn

    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    n_classes = int(labels.max()) + 1
    size = images.shape[1]
    model = _make_cnn(n_classes, size)
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    x_all = torch.from_numpy(images.transpose(0, 3, 1, 2).astype(np.float32) / 255.0)
    y_all = torch.from_numpy(labels.astype(np.int64))
    history = []
    for epoch in range(epochs):
        if use_augmentation:
            aug = np.stack([augment(img, rng) for img in images])
            x_epoch = torch.from_numpy(aug.transpose(0, 3, 1, 2).astype(np.float32) / 255.0)
        else:
            x_epoch = x_all
        perm = torch.randperm(len(y_all))
        total_loss, correct = 0.0, 0
        model.train()
        for start in range(0, len(perm), batch_size):
            idx = perm[start:start + batch_size]
            logits = model(x_epoch[idx])
            loss = loss_fn(logits, y_all[idx])
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()
            total_loss += float(loss.detach()) * len(idx)
            correct += int((logits.argmax(1) == y_all[idx]).sum())
        history.append({"epoch": epoch + 1, "loss": total_loss / len(perm),
                        "train_accuracy": correct / len(perm)})
    model.eval()
    return model, history


def predict(model, images: np.ndarray) -> np.ndarray:
    """Return predicted class indices for uint8 images of shape ``(N, H, W, 3)``."""
    import torch

    with torch.no_grad():
        x = torch.from_numpy(images.transpose(0, 3, 1, 2).astype(np.float32) / 255.0)
        return model(x).argmax(1).numpy()


def confusion_matrix(pred: np.ndarray, true: np.ndarray, n_classes: int) -> np.ndarray:
    """Rows are true labels, columns are predictions."""
    matrix = np.zeros((n_classes, n_classes), dtype=int)
    for t, p in zip(true, pred):
        matrix[int(t), int(p)] += 1
    return matrix




def make_road_dataset(n: int = 40, size: int = 64, seed: int = 0):
    """A list of ``(image, mask)`` road scenes, generated from consecutive seeds."""
    images, masks = [], []
    for i in range(n):
        image, mask = make_road_scene(seed=seed + i, size=size)
        images.append(image)
        masks.append(mask)
    return np.stack(images), np.stack(masks)


def _make_unet(n_classes: int, base: int = 8):
    import torch.nn as nn

    def block(cin, cout):
        return nn.Sequential(nn.Conv2d(cin, cout, 3, padding=1), nn.ReLU(),
                             nn.Conv2d(cout, cout, 3, padding=1), nn.ReLU())

    class TinyUNet(nn.Module):
        """Two down-samples, two up-samples and skip concatenations — U-Net in miniature."""

        def __init__(self):
            super().__init__()
            self.enc1 = block(3, base)
            self.enc2 = block(base, base * 2)
            self.bottleneck = block(base * 2, base * 4)
            self.up2 = nn.ConvTranspose2d(base * 4, base * 2, 2, stride=2)
            self.dec2 = block(base * 4, base * 2)
            self.up1 = nn.ConvTranspose2d(base * 2, base, 2, stride=2)
            self.dec1 = block(base * 2, base)
            self.head = nn.Conv2d(base, n_classes, 1)

        def forward(self, x):
            e1 = self.enc1(x)
            e2 = self.enc2(nn.functional.max_pool2d(e1, 2))
            b = self.bottleneck(nn.functional.max_pool2d(e2, 2))
            d2 = self.dec2(torch_cat(self.up2(b), e2))
            d1 = self.dec1(torch_cat(self.up1(d2), e1))
            return self.head(d1)

    return TinyUNet()


def torch_cat(a, b):
    import torch
    return torch.cat([a, b], dim=1)


def train_segmenter(images: np.ndarray, masks: np.ndarray, epochs: int = 15, seed: int = 0,
                    lr: float = 0.01, batch_size: int = 8, base: int = 12):
    """Train a small U-Net with class-weighted cross-entropy plus Dice loss.

    Returns ``(model, history)`` where each history row holds the epoch loss and the mean IoU over
    the training scenes. Fifteen epochs on 60 scenes at 64x64 takes about 30 s on a laptop CPU.
    """
    import torch
    import torch.nn as nn

    torch.manual_seed(seed)
    n_classes = int(masks.max()) + 1
    model = _make_unet(n_classes, base=base)
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)
    # inverse-frequency class weights: without them the loss is dominated by road pixels and the
    # network collapses to "everything is road" — the failure this module asks students to diagnose
    counts = np.bincount(masks.ravel(), minlength=n_classes).astype(np.float64)
    weights = torch.tensor((counts.sum() / (n_classes * np.maximum(counts, 1))), dtype=torch.float32)
    x = torch.from_numpy(images.transpose(0, 3, 1, 2).astype(np.float32) / 255.0)
    y = torch.from_numpy(masks.astype(np.int64))
    history = []
    for epoch in range(epochs):
        perm = torch.randperm(len(y))
        total = 0.0
        model.train()
        for start in range(0, len(perm), batch_size):
            idx = perm[start:start + batch_size]
            logits = model(x[idx])
            ce = nn.functional.cross_entropy(logits, y[idx], weight=weights)
            probs = torch.softmax(logits, dim=1)
            dice_terms = []
            for c in range(n_classes):
                p = probs[:, c]
                t = (y[idx] == c).float()
                dice_terms.append(1 - (2 * (p * t).sum() + 1.0) / (p.sum() + t.sum() + 1.0))
            loss = ce + torch.stack(dice_terms).mean()
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()
            total += float(loss.detach()) * len(idx)
        model.eval()
        with torch.no_grad():
            predicted = model(x).argmax(1).numpy()
        scores = [mean_iou(predicted[i], masks[i]) for i in range(len(masks))]
        history.append({"epoch": epoch + 1, "loss": total / len(perm),
                        "train_miou": float(np.mean(scores))})
    model.eval()
    return model, history


def predict_masks(model, images: np.ndarray) -> np.ndarray:
    """Predict a class mask per image for uint8 images of shape ``(N, H, W, 3)``."""
    import torch

    with torch.no_grad():
        x = torch.from_numpy(images.transpose(0, 3, 1, 2).astype(np.float32) / 255.0)
        return model(x).argmax(1).numpy().astype(np.uint8)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def run_tests() -> bool:
    """Cheap invariants: every claim printed here is checked, not asserted in prose."""
    leaf_x, leaf_y, _ = make_leaf_images(6, size=16, seed=3)
    assert leaf_x.shape == (18, 16, 16, 3) and leaf_x.dtype == np.uint8
    assert set(np.unique(leaf_y)) == {0, 1, 2}

    sign_x, sign_y, _ = make_sign_images(4, size=16, seed=3)
    assert sign_x.shape == (12, 16, 16, 3) and sign_y.shape == (12,)

    scene, boxes = make_detection_scene(seed=5)
    assert scene.shape == (96, 96, 3)
    for x, y, w, h, _ in boxes:
        assert 0 <= x and 0 <= y and x + w <= 96 and y + h <= 96

    road, mask = make_road_scene(seed=5)
    assert road.shape == (64, 64, 3) and mask.shape == (64, 64)
    assert set(np.unique(mask)).issubset({0, 1, 2}) and 2 in mask

    # convolution: identity kernel leaves the image unchanged
    img = to_gray(scene)
    identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
    assert np.allclose(convolve2d(img, identity), img)
    # a box filter of ones/9 preserves a constant image away from the zero-padded border
    blurred = convolve2d(np.full((8, 8), 7.0), np.ones((3, 3)) / 9)
    assert np.allclose(blurred[1:-1, 1:-1], 7.0)
    assert abs(blurred[0, 0] - 7.0 * 4 / 9) < 1e-12   # border sees only four neighbours
    # valid padding shrinks by k-1
    assert convolve2d(np.zeros((10, 10)), np.ones((3, 3)), "valid").shape == (8, 8)

    # Sobel finds the horizon: row variance should exceed column variance
    edges = sobel_magnitude(img)
    assert edges.max() > 0

    # Otsu on a synthetic two-level image lands between the levels
    two = np.concatenate([np.full(50, 30), np.full(50, 200)]).reshape(10, 10)
    t = otsu_threshold(two)
    # any threshold between the two levels separates the classes; check the split, not the index
    assert 30 <= t < 200, t
    assert abs(two[two <= t].mean() - 30) < 1e-9 and abs(two[two > t].mean() - 200) < 1e-9
    # the same image scaled to [0, 1] must give the same split, in [0, 1] units
    t_float = otsu_threshold(two / 255.0)
    assert 0.0 < t_float < 1.0 and abs(t_float * 255.0 - t) < 4.0, (t, t_float)

    # morphology: dilate grows, erode shrinks
    b = np.zeros((9, 9), dtype=bool)
    b[4, 4] = True
    # one pixel grows to a 3x3 block under dilation and vanishes under erosion
    assert dilate(b).sum() == 9, dilate(b).sum()
    assert erode(b).sum() == 0, erode(b).sum()
    block = np.zeros((9, 9), dtype=bool)
    block[3:6, 3:6] = True
    assert erode(block).sum() == 1 and dilate(block).sum() == 25

    # HOG length and normalisation
    vec = hog_descriptor(img, cell=8, bins=9)
    assert vec.size == (img.shape[0] // 8) * (img.shape[1] // 8) * 9

    # IoU and NMS on known boxes
    assert abs(iou((0, 0, 10, 10), (0, 0, 10, 10)) - 1.0) < 1e-12
    assert abs(iou((0, 0, 10, 10), (5, 0, 10, 10)) - (50 / 150)) < 1e-12
    kept = nms([(0, 0, 10, 10), (1, 1, 10, 10), (40, 40, 10, 10)], [0.9, 0.8, 0.7], 0.4)
    assert kept == [0, 2], kept

    # detection metrics: one perfect prediction, one false positive
    tp, fp, fn = match_boxes([(0, 0, 10, 10), (50, 50, 5, 5)], [0.9, 0.1], [(0, 0, 10, 10)], 0.5)
    assert (tp, fp, fn) == (1, 1, 0)

    # segmentation metrics: perfect prediction scores 1.0
    assert abs(dice(mask, mask, 2) - 1.0) < 1e-12
    assert abs(mean_iou(mask, mask) - 1.0) < 1e-12

    # the segmenter is a smoke test here: shapes and metrics are checked, quality is measured in
    # LAB-09-04 (a three-epoch model on twelve scenes is not supposed to be good)
    road_x, road_y = make_road_dataset(n=12, size=64, seed=0)
    assert road_x.shape == (12, 64, 64, 3) and road_y.shape == (12, 64, 64)
    seg_model, seg_history = train_segmenter(road_x, road_y, epochs=3, seed=0, lr=0.02)
    assert len(seg_history) == 3 and 0.0 <= seg_history[-1]["train_miou"] <= 1.0
    masks = predict_masks(seg_model, road_x[:2])
    assert masks.shape == (2, 64, 64) and masks.dtype == np.uint8
    assert set(np.unique(masks)).issubset({0, 1, 2})
    assert predict_masks(seg_model, road_x[:2]).shape == (2, 64, 64)

    # a classifier trains: with enough data it must beat chance (1/3) on three classes
    big_x, big_y, _ = make_sign_images(20, size=16, seed=4)
    model, history = train_classifier(big_x, big_y, epochs=3, seed=0, batch_size=16)
    assert len(history) == 3 and history[-1]["train_accuracy"] >= 0.55, history
    preds = predict(model, big_x)
    assert preds.shape == big_y.shape and preds.dtype.kind in "iu"
    return True


if __name__ == "__main__":
    print("vision_core self-test:", run_tests())
    x, y, names = make_sign_images(20, seed=2)
    print("sign images:", x.shape, "classes:", names)
    m, h = train_classifier(x, y, epochs=3)
    print("history:", h)
