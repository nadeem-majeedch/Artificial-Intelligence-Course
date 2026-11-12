# ASG-07 — A Deep Model with an Ablation Study

| Module | M07 · Artificial Neural Networks and Deep Learning |
| :--- | :--- |
| Type | Individual assignment |
| Weight | Module grade |
| Effort | ~2 hours of focused work (up to 6 hours with the extensions) |
| Submit | Report, code and figures |
| Covers | L07-03, L07-04, L07-05, L07-08 |

[← Module home](../README.md) · [Labs](../labs/lab-07-02-digital-fashion-and-plant-classifiers.md) · [Quiz](../quizzes/quiz-07.md)

## Brief

Take one image-classification task from the labs and answer a single question with evidence:
**which component of the model actually causes the improvement?**

This is an ablation study, not a leaderboard attempt. A good submission contains one clean baseline,
one factor changed at a time, several seeds, and a table whose rows you can defend line by line.

## Requirements

1. **Task and data.** Use `deep_data.pattern_images` or `deep_data.plant_images`, a fixed split, and a
   stated seed policy. If you use a real dataset instead, document the licence and the split.
2. **Baseline.** A model with no tricks: no dropout, no batch norm changes, no augmentation, Adam at
   `1e-3`, early stopping on validation loss.
3. **Ablations.** At least **four** of the following, one at a time from the baseline:
   - dropout (0.0 vs 0.2 vs 0.4)
   - weight decay (0 vs 1e-4 vs 1e-2)
   - batch normalisation on/off
   - wider vs deeper (`width` 8/16/32, or an extra convolutional block)
   - learning rate (1e-4, 1e-3, 1e-2)
   - label noise (0%, 10%, 25% flipped labels) to test robustness
   - pretraining from another task, frozen vs fine-tuned
4. **Seeds.** Every configuration with **three seeds**; report mean ± standard deviation. A single
   run is not a result.
5. **Metrics.** Accuracy plus macro F1 on the held-out test split, parameters, and training seconds.
6. **Error analysis.** Confusion matrix for the best configuration, and at least three inspected
   failure cases with a sentence each on the likely cause.
7. **Conclusion.** Which factor mattered most, which did nothing, and what you would do next with
   more time.

## Suggested structure

| Section | Content | Length |
| :--- | :--- | :--- |
| 1. Question | One sentence: what are you ablating and why | 2–3 lines |
| 2. Setup | Data, split, seeds, budget, hardware | 1 paragraph |
| 3. Baseline | Configuration and result | 1 paragraph + table row |
| 4. Ablations | Table of mean ± std, one row per configuration | Table |
| 5. Analysis | What each row implies; which differences exceed seed noise | 3–4 paragraphs |
| 6. Error analysis | Confusion matrix, three failure cases | Figure + bullets |
| 7. Limitations | Compute, synthetic data, single task | 1 paragraph |
| 8. Appendix | How to run the code | Commands |

## Worked example of the table

Illustrative numbers from an ablation already run in this module (label-noise study on an 8×8 digit
classifier): clean baseline 0.760 train / 0.870 test; with 25% flipped labels the same model scored
0.710 / 0.890 with dropout and 0.703 / 0.874 with weight decay. Those runs show how a robustness
claim should be phrased — with both splits and the intervention named. Do not reuse these numbers as
your own; produce yours.

## Marking rubric

| Criterion | Weight | What full marks looks like |
| :--- | ---: | :--- |
| Correct, matched baseline | 15% | Same data, budget and seed policy as every other row |
| Ablation design | 20% | One factor at a time; sensible levels; a stated hypothesis per ablation |
| Statistical honesty | 20% | Three seeds, mean ± std, differences smaller than the spread called out as inconclusive |
| Error analysis | 20% | Confusion matrix plus inspected failures with plausible causes |
| Report quality | 15% | Reproducible commands, figures with axis labels, claims limited to the evidence |
| Code quality | 10% | Functions, seeds, no notebooks-as-scripts, deterministic runs |

## Submission checklist

- [ ] `ablation.py` runs end to end from a clean checkout in under 10 minutes on CPU.
- [ ] `results.csv` contains every configuration × seed.
- [ ] Report is self-contained: a reader who has not run the code can follow the argument.
- [ ] No test data used for model selection.
- [ ] Licences and dataset provenance stated.

## Extensions (optional, not graded)

- Repeat the best configuration on a real dataset (MNIST or Fashion-MNIST via `load_idx_images`).
- Add a learning-rate schedule (cosine) as a fifth factor.
- Measure inference latency on CPU for each configuration.
- Turn the study into a mini model card (see LAB-07-02 deliverables).

## Common pitfalls

- Changing two factors in one row, then attributing the effect to one of them.
- Reporting the best seed.
- Stopping on the test split ("I picked the epoch with the best test accuracy").
- Quoting three-decimal differences when the seed spread is two points.
- Confusing parameters with compute: a wider model has more parameters but may train faster per
  epoch than a deeper one.
