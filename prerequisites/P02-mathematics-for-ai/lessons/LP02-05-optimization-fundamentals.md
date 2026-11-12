# LP02-05 — Optimisation Fundamentals

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 150 minutes |
| Prerequisites | [LP02-04](LP02-04-derivatives-partial-derivatives-and-gradients.md) |
| Notebook | [NB-P02-02](../notebooks/nb-p02-02-calculus-and-optimization.ipynb) |
| Lab | [LAB-P02-02](../labs/lab-p02-02-gradient-descent-by-hand.md) |

[← Previous: Gradients](LP02-04-derivatives-partial-derivatives-and-gradients.md) · [P02 home](../README.md) · [Next: Probability and Statistics →](../../P03-probability-and-statistics/README.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **State** the difference between a local and a global minimum, and test convexity with the second
  derivative.
- **Run** gradient descent by hand for two or three steps on a simple function.
- **Predict** what happens with a learning rate that is too small, reasonable, and too large.
- **Explain** why training a neural network is an optimisation problem and why stochastic gradients
  are used.

## 2. Prerequisite Knowledge

- Partial derivatives and gradients: [LP02-04](LP02-04-derivatives-partial-derivatives-and-gradients.md).

## 3. Conceptual Explanation

### 3.1 An optimisation problem has three parts

$$
\min_{\mathbf{x}} \; f(\mathbf{x}) \quad \text{(objective)}, \qquad
\mathbf{x} \in \mathcal{X} \quad \text{(feasible set)}, \qquad
\text{stop when } \|\nabla f\| < \epsilon \ \text{(criterion)}
$$

In machine learning, $f$ is the loss, $\mathbf{x}$ collects the parameters (weights and biases), and
$\mathcal{X}$ is usually all of $\mathbb{R}^d$ — constraints appear as regularisation terms instead.

### 3.2 Local versus global minima

A **global** minimum is the smallest value anywhere; a **local** minimum is smaller than everything
nearby. For a smooth one-dimensional function:

- $f'(x^\ast) = 0$ and $f''(x^\ast) > 0$ → local minimum.
- $f'(x^\ast) = 0$ and $f''(x^\ast) < 0$ → local maximum.
- $f'(x^\ast) = 0$ and $f''(x^\ast) = 0$ → inconclusive; higher-order terms decide (e.g. $x^3$ at 0 is
  a saddle, $x^4$ is a minimum).

A function is **convex** when the straight line between any two points on its graph stays above the
graph. Convex functions have one basin, so any local minimum is global — which is why linear and
logistic regression are "easy" and deep networks are not.

In several dimensions, the test uses the **Hessian** $H$ of second partial derivatives: all eigenvalues
positive → minimum; all negative → maximum; mixed signs → saddle point.

### 3.3 Gradient descent

$$
\mathbf{x}_{t+1} = \mathbf{x}_t - \eta\,\nabla f(\mathbf{x}_t)
$$

with learning rate $\eta > 0$. Subtract the gradient because it points uphill. Each step moves
downhill in proportion to the slope.

Behaviour depends almost entirely on $\eta$:

- **Too small:** correct direction, painfully slow — many steps to arrive.
- **About right:** monotone decrease, convergence in a reasonable number of steps.
- **Too large:** overshoot, oscillation, then divergence — the loss grows without bound.

For a quadratic with curvature $L$ (the second derivative), gradient descent converges when
$\eta < 2/L$. That single inequality explains both the safe range and the failure mode.

### 3.4 Stochastic gradient descent

Computing the exact gradient over a million examples is wasteful when a sample of 32 already points
in roughly the right direction. SGD replaces $\nabla f$ by an estimate from a **mini-batch**, trading
a noisier direction for far more updates per second. The noise even helps: it can push the parameters
out of poor regions.

**Momentum** adds a running average of past gradients so that consistent directions accumulate speed,
and Adam adapts a per-parameter step size. All of them are variations on the same update above; knowing
the base case is what makes the variants readable.

## 4. Worked Examples

### Example 1 — three steps by hand

Minimise $f(x) = x^2$ from $x_0 = 4$ with $\eta = 0.25$. Since $f'(x) = 2x$:

| Step | $x_t$ | $f'(x_t) = 2x_t$ | update | $x_{t+1}$ | $f(x_{t+1})$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | 4 | 8 | $4 - 0.25\cdot8$ | 2 | 4 |
| 1 | 2 | 4 | $2 - 0.25\cdot4$ | 1 | 1 |
| 2 | 1 | 2 | $1 - 0.25\cdot2$ | 0.5 | 0.25 |
| 3 | 0.5 | 1 | $0.5 - 0.25\cdot1$ | 0.25 | 0.0625 |

Each step halves $x$, so the distance to the minimum halves too. This is convergence at a fixed rate:
linear convergence, meaning the error is multiplied by a constant each step.

### Example 2 — the same function, learning rate too large

With $\eta = 1.5$: $x_0 = 4$, gradient 8 → $x_1 = 4 - 12 = -8$ (loss 64). Gradient $-16$ →
$x_2 = -8 + 24 = 16$ (loss 256). Each step doubles the distance from zero. The safe bound here is
$\eta < 2/L = 2/2 = 1$; 1.5 exceeds it, so the iterates diverge.

```python
def descend(f_prime, x0, lr, steps=4):
    x, path = x0, [x0]
    for _ in range(steps):
        x = x - lr * f_prime(x)
        path.append(x)
    return path

print(descend(lambda x: 2 * x, 4.0, 0.25))
print(descend(lambda x: 2 * x, 4.0, 1.5))
```

```text
[4.0, 2.0, 1.0, 0.5, 0.25]
[4.0, -8.0, 16.0, -32.0, 64.0]
```

Same code, same function, one number changed — and the outcome flips from convergence to explosion.

### Example 3 — different curvature per direction

For $f(x, y) = x^2 + 3y^2$, $\nabla f = (2x, 6y)$. From $(2, 1)$ with $\eta = 0.1$:

$$
(x_1, y_1) = (2 - 0.1\cdot4,\; 1 - 0.1\cdot6) = (1.6,\; 0.4)
$$

$f(2,1) = 7$ and $f(1.6, 0.4) = 2.56 + 0.48 = 3.04$. The $y$ direction has three times the curvature,
so with one shared learning rate it converges faster — and if it were steeper still, it would be the
direction that limits the step size. This imbalance is exactly what "poor conditioning" means, and
why normalising features helps optimisers.

## 5. Visual Explanation

```text
   f(x)
    │╲                    ╱
    │ ╲                  ╱
    │  ╲    ________    ╱
    │   ╲__╱        ╲__╱
    │      local min (non-convex)
    └────────────────────────── x

   convex: one basin        non-convex: several basins, saddle points between
```

*Text description of the diagram:* the upper curve has a single bowl — any downhill walk reaches the
bottom, whatever the starting point. The lower curve has two bowls and a bump between them; where you
start decides which bottom you reach, and the bump is a local maximum separating the basins. Gradient
descent cannot cross a barrier, which is the honest limitation of the method.

## 6. Mathematical Formulation

$$
\mathbf{x}_{t+1} = \mathbf{x}_t - \eta \nabla f(\mathbf{x}_t),
\qquad
\text{converges for } 0 < \eta < \frac{2}{L}
\quad \left(L = \lambda_{\max}(H)\right)
$$

For a quadratic $f(\mathbf{x}) = \frac{1}{2}\mathbf{x}^\top A\mathbf{x} - \mathbf{b}^\top\mathbf{x}$
with symmetric positive-definite $A$, gradient descent converges at a rate governed by the
**condition number** $\kappa = \lambda_{\max}/\lambda_{\min}$:

$$
\|\mathbf{x}_t - \mathbf{x}^\ast\| \le \left(1 - \frac{1}{\kappa}\right)^{t}\|\mathbf{x}_0 - \mathbf{x}^\ast\|
$$

Large $\kappa$ (a long, narrow valley) means slow convergence — the quantitative version of the
intuition in Example 3.

## 7. Python Implementation

```python
"""Gradient descent on a 2-D quadratic, with a convergence log."""
import numpy as np


def f(x):
    return x[0] ** 2 + 3 * x[1] ** 2


def grad_f(x):
    return np.array([2 * x[0], 6 * x[1]])


def gradient_descent(x0, lr, steps=20, tol=1e-6):
    x = np.array(x0, dtype=float)
    history = [float(f(x))]
    for _ in range(steps):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        x = x - lr * g
        history.append(float(f(x)))
    return x, history


for lr in (0.01, 0.1, 0.5):
    x_star, hist = gradient_descent([2.0, 1.0], lr=lr, steps=20)
    print(f"lr={lr:<5} final={x_star.round(4)} loss={hist[-1]:.2e} steps={len(hist) - 1}")
```

**Output**

```text
lr=0.01  final=[1.3352 0.2901] loss=2.04e+00 steps=20
lr=0.1   final=[0.0231 0.    ] loss=5.32e-04 steps=20
lr=0.5   final=[      0. 1048576.] loss=3.30e+12 steps=20
```

Read the three rows as the learning-rate spectrum. With $L = 6$ (the curvature in the steep $y$
direction), convergence needs $\eta < 2/6 \approx 0.333$, so 0.01 is safe but slow — still far from
the minimum after 20 steps — 0.1 has essentially arrived, and 0.5 violates the bound and blows up:
the $x$ coordinate is fine because $6 \times 0.5 = 3$ reverses and enlarges $y$ every step. One
learning rate, two very different directions; that is why the reported loss, not a single coordinate,
is what you watch.

## 8. Practical Applications

- **Model training.** Every epoch of every network is this loop with a gradient computed by
  backpropagation; the loss curve you watch is the `history` list above.
- **Hyperparameter search.** Choosing the learning rate, batch size and number of steps is choosing
  $\eta$, the gradient estimator, and the stopping rule.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Learning rate too high | Loss oscillates or becomes `nan` | Step exceeds the basin | Reduce by 10× and retry |
| Learning rate too low | Loss barely moves | Steps too small | Increase, or normalise features |
| Unscaled features | One direction dominates | Poor conditioning | Standardise inputs |
| Assuming a global minimum | Training stuck at a poor loss | Non-convex objective | Restart, or accept local optima |
| Stopping by step count only | Unnecessary compute | No tolerance check | Stop when gradient norm is small |

## 10. Self-Assessment

**1.** $f(x) = (x - 3)^2$. Starting at $x_0 = 0$ with $\eta = 0.1$, compute $x_1$ and $x_2$.
<details><summary>Show answer</summary>

$f'(x) = 2(x-3)$. At $x_0 = 0$, gradient is $-6$, so $x_1 = 0 + 0.6 = 0.6$. Gradient there is
$-4.8$, so $x_2 = 0.6 + 0.48 = 1.08$. The iterates approach 3 from below.
</details>

**2.** Why is a convex objective desirable, and which classical models have one?
<details><summary>Show answer</summary>

Because every local minimum is global, so any convergent method finds the best parameters — no restarts
needed. Linear regression (squared loss) and logistic regression (log loss) are convex in their
parameters; neural networks are not.
</details>

**3.** What does a Hessian with eigenvalues $(-2, 5)$ tell you about the critical point?
<details><summary>Show answer</summary>

Mixed signs mean a **saddle point**: the function curves upward along one eigenvector and downward
along the other. Gradient descent can slow dramatically near saddles, which is one reason momentum and
noise help.
</details>

**4.** Why does mini-batch gradient descent usually beat full-batch on large datasets, even though its
gradient estimate is noisier?
<details><summary>Show answer</summary>

Because progress per unit of computation matters more than per-step accuracy: many cheap, slightly
wrong steps reach a good region faster than few expensive exact ones. The noise also helps escape
shallow saddle regions.
</details>

## 11. Further Reading

- [Mathematics for Machine Learning, Ch. 7](https://mml-book.github.io/) — convex optimisation and gradient methods, in full.
- [Why Momentum Really Works (Distill)](https://distill.pub/2017/momentum/) — an interactive explanation of momentum and conditioning.

## Mini-Lab

Implement gradient descent for $f(x_1, x_2) = (x_1 - 1)^2 + 10(x_2 - 2)^2$, starting at $(0, 0)$.
Run with $\eta \in \{0.01, 0.05, 0.11\}$ for 50 steps, and plot all three loss curves on one set of
axes with a legend. Which value diverges, and does it match the bound $\eta < 2/L$? Then standardise
the problem by rescaling $x_2$ so both curvatures match, and compare the number of steps needed.

## What to Do Next

P02 is complete. Continue to [P03 Probability and Statistics](../../P03-probability-and-statistics/README.md),
which turns the deterministic world of this unit into one with uncertainty.
