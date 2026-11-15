# Phase 24 — LAB-14-01 Experimental Saturation Report

**Finding.** The LAB-14-01 starter reported graph model 1.000 and feature-only baseline 1.000.
The comparison carried no information: both models had memorised the same 60 labelled nodes.

**Status.** Replaced with a leakage-free, multi-seed experiment. No result was manufactured, no
seed was selected to produce a gap, and the graph is not guaranteed to win. Final measured output
is reproducible from the committed scripts.

---

## 1. Root cause

The starter had three independent defects:

1. **No train/test separation.** `train()` fitted on all 60 nodes and `accuracy()` evaluated the
   same 60 nodes. The reported number measured memorisation, not generalisation.
2. **A feature that gave the answer away.** `features[:, 0] += 2.0 * labels` made the two classes
   almost linearly separable, so the feature-only baseline reached 1.000 without using the graph.
3. **One seed, no label noise, no variance.** A single deterministic run produced one number with
   no way to tell a real effect from an artefact. The two-community graph also had homophily near
   0.98, so message passing added nothing that the feature had not already supplied.

The reference experiment in `code/graphs.py` had a related problem: at homophily ≥ 0.7 the GCN
reached 1.000, and the code also selected the best epoch using the test set — a second, subtler
leak. Both were corrected.

## 2. Redesign

### 2.1 Graph generation (`code/graphs.py`)

| Property | Before | After |
| --- | --- | --- |
| Classes / nodes | 5 / 200 | 5 / 200 (unchanged) |
| Feature noise | 2.0 | 2.6 (weaker signal) |
| Degree | 6 | 4 |
| Edge rule | fixed same/other counts | each edge slot same-class with probability `homophily`, otherwise uniform over all nodes |
| Homophily sweep | 0.1–0.9 | 0–1 requested, reported by measured edge homophily |

The edge rule matters: the old construction forced every non-same edge to be cross-class, so
"homophily 0" was a perfectly heterophilous, highly informative graph rather than a random one.
It flattered the GNN at the low end. Uniform sampling fixes that; with five classes, random
mixing measures about 0.2.

### 2.2 Leakage-free protocol

- **20% of nodes labelled for training**, stratified by class; the other 80% are test nodes.
  Message passing may use the whole graph, but only training labels enter the loss (transductive
  node classification — stated as a limitation).
- **10% of training labels flipped** to another class; test labels stay clean.
- **Five seeds** (0–4) per condition; mean ± standard deviation reported.
- **Test set evaluated once**, after a fixed 200 epochs. No best-epoch selection, no
  hyperparameter tuning on test.
- Fixed model sizes, learning rate and weight decay for every condition; only the graph changes.

### 2.3 Starter (`labs/starters/lab-14-01_starter.py`)

Rewritten in pure NumPy with the same protocol: two classes, weak features, 20% labelled,
10% training-label noise, five seeds, and a printed homophily sweep against a feature-only
baseline. The `TODO` tasks (second modality, extra edge type, whether the graph still helps)
remain.

## 3. Measured results

### 3.1 Reference experiment (`python code/graphs.py`)

Graph: 200 nodes, 5 classes, 12 features, 763 edges; measured edge homophily **0.783 ± 0.006**;
20% labelled; 10% training-label noise.

```text
  model                     mean      sd
  MLP                      0.342   0.049
  GCN-2                    0.829   0.057
  GCN-4                    0.840   0.062
  GCN-8                    0.188   0.020

  graph gain over features only: +0.486
```

GCN-2 and GCN-4 differ by less than one standard deviation: there is no evidence that four
layers is reliably better. The 8-layer model is at chance (0.2).

Homophily sweep (measured homophily, five seeds per row):

```text
   homophily     MLP   GCN-2    gain
       0.189   0.334   0.293  -0.041
       0.380   0.334   0.477  +0.144
       0.581   0.334   0.702  +0.369
       0.783   0.334   0.829  +0.495
       1.000   0.334   0.906  +0.573
```

The graph hurts slightly below ~0.3 measured homophily, is roughly neutral at random mixing, and
helps above it. At perfect homophily the GNN reaches 0.906 — not 1.000, because 10% of training
labels are wrong.

### 3.2 Starter (`python labs/starters/lab-14-01_starter.py`)

```text
 edge homophily  graph mean  graph sd  baseline    gain
          0.500       0.562     0.041     0.590  -0.027
          0.628       0.671     0.054     0.590  +0.081
          0.750       0.804     0.053     0.590  +0.214
          0.874       0.886     0.047     0.590  +0.296
          1.000       0.952     0.015     0.590  +0.362
```

The starter's baseline is stable at 0.590 and the graph gain rises with homophily. Neither model
reaches 1.000 at the default setting, so the comparison is informative.

## 4. Changes to teaching material

| File | Change |
| --- | --- |
| `code/graphs.py` | New edge sampling, degree/noise, 20% split, label noise, five seeds, measured homophily, final-epoch evaluation; printout rewritten |
| `labs/starters/lab-14-01_starter.py` | Rewritten with split, noise, seeds, baseline comparison and homophily sweep |
| `labs/lab-14-01-…md` | New B0 design section; B1–B3 numbers and questions updated; Part C table; starter-output block; deliverable unchanged in scope |
| `lessons/L14-04-…md` | Reproduction section numbers, sweep table, leakage note and common-mistakes row updated |
| `quizzes/quiz-14.md` | Question 12 uses the new measured gap and the 0.906 ceiling |
| `summary.md` | GNN and homophily rows updated to the measured values |

## 5. Reproducibility check

Run from a fresh process:

```bash
cd modules/M14-advanced-ai-applications-and-capstone/code
python graphs.py
cd ../..
python labs/starters/lab-14-01_starter.py
```

Both complete without downloads or GPU. All randomness flows from explicit seeds; repeated runs
on the same machine reproduce the tables above. The full notebook suite was executed separately
(see the remediation report) and `nb-14-01` passes.

## 6. Honest interpretation and limitations

- **The graph is not guaranteed to win.** At low homophily it loses; the lab asks students to
  report that, not to hide it.
- **Transductive setting.** Test-node features and edges are visible during message passing, as in
  standard GNN benchmarks. It is not an inductive claim about unseen graphs.
- **Synthetic topology.** One generator family, 200 nodes, five classes. Nothing here licenses a
  claim about fraud, citation or social networks.
- **Label noise is artificial** and uniform over training nodes. Real label noise is structured.
- **Five seeds is a small sample.** Standard deviations are reported, but no confidence intervals
  or significance tests are claimed.
- **Accuracy only.** No calibration, robustness or fairness metric is measured on this graph.
- **The perfect-homophily ceiling (0.906)** is a property of the generator, not evidence of method
  quality; the lab now asks why.
- **No result was tuned to create a gap.** Parameters were fixed before measuring; the reported
  outcome includes a regime where the graph loses.
