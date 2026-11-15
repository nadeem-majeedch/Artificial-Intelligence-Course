# M13 — Responsible, Explainable and Secure AI

| Level | 300 |
| :--- | :--- |
| Study time | 22.4 hours — guided 9.0 · practical 5.5 · assessment 5.9 · project 2.0 |
| Lessons | 6 |
| Course outcome | CLO8 — build, audit and govern AI systems whose behaviour can be explained, challenged and defended |
| Prerequisites | M07 (essential), M11 (recommended), L13-01 assumes basic statistics |

[Course home](../../README.md) · [All modules](../README.md) · [Previous module: M12](../README.md#m12)

## Overview

This module is about the questions that arrive *after* a model works: who does it fail, can
anyone see why, can someone make it misbehave, and who answers for it?

It is deliberately measurement-first. Every claim in the lessons comes from a script in
[`code/`](code/) that you can run on a laptop in under two minutes, and the module reports
results that contradict the standard advice:

- pre-processing reweighing, the textbook fairness fix, **changed no metric at all** on the
  recruitment audit, because the bias was in the labels rather than the representation;
- a backdoored model scored **higher clean accuracy (0.917) than the clean baseline (0.913)**
  while misclassifying 85.5% of triggered inputs;
- membership inference **failed** (AUC 0.513) against a model that generalises, which is the
  most useful negative result in the module;
- LIME and Shapley values **ranked the same features in opposite orders** on the same
  prediction, and both implementations were correct.

The four parts map onto the four questions:

| Part | Question | Lessons |
| :--- | :--- | :--- |
| A — Responsible AI | who is harmed, and is the harm distributed fairly? | L13-01, L13-03 |
| B — Explainable AI | can the decision be explained, and is the explanation faithful? | L13-02 |
| C — Security | can someone make it behave outside its purpose? | L13-03, L13-04 |
| D — Safety and governance | who decides, who monitors, who is accountable? | L13-05, L13-06 |

## Practical scenarios and where they are built

| # | Scenario | Where |
| :--- | :--- | :--- |
| 1 | Detecting bias in a recruitment dataset | [L13-01](lessons/L13-01-responsible-ai-fairness-and-bias.md), [LAB-13-01](labs/lab-13-01-fairness-audit.md) §2 |
| 2 | Explaining a student performance prediction | [L13-02](lessons/L13-02-explainability-from-importance-to-counterfactuals.md), [NB-13-01](notebooks/nb-13-01-explainability-toolkit.ipynb) |
| 3 | Evaluating fairness in a loan classifier | [LAB-13-01](labs/lab-13-01-fairness-audit.md) §4 |
| 4 | Adversarial image perturbations | [L13-04](lessons/L13-04-security-adversarial-examples-and-prompt-injection.md), [LAB-13-02](labs/lab-13-02-security-and-prompt-injection-testing.md) §2 |
| 5 | Prompt injection in a local chatbot | [LAB-13-02](labs/lab-13-02-security-and-prompt-injection-testing.md) §4, `code/llm_security.py` |
| 6 | Unsafe tool use by an agent | [LAB-13-02](labs/lab-13-02-security-and-prompt-injection-testing.md) §5, `code/llm_security.py` |
| 7 | Data leakage in a RAG application | [LAB-13-02](labs/lab-13-02-security-and-prompt-injection-testing.md) §6, `code/llm_security.py` |

Scenario 7 links back to the RAG assistant built in M11; this module adds the security
evaluation of it rather than rebuilding it.

## Data, models and licences

No personal data is used anywhere. The three datasets are generated deterministically by
`code/rai_data.py` and carry a documented bias mechanism so that the audit has something
specific to find.

| Asset | Licence | Size / note |
| :--- | :--- | :--- |
| `recruitment()` | **CC0-1.0** | 4,000 rows, 4 features; label bias: merit threshold 0.52 (A) vs 0.62 (B) |
| `student()` | **CC0-1.0** | 3,000 rows, 4 features; proxy bias via `tutoring_access` |
| `loans()` | **CC0-1.0** | 5,000 rows, 4 features; group-correlated calibration offset |
| scikit-learn `load_digits` | **CC BY 4.0** (UCI dataset); BSD-3-Clause loader | 1,797 8×8 images, loaded at runtime; not redistributed |
| The five-document RAG corpus | **CC0-1.0** | authored here; one document is deliberately confidential |

`random_state=0` and `seed=0` throughout. Regenerating the data reproduces every number in the
module. The dataset cards are written to `code/dataset_cards.json` by `rai_data.py`.

**No pretrained weights are downloaded for the security lessons.** The image classifier is a
small MLP trained locally, and the LLM experiments use a deterministic simulator (see the
honesty note below), so the module runs offline.

## Before you start

You need Python with NumPy, scikit-learn and PyTorch (CPU is enough).

```bash
pip install numpy scikit-learn torch matplotlib
```

`shap` and `lime` are **not required**: the methods are implemented from scratch in
`explain.py` so the mechanism is visible. If you have them installed, compare your
implementation against them as an exercise.

**Readiness self-check.** If you cannot do three of these, review M07 first:

1. Compute precision and recall from a confusion matrix and say which one a hiring manager
   feels.
2. Explain what a logistic regression coefficient means in odds terms.
3. Say why a test set must never be used for tuning.
4. Compute a gradient of a loss with respect to an input.
5. Explain what a p-value does and does not tell you.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L13-01 | Responsible AI, Fairness and Bias | Lesson | 90 m | [Read](lessons/L13-01-responsible-ai-fairness-and-bias.md) |
| L13-02 | Explainability: From Importance to Counterfactuals | Lesson | 90 m | [Read](lessons/L13-02-explainability-from-importance-to-counterfactuals.md) |
| L13-03 | Privacy, Memorisation and Model Attacks | Lesson | 90 m | [Read](lessons/L13-03-privacy-memorisation-and-model-attacks.md) |
| L13-04 | Security: Adversarial Examples and Prompt Injection | Lesson | 90 m | [Read](lessons/L13-04-security-adversarial-examples-and-prompt-injection.md) |
| L13-05 | Governance, Risk and the AI Lifecycle | Lesson | 90 m | [Read](lessons/L13-05-governance-risk-and-the-ai-lifecycle.md) |
| L13-06 | Auditing and Responsible Deployment | Lesson | 90 m | [Read](lessons/L13-06-auditing-and-responsible-deployment.md) |
| NB-13-01 | An Explainability Toolkit | Notebook | 60 m | [Open](notebooks/nb-13-01-explainability-toolkit.ipynb) |
| LAB-13-01 | Fairness Audit of Three Models | Lab | 2.5 h | [Start](labs/lab-13-01-fairness-audit.md) |
| LAB-13-02 | Security and Prompt-Injection Testing | Lab | 2.5 h | [Start](labs/lab-13-02-security-and-prompt-injection-testing.md) |
| ASG-13 | Model Card and Audit Report | Assignment | 1.5 h | [Start](assignments/asg-13-model-card-and-audit-report.md) |
| QUIZ-13 | Module self-check | Quiz | 30 m | [Take](quizzes/quiz-13.md) |
| MP-13 | Ethics Review Board Simulation | Mini-project | 2 h | [Start](projects/mp-13-ethics-review-board.md) |

**Total published:** 9.0 h guided study + 5.5 h practical + 5.9 h assessment + 2.0 h project = **22.4 hours**.

Supporting code lives in [`code/`](code/):

| File | Contents |
| :--- | :--- |
| `rai_data.py` | three synthetic datasets with documented bias mechanisms; dataset cards |
| `fairness.py` | group metrics, DP/DI/EOpp/EOdds, calibration, reweighing, threshold search |
| `explain.py` | permutation importance, PDP, exact Shapley, LIME, counterfactuals, sanity checks |
| `security.py` | FGSM/PGD, adversarial training, quantisation, poisoning, backdoor, MI, extraction |
| `guardrails_m13.py` | injection detection, delimiting, redaction, action allowlist |
| `llm_security.py` | injection, RAG leakage and tool-abuse harness with a documented simulator |
| `governance.py` | risk register, model card, datasheet, audit checklist writers |
| `build_notebooks.py` | regenerates and executes NB-13-01 with outputs stripped |

Each script runs standalone:

```bash
python rai_data.py && python fairness.py && python explain.py
python security.py && python guardrails_m13.py && python llm_security.py
python governance.py      # writes outputs/model-card.md and friends
```

## A note on honesty in the security lessons

Two experiments in this module could easily be misread, so they are stated plainly in the code
and the lessons.

**The prompt-injection harness uses a simulator.** `flan-t5-small`, used in M11, refused or
ignored injected instructions in 0.00 of the module's test cases, so it cannot demonstrate an
attack succeeding. `ToyLLM` is a deterministic stand-in that obeys the last imperative in its
prompt. It is a teaching device, not a measurement of any real model, and every lesson says so.
What *is* measured is the relative effect of structural controls: 0.83 → 0.17 attack success,
0/6 unsafe agent actions, 1/5 → 0/5 RAG leaks.

**The membership-inference attack fails.** AUC 0.513 is chance. That is reported as a result,
not hidden, because "we tested and found nothing exploitable, here is the test" is what a model
card should contain.

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L13-01 | 1.5 h |
| 2 | L13-02, NB-13-01 | 2.5 h |
| 3 | LAB-13-01 | 2.5 h |
| 4 | L13-03 | 1.5 h |
| 5 | L13-04 | 1.5 h |
| 6 | LAB-13-02 | 2.5 h |
| 7 | L13-05 | 1.5 h |
| 8 | L13-06, ASG-13 | 3 h |
| 9 | MP-13 | 2 h |
| 10 | QUIZ-13, revision | 0.5 h |

Ten days at roughly two hours. If time is short, keep L13-01, L13-02, L13-04 and LAB-13-01;
they carry the measurement discipline the rest of the module depends on.

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-13-01 | Reproduced metrics, interpretation of disagreement, mitigation costs | 10% |
| LAB-13-02 | Attack strength recorded, defence costs, scope discipline | 10% |
| QUIZ-13 | Conceptual and numerical grasp | 10% |
| ASG-13 | Model card completeness, finding quality, traceability | 25% |
| MP-13 | Evidence use, role fidelity, decision with owned conditions | 35% |

The assessment dimensions are described in the
[curriculum map](../../docs/CURRICULUM-MAP.md#8-assessment-model).

## Compute requirements

| Stage | CPU only | GPU (optional) |
| :--- | :--- | :--- |
| `rai_data.py` + `fairness.py` | ~20 s (threshold search included) | small gain |
| `explain.py` | ~10 s | — |
| `security.py` | 60–90 s (five small models) | seconds |
| `llm_security.py`, `guardrails_m13.py` | under 2 s | — |
| `governance.py` | under 1 s | — |

A 4-core laptop is sufficient. No GPU is required anywhere, and no network access is needed
after installation.

## Key terms introduced

**Responsible AI**, **algorithmic discrimination**, **label bias**, **proxy variable**,
**demographic parity**, **disparate impact ratio**, **equal opportunity**, **equalised odds**,
**predictive parity**, **reweighing**, **permutation importance**, **partial dependence**,
**Shapley value**, **KernelSHAP**, **LIME**, **local surrogate**, **fidelity**, **stability**,
**counterfactual**, **actionability**, **membership inference**, **model extraction**,
**model inversion**, **DP-SGD**, **adversarial example**, **FGSM**, **PGD**, **adversarial
training**, **data poisoning**, **backdoor**, **trigger**, **attack success rate**,
**prompt injection**, **indirect injection**, **action allowlist**, **default deny**,
**supply-chain risk**, **risk register**, **model card**, **datasheet**, **human oversight**,
**automation bias**, **recourse**, **EU AI Act**, **NIST AI RMF**, **release gate**.

All are defined in the [glossary](../../resources/glossary.md). The one-page recap is in
[summary.md](summary.md).

## Resources

- Barocas, Hardt & Narayanan, *Fairness and Machine Learning* (fairmlbook.org).
- Molnar, *Interpretable Machine Learning*, 2nd edition.
- Mitchell et al. (2019). *Model Cards for Model Reporting*.
- Gebru et al. (2021). *Datasheets for Datasets*.
- NIST (2023). *AI Risk Management Framework 1.0*.
- OWASP Top 10 for Large Language Model Applications.
- The module's [summary](summary.md) — every verified number in one table.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) · [Previous: M12](../README.md#m12)

## Assignment

[PA-14 — An Audit of a Model You Built](../../assessments/programming/pa-14-explainable-and-secure-ai.md)
