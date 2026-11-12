# L14-01 — AI in Practice: Case Studies, Hybrid and Neuro-Symbolic Systems

| | |
| :--- | :--- |
| Level | 400 |
| Study time | 90 minutes |
| Prerequisites | M06, M07, M13 |
| Code | `code/neurosymbolic.py` |

[← Module start](../README.md) · [Next: L14-02 From Model to Product: Serving, Compression and MLOps →](L14-02-from-model-to-product-mlops-and-serving.md)

## On this page

- [Why this lesson exists](#why-this-lesson-exists)
- [What you will be able to do](#what-you-will-be-able-to-do)
- [1. Four domains, four different failure modes](#1-four-domains-four-different-failure-modes)
- [2. Hybrid systems: the model inside a boundary](#2-hybrid-systems-the-model-inside-a-boundary)
- [3. Neuro-symbolic, measured](#3-neuro-symbolic-measured)
- [4. Explainable deep learning: attribution is not a reason](#4-explainable-deep-learning-attribution-is-not-a-reason)
- [5. Prototypes are not products](#5-prototypes-are-not-products)
- [Common mistakes](#common-mistakes)
- [Exercises](#exercises)
- [Self-check](#self-check)
- [Key terms](#key-terms)
- [Further reading](#further-reading)

[Module start](../README.md) · [Module home](../README.md) · [Next: L14-02 From Model to Product: Serving, Compression and MLOps →](L14-02-from-model-to-product-mlops-and-serving.md)

## Why this lesson exists

Every module so far taught a technique in isolation, on data chosen to make it work. Deployed
systems are not like that. They are part of a workflow, they answer to a policy, and the thing
that decides whether they are acceptable is often not the model at all.

This lesson has two halves. The first reads four application areas honestly: what the published
claim was, what evidence supported it, and what failed. The second builds the architecture most
real systems land on — a learned component inside a symbolic boundary — and measures why the
boundary matters.

## What you will be able to do

1. Read an applied AI claim and separate the metric from the claim.
2. Name the failure mode that each of the four application areas is most exposed to.
3. Choose between model-only, rules-only and hybrid designs, with a reason.
4. Explain why an attribution is not a reason, using integrated gradients against a policy.
5. Write an honest scope statement for a capstone in an applied domain.

---

## 1. Four domains, four different failure modes

| Domain | Typical claim | What the metric misses | Dominant failure |
| :--- | :--- | :--- | :--- |
| Health | "detects the condition at expert level" | the prevalence of the condition in the trial vs the clinic | shift in prevalence, silent subgroup error |
| Education | "predicts which students will fail" | whether the intervention actually helps | feedback loops and self-fulfilling prediction |
| Finance | "improves credit decisions" | who is denied, and why | label bias in historical decisions, regulatory duty |
| Agriculture | "identifies the disease from a photo" | field conditions: lighting, occlusion, novel pathogens | distribution shift, rare classes |

The pattern is the same in all four: **the model metric is measured on a curated sample, while
the harm happens on the population the system actually meets.** Prevalence, feedback, base
rates and shift are the four ways that gap opens.

Three questions to ask of any applied claim:

1. What is the *decision* the system changes, and who bears its error?
2. What was the evaluation sample, and how was it collected?
3. What happens to the system when the input distribution moves?

If a paper or a vendor cannot answer all three, the claim is a demonstration, not a result.

### Health

A model that reports 0.95 AUC on a balanced research cohort can behave very differently where
prevalence is 2%. Precision collapses as prevalence falls, so a "95% accurate" screen can produce
more false alarms than true cases. The clinical question is not accuracy; it is the trade between
missed cases and the cost of follow-up, and that trade belongs to clinicians, not to the model.

**What to demand:** the prevalence in the evaluation set, per-subgroup sensitivity, and a
statement of intended use that excludes diagnosis.

### Education

Early-warning systems predict failure from engagement data. The prediction is easy; the
intervention is hard. Two specific hazards:

- **Feedback loop.** If advisors act on the score, the score changes the outcome it predicts. A
  model trained on historical data will look accurate while the intervention does the work.
- **Proxy capture.** Attendance and tutoring access correlate with disadvantage. M13 measured
  exactly this: dropping the proxy moved the demographic-parity gap from 0.026 to 0.009.

**What to demand:** an evaluation of the intervention, not just the predictor, and a subgroup
table.

### Finance

Credit models are the most regulated ML in common use. Two things follow. First, the reason for
a denial is a legal artefact, so attribution methods must be defensible to a regulator — M13
showed that Shapley and LIME can rank the same features in opposite orders. Second, the label
("repaid") is observed only for applicants who were granted credit, which is a selection effect,
not ground truth.

**What to demand:** the definition of the label, the treatment of rejected applicants, and the
adverse-action reason given to each person.

### Agriculture

Field images are the hardest distribution in this list: lighting, occlusion, growth stage and
novel pathogens. A model trained on curated leaf images can be excellent in the lab and useless
at 06:00 in a wet field. The mitigation is not a better architecture; it is data collected in
the deployment conditions and a fallback when confidence is low.

**What to demand:** field-collected test data, a per-class table, and an abstention path.

---

## 2. Hybrid systems: the model inside a boundary

A **hybrid system** combines learned components with explicit ones. Four patterns recur:

| Pattern | Structure | Use when |
| :--- | :--- | :--- |
| Gate | model ranks, rules decide | a policy must be satisfied exactly |
| Constrained output | model proposes, a checker rejects | outputs have hard validity rules |
| Retrieval + symbolic | text retrieval feeds a rule engine | the reason must cite a source |
| Ensemble of paradigms | statistical and rule-based scores combined | each covers the other's blind spot |

The gate is the most common and the least glamorous. It is also the only one that gives a
guarantee you can state to an auditor: **no output violates the policy**.

## 3. Neuro-symbolic, measured

`neurosymbolic.py` builds a benefit-eligibility decision with a published policy:

$$
\text{eligible} = (\text{income} < 25000 + 5000\cdot\text{household})
\;\wedge\; (\text{savings} < 3000)
\;\wedge\; \neg(\text{owns property} \wedge \text{income} > 18000).
$$

6,000 synthetic applicants; 3% of historical decisions deviate from policy, as caseworker
judgement does. Three designs:

```text
design             accuracy   policy violations   extra refusals
rules only            0.972                   0                0
model only            0.877                 100                0
hybrid                0.931                   0              100
```

Read the table in order:

- **Rules only beat the model on accuracy** (0.972 vs 0.877), because the labels are the policy
  plus 3% noise. The model is learning noise it cannot recover. This is not a failure of neural
  networks; it is a failure to ask whether a model was needed.
- **The model emits 100 decisions the policy forbids** — 100 people approved who were not
  eligible. In a deployed system that is not an accuracy statistic, it is 100 wrongful payments.
- **The hybrid is strictly compliant and less accurate**, and the 100 "extra refusals" are the
  price: people the caseworker had approved, refused by the rule.

That last column is the honest cost of compliance, and it is borne by individuals. Any proposal
to add a gate should state it.

### When the model does earn its place

The demo's labels are the policy, so rules win. Real cases differ where the policy has soft
edges: a rule cannot read a caseworker's note, and a model cannot certify compliance. The
architecture that works is:

1. the rule decides anything it can decide;
2. the model handles the residual cases, with a confidence threshold;
3. anything below threshold goes to a person;
4. every decision records which path it took.

That is unglamorous and it is what regulators can actually audit.

## 4. Explainable deep learning: attribution is not a reason

For one policy-violating approval, integrated gradients against the model gave:

```text
applicant: income 33,163, savings 0, household 1, owns property 0
model probability 0.718; policy says ineligible
  savings/1k       +0.457
  household        -0.230
  owns property    +0.203
  income/10k       +0.035
```

The binding rule is the income cap: 33,163 against a limit of 30,000. The attribution puts income
*last*. Both are correct statements about the model, and only one is the reason for the decision.

This distinction has a name in regulation: an **adverse action reason** must be the factor that
actually decided the outcome. A saliency map ranks sensitivity; it does not identify the binding
constraint. If you must give a reason, compute it from the decision rule, or from a
counterfactual ("you would have been eligible had your income been below 30,000"), not from a
gradient.

Use attribution for debugging and for finding surprising reliance. Use rules and counterfactuals
for accountability.

## 5. Prototypes are not products

A research prototype and a production system differ in ways that no metric captures:

| Prototype | Product |
| :--- | :--- |
| one curated dataset | a pipeline with provenance and versioning |
| accuracy on a held-out split | monitoring, drift alarms, rollback |
| notebook | service with latency, auth, logging |
| author can explain it | documentation someone else can audit |
| "works on my data" | works on the distribution the users bring |

M13's audit checklist is the bridge between the two. If you cannot fill it, you have a prototype,
and calling it anything else is the failure this module is designed to prevent.

## Common mistakes

| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Quoting one accuracy number for an applied claim | hides prevalence and subgroup effects | report the evaluation sample and per-group results |
| Adding a model where a rule suffices | 100 policy violations, lower accuracy | compare against the rule baseline first |
| Treating saliency as an explanation of the decision | wrong adverse-action reason | use the binding constraint or a counterfactual |
| Evaluating on curated data only | field failure | collect in deployment conditions |
| Presenting a prototype as deployable | harm and liability | state the evidence gap explicitly |

## Exercises

**Beginner.** Run `python neurosymbolic.py`. Copy the three-design table and explain, in one
sentence each, why rules beat the model and why the hybrid is still preferable for deployment.

**Beginner.** Change the label-noise rate from 3% to 15% and rerun. At what noise level does the
model overtake the rules?

**Intermediate.** Tighten the savings cap to 1,500 and rerun. Which design loses most accuracy,
and why is that the expected direction?

**Intermediate.** Add a second rule (applicants under 18 are ineligible). Does the hybrid remain
compliant? What breaks first?

**Advanced.** Replace integrated gradients with a counterfactual explanation ("the smallest
change that would make this applicant eligible") and compare it with the rule trace. Which is
more useful to the applicant, and which is more defensible to an auditor?

**Advanced.** Construct a synthetic case where the model *does* beat the rules — a soft policy
signal the rules cannot express — and report the accuracy gain alongside the violation rate.

## Self-check

1. Why can a 0.95 AUC model be a poor screen at 2% prevalence?
2. What is the feedback-loop hazard in an early-warning system?
3. State the guarantee a gate provides, and its cost.
4. Why did the attribution rank income last when income was binding?
5. Name three things a prototype lacks that a product needs.

## Key terms

**Hybrid system**, **neuro-symbolic AI**, **rule gate**, **constrained output**,
**adverse action reason**, **integrated gradients**, **binding constraint**,
**feedback loop**, **distribution shift**, **prototype**.

## Further reading

- Topol (2019). *High-performance medicine: the convergence of human and artificial intelligence*.
- Obermeyer et al. (2019). *Dissecting racial bias in an algorithm used to manage the health of
  populations* — the prevalence and label problem in one paper.
- Kautz (2022). *The Third AI Summer* — a readable case for neuro-symbolic architectures.
- Sundararajan, Taly & Yan (2017). *Axiomatic Attribution for Deep Networks* — integrated
  gradients.

---

**Navigation:** [← Module start](../README.md) · [Next: L14-02 From Model to Product: Serving, Compression and MLOps →](L14-02-from-model-to-product-mlops-and-serving.md)
