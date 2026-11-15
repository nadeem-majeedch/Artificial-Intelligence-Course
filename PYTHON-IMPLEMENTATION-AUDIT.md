# Python Implementation Audit — Phase 23

**Scope:** 72 Python files, 21,835 lines, under `modules/*/code/` and `prerequisites/*/code/`.
**Method:** compile every file, import every module, run every `run_tests()` that exists, inspect the
algorithms named in the brief, and exercise the numeric code through an independent verification harness
(`audit/math_verify.py`, 32 checks). Execution alone was not treated as correctness.

## 1. Inventory and static health

| Check | Result |
| :--- | :--- |
| Files compiled with `py_compile` | 72 / 72, **0 syntax errors** |
| Modules imported successfully (all code directories on `sys.path`) | 72 / 72, **0 import failures** |
| Self-tests (`run_tests`) found and executed | 5 modules, **all return True** |
| Self-test runtime | `vision_core` 4.1 s, `experiments` 1.7 s, `alarm_network`, `expert_system`, `variable_elimination` < 0.1 s |

Self-tests exist in `M04/code/expert_system.py`, `M05/code/{alarm_network, variable_elimination}.py`,
`M09/code/vision_core.py` and `M10/code/experiments.py`. **They do not exist in M06, M07, M08, M11, M12 or
M13**, and `rl_envs.py`, `dp.py`, `tabular.py` and `dqn.py` have no in-file tests (M10 puts its tests in
`experiments.py`). This is the largest engineering weakness: a third of the codebase has no automated
statement of what it is supposed to do.

## 2. Algorithm correctness (reviewed file by file)

| File | What it implements | Verdict |
| :--- | :--- | :--- |
| `M03/search_algorithms.py` | BFS, DFS, DLS, IDS, UCS, A*, greedy, hill climbing, simulated annealing, minimax, alpha-beta, CSP backtracking | Correct; UCS and A* verified against an independent Dijkstra on 120 random graphs; A* re-expands when a cheaper `g` arrives, so it stays optimal with an inconsistent-but-admissible heuristic |
| `M04/prop_logic.py` | AST, evaluation, CNF, entailment by model checking | Correct; truth table and modus ponens verified |
| `M04/fol_core.py` | Terms, unification with occurs check, CNF/Skolemisation, resolution, forward chaining | Correct; occurs check, MGU composition, soundness and a refused non-entailment verified |
| `M04/expert_system.py` | Unifying rule engine, explanations, Bayesian network | Correct; three defects found and fixed in Phase 22 (propositional matching, reversed F5 rule, mutation during iteration); self-test covers them |
| `M05/variable_elimination.py` | Factors, restrict/multiply/sum-out/normalise, VE, alarm network | Correct; equals brute-force enumeration to 1e-10 on 4 queries |
| `M06/linreg.py`, `classifiers.py` | OLS, ridge, lasso, polynomial features, logistic GD, kNN, Gaussian/multinomial NB, CART, random forest, gradient boosting, linear SVM | OLS, ridge, R², NB, GD convergence and tree splits verified independently; the rest read against their stated objectives |
| `M07/nn_numpy.py` | MLP forward/backward, softmax, SGD/momentum/RMSProp/Adam, dropout, gradient check | Backprop verified by finite differences (7.6e-9); softmax shift-invariant |
| `M08/seq_models.py` | N-gram LM, Bahdanau attention seq2seq, causal LM, perplexity, sampling, optional HF path | Attention verified as a masked distribution; formula matches the docstring |
| `M09/vision_core.py` | Synthetic data, convolution, Sobel, Otsu, morphology, HOG, IoU/NMS/AP, Dice/mIoU, TinyCNN, TinyUNet | Convolution, Otsu, IoU, Dice, mIoU, NMS verified; **one defect fixed (see §4)** |
| `M10/{rl_envs,dp,tabular,dqn,experiments}.py` | Gridworlds, cliff walking, DP, TD control, DQN/REINFORCE/AC/PPO | Bellman residual 2.9e-12, policy/value iteration agree exactly, Q-learning reaches the goal, SARSA/Q-learning ordering reproduced |
| `M11/{gen_models,lora,rag,llm_eval,...}.py` | VAE, GAN, diffusion, LoRA, retrieval, evaluation metrics | Losses and shapes sane under execution; LoRA update matches `W + (α/r)BA`; no closed-form correctness test is possible for trained generators |
| `M12/agent_core.py`, `tools.py`, `multi_agent.py` | Agent loop, tool registry, coordination | Read and executed through the notebook; no independent oracle exists, so correctness is judged by behaviour on the notebook's scripted scenarios |
| `M13/fairness.py`, `explain.py`, `security.py`, `governance.py` | Group metrics, attribution/counterfactuals, attack demonstrations, risk register | Disparate impact ratio verified against min/max selection rate; the rest read against definitions |

## 3. Input validation, edge cases, error handling

Verified behaviour:

- `Factor.from_array` rejects shape mismatches, `variable_elimination` rejects unknown evidence, non-boolean
  evidence, unknown queries and queries that appear in the evidence, and it refuses to normalise zero mass.
- `vision_core.iou` returns 0.0 for disjoint or zero-area boxes; `nms` handles empty input; `otsu_threshold`
  returns the minimum for a constant image instead of dividing by zero.
- `tabular.exact_values` requires an environment exposing `unwrapped.P` (a Gymnasium-style model) and will
  raise `AttributeError` on the course's own `MDPAdapter`; that is a documented contract in its docstring,
  but the failure mode is a raw exception rather than a clear message.
- `astar` assumes `h(goal) = 0`; with a non-zero goal heuristic it can return a suboptimal path silently.
- `nn_numpy.gradient_check` mutates and restores weights correctly (verified by the 7.6e-9 agreement).

Not verified: behaviour under NaN/inf inputs, extremely large state spaces, or concurrent use. Those are
outside the teaching scope, and no claim is made about them.

## 4. Defect found and fixed

**`vision_core.otsu_threshold(gray, bins=64)` — two defects.**

1. `bins` was accepted and never used; the histogram was hard-coded to 256 integer levels.
2. The scale was inferred by `gray.astype(np.uint8)`. On an image in [0, 1] every value truncated to 0, so
   the function returned 0.0 with no error, and `gray > 0.0` produced an all-foreground mask.

Fix: the observed range is quantised into `bins` levels and the threshold is returned in the input's own
units, so uint8 and [0, 1] copies of the same image split identically (103.6/255 vs skimage's 105.2/255).
A regression assertion for the float case was added to `run_tests()`. The notebook using the function was
re-executed (10.1 s, 0 errors) and now prints `otsu threshold: 101.6`.

## 5. Reproducibility and determinism

- Every dataset generator and training routine takes an explicit seed and builds its own
  `np.random.default_rng(seed)`; no global RNG state is relied on in M06/M09/M10.
- Repeated generation with the same seed is bit-identical (verified for `make_leaf_images`), and different
  seeds produce different images (verified), so train/test splits are genuinely disjoint when seeds differ.
- `torch.manual_seed` is set in the deep-learning entry points (`gen_models.set_seed`, `seq_models.set_seed`).
- Notebooks that train models report specific numbers; those numbers are reproducible on the same seed and
  hardware, and are seed-sensitive on different ones. The lessons state the seed where a number is quoted.

## 6. Numerical stability

- Softmax subtracts the row maximum (confirmed by shift-invariance to `+100`).
- Probability normalisation raises on zero mass rather than returning NaNs.
- `mse`/`r2_score` guard against zero variance only implicitly; `r2_score` on a constant target would divide
  by zero. This is a genuine edge-case gap, untested and unclaimed.
- No gradient clipping in the NumPy MLP; the PPO implementation clips the policy ratio (as the algorithm
  requires), which is a different mechanism.

## 7. Readability and abstraction

The code is consistently typed, docstringed and organised by concept, with module-level `run_tests()` or a
`main()` demonstration. Duplication is low: `rl_envs` owns the environments and `dp`/`tabular`/`dqn` consume
them; `vision_core` owns all vision primitives. The weakest abstraction is `M10/tabular._key`, which silently
converts observations to dictionary keys and is easy to misuse from outside the module (this audit tripped
over exactly that, and the mistake was in the harness, not the library).

## 8. Dependencies

| Package | Required? | Used by |
| :--- | :--- | :--- |
| `numpy` | yes | everywhere |
| `torch` (CPU) | yes for M07/M09/M10/M11 notebooks | CNNs, U-Net, DQN, VAE/GAN/diffusion, seq2seq |
| `matplotlib` | yes for notebooks | plots |
| `scikit-learn` | optional | comparisons in M06 notebooks |
| `scikit-image` | optional | Otsu reference comparison only |
| `opencv-python` | optional | not required by any lesson path |
| `gymnasium` | optional | CartPole labs; bundled environments replace it |
| `transformers` | optional | the two M11 notebooks that load `distilbert-base-uncased` |
| `nbformat`/`nbclient` | development only | executing notebooks |

No import of a package that is not installed was found in the modules that ran; the optional paths check
availability before importing.

## 9. Tests added or extended in this audit

- `vision_core.run_tests()`: added the float-image Otsu assertion (regression for the fixed defect).
- `audit/math_verify.py`: a 32-check independent harness covering search, logic, probability, ML, neural
  networks, vision metrics and RL. It is deliberately **separate** from the course code so it can fail
  without the course changing.

## 10. Verdict for this audit

The implementations are correct where they were independently checked, readable, seeded and honest about
their assumptions. The engineering gaps are test coverage outside five modules and a handful of unguarded
edge cases (constant-target R², `MDPAdapter` vs `exact_values`, non-zero goal heuristic). One real defect —
Otsu's silent scale failure — was found and repaired.
