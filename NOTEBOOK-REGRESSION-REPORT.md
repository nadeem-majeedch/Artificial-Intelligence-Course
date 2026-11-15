# Notebook Regression Report — Phase 23

**Date:** 12 November 2026 · **Method:** every notebook in the repository executed in a
clean kernel with `nbclient` (300 s per-cell timeout, working directory set to the
notebook folder, `kernelspec` forced to the local `python3`), then re-written with the new
outputs. The template notebook under `templates/` is excluded: it is a skeleton for authors, not
student material.

**Totals:** 35 notebooks, 31 PASS, 4 PASS WITH WARNINGS, 0 BLOCKED, 0 FAIL. Wall-clock 477.9 s on CPU only.

## Per-notebook results

| # | Notebook | Module | Status | Time (s) | Cells | Code cells | Errors |
| ---: | :--- | :--- | :--- | ---: | ---: | ---: | :--- |
| 1 | `nb-01-01-capability-test-bench.ipynb` | M01 | PASS | 4.1 | 32 | 13 | none |
| 2 | `nb-02-01-agent-loop-gridworld.ipynb` | M02 | PASS | 1.9 | 15 | 7 | none |
| 3 | `nb-03-01-search-workbench.ipynb` | M03 | PASS | 3.0 | 18 | 9 | none |
| 4 | `nb-04-01-propositional-logic-workbench.ipynb` | M04 | PASS | 2.0 | 27 | 11 | none |
| 5 | `nb-04-02-first-order-inference-and-unification.ipynb` | M04 | PASS | 1.9 | 23 | 9 | none |
| 6 | `nb-05-01-uncertainty-workbench.ipynb` | M05 | PASS | 1.9 | 19 | 9 | none |
| 7 | `nb-05-02-variable-elimination.ipynb` | M05 | PASS | 2.1 | 17 | 8 | none |
| 8 | `nb-06-01-data-preparation-workbench.ipynb` | M06 | PASS | 3.2 | 26 | 11 | none |
| 9 | `nb-06-02-regression-and-classification-workbench.ipynb` | M06 | PASS | 3.2 | 20 | 9 | none |
| 10 | `nb-06-03-model-comparison-and-ensembles.ipynb` | M06 | PASS | 8.5 | 16 | 7 | none |
| 11 | `nb-06-04-clustering-pca-and-anomalies.ipynb` | M06 | PASS | 8.9 | 18 | 8 | none |
| 12 | `nb-07-01-neural-network-fundamentals.ipynb` | M07 | PASS | 7.5 | 17 | 6 | none |
| 13 | `nb-07-02-pytorch-image-classification.ipynb` | M07 | PASS | 11.8 | 16 | 8 | none |
| 14 | `nb-07-03-sequences-attention-transfer.ipynb` | M07 | PASS WITH WARNINGS | 43.2 | 17 | 7 | none |
| 15 | `nb-08-01-tokenisation-and-features.ipynb` | M08 | PASS | 5.8 | 15 | 7 | none |
| 16 | `nb-08-02-classification-and-ner.ipynb` | M08 | PASS | 5.4 | 15 | 7 | none |
| 17 | `nb-08-03-attention-and-sequences.ipynb` | M08 | PASS | 2.6 | 13 | 6 | none |
| 18 | `nb-09-01-image-processing.ipynb` | M09 | PASS | 11.1 | 20 | 9 | none |
| 19 | `nb-09-02-cnn-classification.ipynb` | M09 | PASS | 15.2 | 17 | 8 | none |
| 20 | `nb-09-03-object-detection.ipynb` | M09 | PASS | 11.2 | 15 | 7 | none |
| 21 | `nb-09-04-image-segmentation.ipynb` | M09 | PASS | 22.9 | 15 | 7 | none |
| 22 | `nb-10-01-mdps-and-dynamic-programming.ipynb` | M10 | PASS | 7.6 | 13 | 6 | none |
| 23 | `nb-10-02-tabular-control-sarsa-and-q-learning.ipynb` | M10 | PASS WITH WARNINGS | 10.7 | 13 | 6 | none |
| 24 | `nb-10-03-deep-reinforcement-learning.ipynb` | M10 | PASS | 16.5 | 13 | 6 | none |
| 25 | `nb-11-01-tokens-attention-and-generative-models.ipynb` | M11 | PASS WITH WARNINGS | 99.8 | 14 | 7 | none |
| 26 | `nb-11-02-retrieval-prompting-and-evaluation.ipynb` | M11 | PASS WITH WARNINGS | 73.6 | 14 | 7 | none |
| 27 | `nb-12-01-agentic-ai-workbench.ipynb` | M12 | PASS | 2.4 | 31 | 15 | none |
| 28 | `nb-13-01-explainability-toolkit.ipynb` | M13 | PASS | 10.0 | 18 | 9 | none |
| 29 | `nb-14-01-capstone-starter-kit.ipynb` | M14 | PASS | 46.2 | 15 | 7 | none |
| 30 | `nb-p01-01-python-fundamentals.ipynb` | P01 | PASS | 3.3 | 33 | 18 | none |
| 31 | `nb-p01-02-numpy-pandas-plotting.ipynb` | P01 | PASS | 7.0 | 28 | 16 | none |
| 32 | `nb-p02-01-linear-algebra.ipynb` | P02 | PASS | 3.7 | 27 | 15 | none |
| 33 | `nb-p02-02-calculus-and-optimization.ipynb` | P02 | PASS | 4.4 | 25 | 13 | none |
| 34 | `nb-p03-01-probability-and-statistics.ipynb` | P03 | PASS | 7.8 | 30 | 17 | none |
| 35 | `nb-p04-01-data-preparation.ipynb` | P04 | PASS | 7.5 | 26 | 14 | none |

## Warnings

### `nb-07-03-sequences-attention-transfer.ipynb`

- C:\Users\Nadeem\AppData\Roaming\Python\Python314\site-packages\torch\nn\modules\transformer.py:533: UserWarning: The PyTorch API of nested tensors is in prototy

### `nb-10-02-tabular-control-sarsa-and-q-learning.ipynb`

- C:\Users\Nadeem\AppData\Local\Temp\ipykernel_7660\520285934.py:6: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown

### `nb-11-01-tokens-attention-and-generative-models.ipynb`

- C:\Users\Nadeem\AppData\Roaming\Python\Python314\site-packages\tqdm\auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See http
- Loading weights:   0%|          | 0/76 [00:00<?, ?it/s]
- Loading weights:  30%|███       | 23/76 [00:00<00:00, 179.98it/s]
- Loading weights:  54%|█████▍    | 41/76 [00:00<00:00, 86.88it/s]
- Loading weights: 100%|██████████| 76/76 [00:00<00:00, 173.67it/s]

### `nb-11-02-retrieval-prompting-and-evaluation.ipynb`

- C:\Users\Nadeem\AppData\Roaming\Python\Python314\site-packages\tqdm\auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See http
- Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
- Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]
- Loading weights: 100%|██████████| 103/103 [00:00<00:00, 3154.83it/s]
- Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]

## Runtime dependencies

| Package | Notebooks |
| :--- | ---: |
| `matplotlib` | 18 |
| `sklearn` | 6 |
| `pandas` | 5 |
| `datasets` | 4 |
| `torch` | 3 |
| `gymnasium` | 1 |

**Network use:** no notebook imports an HTTP client directly.
Two M11 notebooks load pretrained weights through `transformers`, which downloads from the
Hugging Face Hub on first run and caches under the user profile; the run recorded here reused a
local cache (the log shows "Loading weights" with no download failure, and one unauthenticated-request
warning). A machine with no network and an empty cache would show those two as BLOCKED, not PASS.

## Reading the results

- **PASS** means every code cell executed and produced no error output.
- **PASS WITH WARNINGS** means execution succeeded but the notebook printed a warning or logged a
  non-fatal stderr message. The four cases are a PyTorch nested-tensor prototype notice, a
  non-interactive matplotlib backend notice, and two Hugging Face/tqdm notices — none affects a result.
- Successful execution is **not** evidence that a notebook's numbers are correct; that evidence
  comes from `MATHEMATICAL-VERIFICATION-REPORT.md` and the module self-tests.
- No notebook was classified PASS without being executed in this run.

## Limitations

- Runs are on Windows 11, Python 3.14, CPU only (no CUDA), with the library versions in
  `README.md`. Runtimes on other hardware will differ; they are reported to show order of
  magnitude, not as a benchmark.
- The 300 s per-cell limit is generous for this material; no cell came close to it.
- Notebook outputs were overwritten by this run, so the stored outputs now correspond to this
  execution rather than to earlier sessions.
