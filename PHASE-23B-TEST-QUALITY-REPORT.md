# PHASE 23B — Test Quality Report

**Scope:** independent verification of `tests/` as delivered by Phase 23A, plus a
measured assessment of what the suite does and does not validate.
**Verdict input:** suite is genuine, independent and stable, with substantial untested
surface. It supports academic review of the modules it covers; it is not evidence of
whole-repository correctness.

---

## 1. What was run

| Check | Command | Result |
| --- | --- | --- |
| Full suite, clean process, no cache plugin | `python -m pytest tests/ -q -p no:cacheprovider` | **138 passed**, 0 failed, 0 skipped, **15.83 s** |
| Repeat run | same | 138 passed, 26.79 s (machine load varies; see §5) |
| Reverse module order | `pytest tests/test_vision.py … tests/test_agents.py` | **138 passed**, 23.47 s |
| Per-file runs | each `tests/test_*.py` separately | all pass: 12, 6, 12, 21, 12, 10, 12, 14, 25, 14 |
| Coverage | `coverage run --source=modules,prerequisites --omit="*/notebooks/*" -m pytest tests/` | 6,139 statements, 2,867 covered, **46.7 %** |
| Compilation | `compileall modules prerequisites assessments tests audit` | exit 0 |

Test code size: 1,262 lines across 10 test modules plus `conftest.py`. Test count by file
matches Phase 23A's claim exactly; runtime does not (Phase 23A reported 13.1–17.7 s; this
audit observed 15.8–26.8 s on the same machine, so 13 s should be read as a best case).

## 2. Do the tests exercise production code?

Yes. `conftest.py` puts every `modules/*/code` and `prerequisites/*/code` directory on
`sys.path`; every test module imports the course module by name (`search_algorithms`,
`dp`, `tabular`, `vision_core`, `text_pipeline`, `agent_core`, …). Nothing is copied
into `tests/`, and no production file was changed to make tests pass.

Independence was checked by reading the assertions rather than the test names:

- **Search:** expected path costs are verified by an independent Dijkstra implementation
  inside the test, not by the module's own `uniform_cost`.
- **Logic:** entailment is checked against exhaustive enumeration of all valuations;
  truth tables are built by the test.
- **Probability:** variable elimination is compared with brute-force summation over the
  32 worlds of the alarm network; the posterior is recomputed from the joint table.
- **ML:** metrics are recomputed from first principles; split/leakage tests assert on
  data partitions, not on model internals.
- **NN:** gradients are checked by finite differences, not by the module's own
  `gradient_check`.
- **Vision:** convolution is compared with `scipy.signal.convolve2d`; IoU/Dice/AP are
  recomputed from pixel definitions.
- **RL:** the Bellman residual is computed from the returned value function; policy
  evaluation is compared with a closed-form linear solve; TD(0) against Gymnasium's
  exact values for a fixed policy.
- **NLP/agents/genai:** hand-computed counts and IDF, a masked-attention distribution,
  guardrail outcomes specified behaviourally, analytic parameter counts.

No test asserts `f(x) == f(x)` or compares a function with a copy of itself. The closest
case is `tests/test_rl.py::test_greedy_action_is_optimal_for_the_value_function`, which
derives Q-values with `dp.action_values` (the module under test) and then checks the
policy is greedy with respect to them. That is a consistency property, not an independent
check of optimality, and it is the weakest assertion in the suite.

## 3. Coverage, with its exact scope

`coverage` recorded **25 of the 66** Python files under `modules/*/code` and
`prerequisites/*/code`. The 41 unmeasured files are never imported by the suite, so the
47 % figure is **not** repository-wide coverage: it is coverage of the 6,139 statements
in the imported subset.

| Subsystem | File | Line coverage |
| --- | --- | ---: |
| M03 search | `search_algorithms.py` | 65 % |
| M04 logic | `prop_logic.py` / `fol_core.py` / `expert_system.py` | 39 / 55 / 73 % |
| M05 uncertainty | `variable_elimination.py` / `alarm_network.py` | 66 / 44 % |
| M06 ML | `classifiers.py` / `linreg.py` / `unsupervised.py` | 67 / 74 / 52 % |
| M07 neural nets | `nn_numpy.py` | 77 % |
| M08 NLP | `text_pipeline.py` / `seq_models.py` / `text_data.py` | 58 / 26 / 21 % |
| M09 vision | `vision_core.py` | 45 % |
| M10 RL | `rl_envs.py` / `dp.py` / `tabular.py` / `experiments.py` / `dqn.py` | 46 / 48 / 37 / 65 / **19 %** |
| M11 generative | `gen_models.py` / `lora.py` / `gen_data.py` | **15 / 21 / 19 %** |
| M12 agents | `agent_core.py` / `tools.py` / `agent_data.py` | 45 / 37 / 42 % |
| **Total (25 files)** | | **46.7 %** |

**41 files with no coverage at all**, by module:

- M01 `capability_check.py`, `eliza_lite.py`
- M02 `agents.py`, `environments.py`
- M04 `knowledge_bases.py`
- M06 `datasets.py`, `evaluation.py`, `prep.py`, `sklearn_compare.py`
- M07 `deep_data.py`, `torch_utils.py`, `transfer.py`
- M08 `classify.py`, `embeddings.py`
- M11 `app.py`, `attention_lab.py`, `build_notebooks.py`, `llm_eval.py`, `llm_gen.py`,
  `prompts.py`, `rag.py`, `tokenizers_lab.py`
- M12 `guardrails.py`, `multi_agent.py`, `protocols.py`, `workflows.py`
- M13 `build_notebooks.py`, `explain.py`, `fairness.py`, `governance.py`,
  `guardrails_m13.py`, `llm_security.py`, `rai_data.py`, `security.py`
- M14 `build_notebooks.py`, `efficiency.py`, `federated.py`, `graphs.py`, `multimodal.py`,
  `neurosymbolic.py`, `timeseries_monitor.py`

The M13 and M14 omissions matter most: those modules carry the ethical, security and
systems content an academic reviewer is most likely to inspect, and none of their code is
under test. The M11 training loops (VAE/GAN/DDPM) and the DQN/PPO training paths are also
untested beyond their heads and schedules.

## 4. Tests that pass without validating much

These are not defects, but they should not be counted as evidence of behaviour:

| Test | What it actually asserts |
| --- | --- |
| `test_policy_network_outputs_a_finite_score_per_action` | output shape and finiteness; a softmax sum if non-negative |
| `test_answer` shape checks in `test_vision` (HOG, synthetic data) | array size and dtype, not correctness of the descriptor values |
| `test_smoothing_and_episodes_to_use_the_documented_window` | array length and one value, not the smoothing mathematics |
| `test_q_network_maps_a_batch_of_states_to_one_value_per_action` | shape only |
| `test_alarm_joint_table_is_a_normalised_distribution` | sums to 1, not that each entry matches the chain rule |

Everything else asserts a computed value, a property (invariance, monotonicity, masking),
an error type, or an exact analytic result.

## 5. Flakiness, environment and order dependence

- **Order dependence:** none observed. Reverse-order and per-file runs both pass; tests do
  not share mutable module state, and stochastic tests take explicit seeds.
- **Timing:** three identical runs took 15.83 s, 23.47 s (reverse order) and 26.79 s. The
  variance is machine load (torch import + pytest startup), not test logic. No test asserts
  on wall-clock time, and no test has a timeout.
- **Environment:** `torch` (CPU), `scipy`, `gymnasium` and `transformers` must be
  installed. `test_agents.py` imports the whole M12 agent stack, so a missing optional
  dependency would fail collection rather than skip.
- **Conditional skip:** `test_agents.py::email_spec` calls `pytest.skip` if the
  `send_email` tool is removed from `TOOL_SPECS`. That is reasonable tolerance for a
  renamed tool, but it means a genuine regression that deletes the tool would reduce
  coverage silently instead of failing. It did not trigger in this audit.
- **Network:** no test touches the network. This was verified by inspection (no
  `requests`/`urllib` imports in `tests/`) and by the 138-passed result with no external
  calls in the log.
- **Randomness:** 40 seed/`random_state` usages; stochastic expectations are inequalities
  over seeded runs (for example SARSA/Q-learning tails above a random baseline across two
  seeds), not exact values.

## 6. Remaining untested behaviour that matters

1. M13 fairness metrics, mitigations, explainability and prompt-injection harnesses.
2. M14 efficiency, federated learning, graph/multimodal and neuro-symbolic code.
3. Full DQN, REINFORCE, actor-critic and PPO training loops; VAE/GAN/DDPM training.
4. M06 data preparation, evaluation helpers and dataset generators (tested only through
   the classifiers that consume them).
5. M01/M02 agent and environment code; M08 embeddings/classification pipelines.
6. CLI entry points, plotting, file I/O and notebook-only helpers.

## 7. Recommendation

Add tests for M13 (highest academic risk), then M14 and the DQN/PPO training paths. Do not
add tests that restate implementation logic or inflate counts; the existing suite's value
comes from its independent references, and that standard should be kept.
