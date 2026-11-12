# LP02-01 — Scalars, Vectors, Matrices, Tensors and Dot Products

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 120 minutes |
| Prerequisites | [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md) (NumPy arrays) |
| Notebook | [NB-P02-01](../notebooks/nb-p02-01-linear-algebra.ipynb) |
| Lab | [LAB-P02-01](../labs/lab-p02-01-image-as-a-matrix.md) |

[← Previous unit: P01](../../P01-python-programming/README.md) · [P02 home](../README.md) · [Next: Matrix Operations →](LP02-02-matrix-operations-and-multiplication.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Map** a data structure in your program to its mathematical object: scalar, vector, matrix or
  tensor — and state its shape.
- **Compute** a dot product by hand and with NumPy, and interpret it geometrically.
- **Use** norms and cosine similarity to measure magnitude and direction separately.
- **Explain** what a vector space is, well enough to say why "adding two images" is a legal
  operation.

## 2. Prerequisite Knowledge

- NumPy arrays, shapes and `axis`: [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md).
- Arithmetic and square roots.

## 3. Conceptual Explanation

### 3.1 One idea, four shapes

| Object | Symbol | Shape | Example in AI |
| :--- | :--- | :--- | :--- |
| Scalar | $a \in \mathbb{R}$ | `()` | A learning rate, a loss value, one pixel's brightness |
| Vector | $\mathbf{a} \in \mathbb{R}^n$ | `(n,)` | One image flattened, one word embedding, one patient's features |
| Matrix | $A \in \mathbb{R}^{m \times n}$ | `(m, n)` | A dataset of $m$ rows and $n$ features, a weight matrix |
| Tensor | $\mathcal{T} \in \mathbb{R}^{d_1 \times \cdots \times d_k}$ | `(d1, ..., dk)` | A colour image `(height, width, 3)`, a batch `(32, 28, 28, 1)` |

The **rank** (or number of dimensions) is the length of the shape, not the number of elements. A
colour image of 224×224 pixels is a rank-3 tensor with 150 528 numbers; a batch of 32 such images is
rank 4 with 4 816 896.

### 3.2 A vector is both a list of numbers and an arrow

Both readings are used constantly:

- **As a record:** `[age, height_cm, weight_kg]` — the entries mean different things, and the vector
  is a point in feature space.
- **As a direction with length:** an arrow from the origin, where only relative geometry matters.

Machine learning lives on the tension between the two: because features are records, we rescale them
(standardisation) so that geometry becomes meaningful; because they are arrows, we can measure angles
and project.

### 3.3 Vector spaces: the rules that make arithmetic legal

A set of vectors forms a **vector space** over $\mathbb{R}$ when addition and scalar multiplication
behave as expected:

1. **Closure:** $\mathbf{u} + \mathbf{v}$ and $c\mathbf{u}$ are still in the set.
2. **Commutativity and associativity** of addition.
3. **A zero vector** $\mathbf{0}$ with $\mathbf{v} + \mathbf{0} = \mathbf{v}$.
4. **Additive inverses:** for every $\mathbf{v}$ there is $-\mathbf{v}$.
5. **Distributivity:** $c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v}$ and
   $(c + d)\mathbf{u} = c\mathbf{u} + d\mathbf{u}$.
6. **Unit scalar:** $1\mathbf{v} = \mathbf{v}$.

Why bother? Because these are exactly the properties that let you average embeddings, subtract a mean
vector, or interpolate between two images. When a property fails, the operation is meaningless — and
you can say why instead of guessing.

### 3.4 Dot product: the single most useful operation

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

The algebraic form (sum of products) is how you compute it; the geometric form (lengths times the
cosine of the angle) is how you interpret it. Both appear in the same paragraph of most papers.

Consequences worth memorising:

- $\mathbf{a} \cdot \mathbf{b} = 0$ ⟺ the vectors are **orthogonal** (perpendicular), when neither is
  zero.
- The dot product is largest when the vectors point the same way, zero at right angles, negative when
  they oppose.
- So $\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$ measures
  **direction agreement only**, ignoring length — which is why it is used for text and embedding
  similarity, where document length should not dominate.

The norm $\|\mathbf{a}\|_2 = \sqrt{\mathbf{a}\cdot\mathbf{a}}$ is the Euclidean length.

## 4. Worked Examples

### Example 1 — dot product, by hand and by NumPy

Let $\mathbf{a} = (1, 2)$ and $\mathbf{b} = (2, 1)$.

$$
\mathbf{a}\cdot\mathbf{b} = 1\cdot2 + 2\cdot1 = 4, \qquad
\|\mathbf{a}\| = \sqrt{1+4} = \sqrt{5} \approx 2.236
$$

```python
import numpy as np

a = np.array([1, 2])
b = np.array([2, 1])
print(a @ b)                      # 4
print(np.linalg.norm(a).round(3)) # 2.236
print(round((a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)), 3))
```

```text
4
2.236
0.8
```

$\cos\theta = 4/5 = 0.8$, so $\theta \approx 36.87°$ — the two vectors point in similar but not
identical directions.

### Example 2 — orthogonality

```python
u = np.array([1, 2])
v = np.array([2, -1])
print(u @ v)
```

```text
0
```

Zero dot product means perpendicular. Geometrically: moving along $(1,2)$ gains nothing in the
direction $(2,-1)$. This is the property behind projections, least squares, and why a linear model's
residual is orthogonal to its features at the optimum.

### Example 3 — a dataset is a matrix, and its columns are vectors

```python
X = np.array([
    [170, 65],
    [160, 55],
    [180, 80],
    [165, 60],
], dtype=float)

print(X.shape)                    # (4, 2)
print(X.mean(axis=0).round(1))    # [168.8  65. ]
print(X[:, 1].mean().round(1))    # column 1 only: 65.0

centre = X - X.mean(axis=0)
print((centre[:, 0] @ centre[:, 1]).round(1))
```

```text
(4, 2)
[168.8  65. ]
65.0
275.0
```

Four samples, two features. `X[:, 1]` is the second feature as a vector of length 4 — a column of the
matrix and a vector in its own right. Subtracting the column means **centres** the data, and the dot
product of the two centred columns is $n-1$ times their covariance ($275 = 3 \times 91.67$), which is
the bridge to P03.

## 5. Visual Explanation

```text
         b = (2, 1)
        /
       /   θ
      /______ a = (1, 2)
     /
    /
   O

projection of a onto b  =  (a·b / ‖b‖) · (b / ‖b‖)
```

*Text description of the diagram:* both vectors start at the origin. The angle between them is
$\theta$; the dot product is $\|\mathbf{a}\|\|\mathbf{b}\|\cos\theta$, which is positive here because
the angle is acute. Dropping a perpendicular from the tip of $\mathbf{a}$ onto the line of
$\mathbf{b}$ gives the projection — the component of $\mathbf{a}$ that lies along $\mathbf{b}$.

## 6. Mathematical Formulation

For $\mathbf{a}, \mathbf{b} \in \mathbb{R}^n$ and $c \in \mathbb{R}$:

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i,
\qquad
\|\mathbf{a}\|_2 = \sqrt{\sum_{i=1}^{n} a_i^2},
\qquad
\cos\theta = \frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

Two identities you will use later without noticing:

$$
\mathbf{a}\cdot\mathbf{a} = \|\mathbf{a}\|^2,
\qquad
\|\mathbf{a} - \mathbf{b}\|^2 = \|\mathbf{a}\|^2 + \|\mathbf{b}\|^2 - 2\,\mathbf{a}\cdot\mathbf{b}
$$

The second is the law of cosines, and it is exactly the expansion that turns squared Euclidean
distance into a dot product — the step that makes kernel methods and nearest-neighbour search fast.

## 7. Python Implementation

```python
"""Shapes and geometry: the two things that break ML code most often."""
import numpy as np

a = np.array([3.0, 4.0])
print("norm:", np.linalg.norm(a))                 # 5.0

# Cosine similarity for a tiny"document" example: term counts.
doc1 = np.array([2, 0, 1, 3])
doc2 = np.array([1, 1, 1, 0])

cos = (doc1 @ doc2) / (np.linalg.norm(doc1) * np.linalg.norm(doc2))
print("cosine:", round(float(cos), 3))             # 0.463

# A rank-3 tensor: 2 images of 2x2 pixels, greyscale.
batch = np.zeros((2, 2, 2))
print("shape:", batch.shape, "elements:", batch.size)

# Broadcasting check: centre every image by its own mean.
images = np.arange(8, dtype=float).reshape(2, 2, 2)
centred = images - images.mean(axis=(1, 2), keepdims=True)
print(centred.mean(axis=(1, 2)).round(6))          # [0. 0.]
```

**Output**

```text
norm: 5.0
cosine: 0.463
shape: (2, 2, 2) elements: 8
[0. 0.]
```

`keepdims=True` preserves the reduced axes as length 1, so the result broadcasts back against the
original tensor. Without it, the shapes would not align and NumPy would either error or produce the
wrong answer — a distinction worth remembering.

## 8. Practical Applications

- **Embeddings.** A word or image encoder outputs a vector; similarity search ranks by cosine
  similarity, not by Euclidean distance, because length often encodes frequency rather than meaning.
- **Feature matrices.** Every dataset you load is a matrix $X \in \mathbb{R}^{m\times n}$; the shape
  `(m, n)` is the first thing to check when a library complains.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Using `*` for dot product | Elementwise result, wrong shape | `*` is Hadamard product | Use `@` or `np.dot` |
| Confusing rank with size | `(3,)` called "3-dimensional matrix" | Rank = number of axes | Say "vector of length 3" |
| Comparing dot products of unscaled vectors | Long documents always "most similar" | Dot product includes magnitude | Normalise, or use cosine |
| Forgetting `keepdims` | Broadcast error | Reduced axis disappears | `keepdims=True` |

## 10. Self-Assessment

**1.** What is the shape of a batch of 16 RGB images of 32×32 pixels, and how many scalars does it
contain?
<details><summary>Show answer</summary>

`(16, 32, 32, 3)` — rank 4, containing $16 \times 32 \times 32 \times 3 = 49\,152$ scalars.
</details>

**2.** $\mathbf{a} = (1, 0, 2)$ and $\mathbf{b} = (2, 5, -1)$. Compute $\mathbf{a}\cdot\mathbf{b}$ and
say whether the angle is acute, right or obtuse.
<details><summary>Show answer</summary>

$1\cdot2 + 0\cdot5 + 2\cdot(-1) = 2 - 2 = 0$. The vectors are orthogonal, so the angle is exactly
90°.
</details>

**3.** Two documents have cosine similarity 0.95 but very different lengths. What does that tell you?
<details><summary>Show answer</summary>

Their term distributions have nearly the same *shape* — the same words in similar proportions — even
though one document is much longer. That is usually the desired behaviour for text similarity, and it
is precisely what raw dot product would obscure.
</details>

**4.** Why is "the set of all 2×2 matrices with determinant 0" not a vector space?
<details><summary>Show answer</summary>

It is not closed under addition: two singular matrices can sum to an invertible one, e.g.
$\begin{bmatrix}1&0\\0&0\end{bmatrix} + \begin{bmatrix}0&0\\0&1\end{bmatrix} = I$, which has
determinant 1. Closure is the axiom that fails.
</details>

## 11. Further Reading

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) — visual intuition for vectors, spans and dot products.
- [NumPy: Linear algebra](https://numpy.org/doc/stable/reference/routines.linalg.html) — `dot`, `norm`, `matmul` and friends.

## Mini-Lab

Take a 4×4 grayscale image as a NumPy array of integers 0–255 (write it by hand or generate it). Treat
each **row** as a vector and compute all pairwise cosine similarities. Which two rows are most alike?
Then flatten the image to a 16-vector and compute its norm. Finally, add 10 to every pixel and
recompute the norm — explain in one sentence why the norm changed but the cosine similarities between
rows did not change much (or did they?).

## What to Do Next

Continue to [LP02-02 Matrix Operations](LP02-02-matrix-operations-and-multiplication.md), where these
vectors become transformations.
