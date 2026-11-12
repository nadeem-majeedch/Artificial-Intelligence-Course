# Content Quality Report

**Scope:** 49 lessons across 8 modules, plus module pages and teaching-adjacent documents.
**Method:** structural measurement of all 49 lessons, full or partial readings of ten lessons
(five early, three mathematical, two advanced), and hand verification of numerical claims.

---

## 1. Corpus measurements

| Metric | Value |
| --- | --- |
| Lessons | 49 |
| Total lesson lines | 16,977 |
| Shortest / longest lesson | 236 / 457 lines |
| Median lesson | ca. 340 lines |
| Lessons with `## Exercises` | 49 / 49 |
| Lessons with key terms | 49 / 49 |
| Lessons with further reading | 49 / 49 |
| Lessons with self-assessment or self-check | 49 / 49 (38 + 13, two with both) |
| Lessons with "Common mistakes"/pitfalls | 42 / 49 |
| Lessons with a worked example | 40 / 49 |
| Lessons with a "Python implementation" section | 37 / 49 |
| Lessons containing inline `python` code | 38 / 49 |
| Lessons containing display mathematics (`$$`) | 39 / 49 |
| Lessons with collapsible hints (`<details>`) | 38 / 49 |
| Mermaid diagrams (whole repo) | 18, each followed by a text description |
| Images | 0 (none required, none referenced, none missing) |

No lesson is a bare definition list. The shortest lesson (236 lines) still contains
objectives, explanation, an example, exercises and references.

## 2. Structural consistency

Every lesson carries the same skeleton:

1. H1 title
2. Metadata table (level, study time, prerequisites, code)
3. One navigation line
4. `## On this page` table of contents (44 lessons above a length threshold)
5. Why the lesson exists / what you will be able to do
6. Numbered conceptual sections
7. Worked example(s)
8. Python implementation
9. Visual explanation (diagram plus text)
10. Real-world application
11. Common mistakes
12. Exercises
13. Self-assessment
14. Key terms
15. Further reading
16. Navigation line

Two consistency deviations were identified and are reported rather than papered over:

- **M13 and M14 (11 lessons) contain no inline Python block.** They reference module scripts
  (`code/rai_data.py`, `code/fairness.py`, `code/explain.py`, `code/serving.py`) and their
  numbers come from those scripts and notebooks. This is defensible — the code is real and
  tested — but it is a departure from the other 38 lessons, where the implementation is visible
  on the page. A student reading only the Markdown cannot see the code without opening a second
  file.
- **Self-assessment wording differs** between "Self-Assessment" (38) and "Self-check" (13).
  Both are functional; the inconsistency is cosmetic.

## 3. Conceptual accuracy — spot audit

| Claim checked | Where | Verdict |
| --- | --- | --- |
| PPV for 90% sensitivity, 90% specificity at 0.8% prevalence = 0.073 | `L06-05` | **Correct.** 0.0072 / 0.0992 = 0.0726 |
| XOR is not linearly separable; perceptron never converges on it | `L07-01`, lab-07-01 | **Correct**, and demonstrated numerically in the lab |
| Softmax + cross-entropy gradient is `(p − y)/n` | `L07-01` | **Correct** |
| Demographic parity gap / disparate impact ratio definitions | `L13-01` | **Correct**; DI = 0.096 / 0.172 = 0.558, as quoted |
| Reweighing cannot change a decision boundary fitted to a fixed feature set in the way the lesson claims | `L13-01` | **Correct and unusually honest** — the lesson treats the null result as the lesson |
| AUC interpretation as ranking probability | `L06-05` | **Correct**, with the standard caveat about prevalence stated explicitly |
| RMSE ≥ MAE with the gap indicating error concentration | `L06-05` | **Correct** |
| Calibration/ECE bucket arithmetic | `L13-01`, `L06-05` | **Correct** |

No mathematical error was found in the lessons sampled. The mathematics is written for
self-study: symbols are defined where introduced, and each formula is followed by an
interpretation sentence rather than left bare.

## 4. Explanatory depth — assessment

**Strengths observed across the sample:**

- **Motivation before formalism.** Lessons open with a concrete failure ("a model that is
  94.7% accurate can still allocate opportunity unfairly") before defining metrics.
- **Worked examples are numerical, not gestural.** `L06-05` computes a confusion matrix,
  PPV, ROC points and a cost-optimal threshold; `L13-01` reports specific group rates
  (selection 0.172 / 0.096, TPR 0.745 / 0.921).
- **Honest limitations.** Every lesson sampled names what its method cannot do — AUC not
  implying deployable precision; permutation importance not being causal; fairness metrics
  disagreeing by construction.
- **Exercises are graded in difficulty** and many require producing a number, not restating a
  definition.
- **References are specific** (paper titles and identifiers), not "see the literature".

**Weaknesses observed:**

- Some lessons in M06 are long enough (450+ lines) that a self-study reader may lose the
  thread; the on-page TOC mitigates but does not solve this.
- A few "Visual explanation" sections describe a diagram in prose in a way that assumes the
  reader can see the Mermaid rendering; where Mermaid fails to render (some Markdown viewers),
  the text description is the only artefact. The descriptions exist, so this is a warning, not
  a defect.
- M14's "Reading and reproducing AI research" lesson is strong on process but thin on a worked
  reproduction; it stops at a checklist.

## 5. Worked examples and Python implementations

- 40 lessons contain an explicit worked example; the remaining 9 (mostly M13/M14) embed the
  numbers in scenario walkthroughs instead.
- 38 lessons contain runnable inline Python. All fenced Python blocks in lessons were parsed
  by the project's own validation rule (V08, `docs/ARCHITECTURE.md`) and by this audit's
  notebook/lab execution; no syntax error was found in the lesson code that was executed via
  the notebooks.
- The strongest implementation content is in M07 (perceptron, MLP, gradient check) and M11
  (BPE from scratch, attention, RAG). These are not library wrappers: they implement the
  mechanism, then compare against the library.

## 6. Superficiality check

No lesson qualified as "only lists definitions or headings". The lowest-density lessons are in
M14 (case studies), which are necessarily survey-like, but each still contains a decision
framework, numbers and exercises. The measured minimum of 236 lines with exercises, key terms
and references is well above the threshold at which a lesson becomes a glossary entry.

## 7. Content defects and remediation

| ID | Defect | Severity | Status |
| --- | --- | --- | --- |
| Q1 | 11 lessons (M13, M14) have no inline Python, unlike the other 38 | Medium | Reported, not changed — the implementations exist and run |
| Q2 | Self-assessment heading naming inconsistent (38 vs 13) | Low | Reported |
| Q3 | M13/M14 lessons rely on scripts whose output the student must generate first | Low | Documented in lessons' setup tables |
| Q4 | 11 table-of-contents anchors in seven M04 lessons pointed at the wrong slug (em dash handling) | Medium | **Fixed** — anchors regenerated from headings; anchor check now 0 broken |
| Q5 | Lesson code cannot be executed directly from the Markdown without the module's `code/` directory on the path | Medium | Documented; notebooks fixed (see notebook report) |

## 8. Quality score

| Dimension | Weight | Score | Basis |
| --- | ---: | ---: | --- |
| Conceptual accuracy | 25% | 25/25 | no error found in sampled claims; arithmetic re-derived |
| Mathematical correctness | 20% | 20/20 | formulas and numbers verified |
| Explanatory depth | 20% | 17/20 | strong; some very long lessons, M14 survey-thin |
| Worked examples | 15% | 13/15 | 40 explicit, rest embedded |
| Python implementations | 15% | 11/15 | 38 inline; 11 defer to scripts |
| Exercises and self-assessment | 5% | 5/5 | 49/49 |

**Audit 2 verdict: PASS WITH WARNINGS.** The written content is accurate, well structured and
genuinely self-study oriented. The warnings concern the 11 lessons without inline code and the
long-lesson readability issue, neither of which is a correctness defect.
