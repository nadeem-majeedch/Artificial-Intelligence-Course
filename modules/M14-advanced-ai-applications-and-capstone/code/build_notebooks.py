"""build_notebooks.py -- regenerate and execute NB-14-01 (M14).

Same pattern as M11 and M13: build with nbformat, execute with nbclient from the code directory,
strip outputs so the committed notebook stays small and diffable.

    python build_notebooks.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

HERE = Path(__file__).resolve().parent
NOTEBOOKS = HERE.parent / "notebooks"
TARGET = NOTEBOOKS / "nb-14-01-capstone-starter-kit.ipynb"

CELLS = [
    ("markdown", """# NB-14-01 — Capstone Starter Kit

A small, complete slice of what a capstone needs: a leakage-free split, a baseline, a better
model, a per-class table, a size/latency measurement, and a drift monitor.

Every number printed here is reproducible by re-running the cells. Use this notebook as the spine
of your own project: replace the dataset, keep the evaluation discipline.

Runtime: about 15 seconds on a 4-core laptop."""),
    ("code", """import time

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split

d = load_digits()
X = (d.data / 16.0).astype(np.float32)
y = d.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print("train", Xtr.shape, "test", Xte.shape)
print("class counts (test):", np.bincount(yte, minlength=10).tolist())"""),
    ("markdown", """## 1. Baseline first

A trivial baseline is not optional: without it, no later number means anything. Logistic
regression on raw pixels is the standard method here."""),
    ("code", """t0 = time.perf_counter()
base = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
base_pred = base.predict(Xte)
print(f"logistic: macro F1 {f1_score(yte, base_pred, average='macro'):.3f} "
      f"({time.perf_counter() - t0:.1f} s fit)")

majority = np.full_like(yte, np.bincount(ytr).argmax())
print(f"majority class: macro F1 {f1_score(yte, majority, average='macro'):.3f}")"""),
    ("markdown", """## 2. A stronger model, with the same split

Gradient boosting on the same features. Report the comparison as a table, not a sentence."""),
    ("code", """gb = HistGradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
gb_pred = gb.predict(Xte)

for name, pred in (("logistic", base_pred), ("boosting", gb_pred)):
    print(f"{name:10s} macro F1 {f1_score(yte, pred, average='macro'):.3f}  "
          f"accuracy {(pred == yte).mean():.3f}")"""),
    ("markdown", """## 3. Per-class results

The aggregate hides where the model fails. Always print the per-class table."""),
    ("code", """print(classification_report(yte, gb_pred, digits=3, zero_division=0))

per_class = []
for c in range(10):
    mask = yte == c
    per_class.append((c, int(mask.sum()), float((gb_pred[mask] == c).mean())))
worst = min(per_class, key=lambda r: r[2])
print("worst class:", worst[0], "recall", round(worst[2], 3), "n", worst[1])"""),
    ("markdown", """## 4. Seed spread

A single run is a point estimate. Repeat with different seeds and report the spread: this is the
cheapest form of uncertainty."""),
    ("code", """scores = []
for seed in range(5):
    Xa, Xb, ya, yb = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    m = HistGradientBoostingClassifier(random_state=seed).fit(Xa, ya)
    scores.append(f1_score(yb, m.predict(Xb), average="macro"))
scores = np.array(scores)
print("macro F1 over 5 seeds:", np.round(scores, 3).tolist())
print(f"mean {scores.mean():.3f}  sd {scores.std():.3f}  "
      f"range {scores.min():.3f}-{scores.max():.3f}")
print("if two models differ by less than this spread, the difference is not established.")"""),
    ("markdown", """## 5. Size and latency

Two of the four columns a compression claim needs. `nbytes` is the honest size; parameter counts
mislead once weights are quantised (M14, L14-02)."""),
    ("code", """def model_bytes(model):
    total = 0
    for attr in ("coef_", "intercept_"):
        if hasattr(model, attr):
            total += np.asarray(getattr(model, attr)).nbytes
    return total

def latency_us(model, x, reps=500):
    for _ in range(20):
        model.predict(x)
    t0 = time.perf_counter()
    for _ in range(reps):
        model.predict(x)
    return (time.perf_counter() - t0) / reps * 1e6

for name, m in (("logistic", base), ("boosting", gb)):
    print(f"{name:10s} {model_bytes(m) / 1024:8.1f} KB  "
          f"{latency_us(m, Xte[:1]):8.1f} us/example")

print("\\nnote: sklearn models are not int8-quantised; this measures the pipeline, not quantisation.")"""),
    ("markdown", """## 6. Drift monitor

PSI between a reference sample and a shifted one. This is the leading indicator: it needs no
labels, so it fires before the error metric can."""),
    ("code", """def psi(ref, cur, bins=10):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    p = np.histogram(ref, bins=edges)[0] / len(ref)
    q = np.histogram(cur, bins=edges)[0] / len(cur)
    eps = 1e-6
    return float(np.sum((q - p) * np.log((q + eps) / (p + eps))))

feature = 0
ref = Xtr[:, feature]
for shift in (0.0, 0.5, 1.0, 2.0):
    cur = np.clip(ref + shift, 0, 1)
    v = psi(ref, cur)
    status = "stable" if v < 0.1 else "monitor" if v < 0.25 else "alert"
    print(f"shift {shift:.1f}  PSI {v:6.3f}  {status}")"""),
    ("markdown", """## 7. What a capstone still needs

This notebook has the spine. Your project adds:

1. **Your data**, with provenance and licence in the report.
2. **A split that matches deployment** — time, site or patient, not random.
3. **An error analysis** of three concrete failures.
4. **A limitation** traceable to a measurement.
5. **A failure condition**: what result would mean the project did not succeed.

See [`capstone/report-template.md`](../capstone/report-template.md) and the
[rubric](../capstone/rubric.md)."""),
]


def build() -> Path:
    NOTEBOOKS.mkdir(exist_ok=True)
    nb = new_notebook()
    nb.cells = [new_markdown_cell(src) if kind == "markdown" else new_code_cell(src)
                for kind, src in CELLS]
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    }
    NotebookClient(nb, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": str(HERE)}}).execute()
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    TARGET.write_text(nbformat.writes(nb) + "\n", encoding="utf-8")
    return TARGET


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes, outputs stripped)")
