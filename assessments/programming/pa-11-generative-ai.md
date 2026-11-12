# PA-11 — A Small Generative Model, Sampled Three Ways

| | |
| :--- | :--- |
| Assignment | 11 |
| Difficulty | Advanced |
| Estimated time | 5 hours |
| Prerequisites | M11 (L11-01 … L11-03), PA-07 |
| Covers | autoregressive models, sampling, temperature, evaluation of generative output |

[Assessment index](../README.md) · [Programming assignments](README.md)

## Background

Generative models are judged by samples, and samples are easy to over-interpret. This assignment
requires a model, three decoding strategies, and an evaluation that distinguishes "looks plausible"
from "covers the distribution".

## Problem scenario

Train a character-level autoregressive model on a small text corpus (a public-domain book or the
course's own generated text). Then sample with greedy, temperature and top-p decoding and compare.

## Learning outcomes

1. Implement a character-level model and training loop.
2. Explain and implement temperature and nucleus sampling.
3. Measure distribution coverage, not just sample plausibility.
4. Report the trade between diversity and coherence.

## Tasks

1. **Data.** Character vocabulary, train/validation split by contiguous blocks (not random).
2. **Model.** Small RNN or transformer; report parameter count and validation loss.
3. **Decoding.** Greedy, temperature ∈ {0.5, 1.0, 1.5}, top-p ∈ {0.9, 0.95}.
4. **Coverage.** For each setting, report distinct n-grams and the fraction of generated 4-grams that
   appear in the training corpus.
5. **Samples.** Ten samples per setting, fixed length; include two in the report.
6. **Verdict.** Which setting would you ship for a creative tool, and which for a factual one?

## Constraints

- CPU only; keep the model under 1M parameters.
- Fixed seed for every sample set.
- No pretrained weights.

## Expected deliverables

`charmodel.py`, `samples.md`, `results.md` with the coverage table, and the training curve.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Model and training | 25% | trains, validation loss reported |
| Decoding implementations | 25% | temperature and top-p correct |
| Evaluation | 30% | coverage measured, not eyeballed |
| Samples and verdict | 20% | choice justified by numbers |

## Bonus challenges

- Compute perplexity on held-out text and compare with the coverage results.
- Add repetition penalty and measure its effect on distinct n-grams.

---

[Assessment index](../README.md) · [PA-10](pa-10-reinforcement-learning.md) · [PA-12](pa-12-llm-applications.md)
