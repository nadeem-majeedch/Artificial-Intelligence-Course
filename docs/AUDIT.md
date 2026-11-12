# Repository Audit Report — Phase 01

| Field | Value |
| :--- | :--- |
| Repository | `nadeem-majeedch/Artificial-Intelligence-Course` |
| Local working copy | the repository root |
| Audit date | 10 November 2026 |
| Phase | 01 — Repository Audit and Architecture |
| Scope | Repository contents, Git state, remote state, local toolchain, constraints |

---

## 1. Verdict

**The repository is empty. This is a greenfield build.**

There is no existing course material, no earlier directory layout, no configuration file and no
commit history to preserve, migrate or reconcile. The architecture can therefore be designed on
merit rather than adapted around legacy decisions — and rule 7 ("do not overwrite existing
content without inspecting it") is satisfied vacuously, because there is no content to overwrite.

Two facts make this audit unusually short and unusually important:

1. **The GitHub remote exists but has zero refs.** It has been created but never pushed to.
2. **The local folder is not a Git repository at all.** No `.git` directory exists locally.

The second fact has a direct consequence for this phase's final deliverable: `git status` cannot
report a working tree, because there is no working tree to report on. Section 6 records this
precisely rather than presenting a green status line that would be misleading.

## 2. Evidence

All checks were read-only. No command in this audit wrote to the repository, the remote, or Git
history.

| # | Check | Command | Result |
| :--- | :--- | :--- | :--- |
| 1 | Local directory listing | `ls -la` | Empty except `.freebuff/` |
| 2 | Local file inventory | `find . -type f` | **2 files**, both Freebuff metadata |
| 3 | Git repository present | `git status` | `fatal: not a git repository (or any of the parent directories)` |
| 4 | Git remotes | `git remote -v` | No output — no remotes configured (no repository) |
| 5 | Remote branch refs | `git ls-remote <url>` | Exit `0`, **0 refs** — repository exists, has no branches |
| 6 | Remote reachability | `curl -o /dev/null -w "%{http_code}"` | **200** — remote is reachable and public |
| 7 | Python interpreter | `python --version` | **3.14.7** |
| 8 | `python3` alias | `python3 --version` | Not available (Windows App Execution Alias stub) |
| 9 | Jupyter stack | `jupyter --version` | notebook 7.5.7, jupyterlab 4.5.9, nbformat 5.11.1, nbclient 0.11.0 |
| 10 | Git version | `git --version` | 2.56.0.windows.2 |
| 11 | Shell | environment probe | Windows 10/11, Git Bash (POSIX syntax) |
| 12 | Scientific packages | `importlib.util.find_spec` probe | See section 4 |

### Local inventory (complete)

```
Artificial-Intelligence-Course/
└── .freebuff/
    ├── .gitignore      # ignores itself and project-id
    └── project-id      # d8dd795a-52b8-4522-8445-410e8dbccf2a
```

`.freebuff/` is Freebuff's own workspace marker. It must never be committed, and the root
`.gitignore` created in this phase excludes it.

## 3. Remote state

The remote repository is reachable (`HTTP 200`) and has **no branches, no tags and no commits**.
`git ls-remote` returned an empty reference list with exit status 0, which distinguishes "empty
repository" from "repository not found" (the latter returns a fatal error on stderr).

**Implication:** the first push of this project will be its initial commit. That action is
explicitly out of scope for this phase and for every phase until the instructor authorises it.

## 4. Local toolchain inventory

| Package | Status | Relevance |
| :--- | :--- | :--- |
| `numpy` | ✅ Present | All numerical lessons, M03–M11 |
| `pandas` | ✅ Present | Data handling, P04, M06 |
| `matplotlib` | ✅ Present | Visualisation in every module |
| `scipy` | ✅ Present | Optimisation, statistics, M05–M07 |
| `scikit-learn` | ✅ Present | Core of M06 |
| `torch` | ✅ Present | M07, M08, M09, M11 |
| `transformers` | ✅ Present | M08, M11 |
| `networkx` | ✅ Present | Graphs: search (M03), Bayesian networks (M04, M05) |
| `nbformat`, `ipykernel` | ✅ Present | Notebook generation and validation |
| `requests` | ✅ Present | Dataset downloads where unavoidable |
| `seaborn` | ❌ Absent | Optional visual polish, P04 |
| `nbconvert` | ❌ Absent | Notebook → HTML conversion if ever needed |
| `gymnasium` | ❌ Absent | M10 environments |
| `scikit-fuzzy` | ❌ Absent | M05 fuzzy logic (a ~120-line implementation is preferable anyway) |
| `openai` | ❌ Absent | M11/M12 API-optional lessons |
| `graphviz` | ❌ Absent | Diagram rendering (Mermaid is preferred) |
| `tensorflow`, `jax` | ❌ Absent | Not required; one framework is taught, not three |

## 5. Findings and their architectural consequences

Each finding is stated with the design decision it forces. These are the load-bearing constraints
behind [ARCHITECTURE.md](ARCHITECTURE.md).

| ID | Finding | Risk if ignored | Architectural response |
| :--- | :--- | :--- | :--- |
| **F1** | Repository is empty; no legacy structure | None — but an unstructured build would produce an unnavigable pile of files | Full numbering and naming scheme defined up front (§4 of the architecture) |
| **F2** | No local Git repository; remote has zero refs | First commit is the initial commit; history questions arise later | Phase 02 initialises the repository only with explicit authorisation; this phase performs no Git write operations |
| **F3** | Local Python is **3.14.7**, released recently | Student machines (often 3.10–3.12) will fail on syntax or wheels that 3.14 allows | Course targets **Python 3.11+**, avoids bleeding-edge syntax, and pins a tested dependency set. Content is validated against the stated minimum, not against this machine |
| **F4** | Students often have CPU-only, low-RAM laptops | Notebooks that need a GPU or 20 minutes to run are never completed | Hard budget: every notebook trains on CPU in **under 60 seconds**, on datasets shipped in the repo or generated synthetically |
| **F5** | No CI/CD permitted (rules 4 and 5) | Quality drift as ~90 lessons are written by different future passes | Validation is a **local, scripted, documented** process (`tools/`) plus a per-artifact Definition of Done; no workflow files are created |
| **F6** | Content surface is large (~89 lessons, 30+ labs) | Half-finished modules that look complete | Rule 9 formalised as a Definition of Done: **no lesson directory is created before its content exists**. Phases ship whole modules, never stubs |
| **F7** | Students may have limited bandwidth and no API budget | Lessons requiring paid API keys or large downloads exclude most of the class | **Offline-first**: local datasets, tiny models, deterministic synthetic data. Any hosted-API lesson (M11/M12) is explicitly optional with an offline alternative |
| **F8** | No `LICENSE` file | Content is "all rights reserved" by default, blocking reuse | Licence choice raised as an open decision (§7) — not chosen unilaterally |
| **F9** | `python3` alias is broken on this machine | Instructions copy-pasted into student shells fail on Windows | All commands in course material are written as `python` in a documented "Windows note" callout, and `python3` for macOS/Linux |
| **F10** | Notebooks do not render as HTML on a static site by default | Students see raw JSON instead of a readable page | Every notebook is paired with a Markdown lesson that carries the theory; notebooks are offered as downloadable, runnable artefacts, not as the primary reading surface |

## 6. Git state at the end of Phase 01

Verification performed after all files were created:

| Check | Command | Result | Conclusion |
| :--- | :--- | :--- | :--- |
| Working tree | `git status` | `fatal: not a git repository` | No repository exists, so no commit, branch or index was created |
| Remote refs | `git ls-remote <url>` | 0 refs | No push occurred; the remote is untouched |
| Local `.git` | directory probe | absent | No history was initialised, modified or rewritten |

**Statement:** no commit, push, pull, merge, tag or history modification was performed in this
phase. No GitHub Actions workflow and no GitHub Pages configuration were created. The repository
remains exactly as found: an empty remote with no local clone.

## 7. Open decisions requiring the instructor

These are recorded, not resolved. Each is placed in the phase where it is needed.

| # | Decision | Options | Needed by |
| :--- | :--- | :--- | :--- |
| D1 | **Licence** | (a) Content CC BY-NC-SA 4.0 + code MIT — recommended for an academic course; (b) CC BY 4.0 + MIT; (c) no licence (all rights reserved) | Phase 02 |
| D2 | **Target Python baseline** | (a) 3.11+ — recommended, widest wheel support; (b) 3.12+; (c) follow 3.14 | Phase 02 |
| D3 | **Deep-learning framework** | (a) PyTorch only — recommended; (b) PyTorch + Keras appendix | Phase 05 (M07) |
| D4 | **Hosted LLM access for M11/M12** | (a) offline-first with optional hosted key — recommended; (b) hosted API required; (c) local small model only | Phase 07 (M11) |
| D5 | **Assessment answers** | (a) answers hidden in collapsible blocks on the same page — recommended for self-study; (b) separate answer key pages | Phase 02 |
| D6 | **Repository initialisation** | When, and by whom, the first `git init` + push happens | Phase 02, on authorisation |

## 8. Conclusion

The audit found nothing to preserve and nothing to repair. The environment is capable
(Python, Jupyter and the full scientific stack are installed), the constraints are known
(no CI, no Pages configuration, CPU-only student hardware, offline-first), and the design space
is unconstrained by legacy choices.

Phase 01 therefore delivers a complete **blueprint**: a directory structure, a numbering scheme,
a curriculum inventory, artifact templates, quality and validation standards, a dependency map
and a phased build plan. Phase 02 begins construction once the instructor approves.
