# About the Course

**Course home:** [README](../README.md) · **Learning paths:** [learning-path.md](learning-path.md) ·
**FAQ:** [faq.md](faq.md)

## Why this course exists

Most people who try to learn Artificial Intelligence on their own do not fail because the subject
is too difficult. They fail for three avoidable reasons: the material is written for someone who
already knows the answer, the mathematics arrives without warning, and nothing ever asks them to
produce something and be judged on it.

This course is built to remove those three obstacles. It explains ideas from intuition before
formalism, it supplies every piece of mathematics it uses in a dedicated prerequisite track, and it
asks you to build, measure and defend your work — with rubrics honest enough to mark yourself
against.

It is also deliberately broader than the current fashion. Modern AI is mostly machine learning, but
the field also contains search, logic, planning and multi-agent reasoning, and those ideas run
production systems every day. A course that begins at neural networks produces graduates who can
recognise AI only in its most recent costume.

## How the course is designed

**Self-study first.** Every lesson is written for a reader with no instructor present. Objectives
come before content, every technical term is defined on first use, worked examples show intermediate
steps rather than final answers, and each lesson ends with a self-check whose answers are included.

**One idea per lesson.** Lessons are short and single-purpose: forty-five to sixty minutes of
reading and practice. This keeps progress visible and makes it possible to resume after a week away
without rereading a chapter.

**Predictable structure.** Every lesson has the same eleven parts — objectives, prerequisites,
concept, worked examples, visuals, mathematics, code, applications, common mistakes,
self-assessment, further reading. Once you learn the structure, you always know where to look.

**Runnable, not merely readable.** Every algorithm the course teaches is implemented in Python you
can run, change and break. Notebooks execute on a CPU; most finish in seconds, and the longest take
about 1–1.5 minutes on the release-audit machine. Datasets ship with the course or are generated
locally.

**Offline after first use and affordable by design.** No paid account and no GPU are required.
Two M11 notebooks download small pretrained weights on first use and then run offline; optional
M08 demonstrations may do the same. Where a hosted language model illustrates something important,
an offline alternative teaches the same idea, and assessment never depends on the paid path.

**Assessment you can use alone.** Quizzes mark themselves with explained answers and point to the
lesson to revisit. Labs and assignments come with rubrics that state what "excellent" looks like,
so you can judge your own work the way an instructor would.

**Responsibility as engineering.** Fairness, explainability, privacy and security are taught after
you have built systems, not before, and they are assessed — because in practice they are
requirements, not closing remarks.

## What the course contains

| Part | Content |
| :--- | :--- |
| Prerequisite track | Four sections: Python, mathematics (notation, linear algebra and calculus), probability and statistics, and data preparation |
| Modules M01–M14 | Foundations, agents, search, logic, uncertainty, machine learning, deep learning, NLP, vision, reinforcement learning, generative AI, agentic AI, responsible AI, applications |
| Lessons | Teaching pages with objectives, worked examples, mathematics, code, applications, mistakes and self-assessment |
| Notebooks | Runnable practicals that execute on a CPU; a few optional demonstrations download small pretrained weights on first use |
| Labs | Realistic scenarios with a stakeholder, requirements, deliverables and a rubric |
| Assignments | Graded, specification-driven work with a six-dimension rubric |
| Quizzes | Multiple-choice sets with explained answers and a revision map |
| Projects | A mini-project per module, and a capstone with milestones and a defence |
| Reference | Glossary, curated books, official documentation, primary research papers |

Full inventory: [curriculum map](CURRICULUM-MAP.md).

## What the course is not

**It is not a library tutorial.** You will use scikit-learn and PyTorch, but knowing which function
to call is the smallest part of the skill. The course spends its effort on why a method works, when
it fails, and how to prove which of two options is better.

**It is not a shortcut to a job title.** It is a foundation. Employers hire people who can
evaluate, debug and explain systems; that ability is built by the labs and the capstone, not by
finishing the reading.

**It is not a substitute for a supervisor on research.** M14 teaches you to read and reproduce a
paper, not to conduct novel research independently.

## Assessment philosophy

Every graded artifact is judged on six dimensions: correctness, understanding, code quality,
evaluation, communication, and responsibility. The weighting is deliberately not all in the code.
A correct implementation that cannot say how well it works, or where it fails, is an unfinished
piece of engineering — and the rubric says so before you begin.

Marks are not the point of a self-study course; evidence is. Each module project and the capstone
produces something you can show: a repository, a figure, a short report. That portfolio is worth
more than any certificate, because it demonstrates what you can actually do.

## Using this course as an instructor

The structure, labs, rubrics and quizzes are designed to be adopted or adapted. Module pages list
outcomes and hours; the curriculum map gives the full inventory and outcome traceability; the
architecture document defines the templates and quality standards used throughout. If you teach a
3-credit course, the core path in [learning paths](learning-path.md) fits a single semester.

## Acknowledgements

This course stands on decades of open teaching. Its organisation follows the conventional shape of
university AI curricula, and students will see *Artificial Intelligence: A Modern Approach* by
Russell and Norvig referenced throughout the further reading — the standard reference for the
classical half of the field, and the source of much of the shared vocabulary. The applied modules
draw on the published research listed in [research papers](../resources/research-papers.md), and on
the documentation of the open-source libraries the course uses.

Gratitude is due to the maintainers of Python, NumPy, pandas, Matplotlib, scikit-learn, PyTorch,
Hugging Face Transformers and Gymnasium, whose work makes a course like this possible without a
budget, and to the students whose questions shaped the explanations.

## About the instructor

**Engr. Dr. Muhammad Nadeem Majeed**
Professor
Department of Data Science (PUCIT)
University of the Punjab, Lahore, Pakistan

Dr. Majeed teaches and supervises work in artificial intelligence and data science at the
Department of Data Science (PUCIT), University of the Punjab, Lahore. He designed this course for
students who want to understand AI deeply enough to build it and to question it — and for the many
learners outside a classroom who deserve the same material, explained as carefully.

The course reflects his conviction that AI is learned by deriving an idea, implementing it, breaking
it deliberately, and measuring what it actually does. Every module is built around that loop, and
every claim in the course can be checked by running the code.

**Navigation:** [Course home](../README.md) · [Learning paths](learning-path.md) ·
[Course roadmap](course-roadmap.md) · [FAQ](faq.md) · [Documentation index](index.md)
