# SA-M06 — Self-Assessment: Machine Learning Fundamentals

Module M06 · [Module](../../modules/M06-machine-learning-fundamentals/README.md) · [Quiz](../quizzes/quiz-m06.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Distinguish supervised, unsupervised and self-supervised learning
- [ ] Explain bias and variance and identify each from learning curves
- [ ] Choose a metric appropriate to class imbalance and state why accuracy fails
- [ ] Describe k-fold cross-validation and what it protects against
- [ ] Recognise leakage in a feature list
- [ ] Explain regularisation as a constraint on the hypothesis space

## Knowledge-check questions

1. A model has 0.99 train and 0.72 validation accuracy. Diagnose and prescribe two remedies.
2. Why is accuracy misleading at 2% prevalence? Give the precision of an always-negative classifier.
3. What does a `Pipeline` guarantee that manual preprocessing does not?
4. Distinguish L1 and L2 regularisation by their effect on weights.
5. What is the difference between a hyperparameter and a parameter? Give one example each.

## Practical competency checklist

- [ ] Split data with a justified strategy for the deployment setting
- [ ] Fit preprocessing inside cross-validation folds
- [ ] Report per-class precision and recall alongside a headline metric
- [ ] Produce a calibration table or plot
- [ ] Inspect misclassified examples and describe a pattern

## Suggested revision topics

Learning paradigms · overfitting and underfitting · cross-validation · leakage · metrics for
imbalance · regularisation · calibration · error inspection.

## Readiness test for M07

Without notes:

1. Diagnose under/overfitting from two learning curves.
2. Explain why stratified splitting matters and when a time-based split is required.
3. Compute precision and recall from a confusion matrix.

If any is shaky, revisit L06-03 and L06-06 before M07.
