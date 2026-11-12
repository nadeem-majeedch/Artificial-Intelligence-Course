# QUIZ-M14 — Solutions and Explanations

[Quiz](quiz-m14.md) · [Assessment index](../README.md)

---

## Part A

**Q14.1 — B.** The gate's value is a guarantee: no output violates the policy. In the module's
demo the rules-only model was *more* accurate than the network (0.972 vs 0.877) and the hybrid was
less accurate than the rules alone (0.931) — the gate is bought with refusals, not accuracy.

**Q14.2 — B.** PSI above 0.25 is the conventional alert threshold for a distribution shift worth
investigating. Below 0.10 is treated as stable; 0.10–0.25 is "monitor".

**Q14.3 — B.** Message passing helps when neighbours carry class information and the features are
weak. At low homophily the GNN lost 0.210 accuracy to a feature-only model in the module's sweep.

**Q14.4 — B.** The registry records version, metrics, owner, approval and target — the things that
let someone answer "what is live, and is it approved?".

## Part B

**Q14.5 — False.** Quantisation reduces size, but speed depends on kernels and memory bandwidth.
In the module the int8 model was 2.62× *slower* because weights were dequantised on every forward
pass. It is faster where int8 kernels exist or memory bandwidth dominates.

## Part C

**Q14.6 — Model answer.** If many captions describe the same class, exact-pair retrieval has a low
ceiling by construction: the model may retrieve a different but equally correct caption and still be
scored wrong. The meaningful metric is class-level retrieval (0.961 in the module) or recall@k with
an ambiguity-aware judgement.

**Q14.7 — Model answer.** The global average can hide clients that are much worse off. In the
module the federated model reached 0.898 overall with a 0.364 spread across classes, so some clients
would have been better off alone. Per-client reporting makes that visible.

## Part D

**Q14.8 —** $5.2/18.8=0.2766$, so 27.7% of the float size. Compression factor
$18.8/5.2\approx3.6\times$.

**Q14.9 —** Coverage 0.84 against a nominal 0.80 means the interval is slightly **too wide** (it
contains the truth more often than promised), not too narrow. The width of 13.81 is the cost; a
narrower interval with 0.80 coverage would be better calibrated.

## Part E

**Q14.10 —** Mean aggregation gives both nodes $(2+6)/2=4$. After one step the two representations
are identical, so the classifier can no longer distinguish them; at depth 8 this is the
oversmoothing collapse observed in the module (8-layer GCN accuracy 0.250).

## Part F

**Q14.11 —** `10 10 1.0`

Both lists have 10 elements; `q` sums to $10\times0.1=1.0$ (subject to floating-point display), so
the sizes are equal even though the last values differ. The snippet tests attention to lengths
rather than to the values.

---

[Quiz](quiz-m14.md) · [Previous solutions](quiz-m13.md) · [Assessment index](../README.md)
