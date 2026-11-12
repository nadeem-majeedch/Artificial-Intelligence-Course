# QUIZ-M07 — Solutions and Explanations

[Quiz](quiz-m07.md) · [Assessment index](../README.md)

---

## Part A

**Q7.1 — B.** $W_2(W_1x+b_1)+b_2=(W_2W_1)x+(W_2b_1+b_2)$, a single affine map. This is why
nonlinearities are not optional.

**Q7.2 — B.** Dropout randomly zeroes units, so at inference you must use the expectation — either
scale activations by the keep probability during training (inverted dropout) or multiply by it at
test time. Leaving dropout on makes predictions stochastic and mis-scaled.

**Q7.3 — C.** $3\times16\times3\times3+16=432+16=448$. Forgetting the bias gives 432; multiplying
by the number of output positions is the other common error.

**Q7.4 — C.** Every token attends to every other, so the attention matrix is $n\times n$. This is
why long-context models need sparse or linear approximations.

## Part B

**Q7.5 — False.** A 99/60 gap is overfitting (high variance). Adding capacity increases variance,
so validation accuracy is likely to get worse. The standard responses are more data,
regularisation, augmentation, or a smaller model.

## Part C

**Q7.6 — Model answer.** With $\sigma$ linear, $\sigma(W_2\sigma(W_1x))$ collapses to a single
affine transformation, so depth adds no representational power. The composition of affine maps is
affine.

**Q7.7 — Model answer.** During training, batch normalisation standardises each mini-batch's
activations using that batch's mean and variance, which stabilises optimisation. At inference a
batch may be one example, so batch statistics are unavailable and noisy; the layer instead uses
running estimates accumulated during training, making predictions deterministic.

## Part D

**Q7.8 —** $\lfloor(32-3)/1\rfloor+1=30$, so $30\times30$.

**Q7.9 —** $64\times32+32+32\times10+10=2048+32+320+10=2{,}410$.

**Q7.10 —** $\lfloor(28-5)/2\rfloor+1=\lfloor11.5\rfloor+1=12$, so $12\times12$.

## Part E

**Q7.11 —** $Wx=\begin{bmatrix}3-1\\6+0\end{bmatrix}=\begin{bmatrix}2\\6\end{bmatrix}$; ReLU leaves
both positive, so $h=[2,6]$. Then $y=1(2)+(-1)(6)=-4$.

---

[Quiz](quiz-m07.md) · [Assessment index](../README.md) · [Next solutions](quiz-m08.md)
