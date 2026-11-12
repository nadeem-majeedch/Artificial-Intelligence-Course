"""Datasets and image generators for M07, all seeded and CPU-sized.

The module deliberately avoids torchvision downloads: every practical runs offline in
seconds. Where a public dataset is the intended target, the loader function accepts a
local copy of that dataset's files and otherwise falls back to a synthetic stand-in
that is clearly labelled as such.

Public datasets named here, with licences:

* MNIST handwritten digits — LeCun & Cortes, CC BY-SA 3.0 (http://yann.lecun.com/exdb/mnist/)
* Fashion-MNIST — Xiao, Rasul & Vollgraf (2017), MIT licence
* PlantVillage — Hughes & Salathé (2015), CC BY-SA 3.0 (images of plant leaves)
* IMDB movie reviews — Maas et al. (2011), for research use; cite the paper
* UCI Electricity Load Diagrams / synthetic series — the module uses generated series

Run `python deep_data.py` for shapes and a class-balance check.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "xor_data",
    "digit_images",
    "pattern_images",
    "plant_images",
    "sentiment_data",
    "series_windows",
    "load_idx_images",
    "DIGIT_FONT",
]

# 5x7 bitmap font for the ten digits, used by the synthetic digit generator.
DIGIT_FONT = {
    0: ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    1: ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    2: ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    3: ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    4: ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    5: ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    6: ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    7: ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    8: ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    9: ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# Logic gates
# ---------------------------------------------------------------------------
def xor_data():
    """The four XOR examples as float arrays: X (4,2), y (4,1)."""
    X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], dtype=np.float32)
    y = np.array([[0.0], [1.0], [1.0], [0.0]], dtype=np.float32)
    return X, y


def _render_digit(digit: int, size: int, rng: np.random.Generator) -> np.ndarray:
    font = np.array([[float(c) for c in row] for row in DIGIT_FONT[digit]])
    canvas = np.zeros((size, size), dtype=np.float32)
    height, width = font.shape
    top = rng.integers(0, max(size - height, 1))
    left = rng.integers(0, max(size - width, 1))
    canvas[top:top + height, left:left + width] = font
    # Jitter intensity, drop a few pixels and add noise. Without this the ten
    # templates are trivially separable and every model scores 1.000 immediately.
    canvas *= rng.uniform(0.55, 1.0, size=(size, size)).astype(np.float32)
    drop = rng.random((size, size)) < 0.05
    canvas[drop] = 0.0
    canvas += rng.normal(0.0, 0.10, size=(size, size)).astype(np.float32)
    return np.clip(canvas, 0.0, 1.0)


def digit_images(n: int = 2000, size: int = 8, seed: int = 0):
    """Synthetic handwritten-digit-like images.

    Returns (X, y) with X of shape (n, 1, size, size) in [0, 1] and y integer labels.
    The glyphs come from a 5x7 bitmap font with random placement and noise, so a CNN
    can learn them but a linear model struggles more than on clean MNIST. This is a
    teaching stand-in: report results as synthetic, never as MNIST.
    """
    rng = _rng(seed)
    labels = rng.integers(0, 10, n)
    images = np.stack([_render_digit(int(d), size, rng) for d in labels])
    return images[:, None, :, :], labels.astype(np.int64)


# ---------------------------------------------------------------------------
# Fashion stand-in
# ---------------------------------------------------------------------------
def _pattern(kind: int, size: int, rng: np.random.Generator) -> np.ndarray:
    yy, xx = np.mgrid[0:size, 0:size]
    img = np.zeros((size, size), dtype=np.float32)
    if kind == 0:
        img = ((yy % 3) < 1).astype(np.float32) * 0.8
    elif kind == 1:
        img = ((xx % 3) < 1).astype(np.float32) * 0.8
    elif kind == 2:
        img = (((yy // 2) + (xx // 2)) % 2).astype(np.float32) * 0.8
    elif kind == 3:
        img = (((xx + yy) % 4) < 2).astype(np.float32) * 0.8
    elif kind == 4:
        img = (((yy - size / 2) ** 2 + (xx - size / 2) ** 2) < (size / 3.2) ** 2).astype(np.float32) * 0.9
    elif kind == 5:
        img = ((np.abs(xx - size / 2) < 1) | (np.abs(yy - size / 2) < 1)).astype(np.float32) * 0.9
    elif kind == 6:
        border = (xx == 0) | (yy == 0) | (xx == size - 1) | (yy == size - 1)
        img = border.astype(np.float32) * 0.9
    elif kind == 7:
        img = (((yy - size / 2) ** 2 + (xx - size / 2) ** 2) < (size / 5.0) ** 2).astype(np.float32)
    elif kind == 8:
        img = (yy / max(size - 1, 1)).astype(np.float32)
    else:
        img = (rng.random((size, size)) < 0.25).astype(np.float32)
    img = (img + rng.normal(0.0, 0.06, (size, size))).astype(np.float32)
    return np.clip(img, 0.0, 1.0)


def pattern_images(n: int = 3000, size: int = 8, seed: int = 0):
    """Ten geometric texture classes standing in for Fashion-MNIST.

    A real Fashion-MNIST run needs the IDX files; without them this keeps the same
    ten-class shape so the pipeline, the confusion matrix and the error analysis are
    identical in structure. The classes are textures, not garments — do not label them
    as fashion items in a report.
    """
    rng = _rng(seed)
    labels = rng.integers(0, 10, n)
    images = np.stack([_pattern(int(k), size, rng) for k in labels])
    return images[:, None, :, :], labels.astype(np.int64)


# ---------------------------------------------------------------------------
# Plant leaves (synthetic three-class)
# ---------------------------------------------------------------------------
def plant_images(n: int = 600, size: int = 16, seed: int = 0):
    """Three synthetic leaf classes: healthy, rust spots, powdery mildew.

    RGB images of shape (n, 3, size, size). The class is encoded in colour and texture
    so a small CNN reaches high accuracy quickly, while a model that ignores colour
    (grayscale) does much worse — the point of the error-analysis exercise.
    """
    rng = _rng(seed)
    labels = rng.integers(0, 3, n)
    images = np.zeros((n, 3, size, size), dtype=np.float32)
    yy, xx = np.mgrid[0:size, 0:size]
    for i, label in enumerate(labels):
        cx, cy = size / 2 + rng.normal(0, 1.2), size / 2 + rng.normal(0, 1.2)
        leaf = (((xx - cx) / (size * 0.42)) ** 2 + ((yy - cy) / (size * 0.3)) ** 2) < 1.0
        green = np.stack([leaf * 0.25, leaf * 0.75, leaf * 0.3], axis=0)
        if label == 0:  # healthy: uniform green with a vein
            vein = (np.abs(xx - cx) < 0.7)
            green[:, vein] *= 0.75
        elif label == 1:  # rust: orange-brown spots
            spots = (rng.random((size, size)) < 0.18) & leaf
            green[0, spots] = 0.85
            green[1, spots] = 0.45
            green[2, spots] = 0.12
        else:  # mildew: pale patches
            patches = (rng.random((size, size)) < 0.25) & leaf
            green[:, patches] = 0.92
        images[i] = np.clip(green + rng.normal(0, 0.05, (3, size, size)), 0, 1)
    return images.astype(np.float32), labels.astype(np.int64)


# ---------------------------------------------------------------------------
# Sentiment
# ---------------------------------------------------------------------------
POSITIVE = ["good", "great", "excellent", "love", "brilliant", "enjoyed", "best", "wonderful"]
NEGATIVE = ["bad", "awful", "boring", "hate", "terrible", "worst", "disappointing", "dull"]
NEUTRAL = ["the", "film", "was", "a", "it", "and", "with", "some", "plot", "acting", "scene", "cast"]


def sentiment_data(n: int = 1500, seed: int = 0):
    """Synthetic two-class sentiment sentences with a majority-vote label.

    Returns (texts, labels, vocabulary). Sentences are 6-12 tokens with one to three
    polar words; the label is 1 when positives outnumber negatives. This is a structural
    stand-in for IMDB: same task, no download, and a deliberate ambiguity when the polar
    counts tie (those rows are labelled 0 and are the hard cases).
    """
    rng = _rng(seed)
    texts, labels = [], []
    for _ in range(n):
        length = int(rng.integers(6, 13))
        n_polar = int(rng.integers(1, 4))
        tokens = [NEUTRAL[int(rng.integers(len(NEUTRAL)))] for _ in range(length)]
        positions = rng.choice(length, size=min(n_polar, length), replace=False)
        pos = neg = 0
        for position in positions:
            if rng.random() < 0.5:
                tokens[position] = POSITIVE[int(rng.integers(len(POSITIVE)))]
                pos += 1
            else:
                tokens[position] = NEGATIVE[int(rng.integers(len(NEGATIVE)))]
                neg += 1
        texts.append(" ".join(tokens))
        labels.append(1 if pos > neg else 0)
    vocab = {word: i + 1 for i, word in enumerate(sorted(set(" ".join(texts).split())))}
    return texts, np.array(labels, dtype=np.int64), vocab


def encode_sentiment(texts, vocab, max_len: int = 12) -> np.ndarray:
    """Map tokenised sentences to a padded integer matrix (0 = padding)."""
    out = np.zeros((len(texts), max_len), dtype=np.int64)
    for i, text in enumerate(texts):
        ids = [vocab.get(word, 0) for word in text.split()][:max_len]
        out[i, : len(ids)] = ids
    return out


# ---------------------------------------------------------------------------
# Time series
# ---------------------------------------------------------------------------
def series_windows(n: int = 800, window: int = 24, horizon: int = 1, seed: int = 0):
    """Windowed univariate series for one-step forecasting.

    Each series is a sum of two sinusoids, a linear trend and noise, then chopped into
    overlapping windows. Returns X of shape (n, window, 1) and y of shape (n,).
    """
    rng = _rng(seed)
    total = n + window + horizon + 50
    t = np.arange(total, dtype=np.float32)
    phase = rng.uniform(0, 2 * np.pi, 4)
    series = (
        np.sin(2 * np.pi * t / 12 + phase[0])
        + 0.5 * np.sin(2 * np.pi * t / 5 + phase[1])
        + rng.normal(0, 0.12, total)
    ).astype(np.float32)
    # Standardise so that an MSE of 0.05 is interpretable as "5% of the variance".
    series = (series - series.mean()) / series.std()

    X = np.stack([series[i:i + window] for i in range(n)])[:, :, None]
    y = np.array([series[i + window + horizon - 1] for i in range(n)], dtype=np.float32)
    return X, y


# ---------------------------------------------------------------------------
# Optional real-file loaders
# ---------------------------------------------------------------------------
def load_idx_images(path: str, max_items: int | None = None):
    """Read an IDX image file (MNIST / Fashion-MNIST format) without torchvision.

    Usage: download `train-images-idx3-ubyte.gz` and `train-labels-idx1-ubyte.gz`
    from the dataset's official page, gunzip them, then:

        X, y = load_idx_images("train-images-idx3-ubyte")

    Returns uint8 images of shape (n, 1, 28, 28), scaled to [0, 1] floats.
    """
    with open(path, "rb") as handle:
        magic = int.from_bytes(handle.read(4), "big")
        if magic != 2051:
            raise ValueError("not an IDX image file")
        count = int.from_bytes(handle.read(4), "big")
        rows = int.from_bytes(handle.read(4), "big")
        cols = int.from_bytes(handle.read(4), "big")
        count = count if max_items is None else min(count, max_items)
        data = np.frombuffer(handle.read(count * rows * cols), dtype=np.uint8)
    return (data.reshape(count, 1, rows, cols).astype(np.float32) / 255.0)


if __name__ == "__main__":
    X, y = xor_data()
    print("xor:", X.shape, y.ravel().tolist())
    for name, fn in [("digit_images", digit_images), ("pattern_images", pattern_images), ("plant_images", plant_images)]:
        images, labels = fn()
        print(f"{name:15s} X {images.shape} y {labels.shape} classes {np.bincount(labels).tolist()} max {images.max():.2f}")
    texts, labels, vocab = sentiment_data()
    print("sentiment:", len(texts), "labels", np.bincount(labels).tolist(), "vocab", len(vocab))
    Xs, ys = series_windows()
    print("series:", Xs.shape, ys.shape, "y range", round(float(ys.min()), 2), round(float(ys.max()), 2))
