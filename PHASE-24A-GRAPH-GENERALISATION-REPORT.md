# Phase 24A — Graph Generalisation and Inductive Evaluation Report

**Date:** 14 November 2026  
**Scope:** LAB-14-01 (M14), lessons and quiz claims about GCNs  
**Status:** Complete; no Git operations performed.

## 1. Objective

Test whether the Phase 24 GCN advantage is specific to one synthetic graph generator and one
transductive split. The Phase 24 experiment is retained unchanged in behaviour (degree-4
random-mix family, five seeds, 10% training-label noise, fixed final-epoch evaluation, homophily
sweep, MLP/GCN comparison), with model initialisation now explicitly seeded per model.

## 2. What was added

### 2.1 Second graph family: stochastic block model

`make_sbm(n=200, dim=12, p_in=0.12, p_out=0.01, seed=...)` assigns 40 nodes per class and samples
every pair independently: `p_in` within class, `p_out` across classes. Classes are balanced,
features come from the same weak prototype generator as random-mix, and edges never read feature
values. `p_out` controls homophily; the sweep uses 0.20, 0.06, 0.02, 0.01 and 0.0.

Documented assumptions/limits: edges are independent given the blocks (no triangles or degree
correction), classes are equal-sized, and the model is not a fit to any real network.

### 2.2 Inductive protocol

- Disjoint stratified 60/20/20 train/validation/test nodes.
- 10% of training labels flipped; validation and test labels clean.
- Training graph `A_fit`: test rows and columns zeroed, so test nodes are absent during training
  except for their own self-loop.
- Inference graph `A_infer`: test–test edges zeroed, test–train edges retained. Test features and
  their links to training nodes are available at inference, as in a deployed service.
- Epoch selected on validation accuracy only (patience 40, maximum 300). Test evaluated once.
- Matched control: transductive training on exactly the same train/test nodes, validation unused,
  full graph including test–test edges. This separates protocol from label budget and test-set
  identity.

### 2.3 Metrics

`evaluate_metrics` returns accuracy, macro-F1, a confusion matrix, and per-class precision,
recall and F1. Every condition reports mean ± SD over five seeds. `majority_baseline` predicts the
largest training class.

### 2.4 Fairness controls

MLP and GCN receive the same features, splits, label noise and epoch budget (200 fixed
transductive; identical validation-selected budget inductive). The MLP never receives edges; the
GCN never receives extra labels. No test-set number influences training, early stopping or
hyperparameter choice.

## 3. Results

Full tables, per-class results and runtime are in `PHASE-24A-EXPERIMENT-RESULTS.md`. Headline:

| Condition | MLP | GCN | Gap |
| :--- | ---: | ---: | ---: |
| random-mix, transductive | 0.399 ± 0.042 | 0.866 ± 0.020 | +0.467 |
| random-mix, inductive | 0.370 ± 0.091 | 0.945 ± 0.029 | +0.575 |
| SBM, transductive | 0.399 ± 0.042 | 0.794 ± 0.029 | +0.395 |
| SBM, inductive | 0.370 ± 0.091 | 0.835 ± 0.020 | +0.465 |
| matched control, random-mix | 0.405 ± 0.048 | 0.855 ± 0.062 | +0.450 |
| matched control, SBM | 0.405 ± 0.048 | 0.830 ± 0.068 | +0.425 |

The advantage holds in both families and both protocols. It disappears or reverses at low
homophily in both families (−0.131 random-mix, −0.120 SBM) and narrows but persists at 20% label
noise (+0.410/+0.379). Perfect homophily remains below 1.0 (0.906/0.844) because of label noise
and finite training.

Two honest caveats:

- Absolute inductive accuracy exceeds transductive accuracy partly because inductive training
  uses 60% of nodes rather than 20%. The matched control removes that confound and still shows
  the graph advantage, but the control differs in test-subgraph visibility and early stopping.
- The GCN-8 seed spread (±0.186/±0.157) is large; five seeds estimate variance coarsely.

## 4. Teaching updates

- `labs/lab-14-01-multimodal-and-graph-systems.md`: protocols table, two-family results, matched
  control, depth, homophily and noise tables, per-class analysis, six answered analysis questions,
  revised marking criteria and reflection prompts.
- `labs/starters/lab-14-01_starter.py`: `--family {random-mix,sbm}`; SBM generator; still
  transductive and deliberately simpler than the reference implementation.
- `lessons/L14-04-...md`: reproduction section rewritten with both families, inductive protocol,
  macro-F1, matched control, noise results and explicit limitations.
- `quizzes/quiz-14.md`: Q12 and answer key revised; asks about the inductive claim and its
  dependencies.
- `summary.md`, module `README.md`, `modules/README.md`: stale Phase 24 numbers replaced.
- No notebook change was required; LAB-14-01 has no notebook paired with this experiment.

## 5. Validation performed

| Check | Result |
| :--- | :--- |
| Clean experiment run, exit status | 0 (135 s) |
| Seeds | 0–4 for every reported condition |
| Existing + new M14 tests | 28 passed |
| Full pytest suite | 196 passed in 33.2 s |
| Python compilation (`compileall`) | passed |
| Course link/structure checker | passed |
| Curriculum-hour checker | passed |
| Licensing checker | passed |
| Git | no add/commit/push/stage; worktree remains dirty as before |

Leakage checks: inductive split disjointness and completeness, `A_fit` test rows/columns zero,
`A_infer` test–test block diagonal, test labels never passed to training or validation, and
validation-only epoch selection are covered by tests.

## 6. Limitations

- Synthetic families only; neither is evidence about citation, social or fraud graphs.
- SBM edges are independent given blocks, which understates clustering in real networks.
- Features are deliberately weak; with strong features the graph advantage would shrink.
- Five seeds, fixed architectures, no hyperparameter search: the experiment tests robustness of
  the direction, not state-of-the-art performance.
- Protocol comparison cannot be perfectly isolated because training schedules and graph
  visibility differ; the matched control reduces but does not eliminate this.

## 7. Verdict

**PASS WITH WARNINGS — COMPLETE WITH DOCUMENTED LIMITATIONS**

The GCN advantage generalises across the two synthetic families and survives a strict inductive
protocol with no test-set leakage. It is conditional on homophily and label quality, and the
absolute numbers are not directly comparable across protocols. Those limitations are stated in
the student-facing materials rather than hidden.
