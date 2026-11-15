# Phase 24 — Targeted M13/M14 Test Coverage Report

**Question.** Do the executable components of M13 and M14 have meaningful automated tests, and
what changed?

**Answer.** They had none before this phase: the existing suite imported neither module's code, so
coverage of the 15 M13/M14 code files was **0%**. Fifty tests now cover the reusable measurement,
governance, security, graph, policy, monitoring and averaging functions. Coverage of those files is
**34%** (609 of 1,800 statements), with the demo and training loops deliberately left uncovered.

---

## 1. What was tested

Two new files follow the repository's existing pytest conventions and reuse `tests/conftest.py`:

| File | Tests | Modules |
| --- | ---: | --- |
| `tests/test_responsible_ai.py` | **30** | `fairness`, `governance`, `guardrails_m13`, `llm_security`, `security`, `explain` |
| `tests/test_advanced_applications.py` | **20** | `graphs`, `neurosymbolic`, `timeseries_monitor`, `federated`, `multimodal`, `efficiency` |

The tests assert hand-computed values or explicit properties, not shapes:

### M13 — responsible, explainable and secure AI

| Area | What is checked |
| --- | --- |
| Group metrics | Selection rate, TPR, FPR, PPV and accuracy against a hand-worked 6-row example; groups with no positives return NaN rather than crashing |
| Fairness gaps | Demographic parity, disparate-impact ratio, equal-opportunity gap and equalised-odds gap each against their definitions; a single group has zero gap |
| Reweighing | Mean-normalised weights, and `mass(y,g)/P(g)` equal across groups, i.e. label and group become independent |
| Risk register | Band boundaries at 4/5, 9/10, 15/16; residual scores sorted descending; `reduction = inherent − residual` |
| Audit checklist | Missing-evidence count and per-area status |
| Injection detection | Flags instruction override and email exfiltration; benign fee question returns no hits |
| Sanitising / redaction | Instruction lines removed while data lines survive; salary, email and phone masked |
| Action allowlist | Default answer-only; blocked action increments the counter; confidentiality test |
| Retrieval leakage | Relevant document retrieved; no-overlap query returns nothing; unguarded RAG leaks, document-level access control leaks 0/5 |
| Agent abuse | Default-deny blocks every unsafe execution; unguarded run executes at least one |
| FGSM | Perturbation shape and strict ε-ball bound |
| Quantisation | Output lies on the requested grid and inside [0,1] |
| Membership inference | AUC/TPR/FPR all in [0,1] |
| Explanation | Permutation importance ranks the informative feature first and leaves noise near zero; exact Shapley values satisfy the efficiency property on an additive model; >10 features rejected; partial dependence is linear for a linear model |

### M14 — advanced applications

| Area | What is checked |
| --- | --- |
| Graph construction | Shape, symmetry, zero diagonal, degree bounds, balanced classes; measured homophily rises with the parameter and is ≈0.2 under random mixing with five classes |
| Splits and noise | Disjoint, stratified split covering every node; exactly 10% of training labels flipped, test labels untouched, reproducible |
| Normalisation | Exact symmetric-normalised adjacency on a two-node graph |
| Training | Same seed and same initial weights reproduce the same accuracy; result in [0,1] |
| Housing policy | Strict income boundary, savings cap, per-person allowance, property rule |
| Policy evaluation | Threshold decisions and exact violation count |
| Lag matrix | Feature/target alignment, most-recent-first columns, no leakage |
| Seasonal naïve | Exact repeat of the last season |
| PSI | Zero for identical samples; >0.25 under a large shift |
| Federated averaging | Identical models average to themselves; weight [1,0] returns the first model |
| Multimodal | Vocabulary encoding and unknown-word handling; perfect retrieval for aligned pairs, zero for reversed |
| Efficiency | Parameter count and size arithmetic; int8 quantisation within 0.05 of float output; pruning preserves shapes and reduces non-zeros |

## 2. Results

```text
python -m pytest tests/ -q
188 passed in 21.68s
```

- 138 pre-existing tests still pass.
- 50 new tests pass (30 + 20).
- New files alone: `50 passed in 11.46s`.

## 3. Coverage change

Measured with `coverage run --source=<M13 code>,<M14 code> -m pytest tests/`:

| File | Before | After |
| --- | ---: | ---: |
| `M13/code/fairness.py` | 0% | 34% |
| `M13/code/governance.py` | 0% | 57% |
| `M13/code/guardrails_m13.py` | 0% | 76% |
| `M13/code/llm_security.py` | 0% | 55% |
| `M13/code/security.py` | 0% | 23% |
| `M13/code/explain.py` | 0% | 35% |
| `M13/code/rai_data.py` | 0% | 13% |
| `M13/code/build_notebooks.py` | 0% | 0% |
| `M14/code/graphs.py` | 0% | 58% |
| `M14/code/efficiency.py` | 0% | 38% |
| `M14/code/federated.py` | 0% | 20% |
| `M14/code/multimodal.py` | 0% | 26% |
| `M14/code/neurosymbolic.py` | 0% | 21% |
| `M14/code/timeseries_monitor.py` | 0% | 25% |
| `M14/code/build_notebooks.py` | 0% | 0% |
| **Total** | **0%** (0/1,800) | **34%** (609/1,800) |

The 0% baseline is a real finding: none of the 138 existing tests imported M13 or M14 code, so
these modules had no regression protection at all.

## 4. What remains untested, and why

| Area | Reason |
| --- | --- |
| Training loops in `security.py`, `federated.py`, `multimodal.py`, `neurosymbolic.py` | Slow, stochastic and already exercised end-to-end by the module scripts and notebooks; a unit test would mostly assert that PyTorch trains |
| `explain.py` LIME, kernel SHAP, counterfactuals, stability | Sampled approximations; meaningful assertions need tolerance design that would be brittle. Exact Shapley and permutation importance are covered instead |
| `fairness.py` threshold search and end-to-end training | Grid search over fitted models; covered indirectly by LAB-13-01, not by unit tests |
| `rai_data.py` generators | Data-generation details are exercised by every fairness/explain test that imports them; schema-specific tests would duplicate the dataset cards |
| `efficiency.py` latency measurement | Wall-clock timing is machine-dependent and unsuitable for deterministic assertions |
| `timeseries_monitor.py` model fitting/backtesting | Slower scikit-learn loops; the alignment, forecast and drift primitives are covered |
| `build_notebooks.py` | Build tooling, not course logic; executing the notebooks is the appropriate check |
| Error handling for malformed arrays in graph/metric helpers | The functions document array contracts rather than validate them; adding validation would change course code beyond this phase's scope |

No test asserts only an array shape or a callable's existence. No coverage target was chased:
100% would require testing educational demo lines that exist to print a table.

## 5. Limitations

- Coverage measures executed lines, not assertion quality. The tests were written against
  hand-computed values and explicit mathematical properties, but a line covered by an import is
  still counted as covered by `coverage.py` only when executed, so the figures are conservative.
- Stochastic components are tested for bounded outputs and reproducibility, not for statistical
  accuracy claims.
- The suite does not test the notebooks; those are validated by execution (35 notebooks, 0
  failures, 442.8 s) and by the repository's link/structure checks.
- These tests protect against regressions in the measured functions; they are not a security
  certification of the teaching code.
