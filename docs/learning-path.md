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
| **Complete beginner** — new to programming | P01 → P02 → P03 → P04 → M01 → M04 | Install Python (see [README §16](../README.md#16-software-and-tools-you-will-need)) and work through P01 lessons 1–3 |
| **Programmer, weak mathematics** | P02 → P03 → P04 → M01 → M06 | Start P02, and run the NB-P02-01 notebook alongside |
| **Science or engineering graduate** | M01 → M04 → M06, skimming P02–P04 | Read M01's concept sections and take its quiz |
| **Software developer moving into ML** | M01 → M04 → M06, with P02–P04 as reference | Start M01; M03 is not published, so M04 is the first classical-AI module you can finish |
| **Already know ML, new to classical AI** | M04 → M06 revision → M07 | Start M04; use M06 to find gaps in evaluation practice |
| **Already know ML, want deep learning** | M06 revision → M07 | Take the M06 quiz, then start at [L07-01](../modules/M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md) |
| **Want to build an LLM application** | M07 attention → M11 → LAB-11-02 | Read [L07-07](../modules/M07-neural-networks-and-deep-learning/lessons/L07-07-attention-and-transformers.md), then start M11 at L11-01 |
| **Want to build an autonomous agent** | M02 L02-01 → M11 → M12 reference code | Read M12's status page first: its lessons are not published, so you can read the code but cannot finish the module |
| **Returning after a long break** | Re-take the eight questions above, then restart one module earlier than you think | Re-read your old written summaries before starting |

## 3. Path A — Core path (≈ 165 hours)

The core path covers CLO1–CLO5: foundations, classical AI and machine learning. It is the right
choice for a single-semester course, or for a first pass that gets you to a defensible model.

| Weeks | Work | Hours/week | Cumulative |
| :--- | :--- | ---: | ---: |
| 1–2 | P01 complete | 9 | 18 |
| 3 | P02 vectors, matrices and eigenvalues | 10 | 28 |
| 4 | P02 derivatives and optimisation | 10 | 38 |
| 5 | P03 probability; P04 data preparation essentials | 7 | 45 |
| 6 | M01 complete | 10 | 55 |
| 7 | M02: L02-01 and the reference code (four further lessons not yet published) | 4 | 59 |
| 8–10 | M04 complete: seven lessons and two notebooks | 10 | 89 |
| 11–14 | M06 lessons 1–10, four notebooks, assignment | 10 | 129 |

**Status of this path.** It schedules only what is published: P01–P04, M01, M02 (one lesson),
M04 and M06. M03 and M05 are in the syllabus but have no lessons yet, so they are excluded —
which is why the published total is about 129 hours against the 165-hour design figure. The
classical-AI stage cannot be completed today, and no reading plan can change that.

**What you give up.** No deep learning, no NLP, no vision, no reinforcement learning, no generative
AI, and no capstone. What you gain is the foundation that makes all of those learnable later —
especially the evaluation discipline in M06, which is where most self-taught practitioners are
weakest.

**Where to go next.** Continue with Path B (three more weeks for M07), then any specialisation.

## 4. Path B — Core plus deep learning (≈ 192 hours)

| Weeks | Work | Hours/week |
| :--- | :--- | ---: |
| 1–17 | Core path, as above | 9–12 |
| 18–20 | M07: eight lessons, three labs, assignment | 9 |

M07 is the gate to every modern application. Even if you never build a transformer, understanding
backpropagation and attention changes how you read about AI. If you can only add three weeks to the
core path, add these.

## 5. Path C — Full programme (≈ 374 hours)

Every module, every lab, and a full capstone. This is the course in its complete form and the right
route if you are preparing for postgraduate study or a career change.

| Semester | Content | Hours | Weekly load |
| :--- | :--- | ---: | ---: |
| 1 | P01–P04, M01–M05 | 155 | ≈ 10 h over 16 weeks |
| 2 | M06–M14 | 219 | ≈ 14 h over 16 weeks |

If 14 hours a week is not sustainable, use three semesters of about 8 hours: prerequisites and
M01–M03; then M04–M07; then M08–M14 including the capstone. The boundaries matter less than the
order.

**Status of this path.** The full programme is a design target, not something you can finish in
this repository today. Published: P01–P04, M01, M02 (1 of 5 lessons), M04, M06, M07, M11, M13 and
M14. Not published: M03, M05 and M09 (no content at all), plus M08, M10 and M12 (reference code,
no lessons). A student following the semester table as written meets an empty module at M03, again
at M05, and no lessons in M08. Plan around that, or start from the routes in section 2.

## 6. Specialisation paths

Each specialisation assumes the core path plus M07 (≈ 192 hours) and then adds its own modules.

| Specialisation | Add | Total | For |
| :--- | :--- | ---: | :--- |
| **NLP and generative AI** | M11 (M08 lessons not published; the NLP background is inside M11) | ≈ 195 h | Language technology, applied LLM work |
| **Computer vision** | M07 CNN lessons plus the M14 vision labs (M09 not published) | ≈ 200 h | Imaging and applied vision |
| **Decision systems** | M12 reference code (M10 lessons not published) | ≈ 190 h | Agent engineering, not RL research |
| **Responsible AI** | M13 in full, plus M11 for generative-system risk | ≈ 215 h | Audit, governance, policy, safety engineering |

**Honest version.** Only the NLP/generative and responsible-AI specialisations can be completed
as designed. The vision and decision-systems routes teach the surrounding material but not the
named module, and the totals above exclude the missing hours.

Choose one and finish it rather than sampling three. Depth in one area plus the shared foundation
is more useful than a shallow tour, and every specialisation keeps CLO1–CLO7 intact.

## 7. Pacing options

| Hours per week | Full programme takes | Core path takes | Realistic for |
| ---: | :--- | :--- | :--- |
| 5 | ≈ 75 weeks | ≈ 33 weeks | Studying alongside a full-time job |
| 8 | ≈ 47 weeks | ≈ 21 weeks | A steady, sustainable habit |
| 12 | ≈ 31 weeks | ≈ 14 weeks | A serious course load |
| 20 | ≈ 19 weeks | ≈ 8 weeks | Full-time study, with retention risk |

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
