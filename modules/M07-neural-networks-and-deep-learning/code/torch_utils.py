"""PyTorch utilities and small reference models for M07.

Everything runs on CPU in seconds; if CUDA is available the same code uses it. No
torchvision is required: the datasets come from `deep_data.py`.

Contents
--------
* seeding, device selection, tensor conversion
* `Trainer`: a training loop with validation, early stopping and history
* model definitions: MLP, SmallCNN, LSTMRegressor, TinyTransformerClassifier
* `freeze`, `unfreeze`, `count_parameters`, save/load helpers

Run `python torch_utils.py` for a short end-to-end demonstration on synthetic digits.
"""

from __future__ import annotations

import copy
import time

import numpy as np
import torch
from torch import nn

__all__ = [
    "set_seed", "get_device", "as_tensor", "make_loader",
    "Trainer", "MLP", "SmallCNN", "LSTMRegressor", "TinyTransformerClassifier",
    "count_parameters", "freeze", "unfreeze", "save_checkpoint", "load_checkpoint",
]


def set_seed(seed: int = 0) -> None:
    """Seed Python, NumPy and torch so a run is repeatable on the same device."""
    import random

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    """CUDA when available, otherwise CPU. The rest of the code never asks again."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def as_tensor(array, dtype=torch.float32) -> torch.Tensor:
    return torch.as_tensor(np.ascontiguousarray(array), dtype=dtype)


def make_loader(X, y, batch_size: int = 64, shuffle: bool = True, seed: int = 0) -> torch.utils.data.DataLoader:
    """Wrap NumPy arrays in a TensorDataset and a DataLoader.

    X may be (n, features) for tabular data or (n, c, h, w) for images. y may be a
    class vector or a float target vector.
    """
    # Token ids must stay integer for nn.Embedding; images and features are float.
    X_array = np.asarray(X)
    x_dtype = torch.long if np.issubdtype(X_array.dtype, np.integer) else torch.float32
    X_t = as_tensor(X_array, x_dtype)
    if y is None:
        dataset = torch.utils.data.TensorDataset(X_t)
    else:
        y_array = np.asarray(y)
        dtype = torch.long if np.issubdtype(y_array.dtype, np.integer) else torch.float32
        dataset = torch.utils.data.TensorDataset(X_t, as_tensor(y_array, dtype=dtype))
    generator = torch.Generator().manual_seed(seed)
    return torch.utils.data.DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle, generator=generator
    )


class Trainer:
    """A small, explicit training loop with validation and early stopping.

    Parameters
    ----------
    model : nn.Module
    criterion : loss function (default CrossEntropyLoss)
    device : torch.device, optional
    patience : int, optional
        Stop when validation loss has not improved for this many epochs. This is the
        cheapest regulariser in deep learning and the one most often forgotten.
    classification : bool, optional
        Compute accuracy from `argmax`. Set False for reconstruction or regression
        losses where the target has the same shape as the output (e.g. autoencoders).
    """

    def __init__(self, model, criterion=None, device=None, patience=None, min_delta=1e-4,
                 classification=True):
        self.model = model
        self.device = device or get_device()
        self.model.to(self.device)
        self.criterion = criterion or nn.CrossEntropyLoss()
        self.patience = patience
        self.classification = classification
        self.min_delta = min_delta
        self.history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
        self.best_state = None
        self.best_val_loss = float("inf")
        self.epochs_run = 0

    # -- one pass --------------------------------------------------------
    def _run_epoch(self, loader, optimizer=None):
        training = optimizer is not None
        self.model.train(training)
        total_loss, correct, seen = 0.0, 0, 0
        all_preds, all_labels = [], []

        for batch in loader:
            if len(batch) == 2:
                xb, yb = batch
            else:
                (xb,) = batch
                yb = None
            xb = xb.to(self.device)
            yb = yb.to(self.device) if yb is not None else None

            with torch.set_grad_enabled(training):
                outputs = self.model(xb)
                loss = self.criterion(outputs, yb)
                if training:
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

            total_loss += float(loss.item()) * len(xb)
            seen += len(xb)
            if self.classification and yb is not None and outputs.ndim > 1 and outputs.shape[1] > 1:
                preds = outputs.argmax(dim=1)
                correct += int((preds == yb).sum())
                all_preds.append(preds.detach().cpu())
                all_labels.append(yb.detach().cpu())

        accuracy = correct / seen if seen else float("nan")
        preds = torch.cat(all_preds).numpy() if all_preds else None
        labels = torch.cat(all_labels).numpy() if all_labels else None
        return total_loss / max(seen, 1), accuracy, preds, labels

    # -- public API ------------------------------------------------------
    def fit(self, train_loader, val_loader=None, epochs=10, optimizer=None, lr=1e-3,
            weight_decay=0.0, scheduler=None, verbose=False):
        optimizer = optimizer or torch.optim.Adam(self.model.parameters(), lr=lr,
                                                  weight_decay=weight_decay)
        stale = 0
        for epoch in range(1, epochs + 1):
            train_loss, train_acc, _, _ = self._run_epoch(train_loader, optimizer)
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)

            if val_loader is not None:
                with torch.no_grad():
                    val_loss, val_acc, _, _ = self._run_epoch(val_loader)
                self.history["val_loss"].append(val_loss)
                self.history["val_acc"].append(val_acc)
            else:
                val_loss, val_acc = train_loss, train_acc

            if scheduler is not None:
                scheduler.step()

            self.epochs_run = epoch
            if verbose:
                print(f"epoch {epoch:3d} train_loss {train_loss:.4f} val_loss {val_loss:.4f} "
                      f"val_acc {val_acc:.3f}")

            if val_loss < self.best_val_loss - self.min_delta:
                self.best_val_loss = val_loss
                self.best_state = copy.deepcopy(self.model.state_dict())
                stale = 0
            else:
                stale += 1
                if self.patience is not None and stale >= self.patience:
                    if verbose:
                        print(f"early stopping after epoch {epoch}")
                    break

        if self.best_state is not None:
            self.model.load_state_dict(self.best_state)
        return self.history

    @torch.no_grad()
    def evaluate(self, loader):
        """Return (loss, accuracy, predictions, labels)."""
        loss, acc, preds, labels = self._run_epoch(loader, optimizer=None)
        return loss, acc, preds, labels

    @torch.no_grad()
    def predict(self, X):
        self.model.eval()
        x = as_tensor(X).to(self.device)
        outputs = self.model(x)
        return outputs.argmax(dim=1).cpu().numpy()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class MLP(nn.Module):
    """Configurable feedforward classifier: Linear → activation → dropout per layer."""

    def __init__(self, in_features, hidden=(128, 64), n_classes=10, dropout=0.0,
                 activation="relu", batchnorm=False):
        super().__init__()
        act = {"relu": nn.ReLU, "tanh": nn.Tanh, "leaky_relu": nn.LeakyReLU}[activation]
        layers = []
        previous = in_features
        for width in hidden:
            layers.append(nn.Linear(previous, width))
            if batchnorm:
                layers.append(nn.BatchNorm1d(width))
            layers.append(act())
            if dropout:
                layers.append(nn.Dropout(dropout))
            previous = width
        layers.append(nn.Linear(previous, n_classes))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(torch.flatten(x, start_dim=1))


class SmallCNN(nn.Module):
    """Two convolutional blocks followed by a classifier head.

    Block: Conv(3x3, padding 1) → BatchNorm → ReLU → MaxPool(2).
    The receptive field and the channel progression (1→16→32) are deliberately small
    so the model trains on CPU in seconds; the structure is the standard one.
    """

    def __init__(self, in_channels=1, n_classes=10, width=16, image_size=8, dropout=0.0):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, width, 3, padding=1),
            nn.BatchNorm2d(width),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(width, width * 2, 3, padding=1),
            nn.BatchNorm2d(width * 2),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        reduced = image_size // 4
        reduced = max(reduced, 1)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(width * 2 * reduced * reduced, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, n_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class LSTMRegressor(nn.Module):
    """LSTM over a univariate window, predicting one scalar.

    Input (batch, seq_len, 1). The final hidden state is passed through a linear
    layer. `batch_first=True` keeps the shapes readable.
    """

    def __init__(self, hidden_size=32, num_layers=1, dropout=0.0):
        super().__init__()
        self.lstm = nn.LSTM(1, hidden_size, num_layers=num_layers,
                            batch_first=True, dropout=dropout if num_layers > 1 else 0.0)
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1, :]).squeeze(-1)


class TinyTransformerClassifier(nn.Module):
    """Embedding + positional encoding + one Transformer encoder layer + mean pool.

    Small enough to train on CPU, complete enough to show every component of the
    architecture: token embedding, positional information, multi-head self-attention,
    feedforward block, residual connections and layer normalisation — the latter three
    are inside `nn.TransformerEncoderLayer`.
    """

    def __init__(self, vocab_size, max_len=12, d_model=32, nhead=4, n_classes=2, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.position = nn.Parameter(torch.zeros(1, max_len, d_model))
        layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=64,
            dropout=dropout, batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=1)
        self.head = nn.Linear(d_model, n_classes)

    def forward(self, x):
        mask = (x == 0)
        h = self.embedding(x) + self.position[:, : x.shape[1], :]
        h = self.encoder(h, src_key_padding_mask=mask)
        # Mean-pool over non-padding positions so padding does not dilute the signal.
        lengths = (~mask).sum(dim=1, keepdim=True).clamp(min=1)
        pooled = (h * (~mask).unsqueeze(-1)).sum(dim=1) / lengths
        return self.head(pooled)


class AutoEncoder(nn.Module):
    """Symmetric bottleneck network for reconstruction and anomaly scoring.

    The encoder compresses a flattened image to `latent` dimensions; the decoder
    rebuilds it. Trained only on normal data, the reconstruction error becomes an
    anomaly score: unseen structure is compressed badly and rebuilt badly.
    """

    def __init__(self, in_features=64, latent=8, hidden=(32,)):
        super().__init__()
        encoder, previous = [], in_features
        for width in hidden:
            encoder += [nn.Linear(previous, width), nn.ReLU()]
            previous = width
        encoder.append(nn.Linear(previous, latent))
        self.encoder = nn.Sequential(*encoder)

        decoder, previous = [], latent
        for width in reversed(hidden):
            decoder += [nn.Linear(previous, width), nn.ReLU()]
            previous = width
        decoder.append(nn.Linear(previous, in_features))
        self.decoder = nn.Sequential(*decoder)

    def encode(self, x):
        return self.encoder(torch.flatten(x, start_dim=1))

    def forward(self, x):
        flat = torch.flatten(x, start_dim=1)
        return self.decoder(self.encoder(flat))

    @torch.no_grad()
    def reconstruction_error(self, X):
        """Per-sample mean squared error, shape (n,)."""
        self.eval()
        x = as_tensor(X)
        rebuilt = self.forward(x)
        return ((rebuilt - torch.flatten(x, start_dim=1)) ** 2).mean(dim=1).cpu().numpy()


# ---------------------------------------------------------------------------
# Parameter utilities
# ---------------------------------------------------------------------------
def count_parameters(model) -> int:
    """Trainable parameters only — the number to quote in a model comparison."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def freeze(module) -> None:
    """Stop gradients for every parameter in `module` (transfer-learning step 1)."""
    for parameter in module.parameters():
        parameter.requires_grad = False


def unfreeze(module) -> None:
    for parameter in module.parameters():
        parameter.requires_grad = True


def save_checkpoint(model, path, config=None):
    torch.save({"state_dict": model.state_dict(), "config": config or {}}, path)
    return path


def load_checkpoint(model, path, map_location=None):
    bundle = torch.load(path, map_location=map_location or get_device(), weights_only=False)
    model.load_state_dict(bundle["state_dict"])
    return model, bundle.get("config", {})


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import deep_data as dd

    set_seed(0)
    device = get_device()
    print("device:", device)

    images, labels = dd.digit_images(2400, seed=0)
    split = 1800
    train_loader = make_loader(images[:split], labels[:split], batch_size=64, seed=0)
    val_loader = make_loader(images[split:], labels[split:], batch_size=128, shuffle=False)

    print(f"{'model':22s} {'params':>8s} {'val acc':>8s} {'seconds':>8s}")
    for name, model in [
        ("MLP 64-32", MLP(64, hidden=(32,), n_classes=10)),
        ("CNN width 16", SmallCNN(n_classes=10, width=16, image_size=8)),
    ]:
        start = time.time()
        trainer = Trainer(model, device=device, patience=5)
        trainer.fit(train_loader, val_loader, epochs=5, lr=1e-3, verbose=False)
        _, acc, _, _ = trainer.evaluate(val_loader)
        print(f"{name:22s} {count_parameters(model):8d} {acc:8.3f} {time.time() - start:8.2f}")

    # Sequence demo
    Xs, ys = dd.series_windows(400, seed=0)
    seq_model = LSTMRegressor(hidden_size=24)
    seq_trainer = Trainer(seq_model, criterion=nn.MSELoss(), device=device)
    seq_trainer.fit(
        make_loader(Xs[:320], ys[:320], batch_size=32, seed=0),
        make_loader(Xs[320:], ys[320:], batch_size=64, shuffle=False),
        epochs=25, lr=0.01,
    )
    loss, _, _, _ = seq_trainer.evaluate(make_loader(Xs[320:], ys[320:], batch_size=64, shuffle=False))
    print("LSTM final validation MSE:", round(loss, 4))

    # Autoencoder demo: train on digits 0-7, score digits 8-9 as unseen structure
    images8, labels8 = dd.digit_images(2400, size=8, seed=1)
    normal = labels8 < 8
    flat8 = images8.reshape(len(images8), -1)
    ae = AutoEncoder(in_features=64, latent=8)
    ae_trainer = Trainer(ae, criterion=nn.MSELoss(), device=device, classification=False)
    ae_trainer.fit(make_loader(flat8[normal], flat8[normal], 64, seed=0), epochs=20, lr=1e-3)
    errors = ae.reconstruction_error(flat8)
    print("AE params:", count_parameters(ae))
    print("AE error normal:", round(float(errors[normal].mean()), 4),
          "unseen:", round(float(errors[~normal].mean()), 4))
