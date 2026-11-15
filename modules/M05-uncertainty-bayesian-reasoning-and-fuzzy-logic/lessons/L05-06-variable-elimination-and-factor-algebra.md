# L05-06 — Variable Elimination and Factor Algebra

| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| :--- | :--- |
| Level | 300 |
| Study time | 95 minutes |
| Prerequisites | [L05-02](L05-02-bayesian-networks-independence-and-inference.md) |
| Code | [`code/variable_elimination.py`](../code/variable_elimination.py) (tested) |
| Notebook | `notebooks/nb-05-02-variable-elimination.ipynb` |

[← Previous: L05-05](L05-05-fuzzy-inference-mamdani-sugeno-and-defuzzification.md) · [Module home](../README.md)

## 1. Learning Objectives

- **Explain** why enumeration re-does work, and what variable elimination removes.
- **Represent** a conditional probability table as a factor and perform restrict, multiply, sum-out and normalise on it.
- **Execute** variable elimination by hand on the alarm network for $P(B\mid j,m)$, showing every intermediate factor.
- **Choose** an elimination order and quantify the cost of a bad one.
- **Implement** generic variable elimination and prove it agrees with enumeration.

## 2. Prerequisite Knowledge

The alarm network, its CPTs and enumeration — [L05-02](L05-02-bayesian-networks-independence-and-inference.md). You should be able to compute $P(B\mid j,m)$ there.

## 3. Conceptual Explanation

### 3.1 What enumeration wastes

Enumeration computes the joint for all $2^5 = 32$ assignments and throws most of it away. If two
queries share evidence, it recomputes the same sums. Variable elimination (VE) rewrites the same
mathematical expression as a sequence of small table operations, each of which discards a variable as
soon as it can.

### 3.2 Factors

A **factor** $f(X_1,\dots,X_k)$ maps each assignment of its variables to a non-negative number. A CPT
is a factor; an evidence-restricted CPT is a factor over fewer variables. The four operations are:

| Operation | Notation | Meaning |
| :--- | :--- | :--- |
| Restrict | $f[\mathbf{e}]$ | fix evidence, drop those variables |
| Multiply | $f \cdot g$ | over the union of variables: $h(x) = f(x_{|X})g(x_{|Y})$ |
| Sum out | $\sum_X f$ | marginalise one variable: $h(y) = \sum_x f(x,y)$ |
| Normalise | $f / \sum f$ | divide by the total mass; record the mass as $P(\mathbf{e})$ |

### 3.3 The identity that makes VE correct

Because a product of factors distributes over sums,

$$\sum_{E}\sum_{A} \underbrace{P(B)P(E)P(A\mid B,E)P(j\mid A)P(m\mid A)}_{\text{one big factor}}
= P(B)\sum_{A} P(j\mid A)P(m\mid A)\underbrace{\sum_{E} P(E)P(A\mid B,E)}_{g(A,B)}$$

The inner sum over $E$ is computed once for each $(A,B)$ pair instead of once per full assignment.

### 3.4 Ordering is the whole engineering problem

Eliminating a variable multiplies every factor that mentions it. Eliminate in the wrong order and the
intermediate factor can be larger than the joint it came from. For this network both orders are
cheap; in a 30-node network the difference between a good and a bad order is the difference between
seconds and hours.

## 4. Worked Example — $P(B\mid j,m)$ by variable elimination

Factors from the network: $f_B(B)$, $f_E(E)$, $f_{A}(A,B,E)$, $f_J(J,A)$, $f_M(M,A)$.

**Step 0 — evidence.** Restrict $J{=}T$ and $M{=}T$:

Restricting the two caller factors to $J{=}T$ and $M{=}T$ leaves two factors over $A$ alone:

$$g_J(A) = \begin{cases}0.90 & A=T\\ 0.05 & A=F\end{cases}
\qquad
g_M(A) = \begin{cases}0.70 & A=T\\ 0.01 & A=F\end{cases}$$

**Step 1 — eliminate $E$:** multiply $f_E \cdot f_A$ and sum out $E$.

$$g_1(A,B) = \sum_{E} P(E)P(A\mid B,E)$$

| | $A=T$ | $A=F$ |
| :--- | ---: | ---: |
| $B=T$ | $0.002(0.95) + 0.998(0.94) = 0.94002$ | $0.002(0.05) + 0.998(0.06) = 0.05998$ |
| $B=F$ | $0.002(0.29) + 0.998(0.001) = 0.001578$ | $0.002(0.71) + 0.998(0.999) = 0.998422$ |

**Step 2 — eliminate $A$:** multiply $g_1 \cdot f_J \cdot f_M$ and sum out $A$.

$$g_2(B) = \sum_A g_1(A,B)\,P(j\mid A)\,P(m\mid A)$$

- $B=T$: $0.94002(0.90)(0.70) + 0.05998(0.05)(0.01) = 0.5922126 + 0.0000300 = 0.5922426$
- $B=F$: $0.001578(0.63) + 0.998422(0.0005) = 0.0009941 + 0.0004992 = 0.0014934$

**Step 3 — multiply the remaining prior and normalise:**

$$P(B\mid j,m) \propto f_B(B)\,g_2(B) =
\begin{cases}0.001 \times 0.5922426 = 0.0005922\\ 0.999 \times 0.0014934 = 0.0014919\end{cases}$$

Total $= 0.0020841$, so

$$P(B\mid j,m) = \frac{0.0005922}{0.0020841} = 0.2842$$

This is the value enumeration produced in L05-02 §4.3 — two different algorithms, one number. The
implementation reproduces exactly these intermediate tables (see §6), so you can check each row.

## 5. Mathematical Formulation

For query $Q$, evidence $\mathbf{e}$, and elimination order $\sigma$ over the hidden variables:

$$P(Q\mid\mathbf{e}) = \alpha \sum_{\sigma_1}\cdots\sum_{\sigma_k} \prod_{f \in \Phi} f[\mathbf{e}]$$

Cost is governed by the **induced width**: eliminating $\sigma_i$ creates a factor over its neighbours
in the current graph. The intermediate factor has size $2^{w+1}$ where $w$ is that neighbourhood size,
so total cost is $O(n \cdot 2^{w+1})$ — exponential in treewidth, not in the number of nodes.

| Method | Time | Space | Reuse of shared subexpressions |
| :--- | :--- | :--- | :--- |
| Enumeration | $O(2^n)$ per query | $O(2^n)$ | none |
| Variable elimination | $O(n\,2^{w+1})$ | $O(2^{w+1})$ | within one query |
| Junction tree | polynomial in $2^w$ | $O(2^w)$ | across queries |

For the alarm network, enumeration performs 32 joint evaluations and 31 additions; VE multiplies
three small tables and performs two sums.

## 6. Python Implementation

Generic and network-agnostic; full file in [`code/variable_elimination.py`](../code/variable_elimination.py).

```python
import numpy as np
from itertools import product


class Factor:
    def __init__(self, variables, table):
        self.variables = tuple(variables)
        self.table = {tuple(k): float(v) for k, v in table.items()}

    def restrict(self, evidence):
        fixed = {v: bool(evidence[v]) for v in self.variables if v in evidence}
        remaining = tuple(v for v in self.variables if v not in fixed)
        table = {}
        for assignment in product([True, False], repeat=len(remaining)):
            full, it = {}, iter(assignment)
            for v in self.variables:
                full[v] = fixed[v] if v in fixed else next(it)
            table[assignment] = self.table[tuple(full[v] for v in self.variables)]
        return Factor(remaining, table)

    def multiply(self, other):
        merged = list(self.variables) + [v for v in other.variables if v not in self.variables]
        table = {}
        for assignment in product([True, False], repeat=len(merged)):
            values = dict(zip(merged, assignment))
            table[assignment] = (self.table[tuple(values[v] for v in self.variables)]
                                 * other.table[tuple(values[v] for v in other.variables)])
        return Factor(merged, table)

    def sum_out(self, variable):
        remaining = tuple(v for v in self.variables if v != variable)
        table = {}
        for assignment in product([True, False], repeat=len(remaining)):
            values = dict(zip(remaining, assignment))
            table[assignment] = sum(
                self.table[tuple({**values, variable: x}[v] for v in self.variables)]
                for x in (True, False))
        return Factor(remaining, table)

    def normalize(self):
        total = sum(self.table.values())
        return Factor(self.variables, {k: v / total for k, v in self.table.items()}), total
```

```python
>>> from variable_elimination import alarm_factors, variable_elimination
>>> variable_elimination(alarm_factors(), "B", {"J": True, "M": True}, order=["E", "A"])
(0.2841718..., 0.0020841...)
>>> # a deliberately poor order still gives the same answer, at higher cost
>>> variable_elimination(alarm_factors(), "B", {"J": True, "M": True}, order=["A", "E"])
(0.2841718..., 0.0020841...)
```

The implementation uses NumPy for the dense tables (`Factor.dense()`) and pure Python for the
algebra, because the algebra is what the lesson is about. No posterior is hardcoded: the tests compare
VE against enumeration and against a brute-force sum of the 32-entry joint table for nine evidence
cases, agreeing to $10^{-12}$.

## 7. Practical Applications

- **Medical diagnosis** — posteriors for many diseases over shared evidence.
- **Fault localisation** — the largest practical use of VE in industry.
- **Risk and reliability models** — networks with hundreds of variables, queried repeatedly.
- **Probabilistic programming** — the inference engine behind many libraries.

## 8. Common Mistakes

1. **Forgetting to restrict evidence first**, so the elimination sums out an observed variable and
   returns a marginal instead of a posterior.
2. **Summing out the query variable** — it must survive to the end.
3. **Multiplying factors that do not share a variable** and expecting a smaller table; the product is
   over the union, so it grows.
4. **Normalising too early**, which throws away the evidence mass you still need.
5. **Assuming any order is efficient.** It is always correct; it is not always cheap.
6. **Storing numpy indices as factor keys.** `True == 1` in Python, so an index-keyed table silently
   returns the False slice. This exact bug was found in this module's own implementation (Phase 21B):
   the fix is to key on booleans, never on integer indices.

## 9. Exercises

1. Reproduce $P(B\mid j,m)$ by hand using the factors in §4 and check each intermediate with the code.
2. Compute $P(B\mid j)$ and $P(B\mid m)$ by VE with the same order and confirm they match L05-02's table.
3. Eliminate in the order $A$ then $E$ and compare the sizes of the intermediate factors with the order $E$ then $A$.
4. Add a sixth node (a second earthquake indicator) and recompute the induced width for both orders.
5. Replace the dense factor arrays with sparse dicts and measure memory on a 12-node chain.

## 10. Self-Assessment

1. State the four factor operations and their effect on the variable set.
2. Why is VE exact rather than approximate?
3. What determines the size of the largest intermediate factor?
4. Why does the final step need a normalisation, and what does it give you besides the posterior?
5. Give one reason a poor elimination order is a performance bug rather than a correctness bug.

## 11. Key Terms

**Factor**, **evidence restriction**, **factor multiplication**, **summing out**, **elimination order**,
**induced width**, **treewidth**, **normalisation**, **variable elimination**.

## 12. Further Reading

- Koller & Friedman, *Probabilistic Graphical Models*, chapter 9 — the definitive treatment.
- Russell & Norvig, section 14.4; Zhang & Poole (1994) on ordering heuristics.

## What to Do Next

Work [LAB-05-02](../labs/lab-05-02-bayesian-network-inference-and-diagnosis.md), which builds a
six-node fault-diagnosis network and requires enumeration and variable elimination to agree, then
compare the two engines on your own network. [LAB-05-01](../labs/lab-05-01-bayesian-and-fuzzy-decision-system.md)
covers the classifier and fuzzy half of the module.
