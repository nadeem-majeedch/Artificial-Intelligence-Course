# Documentation and Navigation Report

**Scope:** all 275 Markdown files in the repository, all internal links and anchors, all
external URLs, navigation lines, module numbering, duplicate files, placeholders and
instructor information.
**Method:** script that strips fenced and inline code, extracts `[text](target)`, resolves each
relative target from the file's directory, and validates `#fragment` against heading slugs plus
explicit `<a id="...">` anchors.

---

## 1. Link validation

| Metric | Before audit | After remediation |
| --- | ---: | ---: |
| Markdown files | 275 | 275 |
| Internal links checked | 2,834 | 2,834 |
| Broken file targets | 0 | 0 |
| Broken anchors | **11** | **0** |

### 1.1 The 11 broken anchors (fixed)

All eleven were table-of-contents entries in seven M04 lessons. The headings contain an em dash
(`## 5. Worked Example — the same question, three representations`), and GitHub's slug rule
removes the dash while leaving both surrounding spaces, producing a double hyphen. The TOCs
used a single hyphen, so the links jumped nowhere.

Fixed by regenerating each TOC anchor from its heading text. Affected files:

- `L04-01-knowledge-representation-fundamentals.md` (2)
- `L04-02-propositional-logic.md` (1)
- `L04-03-inference-rules-and-equivalence.md` (3)
- `L04-04-first-order-logic-and-quantifiers.md` (1)
- `L04-05-unification-and-chaining.md` (1)
- `L04-06-resolution-and-automated-reasoning.md` (1)
- `L04-07-rule-based-and-expert-systems.md` (2)

### 1.2 External URLs

- **109 unique external URL targets** appear in Markdown links (README, lessons, labs,
  resources, glossary).
- A random sample of 40 was probed with HEAD (GET fallback). **28/40 returned success**.
- The 12 failures were **not 404s**: they were `SSL: CERTIFICATE_VERIFY_FAILED` for arxiv.org
  and `WinError 10054` for stanford.edu, from this machine's Python TLS chain. `python.org` and
  `scikit-learn.org` returned 200 from the same interpreter, so the network was up; the failure
  is local certificate/endpoint behaviour, not link rot.
- **Limitation:** external reachability could not be fully verified in this environment. This
  is reported as unverified, not as passing. An earlier audit phase that used a browser-style
  check reported 117/118 reachable; that figure is not relied upon here.

## 2. Navigation consistency

| Check | Result |
| --- | --- |
| Lessons with exactly one header navigation line | 49 / 49 |
| Lessons with exactly one footer `**Navigation:**` line | 49 / 49 |
| Boundary handling (first lesson → module start; last → module end) | correct in all 8 complete modules |
| Lessons with `## On this page` TOC | 44 (all lessons above the length threshold) |
| Duplicate navigation lines | 0 |
| Module pages with a study plan, assessment table and navigation | 11 / 11 |
| `modules/README.md` "Start here" entries | 11 (one per published module) |

## 3. Structure and numbering

- Module directories are numbered `M01 … M14` with gaps at M03, M05 and M09, matching the
  absent modules. Numbering is internally consistent: no duplicate module numbers, no lesson ID
  outside its module's range, no lab ID mismatch.
- Lesson IDs `L01-01 … L14-05` are contiguous within each module that has lessons.
- **Cross-reference consistency problem:** 61 files reference M03/M05/M09 (roadmap, curriculum
  map, glossary, learning path, 14 quizzes). Because `modules/README.md` keeps anchors for
  those modules, links resolve — they land on an "in preparation" section. No broken link, but
  the destination is empty. That is a completeness issue, reported in the completeness report,
  not a documentation-link failure.
- Duplicate files: **0** identical Markdown files (MD5 grouping over all 275).
- Missing images: **0** referenced, **0** expected. The course uses 18 Mermaid diagrams plus
  text descriptions instead of image assets, so there are no orphaned image paths.

## 4. Placeholders and instructor information

| Finding | Assessment |
| --- | --- |
| `TBD` / `TODO` in `docs/ARCHITECTURE.md` | **False positive** — they appear inside the list of forbidden content that the project's validator V08/V14 checks for |
| `TBD` in `templates/README.md` | **False positive** — it is an instruction ("do not leave a `TBD` outside this folder") |
| "in preparation" in `README.md`, `modules/README.md`, M02/M04 pages, resource library | **Accurate status labels**, not unfilled placeholders |
| Instructor details | Present once, in the root `README.md` "About the Instructor" section and module metadata — this is the course homepage, which is the documented exception; no instructor details appear inside lessons, labs or assessments |
| Deployment instructions in `README.md` | None found |
| `.github/workflows`, GitHub Pages config | None present (consistent with the restriction on creating them) |

## 5. Repository noise

- **32 `.pyc` files** exist under `modules/*/code/__pycache__/`. They are build artefacts, not
  content; if they are tracked by Git they will produce meaningless diffs. Not deleted in this
  audit (no destructive changes), but recorded as housekeeping.
- `_audit_nb_results.json` was created by this audit for evidence and has been removed; the
  audit reports themselves are the durable record.

## 6. Documentation quality

- Root `README.md` is 620 lines with a 20-entry contents list, an availability statement, a
  page-conventions block and a module-wise navigation table.
- `docs/` contains a curriculum map, roadmap, architecture and validation rules, FAQ, learning
  paths and an audit page. Cross-links between them all resolve.
- `resources/` provides a 136-entry curated library across 9 pages, a 267-term glossary and a
  papers list. Entry fields are consistent (7 fields per entry).
- Every lesson, lab, quiz and module page can be reached from the root README or from
  `modules/README.md`; no orphan documents were found other than the three orphan quizzes for
  unpublished modules.

## 7. Score

| Dimension | Weight | Score |
| --- | ---: | ---: |
| Internal link integrity | 35% | 35/35 (0 broken after fix) |
| Anchor integrity | 15% | 15/15 |
| Navigation consistency | 20% | 20/20 |
| Numbering and structure | 10% | 9/10 (empty anchors for absent modules) |
| Placeholders and prohibited content | 10% | 10/10 |
| External link health | 10% | 6/10 (not fully verifiable in this environment) |

**Audit 6 verdict: PASS WITH WARNINGS.** Every internal link and anchor resolves after the
eleven M04 anchor fixes. The warning is external-URL verification, which this environment's TLS
stack could not complete, plus the structural curiosity of anchors that point at modules which
do not exist.
