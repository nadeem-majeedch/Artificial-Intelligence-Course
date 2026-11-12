# Final Course Audit

**Repository:** Artificial Intelligence — A Complete Course for Self-Study
**Audit date:** 11 November 2026
**Auditor stance:** independent; previous implementation phases were not assumed correct, and
every claim below is backed by a command whose output is recorded in the companion reports.
**Constraints observed:** no commits, no pushes, no history changes, no GitHub Pages, no
Actions workflows, no large downloads.

---

## 1. Verdict

# FAIL

The course **cannot be certified complete**. Seven of the fourteen advertised modules are
fully taught; three modules (M03, M05, M09) do not exist at all, three (M08, M10, M12) contain
reference code but no teaching content, and M02 is one fifth written. In addition, the
repository has **no licence**.

The quality of what exists is high: all 14 notebooks execute on CPU, every internal link
resolves, lesson mathematics checks out, and the lab briefs are realistic and rubric-scored.
The failure is one of **coverage and legal status**, not of craft.

| Audit area | Verdict | Key evidence |
| --- | --- | --- |
| 1. Curriculum completeness | **FAIL** | 7/14 modules complete; M03/M05/M09 absent; M08/M10/M12 code-only; M02 1/5 |
| 2. Lesson quality | **PASS WITH WARNINGS** | 49 lessons, 16,977 lines, 49/49 exercises and references; 11 lessons without inline code |
| 3. Laboratory completeness | **PASS WITH WARNINGS** | 16 labs, all with scenario/deliverable/rubric; 8 lack an objectives heading, 3 lack extensions; M02/M04 have none |
| 4. Notebook validation | **PASS** | 14/14 executed after fixing a real import-path defect; ≈209 s total on CPU |
| 5. Assessment validation | **PASS WITH WARNINGS** | 14 quizzes, keys exhaustive (14/14), 12/12 numerical answers re-derived, 22/22 rubrics sum to 100; 3 papers unanswerable |
| 6. Documentation and navigation | **PASS WITH WARNINGS** | 2,834 internal links, 0 broken files, 0 broken anchors after fixing 11; external URLs not fully verifiable |
| 7. Licensing and attribution | **FAIL** | No LICENSE/COPYING; only a FAQ stating permission is required; no third-party notices |
| 8. Student experience | **FAIL** | A student following the roadmap hits three empty modules and six that teach nothing |
| 9. Reports | Complete | Seven reports delivered at repository root |

## 2. Evidence: what was actually run

| Test | Method | Result |
| --- | --- | --- |
| Notebook execution | `nbclient` + live kernel, CPU, 300 s timeout, cwd = notebook folder | 14/14 pass, ≈209 s |
| Link integrity | Strip fenced/inline code; resolve 2,834 relative links; validate 11-style anchors | 0 broken files, 0 broken anchors |
| Duplicate content | MD5 over 275 Markdown files | 0 duplicate groups |
| Images | Extract `![](...)` targets | 0 referenced, 0 missing |
| Quiz keys | Set-compare question numbers between 14 quizzes and 14 keys | exact match 14/14 |
| Numerical answers | 12 independent recomputations (conv params 448 and 2,410, output 30×30, TF-IDF 0.347, IoU 0.143, returns 2.62 and 3.3, perplexity 4.48, LoRA 8,192, 3⁵ = 243, DI 0.558, 5.2/18.8 = 27.7%) | 12/12 correct (two flagged as "missing" only because the key uses LaTeX `{,}` separators) |
| Assignment rubrics | Sum weighted percentages in 22 briefs | 22/22 = 100% |
| Lesson structure | 49 lessons scanned for nine required sections | see content report |
| Lab structure | 16 labs scanned against nine required elements | see lab report |
| Module inventory | Directory, lesson, lab and notebook counts per module | see completeness report |
| Dependency licences | Installed package metadata for 17 packages | all permissive; no copyleft |
| External URLs | 40-URL random sample, HEAD then GET | 28 reachable; 12 blocked by local TLS/endpoint, not 404 |

## 3. Defects fixed during this audit

1. **Notebook import failure (3 notebooks).** `nb-11-01`, `nb-11-02` and `nb-13-01` inserted
   `"."` into `sys.path`, which is the `notebooks/` directory, while their modules live in
   `code/`. They raised `ModuleNotFoundError` when opened the normal way. A bootstrap cell that
   locates the module's `code/` directory from either the notebook or module folder was added,
   and the three notebooks now execute. All 14 were re-run afterwards.
2. **Generated artefact path (1 notebook).** `nb-11-01` loaded `gen_samples.npz` relative to
   the current directory; the file exists only in `code/`. The call now resolves through
   `CODE_DIR`.
3. **Eleven broken TOC anchors (7 M04 lessons).** Em-dash headings produce double-hyphen
   slugs; the TOCs used single hyphens. Anchors regenerated from heading text; anchor check is
   now clean.
4. **Orphan assessments (3 quizzes + 3 keys).** `quiz-m03`, `quiz-m05`, `quiz-m09` and their
   keys test modules that have no content and claim to cover lessons that do not exist. Each now
   carries an availability notice explaining that the module is not published.

Nothing was hidden: the first-run notebook result (11/14) is recorded in the notebook report
alongside the fix.

## 4. Defects reported but not fixed

These require content authoring or a legal decision and are outside an audit's authority:

| ID | Defect | Why not fixed |
| --- | --- | --- |
| C1 | M03, M05, M09 do not exist (search, uncertainty, vision) | Would require writing three modules |
| C2 | M08, M10, M12 have no lessons | Would require writing three modules |
| C3 | M02 has 1 of 5 lessons | Would require writing four lessons |
| C4 | M04 has no lab or practical assessment | Would require authoring a lab |
| X1 | No repository licence | Legal choice belonging to the rights holder |
| L1–L4 | Lab template gaps (objectives/extensions/expected outputs; one lab without code) | Editing briefs would rewrite assessment design |
| Q1 | M13/M14 lessons have no inline Python | Deliberate design; implementation lives in `code/` |

## 5. Student-experience assessment (Audit 8)

A motivated beginner can complete **M01, M06, M07, M11, M13 and M14** end to end. In those
modules the sequence is: read a structured lesson, run a notebook that reproduces the lesson's
numbers, do a lab with a rubric, then a quiz with a separate key. Prerequisites are explicit and
satisfied. No GPU is required; no API key is required; no dataset download exceeds a few
megabytes; every internal link works.

The same student following `docs/learning-path.md` from the start will:

1. Meet M02 after one lesson and find no way to continue it.
2. Meet M03 and find nothing — but a quiz that covers seven lessons that do not exist.
3. Lose the classical-AI foundation (search, probability) that later modules assume.
4. Arrive at M08/M10/M12 and find code with no explanation of what to do with it.
5. Find no licence telling them whether they may reuse any of it.

Unexplained notation and inadequate exercises were **not** found in the completed modules;
those problems are concentrated entirely in the missing content.

## 6. Conditions for a PASS

The course would move to **PASS WITH WARNINGS** with:

1. A root `LICENSE` (or an explicit licence section) and a consistent FAQ answer.
2. A prominent availability statement on the homepage that names the seven modules that are
   not yet teachable, so no student is routed into an empty module.

It would move to **PASS** only when all fourteen modules contain lessons, at least one lab and
at least one notebook, and M02/M04 are completed. The three orphan quizzes should then either
match published lessons or be withdrawn.

## 7. Overall quality statement

The repository is a **high-quality partial course presented as a complete one**. The written
instruction is accurate, the mathematics is correct, the notebooks run, the labs are realistic
and the assessments are internally consistent. Its failure is scope: half the advertised
curriculum is missing, and the legal terms of use are unstated. Fix the licence, state the
availability honestly on the first screen, and finish M03/M05/M08/M09/M10/M12 — the material
already present suggests the rest can meet the same standard.
