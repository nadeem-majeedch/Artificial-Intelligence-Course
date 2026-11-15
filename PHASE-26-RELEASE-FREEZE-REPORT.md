# Phase 26 — Release Freeze Report

**Repository:** `C:\Users\Nadeem\Documents\Artificial-Intelligence-Course`  
**HEAD:** `fba4161aab98ebc3c3f8252d4a43e8e268b24b3c`  
**Date:** 15 November 2026  
**Owner:** Muhammad Nadeem Majeed

---

## 1. Final verdicts

### Licensing implementation

**PASS WITH WARNINGS — APPROVED ARCHITECTURE IMPLEMENTED, OWNERSHIP REVIEW PENDING**

### Documentation

**PASS — STUDENT-FACING DOCUMENTATION COMPLETE**

### Release readiness

**PASS WITH WARNINGS — READY SUBJECT TO SPECIFIC OWNER APPROVALS**

The repository is academically and technically ready for the owner's publication decision. No
critical or open technical/licensing defect was found in the distributed material. The remaining
items are the owner's chain-of-title review, acceptance of the model-output/quotation policy, a
visual render on the chosen platform, and the owner's own Git/publication operations.

---

## 2. What was changed

| File or area | Change |
| :--- | :--- |
| `README.md` | Professional student-facing rewrite; all 14 module links; verified inventory, workload, prerequisites, software and four-layer licensing |
| `LICENSE` | Added explicit software-only scope while preserving the canonical MIT terms and copyright line |
| `CONTENT-LICENSE.md` | New course title in attribution; explicit redistribution/adaptation/commercial statement |
| `CITATION.cff` | New title, mixed-licence scope, removed invalid author `title`; validated against CFF 1.2.0 |
| `THIRD-PARTY-ATTRIBUTIONS.md` | Upstream URLs, dates, UCI DOIs, per-model licences, output and quotation policies |
| `LICENSING-INVENTORY.md` | Refreshed counts, resolved upstream uncertainties, ownership checklist link |
| `OWNERSHIP-REVIEW-CHECKLIST.md` | New owner chain-of-title and sign-off checklist |
| `docs/index.md` | Four-layer licensing link; ownership checklist entry |
| `docs/faq.md` | Corrected runtime, download and README-section claims |
| `docs/about.md` | Corrected prerequisite sections, runtime/download claims and project count |
| `docs/learning-path.md` | Corrected software-requirements link |
| `docs/ARCHITECTURE.md` | Documented first-run download exception with offline fallback |
| `modules/README.md` | Removed stale publication-status language; corrected int8 summary |
| M11/M13/M14 pages and M14 lab | Corrected `load_digits` licence from public domain to CC BY 4.0 |
| `modules/M14/.../L14-02...md` | Replaced single-run latency constants with five-run ranges and full methodology |
| `modules/M14/.../summary.md` | Updated compression table to measured ranges |
| `modules/M14/.../lab-14-02...md` | Corrected int8 and pruning claims |
| `modules/M14/.../quiz-14.md`, `assessments/solutions/quiz-m14.md` | Corrected int8 range and homophily value |
| `modules/M14/.../code/efficiency.py` | Latency table and ratios now use the same measurement; median of three trials; environment printed |
| `audit/check_licensing.py` | Docstring updated to the four-layer and software-only CFF scope |
| `.gitignore` | Added coverage files, notebook execution outputs and local logs |
| Four Phase 26 reports + ownership checklist | Release handover |

No module, lesson, lab, notebook, assignment, quiz, project or capstone brief was added or removed.
No curriculum expansion was performed.

## 3. M14 benchmark correction

### 3.1 Harness defect corrected

The original harness timed each row once for the table, then timed the baselines again for the
ratios. On a noisy CPU the printed table and printed ratios could therefore disagree. The harness
now:

- measures each model once and reuses that value in the table and ratios;
- warms up 20 calls;
- reports the median of three trials of 300 single-example forward passes;
- prints Python, PyTorch, thread count and platform on every run.

This is a correctness fix to the measurement harness, not a change to the model or curriculum.

### 3.2 Recorded environment

- Windows 11 `Windows-11-10.0.26300-SP0`
- Intel64 Family 6 Model 142 Stepping 10
- Python 3.14.7
- PyTorch 2.14.1+cpu
- NumPy 2.5.3, scikit-learn 1.9.1
- 4 PyTorch threads, CPU only
- `load_digits`: 1,797 8×8 images, 70/30 stratified split, seed 0
- Student MLP: 64→64→10, 4,810 parameters, 40 epochs
- Teacher MLP: 64→256→256→10, 85,002 parameters, 50 epochs

### 3.3 Five release-validation runs

| Comparison | Measured result | Median | Earlier historical claim |
| :--- | :--- | ---: | :--- |
| int8 vs float student | **1.61–2.35× slower** | 1.68× | 2.62× from one unrecorded run |
| 50% pruning vs float student | **0.80–1.30×** (no reliable speed change) | 1.01× | 1.45× from one unrecorded run |
| int8 size | 5.2 KB = 27.7% of float | — | 27.7% |
| int8 accuracy | 0.898, unchanged | — | 0.898 |
| pruning sparsity | 50% | — | 50% |
| pruning accuracy | 0.865 (−0.033) | — | 0.865 |
| pruning size | 18.8 KB, unchanged | — | 18.8 KB |

The exact earlier constants are retained only as historical observations. They are no longer
presented as universal results. The direction is stable: this naive int8 path is slower on CPU
float kernels, and dense pruning does not reliably improve latency.

## 4. Validation results

| Check | Command / method | Result |
| :--- | :--- | :--- |
| Test suite | `python -m pytest -q` | **196 passed in 67.90 s**, no skips |
| Python compilation | `python -m compileall -q .` | **exit 0** |
| Links and anchors | `python audit/check_course.py` | **0 problems**; 4,140 links in the final check |
| Course structure | same checker | 89 lessons; 38 labs; CFF parsed |
| Curriculum hours | `python audit/check_hours.py` | **0 failures** |
| Licensing mechanics | `python audit/check_licensing.py` | **0 failures** |
| CFF YAML/schema | official CFF 1.2.0 schema + `jsonschema` | **PASS** |
| Notebook inventory | filesystem count | 35 course notebooks (29 module + 6 prerequisite) + 1 template = 36 files |
| M14 benchmark | five independent runs | Completed; deterministic accuracy/size; latency ranges recorded |
| Git integrity | `git rev-parse`, `git status`, `git diff --cached` | HEAD unchanged; remote unchanged; **0 staged** |

The final link-count rerun after adding all four reports was 4,140 links, 0 broken. No `deploy`,
publish, release, tag, commit, push or stage operation was performed.

## 5. Housekeeping

Removed as clearly disposable generated artefacts:

| Removed item | Quantity | Reason |
| :--- | ---: | :--- |
| `.coverage` | 1 | Local coverage database, regenerable |
| `_hf_dl.log`, `_pip_cv2.log`, `_pip_gym.log`, `_pip_sp.log` | 4 | Local installation/download logs |
| `__pycache__` directories | 21 | Python bytecode caches |
| `.pytest_cache` | 0 at cleanup time | None present |
| `.ipynb_checkpoints` | 0 | None present |

No audit JSON, reference inventory, report, committed data file or course resource was deleted. The
test run recreates Python caches; those remain ignored by `.gitignore`.

`.gitignore` now covers `.coverage`, `.coverage.*`, `coverage.xml`, `htmlcov/`, `.hypothesis/`,
`*.nbconvert.ipynb` and `_*.log` in addition to the existing cache rules. `*.log` already covered
the root logs; the explicit `_*.log` rule documents intent.

## 6. Git state

| Item | Value |
| :--- | :--- |
| HEAD | `fba4161aab98ebc3c3f8252d4a43e8e268b24b3c` |
| Origin | `https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git` |
| Staged files | **0** |
| Commits / pushes / tags / releases | None performed |
| Porcelain status | 178 entries at the validation checkpoint (modified and untracked; no deletions) |

The working tree is intentionally uncommitted. The owner will review and perform all Git
operations.

## 7. Visual and student-experience check

No website source, static-site generator, package manifest, HTML page or browser build target exists.
The course is Markdown with Mermaid diagrams. A visual preview therefore cannot be run without
creating a deployment configuration, which this phase was not authorised to do.

- Internal links and anchors: checked (0 broken).
- Heading structure, tables and code fences: structurally checked.
- Rendered Mermaid, typography, responsive/mobile layout: **not verified**.
- No screenshot or browser interaction was performed.

Visual acceptance remains an explicit owner check on the chosen platform.

## 8. Remaining owner decisions

1. **Ownership / chain of title.** Complete [OWNERSHIP-REVIEW-CHECKLIST.md](OWNERSHIP-REVIEW-CHECKLIST.md),
   including institutional ownership, contributor assignments and authority to license.
2. **Model-output and quotation policy.** Accept the recorded policy or obtain legal advice; no
   legal clearance is claimed.
3. **Licence re-check.** Confirm Flan-T5-small, UCI and other upstream terms at publication if they
   may have changed.
4. **Visual review.** Render the Markdown on GitHub or the chosen static-site platform and inspect
   tables, Mermaid diagrams and mobile layout.
5. **GitHub metadata.** Optionally apply the recommended description and topics manually.
6. **Publication.** Review the working tree and perform commit, tag, push and publication. Nothing
   has been staged or published by this phase.

## 9. Acceptance criteria

| Criterion | Status |
| :--- | :--- |
| MIT, CC BY 4.0 and CC0 clearly separated | Pass |
| Third-party material not accidentally relicensed | Pass |
| Ownership uncertainties explicitly recorded | Pass (checklist and reports) |
| README professional and student-facing | Pass |
| Course homepage and README consistent | Pass |
| All 14 modules represented correctly | Pass |
| Course workload consistent | Pass (checker 0 failures) |
| M14 benchmark claims properly qualified | Pass (ranges and environment recorded) |
| Temporary artefacts handled safely | Pass (disposable items removed; audit resources kept) |
| Automated checks pass | Pass |
| Git history and remote unchanged | Pass |
| Nothing staged, committed, pushed, released or published | Pass |

## 10. Handover statement

The repository is released to the owner in a documented, validated freeze state. The course content
and approved licensing architecture are intact. The remaining actions are owner approvals and
publication operations, not unfinished curriculum work.

**Release readiness: PASS WITH WARNINGS — READY SUBJECT TO SPECIFIC OWNER APPROVALS.**
