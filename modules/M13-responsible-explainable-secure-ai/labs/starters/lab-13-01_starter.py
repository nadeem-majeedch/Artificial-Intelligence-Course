"""LAB-13-01 starter — fairness audit of a toy recruitment model.

What this gives you
-------------------
* the synthetic dataset the module ships (``code/data/rai_datasets.npz``);
* a trained baseline and the four group metrics already printed;
* a place to add the mitigations the lab asks for.

What is missing (your work)
---------------------------
1. Choose a decision threshold on purpose instead of using 0.5, and justify it.
2. Implement one mitigation (reweighing, threshold adjustment or removing a proxy).
3. Report accuracy *and* both gaps after the mitigation, plus the trade-off you accepted.

Run:  python lab-13-01_starter.py     (from the module's code directory, or as-is)
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "..", "..", "code")
sys.path.insert(0, CODE)

from fairness import disparate_impact_ratio, group_metrics  # noqa: E402

DATA = os.path.join(CODE, "data", "rai_datasets.npz")


def load():
    bundle = np.load(DATA, allow_pickle=False)
    return bundle["recruitment_X"], bundle["recruitment_y"], bundle["recruitment_group"]


def train(X, y, seed=0):
    """Logistic regression by gradient descent, written here to keep the starter runnable."""
    rng = np.random.default_rng(seed)
    X = np.asarray(X, dtype=float)
    X = (X - X.mean(0)) / (X.std(0) + 1e-9)
    X = np.c_[np.ones(len(X)), X]
    w = np.zeros(X.shape[1])
    for _ in range(400):
        p = 1 / (1 + np.exp(-X @ w))
        w -= 0.5 * (X.T @ (p - y)) / len(y)
    return w, X.mean(0), X.std(0) + 1e-9


def predict(w, X):
    X = np.asarray(X, dtype=float)
    X = (X - X.mean(0)) / (X.std(0) + 1e-9)
    return 1 / (1 + np.exp(-(np.c_[np.ones(len(X)), X] @ w)))


def main():
    X, y, group = load()
    split = int(0.7 * len(X))
    w, _mu, _sd = train(X[:split], y[:split])

    scores = predict(w, X[split:])
    threshold = 0.5                      # TODO: justify a different threshold
    predicted = (scores >= threshold).astype(int)
    truth, labels = y[split:], group[split:]

    metrics = group_metrics(truth, predicted, labels)
    print(f"threshold {threshold}: accuracy {(predicted == truth).mean():.3f}")
    for name, values in metrics.items():
        print(f"  group {name}: selection {values['selection_rate']:.3f} "
              f"TPR {values['tpr']:.3f} FPR {values['fpr']:.3f}")
    print(f"  disparate impact ratio: {disparate_impact_ratio(metrics):.3f}")

    # TODO: mitigation. Reweigh the training rows by 1/P(group, label), retrain, and
    # print the same table. Does the gap close by moving the boundary or by moving
    # the threshold? State which one you would defend to a regulator, and why.


if __name__ == "__main__":
    main()
