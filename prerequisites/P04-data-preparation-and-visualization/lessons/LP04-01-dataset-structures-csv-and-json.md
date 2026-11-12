# LP04-01 — Dataset Structures, CSV and JSON

| Unit | P04 · Data Preparation and Visualisation |
| :--- | :--- |
| Level | 100 |
| Study time | 90 minutes |
| Prerequisites | [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md) |
| Notebook | [NB-P04-01](../notebooks/nb-p04-01-data-preparation.ipynb) |
| Lab | [LAB-P04-01](../labs/lab-p04-01-messy-survey-cleanup.md) |

[← Previous unit: P03](../../P03-probability-and-statistics/README.md) · [P04 home](../README.md) · [Next: Missing Values and Duplicates →](LP04-02-missing-values-and-duplicates.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Check** a freshly loaded dataset for shape, column types and obvious structural problems.
- **Explain** tidy data and convert a wide table to long form and back.
- **Load** CSV and JSON into pandas with the right options for encoding, separators and types.
- **Diagnose** the five structural faults that break analyses: merged headers, units in names, multiple
  values per cell, wide layout, and text-encoded numbers.

## 2. Prerequisite Knowledge

- Reading files and `pathlib`: [LP01-05](../../P01-python-programming/lessons/LP01-05-objects-modules-exceptions-and-files.md).
- pandas `DataFrame` basics: [LP01-06](../../P01-python-programming/lessons/LP01-06-numpy-pandas-and-plotting.md).

## 3. Conceptual Explanation

### 3.1 Tidy data: three rules

A dataset is **tidy** when:

1. Each **row** is one observation (one student, one transaction, one image).
2. Each **column** is one variable, with one type.
3. Each **cell** holds exactly one value.

Tidy data is not a style preference. It is the layout that makes grouping, filtering and plotting
mechanical: `df.groupby("city")["score"].mean()` only works because city is a column rather than part
of a column name.

### 3.2 Wide versus long

| | Wide | Long |
| :--- | :--- | :--- |
| Layout | one column per measurement | one row per measurement |
| Example | `student, maths, physics, chemistry` | `student, subject, score` |
| Good for | reading, reports | grouping, plotting, modelling |

`pd.melt` converts wide to long; `pivot_table` goes back. Most plotting libraries and every modelling
API want long form, which is why the conversion appears at the start of so many analyses.

### 3.3 The five structural faults

1. **Merged header rows.** Two title rows above the real header — fix with `skiprows`.
2. **Units inside names.** `weight_kg`, `weight_lb` in different files; strip the unit into a column or
   normalise it, never add them together.
3. **Multiple values in one cell.** `"Lahore; Karachi"` cannot be grouped; split into rows or a
   separate table.
4. **Values as column names.** `score_2023, score_2024` is wide data hiding a `year` variable.
5. **Text where numbers belong.** `"1,200"`, `"12%"`, `"<5"` — parse deliberately with
   `pd.to_numeric(..., errors="coerce")` and check what became missing.

### 3.4 CSV versus JSON

**CSV** is a flat table of text: small, universal, and type-blind. Everything comes back as a string
unless pandas can infer otherwise, and any nested structure must be flattened first.

**JSON** keeps types and nesting: lists, objects, booleans, nulls. It is the right format for API
responses and configuration, and the wrong format for a million-row numeric table, where CSV or Parquet
is far more compact.

`pd.read_json` handles a list of records; `json.load` plus `pd.json_normalize` handles nested objects.

## 4. Worked Examples

### Example 1 — inspect before you trust

```python
import pandas as pd

df = pd.DataFrame({
    "student": ["Ali", "Sara", "Bilal"],
    "city": ["Lahore", "Karachi", "Lahore"],
    "score": [78, 91, 64],
})
print(df.shape)
print(df.select_dtypes("number").columns.tolist())
print(df.head(2).to_string(index=False))
```

```text
(3, 3)
['score']
student  city  score
    Ali Lahore     78
   Sara Karachi    91
```

Three lines answer three questions before any analysis: how many rows and columns, is each column the
type it should be, and do the values look like what the column claims.

### Example 2 — wide to long, by hand

Wide:

| student | maths | physics |
| :--- | ---: | ---: |
| Ali | 78 | 82 |
| Sara | 91 | 88 |

```python
wide = pd.DataFrame({"student": ["Ali", "Sara"], "maths": [78, 91], "physics": [82, 88]})
long = wide.melt(id_vars="student", var_name="subject", value_name="score")
print(long.to_string(index=False))
```

```text
student  subject  score
    Ali    maths     78
   Sara    maths     91
    Ali  physics     82
   Sara  physics     88
```

Long form has one row per (student, subject) pair — and now `long.groupby("subject")["score"].mean()`
is a single call.

### Example 3 — a CSV that lies about its types

```python
from io import StringIO
import pandas as pd

raw = StringIO('name,score,attendance\nAli,78,90%\nSara,"1,200",95%\nBilal,,80%\n')
df = pd.read_csv(raw)
print(df.select_dtypes("number").columns.tolist())
print(df["score"].tolist())
```

```text
[]
['78', '1,200', nan]
```

Not one column was recognised as numeric: the quotes around `"1,200"` made `score` text, and `90%` did
the same for `attendance`. The empty list is the diagnostic.

`score` is text because of the thousands separator in the second row; the third value became `NaN`
because it was empty. Any arithmetic on `score` would now fail or silently coerce. The fix is explicit:

```python
df["score"] = pd.to_numeric(df["score"].str.replace(",", ""), errors="coerce")
df["attendance"] = pd.to_numeric(df["attendance"].str.rstrip("%")) / 100
print(df["score"].tolist(), df["attendance"].tolist())
```

```text
[78.0, 1200.0, nan] [0.9, 0.95, 0.8]
```

Notice what the diagnosis required: looking at the raw strings. `describe()` would have shown only
`count`, `unique` and `top` for a text column and told you nothing about which row misbehaved.

## 5. Visual Explanation

| Symptom in `df.head()` | Diagnosis | Fix |
| :--- | :--- | :--- |
| Column names like `Unnamed: 0` | Index written as a column | `index_col=0` |
| First row is real data in headers | Header row skipped | `header=None`, then rename |
| One column holds `a;b` | Multiple values per cell | Split, then explode |
| `score_2019`, `score_2020`, … | Wide layout | `melt` |
| Dtype `object` for a numeric column | Text encoding | Clean, then `to_numeric` |

*Text description of the table:* read it as a diagnostic chart — each row is something you can see in
the first five rows of a table, the likely cause, and the one-line repair. Most of data preparation is
working down a table like this one.

## 6. Mathematical Formulation

Tidy data is a normal form: a table in which the columns are a set of variables $V$ and each row is a
value assignment to all of $V$. Wide data represents a *function* $f(\text{entity}, \text{time})$
spread across columns, which is why it must be converted before grouping — grouping presupposes that
the grouping key is a column.

Formally, melting maps a table with key $k$ and measure columns $m_1,\dots,m_p$ to one with rows
$(k, m_j, v_{kj})$ — a change of index from $\{k\} \times \{m_j\}$ to a single record identifier. The
information content is identical; only the shape changes.

## 7. Python Implementation

```python
"""Load both formats, normalise, and confirm the round trip."""
import json
from pathlib import Path

import pandas as pd

records = [
    {"student": "Ali", "scores": {"maths": 78, "physics": 82}},
    {"student": "Sara", "scores": {"maths": 91, "physics": 88}},
]

path = Path("nested.json")
path.write_text(json.dumps(records, indent=2), encoding="utf-8")

flat = pd.json_normalize(records, sep="_")
print(flat.to_string(index=False))
print(flat.select_dtypes("number").columns.tolist())

csv_path = Path("flat.csv")
flat.to_csv(csv_path, index=False)
back = pd.read_csv(csv_path)
print("round trip equal:", back.equals(flat))
```

**Output**

```text
student  scores_maths  scores_physics
    Ali            78              82
   Sara            91              88
['scores_maths', 'scores_physics']
round trip equal: True
```

`json_normalize` flattens one level of nesting with a separator, turning `{"scores": {"maths": 78}}`
into a column `scores_maths`. This is the standard first step when an API returns nested JSON and you
want a table.

## 8. Practical Applications

- **Data ingestion.** Every project starts with a script that loads, validates and reshapes raw files;
  the faults in §3.3 are what that script exists to catch.
- **Reproducible reports.** Storing tidy CSVs instead of hand-formatted spreadsheets means the numbers
  in a report can be regenerated rather than retyped.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Analysing before checking dtypes | `TypeError` mid-pipeline | Text columns | `df.dtypes`, then convert |
| Grouping on a wide layout | No such column | Variable is in the header | `melt` first |
| Assuming `read_csv` guessed right | Silent `NaN`s | Inference failure | Pass `dtype=` explicitly |
| Forgetting `encoding="utf-8"` | `UnicodeDecodeError` | Platform default | Pass `encoding` |

## 10. Self-Assessment

**1.** A table has columns `id, jan, feb, mar`. Is it tidy? What would you change?
<details><summary>Show answer</summary>

No. The month is a variable stored in the column names. Melt to `id, month, value`, which then supports
grouping by month, plotting a time series, and joining with other tables.
</details>

**2.** Why does `read_csv` return a numeric-looking column as `object`?
<details><summary>Show answer</summary>

Because at least one value is not a plain number — a thousands separator, a percent sign, a stray space,
or a missing-value marker like "NA". pandas falls back to text for the whole column rather than guess.
</details>

**3.** When is CSV a poor choice?
<details><summary>Show answer</summary>

When the data is nested (use JSON), when types must be preserved exactly, and when the table is very
large and numeric (Parquet is smaller and faster). CSV also cannot represent multiple tables in one
file.
</details>

**4.** `df.shape` returns `(0, 12)`. What happened, and what do you check first?
<details><summary>Show answer</summary>

The file was parsed but no data rows were found — usually a wrong `sep`, a `skiprows` that removed
everything, or a header-only file. Print the first few raw lines of the file before changing options.
</details>

## 11. Further Reading

- [pandas: IO tools](https://pandas.pydata.org/docs/user_guide/io.html) — every option for `read_csv` and `read_json`.
- [Tidy Data (Wickham, 2014)](https://www.jstatsoft.org/article/view/v059i10) — the paper that named the three rules.

## Mini-Lab

Create a messy CSV by hand with: a title row above the header, a column `weight (kg)`, a column with
`"Lahore; Karachi"` in one cell, and a score column containing `"1,200"`. Load it with the appropriate
`skiprows`, rename the unit-bearing column, split the multi-value cell with `.str.split(";")` and
`.explode()`, and parse the score. Report the final dtypes and shape, and how many rows the explode
added.

## What to Do Next

Continue to [LP04-02 Missing Values and Duplicates](LP04-02-missing-values-and-duplicates.md).
