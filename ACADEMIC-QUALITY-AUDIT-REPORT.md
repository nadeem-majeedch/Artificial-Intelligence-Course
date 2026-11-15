# Academic Quality Audit Report — Phase 23

**Reviewer role:** independent university-level AI curriculum reviewer.
**Scope:** all 14 modules, 89 lessons, 38 laboratories, 8 mini-projects, 14 quizzes with keys, 14
programming assignments, 8 analytical assignments, 35 notebooks.
**Method:** structural measurement of every file (not sampling of counts), close reading of a stratified
sample of lessons and labs, and independent re-derivation of every quantitative claim listed in
`MATHEMATICAL-VERIFICATION-REPORT.md`. Reports from earlier phases were treated as claims, not evidence.

## 1. What the repository actually contains

Measured by script over the working tree, not taken from the README:

| Module | Lessons | Labs | Notebooks | Project | Quiz | Assignment |
| :--- | ---: | ---: | ---: | :--- | :--- | :--- |
| M01 Foundations | 5 | 2 | 1 | MP-01 | ✓ | PA-01 |
| M02 Intelligent Agents | 5 | 2 | 1 | — | ✓ | PA-03 |
| M03 Search | 7 | 2 | 1 | — | ✓ | PA-02 |
| M04 Knowledge Representation | 7 | 3 | 2 | PROJECT-04-01 | ✓ | PA-04 |
| M05 Uncertainty | 6 | 2 | 2 | — | ✓ | PA-05 |
| M06 Machine Learning | 10 | 4 | 4 | MP-06 | ✓ | PA-06 |
| M07 Deep Learning | 8 | 3 | 3 | MP-07 | ✓ | PA-07 |
| M08 NLP | 6 | 3 | 3 | — | ✓ | PA-08 |
| M09 Computer Vision | 6 | 4 | 4 | — | ✓ | PA-09 |
| M10 Reinforcement Learning | 5 | 4 | 3 | MP-10 | ✓ | PA-10 |
| M11 Generative AI and LLMs | 7 | 3 | 2 | MP-11 | ✓ | PA-11 |
| M12 Agentic AI | 6 | 2 | 1 | MP-12 | ✓ | PA-13 |
| M13 Responsible and Secure AI | 6 | 2 | 1 | MP-13 | ✓ | PA-14 |
| M14 Advanced Applications and Capstone | 5 | 2 | 1 | — (capstone in page) | ✓ | — |
| **Total** | **89** | **38** | **35** | **8** | **14** | **14** |

Lesson body length: median 1,957 words, range 816–3,395. Python blocks per lesson: 0–10. No lesson pair
shares more than 10% of its six-word shingles, so there is **no detectable duplication between lessons** —
the modules cover different material rather than restating one template.

## 2. Curriculum completeness

**Coverage is genuine, not nominal.** Every named area of a standard undergraduate AI sequence is present
with worked material: agents and environments (M02), uninformed/informed/local search, CSP and game search
(M03), propositional and first-order logic with resolution and unification, plus a rule engine (M04),
Bayesian networks, variable elimination and fuzzy inference (M05), supervised/unsupervised learning with
honest evaluation (M06), backpropagation, CNNs, sequence models and attention (M07), tokenisation through
transformer fine-tuning (M08), classical vision, detection and segmentation (M09), MDPs, DP, TD control,
DQN, policy gradients and PPO (M10), tokenisation, VAEs, GANs, diffusion, LoRA, RAG and evaluation (M11),
agent loops, tools, multi-agent coordination and safety limits (M12), fairness, explainability, privacy,
adversarial security and governance (M13), and deployment, monitoring, research reproduction and a capstone
(M14).

Three findings qualify that coverage:

1. **M01 has a mini-project but no lab pair of its own kind**; its two labs are audits of claims and a
   Turing-test conversation. That is appropriate for an orientation module, but a student expecting to
   write code in week one gets it in M02 instead. The module page says so.
2. **M02's assignment is PA-03 and M03's is PA-02** (the numbering follows the syllabus, not the module
   order). At the start of this audit only five module pages (M03, M04, M09, M10 and M02 after a fix)
   linked their assignment at all; the other nine did not, so a student could not reach the assessed work
   from the module page. **Fixed in this audit**: every module except M14 now links its programming
   assignment. The numbering inconsistency remains, and is documented in `assessments/README.md`.
3. **M14 has no assessment file of its own.** Its assessment is the capstone, described in the module
   page and the capstone starter notebook. That is defensible for a capstone, and it is stated.

## 3. Progression and prerequisites

The prerequisite graph declared in `modules/README.md` is acyclic and matches the material:

`M01 → M02 → M03 → M04 → M05 → M06 → M07 → {M08, M09} → M10 (also M05, M06) → M11 → M12 → M13 → M14`.

Checked against lesson content: every module's lessons name the specific earlier lesson they rely on
(for example M10 L10-01 requires M05 probability and M06 evaluation), and the four prerequisite sections
P01–P04 supply the Python, linear algebra, calculus, probability and data-handling background that M06
and M07 assume. Two soft edges remain:

- **M07 assumes calculus fluency** (chain rule, Jacobians) that P02 introduces but does not exercise at
  the depth backpropagation needs. The lesson provides the derivation, so a student can recover, but this
  is the steepest step in the course.
- **M10 assumes discounted-return fluency** that no earlier module drills. L10-01 defines it from scratch,
  so the dependency is declared rather than hidden, but it is new material inside a 400-level module.

No module requires a concept that is never taught anywhere in the repository. That was checked by
searching for undefined forward references in prerequisites sections; none were found.

## 4. Academic level and depth

The course is pitched at final-year undergraduate / taught-master's level. Evidence:

- **Mathematical content is present, not gestured at.** Lessons carry "Mathematical Formulation" sections
  with derivations (backpropagation chain rule, Bellman operators, softmax Jacobian, attention scaling,
  Bayes rule, factor products). `MATHEMATICAL-VERIFICATION-REPORT.md` confirms 32 independent checks.
- **Worked examples use real numbers.** The M09 and M10 numbers were reproduced on this machine; M04's
  posteriors (P(P)=0.10, P(W)=0.2581, P(C|W)=0.4595) match enumeration to 1e-12.
- **Negative results are taught.** M09 shows a HOG baseline matching a CNN on synthetic data and a road
  colour rule scoring mIoU 0.65 with obstacle Dice 0.00. M10 shows SARSA outperforming Q-learning online
  on cliff walking. M06 teaches why 70% accuracy can be worthless. This is a marker of academic honesty
  that most self-study material lacks.
- **Where depth is thinner:** M13 and M14 contain no runnable Python in their lessons (11 of 89 lessons
  have zero code blocks). M13's code lives in `code/fairness.py`, `explain.py`, `security.py` and the
  notebook, so the material is executable, but a student reading only the lesson cannot run the example
  in place. M14 is capstone guidance, where that is expected.

## 5. Descriptive versus educational content

A lesson was counted as descriptive if it had no worked example, no code and no exercise. None met all
three. The weakest pattern found is the opposite: **60 of 89 lessons have no `Exercises` section**. They
do have a `Self-check` block and a `Common mistakes` section, which supports comprehension, but they do
not ask the student to produce anything. Students who need practice must rely on labs, notebooks and the
quiz. This is the single largest pedagogical gap in the repository, and it is a content gap rather than a
defect: the lessons are explanatory and correct, just less demanding than a university course would be.

## 6. Modern AI coverage

Current as of late 2026 in the areas that matter: transformer attention from scratch plus a fine-tuning
path, LoRA and adapter economics, retrieval-augmented generation with evaluation, diffusion models,
agent tool use and multi-agent coordination, prompt injection and adversarial examples, fairness metrics
and governance. The limitations are stated rather than papered over: Hugging Face models are optional
downloads, no frontier model is required, and the LLM material runs on small local models.

## 7. Duplication and inconsistency

- **No duplicated lessons** (similarity < 0.1 between all pairs).
- **Two lab templates coexist**: 11 labs use the numbered 14-section template (M04, M09, M10), 27 use an
  older unnumbered template (`Scenario`, `Your role`, `What you are given`, `Requirements`, `Tasks`,
  `Deliverables`, `Evaluation criteria`, `Extension challenges`, `Hints`, `Reflection`, `Time budget`).
  Both carry the same substance; a reader moving from M02 to M09 sees a different shape. This is a
  presentation inconsistency, documented rather than mass-rewritten because rewriting 27 labs risks
  damaging content that is already good.
- **Two lesson openers coexist**: M01–M12 lessons begin with an "On this page" block; M09 and M13/M14
  begin directly with objectives. Minor, and both are navigable.

## 8. Study-hour claims

Every module page now states hours in the same five-category form, and the sums are consistent with the
central index (verified by script: 14/14 rows match, category sums equal totals). Total published
material is **350.7 hours** across the 14 modules, plus the prerequisite sections.

Two corrections were required during this audit and are recorded in `FINAL-PHASE-23-REPORT.md`:
five project files declare their effort as `| Effort | … |`, which the earlier calculator did not parse,
so M01, M06, M07, M11 and M12 under-counted their projects (and their prose totals contradicted their own
page totals); M13 and M14 prose totals were stale. All are now derived from the files.

## 9. Verdict for this audit

The curriculum is academically coherent, correctly sequenced and substantially deeper than its own
summary suggests. Its weaknesses are pedagogical load (few exercises), presentation consistency (two lab
templates) and the uneven presence of runnable code in M13/M14 — not missing or wrong subject matter.
