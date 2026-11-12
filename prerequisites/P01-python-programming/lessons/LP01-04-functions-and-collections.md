# LP01-04 — Functions and Collections

| Unit | P01 · Python Programming for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 90 minutes |
| Prerequisites | [LP01-03](LP01-03-conditionals-loops-and-comprehensions.md) |
| Notebook | [NB-P01-01](../notebooks/nb-p01-01-python-fundamentals.ipynb) |
| Lab | [LAB-P01-01](../labs/lab-p01-01-student-results-analysis.md) |

[← Previous: Control Flow](LP01-03-conditionals-loops-and-comprehensions.md) · [P01 home](../README.md) · [Next: Objects, Modules, Files →](LP01-05-objects-modules-exceptions-and-files.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Write** functions with positional, keyword and default arguments, and return values rather than
  printing them.
- **Explain** local versus global scope, and why mutation inside a function surprises people.
- **Choose** between a list, tuple, set and dictionary for a given job.
- **Build** a frequency count and a lookup table with correct, idiomatic Python.

## 2. Prerequisite Knowledge

- Variables, types, loops and comprehensions: [LP01-02](LP01-02-variables-types-and-operators.md),
  [LP01-03](LP01-03-conditionals-loops-and-comprehensions.md).

## 3. Conceptual Explanation

### 3.1 A function is a named transformation

```python
def mean(values: list[float]) -> float:
    """Return the arithmetic mean of values."""
    return sum(values) / len(values)
```

Three habits separate functions that scale from functions that become a problem:

1. **Return, do not print.** A function that returns a value can be tested, reused, and composed.
   A function that prints can only be watched.
2. **Name the arguments for the reader.** `mean(values=temperature)` at the call site documents
   itself; `mean(temperature)` requires remembering the signature.
3. **Say what it assumes.** `mean([])` raises `ZeroDivisionError`. Either document that the list
   must be non-empty, or handle it.

### 3.2 Arguments in four forms

```python
def describe(name, score=0, *, verbose=False):
    ...

describe("Ali")                        # default score
describe("Sara", 91)                   # positional
describe("Sara", score=91)             # keyword
describe("Sara", 91, verbose=True)     # keyword-only
```

`*` makes `verbose` keyword-only, which prevents a caller from accidentally passing it positionally.
`*args` collects extra positional arguments into a tuple and `**kwargs` collects extra keyword
arguments into a dictionary; you will meet them in library code far more often than you need to
write them.

### 3.3 Scope, and the mutation trap

Names created inside a function are **local** — invisible outside it. Reading a global works;
assigning to it inside a function creates a local unless you declare `global` (which is almost always
a design smell).

The subtler issue is **mutation**. A function can change a list you pass it, because the list is a
reference:

```python
def add_zero(values):
    values.append(0)          # mutates the caller's list

nums = [1, 2]
add_zero(nums)
print(nums)                   # [1, 2, 0]
```

Returning a new list instead keeps the function predictable:

```python
def with_zero(values):
    return [*values, 0]
```

### 3.4 The four collections, and when each is right

| Collection | Ordered | Mutable | Duplicates | Lookup by | Reach for it when |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `list` | yes | yes | allowed | index | You have a sequence of items |
| `tuple` | yes | no | allowed | index | The items form a fixed record, e.g. `(lat, lon)` |
| `set` | no | yes | removed | membership | You need uniqueness or set operations |
| `dict` | yes (insertion) | yes | keys unique | key | You need a lookup table or a count |

Two idioms worth memorising, because they appear in every data program:

```python
# Count occurrences
counts = {}
for word in ["ai", "agent", "ai"]:
    counts[word] = counts.get(word, 0) + 1

# Group items by a key
by_first = {}
for word in ["ai", "agent", "search"]:
    by_first.setdefault(word[0], []).append(word)
```

`dict.get(key, default)` avoids a `KeyError`; `setdefault` creates the empty list on first use. Both
are the readable alternative to an `if key not in d:` block.

## 4. Worked Examples

### Example 1 — mean and standard deviation by hand, then by function

For values $[2, 4, 4, 4, 5, 5, 7, 9]$: mean $= 40/8 = 5$. Deviations from the mean are
$-3, -1, -1, -1, 0, 0, 2, 4$; squared: $9, 1, 1, 1, 0, 0, 4, 16$; sum $= 32$. Population variance
$= 32/8 = 4$, so standard deviation $= 2$.

```python
def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def stdev(xs: list[float], sample: bool = True) -> float:
    """Standard deviation; sample=True divides by n-1."""
    m = mean(xs)
    n = len(xs) - (1 if sample else 0)
    return (sum((x - m) ** 2 for x in xs) / n) ** 0.5


data = [2, 4, 4, 4, 5, 5, 7, 9]
print(mean(data), round(stdev(data, sample=False), 4))
```

```text
5.0 2.0
```

The `sample` flag is the whole reason the two formulas differ; conflating them is a common error when
moving from a textbook to a library.

### Example 2 — a function that returns two values

```python
def min_max(values: list[float]) -> tuple[float, float]:
    """Return (minimum, maximum) without calling min/max twice over the data."""
    low = high = values[0]
    for v in values[1:]:
        if v < low:
            low = v
        if v > high:
            high = v
    return low, high


low, high = min_max([3, 1, 4, 1, 5])
print(low, high)
```

```text
1 5
```

Returning a tuple and unpacking it at the call site is idiomatic and self-documenting.

### Example 3 — deduplicate while preserving order

```python
seen = set()
unique = []
for item in ["b", "a", "b", "c", "a"]:
    if item not in seen:
        seen.add(item)
        unique.append(item)
print(unique)
```

```text
['b', 'a', 'c']
```

`set(items)` would also deduplicate but discard the order, which changes downstream results. When
order matters, keep the list and use a set only as the membership test.

## 5. Visual Explanation

```text
caller                         function mean(values)
------                         ---------------------
values ──── reference ────▶    [2, 4, 4, 4, 5, 5, 7, 9]
                               sum(...) → 40
                               len(...) → 8
return value ◀──── float ────  40 / 8 → 5.0
```

*Text description of the diagram:* the caller passes a reference to the list, not a copy. The
function reads it and returns a new float; the list is untouched. Replace the read with
`values.append(...)` and the arrow becomes two-way — which is the mutation trap described in §3.3.

## 6. Mathematical Formulation

The two standard deviations differ by one degree of freedom:

$$
s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2},
\qquad
\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}
$$

Use $s$ (sample) when the data is a sample from a larger population — which is almost always the case
in machine learning — and $\sigma$ when you have the entire population. For large $n$ they are nearly
identical; for $n = 8$ they differ by about 7%, enough to change a reported result.

## 7. Python Implementation

```python
"""Build a small lookup table and a frequency count — the core of most data work."""
from collections import Counter

records = [
    {"name": "Ali", "city": "Lahore", "score": 78},
    {"name": "Sara", "city": "Karachi", "score": 91},
    {"name": "Bilal", "city": "Lahore", "score": 64},
    {"name": "Hina", "city": "Islamabad", "score": 85},
]


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of an empty sequence is undefined")
    return sum(values) / len(values)


by_city: dict[str, list[int]] = {}
for r in records:
    by_city.setdefault(r["city"], []).append(r["score"])

for city, scores in by_city.items():
    print(f"{city:10s} n={len(scores)} mean={mean(scores):.1f}")

print(Counter(r["city"] for r in records).most_common())
```

**Output**

```text
Lahore     n=2 mean=71.0
Karachi    n=1 mean=91.0
Islamabad  n=1 mean=85.0
[('Lahore', 2), ('Karachi', 1), ('Islamabad', 1)]
```

`Counter` is a dictionary subclass for exactly this job. You could write the loop yourself — and
should, once — but recognising the standard tool afterwards is the point.

## 8. Practical Applications

- **Grouping for analysis.** Every "average score per city" or "sales per region" question is the
  `setdefault`/`defaultdict` pattern above, whether written by hand or by pandas `groupby`.
- **Fixed-size records.** Coordinates, bounding boxes and (prediction, confidence) pairs belong in
  tuples, where immutability and unpacking do useful work.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Printing instead of returning | `None` when you use the result | No `return` statement | `return` the value |
| Mutable default argument | Results accumulate between calls | Default list created once | `def f(x, acc=None): acc = acc or []` |
| Mutating an argument silently | Caller's data changes | Lists are references | Return a new object, or document the mutation |
| Using a `set` where order matters | Output order changes between runs | Sets are unordered | Preserve order with a list plus a `seen` set |

## 10. Self-Assessment

**1.** What does this print, and why?

```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add(1), add(2))
```
<details><summary>Show answer</summary>

`[1, 2] [1, 2]` — the default list is created **once**, when the function is defined, and shared
between calls. Both prints show the same object after both appends. Use `bucket=None` and create the
list inside the body.
</details>

**2.** When is a tuple better than a list?
<details><summary>Show answer</summary>

When the collection is a fixed record whose length carries meaning: `(latitude, longitude)`, a
matrix shape, a function's multiple return values. Immutability prevents accidental edits and signals
to the reader that the structure is fixed.
</details>

**3.** Write the one-line expression that counts how many distinct cities appear in `records`.
<details><summary>Show answer</summary>

`len({r["city"] for r in records})` — a set comprehension deduplicates, and `len` counts.
</details>

**4.** Why prefer `counts.get(word, 0) + 1` over `counts[word] += 1` in a counting loop?
<details><summary>Show answer</summary>

Because `counts[word]` raises `KeyError` the first time a word is seen. `get` supplies a default,
which is both shorter and safer than wrapping every increment in a membership test.
</details>

## 11. Further Reading

- [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) — arguments, defaults and keyword-only parameters.
- [collections — Container datatypes](https://docs.python.org/3/library/collections.html) — `Counter`, `defaultdict`, `deque` and friends.

## Mini-Lab

A course office holds a list of `(student, course, score)` tuples. Write functions that return: the
mean score per course (a dictionary), the names of students scoring above the overall mean, and the
course with the highest mean. Handle an empty input without crashing, and state in one sentence
which collection type you chose for each result and why.

## What to Do Next

Continue to [LP01-05 Objects, Modules, Exceptions and Files](LP01-05-objects-modules-exceptions-and-files.md).
