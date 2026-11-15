# Phase 23C — Licensing Implementation and Repository Compliance

**Date:** 13 November 2026
**Scope:** Implement the owner-approved licensing architecture and validate it without
committing, publishing or altering Git history.
**Verdict:** **PASS WITH WARNINGS — IMPLEMENTED, OWNER REVIEW REQUIRED**

The warnings are legal-review items, not implementation failures: authorship is inferred from
repository history, and two upstream licence details could not be re-confirmed during this
phase. Nothing here constitutes legal clearance.

---

## 1. Implemented licence architecture

| Material | Licence | Operative document |
| --- | --- | --- |
| Original source code (Python, notebook code cells, tests, audit tooling) | MIT | `LICENSE` |
| Original educational content (lessons, labs, assignments, projects, quizzes, documentation, notebook prose) | CC BY 4.0 | `CONTENT-LICENSE.md` |
| Original synthetic datasets and generated samples | CC0 1.0 | `DATASET-LICENSE.md` |
| Third-party code, datasets, model weights, papers, quotations | Their own terms — not relicensed | `THIRD-PARTY-ATTRIBUTIONS.md` |

Copyright holder: **Muhammad Nadeem Majeed** (2026). No blanket repository-wide licence is
claimed anywhere; `README.md` states explicitly that there is no single repository-wide licence.

## 2. Files created

| File | Contents |
| --- | --- |
| `LICENSE` | Canonical MIT text, `Copyright (c) 2026 Muhammad Nadeem Majeed` |
| `CONTENT-LICENSE.md` | CC BY 4.0 deed/legal-code URLs, covered and excluded material, attribution format, modification notice, notebook mixed-content rule |
| `DATASET-LICENSE.md` | CC0 1.0 dedication, 11-row synthetic dataset catalogue with generator, method, reproduction command, external exclusions, integrity notes |
| `THIRD-PARTY-ATTRIBUTIONS.md` | Dependency table (14 packages), external dataset table (4), model table (6), bibliography policy, diagram/image finding, redistributor obligations, owner-review list |
| `LICENSING-INVENTORY.md` | Ten-category inventory with patterns, ownership, licence, attribution, evidence, uncertainty; mixed-content rules; limits of the audit |
| `audit/check_licensing.py` | Deterministic checker, ten check groups, non-zero exit on failure, explicit legal-review disclaimer |
| `PHASE-23C-LICENSING-IMPLEMENTATION-REPORT.md` | This report |

## 3. Files modified

| File | Change |
| --- | --- |
| `README.md` | Added TOC entry and §21 “Licence” with the three grants plus third-party exclusion |
| `docs/faq.md` | Replaced “permission is required” answer with the split-licence answer and links |
| `docs/index.md` | New “Licensing and reuse” table linking all licence documents and `CITATION.cff` |
| `CITATION.cff` | Added `license: MIT`; no DOI, ORCID, version, date or venue invented |
| `LICENSE-AND-ATTRIBUTION-PROPOSAL.md` | Marked superseded, points to operative documents, records the `distilgpt2` correction |
| `modules/M04-…/labs/lab-04-01`, `lab-04-02`, `lab-04-03` | Replaced “no licence obligation/applies” with CC BY 4.0 text + CC0 data |
| `modules/M07-…/labs/lab-07-01`, `lab-07-02` | Replaced “no licence” with CC0 1.0 for the synthetic dataset |
| `modules/M09-…/labs/lab-09-02`, `README.md`, `code/vision_core.py` | Replaced “no licence attaches” with CC0 1.0, third-party obligation clarified |
| `modules/M06-…/code/datasets.py` | “no licence questions” → “no third-party licensing questions” |
| `modules/M13-…/code/governance.py` | Model card licence `CC0-1.0 (code), synthetic data` → `MIT (code), CC0-1.0 (synthetic data)` |

No notebook, test, workflow, remote or published site was modified. No third-party licence text
was overwritten.

## 4. Category treatment

| Category | Count / pattern | Treatment |
| --- | --- | --- |
| Original code | 93 `.py` + notebook code cells | MIT |
| Original content | 385 `.md`; 89 lessons, 38 labs, 5 assignments, 8 projects, 14 quizzes + solutions, capstone | CC BY 4.0 |
| Synthetic data | 2 committed `.npz`, 11 generator families | CC0 1.0 |
| Third-party code | 0 vendored files; 14 runtime dependencies | Upstream licences |
| Third-party teaching material | Citations and short quotations only | Not relicensed |
| External images/figures | 0 image files | Not applicable |
| External datasets | UCI digits, Fashion-MNIST, Iris, Gymnasium envs — none committed | Upstream terms |
| Dependencies/models | 14 packages, 6 model checkpoints | Upstream terms |
| Bibliography | 95 entries | Citation only |
| Generated outputs | notebook outputs, `.npz`, audit JSON | CC0 data / CC BY prose / MIT code |

## 5. Third-party findings

- **No third-party asset is redistributed**: no images, no dataset rows, no model weights, no
  copied code, no paper PDFs.
- Dependency licences were read from installed package metadata: BSD-3-Clause (NumPy, SciPy,
  pandas, PyTorch, scikit-learn, nbclient, nbformat), MIT (Gymnasium, pytest, PyYAML),
  Apache-2.0 (transformers, sentence-transformers, `datasets`), PSF-based (matplotlib),
  MPL-2.0 AND MIT (tqdm).
- Model licences were read from the Hugging Face API: `distilgpt2` **Apache-2.0**, `gpt2` MIT,
  `t5-small` Apache-2.0, `distilbert-base-uncased` Apache-2.0,
  `all-MiniLM-L6-v2` Apache-2.0.
- **Correction:** the Phase 23A proposal listed `distilgpt2` as MIT. It is Apache-2.0; the
  proposal is annotated and the register states the correct licence.
- `google/flan-t5-small` lookup timed out; it is recorded as Apache-2.0 (T5 family) and flagged.
- UCI digits and Iris are treated as CC BY 4.0 per UCI terms; the licence page was not re-fetched.
  No UCI rows are redistributed, so repository exposure is limited to the citations.

## 6. Validation commands and results

| Command | Result |
| --- | --- |
| `python audit/check_licensing.py` | **0 failures** across required files, MIT text, CC URLs, README/FAQ consistency, dataset catalogue, third-party fields, ten-category inventory, CFF syntax, link resolution, contradiction scan |
| `python -m pytest tests/ -q` | **138 passed** in 16.10 s |
| `python -m compileall -q modules prerequisites assessments tests audit` | exit **0** |
| `python audit/check_course.py` | **4,151 links, 0 broken**; 89 lessons; 38 labs; `CITATION.cff` parsed, keys=10; **TOTAL PROBLEMS 0** |
| YAML/CFF validation | `license: MIT`, author `Majeed`, repository URL exact, no `doi`/`orcid`/`version`/`date-released`/`identifiers` |
| Dataset inventory | 2 `.npz` files listed; 3 dataset cards all `CC0-1.0` |
| Image asset scan | 0 `.png`/`.jpg`/`.svg`/`.gif` |
| Contradiction scan | 0 remaining “no licence applies” / “permission is required” statements in course files |

The licensing checker is mechanical: it proves the documents agree with each other and with
the repository layout, not that the author owns every file or that third-party reuse is
permitted.

## 7. Git status

| Point | Porcelain lines | Modified | Untracked | Staged |
| --- | --- | --- | --- | --- |
| Before Phase 23C | 140 | 95 | 45 | 0 |
| After Phase 23C | 151 | 99 | 52 | 0 |

- HEAD unchanged: `fba4161 final QA complete`.
- Remote unchanged: `https://github.com/nadeem-majeedch/Artificial-Intelligence-Course.git`.
- `git diff --cached --name-only` → empty. No commit, push, tag, release, workflow or deployment.
- The increased modified count is the four tracked documentation edits (README, FAQ, docs index,
  M09 README); lab and code edits are in files already untracked from earlier phases.
- Seven new untracked files: the five licence documents, `audit/check_licensing.py` and this report.

## 8. Pending owner review

1. **Legal review** — authorship is inferred from a single-author history; no CLA, IP assignment
   or chain-of-title record exists. Counsel should confirm the MIT/CC BY/CC0 split.
2. **`google/flan-t5-small`** — confirm Apache-2.0 on the live model card (API timed out).
3. **UCI digits and Iris** — confirm current UCI licence terms if the course ever bundles rows
   (it does not today).
4. **Quotation audit** — no exhaustive quotation-length review was performed; sampled lessons
   showed attributed citation practice only.
5. **Model outputs** — spot checks found no long verbatim pretrained-model generations in
   notebooks; a full provenance pass was not attempted.
6. **Dependency drift** — no lockfile; a future dependency release could change the licence
   surface and would require re-running the checker and updating the register.
7. **Commit and publication** — deliberately left to the owner, as instructed.

## 9. Limitations

- CC BY 4.0 and CC0 1.0 are referenced by canonical URL with scope and attribution guidance,
  not by embedding the full legal code. MIT is embedded in full because the licence requires
  the notice to travel with the software.
- The checker scans Markdown and module Python for contradictions; it does not parse notebook
  JSON prose, so a stale licence sentence inside a notebook markdown cell would not be caught.
  No notebook was modified in this phase.
- Dataset classification relies on generator code and cards, not on data-provenance tooling.
- This report is a technical record, not a legal opinion, and claims no legal clearance.
