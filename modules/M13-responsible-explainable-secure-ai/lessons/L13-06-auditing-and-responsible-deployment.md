# L13-06 — Auditing and Responsible Deployment

| | |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | L13-01 to L13-05 |
| Code | `code/governance.py` (checklist), all previous scripts |

[← Previous: L13-05 Governance, Risk and the AI Lifecycle](L13-05-governance-risk-and-the-ai-lifecycle.md) · [Module end](../README.md)

## Why this lesson exists

An audit is a claim-by-claim check that the evidence exists and says what the documentation
says it says. It is the point where every earlier lesson becomes a file, a number or a
missing row.

This final lesson is a rehearsal. You get a checklist of ten areas, a system with gaps in it,
and ninety minutes to find them and write a verdict. The most useful outcome is discovering
that a claim you believed — "we test for bias" — has no evidence behind it.

## What you will be able to do

1. Run a ten-item audit and produce a defensible pass/fail per item.
2. Distinguish a missing artefact from an inadequate one.
3. Write findings as observations, evidence, risk and required action.
4. Design monitoring that would catch the failures this module demonstrated.
5. State a release recommendation with conditions and an owner.

---

## 1. Safety fundamentals, in engineering terms

Safety is not the absence of attacks. It is the property that the system's behaviour stays
inside an acceptable envelope, including when inputs are unusual, adversarial, or outside the
training distribution.

Four concepts worth carrying:

- **Hazard**: a state that can cause harm (an unqualified applicant rejected; a confidential
  record disclosed).
- **Risk**: likelihood × severity of that hazard, in a stated context of use.
- **Control**: something that prevents, detects or mitigates the hazard. Every control has a
  cost and a failure mode.
- **Residual risk**: what remains after controls, which must be accepted by a named person.

The engineering consequence: **you cannot evaluate safety without a threat model and a
context of use**. "Is this model safe?" is not answerable. "Is this model safe for shortlisting
interview candidates, given a human makes the final decision, with these controls?" is.

## 2. The ten-item audit

`governance.py` defines the checklist and counts missing evidence:

```text
# Audit checklist
| # | Area | Requirement | Evidence | Status |
| 1 | Purpose and scope | ... | model-card.md#intended-use | complete |
...
**Missing evidence: 3 of 10 items.**
```

The demo supplies evidence for 7 of 10 areas; the three gaps are deliberate. Run it and find
them:

```text
$ python governance.py
...
audit status:
  evidence provided for 7 of 10 areas
```

For each item, the audit asks three questions:

| Question | Passes when | Fails when |
| :--- | :--- | :--- |
| Does the artefact exist? | file, link or record | "we discussed it" |
| Does it contain the required content? | the specific metric or field | a heading with no numbers |
| Is it current? | dated within the review cycle | references a previous model version |

An audit that only checks existence is a filing exercise. The second question is where most
findings come from: a fairness section that names a metric but reports no gap, a security
section that lists attacks but no results.

## 3. Writing a finding

Four fields, in this order:

```text
Finding F-03 — Subgroup performance not reported
Observation: model-card.md reports accuracy 0.798 overall; no per-group table.
Evidence: fairness.py prints per-group selection rate, TPR, FPR and PPV; not transcribed.
Risk: disparity of 0.026 in selection rate and 0.021 in TPR is invisible to a reader.
Severity: high (release blocker for a decision affecting access).
Action: transcribe the subgroup table into the model card; re-audit within 5 working days.
```

Note what makes it usable: it names a file, a number and an owner-action, and it links the
gap to a harm. "Documentation could be improved" is not a finding.

## 4. What monitoring would have caught the failures in this module

Each failure mode from L13-01 to L13-05 has a monitor that would surface it:

| Failure | Monitor | Trigger |
| :--- | :--- | :--- |
| Recruitment label bias | selection rate by group, weekly | >5 point shift, or DI ratio < 0.80 |
| Proxy feature creep | correlation of each feature with group, on every retrain | new feature with \|r\| > 0.3 |
| Silent accuracy loss under attack | accuracy on a canary adversarial set | drop >10 points |
| Backdoored model | evaluation on data collected after model receipt | any targeted-class error spike |
| Prompt injection success | rate of actions attempted outside the allowlist | any non-zero |
| RAG leakage | canary confidential document in the index | any verbatim match in output |
| Distribution drift | PSI or KS on each feature, weekly | PSI > 0.2 |
| Calibration drift | Brier score by group, monthly | Brier gap > 0.05 |

Monitoring is not a dashboard. It is a metric, a threshold, an alert destination and a
documented response. Without the last two it is decoration.

The loans model in L13-01 is a good example of why calibration monitoring matters: group A's
mean predicted probability was 0.671 against an observed rate of 0.693 (Brier 0.206), while
group B's was 0.674 against 0.603 (Brier 0.234). Overall accuracy, 0.672, hides a group whose
scores are systematically too high in the lowest bin (predicted 0.553, observed 0.391).

## 5. Human-in-the-loop, specified

A HITL control needs five properties to be auditable:

1. **Trigger**: which decisions require review (all rejections; all scores within ±0.05 of the
   threshold).
2. **Information**: what the reviewer sees (score, top three features, nearest counterfactual,
   the applicant's file).
3. **Authority**: the reviewer may override without justification penalty; overrides are
   recorded.
4. **Timeliness**: a maximum time-to-decision, and a workload model that makes it feasible.
5. **Recourse**: the affected person can request review, with a published route and deadline.

Measured oversight: approval rate, override rate, time per case, and disagreement between
reviewer and model. A 99.7% approval rate is not evidence of quality; it is evidence that the
review is not doing anything.

## 6. Deployment decisions, with conditions

Three outcomes, not two:

| Outcome | Meaning | Requires |
| :--- | :--- | :--- |
| Release | evidence complete, residual risk acceptable | owner sign-off |
| Release with conditions | specific gaps with dated remediation | named acceptor per condition |
| Do not release | critical residual, or missing evidence for a high-severity hazard | documented reason |

"Release with conditions" is where most real systems land, and it is the easiest to abuse:
conditions without dates and owners become permanent. Write them as tickets.

```text
Decision: release with conditions
Conditions:
  C1 per-group table in model card — owner: modelling lead — due: 5 working days
  C2 canonical adversarial set in CI — owner: ML engineer — due: 10 working days
  C3 appeal route published — owner: product — due: before first external user
Acceptor: <role>, <date>
Review: 30 days, then quarterly
```

## 7. Responsible deployment, end to end

The full sequence this module has built, as a checklist you can actually run:

1. **Frame the decision.** What changes for a person because of this system? Is a model needed?
2. **Audit the data.** Provenance, licence, group counts, label policy (L13-01).
3. **Train a baseline, report the decision-relevant metric and a subgroup table** (L13-01).
4. **Explain it.** Global and local, with fidelity and stability (L13-02).
5. **Attack it.** Evasion, poisoning, injection, tool abuse (L13-04).
6. **Measure privacy.** Membership inference, extraction where relevant (L13-03).
7. **Document.** Model card, datasheet, risk register (L13-05).
8. **Design oversight.** Trigger, information, authority, timeliness, recourse (this lesson).
9. **Instrument monitoring.** Metrics, thresholds, alerts, response (this lesson).
10. **Decide and record.** Release, conditions, acceptor, review date.

Steps 3 to 6 are the ones that produce numbers. Steps 1, 7, 9 and 10 are the ones that
determine whether the numbers matter.

## Common mistakes

| Mistake | Why it is wrong | Fix |
| :--- | :--- | :--- |
| Auditing documents only | content can be empty | check the specific metric |
| Findings without severity | everything looks equal | rank by harm |
| Conditions without dates | permanent exceptions | ticket each condition |
| Monitoring without a response plan | alerts nobody acts on | name the responder |
| HITL with no override authority | rubber stamp | documented authority |
| Treating audit as adversarial | hides problems | shared interest in accuracy |

## Exercises

**Beginner.** Run `python governance.py`, open `outputs/audit-checklist.md`, and list the
three missing areas with the evidence you would need.

**Beginner.** Pick one complete item and rewrite its evidence cell as a specific file plus
line or metric, so a stranger could verify it in under a minute.

**Intermediate.** Write finding F-01 for the missing monitoring section, in the four-field
format, with a severity and an action.

**Intermediate.** Design the canary adversarial test set for the digit model: how many
examples, generated how, and what threshold triggers a rollback?

**Advanced.** Take the model card in `outputs/` and mark every claim that is not traceable to
a command. Rewrite two of them so they are.

**Advanced.** Write the release decision for a recruitment screening tool with the measured
fairness results from L13-01 (DI ratio 0.557, EOpp gap 0.176). Defend your choice of release,
conditional release or no release in 200 words.

## Self-check

1. What are the three questions an auditor asks of each artefact?
2. Why is "we test for bias" not evidence?
3. Name a monitor for each of: label bias, backdoor, prompt injection, RAG leakage.
4. What five properties make a HITL control auditable?
5. When is "release with conditions" the wrong decision?

## Key terms

**Audit**, **finding**, **severity**, **evidence**, **residual risk acceptance**,
**canary test**, **drift**, **PSI**, **calibration monitoring**, **oversight rate**,
**recourse**, **release gate**, **conditional release**.

## Further reading

- Raji et al. (2020). *Closing the AI Accountability Gap* — internal algorithmic auditing.
- NIST AI RMF Playbook — the measure and manage functions.
- ICO (2022). *AI and data protection risk toolkit*.
- Sculley et al. (2015). *Hidden Technical Debt in Machine Learning Systems* — why monitoring
  is not optional.

---

[Previous: L13-05](L13-05-governance-risk-and-the-ai-lifecycle.md) · [Module home](../README.md) ·
[Assignment ASG-13](../assignments/asg-13-model-card-and-audit-report.md)

---

**Navigation:** [← Previous: L13-05 Governance, Risk and the AI Lifecycle](L13-05-governance-risk-and-the-ai-lifecycle.md) · [Module end](../README.md)
