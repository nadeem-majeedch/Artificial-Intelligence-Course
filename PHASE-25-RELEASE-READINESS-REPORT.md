# Phase 25 — Release Readiness Report

**Assessment date:** 15 November 2026  
**HEAD:** `fba4161`  
**Working tree:** 167 porcelain lines (108 modified, 59 untracked, 0 staged, 0 deleted)  
**Operations performed:** none of commit, push, stage, tag, release, publish or deploy.

---

## 1. Verdicts

### Academic acceptance

**PASS WITH WARNINGS — READY WITH DOCUMENTED LIMITATIONS**

The course teaches its advertised subjects, its core algorithms and mathematics were independently
verified, and its practical materials execute. The warnings are bounded: exact M14 latency figures
vary by machine, certain modules use synthetic/bundled data, and five graph seeds/two synthetic
families are not evidence about real networks. None of these invalidates the course.

### Public-release readiness

**PASS WITH WARNINGS — READY SUBJECT TO OWNER APPROVALS**

There is no critical or open High-severity technical/content defect. The repository is ready for the
owner to publish after routine owner decisions: licence confirmations, disclosure of benchmark
variability, and a visual check on the chosen renderer. The working tree is intentionally dirty and
nothing was staged or committed; Git/publication operations remain the owner's.

---

## 2. Evidence supporting academic acceptance

| Evidence | Result |
| :--- | :--- |
| Modules / lessons / labs / notebooks | 14 / 89 / 38 / 35 course notebooks |
| Module pages with outcomes, prerequisites, map, plan, assessment | 14/14 |
| Lessons with objectives, exercises, self-check and references | 89/89 structurally; sampled deep reads across all modules |
| Full pytest suite | 196 passed, 0 failed, 0 skipped in final run |
| Python compilation | exit 0 |
| Independent algorithm/maths checks | 34/34 passed |
| Notebook regression | 35/35 executed, 0 failed cells, 4 library warnings |
| Links/anchors/structure | 4,154 links, 0 broken, 0 problems |
| Curriculum hours | 0 failures; 350.7 module + 56 prerequisite = 406.7 |
| LAB-14-01 reproduction | Exact five-seed values; leakage ablations pass |
| Representative lab runs | Fairness, security, serving/drift, graph reference/starter all exit 0 |
| Licensing mechanics | 0 failures; explicit "mechanical only" disclaimer |

The academic materials are not merely present: the sampled lessons contain derivations, worked
examples, code, failure analysis and exercises. The labs require measurements and reports, not
click-throughs. The capstone requires a baseline, per-class/subgroup table, uncertainty and
limitations.

---

## 3. Conditions and owner actions before publication

These are not code/content blockers, but they should be settled before a public release.

1. **Licence confirmation.** Confirm `google/flan-t5-small` model-card terms, UCI digits/Iris terms
   and the policy for model-generated notebook outputs and quotations. `check_licensing.py` is
   mechanical and does not grant legal clearance. See `THIRD-PARTY-ATTRIBUTIONS.md` §8.
2. **Benchmark disclosure.** D-05: the exact M14 latency ratios (2.62× int8, 1.45× pruning) did not
   reproduce in this audit (1.72×, 1.10×). Publish a measured range/environment or re-measure on the
   publication machine. The qualitative claims remain correct.
3. **Visual check.** Render the Markdown on the intended platform (GitHub or a chosen static-site
   renderer) and check tables, Mermaid diagrams and mobile layout. No browser target exists in the
   repository, so this audit cannot certify appearance.
4. **Working-tree hygiene.** Decide whether to remove or ignore `.coverage`, `_*.log`, `__pycache__`
   and `audit/*.json`/`*.log` before committing. Do not commit model weights or local outputs.
5. **Git operations.** Stage/commit/push/tag/release only after owner review. The audit made no Git
   changes.

---

## 4. Why not "CONDITIONAL PASS" or "FAIL"

- No critical defect found.
- No open High-severity defect: the one High (M08 arithmetic) was corrected and rechecked.
- Core claims are supported by independent checks and reproducible experiments.
- Tests, notebooks, links, hours and graph results all pass.
- The remaining issues are documentation/benchmarking consistency and owner-review permissions, not
  invalidated teaching or broken functionality.

A "CONDITIONAL PASS" would overstate D-05/D-08: they do not prevent academic use and are already
documented as limitations. A "FAIL" would contradict the measured evidence.

---

## 5. What would change the verdict

- A demonstrated licence violation or missing permission for redistributed material → release
  blocker.
- A core algorithm error that changes lesson conclusions → academic blocker.
- A failed notebook/test after a content change → conditional until fixed.
- A benchmark claim presented as universal when it is environment-specific → already a warning; if
  repeated as a headline marketing claim, it would become a High documentation defect.

---

## 6. Final release statement

The repository is academically sound and technically reproducible at the level claimed, with the
documented limitations above. It is suitable for the owner to prepare for public educational use
after the owner approvals listed in §3. This audit does not itself publish, deploy, commit, tag or
release anything.
