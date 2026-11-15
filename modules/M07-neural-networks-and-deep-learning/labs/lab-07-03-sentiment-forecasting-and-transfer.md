# LAB-07-03 — Sentiment, Forecasting and Transfer Learning

> **Module M07** · Lab 3 of 3 · ~150 minutes · Level 300
> **Scenarios:** 5 (review sentiment), 6 (LSTM demand forecasting), 7 (transfer learning)
> **Prerequisites:** L07-06, L07-07, L07-08 · **Pairs with:** NB-07-03

[Module overview](../README.md) · [Previous lab: LAB-07-02](lab-07-02-digital-fashion-and-plant-classifiers.md) · [Assignment: ASG-07 →](../assignments/asg-07-ablation-study.md)

Three sequence-and-transfer problems. The thread joining them is **evaluation honesty**: each has a
baseline that is easy to forget and that changes the conclusion when you include it.

---

## Scenario 5 — Review sentiment classification

### Problem description

Classify synthetic film-review sentences as positive or negative. Train a bag-of-words logistic
baseline, a GRU, and a tiny transformer, and compare all three with the majority-class rate.

### Business context

Routing customer reviews to a support queue by sentiment. The decision threshold, not the accuracy,
sets the operating cost: flagging negatives aggressively increases recall but floods the queue.
Prevalence matters — most reviews are positive, so a majority classifier already looks reasonable.

### Dataset source and licence

- **In this lab:** `code/deep_data.sentiment_data(n=1500, seed=0)` — synthetic sentences built from
  polar and neutral word lists, with the label decided by a majority vote of polar words. Generated
  in-script; the deliberate tie cases are the hard examples.
- **Real counterpart:** IMDB Large Movie Review Dataset (Maas et al., 2011). The dataset page states
  it is for **research use**; check the current terms before any commercial use. 50,000 reviews,
  balanced, with 25,000 labelled train examples.
- Do not report synthetic accuracy as an IMDB result; vocabulary size and sentence length differ by
  orders of magnitude.

### Dataset description

1,500 sentences, vocabulary 28 tokens, max length 12 after padding, class counts `[866, 634]`
(majority rate 0.578). Default split: 1,100 train / 400 test.

### Tasks

1. **Baseline.** Frequency-based logistic regression or a majority classifier. Record the accuracy.
2. **GRU.** Embedding (dim 16) → GRU (hidden 32) → linear. Train for up to 15 epochs with early
   stopping; report parameters and accuracy.
3. **Transformer.** `TinyTransformerClassifier(len(vocab)+1, max_len=12)`; 12 epochs, Adam at `1e-3`.
   Report parameters and accuracy.
4. **Error analysis.** List the misclassified sentences. How many are the deliberate polar-count
   ties? Does the model fail on negation ("not good")?
5. **Threshold trade-off.** Sweep the decision threshold over the positive-class probability and
   plot precision/recall for the test split.
6. **Comparison table.** Baseline, GRU, transformer: parameters, accuracy, training seconds, and a
   one-line verdict on which you would ship and why.

### Expected results

```text
vocab 28, encoded (1500, 12), class counts [866 634]
transformer params 9922, validation accuracy 0.990, majority baseline 0.578
```

The transformer reaches 0.99 on a task that is almost linear in the polar words. That is the honest
finding: the architecture is not the reason it works, the label rule is. On real IMDB the ordering
between GRU and transformer is far less predictable.

---

## Scenario 6 — Demand forecasting with an LSTM

### Problem description

Forecast the next value of a noisy seasonal series from the previous 24 observations. The baseline
is "repeat the last observed value". A model that cannot beat it has no business being deployed.

### Business context

Daily demand or server-load forecasting where the cost of being wrong is asymmetric. The naive
baseline is what the business currently uses, so it is the number to beat — not zero.

### Dataset source and licence

- **In this lab:** `code/deep_data.series_windows(n=800, window=24, horizon=1, seed=0)` — sine wave
  plus trend plus Gaussian noise. Generated in-script.
- **Real counterpart:** any public time series, e.g. the **M3/M4 competition datasets** or
  **UCI Electricity Load Diagrams** (CC BY 4.0). Keep the same windowing code; only the loader
  changes.

### Dataset description

800 windows, shape `(800, 24, 1)`, one scalar target each. Default split: 640 train / 160 test.

### Tasks

1. Train `LSTMRegressor(hidden_size=24)` with MSE loss, Adam at `0.01`, 25 epochs.
2. Compute the repeat-last baseline MSE on the same test windows.
3. Plot actual, LSTM and baseline forecasts for 120 test points.
4. Re-train with `horizon=3` and compute a 3-step repeat-last baseline. Does the LSTM still win?
5. Residual analysis: plot the error distribution and check for a pattern against the seasonal phase.
6. Try `hidden_size` 8, 24, 64. Plot test MSE against parameters.

### Expected results

```text
LSTM params 2617
LSTM MSE 0.0249 | repeat-last baseline MSE 0.5372
```

A 20× improvement over the naive baseline. One-step-ahead forecasting of a smooth series is an easy
problem; the multi-step horizon in task 4 is where error accumulation appears and where the LSTM's
advantage usually shrinks.

---

## Scenario 7 — Transfer learning with 60 labels

### Problem description

Build a three-class leaf-disease classifier with only 60 labelled images. Pretrain a CNN on 3,000
texture images, then compare frozen features, full fine-tuning and training from scratch over three
seeds and two dataset sizes.

### Business context

A agritech startup has thousands of unlabelled field photos but can only afford 60 expert labels.
The decision — ship a scratch model, a linear probe, or a fine-tuned model — depends on measured
evidence, not on folklore about transfer learning.

### Dataset source and licence

- **In this lab:** `code/deep_data.pattern_images` (source task) and `code/deep_data.plant_images`
  (target task), both synthetic and generated in-script.
- **Real counterpart:** pretrained ImageNet weights (licences vary by checkpoint and by training
  data) transferred to PlantVillage (CC BY-SA 3.0). Check both licences: dataset licence and
  weights licence are separate.
- `code/transfer.py` implements the whole experiment; read it before running it.

### Tasks

1. Run `python code/transfer.py` and reproduce the table.
2. Explain the head-swap mechanism: why does `strict=False` drop exactly two parameters?
3. Run the same sweep with 30 labelled images. How large is the gain, and how large is the
   seed-to-seed spread?
4. Repeat with digits (`dd.digit_images(2000, size=16)`) as the source task. Is this negative
   transfer? Justify with numbers.
5. Fine-tune at `lr=1e-2` and describe what happens in the first epoch.
6. Train an autoencoder on the 60 labelled leaves plus the unlabelled remainder, then use its latent
   code as features for a linear classifier. Does unlabelled data help?

### Expected results

```text
pretrained on textures: acc 1.000, params 38378
labels  scratch   frozen  finetune
    60    0.502    0.756     0.769
   150    0.938    0.836     0.947
```

Transfer wins clearly at 60 labels and is roughly level at 150. Frozen versus fine-tuned differs by
about a point — with 60 labels the head, not the features, is the bottleneck.

---

## Metrics summary

| Scenario | Primary | Baseline you must beat |
| :--- | :--- | :--- |
| Sentiment | accuracy, precision/recall at threshold | majority class (0.578) |
| Forecasting | MSE | repeat last value (0.5372) |
| Transfer | accuracy at fixed label budget | train from scratch, same budget |

## Deliverables

1. `sentiment_compare.py`, `forecast_lstm.py`, `transfer_sweep.py`.
2. Figures: threshold trade-off curve, forecast overlay, residual histogram, transfer bar chart with
   seed error bars.
3. `lab-07-03-report.md` — three sections, one per scenario, each ending with a ship/no-ship
   recommendation and the evidence behind it.

## Extensions

- Add positional encoding ablation to the transformer (remove positions, measure the accuracy drop).
- Replace the LSTM with a GRU and compare parameters and MSE.
- Use a causal-mask transformer for the forecasting task.
- Combine transfer and autoencoding: pretrain the encoder unsupervised on unlabelled leaves, then
  fine-tune with the 60 labels.

## Common pitfalls

- Comparing a model against zero error instead of the naive baseline.
- Tuning the threshold on the test split and reporting the tuned score as unbiased.
- Reporting a single-seed transfer result.
- Forgetting that the majority baseline moves when you change the split.

## Marking guide

| Criterion | Weight |
| :--- | ---: |
| Three pipelines reproduce the expected ranges | 25% |
| Correct baselines in all three scenarios | 20% |
| Seed and data-size sweep for transfer | 20% |
| Error/residual analysis quality | 20% |
| Recommendations justified by the numbers | 15% |

## Starter material

The guided notebook [`nb-07-03-sequences-attention-transfer.ipynb`](../notebooks/nb-07-03-sequences-attention-transfer.ipynb) works through the
same pipeline end to end; use it when you are stuck, and cite what you
changed rather than copying its outputs.

Module reference code: [`../code/`](../code/).
