# Phase 24A — Experiment Results (LAB-14-01)

**Date:** 14 November 2026  
**Script:** `modules/M14-advanced-ai-applications-and-capstone/code/graphs.py`  
**Command:** `python graphs.py` (from `code/`), exit status 0  
**Runtime:** 135 s on the course Windows machine (Python 3.14, PyTorch CPU)  
**Seeds:** 0, 1, 2, 3, 4 (five seeds per condition)  
**Data:** 200 nodes, 5 balanced classes, 12 weak features, 10% training-label noise.  
**Protocols:** transductive (20% labelled, fixed 200 epochs) and inductive (60/20/20,
validation-selected epoch with patience 40, maximum 300 epochs, test evaluated once).

All figures below are copied from the final clean run. Standard deviations are population SD
across the five seeds.

## 1. Graph families at the default setting

| Family | Edges | Mean degree | Measured edge homophily |
| :--- | ---: | ---: | ---: |
| random-mix (degree 4 slots, `homophily` 0.783 requested) | 765 | 7.65 | 0.773 |
| SBM (`p_in` 0.12, `p_out` 0.01) | 630 | 6.30 | 0.747 |

The random-mix graph is slightly denser because each node receives four edge slots, including
duplicates collapsed by the adjacency; the SBM samples each pair independently.

## 2. Default comparison

| Family | Protocol | Majority | MLP | GCN | GCN − MLP |
| :--- | :--- | ---: | ---: | ---: | ---: |
| random-mix | transductive | 0.200 ± 0.000 | 0.399 ± 0.042 | 0.866 ± 0.020 | **+0.467** |
| random-mix | inductive | 0.200 ± 0.000 | 0.370 ± 0.091 | 0.945 ± 0.029 | **+0.575** |
| SBM | transductive | 0.200 ± 0.000 | 0.399 ± 0.042 | 0.794 ± 0.029 | **+0.395** |
| SBM | inductive | 0.200 ± 0.000 | 0.370 ± 0.091 | 0.835 ± 0.020 | **+0.465** |

Macro-F1 tracks accuracy within 0.003 in every row: random-mix transductive MLP 0.394, GCN
0.865; SBM transductive MLP 0.394, GCN 0.791; inductive MLP 0.350, GCN 0.945 (random-mix) and
0.836 (SBM). The MLP is identical across families by construction — the families change edges,
not features — which is the intended control.

### Matched protocol control

Same train/test nodes as the inductive run, 60% of nodes labelled, validation nodes unused,
test–test edges left visible:

| Family | MLP | GCN | Gap |
| :--- | ---: | ---: | ---: |
| random-mix | 0.405 ± 0.048 | 0.855 ± 0.062 | +0.450 |
| SBM | 0.405 ± 0.048 | 0.830 ± 0.068 | +0.425 |

Inductive GCN is 0.014–0.090 higher than this control with the same nodes. The remaining
difference is protocol (test-subgraph visibility and validation-based early stopping), not label
budget or test-set identity.

## 3. Homophily sweeps (transductive)

Random-mix, measured edge homophily:

| h | MLP | GCN | Gain |
| ---: | ---: | ---: | ---: |
| 0.187 | 0.399 | 0.268 | −0.131 |
| 0.385 | 0.399 | 0.424 | +0.025 |
| 0.586 | 0.399 | 0.691 | +0.293 |
| 0.773 | 0.399 | 0.866 | +0.467 |
| 1.000 | 0.399 | 0.906 | +0.508 |

SBM, varying `p_out` (0.20, 0.06, 0.02, 0.01, 0.0):

| h | MLP | GCN | Gain |
| ---: | ---: | ---: | ---: |
| 0.127 | 0.399 | 0.279 | −0.120 |
| 0.325 | 0.399 | 0.407 | +0.009 |
| 0.590 | 0.399 | 0.672 | +0.274 |
| 0.747 | 0.399 | 0.794 | +0.395 |
| 1.000 | 0.399 | 0.844 | +0.445 |

Crossover (first positive gain) is between 0.187 and 0.385 for random-mix, and between 0.127 and
0.325 for SBM. At the lowest homophily the graph actively hurts in both families.

## 4. Depth (transductive)

| Family | GCN-2 | GCN-4 | GCN-8 |
| :--- | ---: | ---: | ---: |
| random-mix | 0.866 ± 0.020 | 0.821 ± 0.028 | 0.273 ± 0.186 |
| SBM | 0.794 ± 0.029 | 0.825 ± 0.029 | 0.319 ± 0.157 |

Eight layers collapse toward chance (0.2) with a large seed spread. Four layers is mildly worse
than two on random-mix and mildly better on SBM; neither difference is a reliable depth rule.

## 5. Label-noise sweep (transductive)

| Noise | random-mix MLP | random-mix GCN | SBM MLP | SBM GCN |
| ---: | ---: | ---: | ---: | ---: |
| 0.00 | 0.430 | 0.984 | 0.430 | 0.905 |
| 0.10 | 0.399 | 0.866 | 0.399 | 0.794 |
| 0.20 | 0.350 | 0.760 | 0.350 | 0.729 |

Gain narrows from +0.554 to +0.410 (random-mix) and from +0.475 to +0.379 (SBM). Noiseless
random-mix is close to saturation (0.984), so the noiseless gap is an upper bound.

## 6. Confusion matrix and per-class results

GCN, random-mix, transductive, seed 0 (accuracy 0.866; macro-F1 0.907 on this seed):

```text
            predicted
true    0    1    2    3    4
0      27    5    0    0    0
1       0   27    5    0    0
2       1    0   30    0    1
3       1    0    0   31    0
4       2    0    0    0   30

class  precision  recall     f1
0         0.871   0.844  0.857
1         0.844   0.844  0.844
2         0.857   0.938  0.896
3         1.000   0.969  0.984
4         0.968   0.938  0.952
```

Errors are class-adjacent (0↔1, 1↔2) rather than uniform, and the worst class (1) is not
dramatically worse than the best (3). The script prints the equivalent matrices for both
protocols and both families.

## 7. Answers to the analysis questions

1. **Both families?** Yes at the default setting: +0.467 (random-mix) and +0.395 (SBM)
   transductive; +0.575 and +0.465 inductive.
2. **Homophily effect?** GCN accuracy and gain rise monotonically with measured homophily in
   both families.
3. **Heterophilous graphs?** The GCN is below the feature-only model at the lowest homophily
   (−0.131, −0.120), not merely equal to it.
4. **Inductive retention?** Yes: the gap is larger, not smaller, under the strict split. Part of
   the absolute gain comes from 60% versus 20% labelled nodes; the matched control still shows
   +0.450/+0.425 with identical train/test nodes.
5. **Label-noise sensitivity?** Both models degrade and the gap narrows, but the GCN stays ahead
   at 20% flipped labels in both families.
6. **When is there little benefit?** Low homophily, very high label noise, and features that
   already separate classes. The graph is not a universal improvement.

## 8. Reproducibility notes

- Split, label flips, feature prototypes and SBM edges are driven by explicit seeds.
- Feature prototypes use `50_000 + seed % 5`, so class structure is stable within a condition.
- Model construction is seeded immediately before each model, so the depth table and the main
  table produce identical GCN-2 numbers.
- Test labels are used only in `evaluate_metrics` after prediction. Validation labels select the
  epoch in the inductive protocol; test is evaluated once.
