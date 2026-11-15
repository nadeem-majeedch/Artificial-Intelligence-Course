"""LAB-14-02 starter — serving cost, measured rather than asserted.

This measures the two things the lab asks you to defend: latency versus batch size, and
the accuracy/size trade-off of int8 quantisation, on a matrix-multiply "model" that
needs only numpy.

What is missing (your work)
---------------------------
1. Add p50/p95 latency over repeated trials, not a single timing.
2. Quantise the weights (``quantise``) and report the error it introduces.
3. Compute the throughput ceiling and say which component sets it.

Run:  python lab-14-02_starter.py
"""

import time

import numpy as np


class TinyModel:
    """A two-layer matrix model: y = relu(x W1) W2."""

    def __init__(self, d_in=256, hidden=128, d_out=10, seed=0):
        rng = np.random.default_rng(seed)
        self.w1 = rng.normal(scale=0.05, size=(d_in, hidden)).astype(np.float32)
        self.w2 = rng.normal(scale=0.05, size=(hidden, d_out)).astype(np.float32)

    def __call__(self, x):
        return np.maximum(x @ self.w1, 0.0) @ self.w2

    def nbytes(self):
        return self.w1.nbytes + self.w2.nbytes


def quantise(weights, scale=None):
    """Symmetric int8 quantisation: returns (int8 weights, scale)."""
    scale = scale or float(np.abs(weights).max() / 127.0)
    return np.clip(np.round(weights / scale), -127, 127).astype(np.int8), scale


def dequantise(quantised, scale):
    return quantised.astype(np.float32) * scale


def timeit(fn, repeats=30):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        times.append(time.perf_counter() - start)
    return np.percentile(times, 50), np.percentile(times, 95)


def main():
    model = TinyModel()
    print(f"parameters: {model.nbytes() / 1024:.1f} KiB")
    for batch in (1, 8, 32, 128):
        x = np.random.default_rng(0).normal(size=(batch, 256)).astype(np.float32)
        p50, p95 = timeit(lambda: model(x))
        print(f"batch {batch:>3}: p50 {p50 * 1e3:6.2f} ms  p95 {p95 * 1e3:6.2f} ms  "
              f"{batch / p50:8.0f} examples/s")

    x = np.random.default_rng(1).normal(size=(64, 256)).astype(np.float32)
    reference = model(x)
    q1, s1 = quantise(model.w1)
    q2, s2 = quantise(model.w2)
    approx = np.maximum(x @ dequantise(q1, s1), 0.0) @ dequantise(q2, s2)
    print(f"int8 relative error: {np.abs(approx - reference).max() / np.abs(reference).max():.3%}")

    # TODO: add p50/p95 for the quantised path, then write the one-paragraph
    # deployment recommendation the lab asks for, including the rollback trigger.


if __name__ == "__main__":
    main()
