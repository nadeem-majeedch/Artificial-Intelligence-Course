# Course Completeness Report

**Repository:** Artificial Intelligence — A Complete Course for Self-Study
**Audit date:** 11 November 2026
**Auditor role:** independent academic auditor (curriculum completeness)
**Method:** direct inspection of every module directory, lesson file, lab, notebook and
assessment; no reliance on prior implementation claims.

---

## 1. What the course claims to be

The root `README.md` describes **fourteen modules** progressing from foundations through
classical AI, machine learning, deep learning, applied AI, responsibility, and a capstone.
`docs/CURRICULUM-MAP.md` and `docs/course-roadmap.md` name the same fourteen modules and
associate lessons `L01-01 … L14-05` with them.

## 2. What actually exists

| # | Module | Directory | Lessons | Labs | Notebooks | Verdict |
| --- | --- | --- | ---: | ---: | ---: | --- |
| M01 | Introduction and Foundations | yes | 5 | 2 | 1 | Complete |
| M02 | Intelligent Agents and Environments | yes | **1 of 5** | 0 | 0 | Incomplete |
| M03 | Problem Solving and Search | **absent** | 0 | 0 | 0 | Missing |
| M04 | Knowledge Representation and Reasoning | yes | 7 | **0** | 2 | Lessons only |
| M05 | Reasoning Under Uncertainty | **absent** | 0 | 0 | 0 | Missing |
| M06 | Machine Learning Fundamentals | yes | 10 | 4 | 4 | Complete |
| M07 | Neural Networks and Deep Learning | yes | 8 | 3 | 3 | Complete |
| M08 | Natural Language Processing | yes (code only) | **0** | 0 | 0 | Code only |
| M09 | Computer Vision | **absent** | 0 | 0 | 0 | Missing |
| M10 | Reinforcement Learning | yes (code only) | **0** | 0 | 0 | Code only |
| M11 | Generative AI and Large Language Models | yes | 7 | 3 | 2 | Complete |
| M12 | AI Agents and Agentic Systems | yes (code only) | **0** | 0 | 0 | Code only |
| M13 | Responsible, Explainable and Secure AI | yes | 6 | 2 | 1 | Complete |
| M14 | Advanced Applications and Capstone | yes | 5 | 2 | 1 | Complete |

Totals measured on disk: **11 module directories of 14**, **49 lessons**, **16 labs**,
**14 notebooks**, **69 assessment documents**, **275 Markdown files**.

### 2.1 Modules that do not exist at all

`M03` (search), `M05` (uncertainty) and `M09` (computer vision) have **no directory and no
lesson, lab or notebook**, yet:

- `modules/README.md` contains placeholder sections with anchors `#m03`, `#m05`, `#m09` and the
  text "Content status: in preparation".
- Fourteen quizzes exist, including `assessments/quizzes/quiz-m03.md`,
  `quiz-m05.md` and `quiz-m09.md`, which state "Covers L03-01 … L03-07" and similar.
- 61 files reference these module numbers, including `docs/CURRICULUM-MAP.md` (30 mentions),
  `resources/glossary.md` (26) and `README.md` (21).

This is the single largest completeness defect: three of the fourteen advertised modules have
no teaching content, and assessments exist for content that does not.

### 2.2 Modules advertised with lessons that have none

`M08`, `M10` and `M12` each have a directory, reference code and a status page, but **zero
lessons, zero labs and zero notebooks**. Their module pages are explicit about this
("reference code … is published; lessons, notebooks and labs are not yet written"), which is
honest but does not make them complete. A student cannot learn NLP, reinforcement learning or
agentic systems from this repository today.

### 2.3 Modules that are partial

- **M02** has 1 of the 5 lessons listed in its own module map, no lab, no notebook, but a
  12-question quiz and a programming assignment. The single lesson is well formed; the module
  is not.
- **M04** has 7 lessons and 2 notebooks but **no labs, no assignment implementation guidance
  beyond the brief**, and no practical artefact that applies the logic engine to a scenario.
  The module page is described as newly created; its study plan still points to material that
  is thin at the practical end.

## 3. Topic coverage and progression

### 3.1 Covered well

- **Foundations (M01):** definitions, history and AI winters, symbolic/statistical/generative
  distinction, capability limits, and study workflow. Claims are treated critically (the
  capability audit lab requires a baseline before believing an accuracy figure).
- **Machine learning (M06):** the ten lessons form a coherent arc — what learning is, leakage
  and cross-validation, linear regression from first principles, logistic regression,
  evaluation and ROC, bias–variance and regularisation, k-NN and naive Bayes, trees/forests/
  boosting/SVM, unsupervised learning and dimensionality reduction, reproducible pipelines.
  This is the strongest module in the course.
- **Deep learning (M07):** perceptron → MLP → backpropagation → PyTorch → sequences and
  attention → transfer learning, with a from-scratch NumPy lab that gradient-checks its own
  implementation.
- **Generative AI (M11):** tokenisation, attention, VAEs/GANs/diffusion, prompting, retrieval,
  evaluation, fine-tuning.
- **Responsibility (M13):** fairness metrics, explainability, privacy, adversarial security,
  governance, auditing. Unusually for a course at this level, the fairness lesson deliberately
  shows a mitigation that does nothing, which is pedagogically valuable.
- **Capstone (M14):** case studies, MLOps, monitoring and drift, reading research, capstone
  studio.

### 3.2 Missing foundational and advanced topics

Because M03, M05 and M09 are absent, the following topics named in the course roadmap have no
teaching content anywhere in the repository:

| Topic | Normally belongs to | Present? |
| --- | --- | --- |
| Uninformed and informed search (BFS, DFS, A*, heuristics, admissibility) | M03 | No |
| Constraint satisfaction, local search, adversarial search | M03 | No |
| Probability, Bayes' rule, Bayesian networks, HMMs | M05 | No |
| Convolutional networks, image classification pipelines, detection/segmentation | M09 | No |
| Text processing pipelines as taught content | M08 | Code only |
| MDPs, dynamic programming, Q-learning, policy gradients | M10 | Code only |
| Agent loops, tool use, multi-agent orchestration | M11/M12 | Code only |

Consequences for progression:

- **A\* search is absent** while M03-dependent references remain in `resources/glossary.md`
  and the roadmap. A student following the roadmap meets a module that does not exist.
- **Probability is absent** before M06's evaluation lessons and M11's sampling lessons. Those
  lessons compensate with inline explanation, but the prerequisite named by the curriculum is
  not delivered.
- **Computer vision** appears only as a PyTorch image-classification notebook inside M07 and an
  M14 lab; convolution is explained in M07, so the deep-learning path is not broken, but the
  dedicated vision module is.
- The **capstone** depends on modules that are absent (for example an NLP or RL capstone
  pathway), which narrows the capstone to the seven modules that are complete.

### 3.3 Prerequisite structure

Prerequisites are declared in every lesson header and every module page, and the declared
prerequisites that do exist are satisfied by earlier modules. Two structural problems:

1. `README.md` and `docs/learning-path.md` still describe a fourteen-module sequence, so a
   reader is routed through modules with no content.
2. M04's lessons declare M01/M02 prerequisites; M02 is 20% complete, so a student who obeys the
   prerequisite rule is blocked before M04 even though M04's own content is self-contained.

### 3.4 Beginner-to-advanced progression

Within the seven complete modules the progression is correct: level 100 material in M01,
200–300 in M06/M07/M11, 300 in M13/M14, with difficulty labels on every lesson, lab and
assessment. Across the course as a whole the progression is interrupted by the six modules
that are missing or code-only, which removes the classical-AI stage almost entirely.

## 4. Specific completeness defects found

| ID | Defect | Severity | Remediated in this audit |
| --- | --- | --- | --- |
| C1 | M03, M05, M09 have no content; quizzes and roadmap references remain | Critical | No (content authoring out of scope); quizzes now carry an availability notice |
| C2 | M08, M10, M12 have code but no lessons | High | No |
| C3 | M02 has 1 of 5 lessons | High | No |
| C4 | M04 has no lab or practical assessment | Medium | No |
| C5 | Fourteen quizzes exist for fourteen modules, three of which cannot be attempted | Medium | Yes — availability notice added to quiz-m03/m05/m09 and their keys |
| C6 | `modules/README.md` mixed anchors (`#m03`) and "in preparation" sections imply presence | Low | No (labels are accurate; only the anchors are structural) |

## 5. Completeness score

| Dimension | Weight | Score | Basis |
| --- | ---: | ---: | --- |
| Module presence (14 of 14) | 30% | 11/14 | 8 with lessons, 3 code-only, 3 absent |
| Lesson coverage of advertised topics | 25% | ~55% | 49 lessons; search, uncertainty and vision absent |
| Practice coverage (labs/notebooks) | 20% | 13/14 modules with any practice; 8/14 with lessons | M02/M04 gaps |
| Assessment coverage | 15% | 14/14 papers, 8/14 answerable | three papers unanswerable |
| Progression and prerequisites | 10% | coherent within complete modules, broken globally | see §3.3 |

**Audit 1 verdict: FAIL.** The course is not complete. Seven of fourteen modules are fully
taught; six are missing or code-only, and one is one fifth written. The material that exists is
of high quality, but a student cannot complete the advertised curriculum, and "do not mark a
topic complete because a directory or heading exists" applies directly to M08, M10 and M12,
whose directories exist without lessons.
