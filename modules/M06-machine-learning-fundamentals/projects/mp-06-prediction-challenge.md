# MP-06 — Prediction Challenge: Best Model Under Honest Rules

| Module | M06 · Machine Learning Fundamentals and Algorithms |
| :--- | :--- |
| Effort | 3–4 hours |
| Type | Mini-project, individual or pairs |
| Lessons covered | L06-02 to L06-10 |
| Deliverables | `submission.py`, `validation.json`, `writeup.md` (≤ 800 words) |

[← Module home](../README.md) · [Course home](../../../README.md)

## The challenge

Pick **one** of the three challenge tasks below. Build the best model you can under rules that make
the comparison fair, and submit a validation score plus the code that produced it. The score on the
leaderboard is worth less than the honesty of the process: a leaked 0.99 loses to an honest 0.78.

| Task | Dataset | Label | Metric | Positive rate |
| :--- | :--- | :--- | :--- | ---: |
| **A** Loan approval | `datasets.loans()` | `approved` | average precision | 30% |
| **B** Intrusion | `datasets.intrusion()` | `is_attack` | average precision | 21% |
| **C** Fraud | `datasets.transactions()` | `is_fraud` | precision at top 30 | 0.8% |

Average precision is preferred to accuracy and AUC for A and B because it concentrates on the
positive class and the false positives an operator would review.

## Rules

1. **Fixed split.** Use `train_test_split(..., test_size=0.25, seed=0, stratify=y)` for A and B.
   For C, use a time-ordered split at row 3,750 (earlier rows train, later rows validate) and say
   why a random split would flatter you.
2. **No external labels.** You may use the features and the training labels only.
3. **No test-peeking.** The validation set is for your final number. If you tune on it more than a
   handful of times, say so and use cross-validation inside train instead.
4. **Report the pipeline and the seed.** A submission without them is not scored.
5. **Baseline required.** Majority-class and "no-skill" precision at the budget.
6. **No fabricated numbers.** The marker re-runs `submission.py`; the score in `validation.json`
   must match to three decimal places.

## What to submit

### `submission.py`

A single script that:
- loads the data and builds the split exactly as specified;
- defines the model as a `Pipeline` including imputation and scaling where relevant;
- fits, predicts, and prints the metric;
- writes `validation.json` with `{"task": ..., "metric": ..., "score": ..., "seed": 0, "config": {...}}`.

No CLI arguments required. It must run in under two minutes on a laptop.

### `validation.json`

The machine-readable result, including the metric name and the model configuration. If your score
depends on a threshold or a budget, record it.

### `writeup.md` (≤ 800 words)

1. **Approach.** What you tried and why, in three short paragraphs.
2. **Comparison table.** At least three configurations, scored by the same CV procedure.
3. **The final choice.** Why this configuration, and what you gave up.
4. **Error analysis.** One slice where the model is weakest and what you would do about it.
5. **Honesty note.** Anything that could inflate the score: repeated validation peeking, feature
   selection on all rows, a threshold chosen after seeing validation. Say it plainly.

## Scoring

| Component | Weight |
| :--- | ---: |
| Validation metric (relative to the best honest submission, capped at 100%) | 30% |
| Pipeline correctness (split, leakage, seeding) | 25% |
| Comparison methodology (same folds, baseline, spread) | 20% |
| Error analysis quality | 15% |
| Writeup clarity and honesty | 10% |

Ties are broken by the honesty note and the reproducibility of the number.

## Reference points

These are the module's own results, on the same splits. Beating them is not required; explaining
your position relative to them is.

```text
Loans, logistic regression       : accuracy 0.783, AUC 0.798, AP 0.668
Loans, random forest             : accuracy 0.762, AUC 0.802
Intrusion, random forest         : accuracy 0.979, AUC 0.996, recall 0.937
Fraud, Mahalanobis top 30        : precision ~0.85, recall ~0.67
```

## Stretch goals (no extra marks, but worth doing)

1. Beat the reference with a calibrated ensemble and prove the gain is outside the CV spread.
2. Show that your winner's advantage disappears under a different seed. Report it.
3. Build a one-page model card for the submitted model.
4. Add a drift check: compare feature distributions between train and validation and report PSI for
   the two most important features.

## Common failure modes

- Tuning the threshold on validation until the metric looks good, then reporting it as a result.
- Using `X_test` anywhere in feature selection, imputation or scaling.
- Reporting average precision but deploying a 0.5 threshold without checking the resulting precision.
- A `validation.json` that does not match a fresh run.
- An error analysis with no numbers.

## Submission

Submit the three files in one folder named `mp-06-<yourname>`. The marker runs
`python submission.py`, diffs `validation.json`, and reads the writeup. Late submissions are
accepted for seven days at a 10% penalty per day.
