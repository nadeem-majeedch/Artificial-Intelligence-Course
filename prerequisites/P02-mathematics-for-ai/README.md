# P02 — Mathematics for AI

**Level 100 · 24 hours · 5 lessons, 2 notebooks, 2 labs**

[← Previous unit: P01](../P01-python-programming/README.md) · [Next unit: P03 Probability →](../P03-probability-and-statistics/README.md)

Linear algebra and calculus, restricted to what the modules actually use. Every idea is introduced with
a picture, computed by hand once, then written in NumPy so you can check it. There is no proof-heavy
material and no series convergence: the goal is to read a formula in a paper, know what it does to a
vector, and reproduce it in code.

## Who this unit is for

- **No linear algebra before:** follow the order given. LP02-01 to LP02-03 build on each other; skipping
  one leaves holes that show up in M04.
- **Comfortable with matrices:** work LP02-03 and LP02-04 carefully — eigenvalues and the chain rule are
  where most students' intuition is thinnest.
- **Strong maths, rusty code:** do the notebooks and labs; the hand derivations will be quick.

## Learning outcomes

By the end of P02 you can:

1. State the shape of any array you use, and say whether it is a scalar, vector, matrix or tensor.
2. Compute a dot product, a matrix–vector product and a matrix–matrix product, and explain what each
   means geometrically.
3. Invert a 2×2 matrix, decide when no inverse exists, and find eigenvalues and eigenvectors by solving
   the characteristic equation.
4. Derive a gradient by hand, verify it numerically, and explain why $-\nabla f$ is the descent
   direction.
5. Run gradient descent, predict whether a given learning rate will converge, and explain the role of
   the condition number.

These outcomes are the prerequisites for **M03, M04, M05, M07 and M10**, where they appear as weight
matrices, losses, gradients and PCA components.

## Lessons

| ID | Lesson | Time | Focus |
| :--- | :--- | ---: | :--- |
| [LP02-01](lessons/LP02-01-scalars-vectors-matrices-and-tensors.md) | Scalars, Vectors, Matrices, Tensors and Dot Products | 120 min | Shapes, vector spaces, norms, cosine similarity |
| [LP02-02](lessons/LP02-02-matrix-operations-and-multiplication.md) | Matrix Operations and Matrix Multiplication | 120 min | Shape contracts, column mixtures, layer parameters |
| [LP02-03](lessons/LP02-03-transpose-inverse-and-eigenvalues.md) | Transpose, Inverse and Eigenvalues | 120 min | Determinants, singular matrices, least squares, eigendecomposition |
| [LP02-04](lessons/LP02-04-derivatives-partial-derivatives-and-gradients.md) | Derivatives, Partial Derivatives and Gradients | 150 min | Sensitivity, gradients, chain rule, numeric checks |
| [LP02-05](lessons/LP02-05-optimization-fundamentals.md) | Optimisation Fundamentals | 150 min | Minima, convexity, gradient descent, learning rates, SGD |

## Notebooks

| Notebook | Pairs with | What it demonstrates |
| :--- | :--- | :--- |
| [NB-P02-01](notebooks/nb-p02-01-linear-algebra.ipynb) | LP02-01 … LP02-03 | Shapes, dot products, matrix products, inverses, eigenvalues, least squares |
| [NB-P02-02](notebooks/nb-p02-02-calculus-and-optimization.ipynb) | LP02-04 … LP02-05 | Numeric gradients, chain rule, gradient descent traces, learning-rate comparison |

Both notebooks plot as well as compute: a vector field or a descent path is easier to trust than a
column of numbers.

## Labs

| Lab | Time | What you build |
| :--- | :--- | :--- |
| [LAB-P02-01 — An Image Is a Matrix](labs/lab-p02-01-image-as-a-matrix.md) | 2.5 h | Build an image as an array, apply transforms, measure similarity |
| [LAB-P02-02 — Gradient Descent by Hand](labs/lab-p02-02-gradient-descent-by-hand.md) | 2.5 h | Derive a gradient, verify it, tune a learning rate |

The first lab connects shapes to something you can see; the second connects derivatives to an algorithm
you will use for the rest of the course.

## Time budget

| Activity | Hours |
| :--- | ---: |
| Five lessons | 11.0 |
| Two notebooks | 5.0 |
| Two labs | 5.0 |
| Review and self-assessment | 3.0 |
| **Total** | **24.0** |

At three hours a week this is an eight-week unit; at six hours a week, four. Do not compress LP02-04 and
LP02-05 — the gradient material is the single most reused idea in the programme.

## How to check yourself

Every lesson pairs a hand calculation with a code block that reproduces it. If your hand answer and the
printed answer disagree, stop and find out which is wrong before continuing: that habit is worth more
than any single result. The notebooks include gradient-checking cells; run them even when you are
confident.

## Common sticking points

- **Axis confusion.** `axis=0` collapses rows. Print `shape` before and after until it is automatic.
- **`*` versus `@`.** `*` is elementwise; `@` is the matrix product. Almost every shape error traces to
  this.
- **Variance versus standard deviation.** In code the parameter is usually called `scale` and expects
  the standard deviation.
- **Sign of the gradient step.** Descent subtracts. If the loss rises every step, check the sign first.

## Next

Continue to [P03 — Probability and Statistics](../P03-probability-and-statistics/README.md).
