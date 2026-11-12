# Capstone Rubric

Applied to the final report, repository and defence. Ten criteria, 100 points. Read it at M1: most
of the marks are decided by early choices.

| # | Criterion | Weight | What is being judged |
| ---: | :--- | ---: | :--- |
| 1 | Problem understanding | 10 | the decision, the user, and why a model is the right tool |
| 2 | Literature review | 10 | three to five relevant sources, used rather than listed |
| 3 | Data preparation | 12 | provenance, licence, split discipline, leakage awareness |
| 4 | Algorithm selection | 10 | justified choice against a baseline, including a simpler option |
| 5 | Implementation | 13 | working, reproducible code with seeds and a single command |
| 6 | Evaluation | 15 | primary metric, baselines, uncertainty, per-class/subgroup table |
| 7 | Explainability and limitations | 12 | an explanation with a fidelity check; a limitations section that bites |
| 8 | Documentation | 8 | report structure, model card, reproduction instructions |
| 9 | Demonstration | 5 | a five-minute demo that shows the result and one failure |
| 10 | Ethical considerations | 5 | data ethics, affected parties, and the prototype boundary |

## Band descriptors

Use these for each criterion. The difference between bands is evidence, not effort.

### 1. Problem understanding (10)

| Band | Descriptor |
| :--- | :--- |
| 9–10 | names the decision, the person affected, and the counterfactual ("what happens now"); scopes out what is not being solved |
| 6–8 | clear problem, vague beneficiary or missing counterfactual |
| 3–5 | "apply AI to X" with no decision identified |
| 0–2 | no problem statement, or one contradicted by the work |

### 2. Literature review (10)

| Band | Descriptor |
| :--- | :--- |
| 9–10 | sources are used: each one changes a design choice, and disagreements between them are noted |
| 6–8 | relevant sources, summarised but not applied |
| 3–5 | a list of papers with no connection to the method |
| 0–2 | absent, or cites work that does not exist |

### 3. Data preparation (12)

| Band | Descriptor |
| :--- | :--- |
| 11–12 | provenance and licence stated; split matches deployment; leakage explicitly checked; known gaps documented |
| 8–10 | clean pipeline, licence stated, split justified but not tested for leakage |
| 5–7 | pipeline works, provenance thin, random split for a time-dependent task |
| 0–4 | data of unknown origin, or the test set influenced training |

### 4. Algorithm selection (10)

| Band | Descriptor |
| :--- | :--- |
| 9–10 | baseline first, then a justified step up; a simpler alternative is discussed and rejected with a reason |
| 6–8 | sound choice, weak justification, baseline present |
| 3–5 | the fashionable model, no baseline |
| 0–2 | no rationale, or a model that cannot work on this data |

### 5. Implementation (13)

| Band | Descriptor |
| :--- | :--- |
| 12–13 | one command reproduces every number; seeds fixed; environment pinned; code readable |
| 9–11 | runs, mostly reproducible, minor manual steps |
| 5–8 | runs on the author's machine with undocumented steps |
| 0–4 | does not run, or results cannot be regenerated |

### 6. Evaluation (15)

| Band | Descriptor |
| :--- | :--- |
| 14–15 | primary metric tied to the decision; two baselines; uncertainty reported; per-class or subgroup table; error analysis of concrete failures |
| 10–13 | solid metrics and a baseline; uncertainty or subgroup analysis missing |
| 6–9 | one accuracy number on one split |
| 0–3 | no held-out evaluation, or test data used for tuning |

### 7. Explainability and limitations (12)

| Band | Descriptor |
| :--- | :--- |
| 11–12 | an explanation used for a real decision, with a fidelity or stability check; limitations stated in the abstract and each one traceable to a measurement |
| 8–10 | explanation present but unevaluated; limitations generic ("data may be biased") |
| 5–7 | a saliency plot with no interpretation; limitations in name only |
| 0–4 | claims beyond the evidence, including production-readiness for a high-stakes use |

### 8. Documentation (8)

| Band | Descriptor |
| :--- | :--- |
| 7–8 | report follows the template; model card complete; reproduction instructions tested by someone else |
| 5–6 | readable report, model card partial |
| 3–4 | unstructured notes |
| 0–2 | no documentation beyond code comments |

### 9. Demonstration (5)

| Band | Descriptor |
| :--- | :--- |
| 5 | five minutes, live, shows the main result and one failure, answers "what would break this?" |
| 3–4 | works, but only the happy path |
| 1–2 | slides of code |
| 0 | no demo |

### 10. Ethical considerations (5)

| Band | Descriptor |
| :--- | :--- |
| 5 | data ethics and affected parties named; prototype boundary stated explicitly; licence respected |
| 3–4 | generic ethics paragraph |
| 1–2 | one sentence, or only "we used public data" |
| 0 | absent, or claims that would require validation the project does not have |

## Automatic deductions

- **Unreproducible numbers** (−10): a reported metric that no command in the repository produces.
- **Test-set contamination** (−15): tuning on the test split, or leakage through preprocessing.
- **Overclaiming high-stakes reliability** (−10): clinical, financial, legal or safety claims
  without appropriate validation.
- **Missing licence statement** (−5): data of unclear provenance used or redistributed.
- **No baseline** (−8): a result with nothing to compare against.

Deductions are applied after the criteria and are not offset by strength elsewhere. They exist
because these are the failures that matter outside a classroom.

## Score bands

| Total | Band |
| ---: | :--- |
| 85–100 | distinction: publishable as a technical report with minor edits |
| 70–84 | strong pass: complete evidence, some gaps in analysis |
| 55–69 | pass: works, evaluation or limitations thin |
| 40–54 | marginal: a demo rather than a study |
| below 40 | fail: claims not supported by evidence |

## Self-assessment

Before submitting, score yourself on all ten criteria and write one sentence of evidence for each
score. If you cannot produce evidence for a claim, the claim is not ready.

| Criterion | Self-score | Evidence (file, number, line) |
| :--- | ---: | :--- |
| 1 Problem | | |
| 2 Literature | | |
| 3 Data | | |
| 4 Algorithm | | |
| 5 Implementation | | |
| 6 Evaluation | | |
| 7 Explainability | | |
| 8 Documentation | | |
| 9 Demonstration | | |
| 10 Ethics | | |

---

[Capstone home](README.md) · [Milestones](milestones.md) · [Report template](report-template.md)
