# Getting Started

This course can be studied independently, used as a second explanation alongside a university
module, or adapted for classroom teaching. The important thing is to start at the right level and
work in a sequence that supplies the background each idea needs.

!!! tip "Choose a route before you start"
    Write down your route and your weekly study hours. Drifting between the core path, a
    specialisation and the full programme is the most common way to accumulate gaps.

## 1. Take the readiness diagnostic

The [prerequisite diagnostic](prerequisites/diagnostic.md) is an eight-question self-check. It maps
each gap to a specific preparation section rather than telling you simply to "learn the maths".

| If you... | Start with |
| :--- | :--- |
| Have never programmed | [P01 Python](prerequisites/P01-python-programming/README.md) |
| Program but are unsure of the mathematics | [P02](prerequisites/P02-mathematics-for-ai/README.md), then P03 and P04 |
| Know Python and first-year mathematics | [M01](modules/M01-introduction-and-foundations/README.md) |
| Already know machine learning | [M03](modules/M03-problem-solving-and-search-algorithms/README.md), M04 and M05, then M06 |
| Are returning after a break | [Learning paths](docs/learning-path.md) |

## 2. Choose a study route

| Route | Composition | Estimate |
| :--- | :--- | ---: |
| Core path | P01, essentials of P02–P04, M01–M06 | ≈ 169 hours |
| Core plus deep learning | Core path plus M07 | ≈ 194 hours |
| Full programme | All prerequisites, M01–M14 and the capstone | ≈ 407 hours |
| NLP and generative AI | Core plus M07, M08, M11 and M12 | ≈ 270 hours |
| Vision | Core plus M07, M09 and M13 | ≈ 243 hours |

The [learning paths](docs/learning-path.md) page contains week-by-week plans and pacing options.

## 3. Set up your environment

You need Python 3.11 or newer and a notebook environment. Install only what the current module
needs:

```bash
pip install numpy pandas matplotlib scikit-learn jupyter
```

Add PyTorch when you reach M07, and the optional Hugging Face packages when a module asks for them.
The full requirement list, CPU guidance and first-run download notes are on the
[course homepage](index.md#software-requirements).

## 4. Work through a lesson

Every lesson follows the same pattern:

1. Read the learning objectives and prerequisites.
2. Work the examples with the solutions covered.
3. Copy the mathematical formulation by hand.
4. Run the Python implementation and change one thing.
5. Answer the self-assessment before opening the answers.
6. Write a three-sentence summary: what the idea is, why it works and when it fails.

!!! warning "Running a notebook is not the exercise"
    Read the Markdown before the code, predict the output, then run it. The gap between your
    prediction and the result is where the learning happens.

## 5. Complete the practical work

Use the [laboratory guide](laboratories.md) to find a lab for the current module. A laboratory is
finished when you can state the decision, show a baseline, report the metric and explain one failure
case with its cause.

=== "Laboratory workflow"

    1. Read the scenario twice and write the decision in one sentence.
    2. List what you were given and what you were not.
    3. Build the simplest working baseline.
    4. Evaluate against the stated criteria, not your impressions.
    5. Write the stakeholder summary and one limitation.

=== "Assessment workflow"

    1. Read the specification and rubric before writing code.
    2. Fix seeds and use relative paths.
    3. Report the primary metric, baseline and uncertainty.
    4. Mark your own work against the rubric.
    5. Revisit the lessons named by any quiz error.

## 6. Finish with a capstone

The [capstone studio](projects-and-capstones.md) contains twelve briefs, four milestones, a rubric,
a report template and defence guidance. Choose a problem you understand and can evaluate with data
you are allowed to use.

## Where to go next

- [Prerequisites](prerequisites/README.md)
- [Module 01](modules/M01-introduction-and-foundations/README.md)
- [Course roadmap](docs/course-roadmap.md)
- [Frequently asked questions](docs/faq.md)
- [Software and tools](index.md#software-requirements)
