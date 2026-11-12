# QUIZ-M06 — Solutions and Explanations

[Quiz](quiz-m06.md) · [Assessment index](../README.md)

---

## Part A

**Q6.1 — C.** Selecting features on the full dataset lets test-set information influence which
features exist, so the test score is optimistic. A and B are correct practice (fit on train only);
D changes class balance, not leakage.

**Q6.2 — B.** With 2% positives, accuracy is dominated by the negative class and R²/MSE are
regression metrics. Precision–recall AUC focuses on the rare positive class.

**Q6.3 — B.** Larger $k$ smooths the decision boundary: bias rises (less flexible), variance falls.
$k=1$ is the low-bias, high-variance extreme.

**Q6.4 — B.** Components are ordered by variance explained; they are unsupervised, so they are not
ordered by correlation with a target (A) unless you use a supervised variant.

## Part B

**Q6.5 — True.** A large train–test gap is the signature of overfitting (high variance). More data
is a reasonable first response because it reduces variance; stronger regularisation or a simpler
model are the other standard responses. It is not *always* the best response — if the gap came from
leakage in training, more data will not help — but the statement is true as written.

## Part C

**Q6.6 — Model answer.** If a scaler or imputer sees validation-fold statistics, information from
the validation data leaks into training and the validation score is optimistic. Fitting inside each
fold estimates performance for a pipeline that will see only training data at fit time. The same
argument applies to feature selection: choosing features using all data is a leak.

**Q6.7 — Model answer.** With 0.1% fraud, predicting "not fraud" always gives 99.9% accuracy while
catching nothing. Report precision–recall AUC (or average precision) and recall at a fixed
precision that matches the review capacity; also report the confusion matrix at the deployed
threshold.

## Part D

**Q6.8 —** $TP=40$, $FP=10$, $FN=20$, $TN=130$.

- precision $=40/50=0.800$
- recall $=40/60\approx0.667$
- F1 $=2(0.8)(0.667)/(0.8+0.667)\approx1.0667/1.4667\approx0.727$
- accuracy $=(40+130)/200=0.850$

Marks: 1 per metric.

**Q6.9 —** Accuracy $=900/1000=0.900$. Recall for the positive class $=0/100=0.000$. This is the
majority-class baseline: high accuracy, zero usefulness for the task.

## Part E

**Q6.10 —** Distances from $(1,1)$: to $(0,0)$ is $\sqrt2\approx1.414$; to $(2,2)$ is
$\sqrt2\approx1.414$; to $(3,3)$ is $\sqrt8\approx2.828$. The nearest neighbour is a tie between
$A$ and $B$ at 1.414, so 1-NN is undecided without a tie-break rule (choose the lowest index, or
report the ambiguity). This is a real property of 1-NN, not a trick: ties must be handled
explicitly. Award full marks for identifying the tie and the margin; deduct if a confident label
is given with no tie-break stated.

## Part F

**Q6.11 —** `0.800 0.667 0.727`

Precision $40/50=0.8$; recall $40/60=0.6666\ldots$ printed as `0.667`; F1 computed from the
unrounded values is $0.72727\ldots$, printed `0.727`. Note that computing F1 from the *rounded*
precision and recall gives $0.7273$ as well here, but in general rounding before the final
calculation can shift the last digit.

---

[Quiz](quiz-m06.md) · [Previous solutions](quiz-m05.md) · [Assessment index](../README.md)
