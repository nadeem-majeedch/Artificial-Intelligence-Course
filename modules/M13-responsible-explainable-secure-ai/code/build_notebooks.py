"""build_notebooks.py -- regenerate and execute NB-13-01 (M13).

Follows the M11 pattern: build the notebook with nbformat, execute it with nbclient from the
code directory, then strip outputs so the committed file stays small and diffable.

    python build_notebooks.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

HERE = Path(__file__).resolve().parent
NOTEBOOKS = HERE.parent / "notebooks"
TARGET = NOTEBOOKS / "nb-13-01-explainability-toolkit.ipynb"

CELLS = [
    ("markdown", """# NB-13-01 — An Explainability Toolkit

Build six explanation methods on the synthetic student data, then evaluate them: fidelity,
stability and a label-shuffling sanity check.

Every number printed here appears in L13-02. The methods are implemented from scratch; the
`shap` and `lime` packages are not required (compare against them as an exercise).

Run time on a 4-core laptop: about 10 seconds."""),
    ("code", """import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import explain as X
from rai_data import student

d = student()
Xf, y, names = d["X"], d["y"], d["feature_names"]
X_tr, X_te, y_tr, y_te = train_test_split(Xf, y, test_size=0.3, random_state=0, stratify=y)
print("train", X_tr.shape, "test", X_te.shape, "features", names)"""),
    ("markdown", """## 1. Two models, same features

The interpretable model is the explanation. The black box exists to show what post-hoc methods
cost."""),
    ("code", """lr = LogisticRegression(max_iter=2000).fit(X_tr, y_tr)
gb = GradientBoostingClassifier(n_estimators=80, max_depth=2, random_state=0).fit(X_tr, y_tr)

for name, m in (("logistic", lr), ("boosting", gb)):
    print(f"{name:10s} accuracy {X.accuracy_at_half(m, X_te, y_te):.3f}  AUC {X.auc(m, X_te, y_te):.3f}")

print("\\nlogistic coefficients (the explanation):")
for n, c in sorted(zip(names, lr.coef_[0]), key=lambda kv: -abs(kv[1])):
    print(f"  {n:20s} {c:+.3f}")"""),
    ("markdown", """## 2. Permutation importance

AUC drop when a feature is shuffled, five repeats. Correlated features split credit, which is
why attendance looks unimportant."""),
    ("code", """for row in X.permutation_importance(gb, X_te, y_te, names, n_repeats=5):
    print(f"{row['feature']:20s} {row['mean_drop']:+.4f}  (sd {row['std']:.4f})")"""),
    ("markdown", """## 3. Partial dependence

Average prediction as attendance sweeps its observed range."""),
    ("code", """j = names.index("attendance_rate")
grid, values = X.partial_dependence(gb, X_te, j, n_grid=6)
for g, v in zip(grid, values):
    print(f"attendance {g:.2f} -> mean predicted pass {v:.3f}")"""),
    ("markdown", """## 4. Exact Shapley values

Enumerate all $2^4$ coalitions. The efficiency check `sum(phi) == f(x) - E[f]` is the test that
catches a broken implementation."""),
    ("code", """probs = X.probability(gb, X_te)
idx = int(np.argsort(np.abs(probs - 0.5))[0])
x = X_te[idx]
print(f"instance {idx}, predicted {probs[idx]:.3f}")

sh = X.shapley_values(gb, x, X_tr, names)
print(f"base {sh['base_value']:.4f}  sum(phi) {sh['sum_phi']:+.4f}  "
      f"expected {sh['expected_sum']:+.4f}  gap {sh['efficiency_gap']:.2e}")
for f, v in zip(sh["features"], sh["values"]):
    print(f"  {f:20s} {v:+.4f}")"""),
    ("markdown", """## 5. LIME and its fidelity

Fidelity is the number most reports omit. A local $R^2$ of 0.26 means the linear story explains a
quarter of the black box's local behaviour."""),
    ("code", """lim = X.lime_tabular(gb, x, X_tr, names)
for f, v in zip(lim["features"], lim["values"]):
    print(f"  {f:20s} {v:+.3f}")
print(f"local R^2 {lim['local_r2']:.3f}")

stab = X.explanation_stability(gb, x, X_tr, names)
print(f"stability over 5 seeds: mean r {stab['mean_correlation']:.3f} "
      f"(min {stab['min']:.3f}, max {stab['max']:.3f})")
print("\\nShapley vs LIME ranking:")
print("  shapley:", sh["features"])
print("  lime   :", lim["features"])"""),
    ("markdown", """## 6. Counterfactual

The nearest input change that flips the decision. Report the distance: a decision that turns on
0.03 standard deviations is fragile."""),
    ("code", """p = float(X.probability(gb, x[None, :])[0])
cf = X.counterfactual(gb, x, X_tr, names, desired=1 if p < 0.5 else 0)
print("found:", cf["found"])
if cf["found"]:
    for ch in cf["changes"]:
        print(f"  {ch['feature']:20s} {ch['from']:.2f} -> {ch['to']:.2f}")
    print(f"  distance {cf['distance']:.3f} sd, new probability {cf['new_probability']:.3f}")"""),
    ("markdown", """## 7. Sanity check

Retrain on shuffled labels. A correct method must collapse to near-zero importance."""),
    ("code", """chk = X.sanity_check(Xf, y, names)
print(f"real      AUC {chk['real_auc']:.3f}  max importance {chk['real_max']:+.4f}")
print(f"shuffled  AUC {chk['shuffled_auc']:.3f}  max importance {chk['shuffled_max']:+.4f}")
assert chk["real_max"] > 5 * chk["shuffled_max"], "importance method may be measuring the data"
print("\\npass: real importance exceeds shuffled by more than 5x")"""),
    ("markdown", """## Exercises

1. Replace exact enumeration with a sampled KernelSHAP and plot the efficiency gap against the
   number of samples. How many samples do you need before the gap falls below 0.01?
2. Raise LIME's `n_samples` to 4000. Report the change in local $R^2$ and stability.
3. Find the instance furthest from the decision boundary and repeat sections 4–6. Which
   explanation changes most?
4. Add a fifth feature that is a copy of `attendance_rate` plus noise. What happens to both
   features' Shapley values, and to permutation importance?
5. Run the sanity check with a model trained on 5% of the data. Does the shuffled-label
   importance stay near zero?"""),
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
    client = NotebookClient(nb, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": str(HERE)}})
    client.execute()
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    TARGET.write_text(nbformat.writes(nb) + "\n", encoding="utf-8")
    return TARGET


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes, outputs stripped)")
