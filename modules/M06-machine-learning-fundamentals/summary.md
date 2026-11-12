# M06 — One-Page Summary

[Module home](README.md) · [Course home](../../README.md) · [Quiz](quizzes/quiz-06.md)

## The workflow

```text
frame → collect → profile → split → prepare (inside the split) → fit → validate → test once
      → error analysis → model card → monitor
```

The two rules that prevent most disasters:

1. **Split before you touch anything.** Every statistic used in preprocessing comes from the
   training rows.
2. **Choose the metric from the cost of errors**, before you see a score.

## Learning paradigms

| Paradigm | Signal | Example |
| :--- | :--- | :--- |
| Supervised | labelled $(x,y)$ | loan approval |
| Unsupervised | $x$ only | customer segments |
| Semi-supervised | few labels, many rows | 200 labelled scans, 200,000 unlabelled |
| Self-supervised | label hidden in the data | next-word prediction |
| Reinforcement | reward over time | robot locomotion |

## Formulas to know cold

$$
\text{standardise: } z=\frac{x-\mu}{\sigma}
\qquad
\text{IQR fence: } [Q_1-1.5\,\text{IQR},\; Q_3+1.5\,\text{IQR}]
$$

$$
\text{OLS: } \hat w=(X^\top X)^{-1}X^\top y
\qquad
\text{ridge: } \hat w=(X^\top X+\lambda I)^{-1}X^\top y
$$

$$
\sigma(z)=\frac{1}{1+e^{-z}}
\qquad
\text{log-loss: } -\frac1n\sum\big[y\log p+(1-y)\log(1-p)\big]
$$

$$
\text{precision}=\frac{TP}{TP+FP}
\qquad
\text{recall}=\frac{TP}{TP+FN}
\qquad
F_1=\frac{2PR}{P+R}
$$

$$
\text{bias–variance: } \mathbb{E}[(y-\hat f)^2]=\text{bias}^2+\text{variance}+\sigma^2
$$

$$
\text{bagging: } \text{Var}=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2
\qquad
\text{Gini: } 1-\sum_c p_c^2
\qquad
\text{entropy: } -\sum_c p_c\log_2 p_c
$$

$$
\text{silhouette: } \frac{b-a}{\max(a,b)}
\qquad
\text{Mahalanobis: } (x-\mu)^\top\Sigma^{-1}(x-\mu)
$$

## The reference numbers (this module's data, seed 0)

| Problem | Model | Result |
| :--- | :--- | :--- |
| Students, regression | OLS, 4 features | MAE 4.53, RMSE 5.52, R² 0.540 |
| Students, classification | logistic | accuracy 0.827 (honest), 1.000 with leakage |
| Houses | OLS, clipped | RMSE 35.3, R² 0.75 (raw: 74.1, 0.38) |
| Loans | logistic | acc 0.783, AUC 0.798, AP 0.668, recall(approved) 0.527 |
| Loans | forest / boosting | test acc 0.762, AUC 0.802 / 0.790 |
| Loans | unlimited tree | train 1.000, test 0.679 |
| Spam | Gaussian NB | acc 0.970, P 0.855, R 0.979 |
| Spam | logistic | acc 0.983, P 0.939, R 0.958 |
| Attrition | logistic, no weights | acc 0.843, recall 0.125 |
| Attrition | logistic, balanced | acc 0.680, recall 0.786 |
| Intrusion | forest | acc 0.979, P 0.961, R 0.937, AUC 0.996 |
| Customers | k-means k=4 | sizes [80, 170, 110, 140]; silhouette 0.539 (k=2 gives 0.580) |
| Customers | PCA | 2 components keep 93.7% |
| Transactions | Mahalanobis top 25 | precision 0.920, recall 0.590 |
| Transactions | z > 3 | 73 flags, precision 0.438 |
| Transactions | IQR k=1.5 | 932 flags, precision 0.042 |

## Decision rules

- **Imbalanced classes:** report precision/recall at a budget, not accuracy. Majority baseline
  first.
- **Threshold:** minimise $c_{FP}FP+c_{FN}FN$; never accept 0.5 by default.
- **Rare positives:** average precision beats AUC; AUC is threshold-free and can mislead.
- **High train, low validation:** reduce capacity, regularise, average, or get more data.
- **Both scores low:** better features, not more tuning.
- **Clustering:** scale, profile every cluster, name it, check stability; silhouette is advisory.
- **Anomalies:** fix the alert budget, then maximise precision at it.
- **Before shipping:** pipeline, seed, baseline, interval, model card, monitoring plan.

## Leakage checklist

- [ ] Target not derived into a feature.
- [ ] Imputer/scaler/encoder fitted on training rows only.
- [ ] Split respects time order.
- [ ] Split respects entity groups.
- [ ] Feature selection done inside CV.
- [ ] Test set touched once.

## Common exam traps

1. Accuracy on 1% positives.
2. "AUC is high, so precision is fine."
3. Confusing standardisation with normalisation.
4. Reading coefficients as causal effects.
5. Thinking a deeper tree or higher degree is "more accurate".
6. Believing ridge always helps.
7. Choosing k by inertia alone.
8. Reporting a score without its seed, split and interval.

## If you remember five things

1. A baseline is not optional.
2. Split first; fit preprocessing on train only.
3. The metric encodes the cost of being wrong.
4. Variance is fixed by data and constraint, bias by better features.
5. A model you cannot reproduce is not a result.
