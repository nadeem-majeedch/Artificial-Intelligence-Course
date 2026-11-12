"""A multilayer perceptron from scratch in NumPy: forward pass, backprop, optimisers.

Nothing here imports a deep-learning framework. The purpose is to make every gradient
explicit, so that when PyTorch computes it for you later the shapes and the chain rule
are already familiar.

Run `python nn_numpy.py` for the XOR, perceptron, digits and gradient-check demos.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "sigmoid", "tanh", "relu", "leaky_relu", "softmax", "step",
    "MLP", "SGD", "Momentum", "RMSProp", "Adam",
    "perceptron_rule", "gradient_check", "accuracy",
]


# ---------------------------------------------------------------------------
# Activations
# ---------------------------------------------------------------------------
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


def tanh(z):
    return np.tanh(z)


def relu(z):
    return np.maximum(0.0, z)


def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)


def step(z):
    """The original perceptron's hard threshold."""
    return (z > 0).astype(float)


def softmax(z):
    shifted = z - z.max(axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=1, keepdims=True)


ACTIVATIONS = {
    "sigmoid": (sigmoid, lambda z, a: a * (1 - a)),
    "tanh": (tanh, lambda z, a: 1 - a**2),
    "relu": (relu, lambda z, a: (z > 0).astype(float)),
    "leaky_relu": (leaky_relu, lambda z, a: np.where(z > 0, 1.0, 0.01)),
    "step": (step, lambda z, a: np.zeros_like(z)),  # not differentiable; demo only
}


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
class MLP:
    """Fully connected network trained by backpropagation.

    Parameters
    ----------
    sizes : list[int]
        Layer widths, e.g. [64, 32, 10] means 64 inputs, one hidden layer of 32,
        10 outputs.
    activation : {"relu", "tanh", "sigmoid", "leaky_relu"}
        Hidden activation. tanh is the right choice for tiny problems such as XOR;
        relu is the default for anything with more than a handful of units.
    init : {"he", "xavier"}
        He scaling for relu, Xavier for tanh/sigmoid.
    """

    def __init__(self, sizes, activation="relu", init=None, seed=0):
        if len(sizes) < 2:
            raise ValueError("need at least input and output layers")
        self.sizes = list(sizes)
        self.activation_name = activation
        self.act, self.act_grad = ACTIVATIONS[activation]
        self.rng = np.random.default_rng(seed)

        if init is None:
            init = "he" if activation in {"relu", "leaky_relu"} else "xavier"
        self.W, self.b = [], []
        for fan_in, fan_out in zip(self.sizes[:-1], self.sizes[1:]):
            scale = np.sqrt(2.0 / fan_in) if init == "he" else np.sqrt(1.0 / fan_in)
            self.W.append(self.rng.normal(0.0, scale, (fan_in, fan_out)))
            self.b.append(np.zeros(fan_out))

    # -- forward ---------------------------------------------------------
    def forward(self, X, dropout=0.0, training=False):
        """Return (probabilities, cache). Cache holds what backward needs."""
        cache = {"A": [X], "Z": [], "masks": []}
        A = X
        last = len(self.W) - 1
        for layer, (W, b) in enumerate(zip(self.W, self.b)):
            Z = A @ W + b
            if layer == last:
                A_out = softmax(Z)
            else:
                A_out = self.act(Z)
                if dropout > 0.0 and training:
                    # Inverted dropout: scale survivors so the expected activation is
                    # unchanged, which means no scaling is needed at inference.
                    mask = (self.rng.random(A_out.shape) >= dropout) / (1.0 - dropout)
                    A_out = A_out * mask
                    cache["masks"].append(mask)
                else:
                    cache["masks"].append(None)
            cache["Z"].append(Z)
            cache["A"].append(A_out)
            A = A_out
        return A, cache

    # -- loss and backward ----------------------------------------------
    def loss(self, probs, y):
        """Mean cross-entropy. y is an integer class vector."""
        n = len(y)
        correct = probs[np.arange(n), y]
        return float(-np.mean(np.log(np.clip(correct, 1e-12, 1.0))))

    def backward(self, cache, y):
        """Return (grad_W, grad_b). This is the chain rule, layer by layer."""
        n = len(y)
        grads_W = [None] * len(self.W)
        grads_b = [None] * len(self.b)

        # dL/dlogits for softmax + cross-entropy simplifies to (p - onehot)/n.
        dZ = cache["A"][-1].copy()
        dZ[np.arange(n), y] -= 1.0
        dZ /= n

        for layer in range(len(self.W) - 1, -1, -1):
            A_prev = cache["A"][layer]
            grads_W[layer] = A_prev.T @ dZ
            grads_b[layer] = dZ.sum(axis=0)
            if layer > 0:
                dA = dZ @ self.W[layer].T
                mask = cache["masks"][layer - 1]
                if mask is not None:
                    dA = dA * mask
                dZ = dA * self.act_grad(cache["Z"][layer - 1], cache["A"][layer])
        return grads_W, grads_b

    # -- inference -------------------------------------------------------
    def predict_proba(self, X):
        probs, _ = self.forward(X)
        return probs

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == y))


def accuracy(y_true, y_pred) -> float:
    return float(np.mean(np.asarray(y_true) == np.asarray(y_pred)))


# ---------------------------------------------------------------------------
# Optimisers
# ---------------------------------------------------------------------------
class SGD:
    """w <- w - lr * grad."""

    name = "sgd"

    def __init__(self, lr=0.1):
        self.lr = lr

    def step(self, params, grads):
        for p, g in zip(params, grads):
            p -= self.lr * g


class Momentum:
    """Accumulate an exponentially weighted average of past gradients.

    v <- beta*v + g;  w <- w - lr*v. Damps oscillation in ravines and speeds up
    progress along consistent directions.
    """

    name = "momentum"

    def __init__(self, lr=0.05, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.v = None

    def step(self, params, grads):
        if self.v is None:
            self.v = [np.zeros_like(p) for p in params]
        for i, (p, g) in enumerate(zip(params, grads)):
            self.v[i] = self.beta * self.v[i] + g
            p -= self.lr * self.v[i]


class RMSProp:
    """Scale each parameter's step by its recent gradient magnitude.

    s <- beta*s + (1-beta)*g^2;  w <- w - lr*g / (sqrt(s) + eps).
    """

    name = "rmsprop"

    def __init__(self, lr=0.01, beta=0.9, eps=1e-8):
        self.lr = lr
        self.beta = beta
        self.eps = eps
        self.s = None

    def step(self, params, grads):
        if self.s is None:
            self.s = [np.zeros_like(p) for p in params]
        for i, (p, g) in enumerate(zip(params, grads)):
            self.s[i] = self.beta * self.s[i] + (1 - self.beta) * g**2
            p -= self.lr * g / (np.sqrt(self.s[i]) + self.eps)


class Adam:
    """Momentum plus RMSProp, with bias correction.

    m and v are biased toward zero early in training; dividing by (1 - beta^t)
    corrects that, which is why Adam works with the default lr = 1e-3.
    """

    name = "adam"

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        self.t += 1
        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g**2
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------
def train(model, X, y, epochs=50, batch_size=64, optimizer=None, dropout=0.0,
          weight_decay=0.0, seed=0, verbose=False):
    """Mini-batch training. Returns a history dict with loss and accuracy per epoch."""
    rng = np.random.default_rng(seed)
    optimizer = optimizer if optimizer is not None else SGD(0.1)
    history = {"loss": [], "accuracy": []}
    n = len(X)

    for epoch in range(1, epochs + 1):
        order = rng.permutation(n)
        epoch_loss = 0.0
        batches = 0
        for start in range(0, n, batch_size):
            idx = order[start:start + batch_size]
            Xb, yb = X[idx], y[idx]
            probs, cache = model.forward(Xb, dropout=dropout, training=True)
            epoch_loss += model.loss(probs, yb)
            batches += 1
            grads_W, grads_b = model.backward(cache, yb)
            if weight_decay:
                grads_W = [g + weight_decay * w for g, w in zip(grads_W, model.W)]
            params = model.W + model.b
            grads = grads_W + grads_b
            optimizer.step(params, grads)

        history["loss"].append(epoch_loss / max(batches, 1))
        history["accuracy"].append(model.score(X, y))
        if verbose and (epoch % max(epochs // 5, 1) == 0 or epoch == 1):
            print(f"epoch {epoch:4d} loss {history['loss'][-1]:.4f} acc {history['accuracy'][-1]:.3f}")
    return history


# ---------------------------------------------------------------------------
# Perceptron learning rule (the historical algorithm)
# ---------------------------------------------------------------------------
def perceptron_rule(X, y, epochs=20, lr=1.0):
    """Rosenblatt's perceptron: w <- w + lr*(y - step(w.x))*x, with labels 0/1.

    Returns (w, b, errors_per_epoch). It converges if and only if the data are
    linearly separable — which XOR is not, so the error count never reaches zero.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float).ravel()
    w = np.zeros(X.shape[1])
    b = 0.0
    errors = []
    for _ in range(epochs):
        wrong = 0
        for xi, yi in zip(X, y):
            pred = 1.0 if xi @ w + b > 0 else 0.0
            update = lr * (yi - pred)
            w += update * xi
            b += update
            wrong += int(pred != yi)
        errors.append(wrong)
    return w, b, errors


# ---------------------------------------------------------------------------
# Numerical gradient check
# ---------------------------------------------------------------------------
def gradient_check(model, X, y, epsilon=1e-6, seed=0):
    """Compare analytic and finite-difference gradients for one batch.

    Returns the maximum relative error. Below ~1e-6 is a correct implementation;
    a value near 1e-2 means the backward pass and the forward pass disagree.
    """
    rng = np.random.default_rng(seed)
    probs, cache = model.forward(X, dropout=0.0, training=False)
    grads_W, grads_b = model.backward(cache, y)

    worst = 0.0
    for layer in range(len(model.W)):
        for _ in range(min(8, model.W[layer].size)):
            i = int(rng.integers(model.W[layer].shape[0]))
            j = int(rng.integers(model.W[layer].shape[1]))
            original = model.W[layer][i, j]

            model.W[layer][i, j] = original + epsilon
            plus, _ = model.forward(X)
            loss_plus = model.loss(plus, y)

            model.W[layer][i, j] = original - epsilon
            minus, _ = model.forward(X)
            loss_minus = model.loss(minus, y)

            model.W[layer][i, j] = original
            numeric = (loss_plus - loss_minus) / (2 * epsilon)
            analytic = grads_W[layer][i, j]
            denom = max(abs(numeric) + abs(analytic), 1e-12)
            worst = max(worst, abs(numeric - analytic) / denom)
    return float(worst)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import deep_data as dd

    print("=== perceptron rule on the four gates ===")
    data = {
        "AND": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float), np.array([0, 0, 0, 1])),
        "OR": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float), np.array([0, 1, 1, 1])),
        "XOR": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float), np.array([0, 1, 1, 0])),
    }
    for name, (Xg, yg) in data.items():
        w, b, errors = perceptron_rule(Xg, yg, epochs=20)
        preds = ((Xg @ w + b) > 0).astype(int)
        print(f"{name:4s} errors per epoch: {errors[:6]} ... final acc {np.mean(preds == yg):.2f}")

    print()
    print("=== MLP on XOR ===")
    X, y = dd.xor_data()
    net = MLP([2, 4, 2], activation="tanh", seed=1)
    hist = train(net, X, y.ravel().astype(int), epochs=2000, batch_size=4, optimizer=Adam(0.05), seed=1)
    print("final loss", round(hist["loss"][-1], 5), "accuracy", hist["accuracy"][-1])
    print("probabilities:", np.round(net.predict_proba(X), 3).tolist())

    print()
    print("=== MLP on synthetic digits ===")
    images, labels = dd.digit_images(2000, seed=0)
    Xd = images.reshape(len(images), -1)
    split = 1600
    net = MLP([64, 32, 10], activation="relu", seed=0)
    hist = train(net, Xd[:split], labels[:split], epochs=15, batch_size=64,
                 optimizer=Adam(0.001), seed=0)
    print("train acc", round(net.score(Xd[:split], labels[:split]), 3),
          "test acc", round(net.score(Xd[split:], labels[split:]), 3))
    print("loss first/last:", round(hist["loss"][0], 3), round(hist["loss"][-1], 3))

    print()
    print("gradient check (max relative error):", f"{gradient_check(net, Xd[:32], labels[:32]):.2e}")

    print()
    print("=== optimiser comparison on digits (5 epochs) ===")
    for name, opt in [("sgd", SGD(0.05)), ("momentum", Momentum(0.02)), ("rmsprop", RMSProp(0.001)), ("adam", Adam(0.001))]:
        m = MLP([64, 32, 10], seed=2)
        h = train(m, Xd[:split], labels[:split], epochs=5, batch_size=64, optimizer=opt, seed=2)
        print(f"{name:9s} loss {h['loss'][-1]:.3f} train acc {h['accuracy'][-1]:.3f}")
