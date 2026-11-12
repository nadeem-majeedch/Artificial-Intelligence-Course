# QUIZ-13 — Module Self-Check

| | |
| :--- | :--- |
| Time | 30 minutes |
| Questions | 15 |
| Format | short answer, closed book except for the module's own tables |

[Module home](../README.md) · [Summary](../summary.md)

Answer before reading the key. Numerical answers should be quoted to the precision used in the
module's output.

---

## Part A — Responsible AI and fairness (questions 1–5)

**1.** A recruitment model has accuracy 0.947 and a disparate impact ratio of 0.557. Explain in
two sentences why both statements can be true and why neither is sufficient.

**2.** The same model has selection rates 0.172 (group A) and 0.096 (group B), but TPRs 0.745
and 0.921. Which group does the model favour, and under which fairness definition?

**3.** Reweighing left every metric unchanged. Give the structural reason, in terms of what the
weights can see.

**4.** Dropping `referral` moved the DP difference from 0.076 to 0.004 while the equal
opportunity gap went from 0.176 to 0.168. What does this tell you about proxies?

**5.** The 80% rule flags a DI ratio below 0.80. Name one thing it does not tell you.

## Part B — Explainability (questions 6–9)

**6.** Exact Shapley values satisfied `sum(phi) = -0.2177` against an expected sum of −0.2177,
with an efficiency gap of 0.00e+00. What would a gap of 0.4 indicate?

**7.** For the same instance, Shapley ranked `study_hours` first (−0.1581) and LIME ranked
`tutoring_access` first (−0.128). Give one reason this is not an implementation bug.

**8.** LIME's local $R^2$ was 0.259. Write the sentence you would put in a report, including the
limitation.

**9.** The label-shuffling check gave max importance +0.1568 for the real model and +0.0111 for
the shuffled one. What would it mean if the shuffled value were +0.15?

## Part C — Security and privacy (questions 10–13)

**10.** Accuracy falls from 0.913 to 0.030 at $\varepsilon=0.2$. State what claim about the
model is now justified, and what claim is not.

**11.** The backdoored model had clean accuracy 0.917 and attack success rate 0.855. Why is
clean evaluation structurally unable to find it?

**12.** Membership inference returned AUC 0.513 with a train–test confidence gap of 0.009.
Explain the relationship between overfitting and this attack.

**13.** Prompt injection success fell from 0.83 to 0.17 under guardrails, and case I1 still
succeeded. Name the control that failed and the class of attack it cannot stop.

## Part D — Governance (questions 14–15)

**14.** The risk register shows R4 falling from 20 to 4 and R1 from 20 to 12. What determines
how far a residual can fall, and why is R1 stuck?

**15.** Name the three release outcomes and the one field that makes "conditional" meaningful.

---

## Answer key

**1.** Accuracy measures how often the prediction is right overall; the DI ratio compares
selection rates across groups, so a model can be right about most people while allocating
positive outcomes unevenly. Neither is sufficient: accuracy ignores distributional harm, and a
ratio ignores error rates and base rates.

**2.** Both readings are correct. Group A is favoured in volume (selection rate), group B in
per-qualified-applicant terms (TPR 0.921 vs 0.745): a qualified B applicant must clear a higher
bar, so those who do are more likely to be hired. The definitions are demographic parity and
equal opportunity respectively.

**3.** Reweighing balances the marginal label distribution $P(Y\mid G)$ it is given. The
disparity here is conditional — at equal merit, group B needed a higher score — and the
protected attribute is not a feature, so no reweighting of rows can rotate a decision boundary
that is a function of the four features alone.

**4.** Removing a proxy removes the *route* by which the model learned the disparity, not the
disparity's source. Parity improved because the biased shortcut was gone; the TPR gap persisted
because it comes from the labelling policy, which is unchanged.

**5.** It does not tell you whether the selection process is justified, whether error rates are
equal, whether the groups are comparable, or whether the ratio is stable across samples. It is
a screening heuristic, not a finding.

**6.** The explanation would not be a Shapley decomposition: the contributions would fail to add
up to the difference between the prediction and the baseline, which means the sampler or the
background distribution is wrong. Efficiency is the cheapest correctness check available.

**7.** They answer different questions. LIME fits a linear surrogate in a neighbourhood sampled
relative to the training distribution, so a feature that co-varies with the outcome there gets
weight; Shapley averages marginal contributions over coalitions, so a redundant feature gets
little. Neither is wrong.

**8.** "A local linear surrogate explains 26% of the variance of the black box around this
prediction; the ranking should be treated as indicative of this neighbourhood, not as a
decomposition of the model."

**9.** That the importance method is measuring structure in the data rather than in the learned
function — the classic symptom of leakage, a broken permutation, or a mis-specified metric.

**10.** Justified: this model is not robust to $\ell_\infty$ perturbations of size 0.2. Not
justified: "the model is insecure" in general, or any claim about attacks outside the tested
family and budget.

**11.** The trigger appears in a tiny fraction of inputs, so an evaluation on clean data never
exercises it. The model is *better* than baseline on the clean distribution; only a
trigger-aware test set can reveal the behaviour.

**12.** Membership inference exploits the confidence gap between seen and unseen records. With a
gap of 0.009 there is almost nothing to exploit, so the attack sits at chance (0.513). Defence
here is mostly the absence of overfitting.

**13.** The action allowlist held; the failed case is a **content** attack — the model was
allowed to answer, and the answer contained the attacker's string. Capability controls stop
actions, not text; content injections are mitigated downstream or by keeping secrets out of the
context.

**14.** How much the control actually changes the mechanism. R4's control (document-level access
control before retrieval) removes the disclosure path, so residual falls to low. R1's controls
(measurement and threshold review) detect and partially compensate but do not remove label
bias, so residual stays high — as L13-01 measured when reweighing changed nothing.

**15.** Release, conditional release, do not release. The field that makes "conditional"
meaningful is a dated, owned remediation condition; without a date and an owner it becomes a
permanent exception.

---

## Scoring

| Score | Meaning |
| ---: | :--- |
| 13–15 | ready for the assignment and the mini-project |
| 10–12 | reread the lesson named by each miss |
| 6–9 | redo LAB-13-01 and LAB-13-02 before continuing |
| 0–5 | work through L13-01 to L13-06 again; the numbers matter |

---

[Module home](../README.md) · [Summary](../summary.md) ·
[Assignment](../assignments/asg-13-model-card-and-audit-report.md)
