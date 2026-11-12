# MP-07 — Image Classifier Sprint

| Module | M07 · Artificial Neural Networks and Deep Learning |
| :--- | :--- |
| Type | Mini-project (pairs or individual) |
| Effort | ~2 hours core, up to 8 hours with the production extras |
| Deliverables | Working repository, short report, five-minute demo |
| Covers | L07-03 to L07-08 |

[← Module home](../README.md) · [Assignment](../assignments/asg-07-ablation-study.md) · [Summary](../summary.md)

## The brief

Ship a small image classifier that another person can run, evaluate and distrust appropriately.

You choose one of the three module tasks:

| Track | Data | Classes | Notes |
| :--- | :--- | :--- | :--- |
| A — Digits | `deep_data.digit_images` or real MNIST | 10 | easy, near-ceiling accuracy |
| B — Textures | `deep_data.pattern_images` or Fashion-MNIST | 10 | confusion structure is the interesting part |
| C — Plant disease | `deep_data.plant_images` or PlantVillage | 3 | cue dependence is the interesting part |

Track C is the best choice if you want the report to say something non-obvious.

## Required work

1. **Baseline first.** A model with no tricks, evaluated on a held-out test split, with the metric
   chosen from the decision the classifier supports.
2. **An improved model.** At least one architectural or training change, justified before it is run.
3. **Evidence.** Three seeds for baseline and improved model, mean ± std, parameters, training time.
4. **Error analysis.** Confusion matrix, per-class recall, three inspected failures.
5. **Save and load.** A checkpoint that reloads into a fresh process and reproduces the reported
   accuracy.
6. **Model card.** Intended use, out-of-scope use, training data and licence, metrics, known failure
   modes, and what monitoring you would add in production.
7. **Demo.** Five minutes: the problem, the baseline, the change, the evidence, the caveat.

## Milestones

| Time | Milestone | Exit criterion |
| :--- | :--- | :--- |
| 0:00–0:15 | Choose track, fix split and metric | Split written down; majority baseline computed |
| 0:15–0:45 | Baseline trained and evaluated | Reproducible run, three seeds |
| 0:45–1:15 | Improved model | At least one factor changed, same budget |
| 1:15–1:40 | Error analysis + checkpoint reload | Confusion matrix and three failures documented |
| 1:40–2:00 | Model card and demo prep | Report sections complete |

## Repository layout

```text
mp07/
  README.md            # how to run, in five commands or fewer
  data.py              # loader wrapper: synthetic or real, one flag
  model.py             # architectures
  train.py             # CLI: --track --seed --epochs --out
  evaluate.py          # confusion matrix, per-class recall, saves figures
  results/             # metrics.json, figures, checkpoint
  REPORT.md            # baseline vs improved, error analysis, model card
```

## Reproducibility requirements

- One command trains the model: `python train.py --track c --seed 0 --epochs 12`.
- Seeds are explicit and documented; `torch.use_deterministic_algorithms` is not required, but you
  must state that CPU runs vary slightly.
- No absolute paths. No downloads at import time.
- `results/metrics.json` records every configuration × seed.

## Grading

| Criterion | Weight |
| :--- | ---: |
| Baseline correctness and metric justification | 20% |
| Improvement measured against the baseline with seeds | 25% |
| Error analysis quality | 20% |
| Reproducibility (clean run, checkpoint reload) | 15% |
| Model card honesty and completeness | 15% |
| Demo clarity | 5% |

## Stretch goals

- Swap in a real dataset and report both synthetic and real numbers side by side.
- Pretrain on one track and fine-tune on another; report whether transfer helps and by how much.
- Add test-time augmentation and measure the accuracy/latency trade-off.
- Export the model with `torch.jit.trace` and compare inference latency.
- Add a simple confidence threshold that routes uncertain images to human review, and compute the
  review rate at 95% coverage.

## Anti-goals

These do not earn marks: a 1.000 accuracy on a synthetic dataset with no analysis; a table of five
architectures with no baseline; a notebook that cannot be re-run from top to bottom; claims about
real-world deployment from synthetic data.

## Presentation questions you should be able to answer

1. What decision does this classifier support, and what does a false negative cost?
2. What is the majority-class baseline on your test split?
3. Which change gave the largest improvement, and is it larger than the seed spread?
4. What are the three most likely ways this model fails in production?
5. What would you measure first if it underperformed next month?
