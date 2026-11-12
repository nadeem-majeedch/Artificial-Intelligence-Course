# Templates

Copy the right template, rename it using the scheme in
[Architecture §4](../docs/ARCHITECTURE.md#4-naming-and-numbering-scheme), then replace every
`«…»` prompt. Nothing in this folder is student-facing content, and the validator skips it
(templates necessarily contain unfilled prompts).

| Template | Use for | Naming pattern | Required sections |
| :--- | :--- | :--- | :--- |
| [`lesson.md`](lesson.md) | Every teaching lesson | `lessons/L{MM}-{NN}-kebab-title.md` | 11 mandated sections |
| [`lab.md`](lab.md) | Every laboratory scenario | `labs/lab-{mm}-{nn}-kebab-title.md` | 11 parts incl. rubric |
| [`assignment.md`](assignment.md) | Graded assignments and mini-projects | `assignments/asg-{mm}-kebab-title.md`, `projects/mp-{mm}-kebab-title.md` | Spec + rubric |
| [`module-readme.md`](module-readme.md) | Module landing page | `README.md` inside the module | Outcomes, map, plan |
| [`quiz.md`](quiz.md) | Module MCQ set | `quizzes/quiz-{mm}.md` | 12–20 MCQs + key |
| [`notebook.ipynb`](notebook.ipynb) | Jupyter practical | `notebooks/nb-{mm}-{nn}-kebab-title.ipynb` | Fixed cell order |

## Note on links inside templates

Template links are written for the file's **destination**, not for `templates/`. A lab copied to
`modules/M03-…/labs/` must reach the repository root with `../README.md`, so the link looks
broken while the file still sits here. Two consequences:

- The validator skips `templates/` for the link check (V05); verify links after copying, or by
  resolving them against the destination depth by hand.
- Links to `glossary/terms.md` and `modules/README.md` will resolve only once Phase 02 creates
  those files — that is expected in a template, not in published content.

## Authoring workflow

1. Copy the template to its destination and rename it.
2. Fill the metadata table first — it forces you to name the prerequisites and the study time.
3. Write §3 (concept) and §4 (worked examples) before touching code; the code follows the example.
4. Write the code, run it, paste the real output.
5. Write §9 (common mistakes) last: by then you have made them yourself.
6. Run `python tools/validate.py` and `python tools/check_links.py`.
7. Add the new artifact to the module `README.md` map table — an unlisted artifact does not exist
   for the student.

## What not to do

- Do not add a twelfth mandatory section; if the lesson needs one, it is probably two lessons.
- Do not leave an `«…»` prompt or `TBD` in a file outside this folder.
- Do not reference an artifact that has not been created yet (§10 of the architecture, check V05).
- Do not copy an existing lesson as a starting point — copy the template, so drift cannot
  accumulate.
