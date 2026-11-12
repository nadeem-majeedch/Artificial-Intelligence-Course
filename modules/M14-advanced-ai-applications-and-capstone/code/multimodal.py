"""multimodal.py -- a small contrastive vision-language model, from scratch (M14, L14-03).

A vision-language model is two encoders trained so that matching (image, text) pairs land
close together in one space. This script builds the smallest honest version of that:

    image encoder   64 -> 64 -> 32 on 8x8 digits
    text encoder    bag-of-words -> 32 -> 32, learned word vectors
    objective       symmetric InfoNCE over a batch, temperature 0.07
    evaluation      image->text R@1/R@5, text->image R@1, zero-shot digit accuracy

The digit labels are never given to the text encoder. The only supervision is which caption
belongs to which image, which is exactly how CLIP is trained and why it can classify classes
it was never trained on.

Run ``python multimodal.py``.
"""

from __future__ import annotations

import re

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

torch.manual_seed(0)
np.random.seed(0)

STYLES = ["dim", "faint", "clear", "bright", "crisp"]
DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
EXTRA = ["scan", "sample", "sheet", "form", "note"]


# ---------------------------------------------------------------------------
# 1. Data: images plus templated captions
# ---------------------------------------------------------------------------

def build_captions(X, y, rng):
    """Caption style depends on image intensity, so the text carries real information."""
    mean = X.mean(axis=1)
    captions = []
    for i, digit in enumerate(y):
        style = STYLES[min(len(STYLES) - 1, int(mean[i] * len(STYLES)))]
        extra = EXTRA[rng.integers(len(EXTRA))]
        captions.append(f"a {style} {extra} of the number {DIGIT_WORDS[digit]}")
    return captions


def build_vocab(captions):
    words = sorted({w for c in captions for w in re.findall(r"[a-z]+", c)})
    return {w: i for i, w in enumerate(words)}


def encode_text(captions, vocab):
    M = np.zeros((len(captions), len(vocab)), dtype=np.float32)
    for i, c in enumerate(captions):
        for w in re.findall(r"[a-z]+", c):
            if w in vocab:
                M[i, vocab[w]] = 1.0
    return M


# ---------------------------------------------------------------------------
# 2. The two-tower model
# ---------------------------------------------------------------------------

class TwoTower(nn.Module):
    def __init__(self, img_dim=64, vocab=32, dim=32):
        super().__init__()
        self.image = nn.Sequential(nn.Linear(img_dim, 64), nn.ReLU(), nn.Linear(64, dim))
        self.word = nn.Embedding(vocab, dim)
        self.text = nn.Sequential(nn.Linear(dim, dim), nn.ReLU(), nn.Linear(dim, dim))

    def forward(self, x_img, x_txt):
        zi = F.normalize(self.image(x_img), dim=-1)
        pooled = F.normalize(x_txt @ self.word.weight, dim=-1)   # mean of word vectors
        zt = F.normalize(self.text(pooled), dim=-1)
        return zi, zt


def contrastive_loss(zi, zt, temperature=0.07):
    logits = zi @ zt.t() / temperature
    target = torch.arange(len(zi))
    return 0.5 * (F.cross_entropy(logits, target) + F.cross_entropy(logits.t(), target))


# ---------------------------------------------------------------------------
# 3. Evaluation
# ---------------------------------------------------------------------------

def retrieval_metrics(zi, zt):
    sim = (zi @ zt.t()).numpy()
    ranks = (-sim).argsort(axis=1)
    pos = np.arange(len(sim))[:, None]
    i2t_rank = (ranks == pos).argmax(axis=1)
    ranks_t = (-sim.T).argsort(axis=1)
    t2i_rank = (ranks_t == pos).argmax(axis=1)
    return {
        "i2t_r1": float((i2t_rank < 1).mean()),
        "i2t_r5": float((i2t_rank < 5).mean()),
        "t2i_r1": float((t2i_rank < 1).mean()),
    }


def zero_shot(model, X_img, y, vocab):
    with torch.no_grad():
        zi, _ = model(torch.tensor(X_img), torch.zeros(len(X_img), len(vocab)))
        prompts = [f"a clear sample of the number {DIGIT_WORDS[d]}" for d in range(10)]
        P = encode_text(prompts, vocab)
        _, zt = model(torch.zeros(10, 64), torch.tensor(P))
        pred = (zi @ zt.t()).argmax(dim=1).numpy()
    return float((pred == y).mean())


# ---------------------------------------------------------------------------
# 4. Demo
# ---------------------------------------------------------------------------

def main():
    d = load_digits()
    X = (d.data / 16.0).astype(np.float32)
    y = d.target
    rng = np.random.default_rng(0)
    captions = build_captions(X, y, rng)
    vocab = build_vocab(captions)
    T = encode_text(captions, vocab)

    idx_tr, idx_te = train_test_split(np.arange(len(y)), test_size=0.3,
                                      random_state=0, stratify=y)
    Xtr, Xte = X[idx_tr], X[idx_te]
    Ttr, Tte = T[idx_tr], T[idx_te]
    ytr, yte = y[idx_tr], y[idx_te]

    print("=" * 80)
    print("1. The data")
    print("=" * 80)
    print(f"  images {X.shape}, captions {len(captions)}, vocabulary {len(vocab)} words")
    print("  example captions:")
    for c in captions[:3]:
        print("   ", c)

    model = TwoTower(vocab=len(vocab))
    with torch.no_grad():
        zi, zt = model(torch.tensor(Xte), torch.tensor(Tte))
    before = retrieval_metrics(zi, zt)
    zs_before = zero_shot(model, Xte, yte, vocab)
    print(f"\n  before training: {before}, zero-shot accuracy {zs_before:.3f}")

    opt = torch.optim.Adam(model.parameters(), lr=3e-3)
    Xt, Tt = torch.tensor(Xtr), torch.tensor(Ttr)
    batch = 128
    print("\n" + "=" * 80)
    print("2. Contrastive training (the only labels are the pairs)")
    print("=" * 80)
    for step in range(1, 301):
        perm = torch.randperm(len(Xt))[:batch]
        zi_b, zt_b = model(Xt[perm], Tt[perm])
        loss = contrastive_loss(zi_b, zt_b)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step in (1, 50, 100, 200, 300):
            with torch.no_grad():
                zi_e, zt_e = model(torch.tensor(Xte), torch.tensor(Tte))
                m = retrieval_metrics(zi_e, zt_e)
            print(f"  step {step:3d}  loss {loss.item():.3f}  "
                  f"i2t R@1 {m['i2t_r1']:.3f}  t2i R@1 {m['t2i_r1']:.3f}")

    with torch.no_grad():
        zi, zt = model(torch.tensor(Xte), torch.tensor(Tte))
    after = retrieval_metrics(zi, zt)
    zs_after = zero_shot(model, Xte, yte, vocab)

    print("\n" + "=" * 80)
    print("3. Retrieval and zero-shot classification")
    print("=" * 80)
    print(f"  {'metric':10s} {'before':>8} {'after':>8}")
    for k in after:
        print(f"  {k:10s} {before[k]:8.3f} {after[k]:8.3f}")
    print(f"  {'zero-shot':10s} {zs_before:8.3f} {zs_after:8.3f}")
    print("\n  The classifier was never given a digit label. It works because the caption")
    print("  text names the digit, so the image tower inherits the classes from the pairs.")

    # show one retrieval example
    sim = (zi @ zt.t())
    q = 0
    best = int(sim[q].argmax())
    print(f"\n  example: image {q} (true digit {yte[q]}) retrieved caption")
    print(f"    '{captions[idx_te[best]]}' (exact instance match: {best == q})")
    top = sim.argmax(dim=1).numpy()
    digit_hit = float((yte[top] == yte).mean())
    print(f"  digit-level retrieval accuracy: {digit_hit:.3f}")
    print("  Instance-level R@1 is near chance here because dozens of captions describe")
    print("  the same digit; the meaningful measure for this data is digit-level retrieval.")
    print("  Choosing the metric is part of the experiment, not an afterthought.")

    # failure analysis: which classes fail most
    with torch.no_grad():
        preds = (zi @ zt.t()).argmax(dim=1).numpy()
    per_class = [(float((yte[top] == yte)[yte == c].mean()), c) for c in range(10)]
    print()
    print("  digit-level retrieval accuracy by class:")
    print("  " + "  ".join(f"{c}:{a:.2f}" for a, c in per_class))
    worst = min(per_class)
    print(f"  worst class {worst[1]} at {worst[0]:.2f}")
    print("\n  Limitations: 8x8 images, templated captions, one object per image and a")
    print("  closed vocabulary. A real VLM handles open text, multiple objects and scale;")
    print("  this model demonstrates the training signal, not the capability.")


if __name__ == "__main__":
    main()
