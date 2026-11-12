# L14-05 — Capstone Studio: Scoping, Milestones and Defence

| | |
| :--- | :--- |
| Level | 400 |
| Study time | 90 minutes |
| Prerequisites | L14-01 to L14-04 |
| Artefacts | [`capstone/`](../capstone/README.md): briefs, rubric, milestones, report template |

[← Previous: L14-04 Reading and Reproducing AI Research](L14-04-reading-and-reproducing-ai-research.md) · [Module end](../README.md)

## Why this lesson exists

Most capstone projects fail for a reason that has nothing to do with modelling: the scope was
too large, the data arrived late, the evaluation was never defined, or the demo is the only thing
that got built. This lesson is the project-management half of the module, and it is deliberately
prescriptive, because "be pragmatic about scope" is not actionable and "cut feature three" is.

## What you will be able to do

1. Turn a brief into a scoped proposal with a falsifiable evaluation plan.
2. Set milestones that produce evidence rather than activity.
3. Choose a dataset you can actually obtain and defend its licence.
4. Present a project with its limitations stated first.
5. Apply the rubric to your own work before someone else does.

---

## 1. Choosing a brief

Twelve briefs are provided across three levels in [`capstone/briefs/`](../capstone/briefs/).
Choose by constraint, not by ambition:

| Your situation | Choose |
| :--- | :--- |
| Little time, want a solid result | beginner brief, one dataset, one model, honest evaluation |
| Comfortable with the pipeline | intermediate brief with a retrieval or deployment component |
| Strong base, want a research flavour | advanced brief with a measured comparison and a limitation study |

The level is about the *evidence you will produce*, not the difficulty of the model. A beginner
brief done with a subgroup table, a baseline and a limitations section scores higher than an
advanced brief with a demo and no evaluation.

**Do not pick a brief whose data you cannot get this week.** Data acquisition is the most common
cause of a failed capstone. If the dataset requires an application, an ethics approval or a
partner organisation, choose something else unless the approval is already in hand.

## 2. Scope: the one-page test

Write the proposal, then check it against these five tests. If any fails, cut scope until it
passes.

| Test | Passes when | Fails when |
| :--- | :--- | :--- |
| One-sentence goal | you can say what will be true at the end | the sentence contains "and" twice |
| Data available | you have the files or a confirmed download | "we will collect it" |
| Baseline named | a trivial method exists to beat | no comparison |
| Metric defined | one number decides success | "we will evaluate qualitatively" |
| Failure condition | you can state what would count as a negative result | every outcome is success |

That last one matters most. A project with no failure condition cannot produce a finding, only a
demo.

### A worked scope

```text
Brief:        B-03 image classification application
Goal:         classify 10 crop-leaf conditions from field photos, and report where it fails
Data:         PlantVillage subset (CC BY-SA 3.0) plus 150 self-collected phone photos
Baseline:     logistic regression on colour histograms
Model:        small CNN, transfer learning from a pretrained backbone if available
Metric:       macro F1 on the field-photo set, with a per-class table
Failure:      if macro F1 on field photos is below 0.60, report the lab-vs-field gap as the finding
Deliverables: code, model card, 6-page report, 5-minute demo
Out of scope: deployment, mobile app, real-time inference
```

Note what the failure condition does: it converts a possible disappointment into a result. The
lab-versus-field gap is a legitimate finding and is more interesting than another 0.98 on a
curated dataset.

## 3. Milestones that produce evidence

Four milestones, each ending in an artefact you can show:

| Milestone | Ends with | Common failure |
| :--- | :--- | :--- |
| M1 Proposal | approved scope + evaluable metric | scope too broad to approve |
| M2 Data + baseline | working pipeline, baseline number | data cleaning ate the week |
| M3 Model + evaluation | main result, subgroup/per-class table | tuned without a baseline |
| M4 Report + demo | written report, demo, limitations | demo built, evaluation missing |

Front-load the boring risk. The pipeline that loads and splits the data correctly is worth more
than a better architecture, because without it no number is trustworthy.

**Weekly evidence rule.** Each week, produce one artefact: a plot, a metric, a table, a
paragraph of the report. Not a status update.

## 4. Evaluation plan

Your evaluation plan has four parts:

1. **Split.** How the data is divided, and why that split matches deployment (by time, by
   patient, by site — not randomly, if the real use is out-of-distribution).
2. **Metrics.** One primary metric tied to the decision, plus supporting metrics, plus a
   subgroup or per-class table.
3. **Baselines.** At least one trivial method, and one standard method.
4. **Uncertainty.** Confidence intervals, repeated runs, or an explicit statement that n is too
   small to distinguish the models.

A result without part 4 is a point estimate pretending to be a finding. With a test set of 100
examples, a 2-point difference in accuracy is noise.

## 5. The research-prototype boundary

Every capstone in this module is a **research prototype**. That is not a disclaimer to hide
behind; it is a statement about the evidence you have.

| A prototype has | A deployable system needs |
| :--- | :--- |
| one dataset | provenance, versioning, retraining |
| a held-out split | monitoring, drift alarms, rollback |
| offline metrics | latency, cost, failure modes in service |
| author-run evaluation | independent validation |
| a limitations paragraph | a risk register and an owner |

You may say: "this prototype achieves X on dataset Y under split Z, and here is where it fails."
You may not say: "this system is accurate for clinical use", "this is production-ready", or "this
detects fraud reliably" — unless you have the validation that those claims require, which a
one-semester capstone does not.

**High-stakes rule.** If a brief touches health, finance, law or safety, your report must state
explicitly that the prototype is not validated for those decisions, and must describe what
validation would require.

## 6. The report

Use [`capstone/report-template.md`](../capstone/report-template.md) and follow
[`capstone/report-writing.md`](../capstone/report-writing.md). Structure:

1. Problem and motivation (why this decision, for whom)
2. Related work (three to five papers, and what you borrowed)
3. Data (provenance, licence, split, known gaps)
4. Method (baseline, model, and why)
5. Results (primary metric, per-class table, uncertainty)
6. Error analysis (three concrete failures, explained)
7. Limitations and ethics (what this cannot support)
8. Reproduction (commands, seeds, environment)

Six pages excluding references. A report that is nine pages of method and half a page of results
has the proportions wrong.

## 7. The defence

Ten minutes, five slides, then questions:

| Slide | Content |
| :--- | :--- |
| 1 | the problem and who it affects |
| 2 | data and baseline, with the number |
| 3 | your method and the main result |
| 4 | where it fails (per-class or subgroup table) |
| 5 | limitations and what you would do next |

State a limitation before anyone asks. It signals that you know what your evidence supports, and
it is the single strongest thing you can do in a defence.

Anticipate these five questions:

1. What is your baseline, and is it tuned?
2. How large is your test set, and what is the uncertainty on your metric?
3. What happens on data from a different source?
4. What is the licence of your data, and can you redistribute the model?
5. Which of your claims would survive if your main result were 5 points worse?

## Common mistakes

| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Scope with no failure condition | no possible finding | state what a negative result looks like |
| Data not secured at M1 | project stalls at M2 | confirm access before proposing |
| Tuning before a baseline | cannot attribute improvement | baseline first, always |
| Random split for a deployment-time task | optimistic metrics | split as deployment does |
| No uncertainty | point estimate presented as fact | intervals or repeated runs |
| Demo-driven project | no evaluation, weak report | evaluation first, demo second |
| Claiming production readiness | overclaiming, and a marking penalty | state the prototype boundary |

## Exercises

**Beginner.** Take one brief from each level and write its five scope tests. Which one fails
first, and why?

**Beginner.** Rewrite a vague goal ("build an AI system for X") into a falsifiable one with a
metric and a failure condition.

**Intermediate.** For your chosen brief, list the three risks most likely to stop you and the
mitigation for each, with a date.

**Intermediate.** Define your evaluation split and justify it against the deployment setting. If
you chose randomly, defend that choice explicitly.

**Advanced.** Write the limitations section of your final report now, before doing the work.
Update it at M4 and compare.

**Advanced.** Prepare the five defence questions with your current numbers, and identify which
one you cannot answer yet.

## Self-check

1. What are the five scope tests?
2. Why does a failure condition improve a project?
3. What does each milestone have to produce?
4. What are the four parts of an evaluation plan?
5. Name three claims a capstone prototype cannot support.

## Key terms

**Scope**, **failure condition**, **baseline**, **primary metric**, **subgroup table**,
**uncertainty**, **milestone**, **research prototype**, **deployment boundary**,
**reproduction package**.

## Further reading

- [`capstone/rubric.md`](../capstone/rubric.md) — the marking scheme, read it before you start.
- [`capstone/milestones.md`](../capstone/milestones.md) — the four gates in detail.
- [`capstone/report-writing.md`](../capstone/report-writing.md) — structure and worked examples.
- Pineau et al. (2021). *Improving Reproducibility in Machine Learning Research*.

---

[Previous: L14-04](L14-04-reading-and-reproducing-ai-research.md) · [Module home](../README.md) ·
[Proposal](../assignments/asg-14-capstone-proposal.md)

---

**Navigation:** [← Previous: L14-04 Reading and Reproducing AI Research](L14-04-reading-and-reproducing-ai-research.md) · [Module end](../README.md)
