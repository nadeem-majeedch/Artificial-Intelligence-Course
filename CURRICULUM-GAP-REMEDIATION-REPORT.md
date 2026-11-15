# Curriculum Gap Remediation Report — Phase 21

**Date:** 12 November 2026
**Scope:** resolve the gaps identified by Phase 20 (`STUDENT-SELF-STUDY-ACCEPTANCE-REPORT.md`)
**Phase 21A (12 November 2026):** the M05 Bayesian-network defect reported below has been
investigated to root cause, repaired and retested — see §2.1. The remaining gaps are unchanged.

**Status:** **partially complete — acceptance is NOT claimed.**

**Phase 21B (12 November 2026):** M05 gained a tested variable-elimination implementation and lesson;
M02 and M08 are now complete. The Phase 21B update at the end of this report supersedes the
"remaining gaps" sections above wherever they conflict, and it is the current statement of status.

Four modules were in scope for content creation (M03, M05, M02, M08, M12, plus prerequisite
exercises). Three (M03, M05, M12) now have published lessons, executed notebooks and labs. **M02 and
M08 were not remediated in this phase** and the prerequisite exercise upgrade was not started; both
are listed as remaining gaps below, and the Phase 20 acceptance verdict therefore still stands.

Nothing was committed, staged, pushed, or configured in CI or Pages. No existing lesson, notebook or
lab was deleted; no unrelated module was rewritten.

---

## 1. Previously missing material (from Phase 20)

| Module | Phase 20 finding | Phase 21 outcome |
| :--- | :--- | :--- |
| M03 Problem Solving and Search | No module directory, no lessons, no lab | **Resolved** — 7 lessons, notebook, 2 labs, code |
| M05 Uncertainty and Reasoning | No module directory, no lessons | **Resolved** — 5 lessons, notebook, 1 lab |
| M12 AI Agents | README with 6 planned lessons, 0 published, no labs | **Resolved** — 6 lessons, 2 labs, 1 project |
| M02 Intelligent Agents | 1 of 5 lessons | **Not resolved** — unchanged |
| M08 NLP | Reference code only, no lessons, no labs | **Not resolved** — unchanged |
| Prerequisites | Mini-lab only, no multi-part exercises | **Not started** — unchanged |

## 2. Newly developed material

### M03 — `modules/M03-problem-solving-and-search-algorithms/`

| Artefact | Detail |
| :--- | :--- |
| `README.md` | Module page: outcomes, map, study plan, assessment, navigation |
| 7 lessons | L03-01 formulation · L03-02 uninformed (BFS/DFS/UCS/DLS/IDS) · L03-03 informed (greedy, A\*, heuristics) · L03-04 local search (hill, annealing, GA) · L03-05 minimax and alpha–beta · L03-06 CSP · L03-07 strategy selection |
| `code/search_algorithms.py` | All fifteen algorithms, standard library only, shared graph interface, `run_comparison()` |
| `notebooks/nb-03-01` | 9 code cells, executed |
| 2 labs | `lab-03-01` route planning under constraints; `lab-03-02` game agent and timetable solver |

Measured facts used in the lessons and notebook (grid 6×6, four blocked cells, Manhattan heuristic):
BFS 31 expansions, cost 10; DFS 24 expansions, cost 24 (not optimal); UCS 31, cost 10; A\* 31, cost
10; greedy 10 expansions, cost 10 on this instance; IDS 66 expansions for the same solution. With the
heuristic scaled by 1.5, A\* expands 10 nodes. Hill climbing reached 0 conflicts on 4 of 5 random
starts; annealing reached 0. Alpha–beta returned the minimax value, 2.

### M05 — `modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/`

| Artefact | Detail |
| :--- | :--- |
| `README.md` | Module page |
| 5 lessons | L05-01 probability and Bayes · L05-02 Bayesian networks and inference · L05-03 naive Bayes · L05-04 fuzzy sets and membership · L05-05 fuzzy inference and defuzzification |
| `code/alarm_network.py` | Full CPTs, exact enumeration, evidence validation, self-tests (Phase 21A) |
| `notebooks/nb-05-01` | 9 code cells, executed from a clean kernel (2.3 s); all self-tests pass |
| 1 lab | `lab-05-01` Bayesian classifier plus fuzzy ventilation controller |

**Defect resolved in Phase 21A.** The alarm-network enumeration that printed the same posterior for
every evidence combination is fixed; see §2.1. The worked example, the evidence table and the
step-by-step derivation are back in L05-02, backed by a tested module.

### 2.1 M05 defect investigation (Phase 21A)

**Symptom.** `nb-05-01` printed `P(B|j,m) = 0.374` and `P(B|j,¬m) = 0.374` — identical posteriors for
different evidence.

**Root cause.** The conditional probability table for the alarm stored only `P(A=True | b, e)`:

```python
P_A = {(True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001}
... P_A[(b, e)] * ...      # used for BOTH a=True and a=False
```

Yet the enumeration also visits `a=False`, where the factor should be `1 - P(A=True | b, e)`. Using the
`a=True` value there made the joint distribution sum to **0.005032884** instead of 1. Because the
alarm factor was the same number for both values of A, the A-summation barely depended on the callers,
and every posterior collapsed toward the same value. The code ran, printed plausible numbers, and was
wrong — the failure mode that normalisation tests exist to catch.

**Repair.** `modules/M05-.../code/alarm_network.py` now stores full CPTs and applies the complement in
`p_alarm()`, validates evidence (unknown nodes and non-boolean values raise `ValueError`), and ships
`run_tests()` declaring eight groups of assertions: joint normalisation (1.0 to 1e-12), marginal priors,
B ⊥ E, published posteriors, monotone evidence response, explaining away, order-independence of
evidence, and rejection of invalid input.

**Independently verified results** (joint total 1.0):

| Evidence | P(B\|e) | P(e) |
| :--- | ---: | ---: |
| none | 0.0010 | 1.0000000 |
| John calls | 0.0163 | 0.0521390 |
| Mary calls | 0.0561 | 0.0117363 |
| both call | 0.2842 | 0.0020841 |
| John only | 0.0051 | 0.0500549 |
| Mary only | 0.0069 | 0.0096522 |
| neither calls | 0.0001 | 0.9382088 |
| earthquake | 0.0010 | 0.0020000 |
| earthquake, both call | 0.0033 | 0.0003669 |

Cross-checks: hand-derived branch sums for the both-call case give P(b,j,m) = 0.00059224 and
P(¬b,j,m) = 0.00149186, so the posterior is 0.28424 — matching the textbook value 0.284 for the
Russell–Norvig alarm network. P(A|J) = 0.0434 is consistent with Bayes: 0.90 × 0.002516442 / 0.0521390.
P(B|E) = P(B) = 0.0010 confirms the modelled independence of B and E, while P(B|e,j,m) = 0.0033 against
P(B|j,m) = 0.2842 demonstrates explaining away at the collider.

### M12 — `modules/M12-ai-agents-and-agentic-systems/`

| Artefact | Detail |
| :--- | :--- |
| `README.md` | Rewritten: status, module map, code table, mermaid diagram, study plan |
| 6 lessons | L12-01 foundations and architecture · L12-02 tool calling and structured outputs · L12-03 planning, memory and orchestration · L12-04 frameworks and implementation · L12-05 multi-agent systems · L12-06 MCP, security and evaluation |
| 2 labs | `lab-12-01` tool-using support agent; `lab-12-02` security and evaluation |
| 1 project | `projects/mp-12-multi-tool-agent.md` — four tools, approval binding, resumption, evaluation |

The labs and project are CPU-only and use the module's deterministic policy; no paid API is required
anywhere.

## 3. Lessons and labs per module (after this phase)

| Module | Lessons | Notebooks | Labs | Projects |
| :--- | ---: | ---: | ---: | ---: |
| M01 | 5 | 1 | 2 | 0 |
| M02 | 1 | 0 | 0 | 0 |
| M03 | 7 | 1 (executed) | 2 | 0 |
| M04 | 7 | 2 | 0 | 0 |
| M05 | 5 | 1 (executed) | 1 | 0 |
| M06 | 10 | 4 | 4 | 0 |
| M07 | 8 | 3 | 3 | 0 |
| M08 | 0 | 0 | 0 | 0 |
| M11 | 7 | 2 | 3 | 0 |
| M12 | 6 | 0 | 2 | 1 |
| M13 | 6 | 1 | 2 | 0 |
| M14 | 5 | 1 | 2 | 0 |

M03, M05 and M12 statuses in `modules/README.md` now read "complete" for the material actually
published; the availability notices in `assessments/quizzes/quiz-m03.md`, `quiz-m05.md` and
`quiz-m12.md` were replaced with accurate statements. Notices for M02, M08, M09 and M10 are unchanged
because those modules are still incomplete.

## 4. Notebook execution results

| Notebook | Result |
| :--- | :--- |
| `nb-03-01-search-workbench.ipynb` | **Executed** — 3.3 s, 9 code cells, outputs stored |
| `nb-05-01-uncertainty-workbench.ipynb` | **Executed from a clean kernel** — 2.3 s, 9 code cells, outputs stored; normalisation, evidence and invalid-input tests pass (Phase 21A) |
| Other module notebooks | Not re-executed in this phase. A heuristic scan found 13 of them without stored outputs on every code cell; that check is not a reliable executed-versus-not signal, so their Phase 20 execution status is neither confirmed nor refuted here. |
| Prerequisite notebooks | Not re-executed in this phase (6/6 passed in Phase 20) |

Two defects were found by executing rather than reading:

1. `run_comparison()` in `search_algorithms.py` returned 3-tuples where the notebook expected 4, so the
   notebook cell raised `ValueError`. Fixed, and the notebook re-executed.
2. `m = NB().fit(docs, labels)` in `nb-05-01` bound `None`, because `fit` returns nothing. Fixed by
   calling `fit` on its own line, then re-executing.

## 5. Broken links

| Run | Internal links checked | Broken targets | Broken anchors |
| :--- | ---: | ---: | ---: |
| Before fixes | 3,689 | 6 | 0 |
| After fixes | 3,689 | **0** | **0** |

The six were: two `../quizzes/quiz-03.md` references in the M03 labs (the quiz lives at
`assessments/quizzes/quiz-m03.md`), one relative `labs/…` path in L03-07, and one glossary link in the
M05 README that named a non-existent glossary page (now the glossary index). The checker strips fenced
and inline code and accepts `<a id="…">` anchors, as in earlier phases.

## 6. Remaining curriculum gaps

Honest list, in the order the Phase 21 brief set them:

1. **M02 Intelligent Agents (Priority 3) — not done.** L02-02 through L02-05 do not exist: simple
   reflex and model-based agents, goal-based and utility-based agents, learning agents, and agent
   architectures/design. No M02 lab exists. The module still has 1 of 5 lessons and its README and
   the `quiz-m02.md` availability notice remain accurate as written.
2. **M08 NLP (Priority 4) — not done.** No lessons, notebooks or labs. All sixteen mandated topics
   (preprocessing, tokenization, stemming, BoW, n-grams, TF-IDF, embeddings, Word2Vec, classification,
   sentiment, NER, language models, seq2seq, attention, transformers, Urdu/English examples) remain
   untaught; only the reference code is published.
3. **Prerequisite exercises (Priority 6) — not started.** The six prerequisite notebooks and their
   mini-labs are unchanged; the 21 prerequisite lessons still have a single mini-lab each and no
   multi-part `Exercises` section.
4. **M05 depth.** Two topics in the Phase 21 brief — conditional independence as a standalone treatment
   and inference beyond enumeration (variable elimination) — are covered inside L05-02 rather than as
   separate lessons. The planned second M05 lab and second notebook were not built. The alarm-network
   defect described in §2.1 was resolved in Phase 21A, with tests and a re-executed notebook.
5. **M12 notebook.** `modules/README.md` lists a notebook among M12's planned components; none was
   created. Lessons, labs and the project do not depend on it.
6. **Navigation is only partly updated.** Module statuses in `modules/README.md` and the three quiz
   notices were corrected, but `docs/learning-path.md` and `docs/course-roadmap.md` still describe M03,
   M05 and M12 as forthcoming and were **not** edited in this phase, so they currently understate what
   is available. `activateSTUDENT-SELF-STUDY-ACCEPTANCE-REPORT.md` was not edited, by design: it is
   superseded only by a retest, and no retest was run.
7. **Student learning journeys were not retested.** No end-to-end student run through M03, M05 or M12
   was performed, so nothing here supports an acceptance claim. The Phase 20 verdict ("conditional
   acceptance") is unchanged.

## 7. What a reviewer should check next

1. Review the M05 evidence table against a second independent implementation, then add the variable
   elimination exercise as a separate lesson.
2. Write M02 L02-02…L02-05 and the two labs, then update `quiz-m02.md`.
3. Write the M08 lesson set, two notebooks and three labs.
4. Update `docs/learning-path.md` and `docs/course-roadmap.md` for M03, M05 and M12.
5. Re-run the full notebook suite and the link checker after each change.
6. Only then re-run the student self-study journeys and issue a new acceptance verdict.

---

## Phase 21B update — 12 November 2026

### 1. M05: variable elimination (Task 1 — complete)

| Artefact | Detail |
| :--- | :--- |
| `lessons/L05-06-variable-elimination-and-factor-algebra.md` | Factor algebra, evidence restriction, multiplication, summing out, ordering, induced width, cost comparison against enumeration |
| `code/variable_elimination.py` | Generic NumPy-backed `Factor` (restrict, multiply, sum_out, normalize), `variable_elimination(factors, query, evidence, order, trace)`, network-agnostic; no posterior hardcoded |
| `notebooks/nb-05-02-variable-elimination.ipynb` | 8 code cells, executed from a clean kernel in 2.5 s |

Worked numbers in the lesson are the measured intermediates: after eliminating E,
g1(A=T,B=T)=0.94002, g1(A=F,B=T)=0.05998, g1(A=T,B=F)=0.001578, g1(A=F,B=F)=0.998422;
after eliminating A, g2(B=T)=0.5922426 and g2(B=F)=0.0014934; multiplying by the prior and
normalising gives **P(B|j,m)=0.2842**, matching the enumeration value in L05-02.

Verification (all assertions in `run_tests()`, executed): factor algebra on hand-checkable tables;
agreement with `alarm_network.enumerate_posterior` for nine evidence cases; agreement with a
brute-force sum over the 32-entry joint table for the same nine cases; identical results under two
elimination orders; and rejection of invalid evidence. Worst absolute difference across the three
implementations: **1.1e-16**; joint total 1.0.

Two defects were found and fixed while building this — both real, neither cosmetic:

1. `Factor.from_array` stored NumPy integer indices as table keys. Because `True == 1` in Python, every
   `table[(True, ...)]` lookup returned the *False* slice, so all posteriors collapsed to 0.5. Fixed by
   keying on booleans.
2. Evidence naming an unknown variable was silently ignored (the factor simply had no such variable).
   `variable_elimination` now raises `ValueError` for unknown names, non-boolean values, an unknown
   query, or a query that appears in the evidence.

### 2. M02: intelligent agents (Task 2 — complete)

Five lessons, one executed notebook, two labs.

| ID | Title |
| :--- | :--- |
| L02-02 | Rational Agents and PEAS Descriptions (rationality, omniscience, PEAS design, autonomy) |
| L02-03 | Task Environments and Their Properties (seven dimensions, MDP formalisation, GridWorld) |
| L02-04 | Simple Reflex and Model-Based Agents (completeness, belief state, bump handling) |
| L02-05 | Goal-Based, Utility-Based and Learning Agents (subgoals, utility, critic + learning element) |

The five required implementations already existed in `code/agents.py` (`ReflexAgent`,
`ModelBasedAgent`, `GoalBasedAgent`, `UtilityBasedAgent`, `LearningAgent`); they are now taught,
measured and exercised rather than merely present. `nb-02-01-agent-loop-gridworld.ipynb` (7 code
cells, executed in 2.2 s) runs all five agents, the learning curve and four checks.

Labs: `lab-02-01-intelligent-vacuum-cleaner.md` and `lab-02-02-campus-navigation-agent.md`, each with
scenario, environment definition, requirements, starter code, expected behaviour, tests, rubric and
extensions.

**A claim was corrected during this task.** The architecture comparison originally read "goal-based 7
steps", which is only true with a *full* percept. Measured with the local percept that `agents.py`
defaults to, model-based, goal-based and utility-based all take 15 steps; the planner reaches 7 only
when it can see the goal. Lessons, module README and notebook now state both settings — the difference
is itself the module's main result (the environment chooses the architecture).

### 3. M08: natural language processing (Task 3 — complete)

Six lessons, three executed notebooks, three labs.

| ID | Title |
| :--- | :--- |
| L08-01 | Introduction to NLP and the Text Pipeline |
| L08-02 | Preprocessing, Tokenization, Stemming and Lemmatization (incl. Urdu script problems) |
| L08-03 | Bag of Words, N-grams and TF-IDF |
| L08-04 | Word Embeddings, Word2Vec and Semantic Similarity (PPMI + SVD, skip-gram maths) |
| L08-05 | Text Classification, Sentiment Analysis and NER (BIO, span F1, macro-F1) |
| L08-06 | Sequence Models, Attention and Transformers |

Notebooks, all executed from a clean kernel: `nb-08-01-tokenisation-and-features.ipynb` (2.4 s, 7
cells), `nb-08-02-classification-and-ner.ipynb` (1.3 s, 7 cells), `nb-08-03-attention-and-sequences.ipynb`
(2.0 s, 6 cells). Verified outputs include: attention rows summing to 1; unscaled logits saturating the
softmax to a max weight of 1.000 while scaled logits give 0.647; causal masking producing
[1,0,0,0]…[0.015,0.016,0.08,0.889]; permutation invariance without positional encodings and its
disappearance with them; a constant-`O` tagger scoring 0.571 token accuracy and 0 span F1; and Urdu
negation surviving tokenisation.

Labs: `lab-08-01-text-preprocessing-and-feature-extraction.md`,
`lab-08-02-news-and-document-classification.md`,
`lab-08-03-urdu-and-english-sentiment-and-ner.md`. Each states dataset provenance and licence
(synthetic, created for this repository) and requires per-language reporting.

**Deliberate non-claims.** `nltk`, `spaCy`, `transformers` and CPU `torch` are installed, but no
pre-trained model is downloaded, bundled or evaluated. No claim is made that any checkpoint supports
Urdu: the lessons say to record name, revision and measured performance before quoting a number.
`gensim` is not installed, so Word2Vec is taught through its objective and a NumPy PPMI+SVD
implementation, with the gensim call shown as a comment.

### 4. Integration (Task 4)

- `modules/README.md`: M02, M05, M08, M12 statuses now read complete for the material that exists.
- `assessments/quizzes/quiz-m02.md`, `quiz-m08.md`: availability notices replaced with accurate ones.
- `assessments/quizzes/quiz-m05.md`: coverage corrected from L05-01…L05-07 to L05-01…L05-06.
- `docs/learning-path.md`: six stale statements about M02/M03/M05/M08 replaced with accurate ones.
- Module READMEs for M02, M05 and M08 rewritten with lesson maps, labs, datasets and assessment.
- Lesson cross-references updated (L02-03 → `agents.py`; L05-02 ↔ L05-06; L08-05 → M06 L06-02;
  L08-06 → M07 L07-03).
- `docs/course-roadmap.md`: no stale M02/M08 statements found; unchanged.

### 5. Validation (Task 5)

| Check | Result |
| :--- | :--- |
| Markdown links | 338 files, **3,829 internal links, 0 broken targets, 0 broken anchors** (7 defects found and fixed in this phase) |
| Notebook execution | nb-02-01, nb-05-02, nb-08-01, nb-08-02, nb-08-03 executed this phase; nb-03-01 and nb-05-01 re-verified |
| Unit tests | `alarm_network.run_tests()` and `variable_elimination.run_tests()` both return True |
| Numerical equivalence | VE vs enumeration vs brute force, 9 evidence cases, worst difference 1.1e-16 |
| Python syntax | `agents.py`, `environments.py`, both M05 modules and all builders ran clean |
| Quiz/answer-key presence | 14 quizzes and 14 self-assessment sheets present; coverage lines checked for M02, M05, M08 |
| Lab references | every lab linked from its module README and its paired lessons exists |

Older notebooks (M01, M04, M06, M07, M11, M13, M14) were **not re-executed** in this phase; they store
no outputs, so their state is neither confirmed nor refuted here.

### 6. Remaining gaps after Phase 21B

1. **M12 notebook** — `modules/README.md` lists one among M12's planned components; none exists. No
   lesson or lab depends on it.
2. **M05 second lab** — only LAB-05-01 exists; the planned second lab was not written.
3. **Prerequisite exercises** — the six prerequisite notebooks still have a single mini-lab each and no
   multi-part `Exercises` section (Phase 21 priority 6, outside the 21B brief).
4. **Glossary** — new M05/M08 terms (factor, induced width, PPMI, BIO, span F1) are defined in the
   lessons but not yet added to `resources/glossary/`.
5. **Student journeys** — not retested. No acceptance claim is made, and the Phase 20 verdict stands.

### 7. Files created and modified in Phase 21B

**Created:** `modules/M05-.../lessons/L05-06-variable-elimination-and-factor-algebra.md`;
`modules/M05-.../code/variable_elimination.py`; `modules/M05-.../notebooks/nb-05-02-variable-elimination.ipynb`;
`modules/M02-.../lessons/L02-02…L02-05`; `modules/M02-.../labs/lab-02-01`, `lab-02-02`;
`modules/M02-.../notebooks/nb-02-01-agent-loop-gridworld.ipynb`; `modules/M08-.../lessons/L08-01…L08-06`;
`modules/M08-.../labs/lab-08-01`, `lab-08-02`, `lab-08-03`; `modules/M08-.../notebooks/nb-08-01`,
`nb-08-02`, `nb-08-03`.

**Modified:** `modules/M02-.../README.md`, `modules/M05-.../README.md`, `modules/M08-.../README.md`,
`modules/M05-.../lessons/L05-02`, `modules/README.md`, `docs/learning-path.md`,
`assessments/quizzes/quiz-m02.md`, `quiz-m05.md`, `quiz-m08.md`, this report.

Nothing was committed, staged, pushed, or configured in CI or Pages. No existing lesson or notebook was
deleted, and no unrelated module was rewritten.

---

# Phase 21C update — 12 November 2026

Supersedes the "remaining gaps" lists in Phase 21 and Phase 21B where they overlap.

## 1. Deliverables completed in this phase

| Task | Deliverable | Status |
| :--- | :--- | :--- |
| 1 | `modules/M12-.../notebooks/nb-12-01-agentic-ai-workbench.ipynb` | complete, executed (2.0 s) |
| 2 | `modules/M05-.../labs/lab-05-02-bayesian-network-inference-and-diagnosis.md` | complete, maths validated |
| 3 | `prerequisites/EXERCISES.md` (9 topics, 3 + 1 + 1 each) | complete, linked |
| 4 | `resources/glossary.md` (+15 entries) | complete, links validated |
| 5 | Documentation reconciliation | complete for the stale claims found |
| 6 | Notebook regression, all 28 notebooks | complete, 28 PASS |
| 7 | Six student journeys re-tested | complete, verdict below |
| 8 | QA (links, anchors, syntax, maths, assessments) | complete |

## 2. Task 1 — M12 integrated notebook

`nb-12-01-agentic-ai-workbench.ipynb` is 31 cells (16 markdown, 15 code) and covers the fourteen required
topics in order: agent architecture, goal decomposition, tool definitions and registration, structured
inputs and outputs with argument validation, tool selection, state management, memory (working notes
versus episodic trace), multi-step execution, error handling, human approval, permission boundaries,
evaluation, prompt-injection defence, and multi-agent collaboration. Everything runs against the
module's own `agent_core.py`, `guardrails.py` and `multi_agent.py`; there is no paid API. The optional
LLM path is named (`LLMPolicy`) and marked as not executed, because the phase forbids paid APIs.

Three defects surfaced while making it execute, all fixed:

1. `multi_agent.py`: `bus, board = MessageBus(max_depth=3)` raised `TypeError` on the first call to
   `build_team()` — the module's own labs assumed a working function. Repaired to two assignments.
2. The tool-selection demo used pure name/description overlap, so "calculate 26400 - 4000" scored 0 for
   `calculator`. The notebook now adds a numeric-signal rule, which is the lesson: lexical selection
   fails on arithmetic and needs a signal the request actually carries.
3. The approval demo looked like it worked while the role's scope list denied `send_email` before the
   gate was ever consulted. The notebook now grants the `external` scope explicitly and shows the real
   `awaiting_approval` outcome, with a note that scope checks and approval gates are two different
   defences.

## 3. Task 2 — LAB-05-02

Six-node HVAC fault network (fan failure F, dust clog D, overheating O, smoke S, alarm A, log warning M)
with full conditional probability tables. Students implement enumeration and variable elimination,
compare them under five evidence sets, analyse the independence assumptions and run a prior-sensitivity
sweep. Validated numbers used in the lab (joint sums to 1.0; VE equals enumeration to 1e-16):

| Evidence | P(O) | P(F) |
| :--- | ---: | ---: |
| none | 0.1774 | 0.0800 |
| alarm | 0.9066 | 0.3209 |
| alarm + smoke | 0.9983 | 0.3512 |
| alarm + no smoke | 0.7968 | 0.2846 |
| log warning only | 0.3728 | 0.3784 |
| alarm + log | 0.9640 | 0.7678 |

Prior sensitivity: P(O | A) = 0.786 / 0.907 / 0.966 at priors 0.02 / 0.08 / 0.25. The lab states plainly
that this is an educational simulation, not a diagnostic system.

## 4. Task 3 — prerequisite exercises

`prerequisites/EXERCISES.md` covers the nine topics with three graded exercises, one guided exercise
with expected output, and one independent challenge each, plus validation criteria and hints that stop
short of solutions. It is linked from `prerequisites/README.md`. All exercises are CPU-only and run in
seconds; nothing was added to notebook execution time.

## 5. Task 4 — glossary

15 entries added (Heuristic function, Variable elimination, Elimination ordering, Membership function,
Pointwise mutual information, Causal masking, Tool calling, Agent orchestration, Agent memory, Model
Context Protocol, Agent evaluation, Constraint satisfaction problem, Factor, Tokenization,
Lemmatization). The other nine named terms (rational agent, PEAS, state space, Bayesian network, TF-IDF,
word embedding, NER, human-in-the-loop, attention) already had entries. The glossary now holds 341
entries, each with a definition, a student-language gloss where the term needs one, a lesson link and a
formula where a formula helps. All links validate.

## 6. Task 5 — documentation reconciliation

Claims corrected against the files:

- `README.md` §9 availability paragraph was three phases out of date (it called M02 and M04 "in
  progress" and M03, M05 "syllabus entries only"). Rewritten to the measured state, and "eleven of them
  have their own page" corrected to thirteen.
- `modules/README.md`: M05 described as "5 lessons, 1 notebook, 1 lab" (actual 6/2/2); M12 omitted its
  notebook; both fixed.
- `modules/M12-.../README.md`: study time annotated (24 published hours against a 19-hour design budget).
- `modules/M05-.../README.md` and `L05-06`: now point at LAB-05-02, which is the lab that exercises the
  lesson's material; the old pointer sent students to LAB-05-01's classifier half.
- `prerequisites/README.md`: links the new exercise collection.

Lesson, lab and notebook counts were verified by counting files for all thirteen published modules; the
only remaining mismatches are the study-hour pairs listed in the acceptance report, where the module
page and the index deliberately measure different things.

## 7. Task 6 — notebook regression

28 notebooks, 28 PASS, 318.7 s total on CPU, no skips, no network requirement, no paid API. Full table
with per-notebook durations in [NOTEBOOK-REGRESSION-REPORT.md](NOTEBOOK-REGRESSION-REPORT.md).

## 8. Task 8 — QA results

| Check | Result |
| :--- | :--- |
| Markdown files scanned | 340 |
| Internal links checked | 3,882 |
| Broken links / anchors | 0 |
| Python files compiled | 72, 0 failures |
| `alarm_network.run_tests()` | True |
| `variable_elimination.run_tests()` | True |
| P(B \| j, m) by enumeration | 0.284172 (P(j,m) = 0.0020841) |
| Quizzes with answer keys | 14 of 14 |
| Programming assignments / self-assessment sheets | 15 / 15 |
| Labs / notebooks | 27 / 28 |

The link checker was itself wrong on the first pass: it collapsed spaces when slugifying headings, so
eleven correct GitHub-style anchors containing an em dash (`#5-worked-example--the-…`) were reported
broken. Fixed the checker, re-ran: zero broken. Report the tool, not the content.

Dataset licensing: no dataset is redistributed except `modules/M13-.../code/data/` (a synthetic
`rai_datasets.npz` and a synthetic dataset-card catalogue), both generated for the course. scikit-learn
toy datasets are loaded through the library, not vendored. M11 uses four Apache-2.0 models already
cached in the repository.

## 9. Remaining gaps after Phase 21C

These are content gaps, not documentation gaps. None of them can be closed by navigation work.

1. **M09 Computer Vision — nothing.** No directory, no page, no lessons, no labs, no notebooks. A quiz,
   an assignment and a self-assessment sheet exist for it. Either build the module or withdraw its
   assessment material.
2. **M10 Reinforcement Learning — reference code only.** Four tested modules, no lessons, no labs, no
   notebooks. The page is honest; the curriculum map still lists seven lessons.
3. **M04 — no labs and no mini-project**, although lessons, notebooks, quiz, assignment and sheet are
   published.
4. **Study-hour pairs** (M02, M03, M05, M08, M12) need one policy: either both pages state published
   hours, or both state design hours.
5. **Duplicate-content risk** is low but unmeasured: the same worked example (the alarm network) now
   appears in M05 lessons, LAB-05-01, LAB-05-02 and NB-05-01. Reading shows different uses — diagnosis,
   classifier, factor algebra, sensitivity — but a future editor should know it is one network in four
   places.
6. **Instructor information** is present in `docs/` and module pages; no instructor name is invented
   anywhere, and the repository still has no licence file. That is a decision for the owner, not a
   defect to fix silently.

## 10. Verdict

**PASS WITH WARNINGS.** Six of six student journeys complete to their stated scope; 28 of 28 notebooks
execute; 3,882 links resolve. The course is not complete as a fourteen-module programme: M09 has no
content and M10 has no teaching material, and both are advertised in the curriculum map.

## 11. Files created and modified in Phase 21C

**Created:** `modules/M12-.../notebooks/nb-12-01-agentic-ai-workbench.ipynb`;
`modules/M05-.../labs/lab-05-02-bayesian-network-inference-and-diagnosis.md`;
`prerequisites/EXERCISES.md`; `NOTEBOOK-REGRESSION-REPORT.md`.

**Modified:** `modules/M12-.../code/multi_agent.py` (defect fix);
`modules/M12-.../README.md`, `modules/M05-.../README.md`, `modules/M05-.../lessons/L05-06-...md`,
`modules/README.md`, `README.md`, `prerequisites/README.md`, `resources/glossary.md`,
`STUDENT-SELF-STUDY-ACCEPTANCE-REPORT.md`, this report.

Nothing was committed, staged, pushed, or configured in CI or Pages. No existing lesson, notebook, lab
or report was deleted.
