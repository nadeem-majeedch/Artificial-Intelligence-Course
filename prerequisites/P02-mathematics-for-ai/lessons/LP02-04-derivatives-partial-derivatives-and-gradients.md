# LP02-04 — Derivatives, Partial Derivatives and Gradients

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 150 minutes |
| Prerequisites | [LP02-01](LP02-01-scalars-vectors-matrices-and-tensors.md), [LP02-02](LP02-02-matrix-operations-and-multiplication.md) |
| Notebook | [NB-P02-02](../notebooks/nb-p02-02-calculus-and-optimization.ipynb) |
| Lab | [LAB-P02-02](../labs/lab-p02-02-gradient-descent-by-hand.md) |

[← Previous: Eigenvalues](LP02-03-transpose-inverse-and-eigenvalues.md) · [P02 home](../README.md) · [Next: Optimisation →](LP02-05-optimization-fundamentals.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Interpret** a derivative as a rate of change and as the slope of a tangent line.
- **Compute** partial derivatives by holding all other variables constant.
- **Assemble** a gradient vector and say which direction increases the function fastest.
- **Apply** the chain rule, including through a two-step composition, and check the result numerically.

## 2. Prerequisite Knowledge

- Functions and plotting basics: [LP01-04](../../P01-python-programming/lessons/LP01-04-functions-and-collections.md).
- Vectors and dot products: [LP02-01](LP02-01-scalars-vectors-matrices-and-tensors.md).

## 3. Conceptual Explanation

### 3.1 The derivative measures sensitivity

$$
f'(x) = \lim_{h \to 0}\frac{f(x+h) - f(x)}{h}
$$

Three readings, all used in machine learning:

- **Geometric:** slope of the tangent to the curve at $x$.
- **Numerical:** how much $f$ changes when $x$ changes a little — "per unit change of $x$".
- **Algorithmic:** the number a training loop multiplies by the learning rate.

The limit matters: the difference quotient with a finite $h$ is an approximation, and as $h$ shrinks
the approximation improves until floating-point cancellation takes over. That trade-off is exactly why
numerical gradient checking uses $h \approx 10^{-5}$, not $10^{-15}$.

### 3.2 Derivatives you should know without thinking

| $f(x)$ | $f'(x)$ |
| :--- | :--- |
| $c$ | $0$ |
| $x^n$ | $n x^{n-1}$ |
| $e^x$ | $e^x$ |
| $\ln x$ | $1/x$ |
| $\sin x$ | $\cos x$ |
| $\sigma(x) = \frac{1}{1+e^{-x}}$ | $\sigma(x)\,(1-\sigma(x))$ |

The last row is worth memorising: the sigmoid's derivative in terms of its own output is what makes
backpropagation through sigmoid units cheap.

### 3.3 Partial derivatives: one variable at a time

For $f(x, y)$, the partial derivative $\partial f/\partial x$ treats $y$ as a **constant** and
differentiates with respect to $x$. It answers: if I nudge $x$ only, how does $f$ respond?

$$
\frac{\partial f}{\partial x}(x_0, y_0) =
\lim_{h\to 0}\frac{f(x_0 + h, y_0) - f(x_0, y_0)}{h}
$$

### 3.4 Gradient: all partials in one vector

$$
\nabla f = \left(\frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n}\right)
$$

The gradient points in the direction of **steepest increase**; its magnitude is the slope in that
direction. Therefore $-\nabla f$ points downhill, which is the single fact that gradient descent is
built on. At a minimum, $\nabla f = \mathbf{0}$.

### 3.5 Chain rule: derivatives along a computation

If $y = f(u)$ and $u = g(x)$, then

$$
\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}
$$

Backpropagation is this rule applied repeatedly, once per layer, with the intermediate derivatives
stored rather than recomputed. When you read "gradients flow backwards", this is the entire mechanism.

## 4. Worked Examples

### Example 1 — derivative at a point

$f(x) = x^2$, so $f'(x) = 2x$ and $f'(3) = 6$. Meaning: near $x = 3$, increasing $x$ by 1 increases
$f$ by about 6. Check numerically:

```python
import numpy as np

f = lambda x: x**2
h = 1e-5
print(round((f(3 + h) - f(3 - h)) / (2 * h), 6))
```

```text
6.0
```

The symmetric difference quotient is accurate to $O(h^2)$, far better than the one-sided version. This
is how you verify any derivative you derive by hand.

### Example 2 — partial derivatives of a two-variable function

$$
g(x, y) = x^2 y + 3y
$$

Holding $y$ constant: $\dfrac{\partial g}{\partial x} = 2xy$.
Holding $x$ constant: $\dfrac{\partial g}{\partial y} = x^2 + 3$.

At $(2, 1)$: $\partial g/\partial x = 4$ and $\partial g/\partial y = 7$, so
$\nabla g = (4, 7)$.

```python
g = lambda x, y: x**2 * y + 3 * y
print(round((g(2 + h, 1) - g(2 - h, 1)) / (2 * h), 4))   # ∂g/∂x = 4
print(round((g(2, 1 + h) - g(2, 1 - h)) / (2 * h), 4))   # ∂g/∂y = 7
```

```text
4.0
7.0
```

### Example 3 — chain rule through a composition

$h(x) = (3x + 1)^2$. Let $u = 3x + 1$, so $h = u^2$:

$$
\frac{dh}{dx} = 2u \cdot 3 = 6(3x+1) = 18x + 6
$$

At $x = 1$: $24$. Expanding first gives $9x^2 + 6x + 1$, whose derivative $18x + 6$ agrees — a useful
cross-check.

### Example 4 — the gradient of a loss function

Mean squared error for a single weight and bias:

$$
L(w, b) = \frac{1}{n}\sum_{i=1}^{n}\left(wx_i + b - y_i\right)^2
$$

$$
\frac{\partial L}{\partial w} = \frac{2}{n}\sum_i x_i\left(wx_i + b - y_i\right),
\qquad
\frac{\partial L}{\partial b} = \frac{2}{n}\sum_i \left(wx_i + b - y_i\right)
$$

With $x = (1, 2)$, $y = (3, 5)$, $w = 1$, $b = 0$: residuals are $-2$ and $-3$, so
$\partial L/\partial w = (2/2)(1(-2) + 2(-3)) = -8$ and $\partial L/\partial b = (2/2)(-5) = -5$.
Both are negative, so **increasing** $w$ and $b$ will decrease the loss — which is what one gradient
step with a positive learning rate does by subtracting a negative number.

## 5. Visual Explanation

```text
  f(x)
   │        ╱ tangent, slope f'(x₀)
   │      ╱
   │    ╱ •  ← (x₀, f(x₀))
   │  ╱
   │╱
   └────────────────── x
          x₀

 contour view of f(x,y):  ∇f ⟂ contour lines, pointing uphill
        ╲   ╱
      ───(•)───   ← ∇f
        ╱   ╲
```

*Text description of the diagram:* the top sketch shows the tangent whose slope is the derivative. The
bottom sketch shows level curves of a two-variable function: the gradient at a point is perpendicular
to the contour through that point and points toward higher values — which is why following $-\nabla f$
moves you across contours toward the minimum.

## 6. Mathematical Formulation

$$
f'(x) = \lim_{h\to0}\frac{f(x+h)-f(x)}{h}, \qquad
\frac{\partial f}{\partial x_i} \approx \frac{f(\mathbf{x} + h\mathbf{e}_i) - f(\mathbf{x} - h\mathbf{e}_i)}{2h}
$$

$$
\nabla_{\mathbf{x}} (\mathbf{a}^\top\mathbf{x}) = \mathbf{a}, \qquad
\nabla_{\mathbf{x}} (\mathbf{x}^\top A\mathbf{x}) = (A + A^\top)\mathbf{x}
$$

The second identity, for symmetric $A$, gives $2A\mathbf{x}$ — the step that turns the normal
equations of least squares into an equation you can solve. It is the matrix analogue of
$\frac{d}{dx}(ax^2) = 2ax$.

For a composition $L = f(g(\mathbf{x}))$ with $\mathbf{u} = g(\mathbf{x})$:

$$
\nabla_{\mathbf{x}} L = J_g^\top \,\nabla_{\mathbf{u}} f
$$

where $J_g$ is the Jacobian of $g$. This vector-Jacobian product is what an autograd engine computes
for every node in the graph.

## 7. Python Implementation

```python
"""Verify analytic gradients numerically — the habit that prevents silent bugs."""
import numpy as np


def numeric_grad(f, x, h=1e-5):
    """Central-difference gradient of a scalar function of a vector."""
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(x.size):
        step = np.zeros_like(x)
        step[i] = h
        grad[i] = (f(x + step) - f(x - step)) / (2 * h)
    return grad


def loss(params, X, y):
    w, b = params
    return float(np.mean((w * X + b - y) ** 2))


X = np.array([1.0, 2.0])
y = np.array([3.0, 5.0])
params = np.array([1.0, 0.0])

resid = params[0] * X + params[1] - y
analytic = np.array([2 * np.mean(X * resid), 2 * np.mean(resid)])
print("analytic:", analytic)                  # [-8. -5.]
print("numeric :", numeric_grad(lambda p: loss(p, X, y), params).round(6))
print("match   :", np.allclose(analytic, numeric_grad(lambda p: loss(p, X, y), params)))
```

**Output**

```text
analytic: [-8. -5.]
numeric : [-8. -5.]
match   : True
```

Twelve lines of checking code have saved more debugging time, across more projects, than any other
twelve lines in this course. Whenever you derive a gradient by hand, run this comparison before
trusting a training run.

## 8. Practical Applications

- **Training any model.** Every optimiser — SGD, Adam, anything — consumes gradients; understanding
  where they come from is what makes learning-rate and convergence behaviour explicable.
- **Sensitivity analysis.** "Which input most affects the output?" is a partial derivative question,
  and the answer is used for feature attribution and for safety analysis.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Treating other variables as constants incorrectly | Wrong gradient, training stalls | Forgetting the product rule | Differentiate term by term |
| Sign error in $-\nabla f$ | Loss increases each step | Ascending instead of descending | Subtract the gradient |
| $h$ too small in numeric check | Garbage values | Floating-point cancellation | Use $h \approx 10^{-5}$ |
| Forgetting the factor 2 in MSE | Gradients off by 2× | Derivative of a square | Or use $\frac{1}{2n}$ so it cancels |

## 10. Self-Assessment

**1.** $f(x) = 3x^2 - 4x + 1$. Find $f'(2)$.
<details><summary>Show answer</summary>

$f'(x) = 6x - 4$, so $f'(2) = 8$. The function is increasing at $x = 2$ at a rate of 8 per unit.
</details>

**2.** $f(x, y, z) = x y + y z$. Write $\nabla f$.
<details><summary>Show answer</summary>

$\partial f/\partial x = y$, $\partial f/\partial y = x + z$, $\partial f/\partial z = y$, so
$\nabla f = (y,\ x+z,\ y)$.
</details>

**3.** Why does the gradient point uphill rather than downhill?
<details><summary>Show answer</summary>

Because each component is the rate of increase in that coordinate direction, and the vector combining
them is the direction in which a small step increases $f$ fastest. Moving opposite to it decreases $f$
fastest — hence gradient *descent* uses $-\nabla f$.
</details>

**4.** $h(x) = \sigma(2x + 3)$ where $\sigma$ is the sigmoid. Write $h'(x)$.
<details><summary>Show answer</summary>

By the chain rule, $h'(x) = 2\,\sigma(2x+3)\,(1 - \sigma(2x+3))$ — the inner derivative 2 times the
sigmoid derivative expressed through its output.
</details>

## 11. Further Reading

- [Khan Academy: Multivariable calculus](https://www.khanacademy.org/math/multivariable-calculus) — gradients, partial derivatives and the chain rule, visually.
- [Mathematics for Machine Learning, Ch. 5](https://mml-book.github.io/) — the vector-calculus chapter this lesson compresses.

## Mini-Lab

Pick $f(x, y) = x^2 + 3y^2 - 2xy$. Derive both partials by hand, then verify them numerically at
$(1, 2)$ with central differences. Confirm that at the point where both partials vanish — solve the
two equations — the function has its minimum, and state the value of $f$ there.

## What to Do Next

Continue to [LP02-05 Optimisation Fundamentals](LP02-05-optimization-fundamentals.md), where gradients
become an algorithm.
