# P01 — Python Programming for AI

**Level 100 · 14 hours · 6 lessons, 2 notebooks, 1 lab**

[← Prerequisites home](../README.md) · [Next unit: P02 Mathematics →](../P02-mathematics-for-ai/README.md)

This unit takes you from "I have never opened a terminal" to "I can load a dataset, clean a column,
compute a summary and draw a labelled chart". Every example is written for numerical work: no web
frameworks, no databases, no packaging beyond the standard library and the four data libraries the
rest of the course uses.

If you already program in another language, read the lessons quickly and spend your time on
[LP01-06](lessons/LP01-06-numpy-pandas-and-plotting.md) and the notebooks — the vectorised style is
the part that transfers least from other languages.

## Who this unit is for

- **Complete beginners:** work through every lesson in order and type every code block. Do not copy and
  paste; the typing is the practice.
- **Programmers new to Python:** skim lessons 1–5, then do lesson 6 and both notebooks carefully.
- **Python users new to data work:** start at [LP01-06](lessons/LP01-06-numpy-pandas-and-plotting.md),
  then the notebooks, then the lab.

## Learning outcomes

By the end of P01 you can:

1. Install Python, create a virtual environment, and run a Jupyter notebook.
2. Write functions and small classes that return values rather than printing them, and handle the
   errors you expect.
3. Choose correctly between a list, tuple, set and dictionary, and read a comprehension as a set
   definition.
4. Load CSV and JSON data into pandas, inspect shape and types, and filter, group and sort a table.
5. Produce a labelled figure with Matplotlib and a grouped statistical plot with Seaborn.
6. Read a traceback from the bottom and fix the error it names.

These outcomes feed **M01–M03** directly: every module from M01 onward assumes you can run a notebook
and manipulate a DataFrame.

## Lessons

| ID | Lesson | Time | Focus |
| :--- | :--- | ---: | :--- |
| [LP01-01](lessons/LP01-01-setting-up-python-and-jupyter.md) | Setting Up Python and Jupyter | 75 min | Install, virtual environments, notebook workflow |
| [LP01-02](lessons/LP01-02-variables-types-and-operators.md) | Variables, Types, Operators and Expressions | 75 min | Five core types, precedence, floating point |
| [LP01-03](lessons/LP01-03-conditionals-loops-and-comprehensions.md) | Conditionals, Loops, Comprehensions and Lambda | 90 min | Branch order, `range`, comprehensions, `lambda` |
| [LP01-04](lessons/LP01-04-functions-and-collections.md) | Functions and Collections | 90 min | Arguments, scope, mutation, the four collections |
| [LP01-05](lessons/LP01-05-objects-modules-exceptions-and-files.md) | Objects, Modules, Exceptions and Files | 90 min | Classes, imports, `try`/`except`, `pathlib` |
| [LP01-06](lessons/LP01-06-numpy-pandas-and-plotting.md) | NumPy, pandas and Plotting | 120 min | Arrays, broadcasting, DataFrames, figures |

## Notebooks

| Notebook | Pairs with | What it demonstrates |
| :--- | :--- | :--- |
| [NB-P01-01](notebooks/nb-p01-01-python-fundamentals.ipynb) | LP01-01 … LP01-05 | Types, control flow, functions, collections, files, exceptions |
| [NB-P01-02](notebooks/nb-p01-02-numpy-pandas-plotting.ipynb) | LP01-06 | Array shapes and broadcasting, DataFrame operations, four chart types |

Run each notebook top to bottom before reading the next lesson. Cells marked **Exercise** have a
solution cell directly below; write your answer first, then compare.

## Lab

[LAB-P01-01 — Student Results Analysis](labs/lab-p01-01-student-results-analysis.md) (2.5 h) builds a
small analysis end to end: load raw records, clean them, compute per-group summaries, and produce a
figure. It is the rehearsal for everything P04 and M02 ask of you.

## Time budget

| Activity | Hours |
| :--- | ---: |
| Six lessons | 9.0 |
| Two notebooks | 2.5 |
| Lab | 2.5 |
| **Total** | **14.0** |

Split it over two weeks: lessons 1–3 and notebook 1 in week one, lessons 4–6, notebook 2 and the lab in
week two.

## How to check yourself

Each lesson ends with four self-assessment questions with hidden answers, and a Mini-Lab. If you cannot
answer three of four without opening the answers, reread the section that covers them before moving on.
At the end of the unit, the [diagnostic](../diagnostic.md) includes Python questions drawn from these
lessons.

## Common sticking points

- **`python` versus `python3` on Windows.** Use `python`; the `python3` alias may not exist. See
  [LP01-01](lessons/LP01-01-setting-up-python-and-jupyter.md).
- **`ModuleNotFoundError: numpy`.** The notebook is using a different interpreter from the one you
  installed into — select the right kernel in Jupyter.
- **A shape error in pandas.** Print `df.shape` before and after each step; the step that changed the
  shape unexpectedly is the bug.

## Next

Continue to [P02 — Mathematics for AI](../P02-mathematics-for-ai/README.md).
