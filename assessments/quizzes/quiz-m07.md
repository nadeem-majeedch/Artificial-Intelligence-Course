# QUIZ-M07 — Artificial Neural Networks and Deep Learning

| | |
| :--- | :--- |
| Module | M07 · Artificial Neural Networks and Deep Learning |
| Questions | 11 (20 marks) |
| Time | 40 minutes |
| Covers | L07-01 … L07-08 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m07.md)

Calculator allowed. Shape arithmetic must show the formula.

---

## Part A — Multiple choice (4 marks)

**Q7.1** Stacking two linear layers with no activation between them is equivalent to

- A. a deeper nonlinear model
- B. a single linear layer
- C. a convolutional layer
- D. a residual network

**Q7.2** Dropout is disabled at inference because

- A. it would slow the model down
- B. the expected activation would be scaled incorrectly and predictions would be noisy
- C. gradients are not available
- D. it only works for convolutional layers

**Q7.3** A $5\times5$ convolution with 3 input channels and 16 output filters has how many parameters
(including bias)?

- A. 240
- B. 256
- C. 448
- D. 1,200

**Q7.4** Self-attention's cost in sequence length $n$ grows as

- A. $O(n)$
- B. $O(n\log n)$
- C. $O(n^2)$
- D. $O(1)$

## Part B — True or false, with a reason (2 marks)

**Q7.5** "A network with 99% train accuracy and 60% validation accuracy will improve if you add
another hidden layer."

## Part C — Conceptual (4 marks)

**Q7.6** (2 marks) Why is a nonlinear activation required between layers? Give the one-line
algebraic reason.

**Q7.7** (2 marks) Explain what batch normalisation changes during training and why it is switched
to running statistics at inference.

## Part D — Numerical (6 marks)

**Q7.8** (2 marks) A $32\times32$ image passes through a $3\times3$ convolution with stride 1 and no
padding. What is the output spatial size?

**Q7.9** (2 marks) A fully connected network maps 64 inputs to 32 hidden units to 10 outputs. How
many learnable parameters, including biases?

**Q7.10** (2 marks) A $28\times28$ image passes through a $5\times5$ convolution with stride 2 and no
padding. What is the output size?

## Part E — Tracing (2 marks)

**Q7.11** With $W=\begin{bmatrix}1&-1\\2&0\end{bmatrix}$, $b=0$, $x=\begin{bmatrix}3\\1\end{bmatrix}$,
compute $h=\mathrm{ReLU}(Wx)$ and then $y=[1,-1]\cdot h$.

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m07.md) · [Next quiz](quiz-m08.md)
