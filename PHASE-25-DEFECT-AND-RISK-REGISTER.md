# Phase 25 — Defect and Risk Register

**Status key:** Corrected = fixed during this audit; Open = requires owner action; Observation =
limitation or improvement opportunity, not a demonstrated defect.  
**Severity key:** Critical / High / Medium / Low / Observation.

No critical defect was found. No open High-severity defect remains. The only High item was corrected
during the audit.

| ID | Finding | Severity | Status | Evidence | Required action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | M08 attention worked example gave softmax weights 0.373/0.354/0.273, which do not follow from its own scaled logits 0.636/0.580/0.495. The correct weights are 0.355/0.336/0.309. | High | **Corrected** | Recalculated softmax; documented in `modules/M08.../lessons/L08-06...md` | None; corrected text now says "most to 'the', then itself, then 'sat'" |
| D-02 | M11 README said M08 lessons were unpublished; six M08 lessons, three notebooks and three labs exist. | Medium | **Corrected** | `modules/M11.../README.md`; M08 module map and inventory | None; M08 now listed as recommended, not absent |
| D-03 | Main README claimed every notebook runs in under a minute and no notebook needs a download. Measured maximum was 82.8 s; two M11 notebooks use cached pretrained weights and made an HF Hub request on first use. | Medium | **Corrected** | Notebook regression 500.1 s; M11 warnings; M11 README documents model downloads | None; README now states "most in seconds, longest about 1–1.5 min" and documents first-run downloads |
| D-04 | LAB-14-01 said `graphs.py` takes ~30 s; clean runs take 135–147 s. | Low | **Corrected** | Three timed runs; Phase 24A reports record 135 s | None; lab now says ~2 min |
| D-05 | M14 exact latency ratios are not reproducible across runs: int8 vs float measured 1.72× in this audit versus 2.62× in the lesson/summary; pruning 1.10× versus 1.45×. Direction (int8 slower, pruning not faster) held. | Medium | **Open** | `python efficiency.py`, 26 s; lab and lesson quotes | Owner should report a range/environment, or re-measure on the publication machine before presenting exact constants as universal. Do not tune against a test set; this is a benchmarking caveat, not a model result. |
| D-06 | Local generated artefacts at root: `.coverage`; ignored `_hf_dl.log`, `_pip_cv2.log`, `_pip_gym.log`, `_pip_sp.log`; 21 `__pycache__` directories; untracked `audit/*.json`/`*.log`. | Low | **Open** | `git status --porcelain`; filesystem scan | Owner may remove or ignore before committing. They do not affect course execution. Do not clean the working tree as part of this audit. |
| D-07 | No browser/site generator/HTML target exists (static Markdown, 15 Mermaid diagrams, no images), so visual rendering, mobile layout and Mermaid rendering are unverified. | Observation | **Open** | No `mkdocs`, `package.json`, `index.html`; 0 images | Owner should preview on GitHub or a chosen renderer before publication. Do not claim a visual pass. |
| D-08 | Licensing: `google/flan-t5-small` model-card licence and UCI digits/Iris terms were not re-fetched; model outputs and third-party quotations were not exhaustively audited. No legal clearance is claimed. | Observation (owner-review risk) | **Open** | `THIRD-PARTY-ATTRIBUTIONS.md` §8; `LICENSING-INVENTORY.md` uncertainties; `check_licensing.py` is mechanical | Owner must confirm model/dataset terms and quotation policy before public release. No licence file was changed. |
| D-09 | `CITATION.cff` declares `license: MIT` although the repository is mixed MIT/CC BY/CC0. CFF has no native multi-licence field. | Low | **Open** | `CITATION.cff`; README licence section | Owner may add a note that the citation metadata refers to code, with content under CC BY 4.0. Not a functional defect. |
| D-10 | `tests/test_agents.py` conditionally skips if `send_email` is removed from the tool registry, so a regression could silently skip three tests. It did not skip in this run (196 passed, no skips). | Low | **Open** | `tests/test_agents.py:19` | Owner may change the helper to fail hard if the tool is expected. Not changed during this audit to avoid altering test semantics without approval. |
| D-11 | Minor heading-level jumps (H1→H3) in L06-05, L06-10 and seven resource-library pages; some H1 matches are code comments inside fences, not real headings. | Low | **Open** | Heading scan over 392 Markdown files | Editorial/accessibility polish; no content impact |
| D-12 | LAB-14-01 uses five seeds and two synthetic graph families; SBM edges are independent and classes equal-sized. Results do not establish performance on real networks. | Observation | **Open** | Phase 24A reports and lab limitations | Already disclosed in the lesson/lab; retain the limitation |
| D-13 | Four notebook warnings: PyTorch nested-tensor prototype, Agg canvas, tqdm/ipywidgets, unauthenticated HF Hub request. No failed cells. | Low | **Open** | Notebook regression JSON/log | Optional environment polish; not release blockers |
| D-14 | The course uses bundled/synthetic data in several modules; M11 requires internet on first model use. | Observation | **Open** | M11 README; notebook HF warning | README now discloses; keep the offline alternatives |
| D-15 | Tests cover 36.3% of M13+M14 code; generation scripts, demo mains, optional model paths and error branches are untested. | Observation | **Open** | Coverage report: 722/1,989 statements | Acceptable for a teaching repository; expand only where a concrete regression risk exists |

## Corrected-file list

| File | Change |
| :--- | :--- |
| `modules/M08-natural-language-processing/lessons/L08-06-sequence-models-attention-and-transformers.md` | Corrected softmax weights and wording |
| `modules/M11-generative-ai-and-large-language-models/README.md` | Corrected stale M08 prerequisite statement |
| `README.md` | Corrected notebook runtime and internet/download FAQ claims |
| `modules/M14-advanced-ai-applications-and-capstone/labs/lab-14-01-multimodal-and-graph-systems.md` | Corrected graph runtime estimate |

## Previously reported defects

No previously reported defect was hidden or downgraded. Phase 23/24 corrections remain present:
the M05 CPT normalisation, graph leakage controls, licensing files, reports, tests and hour
reconciliation. The Phase 24 figure of 34% M13/M14 coverage is superseded by the measured 36.3%
after the graph-code/test growth; this is reported, not silently replaced.

## Residual risk statement

The remaining risks are documentation/benchmarking and owner-review items, not invalidated course
content. No critical or open High defect was found. The academic and release verdicts can therefore
be positive with warnings, subject to owner approvals.
