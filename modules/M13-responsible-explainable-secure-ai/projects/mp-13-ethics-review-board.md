# MP-13 — Ethics Review Board Simulation

| | |
| :--- | :--- |
| Time | 2 hours |
| Weight | 35% of the module |
| Prerequisites | All lessons, both labs, ASG-13 |
| Deliverables | dossier (1 page), hearing notes, decision memo (≤800 words) |

[Module home](../README.md) · [Assignment](../assignments/asg-13-model-card-and-audit-report.md)

## Why this project exists

Every technique in this module produces evidence. This project is about the room where the
evidence is used: people with different obligations, incomplete information, a deadline, and a
decision that affects someone who is not in the room.

You will run a review board. Working alone, you take all four roles in sequence; working in a
group, one role each. The point is not to reach the "right" answer — there isn't one — but to
produce a decision that survives being challenged from each seat.

## The system under review

**Northfield Applicant Screening Assistant, version 2.1**

A university department uses a model to rank applicants for interview shortlisting. A human
makes the final shortlisting decision. The model is trained on five years of historical
shortlisting decisions. Inputs: degree classification, work experience, a written statement
score, and whether the applicant attended an outreach event.

Measured evidence available to the board (all from this module's scripts, adapted):

```text
Accuracy 0.947   AUC 0.981
Selection rate   group A 0.172   group B 0.096
TPR              0.745           0.921
PPV              0.929           0.673
DP difference 0.076   DI ratio 0.557   EOpp gap 0.176
Proxy: outreach attendance 0.283 (A) vs 0.080 (B)
Reweighing: no effect on any metric
Group thresholds (0.375 / 0.600): DP gap 0.002, accuracy 0.954
Without outreach feature: accuracy 0.892, DP 0.004, EOpp 0.168
Prompt-injection test on the reviewer chatbot: 1 of 6 succeeded (content only)
RAG assistant over applications: 1 of 5 queries leaked a confidential record before
  document-level access control, 0 of 5 after
```

The board also has the model card, the risk register and the audit checklist from ASG-13.

## Roles

### 1. Product owner

Wants the system deployed this term. Argues: accuracy is 94.7%, a human makes the final call,
the alternative is unaided human shortlisting which has never been audited at all, and the
department is under pressure to process 4,000 applications.

Must prepare: the business case, the fallback plan if the board says no, and an answer to
"what does the human actually see?"

### 2. Data protection / legal

Focuses on lawful basis, minimisation, Article 22 (solely automated decisions), retention, and
whether the outreach feature is a special-category proxy. Notes that the historical decisions
are the training signal and were made under an older policy.

Must prepare: the three obligations the deployment would breach as configured, and the minimum
changes that would satisfy them.

### 3. Affected-party advocate

Represents applicants, especially group B. Asks what a rejected applicant is told, whether they
can appeal, whether the 0.921 TPR is a comfort or an indictment, and what happens to someone
who could not attend an outreach event because they work.

Must prepare: one concrete case narrative and the remedy they would accept.

### 4. Independent auditor

Presents the evidence and refuses to advocate. Flags that the DI ratio is 0.557, that
reweighing did nothing, that the outreach feature is a proxy, and that the TPR gap *widens* in
the direction that favours the disadvantaged group per qualified applicant — which is not the
same as fairness.

Must prepare: the two findings the board cannot ignore, and the two pieces of evidence that are
missing.

## Schedule (2 hours)

| Time | Activity |
| ---: | :--- |
| 0:00–0:15 | Read the dossier; each role writes its three key points |
| 0:15–0:45 | Opening statements, 5 minutes per role, no interruptions |
| 0:45–1:15 | Cross-examination: each role puts two questions to one other role |
| 1:15–1:35 | Negotiate conditions: what would each role accept? |
| 1:35–1:50 | Decision and vote |
| 1:50–2:00 | Write the decision memo |

## Deliverable 1 — Dossier (one page)

For the role you played: your position in one sentence, your three strongest evidence points
with numbers, your two non-negotiables, and the one thing you would concede.

## Deliverable 2 — Hearing notes

Two questions you asked and the answers you received. One point where your position changed, or
an explicit statement that it did not and why.

## Deliverable 3 — Decision memo (≤800 words)

Written as the board, addressed to the department. Must contain:

1. **Decision**: release / conditional release / do not release.
2. **Grounds**: at most four, each tied to a measured number.
3. **Conditions**, if any: each with an owner and a date.
4. **Dissent**: the strongest argument against the decision, stated fairly.
5. **Monitoring and review**: metrics, thresholds, cadence, and the named accountable owner.
6. **Appeal route** for an affected applicant.

## Constraints

- Use only the evidence in this brief and your own runs. Do not invent numbers; if something is
  not measured, say "not measured".
- Do not modify the system to make the decision easier.
- No deployment, no commit, no push.

## Marking criteria

| Criterion | Weight | Excellent | Adequate | Weak |
| :--- | ---: | :--- | :--- | :--- |
| Evidence use | 25% | every ground cites a measured number | most do | assertions |
| Role fidelity | 20% | argues from that role's obligations | recognisable | all roles sound alike |
| Decision quality | 25% | conditions owned, dated, monitorable | decision justified | decision asserted |
| Dissent | 15% | strongest counter-argument stated fairly | mentioned | absent or strawman |
| Appeal and monitoring | 15% | specific, testable | present | generic |

## Reflection questions

1. Which role was hardest to argue, and what did that reveal about your own defaults?
2. The TPR gap favours group B per qualified applicant while the selection rate favours group A.
   Which number did your board use, and was that choice defensible?
3. Would you accept a deployment with group-specific thresholds? What would you tell an
   applicant who asked why the rules differ?
4. The outreach feature costs 5.5 accuracy points to remove. Who pays those points, and who
   pays for keeping it?
5. If the board said "conditional release", what would make you revisit in 30 days — and what
   would the condition look like as a ticket?

---

[Module home](../README.md) · [Quiz](../quizzes/quiz-13.md)
