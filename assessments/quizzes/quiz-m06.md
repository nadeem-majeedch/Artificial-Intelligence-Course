# QUIZ-M06 — Machine Learning Fundamentals

| | |
| :--- | :--- |
| Module | M06 · Machine Learning Fundamentals and Algorithms |
| Questions | 11 (20 marks) |
| Time | 40 minutes |
| Covers | L06-01 … L06-10 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m06.md)

Closed book, calculator allowed. For Part D show the confusion matrix before the metrics.

---

## Part A — Multiple choice (4 marks)

**Q6.1** Which is a leakage example?

- A. Fitting the scaler on the training split only
- B. Imputing with the training median inside a pipeline
- C. Selecting features using the full dataset before splitting
- D. Using stratified sampling

**Q6.2** For a 2% positive class, the most informative single metric is usually

- A. accuracy
- B. precision–recall AUC
- C. mean squared error
- D. R²

**Q6.3** Increasing $k$ in k-NN generally

- A. decreases bias and increases variance
- B. increases bias and decreases variance
- C. changes neither
- D. increases both

**Q6.4** PCA components are ordered by

- A. correlation with the target
- B. variance explained
- C. coefficient magnitude
- D. class separability

## Part B — True or false, with a reason (2 marks)

**Q6.5** "A model with 99% training accuracy and 71% test accuracy is overfitting; adding more
training data is a reasonable first response."

## Part C — Conceptual (4 marks)

**Q6.6** (2 marks) Why must preprocessing that learns parameters (scaling, imputation, feature
selection) be fitted inside cross-validation folds?

**Q6.7** (2 marks) Explain why accuracy alone is misleading for a fraud detector, and name two
metrics you would report instead.

## Part D — Numerical (6 marks)

**Q6.8** (4 marks) A classifier produces TP = 40, FP = 10, FN = 20, TN = 130. Compute precision,
recall, F1 and accuracy to three decimal places.

**Q6.9** (2 marks) A dataset has 1,000 rows: 900 negative, 100 positive. A model predicts
"negative" for every row. Report its accuracy and its recall for the positive class.

## Part E — Tracing (2 marks)

**Q6.10** A 1-NN classifier is trained on points $(0,0)\to A$, $(2,2)\to B$, $(3,3)\to B$. Classify
$(1,1)$ using Euclidean distance and state the margin to the nearest point of the other class.

## Part F — Python output (2 marks)

**Q6.11** What does this print?

```python
tp, fp, fn = 40, 10, 20
precision = tp / (tp + fp)
recall = tp / (tp + fn)
print(f"{precision:.3f} {recall:.3f} {2 * precision * recall / (precision + recall):.3f}")
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m06.md) · [Next quiz](quiz-m07.md)
