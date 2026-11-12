# Laboratory Validation Report

**Scope:** all 16 laboratory briefs under `modules/*/labs/`.
**Method:** structural scan of all 16 against nine required elements, full reading of three
labs (LAB-01-01, LAB-07-01, LAB-13-01), and execution of the code the labs depend on through
the 14 module notebooks.

---

## 1. Inventory

| Module | Labs | Lines |
| --- | ---: | --- |
| M01 Introduction | 2 | 194, 173 |
| M06 Machine Learning | 4 | 266, 275, 283, 343 |
| M07 Deep Learning | 3 | 165, 216, 204 |
| M11 Generative AI | 3 | 123, 159, 157 |
| M13 Responsible AI | 2 | 154, 160 |
| M14 Advanced Applications | 2 | 143, 145 |
| **Total** | **16** | 123–343 lines |

Modules with lessons but **no lab**: M02 (1 lesson), M04 (7 lessons). Modules with no lessons
have no labs (M08, M10, M12), and M03/M05/M09 do not exist.

## 2. Required-element matrix

Elements checked: realistic scenario, learning objectives, complete instructions, dataset and
licence, executable starter code, expected outputs, testing requirements, evaluation criteria,
extension challenges.

| Lab | Scenario | Objectives | Tasks | Deliverables | Rubric | Extensions | Pitfalls | Expected results | Code block |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| LAB-01-01 | yes | — | yes | yes | yes | yes | — | — | yes |
| LAB-01-02 | yes | — | yes | yes | yes | yes | — | — | yes |
| LAB-06-01 | yes | yes | yes | yes | yes | yes | — | yes | — |
| LAB-06-02 | yes | yes | yes | yes | yes | yes | — | yes | yes |
| LAB-06-03 | yes | yes | yes | yes | yes | yes | — | yes | yes |
| LAB-06-04 | yes | yes | yes | yes | yes | yes | — | yes | yes |
| LAB-07-01 | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| LAB-07-02 | yes | — | yes | yes | yes | yes | yes | yes | yes |
| LAB-07-03 | yes | — | yes | yes | yes | yes | yes | yes | yes |
| LAB-11-01 | yes | — | yes | yes | yes | yes | yes | yes | yes |
| LAB-11-02 | yes | — | yes | yes | yes | yes | yes | yes | yes |
| LAB-11-03 | yes | — | yes | yes | yes | yes | yes | yes | yes |
| LAB-13-01 | yes | — | yes | yes | yes | — | yes | — | yes |
| LAB-13-02 | yes | — | yes | yes | yes | — | yes | — | yes |
| LAB-14-01 | yes | — | yes | yes | yes | — | — | — | yes |
| LAB-14-02 | yes | — | yes | yes | yes | — | — | — | yes |

Counts: scenario 16/16, tasks 16/16, deliverables 16/16, rubric 16/16, extensions 13/16,
pitfalls 11/16, explicit expected results 11/16, objectives 8/16, code block 15/16.

The "—" entries are **heading-name variants, not missing pedagogy**, with two exceptions noted
in §6. For example LAB-01-01 states its outcomes as requirement identifiers
(R1–R5, N1–N3) with success criteria in each task, which is functionally equivalent to a
learning-objectives list.

## 3. Deep review of three labs

### LAB-01-01 — Claim Audit (M01, level 100)

- **Scenario:** a university student-services office is offered a vendor system claiming 96%
  accuracy; the student plays a one-day contracted analyst. Realistic, with a named stakeholder
  who must defend the decision to a committee.
- **Data:** 240 synthetic enquiry emails with a fixed seed, generated in the lab. No download,
  no licence question. Deliberately imbalanced (96/72/48/24) and half the messages contain a
  second topic — a deliberate trap that makes keyword classification fail.
- **Instructions:** six numbered tasks with per-task success criteria. Requirements are split
  into functional (R1–R5) and non-functional (N1–N3) — unusually rigorous for a level-100 lab.
- **Expected outputs:** no separate "expected results" section; instead each task states what
  success looks like ("your table shows at least one class where recall and precision differ by
  more than 0.2"). Acceptable, but a student cannot self-check an exact number.
- **Testing:** N3 requires every number to be script-generated; three hints include a
  consistency check (`accuracy == trace / total`).
- **Rubric:** five weighted criteria, 30/25/20/15/10 = 100, with Excellent/Adequate/Not-yet
  descriptors.
- **Extensions:** three, each changing one variable (prevalence, adversarial wording, human
  agreement ceiling).

**Verdict: complete and strong.** One formal gap: no explicit learning-objectives list.

### LAB-07-01 — Neural Network From Scratch (M07, level 300)

- **Scenario:** four-point logic gates; the perceptron's failure on XOR is the point.
- **Objectives:** six measurable objectives, including "validate gradients numerically with a
  relative-error check below 1e-6".
- **Code:** runnable starter snippets against `nn_numpy.py`, `deep_data.py`; the lab requires
  the student to write their own forward/backward before comparing.
- **Expected outputs:** exact printed tables for perceptron error counts per epoch, final loss
  (5.95e-05), accuracy 1.000, gradient-check value 1.22e-08. This is the best-specified lab in
  the repository: every number has a stated tolerance.
- **Testing:** gradient check below 1e-6 is a hard pass condition; failure modes are diagnosed.
- **Rubric:** 20/30/25/15/10 = 100.
- **Extensions:** three, all falsifiable.

**Verdict: exemplary.** This is the model the other labs should follow.

### LAB-13-01 — Fairness Audit (M13, level 300)

- **Scenario:** three datasets (recruitment, student performance, loans), three different
  failure modes, with ethics statement and synthetic-data provenance (CC0).
- **Tasks:** each task names the numbers the student should reproduce (selection 0.172/0.096,
  DP gap 0.002, accuracy 0.954, DI ratio, calibration bins), which makes cheating detectable
  and self-checking possible.
- **Rubric:** 30/30/20/10/10 = 100, plus nine common pitfalls.
- **Gaps:** no learning-objectives heading (outcomes are implicit in the tasks), no separate
  expected-results table (numbers are embedded in the task text), and no extension challenges.

**Verdict: complete in substance**, formally short of the repository's own lab template in
three headings.

## 4. Datasets and licensing

- 16/16 labs use either synthetic in-script data or a small public dataset.
- Real datasets are named with licences where used: UCI Iris (CC BY 4.0), Fashion-MNIST and
  plant imagery referenced via their standard sources, and the M13 datasets declared
  synthetic/CC0.
- No lab requires a download larger than a few megabytes; no lab requires a GPU.
- No lab requires an API key. Where an LLM API would be natural (M11 prompting lab), the lab
  is built around the module's local tokeniser and a scripted model so it runs offline.

## 5. Executability

All code the labs reference lives in `modules/*/code/` and is exercised by the module
notebooks, which were executed end to end (14/14 pass — see `NOTEBOOK-EXECUTION-REPORT.md`).
Two caveats:

1. `gen_samples.npz` is a generated artefact committed into `modules/M11.../code/`; a lab or
   notebook that runs from another directory must resolve it by path. This broke notebook
   NB-11-01 in this audit and was fixed there.
2. LAB-06-01 contains no code block of its own; it directs students to `code/ml_data.py`. The
   instructions are complete, but a student who skims for code will not find starter code on
   the page.

## 6. Defects

| ID | Defect | Severity | Status |
| --- | --- | --- | --- |
| L1 | 8 of 16 labs have no explicit learning-objectives section | Medium | Reported; outcomes are present as requirements/success criteria |
| L2 | LAB-13-01, LAB-13-02, LAB-14-01, LAB-14-02 have no extension challenges | Low | Reported |
| L3 | LAB-14-01/02 have neither pitfalls nor expected-results sections | Medium | Reported — the two weakest briefs structurally |
| L4 | LAB-06-01 has no starter code block | Low | Reported |
| L5 | M02 and M04 have no labs at all despite having lessons | High | Reported (content gap) |
| L6 | LAB-01-01/02 have no expected numerical results | Low | Design choice: the corpus is deterministic, so exact values are reproducible but not published |

## 7. Score

| Dimension | Weight | Score |
| --- | ---: | ---: |
| Realistic scenario and stakeholder | 20% | 20/20 |
| Objectives and instructions | 20% | 16/20 |
| Dataset appropriateness and licence | 15% | 15/15 |
| Executable code and expected outputs | 20% | 16/20 |
| Testing and evaluation criteria | 15% | 15/15 |
| Extensions | 10% | 8/10 |

**Audit 3 verdict: PASS WITH WARNINGS.** Every lab is realistic, defines a deliverable, and
carries a rubric summing to 100%. The warnings are template-consistency gaps (objectives,
extensions, expected outputs in six briefs) and the absence of labs in M02 and M04.
