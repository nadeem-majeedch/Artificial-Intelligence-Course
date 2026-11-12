# L13-01 — Responsible AI, Fairness and Bias

| | |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | M07 (evaluation), basic statistics |
| Code | `code/rai_data.py`, `code/fairness.py` |

[← Module start](../README.md) · [Next: L13-02 Explainability: From Importance to Counterfactuals →](L13-02-explainability-from-importance-to-counterfactuals.md)

## On this page

- [Why this lesson exists](#why-this-lesson-exists)
- [What you will be able to do](#what-you-will-be-able-to-do)
- [1. What "responsible AI" covers](#1-what-responsible-ai-covers)
- [2. The synthetic recruitment dataset](#2-the-synthetic-recruitment-dataset)
- [3. Four metrics, and what each one misses](#3-four-metrics-and-what-each-one-misses)
- [4. The audit](#4-the-audit)
- [5. Three mitigations, measured](#5-three-mitigations-measured)
- [6. A procedure you can reuse](#6-a-procedure-you-can-reuse)
- [Common mistakes](#common-mistakes)
- [Exercises](#exercises)
- [Self-check](#self-check)
- [Key terms](#key-terms)
- [Further reading](#further-reading)

[Module start](../README.md) · [Module home](../README.md) · [Next: L13-02 Explainability: From Importance to Counterfactuals →](L13-02-explainability-from-importance-to-counterfactuals.md)

## Why this lesson exists

A model that is 94.7% accurate can still allocate opportunity unfairly. Accuracy answers
"how often is the prediction right?"; fairness asks "who bears the errors?" Those are
different questions with different answers, and no single metric settles both.

This lesson builds the vocabulary of responsible AI, then makes it operational: you will
generate a synthetic recruitment dataset with a *known* bias mechanism, train a model on it,
measure four group metrics, and try three mitigations. Two of them behave in ways that
contradict the folklore, and the lesson is built around that surprise.

## What you will be able to do

By the end you can:

1. Distinguish fairness by unawareness, by group parity, and by equal error rates, and say
   why they can conflict.
2. Measure demographic parity difference, disparate impact ratio, equal opportunity and
   equalised odds on a real model.
3. Diagnose label bias, sampling bias and proxy bias from data alone.
4. Explain why pre-processing reweighing can leave a model's decisions unchanged.
5. Write a fairness statement that a reviewer could check.

---

## 1. What "responsible AI" covers

Responsible AI is not a single technique. It is a set of commitments that have to be
implemented, measured and governed. The parts that show up in this module:

| Commitment | Question it answers | Where it is measured here |
| :--- | :--- | :--- |
| Fairness | Are outcomes and errors distributed acceptably across groups? | L13-01, LAB-13-01 |
| Privacy | Does the system reveal things about the people in its data? | L13-03 |
| Transparency | Can an affected person get a reason for a decision? | L13-02 |
| Accountability | Who is answerable when it goes wrong? | L13-05 |
| Human oversight | Can a person stop or override it? | L13-04, L13-06 |
| Security | Can someone make it behave outside its purpose? | L13-04 |
| Safety | Are foreseeable harms identified and controlled? | L13-05 |
| Governance | Are there rules, owners, reviews and records? | L13-05, MP-13 |

These are not independent. A system with perfect explanations and no accountability is
theatre; a system with strong access control and a biased label is still discriminatory.

**Ethics is not compliance.** Compliance asks "is this permitted?". Ethics asks "should we
do this, and to whom is the harm distributed?". A system can be lawful and still wrong:
historically biased labels are legal to learn from.

---

## 2. The synthetic recruitment dataset

`code/rai_data.py` generates 4,000 applicants with four features and a binary label that
simulates **a human hiring decision**, not ability.

```text
recruitment: 4000 rows, 4 features, licence CC0-1.0
  label            : hired (a historical decision, not ground truth about ability)
  bias mechanism   : label bias: merit threshold 0.52 for group A, 0.62 for B
  positive rate    : 0.149
    group A: n= 2158 positive rate 0.219
    group B: n= 1842 positive rate 0.067
  ratio 0.307   difference 0.152
  feature means by group:
    experience_years          3.229 vs     3.241
    education_score          68.024 vs    68.045
    interview_score          60.140 vs    59.967
    referral                  0.283 vs     0.080
```

Read the feature means carefully. Experience, education and interview scores are
essentially identical across groups. Only `referral` differs: 0.283 versus 0.080.

That single feature is the whole mechanism. The label was produced by two different
thresholds on a latent merit score, so equally qualified applicants were hired at
different rates, and the model has exactly one feature that can learn the difference.

This is **label bias**, and it is the most common failure in deployed systems: the model
faithfully reproduces a decision process that was already unequal. No amount of model
inspection finds it — you have to look at the data-generating process.

### Three bias mechanisms, three symptoms

| Mechanism | How it appears | Diagnostic |
| :--- | :--- | :--- |
| Label bias | base rates differ, features look similar | compare positive rate to feature means |
| Sampling bias | one group under-represented | count rows per group before modelling |
| Proxy bias | a neutral feature correlates with group *and* predicts the label | correlate each feature with group, then ablate |

The student dataset in the same file is a proxy case: `tutoring_access` is group-correlated
and predictive, so removing it changes both accuracy and the disparity. You will measure
that in LAB-13-01.

---

## 3. Four metrics, and what each one misses

For a binary decision with a protected group $g$:

$$
\text{selection rate}_g=\Pr(\hat Y=1\mid G=g),\qquad
\text{DP difference}=\max_g s_g-\min_g s_g,
$$

$$
\text{disparate impact ratio}=\frac{\min_g s_g}{\max_g s_g},\qquad
\text{TPR}_g=\Pr(\hat Y=1\mid Y=1,G=g).
$$

- **Demographic parity (independence)** asks for equal selection rates. It ignores who
  deserved the positive outcome, so it can be satisfied by hiring at random.
- **Equal opportunity (separation)** asks for equal TPR: among qualified applicants, the
  same share is hired. It permits different selection rates when base rates differ.
- **Equalised odds** adds equal FPR: the cost of a false positive must also be shared.
- **Predictive parity (sufficiency)** asks for equal precision. It conflicts with the other
  two whenever base rates differ — this is the impossibility result of Kleinberg et al.
  (2016). You cannot have all of them, so **choosing a metric is an ethical decision, not a
  technical one**, and it belongs in the model card.

The 80% rule from US employment law is a screening heuristic: a disparate impact ratio
below 0.80 invites scrutiny. It is a floor for investigation, not a proof of fairness.

---

## 4. The audit

`code/fairness.py` trains logistic regression on a stratified 70/30 split:

```text
baseline
  accuracy 0.947  AUC 0.981  features ['experience_years', 'education_score', 'interview_score', 'referral']
  group      n  select    TPR    FPR    PPV   base
  A        657   0.172  0.745  0.016  0.929  0.215
  B        543   0.096  0.921  0.034  0.673  0.070
  DP difference 0.076   DI ratio 0.557   EOpp gap 0.176   EOdds gap 0.176
```

Four things to notice, because each one is a different lesson:

1. **Accuracy is excellent and the disparity is large.** 0.947 and a DI ratio of 0.557
   coexist. Accuracy is not a fairness metric.
2. **Selection rates differ by 7.6 points** (0.172 vs 0.096), so the model hires group A at
   nearly twice the rate.
3. **The TPR gap runs the other way.** Group B's true positive rate (0.921) is *higher* than
   group A's (0.745): qualified B applicants are more likely to be hired, because the model
   needs stronger evidence from them to cross the threshold. A naive "the model favours A"
   reading is wrong — it favours A in volume and B in per-qualified-applicant terms.
4. **Precision differs a lot** (0.929 vs 0.673), which is what a lower base rate does to a
   fixed threshold.

This is why one number is never enough. DP says discrimination; TPR says the opposite;
PPV says "of course, base rates differ". All three are true.

---

## 5. Three mitigations, measured

### 5.1 Reweighing (pre-processing) — no effect here

Kamiran–Calders reweighing assigns each (group, label) cell a weight inversely proportional
to how over-represented it is:

$$
w(g,y)=\frac{\Pr(G=g)\Pr(Y=y)}{\Pr(G=g,Y=y)} .
$$

Result:

```text
reweighed
  accuracy 0.947  AUC 0.981
  group      n  select    TPR    FPR    PPV   base
  A        657   0.172  0.745  0.016  0.929  0.215
  B        543   0.096  0.921  0.034  0.673  0.070
  DP difference 0.076   DI ratio 0.557   EOpp gap 0.176   EOdds gap 0.176
```

Identical to three decimal places. This is not a bug, and it is the most valuable result in
the lesson.

Reweighing balances the *marginal* label distribution it is given. The disparity here is
**conditional**: at equal merit, group B needs a higher score to be labelled positive.
Reweighing cannot see that, because it only looks at $P(Y\mid G)$, not at $P(Y\mid G,
\text{merit})$. And once the protected attribute is absent from the feature set, the model's
decision boundary is a single function of the four features — reweighting the loss cannot
rotate it.

**Rule of thumb:** pre-processing fixes *representation* problems, not *label* problems.
If the labels are the biased artefact, weighting rows reweights the bias faithfully.

### 5.2 Group-specific thresholds (post-processing) — works, at a cost

Choosing a separate decision threshold per group to equalise selection:

```text
balanced thresholds {'A': 0.375, 'B': 0.600}  gap 0.002  accuracy 0.954 (baseline 0.947)
```

The gap collapses from 0.076 to 0.002. Accuracy *rises* slightly, to 0.954, because the
threshold search is also a better global operating point than the default 0.5 — do not read
that as a general law; it is an artefact of this dataset and this split. On other data this
method costs accuracy.

Two objections you must be able to answer before using it:

- **It uses the protected attribute at decision time.** Legal in some jurisdictions for
  remediation, illegal in others. Check before shipping.
- **It produces different rules for different people**, which many find objectionable even
  when the outcome is fairer in aggregate.

### 5.3 Dropping the proxy — fixes parity, not error rates

Removing `referral`:

```text
recruitment without referral       0.892    0.004     0.168
```

DP difference falls from 0.076 to 0.004 and the DI ratio improves past 0.99. Accuracy falls
from 0.947 to 0.892 — a 5.5-point cost, and the honest price of not using the biased
shortcut.

But the **equal opportunity gap barely moves**, 0.176 to 0.168. The referral feature
explained *who got hired*; it did not explain why equally qualified people were treated
differently. Removing a proxy removes the symptom, not the label bias.

### 5.4 The summary table

```text
variant                         accuracy  DP diff  EOpp gap
recruitment baseline               0.947    0.076     0.176
recruitment reweighed              0.947    0.076     0.176
recruitment without referral       0.892    0.004     0.168
student with proxy                 0.798    0.026     0.021
student without proxy              0.793    0.009     0.009
loans                              0.672    0.010     0.015
```

No row dominates. Reweighing changes who is hired, not who is qualified; dropping a proxy
costs accuracy; balancing thresholds trades accuracy for parity and needs a legal basis.
Reporting this table is a fairness audit. Reporting only the row you like is not.

---

## 6. A procedure you can reuse

1. **Name the decision and the groups.** Before any model, write down what the model
   decides and which groups you will report. Two groups is the minimum; intersectional
   slices are better.
2. **Audit the data-generating process.** Who created the labels, under what policy, and
   with what threshold? Label bias lives here.
3. **Count before modelling.** Rows per group, positive rate per group, feature means per
   group. A table like the one in section 2.
4. **Train one baseline and report accuracy plus the decision-relevant metric.**
5. **Report all four group metrics.** Selection rate, TPR, FPR, PPV. Expect them to
   disagree; explain the disagreement.
6. **Try one mitigation of each type** and report the accuracy cost with it.
7. **Write a fairness statement**: metric chosen, why, measured gap, accepted threshold,
   who accepted it and when. That sentence is what an auditor asks for.

## Common mistakes

| Mistake | Why it is wrong | Do instead |
| :--- | :--- | :--- |
| Reporting accuracy as evidence of fairness | 0.947 with a 0.557 DI ratio | report group metrics alongside |
| Treating DP as *the* fairness metric | ignores base rates and qualification | state which definition you chose |
| Assuming reweighing fixes label bias | measured: no change at all here | fix the labels, or post-process |
| Dropping the protected attribute | proxies remain; disparity persists | ablate proxies and measure |
| Auditing only the deployed threshold | the ranking can be biased too | report AUC and calibration by group |
| Using one split | gaps move with sampling noise | report intervals or repeat splits |

## Exercises

**Beginner.** Run `python rai_data.py` and `python fairness.py`. Copy the baseline table into
a note and write one sentence for each of the four metrics saying who it favours.

**Beginner.** Change `random_state` in the split to 1, 2 and 3. Record the DP and equal
opportunity gaps for each. How much do they move without any change to the model?

**Intermediate.** Set the group-B merit threshold in `rai_data.recruitment()` to 0.52 (equal
to A) and regenerate. What happens to the raw positive-rate ratio, the baseline DP gap and
the equal opportunity gap? Which one moves most, and why?

**Intermediate.** Implement *random* selection at group A's rate for group B and measure
accuracy, DP and TPR. Explain why this satisfies one definition and destroys another.

**Advanced.** Extend `fairness.py` with a bootstrap over 200 resamples of the test set and
report 95% intervals for the DP difference. Is the 0.076 gap distinguishable from zero?

**Advanced.** Construct a dataset where reweighing *does* change the decision boundary, and
explain the structural difference from this one.

## Self-check

1. Why does the model's TPR favour group B while its selection rate favours group A?
2. State the impossibility result in one sentence and name the three properties.
3. Why is reweighing ineffective on this dataset? Answer in terms of what the weights see.
4. A colleague reports "DI ratio 0.99, no bias". Name two things you would still check.
5. Your model is 94.7% accurate. Write the next sentence of the model card.

## Key terms

**Responsible AI**, **algorithmic discrimination**, **label bias**, **sampling bias**,
**proxy variable**, **demographic parity**, **disparate impact ratio**, **80% rule**,
**equal opportunity**, **equalised odds**, **predictive parity**, **reweighing**,
**group-specific threshold**, **fairness statement**.

## Further reading

- Barocas, Hardt & Narayanan, *Fairness and Machine Learning* (fairmlbook.org) — chapters 2–4
  for definitions and the impossibility result.
- Kleinberg, Mullainathan & Raghavan (2016). *Inherent Trade-Offs in the Fair Determination
  of Risk Scores*.
- Kamiran & Calders (2012). *Data Pre-processing Techniques for Classification without
  Discrimination* — the reweighing method used here.
- US EEOC *Uniform Guidelines on Employee Selection Procedures* — the origin of the 80% rule.

---

**Navigation:** [← Module start](../README.md) · [Next: L13-02 Explainability: From Importance to Counterfactuals →](L13-02-explainability-from-importance-to-counterfactuals.md)
