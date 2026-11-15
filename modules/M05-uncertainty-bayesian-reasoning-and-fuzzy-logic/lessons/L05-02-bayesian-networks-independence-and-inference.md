# L05-02 — Bayesian Networks, Conditional Independence and Inference

| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| :--- | :--- |
| Level | 300 |
| Study time | 100 minutes |
| Prerequisites | [L05-01](L05-01-probability-conditional-probability-and-bayes-theorem.md) |
| Code | [`code/alarm_network.py`](../code/alarm_network.py) (tested) |
| Notebook | `notebooks/nb-05-01-uncertainty-workbench.ipynb` |

[← Previous: L05-01](L05-01-probability-conditional-probability-and-bayes-theorem.md) · [Next: L05-03 Naive Bayes →](L05-03-naive-bayes-and-text-classification.md)

## 1. Learning Objectives

- **Build** the alarm network from its causal story: nodes, edges and full conditional probability tables.
- **Read** conditional independence from the graph using d-separation, and state the factorisation it implies.
- **Compute** a posterior by exact enumeration, and show that the joint distribution is normalised.
- **Demonstrate** explaining away numerically: the same alarm evidence means different things once an earthquake is observed.
- **Recognise** the implementation errors that make a network silently wrong.

## 2. Prerequisite Knowledge

Conditional probability and Bayes' theorem — [L05-01](L05-01-probability-conditional-probability-and-bayes-theorem.md).

## 3. Conceptual Explanation

### 3.1 The factorisation

A Bayesian network encodes

$$P(X_1,\dots,X_n) = \prod_{i=1}^{n} P(X_i \mid \text{Pa}(X_i))$$

The graph is a compact statement about independence. Direction is a modelling choice: the arrows run
from cause to effect because that is the easiest way to elicit probabilities from a person, not
because inference requires that order.

### 3.2 Three structures that explain everything

| Structure | Shape | Independence |
| :--- | :--- | :--- |
| Chain | A → B → C | A ⊥ C given B |
| Fork | A ← B → C | A ⊥ C given B |
| Collider | A → B ← C | A ⊥ C marginally; dependent given B (explaining away) |

Explaining away is the counter-intuitive one: two independent causes become dependent once the
effect is observed. It is also why "the alarm went off" makes burglary and earthquake compete.

### 3.3 Inference

Exact inference by enumeration sums the joint over the hidden variables. It is exponential in the
worst case, which is why real systems use variable elimination, junction trees or sampling. For five
binary nodes, enumeration is cheap and shows exactly what the algorithm does;
[L05-06](L05-06-variable-elimination-and-factor-algebra.md) then rewrites the same sum as factor
operations and removes the repeated work.

## 4. Worked Example — the classic alarm network

### 4.1 Structure

```text
Burglary (B)        Earthquake (E)
      \\                 /
       \\               /
          Alarm (A)
          /       \\
   JohnCalls (J)  MaryCalls (M)
```

Edges: B → A, E → A, A → J, A → M. Parents: Pa(A) = {B, E}, Pa(J) = {A}, Pa(M) = {A};
B and E have no parents.

**Independence assumptions:**

1. Burglary and earthquake are independent: $B \perp E$ (no common ancestor).
2. John and Mary call independently *given the alarm*: $J \perp M \mid A$ (their only shared cause is A).
3. Once A is known, the callers tell you nothing further about B or E — the alarm screens them off.

**Factorisation:**

$$P(B,E,A,J,M) = P(B)\,P(E)\,P(A\mid B,E)\,P(J\mid A)\,P(M\mid A)$$

### 4.2 Conditional probability tables

| $B$ | $E$ | $P(A{=}T \mid B,E)$ | $P(A{=}F \mid B,E)$ |
| :--- | :--- | ---: | ---: |
| T | T | 0.95 | 0.05 |
| T | F | 0.94 | 0.06 |
| F | T | 0.29 | 0.71 |
| F | F | 0.001 | 0.999 |

Every row sums to 1 — this is the requirement that the original version of this example broke.

| | $P(\cdot = T)$ | $P(\cdot = F)$ | | $P(\cdot = T)$ | $P(\cdot = F)$ |
| :--- | ---: | ---: | :--- | ---: | ---: |
| $P(B)$ | 0.001 | 0.999 | $P(E)$ | 0.002 | 0.998 |
| $P(J\mid A{=}T)$ | 0.90 | 0.10 | $P(J\mid A{=}F)$ | 0.05 | 0.95 |
| $P(M\mid A{=}T)$ | 0.70 | 0.30 | $P(M\mid A{=}F)$ | 0.01 | 0.99 |

Size: the full joint table needs $2^5-1 = 31$ numbers; the network needs $1+1+4+2+2 = 10$.

### 4.3 Derivation for the query $P(B \mid J{=}T, M{=}T)$

By definition,

$$P(B\mid j,m) = \frac{P(B,j,m)}{P(j,m)}, \qquad
P(B,j,m) = \sum_{e}\sum_{a} P(B)P(e)P(a\mid B,e)P(j\mid a)P(m\mid a)$$

and $P(j,m)$ is the same sum taken over both values of $B$ — that is, the two branch totals below,
added.

**Numerator, $B = T$.** Factor out $P(B)=0.001$.

| $E$ | $A{=}T$ term: $P(A\mid B,E)P(j\mid A)P(m\mid A)$ | $A{=}F$ term | Sum over $A$ |
| :--- | :--- | :--- | ---: |
| T | $0.95 \times 0.90 \times 0.70 = 0.5985$ | $0.05 \times 0.05 \times 0.01 = 0.000025$ | 0.598525 |
| F | $0.94 \times 0.90 \times 0.70 = 0.5922$ | $0.06 \times 0.05 \times 0.01 = 0.00003$ | 0.592230 |

$P(B{=}T, j, m) = 0.001 \times \left(0.002 \times 0.598525 + 0.998 \times 0.592230\right)
= 0.001 \times 0.5922426 = 0.00059224$.

**Denominator branch, $B = F$.** Factor out $P(B)=0.999$.

| $E$ | $A{=}T$ term | $A{=}F$ term | Sum over $A$ |
| :--- | :--- | :--- | ---: |
| T | $0.29 \times 0.63 = 0.1827$ | $0.71 \times 0.0005 = 0.000355$ | 0.183055 |
| F | $0.001 \times 0.63 = 0.00063$ | $0.999 \times 0.0005 = 0.0004995$ | 0.0011295 |

$P(B{=}F, j, m) = 0.999 \times \left(0.002 \times 0.183055 + 0.998 \times 0.0011295\right)
= 0.999 \times 0.001493351 = 0.00149186$.

**Result.**

$$P(B\mid j,m) = \frac{0.00059224}{0.00059224 + 0.00149186} = \frac{0.00059224}{0.00208410} = 0.2842$$

Both calls raise the burglary posterior from the 0.001 prior to 0.284 — a factor of 284. The same
calculation gives $P(B \mid j,\neg m) = 0.0051$ and $P(B \mid \neg j, m) = 0.0069$: agreement between
the callers is what makes the evidence strong.

### 4.4 Evidence comparison table

Measured with `code/alarm_network.py` (`evidence_table()`), joint total 1.0:

| Evidence | $P(B \mid e)$ | $P(e)$ |
| :--- | ---: | ---: |
| none | 0.0010 | 1.0000000 |
| John calls | 0.0163 | 0.0521390 |
| Mary calls | 0.0561 | 0.0117363 |
| both call | **0.2842** | 0.0020841 |
| John only (Mary silent) | 0.0051 | 0.0500549 |
| Mary only (John silent) | 0.0069 | 0.0096522 |
| neither calls | 0.0001 | 0.9382088 |
| earthquake | 0.0010 | 0.0020000 |
| earthquake, both call | **0.0033** | 0.0003669 |

### 4.5 Interpretation

- **Each caller is weak evidence alone.** A phone call raises the posterior to 0.016 or 0.056,
  because people call for other reasons ($P(j\mid\neg a) = 0.05$).
- **Agreement is strong evidence.** Both calling gives 0.284, far more than the sum of the
  individual effects — two semi-independent channels confirming one cause.
- **Explaining away is visible.** Add the earthquake and the posterior *falls* from 0.284 to 0.0033,
  a factor of about 86. The same calls now have a competing explanation, so burglary becomes unlikely
  again. Note that the earthquake alone changes nothing (0.0010): B and E are independent. Only in the
  presence of the alarm's effects does the second cause matter — the collider signature.
- **Silence is evidence too.** Neither calling drops the posterior to 0.0001, because $P(\neg j, \neg m
  \mid a) = 0.10 \times 0.30 = 0.03$ is small.

## 5. Mathematical Formulation

Enumeration for query variables $Q$, evidence $E=e$, hidden $H$:

$$P(Q\mid e) = \alpha \sum_{h} \prod_{x_i \in \{Q,h\}} P(x_i \mid \text{Pa}(x_i)),
\qquad \alpha = \frac{1}{P(e)}, \quad P(e) = \sum_{Q}\sum_{h}\prod_i P(x_i\mid\text{Pa}(x_i))$$

Complexity $O(2^{|H|})$ per query; variable elimination reduces it by summing out early. A network
whose joint does not sum to 1 violates the definition of $\alpha$ and produces the wrong answer
silently — which is why the tests in §6 assert normalisation.

## 6. Python Implementation

The full implementation, with its tests, is [`code/alarm_network.py`](../code/alarm_network.py).
The essential parts:

```python
from itertools import product

NODES = ("B", "E", "A", "J", "M")

P_BURGLARY = {True: 0.001, False: 0.999}
P_EARTHQUAKE = {True: 0.002, False: 0.998}
P_ALARM_TRUE = {(True, True): 0.95, (True, False): 0.94,
                (False, True): 0.29, (False, False): 0.001}
P_JOHN_CALLS = {True: 0.90, False: 0.05}
P_MARY_CALLS = {True: 0.70, False: 0.01}


def p_alarm(a, b, e):
    """P(A=a | B=b, E=e) for BOTH values of a -- this is the repaired line."""
    p_true = P_ALARM_TRUE[(b, e)]
    return p_true if a else 1.0 - p_true


def joint(b, e, a, j, m):
    return (P_BURGLARY[b] * P_EARTHQUAKE[e] * p_alarm(a, b, e)
            * (P_JOHN_CALLS[a] if j else 1.0 - P_JOHN_CALLS[a])
            * (P_MARY_CALLS[a] if m else 1.0 - P_MARY_CALLS[a]))


def enumerate_posterior(query_node, evidence=None):
    evidence = validate_evidence(evidence or {})
    table = joint_table()
    idx = {name: i for i, name in enumerate(NODES)}
    match = lambda k, fixed: all(k[idx[n]] == v for n, v in fixed.items())
    p_e = sum(v for k, v in table.items() if match(k, evidence))
    p_qe = sum(v for k, v in table.items() if match(k, evidence) and k[idx[query_node]] is True)
    return p_qe / p_e, p_e
```

```python
>>> enumerate_posterior("B", {"J": True, "M": True})[0]
0.2841718...
>>> enumerate_posterior("B", {"E": True, "J": True, "M": True})[0]
0.0033...
```

`validate_evidence` rejects unknown node names and non-boolean values, so a typo raises instead of
returning the prior.

## 7. Practical Applications

- **Diagnosis** — symptoms as evidence, diseases as queries.
- **Reliability engineering** — components and failure modes with shared causes.
- **Risk models** — credit and insurance networks with expert-defined structure.
- **Root-cause analysis** — telemetry evidence over a service dependency graph.

## 8. Common Mistakes

1. **A partial conditional probability table.** Storing only $P(A{=}T\mid b,e)$ and using that number
   for the $a{=}F$ branch as well. The joint then sums to 0.005 instead of 1 and every posterior is
   wrong, while the code still runs and prints plausible numbers. Use the complement, and assert that
   the joint sums to 1.
2. **Conditioning on the effect incorrectly.** Writing $P(B\mid A)$ as $P(A\mid B)$; they differ by the
   prior ratio.
3. **Treating "no evidence" as zero probability.** An empty evidence dict must give the prior, not an
   error and not a division by zero.
4. **Using `if value:` for evidence.** `False` is falsy, so `if evidence_dict` treats
   `{"J": False}` as no evidence. Test membership (`node in evidence`) instead.
5. **Forgetting a row of a table**, so probabilities do not sum to 1 along the conditioned variable.
6. **Adding edges because variables correlate**, which destroys the independence structure the graph
   is meant to encode.
7. **Reading causality from every arrow**, or ignoring explaining away when interpreting a posterior.
8. **Enumerating with 40 hidden variables** — exponential, not slow.

## 9. Exercises

1. Reproduce the derivation in §4.3 for $P(B\mid j,\neg m)$ and check it against the table.
2. Show that $P(B\mid E)=P(B)$ numerically, and explain why the collider does not change that.
3. Add a node "Radio reports earthquake" (child of E, with its own noisy table) and show that it also
   produces explaining away.
4. Break the normalisation deliberately: set $P(A{=}F\mid F,F)$ to 0.5 instead of 0.999 and observe
   what the posterior does. Explain the failure.
5. Implement variable elimination for this network and compare the number of multiplications with
   enumeration (there are 5 tables; count them for each query).

## 10. Self-Assessment

1. What does the factorisation buy you, in numbers?
2. State the collider rule and give the alarm network example.
3. Why is exact inference exponential in general?
4. Why must the joint distribution sum to 1, and what goes wrong if it does not?
5. Why is $P(B\mid j,m) = 0.284$ rather than 0.849, when both callers agree?

## 11. Key Terms

**Bayesian network**, **factorisation**, **d-separation**, **collider**, **explaining away**,
**enumeration**, **normalisation**, **variable elimination**.

## 12. Further Reading

- Pearl (1988), *Probabilistic Reasoning in Intelligent Systems*.
- Russell & Norvig, chapter 14 — the alarm network and its published posteriors.

## What to Do Next

[L05-06](L05-06-variable-elimination-and-factor-algebra.md) computes the same posteriors by variable
elimination, and shows why it is the method used in practice.
[L05-03](L05-03-naive-bayes-and-text-classification.md) applies this factorisation to a classifier you
can train in fifty lines.
