# Learning Paths

This page answers two questions: **where should I start**, and **how do I get to the end without
giving up**. The full sequence is in the [course roadmap](course-roadmap.md); here you choose a
route through it.

**Course home:** [README](../README.md) · **Prerequisites:** [prerequisites/README.md](../prerequisites/README.md) ·
**Modules:** [modules/README.md](../modules/README.md)

## 1. Find your starting point

Answer these eight questions without looking anything up. Each one tests a prerequisite the course
assumes. Do not guess — if you are unsure, treat it as a "no".

1. Can you write a Python function that takes a list and returns a new list, without help?
2. Can you explain the difference between a list and a dictionary, and say when each is better?
3. Can you multiply a 2×3 matrix by a 3×2 matrix by hand?
4. Can you compute the mean and standard deviation of five numbers, and say what the standard
   deviation means?
5. Can you compute a conditional probability, such as P(disease | positive test), from the base
   rate and the test's accuracy?
6. Can you differentiate $f(x) = x^3 + 2x$ and explain what the derivative tells you?
7. Can you load a CSV file, filter rows, and plot a column with pandas and Matplotlib?
8. Can you explain what "overfitting" means to someone who has never studied machine learning?

| If you answered "no" to | Study first | Then start at |
| :--- | :--- | :--- |
| 1 or 2 | [P01 Python programming](../prerequisites/P01-python-programming/README.md) | P02, then M01 |
| 3 | [P02 Mathematics: vectors and matrices](../prerequisites/P02-mathematics-for-ai/README.md) | M01 (mathematics can run in parallel) |
| 4 or 5 | [P03 Probability and statistics](../prerequisites/P03-probability-and-statistics/README.md) | M01, then M05 when you reach it |
| 6 | [P02 Mathematics: derivatives and optimisation](../prerequisites/P02-mathematics-for-ai/lessons/LP02-04-derivatives-partial-derivatives-and-gradients.md) | M01 |
| 7 | [P04 Data preparation](../prerequisites/P04-data-preparation-and-visualization/README.md) | M01 |
| 8 | Nothing — that is what the course teaches | M01 |
| None of them | You are ready | M01, or M03 if you want to start with algorithms |

**Rule of thumb.** If you answered "no" to three or more, spend two to four weeks on the
prerequisite track first. It is the cheapest investment in the course: every hour spent there saves
several later.

## 2. Entry points by background

| Your situation | Route | First week |
| :--- | :--- | :--- |
| **Complete beginner** — new to programming | P01 → P02 → P03 → P04 → M01 → M04 | Install Python (see [README §8](../README.md#8-software-requirements)) and work through P01 lessons 1–3 |
| **Programmer, weak mathematics** | P02 → P03 → P04 → M01 → M06 | Start P02, and run the NB-P02-01 notebook alongside |
| **Science or engineering graduate** | M01 → M04 → M06, skimming P02–P04 | Read M01's concept sections and take its quiz |
| **Already know ML, new to classical AI** | M04 → M06 revision → M07 | Start M04; use M06 to find gaps in evaluation practice |
| **Already know ML, want deep learning** | M06 revision → M07 | Take the M06 quiz, then start at [L07-01](../modules/M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md) |
| **Want to build an LLM application** | M07 attention → M11 → LAB-11-02 | Read [L07-07](../modules/M07-neural-networks-and-deep-learning/lessons/L07-07-attention-and-transformers.md), then start M11 at L11-01 |
| **Returning after a long break** | Re-take the eight questions above, then restart one module earlier than you think | Re-read your old written summaries before starting |

## 3. Path A — Core path (≈ 169 hours)

| Week | Work | Hours | Cumulative |
| :--- | :--- | ---: | ---: |
| 1–2 | P01 Python (14 h) | 7 | 14 |
| 3 | P02 vectors, matrices, eigenvalues and derivatives (12 h) | 12 | 26 |
| 4 | P03 probability and P04 data preparation essentials (9 h) | 9 | 35 |
| 5 | M01 in full: lessons, notebook, two labs, mini-project | 12.8 | 48 |
| 6–7 | M02 in full: five lessons, notebook, two labs | 9 | 66 |
| 8–9 | M03 in full: seven lessons, search workbench, two labs | 10 | 86 |
| 10–12 | M04 in full: seven lessons, two notebooks, three labs, project | 10.5 | 117 |
| 13–14 | M05 in full: six lessons, two notebooks, two labs | 10 | 138 |
| 15–17 | M06 in full: ten lessons, four notebooks, four labs, PA-06, mini-project | 10.5 | 169 |

**Status of this path.** Every unit it schedules is published: four prerequisite sections, M01, M02,
M03, M04, M05 and M06. The total is **169.2 hours**: P01 in full (14 h), 50% of P02–P04 (21 h) as
an explicit planning assumption for "the essentials", and the measured module totals for M01–M06
(134.2 h). It uses the same method as [curriculum map §3.1](CURRICULUM-MAP.md#31-how-the-hour-totals-are-calculated);
no design budget is used.

**What you give up.** No deep learning, no NLP, no vision, no reinforcement learning, no generative AI,
and no capstone. What you gain is the foundation that makes all of those learnable later — especially
the evaluation discipline in M06, which is where most self-taught practitioners are weakest.

**Where to go next.** Continue with Path B (three more weeks for M07), then any specialisation.

## 4. Path B — Core plus deep learning (≈ 194 hours)

| Weeks | Work | Hours/week |
| :--- | :--- | ---: |
| 1–17 | Core path, as above | 9–12 |
| 18–20 | M07: eight lessons, three labs, assignment | 9 |

M07 is the gate to every modern application. Even if you never build a transformer, understanding
backpropagation and attention changes how you read about AI. If you can only add three weeks to the
core path, add these.

## 5. Path C — Full programme (≈ 407 hours)

Every module, every lab, and a full capstone. This is the course in its complete form and the right
route if you are preparing for postgraduate study or a career change.

| Semester | Content | Hours | Weekly load |
| :--- | :--- | ---: | ---: |
| 1 | P01–P04, M01–M05 | 158.8 | ≈ 10 h over 16 weeks |
| 2 | M06–M14 | 247.9 | ≈ 15.5 h over 16 weeks |

If 14 hours a week is not sustainable, use three semesters of about 8 hours: prerequisites and
M01–M03; then M04–M07; then M08–M14 including the capstone. The boundaries matter less than the
order.

**Status of this path.** Every section and module named here is published: all four prerequisite
sections and all fourteen modules. The total is **406.7 hours** (56 prerequisite + 350.7 module
hours), so the semester split above is the measured one, not a design target.

## 6. Specialisation paths

Each specialisation assumes the core path plus M07 (≈ 194 hours) and then adds its own modules.

| Specialisation | Add | Total | For |
| :--- | :--- | ---: | :--- |
| **NLP and generative AI** | M08, M11, M12 | ≈ 270 h | Language technology, LLM applications |
| **Computer vision** | M09 and M13 in full | ≈ 243 h | Imaging, medical and industrial applications |
| **Decision systems** | M10, M12 | ≈ 256 h | Operations research, control, robotics |
| **Responsible AI** | M13, M12, M11 | ≈ 268 h | Audit, governance, policy, safety engineering |

**Honest version.** Every specialisation can be completed: every module it names has lessons, labs
and notebooks. Totals use the module pages' measured hours (core 169.2 + M07 24.9 + the named
modules); no design figure is mixed in.

Choose one and finish it rather than sampling three. Depth in one area plus the shared foundation
is more useful than a shallow tour, and every specialisation keeps CLO1–CLO7 intact.

## 7. Pacing options

| Hours per week | Full programme takes | Core path takes | Realistic for |
| ---: | :--- | :--- | :--- |
| 5 | ≈ 81 weeks | ≈ 34 weeks | Studying alongside a full-time job |
| 8 | ≈ 51 weeks | ≈ 21 weeks | A steady, sustainable habit |
| 12 | ≈ 34 weeks | ≈ 14 weeks | A serious course load |
| 20 | ≈ 20 weeks | ≈ 8 weeks | Full-time study, with retention risk |

**A warning about the last row.** Twenty hours a week works only if you keep doing the labs and the
self-assessment. Students who read quickly and skip the practice finish early and retain little.
The labs are the course; the reading is preparation for them.

## 8. What to do when you get stuck

Getting stuck is normal and predictable. A protocol beats willpower:

1. **Name the exact point of failure.** "I do not understand why A\* needs a consistent heuristic"
   is workable; "I do not understand search" is not. Write the sentence down.
2. **Check the prerequisite, not the current lesson.** Nine times in ten, the block is one level
   down: a matrix operation, a derivative rule, a Python idiom.
3. **Re-read section 3 of the lesson** (the conceptual explanation) and skip everything else. Then
   reread the first worked example with the solution covered.
4. **Run the code and change one number.** Concrete behaviour resolves more confusion than another
   paragraph of explanation.
5. **Explain it out loud to nobody**, in three sentences. The sentence you cannot finish is the gap.
6. **Only then use a hint, a book, or a video.** Attempting first is what makes the explanation
   stick.
7. **If you are still stuck after 45 minutes, move on** and return the next day. Spaced return
   solves a remarkable number of problems, and grinding for three hours teaches you to dislike the
   subject.

## 9. If you have to pause

Life interrupts courses. When you return:

- **Restart one module earlier than you think you need.** Re-read its summary sections and take its
  quiz; that is a two-hour diagnostic, not a setback.
- **Re-run one notebook from the module before.** If it makes sense, you have retained more than
  you feared.
- **Do not restart the whole course.** Restarting from M01 is the most common way a promising
  self-study attempt dies.

## 10. Knowing you are ready to advance

Each stage has evidence attached, listed in [course roadmap §6](course-roadmap.md#6-what-finished-means-at-each-stage).
The short version: you are ready when you can *do* the thing, not when you have read about it.
Finishing a module's lessons is not the same as finishing the module — the lab and the quiz are
what tell you whether the ideas are yours.

**Navigation:** [Course home](../README.md) · [Course roadmap](course-roadmap.md) ·
[Modules](../modules/README.md) · [Prerequisites](../prerequisites/README.md) ·
[FAQ](faq.md) · [Documentation index](index.md)
