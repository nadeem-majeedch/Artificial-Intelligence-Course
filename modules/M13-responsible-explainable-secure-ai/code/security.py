"""security.py -- adversarial ML attacks and defences on a small image model (M13, L13-04 / LAB-13-02).

Every experiment runs locally on the 8x8 digits bundled with scikit-learn. The
point is mechanism, not weaponry: each attack is paired with the measurement
that shows whether a defence helps.

    evasion        FGSM and PGD, accuracy against perturbation budget eps
    defence        adversarial training, and input quantisation as a cheap test-time filter
    poisoning      label flips on one class, measured as targeted error rate
    backdoor       a trigger pattern, measured as attack success rate on triggered inputs
    privacy        membership inference from prediction confidence
    extraction     a surrogate trained only on the model's outputs

Nothing here scales to a hosted model, and none of it is a recipe for attacking
someone else's system. It is a measurement lab.

Run ``python security.py``. Numbers in L13-04 and LAB-13-02 come from here.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

torch.set_num_threads(4)


def set_seed(seed: int = 0) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)


class SmallNet(nn.Module):
    def __init__(self, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(64, hidden), nn.ReLU(),
                                 nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, 10))

    def forward(self, x):
        return self.net(x)


def load_data(seed: int = 0):
    d = load_digits()
    X = (d.images.reshape(len(d.images), -1) / 16.0).astype(np.float32)
    y = d.target.astype(np.int64)
    return train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)


def train(model, X, y, epochs: int = 6, batch: int = 128, lr: float = 1e-3,
          adv_eps: float = 0.0, seed: int = 0) -> list[float]:
    set_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    Xt, yt = torch.from_numpy(X), torch.from_numpy(y)
    losses = []
    n = len(Xt)
    for _ in range(epochs):
        perm = torch.randperm(n)
        for i in range(0, n, batch):
            idx = perm[i:i + batch]
            xb, yb = Xt[idx], yt[idx]
            if adv_eps > 0:
                xb = fgsm(model, xb, yb, adv_eps).detach()
            logits = model(xb)
            loss = F.cross_entropy(logits, yb)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss))
    return losses


@torch.no_grad()
def accuracy(model, X, y) -> float:
    logits = model(torch.from_numpy(X))
    return float((logits.argmax(1).numpy() == y).mean())


def fgsm(model, x, y, eps: float) -> torch.Tensor:
    """One-step sign gradient attack in the input space."""
    x = x.clone().detach().requires_grad_(True)
    loss = F.cross_entropy(model(x), y)
    grad, = torch.autograd.grad(loss, x)
    return (x + eps * grad.sign()).clamp(0, 1).detach()


def pgd(model, x, y, eps: float = 0.2, steps: int = 7, alpha: float = 0.03) -> torch.Tensor:
    """Iterative projected gradient attack: stronger, and a better stress test."""
    x_adv = x.clone().detach()
    for _ in range(steps):
        x_adv.requires_grad_(True)
        loss = F.cross_entropy(model(x_adv), y)
        grad, = torch.autograd.grad(loss, x_adv)
        x_adv = (x_adv + alpha * grad.sign()).detach()
        x_adv = torch.max(torch.min(x_adv, x + eps), x - eps).clamp(0, 1)
    return x_adv


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def evasion_sweep(model, X, y, epsilons=(0.0, 0.05, 0.1, 0.2, 0.3)) -> list[dict]:
    Xt, yt = torch.from_numpy(X), torch.from_numpy(y)
    rows = []
    for eps in epsilons:
        adv = fgsm(model, Xt, yt, eps) if eps > 0 else Xt
        pgd_adv = pgd(model, Xt, yt, eps=eps) if eps > 0 else Xt
        with torch.no_grad():
            f_acc = float((model(adv).argmax(1) == yt).float().mean())
            p_acc = float((model(pgd_adv).argmax(1) == yt).float().mean())
        rows.append({"eps": eps, "fgsm_acc": f_acc, "pgd_acc": p_acc})
    return rows


def poison_labels(X, y, source: int = 3, target: int = 8, fraction: float = 0.10,
                  seed: int = 0) -> tuple[np.ndarray, int]:
    """Flip a fraction of one class's labels to another; returns new labels."""
    rng = np.random.default_rng(seed)
    y = y.copy()
    idx = np.where(y == source)[0]
    chosen = rng.choice(idx, size=int(fraction * len(idx)), replace=False)
    y[chosen] = target
    return y, len(chosen)


def targeted_error(model, X, y, source: int = 3) -> float:
    mask = y == source
    if mask.sum() == 0:
        return float("nan")
    with torch.no_grad():
        pred = model(torch.from_numpy(X[mask])).argmax(1).numpy()
    return float((pred != source).mean())


def add_trigger(X: np.ndarray) -> np.ndarray:
    """A 2x2 white patch in the bottom-right corner: the classic backdoor trigger."""
    X = X.copy()
    view = X.reshape(-1, 8, 8)
    view[:, 6:8, 5:8] = 1.0
    return view.reshape(X.shape)


def backdoor_rate(model, X, y, source: int = 3, target: int = 8) -> tuple[float, float]:
    mask = y == source
    triggered = add_trigger(X[mask])
    with torch.no_grad():
        pred = model(torch.from_numpy(triggered)).argmax(1).numpy()
    return float((pred == target).mean()), float(len(pred))


def membership_inference(model, X_train, y_train, X_test, y_test, seed: int = 0) -> dict:
    """Confidence-threshold attack: members tend to be predicted more confidently."""
    with torch.no_grad():
        p_train = torch.softmax(model(torch.from_numpy(X_train)), 1).max(1).values.numpy()
        p_test = torch.softmax(model(torch.from_numpy(X_test)), 1).max(1).values.numpy()
    scores = np.concatenate([p_train, p_test])
    labels = np.concatenate([np.ones(len(p_train)), np.zeros(len(p_test))])
    auc = float(roc_auc_score(labels, scores))
    threshold = float(np.median(p_train))
    tpr = float((p_train > threshold).mean())
    fpr = float((p_test > threshold).mean())
    return {"auc": auc, "threshold": threshold, "tpr": tpr, "fpr": fpr,
            "mean_conf_train": float(p_train.mean()),
            "mean_conf_test": float(p_test.mean())}


def model_extraction(model, X_query, y_query, X_test, y_test) -> dict:
    """Train a surrogate on the target's hard labels; measure agreement."""
    with torch.no_grad():
        pseudo = model(torch.from_numpy(X_query)).argmax(1).numpy()
    surrogate = LogisticRegression(max_iter=2000).fit(X_query, pseudo)
    agree = float((surrogate.predict(X_test) == pseudo_from(model, X_test)).mean())
    true_acc = float((surrogate.predict(X_test) == y_test).mean())
    return {"queries": len(X_query), "agreement": agree, "surrogate_accuracy": true_acc,
            "surrogate": surrogate}


def pseudo_from(model, X) -> np.ndarray:
    with torch.no_grad():
        return model(torch.from_numpy(X)).argmax(1).numpy()


def quantise(X: np.ndarray, levels: int = 4) -> np.ndarray:
    """Test-time input smoothing: a cheap, imperfect defence against small eps."""
    return (np.round(X * levels) / levels).astype(np.float32)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    X_tr, X_te, y_tr, y_te = load_data()
    print("=" * 86)
    print("Data and clean model")
    print("=" * 86)
    print(f"  train {X_tr.shape}  test {X_te.shape}  classes {len(np.unique(y_tr))}")

    set_seed(0)
    model = SmallNet()
    losses = train(model, X_tr, y_tr, epochs=12)
    clean = accuracy(model, X_te, y_te)
    print(f"  final training loss {losses[-1]:.3f}  clean test accuracy {clean:.3f}")

    print("\n" + "=" * 86)
    print("1. Evasion: accuracy under FGSM and PGD")
    print("=" * 86)
    print(f"  {'eps':>5} {'FGSM acc':>10} {'PGD acc':>9}")
    rows = evasion_sweep(model, X_te, y_te)
    for r in rows:
        print(f"  {r['eps']:5.2f} {r['fgsm_acc']:10.3f} {r['pgd_acc']:9.3f}")

    print("\n" + "=" * 86)
    print("2. Defence 1: adversarial training")
    print("=" * 86)
    set_seed(1)
    robust = SmallNet()
    train(robust, X_tr, y_tr, epochs=10, adv_eps=0.2)
    robust_clean = accuracy(robust, X_te, y_te)
    adv_te = fgsm(robust, torch.from_numpy(X_te), torch.from_numpy(y_te), 0.2)
    with torch.no_grad():
        robust_adv = float((robust(adv_te).argmax(1).numpy() == y_te).mean())
    print(f"  clean accuracy      : standard {clean:.3f}  adversarially trained "
          f"{robust_clean:.3f}")
    print(f"  accuracy at eps=0.2 : standard {rows[3]['fgsm_acc']:.3f}  "
          f"adversarially trained {robust_adv:.3f}")

    print("\n" + "=" * 86)
    print("3. Defence 2: input quantisation at test time")
    print("=" * 86)
    adv = fgsm(model, torch.from_numpy(X_te), torch.from_numpy(y_te), 0.1).numpy()
    with torch.no_grad():
        raw = float((model(torch.from_numpy(adv)).argmax(1).numpy() == y_te).mean())
        smoothed = float((model(torch.from_numpy(quantise(adv))).argmax(1).numpy()
                          == y_te).mean())
        clean_smoothed = float((model(torch.from_numpy(quantise(X_te))).argmax(1).numpy()
                                == y_te).mean())
    print(f"  adversarial accuracy  : raw {raw:.3f}  quantised {smoothed:.3f}")
    print(f"  clean accuracy        : quantised {clean_smoothed:.3f}")
    print("  quantisation helps a little here and is not a serious defence.")

    print("\n" + "=" * 86)
    print("4. Poisoning: 10% of class 3 relabelled as 8")
    print("=" * 86)
    y_poison, flipped = poison_labels(X_tr, y_tr)
    set_seed(2)
    poisoned = SmallNet()
    train(poisoned, X_tr, y_poison, epochs=10)
    print(f"  flipped {flipped} labels")
    print(f"  clean accuracy {accuracy(poisoned, X_te, y_te):.3f} "
          f"(baseline {clean:.3f})")
    print(f"  fraction of true 3s misclassified: {targeted_error(poisoned, X_te, y_te):.3f} "
          f"(baseline {targeted_error(model, X_te, y_te):.3f})")

    print("\n" + "=" * 86)
    print("5. Backdoor: a 2x2 trigger patch, 30% of class 3 relabelled as 8")
    print("=" * 86)
    rng = np.random.default_rng(3)
    y_back = y_tr.copy()
    idx = np.where(y_back == 3)[0]
    chosen = rng.choice(idx, size=int(0.30 * len(idx)), replace=False)
    y_back[chosen] = 8
    X_back = X_tr.copy()
    X_back[chosen] = add_trigger(X_back[chosen])
    set_seed(3)
    trojan = SmallNet()
    train(trojan, X_back, y_back, epochs=14)
    asr, n_src = backdoor_rate(trojan, X_te, y_te)
    print(f"  clean accuracy {accuracy(trojan, X_te, y_te):.3f}")
    print(f"  attack success rate on triggered class-3 inputs: {asr:.3f} (n={int(n_src)})")
    print(f"  same inputs without the trigger: "
          f"{targeted_error(trojan, X_te, y_te):.3f} misclassified")

    print("\n" + "=" * 86)
    print("6. Membership inference")
    print("=" * 86)
    mi = membership_inference(model, X_tr, y_tr, X_te, y_te)
    print(f"  mean confidence train {mi['mean_conf_train']:.3f}  test "
          f"{mi['mean_conf_test']:.3f}")
    print(f"  attack AUC {mi['auc']:.3f}  TPR {mi['tpr']:.3f}  FPR {mi['fpr']:.3f} "
          f"at threshold {mi['threshold']:.3f}")

    print("\n" + "=" * 86)
    print("7. Model extraction from query access")
    print("=" * 86)
    n_q = 300
    X_query, y_query = X_te[:n_q], y_te[:n_q]
    ex = model_extraction(model, X_query, y_query, X_te[n_q:], y_te[n_q:])
    print(f"  queries {ex['queries']}  surrogate agreement {ex['agreement']:.3f}  "
          f"true accuracy {ex['surrogate_accuracy']:.3f}")

    print("\n" + "=" * 86)
    print("8. Summary")
    print("=" * 86)
    print(f"  {'experiment':34s} {'result':>10}")
    print(f"  {'clean accuracy':34s} {clean:10.3f}")
    print(f"  {'accuracy at eps=0.2 (FGSM)':34s} {rows[3]['fgsm_acc']:10.3f}")
    print(f"  {'robust accuracy at eps=0.2':34s} {robust_adv:10.3f}")
    print(f"  {'membership inference AUC':34s} {mi['auc']:10.3f}")
    print(f"  {'extraction agreement':34s} {ex['agreement']:10.3f}")
    print(f"  {'backdoor attack success rate':34s} {asr:10.3f}")


if __name__ == "__main__":
    main()
