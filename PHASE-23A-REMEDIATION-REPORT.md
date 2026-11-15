# PHASE 23A — Academic Quality Remediation Report

**Scope:** exercises, Python tests, laboratory starter material, extension challenges, licensing
proposal, citation metadata, reference verification, and regression testing.
**Status:** all eight tasks completed; two items are proposals awaiting the repository owner
(licensing architecture, final citation release fields). Nothing was committed, staged or pushed.
`git diff --cached --stat` is empty.

---

## 0. Method and premises checked

The six Phase 23 reports were read first. Two audit premises did not survive measurement, and the
work below is based on the measured values:

| Audit premise | Measured | Consequence |
| --- | --- | --- |
| 60 of 89 lessons lack an exercises section | 89 of 89 have one; M01–M11 title it `Practical Exercises`, M12 uses `## 10. Exercises`, M13–M14 use `## Exercises` | No exercises were invented. Verified counts instead |
| ~60 external research references were never fetched | 95 bibliography entries across two layouts (44 table rows in `research-papers.md`, 51 heading entries in `library/`); 38 unique arXiv identifiers | All 38 resolved through the arXiv API; 0 unverifiable arXiv entries |

A checker was written so these claims are reproducible: `audit/check_course.py`
(`python audit/check_course.py`, exit 1 on any failure).

---

## 1. Task 1 — Lesson exercises

**Completed: verification, no additions.** Adding exercises to lessons that already have them
would have been the superficial change the brief forbids, so the section was verified instead.

Measured distribution over 89 lessons (`audit/check_course.py`):

| Items per lesson | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lessons | 38 | 29 | 14 | 4 | 3 | 1 |

- Every lesson meets the 2–4 minimum and exceeds it; the four M11 lessons with 7–9 items were left
  as they are, because trimming real exercises to hit a count is the same error in reverse.
- M13 and M14 use graded analytical sets with bold `**Beginner.** / **Intermediate.** /
  **Advanced.**` labels (six each), including bootstrap intervals, dataset construction and
  counterfactual comparison. They were **not** forced into Python exercises. M12 mixes code tasks
  with architecture and failure-mode questions.
- The checker accepts `Exercises`, `Practical Exercises` and numbered headings, which is why the
  earlier audit saw zero for M12–M14: it matched only the literal string `Practical Exercises`.

**Outstanding:** nothing for this task. The audit report's "60 lessons" figure should be treated as
superseded by the measured table above.

---

## 2. Task 2 — Python implementation tests

### Structure

`tests/` with `conftest.py` placing every `modules/*/code` and `prerequisites/*/code` directory on
`sys.path`, so tests import course modules by name and no production file was moved or renamed.
Tests are grouped by subsystem and use independent reference implementations rather than calling
the code under test twice.

### New tests: 138, all passing, 17.7 s wall clock on CPU

| File | Tests | Covers | Independent reference used |
| --- | ---: | --- | --- |
| `test_search.py` | 25 | BFS/DFS/UCS/DLS/IDS, A*, greedy, minimax, alpha-beta pruning, CSP | Own Dijkstra and path-cost verification; pruning counts |
| `test_logic.py` | 12 | Truth tables, entailment, CNF, resolution, FOL substitution, unification, occurs check, forward/backward chaining | Enumeration of all valuations |
| `test_probability.py` | 12 | Factors, restriction, normalisation, variable elimination, alarm network, explaining away, evidence validation | Brute-force joint summation over 32 worlds |
| `test_ml.py` | 21 | k-NN, decision tree, naive Bayes, logistic regression, SVM, k-means, PCA, metrics, leakage guard | Hand-computed metrics; sklearn-free references |
| `test_nn.py` | 10 | Dense/Conv/Pool shapes, ReLU/softmax, cross-entropy, backprop gradient check, SGD/Momentum/RMSProp/Adam | Finite differences for gradients |
| `test_nlp.py` | 12 | Sentence splitting, tokenisation, normalisation, stopwords, stemming, n-grams, BoW, TF-IDF, bigram LM, attention masking | Manual counts/IDF; perplexity ordering |
| `test_vision.py` | 14 | Convolution, padding, Gaussian/Sobel, Otsu, morphology, HOG, IoU, NMS, AP, Dice/mIoU, synthetic datasets | `scipy.signal.convolve2d`; pixel-level definitions |
| `test_rl.py` | 14 | Value iteration, policy iteration, exact policy evaluation, epsilon-greedy, Q-learning, SARSA, TD(0), replay buffer, DQN heads, schedules | Bellman residual; policy evaluation vs closed form; Gymnasium FrozenLake |
| `test_agents.py` | 12 | Argument validation, approval gate, scope checks, budget enforcement, audit log, scripted policy | Behavioural specification of the guardrails |
| `test_genai.py` | 6 | Diffusion schedule monotonicity/endpoints, LoRA identity at init, frozen base, parameter accounting | Analytic parameter counts |

Properties covered: normal inputs, edge cases (empty/constant images, single-state cases, zero
mass), invalid inputs (wrong arity, unknown tool, unknown evidence node, non-string argument), and
deterministic behaviour under seeds. Stochastic expectations are stated as inequalities over seeded
runs (for example SARSA/Q-learning tails above a random baseline over two seeds), not exact values.

### Measured coverage

`python -m coverage run --source=modules --omit="*/notebooks/*" -m pytest tests/`
then `python -m coverage report --include="modules/*/code/*.py"`:

| Subsystem | File coverage (line) |
| --- | --- |
| M03 search | `search_algorithms.py` 65% |
| M04 logic | `prop_logic.py` 39%, `fol_core.py` 55%, `expert_system.py` 73% |
| M05 uncertainty | `variable_elimination.py` 66%, `alarm_network.py` 44% |
| M06 ML | `classifiers.py` 67%, `linreg.py` 74%, `unsupervised.py` 52% |
| M07 neural nets | `nn_numpy.py` 77% |
| M08 NLP | `text_pipeline.py` 58%, `seq_models.py` 26%, `text_data.py` 21% |
| M09 vision | `vision_core.py` 45% |
| M10 RL | `rl_envs.py` 46%, `dp.py` 48%, `tabular.py` 37%, `experiments.py` 65%, `dqn.py` 19% |
| M11 generative | `gen_models.py` 15%, `lora.py` 21%, `gen_data.py` 19% |
| M12 agents | `agent_core.py` 45%, `tools.py` 37%, `agent_data.py` 42% |
| **Total (25 imported files)** | **6,139 statements, 3,272 missed, 47%** |

**This is not complete coverage and is not presented as such.** The 47% is over the 6,139
statements in module files the suite imports; `coverage` reports nothing for files the suite never
imports, so the share of all Python in the repository is lower.

### Remaining untested code

- **M13 code** (`rai_data.py`, `fairness.py`, `explain.py`, `adversarial.py`) — not imported by any
  test; the new LAB-13-01 starter exercises `fairness.py` at run time but not under pytest.
- **M14 code** and the **prerequisite** packages — no tests.
- **Generative training loops** (VAE/GAN/DDPM training, `train_dqn`, `reinforce`, PPO) — only
  schedules, heads and parameter mechanics are tested; full training runs were left out to keep the
  suite CPU-friendly.
- **CLI `main()` functions and plotting paths**, notebook-only helpers, and M11 `gen_data` corpora.
- Argument-parsing, file-writing and environment-variable branches are largely uncovered.

---

## 3. Task 3 — Laboratory starter material

The 18 laboratories without inline code now all have starter material. Two forms were used, and no
file was created where a guided notebook already does the job.

**Seven new runnable starter scripts** (each executed during this phase; all exit 0):

| Lab | Starter | What it does | What is left to the student |
| --- | --- | --- | --- |
| LAB-03-01 | `labs/starters/lab-03-01_starter.py` | 12×12 street grid, 9 origin–destination pairs, BFS/UCS/A* table | One-way streets, greedy/DFS columns, cost analysis |
| LAB-03-02 | `labs/starters/lab-03-02_starter.py` | Tic-tac-toe minimax; CSP timetable with 4 courses, 5 slots, 2 rooms | Depth-aware scoring; room constraint; feasibility report |
| LAB-05-01 | `labs/starters/lab-05-01_starter.py` | Rain–Sprinkler–Wet elimination and fuzzy membership skeleton | Rule base, centroid defuzzification, comparison with a threshold controller |
| LAB-13-01 | `labs/starters/lab-13-01_starter.py` | Loads `rai_datasets.npz`, trains logistic baseline, prints four group metrics and DI ratio | Threshold justification, reweighing mitigation, trade-off defence |
| LAB-13-02 | `labs/starters/lab-13-02_starter.py` | Offline toy assistant, 6 injection attacks, 3 benign controls, pass/fail report | Four more attacks (one via retrieved document), a defence, precision/recall |
| LAB-14-01 | `labs/starters/lab-14-01_starter.py` | numpy two-layer message passing on a synthetic two-community graph, with feature-only baseline | Second modality, edge types, graph-ablation argument |
| LAB-14-02 | `labs/starters/lab-14-02_starter.py` | Latency p50/p95 by batch size and int8 quantisation error on a numpy model | Serving budget, quantisation sweep, rollback runbook |

Each starter states its inputs/outputs, prints a baseline, marks gaps with `TODO`, runs with the
documented interpreter and requires only packages the course already uses. The M13/M14 starters
deliberately avoid API keys and networks.

**Eleven laboratories already served by a guided notebook** now carry a `## Starter material`
section linking the notebook and the module's `code/` directory instead of a duplicate script:
LAB-06-01…04, LAB-07-02, LAB-07-03, LAB-11-01…03, LAB-12-01, LAB-12-02, plus LAB-13-01 links
NB-13-01 as related material.

All 18 links resolve (`audit/check_course.py`: 18 labs with starter material, 7 with a script,
0 broken starter links). Purely analytical labs (for example the M13 governance case study) were
not given scripts.

---

## 4. Task 4 — Extension challenges

Added as clearly optional `## Extension challenges (optional)` sections to the four labs that had
none, three challenges each:

- **LAB-13-01** — threshold sweep against both gaps; proxy leakage; bootstrap interval for the DI
  ratio.
- **LAB-13-02** — indirect injection through retrieved documents; defence precision/recall on a
  labelled set; capability removal versus refusal.
- **LAB-14-01** — modality ablation against seed spread; graph-versus-no-graph evidence; relation-
  specific edges and their parameter cost.
- **LAB-14-02** — p95 latency budget derived from a user requirement; float32/int8-dynamic/int8-
  static sweep; a one-page rollback runbook.

Each is marked optional and unmarked, and each asks for a measurement or an artefact rather than a
restatement of the lab.

---

## 5. Task 5 — Licensing proposal (proposal only)

`LICENSE-AND-ATTRIBUTION-PROPOSAL.md` written. **No licence file was added and nothing was
relicensed.** The proposal records:

- **Inspection results:** no `LICENSE`/`COPYING` anywhere; no copyright line; no vendored
  third-party code; no bundled third-party datasets (the two `.npz` files are generated by seeded
  course code, and `dataset_cards.json` declares `CC0-1.0` with known limits); no third-party
  images; no model weights committed; attribution for Fashion-MNIST present at the point of use.
- **Proposed split:** MIT for original code, CC BY 4.0 for original educational content, CC0 1.0
  for original synthetic datasets, with third-party materials and external models explicitly
  excluded from any repository licence.
- **Exclusion table:** scikit-learn `load_digits` (BSD-3 / UCI CC BY 4.0), Fashion-MNIST (MIT,
  research use), Iris (CC BY 4.0), `gpt2` (MIT), `t5-small`/`flan-t5-small` (Apache-2.0),
  `distilbert-base-uncased` (Apache-2.0), `all-MiniLM-L6-v2` (Apache-2.0).
- **Pre-application gaps:** the FAQ currently says permission is required and would contradict an
  open licence; model licences are not stated uniformly in M11; no copyright holder/year line; the
  notebook code/prose split must be stated.
- **Mechanical change if approved:** `LICENSE`, `LICENSE-CONTENT`, `LICENSE-DATA`, a README licence
  section and the FAQ edit, as one reviewed commit.

---

## 6. Task 6 — Citation metadata

`CITATION.cff` created as a proposal. Verified content only:

- `cff-version: 1.2.0`, `title`, `abstract`, `type: software`;
- author **Engr. Dr. Muhammad Nadeem Majeed**, family `Majeed`, given `Muhammad Nadeem`,
  affiliation *Department of Data Science (PUCIT), University of the Punjab, Lahore, Pakistan*;
- `repository-code` and `url` from `git remote -v`
  (`https://github.com/nadeem-majeedch/Artificial-Intelligence-Course`);
- keywords.

**Deliberately omitted and documented:** DOI (none exists), release version (no tagged release),
publication date (no release date to state), archival identifier, ORCID (none supplied). Git metadata
shows a single author identity, `Dr. Muhammad Nadeem Majeed`, consistent with the CFF author.

Validation: parsed with PyYAML — 9 top-level keys, 1 author, all CFF-required keys present, no
`doi`/`version`/`date-released`/`identifiers`/`orcid` fields. Not validated with `cffconvert`
(not installed); YAML syntax and required-key checks are the extent of the verification.

---

## 7. Task 7 — External reference verification

`audit/verify_references.py` fetches every entry's link, queries the arXiv API once for all arXiv
identifiers, and compares title (fuzzy), first-author surname and year. It parses both bibliography
layouts: heading entries in `resources/library/` and table rows in `resources/research-papers.md`
(the first version of the script missed the table rows entirely; that was a defect in the checker,
not in the bibliography). Results are stored in `audit/reference_verification.json`.

**95 entries measured**: 44 in `resources/research-papers.md`, 43 in
`resources/library/papers-and-surveys.md`, 8 in `resources/library/ai-agents.md`. 59 entries carry an
arXiv link; they resolve to 38 unique identifiers because several papers appear in two files.

| Status | Count | Meaning |
| --- | ---: | --- |
| Verified against arXiv | 65 entries (38 unique IDs) | Title, first author and year agree |
| Verified, version year differs | 3 | Same work, journal year after the preprint |
| Verified, preprint documented | 2 | Entry links the preprint and names it while citing the published venue |
| Reachable, publisher gatekeeper (HTTP 202/403) | 1 | URL valid; scripted fetch blocked |
| Access-restricted (paywalled) | 24 | No URL to fetch; retained, per instructions |
| Unreachable or unverifiable arXiv entry | 0 | — |

Notes:

- **Datasheets for Datasets** — entry cites *Communications of the ACM*, 2021; arXiv v1 is 2018.
  Title and authors exact, so this is a version-year difference, not an error.
- **Fairness in Machine Learning: A Survey** — entry cites *ACM Computing Surveys* 56(7), 2024;
  arXiv 2020. Same conclusion. The third version-year case is the *Journal of Machine Learning
  Research* edition of a paper whose arXiv preprint predates it.
- **Dropout (Srivastava et al.)** — the entry cited the JMLR 2014 paper but linked arXiv
  `1207.0580`, which is the earlier preprint under a different title. The row now names that
  preprint explicitly; the citation and the link no longer disagree silently.
- **Batch Normalization (Ioffe & Szegedy)** — the title was truncated to two words; restored to the
  full published title, which now matches arXiv exactly.
- **Mnih et al. (2015)** — entry links arXiv `1312.5602` ("Playing Atari with Deep Reinforcement
  Learning") while citing the *Nature* paper, and says so in the row. Recorded as a documented
  preprint pair rather than flagged.
- **ImageNet (CVPR 2009)** — IEEE Xplore answers scripted requests with 202. The DOI was checked
  independently through Crossref (`10.1109/CVPR.2009.5206848`, correct title, venue, 2009,
  first author Deng) and added to the entry.
- **Five paywalled references** (Hart/Nilsson/Raphael 1968; Rumelhart/Hinton/Williams 1986;
  Cortes/Vapnik 1995; Breiman 2001; and one further IEEE/Springer item) were kept. Access
  restriction is not a metadata defect.
- The local TLS context disables certificate verification because this machine has no CA bundle for
  Python; the script only reads public metadata and writes nothing outside `audit/`.

---

## 8. Task 8 — Regression testing

| Check | Command | Result |
| --- | --- | --- |
| Python tests | `python -m pytest tests/ -q` | **138 passed**, 0 failed, 17.7 s |
| Compile all Python | `python -m compileall -q modules prerequisites assessments audit tests` | exit 0 |
| Links and anchors | `python audit/check_course.py` | **4,115 links, 0 broken**; 0 missing anchors |
| Lesson exercises | same | 89 lessons, 0 with fewer than 2 items |
| Lab starter links | same | 18 labs, 7 scripts, 0 broken |
| Extension challenges | same | 4/4 present |
| Citation syntax | same | YAML parsed, required keys present, no invented fields |
| Notebook execution | `jupyter nbconvert --execute nb-03-01-search-workbench.ipynb` | exit 0 (representative notebook; see limitation) |
| Staging | `git diff --cached --stat` | empty |

Notebooks: no `.ipynb` file was modified in this phase, so the Phase 23 notebook baseline
(35 notebooks, 31 pass, 4 pass with warnings) still applies. One representative notebook was
re-executed to confirm the environment still runs notebooks; the full 35-notebook sweep was not
repeated, so this report does not claim a fresh full sweep.

**Pre-existing defects found and fixed while validating links:**

- `docs/ARCHITECTURE.md` linked `../lessons/L03-04-heuristics-and-greedy-best-first-search.md`,
  `../notebooks/nb-03-02-search-benchmarks.ipynb` and `../labs/lab-03-01-campus-route-planning.md`
  — none of these files exist. Corrected to the real paths under
  `modules/M03-problem-solving-and-search-algorithms/`.
- The same document's M03 layout diagram listed a duplicated notebook line and a notebook that does
  not exist; corrected to the actual file.

These were reported as "0 broken" in Phase 23 because that checker did not parse HTML anchors
(`<a id="m01">`), did not strip inline code (the literal example `[text](target)` was treated as a
link), and used a slug function that collapsed the double hyphen produced by an em dash. The new
checker handles all three; the corrected count is 4,115 links, 0 broken.

---

## 9. Files added or changed in this phase

**Added**

- `tests/` — `conftest.py` and 10 test modules (138 tests).
- `modules/M03…/labs/starters/lab-03-01_starter.py`, `lab-03-02_starter.py` (2 files)
- `modules/M05…/labs/starters/lab-05-01_starter.py`
- `modules/M13…/labs/starters/lab-13-01_starter.py`, `lab-13-02_starter.py` (2 files)
- `modules/M14…/labs/starters/lab-14-01_starter.py`, `lab-14-02_starter.py` (2 files)
- `audit/check_course.py`, `audit/verify_references.py`, `audit/reference_verification.json`
- `LICENSE-AND-ATTRIBUTION-PROPOSAL.md`, `CITATION.cff`, this report.

**Modified**

- 18 laboratory Markdown files: `## Starter material` section (and the four extension sections).
- `resources/library/papers-and-surveys.md`: DOI added to the ImageNet entry.
- `resources/research-papers.md`: Dropout row now names its linked preprint; Batch Normalization
  title restored to the full published title.
- `docs/ARCHITECTURE.md`: four stale paths and one duplicated diagram line corrected.
- `tests/test_nn.py`: one over-tight Adam assertion replaced by a bound justified by adaptive
  scaling.

**Not touched:** lesson content, existing course implementations (except the Phase 23 Otsu fix),
notebooks, assessment questions, Git history, CI configuration.

---

## 10. What remains outstanding

1. **Licensing approval.** The proposal is a recommendation; no licence is in force. The FAQ's
   "permission required" answer must change in the same commit as any licence file.
2. **Coverage gaps.** M13 and M14 code, prerequisites, DQN/VAE/GAN/PPO training loops and CLI
   paths have no automated tests. Measured coverage is 47% of imported module statements, not the
   whole repository.
3. **Full notebook sweep.** Not re-run in this phase; no notebook changed, but the Phase 23 result
   is now three phases old.
4. **Model licence statements** in M11 are not uniform; the proposal lists this as a pre-application
   gap rather than editing lessons in a remediation phase.
5. **Exercise counts above target.** Four M11 lessons carry 7–9 exercises. This is a deliberate
   non-change; an academic reviewer may prefer a split into "core" and "extension".
6. **No CI.** The checks exist as scripts and were run manually, as required by the restriction on
   GitHub Actions.
7. **Academic acceptance.** Technical checks passing says nothing about academic peer review. This
   phase raises implementation confidence and removes documented defects; it does not constitute
   academic validation, and the exercise, citation and licensing items still need a human reviewer.
