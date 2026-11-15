# LAB-04-03 — Bayesian and Knowledge-Based Decision Support

| | |
| :--- | :--- |
| Module | M04 · Knowledge Representation and Logical Reasoning |
| Level | 200 |
| Time | 3 hours |
| Prerequisites | [L04-07](../lessons/L04-07-rule-based-and-expert-systems.md), [L05-02](../../M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-02-bayesian-networks-independence-and-inference.md) |
| Code | `code/expert_system.py` (`BayesNet`, `bayes_posterior`) |

[← LAB-04-02](lab-04-02-logic-based-reasoning-and-inference.md) · [Module](../README.md)

## 1. Learning objectives

- **Contrast** deductive inference with probabilistic inference on the same equipment scenario.
- **Build** a small binary Bayesian network and compute a posterior by enumeration.
- **Explain** what a logical rule base cannot express and what a probability adds.
- **Choose** the representation from the decision, not from preference.
- **State** the assumptions a posterior depends on.

## 2. Scenario

An IT support desk triages "the projector will not turn on". The team has two candidate tools: a rule base
that concludes *faulty power supply* when the fuse is blown, and a probabilistic model that ranks causes when
the evidence is partial. The desk wants a decision, not a lecture.

The network in this lab is synthetic: four binary variables and invented numbers. It is a teaching
simulation of decision support, not a real diagnostic device.

## 3. Problem statement

1. encode the equipment network: power fault `P`, clog `C`, overheating `O` (caused by P or C), warning light
   `W` (caused by O);
2. compute priors and posteriors for several evidence sets by enumeration;
3. answer the same questions with a rule base and record where it has nothing to say;
4. decide which tool answers "the light is on, what is most likely wrong?";
5. state the independence assumptions and one way they are wrong in reality.

## 4. Background concepts

- $P(X_1,\dots,X_n) = \prod_i P(X_i \mid \mathrm{Pa}(X_i))$ — the network is a compact joint distribution.
- Enumeration sums the joint over hidden variables, then normalises.
- Logic yields *true / false / unprovable*; probability yields a distribution over causes.
- Evidence can raise a posterior without proving anything: that is the useful case in support desks.
- Every number in a CPT is an assumption; the posterior inherits all of them.

## 5. Dataset information and licensing

The network and its conditional probability tables are synthetic and course-authored
(`troubleshooting_net()`); the numbers were chosen to make the posterior move visibly. No logs, tickets or
personal data are used. The synthetic content is dedicated to the public domain under CC0 1.0; the M05
module's alarm network is a separate teaching example and is not reused here.

## 6. Software requirements

Python 3.10+ and `expert_system.py`. NumPy is used by the module but this lab needs only the standard
library plus that file.

## 7. Step-by-step tasks

1. Print the network structure and the four CPTs. Identify parents and children for each node.
2. Compute priors for each node with no evidence.
3. Compute posteriors: `P(P | W=True)`, `P(C | W=True)`, `P(O | W=True)`.
4. Compute `P(P | O=True)` and compare with the prior; explain the change.
5. Write rules that answer "if W then O", "if O then P or C", and note the two questions they cannot answer.
6. Decide which tool the support desk should use, in one paragraph with the numbers from step 3.
7. List the independence assumptions and one realistic violation (for example, a clog raises temperature,
   which also stresses the power supply).

## 8. Starter code

```python
import expert_system as es

net = es.troubleshooting_net()
print("nodes:", list(net.parents))
for node, table in net.cpt.items():
    print(node, "parents:", net.parents[node], "table:", table)

def show(query, evidence=None):
    post = es.bayes_posterior(net, query, evidence or {})
    print(f"P({query}=True | {evidence}) = {post[True]:.4f}")

show("P")
show("C")
show("O", {"W": True})
show("P", {"W": True})
show("C", {"W": True})
show("P", {"O": True})
```

## 9. Expected behaviour

- Priors reproduce the CPT marginals: `P(P) = 0.10`, `P(C) = 0.20`.
- With the warning light on, `P(P)` rises to roughly **0.26** and `P(C)` to roughly **0.46**: the light is
  better evidence for a clog than for a power fault, because the clog has the higher prior.
- `P(P | O=True)` rises further than `P(P | W=True)` because `O` is closer to `P` in the graph.
- The rule base answers "is overheating true?" and stops; it cannot rank the two causes, which is exactly the
  question the desk needs answered.

Numbers depend on the CPTs in the code; report what your run prints.

## 10. Evaluation metrics

| Check | Pass condition |
| :--- | :--- |
| Network correctness | joint sums to 1 over all 16 assignments |
| Posterior correctness | matches enumeration computed by hand for one case |
| Normalisation | posterior pairs sum to 1 |
| Evidence handling | logically impossible evidence is rejected, not silently zeroed |
| Comparison | rule base and network answer different questions, stated explicitly |

## 11. Testing instructions

- Enumerate all 16 assignments and assert the total probability is 1.0.
- Assert `P(P)` with no evidence equals the CPT prior to 1e-12.
- Assert posteriors sum to 1.0 for both query values.
- Assert the rule base derives `overheating` from `W=True` but cannot produce a ranking.
- Run `python code/expert_system.py` and confirm the self-test passes.

## 12. Submission requirements

The CPT table, the posterior table for three evidence sets, the rule-base comparison, the recommendation and
the assumptions list. No real device data.

## 13. Evaluation rubric

| Criterion | Weight | Excellent looks like |
| :--- | ---: | :--- |
| Model construction | 25% | structure and CPTs justified, not arbitrary |
| Inference | 25% | enumeration implemented or correctly used, normalisation checked |
| Interpretation | 25% | posteriors explained in decision terms |
| Contrast with logic | 15% | limitations of each named with examples |
| Assumptions | 10% | at least one realistic violation identified |

## 14. Extension challenges

1. **More evidence.** Add a second symptom node and show how the posterior ranking changes.
2. **Prior sensitivity.** Vary `P(C)` from 0.05 to 0.5 and plot `P(C | W=True)`.
3. **Decision rule.** Add a cost matrix and choose the action with minimum expected cost.
4. **From rules to probabilities.** Take one rule from LAB-04-01 and give it a confidence; state what breaks.

## Reflection

Logic tells you what follows. Probability tells you what is likely, which is usually what a support desk
needs. The honest engineering position is not "one is better" but "the decision determines the
representation" — and both inherit their assumptions from whoever wrote the tables.
