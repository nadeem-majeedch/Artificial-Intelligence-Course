# Final Phase 23 Report — Independent Academic and Technical Quality Audit

**Date:** 12 November 2026
**Repository:** `C:\Users\Nadeem\Documents\Artificial-Intelligence-Course`
**Scope:** 14 modules, 89 lessons, 38 laboratories, 8 mini-projects, 35 notebooks, 14 quizzes with keys,
14 programming assignments, 8 analytical assignments.
**Restrictions observed:** nothing was committed, staged or pushed; Git history was not modified; no
workflow, Pages configuration or deployment was created; existing content was preserved except where a
defect required a correction, and every correction is listed below.

## Verdict

**PASS WITH WARNINGS.**

The course is a coherent, mathematically sound, executable final-year undergraduate AI curriculum. Its
claims survive independent recomputation: 32 of 32 mathematical checks passed, all 35 notebooks executed
from clean kernels, all 72 Python files compile, and 4,090 internal links resolve. It is not a polished
commercial product: 60 lessons have no exercises, a third of the code has no tests, two lab templates
coexist, deep-RL convergence is not demonstrated, and external links were not fetched. Those are the
warnings.

## 1. Evidence supporting the verdict

| Evidence | Result | Report |
| :--- | :--- | :--- |
| Notebooks executed in clean kernels | 35 / 35 (31 PASS, 4 PASS WITH WARNINGS, 0 FAIL, 0 BLOCKED), 477.9 s | `NOTEBOOK-REGRESSION-REPORT.md` |
| Independent mathematical checks | 32 / 32 pass | `MATHEMATICAL-VERIFICATION-REPORT.md` |
| Python compile | 72 files, 0 failures | `PYTHON-IMPLEMENTATION-AUDIT.md` |
| Module self-tests | 5 modules, all True | `PYTHON-IMPLEMENTATION-AUDIT.md` |
| Internal links and anchors | 4,090 checked, 0 broken (372 Markdown files) | this report |
| Lessons with required sections | 89 / 89 have objectives, prerequisites, conceptual explanation, worked examples, code or self-check | `ACADEMIC-QUALITY-AUDIT-REPORT.md` |
| Labs with a rubric | 38 / 38 | `LAB-AND-ASSESSMENT-AUDIT.md` |
| Quizzes with answer keys | 14 / 14; sampled numeric answers recomputed and correct | `LAB-AND-ASSESSMENT-AUDIT.md` |
| Study-hour consistency | 14 / 14 module pages agree with both central tables; category sums equal totals | this report |
| Licence position | no third-party data, weights or images redistributed; no secrets committed | `LICENSING-AND-REFERENCES-AUDIT.md` |

## 2. Verified defects (found and fixed)

Each was reproduced before the fix and re-checked after it.

1. **`vision_core.otsu_threshold` returned 0.0 for any image in [0, 1]** and ignored its `bins`
   argument. The cast to `uint8` truncated the whole image to zero, so a student normalising an image
   before thresholding got an all-foreground mask with no error. Fixed to quantise the observed range into
   `bins` levels and return the threshold in the input's units; regression assertion added; the notebook
   using it re-executed (10.1 s, 0 errors; threshold now 101.6 instead of 0.0).
2. **Five modules under-counted their project hours.** M01, M06, M07, M11 and M12 declare project effort as
   `| Effort | … |`, which the earlier hour calculation did not parse, so projects were counted as 0.0 h
   while the same pages claimed 2 h (and M12, 8–10 h). Fixed by reading the `Effort` rows: M01 10.8 → 12.8,
   M06 27.9 → 31.4, M07 22.9 → 24.9, M11 21.3 → 23.3, M12 18.8 → 27.8. Both central tables and the learning
   path were updated, so the published total is now 350.7 hours.
3. **Stale prose totals contradicted page totals** in M13 (19 vs 22.4) and M14 (30 vs 32.9). Replaced with
   the four-category statement that the rest of the course uses.
4. **Nine module pages did not link their programming assignment**, so the assessed work was unreachable
   from the module page. M02 received an inline navigation link; M01, M05, M06, M07, M08, M11, M12 and M13
   received an `## Assignment` section pointing at their PA file. M14 has no PA by design (the capstone is
   the assessment).
5. **Three mini-projects had no marking scheme** (MP-06, MP-07, MP-11). Each now ends with a five-criterion
   weighting table consistent with the rubrics used elsewhere.

Nothing else was modified for audit reasons. In particular, no lesson was rewritten, no lab was
restructured, and no result was edited to look better.

## 3. Potential weaknesses (documented, not fixed)

These are genuine limitations. They were left alone because fixing them means writing new educational
content or running long experiments, not repairing a defect, and the brief forbids cosmetic or scope-
expanding edits.

1. **60 of 89 lessons have no `Exercises` section.** They have self-check questions and common-mistake
   sections, but no task the student must produce. This is the biggest pedagogical gap; labs and quizzes
   partly compensate.
2. **11 lessons contain no Python** (six in M13, five in M14). M13's executable material lives in its code
   files and notebook; M14 is capstone guidance. A student reading only the lesson cannot run an example.
3. **Test coverage is uneven.** Only 5 of 72 Python files expose `run_tests()`. M06, M07, M08, M11, M12 and
   M13 have none, and `rl_envs`/`dp`/`tabular`/`dqn` are tested indirectly through `experiments.py`. The
   audit's own harness covers the highest-risk algorithms, but it lives outside the course code.
4. **18 labs have no inline starter code** and only the older lab template includes hints. A student with no
   instructor has reference files to read, not a scaffold to edit.
5. **Four labs have no extension task** (LAB-13-01, LAB-13-02, LAB-14-01, LAB-14-02).
6. **Two lab templates and two lesson openers coexist.** Both work; the inconsistency costs a reader moving
   between modules.
7. **No `LICENSE`, `CITATION.cff` or per-page copyright.** Deliberately not added: choosing a licence is the
   owner's decision, not an auditor's.
8. **M14 has no separate assessment file.** Its assessment is the capstone, described in the module page and
   the starter notebook.
9. **The M02/M03 assignment numbering is out of module order** (PA-03 for agents, PA-02 for search). It
   follows the syllabus numbering and is documented, but it confuses browsing.

## 4. Unverified claims

Stated plainly, because an audit that hides its blind spots is worthless:

- **Deep-RL convergence.** No DQN or PPO run reached a solved benchmark in this audit. The labs state
  expected ranges and require students to report their own numbers; the course does not claim a measured
  solve, and neither does this report.
- **External links.** 60 arXiv references and the documentation links were not fetched. Their current
  availability is unverified; no lesson depends on a link resolving.
- **Every quiz answer.** Two numeric answers and one tracing answer were recomputed by hand and matched. The
  remaining keys were checked for structure and part coverage, not recomputed item by item.
- **Every lab's expected numbers.** M09 and M10 numbers were reproduced on this machine; older labs state
  ranges and qualitative criteria, which cannot be "verified" in the same sense.
- **Large-model claims** in M11 (scaling behaviour, frontier-model quality) are citations, not experiments.
- **Statistical significance** of model comparisons rests on the course's own resampling code; no
  independent significance testing was done.
- **Windows-only execution.** All runs were on Windows 11, Python 3.14, CPU. Behaviour on Linux/macOS or
  with CUDA is untested.

## 5. Audit trail

Commands executed (all local, none networked except optional Hugging Face cache reads):

1. `python _nb_audit.py` — 35 notebooks, clean kernels, 300 s cell timeout, results in
   `audit/notebook_results.json`, log in `audit/notebook_run.log`.
2. `python _math_verify.py` — 32 independent checks, all pass after the harness's own API mistakes were
   corrected (recorded in the mathematical report so the false positives are not mistaken for defects).
3. Module imports and `run_tests()` for all 72 files; `py_compile` for all 72.
4. `python _content_audit.py` — structural counts, similarity analysis, licence and domain inventory.
5. Link and anchor checker over 372 Markdown files; final run 4,090 links, 0 broken.
6. Hour reconciliation script over all 14 module pages and both central tables.

Files changed after the fixes: `modules/M09-computer-vision/code/vision_core.py` (Otsu),
`modules/M09-computer-vision/notebooks/nb-09-01-image-processing.ipynb` (re-executed),
14 module `README.md` files (hours, assignment links), `modules/M06|M07|M11/projects/*.md` (rubrics),
`README.md`, `modules/README.md`, `docs/learning-path.md` (totals), and the seven audit reports.
Notebooks whose outputs were refreshed by the regression run are shown as modified in `git status`; their
content changed only in stored outputs.

`git status --short` shows modified files only; `git diff --cached --stat` is empty, confirming nothing was
staged.

## 6. Recommendations, in priority order

1. **Add exercises to the 60 lessons that lack them** — three graded tasks each, with answers in a solutions
   appendix. This is the highest-value improvement per hour of work.
2. **Give M06, M07, M08, M11, M12 and M13 a `run_tests()`** modelled on `vision_core`'s, so the course's own
   claims are executable rather than audited once.
3. **Add starter code to the 18 labs that lack it** — even a five-line skeleton with a TODO narrows the gap
   between reading and doing.
4. **Run the DQN and PPO labs to convergence once**, record the runtime and the seed spread, and quote those
   numbers instead of ranges.
5. **Unify the lab template** the next time a lab is edited, rather than in a mass rewrite.
6. **Add a `LICENSE` and `CITATION.cff`** once the owner has decided the terms.

## 7. What this audit does not establish

It does not establish that the course is equivalent to a accredited university module, that a student who
completes it is employable, or that every explanation is optimal for every learner. It establishes that the
material exists, is internally consistent, is mathematically correct where checkable, executes on a clean
machine, and does not misrepresent its own evidence.
