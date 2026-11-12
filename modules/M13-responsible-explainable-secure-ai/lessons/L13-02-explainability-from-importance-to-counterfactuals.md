# L13-02 — Explainability: From Importance to Counterfactuals

| | |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | L13-01, logistic regression, basic trees |
| Code | `code/explain.py`, `code/rai_data.py` |

[← Previous: L13-01 Responsible AI, Fairness and Bias](L13-01-responsible-ai-fairness-and-bias.md) · [Module home](../README.md) · [Next: L13-03 Privacy, Memorisation and Model Attacks →](L13-03-privacy-memorisation-and-model-attacks.md)

## On this page

- [Why this lesson exists](#why-this-lesson-exists)
- [What you will be able to do](#what-you-will-be-able-to-do)
- [1. Two models, same features](#1-two-models-same-features)
- [2. Global: permutation importance](#2-global-permutation-importance)
- [3. Global: partial dependence](#3-global-partial-dependence)
- [4. Local: Shapley values](#4-local-shapley-values)
- [5. Local: LIME](#5-local-lime)
- [6. Counterfactuals](#6-counterfactuals)
- [7. Do explanations pass their own tests?](#7-do-explanations-pass-their-own-tests)
- [8. Reporting explainability](#8-reporting-explainability)
- [Common mistakes](#common-mistakes)
- [Exercises](#exercises)
- [Self-check](#self-check)
- [Key terms](#key-terms)
- [Further reading](#further-reading)

## Why this lesson exists

"Explainable AI" is often sold as one thing. It is at least four: a global summary of what a
model relies on, a local account of one prediction, a check on whether that account is
faithful, and a concrete alternative the person could act on. They answer different
questions and routinely disagree — in this lesson, the two most popular methods rank the same
features in opposite orders on the same prediction.

You will implement each method from scratch so the mechanism is visible, and evaluate each
one instead of trusting it.

## What you will be able to do

1. Choose between an interpretable model and a post-hoc explanation, with the trade-off named.
2. Compute permutation importance, partial dependence and exact Shapley values.
3. Implement LIME and say precisely what its ridge coefficients mean.
4. Measure fidelity, stability and a label-shuffling sanity check.
5. Produce a counterfactual and judge whether it is actionable.
6. Explain why two correct methods can disagree.

---

## 1. Two models, same features

`explain.py` trains both on the synthetic student data:

```text
  logistic regression : accuracy 0.798 AUC 0.777
  gradient boosting   : accuracy 0.792 AUC 0.768
```

The readable model is not worse here. That is worth internalising: *if a linear model
performs as well, use it*. Post-hoc explanation exists for the cases where it does not —
images, text, large ensembles — and every post-hoc method is an approximation with an error
term you must report.

The logistic coefficients are the explanation:

```text
  tutoring_access      +...   (positive, largest)
  prior_attainment     +...
  attendance_rate      +...
  study_hours          +...
```

Sign and magnitude, no sampling, no surrogate. This is **transparency by construction**, and
it is the strongest form of explanation available.

## 2. Global: permutation importance

Shuffle one feature, measure how much the metric drops. Model-agnostic, no gradients, no
retraining.

$$
I_j=\frac1K\sum_{k=1}^{K}\Big(\text{AUC}(f,X,y)-\text{AUC}(f,X^{(k)}_{\text{perm }j},y)\Big).
$$

Measured on the gradient-boosted model (test set, 5 repeats):

```text
  tutoring_access      AUC drop +0.1445 (sd 0.0153)
  prior_attainment     AUC drop +0.0620 (sd 0.0062)
  study_hours          AUC drop +0.0514 (sd 0.0057)
  attendance_rate      AUC drop +0.0074 (sd 0.0035)
```

Two cautions, both visible in those numbers:

- **Correlated features split credit.** Attendance matters causally but barely matters here,
  because `study_hours` and `prior_attainment` carry the same signal; shuffling one leaves
  the others intact. Importance is *unique* contribution, not total influence.
- **Shuffling creates impossible rows.** A permuted attendance rate is averaged over an
  unrealistic joint distribution. Report it as a sensitivity measure, not a causal claim.

Use AUC rather than accuracy for the metric: accuracy saturates near 0.8 here and hides
differences that AUC exposes.

## 3. Global: partial dependence

Average the prediction while sweeping one feature over its observed range:

$$
\text{PD}_j(v)=\frac1n\sum_{i=1}^{n} f(x_i \text{ with } x_{ij}=v).
$$

It answers "on average, how does the prediction move with this feature?" It assumes the
feature is independent of the others — false for correlated inputs, which is why PDP and
permutation importance disagree about attendance. For correlated features use ICE curves or
accumulated local effects.

## 4. Local: Shapley values

Shapley values come from cooperative game theory. Treat features as players, the prediction
as the payout, and ask what each player contributed across all orderings:

$$
\phi_j=\sum_{S\subseteq F\setminus\{j\}}\frac{|S|!\,(|F|-|S|-1)!}{|F|!}
\Big[v(S\cup\{j\})-v(S)\Big],
$$

where $v(S)$ is the model output with features in $S$ taken from the instance and the rest
from a background distribution. Exact enumeration costs $2^{|F|}$ evaluations: trivial for
4 features, hopeless for 400, which is why KernelSHAP samples coalitions instead.

Measured for test instance 830 (prediction 0.498, close to the boundary):

```text
  prediction 0.4978  base 0.7156  sum(phi) -0.2177
    study_hours          -0.1581
    prior_attainment     -0.0397
    attendance_rate      -0.0199
    tutoring_access      +0.0000
  efficiency gap: 0.00e+00
```

Read it as a ledger: the average student is predicted at 0.716; this student's study hours
pull the prediction down by 0.158, prior attainment by 0.040, attendance by 0.020, and
tutoring access by nothing, landing at 0.498.

**The efficiency property** $\sum_j\phi_j=f(x)-\mathbb{E}[f]$ is the check that catches
broken implementations. A sampler that misses it is not producing Shapley values, whatever
the library says. This implementation hits it exactly (gap 0.00e+00) because it enumerates.

Shapley values satisfy dummy, symmetry, additivity and efficiency. They do **not** give
causality, and they inherit whatever correlation structure the background set has.

## 5. Local: LIME

Fit a sparse linear model to the black box in the neighbourhood of one instance:

1. Sample binary vectors indicating "keep the original value" or "replace with a training
   value".
2. Predict with the black box on each perturbed row.
3. Fit a weighted ridge regression, weighting by proximity to the instance.
4. Report the coefficients as the explanation.

Measured for the same instance:

```text
    tutoring_access      -0.128
    study_hours          -0.120
    attendance_rate      -0.060
    prior_attainment     -0.009
  local R^2 (fidelity to the black box): 0.259
  stability across 5 seeds: mean r 0.972 (min 0.939, max 0.998)
```

**The disagreement.** Shapley ranks study hours first (−0.158) and tutoring access last
(0.000). LIME ranks tutoring access first (−0.128) and prior attainment last. Both are
correct implementations. They answer different questions:

- LIME: *what linear story fits this neighbourhood?* It samples rows with features randomly
  replaced, so it measures influence **relative to the training distribution** — and in that
  distribution, tutoring access co-varies with the outcome.
- Shapley: *what is each feature's fair share of this prediction?* It averages marginal
  contributions over coalitions, so a feature that is redundant given the others gets little.

`local R² = 0.259` is the honest headline: the linear surrogate explains about a quarter of
the variance of the black box in that neighbourhood. A local explanation that fits badly is
a story about the neighbourhood, not the model. Report fidelity with every LIME output.

Stability is good here (mean r 0.972), but note the minimum, 0.939: five seeds, five
different rankings at the margins. Seed your sampler and say so.

## 6. Counterfactuals

A counterfactual is the nearest input that changes the decision:

```text
  original probability 0.498; seeking outcome 1
    change prior_attainment     60.06 -> 60.44
  distance 0.034 sd, new probability 0.541
```

The student is 0.002 below the threshold; a 0.38-point change in prior attainment flips the
prediction. That is a *fragile* decision, and the explanation exposes it: a model whose
decision turns on 0.38 points of a noisy measurement is not making a meaningful judgement.

Judge counterfactuals on three axes:

| Axis | Question | Failure |
| :--- | :--- | :--- |
| Proximity | how far is the change? | distant changes are not explanations |
| Actionability | can the person act on it? | "change your group" is not advice |
| Plausibility | is the result a realistic person? | counterfactuals can leave the data manifold |

Always report proximity. A counterfactual at 0.034 sd is an explanation; one at 3 sd is an
artefact of the search.

## 7. Do explanations pass their own tests?

Three tests, all cheap:

**Fidelity.** Does the surrogate reproduce the model locally? Measured: LIME $R^2=0.259$.
Low fidelity means the explanation is not about the model.

**Stability.** Do explanations survive reseeding? Measured: mean $r=0.972$ for LIME. Shapley
with exact enumeration is deterministic; sampled Shapley is not, and its variance is a
reportable quantity.

**Sanity (label shuffling).** Retrain on shuffled labels. A correct importance method must
collapse:

```text
  real model      AUC 0.731  max importance +0.1568
  shuffled-label  AUC 0.459  max importance +0.0111
```

Importance falls by more than an order of magnitude while AUC falls to chance. Any method
that keeps reporting structure after labels are randomised is measuring the data, not the
model. Run this test once per method, before you trust it.

## 8. Reporting explainability

A usable explainability section contains:

1. Which model, and why it is not interpretable by construction.
2. One global method with its metric and the correlation caveat.
3. One local method, the instance, and the fidelity value.
4. A stability number and the seeds used.
5. A sanity check.
6. A counterfactual with distance and actionability.
7. What the explanation does **not** show — causality, or behaviour outside the training
   distribution.

## Common mistakes

| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Calling an explanation causal | wrong interventions | say "sensitivity", test interventions |
| Reporting LIME without fidelity | unfalsifiable story | report $R^2$ by the instance |
| Trusting one seed | ranking instability | repeat, report variance |
| Using accuracy for importance | saturation hides effects | use AUC or log-loss |
| Skipping the shuffle test | silently broken method | always run it |
| Single-feature counterfactuals only | misses joint changes | allow up to 3, report distance |

## Exercises

**Beginner.** Run `python explain.py`. Copy the permutation table and write one sentence per
feature explaining its drop, including the correlation caveat.

**Beginner.** Change `n_grid` in the partial dependence call and describe how the curve
changes. Does the shape or only the resolution change?

**Intermediate.** Implement KernelSHAP properly: sample coalitions with the kernel weight
$\pi(S)=(|F|-1)/(\binom{|F|}{|S|}|S|(|F|-|S|))$, solve for $\phi$, and compare with the exact
values. Report the efficiency gap as a function of the number of samples.

**Intermediate.** Increase the LIME `n_samples` from 800 to 4000. What happens to local $R^2$
and to stability? Is the extra cost worth it?

**Advanced.** Build a counterfactual that changes at most two features *and* lands on a
realistic row (nearest neighbour in the training set within 1 sd). Compare its distance to
the unconstrained one.

**Advanced.** Repeat the sanity check with a model trained on 5% of the data. Does the
shuffled-label importance stay near zero?

## Self-check

1. Why is the logistic regression not "less explainable" than boosting here?
2. State the efficiency property and explain why a broken KernelSHAP violates it.
3. Give one reason Shapley and LIME disagree that is not an implementation bug.
4. What does a local $R^2$ of 0.259 license you to claim?
5. A counterfactual requires changing group. What do you do with it?

## Key terms

**Interpretable model**, **post-hoc explanation**, **feature importance**,
**permutation importance**, **partial dependence**, **ICE**, **Shapley value**,
**KernelSHAP**, **efficiency property**, **LIME**, **local surrogate**, **fidelity**,
**stability**, **counterfactual**, **actionability**, **sanity check**.

## Further reading

- Molnar, *Interpretable Machine Learning* (2nd ed.) — the reference for PDP, ICE and
  permutation importance.
- Lundberg & Lee (2017). *A Unified Approach to Interpreting Model Predictions*.
- Ribeiro, Singh & Guestrin (2016). *"Why Should I Trust You?": Explaining the Predictions
  of Any Classifier* — LIME, plus the fidelity discussion.
- Wachter, Mittelstadt & Russell (2017). *Counterfactual Explanations without Opening the
  Black Box*.

---

[Previous: L13-01](L13-01-responsible-ai-fairness-and-bias.md) · [Module home](../README.md) ·

---

**Navigation:** [← Previous: L13-01 Responsible AI, Fairness and Bias](L13-01-responsible-ai-fairness-and-bias.md) · [Module home](../README.md) · [Next: L13-03 Privacy, Memorisation and Model Attacks →](L13-03-privacy-memorisation-and-model-attacks.md)
