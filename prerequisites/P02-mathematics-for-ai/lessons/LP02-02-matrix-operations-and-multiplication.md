# LP02-02 — Matrix Operations and Matrix Multiplication

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 120 minutes |
| Prerequisites | [LP02-01](LP02-01-scalars-vectors-matrices-and-tensors.md) |
| Notebook | [NB-P02-01](../notebooks/nb-p02-01-linear-algebra.ipynb) |
| Lab | [LAB-P02-01](../labs/lab-p02-01-image-as-a-matrix.md) |

[← Previous: Vectors and Tensors](LP02-01-scalars-vectors-matrices-and-tensors.md) · [P02 home](../README.md) · [Next: Transpose, Inverse, Eigen →](LP02-03-transpose-inverse-and-eigenvalues.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Add** matrices and multiply by a scalar, checking shape compatibility first.
- **Compute** a matrix–vector product as a weighted sum of columns, and a matrix–matrix product as a
  batch of such products.
- **Explain** why $AB \ne BA$ in general, and what the shape rule $(m\times k)(k\times n)$ means.
- **Recognise** the shapes of a neural network layer and count its parameters.

## 2. Prerequisite Knowledge

- Dot products and shapes: [LP02-01](LP02-01-scalars-vectors-matrices-and-tensors.md).

## 3. Conceptual Explanation

### 3.1 Elementwise operations are the easy ones

Addition and scalar multiplication act entry by entry, and require **identical shapes**:

$$
(A + B)_{ij} = a_{ij} + b_{ij}, \qquad (cA)_{ij} = c\,a_{ij}
$$

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A + B)          # [[ 6  8] [10 12]]
print(2 * A)          # [[ 2  4] [ 6  8]]
```

### 3.2 Matrix–vector product: a weighted sum of columns

For $A \in \mathbb{R}^{m\times n}$ and $\mathbf{x} \in \mathbb{R}^n$:

$$
(A\mathbf{x})_i = \sum_{j=1}^{n} a_{ij}x_j
$$

Read column-wise, $A\mathbf{x} = x_1\mathbf{a}_{:1} + x_2\mathbf{a}_{:2} + \cdots$ — the columns of
$A$ mixed in the proportions given by $\mathbf{x}$. Read row-wise, entry $i$ is the dot product of row
$i$ with $\mathbf{x}$. Both readings are correct; the column one explains *what a matrix does*, the
row one explains *how to compute it*.

### 3.3 Matrix–matrix product: apply the same map to several vectors

$C = AB$ with $A \in \mathbb{R}^{m\times k}$, $B \in \mathbb{R}^{k\times n}$:

$$
c_{ij} = \sum_{p=1}^{k} a_{ip}\,b_{pj}
$$

The inner dimensions must match ($k = k$); the result takes the outer ones, $m \times n$. The
interpretation that matters: **column $j$ of $C$ is $A$ applied to column $j$ of $B$.** So a
matrix–matrix product is a matrix–vector product repeated for each column, done in one compiled call.

### 3.4 Three properties, one warning

- **Associative:** $(AB)C = A(BC)$ — so you may regroup for efficiency.
- **Distributive:** $A(B + C) = AB + AC$.
- **Not commutative:** $AB \ne BA$ in general — and often $BA$ is not even defined.

The non-commutativity is not a technicality. Rotating then scaling is not the same as scaling then
rotating, and matrix multiplication is exactly the algebra of "do this, then that".

### 3.5 The neural network layer is one matrix product

A dense layer computes $\mathbf{y} = W\mathbf{x} + \mathbf{b}$, with $W \in \mathbb{R}^{d_{out}\times
d_{in}}$. For a batch $X \in \mathbb{R}^{B \times d_{in}}$ it becomes $Y = XW^\top + \mathbf{b}$, and
the parameter count is $d_{in}d_{out} + d_{out}$. This is why shape errors dominate deep-learning bug
reports: every layer is a shape contract.

## 4. Worked Examples

### Example 1 — a full 2×2 product by hand

$$
A = \begin{bmatrix}1&2\\3&4\end{bmatrix}, \quad
B = \begin{bmatrix}5&6\\7&8\end{bmatrix}
$$

$$
AB = \begin{bmatrix}
1\cdot5 + 2\cdot7 & 1\cdot6 + 2\cdot8\\
3\cdot5 + 4\cdot7 & 3\cdot6 + 4\cdot8
\end{bmatrix}
= \begin{bmatrix}19&22\\43&50\end{bmatrix}
$$

$$
BA = \begin{bmatrix}
5\cdot1 + 6\cdot3 & 5\cdot2 + 6\cdot4\\
7\cdot1 + 8\cdot3 & 7\cdot2 + 8\cdot4
\end{bmatrix}
= \begin{bmatrix}23&34\\31&46\end{bmatrix}
$$

```python
print(A @ B)
print(B @ A)
```

```text
[[19 22]
 [43 50]]
[[23 34]
 [31 46]]
```

Same two matrices, two different answers. Neither is "wrong"; the order is part of the operation.

### Example 2 — matrix–vector as a column mixture

$$
\begin{bmatrix}1&2\\3&4\end{bmatrix}\begin{bmatrix}1\\1\end{bmatrix}
= 1\cdot\begin{bmatrix}1\\3\end{bmatrix} + 1\cdot\begin{bmatrix}2\\4\end{bmatrix}
= \begin{bmatrix}3\\7\end{bmatrix}
$$

```python
print(A @ np.array([1, 1]))
```

```text
[3 7]
```

Confirming the row-wise rule on the same input: row 1 is $(1,2)$, dot $(1,1)$ is 3; row 2 is $(3,4)$,
dot $(1,1)$ is 7.

### Example 3 — one layer, and its parameter count

A layer with 4 inputs and 3 outputs:

```python
W = np.ones((3, 4))
b = np.array([0.5, 0.5, 0.5])
x = np.array([1.0, 2.0, 3.0, 4.0])
print((W @ x + b).shape, W.size + b.size)
```

```text
(3,) 15
```

$3 \times 4 = 12$ weights plus 3 biases = 15 parameters. For a batch of 8 inputs, `X @ W.T` has shape
`(8, 3)` and the parameter count is unchanged — parameters do not scale with batch size, activations
do.

## 5. Visual Explanation

```text
      B                 A                  AB
  k columns  ──▶  m×k times k×n  ──▶  m rows, n columns
                    ▲
                    │
        inner dimensions must match

   [m × k] · [k × n] = [m × n]
       └───┬───┘
        must be equal
```

*Text description of the diagram:* write the two shapes side by side. The two inner numbers are the
ones that must agree; the two outer numbers become the result's shape. If the inner pair disagrees,
the multiplication is undefined — check this before writing any code.

## 6. Mathematical Formulation

$$
(AB)_{ij} = \sum_{p=1}^{k} a_{ip}b_{pj},
\qquad
A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y},
\qquad
(AB)\mathbf{x} = A(B\mathbf{x})
$$

The last identity is the associativity that lets a deep network collapse two linear layers into one —
useful for pruning, and the reason stacking linear layers without a nonlinearity gains nothing:
$W_2(W_1\mathbf{x}) = (W_2W_1)\mathbf{x}$, still a single linear map.

Complexity: naive multiplication is $O(mnk)$. That is why GPUs — built for exactly this pattern — are
the hardware of deep learning.

## 7. Python Implementation

```python
"""Shape discipline: implement matmul by hand, then check it against NumPy."""
import numpy as np


def matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Return A @ B, raising a clear error on incompatible shapes."""
    m, k = A.shape
    k2, n = B.shape
    if k != k2:
        raise ValueError(f"inner shapes differ: {A.shape} @ {B.shape}")
    out = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            out[i, j] = sum(A[i, p] * B[p, j] for p in range(k))
    return out


A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(matmul(A, B).astype(int).tolist())        # [[19, 22], [43, 50]]
print(np.allclose(matmul(A, B), A @ B))         # True

# Batch: 8 samples, 4 features, 3 outputs.
X = np.arange(32, dtype=float).reshape(8, 4)
W = np.ones((3, 4))
print((X @ W.T).shape)                          # (8, 3)
```

**Output**

```text
[[19, 22], [43, 50]]
True
```

Writing the triple loop once is the fastest way to stop being confused by shapes: after it, `A @ B`
is shorthand rather than magic, and the error message above is the one you will actually meet.

## 8. Practical Applications

- **Model inference.** Every forward pass is a sequence of matrix products; a batch of 64 images
  through one layer is one `(64, d) @ (d, h)` call.
- **Image transforms.** Rotating, scaling or shearing an image is multiplication by a 2×2 or 3×3
  matrix applied to each pixel coordinate — the lab for this unit does exactly that.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Assuming $AB = BA$ | Results that disagree with a hand check | Non-commutative | Keep the order from the derivation |
| `A * B` instead of `A @ B` | Elementwise values | `*` is Hadamard | Use `@` |
| Wrong inner dimensions | `ValueError: matmul` | Shape contract violated | Transpose or reshape deliberately |
| Forgetting the bias shape | Broadcast across the wrong axis | `b` must be length $d_{out}$ | `Y + b` with `Y` of shape `(B, d_out)` |

## 10. Self-Assessment

**1.** $A$ is $3\times4$ and $B$ is $4\times2$. What is the shape of $AB$, and of $BA$?
<details><summary>Show answer</summary>

$AB$ is $3\times2$. $BA$ is undefined: the inner dimensions would be $2$ and $3$, which do not match.
</details>

**2.** Without computing, what is $A\mathbf{0}$ for any matrix $A$? And $A I$?
<details><summary>Show answer</summary>

$A\mathbf{0} = \mathbf{0}$ and $AI = A$ — the zero vector and the identity are the neutral elements
of the two operations. These are the vector-space axioms from LP02-01 showing up in matrix form.
</details>

**3.** A dense layer takes 128 inputs and produces 64 outputs. How many parameters does it have,
including biases?
<details><summary>Show answer</summary>

$128 \times 64 = 8192$ weights plus 64 biases = 8256. Written as a shape contract:
`(B, 128) @ (128, 64) → (B, 64)`.
</details>

**4.** Two linear layers are stacked with no activation between them. What does the composition
compute, and why is the extra depth useless?
<details><summary>Show answer</summary>

$W_2(W_1\mathbf{x}) = (W_2W_1)\mathbf{x}$, a single linear map with weight matrix $W_2W_1$. The
composition is no more expressive than one layer, which is precisely why nonlinear activations are
required.
</details>

## 11. Further Reading

- [MIT 18.06 Linear Algebra, Lecture 3: Multiplication and Inverse Matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) — Gilbert Strang's four ways to read a matrix product.
- [NumPy: `matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) — broadcasting rules for stacked matrix products.

## Mini-Lab

Write `matmul` by hand for $2\times3$ and $3\times2$ integer matrices, verify against NumPy, then use
it to apply a 90° rotation matrix $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ to the points
$(1,0), (1,1), (0,1)$. Plot the original and rotated points on the same axes. Which point moved to
$(-1, 1)$?

## What to Do Next

Continue to [LP02-03 Transpose, Inverse and Eigenvalues](LP02-03-transpose-inverse-and-eigenvalues.md).
