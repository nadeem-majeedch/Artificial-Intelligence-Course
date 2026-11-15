# Phase 27 — MkDocs Material Website and GitHub Pages Deployment

**Date:** 15 November 2026  
**Repository:** `C:\Users\Nadeem\Documents\Artificial-Intelligence-Course`  
**GitHub:** <https://github.com/nadeem-majeedch/Artificial-Intelligence-Course>  
**Intended live URL:** <https://nadeem-majeedch.github.io/Artificial-Intelligence-Course/>  
**Instructor:** Engr. Dr. Muhammad Nadeem Majeed, Professor, Department of Data Science (PUCIT), University of the Punjab, Lahore, Pakistan.

## Final verdict

## PASS — WEBSITE BUILD AND DEPLOYMENT CONFIGURATION READY

The complete course builds locally in strict mode, all required module and download targets resolve, the rendered site was checked in a browser at desktop and mobile widths, and the GitHub Pages workflow is configured for the correct project-site base path.

No commit, push, tag, history change, remote change or deployment was performed.

## 1. Scope and constraints observed

- All 14 module directories, 89 module lessons, 38 laboratories, 22 assignments, 8 module projects, 14 quizzes and self-assessment sets, 12 capstone briefs and 29 module notebooks were preserved.
- Six prerequisite notebooks bring the runnable-notebook total to 35.
- Existing Markdown remains the single source of truth. No lesson body was copied into a second maintained source page.
- The approved four-layer licensing architecture was not changed: MIT for original code, CC BY 4.0 for original educational content, CC0 1.0 for original synthetic datasets, and upstream terms for third-party material.
- No generated site files or staging files are tracked.
- Git history and the remote were not modified.

## 2. Repository inventory used by the build

| Area | Count / location |
| :--- | :--- |
| Modules | 14 · `modules/M01…` to `modules/M14…` |
| Module lessons | 89 · `modules/M*/lessons/L*.md` |
| Module laboratories | 38 · `modules/M*/labs/lab-*.md` |
| Module notebooks | 29 · `modules/M*/notebooks/*.ipynb` |
| Prerequisite tracks | 4 · `prerequisites/P01…` to `P04…` |
| Prerequisite notebooks | 6 |
| Assignments | 22 · `assessments/` |
| Module projects | 8 |
| Capstone briefs | 12 |
| Quizzes and self-assessment | 14 + 14 |
| Existing Pages workflow before this phase | None |

The staging script revalidates the 14-module, 89-lesson and 38-laboratory inventory on every run and stops if the expected structure is missing.

## 3. Website architecture

### `mkdocs.yml`

Configured MkDocs Material with:

- `site_url: https://nadeem-majeedch.github.io/Artificial-Intelligence-Course/`
- `docs_dir: .site-build/docs`
- `site_dir: site`
- `strict: true`
- Material light/dark palettes, custom primary/accent colours, logo, favicon and Inter / JetBrains Mono fonts.
- Search, search suggestions, search highlighting, instant navigation, navigation tracking and section tracking, top links, footer navigation, table-of-contents following, code copy/annotations and linked tabs.
- Python/Pygments highlighting, tables, footnotes, definition lists, abbreviations, admonitions, details, tabbed content, Markdown in HTML, attribute lists, emoji icons and Mermaid fences.
- MathJax through `pymdownx.arithmatex` in generic mode with a local configuration script and a pinned MathJax 3.2.2 runtime.
- Mermaid 11.12.0, pinned on the CDN and rendered by a local script.
- A GitHub-compatible heading slugger so existing M04 in-page anchors resolve in the rendered site.
- `not_in_nav` entries for reports, templates, assessments, glossary detail pages, prerequisite lesson/lab pages and generated corpus Markdown.

### Deterministic staging

`scripts/stage_site.py` assembles `.site-build/docs` from the repository:

1. Copies `modules/`, `prerequisites/`, `assessments/`, `resources/`, `docs/`, `website/assets`, `website/stylesheets` and `website/javascripts`.
2. Copies the licensing files and root README content needed by course links.
3. Maps the custom website pages onto the documentation root, including `website/home.md` → `index.md`.
4. Rewrites repository-relative links only in the generated staging tree:
   - Root README links → hidden `course-home.md`, preserving anchors.
   - Source directory links such as `code/` and `capstone/briefs/` → their GitHub tree URLs, so no dead website directory URLs are produced.
   - Deliberately unhosted repository files (templates, ownership checklist) → their GitHub source URLs.
5. Removes corpus/output Markdown under `modules/*/code/**` from the website staging tree because those files are data, not student-facing pages.
6. Refuses to proceed if the expected module/lesson/lab inventory is absent.

The source Markdown is never edited by the staging process.

### Post-build validation

`scripts/check_site.py` checks:

- `site/index.html`
- search index and its JSON validity
- sitemap and at least 14 module URLs
- all 14 module landing pages
- all 89 lesson pages
- all 38 laboratory pages
- all 29 module notebooks as downloadable files
- the seven custom website pages
- logo, favicon, stylesheet, MathJax configuration and Mermaid script
- the `/Artificial-Intelligence-Course/` base path in the homepage
- absence of caches, logs, phase reports and other private/temporary artefacts in `site/`

### Repository hygiene

`.gitignore` now excludes:

```text
site/
.site-build/
.venv-site/
.cache/
```

The build is not committed; the workflow uploads `site/` as a Pages artifact.

## 4. Homepage and navigation

The custom homepage includes:

- Course title, subtitle and academic description.
- Instructor name, rank, department and university.
- Course learning outcomes (CLO1–CLO8).
- Explicit prerequisites and readiness-diagnostic links.
- The complete 14-module roadmap with focus and hours.
- Study workload and learning routes.
- The derive → implement → break → measure methodology.
- Laboratory, assignment, project and capstone guidance.
- Software requirements.
- Licensing summary.
- Getting-started steps.

Navigation is grouped as requested:

1. Home
2. Getting Started
3. Prerequisites
4. Modules 01–14 (overview plus expandable lessons, laboratories, summaries, assignments, projects and quizzes)
5. Laboratories
6. Assignments
7. Projects and Capstones
8. Quizzes and Self-Assessment
9. Resources
10. FAQ
11. Licensing
12. About the Instructor

Each module section contains its lessons and labs; associated assignments, projects, quizzes, summaries and the M14 capstone studio are included where present.

## 5. GitHub Pages workflow

`.github/workflows/deploy-pages.yml`:

- Triggers on pushes to `main` and on `workflow_dispatch`.
- Uses the official maintained action majors current at implementation time:
  - `actions/checkout@v7`
  - `actions/setup-python@v7`
  - `actions/configure-pages@v6`
  - `actions/upload-pages-artifact@v5`
  - `actions/deploy-pages@v5`
- Installs the complete pinned dependency set from `requirements-pages.txt`.
- Runs the course audit before staging.
- Runs the deterministic staging script.
- Runs `mkdocs build --strict`; broken links, missing pages, bad anchors and other warnings fail the build.
- Runs `scripts/check_site.py`.
- Configures Pages, uploads only `site/`, and deploys with the `github-pages` environment.
- Declares `contents: read`, `pages: write` and `id-token: write`.
- Uses `concurrency: group: pages` with `cancel-in-progress: false`.
- Does not commit generated files or run `gh-pages` deployment commands.

No second Pages workflow exists.

## 6. README

The root README now contains:

- The intended live course website URL.
- The repository URL.
- A short explanation that the website and repository share one Markdown source.
- Student start links.
- The existing four-layer licence summary and attribution guidance, retained unchanged.

## 7. Validation evidence

All commands below were run locally against the final files. The website environment was created fresh in `.venv-site` from `requirements-pages.txt`.

| Check | Result |
| :--- | :--- |
| Clean dependency install | PASS |
| Inventory staging | PASS — 14 modules, 89 lessons, 38 labs |
| MkDocs strict build | PASS — 0 warnings, exit 0 |
| `site/index.html` | PASS |
| Module landing pages | PASS — 14/14 |
| Lesson pages | PASS — 89/89 |
| Laboratory pages | PASS — 38/38 |
| Module notebook downloads | PASS — 29/29 |
| Built lesson links | PASS — 93 links, 0 missing |
| Built laboratory links | PASS — 38 links, 0 missing |
| Built notebook download links | PASS — 29 links, 0 missing |
| Project-site base path | PASS — `/Artificial-Intelligence-Course/` |
| Search index JSON | PASS |
| Sitemap module URLs | PASS |
| Private/temporary artefacts in `site/` | PASS — none |
| Source course audit | PASS — 4,310 links, 0 broken, 0 total problems |
| Hours audit | PASS — 0 failures |
| Licensing audit | PASS — 0 failures |
| `CITATION.cff` syntax/keys | PASS — parsed, 10 keys, 1 author |
| Python compilation | PASS |
| Pytest suite | PASS — 196 passed |
| Workflow YAML structure | PASS — triggers, permissions, environment and jobs verified |
| `git diff --check` | PASS — no whitespace errors |
| Tracked generated site files | PASS — none |

### Browser validation

The built site was served locally and inspected in Chromium:

- **MathJax:** 22 `.arithmatex` spans on a representative lesson produced 44 MathJax containers.
- **Mermaid:** one diagram produced one rendered SVG after the final fence configuration.
- **Markdown rendering:** tables (4), code blocks (3), admonitions (2) and tabbed content (2 tabs) rendered on the inspected pages.
- **Search:** search input present and search index loaded.
- **Mobile layout:** 390 × 844 viewport, no horizontal overflow; hero, buttons and content stack correctly.
- **Mobile navigation:** drawer opens, sections expand, and “Start Here” navigates to `/getting-started/`.
- **Canonical URL:** `https://nadeem-majeedch.github.io/Artificial-Intelligence-Course/getting-started/`.
- **Console:** no site JavaScript errors after the final Mermaid correction.

## 8. Limits and maintenance notes

- **No remote Actions run.** The workflow has been validated locally and its YAML parsed, but GitHub Actions itself was not executed and the site was not deployed. Remote publication and the Actions environment remain unverified until the owner pushes and runs the workflow.
- **Local vs workflow Python.** The local clean build used the available Python 3.14 interpreter; the workflow pins Python 3.12. The dependency set is platform-independent Python packages and installed successfully, but the exact Linux/Python 3.12 runner run has not occurred.
- **Material end-of-life notice.** MkDocs Material 9.8.1 prints a notice that upstream support ends on 5 May 2027. This does not affect the current build. The dependency should be reviewed before that date.
- **External runtime assets.** MathJax and Mermaid are loaded from `unpkg.com` at pinned versions. The browser check confirmed both loaded. A future move to fully vendored assets would remove the external runtime dependency.
- **GitHub latest-release lookup.** Material may request repository release metadata; a repository with no releases can return 404 for that optional request. This does not affect page rendering.

## 9. Files delivered or changed

New:

- `mkdocs.yml`
- `requirements-pages.txt`
- `.github/workflows/deploy-pages.yml`
- `scripts/stage_site.py`
- `scripts/check_site.py`
- `scripts/site_slugify.py`
- `website/home.md`
- `website/getting-started.md`
- `website/laboratories.md`
- `website/assignments.md`
- `website/projects-and-capstones.md`
- `website/quizzes-and-self-assessment.md`
- `website/licensing.md`
- `website/about-instructor.md`
- `website/assets/logo.svg`
- `website/assets/favicon.svg`
- `website/stylesheets/extra.css`
- `website/javascripts/mathjax.js`
- `website/javascripts/mermaid.js`
- `PHASE-27-WEBSITE-IMPLEMENTATION-REPORT.md`

Modified:

- `.gitignore`
- `README.md`
- `audit/check_course.py` — website source links are now audited against their staging location, with a source-local fallback for sibling website pages. Existing course link checks are unchanged.

## 10. Handover state

- Working tree contains the Phase 27 implementation but no commit was created.
- No files are staged.
- HEAD remains at `9e7e43422c0e9f34f8ce86ee47b048da9c44de42`.
- Remote remains `https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git`.
- No push, tag, release, manual Pages deployment or history modification occurred.
- The generated preview tree remains local and ignored: `.site-build/`, `site/`, `.venv-site/`.

The next owner action is to review the working tree, commit the Phase 27 changes, push to `main`, and watch the first GitHub Actions Pages run. The expected public URL is <https://nadeem-majeedch.github.io/Artificial-Intelligence-Course/>.
