# PHASE 23B — Independent Acceptance Audit

**Repository:** `C:\Users\Nadeem\Documents\Artificial-Intelligence-Course`
**Audit type:** independent verification of the Phase 23A remediation; evidence collected
from the working tree, not from earlier reports.
**Date of audit:** 13 November 2026.
**Commit under audit:** `fba4161` ("final QA complete"), unchanged.

---

## 1. Executive summary

The repository is coherent, executable and largely self-consistent. Every claim that could
be measured was measured again: 138 tests pass, all 36 notebooks execute with 0 failures,
4,115 internal links resolve, 66/66 code modules import, 95 bibliography entries now carry
verified or metadata-verified status, and the mathematical audit's 32 assertions all hold.

Three kinds of defect were found:

1. **Mechanical, user-visible, fixed here:** 88 literal "? Lesson" navigation labels across
   22 lesson files; a doc heading that said "four-line proof" for a five-line proof; four
   bibliography entries with no canonical identifier (now DOI/arXiv-verified); empty CFF
   name fields.
2. **Content-level, reported for the owner:** two M13 lessons lack an explicit objectives
   section; one M05 lab has no deliverables section; the curriculum map's study-hour table
   is stale (≈318/374 h against a measured 350.7/407 h); one M14 starter's baseline
   saturates and weakens its intended comparison.
3. **Structural coverage limits:** automated tests cover 25 of 66 module code files at
   46.7 % of their statements; M13 and M14 code is entirely untested; M11 notebooks need
   cached Hugging Face weights and have no offline fallback.

**Verdict:** **PASS WITH WARNINGS — READY FOR ACADEMIC REVIEW WITH DOCUMENTED LIMITATIONS.**

**Public-release assessment (separate):** **NOT READY.** There is still no licence, the
licensing proposal awaits owner approval, the FAQ contradicts an open licence, there is no
release tag or archival identifier, and the M11 offline gap would surface immediately for
external readers. None of these blocks academic review; all of them block release.

## 2. Scope and methodology

| Area | Method | Deliverable |
| --- | --- | --- |
| Tests | Clean-process pytest runs, repeat run, reverse-order run, per-file runs, coverage run, source inspection for self-referential assertions | `PHASE-23B-TEST-QUALITY-REPORT.md` |
| References | Parsed both bibliography layouts; arXiv API for arXiv links; live HTTP fetch for other URLs; Crossref bibliographic/DOI lookup for paywalled entries | `PHASE-23B-REFERENCE-INVENTORY.md` |
| Notebooks | Fresh kernel per notebook, 300 s per-cell timeout, no write-back, output scan | `PHASE-23B-NOTEBOOK-REGRESSION-REPORT.md` |
| Lessons/labs/assessments | Structural checks over all 89 lessons, 38 labs and 14 quizzes; deep reading of a stratified sample; numerical spot checks | `PHASE-23B-ACADEMIC-QUALITY-REPORT.md` |
| Repository integrity | Link/anchor check, compileall, import smoke test, hours reconciliation, navigation reciprocity, CFF validation, licence inspection, Git status before/after | this report |

The brief's counts were checked rather than assumed: the repository has **38 labs, not 27**,
**36 notebooks (35 course + 1 template), not 35**, and **95 bibliography entries**, which
matches. Those differences are recorded where they matter.

No Git history, remote, workflow, licence or deployment configuration was touched.

## 3. Verified results

### 3.1 Tests

- **138 passed, 0 failed, 0 skipped** in **17.99 s** (runs during the audit: 15.83 s,
  23.47 s reverse order, 26.79 s repeat, 17.99 s final).
- Counts by file: search 25, vision 14, RL 14, ML 21, logic 12, probability 12, NLP 12,
  agents 12, NN 10, genai 6.
- Tests import production modules through `conftest.py`; independent references are used
  for Dijkstra, truth tables, joint summation, finite-difference gradients, scipy
  convolution, closed-form policy evaluation and Gymnasium exact values.
- Coverage: **46.7 %** of 6,139 statements in the **25 of 66** module files the suite
  imports. The 41 unmeasured files are listed in the test report; M13 and M14 have none.

### 3.2 Notebooks

- **36 executed, 0 failed, 473.3 s.** Of the 35 course notebooks: 33 PASS, 2 PASS WITH
  WARNINGS. The template also passes.
- The two warnings are `tqdm`/`transformers` progress output and an unauthenticated-HF-Hub
  notice; no traceback, no timeout.
- No notebook writes back to the repository during this audit, and no notebook produced
  `NaN`/`inf` outside the deliberate missing-value demonstration in `nb-06-01`.
- M11 requires cached `distilgpt2`/`flan-t5-small` weights (runtime download on a clean
  machine); no offline fallback exists.

### 3.3 References

- **95 entries: 67 Verified, 9 Verified with a documented qualification, 19 Paywalled
  but bibliographic metadata verified, 0 Unverified, 0 invalid.**
- 61 entries carry an arXiv link, resolving to 38 unique identifiers.
- 62 entries appear in more than one bibliography file; duplicates are flagged per record.
- Phase 23A's "65 verified" was reconciled: the earlier checker parsed only heading
  entries and only arXiv links, and classified four works as unverified because their
  entries carried no identifier. Identifiers were confirmed through Crossref/arXiv before
  being added.
- No paywalled reference was removed or replaced with an open-access substitute.

### 3.4 Repository checks

| Check | Result |
| --- | --- |
| Markdown links and anchors | **4,115 checked, 0 broken** |
| Python compilation | `compileall modules prerequisites assessments tests audit` exit 0 |
| Import smoke test | **66/66** module code files import |
| Mathematical audit | `audit/math_verify.py` **32/32 passed** |
| Lesson exercises | 89 lessons, 4–9 items, none below 4 |
| Lab starter material | 18 labs covered (7 scripts, 11 linked notebooks), 0 broken links |
| Extension challenges | 4/4 present |
| Quiz answer keys | 14/14 quizzes have a solution file and matching question markers (10–12 each) |
| Numeric answers spot-checked | QUIZ-M05 Q5.8, QUIZ-M10 Q10.8/9/10 — all correct |
| Assignment/project rubrics | 5 assignments, 8 projects, all with evaluation criteria; capstone rubric 10 criteria |
| Module study-hour sum | 14 module READMEs total **350.7 h** (matches Phase 23A's measurement) |
| Citation metadata | CFF parses; required keys present; no DOI/version/date/ORCID |
| Licence files | none applied (`LICENSE-AND-ATTRIBUTION-PROPOSAL.md` only) |
| Phase 23A fixes still present | Otsu implementation, ARCHITECTURE paths, project rubrics, assignment links — all verified |

## 4. Defects found and corrections made

### 4.1 Corrected in this audit

| # | Defect | Location / extent | Change | Risk |
| --- | --- | --- | --- | --- |
| 1 | Navigation rendered as "? Lesson" in both header and footer | 22 lesson files, 88 occurrences (M06–M11) | Replaced with the target lesson ID (`Previous: L06-01`, `Next: L06-03 →`), matching the existing in-page style | None; link text only |
| 2 | Heading "four-line proof" for a five-line proof | `modules/M04-…/lessons/L04-03-…md` (heading + TOC anchor) | Renamed to "five-line proof" and updated anchor | None |
| 3 | Four works had no canonical identifier | `resources/research-papers.md`, `resources/library/papers-and-surveys.md` | Added Crossref-verified DOI for SVM and LSTM; arXiv IDs for FCN and AutoGen; library SVM entry gained its DOI line | Metadata only, each verified before insertion |
| 4 | Empty `name-particle`/`name-suffix` values | `CITATION.cff` | Removed the empty fields | Prevents strict-schema rejection |

No production Python, notebook, quiz, rubric or lesson prose was otherwise changed.

### 4.2 Reported, not changed (owner decision required)

| # | Finding | Why not fixed here |
| --- | --- | --- |
| A | `L13-03` and `L13-04` have no explicit "What you will be able to do" section (the other four M13 lessons do) | Writing objectives is authoring content |
| B | `LAB-05-02` has no deliverables/submission section | Requires an authorial choice of report format |
| C | `docs/CURRICULUM-MAP.md` table says ≈318 h modules / ≈374 h total; measured is 350.7 / ≈407 | Changing published course totals is an academic claim |
| D | `LAB-14-01` starter prints 1.000 for both graph model and feature-only baseline, so the "does the graph help?" question is uninteresting | Changing the synthetic signal changes the exercise's expected output |
| E | Eight lessons carry 7–9 exercises, above the 2–4 brief | Trimming real exercises to meet a count would be the padding error in reverse |
| F | M11 notebooks require cached HF weights; no offline fallback | Adding a fallback or explicit download cell is a design choice |

## 5. Remaining limitations and risks

1. **Coverage is partial.** 41 of 66 code files are untested; M13/M14 code has no tests at
   all; DQN training is 19 % covered; generative training loops are essentially untested.
2. **Academic review is not peer review.** This audit checks consistency, executability,
   numerical spot checks and metadata; it does not validate every sentence in 89 lessons.
   Eight lessons were read closely, not all 89.
3. **Notebook environment dependence.** M11 needs network/cache and ~hundreds of MB of
   weights; a disconnected reviewer will see failures the pass table does not show.
4. **Undated, unversioned citation.** `CITATION.cff` is valid but cannot be a release
   citation until the owner supplies a version/date/DOI decision.
5. **No CI.** Checks are scripts run manually, by constraint; a future contributor can
   regress links or tests without noticing.
6. **Generated artifacts.** The audit left JSON/log artefacts in `audit/`; they are
   evidence, not course content, and are untracked like the rest of the Phase 23 reports.

## 6. Licensing and attribution status

- **No licence is applied.** `LICENSE`, `COPYING` and `LICENCE` do not exist.
- `LICENSE-AND-ATTRIBUTION-PROPOSAL.md` distinguishes original code (proposed MIT),
  educational content (CC BY 4.0), synthetic datasets (CC0 1.0), third-party materials and
  external models, and excludes third-party material from any blanket grant.
- The FAQ still says permission is required; that contradiction must be resolved in the
  same change as any licence file.
- **Licence application is not ready for approval until the owner answers:** (i) accept the
  MIT/CC BY/CC0 split or choose a non-commercial variant; (ii) confirm the copyright
  holder line and year; (iii) approve the FAQ rewrite.

## 7. Git integrity

| Item | Before audit | After audit |
| --- | --- | --- |
| `git status --porcelain` lines | 111 | 140 |
| Modified files | (pre-existing Phase 23A state) | 95 |
| Untracked files | 41 | 45 |
| Staged files | **0** | **0** |
| Commit | `fba4161` | `fba4161` (unchanged) |
| Remote | `origin` GitHub URL | unchanged |
| Push/publish/deploy | none | none |
| Workflows / pages | none created | none created |

Nothing was staged, committed, amended, reset, rebased or pushed. The increased status
count is the five new reports plus the four corrected bibliography/lesson files and the
Phase 23A artifacts that were already untracked.

## 8. Prioritised recommendations

1. **Author the two missing M13 objectives sections and the LAB-05-02 deliverables
   section.** Small, high-visibility fixes before external review.
2. **Decide the study-hour table.** Either update `docs/CURRICULUM-MAP.md` to 351/407 or
   relabel it explicitly as design hours. Do not leave two totals in one document.
3. **Add M13 tests** (fairness metrics, mitigations, prompt-injection harness) and then
   M14; this is the largest academic-risk gap in the test suite.
4. **Add an M11 offline path** (download-once cell or synthetic fallback) and state the
   cache requirement in the notebook header.
5. **Approve or amend the licensing architecture**, then apply it with the FAQ rewrite in
   one reviewed change.
6. **Fix the LAB-14-01 signal** so the graph-versus-baseline comparison is informative.
7. **Tag a release and complete `CITATION.cff`** only after the licence decision; do not
   invent a DOI or date to fill the fields.

## 9. Decisions required from the repository owner

1. Approve, amend or reject the MIT / CC BY 4.0 / CC0 1.0 licensing split, and confirm the
   copyright holder line and year.
2. Approve the FAQ change that removes the "permission required" statement if an open
   licence is adopted.
3. Decide whether the curriculum map should show measured hours (351/407) or design hours
   (318/374), and whether to relabel it.
4. Author (or delegate) the missing objectives in L13-03/L13-04 and deliverables in
   LAB-05-02.
5. Decide whether to invest in M13/M14 test coverage before release.
6. Decide the release/version/DOI approach so `CITATION.cff` can be completed without
   unverified metadata.
