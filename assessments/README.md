# Assessment Collection

Independent-study assessments for the fourteen modules: a quiz per module with a separate answer key,
fourteen programming assignments, eight analytical assignments, and a self-assessment sheet per
module. Everything here is designed to be worked without an instructor in the room, which is why the
self-assessment sheets and the answer keys exist.

[Course home](../README.md) · [Curriculum map](../docs/CURRICULUM-MAP.md) · [Modules](../modules/README.md)

## Structure

```text
assessments/
├── README.md              this index
├── quizzes/               14 student-facing quizzes (no answers)
├── solutions/             14 answer keys with explanations
├── programming/           14 programming assignments + index
├── analytical/            8 analytical assignments + index
└── self-assessment/       14 module self-assessment sheets + index
```

## Quizzes

Twenty marks each, 30–40 minutes, mixing multiple choice, true/false with justification, conceptual,
numerical, tracing, Python-output and short-answer questions. Questions are ordered by part so that
the difficulty rises through the paper; the last two questions in each are the ones that separate a
pass from a good pass.

| Module | Quiz | Questions | Solutions |
| :--- | :--- | ---: | :--- |
| M01 Introduction and foundations | [QUIZ-M01](quizzes/quiz-m01.md) | 12 | [key](solutions/quiz-m01.md) |
| M02 Intelligent agents | [QUIZ-M02](quizzes/quiz-m02.md) | 12 | [key](solutions/quiz-m02.md) |
| M03 Search | [QUIZ-M03](quizzes/quiz-m03.md) | 12 | [key](solutions/quiz-m03.md) |
| M04 Knowledge-based systems | [QUIZ-M04](quizzes/quiz-m04.md) | 11 | [key](solutions/quiz-m04.md) |
| M05 Reasoning under uncertainty | [QUIZ-M05](quizzes/quiz-m05.md) | 11 | [key](solutions/quiz-m05.md) |
| M06 Machine learning | [QUIZ-M06](quizzes/quiz-m06.md) | 11 | [key](solutions/quiz-m06.md) |
| M07 Neural networks | [QUIZ-M07](quizzes/quiz-m07.md) | 11 | [key](solutions/quiz-m07.md) |
| M08 NLP | [QUIZ-M08](quizzes/quiz-m08.md) | 10 | [key](solutions/quiz-m08.md) |
| M09 Computer vision | [QUIZ-M09](quizzes/quiz-m09.md) | 10 | [key](solutions/quiz-m09.md) |
| M10 Reinforcement learning | [QUIZ-M10](quizzes/quiz-m10.md) | 10 | [key](solutions/quiz-m10.md) |
| M11 Generative AI and LLMs | [QUIZ-M11](quizzes/quiz-m11.md) | 11 | [key](solutions/quiz-m11.md) |
| M12 AI agents | [QUIZ-M12](quizzes/quiz-m12.md) | 11 | [key](solutions/quiz-m12.md) |
| M13 Responsible and secure AI | [QUIZ-M13](quizzes/quiz-m13.md) | 11 | [key](solutions/quiz-m13.md) |
| M14 Advanced applications | [QUIZ-M14](quizzes/quiz-m14.md) | 11 | [key](solutions/quiz-m14.md) |

## Programming assignments

Fourteen briefs, each with the full twelve-field structure: number, title, difficulty, estimated time,
background, problem scenario, learning outcomes, tasks, constraints, expected deliverables, evaluation
rubric and bonus challenges. The beginner assignment is doable in an afternoon; the advanced ones
assume the module's notebook has been worked through.

| # | Assignment | Difficulty | Time |
| ---: | :--- | :--- | ---: |
| 01 | [Python and NumPy](programming/pa-01-python-and-numpy.md) | Beginner | 3 h |
| 02 | [Search](programming/pa-02-search-algorithms.md) | Intermediate | 4 h |
| 03 | [Intelligent agents](programming/pa-03-intelligent-agents.md) | Intermediate | 4 h |
| 04 | [Knowledge-based systems](programming/pa-04-knowledge-based-systems.md) | Intermediate | 4 h |
| 05 | [Bayesian reasoning](programming/pa-05-bayesian-reasoning.md) | Intermediate | 4 h |
| 06 | [Machine learning](programming/pa-06-machine-learning.md) | Intermediate | 5 h |
| 07 | [Neural networks](programming/pa-07-neural-networks.md) | Advanced | 5 h |
| 08 | [NLP](programming/pa-08-nlp.md) | Advanced | 5 h |
| 09 | [Computer vision](programming/pa-09-computer-vision.md) | Advanced | 5 h |
| 10 | [Reinforcement learning](programming/pa-10-reinforcement-learning.md) | Advanced | 5 h |
| 11 | [Generative AI](programming/pa-11-generative-ai.md) | Advanced | 5 h |
| 12 | [LLM applications](programming/pa-12-llm-applications.md) | Advanced | 5 h |
| 13 | [AI agents](programming/pa-13-ai-agents.md) | Advanced | 5 h |
| 14 | [Explainable and secure AI](programming/pa-14-explainable-and-secure-ai.md) | Advanced | 5 h |

## Analytical assignments

Eight written assignments for the skills that code alone does not teach: comparison under constraints,
complexity accounting, derivation, evaluation critique, error taxonomy, dataset audit, paper review
and architecture review.

| # | Assignment | Focus | Time |
| ---: | :--- | :--- | ---: |
| 01 | [Algorithm comparison](analytical/aa-01-algorithm-comparison.md) | search choice under constraints | 2 h |
| 02 | [Complexity analysis](analytical/aa-02-complexity-analysis.md) | FLOPs and memory accounting | 2 h |
| 03 | [Mathematical derivation](analytical/aa-03-mathematical-derivation.md) | logistic regression gradients | 2 h |
| 04 | [Model evaluation](analytical/aa-04-model-evaluation.md) | critiquing a vendor claim | 2 h |
| 05 | [Error analysis](analytical/aa-05-error-analysis.md) | taxonomy and prioritisation | 2 h |
| 06 | [Dataset bias analysis](analytical/aa-06-dataset-bias-analysis.md) | construct validity and proxies | 2 h |
| 07 | [Research paper analysis](analytical/aa-07-research-paper-analysis.md) | claims, evidence, ablations | 3 h |
| 08 | [System architecture evaluation](analytical/aa-08-system-architecture-evaluation.md) | failure modes and budgets | 3 h |

## Self-assessment

One sheet per module in [self-assessment/](self-assessment/README.md): key-concepts checklist,
knowledge-check questions, practical competency checklist, revision topics, and a readiness test for
the next module. Unmarked, and best done before revising rather than after.

## Solutions policy

**Quizzes.** Full answer keys live in [`solutions/`](solutions/README.md), one file per quiz, numbered
to match. They are not placed under the questions: a student can work a quiz, then open the key, and
still has to check each answer rather than reading past it. Keys give the correct answer, the
reasoning, why the distractors are wrong, and the arithmetic for numerical questions.

**Programming and analytical assignments.** No model solutions are published. These assignments are
judged on process — measurement, error analysis, stated assumptions — and a published solution would
turn them into copying exercises. Each brief carries a weighted rubric naming what a strong
submission contains, and the module notebook is the reference implementation for the techniques.

**Hints.** Where a task is likely to stall, the brief names the obstacle rather than the fix (for
example "check whether the feature is available at prediction time" rather than "drop column X").

## Difficulty and marks

- Quizzes: 20 marks, pass 12. Roughly 40% recall, 40% application, 20% analysis.
- Programming: 100 marks by rubric, pass 60. Beginner ×1, intermediate ×5, advanced ×8.
- Analytical: 100 marks by rubric, pass 60. Intermediate ×6, advanced ×2.

## Suggested use

**As a student.** Take the module quiz closed-book after the lessons, then read the key. Do the
self-assessment sheet before starting the next module. Do the programming assignment for modules you
intend to use in the capstone; do the analytical assignments in numerical order, since each assumes
the previous one's habits.

**As an instructor.** Quizzes are self-contained and can be used as-is or split by part. The rubrics
are written to be applied without a marking meeting: each criterion names observable evidence. If you
change a question, update the matching key — the numbering is the contract between the two files.

## Quality checks

The collection is checked by script on every change:

1. **Answer coverage.** Every question number in a quiz appears exactly once in its key, and no key
   contains a number the quiz does not have.
2. **Sequential numbering.** Questions run `Q<module>.1` upward with no gaps or duplicates.
3. **No inline answers.** Student-facing quizzes contain no answer text and no key markers.
4. **Links.** Every relative link in `assessments/` resolves to an existing file, and the root
   markdown links still resolve.
5. **Structure.** Every programming and analytical brief contains all twelve required fields with a
   weighted rubric summing to 100%.

Numbers quoted in explanations come from the module notebooks (for example the M13 fairness gaps and
the M14 compression timings) so that a reader can reproduce them rather than trust them.

---

[Course home](../README.md) · [Quizzes](quizzes/quiz-m01.md) · [Programming](programming/README.md) · [Analytical](analytical/README.md) · [Self-assessment](self-assessment/README.md)
