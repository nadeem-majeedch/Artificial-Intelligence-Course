"""efficiency.py -- distillation, int8 quantisation, pruning and latency (M14, L14-02).

One teacher, three compressions, four measurements: accuracy, model size, parameter count and
single-example latency. Compression claims need all four, because the cost shows up in a
different column depending on the method -- and sometimes it shows up as *slower* inference.

    teacher          64 -> 256 -> 256 -> 10
    student          64 -> 64 -> 10, trained from scratch and by distillation
    int8              symmetric per-output-channel weight quantisation of the student
    pruning          50% of the smallest-magnitude weights set to zero

Run ``python efficiency.py``.
"""

from __future__ import annotations

import copy
import platform
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

torch.manual_seed(0)
np.random.seed(0)


def mlp(dims):
    layers = []
    for a, b in zip(dims[:-1], dims[1:]):
        layers += [nn.Linear(a, b), nn.ReLU()]
    return nn.Sequential(*layers[:-1])


class Net(nn.Module):
    def __init__(self, dims):
        super().__init__()
        self.net = mlp(dims)

    def forward(self, x):
        return self.net(x)


def train(model, X, y, epochs=40, lr=3e-3, teacher=None, T=4.0, alpha=0.5, seed=0):
    torch.manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    Xt, yt = torch.tensor(X), torch.tensor(y)
    for _ in range(epochs):
        opt.zero_grad()
        logits = model(Xt)
        loss = F.cross_entropy(logits, yt)
        if teacher is not None:
            with torch.no_grad():
                soft = F.log_softmax(teacher(Xt) / T, dim=1)
            loss = alpha * loss + (1 - alpha) * F.kl_div(
                F.log_softmax(logits / T, dim=1), soft, log_target=True) * (T * T)
        loss.backward()
        opt.step()
    return model


def accuracy(model, X, y):
    with torch.no_grad():
        return float((model(torch.tensor(X)).argmax(1).numpy() == y).mean())


class Int8Linear(nn.Module):
    """Symmetric per-output-channel int8 weights, float32 activations."""

    def __init__(self, linear: nn.Linear):
        super().__init__()
        W = linear.weight.detach()
        scale = W.abs().amax(dim=1, keepdim=True).clamp_min(1e-8) / 127.0
        self.register_buffer("W_int8", torch.round(W / scale).clamp(-127, 127).to(torch.int8))
        self.register_buffer("scale", scale)
        self.bias = nn.Parameter(linear.bias.detach().clone(), requires_grad=False)

    def forward(self, x):
        W = self.W_int8.to(torch.float32) * self.scale
        return F.linear(x, W, self.bias)


def quantise(model):
    q = copy.deepcopy(model)
    q.net = nn.Sequential(*[Int8Linear(m) if isinstance(m, nn.Linear) else m for m in q.net])
    return q


def prune(model, fraction=0.5):
    p = copy.deepcopy(model)
    with torch.no_grad():
        for m in p.net:
            if isinstance(m, nn.Linear):
                flat = m.weight.abs().flatten()
                k = int(fraction * flat.numel())
                if k:
                    threshold = flat.sort().values[k - 1]
                    m.weight.mul_((m.weight.abs() > threshold).float())
    return p


def n_params(model):
    return sum(p.numel() for p in model.parameters())


def size_kb(model):
    return (sum(p.numel() * p.element_size() for p in model.parameters())
            + sum(b.numel() * b.element_size() for b in model.buffers())) / 1024


def latency_us(model, x_single, reps=300, trials=3):
    """Median single-example CPU latency over independent timed trials."""
    model.eval()
    with torch.no_grad():
        for _ in range(20):
            model(x_single)
        timings = []
        for _ in range(trials):
            t0 = time.perf_counter()
            for _ in range(reps):
                model(x_single)
            timings.append((time.perf_counter() - t0) / reps * 1e6)
    return float(np.median(timings))


def main():
    d = load_digits()
    X = (d.data / 16.0).astype(np.float32)
    y = d.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

    teacher = train(Net([64, 256, 256, 10]), Xtr, ytr, epochs=50)
    student = train(Net([64, 64, 10]), Xtr, ytr, epochs=40)
    distilled = train(Net([64, 64, 10]), Xtr, ytr, epochs=40, teacher=teacher)
    q8 = quantise(distilled)
    pruned = prune(distilled, 0.5)

    rows = [("teacher", teacher), ("student (scratch)", student),
            ("student (distilled)", distilled), ("distilled int8", q8),
            ("distilled 50% pruned", pruned)]
    xs = torch.tensor(Xte[:1])

    print("=" * 84)
    print("1. Accuracy, size, parameters and latency")
    print("=" * 84)
    print(f"environment: Python {platform.python_version()}, PyTorch {torch.__version__}, "
          f"threads {torch.get_num_threads()}, {platform.platform()}")
    print("latency: one test example, eval/no_grad, 20 warm-up calls, then the median")
    print("         of 3 trials x 300 forward calls; CPU wall clock, not a target-device claim")
    print(f"{'model':22s} {'accuracy':>9} {'size KB':>9} {'params':>9} {'us/example':>12}")
    measured = []
    for name, m in rows:
        measured.append((name, accuracy(m, Xte, yte), size_kb(m), n_params(m),
                         latency_us(m, xs)))
        print(f"{name:22s} {measured[-1][1]:9.3f} {measured[-1][2]:9.1f} "
              f"{measured[-1][3]:9d} {measured[-1][4]:12.1f}")

    # Reuse the exact timings shown in the table; re-timing only the baselines made
    # the printed ratios disagree with the printed table on a noisy CPU.
    _, t_acc, t_kb, _, t_us = measured[0]
    _, s_acc, _, _, _ = measured[1]
    _, d_acc, d_kb, _, d_us = measured[2]
    _, q_acc, q_kb, _, q_us = measured[3]
    _, p_acc, p_kb, _, p_us = measured[4]

    print()
    print(f"  distillation gain over scratch: {d_acc - s_acc:+.3f}")
    print(f"  student vs teacher: accuracy {d_acc - t_acc:+.3f}, "
          f"size {d_kb / t_kb:.1%} of teacher, latency {d_us / t_us:.2f}x")
    print(f"  int8 vs distilled: accuracy {q_acc - d_acc:+.3f}, size {q_kb / d_kb:.1%}, "
          f"latency {q_us / d_us:.2f}x")

    with torch.no_grad():
        zeros = sum(int((m.weight == 0).sum()) for m in pruned.net if isinstance(m, nn.Linear))
        total_w = sum(m.weight.numel() for m in pruned.net if isinstance(m, nn.Linear))
    print()
    print(f"  pruning sparsity: {zeros / total_w:.1%} of weights are exactly zero")
    print(f"  pruning changed size to {p_kb:.1f} KB and latency to {p_us / d_us:.2f}x:")
    print("  zeros are still multiplied unless a sparse kernel or format is used, so")
    print("  pruning alone buys nothing at inference time.")

    print()
    print("=" * 84)
    print("2. Distillation sweep")
    print("=" * 84)
    print(f"{'temperature':>12} {'alpha':>7} {'accuracy':>10}")
    for T in (1.0, 2.0, 4.0, 8.0):
        for alpha in (0.3, 0.7):
            m = train(Net([64, 64, 10]), Xtr, ytr, epochs=30,
                      teacher=teacher, T=T, alpha=alpha, seed=1)
            print(f"{T:12.1f} {alpha:7.1f} {accuracy(m, Xte, yte):10.3f}")
    print("  alpha is the weight on the hard label; 1-alpha on the teacher's soft scores.")

    print()
    print("=" * 84)
    print("3. Per-class effect of int8")
    print("=" * 84)
    with torch.no_grad():
        a = distilled(torch.tensor(Xte)).argmax(1).numpy()
        b = q8(torch.tensor(Xte)).argmax(1).numpy()
    for c in range(10):
        mask = yte == c
        ca, cb = (a[mask] == c).mean(), (b[mask] == c).mean()
        print(f"  digit {c}: float {ca:.3f}  int8 {cb:.3f}  change {cb - ca:+.3f}")

    deltas = [(b[yte == c] == c).mean() - (a[yte == c] == c).mean() for c in range(10)]
    worst = max(deltas, key=abs)
    print()
    print(f"  largest per-class change: {worst:+.3f} (class {deltas.index(worst)})")
    if abs(worst) < 0.005:
        print("  int8 changed no class measurably: this network is heavily redundant, so")
        print("  8-bit weights cost nothing here. That is a property of this model, not a")
        print("  guarantee. Report per-class numbers anyway; that is how you find out.")
    else:
        print("  classes with the closest boundaries lose most, which is why the per-class")
        print("  table belongs in the report.")
    print(f"  int8 latency was {q_us / d_us:.2f}x float: dequantising weights on every")
    print("  forward pass costs time, so a smaller model is not automatically faster.")


if __name__ == "__main__":
    main()
