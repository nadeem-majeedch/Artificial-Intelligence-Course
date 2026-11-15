# LAB-05-01 — A Bayesian and Fuzzy Decision System

| | |
| :--- | :--- |
| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| Time | 3 hours |
| Level | 300 |
| Pairs with | L05-03, L05-05 |

[Module home](../README.md) · [Notebook](../notebooks/nb-05-01-uncertainty-workbench.ipynb)

## Scenario

A campus facilities team runs a building with two problems. First, the email triage queue misroutes
complaints about heating. Second, the ventilation controller is a bang-bang switch: below 19 °C full
heat, above it nothing, so the rooms oscillate between stuffy and cold. The team has sensors but no
data scientist.

You will deliver two components: a **naive Bayes classifier** for complaint routing, and a **fuzzy
controller** for ventilation, plus a short explanation the facilities manager can act on.

## Your role

You are the only technical person on the project. Your report will be read by a manager who cares
about oscillation and misrouting, not about likelihoods.

## What you are given

| Item | Details |
| :--- | :--- |
| Emails | 60 plain-text complaints across four categories: heating, lighting, noise, cleaning |
| Sensor ranges | temperature 10–30 °C, CO₂ 400–2000 ppm |
| Output | ventilation damper 0–100% |
| Reference | lessons L05-03 and L05-05; notebook NB-05-01 |

## Starter material

A runnable starter is provided: [`starters/lab-05-01_starter.py`](starters/lab-05-01_starter.py).
It loads the lab's data, prints a baseline you can compare against, and
marks the parts left for you with `TODO`. Run it before you write anything.

Module reference code: [`../code/`](../code/).

## Requirements

- **R1** Train naive Bayes with Laplace smoothing; report a confusion matrix and per-class recall.
- **R2** Report accuracy *and* macro-averaged recall, and say why the second matters more here.
- **R3** Design at least four fuzzy rules over temperature and CO₂.
- **R4** Implement Sugeno inference with a documented default when no rule fires.
- **R5** Show the controller's output curve over temperature at 600 and 1200 ppm, and argue it removes oscillation.

## Tasks

1. **Data** (20 min). Load the 60 emails, split 45/15, tokenise by whitespace and lowercasing.
2. **Classifier** (50 min). Train, predict, confusion matrix, per-class precision and recall.
3. **Failure analysis** (25 min). Find the misclassified emails and name the cause for each (rare word, ambiguity, label noise).
4. **Fuzzy design** (40 min). Membership functions for both inputs and the output; draw the rule table.
5. **Implementation** (45 min). Implement inference and defuzzification; produce the output curves.
6. **Report** (20 min). Two pages: what works, what does not, what the manager should do.

## Expected results

- Naive Bayes accuracy between 0.75 and 0.90 on 15 held-out emails; "noise" is usually the weakest class.
- At least one misclassification caused by a word shared across categories ("noisy heater").
- The controller output is continuous: no jump larger than 10 percentage points for a 1 °C change.
- With CO₂ at 1200 ppm the damper stays open far longer than at 600 ppm at the same temperature.

## Deliverables

| File | Contents |
| :--- | :--- |
| `triage.py` | Classifier with smoothing and evaluation |
| `ventilation.py` | Membership functions, rules, Sugeno inference |
| `REPORT.md` | ≤ 700 words with both results and the recommendation |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Bayes component | 30% | correct smoothing, per-class metrics, cause-level failure analysis | accuracy only | broken probabilities |
| Fuzzy component | 30% | continuous surface, justified rules, no zero-denominator case | works for some inputs | bang-bang in disguise |
| Measurement | 20% | curves and confusion matrix with interpretation | numbers without reading | none |
| Communication | 20% | manager can act on the recommendation | descriptive | jargon |

## Extension challenges

1. Add a third input (humidity) and show which rules become redundant.
2. Replace the naive Bayes classifier with a Bayesian network over two features and compare.
3. Tune $\alpha$ and the membership overlaps; report the sensitivity of the output surface.

## Reflection

1. Which uncertainty in this lab is random, and which is vague?
2. The classifier is 82% accurate. Is that good enough for routing? For what consequence?
3. What would you monitor in production to know the controller is still behaving?

---

[Module home](../README.md) · [Notebook](../notebooks/nb-05-01-uncertainty-workbench.ipynb)
