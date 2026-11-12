# Report Writing Guide

Technical writing is a skill the rubric marks, and it is learnable. This guide covers structure,
numbers, figures, and the two sections students most often get wrong.

## 1. Structure is an argument

A report is not a diary of what you did. It is an argument that a specific claim is supported by
specific evidence. Every section answers one question:

| Section | The question it answers |
| :--- | :--- |
| Abstract | what did you find, and how sure are you? |
| Problem | why does this matter, to whom? |
| Related work | what is already known, and what did you borrow? |
| Data | what evidence base do you have, and what is missing from it? |
| Method | what did you do, and why that and not something simpler? |
| Results | what happened, with numbers and uncertainty? |
| Error analysis | where does it fail, concretely? |
| Limitations | what does this not establish? |
| Conclusion | what is now true that was not before? |

If a paragraph does not serve its section's question, cut it.

## 2. Numbers

Every number in the report must satisfy three tests:

1. **Provenance.** A command in the repository produces it.
2. **Context.** It is reported with the split, the sample size, and the metric definition.
3. **Uncertainty.** It has an interval, a seed spread, or an explicit caveat.

Bad: "Our model achieved 94% accuracy."
Good: "On the held-out field set (n = 312, 10 classes), the model reached macro F1 0.84
(95% CI 0.79–0.88 over five seeds), against 0.61 for the colour-histogram baseline."

The second sentence lets a reader disagree with you. That is the point.

### Reporting a comparison

```text
| Model            | Macro F1 | 95% CI        | n   |
| Baseline (hist.) | 0.61     | 0.55–0.67     | 312 |
| CNN (ours)       | 0.84     | 0.79–0.88     | 312 |
```

Rules: same rows for every model, same split, intervals for both, n stated once. If the intervals
overlap, say so — "the difference is within seed noise" is a finding.

## 3. Figures

A figure earns its place if it shows something a table cannot:

| Figure | Shows |
| :--- | :--- |
| confusion matrix | which classes are confused with which |
| per-class bar chart with n | where the aggregate hides failures |
| learning curve (train vs val) | overfitting, or underfitting |
| calibration plot | whether probabilities mean anything |
| drift over time | when the input distribution moved |

Every figure needs a caption that states the takeaway, not the axis labels: "Recall on class 7
falls by 30 points when the image is captured at night (n = 40)" beats "Figure 3: recall by
lighting condition".

Do not include a screenshot of code. Do not include a loss curve with no axis labels.

## 4. The limitations section

This is where marks are won and lost. A good limitations section:

- names a specific measurement ("accuracy on class X is 0.51 with n = 42"),
- says who is affected,
- says what would be needed to fix it.

A bad one is a list of universal caveats that could be pasted into any report: "the dataset may
be biased", "more data would help", "the model is not perfect".

**Test:** could this paragraph appear unchanged in a different student's report? If yes, it is
not about your project.

## 5. The abstract

Write it last. Structure: context (one sentence), gap (one), what you did (one), result with a
number (one), limitation (one). Five sentences, no citations, no "in this report we will".

Example:

> Early-warning systems for programming courses typically use engagement logs, but their
> predictions are rarely validated against the intervention they trigger. We built a week-6
> risk classifier on three years of LMS data and evaluated it on the most recent cohort held out
> entirely. At fixed precision 0.50 the model reached recall 0.63 (95% CI 0.58–0.68), against
> 0.41 for a logistic baseline on attendance alone. The gain depends on a feature (forum reads)
> that is only available for students who use the institutional platform, so the model
> under-serves exactly the students who work offline; we quantify that gap and do not recommend
> deployment without it being closed.

That abstract states a result, an uncertainty, and a limitation that bites.

## 6. Style

- **Active voice** where it clarifies: "we trained", not "training was performed".
- **Past tense** for what you did, present tense for what is true.
- **One idea per paragraph**, first sentence carries it.
- **Define acronyms** at first use, then use them.
- **No hedging chains**: "may possibly suggest" → "suggests".
- **Numbers**: two decimal places for metrics, consistent units, thousands separators.

## 7. Common report failures

| Failure | Fix |
| :--- | :--- |
| Method is 60% of the report, results 10% | results and error analysis are the contribution |
| No baseline in the results table | add it, even if it is worse |
| Accuracy only, on imbalanced data | macro F1, per-class table |
| "Significant" used without a test | say "larger" unless you ran a test |
| Limitations that could apply to any project | tie each to a measurement |
| Claims of production readiness | state the prototype boundary |
| Figures without captions that interpret | caption states the takeaway |
| No reproduction instructions | one command, seeds, environment |

## 8. Before you submit

- [ ] Abstract contains a number and a limitation
- [ ] Every table states the split and n
- [ ] Every model in the comparison has an interval or a stated caveat
- [ ] At least one per-class or subgroup table
- [ ] Three concrete errors analysed
- [ ] Limitations traceable to measurements
- [ ] `reproduce.py` regenerates the tables
- [ ] Model card included
- [ ] Licence of the data stated
- [ ] Prototype boundary stated if the domain is high-stakes

---

[Capstone home](README.md) · [Rubric](rubric.md) · [Report template](report-template.md)
