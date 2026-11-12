"""federated.py -- federated learning, non-IID data and the privacy cost (M14, L14-04).

Three ways to learn the same classifier from data held by ten clients:

    centralised   pool every client's rows (the baseline nobody can actually run)
    local only    each client trains alone, evaluated globally
    FedAvg        clients train locally, the server averages weights each round
    FedAvg + DP   the same, with per-client gradient clipping and Gaussian noise

The data split is deliberately non-IID: each client sees two digit classes. That is the
setting where federated averaging is hardest, and where the accuracy gap is worth measuring
rather than assuming.

Run ``python federated.py``.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

torch.manual_seed(0)
np.random.seed(0)


def make_model(d_in=64, n_classes=10):
    return nn.Sequential(nn.Linear(d_in, 32), nn.ReLU(), nn.Linear(32, n_classes))


def accuracy(model, X, y):
    with torch.no_grad():
        return float((model(torch.tensor(X)).argmax(1).numpy() == y).mean())


def local_train(model, X, y, epochs=3, lr=0.05, clip=None, sigma=0.0, seed=0):
    """Train a copy locally; optionally clip the update and add Gaussian noise."""
    torch.manual_seed(seed)
    before = [p.detach().clone() for p in model.parameters()]
    opt = torch.optim.SGD(model.parameters(), lr=lr)
    Xt, yt = torch.tensor(X), torch.tensor(y)
    for _ in range(epochs):
        opt.zero_grad()
        F.cross_entropy(model(Xt), yt).backward()
        opt.step()
    if clip is None:
        return model
    # clip the *update*, then add noise -- the DP-SGD pattern
    with torch.no_grad():
        for p, b in zip(model.parameters(), before):
            delta = p - b
            norm = delta.norm()
            if norm > clip:
                delta *= clip / (norm + 1e-12)
            p.copy_(b + delta + torch.randn_like(p) * sigma * clip)
    return model


def avg_models(models, weights=None):
    out = make_model()
    with torch.no_grad():
        for i, p in enumerate(out.parameters()):
            stack = torch.stack([list(m.parameters())[i].detach() for m in models])
            if weights is None:
                p.copy_(stack.mean(0))
            else:
                w = torch.tensor(weights, dtype=torch.float32).view(-1, *([1] * (stack.dim() - 1)))
                p.copy_((stack * w).sum(0) / w.sum())
    return out


def fedavg(clients, rounds=50, local_epochs=5, lr=0.1, clip=None, sigma=0.0):
    global_model = make_model()
    for r in range(rounds):
        locals_ = []
        for Xc, yc in clients:
            m = make_model()
            m.load_state_dict(global_model.state_dict())
            m = local_train(m, Xc, yc, epochs=local_epochs, lr=lr,
                            clip=clip, sigma=sigma, seed=r)
            locals_.append(m)
        global_model = avg_models(locals_)
        if (r + 1) in (1, 5, 10, 25, 50):
            yield r + 1, global_model


def main():
    d = load_digits()
    X = (d.data / 16.0).astype(np.float32)
    y = d.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

    # non-IID: ten clients, each holding two classes
    clients = []
    for c in range(10):
        cls = [(c) % 10, (c + 5) % 10]
        idx = np.where(np.isin(ytr, cls))[0]
        rng = np.random.default_rng(c)
        rng.shuffle(idx)
        keep = idx[: int(0.5 * len(idx))]
        clients.append((Xtr[keep], ytr[keep]))
    print("=" * 82)
    print("1. Ten clients, non-IID label split")
    print("=" * 82)
    print(f"  {'client':>6} {'rows':>6} {'classes':>14}")
    for i, (Xc, yc) in enumerate(clients[:5]):
        print(f"  {i:6d} {len(yc):6d} {str(sorted(set(yc.tolist()))):>14}")
    print("  ... (5 more; every client sees 2 of the 10 classes, disjoint pairs)")

    print("\n" + "=" * 82)
    print("2. Centralised, local-only and federated")
    print("=" * 82)
    central = make_model()
    train_X = np.concatenate([c[0] for c in clients])
    train_y = np.concatenate([c[1] for c in clients])
    opt = torch.optim.Adam(central.parameters(), lr=3e-3)
    for _ in range(80):
        opt.zero_grad()
        F.cross_entropy(central(torch.tensor(train_X)), torch.tensor(train_y)).backward()
        opt.step()
    central_acc = accuracy(central, Xte, yte)

    local_accs = []
    for Xc, yc in clients:
        m = local_train(make_model(), Xc, yc, epochs=20, lr=0.05)
        local_accs.append(accuracy(m, Xte, yte))
    print(f"  centralised (pooled)      {central_acc:.3f}")
    print(f"  local only, mean          {np.mean(local_accs):.3f} "
          f"(min {min(local_accs):.3f}, max {max(local_accs):.3f})")

    history = {}
    for label, kw in (("FedAvg", {}), ("FedAvg + DP", {"clip": 1.0, "sigma": 0.02})):
        accs = {}
        for r, model in fedavg(clients, rounds=50, **kw):
            accs[r] = accuracy(model, Xte, yte)
        history[label] = accs
        print(f"  {label:25s} {accs[50]:.3f} at round 50 "
              f"(round 5: {accs[5]:.3f})")

    print("\n" + "=" * 82)
    print("3. Convergence")
    print("=" * 82)
    print(f"  {'round':>6} {'FedAvg':>9} {'FedAvg+DP':>11}")
    for r in (1, 10, 25, 50):
        print(f"  {r:6d} {history['FedAvg'][r]:9.3f} {history['FedAvg + DP'][r]:11.3f}")

    # per-client fairness: who benefits?
    global_plain = None
    for r, m in fedavg(clients, rounds=50):
        global_plain = m
    per_client = [accuracy(global_plain, Xte[yte == c], yte[yte == c]) for c in range(10)]
    print("\n" + "=" * 82)
    print("4. Per-class accuracy of the federated model (fairness across clients)")
    print("=" * 82)
    print("  " + "  ".join(f"{c}:{a:.2f}" for c, a in enumerate(per_client)))
    print(f"  spread: {max(per_client) - min(per_client):.3f}")
    print("  A client whose classes are rare or unusual can end up worse off than if it")
    print("  had trained alone. Federated learning improves the average, not every client,")
    print("  and the per-client table is the honest way to report it.")

    print("\n" + "=" * 82)
    print("5. What the DP cost means")
    print("=" * 82)
    print("  clip=1.0 bounds each client's update; sigma=0.02 adds noise proportional to")
    print("  that bound. The privacy guarantee depends on sigma, the number of rounds and")
    print("  the sampling rate -- none of which this script computes. Reporting 'DP' without")
    print("  an epsilon is a claim, not a guarantee; use a proper accountant before you do.")


if __name__ == "__main__":
    main()
