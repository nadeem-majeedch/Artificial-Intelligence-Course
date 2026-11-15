# Phase 25 — Student Experience and Self-Study Audit

**Method:** six paper/browser-free student journeys through the actual README, learning paths,
module maps, lessons, labs, notebooks, assessments and capstone materials. This is a navigation and
materials audit, not a usability study with human participants. Every link cited was checked by
`audit/check_course.py` (4,154 links, 0 broken).

**Course scale:** 14 modules, 89 lessons, 38 lab briefs, 35 course notebooks, 14 quizzes, 14
self-assessments, 22 assignments, 8 module projects, 12 capstone briefs, 350.7 module hours and
406.7 programme hours.

---

## 1. Journey 1 — Complete beginner starting with Python and AI prerequisites

**Starting point:** main README → `docs/learning-path.md` §1 eight-question diagnostic, then
`prerequisites/README.md`.

**Route observed:** P01 Python (6 lessons, 2 notebooks, lab) → P02 Mathematics (5 lessons, 2
notebooks, 2 labs) → P03 Probability (6 lessons, notebook, lab) → P04 Data preparation (4 lessons,
notebook, lab) → M01.

**Evidence that it works:**

- The diagnostic maps each "no" answer to a specific prerequisite and a starting point.
- P01 begins with values, variables and control flow; no AI background is assumed.
- P02/P03/P04 each have a readiness self-check, lessons, notebook and lab.
- M01's prerequisites say "None (P01 recommended if you have never programmed)".
- The core path explicitly counts 14 h of P01 and a stated 50% share of P02–P04 (21 h).

**Caveat:** the "complete beginner" row of `docs/learning-path.md` recommends M01 → M04 after the
prerequisites, skipping M02 and M03. That is a legitimate alternative entry because M04 depends only
on P02, but a student who wants the full conceptual sequence should follow the module index/roadmap
(M01 → M02 → M03 → M04). The page does not hide this; it presents the shortcut as a route, not the
only route.

**Outcome:** a beginner can start without guessing. **PASS.**

---

## 2. Journey 2 — Search and problem solving

**Starting point:** M03 module page (`modules/M03-problem-solving-and-search-algorithms/README.md`).

**Route observed:** L03-01 problem formulation → L03-02 uninformed search → L03-03 informed search
(A*) → L03-04 local search → L03-05 adversarial search → L03-06 CSP → L03-07 choosing strategies →
NB-03-01 Search Workbench → LAB-03-01 route planning → LAB-03-02 game agent/timetable → PA-02 →
QUIZ-03.

**Evidence:**

- Each lesson states level, time, prerequisites and links to the next lesson.
- The module map lists every lesson, notebook, lab, assignment and quiz with times.
- A* is taught with admissibility, consistency, a worked grid and a Python implementation.
- The independent audit verified A* and UCS optimality on a weighted grid; the search notebook
  executes in 3.2 s.
- The lab briefs provide scenarios, tasks, deliverables and rubrics.

**Outcome:** the path is complete and assessable. **PASS.**

---

## 3. Journey 3 — Machine learning

**Starting point:** M06 (`modules/M06-machine-learning-fundamentals/README.md`), with P02, P03, P04
and M05 recommended.

**Route observed:** L06-01 what ML is → L06-02 splitting/leakage/CV → linear regression →
logistic regression → metrics/ROC → bias–variance/regularisation → kNN/naive Bayes → trees/forests/
boosting/SVM → unsupervised/PCA → reproducible pipelines. Practice: 4 notebooks, 4 labs, PA-06,
MP-06, quiz.

**Evidence:**

- The module page has a readiness check and names the exact prerequisite concepts.
- Leakage is taught before model comparison, not as a footnote.
- Metrics are verified against scikit-learn; the labs cover student performance, spam/loans,
  segmentation/attrition, and intrusion/fraud with leakage.
- The capstone and later modules reuse this evaluation discipline.

**Caveat:** the core path schedules M06 in 10.5 h, which is tight for ten lessons, four notebooks,
four labs and an assignment; the page states the hours are an estimate, and the full programme gives
more room. A self-study student may need longer.

**Outcome:** the student can learn, practise and self-mark ML. **PASS.**

---

## 4. Journey 4 — NLP and computer vision

**Starting point:** M07 (attention for NLP) → M08 and M09.

**NLP route:** L08-01 pipeline → L08-02 preprocessing → L08-03 BoW/ngrams/TF-IDF → L08-04
embeddings → L08-05 classification/sentiment/NER → L08-06 sequence models/attention/transformers.
Practice: 3 notebooks, 3 labs (preprocessing/features, news/document classification, Urdu/English
sentiment and NER). M11's prerequisite line now correctly treats M08 as recommended, not
unpublished.

**Vision route:** L09-01 introduction → image processing/features → CNN classification → object
detection → segmentation → advanced vision. Practice: 4 notebooks, 4 labs. IoU, NMS and matching
are implemented and were independently verified.

**Evidence:**

- Both modules have module maps with times, notebooks, labs and quizzes.
- Notebooks execute cleanly (M08: 2.8–6.4 s; M09: 13.0–24.1 s).
- The NLP lessons are concise (roughly 0.9–1.3k words), but the labs and notebooks carry the
  practical work; the vision lessons are slightly longer (1.2–1.3k words).
- M08's worked attention arithmetic was corrected during this audit; the concept and code were
  otherwise correct.

**Outcome:** materials are complete; a student can specialise in either area. **PASS with an
editorial caveat** on NLP prose density. **PASS.**

---

## 5. Journey 5 — Generative AI and agentic AI

**Starting point:** M07/L07-07 attention → M11 → M12.

**Generative AI route:** L11-01 landscape → L11-02 tokens/attention/next-token → L11-03
pretraining/instruction tuning/alignment → L11-04 prompting → L11-05 RAG → L11-06 fine-tuning/PEFT
→ L11-07 evaluation. Practice: 2 notebooks (token/attention and retrieval/prompting), 3 labs,
MP-11, quiz.

**Agent route:** L12-01 foundations → L12-02 tool calling/structured outputs → L12-03
planning/memory/workflow → L12-04 frameworks → L12-05 multi-agent → L12-06 MCP/security/evaluation.
Practice: notebook, 2 labs, MP-12, quiz.

**Evidence:**

- M11 documents four cached models, their licences and CPU expectations; it states "offline after
  the first model download".
- The two M11 notebooks executed in 82.8 s and 68.4 s. The second made an unauthenticated Hugging
  Face Hub request on first use; this is consistent with the module page, not with the old global
  README claim that no notebook needs a download. The global claim was corrected during the audit.
- M12's lessons are concise but concrete: schema validation, permission checks, retry bounds,
  audit logs and prompt-injection defences are taught as code and measured in labs.
- The agent notebook executes in 2.6 s; the security harnesses run in seconds.

**Outcome:** the path is coherent and honest about model dependence and security limits. **PASS
with a documented first-run download caveat.**

---

## 6. Journey 6 — Advanced AI capstone

**Starting point:** M14 → `capstone/README.md` → twelve briefs.

**Route observed:** L14-01 case studies/hybrid systems → L14-02 MLOps/serving → L14-03
monitoring/drift → L14-04 reading/reproducing research → L14-05 capstone studio → ASG-14 proposal
→ milestones M1–M4 → report → defence.

**Evidence:**

- The capstone studio names twelve briefs (four beginner, four intermediate, four advanced), a
  rubric, four milestones, a report template and report-writing guidance.
- The briefs state prerequisite modules, data rules, scope, honesty requirements and no-deployment
  boundary.
- The time budget is explicit: 14 h, with 2 h proposal, 4 h data/baseline, 5 h model/evaluation,
  3 h report/demo/defence.
- LAB-14-01 and LAB-14-02 supply reproducible experiments in graph learning, compression, latency
  and drift; LAB-14-01's five-seed results reproduced in this audit.
- The M14 notebook executes in 48.8 s.

**Caveat:** the exact serving-latency ratios in LAB-14-02/M14 are machine-dependent and did not
reproduce exactly (see D-05). Students can reproduce the direction but should record their own
timings. The lab already asks them to measure and report, which is the right pedagogy.

**Outcome:** a student can scope, execute, evaluate and defend a capstone using the provided
material. **PASS.**

---

## 7. Cross-journey navigation and support

| Requirement | Finding |
| :--- | :--- |
| Starting point | README → learning paths → diagnostic → prerequisites; clear |
| Prerequisite clarity | Each module states prerequisites and a readiness check or equivalent |
| Lesson sequence | Every module has a module map in reading order with times |
| Practical activities | Every module has notebooks/labs; 38 lab briefs; 7 starter scripts |
| Assessment availability | 14 quizzes, 14 self-assessments, 14 quiz keys, 22 assignments, projects |
| Supporting resources | Glossary, concept maps, books, documentation, papers, FAQ |
| Links | 4,154 checked, 0 broken |
| Learning outcomes | Eight CLOs mapped across modules; objectives per lesson |
| Expected outcome | Each module states what the student will be able to do |

### Issues found

1. The main README overclaimed notebook runtime and offline operation. **Corrected** (D-03).
2. M11 said M08 was unpublished. **Corrected** (D-02).
3. M08's attention example had incorrect softmax values. **Corrected** (D-01).
4. M14's exact latency constants are not stable across machines. **Open, Medium** (D-05).
5. No automated progress tracking exists; the course explicitly relies on self-checks and rubrics.
   This is a design choice, not a defect.
6. No human usability test was conducted; this audit verifies materials and navigation, not student
   comprehension.

---

## 8. Student-experience verdict

**PASS WITH WARNINGS — READY FOR SELF-STUDY WITH DOCUMENTED LIMITATIONS**

The course is navigable, sequenced and practically supported. A motivated student can start from
the diagnostic, follow a path, run the notebooks, complete labs and self-mark with the provided
keys/rubrics. The warnings concern exact performance figures, first-run model downloads and the
absence of a human usability study; none prevents self-study.
