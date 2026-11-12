# AA-03 — Deriving the Logistic Regression Gradient

| | |
| :--- | :--- |
| Assignment | 03 |
| Difficulty | Intermediate |
| Estimated time | 2 hours |
| Prerequisites | P02, M06 (L06-04) |
| Format | Mathematical derivation |
| Covers | likelihood, cross-entropy, gradients, convexity |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

Every framework computes this gradient for you, which means the derivation is rarely checked. Doing it
once by hand makes the loss curves, the learning rate and the calibration discussion legible.

## Problem scenario

Binary logistic regression with parameters $w\in\mathbb R^d$, $b\in\mathbb R$, sigmoid
$\sigma(z)=1/(1+e^{-z})$, and $n$ examples $(x_i,y_i)$ with $y_i\in\{0,1\}$.

## Learning outcomes

1. Derive the log-likelihood and its negative.
2. Differentiate the loss with respect to $w$ and $b$.
3. Show the loss is convex.
4. Connect the algebra to a numerical stability issue.

## Tasks

1. **Likelihood.** Write $p(y_i\mid x_i)$ and the log-likelihood; show it equals the negative
   cross-entropy.
2. **Gradient.** Derive $\partial L/\partial w$ and $\partial L/\partial b$, showing the sigmoid
   derivative step.
3. **Matrix form.** Express the gradient for the full dataset as $X^\top(\hat y-y)/n$; state shapes.
4. **Convexity.** Show the Hessian is positive semi-definite, or argue convexity another way.
5. **Numerics.** Explain why `log(1 + exp(-z))` overflows and give the stable form.
6. **Check.** With $x=(2,1)$, $y=1$, $w=(0,0)$, $b=0$, compute the gradient contribution.

## Constraints

- Every step justified; no "it can be shown".
- Consistent notation throughout.
- The numerical check must be computed exactly, not approximated.

## Expected deliverables

A written derivation of at most 700 words plus the worked check.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Likelihood derivation | 25% | correct and connected to cross-entropy |
| Gradient derivation | 30% | chain rule shown, no skipped steps |
| Matrix form and shapes | 15% | dimensions consistent |
| Convexity | 15% | valid argument |
| Numerical check | 15% | exact values with working |

## Bonus challenges

- Extend to $L_2$ regularisation and show how the Hessian changes.
- Derive the gradient for softmax regression with $K$ classes.

---

[Assessment index](../README.md) · [AA-02](aa-02-complexity-analysis.md) · [AA-04](aa-04-model-evaluation.md)
