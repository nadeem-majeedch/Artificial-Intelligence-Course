# Phase 25 — Technical Verification

**Audit date:** 15 November 2026  
**Repository:** `C:\Users\Nadeem\Documents\Artificial-Intelligence-Course`  
**HEAD:** `fba4161aab98ebc3c3f8252d4a43e8e268b24b3c`  
**Remote:** `origin https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git`  
**Python:** 3.14 on Windows, PyTorch CPU, pytest 9.1.1

This report records what was executed and independently checked. It is not a substitute for the
academic review in `PHASE-25-FINAL-ACADEMIC-AUDIT.md`.

## 1. Repository inventory and state

| Item | Measured |
| :--- | :--- |
| Modules | 14 (`M01`–`M14`) |
| Lessons | 89 |
| Lab markdown files | 38 |
| Course notebooks | 35 (plus `templates/notebook.ipynb`, excluded from execution) |
| Test functions | 175, collected as 196 tests through parametrisation |
| Quizzes / self-assessments / solutions | 14 / 14 / 14 |
| Programming / analytical assignments | 14 / 8 |
| Module projects / capstone briefs | 8 module projects, 12 capstone briefs |
| Git status | 167 porcelain lines: 108 modified, 59 untracked, **0 staged**, no deletions |
| Tags | none |
| HEAD | `fba4161`; unchanged during the audit |

No tracked file was deleted. No staged change exists. The remote was not changed. No commit, push,
tag, release or deployment was performed.

### Generated/temporary artefacts found

- `.coverage` (untracked, root)
- `_hf_dl.log`, `_pip_cv2.log`, `_pip_gym.log`, `_pip_sp.log` (ignored logs, root)
- `__pycache__/` directories (ignored)
- `audit/*.json` and `audit/*.log` (untracked audit artefacts)

These are local artefacts, not course content. They should be removed or ignored before a public
commit at the owner's discretion. They do not affect execution.

## 2. Automated checks

| Check | Command | Exit | Result |
| :--- | :--- | ---: | :--- |
| Full pytest suite | `python -m pytest -q` | 0 | **196 passed** in 61.0 s |
| Compilation | `python -m compileall -q modules prerequisites tests audit` | 0 | no syntax errors |
| Course structure/links/anchors/CFF | `python audit/check_course.py` | 0 | 4,154 links, **0 broken**, 0 problems |
| Curriculum hours | `python audit/check_hours.py` | 0 | 0 failures |
| Licensing mechanics | `python audit/check_licensing.py` | 0 | 0 failures; explicitly mechanical only |
| Citation file | included in `check_course.py` | 0 | `CITATION.cff` parsed, 10 keys, 1 author |
| Graph experiment | `python modules/M14-.../code/graphs.py` | 0 | 147 s, results reproduce |
| Notebook regression | 35 notebooks, clean kernels, outputs not written back | 0 | 31 pass, 4 pass with warnings, **0 failures**, 500.1 s |

The link checker covers relative links and anchors across 4,154 links. The hour checker verifies
the four-component arithmetic, the 350.7 module total, 406.7 programme total, study paths and
stale-figure absence.

## 3. Independent mathematical and algorithmic verification

Each check used a reference that is not the production implementation as its own oracle: a hand
calculation, an independent NumPy implementation, brute-force enumeration, central finite
differences, or scikit-learn. The one exception is the alarm-network cross-check, where variable
elimination and enumeration share the same CPT constants; it is an algorithm cross-check, not an
independent derivation of the constants. All 34 checks passed.

| # | Algorithm / function | Input | Independent reference | Actual | Expected | Tolerance | Result |
| ---: | :--- | :--- | :--- | ---: | ---: | ---: | :--- |
| 1 | `uniform_cost` / Dijkstra | 6×6 weighted grid, start (0,0), goal (5,5) | own heapq Dijkstra | 41.0 | 41 | exact | PASS |
| 2 | `astar` | same grid, Manhattan h | own Dijkstra | 41.0 | 41 | exact | PASS |
| 3 | `bfs` | same grid, unit hops | Manhattan distance | 10 | 10 | exact | PASS |
| 4 | `unify_atoms` | `p(x,b)`, `p(a,y)` | hand MGU | `{x:a, y:b}` | `{x:a, y:b}` | exact | PASS |
| 5 | `unify` occurs check | `x`, `f(x)` | should fail | `None` | `None` | exact | PASS |
| 6 | `unify_atoms` mismatch | `p(x)`, `q(a)` | `None` | `None` | `None` | exact | PASS |
| 7 | Variable elimination | 3-variable custom net, `P(A)` | brute-force joint | 0.3000000000000 | 0.3 | 1e-12 | PASS |
| 8 | Variable elimination | custom net, `P(A|C=T)` | brute force | 0.8108108108 | 0.8108108108 | 1e-12 | PASS |
| 9 | Variable elimination | custom net, `P(B|C=T)` | brute force | 0.8243243243 | 0.8243243243 | 1e-12 | PASS |
| 10 | Variable elimination | custom net, `P(B|C=T,A=F)` | brute force | 0.5 | 0.5 | 1e-12 | PASS |
| 11 | Alarm VE | `P(B|J=T,M=T)` | module enumeration (same CPTs) | 0.2841718354 | 0.2841718354 | 1e-12 | PASS |
| 12 | Logistic regression dW | 4 samples, w=[0.3,−0.4], b=0.1 | central finite difference | [−0.07957147, 0.08205853] | same | 1e-6 | PASS |
| 13 | Logistic regression db | same | central finite difference | 0.0635992590 | 0.0635992590 | 1e-6 | PASS |
| 14 | MLP backprop | 3-4-2 tanh, `w2[1,0]` | central finite difference | 0.1692757204 | 0.1692757204 | 1e-6 | PASS |
| 15 | `edge_homophily` | 4-node path, labels 0,0,1,1 | hand: 4 same of 6 directed | 0.6666666667 | 0.6666666667 | 1e-12 | PASS |
| 16 | `normalise` | 4-node path | `D^-1/2 (A+I) D^-1/2` | max error 1.49e-8 | 0 | 1e-6 | PASS |
| 17 | GCN forward | fixed random weights, 2 layers | independent NumPy `A@X@W+ReLU` | max error 7.45e-9 | 0 | 1e-5 | PASS |
| 18 | SBM within-block rate | seed 3, `p_in=0.12` | a-priori sampling rate | 0.116923 | 0.12 | 0.02 | PASS |
| 19 | SBM cross-block rate | seed 3, `p_out=0.01` | a-priori sampling rate | 0.011 | 0.01 | 0.005 | PASS |
| 20 | Inductive fit adjacency | seed 3 test nodes | no test rows/columns except self-loop | 0.0 | 0.0 | 1e-9 | PASS |
| 21 | Inductive inference adjacency | seed 3 | test-test off-diagonal zero | 0.0 | 0.0 | 1e-9 | PASS |
| 22 | `iou` | (0,0,2,2) vs (1,1,2,2) | hand: inter 1, union 7 | 0.1428571429 | 1/7 | 1e-12 | PASS |
| 23 | `iou` disjoint | (0,0,1,1) vs (5,5,1,1) | hand: 0 | 0.0 | 0 | exact | PASS |
| 24 | `nms` | 2 overlapping + 1 disjoint box | hand: keep [0,2] | [0,2] | [0,2] | exact | PASS |
| 25 | Fairness selection rate | synthetic group A | hand 2/4 | 0.5 | 0.5 | exact | PASS |
| 26 | Fairness TPR | synthetic group A | hand 2/4 positives | 0.5 | 0.5 | exact | PASS |
| 27 | Fairness FPR with no negatives | group A | undefined → NaN | NaN | NaN | exact | PASS |
| 28 | Demographic parity gap | rates 0.5 vs 0.25 | hand 0.25 | 0.25 | 0.25 | 1e-12 | PASS |
| 29 | Exact Shapley | 3-feature linear score | `phi_i = w_i(x_i - E[bg_i])` | [0,−3,−1] | [0,−3,−1] | 1e-9 | PASS |
| 30 | Q-learning update | two-step episode, terminal reward 1, gamma .9, optimistic init | hand bootstrap 0.9 | 0.9 | 0.9 | 1e-12 | PASS |
| 31 | Precision | 8 labels | scikit-learn | 0.75 | 0.75 | 1e-12 | PASS |
| 32 | Recall | 8 labels | scikit-learn | 0.6 | 0.6 | 1e-12 | PASS |
| 33 | F1 | 8 labels | scikit-learn | 0.6666666667 | 0.6666666667 | 1e-12 | PASS |
| 34 | ROC AUC | 8 scores | scikit-learn | 0.8666666667 | 0.8666666667 | 1e-12 | PASS |

Additional checks not in the count above: SBM symmetry and class balance; random-mix homophily
monotonicity; inductive split disjointness and stratification; `noisy_labels` only changes
training labels; feature/label linear probe; and model-init reproducibility. These are covered in
`tests/test_advanced_applications.py` and the LAB-14-01 review.

## 4. LAB-14-01 independent review

### 4.1 Reported results reproduced

Running the production functions over seeds 0–4 produced exactly the values in
`PHASE-24A-EXPERIMENT-RESULTS.md`:

| Family | Protocol | MLP accuracy | GCN accuracy | Gap |
| :--- | :--- | ---: | ---: | ---: |
| random-mix | transductive | 0.399 ± 0.042 | 0.866 ± 0.020 | +0.467 |
| random-mix | inductive | 0.370 ± 0.091 | 0.945 ± 0.029 | +0.575 |
| SBM | transductive | 0.399 ± 0.042 | 0.794 ± 0.029 | +0.395 |
| SBM | inductive | 0.370 ± 0.091 | 0.835 ± 0.020 | +0.465 |

Matched protocol control: MLP 0.405 ± 0.048; GCN 0.855 ± 0.062 (random-mix), 0.830 ± 0.068
(SBM). Full `graphs.py` runtime was 147 s on the audit machine.

### 4.2 Leakage checks

| Check | Measured | Verdict |
| :--- | :--- | :--- |
| Inductive split disjoint and complete | 120 train / 40 validation / 40 test | PASS |
| Validation and test labels unchanged by noise | `yt[va+te] == y[va+te]` | PASS |
| Training labels flipped at 10% | 12 of 120 | PASS |
| `A_fit` test-to-training weight | 0.0 | PASS |
| `A_fit` test rows/columns | self-loop only, no train links | PASS |
| `A_infer` test-test off-diagonal | 0.0 | PASS |
| Test labels passed to training/selection | not passed; selection uses validation only | PASS by code inspection and API shape |
| Feature-only linear probe on test | 0.45 accuracy | Weak features, as designed; no direct label column |

### 4.3 Ablations (inductive, seed 0)

| Family | Ablation | MLP test acc | GCN test acc | Interpretation |
| :--- | :--- | ---: | ---: | :--- |
| random-mix | none | 0.225 | 0.925 | graph + features |
| random-mix | shuffled training labels | 0.100 | 0.125 | near chance (0.2); no leakage via labels |
| random-mix | permuted features | 0.250 | 0.450 | graph alone gives partial signal |
| random-mix | permuted edges | 0.225 | 0.275 | edge signal removed |
| SBM | none | 0.225 | 0.825 | graph + features |
| SBM | shuffled training labels | 0.100 | 0.125 | near chance |
| SBM | permuted features | 0.250 | 0.450 | graph alone gives partial signal |
| SBM | permuted edges | 0.225 | 0.275 | edge signal removed |

These are single-seed ablation runs, so they are diagnostic rather than estimates. They show that
the high inductive GCN accuracy is driven by graph structure plus weak features, and collapses when
either the labels or the edges are destroyed. I found no evidence of test-label leakage or
feature-label shortcut beyond the declared synthetic design. The high value is legitimate for this
task; it is not evidence about real graphs.

### 4.4 Protocol and reporting limitations

- Inductive training uses 60% of nodes, transductive 20%; absolute accuracies are not directly
  comparable across protocols. The matched control holds train/test fixed and still shows +0.450
  and +0.425.
- Five seeds give coarse variance estimates; GCN-8 has SD ±0.186 (random-mix) and ±0.157 (SBM).
- The SBM has independent edges given class blocks and equal class sizes; it is a teaching model,
  not a fit to a real network.

**LAB-14-01 verdict:** methodologically valid, reproducible, leakage-controlled, and honestly
reported. Retain the results.

## 5. Notebook regression

Clean kernels, `nbclient`, timeout 300 s, outputs **not written back**. Inventory: 35 course
notebooks, 691 cells, 329 code cells, 500.1 s total. The template is the 36th `.ipynb` file and was
excluded, as in prior regressions.

| Notebook | Cells | Status | Seconds | Warning / note |
| :--- | ---: | :--- | ---: | :--- |
| M01/.../nb-01-01-capability-test-bench | 32 | PASS | 7.2 | |
| M02/.../nb-02-01-agent-loop-gridworld | 15 | PASS | 2.1 | |
| M03/.../nb-03-01-search-workbench | 18 | PASS | 3.2 | |
| M04/.../nb-04-01-propositional-logic-workbench | 27 | PASS | 2.1 | |
| M04/.../nb-04-02-first-order-inference-and-unification | 23 | PASS | 2.0 | |
| M05/.../nb-05-01-uncertainty-workbench | 19 | PASS | 2.0 | |
| M05/.../nb-05-02-variable-elimination | 17 | PASS | 2.2 | |
| M06/.../nb-06-01-data-preparation-workbench | 26 | PASS | 4.8 | |
| M06/.../nb-06-02-regression-and-classification-workbench | 20 | PASS | 3.5 | |
| M06/.../nb-06-03-model-comparison-and-ensembles | 16 | PASS | 10.2 | |
| M06/.../nb-06-04-clustering-pca-and-anomalies | 18 | PASS | 10.5 | |
| M07/.../nb-07-01-neural-network-fundamentals | 17 | PASS | 11.8 | |
| M07/.../nb-07-02-pytorch-image-classification | 16 | PASS | 15.8 | |
| M07/.../nb-07-03-sequences-attention-transfer | 17 | PASS WITH WARNINGS | 61.6 | PyTorch nested-tensor prototype warning |
| M08/.../nb-08-01-tokenisation-and-features | 15 | PASS | 6.4 | |
| M08/.../nb-08-02-classification-and-ner | 15 | PASS | 5.9 | |
| M08/.../nb-08-03-attention-and-sequences | 13 | PASS | 2.8 | |
| M09/.../nb-09-01-image-processing | 20 | PASS | 13.2 | |
| M09/.../nb-09-02-cnn-classification | 17 | PASS | 18.2 | |
| M09/.../nb-09-03-object-detection | 15 | PASS | 13.0 | |
| M09/.../nb-09-04-image-segmentation | 15 | PASS | 24.1 | |
| M10/.../nb-10-01-mdps-and-dynamic-programming | 13 | PASS | 8.4 | |
| M10/.../nb-10-02-tabular-control-sarsa-and-q-learning | 13 | PASS WITH WARNINGS | 9.8 | non-interactive Agg canvas warning |
| M10/.../nb-10-03-deep-reinforcement-learning | 13 | PASS | 16.2 | |
| M11/.../nb-11-01-tokens-attention-and-generative-models | 14 | PASS WITH WARNINGS | 82.8 | tqdm/ipywidgets warning; loads weights |
| M11/.../nb-11-02-retrieval-prompting-and-evaluation | 14 | PASS WITH WARNINGS | 68.4 | tqdm warning; unauthenticated HF Hub request |
| M12/.../nb-12-01-agentic-ai-workbench | 31 | PASS | 2.6 | |
| M13/.../nb-13-01-explainability-toolkit | 18 | PASS | 10.2 | |
| M14/.../nb-14-01-capstone-starter-kit | 15 | PASS | 48.8 | |
| P01/.../nb-p01-01-python-fundamentals | 33 | PASS | 3.2 | |
| P01/.../nb-p01-02-numpy-pandas-plotting | 28 | PASS | 7.0 | |
| P02/.../nb-p02-01-linear-algebra | 27 | PASS | 3.8 | |
| P02/.../nb-p02-02-calculus-and-optimization | 25 | PASS | 4.4 | |
| P03/.../nb-p03-01-probability-and-statistics | 30 | PASS | 6.5 | |
| P04/.../nb-p04-01-data-preparation | 26 | PASS | 5.4 | |

No notebook had an error output, missing dependency, or failed cell. The four warnings are library
notices, not execution failures. The two M11 notebooks download/cache small model weights on first
use; after caching they run offline. No large pretrained model was downloaded specifically for the
audit. No notebook outputs were written back into the repository.

## 6. Test-suite quality and coverage

- 196 tests passed; no skips or xfails occurred in the final run.
- 175 test functions; parameterisation accounts for the difference.
- Tests use deterministic seeds and explicit tolerance (`pytest.approx` or numeric comparisons).
- No test was found that only asserts a shape without checking behaviour; 32 shape/length
  assertions exist as guards alongside value assertions.
- `tests/test_agents.py` contains a conditional `pytest.skip` if the `send_email` tool is removed;
  it did not skip in this run, but it could hide a regression if the tool disappears. Low.
- No shared mutable fixture or cross-test state was found; `conftest.py` only adds code
  directories to `sys.path`.

Coverage of M13/M14 reference code, measured with `coverage` over the full suite:

| Subsystem | Statements | Missed | Coverage |
| :--- | ---: | ---: | ---: |
| M13 responsible/explainable/secure AI | 961 | 616 | 35.9% |
| M14 advanced applications | 1,028 | 651 | 36.7% |
| **Combined M13+M14** | **1,989** | **1,267** | **36.3%** |

This supersedes the Phase 24 figure of 34% (609/1,800): the graph code and tests grew, and the
measured combined figure is now 36.3%. Highest-value covered areas include fairness metrics,
Shapley values, security attacks, graph generation/protocols and metrics. Untested code is mostly
`build_notebooks.py` (0%, generation tooling), standalone `main()` demonstration paths, optional
model-dependent code, error branches, plotting helpers and full federated/multimodal/efficiency
pipelines. This is adequate for a teaching repository but is not full branch coverage.

## 7. Representative lab execution

| Lab | What was executed | Result |
| :--- | :--- | :--- |
| LAB-05-02 Bayesian HVAC diagnosis | NB-05-02 clean execution; the VE algorithm it teaches checked against brute force on an independent custom net and against alarm enumeration | PASS; agreement to 1e-12; notebook passes |
| LAB-13-01 fairness audit | `python fairness.py` (5 s) | PASS; printed recruitment 0.947, selection 0.172/0.096, student 0.798→0.793, loans 0.672, matching the lab text |
| LAB-13-02 security/prompt injection | `security.py` (11 s), `llm_security.py`, `guardrails_m13.py` | PASS; backdoor ASR 0.855 and other tables produced; no errors |
| LAB-14-01 graph learning | `graphs.py` (147 s), starter with both families | PASS; five-seed results reproduce; starter runs |
| LAB-14-02 efficient serving | `efficiency.py` (26 s), `timeseries_monitor.py` (14 s) | PASS; direction of compression results holds, but exact latency ratios differ (see defect register) |

## 8. Residual technical limitations

- No browser or site generator exists in the repository; visual rendering was not executed. Static
  Markdown structure was checked, but a visual acceptance claim cannot be made.
- The M14 latency ratios are machine-dependent and did not reproduce exactly (int8 1.72× vs 2.62×;
  pruning 1.10× vs 1.45× in this run). Direction (slower, no size benefit from pruning) held.
- Licensing checks are mechanical; they do not establish legal clearance for model weights, UCI
  data or quotations.
- Five graph seeds and two synthetic families do not establish performance on real networks.
