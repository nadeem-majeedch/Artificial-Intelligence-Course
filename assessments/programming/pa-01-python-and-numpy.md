# PA-01 — Student Results Analysis with Python and NumPy

| | |
| :--- | :--- |
| Assignment | 01 |
| Difficulty | Beginner |
| Estimated time | 3 hours |
| Prerequisites | P01 (L01-01 … L01-06) |
| Covers | Python data structures, functions, NumPy arrays, vectorisation |

[Assessment index](../README.md) · [Programming assignments](README.md) · [Solutions guidance](../solutions/README.md)

## Background

A department has three years of module results in a CSV file. The registry asks for a summary that
is correct, reproducible, and cheap enough to run on the full dataset every night. Doing this with
nested Python loops is acceptable for 500 rows and unacceptable for 500,000 — the assignment asks
you to write both and measure the difference.

## Problem scenario

`results.csv` has columns `student_id, module, year, score, attempted`. Some rows are malformed:
missing scores, duplicate submissions, scores as strings with a percent sign. You must produce a
summary and a reproducible report, not a one-off notebook.

## Learning outcomes

1. Write functions with clear inputs and outputs instead of scripts that share globals.
2. Use NumPy arrays and vectorised operations where the loop would be slow.
3. Handle malformed input explicitly rather than crashing or silently dropping it.
4. Measure runtime and state the complexity of your approach.

## Tasks

1. **Load and validate.** Parse the CSV; report how many rows were dropped, and why, by category.
2. **Summarise.** Per module: count, mean, median, pass rate (score ≥ 40). Per year: same.
3. **Normalise.** Convert scores to a 0–100 scale, handling the percent strings and any values
   outside the range.
4. **Compare implementations.** Compute the per-module mean once with a Python loop and once with
   NumPy `groupby`-style masking. Time both on the provided file and on a synthetic 500k-row file
   you generate; report the ratio.
5. **Anomalies.** Flag students whose score changed by more than 20 points between attempts, and
   report how many such cases exist.
6. **Write the report.** A script that regenerates every number in a markdown file.

## Constraints

- Python 3.10+, NumPy and pandas only.
- No manual editing of the CSV.
- Every number in the report must be produced by the script.
- Handle missing values explicitly; do not use `dropna()` without reporting what was dropped.

## Expected deliverables

`analysis.py`, `report.md` (generated), `results_summary.csv`, and a short README with the runtime
measurements and the commands to reproduce them.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Correctness | 35% | summaries match a reference computation |
| Validation | 20% | dropped rows counted and explained |
| Performance | 15% | loop vs vectorised comparison with timings |
| Reproducibility | 15% | one command regenerates the report |
| Code quality | 15% | functions, no globals, readable names |

## Bonus challenges

- Stream the 500k file in chunks and keep memory below 100 MB; measure peak memory.
- Add a `--year` filter and test it against the unfiltered run on a single year.

---

[Assessment index](../README.md) · [PA-02](pa-02-search-algorithms.md)
