# LAB-13-01 — Fairness Audit of Three Models

| | |
| :--- | :--- |
| Time | 2.5 hours |
| Level | 300 |
| Prerequisites | L13-01, L13-02 |
| Code | `code/rai_data.py`, `code/fairness.py`, `code/explain.py` |

[Module home](../README.md) · [Lab 13-02](lab-13-02-security-and-prompt-injection-testing.md) · [Assignment](../assignments/asg-13-model-card-and-audit-report.md)

## Purpose

Audit three models on synthetic data — recruitment, student performance and loans — and
produce a fairness report that a reviewer could check. You will find that the three datasets
fail in three different ways, and that the mitigation which looks most principled is
sometimes the least effective.

**Ethics.** All data is synthetic and generated in-script (CC0-1.0). No real applicants,
students or borrowers are represented. Do not swap in real personal data for this lab; the
measurements would be valid but the privacy and legal position would not.

**Deliverable.** A report of at most 1,200 words plus tables, with the five sections in
section 6.

---

## 1. Setup

```bash
cd modules/M13-responsible-explainable-secure-ai/code
python rai_data.py       # writes data/rai_datasets.npz and dataset_cards.json
python fairness.py       # prints the audit tables used below
python explain.py        # for the explanation section
```

If `fairness.py` takes more than a minute, you are on a slow machine. The group-specific
threshold search is the expensive part: comment out the `choose_thresholds` call in `main()` to
skip it, and record in your report that you did.

**Readiness check.** You should be able to answer, before starting: what is a false positive
rate, and why does a base-rate difference change PPV at a fixed threshold?

## 2. Scenario 1 — recruitment bias (40 minutes)

Run the audit and record the baseline table. Then answer:

1. **Where is the bias?** Compare feature means by group. Which feature differs, and by how
   much? Express the referral gap in percentage points.
2. **Is the disparity in volume or in error rates?** Selection rates are 0.172 / 0.096; TPRs
   are 0.745 / 0.921. Explain in two sentences how both can be true.
3. **Apply reweighing.** Record every metric. Explain why nothing changed, referring to what
   the weights can and cannot see.
4. **Apply group thresholds.** Record the thresholds chosen (0.375 / 0.600), the resulting DP
   gap (0.002) and accuracy (0.954). State two objections to shipping this.
5. **Drop `referral`.** Record accuracy (0.892), DP (0.004) and EOpp (0.168). Explain why
   parity improved while the TPR gap barely moved.

**Write-up prompt.** You are the auditor. Your client wants to ship the baseline model because
it has 94.7% accuracy. Write the 120-word paragraph you would send.

## 3. Scenario 2 — student performance (35 minutes)

The student dataset contains a proxy: `tutoring_access` is group-correlated and predictive.

1. Record the with-proxy and without-proxy tables. Report the accuracy change (0.798 → 0.793)
   and the DP change (0.026 → 0.009).
2. The accuracy cost of dropping the proxy is **+0.004** — dropping it slightly *helped*. Is
   that a reason to drop it? Answer in terms of what the proxy measures and who it advantages.
3. Use `explain.py` to compute permutation importance. Where does `tutoring_access` rank
   (+0.1445 AUC drop, first)? What does that tell you about using importance as a guide to
   fairness?
4. Compute a counterfactual for a student just below the threshold. Report the distance. Is
   the decision robust or fragile?
5. Write one sentence for the model card that states the proxy decision and its measurement.

## 4. Scenario 3 — loan fairness and calibration (35 minutes)

The loans model is the least accurate (0.672) and the least disparate (DP 0.010).

1. Record the group table. Explain why selection rates (0.946 / 0.957) are almost equal while
   PPV differs (0.704 / 0.616).
2. **Calibration.** Group A: mean predicted 0.671, observed 0.693, Brier 0.206. Group B: mean
   predicted 0.674, observed 0.603, Brier 0.234. Which group is over-scored, and in which
   probability bin is the error largest? (Look at bin 0: predicted 0.553, observed 0.391.)
3. A model can be calibrated overall and miscalibrated by group. Explain how that happens.
4. If a loan officer uses the score to prioritise manual review, which group bears the cost of
   the miscalibration?
5. Propose one monitoring metric that would have caught this before deployment.

## 5. Comparing the three

Fill this table from your own runs:

| Dataset | Accuracy | DP diff | DI ratio | EOpp gap | Dominant failure |
| :--- | ---: | ---: | ---: | ---: | :--- |
| recruitment | | | | | |
| student | | | | | |
| loans | | | | | |

Then answer:

- Which dataset would you refuse to deploy, and on what grounds?
- Which mitigation worked best per dataset, and what did it cost?
- Is there any metric on which all three look acceptable? What does that tell you about
  single-metric reporting?

## 6. Report structure

1. **Summary** (100 words): the three verdicts.
2. **Method**: data, model, split, metrics, seeds. Enough for reproduction.
3. **Findings**: one subsection per dataset, each with its table and the three numbers that
   matter.
4. **Mitigations**: what you tried, what changed, what it cost.
5. **Recommendation**: per dataset, release / conditional / no release, with reasons and
   monitoring.

## 7. Reflection questions

Answer in a paragraph each.

1. Reweighing is the textbook pre-processing fix. It did nothing here. What does that tell you
   about the difference between a *representation* problem and a *labelling* problem?
2. Dropping the proxy improved parity and (slightly) accuracy. Why is "it costs nothing" a
   dangerous argument for removing a feature?
3. Group-specific thresholds produced a fairer outcome and a better accuracy. Why might a
   regulator still object?
4. The loans model is the most accurate at ranking and the least accurate in absolute terms
   (0.672). Which of those properties matters to a borrower?
5. If you could add one column to the dataset to make the audit conclusive, what would it be,
   and what would it cost to collect?

## 8. Marking criteria

| Criterion | Weight | What distinguishes a strong answer |
| :--- | ---: | :--- |
| Measurement | 30% | every number reproduced; seeds and split stated |
| Interpretation | 30% | explains *why* metrics disagree, not just what they are |
| Mitigation analysis | 20% | costs reported alongside benefits |
| Recommendation | 10% | specific, conditional, with monitoring |
| Reflection | 10% | engages with the uncomfortable trade-offs |

## 9. Common pitfalls

- Reporting only DP. It is the metric most likely to look fine while error rates diverge.
- Treating "accuracy unchanged" as "mitigation harmless" — reweighing changed nothing at all.
- Dropping the protected attribute and declaring the model blind. Proxies remain.
- Skipping calibration because accuracy looks acceptable.
- Quoting a number without the split and seed it came from.

---

[Module home](../README.md) · [Lab 13-02](lab-13-02-security-and-prompt-injection-testing.md) ·
[Quiz](../quizzes/quiz-13.md)
