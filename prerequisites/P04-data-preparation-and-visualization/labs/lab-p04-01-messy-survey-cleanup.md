# LAB-P04-01 — Messy Survey Cleanup

| Unit | P04 · Data Preparation and Visualisation |
| :--- | :--- |
| Level | 100 |
| Effort | 1 hour, single session |
| Lessons covered | [LP04-01](../lessons/LP04-01-dataset-structures-csv-and-json.md) … [LP04-04](../lessons/LP04-04-visualization-and-exploratory-data-analysis.md) |
| Dataset | generated in the lab (fixed seed) |
| Notebook | [NB-P04-01](../notebooks/nb-p04-01-data-preparation.ipynb) — the same procedure on a different dataset |

[← Unit home](../README.md) · [Prerequisites home](../../README.md)

## Scenario

A student society ran a satisfaction survey and exported the responses to CSV. The export has three
spellings of every city, trailing spaces in names, one respondent submitted twice, four satisfaction
scores are blank, and one age is 213. The society's president, Ms. Ayesha, wants a table she can hand to
the dean — and she has been told that "cleaning" means deleting anything awkward. She wants the opposite:
a table where every change is recorded and nothing is deleted without a reason.

## Your role

You are the data steward for the survey. You report to Ms. Ayesha and you will be judged on
**traceability**: anyone should be able to rerun your script and see exactly what it did.

## What you are given

| Item | Location | Notes |
| :--- | :--- | :--- |
| Survey export | generated in Task 1 | 60 rows, 5 columns, deliberate faults |
| Starter code | none | pandas, NumPy, Matplotlib |
| Constraints | — | no manual edits to the CSV; the script must reproduce the cleaned file |

**Not provided:** a list of the faults, the correct city spellings, or a decision about the age of 213.
Finding and justifying each decision is the exercise.

## Requirements

**Functional**

- R1 — Load the raw CSV and report shape, numeric columns, and missing counts per column before any
  change.
- R2 — Normalise city names to a fixed set of three spellings and strip whitespace from names.
- R3 — Remove duplicate respondents by `respondent_id`, keeping the first submission, and report the
  count.
- R4 — Impute missing satisfaction scores with the median and add a `score_missing` indicator.
- R5 — Handle the age of 213 explicitly: either correct it, exclude it, or keep it with a flag — and
  state the rule in the report.
- R6 — Write the cleaned frame to `survey_clean.csv` and print a cleaning report dictionary.

**Non-functional**

- N1 — Runs in under 5 seconds.
- N2 — Deterministic: same seed, same output file.
- N3 — No row is dropped without a count in the report.

## Tasks

1. **Generate the export.** Build 60 rows with `respondent_id`, `name`, `city`, `satisfaction` (1–5) and
   `age`. Corrupt it deliberately: five cities misspelled or padded, two names padded, one duplicated
   respondent, four blank scores, one age of 213. *(success: you can list the faults by inspecting, not
   by remembering)*
2. **Inspect.** Print shape, `select_dtypes("number").columns`, missing counts, and the rows where age
   exceeds 100. *(success: every injected fault appears in your inspection output)*
3. **Clean.** Normalise cities, strip names, deduplicate by id, impute scores with the median plus an
   indicator. *(success: no missing satisfaction remains and the fake city spellings are gone)*
4. **Decide about the age.** Apply your rule and record it. *(success: the report states the rule and the
   number of affected rows)*
5. **Visualise.** Draw a histogram of satisfaction and a bar chart of respondents per city. *(success:
   both labelled, with counts visible)*
6. **Report.** Print the cleaning report and write three sentences to Ms. Ayesha summarising what changed
   and what a reader should not conclude from the data.

## Deliverables

| File | Contents |
| :--- | :--- |
| `lab_p04_01.py` | Runnable script implementing R1–R6 |
| `survey_clean.csv` | The cleaned table |
| `survey_figures.png` | Two panels: satisfaction histogram, respondents per city |
| `report.md` | ≤ 300 words: every decision, with counts |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Cleaning correctness | 35% | All faults handled, counts consistent | Most handled | Faults remain or silent deletions |
| Traceability | 30% | Report lists every change with a number | Changes mentioned | No record of what happened |
| Code and figures | 20% | Reproducible, labelled, readable | Works, plain | Does not run |
| Judgement | 15% | The age decision is justified and its effect stated | Decision made, unexplained | Value silently deleted |

## Extension challenges

1. **Make it a function.** Refactor into `clean(df) -> (df, report)` and call it twice on two different
   exports, asserting that both produce zero missing satisfaction.
2. **Add validation.** Write `assert` statements that fail loudly if a city outside the allowed set
   survives cleaning, or if any satisfaction value falls outside 1–5.
3. **Near-duplicate names.** Normalise names and check for respondents who share a normalised name but
   differ in id. Decide what to do and record it.

## Hints

<details><summary>Hint 1 — getting started</summary>

Work in a fixed order: types, then categorical normalisation, then duplicates, then missing values, then
outliers. Changing the order changes the counts in your report, and the report is the deliverable.

</details>

<details><summary>Hint 2 — the likely sticking point</summary>

`fillna` with a median computed after deduplication gives a different median than one computed before.
Decide which is correct for your question and say so — either is defensible, but only one of them can be
described accurately in the report.

</details>

<details><summary>Hint 3 — checking your work</summary>

The cleaned row count equals the raw count minus the duplicates you removed; the satisfaction median
equals the median of the non-missing values; and summing the `score_missing` column equals the number you
imputed. Three assertions cover most of the lab.

</details>

## Reflection

1. Which fault would have changed a reported average the most, and by how much?
2. Why is an indicator column often more useful than a better imputation?
3. If the dean asks "how satisfied are students?", what single number would you give — and what would you
   say next?

## Time budget

| Session | Tasks | Time |
| :--- | :--- | ---: |
| 1 | 1–6 | 60 min |
