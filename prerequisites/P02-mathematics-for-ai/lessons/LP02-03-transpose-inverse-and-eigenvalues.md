# LP02-03 — Transpose, Inverse and Eigenvalues

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 120 minutes |
| Prerequisites | [LP02-02](LP02-02-matrix-operations-and-multiplication.md) |
| Notebook | [NB-P02-01](../notebooks/nb-p02-01-linear-algebra.ipynb) |
| Lab | [LAB-P02-01](../labs/lab-p02-01-image-as-a-matrix.md) |

[← Previous: Matrix Multiplication](LP02-02-matrix-operations-and-multiplication.md) · [P02 home](../README.md) · [Next: Derivatives and Gradients →](LP02-04-derivatives-partial-derivatives-and-gradients.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Transpose** a matrix and apply the reversal rule $(AB)^\top = B^\top A^\top$.
- **Compute** a 2×2 inverse from the determinant, and recognise when no inverse exists.
- **Find** eigenvalues and eigenvectors of a small matrix by solving
  $\det(A - \lambda I) = 0$.
- **Explain** why eigenvalues describe the "stretch directions" of a transformation, and where that
  matters in PCA and optimisation.

## 2. Prerequisite Knowledge

- Matrix multiplication and the identity matrix: [LP02-02](LP02-02-matrix-operations-and-multiplication.md).
- Solving quadratics.

## 3. Conceptual Explanation

### 3.1 Transpose: rows become columns

$(A^\top)_{ij} = a_{ji}$. For $A \in \mathbb{R}^{m\times n}$, $A^\top \in \mathbb{R}^{n\times m}$.

Three rules cover almost every use:

$$
(A^\top)^\top = A, \qquad (A + B)^\top = A^\top + B^\top, \qquad (AB)^\top = B^\top A^\top
$$

The reversal in the last rule is not a typo — it is forced by the shapes: $AB$ is $m\times n$, so its
transpose is $n\times m$, which only $B^\top A^\top$ can produce. A matrix with $A^\top = A$ is
**symmetric**; covariance and correlation matrices are, which is why they have real eigenvalues.

### 3.2 Inverse: undo the transformation

$A^{-1}$ is the matrix satisfying $AA^{-1} = A^{-1}A = I$. It exists only for **square** matrices with
non-zero determinant. For 2×2:

$$
A = \begin{bmatrix}a&b\\c&d\end{bmatrix}, \qquad
\det A = ad - bc, \qquad
A^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}
$$

If $\det A = 0$ the matrix is **singular**: it collapses some direction to zero, and that information
cannot be recovered. In that case one uses the **pseudo-inverse** $A^{+} = (A^\top A)^{-1}A^\top$,
which gives the least-squares solution instead of an exact one.

### 3.3 Eigenvectors: directions the map only stretches

An eigenvector $\mathbf{v} \ne \mathbf{0}$ and eigenvalue $\lambda$ satisfy

$$
A\mathbf{v} = \lambda\mathbf{v}
$$

Most vectors change direction when multiplied by $A$. An eigenvector is special: $A$ only scales it, by
$\lambda$. If $\lambda > 0$ it keeps pointing the same way; $\lambda < 0$ flips it; $\lambda = 0$ means
that direction is destroyed (the matrix is singular).

To find them, rewrite as $(A - \lambda I)\mathbf{v} = \mathbf{0}$. A non-zero $\mathbf{v}$ exists only
if $A - \lambda I$ is singular, i.e.

$$
\det(A - \lambda I) = 0
$$

Two checks that catch most arithmetic slips: $\sum \lambda_i = \operatorname{trace}(A)$ and
$\prod \lambda_i = \det A$.

### 3.4 Why AI cares

- **PCA** finds the eigenvectors of the covariance matrix: the directions of greatest variance. The
  eigenvalues are the variances along them.
- **Optimisation** analyses the Hessian's eigenvalues: all positive means a minimum, mixed signs mean
  a saddle point, and the ratio of largest to smallest controls how badly gradient descent zig-zags.

## 4. Worked Examples

### Example 1 — inverse by the formula, verified

$$
A = \begin{bmatrix}4&7\\2&6\end{bmatrix}, \quad \det A = 24 - 14 = 10, \quad
A^{-1} = \frac{1}{10}\begin{bmatrix}6&-7\\-2&4\end{bmatrix}
= \begin{bmatrix}0.6&-0.7\\-0.2&0.4\end{bmatrix}
$$

```python
import numpy as np

A = np.array([[4.0, 7.0], [2.0, 6.0]])
inv = np.linalg.inv(A)
print(inv.round(1))
print((A @ inv).round(10))
```

```text
[[ 0.6 -0.7]
 [-0.2  0.4]]
[[1. 0.]
 [0. 1.]]
```

The second print is the definition being satisfied: the product is the identity to numerical
precision. Always verify an inverse this way; it takes one line and catches sign errors.

### Example 2 — a singular matrix

```python
S = np.array([[1.0, 2.0], [2.0, 4.0]])
print(round(np.linalg.det(S), 10))
try:
    np.linalg.inv(S)
except np.linalg.LinAlgError as err:
    print("singular:", err)
```

```text
0.0
singular: Singular matrix
```

Row 2 is exactly twice row 1, so the two rows carry the same information and the matrix maps a
2-D plane onto a line. No inverse can send a line back to a plane.

### Example 3 — eigenvalues of a symmetric matrix

$$
A = \begin{bmatrix}2&1\\1&2\end{bmatrix}
$$

Characteristic equation:

$$
\det\begin{bmatrix}2-\lambda & 1\\ 1 & 2-\lambda\end{bmatrix}
= (2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0
\;\Rightarrow\; \lambda = 3,\ 1
$$

For $\lambda = 3$: $(A - 3I)\mathbf{v} = \begin{bmatrix}-1&1\\1&-1\end{bmatrix}\mathbf{v} = 0$, so
$v_1 = v_2$ and $\mathbf{v}_1 = (1,1)/\sqrt{2}$.
For $\lambda = 1$: $\begin{bmatrix}1&1\\1&1\end{bmatrix}\mathbf{v} = 0$, so $\mathbf{v}_2 = (1,-1)/\sqrt{2}$.

```python
vals, vecs = np.linalg.eigh(A)          # eigh for symmetric matrices
print(vals.round(6))
print(vecs.round(3))
print("check:", (A @ vecs[:, 1]).round(3))   # equals 1 * vecs[:, 1]
```

```text
[1. 3.]
[[-0.707  0.707]
 [ 0.707  0.707]]
check: [2.121 2.121]
```

Checks: trace $= 4 = 3 + 1$ ✓, determinant $= 3 = 3 \times 1$ ✓. The eigenvectors are perpendicular —
the defining property of a symmetric matrix, and the reason PCA components are uncorrelated.

## 5. Visual Explanation

```text
          v₂ = (1,-1)/√2                v₁ = (1,1)/√2
               ↑                            ↗
               │  A v₂ = 1 · v₂             │  A v₁ = 3 · v₁
               │                            │
    ───────────●───────────────────────────▶
               │                            x
```

*Text description of the diagram:* the two eigenvectors sit at right angles through the origin. A map
along $\mathbf{v}_1$ is stretched threefold; along $\mathbf{v}_2$ it is unchanged. Every other
direction is a mixture of the two, so it both stretches and rotates — which is why only these special
directions have a single scaling number attached.

## 6. Mathematical Formulation

$$
\det(A - \lambda I) = 0, \qquad
A = Q\Lambda Q^{-1} \text{ (diagonalisable case)}, \qquad
A = Q\Lambda Q^\top \text{ (symmetric case)}
$$

The **eigendecomposition** says that in the basis of its eigenvectors, $A$ is just a diagonal scaling.
That is the entire content of PCA: choose a basis in which the covariance matrix is diagonal, and the
data's dimensions become independent.

For a symmetric positive-definite matrix, all $\lambda_i > 0$, which is exactly the condition for the
quadratic form $\mathbf{x}^\top A\mathbf{x} > 0$ for all $\mathbf{x} \ne 0$ — the second-order
condition for a strict minimum that LP02-05 uses.

## 7. Python Implementation

```python
"""Least squares via the pseudo-inverse: fitting a line without an exact inverse."""
import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([2.1, 3.9, 6.2, 7.8])

# Design matrix: a column of ones for the intercept, then x.
A = np.column_stack([np.ones_like(x), x])
print("shape:", A.shape)                     # (4, 2) — 4 equations, 2 unknowns

coef, residuals, rank, sv = np.linalg.lstsq(A, y, rcond=None)
print("fit:", coef.round(2))                 # intercept ≈ 0.15, slope ≈ 1.94
print("rank:", rank, "of", A.shape[1])

pred = A @ coef
print("max error:", float(np.abs(pred - y).max().round(3)))

# The normal equations, stated explicitly.
normal = np.linalg.inv(A.T @ A) @ A.T @ y
print("same answer:", np.allclose(normal, coef))
```

**Output**

```text
shape: (4, 2)
fit: [0.15 1.94]
rank: 2 of 2
max error: 0.23
True
```

Four equations in two unknowns have no exact solution, so $A$ is not square and has no inverse. The
normal equations solve the closest problem instead, and `lstsq` is the numerically stable way to
compute it — the same operation behind every linear regression you will fit.

## 8. Practical Applications

- **Dimensionality reduction.** PCA keeps the eigenvectors with the largest eigenvalues; the discarded
  ones carry the least variance, and the eigenvalue ratio tells you how much information you keep.
- **Stability analysis.** In reinforcement learning and control, the eigenvalues of a system's matrix
  decide whether it converges, oscillates or diverges.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Transposing a product in the wrong order | Shape mismatch | $(AB)^\top = B^\top A^\top$ | Reverse the factors |
| Inverting a near-singular matrix | Huge, unstable values | $\det \approx 0$ amplifies noise | Use `lstsq` or add regularisation |
| Forgetting to normalise eigenvectors | Comparison failures | Scale is arbitrary | Normalise before comparing |
| Using `eig` on a symmetric matrix | Complex values, unsorted | General solver | Use `eigh` (real, sorted) |

## 10. Self-Assessment

**1.** $A$ is $2\times3$. What are the shapes of $A^\top$, $AA^\top$ and $A^\top A$?
<details><summary>Show answer</summary>

$A^\top$ is $3\times2$; $AA^\top$ is $2\times2$; $A^\top A$ is $3\times3$. The two products are
different objects of different sizes — a frequent source of confusion in kernel and covariance
computations.
</details>

**2.** $\det A = 0$. What does that imply about $A$'s eigenvalues, and about solving
$A\mathbf{x} = \mathbf{b}$?
<details><summary>Show answer</summary>

At least one eigenvalue is 0. The system has either no solution or infinitely many, depending on
$\mathbf{b}$; there is no unique solution, and $A^{-1}$ does not exist.
</details>

**3.** A symmetric matrix has eigenvalues 5, 1, 0.4. Which direction does PCA keep first, and why?
<details><summary>Show answer</summary>

The eigenvector with eigenvalue 5: it is the direction of greatest variance. Eigenvalues here are
variances along the corresponding directions, so 5 explains the most spread.
</details>

**4.** Verify $\sum\lambda_i = \operatorname{trace}(A)$ for $A = \begin{bmatrix}2&1\\1&2\end{bmatrix}$.
<details><summary>Show answer</summary>

Eigenvalues 3 and 1 sum to 4; the trace is $2 + 2 = 4$. ✓ This check catches most sign errors in a
characteristic equation.
</details>

## 11. Further Reading

- [MIT 18.06, Lecture 21: Eigenvalues and Eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) — the geometric derivation.
- [NumPy: `linalg`](https://numpy.org/doc/stable/reference/routines.linalg.html) — `inv`, `det`, `eig`, `eigh`, `lstsq`, `pinv`.

## Mini-Lab

Take the 2×2 matrix $M = \begin{bmatrix}3&1\\1&3\end{bmatrix}$. Find its eigenvalues by hand, then
with `eigh`. Pick 12 random unit vectors, apply $M$ to each, and plot the original and transformed
vectors as arrows. Which directions were only stretched, and by how much? Confirm both the trace and
determinant identities numerically.

## What to Do Next

Continue to [LP02-04 Derivatives, Partial Derivatives and Gradients](LP02-04-derivatives-partial-derivatives-and-gradients.md).
