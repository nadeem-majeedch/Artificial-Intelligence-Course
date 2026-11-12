# P04 — Data Preparation and Visualisation

**Level 100 · 8 hours · 4 lessons, 1 notebook, 1 lab**

[← Previous unit: P03](../P03-probability-and-statistics/README.md) · [Prerequisites home](../README.md) · [Diagnostic →](../diagnostic.md)

The unit that decides whether the rest of the course works. Real data arrives with the wrong shape,
missing cells, duplicated rows, impossible values and columns stored as text. This unit gives you a
repeatable procedure for turning that into a tidy table you can model, and the plotting habits that let
you see what you are about to model.

## Who this unit is for

Everyone. Even students who have used pandas before tend to skip the parts about *why* a value is
missing and *where* the scaling statistics come from — and those are exactly the parts that produce
silently optimistic results later.

## Learning outcomes

By the end of P04 you can:

1. Inspect a new dataset for shape, types and the five structural faults, and repair each one.
2. Convert between wide and long layouts with `melt` and `pivot_table`.
3. Quantify missingness, choose between dropping and imputing, and keep an indicator when the fact of
   absence is informative.
4. Detect exact and near-duplicate records on a chosen key, and resolve conflicts rather than deleting
   them.
5. Flag outliers with the IQR fence and the modified z-score, and choose between keeping, capping and
   removing.
6. Apply min-max, standard and robust scaling without leaking test information, and explain when each
   is appropriate.
7. Run a structured exploratory analysis and choose a chart type from the question being asked.

These outcomes are the prerequisites for **M06, M08 and M09**, and they are assumed by every lab from
M02 onward.

## Lessons

| ID | Lesson | Time | Focus |
| :--- | :--- | ---: | :--- |
| [LP04-01](lessons/LP04-01-dataset-structures-csv-and-json.md) | Dataset Structures, CSV and JSON | 90 min | Tidy data, wide/long, loading, structural faults |
| [LP04-02](lessons/LP04-02-missing-values-and-duplicates.md) | Missing Values and Duplicates | 90 min | MCAR/MAR/MNAR, imputation, indicators, deduplication |
| [LP04-03](lessons/LP04-03-outliers-normalization-and-standardization.md) | Outliers, Normalisation and Standardisation | 90 min | IQR fence, masking, three scalings, leakage |
| [LP04-04](lessons/LP04-04-visualization-and-exploratory-data-analysis.md) | Visualisation and Exploratory Data Analysis | 90 min | Chart choice, multi-panel figures, four misleading habits |

## Notebook

[NB-P04-01 — Data Preparation](notebooks/nb-p04-01-data-preparation.ipynb) works on one deliberately
messy dataset from start to finish: inspect, reshape, clean missing values and duplicates, detect
outliers, scale, then explore with four chart types. Run it before the lab; the lab asks you to repeat
the procedure on data you have not seen.

## Lab

[LAB-P04-01 — Messy Survey Cleanup](labs/lab-p04-01-messy-survey-cleanup.md) (1 h) gives you a survey
export with inconsistent city names, empty cells, one duplicated respondent and an impossible age. The
deliverable is a cleaned CSV plus a short report of every decision you made and why.

## Time budget

| Activity | Hours |
| :--- | ---: |
| Four lessons | 6.0 |
| Notebook | 1.0 |
| Lab | 1.0 |
| **Total** | **8.0** |

## How to check yourself

After each lesson, open a dataset you have used before and apply the lesson's checklist to it. If you
cannot say, in one sentence each, how many rows are missing what and which column needed scaling, the
lesson has not landed. The [diagnostic](../diagnostic.md) closes the unit with questions from all four
sections.

## Common sticking points

- **Analysing before inspecting.** Print `shape`, `head` and the numeric column list first, every time.
- **Imputing the target.** Never. Drop those rows and say how many.
- **Scaling before splitting.** Fit the scaler on the training split only.
- **Deleting outliers automatically.** Inspect first; some of them are the phenomenon you are studying.

## Next

You have finished all four sections. Take the [prerequisite diagnostic](../diagnostic.md), then start
[Module 01 — Foundations of AI](../../modules/README.md#m01).
