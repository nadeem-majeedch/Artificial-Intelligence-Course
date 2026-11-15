# Course Architecture

| Field | Value |
| :--- | :--- |
| Repository | `Artificial-Intelligence-Course` |
| Phase | 01 — Repository Audit and Architecture |
| Status | Proposed; implemented progressively in Phases 02–10 |
| Supersedes | Nothing (greenfield repository) |

This document is the build specification. It defines where files live, what they are called, what
each artifact must contain, and what "finished" means. The *what* is taught lives in
[Curriculum Map](CURRICULUM-MAP.md); the *when* lives in [Implementation Roadmap](IMPLEMENTATION-ROADMAP.md).

---

## 1. Purpose and Audience

**Primary audience:** a student working alone, on a laptop, possibly with limited bandwidth, who
has no instructor available to answer questions at 11 p.m.

**Secondary audience:** an instructor who adopts this repository for a course and needs the
material to be predictable enough to assign.

**Tertiary audience:** a self-learner returning after months away, who needs to re-enter the
material at the right point without reading everything again.

Every structural decision below is justified by one of those three readers. A structure that
looks elegant to a maintainer but forces a student to guess where the lab for lesson 3.5 lives
has failed.

## 2. Design Principles

| # | Principle | Consequence in the repository |
| :--- | :--- | :--- |
| P1 | **Self-study first.** No lesson may depend on an instructor's verbal explanation. | Intuition before formalism, worked examples before exercises, "common mistakes" and "what to do next" in every lesson |
| P2 | **Predictable structure.** Every lesson of the same kind has the same shape. | Mandatory eleven-section lesson anatomy (§5); automated section checks |
| P3 | **One concept per page.** A lesson teaches one idea well rather than five badly. | 93 lessons rather than 20 long chapters |
| P4 | **Runnable, not merely readable.** Code a student cannot execute is decoration. | Every code block is self-contained; every notebook runs top-to-bottom on CPU in under 60 s |
| P5 | **Offline-first.** Internet access is a convenience, never a requirement. | Local datasets, synthetic generators, API-optional hosted lessons (§13) |
| P6 | **Relative links only.** The repository must work locally, on GitHub, and on any static host. | No absolute repository URLs, no site-root paths, no generated permalinks |
| P7 | **Native rendering.** Prefer what platforms already render over custom machinery. | Markdown, Mermaid, LaTeX, `<details>`, tables — no JavaScript, no custom site application |
| P8 | **Honest scope.** A stub is worse than an absence. | No placeholder lessons; a module directory exists only when its content does (§10) |
| P9 | **Assessable.** Every stated outcome has a matching quiz, lab or assignment. | CLO traceability table in the curriculum map |
| P10 | **Accessible by default.** Diagrams, tables, colour and text must work for every student. | Alt text, diagram descriptions, no colour-only meaning (§11) |

## 3. Proposed Directory Structure

This is the **target** structure. Only `docs/`, `templates/`, `README.md` and `.gitignore` exist
today; everything else is created by the phase named in the comment.

```text
Artificial-Intelligence-Course/
├── README.md                     Student homepage: orientation, module list, how to study   [P01 ✓]
├── .gitignore                    Python, Jupyter, OS and Freebuff ignores                    [P01 ✓]
│
├── docs/                         Course governance (not student reading)
│   ├── AUDIT.md                  Repository audit report                                     [P01 ✓]
│   ├── ARCHITECTURE.md           This document                                               [P01 ✓]
│   ├── CURRICULUM-MAP.md         Module numbering, lesson inventory, progression             [P01 ✓]
│   ├── IMPLEMENTATION-ROADMAP.md Phase plan with exit criteria                               [P01 ✓]
│   ├── STYLE-GUIDE.md            Editorial voice, formatting, maths and code conventions     [P02]
│   ├── VALIDATION.md             Check definitions V01–V14 and how to run them               [P02]
│   └── DECISIONS.md              Architecture decision records                               [P02]
│
├── prerequisites/                Remediation track, P01–P04
│   ├── README.md                 Which section do I need? Readiness self-check             [P03 ✓]
│   ├── diagnostic.md             Forty-question self-assessment across all four sections
│   ├── P01-python-programming/
│   ├── P02-mathematics-for-ai/
│   ├── P03-probability-and-statistics/
│   └── P04-data-preparation-and-visualization/
│
├── modules/                      The course proper, M01–M14
│   ├── README.md                 Module index, progression map, "where do I start?"         [P02]
│   ├── M01-introduction-and-foundations/
│   ├── M02-intelligent-agents-and-environments/
│   ├── M03-problem-solving-and-search/
│   ├── M04-knowledge-representation-and-reasoning/
│   ├── M05-uncertainty-and-bayesian-reasoning/
│   ├── M06-machine-learning-fundamentals/
│   ├── M07-neural-networks-and-deep-learning/
│   ├── M08-natural-language-processing/
│   ├── M09-computer-vision/
│   ├── M10-reinforcement-learning/
│   ├── M11-generative-ai-and-llms/
│   ├── M12-ai-agents-and-agentic-systems/
│   ├── M13-responsible-and-secure-ai/
│   └── M14-applications-and-capstone/
│
├── capstone/                     M14 project studio
│   ├── README.md                 How the capstone works, milestones, timeline             [P09]
│   ├── project-catalogue.md      12 briefs: CP-01 … CP-12                                 [P09]
│   ├── milestones/               Proposal, prototype, evaluation, final report guides    [P09]
│   ├── rubric.md                 Six-dimension rubric with band descriptors              [P09]
│   └── report-template.md        Student report skeleton                                [P09]
│
├── datasets/                     Every dataset the course uses
│   ├── README.md                 Index: name, task, size, licence, which module uses it  [P02]
│   └── <dataset-slug>/
│       ├── README.md             Data dictionary: columns, types, rows, source, licence  [per dataset]
│       ├── data/                 Committed CSV/JSON/Parquet, small by policy (§13)
│       └── SOURCE.md             Provenance and citation
│
├── glossary/
│   ├── README.md                 How to use the glossary, alphabetical index              [P02]
│   └── terms.md                  A–Z table: term, definition, first taught in           [grows each phase]
│
├── resources/
│   ├── README.md                 Curated further reading by goal, not by link dump       [P10]
│   ├── books-and-papers.md
│   ├── courses-and-videos.md
│   ├── tools-and-libraries.md
│   └── datasets-and-benchmarks.md
│
├── faq/
│   └── README.md                 Student FAQ: setup, study order, stuck-points, errors   [P10]
│
├── instructor/
│   ├── README.md                 About the instructor                                   [P02]
│   └── course-info.md            About the course: outcomes, schedule, assessment, policy [P02]
│
├── templates/                    Authoring templates (not student content)
│   ├── README.md                 Which template to copy for which artifact               [P01 ✓]
│   ├── lesson.md                                                                        [P01 ✓]
│   ├── lab.md                                                                           [P01 ✓]
│   ├── assignment.md                                                                    [P01 ✓]
│   ├── module-readme.md                                                                 [P01 ✓]
│   ├── quiz.md                                                                          [P01 ✓]
│   └── notebook.ipynb                                                                   [P01 ✓]
│
└── tools/                        Local validation and authoring helpers (no CI, §10)
    ├── validate.py               Runs V01–V14 over the repository                       [P02]
    ├── check_links.py            Resolves every relative link and anchor                [P02]
    ├── new_lesson.py             Scaffolds a lesson from the template                   [P02]
    └── strip_notebooks.py        Clears outputs before committing notebooks             [P02]
```

### Module internal layout

Every module is identical in shape. Subdirectories exist only when they contain real content —
a module with no notebook does not get an empty `notebooks/` folder (P8).

```text
modules/M03-problem-solving-and-search/
├── README.md                  Module landing page (§8)
├── lessons/
│   ├── L03-01-formulating-a-problem-as-search.md
│   ├── L03-02-uninformed-search.md
│   └── … L03-08
├── labs/
│   ├── lab-03-01-route-planning-under-constraints.md
│   └── lab-03-02-game-agent-and-timetable-solver.md
├── notebooks/
│   └── nb-03-01-search-workbench.ipynb
├── assignments/
│   └── asg-03-a-star-with-a-designed-heuristic.md
├── quizzes/
│   └── quiz-03.md
├── projects/
│   └── mp-03-maze-solving-competition.md
└── resources.md               Module-specific reading and tools (optional)
```

**Why artifacts sit inside their module rather than in top-level `labs/` and `notebooks/` folders:**
a student arriving at M03 sees everything for M03 in one place, relative links stay short and
stable (`../lessons/…`, `./lab-03-01-…`), and deleting or moving a module never orphans a file
elsewhere in the tree. The cost is that a maintainer looking for "all labs" must search; that is
the correct trade-off because the student's navigation is the requirement.

## 4. Naming and Numbering Scheme

### Identifiers

| Artifact | ID format | Example | Scope |
| :--- | :--- | :--- | :--- |
| Prerequisite unit | `P{NN}` | `P03` | Global |
| Prerequisite lesson | `LP{NN}-{NN}` | `LP02-03` | Within section |
| Module | `M{NN}` | `M03` | Global |
| Lesson | `L{MM}-{NN}` | `L03-05` | Within module |
| Laboratory | `LAB-{MM}-{NN}` | `LAB-03-02` | Within module |
| Notebook | `NB-{MM}-{NN}` | `NB-03-01` | Within module |
| Assignment | `ASG-{MM}` | `ASG-03` | One per module |
| Quiz | `QUIZ-{MM}` | `QUIZ-03` | One per module |
| Quiz question | `Q{MM}.{NN}` | `Q03.07` | Within quiz |
| Mini-project | `MP-{MM}` | `MP-03` | One per module (M01–M13) |
| Capstone brief | `CP-{NN}` | `CP-07` | Global |
| Stage | `S{n}` | `S2` | Global |

Zero-padding is mandatory: `M03`, not `M3`. This makes lexicographic sort equal to teaching
order, in the repository, in a file manager, and in a generated site index.

### Filenames

| Artifact | Pattern | Regular expression |
| :--- | :--- | :--- |
| Module directory | `M{NN}-kebab-title` | `^M\d{2}-[a-z0-9]+(-[a-z0-9]+)*$` |
| Prerequisite unit | `P{NN}-kebab-title` | `^P\d{2}-[a-z0-9]+(-[a-z0-9]+)*$` |
| Lesson | `L{MM}-{NN}-kebab-title.md` | `^L\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$` |
| Lab | `lab-{mm}-{nn}-kebab-title.md` | `^lab-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$` |
| Notebook | `nb-{mm}-{nn}-kebab-title.ipynb` | `^nb-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.ipynb$` |
| Assignment | `asg-{mm}-kebab-title.md` | `^asg-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$` |
| Quiz | `quiz-{mm}.md` | `^quiz-\d{2}\.md$` |
| Mini-project | `mp-{mm}-kebab-title.md` | `^mp-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$` |
| Capstone brief | `CP-{NN}-kebab-title.md` | `^CP-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$` |
| Dataset | `datasets/{slug}/` | `^[a-z0-9]+(-[a-z0-9]+)*$` |

Titles in filenames are lowercase ASCII kebab-case, no stop words beyond what clarity requires,
no version suffixes, no dates. `a-star-search.md`, not `A_Star_Search_v2_final.md`.

### Stability rules

1. **IDs are permanent.** Once `L03-05` is published it never becomes `L03-06`, and no ID is ever
   reused for a different topic. External links, notes and student bookmarks depend on this.
2. **Append, do not renumber.** If a lesson is needed between two existing ones, it takes the next
   free number in that module (`L03-09`) and is placed in the reading order the module README
   defines. Renumbering is permitted only before a module is released, and only if the same
   commit updates every reference.
3. **Splitting a lesson** creates a new ID; the original keeps its ID and its topic.
4. **Module numbers are fixed** at M01–M14 as approved. New topics that do not fit an existing
   module become an appendix (`M15+`) only with instructor approval, or a lesson inside the
   closest module.

### No YAML front matter

Content files carry **no** YAML front matter. Metadata appears as a visible table or blockquote at
the top of the page. Reasons: front matter is meaningless to students reading on GitHub, it
couples the repository to one static-site generator, and it duplicates information a validator can
extract from headings. The repository must render correctly with no build step at all.

## 5. Lesson Anatomy

Every lesson file follows this exact skeleton. `templates/lesson.md` is the canonical copy.

```markdown
# L03-05 — A* Search: Admissibility, Consistency and Optimality

| Module | M03 · Problem Solving and Search |
| :--- | :--- |
| Level | 200 |
| Study time | 50 minutes |
| Prerequisites | [L03-04](../modules/M03-problem-solving-and-search-algorithms/lessons/L03-04-local-search-hill-climbing-annealing-genetic.md) |
| Notebook | [NB-03-01](../modules/M03-problem-solving-and-search-algorithms/notebooks/nb-03-01-search-workbench.ipynb) |
| Lab | [LAB-03-01](../modules/M03-problem-solving-and-search-algorithms/labs/lab-03-01-route-planning-under-constraints.md) |

[← Previous: Heuristics](...) · [Module home](../README.md) · [Next: Minimax →](...)

## 1. Learning Objectives
## 2. Prerequisite Knowledge
## 3. Conceptual Explanation
## 4. Worked Examples
## 5. Visual Explanation
## 6. Mathematical Formulation
## 7. Python Implementation
## 8. Practical Applications
## 9. Common Mistakes
## 10. Self-Assessment
## 11. Further Reading
```

### Section requirements

| § | Section | Must contain | Notes |
| :--- | :--- | :--- | :--- |
| — | Title | `# L{ID} — Plain-language title` | Exactly one H1 per file |
| — | Metadata | Visible table: module, level, study time, prerequisites, notebook, lab | Prerequisite rows link to lessons |
| — | Navigation | Previous / module home / next | First and last lesson use "Module start" / "Module end" |
| 1 | Learning Objectives | 3–5 objectives starting with a measurable verb ("explain", "implement", "choose", "evaluate") | Never "understand" alone |
| 2 | Prerequisite Knowledge | What the student must already know, with links | If nothing is required, say so explicitly |
| 3 | Conceptual Explanation | Intuition → formal idea → why it matters; H3 subsections allowed | The longest section; no code here |
| 4 | Worked Examples | ≥ 2, fully traced by hand, with all intermediate steps | Numbers chosen so the student can check by hand |
| 5 | Visual Explanation | Mermaid diagram or table **plus** a text description | Required even when the point seems visual-only |
| 6 | Mathematical Formulation | Formal statement, symbol table, assumptions | If genuinely not applicable, state why in one sentence |
| 7 | Python Implementation | Complete, runnable code; expected output shown | Must run with the course's pinned library set |
| 8 | Practical Applications | ≥ 2 real systems or domains, with what the technique buys them | No hand-waving ("used in games") |
| 9 | Common Mistakes | ≥ 3, each with symptom, cause, fix | Written as the student's error, not the author's |
| 10 | Self-Assessment | 5–10 questions; answers in `<details>` blocks | Mix recall, application, judgement |
| 11 | Further Reading | 2–5 annotated entries with links and a one-line reason to read | Annotated, not a bibliography |

Optional trailing sections, allowed after §11: `## Key Terms` (linking to the glossary) and
`## What to Do Next`. Anything else is a signal the lesson is trying to cover two topics and
should be split.

**Length target:** 1,200–2,500 words for a 45–60 minute lesson. Below 1,000 words it is usually a
stub; above 3,500 it is usually two lessons.

## 6. Laboratory Anatomy

Labs are where a student discovers that real data and real constraints are messier than the
lesson suggested. `templates/lab.md` is the canonical copy.

| Section | Must contain |
| :--- | :--- |
| **Scenario** | A realistic, named situation with a stakeholder and a decision to be made — not "now try it on another dataset" |
| **Your role** | The student's job title and remit (e.g. "you are the data scientist asked to…") |
| **Given** | Files, datasets, starter code, constraints, and what is *not* provided |
| **Requirements** | Numbered functional and non-functional requirements (accuracy target, runtime, interpretability) |
| **Tasks** | 4–8 ordered tasks, each with an observable output |
| **Deliverables** | Exact files and sections the student submits, with names |
| **Evaluation criteria** | Rubric table: criterion, weight, what "excellent" looks like |
| **Extension challenges** | 2–4 optional harder tasks for strong students |
| **Hints** | Progressive hints inside `<details>` blocks, never the full solution |
| **Reflection** | 3 questions on trade-offs and limitations |
| **Time budget** | Expected effort and a suggested split across sessions |

A lab must be completable with the repository's own datasets and no paid service. Every task must
name how the student can tell they have succeeded ("your route cost must be ≤ 42 and your search
must expand no more than 300 nodes").

## 7. Assignment and Mini-Project Anatomy

Assignments are individual, assessed, and open-ended enough to prevent copy-paste solutions.
Mini-projects are smaller, creative and often competitive.

**Assignment** (`templates/assignment.md`): Context → Objective → Specification (inputs, outputs,
constraints, interface) → Starter materials → Tasks → Deliverables → Rubric → Submission checklist
→ Academic-integrity note → Estimated effort → Extensions.

**Mini-project**: Brief → Constraints → Success criteria → Suggested approach → Ideas to stand out
→ Presentation format (a short report and one figure) → Estimated effort.

Both must state the **interface** explicitly when code is submitted (function names, file names,
CLI arguments), so that evaluation is mechanical and the student is not guessing.

## 8. Quiz, Notebook and Module Page Anatomy

### Quiz (`QUIZ-{MM}`)

Instructions → 12–20 multiple-choice questions (four options each, one correct) grouped by lesson,
with difficulty labels → answer key in `<details>` blocks, each answer giving the reasoning and the
lesson that teaches it → 3–5 short-answer questions with model answers → a "where to revise" table
mapping each wrong answer to a lesson.

Self-marking guidance: 80% or above means move on; 60–79% means reread §3 and redo the notebook;
below 60% means revisit the prerequisite lessons named in the module README.

### Notebook (`NB-{MM}-{NN}`)

Cell order is fixed: title and ID → objectives → environment check → concept recap (short, links
back to the lesson) → guided walkthrough → exercises with `# YOUR CODE HERE` → self-check with
expected results → "what you learned" → cleanup. Rules are in §12.

### Module README (`templates/module-readme.md`)

Overview (2–4 sentences: why this module exists) → Learning outcomes (mapped to CLOs) →
Prerequisites (with links and a 5-question readiness self-check) → Module map table (ID, title,
type, time, link, status) → Suggested study plan (seven-day schedule) → Assessment for this module
→ Key terms → Resources → Navigation (previous module, next module, course home).

The module map table is the most important element: it is the module's table of contents and the
only place where a student sees lessons, labs, notebooks and assessments together.

## 9. Navigation and Site Model

The repository is designed to be readable in three contexts, with no custom application:

| Context | How it works |
| :--- | :--- |
| **GitHub web UI** | `README.md` acts as the directory index; Markdown tables, Mermaid, LaTeX and `<details>` render natively |
| **Local clone** | Every relative link resolves in a Markdown viewer such as VS Code preview |
| **Static site** | Any Markdown-to-HTML pipeline (GitHub Pages' default Jekyll included) works without configuration, because there is no front matter, no templating and no absolute URL |

Rules that keep all three working:

1. **Relative links only**, with explicit filenames: `../lessons/L03-04-…md`, never `/modules/…`
   and never `https://github.com/<org>/<repo>/blob/main/…`.
2. **`README.md` in every directory** acts as its landing page.
3. **Breadcrumbs on every page**: `Course home → Module → Lesson`, as a single line under the
   metadata table.
4. **Previous/next links on every lesson**, so a student never needs the sidebar.
5. **Notebooks are linked as files**, not embedded: a student downloads or opens them in Jupyter.
   The theory they need is always in the Markdown lesson, so a rendering environment that cannot
   display `.ipynb` never blocks learning.
6. **Anchors are stable**: section headings are numbered (`## 3. Conceptual Explanation`), and
   cross-file anchors use the generated form (`#3-conceptual-explanation`).
7. **No JavaScript, no build step, no theme dependency.** Tables and `<details>` replace accordions
   and tabs.
8. **Navigation depth ≤ 3 clicks** from the homepage to any lesson.

## 10. Content Quality and Validation Standards

Because the project rules forbid CI/CD and deployment configuration, quality is enforced by a
**local, repeatable validation pass** plus a per-artifact Definition of Done.

### 10.1 Definition of Done

An artifact is done only when all of the following hold:

- [ ] Required sections present, in order, with the mandated content (§5–§8)
- [ ] Every internal link resolves, including anchors
- [ ] Every code block runs as written; outputs shown match reality
- [ ] Mathematical notation defined before use; symbols appear in a symbol table
- [ ] Every diagram has a text description; every image has alt text
- [ ] Self-assessment answers present, correct and hidden in `<details>`
- [ ] Cross-references added: module README table, previous/next links, glossary terms
- [ ] `tools/validate.py` passes with zero errors for the file
- [ ] Read once as a student would, on a narrow window, with no prior context

### 10.2 Validation checks

| ID | Check | Severity |
| :--- | :--- | :--- |
| V01 | Directory names match the module/unit patterns; one `README.md` per directory | Error |
| V02 | Filenames match the artifact patterns (§4) | Error |
| V03 | Lesson contains the eleven required H2 sections, in order | Error |
| V04 | Lesson metadata table present with module, level, time, prerequisites | Error |
| V05 | Every relative link resolves to an existing file; every anchor exists | Error |
| V06 | Exactly one H1; heading levels never skip (H1→H2→H3) | Error |
| V07 | `$`/`$$` delimiters balanced; no image-of-formula; symbols defined | Error |
| V08 | Python blocks parse (`ast.parse`) and contain no `TODO`, secrets or `!pip install` | Error |
| V09 | Notebooks: valid nbformat 4.5, outputs cleared, no absolute paths, no network calls, seeded | Error |
| V10 | Images have alt text; Mermaid blocks are followed by a text description | Error |
| V11 | Quiz answer keys exist for every question and are inside `<details>` | Error |
| V12 | Prerequisite targets exist and are plausible (no forward references except declared soft ones) | Warning |
| V13 | Glossary: bolded key terms have entries | Warning |
| V14 | Forbidden content: instructor details outside `instructor/` and the homepage, deployment instructions in `README.md`, workflow files, placeholder text (`Lorem`, `TODO`, `TBD`) | Error |

**Prohibited by project rules, and checked by V14:** `.github/workflows/*`, any GitHub Pages
configuration, deployment instructions in `README.md`.

### 10.3 How validation runs

`python tools/validate.py` walks the repository and prints a report grouped by file, with an exit
code of 1 on any error. `python tools/check_links.py` performs the link and anchor sweep on its
own, since it is the check most likely to break as files move. Both are run by the author before a
phase is declared complete, and the result is recorded in that phase's summary.

No validation runs in CI. The compensating control is that validation is **cheap enough to run
often** and its output is recorded per phase.

### 10.4 Review standard

Each module receives two passes before it is marked complete: a **technical pass** (a subject
expert checks correctness, currency and code) and an **editorial pass** (a reader who does not know
the topic checks comprehension, link integrity and accessibility). The same reviewer cannot
perform both passes on the same module.

## 11. Accessibility Standards

| Requirement | Implementation |
| :--- | :--- |
| Alternative text | Every image: `!What it shows` — describes the content, not the filename |
| Diagram descriptions | Every Mermaid block is followed by a paragraph beginning *Text description of the diagram:* |
| Colour independence | No meaning conveyed by colour alone in plots; use markers, line styles and direct labels |
| Structure | One H1; sequential heading levels; real tables with header rows, never space-aligned text |
| Link text | Descriptive ("the A\* worked example"), never "click here" |
| Contrast and size | Plot defaults set to a readable size (≥ 8 in wide, ≥ 10 pt); no default pastel-only palettes |
| Motion and interaction | None. No auto-playing media, no hover-only content |
| Language | Plain English, short sentences, technical terms defined on first use, consistent spelling |
| Math | LaTeX source (readable by a screen reader and by the student) rather than rendered images |

## 12. Code, Reproducibility and Notebook Policy

**Language baseline:** Python 3.11+ (see [Audit F3](AUDIT.md#5-findings-and-their-architectural-consequences)).
Windows users run `python`; macOS/Linux users may use `python3`. Both forms are shown on first use
in P01 and never again.

**Code style**

- PEP 8, Black-formatted, 88 columns.
- Type hints on public functions; NumPy-style docstrings for anything a student will call.
- No wildcard imports; explicit imports at the top of each block (notebook cells are self-contained).
- Deterministic randomness: `rng = np.random.default_rng(seed)`; every stochastic example fixes
  `seed`; PyTorch examples set `torch.manual_seed`.
- Educational implementations are written plainly (readability over speed), with a note when a
  library would be preferred in production.
- No hidden state between cells: a notebook must run correctly with "Restart & Run All".

**Library tiers**

| Tier | Contents | Requirement |
| :--- | :--- | :--- |
| Core | `numpy`, `pandas`, `matplotlib`, `scipy`, `scikit-learn` | Required for M01–M06 and P01–P04 |
| Deep learning | `torch` (CPU) | Required from M07 |
| NLP | `transformers`, `datasets` | M08, M11 |
| RL | `gymnasium` | M10 (a bundled minimal environment is the fallback) |
| Optional | `seaborn`, `networkx`, `shap`, `scikit-fuzzy` | Named per lesson; never required for assessment |

**Notebook policy**

1. `nbformat` 4.5, Python 3 kernel, one notebook per listed ID.
2. **Committed with outputs cleared** and execution counts `null`, so diffs stay reviewable. The
   lesson Markdown shows expected output as text.
3. Runs top-to-bottom in **under 60 seconds on a CPU laptop**; no GPU assumptions.
4. **Offline by default.** Data comes from `datasets/`, is generated in-cell, or is a documented
   first-run download of small pretrained weights. Any download must have an offline fallback and
   must be named in the module page.
5. Paths resolved from the repository root by upward search, never hard-coded:

   ```python
   from pathlib import Path

   def repo_root(start: Path | None = None) -> Path:
       """Walk upwards until the repository root (has README.md and modules/) is found."""
       for candidate in [start or Path.cwd(), *(start or Path.cwd()).parents]:
           if (candidate / "README.md").exists() and (candidate / "modules").exists():
               return candidate
       raise RuntimeError("Run this notebook inside the course repository.")
   ```

6. No `!pip install`, no shell escapes, no writes outside the notebook's own folder.
7. Every figure saved to `outputs/` is git-ignored; figures committed for documentation go to the
   module's `figures/` folder with descriptive names.

## 13. Datasets, Offline-First and Hosted API Policy

**Datasets**

- One folder per dataset under `datasets/`, with `README.md` (schema, rows, licence, source,
  intended use, which modules use it) and `SOURCE.md` (citation and provenance).
- Small by policy: ≤ 5 MB per file, ≤ 25 MB for the repository as a whole for committed data.
  Larger sources are described with a download script and an offline fallback.
- No personal, confidential or scraped-without-consent data. No dataset whose licence forbids
  redistribution.
- Synthetic generators are preferred for illustrations; the generator is committed next to the data.
- A dataset is never referenced before it exists: a lesson links to a real folder or to nothing.

**Offline-first**

Every lesson, lab and assignment must be completable with no internet connection and no paid
account. Where a hosted service is pedagogically important, the material supplies:

1. an offline path that teaches the same concept (a small local model, a mock API, or a recorded
   response fixture),
2. an online path clearly marked **optional**,
3. an explicit statement that assessment never depends on the online path.

**Hosted API policy (M11, M12)**

- Keys are read from environment variables (`OPENAI_API_KEY` or equivalent), never committed,
  never printed, never embedded in a notebook output.
- Each lesson names the cost implication and a token-budget estimate.
- Prompt-injection and data-exfiltration warnings accompany any tool-using exercise.
- A `.env.example` documents required variable names with empty values.

## 14. Risks, Trade-offs and Open Questions

| # | Risk / trade-off | Mitigation |
| :--- | :--- | :--- |
| R1 | **Volume.** 114 lessons is far beyond one writing pass. | Phases ship complete modules; counts are tracked and shortfalls reported, not hidden |
| R2 | **Notebook rot.** No CI means notebooks are not executed on every change. | Each phase executes every notebook it touches; dependency versions pinned in one place; runtime budget keeps verification cheap |
| R3 | **Co-location vs discoverability.** Artifacts live inside modules. | Module README tables plus repository-wide indexes (`modules/README.md`, `datasets/README.md`) |
| R4 | **No CI.** Quality depends on discipline. | Cheap local validator + explicit Definition of Done + recorded per-phase results |
| R5 | **Static-site coupling.** Pages configuration is out of scope. | No front matter, no plugins, no absolute paths; the content is portable to any host |
| R6 | **Framework churn in M11/M12.** LLM tooling changes monthly. | Teach durable concepts; pin specific tools inside labs and date them; keep API details in one place per lab |
| R7 | **Single-maintainer bottleneck.** | Templates and tooling reduce per-lesson cost; reviewer roles defined in §10.4 |
| R8 | **Figure size in the repository.** Committed images inflate the repo. | Prefer Mermaid and tables; images only where they teach something text cannot, compressed and dimensioned |

**Open questions carried into Phase 02** (from [Audit §7](AUDIT.md#7-open-decisions-requiring-the-instructor)):
licence, Python baseline confirmation, deep-learning framework scope, hosted-LLM policy, answer-key
format, and authorisation to initialise Git history.
