"""graphs.py -- graph neural networks and where the message passing helps (M14, L14-04).

Two synthetic graph families, two evaluation protocols, one question: when does the graph
carry information that node features do not?

Families
--------
random-mix  each edge slot is same-class with probability `homophily`, otherwise uniform
SBM         stochastic block model: within-class edge probability `p_in`, cross-class `p_out`

Protocols
---------
transductive  train and test nodes share one graph; 20% of labels are used for training
inductive     disjoint train/validation/test nodes; the test subgraph is hidden during
              training, validation selects the epoch, and test labels are used once, for
              the final metrics

Baselines and models
--------------------
majority    predicts the most frequent training class
MLP         uses node features only
GCN         two rounds of neighbourhood averaging, then classification

The experiment is deliberately not saturated: only a minority of nodes are labelled,
10% of training labels are flipped by default, every condition is repeated over seeds, and
the test set is never used to choose an epoch or a hyperparameter.

Run ``python graphs.py``.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support

SEEDS = (0, 1, 2, 3, 4)
TRAIN_FRACTION = 0.2
LABEL_NOISE = 0.1
DEGREE = 4
HOMOPHILY = 0.75
FEATURE_NOISE = 2.6
PROTOTYPE_NOISE = 1.0

torch.manual_seed(0)
np.random.seed(0)


# ---------------------------------------------------------------------------
# 1. Graph families
# ---------------------------------------------------------------------------

def _features_and_labels(classes, per_class, dim, noise, seed):
    rng = np.random.default_rng(seed)
    n = classes * per_class
    y = np.repeat(np.arange(classes), per_class)
    prototype_rng = np.random.default_rng(50_000 + seed % 5)
    proto = prototype_rng.normal(0, PROTOTYPE_NOISE, (classes, dim))
    X = proto[y] + rng.normal(0, noise, (n, dim))
    return X.astype(np.float32), y, rng


def make_graph(classes=5, per_class=40, dim=12, noise=FEATURE_NOISE, homophily=HOMOPHILY,
               degree=DEGREE, seed=0):
    """Random-mix family: each edge slot is same-class with probability `homophily`."""
    X, y, rng = _features_and_labels(classes, per_class, dim, noise, seed)
    n = len(y)
    A = np.zeros((n, n), dtype=np.float32)
    everyone = np.arange(n)
    for i in range(n):
        for _ in range(degree):
            if rng.random() < homophily:
                pool = np.where(y == y[i])[0]
                pool = pool[pool != i]
            else:
                pool = everyone[everyone != i]
            j = rng.choice(pool)
            A[i, j] = A[j, i] = 1.0
    return X, y, A, classes


def make_sbm(classes=5, per_class=40, dim=12, noise=FEATURE_NOISE, p_in=0.12, p_out=0.01,
             seed=0):
    """Stochastic block model with class blocks and controllable homophily.

    Each within-class pair is connected with probability `p_in`; each cross-class pair with
    `p_out`. Lower `p_out` means higher homophily. The expected degree is
    `(per_class - 1) * p_in + (classes - 1) * per_class * p_out`.

    Assumption: class is the only block structure, and edges are independent given the
    blocks. Real graphs have degree heterogeneity, communities that do not equal labels,
    and higher-order structure, none of which is modelled here.
    """
    X, y, rng = _features_and_labels(classes, per_class, dim, noise, seed)
    n = len(y)
    A = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(i + 1, n):
            p = p_in if y[i] == y[j] else p_out
            if rng.random() < p:
                A[i, j] = A[j, i] = 1.0
    return X, y, A, classes


def generate(family, **kwargs):
    if family == "random-mix":
        return make_graph(**kwargs)
    if family == "sbm":
        return make_sbm(**kwargs)
    raise ValueError(f"unknown graph family: {family!r}")


def normalise(A):
    A = A + np.eye(len(A), dtype=np.float32)
    d = A.sum(1)
    D = np.diag(1.0 / np.sqrt(d))
    return (D @ A @ D).astype(np.float32)


def edge_homophily(A, y):
    """Fraction of edge endpoints that share a class, counted over directed edges."""
    total = 0
    same = 0
    for i in range(len(y)):
        nb = np.where(A[i] > 0)[0]
        same += int((y[nb] == y[i]).sum())
        total += len(nb)
    return same / max(1, total)


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


def _fit(model, X, y, A, idx_tr, epochs, lr=0.05, weight_decay=5e-4, seed=0):
    torch.manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    Xt, yt, At = torch.tensor(X), torch.tensor(y), torch.tensor(A)
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        loss = F.cross_entropy(model(Xt, At)[idx_tr], yt[idx_tr])
        loss.backward()
        opt.step()


def train(model, X, y, A, idx_tr, idx_te, epochs=200, lr=0.05, weight_decay=5e-4, seed=0):
    """Transductive baseline: fixed epochs, test evaluated once at the end."""
    _fit(model, X, y, A, idx_tr, epochs, lr, weight_decay, seed)
    model.eval()
    with torch.no_grad():
        pred = model(torch.tensor(X), torch.tensor(A)).argmax(1).numpy()
    return float((pred[idx_te] == y[idx_te]).mean())


def train_with_validation(model, X, y, A, idx_tr, idx_va, epochs=300, patience=40,
                          lr=0.05, weight_decay=5e-4, seed=0):
    """Inductive training: validation selects the epoch; test is not passed in."""
    torch.manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    Xt, yt, At = torch.tensor(X), torch.tensor(y), torch.tensor(A)
    best_acc, best_state, stale = -1.0, None, 0
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        loss = F.cross_entropy(model(Xt, At)[idx_tr], yt[idx_tr])
        loss.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            val_pred = model(Xt, At)[idx_va].argmax(1).numpy()
        acc = float((val_pred == y[idx_va]).mean())
        if acc > best_acc:
            best_acc = acc
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
            stale = 0
        else:
            stale += 1
            if stale >= patience:
                break
    if best_state is not None:
        model.load_state_dict(best_state)
    return model, best_acc


def predict(model, X, A):
    model.eval()
    with torch.no_grad():
        return model(torch.tensor(X), torch.tensor(A)).argmax(1).numpy()


# ---------------------------------------------------------------------------
# 3. Splits and metrics
# ---------------------------------------------------------------------------

def split_nodes(y, train_frac=TRAIN_FRACTION, seed=0):
    """Transductive split: `train_frac` of every class is labelled, the rest is test."""
    rng = np.random.default_rng(seed)
    tr, te = [], []
    for c in np.unique(y):
        idx = np.where(y == c)[0]
        rng.shuffle(idx)
        cut = int(train_frac * len(idx))
        tr += list(idx[:cut])
        te += list(idx[cut:])
    return np.array(tr), np.array(te)


def inductive_split(y, fractions=(0.6, 0.2, 0.2), seed=0):
    """Disjoint stratified train/validation/test split for inductive evaluation."""
    if abs(sum(fractions) - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1")
    rng = np.random.default_rng(seed)
    tr, va, te = [], [], []
    for c in np.unique(y):
        idx = np.where(y == c)[0]
        rng.shuffle(idx)
        n = len(idx)
        n_tr, n_va = int(fractions[0] * n), int(fractions[1] * n)
        tr += list(idx[:n_tr])
        va += list(idx[n_tr:n_tr + n_va])
        te += list(idx[n_tr + n_va:])
    return np.array(tr), np.array(va), np.array(te)


def noisy_labels(y, idx_tr, fraction=LABEL_NOISE, seed=0):
    """Flip `fraction` of the training labels to a different class; test labels stay clean."""
    y_noisy = y.copy()
    rng = np.random.default_rng(10_000 + seed)
    flip = rng.choice(idx_tr, size=int(fraction * len(idx_tr)), replace=False)
    y_noisy[flip] = (y_noisy[flip] + 1) % len(np.unique(y))
    return y_noisy


def evaluate_metrics(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0)
    return {
        "accuracy": float((np.asarray(y_true) == np.asarray(y_pred)).mean()),
        "macro_f1": float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)),
        "confusion": cm,
        "per_class": [{"class": int(c), "precision": float(p), "recall": float(r),
                       "f1": float(f), "support": int(s)}
                      for c, p, r, f, s in zip(labels, precision, recall, f1, support)],
    }


def majority_baseline(y_train, y_test, n_classes):
    values, counts = np.unique(y_train, return_counts=True)
    majority = int(values[np.argmax(counts)])
    return np.full(len(y_test), majority, dtype=int), np.full(n_classes, majority)


# ---------------------------------------------------------------------------
# 4. Experiment runners
# ---------------------------------------------------------------------------

def _prepare_transductive(family, seed, label_noise, train_fraction=TRAIN_FRACTION,
                          **family_kwargs):
    X, y, A, C = generate(family, seed=seed, **family_kwargs)
    An = normalise(A)
    tr, te = split_nodes(y, train_frac=train_fraction, seed=seed)
    yt = noisy_labels(y, tr, fraction=label_noise, seed=seed)
    return X, y, A, yt, An, tr, te, C


def run_transductive(family, seed, label_noise=LABEL_NOISE,
                     train_fraction=TRAIN_FRACTION, **family_kwargs):
    """Transductive comparison with one fixed training budget for both models."""
    X, y, A, yt, An, tr, te, C = _prepare_transductive(
        family, seed, label_noise=label_noise, train_fraction=train_fraction,
        **family_kwargs)
    out = {}
    for name, factory in (("mlp", MLP), ("gcn", GCN)):
        torch.manual_seed(seed)
        model = factory(X.shape[1], C)
        _fit(model, X, yt, An, tr, epochs=200, seed=seed)
        pred = predict(model, X, An)
        out[name] = evaluate_metrics(y[te], pred[te], list(range(C)))
    majority_pred, _ = majority_baseline(yt[tr], y[te], C)
    out["majority"] = evaluate_metrics(y[te], majority_pred, list(range(C)))
    out["homophily"] = edge_homophily(A, y)
    return out


def _inductive_adjacencies(A, idx_test):
    fit = A.copy()
    fit[idx_test, :] = 0.0
    fit[:, idx_test] = 0.0
    infer = A.copy()
    infer[np.ix_(idx_test, idx_test)] = 0.0
    return normalise(fit), normalise(infer)


def run_transductive_matched(family, seed, label_noise=LABEL_NOISE, **family_kwargs):
    """Transductive control with the *same* train/test nodes as the inductive run.

    Validation nodes are unused and test-test edges remain visible to message passing, so
    this isolates the protocol (full graph vs held-out test subgraph) from the size of the
    training set and the identity of the test set.
    """
    X, y, A, C = generate(family, seed=seed, **family_kwargs)
    tr, _va, te = inductive_split(y, seed=seed)
    yt = noisy_labels(y, tr, fraction=label_noise, seed=seed)
    An = normalise(A)
    out = {}
    for name, factory in (("mlp", MLP), ("gcn", GCN)):
        torch.manual_seed(seed)
        model = factory(X.shape[1], C)
        _fit(model, X, yt, An, tr, epochs=200, seed=seed)
        pred = predict(model, X, An)
        out[name] = evaluate_metrics(y[te], pred[te], list(range(C)))
    majority_pred, _ = majority_baseline(yt[tr], y[te], C)
    out["majority"] = evaluate_metrics(y[te], majority_pred, list(range(C)))
    out["homophily"] = edge_homophily(A, y)
    return out


def run_inductive(family, seed, label_noise=LABEL_NOISE, **family_kwargs):
    """Inductive comparison: disjoint splits, validation-only selection, one test pass."""
    X, y, A, C = generate(family, seed=seed, **family_kwargs)
    tr, va, te = inductive_split(y, seed=seed)
    yt = noisy_labels(y, tr, fraction=label_noise, seed=seed)
    A_fit, A_infer = _inductive_adjacencies(A, te)
    out = {}
    for name, factory in (("mlp", MLP), ("gcn", GCN)):
        torch.manual_seed(seed)
        model = factory(X.shape[1], C)
        model, val_acc = train_with_validation(model, X, yt, A_fit, tr, va, seed=seed)
        pred = predict(model, X, A_infer)
        result = evaluate_metrics(y[te], pred[te], list(range(C)))
        result["validation_accuracy"] = float(val_acc)
        out[name] = result
    majority_pred, _ = majority_baseline(yt[tr], y[te], C)
    out["majority"] = evaluate_metrics(y[te], majority_pred, list(range(C)))
    out["homophily"] = edge_homophily(A, y)
    return out


# ---------------------------------------------------------------------------
# 5. Summaries
# ---------------------------------------------------------------------------

def summarise(runs, key, metric="accuracy"):
    values = [run[key][metric] for run in runs]
    return float(np.mean(values)), float(np.std(values))


def _main_table(title, family, protocol):
    runner = run_transductive if protocol == "transductive" else run_inductive
    runs = [runner(family, seed) for seed in SEEDS]
    print(f"\n{title}")
    print(f"  {'model':<12}{'accuracy':>18}{'macro-F1':>18}")
    for key in ("majority", "mlp", "gcn"):
        acc, acc_sd = summarise(runs, key, "accuracy")
        f1, f1_sd = summarise(runs, key, "macro_f1")
        print(f"  {key:<12}{acc:10.3f} ± {acc_sd:.3f}   {f1:10.3f} ± {f1_sd:.3f}")
    gap = summarise(runs, "gcn")[0] - summarise(runs, "mlp")[0]
    print(f"  GCN minus MLP: {gap:+.3f} accuracy")
    return runs


def _homophily_sweep(family, protocol, settings):
    runner = run_transductive if protocol == "transductive" else run_inductive
    print(f"\n  homophily sweep — {family}, {protocol}")
    print(f"  {'h':>8}{'MLP':>9}{'GCN':>9}{'gain':>9}")
    for setting in settings:
        runs = [runner(family, seed, **setting) for seed in SEEDS]
        mlp, _ = summarise(runs, "mlp")
        gcn, _ = summarise(runs, "gcn")
        h = float(np.mean([run["homophily"] for run in runs]))
        print(f"  {h:8.3f}{mlp:9.3f}{gcn:9.3f}{gcn - mlp:+9.3f}")


def _depth_table(family):
    print(f"\n  depth — {family}, transductive")
    for layers in (2, 4, 8):
        values = []
        for seed in SEEDS:
            X, y, A, C = generate(family, seed=seed)
            An = normalise(A)
            tr, te = split_nodes(y, seed=seed)
            yt = noisy_labels(y, tr, seed=seed)
            torch.manual_seed(seed)
            model = GCN(X.shape[1], C, layers=layers)
            _fit(model, X, yt, An, tr, epochs=200, seed=seed)
            pred = predict(model, X, An)
            values.append(float((pred[te] == y[te]).mean()))
        print(f"  GCN-{layers}: {np.mean(values):.3f} ± {np.std(values):.3f}")


def _noise_sweep(family):
    print(f"\n  label-noise sweep — {family}, transductive")
    print(f"  {'noise':>8}{'MLP':>9}{'GCN':>9}{'gain':>9}")
    for noise in (0.0, 0.1, 0.2):
        runs = [run_transductive(family, seed, label_noise=noise) for seed in SEEDS]
        mlp, _ = summarise(runs, "mlp")
        gcn, _ = summarise(runs, "gcn")
        print(f"  {noise:8.2f}{mlp:9.3f}{gcn:9.3f}{gcn - mlp:+9.3f}")


def _print_confusion(family, protocol):
    runner = run_transductive if protocol == "transductive" else run_inductive
    result = runner(family, seed=0)
    print(f"\n  GCN confusion matrix — {family}, {protocol}, seed 0")
    print("        " + "".join(f"{c:>7}" for c in range(len(result["gcn"]["confusion"]))))
    for c, row in enumerate(result["gcn"]["confusion"]):
        print(f"  true {c}" + "".join(f"{v:7d}" for v in row))
    per_class = result["gcn"]["per_class"]
    print("  class   precision  recall   f1")
    for row in per_class:
        print(f"  {row['class']:>5}   {row['precision']:8.3f} {row['recall']:7.3f} "
              f"{row['f1']:6.3f}")


def main():
    print("=" * 78)
    print("1. Graph families at the default setting")
    print("=" * 78)
    for family in ("random-mix", "sbm"):
        X, y, A, C = generate(family, seed=0)
        print(f"  {family:<12} nodes {len(y)}, edges {int(A.sum() / 2):4d}, "
              f"mean degree {A.sum(1).mean():.2f}, "
              f"edge homophily {edge_homophily(A, y):.3f}")
    print(f"  protocol: 20% labelled (transductive) or 60/20/20 with validation "
          f"(inductive); label noise {LABEL_NOISE:.0%}; seeds {len(SEEDS)}")

    for family in ("random-mix", "sbm"):
        for protocol in ("transductive", "inductive"):
            _main_table(f"2. Default comparison — {family}, {protocol}", family, protocol)

    print("\n" + "=" * 78)
    print("2b. Protocol control at a matched 60% label budget")
    print("=" * 78)
    for family in ("random-mix", "sbm"):
        runs = [run_transductive_matched(family, seed) for seed in SEEDS]
        mlp, mlp_sd = summarise(runs, "mlp")
        gcn, gcn_sd = summarise(runs, "gcn")
        print(f"  {family:<12} transductive control: MLP {mlp:.3f} ± {mlp_sd:.3f}  "
              f"GCN {gcn:.3f} ± {gcn_sd:.3f}  gap {gcn - mlp:+.3f}")
    print("  Same train/test nodes as the inductive rows; only test-test edges differ.")

    print("\n" + "=" * 78)
    print("3. Homophily")
    print("=" * 78)
    _homophily_sweep("random-mix", "transductive",
                     [{"homophily": level} for level in (0.0, 0.25, 0.5, 0.75, 1.0)])
    _homophily_sweep("sbm", "transductive",
                     [{"p_out": level} for level in (0.20, 0.06, 0.02, 0.01, 0.0)])

    print("\n" + "=" * 78)
    print("3b. Depth and oversmoothing")
    print("=" * 78)
    for family in ("random-mix", "sbm"):
        _depth_table(family)

    print("\n" + "=" * 78)
    print("4. Label noise")
    print("=" * 78)
    for family in ("random-mix", "sbm"):
        _noise_sweep(family)

    print("\n" + "=" * 78)
    print("5. Confusion matrices and per-class results")
    print("=" * 78)
    for family in ("random-mix", "sbm"):
        for protocol in ("transductive", "inductive"):
            _print_confusion(family, protocol)

    print("\n" + "=" * 78)
    print("6. What these numbers do and do not show")
    print("=" * 78)
    print("  Synthetic graphs with independent edges, balanced classes and one block")
    print("  structure per family. Features are weak by construction, so the graph has")
    print("  something to add. Real graphs have degree skew, overlapping communities and")
    print("  label noise that is not uniform. A GCN win here is conditional on measured")
    print("  homophily; where homophily is low, the graph can hurt. The inductive protocol")
    print("  hides test nodes during training, but test features and their edges to the")
    print("  training subgraph are available at inference, as in a deployed graph service.")
    print("  The transductive protocol is the easier setting and its numbers are not")
    print("  directly comparable to inductive ones.")


if __name__ == "__main__":
    main()
