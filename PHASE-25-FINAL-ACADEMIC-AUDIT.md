# Phase 25 — Final Independent Academic and Technical Acceptance Audit

**Repository:** `C:\Users\Nadeem\Documents\Artificial-Intelligence-Course`  
**GitHub:** `https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git`  
**HEAD:** `fba4161` (unchanged)  
**Audit date:** 15 November 2026  
**Auditor role:** independent acceptance review; no development cycle started.

---

## 1. Executive summary

The repository is a coherent, unusually candid university-level AI course. It contains 14 modules,
89 lessons, 38 lab briefs, 35 course notebooks, 14 quizzes, 14 self-assessments, 22 assignments,
8 module projects, 12 capstone briefs and a complete capstone studio. The lessons generally teach
the subject they advertise: they define terms, work examples by hand, implement the idea, test an
assumption, and state limits. The practical layer is real, not decorative: notebooks execute, labs
have scenarios and deliverables, and the capstone has milestones and a rubric.

Independent verification found **no critical defect**. Thirty-four algorithm/maths checks passed
against hand calculations, brute force, finite differences, independent NumPy implementations or
scikit-learn. The full pytest suite passed (196 tests), all 35 course notebooks executed without a
failed cell (31 clean, 4 with library warnings), all 4,154 links resolved, and the curriculum-hour
and licensing-mechanics checks reported zero failures. LAB-14-01's five-seed results reproduced
exactly; ablations confirmed that its high inductive GCN accuracy comes from legitimate graph
structure and collapses when labels or edges are destroyed.

Four small content defects were found and corrected during the audit:

1. A worked attention example in M08 had softmax values that did not follow from its own logits.
2. M11's README still said M08 lessons were unpublished, although six M08 lessons exist.
3. The main README claimed every notebook runs in under a minute and that no notebook needs a
   download; the measured maximum is 82.8 s, and two M11 notebooks use cached model weights.
4. LAB-14-01 described `graphs.py` as a ~30 s run; it takes 147 s.

One substantive warning remains: exact M14 latency ratios are machine-dependent and did not
reproduce in this audit (int8 1.72× slower vs the stated 2.62×; pruning 1.10× vs 1.45×). The
direction of every claim held, but the exact constants should be presented as a measured range or
with the benchmark environment.

Two release constraints are owner decisions, not technical failures: the `google/flan-t5-small`
and UCI licence confirmations remain flagged for owner review, and no browser/site generator exists
in the repository, so visual acceptance was not executed. Markdown structure and links were checked.

**Academic acceptance: PASS WITH WARNINGS — READY WITH DOCUMENTED LIMITATIONS.**  
**Public-release readiness: PASS WITH WARNINGS — READY SUBJECT TO OWNER APPROVALS.**

---

## 2. Scope and methodology

### 2.1 What was inspected

- All 14 module READMEs: outcomes, prerequisites, module maps, study plans, assessments, hours.
- All 89 lessons structurally: title, objectives, prerequisites, exercises, self-check, references,
  code fences and mathematical notation. Fourteen representative lessons were read in depth across
  M01–M14, including the modules named for special attention (M03, M04, M05, M08, M09, M10, M11,
  M12, M13, M14).
- All 38 lab briefs structurally; LAB-05-02, LAB-13-01, LAB-13-02, LAB-14-01 and LAB-14-02 were
  reviewed in detail and representative code paths executed.
- All 35 course notebooks executed with clean kernels and no write-back.
- The full pytest suite and the audit scripts.
- LAB-14-01 code, starter, lesson, lab, notebook-adjacent materials and both Phase 24A reports.
- Licensing files, attribution inventory, citation metadata and the README/FAQ licence statements.
- Six student journeys derived from the actual navigation and learning-path pages.
- Git state, change inventory, generated artefacts and release tags.

### 2.2 What was not done

- No line-by-line legal review; licensing checks are mechanical and attribution questions remain
  owner decisions.
- No browser rendering or mobile/responsive visual inspection: the repository has no site
  generator, HTML pages or preview configuration, and none was created.
- Not every sentence of all 89 lessons was re-derived; structural coverage was complete, and deep
  technical checks targeted the mathematical core and the modules named in the brief.
- No commit, push, stage, tag, release, publish or deployment.

### 2.3 Evidence sources

- `PHASE-25-TECHNICAL-VERIFICATION.md` — commands, independent checks, notebook table, coverage.
- `PHASE-25-STUDENT-EXPERIENCE-AUDIT.md` — six journeys and navigation.
- `PHASE-25-DEFECT-AND-RISK-REGISTER.md` — findings by severity and status.
- `PHASE-25-RELEASE-READINESS-REPORT.md` — release verdict and owner actions.

---

## 3. Module-by-module academic scorecard

Ratings are qualitative: **Strong** = complete, accurate, well sequenced and well practised;
**Adequate** = sound but thinner in prose or practice; **Needs attention** = a material gap.
No module fell below Adequate.

| Module | Hours | Objectives & prerequisites | Lesson sequence and depth | Practice and assessment | Specific evidence / finding | Rating |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| **M01** Introduction | 12.8 | Clear; none required, P01 recommended | 5 lessons; definitions, history, capability audit, study workflow | NB, 2 labs, quiz, MP-01 | L01-04 separates capability families and asks for operational error cost; complete map | Strong |
| **M02** Agents | 17.9 | Clear; P01 | 5 lessons; percepts, PEAS, environments, four agent architectures | NB, 2 labs, quiz | L02-02 defines rationality as expected performance and ties PEAS to measurable outcomes; lessons are concise but complete | Strong |
| **M03** Search | 19.9 | Clear; P01, P02 | 7 lessons; formulation → uninformed → A* → local → adversarial → CSP → selection | NB, 2 labs, PA-02, quiz | A* optimality and admissibility/consistency explained correctly; independent Dijkstra/A*/BFS checks passed | Strong |
| **M04** Knowledge representation | 31.6 | Clear; P02 | 7 lessons; propositional/FOL, inference, unification, resolution, expert systems | 2 NBs, 3 labs, project, quiz | Resolution refutation and seven-step CNF are correct; MGU and occurs-check checks passed | Strong |
| **M05** Uncertainty | 20.6 | Clear; P03, M04 | 6 lessons; Bayes, BNs, naive Bayes, fuzzy sets/inference, VE | 2 NBs, 2 labs, quiz | Alarm CPTs normalised; VE matches brute force to 1e-12 on an independent net; explaining-away is taught numerically | Strong |
| **M06** Machine learning | 31.4 | Clear; P02–P04, M05 recommended | 10 lessons; splitting/leakage → regression → classification → metrics → bias/variance → trees/SVM → unsupervised → pipelines | 4 NBs, 4 labs, PA-06, MP-06, quiz | Metrics match scikit-learn; leakage is treated as a first-class topic; labs use real evaluation discipline | Strong |
| **M07** Neural networks | 24.9 | Clear; P02, M06 | 8 lessons; perceptron → backprop → training → regularisation → CNN → RNN → attention → transfer/autoencoders | 3 NBs, 3 labs, assignment, quiz | Backprop verified against finite differences; attention derivation correct; notebook warning is a library notice, not a failure | Strong |
| **M08** NLP | 24.3 | Clear; M07 for L08-06, P01 | 6 lessons; pipeline → preprocessing → BoW/TF-IDF → embeddings → classification/NER → attention | 3 NBs, 3 labs, quiz | Concise lessons but real labs; worked attention softmax was arithmetically wrong and was corrected during audit (D-01) | Adequate |
| **M09** Computer vision | 26.8 | Clear; M07, P02 recommended | 6 lessons; imaging → features → CNNs → detection → segmentation → advanced topics | 4 NBs, 4 labs, assignment, quiz | IoU, NMS and matching verified by hand; AP and per-class reporting are taught honestly | Strong |
| **M10** Reinforcement learning | 34.1 | Clear; M06, M05 MDP, P03 | 5 lessons; foundations → value-based → TD → deep RL → advanced RL | 3 NBs, 4 labs, MP-10, quiz | Q-learning bootstrap verified by hand; SARSA/Q-learning difference and reward-shaping condition stated correctly | Strong |
| **M11** Generative AI/LLMs | 23.3 | Clear; M07 essential, P04/M08 recommended (stale M08 statement fixed) | 7 lessons; landscape → tokens/attention → pretraining → prompting → RAG → PEFT → evaluation | 2 NBs, 3 labs, MP-11, quiz | Model weights and licences documented; two notebooks download/cache small models; flan licence flagged for owner review | Strong |
| **M12** Agentic AI | 27.8 | Clear; M11, M02 | 6 lessons; architecture → tool calling/structured output → planning/memory → frameworks → multi-agent → MCP security/evaluation | NB, 2 labs, MP-12, quiz | Tool schema, permission boundary, retries and prompt-injection controls are taught as engineering, not slogans | Strong |
| **M13** Responsible/explainable/secure AI | 22.4 | Clear; M07 essential, M11 recommended | 6 lessons; fairness → explainability → privacy → security → governance → auditing | NB, 2 labs, ASG-13, MP-13, quiz | Fairness metrics, calibration, Shapley efficiency and security harness verified; lab outputs match text | Strong |
| **M14** Advanced applications/capstone | 32.9 | Clear; M13 plus capstone prerequisites | 5 lessons; case studies → MLOps → monitoring → research reproduction → capstone studio | NB, 2 labs, capstone, quiz | Graph experiment valid and reproduced; exact serving-latency ratios are machine-dependent (D-05); capstone studio is complete | Strong |

### 3.1 Curriculum coherence

- The prerequisite chain is explicit and mostly linear: P01–P04 → M01–M07 → M08–M14, with named
  exceptions (M05 needs M04; M11 needs M07; M13 needs M07).
- Module outcomes map to eight course learning outcomes in `modules/README.md`; every module has
  objectives, a readiness check or prerequisites, a module map with times, a study plan and an
  assessment section.
- Conceptual progression is deliberate: search before logic, logic before uncertainty, ML before
  deep learning, deep learning before NLP/vision/RL, generative models before agents, and
  responsibility before the capstone.
- Practice is not an afterthought: every module has at least two labs or a project; the capstone has
  twelve briefs, four milestones and a rubric.
- The weakest prose density is in parts of M02, M03, M05, M08 and M12 (roughly 700–1,300 words per
  lesson versus 2,000–3,500 in M01/M04/M06/M07). Those lessons remain structured and are backed by
  notebooks/labs; this is an editorial observation, not an academic failure.

---

## 4. Independent mathematical and algorithmic verification

Full inputs, outputs, references and tolerances are in
`PHASE-25-TECHNICAL-VERIFICATION.md` §3. Summary:

| Area | Checks | Result |
| :--- | :--- | :--- |
| Search: Dijkstra/UCS, A*, BFS | 3 | All optimal/shortest results matched |
| Unification and occurs check | 3 | MGU and failure cases correct |
| Bayesian variable elimination | 5 | Matched brute force to 1e-12; alarm cross-check matched enumeration |
| Logistic regression and MLP gradients | 3 | Matched central finite differences to 1e-6 |
| GCN forward, normalisation, homophily | 3 | Matched independent NumPy to 1e-5 or better |
| SBM structure and inductive adjacency leakage | 4 | Rates within sampling tolerance; no test-row leakage |
| Vision: IoU, NMS | 3 | Hand calculations matched |
| Fairness and Shapley | 5 | Hand metrics and linear-Shapley values matched |
| Q-learning | 1 | Bootstrap target 0.9 matched hand calculation |
| Classification metrics | 4 | Matched scikit-learn to 1e-12 |

No mathematical error was found in the audited core algorithms. The one lesson arithmetic error
found (M08 softmax) was in prose, not in code, and is recorded as corrected.

---

## 5. LAB-14-01 independent findings

### 5.1 What is valid

- Random-mix and SBM generators produce symmetric graphs with the advertised class structure;
  measured SBM within/cross edge rates match `p_in`/`p_out` within sampling tolerance.
- Homophily is computed over directed edge endpoints and matches hand calculation.
- Inductive split is disjoint, stratified and complete (120/40/40).
- `A_fit` removes all test rows and columns except self-loops; `A_infer` removes test–test
  off-diagonal weight but keeps test–training edges. This is exactly the documented protocol.
- Test and validation labels are not flipped; only 12 of 120 training labels are noisy at 10%.
- Validation chooses the epoch; the test set is evaluated once after the model is fixed.
- The five-seed results reproduce exactly: random-mix transductive +0.467, inductive +0.575; SBM
  +0.395 and +0.465. Matched control gaps are +0.450 and +0.425.

### 5.2 Is the high inductive GCN accuracy a leak?

No evidence of leakage was found. With training labels shuffled, both models fall to chance
(0.100–0.125). With edges permuted, the GCN falls to 0.275, near the MLP. With features permuted,
the GCN retains 0.450 from the graph alone, well below the combined 0.825–0.925. The high result is
therefore graph structure plus weak features doing legitimate work on a synthetic homophilous task.
It is not evidence that a GCN will achieve 0.945 on a real citation or fraud graph.

### 5.3 Limitations retained, not hidden

- Inductive uses 60% labelled nodes versus 20% transductive; absolute values are not directly
  comparable, which is why the matched control is reported.
- Five seeds; GCN-8 has large variance.
- Synthetic families, independent SBM edges and equal class sizes.
- The perfect-homophily ceiling (~0.9) is a generator property, not a general method result.

**Decision:** retain the reported numbers. No correction to the graph experiment was required.

---

## 6. Notebook, test and lab results

- **Notebooks:** 35/35 executed, 0 failed cells, 4 warnings, 500.1 s. The two M11 notebooks use
  small pretrained weights on first run and then cache them. No notebook writes outputs back during
  this audit. Full table in the technical report.
- **Tests:** 196 passed in 61 s; no skips in the final run. Coverage of M13+M14 reference code is
  36.3% (722/1,989 statements), up from the Phase 24 figure of 34% because graph code and tests
  grew. Untested areas are generation scripts, demo mains, optional model paths and error branches.
- **Labs:** 38 lab briefs; all have a purpose/scenario, tasks, deliverable, and marking guidance or
  rubric in substance. Representative code paths ran successfully: fairness (5 s), security (11 s),
  efficiency (26 s), drift monitor (14 s), graph reference (147 s), graph starter (both families).
- **Assessment alignment:** quizzes and self-assessments exist for all 14 modules; solutions exist
  for all 14 quizzes; programming assignments cover 14 modules; analytical assignments cover eight;
  module projects exist for eight modules and the capstone supplies twelve briefs. Rubrics and
  deliverable limits are present in the reviewed labs.

---

## 7. Licensing and attribution status

The Phase 23C architecture is present and internally consistent:

| Material | Stated licence | Evidence |
| :--- | :--- | :--- |
| Original source code | MIT | `LICENSE`, README, `LICENSING-INVENTORY.md` |
| Original educational content | CC BY 4.0 | `CONTENT-LICENSE.md`, README |
| Original synthetic datasets | CC0 1.0 | `DATASET-LICENSE.md`, catalogue |
| Third-party material | Original terms | `THIRD-PARTY-ATTRIBUTIONS.md` |

`CITATION.cff` parses (10 keys, one author). The UCI digits/Iris licence status and
`google/flan-t5-small` model-card licence remain explicitly flagged for owner confirmation. Model
weights are not committed; two M11 notebooks download/cache them. Notebook outputs are runtime
outputs, not a relicensing of model text.

**No legal clearance is claimed.** The mechanical checker passed, but authorship, third-party
permission, quotation length and model-weight terms require the owner's review. No licence file was
changed during this audit.

---

## 8. Student experience

Six journeys were simulated; details are in `PHASE-25-STUDENT-EXPERIENCE-AUDIT.md`.

| Journey | Result |
| :--- | :--- |
| Complete beginner | Pass: reading diagnostic → P01–P04 → M01; clear entry points and readiness checks |
| Search learner | Pass: M03 sequence, notebook, two labs, PA-02, quiz |
| Machine-learning learner | Pass: M06 prerequisites, ten lessons, four notebooks/labs, assignment/project |
| NLP and vision learner | Pass with caveat: complete materials; M08 is concise and M11 model download needs internet once |
| Generative AI and agents | Pass with caveat: M07 attention → M11 → M12; cached weights are documented |
| Capstone learner | Pass: M14 lessons, labs, twelve briefs, rubric, milestones, template, proposal |

Navigation is consistent: 4,154 links, 0 broken; module index and learning paths agree with the
published material. The README remains student-facing; it is long but not a maintainer or
deployment manual. The only stale public statements found were corrected (D-02, D-03).

---

## 9. Visual review status

**Not verified.** The repository is static Markdown with 15 Mermaid diagrams, no HTML pages, no
site generator and no images. There is no browser target to render without inventing a deployment
configuration, which the brief forbids. Structural checks passed (headings, tables, link anchors,
code fences), but professional appearance, mobile responsiveness and rendered Mermaid diagrams
remain unverified. This is a documented limitation, not a claim that the visual layer passed.

---

## 10. Curriculum-hour reconciliation

The single method in `docs/CURRICULUM-MAP.md` §3.1 is applied consistently:

- Four components: guided 112.4, practical 110.0, assessment 75.8, project 52.5 = **350.7 h**.
- Prerequisites **56 h**; programme **406.7 h**.
- Core path **169 h** (P01 full + 50% of P02–P04 + M01–M06), core + deep learning **194 h**, full
  programme **407 h**.
- Specialisations: NLP/GenAI 270, vision 243, decision 256, responsible AI 268.
- Semester split: 158.8 + 247.9 = 406.7.

`audit/check_hours.py` reported zero failures after checking all module pages, the curriculum map,
study paths, FAQ, roadmap and module index. The 50% prerequisite share is explicitly a planning
assumption, not a measurement. These remain estimates of student effort, not guarantees.

---

## 11. Defects and recommended actions

Full register: `PHASE-25-DEFECT-AND-RISK-REGISTER.md`.

**Corrected during audit (small, objectively demonstrated):**

- D-01 M08 attention softmax values now follow from the logits.
- D-02 M11 prerequisite no longer says M08 is unpublished.
- D-03 README notebook runtime and internet claims now match measured behaviour.
- D-04 LAB-14-01 runtime now says ~2 min, not ~30 s.

**Open / owner decisions:**

- D-05 M14 exact latency ratios are not reproducible across runs; report a range or benchmark
  conditions, or re-measure on the publication machine.
- D-06 Local `.coverage`, `_*.log`, `__pycache__` and audit JSON/log artefacts should be removed or
  ignored before a public commit.
- D-07 Visual rendering remains unverified because no site/browser target exists.
- D-08 Flan-T5-small, UCI and model-output licensing remains owner review, not automated clearance.
- D-09 `CITATION.cff` uses a single MIT licence while the repository is mixed-licence; consider a
  note in the citation/README (owner decision).
- D-10 A conditional pytest skip in `test_agents.py` could hide removal of the email tool; make it a
  hard failure if the tool is expected.
- D-11 Minor heading-level jumps in two M06 lessons and resource library pages; accessibility polish,
  not a content defect.
- D-12 Five seeds/synthetic families limit generalisation; stated in LAB-14-01 and Phase 24A.

No critical defect was found. No high-severity defect remains open; D-05 is Medium and D-08 is an
owner-review risk, not a demonstrated licence violation.

---

## 12. Git integrity

- HEAD `fba4161aab98ebc3c3f8252d4a43e8e268b24b3c`; unchanged.
- Remote unchanged: `https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git`.
- No tags, no staged changes, no commits, no pushes.
- 167 porcelain lines: 108 modified, 59 untracked, 0 deleted.
- No tracked course file was removed. Earlier Phase 23/24 corrections remain present (M05 CPTs,
  licensing files, graph leakage controls, reports).
- Audit corrections are four documentation edits only; no course code was changed in Phase 25.

---

## 13. Academic verdict

**PASS WITH WARNINGS — READY WITH DOCUMENTED LIMITATIONS**

Evidence for acceptance: all modules and lessons are present and teach the advertised material;
independent mathematical verification found no core algorithm error; the full test suite, all
notebooks, links, hours and graph experiment pass; labs and capstone are substantive; the course
handles negative results honestly.

Warnings: exact M14 latency figures are machine-dependent; visual rendering is unverified; the
course relies on synthetic or bundled data in several places; five graph seeds and two synthetic
families are not evidence about real networks; licensing requires owner confirmation.

No condition prevents academic use. The warnings are documented, bounded and do not undermine the
course's core claims.
