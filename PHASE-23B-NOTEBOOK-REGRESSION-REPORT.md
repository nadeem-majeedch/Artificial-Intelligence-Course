# PHASE 23B — Notebook Regression Report

**Method:** every `.ipynb` in the repository was executed in a fresh Jupyter kernel with
`nbclient` (300 s per-cell timeout), using `audit/notebook_runner_phase23b.py`. Unlike the
Phase 23 runner, this one does **not** write executed outputs back into the notebooks; the
repository's notebook files were not modified by this audit. Results:
`audit/phase23b_notebook_results.json`.

**Totals:** 36 notebooks found (35 course notebooks + `templates/notebook.ipynb`),
**0 failures**, **473.3 s** total, 2 notebooks with warnings (both progress-bar / Hub
notices, not errors).

---

## 1. Results

| Notebook | Status | Time | Code cells |
| --- | --- | ---: | ---: |
| `modules/M01-introduction-and-foundations/notebooks/nb-01-01-capability-test-bench.ipynb` | PASS | 3.6 s | 13 |
| `modules/M02-intelligent-agents-and-environments/notebooks/nb-02-01-agent-loop-gridworld.ipynb` | PASS | 1.7 s | 7 |
| `modules/M03-problem-solving-and-search-algorithms/notebooks/nb-03-01-search-workbench.ipynb` | PASS | 2.7 s | 9 |
| `modules/M04-knowledge-representation-and-logical-reasoning/notebooks/nb-04-01-propositional-logic-workbench.ipynb` | PASS | 1.7 s | 11 |
| `modules/M04-knowledge-representation-and-logical-reasoning/notebooks/nb-04-02-first-order-inference-and-unification.ipynb` | PASS | 1.7 s | 9 |
| `modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/notebooks/nb-05-01-uncertainty-workbench.ipynb` | PASS | 1.7 s | 9 |
| `modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/notebooks/nb-05-02-variable-elimination.ipynb` | PASS | 1.8 s | 8 |
| `modules/M06-machine-learning-fundamentals/notebooks/nb-06-01-data-preparation-workbench.ipynb` | PASS | 2.8 s | 11 |
| `modules/M06-machine-learning-fundamentals/notebooks/nb-06-02-regression-and-classification-workbench.ipynb` | PASS | 2.9 s | 9 |
| `modules/M06-machine-learning-fundamentals/notebooks/nb-06-03-model-comparison-and-ensembles.ipynb` | PASS | 8.6 s | 7 |
| `modules/M06-machine-learning-fundamentals/notebooks/nb-06-04-clustering-pca-and-anomalies.ipynb` | PASS | 9.4 s | 8 |
| `modules/M07-neural-networks-and-deep-learning/notebooks/nb-07-01-neural-network-fundamentals.ipynb` | PASS | 8.0 s | 6 |
| `modules/M07-neural-networks-and-deep-learning/notebooks/nb-07-02-pytorch-image-classification.ipynb` | PASS | 12.1 s | 8 |
| `modules/M07-neural-networks-and-deep-learning/notebooks/nb-07-03-sequences-attention-transfer.ipynb` | PASS | 48.4 s | 7 |
| `modules/M08-natural-language-processing/notebooks/nb-08-01-tokenisation-and-features.ipynb` | PASS | 5.5 s | 7 |
| `modules/M08-natural-language-processing/notebooks/nb-08-02-classification-and-ner.ipynb` | PASS | 5.1 s | 7 |
| `modules/M08-natural-language-processing/notebooks/nb-08-03-attention-and-sequences.ipynb` | PASS | 2.1 s | 6 |
| `modules/M09-computer-vision/notebooks/nb-09-01-image-processing.ipynb` | PASS | 12.2 s | 9 |
| `modules/M09-computer-vision/notebooks/nb-09-02-cnn-classification.ipynb` | PASS | 17.9 s | 8 |
| `modules/M09-computer-vision/notebooks/nb-09-03-object-detection.ipynb` | PASS | 13.0 s | 7 |
| `modules/M09-computer-vision/notebooks/nb-09-04-image-segmentation.ipynb` | PASS | 26.4 s | 7 |
| `modules/M10-reinforcement-learning/notebooks/nb-10-01-mdps-and-dynamic-programming.ipynb` | PASS | 8.2 s | 6 |
| `modules/M10-reinforcement-learning/notebooks/nb-10-02-tabular-control-sarsa-and-q-learning.ipynb` | PASS | 9.9 s | 6 |
| `modules/M10-reinforcement-learning/notebooks/nb-10-03-deep-reinforcement-learning.ipynb` | PASS | 19.2 s | 6 |
| `modules/M11-generative-ai-and-large-language-models/notebooks/nb-11-01-tokens-attention-and-generative-models.ipynb` | PASS WITH WARNINGS | 79.7 s | 7 |
| `modules/M11-generative-ai-and-large-language-models/notebooks/nb-11-02-retrieval-prompting-and-evaluation.ipynb` | PASS WITH WARNINGS | 73.7 s | 7 |
| `modules/M12-ai-agents-and-agentic-systems/notebooks/nb-12-01-agentic-ai-workbench.ipynb` | PASS | 2.2 s | 15 |
| `modules/M13-responsible-explainable-secure-ai/notebooks/nb-13-01-explainability-toolkit.ipynb` | PASS | 8.9 s | 9 |
| `modules/M14-advanced-ai-applications-and-capstone/notebooks/nb-14-01-capstone-starter-kit.ipynb` | PASS | 47.5 s | 7 |
| `prerequisites/P01-python-programming/notebooks/nb-p01-01-python-fundamentals.ipynb` | PASS | 3.2 s | 18 |
| `prerequisites/P01-python-programming/notebooks/nb-p01-02-numpy-pandas-plotting.ipynb` | PASS | 7.1 s | 16 |
| `prerequisites/P02-mathematics-for-ai/notebooks/nb-p02-01-linear-algebra.ipynb` | PASS | 3.8 s | 15 |
| `prerequisites/P02-mathematics-for-ai/notebooks/nb-p02-02-calculus-and-optimization.ipynb` | PASS | 4.5 s | 13 |
| `prerequisites/P03-probability-and-statistics/notebooks/nb-p03-01-probability-and-statistics.ipynb` | PASS | 7.0 s | 17 |
| `prerequisites/P04-data-preparation-and-visualization/notebooks/nb-p04-01-data-preparation.ipynb` | PASS | 5.5 s | 14 |
| `templates/notebook.ipynb` (template, not a lesson notebook) | PASS | 3.6 s | 7 |

The task brief expected 35 notebooks; the repository contains 36 because the template is
also a valid notebook and Phase 23A counted 35 course notebooks. Excluding the template:
**35 course notebooks — 33 PASS, 2 PASS WITH WARNINGS, 0 FAIL**.

## 2. Warnings: what they are and whether they matter

Both warning notebooks are M11 and both produced the same two classes of message:

1. `tqdm` progress bars emitted by `transformers` while loading weights
   (`Loading weights: 100%|████…`), plus a `TqdmWarning: IProgress not found` about
   `ipywidgets`. Cosmetic; the weights load and the cells complete.
2. `You are sending unauthenticated requests to the HF Hub…` in nb-11-02. Cosmetic and
   expected without `HF_TOKEN`; it does not indicate a failed download.

No error output, no traceback, and no cell exceeded the 300 s timeout.

## 3. External dependencies and offline behaviour

- **No notebook imports `requests`, `urllib`, `httpx`, `socket` or `wget` directly.** Any
  network use is indirect, through `transformers`.
- **M11 depends on pretrained checkpoints.** `code/llm_gen.py` and `code/attention_lab.py`
  call `AutoModelForCausalLM.from_pretrained("distilgpt2")` and the seq2seq loader for
  `flan-t5-small`; `lora.py` names `distilgpt2`. On a machine without a populated
  Hugging Face cache these notebooks require Internet access and roughly a few hundred MB
  of weights. This run used the existing local cache, so weight download was not exercised.
  No `local_files_only` / `HF_HUB_OFFLINE` fallback and no synthetic substitute was found
  for these paths; the rest of the course is offline-capable.
- **M07** uses the synthetic digit/texture data in `deep_data.py` and CPU PyTorch; no
  torchvision download is required for the executed path.
- **M09/M10/M14** use synthetic data and small CPU models; no dataset download occurred.
- **Notebook working directory** is the notebook's own folder, as intended: relative
  `code/` imports resolve. No notebook wrote into the repository during this audit
  (checked with a modification-time scan).

## 4. Output and numerical sanity

Error markers were absent; a scan for `NaN`/`inf` found only:

- `nb-06-01` printing `NaNs in train: 22` and then `NaNs after imputation: 0` — the
  intended missing-value demonstration, not a failure.
- Matches for the substring `" inf"` were English words ("inference") in markdown, not
  infinite values.

Outputs were not re-derived cell by cell. Numerical correctness of the underlying code is
covered separately by `audit/math_verify.py` (**32/32 checks passed** in this audit) and
by the pytest suite.

## 5. Limitations

- Execution used the machine's installed environment (Python 3.14, CPU torch, cached HF
  weights). A clean machine without those weights would fail the two M11 notebooks, and
  that limitation is not visible from the pass result.
- No notebook was executed twice to test cell-order independence or leftover state; each
  ran in its own fresh kernel, which is the stronger check for a reader.
- The total runtime (473 s) is machine-specific and should not be used as a performance
  benchmark.

## 6. Recommendation

Keep the offline paths as they are for M01–M10 and M12–M14. For M11, document the cache
requirement in the notebook header and add a small synthetic fallback (or an explicit
"download once" cell) so the notebooks fail with an instruction rather than a stack trace
on a disconnected machine.
