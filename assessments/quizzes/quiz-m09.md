# QUIZ-M09 — Computer Vision

| | |
| :--- | :--- |
| Module | M09 · Computer Vision |
| Questions | 10 (20 marks) |
| Time | 35 minutes |
| Covers | L09-01 … L09-06 |
| Pass mark | 12 / 20 |

> **Availability.** This module's lessons, notebooks and labs are published in this repository; sit this paper after finishing them.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m09.md)

---

## Part A — Multiple choice (4 marks)

**Q9.1** Intersection over Union (IoU) is

- A. area of overlap / area of union
- B. area of overlap / area of the predicted box
- C. area of union / area of the ground truth box
- D. number of matched pixels

**Q9.2** Padding in a convolution is used to

- A. reduce parameters
- B. control the output spatial size and border effects
- C. add nonlinearity
- D. increase the learning rate

**Q9.3** Which task assigns a class to every pixel?

- A. Image classification
- B. Object detection
- C. Semantic segmentation
- D. Instance retrieval

**Q9.4** Data augmentation primarily reduces

- A. bias
- B. variance
- C. label noise
- D. class imbalance

## Part B — True or false, with a reason (2 marks)

**Q9.5** "A $3\times3$ convolution with stride 1 and padding 1 preserves the spatial dimensions of
its input."

## Part C — Conceptual (4 marks)

**Q9.6** (2 marks) Why can a model reach 0.98 accuracy on a curated dataset and fail on phone
photos? Name two mechanisms.

**Q9.7** (2 marks) Explain why per-class recall matters more than overall accuracy for a defect
detector.

## Part D — Numerical (6 marks)

**Q9.8** (3 marks) Boxes $A=(0,0,4,4)$ and $B=(2,2,6,6)$ in $(x_1,y_1,x_2,y_2)$ coordinates. Compute
IoU to three decimal places.

**Q9.9** (3 marks) A $64\times64$ image passes through: conv $3\times3$, stride 1, pad 1 → max-pool
$2\times2$ → conv $3\times3$, stride 1, pad 0. Give the spatial size after each step.

## Part E — Tracing (2 marks)

**Q9.10** Apply $2\times2$ max-pooling with stride 2 to

$$
\begin{bmatrix}1&3&2&4\\5&7&6&8\\0&2&1&3\\4&6&5&7\end{bmatrix}
$$

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m09.md) · [Next quiz](quiz-m10.md)
