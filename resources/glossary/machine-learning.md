# Glossary — Machine Learning (M06)

Core supervised and unsupervised learning, evaluation and pipelines. Back to the
[glossary index](README.md).

## B

### Baseline
**Abbreviation.** — · **Module.** M06
**Simple definition.** The simple reference result a model must beat before its complexity is
justified.
**Detailed explanation.** A baseline converts a number into a decision: 96% accuracy means
nothing until you know the majority class is 93%. Every serious evaluation states the baseline
first, because a model that fails to beat it has learnt nothing useful regardless of how
sophisticated it looks.
**Mathematics.** $\text{baseline} = \max_c P(c)$ for a majority-class classifier.
**Practical example.** On the M01 enquiry corpus, always predicting "registration" scores 40%
because that class is 96 of 240 messages — a vendor's "96% accuracy" claim is only +56 points
above a rule that reads nothing.
**Related.** [Confusion matrix](#confusion-matrix), [Class imbalance](#class-imbalance), [Precision and recall](#precision-and-recall)
**Where it is taught.** [L06-01 What machine learning is](../../modules/M06-machine-learning-fundamentals/lessons/L06-01-what-machine-learning-is.md)

### Bias–variance trade-off
**Abbreviation.** — · **Module.** M06
**Simple definition.** The tension between a model too simple to capture the pattern and one too
flexible to ignore the noise.
**Detailed explanation.** Expected test error decomposes into bias², variance and irreducible
noise. Increasing capacity lowers bias and raises variance; the practical question is which side
of the minimum you are on, which is diagnosed by comparing training and validation error.
**Mathematics.** $\mathbb{E}[(y - \hat{f})^2] = \text{Bias}^2 + \text{Var} + \sigma^2$
**Practical example.** A depth-2 tree underfits a curved boundary (high bias); a depth-30 tree
fits every training point and swings wildly between folds (high variance).
**Related.** [Overfitting](#overfitting), [Regularisation](#regularisation), [Cross-validation](#cross-validation)
**Where it is taught.** [L06-06 Bias, variance and regularisation](../../modules/M06-machine-learning-fundamentals/lessons/L06-06-bias-variance-and-regularisation.md)

## C

### Calibration
**Abbreviation.** — · **Module.** M06
**Simple definition.** Agreement between predicted probabilities and observed frequencies.
**Detailed explanation.** A model can rank well and still be badly calibrated: if it says 0.9 it
should be right about nine times in ten. Calibration matters whenever a probability drives a
decision — thresholds, alert queues, expected-cost calculations — and it is checked with
reliability curves and ECE.
**Mathematics.** $\text{ECE} = \sum_b \frac{n_b}{n}\,\lvert \text{acc}(b) - \text{conf}(b) \rvert$
**Practical example.** The M01 classifier puts 40 emails in the 0.8–1.0 bucket and is right 55%
of the time; the confidence cannot be used as a routing threshold.
**Related.** [ROC and AUC](#roc-and-auc), [Baseline](#baseline), [Precision and recall](#precision-and-recall)
**Where it is taught.** [L06-05 Model evaluation, metrics and ROC](../../modules/M06-machine-learning-fundamentals/lessons/L06-05-model-evaluation-metrics-and-roc.md)

### Class imbalance
**Abbreviation.** — · **Module.** M06
**Simple definition.** A classification problem where one class is far rarer than the other.
**Detailed explanation.** With 1% positives, predicting "negative" always is 99% accurate and
useless. Imbalance changes which metrics are meaningful (precision, recall, AP) and which
resampling or weighting strategy is appropriate; it does not change the underlying problem.
**Mathematics.** —
**Practical example.** Fraud data with 0.8% positives: accuracy 99.2% for a model that never
flags anything, yet recall 0 and zero fraud caught.
**Related.** [Precision and recall](#precision-and-recall), [ROC and AUC](#roc-and-auc), [Baseline](#baseline)
**Where it is taught.** [L06-05 Model evaluation, metrics and ROC](../../modules/M06-machine-learning-fundamentals/lessons/L06-05-model-evaluation-metrics-and-roc.md)

### Confusion matrix
**Abbreviation.** — · **Module.** M06
**Simple definition.** A table of true positives, false positives, false negatives and true
negatives.
**Detailed explanation.** Every classification metric is a ratio of these four counts, so the
matrix is the primary evidence and the metric is a summary. Reporting a metric without the matrix
hides which error dominates, and the two errors usually have different costs.
**Mathematics.** $\begin{pmatrix} TN & FP \\ FN & TP \end{pmatrix}$
**Practical example.** A screening model with TP 72, FP 8, FN 18, TN 902 has recall 0.80 but
precision 0.90 while missing 18 cases a week.
**Related.** [Precision and recall](#precision-and-recall), [ROC and AUC](#roc-and-auc), [Calibration](#calibration)
**Where it is taught.** [L06-05 Model evaluation, metrics and ROC](../../modules/M06-machine-learning-fundamentals/lessons/L06-05-model-evaluation-metrics-and-roc.md)

### Cross-validation
**Abbreviation.** CV · **Module.** M06
**Simple definition.** Rotating the validation split so every observation is held out once.
**Detailed explanation.** A single split gives a noisy estimate; k-fold repeats training k times
and reports mean and spread. The spread is as important as the mean — a model at 0.785 ± 0.019
is not clearly better than one at 0.774.
**Mathematics.** $\hat{\mu} = \frac{1}{k}\sum_{i=1}^{k} \text{score}_i$, with standard deviation across folds.
**Practical example.** Five-fold CV on the loan data gives 0.785 ± 0.019; the competitor's 0.774
is inside one standard deviation, so the difference is not established.
**Related.** [Hold-out split](#hold-out-split), [Data leakage](#data-leakage), [Overfitting](#overfitting)
**Where it is taught.** [L06-02 Data splitting, leakage and cross-validation](../../modules/M06-machine-learning-fundamentals/lessons/L06-02-data-splitting-leakage-and-cross-validation.md)

## D

### Data leakage
**Abbreviation.** — · **Module.** M06
**Simple definition.** Information from outside the training fold reaching the model, making
validation optimistic.
**Detailed explanation.** Leakage is the most common cause of a model that scores 0.99 offline
and fails in production. It enters through preprocessing fitted on all data, through target-derived
features, and through time — a feature recorded after the outcome is a label in disguise.
**Mathematics.** —
**Practical example.** Scaling features before splitting leaks test-set means into training; a
pipeline that fits the scaler inside each fold gives an honest 0.82 instead of a fantasy 0.94.
**Related.** [Cross-validation](#cross-validation), [Hold-out split](#hold-out-split), [Overfitting](#overfitting)
**Where it is taught.** [L06-02 Data splitting, leakage and cross-validation](../../modules/M06-machine-learning-fundamentals/lessons/L06-02-data-splitting-leakage-and-cross-validation.md)

### Decision tree
**Abbreviation.** — · **Module.** M06
**Simple definition.** A model that partitions the feature space by a sequence of if/else tests.
**Detailed explanation.** Trees are interpretable and need no scaling, but a single tree is
high-variance: small data changes produce different splits. That instability is exactly what
ensembles fix, and why a forest usually beats the tree it contains.
**Mathematics.** Split chosen to maximise information gain $\;H(S) - \sum_k \frac{|S_k|}{|S|}H(S_k)$.
**Practical example.** A depth-3 tree on loan data yields readable rules ("income < 30k and
existing debt > 40% → decline") at 0.79 accuracy.
**Related.** [Random forest](#random-forest), [Gradient boosting](#gradient-boosting), [Bias–variance trade-off](#biasvariance-trade-off)
**Where it is taught.** [L06-08 Trees, forests, boosting and SVM](../../modules/M06-machine-learning-fundamentals/lessons/L06-08-trees-forests-boosting-and-svm.md)

## F

### Feature
**Abbreviation.** — · **Module.** M06
**Simple definition.** A measurable input variable used to predict the target.
**Detailed explanation.** Feature choice encodes assumptions about what matters and what will be
available at prediction time. The hardest discipline is excluding features that will not exist
when the model runs, or that are consequences of the label.
**Mathematics.** $x \in \mathbb{R}^d$ — a vector of $d$ features per example.
**Practical example.** Including `account_closed_date` to predict churn leaks the outcome: an
account closes *because* the customer churned.
**Related.** [Label](#label), [Data leakage](#data-leakage), [Supervised learning](#supervised-learning)
**Where it is taught.** [L06-01 What machine learning is](../../modules/M06-machine-learning-fundamentals/lessons/L06-01-what-machine-learning-is.md)

## G

### Gradient boosting
**Abbreviation.** GBM · **Module.** M06
**Simple definition.** An ensemble that adds trees sequentially, each fitted to the residual
errors of the current model.
**Detailed explanation.** Boosting reduces bias by correcting mistakes; the learning rate and
tree depth control how aggressively. It is the default tabular learner for a reason, but it
overfits small noisy datasets and its feature importances are biased toward high-cardinality
columns.
**Mathematics.** $F_m(x) = F_{m-1}(x) + \nu\, h_m(x)$, with $h_m$ fitted to pseudo-residuals.
**Practical example.** On the spam dataset, 300 shallow trees at learning rate 0.05 reach 0.97
F1, beating logistic regression's 0.94 at the cost of interpretability.
**Related.** [Random forest](#random-forest), [Decision tree](#decision-tree), [Overfitting](#overfitting)
**Where it is taught.** [L06-08 Trees, forests, boosting and SVM](../../modules/M06-machine-learning-fundamentals/lessons/L06-08-trees-forests-boosting-and-svm.md)

## H

### Hold-out split
**Abbreviation.** — · **Module.** M06
**Simple definition.** Dividing data once into training, validation and test sets.
**Detailed explanation.** The test set is touched once, at the end, or it stops being a test set.
The validation set is for choices; the test set estimates generalisation. Time-ordered data must
be split by time, never randomly.
**Mathematics.** —
**Practical example.** 60/20/20 on 10,000 loans gives 6,000 training, 2,000 validation, 2,000
test rows; the test set is used once, after all tuning.
**Related.** [Cross-validation](#cross-validation), [Data leakage](#data-leakage)
**Where it is taught.** [L06-02 Data splitting, leakage and cross-validation](../../modules/M06-machine-learning-fundamentals/lessons/L06-02-data-splitting-leakage-and-cross-validation.md)

## K

### k-means
**Abbreviation.** — · **Module.** M06
**Simple definition.** Clustering that partitions points into $k$ groups by proximity to group
centres.
**Detailed explanation.** It alternates assignment and centroid updates until convergence, which
guarantees a local optimum, not a global one. It assumes roughly spherical, similarly sized
clusters and requires $k$ in advance — both assumptions are usually violated in real data.
**Mathematics.** Minimise $\sum_{i}\sum_{x \in C_i} \lVert x - \mu_i \rVert^2$.
**Practical example.** Segmenting 5,000 customers into four groups for a campaign; the elbow
curve suggests four, and the segments differ in spend by a factor of six.
**Related.** [PCA](#pca), [Unsupervised learning](#unsupervised-learning)
**Where it is taught.** [L06-09 Unsupervised learning and dimensionality reduction](../../modules/M06-machine-learning-fundamentals/lessons/L06-09-unsupervised-learning-and-dimensionality-reduction.md)

## L

### Label
**Abbreviation.** — · **Module.** M06
**Simple definition.** The target value a supervised model is trained to predict.
**Detailed explanation.** Labels are measurements made by someone under some policy, so they
carry that policy's bias. Label noise sets a ceiling on achievable accuracy, and no model can
exceed the agreement rate of its own annotations.
**Mathematics.** $y \in \{0,1\}$ or $y \in \mathbb{R}$.
**Practical example.** Loan defaults are labelled by a 90-day rule; changing the rule to 60 days
relabels thousands of rows and changes every model trained on them.
**Related.** [Feature](#feature), [Supervised learning](#supervised-learning), [Class imbalance](#class-imbalance)
**Where it is taught.** [L06-01 What machine learning is](../../modules/M06-machine-learning-fundamentals/lessons/L06-01-what-machine-learning-is.md)

### Linear regression
**Abbreviation.** — · **Module.** M06
**Simple definition.** Fitting a line (or hyperplane) that minimises squared error.
**Detailed explanation.** The closed-form solution and the gradient view are the same object seen
from two directions, and both reappear in logistic regression and neural networks. Its
coefficients are interpretable only under the assumption that features are not strongly
correlated.
**Mathematics.** $\hat{\beta} = (X^\top X)^{-1} X^\top y$; loss $\frac{1}{n}\lVert y - X\beta \rVert^2$.
**Practical example.** Predicting house price from area and rooms gives coefficients you can
quote as marginal prices — until two features are collinear and the signs flip.
**Related.** [Logistic regression](#logistic-regression), [Regularisation](#regularisation), [Baseline](#baseline)
**Where it is taught.** [L06-03 Linear regression from first principles](../../modules/M06-machine-learning-fundamentals/lessons/L06-03-linear-regression-from-first-principles.md)

### Logistic regression
**Abbreviation.** — · **Module.** M06
**Simple definition.** A linear model whose output is squashed to a probability by the logistic
function.
**Detailed explanation.** It is a classifier with calibrated outputs and interpretable
coefficients, and the standard baseline for binary problems. Its decision boundary is linear,
which is a limitation and also the reason its failures are diagnosable.
**Mathematics.** $p(y=1 \mid x) = \sigma(w^\top x + b) = \frac{1}{1 + e^{-(w^\top x + b)}}$
**Practical example.** A credit model with five features reaches 0.78 AUC, and each coefficient
reads as a log-odds change per unit — enough to write a reason code.
**Related.** [Linear regression](#linear-regression), [Precision and recall](#precision-and-recall), [Calibration](#calibration)
**Where it is taught.** [L06-04 Classification with logistic regression](../../modules/M06-machine-learning-fundamentals/lessons/L06-04-classification-with-logistic-regression.md)

## O

### Overfitting
**Abbreviation.** — · **Module.** M06
**Simple definition.** Learning the training data's noise so well that new data performs worse.
**Detailed explanation.** The signature is training error falling while validation error rises.
Causes are capacity, too little data, leakage, and early stopping on the wrong metric. The fix is
regularisation, more data, or a simpler model — not more epochs.
**Mathematics.** $\text{error}_{train} \ll \text{error}_{val}$
**Practical example.** A 1-nearest-neighbour model memorises 1,000 training rows perfectly and
scores 0.61 on held-out data, below the 0.78 logistic baseline.
**Related.** [Bias–variance trade-off](#biasvariance-trade-off), [Regularisation](#regularisation), [Data leakage](#data-leakage)
**Where it is taught.** [L06-06 Bias, variance and regularisation](../../modules/M06-machine-learning-fundamentals/lessons/L06-06-bias-variance-and-regularisation.md)

## P

### PCA
**Abbreviation.** PCA · **Module.** M06
**Simple definition.** Projecting data onto the directions of greatest variance.
**Detailed explanation.** PCA is a linear, unsupervised compression that decorrelates features and
enables plotting high-dimensional data. It preserves variance, not class separation, so it can
discard exactly the direction that predicts the label.
**Mathematics.** Eigenvectors of the covariance matrix $\Sigma$; project onto the top $k$.
**Practical example.** Reducing 30 sensor channels to 3 components retains 92% of variance and
makes an anomaly cluster visible in a scatter plot.
**Related.** [k-means](#k-means), [Unsupervised learning](#unsupervised-learning)
**Where it is taught.** [L06-09 Unsupervised learning and dimensionality reduction](../../modules/M06-machine-learning-fundamentals/lessons/L06-09-unsupervised-learning-and-dimensionality-reduction.md)

### Precision and recall
**Abbreviation.** — · **Module.** M06
**Simple definition.** Of the items flagged, the share that were right (precision); of the real
positives, the share that were found (recall).
**Detailed explanation.** The two answer different stakeholders' questions: precision is the
person acting on a flag, recall is the person harmed by a miss. They trade off against each
other, and reporting one without the other is how a model looks good while failing.
**Mathematics.** $P = \frac{TP}{TP+FP}$, $R = \frac{TP}{TP+FN}$
**Practical example.** Fraud alerts at precision 0.31 / recall 0.88 mean two thirds of
investigations find nothing, but 12% of fraud still gets through.
**Related.** [Confusion matrix](#confusion-matrix), [F1](#f1), [Class imbalance](#class-imbalance)
**Where it is taught.** [L06-05 Model evaluation, metrics and ROC](../../modules/M06-machine-learning-fundamentals/lessons/L06-05-model-evaluation-metrics-and-roc.md)

### F1
**Abbreviation.** F1 · **Module.** M06
**Simple definition.** The harmonic mean of precision and recall.
**Detailed explanation.** It is high only when both are high, and it treats them as equally
important — which is wrong whenever one error costs more than the other. Use it as a summary,
never as the only number.
**Mathematics.** $F_1 = \frac{2PR}{P+R}$
**Practical example.** $P = 0.80$, $R = 0.50$ gives $F_1 = 0.615$, which looks mediocre even
though the model may be fine if misses are cheap.
**Related.** [Precision and recall](#precision-and-recall), [Confusion matrix](#confusion-matrix)
**Where it is taught.** [L06-05 Model evaluation, metrics and ROC](../../modules/M06-machine-learning-fundamentals/lessons/L06-05-model-evaluation-metrics-and-roc.md)

## R

### Random forest
**Abbreviation.** RF · **Module.** M06
**Simple definition.** Many decision trees trained on bootstrap samples and random feature
subsets, averaged.
**Detailed explanation.** Bagging plus feature randomness decorrelates the trees, so the average
has lower variance than any member. It is robust, needs little tuning, and gives a usable
importance ranking — though that ranking is not causal.
**Mathematics.** $\hat{f}(x) = \frac{1}{B}\sum_{b=1}^{B} T_b(x)$
**Practical example.** 500 trees on the churn dataset reach 0.86 AUC with no tuning, and the
top three features match what the retention team already believed.
**Related.** [Decision tree](#decision-tree), [Gradient boosting](#gradient-boosting), [Bias–variance trade-off](#biasvariance-trade-off)
**Where it is taught.** [L06-08 Trees, forests, boosting and SVM](../../modules/M06-machine-learning-fundamentals/lessons/L06-08-trees-forests-boosting-and-svm.md)

### Regularisation
**Abbreviation.** — · **Module.** M06
**Simple definition.** A penalty on model complexity added to the training objective.
**Detailed explanation.** L2 shrinks coefficients smoothly, L1 drives some to zero and selects
features, and the strength is chosen on validation data. Regularisation is the cheapest defence
against overfitting and the reason linear models remain competitive on small data.
**Mathematics.** $L(\theta) + \lambda\lVert\theta\rVert_2^2$ or $+ \lambda\lVert\theta\rVert_1$
**Practical example.** L2 with $\lambda = 0.1$ drops loan-model validation error from 0.31 to
0.27 while leaving training error almost unchanged — the gap closes.
**Related.** [Overfitting](#overfitting), [Bias–variance trade-off](#biasvariance-trade-off), [Linear regression](#linear-regression)
**Where it is taught.** [L06-06 Bias, variance and regularisation](../../modules/M06-machine-learning-fundamentals/lessons/L06-06-bias-variance-and-regularisation.md)

### ROC and AUC
**Abbreviation.** ROC, AUC · **Module.** M06
**Simple definition.** The curve of true-positive rate against false-positive rate as the
threshold moves, and the area under it.
**Detailed explanation.** AUC is the probability that a random positive is ranked above a random
negative: threshold-free and prevalence-independent. It says nothing about precision at the
operating point you deploy, which is why rare-positive problems need a precision–recall curve.
**Mathematics.** $\text{AUC} = P(\hat{s}(x^+) > \hat{s}(x^-))$
**Practical example.** AUC 0.95 at 1% prevalence can still mean precision 0.16 at the chosen
threshold — excellent ranking, poor alert quality.
**Related.** [Precision and recall](#precision-and-recall), [Calibration](#calibration), [Class imbalance](#class-imbalance)
**Where it is taught.** [L06-05 Model evaluation, metrics and ROC](../../modules/M06-machine-learning-fundamentals/lessons/L06-05-model-evaluation-metrics-and-roc.md)

## S

### Supervised learning
**Abbreviation.** — · **Module.** M06
**Simple definition.** Learning a mapping from inputs to labels using examples where the label is
known.
**Detailed explanation.** The supervision is in the labels, and their quality bounds what can be
learnt. The workflow — split, fit preprocessing inside the fold, train, validate, then test once —
matters as much as the algorithm.
**Mathematics.** minimise $\frac{1}{n}\sum_i L(y_i, f(x_i))$
**Practical example.** Predicting loan default from 10,000 labelled applications, with the split
made by application date so the model is tested on the future.
**Related.** [Unsupervised learning](#unsupervised-learning), [Label](#label), [Feature](#feature)
**Where it is taught.** [L06-01 What machine learning is](../../modules/M06-machine-learning-fundamentals/lessons/L06-01-what-machine-learning-is.md)

### Unsupervised learning
**Abbreviation.** — · **Module.** M06
**Simple definition.** Finding structure in data without labels.
**Detailed explanation.** Clustering and dimensionality reduction are descriptive tools: they
produce hypotheses, not predictions, and their output needs human interpretation. Evaluating them
is genuinely hard because there is no ground truth to compare against.
**Mathematics.** —
**Practical example.** k-means on transaction data surfaces a segment of 340 customers whose
behaviour no one had named; the business decides whether it is real.
**Related.** [k-means](#k-means), [PCA](#pca), [Supervised learning](#supervised-learning)
**Where it is taught.** [L06-09 Unsupervised learning and dimensionality reduction](../../modules/M06-machine-learning-fundamentals/lessons/L06-09-unsupervised-learning-and-dimensionality-reduction.md)

---

[Glossary index](README.md) · [Classical AI](classical-ai.md) · [Deep learning](deep-learning.md) · [Quick reference](../glossary.md)
