# Phase 24 — Academic Quality Remediation and Curriculum Consistency

**Date:** 13 November 2026
**Scope:** Fix the four academic defects carried over from Phase 23B (hours, M13 objectives,
LAB-05-02 deliverables, LAB-14-01 saturation), add targeted M13/M14 tests, and validate.
**Verdict:** **PASS WITH WARNINGS — REMEDIATION COMPLETE WITH DOCUMENTED LIMITATIONS**

Nothing was committed, staged, pushed, tagged, released, published or deployed. No notebook was
modified. No licence decision or licence file changed.

---

## 1. Executive summary

| Issue | Before | After |
| --- | --- | --- |
| Curriculum hours | 318 module / 374 total (design budgets) presented alongside 350.7/407 (measured), mixed across six documents | One method in `docs/CURRICULUM-MAP.md` §3.1; **350.7 / 406.7** used everywhere; automated check |
| M13-03 and M13-04 objectives | No objectives section | Six observable objectives each, aligned to existing exercises |
| LAB-05-02 deliverables | No deliverables section | Explicit four-file submission, evidence list, optional plot rule, reproducibility and format |
| LAB-14-01 experiment | Graph 1.000, baseline 1.000 (and GCN 1.000 in the reference sweep) | Leakage-free, noise-controlled, five-seed experiment: **0.342 vs 0.829** at default homophily; the graph loses at low homophily |
| M13/M14 tests | None; those modules had 0% coverage | **50 new tests**, 188 total passing, **34%** coverage of M13/M14 code |

## 2. Root cause of each issue

1. **Hours.** 318/374 were pre-writing design budgets; 350.7/406.7 were the measured published
   totals on module pages. Both were arithmetically correct, but the map, module index, README,
   FAQ, roadmap and learning path mixed them. `modules/README.md` even used measured hours in its
   index and design hours in each section. The M14 page's itemised table summed to 30 while its
   header said 32.9.
2. **M13 objectives.** L13-03 and L13-04 were written before the module adopted the
   "What you will be able to do" convention used by L13-01/L13-02; the content and exercises were
   present, but the entry point was missing.
3. **LAB-05-02.** The lab had objectives, tasks, testing instructions and a rubric, but no
   statement of what to submit. A student could complete every task and still not know the
   submission boundary.
4. **LAB-14-01.** The starter trained and evaluated on the same 60 nodes, gave one feature a
   class offset of 2.0, used one seed and no label noise, and built a near-perfectly homophilous
   two-community graph. Both models therefore memorised the labels and scored 1.000. The reference
   `graphs.py` also selected the best epoch on the test set and saturated at 1.000 for homophily
   ≥ 0.7. These were design defects, not model failures.
5. **Tests.** The 138 existing tests covered M01–M12 code but never imported M13 or M14.

## 3. Files changed

### Created

| File | Purpose |
| --- | --- |
| `PHASE-24-ACADEMIC-REMEDIATION-REPORT.md` | This report |
| `PHASE-24-CURRICULUM-HOURS-RECONCILIATION.md` | Method, arithmetic and per-module before/after |
| `PHASE-24-LAB-14-01-EXPERIMENT-REPORT.md` | Experiment root cause, redesign, measured results |
| `PHASE-24-TEST-COVERAGE-REPORT.md` | Tests, coverage, untested areas |
| `tests/test_responsible_ai.py` | 30 M13 tests |
| `tests/test_advanced_applications.py` | 20 M14 tests |
| `audit/check_hours.py` | Deterministic curriculum-hour consistency check |

### Modified — course material

| File | Change |
| --- | --- |
| `docs/CURRICULUM-MAP.md` | Measured totals, per-module hours, new §3.1 method, reconciled study paths |
| `modules/README.md` | All fourteen `Study time` lines aligned to module pages; core-path figure |
| `docs/course-roadmap.md` | Stage headings, module table, semester split, total |
| `README.md` | Path table, weekly schedule, FAQ duration |
| `docs/faq.md` | Core/deep-learning/full-programme durations |
| `docs/learning-path.md` | Path A/B/C tables and totals, specialisations, pacing; removed stale bullets and row-sum error |
| `modules/M05-…/labs/lab-05-02-…md` | New §10 Deliverables; extension section renumbered |
| `modules/M13-…/lessons/L13-03-…md` | Six learning objectives |
| `modules/M13-…/lessons/L13-04-…md` | Six learning objectives |
| `modules/M14-…/labs/lab-14-01-…md` | New B0 design section, measured tables, updated questions and starter output |
| `modules/M14-…/lessons/L14-04-…md` | Reproduction numbers, sweep, leakage note, mistakes row |
| `modules/M14-…/quizzes/quiz-14.md` | Question 12 uses the new numbers |
| `modules/M14-…/summary.md` | GNN/homophily rows |
| `modules/M14-…/README.md` | Total line reconciles to 32.9 with a rounding note |
| `modules/M14-…/capstone/README.md` | 14 of 32.9 hours |

### Modified — code

| File | Change |
| --- | --- |
| `modules/M14-…/code/graphs.py` | Random-mix edge sampling, degree 4, noise 2.6, 20% labelled split, 10% label noise, five seeds, final-epoch-only test evaluation, measured homophily printout |
| `modules/M14-…/labs/starters/lab-14-01_starter.py` | Rewritten: weak features, split, label noise, five seeds, baseline and homophily sweep |
| `modules/M14-…/code/neurosymbolic.py` | Replaced deprecated bitwise `~` on a bool with `np.logical_not` (same semantics, no warning) |
| `modules/M13-…/code/fairness.py` | Corrected the reweighing docstring: weights make label and group independent, not cell mass equal |

## 4. Before-and-after measurements

| Metric | Before | After |
| --- | --- | --- |
| Module hours | 318 (design) vs 350.7 (measured) | **350.7** canonical |
| Programme hours | 374 vs 406.7 | **406.7** canonical |
| Core path | 165 (and "190 published") | **169** |
| M13-03/04 objectives | absent | 6 each |
| LAB-05-02 deliverables | absent | 4 files + evidence + format |
| LAB-14-01 default | 1.000 / 1.000 | MLP **0.342 ± 0.049**, GCN-2 **0.829 ± 0.057** |
| LAB-14-01 sweep | GCN 1.000 at 0.7–0.9 | 0.293 at 0.189 → 0.906 at 1.000 |
| Tests | 138 | **188** |
| M13/M14 coverage | 0% (0/1,800) | **34%** (609/1,800) |

## 5. Experimental methodology and results (LAB-14-01)

- 200 nodes, 5 classes, 12 features, degree 4, feature noise 2.6.
- Edges: each slot same-class with probability `homophily`, otherwise uniform over all nodes. The
  old "all non-same edges are cross-class" rule made low homophily artificially informative.
- 20% of nodes labelled (stratified), 80% test; 10% of training labels flipped; test labels clean.
- Five seeds; mean ± standard deviation; fixed 200 epochs; test evaluated once, never used for
  epoch selection.
- Default condition (measured homophily 0.783): MLP 0.342 ± 0.049, GCN-2 0.829 ± 0.057,
  GCN-4 0.840 ± 0.062, GCN-8 0.188 ± 0.020.
- Sweep (measured homophily): 0.189 → gain −0.041; 0.380 → +0.144; 0.581 → +0.369;
  0.783 → +0.495; 1.000 → +0.573.
- Starter: baseline 0.590; graph 0.562 at 0.500 homophily rising to 0.952 at 1.000.

No number was hard-coded, and no seed was chosen to create a gap. The graph loses in a real regime
and the material says so.

## 6. Test results and coverage

- `python -m pytest tests/ -q` → **188 passed in 20.57 s** (138 old + 50 new).
- New files alone → 50 passed in 11.46 s.
- Coverage of the 15 M13/M14 code files: **34%** (609/1,800 statements), up from 0%.
- Highest-value coverage: guardrails 76%, graphs 58%, governance 57%, llm_security 55%.
- Untested areas are listed with reasons in the coverage report; no shape-only tests were added.

## 7. Validation commands and results

| Command | Result |
| --- | --- |
| `python audit/check_hours.py` | **0 failures** (components, totals, paths, index, stale figures) |
| `python audit/check_licensing.py` | **0 failures** |
| `python audit/check_course.py` | **4,154 links, 0 broken**; TOTAL PROBLEMS 0; CFF parsed |
| `python -m pytest tests/ -q` | **188 passed** |
| `python -m compileall -q modules prerequisites assessments tests audit` | exit **0** |
| Full notebook suite (35 course notebooks, templates excluded) | **0 failures, 442.8 s** |
| `nb-05-02` targeted execution | PASS, 2.6 s |
| `nb-14-01` targeted execution | PASS, 47.1 s |
| `python code/graphs.py` | reproduced tables in §5 |
| `python labs/starters/lab-14-01_starter.py` | reproduced starter table in §5 |

The notebook suite was run in memory; no `.ipynb` file was written or modified.

## 8. Git integrity

| Point | Porcelain lines | Modified | Untracked | Staged |
| --- | ---: | ---: | ---: | ---: |
| Before Phase 24 | 151 | 99 | 52 | 0 |
| After Phase 24 | 165 | 108 | 57 | 0 |

- HEAD unchanged: `fba4161 final QA complete`.
- Remote unchanged: `https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git`.
- `git diff --cached --name-only` → empty. No commit, push, tag, release, workflow or deployment.
- The after-count includes this report and the other three Phase 24 reports as untracked files.

## 9. Remaining limitations

1. **Hours are estimates, not measured student time.** Contact hours are not tracked. The core
   path's 50% prerequisite share is an explicit assumption, stated in every place it is used.
2. **LAB-14-01 is a toy.** 200 nodes, one synthetic generator, transductive evaluation, five seeds,
   accuracy only. It demonstrates a design principle; it does not license claims about real graphs.
3. **M13/M14 coverage is 34%, not complete.** Training loops and sampled explanation methods remain
   untested by design; the reasons are recorded rather than hidden.
4. **The notebook regression was a full run of 35 course notebooks**, not of the template
   notebooks, which are not course content.
5. **No teaching-effectiveness or accessibility study** was performed; this phase checked academic
   consistency, not learning outcomes.
6. **No legal or publication review.** Licensing remains as approved in Phase 23C.

## 10. Verdict

**PASS WITH WARNINGS — REMEDIATION COMPLETE WITH DOCUMENTED LIMITATIONS**

All four identified defects are fixed, their fixes are validated, and the new tests and hour check
protect them against regression. The warnings are the limitations above — chiefly the synthetic,
transductive nature of the graph experiment, planning-estimate hours, and partial unit coverage —
not unresolved failures.
