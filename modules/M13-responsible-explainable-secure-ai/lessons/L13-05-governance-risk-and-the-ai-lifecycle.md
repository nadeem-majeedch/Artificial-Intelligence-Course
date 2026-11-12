# L13-05 — Governance, Risk and the AI Lifecycle

| | |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | L13-01 to L13-04 |
| Code | `code/governance.py` |

[← Previous: L13-04 Security: Adversarial Examples and Prompt Injection](L13-04-security-adversarial-examples-and-prompt-injection.md) · [Module home](../README.md) · [Next: L13-06 Auditing and Responsible Deployment →](L13-06-auditing-and-responsible-deployment.md)

## On this page

- [Why this lesson exists](#why-this-lesson-exists)
- [What you will be able to do](#what-you-will-be-able-to-do)
- [1. Governance in one sentence](#1-governance-in-one-sentence)
- [2. The risk register](#2-the-risk-register)
- [3. Model cards](#3-model-cards)
- [4. Datasheets](#4-datasheets)
- [5. The lifecycle, and what each stage owes](#5-the-lifecycle-and-what-each-stage-owes)
- [6. Regulation, briefly and accurately](#6-regulation-briefly-and-accurately)
- [7. Human oversight that is not theatre](#7-human-oversight-that-is-not-theatre)
- [8. Writing the release decision](#8-writing-the-release-decision)
- [Common mistakes](#common-mistakes)
- [Exercises](#exercises)
- [Self-check](#self-check)
- [Key terms](#key-terms)
- [Further reading](#further-reading)

## Why this lesson exists

Everything in this module so far is a measurement. Governance is what turns measurements
into decisions: who accepts a risk, at what threshold, with what evidence, and who is
answerable when it goes wrong.

Done badly, governance is a document nobody reads. Done well, it is a short set of artefacts
that are **generated from evidence you can reproduce** — a risk register with owners, a model
card with numbers, a datasheet with provenance, a checklist with links. This lesson builds
them, and then attacks them.

## What you will be able to do

1. Build a risk register with likelihood, impact, controls and residual scores.
2. Complete a model card and a datasheet whose claims trace to a script.
3. Map a system onto the AI lifecycle and say what evidence each stage owes.
4. Describe the main regulatory instruments and what they actually require.
5. Design human oversight that is not a rubber stamp.
6. Write a release decision with a named accountable owner.

---

## 1. Governance in one sentence

**Governance is the set of decisions about a system that are made before, during and after
its construction, by named people, with recorded evidence and a route to appeal.**

That definition implies the artefacts: decisions need owners, evidence needs reproduction,
appeal needs a human path. It also implies the failure modes: unowned risks, evidence that
cannot be reproduced, and no route for an affected person to object.

## 2. The risk register

`governance.py` scores likelihood (1–5) × impact (1–5) for eight risks, then records the
residual after controls:

```text
ID   category      L  I  score      band  resid      band
R1   fairness      4  5     20  critical     12      high
R5   security      3  3      9    medium      9    medium
R7   security      2  5     10      high      8    medium
R3   privacy       3  4     12      high      6    medium
R6   security      4  5     20  critical      6    medium
R2   fairness      4  3     12      high      4       low
R4   privacy       4  5     20  critical      4       low
R8   governance    3  3      9    medium      2       low
```

Read the gaps between inherent and residual: R4 (RAG returning a confidential record) falls
from 20 to 4 because document-level access control is a strong, cheap control. R1 (the
recruitment screen reproducing label bias) falls only from 20 to 12, because the controls —
group metrics in CI, reweighing or threshold review — do not remove label bias; L13-01
measured exactly that. **Residual risk should reflect what your measurements showed, not what
your controls are called.**

Rules that make a register useful:

- One owner per risk, by role, not "the team".
- Controls listed as things that can be inspected, not aspirations.
- Residual score justified by a measurement or an explicit "not yet measured".
- A release gate: no residual in the critical band, and high-band residuals need a named
  acceptor and a date.

A register with 40 rows nobody reviews is worse than 8 rows reviewed monthly.

## 3. Model cards

A model card is a short, structured disclosure. The template in `governance.py` forces the
fields that are usually missing:

| Section | Contains | Common failure |
| :--- | :--- | :--- |
| Intended use | the decision it supports | vague ("for education") |
| Out of scope | what it must not be used for | absent |
| Training data | provenance, size, label source | "proprietary" |
| Metrics | overall + per-group + baseline | overall only |
| Fairness | chosen definition, measured gap, threshold | "audited for bias" |
| Explainability | method, fidelity, stability | method named, nothing measured |
| Security/privacy | attacks run, results | absent |
| Limitations | what is known to be weak | marketing language |
| Monitoring | live metrics, cadence, triggers | "ongoing monitoring" |

Two tests for a finished card:

1. **Traceability.** Every number can be produced by a command in the repository.
2. **Falsifiability.** A reviewer can tell what would make the claim false.

```text
Fairness
- Definition: equal opportunity (TPR parity), chosen because the decision affects
  qualified applicants.
- Measured: TPR 0.745 (group A) vs 0.921 (group B); gap 0.176 on a 30% holdout (n=1,200).
- Threshold: gaps above 0.05 require sign-off by the fair-access officer.
```

That paragraph can be checked. "The model was designed with fairness in mind" cannot.

## 4. Datasheets

Where a model card describes the model, a datasheet describes the data: motivation,
composition, collection process, preprocessing, known biases, licence, maintenance.

The questions that matter most in practice:

- **Who is missing?** Undocumented exclusions become undocumented failures.
- **How were labels made, and by whom?** L13-01's whole disparity came from the labelling
  policy.
- **What is the licence, and does it survive your use?** A dataset's licence governs the
  data, not the model weights, and neither is inherited automatically by your output.
- **What happens when the data drifts?** A datasheet with no maintenance clause is a snapshot
  pretending to be a description.

## 5. The lifecycle, and what each stage owes

| Stage | Question | Evidence owed |
| :--- | :--- | :--- |
| Problem definition | is a model the right tool? | decision affected, alternative considered |
| Data | is it lawful and representative? | datasheet, licence, group counts |
| Development | does it work, and for whom? | metrics overall and per group, baseline |
| Evaluation | is it robust, private, secure? | attack results, red-team report |
| Documentation | can a stranger audit it? | model card, register, checklist |
| Deployment | who can it harm, and how is that limited? | oversight design, rollback plan |
| Monitoring | is it drifting or being attacked? | live metrics, alert thresholds, cadence |
| Retirement | what happens to the data and the decisions? | decommission plan, retraining policy |

Two lifecycle facts that are widely ignored:

- **The decision to build is a governance decision.** Most harms are cheaper to avoid than to
  mitigate.
- **Retirement is part of the lifecycle.** A system that stops being maintained does not stop
  making decisions.

## 6. Regulation, briefly and accurately

| Instrument | Scope | Core obligation |
| :--- | :--- | :--- |
| EU AI Act (Regulation 2024/1689) | providers and deployers in the EU | risk-tiered duties; prohibited practices; transparency for general-purpose models; conformity assessment for high-risk systems |
| GDPR | personal data processing | lawful basis, data minimisation, access and erasure rights, DPIA for high-risk processing |
| UK GDPR / Data Protection Act 2018 | UK processing | same structure, UK supervisory authority |
| US: sectoral + state law | e.g. employment (EEOC), credit (ECOA), state AI statutes | discrimination and disclosure duties per sector |
| OECD AI Principles | signatories | human-centred values, transparency, accountability |
| NIST AI RMF | voluntary, widely adopted | govern, map, measure, manage |

Two accurate generalisations:

1. **Automated decision-making with personal data already triggers data-protection duties**
   in the EU and UK, independent of any AI-specific law. Article 22 GDPR restricts solely
   automated decisions with legal or similarly significant effects.
2. **High-risk classification drives the heaviest obligations** — risk management, data
   governance, technical documentation, logging, human oversight, accuracy and robustness.
   Whether your system is high-risk is a legal determination, not an engineering one; record
   the reasoning.

Do not treat this table as legal advice, and do not cite a regulation you have not read.

## 7. Human oversight that is not theatre

Oversight fails in predictable ways:

| Failure | Looks like | Fix |
| :--- | :--- | :--- |
| Rubber stamping | 99.7% approval rate | sample audits, measure disagreement |
| Automation bias | reviewers accept the model's suggestion | show evidence before the recommendation |
| No authority | reviewer cannot override | documented override with no penalty |
| No time | 15 seconds per case | workload modelling |
| No information | reviewer sees only the score | counterfactual and top features (L13-02) |
| No recourse | affected person cannot appeal | published appeal route with a deadline |

Measured oversight beats declared oversight: log approvals, refusals, overrides and the time
taken, and review those numbers quarterly.

## 8. Writing the release decision

A release note that a regulator, a journalist and an engineer could all read:

```text
System: candidate screening assistant, version 1.0.0
Decision supported: shortlist for interview (human makes the final call)
Evidence: fairness.py 30% holdout, n=1,200; DI ratio 0.557, EOpp gap 0.176
Residual risks: R1 high (label bias in historical decisions) — accepted by <role>, <date>
Controls in force: group metrics in CI, human review of all rejections, quarterly audit
Monitoring: selection rate by group weekly; alert at 5-point shift
Appeal route: applicant request to <address>, 10 working days
Accountable owner: <role>
```

If you cannot fill a line, you are not ready to release. That is the entire value of the
exercise.

## Common mistakes

| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Controls described but never measured | residual risk is fiction | cite the measurement |
| Model card without per-group metrics | hides the disparity | mandatory subgroup table |
| Datasheet with no licence | unlawful redistribution | record licence and provenance |
| Oversight with no override authority | rubber stamp | documented authority and appeal |
| Treating regulation as a checklist | misses the actual duty | map obligation to evidence |
| No retirement plan | stale model keeps deciding | decommission policy with dates |

## Exercises

**Beginner.** Run `python governance.py` and open the five files in `outputs/`. Identify the
two claims in `model-card.md` that are not traceable to a script.

**Beginner.** Add a ninth risk for "the assistant refuses legitimate requests after a
guardrail change" and score it. What is the residual, and which control reduces it?

**Intermediate.** Rewrite R1's controls so that each one is inspectable. Then recompute the
residual and justify the change.

**Intermediate.** Draft the datasheet for the RAG index in `llm_security.py`: five documents,
one confidential. What must the datasheet say about access control?

**Advanced.** Take the release note template and fill it for a system you have actually built
in this course. Note every line you cannot evidence, and say what you would need to measure.

**Advanced.** Compare the EU AI Act's high-risk obligations with NIST AI RMF functions. Map
each obligation to a function and identify one obligation the RMF does not cover.

## Self-check

1. Why does R1's residual stay high while R4's collapses?
2. Name three model-card fields that are usually missing and what each prevents.
3. Which lifecycle stage is most often skipped, and what harm follows?
4. What makes human oversight real rather than nominal?
5. Write the accountability line for a system you would be willing to own.

## Key terms

**Governance**, **risk register**, **inherent risk**, **residual risk**, **model card**,
**datasheet**, **AI lifecycle**, **human oversight**, **automation bias**, **recourse**,
**EU AI Act**, **GDPR Article 22**, **NIST AI RMF**, **accountable owner**.

## Further reading

- EU AI Act, Regulation (EU) 2024/1689 — read the definitions and the high-risk annexes.
- NIST (2023). *AI Risk Management Framework 1.0*.
- Mitchell et al. (2019). *Model Cards for Model Reporting*.
- Gebru et al. (2021). *Datasheets for Datasets*.
- ICO guidance on automated decision-making and Article 22.

---

[Previous: L13-04](L13-04-security-adversarial-examples-and-prompt-injection.md) ·

---

**Navigation:** [← Previous: L13-04 Security: Adversarial Examples and Prompt Injection](L13-04-security-adversarial-examples-and-prompt-injection.md) · [Module home](../README.md) · [Next: L13-06 Auditing and Responsible Deployment →](L13-06-auditing-and-responsible-deployment.md)
