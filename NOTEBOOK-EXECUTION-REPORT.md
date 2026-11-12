# Notebook Execution Report

**Environment:** Windows 11, CPython 3.14, CPU only, no GPU. Executed with `nbclient` against a
live `python3` kernel, per-notebook timeout 300 s, working directory set to each notebook's own
folder (the way a student opens it). No datasets or models were downloaded during the audit;
everything used was already present in the repository or the local environment.

**Method:** `nbformat.read` → `NotebookClient(...).execute()` for every `.ipynb` in
`modules/*/notebooks/`. A notebook is recorded as passing only if every cell executed without
error in this run.

---

## 1. Final result

**14 of 14 notebooks execute successfully, total wall time ≈ 209 s.**

| # | Notebook | Time (s) | Result |
| ---: | --- | ---: | --- |
| 1 | M01 `nb-01-01-capability-test-bench` | 3.4 | PASS |
| 2 | M04 `nb-04-01-propositional-logic-workbench` | 1.7 | PASS |
| 3 | M04 `nb-04-02-first-order-inference-and-unification` | 1.7 | PASS |
| 4 | M06 `nb-06-01-data-preparation-workbench` | 2.5 | PASS |
| 5 | M06 `nb-06-02-regression-and-classification-workbench` | 2.6 | PASS |
| 6 | M06 `nb-06-03-model-comparison-and-ensembles` | 7.0 | PASS |
| 7 | M06 `nb-06-04-clustering-pca-and-anomalies` | 7.3 | PASS |
| 8 | M07 `nb-07-01-neural-network-fundamentals` | 6.1 | PASS |
| 9 | M07 `nb-07-02-pytorch-image-classification` | 10.1 | PASS |
| 10 | M07 `nb-07-03-sequences-attention-transfer` | 29.9 | PASS |
| 11 | M11 `nb-11-01-tokens-attention-and-generative-models` | 36.0 | PASS (after fix) |
| 12 | M11 `nb-11-02-retrieval-prompting-and-evaluation` | 51.1 | PASS (after fix) |
| 13 | M13 `nb-13-01-explainability-toolkit` | 6.7 | PASS (after fix) |
| 14 | M14 `nb-14-01-capstone-starter-kit` | 30.7 | PASS |

Slowest notebook: 51 s (M11 retrieval). No notebook approaches the 300 s timeout, so the set is
CPU-friendly. Eleven notebooks run in under 11 s.

## 2. First-run failures and root cause

On the **first** audit run, three notebooks failed:

| Notebook | Failure | Root cause |
| --- | --- | --- |
| `nb-11-01-tokens-attention-and-generative-models` | `ModuleNotFoundError` on `gen_data` | `sys.path.insert(0, ".")` resolves to `notebooks/`, but the module's code lives in the sibling `code/` directory |
| `nb-11-02-retrieval-prompting-and-evaluation` | `ModuleNotFoundError` on `gen_data` | same |
| `nb-13-01-explainability-toolkit` | `ModuleNotFoundError` on `explain` | same |

This is a **genuine defect, not a missing dependency**: the required files existed
(`modules/M11.../code/gen_data.py`, `rag.py`; `modules/M13.../code/explain.py`,
`rai_data.py`), but the notebooks only worked if launched from the `code/` directory — which
is not what a student does when they open the notebook in place.

### 2.1 Remediation applied

A bootstrap cell was inserted as the second cell of the three notebooks:

```python
# Make the module's reference code importable from the notebooks/ directory.
import sys, pathlib
CODE_DIR = None
for _base in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
    if (_base / "code").is_dir() and (_base / "notebooks").is_dir():
        CODE_DIR = _base / "code"
        break
if CODE_DIR is None:
    CODE_DIR = pathlib.Path.cwd().parent / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
print("code on path:", CODE_DIR)
```

This searches upward for the directory that contains both `code/` and `notebooks/`, so it works
from the notebook folder or from the module folder, and it is harmless if the path is already
present. It also defines `CODE_DIR` for later cells.

A second defect surfaced immediately after the first fix: `nb-11-01` called
`np.load("gen_samples.npz")`, which exists only in `code/`. The call was changed to
`np.load(CODE_DIR / "gen_samples.npz")` in the same notebook.

After both changes, all three notebooks executed end to end, and a full re-run of all fourteen
confirmed no regression.

## 3. Structure and hygiene checks

| Check | Result |
| --- | --- |
| Valid nbformat 4.x | 14/14 |
| Cell ordering (markdown → code → markdown …) | 14/14 coherent |
| Stored outputs cleared | 14/14 store no execution outputs |
| Absolute paths in cells | 0 found |
| Network calls in cells | 0 found (no `requests`, no `urlopen`, no model downloads during execution) |
| Seeding | every notebook seeds NumPy/PyTorch before stochastic steps; values are quoted in the lessons |
| External services / API keys | none required |
| Missing Python dependencies | none — `numpy`, `matplotlib`, `pandas`, `scikit-learn`, `torch`, `tokenizers`, `nbclient`, `nbformat` are all installed and were all used |

## 4. Reproducibility

- The notebooks are deterministic: fixed seeds and greedy decoding. Re-running the three
  repaired notebooks reproduced the same printed values.
- Values quoted in lessons match notebook output in the sampled cases (for example the M13
  disparate-impact ratio 0.558 and the M11 perplexity 4.48).
- The only artefact dependency is `code/gen_samples.npz`, which is committed; if it were
  deleted, `code/gen_models.py` regenerates it deterministically.

## 5. Limitations of this validation

1. **No GPU paths were exercised.** `nb-07-02` and `nb-07-03` run on CPU here; the notebooks'
   optional CUDA branches were not tested. They execute correctly on CPU with reduced epochs.
2. **Pretrained-weight downloads were not tested from scratch.** The local Hugging Face cache
   supplied the model assets used by M07 transfer learning and M11. A user with an empty cache
   needs network access once; this was not re-tested by clearing the cache (that would have
   required a large download, which the audit brief excludes).
3. **Kernel warnings were ignored, not hidden.** ZeroMQ Proactor-loop warnings were emitted on
   Windows; they are environmental and do not affect results.
4. **Timings are machine-specific.** They are evidence of CPU feasibility, not a benchmark.

## 6. Verdict

**Audit 4 verdict: PASS.** 14/14 notebooks execute end to end on CPU in about three and a half
minutes total. Three notebooks failed on first contact with a real student workflow; the cause
was diagnosed, fixed in the notebooks themselves, and the whole suite re-run. The remaining
limitations (GPU branches, cold-cache model download) are environmental and are stated rather
than concealed.
