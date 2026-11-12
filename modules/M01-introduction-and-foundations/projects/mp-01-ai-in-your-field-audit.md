# MP-01 — AI-in-Your-Field Use-Case Audit

| Module | M01 · Introduction and Foundations of Artificial Intelligence |
| :--- | :--- |
| Effort | 2 hours |
| Type | Mini-project, individual |
| Lessons covered | [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md) – [L01-04](../lessons/L01-04-ai-capabilities-and-limitations.md) |
| Deliverable | `usecase-audit.md` (≤ 900 words) plus `screening.py` |

[← Module home](../README.md) · [Course home](../../../README.md)

## Why this project

M01 asks you to reason about AI systems rather than build them. The best way to prove you can is
to take a system that matters in *your* field, describe it precisely, and state what evidence would
change your mind about it. This project produces one artefact you can show in an interview: a
disciplined one-page audit, not an opinion.

## The brief

Choose one deployed AI system from your own discipline — not a research prototype, not a product
you cannot describe. Examples: a plagiarism detector used by a university, a crop-disease classifier
in an agriculture app, a sepsis early-warning score in a hospital, a credit-scoring model, a
recommendation system in a learning platform.

Then produce:

1. **A mechanism description.** What does it perceive, what does it output, is it symbolic, learned,
   or hybrid? Two sentences, no marketing language.
2. **A capability score.** Fill the four-flag table, state your weights if you change them, and give
   the verdict — with the flags you were unsure about marked as such.
3. **A claim audit.** Six fields from L01-04 §4: task family, dataset, metric, base rate, tail
   behaviour, feedback loop. Mark every field you cannot fill as `UNKNOWN`.
4. **An error budget.** At a stated deployment volume, compute errors per day at the system's
   published accuracy (or your best estimate, clearly labelled). Attach a cost model with named
   harms.
5. **A screening script.** `screening.py` implements your capability scoring for five candidate
   systems in your field, prints the table, and includes at least one system you decided is *not*
   AI. Standard library only, deterministic.
6. **A recommendation.** Three sentences: adopt, pilot, or reject — and what evidence you would need
   before changing that recommendation.

## Deliverable format

`usecase-audit.md`:

```text
# <System name> — capability audit
## 1. Mechanism
## 2. Capability score
## 3. Claim audit (six fields)
## 4. Error budget
## 5. Recommendation and missing evidence
## Sources (2–4, with dates)
```

`screening.py` must run as `python screening.py` and print your table. No notebooks, no
dependencies, no network.

## Assessment rubric

| Dimension | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Precision of description | 25% | Mechanism described so an engineer would recognise it | Mostly accurate, some marketing terms | Vague or promotional |
| Use of the framework | 25% | Four flags and six audit fields used correctly, unknowns explicit | Framework applied with gaps | Framework ignored |
| Quantitative reasoning | 20% | Volume, error rate and cost model consistent and checkable | One arithmetic error or missing assumption | No numbers, or invented ones |
| Judgment | 20% | Recommendation follows from evidence, with a stated threshold for changing it | Recommendation plausible, weakly linked | Recommendation unsupported |
| Communication | 10% | A non-specialist could act on it | Understandable | Unclear |

## Common failure modes

| Failure | What it looks like | Fix |
| :--- | :--- | :--- |
| Auditing a category, not a system | "AI in healthcare" as the subject | Name one deployed product and its mechanism |
| Filling unknowns with guesses | Confident dataset claims with no source | Write `UNKNOWN` and say what you would ask for |
| Accuracy without volume | "97% accurate" and nothing else | Multiply by a stated daily volume and cost the errors |
| No negative example | Every candidate scored as AI | Include at least one automation and justify the verdict |

## Suggested schedule

| Step | Time |
| :--- | ---: |
| Choose the system; collect 2–4 sources | 25 min |
| Score and audit | 35 min |
| Error budget | 20 min |
| Write `screening.py` | 25 min |
| Write the note; check every number against the script | 15 min |
