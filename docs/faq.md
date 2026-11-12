# Frequently Asked Questions

**Course home:** [README](../README.md) · **Learning paths:** [learning-path.md](learning-path.md) ·
**About:** [about.md](about.md) · **Documentation index:** [index.md](index.md)

If your question is not answered here, the answer is usually in one of three places: the
[learning paths](learning-path.md) page (where to start), the [glossary](../resources/glossary.md)
(what a word means), or the module page for whatever you are studying (what comes next).

## Getting started

**Do I need any previous AI knowledge?**
No. M01 assumes nothing beyond the willingness to write code. The prerequisite track exists for the
programming and mathematics, and it starts from the beginning.

**Which module should I start with?**
M01, unless the eight-question self-check on the [learning paths](learning-path.md#1-find-your-starting-point)
page shows a gap in programming or mathematics. If you can already program and know first-year
mathematics, M01 will take you about ten hours and is still worth doing — it fixes the vocabulary
the rest of the course depends on.

**Can I skip the prerequisites if I am impatient?**
You can, and many students try. The predictable result is that M06 becomes incomprehensible around
lesson three, because it assumes linear algebra, probability and calculus without re-teaching them.
If you must skip, at least read P02's first three lessons and P03's first three.

**How much time does the course take?**
About 165 hours for the core path (foundations through machine learning), 192 hours with deep
learning, and about 374 hours for the complete programme including the capstone. Pacing options are
in [learning paths §7](learning-path.md#7-pacing-options).

**Can I study only one module, for a specific need?**
Yes. Every module states its prerequisites and links to the lessons that supply them. Read those
first, then the module is self-contained.

## Studying effectively

**How should I read a lesson?**
Objectives, prerequisites, concept, then worked examples with the solutions covered. Run the code,
break it deliberately, and answer the self-assessment before opening the answers. The full routine
is in [README §11](../README.md#11-how-to-study-each-lesson).

**I understand the lessons but cannot solve the exercises. Is something wrong?**
No — that gap is the normal experience of learning. Understanding an explanation is recognition;
solving a problem is recall and transfer. The exercises and labs are where the learning actually
happens, which is why they are not optional extras.

**Should I take notes?**
Write a three-sentence summary after every lesson: what the idea is, why it works, when it fails.
That single habit is the highest-value thing you can do in this course, and it makes revision
almost free.

**I keep forgetting earlier material. What helps?**
Retrieval practice, not rereading. Redo two quiz questions from an earlier module each week, and
re-run one old notebook. Forgetting is normal; recovering it deliberately is the skill.

**How do I know I have finished a module?**
When you can do the things its outcomes list, pass its quiz, and complete its lab without looking
at the hints. Reading the lessons is not finishing.

## Mathematics

**How much mathematics do I need?**
Vectors and matrices, basic probability, derivatives, and enough data handling to load and clean a
table. Sections P02, P03 and P04 supply all of it in about 42 hours, and every formula in the course
is explained in words before symbols.

**The formulas intimidate me. Should I stop?**
No. Read the sentence before the formula, then the symbol table, then the worked example. Formulas
are compressed sentences, not different knowledge. Start with P02's first lesson, then work the worked
examples by hand with small numbers.

**Do I need to prove theorems?**
You need to follow proofs and justify algorithm choices — for example, why an admissible heuristic
keeps A\* optimal. You are not expected to produce original proofs.

## Tools and notebooks

**Do I need a GPU?**
No. Every notebook runs on a CPU in under a minute. A GPU helps only if you choose to scale up an
experiment in M07 or M11 beyond what the course asks.

**Which Python version?**
3.11 or 3.12 is the safest choice. Newer releases sometimes lack pre-built versions of the
scientific libraries; older ones may miss features the code uses.

**Which editor or environment?**
Any. Jupyter Notebook, JupyterLab or VS Code with the Jupyter extension are the common choices. If
installing locally is difficult, Google Colab or Kaggle Notebooks will run every notebook in the
course.

**The notebook shows as a wall of code when I open it. What happened?**
You are seeing the raw `.ipynb` file rather than a rendered notebook. Download it and open it in
Jupyter, or use the equivalent code from the lesson page, which contains the same implementation.

**A notebook cell fails. What should I do?**
Run *Restart & Run All* first — most notebook errors are stale state from a skipped or out-of-order
cell. If it still fails, check that you installed the libraries the module lists, and read the error
from the bottom up; the last line names the problem.

**Do I need internet access?**
No. Datasets ship with the course and no notebook requires a download. M11 and M12 include optional
hosted-API exercises; every one of them has an offline alternative.

**Do I need to pay for anything?**
No. No paid account is required for any lesson, lab, assignment or project.

## Content and assessment

**Are solutions provided?**
Self-assessment answers and quiz keys are included with reasoning. Labs provide progressive hints.
Full assignment solutions are deliberately not published, because assignments are how you find out
what you can do.

**How do I mark my own work?**
Use the rubric in the artifact. Each one has five criteria with descriptions of excellent,
adequate and not-yet. Be strict with yourself: the rubric exists so that "it works" is not the same
as "it is finished".

**Why are there common-mistakes sections in every lesson?**
Because the mistakes are predictable, and recognising a failure from its symptom is a professional
skill. Reading them before you make them saves hours.

**Is any of the material out of date?**
The classical modules (M03–M05) are stable. The applied modules (M08–M12) move quickly; they teach
durable concepts and pin specific tools inside labs, with dates, so you can tell what has drifted.

**Can I use this material for my own course?**
Ask the instructor. The structure, labs and rubrics were designed to be adapted, but the material
is not offered here under an open licence, so permission is required.

## Projects and careers

**Is there a capstone, and how big is it?**
Yes — M14. The full version takes 40–60 hours across milestones: proposal, prototype, evaluation,
report and presentation. A capstone-lite version of about 15–25 hours appears in the core path.

**Will this course get me a job?**
It will give you the foundation and a portfolio, not a guarantee. Employers look for evidence that
you can build, evaluate and explain systems — which is exactly what the labs, mini-projects and
capstone produce if you do them properly.

**What should I build first, outside the course?**
Something small, in a domain you already understand: a classifier for a dataset from your own work,
a search tool for a local problem, an assistant for a repetitive task. Domain knowledge plus modest
methods beats sophisticated methods on a problem you do not understand.

**Can I contribute or report an error?**
Yes — errors found by students improve the course for everyone. Note the module, lesson and the
exact sentence, and say what you expected instead.

**Navigation:** [Course home](../README.md) · [Learning paths](learning-path.md) ·
[Course roadmap](course-roadmap.md) · [About](about.md) · [Glossary](../resources/glossary.md)
