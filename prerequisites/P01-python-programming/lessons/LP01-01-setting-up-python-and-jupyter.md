# LP01-01 — Setting Up Python and Jupyter

| Unit | P01 · Python Programming for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 75 minutes |
| Prerequisites | None |
| Notebook | [NB-P01-01](../notebooks/nb-p01-01-python-fundamentals.ipynb) |
| Lab | [LAB-P01-01](../labs/lab-p01-01-student-results-analysis.md) |

[← Prerequisites home](../../README.md) · [P01 home](../README.md) · [Next: Variables and Types →](LP01-02-variables-types-and-operators.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Install** Python 3.11 or newer and confirm the version from a terminal.
- **Run** Python in three ways: a script file, an interactive session, and a Jupyter notebook.
- **Explain** what a Jupyter kernel is and why "restart and run all" fixes most notebook errors.
- **Diagnose** the three setup failures beginners actually meet.

## 2. Prerequisite Knowledge

None. This is the first lesson of the course.

## 3. Conceptual Explanation

### 3.1 Three ways to run Python

Python is a program that reads your text and executes it. You can hand it text in three ways, and
you will use all three:

1. **A script** — a `.py` file you run from a terminal: `python hello.py`. This is how real
   programs are delivered.
2. **An interactive session** — type `python` and get a `>>>` prompt. Useful for a one-line
   question ("what does this function return?").
3. **A notebook** — a `.ipynb` file that mixes explanation, code and output. This is how the
   course's practicals are delivered, because you can change a number and see the consequence
   immediately.

### 3.2 What a kernel actually is

A notebook is not the program. It is a document that sends code to a **kernel** — a separate Python
process that holds your variables in memory — and displays what comes back.

That separation explains the most common beginner confusion. If you define `x = 5` in cell 1, skip
cell 2, and use `x` in cell 3, it works — because the kernel still remembers. Then you reopen the
notebook tomorrow, run only cell 3, and get `NameError: name 'x' is not defined`.

The rule that prevents this class of bug entirely: **Restart & Run All** before you trust any
output. A notebook that only works in the order you happened to click is not reproducible.

### 3.3 What "install Python" means

Two things are installed and beginners conflate them:

- The **interpreter** (`python`) — runs the language.
- **pip** — installs libraries that other people wrote, from a public index.

Libraries are not part of the language. `import numpy` works only because NumPy was installed into
the same environment. That is why error messages about missing modules are installation problems,
not coding problems.

## 4. Worked Examples

### Example 1 — your first script

Create a file `hello.py` containing:

```python
name = "Ayesha"
print(f"Hello, {name}. Python is running.")
print(2 + 3 * 4)
```

Run it:

```text
python hello.py
```

**Output**

```text
Hello, Ayesha. Python is running.
14
```

The second line is worth pausing on: the answer is 14, not 20, because multiplication happens before
addition. Operator precedence is the subject of the next lesson.

### Example 2 — checking your installation

```text
python --version
python -c "import sys; print(sys.executable)"
```

**Output (your paths will differ)**

```text
Python 3.11.9
<python-install>\python.exe
```

The version tells you whether the interpreter is new enough; the path tells you *which* interpreter
is being used. When `pip install` seems to succeed but `import` still fails, these two commands
usually reveal that two installations are competing.

## 5. Visual Explanation

| Situation | Symptom | Cause | Fix |
| :--- | :--- | :--- | :--- |
| Two Python installations | `pip install x` works, `import x` fails | pip installed into a different interpreter | Use `python -m pip install x` so pip matches the interpreter |
| Stale kernel state | `NameError` for a variable you defined | Cell order, or deleted then re-run | Kernel → Restart & Run All |
| Notebook opens as text | You see JSON, not cells | Opened the file in an editor | Open it in Jupyter, JupyterLab or VS Code with the Jupyter extension |

*Text description of the table:* the three failures are ordered from most to least common; each row
pairs a symptom a beginner will actually see with the cause and the single command that fixes it.

## 6. Mathematical Formulation

No mathematics is required here. The one quantitative idea worth stating is the version constraint,
because it explains why some tutorials fail:

$$
\text{required}: \text{Python} \ge 3.11
$$

Later modules rely on syntax and library versions that older interpreters do not support, and error
messages from a too-old Python often look unrelated to the actual problem.

## 7. Python Implementation

```python
"""Confirm the environment before starting any exercise."""
import sys
import platform


def environment_report() -> dict[str, str]:
    """Return the interpreter details that matter for this course."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "executable": sys.executable,
        "new_enough": str(sys.version_info >= (3, 11)),
    }


for key, value in environment_report().items():
    print(f"{key:15s} {value}")
```

**Output**

```text
python          3.11.9
implementation  CPython
executable      <python-install>\python.exe
new_enough      True
```

If `new_enough` prints `False`, install a newer Python before continuing — every later lesson
assumes 3.11 or newer.

## 8. Practical Applications

- **Reproducible coursework.** Notebooks run end to end are evidence that your result did not depend
  on a lucky cell order. Every lab in this course is marked partly on this.
- **Debugging in industry.** "Works on my machine" is almost always an environment difference:
  another interpreter, another library version. The two commands in Example 2 are the first thing a
  professional runs.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Installing with a bare `pip` | `ModuleNotFoundError` after a "successful" install | `pip` belongs to a different interpreter | `python -m pip install <package>` |
| Trusting out-of-order execution | Results change when re-run | Kernel retains deleted state | Restart & Run All |
| Editing `.ipynb` as text | Broken JSON, notebook will not open | The file is a JSON document | Edit cells in a notebook interface |

## 10. Self-Assessment

**1.** What is the difference between the notebook document and the kernel?
<details><summary>Show answer</summary>

The document stores cells and outputs; the kernel is the running process that executes code and
holds variables. They can disagree — which is exactly why restarting the kernel and re-running
everything is the reliable way to check a notebook.
</details>

**2.** You install a package and the import still fails. What is your first diagnostic command?
<details><summary>Show answer</summary>

`python -m pip install <package>`, then `python -c "import sys; print(sys.executable)"`. The usual
cause is that pip and the interpreter belong to different installations.
</details>

**3.** Why does the course require Python 3.11 or newer?
<details><summary>Show answer</summary>

Because the course uses language and library features introduced in those versions; on older
interpreters the failures look like unrelated errors rather than a version problem.
</details>

## 11. Further Reading

- [The Python Tutorial](https://docs.python.org/3/tutorial/) — the official introduction; sections 1–3 cover installation and first steps.
- [Jupyter documentation](https://docs.jupyter.org/) — installing and running notebooks, including the kernel menu.

## Mini-Lab

You are handed a laptop with Python installed and asked to prove it is ready for the course. Write
a single script `ready.py` that prints the Python version, the executable path, and whether the
version is at least 3.11. Run it from a terminal and paste the output into your notes. If it fails,
record the exact error — that record is the first entry in your debugging log.

## What to Do Next

Open [NB-P01-01](../notebooks/nb-p01-01-python-fundamentals.ipynb) and run it top to bottom, then
continue to [LP01-02 Variables and Types](LP01-02-variables-types-and-operators.md).
