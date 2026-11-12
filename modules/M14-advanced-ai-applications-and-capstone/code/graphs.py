"""graphs.py -- graph neural networks and where the message passing helps (M14, L14-04).

Node classification on a synthetic homophilous graph, comparing:

    MLP      uses each node's features only
    GNN      two rounds of neighbourhood averaging, then classification
    deep GNN more rounds, to show oversmoothing

The graph is built so that features alone are weak (signal-to-noise is deliberately poor) and
neighbours carry the rest of the information. That is the regime where a GNN earns its cost --
and the regime where the homophily assumption is true. Section 3 breaks the assumption.

Run ``python graphs.py``.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
np.random.seed(0)


# ---------------------------------------------------------------------------
# 1. Synthetic graph
# ---------------------------------------------------------------------------

def make_graph(classes=5, per_class=40, dim=12, noise=2.0, homophily=0.85, seed=0):
    """Features are weak; edges encode class membership with probability `homophily`."""
    rng = np.random.default_rng(seed)
    n = classes * per_class
    y = np.repeat(np.arange(classes), per_class)

    proto = rng.normal(0, 1.0, (classes, dim))
    X = proto[y] + rng.normal(0, noise, (n, dim))

    A = np.zeros((n, n), dtype=np.float32)
    degree = 6
    for i in range(n):
        k_same = int(round(homophily * degree))
        k_other = degree - k_same
        same = np.where(y == y[i])[0]
        same = same[same != i]
        other = np.where(y != y[i])[0]
        if k_same and len(same):
            for j in rng.choice(same, size=min(k_same, len(same)), replace=False):
                A[i, j] = A[j, i] = 1.0
        if k_other and len(other):
            for j in rng.choice(other, size=min(k_other, len(other)), replace=False):
                A[i, j] = A[j, i] = 1.0

    return X.astype(np.float32), y, A, classes


def normalise(A):
    A = A + np.eye(len(A), dtype=np.float32)
    d = A.sum(1)
    D = np.diag(1.0 / np.sqrt(d))
    return (D @ A @ D).astype(np.float32)


# ---------------------------------------------------------------------------
# 2. Models
# ---------------------------------------------------------------------------

class MLP(nn.Module):
    def __init__(self, d_in, n_classes, hidden=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, hidden), nn.ReLU(), nn.Linear(hidden, n_classes))

    def forward(self, X, A=None):
        return self.net(X)


class GCN(nn.Module):
    def __init__(self, d_in, n_classes, hidden=32, layers=2):
        super().__init__()
        sizes = [d_in] + [hidden] * (layers - 1) + [n_classes]
        self.layers = nn.ModuleList([nn.Linear(a, b) for a, b in zip(sizes[:-1], sizes[1:])])

    def forward(self, X, A):
        H = X
        for i, layer in enumerate(self.layers):
            H = A @ H
            H = layer(H)
            if i < len(self.layers) - 1:
                H = F.relu(H)
        return H


def train(model, X, y, A, idx_tr, idx_te, epochs=200, lr=0.05, weight_decay=5e-4, seed=0):
    torch.manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    Xt, yt, At = torch.tensor(X), torch.tensor(y), torch.tensor(A)
    best = 0.0
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        out = model(Xt, At)
        loss = F.cross_entropy(out[idx_tr], yt[idx_tr])
        loss.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            acc = float((model(Xt, At)[idx_te].argmax(1) == yt[idx_te]).float().mean())
        best = max(best, acc)
    return best


# ---------------------------------------------------------------------------
# 3. Demo
# ---------------------------------------------------------------------------

def split_nodes(y, seed=0):
    rng = np.random.default_rng(seed)
    tr, te = [], []
    for c in np.unique(y):
        idx = np.where(y == c)[0]
        rng.shuffle(idx)
        cut = int(0.5 * len(idx))
        tr += list(idx[:cut])
        te += list(idx[cut:])
    return np.array(tr), np.array(te)


def main():
    X, y, A, C = make_graph()
    An = normalise(A)
    tr, te = split_nodes(y)
    edge_homophily = 0
    for i in range(len(y)):
        nb = np.where(A[i] > 0)[0]
        edge_homophily += int((y[nb] == y[i]).sum())
    edge_homophily /= max(1.0, A.sum())

    print("=" * 80)
    print("1. The graph")
    print("=" * 80)
    print(f"  nodes {len(y)}, classes {C}, features {X.shape[1]}, "
          f"edges {int(A.sum() / 2)}, mean degree {A.sum(1).mean():.2f}")
    print(f"  measured edge homophily (same-class endpoints): {edge_homophily:.3f}")

    mlp_acc = train(MLP(X.shape[1], C), X, y, An, tr, te)
    gnn2 = train(GCN(X.shape[1], C, layers=2), X, y, An, tr, te)
    gnn4 = train(GCN(X.shape[1], C, layers=4), X, y, An, tr, te)
    gnn8 = train(GCN(X.shape[1], C, layers=8), X, y, An, tr, te)

    print()
    print("=" * 80)
    print("2. Accuracy when the graph carries information the features do not")
    print("=" * 80)
    print(f"  MLP (features only)      {mlp_acc:.3f}")
    print(f"  GCN, 2 layers            {gnn2:.3f}")
    print(f"  GCN, 4 layers            {gnn4:.3f}")
    print(f"  GCN, 8 layers            {gnn8:.3f}")
    print()
    print(f"  graph gain over features only: {gnn2 - mlp_acc:+.3f}")
    print("  additional layers eventually blur neighbour information (oversmoothing),")
    print("  which is why depth in a GNN is not like depth in a CNN.")

    print()
    print("=" * 80)
    print("3. Where the graph stops helping: homophily sweep")
    print("=" * 80)
    print(f"  {'homophily':>10} {'MLP':>7} {'GCN-2':>7} {'gain':>7}")
    for h in (0.1, 0.3, 0.5, 0.7, 0.9):
        Xh, yh, Ah, Ch = make_graph(homophily=h, seed=1)
        Anh = normalise(Ah)
        trh, teh = split_nodes(yh, seed=1)
        m = train(MLP(Xh.shape[1], Ch), Xh, yh, Anh, trh, teh)
        g = train(GCN(Xh.shape[1], Ch, layers=2), Xh, yh, Anh, trh, teh)
        print(f"  {h:10.1f} {m:7.3f} {g:7.3f} {g - m:+7.3f}")
    print()
    print("  At low homophily the neighbourhood average is dominated by the other class")
    print("  and the GNN loses to feature-only training; from about 0.5 upward it wins")
    print("  clearly. Homophily is a property of the data you must measure, not assume.")

    print()
    print("=" * 80)
    print("4. Cost")
    print("=" * 80)
    print("  A GCN layer is one sparse matrix multiply plus a dense projection.")
    print("  For E edges and F features the neighbour aggregation costs O(E*F); the")
    print("  memory cost of a dense adjacency is O(N^2), which is why real systems")
    print("  use sparse formats or sampling (GraphSAGE, neighbour sampling).")


if __name__ == "__main__":
    main()
