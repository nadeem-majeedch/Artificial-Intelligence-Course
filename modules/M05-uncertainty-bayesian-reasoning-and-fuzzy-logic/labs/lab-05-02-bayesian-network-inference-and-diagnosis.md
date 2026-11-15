# LAB-05-02 — Bayesian Network Inference and Intelligent Diagnosis

| | |
| :--- | :--- |
| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| Time | 3 hours |
| Level | 300 |
| Pairs with | L05-02, L05-06 |
| Code | [`code/variable_elimination.py`](../code/variable_elimination.py), [`code/alarm_network.py`](../code/alarm_network.py) |
| Notebook | [`nb-05-02`](../notebooks/nb-05-02-variable-elimination.ipynb) |

[Module home](../README.md) · [Lab 1](lab-05-01-bayesian-and-fuzzy-decision-system.md)

> **This is an educational simulation.** The network, priors and likelihoods below were chosen for
> teaching and are not calibrated on any machine, patient or fleet. Nothing here is a diagnostic
> system, and no output of this lab should be used to decide whether equipment is safe.

## 1. Learning objectives

- **Specify** a six-node Bayesian network: structure, full CPTs and independence assumptions.
- **Implement** evidence handling and exact inference by enumeration, then by variable elimination.
- **Verify** that two independent inference algorithms agree to $10^{-12}$ on every query.
- **Interpret** posteriors, including explaining away between two competing causes.
- **Quantify** sensitivity to prior probabilities, and say what that implies for deployment.

## 2. Scenario

A fictional HVAC plant has a history of overheating incidents. The maintenance team logs four kinds of
observation and wants a tool that turns them into a ranked list of likely causes:

| Node | Meaning | Observed how |
| :--- | :--- | :--- |
| `F` | Fan failure | maintenance log warning (`M`) |
| `D` | Dust clog in the intake | inspection only — usually unobserved |
| `O` | Overheating | inferred, sometimes directly measured |
| `S` | Smoke | sensor |
| `A` | High-temperature alarm | control panel |
| `M` | Maintenance-log warning | technician note |

The team's question is always the same: *the alarm went off — what is most likely wrong, and what should
we check first?*

## 3. Problem statement

Build the network below, implement exact inference two ways, and answer six diagnostic queries with
numbers rather than adjectives. Then show how the answer moves when the prior on fan failure is
changed, and explain why a team must not read a posterior as a probability of the physical cause
without the priors being justified.

## 4. Mathematical background

Structure: `F → O ← D`, `O → S`, `O → A`, `F → M`. Factorisation:

$$P(F,D,O,S,A,M) = P(F)\,P(D)\,P(O\mid F,D)\,P(S\mid O)\,P(A\mid O)\,P(M\mid F)$$

Independence assumptions, stated so they can be argued with:

1. $F \perp D$ — fan failure and dust clog have independent causes (no shared wear process is modelled).
2. $S \perp A \mid O$ and $S \perp \{F,D\} \mid O$ — smoke and alarm depend on the causes only through overheating.
3. $M \perp \{D,O\} \mid F$ — the log warning reflects the fan alone; it is **not** a second symptom of overheating.

Assumption 3 is the one to attack first: if a technician writes the warning *because* the plant
overheated, then $M$ is a child of $O$ and every posterior in this lab changes.

Conditional probability tables (all rows sum to 1):

| $F$ | $D$ | $P(O{=}T \mid F,D)$ | | $P(M{=}T\mid F)$ | | $P(S{=}T\mid O)$ | $P(A{=}T\mid O)$ |
| :--- | :--- | ---: | :--- | ---: | :--- | ---: | ---: |
| T | T | 0.95 | | $F{=}T$ | 0.70 | $O{=}T$ | 0.60 / 0.90 |
| T | F | 0.75 | | $F{=}F$ | 0.10 | $O{=}F$ | 0.01 / 0.02 |
| F | T | 0.55 | | | | | |
| F | F | 0.05 | | | | | |

Priors: $P(F)=0.08$, $P(D)=0.15$.

## 5. Step-by-step tasks

1. **Specify** (25 min). Write the six CPTs as Python dictionaries with both values of every child. Assert that each conditioned table sums to 1.
2. **Enumerate** (35 min). Build the 64-entry joint distribution and implement `posterior(query, evidence)` by summing with and without the query fixed. Assert the joint totals 1.0.
3. **Eliminate** (40 min). Express the six CPTs as `Factor` objects from `variable_elimination.py` and call `variable_elimination(factors, query, evidence, order=[...])`.
4. **Compare** (20 min). For six evidence cases, print enumeration, VE and the absolute difference. Every difference must be below $10^{-12}$.
5. **Interpret** (25 min). Explain `alarm+smoke` versus `alarm+no smoke` in words; identify the explaining-away structure.
6. **Sensitivity** (20 min). Sweep $P(F) \in \{0.02, 0.08, 0.25\}$ and report $P(O\mid A{=}T)$ for each.
7. **Write up** (15 min). Recommended first check, with the numbers that justify it, and the assumptions you would test first.

## 6. Starter code

```python
import itertools
import numpy as np
from variable_elimination import Factor, variable_elimination

PF = {True: 0.08, False: 0.92}
PD = {True: 0.15, False: 0.85}
PO = {(True, True): 0.95, (True, False): 0.75, (False, True): 0.55, (False, False): 0.05}
PS = {True: 0.60, False: 0.01}
PA = {True: 0.90, False: 0.02}
PM = {True: 0.70, False: 0.10}
NODES = ("F", "D", "O", "S", "A", "M")


def p_child(table, child_value, parent_value):
    """P(child = value | parent) for both values of the child."""
    p_true = table[parent_value]
    return p_true if child_value else 1.0 - p_true


def joint(f, d, o, s, a, m):
    return (PF[f] * PD[d] * p_child(PO, o, (f, d))
            * p_child(PS, s, o) * p_child(PA, a, o) * p_child(PM, m, f))


TABLE = {(f, d, o, s, a, m): joint(f, d, o, s, a, m)
         for f, d, o, s, a, m in itertools.product([True, False], repeat=6)}


def posterior(query, evidence):
    idx = {n: i for i, n in enumerate(NODES)}
    den = sum(v for k, v in TABLE.items() if all(k[idx[n]] == x for n, x in evidence.items()))
    num = sum(v for k, v in TABLE.items()
              if k[idx[query]] is True and all(k[idx[n]] == x for n, x in evidence.items()))
    return num / den, den


def factors():
    """The same six CPTs as Factor objects, for variable elimination."""
    grid = lambda vals: np.array([[[vals[(f, d)] if o else 1 - vals[(f, d)]
                                    for d in (True, False)] for f in (True, False)]
                                  for o in (True, False)])
    two = lambda t: np.array([[t[True], t[False]], [1 - t[True], 1 - t[False]]])
    return [Factor.from_array(["F"], [PF[True], PF[False]]),
            Factor.from_array(["D"], [PD[True], PD[False]]),
            Factor.from_array(["O", "F", "D"], grid(PO)),
            Factor.from_array(["S", "O"], two(PS)),
            Factor.from_array(["A", "O"], two(PA)),
            Factor.from_array(["M", "F"], two(PM))]
```

## 7. Expected behaviour

Verified in this repository (joint total 1.0; VE and enumeration agree to $1.1\times10^{-16}$):

| Evidence | $P(O\mid e)$ | $P(F\mid e)$ | $P(e)$ |
| :--- | ---: | ---: | ---: |
| none | 0.1774 | 0.0800 | 1.0000000 |
| alarm | 0.9066 | 0.3209 | 0.1761120 |
| alarm + smoke | 0.9983 | 0.3512 | 0.0959605 |
| alarm + no smoke | 0.7968 | 0.2846 | 0.0801515 |
| log warning only | 0.3728 | 0.3784 | 0.1480000 |
| alarm + log warning | 0.9640 | 0.7678 | 0.0515184 |

What the numbers show:

- **The alarm is strong evidence of overheating** (0.177 → 0.907), and smoke pushes it to 0.998.
- **Absence of smoke is not absence of overheating**: 0.797, because smoke is only 60% likely even when overheating. Silence is weak evidence.
- **The two causes compete.** With the alarm alone, $P(F)=0.321$; add the log warning and it rises to 0.768, because $M$ is evidence about the fan specifically. Meanwhile $P(O)$ rises to 0.964 — an observation about one cause makes both causes more likely once the effect is present, which is exactly the collider behaviour to explain in the write-up.
- **Prior sensitivity** ($P(O\mid A{=}T)$): 0.02 → 0.786; 0.08 → 0.907; 0.25 → 0.966. The posterior moves a lot, which is why a fleet-level prior must be justified before the number is quoted.

## 8. Testing instructions

| Test | Expected |
| :--- | :--- |
| Table normalisation | every conditioned row sums to 1 within $10^{-12}$ |
| Joint normalisation | sum of 64 entries equals 1.0 within $10^{-12}$ |
| No-evidence query | $P(F\mid\varnothing) = 0.08 \pm 10^{-12}$ |
| Independence | $P(F,D) = P(F)P(D)$ within $10^{-15}$ |
| Algorithm agreement | enumeration vs VE below $10^{-12}$ for all six cases |
| Evidence validation | unknown node, non-boolean value and query-in-evidence all raise |
| Order independence | two elimination orders give identical results |
| Sensitivity | monotone in $P(F)$ |

## 9. Evaluation rubric

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Network specification | 25% | CPTs with both child values, normalisation asserted, assumptions stated | CPTs complete | partial tables |
| Inference | 30% | enumeration and VE, agreement demonstrated numerically | one method | hardcoded answers |
| Interpretation | 25% | explaining away and weak-evidence cases explained with numbers | describes table | repeats numbers |
| Sensitivity | 10% | sweep with interpretation of the range | sweep only | absent |
| Integrity | 10% | states the simulation's limits and the assumptions to test | mentions limits | claims realism |

## 10. Deliverables

Submit one folder named `lab-05-02-<yourname>` containing exactly these files.

| File | Required contents |
| :--- | :--- |
| `bayes_net.py` | The six CPTs with a normalisation assertion, the 64-entry joint, `posterior(query, evidence)`, and the variable-elimination path using `Factor`. Imports from `code/` are allowed; do not edit the module's reference files. |
| `comparison.csv` | Six rows (one per evidence case) with columns `evidence`, `enumeration`, `ve`, `abs_diff`, `p_evidence`. Every `abs_diff` must be below $10^{-12}$. |
| `sensitivity.csv` | Three rows for $P(F)\in\{0.02,0.08,0.25\}$ with the resulting $P(O\mid A{=}T)$. |
| `REPORT.md` | At most 800 words, with the five sections below. |

**`REPORT.md` sections.** (1) The network and its three independence assumptions, stated in
words. (2) The six-query table with a one-paragraph reading of `alarm+smoke` versus
`alarm+no smoke`, naming the explaining-away structure. (3) The sensitivity result and what it
implies for quoting a posterior in deployment. (4) The recommended first check for the
maintenance team, justified by the numbers. (5) Limitations: which assumption you would test
first with real logs and what data that would need.

**Evidence the marker will look for.** Joint total 1.0 within $10^{-12}$; at least one
hand-computed factor product in the report or comments; enumeration and VE agreeing to the
stated tolerance on all six cases; the three sensitivity values; and an explicit statement that
the network is a teaching simulation, not a diagnostic system.

**Plots.** One optional figure: $P(O\mid A{=}T)$ against the three prior values, with axes
labelled. Do not submit screenshots of terminal output; paste the numbers into the CSV instead.

**Reproducibility.** State the Python version and confirm that no random seed is needed — every
number is a deterministic function of the CPTs. The notebook [`nb-05-02`](../notebooks/nb-05-02-variable-elimination.ipynb)
may be submitted *instead of* `bayes_net.py` only if every cell is executed and its outputs
include the comparison table; do not submit both.

**Submission format.** A single `.zip` of the folder, or a repository link containing the same
files. Late policy and the marking scale are in the module README; the rubric in §9 is the
marking scheme.

## 11. Extension challenges

1. **Re-model the log warning.** Make $M$ a child of $O$ as well as $F$ and recompute the table; explain which posterior moves most and why.
2. **Add a repair action.** Add node `R` (repair attempted) and show that observing a successful repair is evidence about the original cause.
3. **Learn a CPT.** Estimate $P(O\mid F,D)$ from a synthetic 500-case run of your own generator, and compare with the hand-set values.
4. **Cost-sensitive decision.** Give each cause a repair cost and a failure cost, and derive the check order that minimises expected cost — the first step from inference to decision.
5. **Second engine.** Implement variable elimination with a different ordering and report the largest intermediate factor for each ordering.

## Reflection

1. Why does $P(O\mid A)$ exceed $P(O)$ by such a large factor, while $P(O\mid M)$ barely moves it?
2. Which single independence assumption would you test first with real data, and what data would you need?
3. The lab calls this a simulation. What exactly would have to change for it to be a diagnostic system?
4. At $P(F)=0.25$ the posterior is 0.966; at 0.02 it is 0.786. Which number would you show a maintenance manager, and why?

---

[Module home](../README.md) · [Lab 1](lab-05-01-bayesian-and-fuzzy-decision-system.md)
