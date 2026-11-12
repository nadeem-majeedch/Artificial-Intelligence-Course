# LP01-02 — Variables, Types, Operators and Expressions

| Unit | P01 · Python Programming for AI |
| :--- | :--- |
| Level | 100 |
| Study time | 75 minutes |
| Prerequisites | [LP01-01](LP01-01-setting-up-python-and-jupyter.md) |
| Notebook | [NB-P01-01](../notebooks/nb-p01-01-python-fundamentals.ipynb) |
| Lab | [LAB-P01-01](../labs/lab-p01-01-student-results-analysis.md) |

[← Previous: Setting Up](LP01-01-setting-up-python-and-jupyter.md) · [P01 home](../README.md) · [Next: Control Flow →](LP01-03-conditionals-loops-and-comprehensions.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Name** the five core Python types and choose the right one for a value.
- **Convert** between types deliberately, and predict when a conversion will fail.
- **Evaluate** an expression using Python's operator precedence rules.
- **Explain** why `0.1 + 0.2 != 0.3`, and why that matters for comparing measurements.

## 2. Prerequisite Knowledge

- Running Python and a notebook: [LP01-01](LP01-01-setting-up-python-and-jupyter.md).

## 3. Conceptual Explanation

### 3.1 A variable is a name for a value

```python
age = 21
name = "Ayesha"
passed = age >= 18
```

Each line binds a *name* to a *value*. Python is **dynamically typed**: the name has no fixed type,
the value does. `age = 21` then `age = "twenty-one"` is legal, though rarely wise — it makes code
harder to reason about and defeats editors that would otherwise catch mistakes.

### 3.2 The five types you need first

| Type | Example | Use it for | Watch out for |
| :--- | :--- | :--- | :--- |
| `int` | `42`, `-7` | Counts, indices, exact arithmetic | Division `/` always produces a float |
| `float` | `3.14`, `2.0` | Measurements, probabilities | Rounding: `0.1 + 0.2` is not exactly `0.3` |
| `str` | `"AI"`, `'Lahore'` | Text, labels, file paths | Strings are immutable; every "change" creates a new one |
| `bool` | `True`, `False` | Conditions, flags | `bool("False")` is `True` — non-empty text is truthy |
| `None` | `None` | "No value yet" | `None` is not `0`, `""` or `False` |

### 3.3 Operators come in families

- **Arithmetic:** `+  -  *  /  //  %  **` — note that `/` gives a float, `//` floors, and `%`
  returns the remainder.
- **Comparison:** `==  !=  <  <=  >  >=` — these produce `bool`.
- **Logical:** `and`, `or`, `not` — combine conditions.
- **Assignment:** `=`, plus shorthands `+=`, `-=`, `*=`.
- **Membership and identity:** `in`, `is` (the second compares identity, not value — do not use it for
  numbers).

### 3.4 Precedence determines the answer

`2 + 3 * 4 ** 2` is `50`, not `194`. Python evaluates `**` first, then `*` and `/` and `//` and `%`
left to right, then `+` and `-`, then comparisons, then `not`, then `and`, then `or`. When you are
unsure, use brackets — they cost nothing and prevent a silent error.

## 4. Worked Examples

### Example 1 — temperature conversion, by hand and by code

Convert 37 °C to Fahrenheit: $F = \frac{9}{5}C + 32$.

By hand: $\frac{9}{5} \times 37 = 66.6$, then $+ 32 = 98.6$.

```python
celsius = 37
fahrenheit = (9 / 5) * celsius + 32
print(fahrenheit)
```

```text
98.6
```

Now the same expression written carelessly as `9 / 5 * celsius + 32` still works, but
`9 / 5 * (celsius + 32)` would give 124.2 — a parentheses error that produces a plausible-looking
number. This is why the course insists on checking against a hand calculation.

### Example 2 — integer division and remainder

```python
total_minutes = 137
hours, minutes = divmod(total_minutes, 60)
print(hours, minutes)
```

```text
2 17
```

`divmod` returns quotient and remainder together. The identity behind it is the one to remember:

$$
137 = 60 \times 2 + 17
$$

which is why `137 // 60 == 2` and `137 % 60 == 17`. Any quantity that wraps around — minutes into
hours, indices into a fixed-size buffer — uses exactly this.

### Example 3 — the floating-point surprise

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

```text
0.30000000000000004
False
```

Binary floating point cannot represent 0.1 exactly, so the sum carries a tiny error. This is not a
Python bug; every language that uses IEEE-754 doubles behaves the same. Compare with a tolerance:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))
```

```text
True
```

## 5. Visual Explanation

| Expression | Result | Type | Why |
| :--- | :--- | :--- | :--- |
| `7 / 2` | `3.5` | `float` | True division always returns a float |
| `7 // 2` | `3` | `int` | Floor division |
| `7 % 2` | `1` | `int` | Remainder |
| `2 ** 10` | `1024` | `int` | Exponent |
| `"ab" * 3` | `"ababab"` | `str` | Repetition |
| `"2" + 3` | `TypeError` | — | Text and number cannot be added |

*Text description of the table:* the first four rows are arithmetic on integers and show how one
pair of numbers produces different results depending on the operator; the last two show that
operators are type-sensitive, which is the source of the most common beginner exception.

## 6. Mathematical Formulation

Floor division and modulo satisfy, for integers $a$ and $b \ne 0$:

$$
a = b\,(a \mathbin{//} b) + (a \bmod b), \qquad 0 \le a \bmod b < |b|
$$

That identity is the reason `divmod` is useful and the reason negative numbers surprise people:
in Python, `-7 // 2` is `-4` and `-7 % 2` is `1`, because Python floors towards negative infinity
so that the identity above still holds.

## 7. Python Implementation

```python
"""A small, complete use of types and expressions: a body-mass index calculator."""


def bmi(weight_kg: float, height_m: float) -> tuple[float, str]:
    """Return (BMI, category) for an adult.

    Raises ValueError when height is not positive, because dividing by zero
    would produce a meaningless infinity rather than an error a user can act on.
    """
    if height_m <= 0:
        raise ValueError("height must be positive")
    value = weight_kg / height_m**2
    if value < 18.5:
        category = "underweight"
    elif value < 25:
        category = "normal"
    elif value < 30:
        category = "overweight"
    else:
        category = "obese"
    return value, category


value, category = bmi(70, 1.75)
print(f"BMI = {value:.1f} ({category})")
```

**Output**

```text
BMI = 22.9 (normal)
```

The `:.1f` inside the f-string rounds for display only; the stored value keeps full precision.
Rounding for presentation and rounding for calculation are different decisions — do the first,
avoid the second.

## 8. Practical Applications

- **Data cleaning.** A column of prices read from a CSV arrives as `str`; every numeric operation
  fails until you convert it. Knowing types is what makes that diagnosis fast.
- **Money and counts.** Use `int` for counts and, for currency, work in the smallest unit (paisa,
  cents) to avoid the floating-point issue in Example 3.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| `"2" + 3` | `TypeError` | Types differ; `+` is not a converter | `int("2") + 3` |
| `==` for a computed float | Unexpected `False` | Binary representation error | `math.isclose(a, b)` |
| Using `is` for values | Works for small ints, fails for large ones | `is` compares identity | Use `==` |
| Shadowing built-ins | `list = [1, 2]` breaks later `list(...)` | Name reuse | Use `items`, `values`, `records` |

## 10. Self-Assessment

**1.** What does `17 // 5` give, and what does `17 % 5` give?
<details><summary>Show answer</summary>

`3` and `2`. Because $17 = 5 \times 3 + 2$, which is the division identity the operators encode.
</details>

**2.** Why is `bool("False")` true?
<details><summary>Show answer</summary>

`bool` of a string tests emptiness, not meaning. `"False"` is a non-empty string, so it is truthy.
Convert explicitly with a comparison if you need to parse text into a boolean.
</details>

**3.** Rewrite `(9 / 5) * c + 32` so that it avoids an unnecessary float division step, and explain
whether the result is the same.
<details><summary>Show answer</summary>

`9 * c / 5 + 32` gives the same value for ordinary inputs because multiplication and division have
equal precedence and are evaluated left to right. Both produce a float; the second does the division
later, which slightly reduces rounding accumulation for large inputs.
</details>

**4.** `len("AI")` returns 2. What does `len(str(1234))` return, and why?
<details><summary>Show answer</summary>

`4` — converting to text produces the four characters `1`, `2`, `3`, `4`; `len` counts characters.
</details>

## 11. Further Reading

- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — the authoritative reference for every operator in this lesson.
- [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html) — the official explanation of Example 3.

## Mini-Lab

A clinic records patient weights in pounds and heights in inches, but your model expects kilograms
and metres. Write a function `to_metric(pounds, inches)` returning `(kg, m)` using
$1\,\text{lb} = 0.45359237\,\text{kg}$ and $1\,\text{in} = 0.0254\,\text{m}$, then convert three
sample patients (150 lb/65 in, 180 lb/70 in, 120 lb/62 in). Check one conversion by hand.

## What to Do Next

Continue to [LP01-03 Control Flow](LP01-03-conditionals-loops-and-comprehensions.md), then work the
exercises in the notebook.
