# QUIZ-06 — Machine Learning Fundamentals self-check

| Module | M06 · Machine Learning Fundamentals and Algorithms |
| :--- | :--- |
| Questions | 20 multiple choice + 6 numerical + 4 short answer + 3 programming |
| Time | 90 minutes |
| Covers | [L06-01](../lessons/L06-01-what-machine-learning-is.md) … [L06-10](../lessons/L06-10-reproducible-ml-pipelines.md) |
| Pass mark | 16 / 20 on Part A, plus 4 / 6 on Part B |

[← Module home](../README.md) · [Course home](../../../README.md)

## How to use this quiz

Part A and Part B are closed-book and hand-computed; use a calculator but no code. Part C is open
book. Mark yourself against the worked answers, then use the revision map at the end. A question
you get right by elimination still counts, but reread the explanation.

## Part A — Multiple choice (20 marks)

**Q06.01** Machine learning is best defined as
- A. any program that uses statistics
- B. improving performance at a task with experience
- C. a neural network trained on big data
- D. automating a human decision

**Q06.02** A model predicts "rejected" for every loan application and scores 70% accuracy. This
- A. proves the model is useful
- B. is the majority-class baseline and has zero recall for approvals
- C. indicates overfitting
- D. indicates class weighting failed

**Q06.03** Which is **not** a leakage example?
- A. using `final_score` to predict `passed`
- B. scaling features before splitting
- C. a random split of time-ordered transactions
- D. imputing missing values with the training median inside a pipeline

**Q06.04** Standardisation computes
- A. $(x-\min)/(\max-\min)$
- B. $(x-\mu)/\sigma$
- C. $\log x$
- D. $x^2$

**Q06.05** Which model does **not** require feature scaling?
- A. k-NN
- B. logistic regression by gradient descent
- C. random forest
- D. k-means

**Q06.06** The normal equations solve
- A. $\min \sum|y-\hat y|$
- B. $\min \sum(y-\hat y)^2$
- C. $\max R^2$
- D. $\min \lambda\lVert w\rVert_1$

**Q06.07** Adding an uninformative feature to OLS
- A. always lowers training R²
- B. cannot lower training R² and may raise it
- C. always lowers test R²
- D. makes the model non-convex

**Q06.08** Logistic regression models
- A. the probability linearly
- B. the log-odds linearly
- C. the odds quadratically
- D. the label directly

**Q06.09** A coefficient of 0.693 multiplies the odds by approximately
- A. 0.69
- B. 1.0
- C. 2.0
- D. 3.0

**Q06.10** Raising the classification threshold from 0.5 to 0.7 generally
- A. raises recall
- B. raises precision
- C. raises AUC
- D. changes the feature ranking

**Q06.11** AUC is the probability that
- A. a positive is classified correctly
- B. a random positive outranks a random negative
- C. the model is calibrated
- D. precision exceeds recall

**Q06.12** With a 0.8% positive rate, a test with 90% sensitivity and 90% specificity has a PPV of
approximately
- A. 0.90
- B. 0.50
- C. 0.07
- D. 0.008

**Q06.13** A fully grown decision tree has
- A. high bias, low variance
- B. low bias, high variance
- C. low bias, low variance
- D. high bias, high variance

**Q06.14** Random forests reduce variance mainly by
- A. growing deeper trees
- B. decorrelating trees through bootstrap samples and feature subsampling
- C. adding more features
- D. scaling the inputs

**Q06.15** In gradient boosting, each new tree is fitted to
- A. the raw labels
- B. the pseudo-residuals
- C. a bootstrap sample
- D. the covariance matrix

**Q06.16** In an SVM, increasing C
- A. widens the margin
- B. penalises margin violations more heavily
- C. removes support vectors
- D. reduces variance

**Q06.17** k-means minimises
- A. the likelihood
- B. within-cluster sum of squares
- C. the silhouette
- D. BIC

**Q06.18** PCA requires standardisation when
- A. the data are non-Gaussian
- B. features have different units
- C. there are missing values
- D. there are more rows than columns

**Q06.19** DBSCAN labels sparse points as
- A. 0
- B. −1
- C. NaN
- D. a singleton cluster

**Q06.20** The main reproducibility benefit of a pipeline is that
- A. it trains faster
- B. every preprocessing statistic is fitted on training data only
- C. it removes the need for a test set
- D. it raises accuracy

## Part B — Numerical problems (6 marks)

Show your working. Each is worth one mark.

**Q06.21** A classifier produces TP = 40, FP = 10, FN = 60, TN = 890. Compute accuracy, precision,
recall and F1.

**Q06.22** Ridge with two features: $X^\top X = \begin{bmatrix}10&5\\5&10\end{bmatrix}$,
$X^\top y = \begin{bmatrix}20\\25\end{bmatrix}$, $\lambda = 5$. Compute $\hat w$.

**Q06.23** Training points A(0,0) class 0, B(1,0) class 0, C(0,1) class 1. Classify $q=(1,1)$ with
$k=3$, uniform weights.

**Q06.24** Prior $P(\text{spam}) = 0.3$, $P(\text{"free"}\mid\text{spam}) = 0.5$,
$P(\text{"free"}\mid\text{ham}) = 0.1$. Compute $P(\text{spam}\mid\text{"free"})$.

**Q06.25** Prevalence 2%, sensitivity 0.90, specificity 0.95. Compute the PPV.

**Q06.26** A node has 5 positives and 5 negatives. A split gives left (4 pos, 1 neg) and right
(1 pos, 4 neg). Compute the Gini gain.

## Part C — Short answer (8 marks)

**Q06.27** Explain, with one example each, the difference between target leakage and temporal
leakage.

**Q06.28** Why can a model with AUC 0.95 have useless precision in production?

**Q06.29** State two levers that reduce variance and the cost of each.

**Q06.30** Why is accuracy a poor headline metric for credit-card fraud detection?

## Part D — Programming (not timed; assessed by rubric)

**Q06.31** Write a function `split_and_score(X, y, k=5)` that performs a stratified k-fold
cross-validation of a logistic regression pipeline (impute → scale → fit) and returns the mean and
standard deviation of accuracy. It must not fit anything on the full data.

**Q06.32** Write `top_k_precision(scores, labels, k)` that returns the precision among the k highest
scores. Use it on the transaction data at k = 25 and k = 100, and explain the difference.

**Q06.33** Extend `linreg.Lasso` with an `elastic_net(alpha, l1_ratio)` option, where the penalty is
$\alpha(\rho\lVert w\rVert_1 + \tfrac{1-\rho}{2}\lVert w\rVert_2^2)$. Verify that
`l1_ratio=1` reproduces `Lasso` and `l1_ratio=0` reproduces `Ridge` up to scaling.

---

## Answers

### Part A

| Q | Answer | Why |
| :--- | :--- | :--- |
| 06.01 | B | Mitchell's definition: performance improves with experience. |
| 06.02 | B | Majority baseline; recall for approvals is zero. |
| 06.03 | D | Fitting the imputer inside the training fold is the correct behaviour. |
| 06.04 | B | Standardisation is $(x-\mu)/\sigma$; A is min–max. |
| 06.05 | C | Trees split on order, which is scale-invariant. |
| 06.06 | B | Least squares. |
| 06.07 | B | SSE cannot increase when a column is added. |
| 06.08 | B | The logit is linear. |
| 06.09 | C | $e^{0.693}\approx 2$. |
| 06.10 | B | Fewer positives flagged, so a higher share is correct. |
| 06.11 | B | The ranking interpretation. |
| 06.12 | C | $0.0072/(0.0072+0.0992)\approx 0.068$. |
| 06.13 | B | Memorises the training set. |
| 06.14 | B | Decorrelation lowers $\rho$ in the variance formula. |
| 06.15 | B | Sequential correction of residuals. |
| 06.16 | B | Large C means a hard margin. |
| 06.17 | B | Inertia. |
| 06.18 | B | Variance is unit-dependent. |
| 06.19 | B | Noise label is −1. |
| 06.20 | B | Structural protection against leakage. |

### Part B

**06.21** Accuracy $= (40+890)/1000 = 0.93$. Precision $= 40/50 = 0.80$. Recall $= 40/100 = 0.40$.
$F_1 = 2(0.8)(0.4)/(1.2) = 0.533$.

**06.22** $X^\top X + 5I = \begin{bmatrix}15&5\\5&15\end{bmatrix}$, determinant 200. Inverse
$=\frac{1}{200}\begin{bmatrix}15&-5\\-5&15\end{bmatrix}$.
$\hat w = \frac{1}{200}\begin{bmatrix}15(20)-5(25)\\ -5(20)+15(25)\end{bmatrix}
= \frac{1}{200}\begin{bmatrix}175\\275\end{bmatrix} = (0.875,\ 1.375)$.

**06.23** Squared distances: A 2, B 1, C 1. Labels 0, 0, 1. Majority 0, so predict class 0.

**06.24** $0.5\times0.3 = 0.15$; $0.1\times0.7 = 0.07$; posterior $= 0.15/0.22 = 0.682$.

**06.25** $0.9\times0.02 = 0.018$; false positive rate $0.05\times0.98 = 0.049$;
PPV $= 0.018/0.067 = 0.269$.

**06.26** Parent Gini $=1-(0.25+0.25)=0.5$. Left $=1-(0.64+0.04)=0.32$; right same $=0.32$.
Weighted $=0.5(0.32)+0.5(0.32)=0.32$. Gain $=0.18$.

### Part C

**06.27** Target leakage: a feature is derived from the label — `final_score` predicting `passed`.
Temporal leakage: the training set contains information from after the prediction moment — a random
split of time-ordered transactions so the model trains on rows that occur later than the test rows.

**06.28** AUC is threshold-free and prevalence-independent. At very low prevalence, even a good
ranking yields mostly false positives among the top-ranked cases, so precision at the deployed
threshold can be near zero.

**06.29** More data (cost: collection, time) and a simpler model or stronger regularisation (cost:
higher bias, possible loss of signal).

**06.30** Positives are 0.8% of rows, so predicting "no fraud" scores 99.2% accuracy while catching
nothing. Precision and recall at the review budget reflect the actual task.

### Part D rubric

| Exercise | Full marks |
| :--- | :--- |
| 06.31 | Fresh pipeline per fold, stratified, returns mean and std, no full-data fit |
| 06.32 | Correct ranking, correct precision, explanation tied to the budget |
| 06.33 | Both limits reproduce the existing classes; tests demonstrate it |

## Revision map

| If you missed | Reread |
| :--- | :--- |
| 06.01–06.07 | [L06-01](../lessons/L06-01-what-machine-learning-is.md), [L06-02](../lessons/L06-02-data-splitting-leakage-and-cross-validation.md), [L06-03](../lessons/L06-03-linear-regression-from-first-principles.md) |
| 06.08–06.12 | [L06-04](../lessons/L06-04-classification-with-logistic-regression.md), [L06-05](../lessons/L06-05-model-evaluation-metrics-and-roc.md) |
| 06.13–06.16 | [L06-06](../lessons/L06-06-bias-variance-and-regularisation.md), [L06-08](../lessons/L06-08-trees-forests-boosting-and-svm.md) |
| 06.17–06.19 | [L06-07](../lessons/L06-07-k-nearest-neighbours-and-naive-bayes.md), [L06-09](../lessons/L06-09-unsupervised-learning-and-dimensionality-reduction.md) |
| 06.20, Part C | [L06-10](../lessons/L06-10-reproducible-ml-pipelines.md), [L06-05](../lessons/L06-05-model-evaluation-metrics-and-roc.md) |

Next: [ASG-06](../assignments/asg-06-complete-ml-pipeline.md) and
[MP-06](../projects/mp-06-prediction-challenge.md).
