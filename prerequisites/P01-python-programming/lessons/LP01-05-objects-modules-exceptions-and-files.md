# LP01-05 — Objects, Modules, Exceptions and Files

| Unit | P01 · Python Programming for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 90 minutes |
| Prerequisites | [LP01-04](LP01-04-functions-and-collections.md) |
| Notebook | [NB-P01-01](../notebooks/nb-p01-01-python-fundamentals.ipynb) |
| Lab | [LAB-P01-01](../labs/lab-p01-01-student-results-analysis.md) |

[← Previous: Functions and Collections](LP01-04-functions-and-collections.md) · [P01 home](../README.md) · [Next: NumPy, pandas and Plotting →](LP01-06-numpy-pandas-and-plotting.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Write** a small class with an initialiser, methods and a readable representation.
- **Import** code from the standard library and from your own modules, and explain what `if __name__ == "__main__"` protects.
- **Handle** errors with `try`/`except` at the right level, rather than swallowing them.
- **Read and write** text, CSV and JSON files safely, with paths that work on any machine.

## 2. Prerequisite Knowledge

- Functions, collections and looping: [LP01-04](LP01-04-functions-and-collections.md).

## 3. Conceptual Explanation

### 3.1 Classes bundle state with behaviour

A class is a template; an instance is one object made from it. Use one when a set of values and the
operations on them travel together.

```python
class Counter:
    """Count observations of categories."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.counts: dict[str, int] = {}

    def add(self, category: str) -> None:
        self.counts[category] = self.counts.get(category, 0) + 1

    def total(self) -> int:
        return sum(self.counts.values())

    def __repr__(self) -> str:
        return f"Counter(name={self.name!r}, total={self.total()})"
```

`self` is the instance being operated on — the explicit equivalent of `this` in other languages.
`__init__` runs at construction; `__repr__` controls how the object prints, which is worth thirty
seconds because you will see that output constantly while debugging.

### 3.2 Modules are files; packages are folders

A module is any `.py` file. `import math` loads the standard library's module; `math.sqrt(16)` uses
one function from it. Three forms, with different consequences:

```python
import math                 # math.sqrt
from math import sqrt       # sqrt — pollutes your namespace
import numpy as np          # np.array — the convention everyone uses
```

Avoid `from module import *`: it makes the origin of every name invisible. When you write your own
modules, keep them in the same folder and import by filename: `from helpers import mean`.

The guard at the bottom of a script:

```python
if __name__ == "__main__":
    main()
```

means "run this only when the file is executed directly, not when it is imported". Without it,
importing your module would also run its demo code.

### 3.3 Exceptions are values that interrupt the flow

When something goes wrong, Python raises an exception. Unhandled, the program stops and prints a
traceback; read tracebacks **from the bottom**: the last line names the error, the lines above show
where it happened.

Catch only what you can handle, and only where you can do something useful:

```python
try:
    value = int(text)
except ValueError:
    value = None            # expected input problem, handled here
```

Never write a bare `except:` that continues silently — it hides the errors you most need to see,
including typos and wrong variable names. Distinguish the three common ones: `ValueError` (right type,
wrong value), `TypeError` (wrong type entirely), `KeyError`/`IndexError` (missing key or position).

### 3.4 Files: always use `with`

```python
from pathlib import Path

path = Path("data") / "scores.txt"
with path.open("w", encoding="utf-8") as f:
    f.write("ali,78\n")
```

`with` closes the file even if an exception occurs — the alternative, calling `close()` by hand,
leaks file handles when something fails. Always pass `encoding="utf-8"`: the default differs by
operating system, and text with non-ASCII characters (Urdu, accented names) will otherwise fail on
Windows.

`pathlib.Path` handles separators for you, so `Path("data") / "scores.csv"` is correct on Windows
and Linux alike. Never build paths with `"data\\" + name`.

## 4. Worked Examples

### Example 1 — read a CSV by hand, then with the right tool

Given `scores.csv`:

```text
name,score
ali,78
sara,91
```

```python
from pathlib import Path
import csv

path = Path("scores.csv")
with path.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

print(rows)
print(sum(int(r["score"]) for r in rows) / len(rows))
```

```text
[{'name': 'ali', 'score': '78'}, {'name': 'sara', 'score': '91'}]
84.5
```

Note that `score` is a **string**. CSV stores text; converting is your job. This is the single most
common cause of `TypeError` in beginner data code, and the reason lesson LP01-06 introduces pandas,
which infers types for you.

### Example 2 — JSON, which preserves structure

```python
import json

record = {"name": "Sara", "score": 91, "tags": ["ml", "vision"]}
text = json.dumps(record, indent=2)
print(text)
back = json.loads(text)
print(back["tags"][0], type(back["score"]).__name__)
```

```text
{
  "name": "Sara",
  "score": 91,
  "tags": [
    "ml",
    "vision"
  ]
}
ml int
```

Unlike CSV, JSON keeps types: the score comes back as an `int`, not `"91"`. Use CSV for tables and
JSON for nested records and configuration.

### Example 3 — handle the error you expect, not every error

```python
def parse_scores(lines: list[str]) -> tuple[list[int], list[str]]:
    """Return (valid scores, rejected lines)."""
    good, bad = [], []
    for line in lines:
        try:
            good.append(int(line))
        except ValueError:
            bad.append(line)
    return good, bad


print(parse_scores(["78", "oops", "91", ""]))
```

```text
([78, 91], ['oops', ''])
```

The function reports what it rejected instead of failing or silently dropping data — which is the
behaviour an auditor will later ask you for.

## 5. Visual Explanation

| Where the error happens | Exception | Typical cause | What to do |
| :--- | :--- | :--- | :--- |
| Reading text into a number | `ValueError` | `int("78 ")` or `int("seventy")` | Strip whitespace; validate format |
| Using the wrong type | `TypeError` | `"78" + 5`, `None["x"]` | Convert, or check for `None` |
| Missing key or index | `KeyError` / `IndexError` | Column renamed; empty list | `get(key, default)`; check length |
| File not found | `FileNotFoundError` | Wrong working directory | `Path` from the notebook's folder |

*Text description of the table:* rows are ordered by how often beginners meet them. Each row names
the exception class itself, so that when you see that word at the bottom of a traceback you can go
straight to the cause and the fix instead of reading the whole stack.

## 6. Mathematical Formulation

No new mathematics. The one formal idea is the **round-trip property** that makes file formats
trustworthy: for any record $r$,

$$
\operatorname{loads}(\operatorname{dumps}(r)) = r
$$

JSON satisfies this for its supported types; CSV does not, because it discards type information. When
you design a data pipeline, ask which of your artefacts need that property and store them as JSON
(or Parquet) rather than CSV.

## 7. Python Implementation

```python
"""Write, read back and validate a small JSON dataset — the shape of every data pipeline."""

import json
from pathlib import Path

root = Path.cwd()
path = root / "students.json"

records = [
    {"name": "Ali", "scores": [78, 82, 71]},
    {"name": "Sara", "scores": [91, 88, 94]},
]

path.write_text(json.dumps(records, indent=2), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))

for r in loaded:
    avg = sum(r["scores"]) / len(r["scores"])
    print(f"{r['name']:6s} mean={avg:.1f}")

print("file size:", path.stat().st_size, "bytes")
```

**Output**

```text
Ali    mean=77.0
Sara   mean=91.0
file size: 155 bytes
```

`Path.write_text` and `Path.read_text` are the short form of `with open(...)` for whole-file
operations. Use them when the file is small enough to fit comfortably in memory, and the `with`
form when you stream large files line by line.

## 8. Practical Applications

- **Configuration.** Model settings, dataset paths and experiment names belong in a JSON or YAML
  file read once at start-up, not scattered through code.
- **Audit trails.** Recording rejected rows (Example 3) is what allows a data pipeline to be
  explained later — the same habit M13's audit work will demand.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Bare `except:` | Bugs vanish silently | Catches everything, including `KeyboardInterrupt` | Catch the specific class |
| No `encoding="utf-8"` | `UnicodeDecodeError` on Windows | Platform default codec | Always pass `encoding` |
| Building paths with `+` | `FileNotFoundError` | Wrong separator | `Path("data") / "file.csv"` |
| Forgetting `newline=""` with `csv` | Blank lines between rows on Windows | Newline translation | Pass `newline=""` |

## 10. Self-Assessment

**1.** What does `if __name__ == "__main__":` prevent?
<details><summary>Show answer</summary>

It prevents the file's demo or entry-point code from running when the file is *imported* as a module.
Without it, `from helpers import mean` would also execute whatever the script does at the bottom.
</details>

**2.** Why is `except Exception: pass` worse than letting the program crash?
<details><summary>Show answer</summary>

Because it converts every failure — including typos, missing files and logic errors — into silent
continuation. You lose the traceback that would have told you what went wrong, and the program
carries on with bad state.
</details>

**3.** You read a CSV and `int(row["score"])` raises `ValueError`. What are the two most likely
causes?
<details><summary>Show answer</summary>

The value contains whitespace or a thousands separator (`"1,200"`), or the column contains a missing
marker such as `""` or `"NA"`. Both are input-quality problems, not Python problems: inspect the raw
value before converting.
</details>

**4.** When would you make an attribute private (leading underscore), and what does that actually
enforce?
<details><summary>Show answer</summary>

A leading underscore (`self._counts`) signals "internal — do not rely on this from outside". Python
does not enforce it; it is a convention that protects you when the class changes later. Real
enforcement would require properties and validation, which is worth it only for invariants that
matter.
</details>

## 11. Further Reading

- [Classes](https://docs.python.org/3/tutorial/classes.html) — the official chapter, including `__init__` and special methods.
- [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — the canonical treatment of `try`/`except`/`finally`.
- [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files) — file modes and encodings.

## Mini-Lab

Write a module `marks.py` exposing a `Student` class (name, scores, `mean()`) and a function
`load(path)` that reads a JSON file of students and returns a list of `Student` objects. Include a
`__main__` block that loads a sample file and prints each student's mean. Then corrupt one record
(a score stored as `"n/a"`) and make `load` report the bad record instead of crashing — while still
loading the good ones.

## What to Do Next

Continue to [LP01-06 NumPy, pandas and Plotting](LP01-06-numpy-pandas-and-plotting.md) — the
lesson where these foundations become data work.
