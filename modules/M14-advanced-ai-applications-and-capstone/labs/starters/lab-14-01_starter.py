"""LAB-14-01 starter — message passing on a small graph, with a modality hook.

The lab asks you to reason about multimodal and graph systems. This starter gives you
the smallest honest graph learner: a two-layer message-passing network implemented with
numpy, trained on a synthetic node-classification task. It runs in a couple of seconds
and has no dependency beyond numpy.

Why the numbers are not 1.000
-----------------------------
Three defects make a toy graph comparison meaningless, and this starter avoids all three:

1. **No train/test separation.** Evaluating on the nodes you trained on measures
   memorisation. Here only 20% of nodes are labelled for training; accuracy is reported
   on the held-out 80%.
2. **A feature that gives the answer away.** If one feature separates the classes
   perfectly, both models score 1.000 and the graph is irrelevant. Here the features are
   deliberately weak.
3. **One seed, one number.** A single run cannot distinguish a real gain from noise.
   Every condition is repeated over five seeds and reported as mean +/- standard deviation.

The training labels are also flipped 10% of the time, so neither model can reach a
perfect score by fitting noise.

What is still missing (your work)
---------------------------------
1. Replace the synthetic node features with a second modality (text embeddings from
   ``M08`` or image features from ``M09``) and align the two feature spaces.
2. Add an edge type and show what changes in the aggregation.
3. Report accuracy against a feature-only baseline that ignores the graph, and say
   whether the graph is doing any work — including at low homophily, where it hurts.

Run:  python lab-14-01_starter.py
"""

import argparse

import numpy as np

SEEDS = (0, 1, 2, 3, 4)
TRAIN_FRACTION = 0.2
LABEL_NOISE = 0.10
DEGREE = 4
HOMOPHILY = 0.75


def make_graph(n=200, dim=8, noise=1.6, homophily=HOMOPHILY, degree=DEGREE, seed=0):
    """Two classes, weak features, and edges that carry part of the class signal."""
    rng = np.random.default_rng(seed)
    labels = (np.arange(n) >= n // 2).astype(int)

    # Two informative dimensions with a small class offset; the rest is noise.
    features = rng.normal(size=(n, dim))
    features[:, 0] += 0.9 * labels
    features[:, 1] += 0.6 * labels

    # Each edge slot is same-class with probability `homophily`; otherwise the neighbour
    # is drawn uniformly from all nodes. This matters: making every non-same edge
    # cross-class would make "0 homophily" perfectly informative rather than random.
    adjacency = np.zeros((n, n))
    everyone = np.arange(n)
    for i in range(n):
        for _ in range(degree):
            if rng.random() < homophily:
                pool = np.where(labels == labels[i])[0]
                pool = pool[pool != i]
            else:
                pool = everyone[everyone != i]
            j = rng.choice(pool)
            adjacency[i, j] = adjacency[j, i] = 1.0
    return adjacency, features, labels


def make_sbm(n=200, dim=8, noise=1.6, p_in=0.12, p_out=0.01, seed=0):
    """Stochastic block model: within-class pairs connect with p_in, cross-class with p_out."""
    rng = np.random.default_rng(seed)
    labels = (np.arange(n) >= n // 2).astype(int)
    features = rng.normal(size=(n, dim))
    features[:, 0] += 0.9 * labels
    features[:, 1] += 0.6 * labels

    adjacency = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            probability = p_in if labels[i] == labels[j] else p_out
            if rng.random() < probability:
                adjacency[i, j] = adjacency[j, i] = 1.0
    return adjacency, features, labels


def normalise(adjacency):
    degree = adjacency.sum(1, keepdims=True)
    return adjacency / np.maximum(degree, 1e-9)


def relu(x):
    return np.maximum(x, 0.0)


def split(labels, fraction=TRAIN_FRACTION, seed=0):
    """Stratified train/test split: `fraction` of each class is labelled."""
    rng = np.random.default_rng(seed)
    train, test = [], []
    for c in np.unique(labels):
        idx = np.where(labels == c)[0]
        rng.shuffle(idx)
        cut = int(fraction * len(idx))
        train += list(idx[:cut])
        test += list(idx[cut:])
    return np.array(train), np.array(test)


def flip_labels(labels, train_idx, fraction=LABEL_NOISE, seed=0):
    """Flip part of the *training* labels; test labels are never touched."""
    noisy = labels.copy()
    rng = np.random.default_rng(10_000 + seed)
    chosen = rng.choice(train_idx, size=int(fraction * len(train_idx)), replace=False)
    noisy[chosen] = 1 - noisy[chosen]
    return noisy


def train(adjacency, features, labels, train_idx, hidden=8, epochs=300, lr=0.5, seed=0):
    """Full-batch gradient descent on the labelled nodes only."""
    rng = np.random.default_rng(seed)
    a_hat = normalise(adjacency + np.eye(len(adjacency)))
    w1 = rng.normal(scale=0.3, size=(features.shape[1], hidden))
    w2 = rng.normal(scale=0.3, size=(hidden, 2))
    y = labels[train_idx]
    for _ in range(epochs):
        h = relu(a_hat @ features @ w1)
        logits = a_hat @ h @ w2
        logits -= logits.max(1, keepdims=True)
        probs = np.exp(logits) / np.exp(logits).sum(1, keepdims=True)

        grad = probs.copy()
        grad[np.arange(len(labels)), labels] -= 1.0
        # Only labelled nodes contribute to the loss.
        mask = np.zeros(len(labels))
        mask[train_idx] = 1.0
        grad *= mask[:, None] / len(train_idx)

        g_w2 = h.T @ (a_hat.T @ grad)
        g_h = (a_hat.T @ grad) @ w2.T * (h > 0)
        g_w1 = features.T @ (a_hat.T @ g_h)
        w1 -= lr * g_w1
        w2 -= lr * g_w2
    return w1, w2, a_hat


def accuracy(w1, w2, a_hat, features, labels, test_idx):
    h = relu(a_hat @ features @ w1)
    pred = np.argmax(a_hat @ h @ w2, axis=1)
    return float((pred[test_idx] == labels[test_idx]).mean())


def evaluate(seed, family="random-mix", level=HOMOPHILY):
    if family == "sbm":
        adjacency, features, labels = make_sbm(p_out=level, seed=seed)
    else:
        adjacency, features, labels = make_graph(homophily=level, seed=seed)
    train_idx, test_idx = split(labels, seed=seed)
    noisy = flip_labels(labels, train_idx, seed=seed)

    graph_model = train(adjacency, features, noisy, train_idx, seed=seed)
    graph_acc = accuracy(*graph_model, features, labels, test_idx)

    feature_only = train(np.zeros_like(adjacency), features, noisy, train_idx, seed=seed)
    baseline_acc = accuracy(*feature_only, features, labels, test_idx)
    return graph_acc, baseline_acc


def measured_homophily(adjacency, labels):
    same = sum((labels[np.where(adjacency[i] > 0)[0]] == labels[i]).sum()
               for i in range(len(labels)))
    return same / max(1, adjacency.sum())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=("random-mix", "sbm"), default="random-mix")
    args = parser.parse_args()

    print(f"family {args.family}; seeds {len(SEEDS)}, train fraction {TRAIN_FRACTION:.0%}, "
          f"training-label noise {LABEL_NOISE:.0%}")
    print(f"\n{'edge homophily':>15}{'graph mean':>12}{'graph sd':>10}"
          f"{'baseline':>10}{'gain':>8}")
    levels = ((0.0, 0.25, 0.5, 0.75, 1.0) if args.family == "random-mix"
              else (0.20, 0.06, 0.02, 0.01, 0.0))
    for level in levels:
        runs = np.array([evaluate(seed, family=args.family, level=level) for seed in SEEDS])
        graph, baseline = runs[:, 0], runs[:, 1]
        measured = []
        for s in SEEDS:
            if args.family == "sbm":
                adjacency, _, labels = make_sbm(p_out=level, seed=s)
            else:
                adjacency, _, labels = make_graph(homophily=level, seed=s)
            measured.append(measured_homophily(adjacency, labels))
        print(f"{np.mean(measured):15.3f}{graph.mean():12.3f}{graph.std():10.3f}"
              f"{baseline.mean():10.3f}{(graph - baseline).mean():+8.3f}")

    print("\nRead the table before writing code: the graph helps only when neighbours")
    print("share the class. At random mixing message passing adds little, and below it the")
    print("graph can be worse than ignoring it entirely. This starter is transductive; the")
    print("reference code shows the inductive protocol and validation-based selection.")
    print("TODO: swap in a second modality, fuse it (concatenate or attention), and")
    print("report whether the graph still adds accuracy once that modality is present.")


if __name__ == "__main__":
    main()
