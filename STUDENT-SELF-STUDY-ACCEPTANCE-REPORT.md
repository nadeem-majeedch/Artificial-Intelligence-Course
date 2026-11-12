# Student Self-Study Acceptance Report

**Date:** 12 November 2026
**Test role:** a student with no instructor available, no cohort, and no one to ask.
**Method:** each journey was walked through the repository as a learner would — following the
recommended starting point, opening the linked pages, running the notebooks, reading the lab
briefs and checking whether an assessment exists and can be attempted. Nothing was accepted on
the basis of a directory or a heading existing.

**Verification runs in this phase**

| Check | Result |
| --- | --- |
| Prerequisite notebooks executed (`nbclient`, CPU) | 6/6 pass, ≈28 s |
| Module notebooks (re-verified from the audit run) | 14/14 pass, ≈209 s |
| Internal links after the changes | 3,490 links, 0 broken, 0 broken anchors |
| Prerequisite lessons inspected | 21, every one has objectives, worked examples, a mini-lab, self-assessment, further reading and Python |
| Module pages inspected | 11 |
| Assessment availability checked | 14 quizzes against published lessons |

---

## 1. Summary of the five journeys

| Journey | Starting point found | Can it be completed today? | Main blocker |
| --- | --- | --- | --- |
| 1. Basic programming, new to AI | P01 | **Yes, to the end of M06** — with one dead module removed from the route | M02 stops after one lesson; M03/M05 absent |
| 2. Python, weak mathematics | P02 | **Yes** through M01 and M06 | none after routing fix |
| 3. Knows ML, wants deep learning | M06 revision → M07 | **Yes** | entry table previously sent this student to M03 |
| 4. Wants an LLM application | L07-07 → M11 | **Yes** | M08 was declared an essential prerequisite but has no lessons |
| 5. Wants an autonomous agent | M02 L02-01 → M11 → M12 code | **No** | M12 has 0 of 6 lessons and no lab |

**Overall: conditional acceptance.** Four of the five journeys can be completed by a student
working alone, once the routing problems below were fixed. The fifth cannot, and no navigation
change can make it completable.

---

## 2. Journey 1 — basic programming, first contact with AI

**Starting point tested:** the eight-question self-check in `docs/learning-path.md`, then P01.

| Step | What the student meets | Result |
| --- | --- | --- |
| P01 Python | 6 lessons, 2 notebooks, 1 lab | Notebooks run (2.8 s, 6.2 s); lab has scenario, tasks, rubric, extensions |
| P02 Mathematics | 5 lessons, 2 notebooks, 2 labs | Notebooks run (2.8 s, 3.3 s); chain rule covered in LP02-04 |
| P03 Probability | 6 lessons, 1 notebook, 1 lab | Notebook runs (4.8 s); base-rate lesson LP03-03 is the one M06 needs |
| P04 Data preparation | 4 lessons, 1 notebook, 1 lab | Notebook runs (4.2 s) |
| M01 Foundations | 5 lessons, 1 notebook, 2 labs, quiz, mini-project | notebook runs (3.4 s) |
| M02 Agents | **1 of 5 lessons**, 0 labs | stops after L02-01 |
| M04 Logic | 7 lessons, 2 notebooks, 0 labs | notebooks run (1.7 s each) |
| M06 Machine learning | 10 lessons, 4 notebooks, 4 labs | notebooks run (2.5–7.3 s) |

**Confusing transition found.** The route in `docs/learning-path.md` sent a beginner from M02 to
**M03**, and Path A scheduled "M03 complete: eight lessons, three labs, assignment" and "M05
complete". Neither module has any content. A beginner following the plan would arrive at an
empty page after roughly 60 hours of work, with no explanation.

**Fix applied.** The entry-point table now routes P01 → P02 → P03 → P04 → M01 → M04, Path A
schedules only published content, and both paths carry a status paragraph naming the modules that
do not exist. The M02 page now tells the student what to do when L02-01 ends (go to M04, then
M06) instead of leaving them at a link labelled "Next module: M03".

**Remaining gap.** M02 and the whole classical-AI stage (search, uncertainty) cannot be studied.

## 3. Journey 2 — knows Python, weak mathematics

**Starting point tested:** P02 (per the self-check, question 3 and 6).

- LP02-04 covers derivatives, partial derivatives and gradients with worked examples, and its
  notebook (`nb-p02-02-calculus-and-optimization`) runs in 3.3 s.
- P03 covers probability and Bayes, which M06 assumes; LP03-03 is the explicit recommendation.
- M06's prerequisite line names P02, P03, P04 and calls M05 "recommended" — and M05 does not
  exist. This is honest (recommended, not required) but a careful student will go looking for it.

**Missing explanation check.** No unexplained notation was found in the sampled lessons
(LP02-04, L06-03): every symbol is defined where introduced and each formula is followed by a
plain-language reading.

**Missing exercise check.** Prerequisite lessons contain one "Mini-Lab" each but not the
multi-part "Practical Exercises" section that module lessons have. A student who wants more
practice has 6 prerequisite notebooks and 5 prerequisite labs — enough to proceed, thinner than
the modules.

**Verdict: pass.** No blocker.

## 4. Journey 3 — knows machine learning, wants deep learning

**Starting point tested:** M06 revision → M07.

- The entry-point table previously listed "Already know ML, new to classical AI: M03 → M04 → M05
  → M06 revision → M07", which begins at an empty module. A separate row now exists —
  "Already know ML, want deep learning: M06 revision → M07" — pointing at L07-01 directly.
- M07 declares P02 and M06 as prerequisites, both available and complete.
- M07 provides 8 lessons, 3 labs, 3 notebooks. The notebooks run in 6.1 s, 10.1 s and 29.9 s on
  CPU, so the module is usable on a laptop without a GPU.
- LAB-07-01 gives the student a way to check their own work without a marker: the expected
  per-epoch error counts, the final loss (5.95e-05) and a gradient check that must fall below
  1e-6. This is the strongest self-verification in the course.

**Verdict: pass.** The only defect was the routing, now fixed.

## 5. Journey 4 — wants to build an LLM application

**Starting point tested:** L07-07 (attention) → M11 → LAB-11-02.

| Step | Finding |
| --- | --- |
| M11 prerequisite line | Declared "M08 (essential)". **M08 has no lessons** — reference code only |
| Actual requirement | L11-02 §3.7 teaches tokenisation, §3.8 embeddings; L11-05 teaches BM25 and dense retrieval. The declared prerequisite was stricter than the content |
| Notebooks | NB-11-01 runs in 36 s, NB-11-02 in 51 s, both after the import-path fix recorded in the audit |
| Labs | LAB-11-01, LAB-11-02 (two scenarios), LAB-11-03 all exist with rubrics |
| Assessment | quiz-m11 attemptable (7/7 lessons published); PA-11 and MP-11 exist |
| Output | LAB-11-02 builds a retrieval-augmented assistant end to end, offline, no API key |

**Fix applied.** The prerequisite line now states that M08's lessons are not published and that
the required NLP is inside M11; a "Start here if your goal is an LLM application" box points
straight to L11-02 and LAB-11-02.

**Remaining gap.** NLP as a subject (NER, stemming, TF-IDF as taught material, text pipelines) is
not available as lessons. A student can build the application but cannot study the NLP module.

## 6. Journey 5 — wants to build an autonomous agent

**Starting point tested:** M02 L02-01 → M11 → M12 reference code.

- **M12 publishes 0 of 6 lessons**, no lab and no notebook. The module page is honest about it,
  but honest is not the same as learnable.
- What exists: five reference code files (`agent_core.py`, `tools.py`, `guardrails.py`,
  `protocols.py`, `multi_agent.py`), a task set, a quiz covering unpublished lessons, and a
  self-assessment sheet.
- The route a student can actually follow: L02-01 for agent vocabulary, L11-04 and L11-05 for
  prompting and retrieval, then the code in reading order. That produces understanding of an
  agent loop, not a completed module.

**Fix applied.** The M12 page now opens with "What you can complete today", states plainly that
the module cannot be finished, gives the three-step route, and warns that the quiz is a preview.

**Remaining gap.** Six lessons, at least one lab and an evaluation exercise. This journey fails
acceptance and is reported as a failure rather than softened.

## 7. Assessment availability

| Module | Quiz attemptable? | Note |
| --- | --- | --- |
| M01, M04, M06, M07, M11, M13, M14 | yes | lessons published |
| M02 | no | 1 of 5 lessons |
| M03, M05, M09 | no | no content |
| M08, M10, M12 | no | reference code only |

Seven quizzes now carry an explicit availability notice (M02, M03, M05, M08, M09, M10, M12),
matching what the student will actually find. Before this phase, five of them silently claimed to
cover lessons that do not exist.

## 8. Can a student proceed without an instructor?

| Question a student asks | Answer available? |
| --- | --- |
| Where do I start? | Yes — eight-question self-check with a routing table |
| What do I do next? | Yes in published modules: every lesson ends with "What to Do Next"; every module page has a study plan |
| Is my answer right? | Yes in M07 (numeric check), M06 (baselines and metrics), M13 (reproducible numbers); quizzes have keys |
| What if I get stuck? | Yes — a seven-step protocol in `docs/learning-path.md` §8 and hints in labs |
| Can I skip this? | Yes — diagnostic in `prerequisites/diagnostic.md`, evidence-based skipping rules |
| Why is this module empty? | Yes — status lines on every module page, now also in the learning paths |

The remaining instructor-dependent moment is **feedback on written work**: rubrics describe what a
strong answer contains, but nobody marks it. That is inherent to self-study materials and is
disclosed rather than hidden.

## 9. Changes made in this phase

1. `docs/learning-path.md`: entry-point table rewritten around published content; Path A weekly
   plan rescheduled to P01–P04, M01, M02 (1 lesson), M04, M06 with a status paragraph; Path C
   status paragraph added; specialisation table corrected and labelled honestly.
2. `modules/M02.../README.md`: exit route to M04 and M06 added.
3. `modules/M04.../README.md`: status note corrected (quiz, assignment and self-assessment exist).
4. `modules/M11.../README.md`: prerequisite claim corrected; LLM-application start box added.
5. `modules/M12.../README.md`: "What you can complete today" section added.
6. Seven quizzes and their answer keys: availability notices added.
7. All links re-validated: 3,490 internal links, 0 broken.

## 10. Verdict

**Conditional acceptance — not a complete self-study course.**

- **Journeys 2, 3 and 4 pass.** A student can start, follow a sequence, run the code, attempt the
  assessments and know when to advance.
- **Journey 1 passes with warnings.** The route is sound, but M02 stops after one lesson and the
  classical-AI stage (M03, M05) is absent.
- **Journey 5 fails.** An autonomous-agent journey cannot be completed because M12 has no
  lessons.

The repository is honest about its gaps once a student reaches a module page, and after this phase
the learning paths no longer contradict the module pages. It is not complete, and no navigation
fix could make it so: six modules still lack teaching content.
