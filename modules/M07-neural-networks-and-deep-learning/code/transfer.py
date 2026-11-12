"""Transfer learning and autoencoders for M07 lesson 8.

The scenario: a plant-disease classifier with only 60 labelled leaf images. We
pretrain a small CNN on 3,000 synthetic texture images (a surrogate for a large
public dataset such as ImageNet), reuse its features on leaves, and compare
against training from scratch on the same 60 labels.

Everything runs on CPU in a couple of minutes. Datasets are synthetic stand-ins;
see `deep_data.py` for the public datasets they mirror and their licences.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn

import deep_data as dd
from torch_utils import (AutoEncoder, SmallCNN, Trainer, count_parameters, freeze,
                         make_loader, set_seed, unfreeze)

HEAD_WEIGHT = "classifier.4.weight"
HEAD_BIAS = "classifier.4.bias"


def strip_head(state: dict) -> dict:
    """Drop the classification head so the rest can load into a new class count."""
    return {k: v for k, v in state.items() if k not in (HEAD_WEIGHT, HEAD_BIAS)}


def pretrain_on_textures(epochs: int = 8, seed: int = 0) -> dict:
    """Train SmallCNN on ten texture classes; return weights without the head."""
    set_seed(seed)
    X, y = dd.pattern_images(3000, size=16, seed=1)
    model = SmallCNN(in_channels=1, n_classes=10, width=16, image_size=16)
    Trainer(model).fit(make_loader(X, y, 64, seed=seed), epochs=epochs, lr=1e-3)
    _, acc, _, _ = Trainer(model).evaluate(make_loader(X, y, 256, shuffle=False))
    return {"state": strip_head(model.state_dict()),
            "pretrain_acc": round(float(acc), 3),
            "params": count_parameters(model)}


def adapt(state: dict, n_classes: int = 3) -> SmallCNN:
    """New 3-class model carrying the pretrained convolutional features."""
    model = SmallCNN(in_channels=1, n_classes=n_classes, width=16, image_size=16)
    missing, unexpected = model.load_state_dict(state, strict=False)
    assert all("classifier.4" in name for name in missing), missing
    assert not unexpected, unexpected
    return model


def leaf_data(train_labels: int = 60, seed: int = 0):
    """Grayscale 16x16 leaves; class signal survives averaging the colour channels."""
    X, y = dd.plant_images(600, size=16, seed=seed)
    gray = X.mean(axis=1, keepdims=True)
    return gray[:train_labels], y[:train_labels], gray[train_labels:], y[train_labels:]


def run_experiment(mode: str, train_labels: int = 60, seed: int = 0,
                   pretrained: dict | None = None, epochs: int = 25) -> float:
    """`mode` in {scratch, frozen, finetune}; returns test accuracy."""
    pretrained = pretrained or pretrain_on_textures(seed=0)
    Xtr, ytr, Xte, yte = leaf_data(train_labels, seed=0)
    set_seed(seed)
    if mode == "scratch":
        model = SmallCNN(in_channels=1, n_classes=3, width=16, image_size=16)
        lr = 1e-3
    elif mode == "frozen":
        model = adapt(pretrained["state"])
        freeze(model.features)
        lr = 1e-3
    elif mode == "finetune":
        model = adapt(pretrained["state"])
        unfreeze(model.features)
        lr = 1e-3
    else:
        raise ValueError(f"unknown mode {mode!r}")

    Trainer(model).fit(make_loader(Xtr, ytr, 32, seed=seed), epochs=epochs, lr=lr)
    _, acc, _, _ = Trainer(model).evaluate(make_loader(Xte, yte, 128, shuffle=False))
    return round(float(acc), 3)


def train_autoencoder(latent: int = 8, epochs: int = 20, seed: int = 0):
    """Autoencoder trained only on digits 0-7; digits 8-9 are the 'unseen' class."""
    set_seed(seed)
    X, y = dd.digit_images(2400, size=8, seed=1)
    flat = X.reshape(len(X), -1)
    normal = y < 8
    model = AutoEncoder(in_features=64, latent=latent)
    Trainer(model, criterion=nn.MSELoss(), classification=False).fit(
        make_loader(flat[normal], flat[normal], 64, seed=seed), epochs=epochs, lr=1e-3)
    return model, flat, y, normal


if __name__ == "__main__":
    torch.set_num_threads(2)

    pretrained = pretrain_on_textures(epochs=8, seed=0)
    print("pretrained on textures: acc", pretrained["pretrain_acc"],
          "params", pretrained["params"])

    print(f"{'labels':>6s} {'scratch':>8s} {'frozen':>8s} {'finetune':>9s}")
    for n_labels in (60, 150):
        row = []
        for mode in ("scratch", "frozen", "finetune"):
            scores = [run_experiment(mode, n_labels, seed=s, pretrained=pretrained) for s in (0, 1, 2)]
            row.append(float(np.mean(scores)))
        print(f"{n_labels:6d} {row[0]:8.3f} {row[1]:8.3f} {row[2]:9.3f}")

    model, flat, labels, normal = train_autoencoder(latent=8, epochs=20, seed=0)
    errors = model.reconstruction_error(flat)
    threshold = float(np.quantile(errors[normal], 0.95))
    flagged = errors > threshold
    print("AE params:", count_parameters(model))
    print("reconstruction error: normal", round(float(errors[normal].mean()), 4),
          "unseen", round(float(errors[~normal].mean()), 4))
    print("threshold", round(threshold, 4),
          "flag rate on normal", round(float(flagged[normal].mean()), 3),
          "recall on unseen", round(float(flagged[~normal].mean()), 3))
