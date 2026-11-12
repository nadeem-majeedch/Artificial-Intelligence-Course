# M14 — One-Page Summary

[Module home](README.md) · [Course home](../../README.md) · [Quiz](quizzes/quiz-14.md) ·
[Capstone](capstone/README.md)

## The four questions of an applied system

```text
does a model belong here? -> rules baseline, hybrid gate          (L14-01)
can it be served?         -> compression, latency, registry        (L14-02)
will it keep working?     -> drift, coverage, monitoring plan      (L14-03)
is the claim reproducible? -> smallest test, ablation, honesty     (L14-04)
```

## Every measured number in the module

| Experiment | Measurement |
| :--- | :--- |
| Eligibility, rules only | accuracy 0.972, 0 policy violations |
| Eligibility, model only | accuracy 0.877, 100 policy violations |
| Eligibility, hybrid | accuracy 0.931, 0 violations, 100 extra refusals |
| Integrated gradients | savings +0.457 … income +0.035, while income was the binding rule |
| Two-tower, before training | zero-shot 0.152; i2t R@1 0.006 |
| Two-tower, after 300 steps | zero-shot 0.904; digit retrieval 0.961; i2t R@1 0.024 (chance ≈ 0.028) |
| Two-tower, per class | worst class 8 at 0.87 |
| Compression, teacher | 0.967 accuracy, 332.0 KB, 85,002 params, 66.3 µs |
| Compression, student scratch | 0.902, 18.8 KB, 4,810 params, 38.1 µs |
| Compression, distilled | 0.898, 18.8 KB, 56.5 µs (gain −0.004) |
| Quantised int8 | 0.898, 5.2 KB, 116.0 µs (2.62× slower) |
| Pruned 50% | 0.865, 18.8 KB, 64.1 µs (1.45× slower, 50% sparsity) |
| Distillation sweep | 0.872 (T=1, α=0.3) down to 0.791 (T=8, α=0.3) |
| GNN | MLP 0.600; GCN-2 1.000; GCN-4 1.000; GCN-8 0.250 |
| Graph homophily | measured 0.825; gain +0.400 at 0.7–0.9, −0.210 at 0.1 |
| Federated | central 0.917; local-only 0.176; FedAvg 0.898; FedAvg+DP 0.844 |
| Federated per class | spread 0.364 (best 1.00, worst 0.65) |
| Backtest | seasonal naive 4.78 (cov 0.85); ridge 3.79 (0.84); boosting 4.27 (0.66) |
| Drift | PSI 3.777 at lag 28 after an 18-point level shift → alert (>0.25) |
| MAE before → after drift | naive 4.63 → 6.21; ridge 3.54 → 5.48; boosting 4.13 → 5.62 |

## Formulas

$$
\text{PSI}=\sum_b (q_b-p_b)\ln\frac{q_b}{p_b},\qquad
\text{coverage}=\frac1n\sum_t \mathbb 1\{y_t\in[\ell_t,u_t]\}.
$$

$$
\text{IG}_i(x)=(x_i-x'_i)\int_0^1 \frac{\partial f(x'+\alpha(x-x'))}{\partial x_i}\,d\alpha,
\qquad
\mathcal L_{\text{KD}}=(1-\alpha)\,\mathcal L_{\text{CE}}+\alpha T^2\,
\text{KL}\!\left(p_T^{\text{student}}\,\|\,p_T^{\text{teacher}}\right).
$$

$$
\phi_j=\sum_{S\subseteq F\setminus\{j\}}\frac{|S|!(|F|-|S|-1)!}{|F|!}\big[v(S\cup\{j\})-v(S)\big]
\quad\text{(Shapley, M13)}.
$$

## What actually worked

| Problem | Control that helped | Cost |
| :--- | :--- | :--- |
| Policy compliance | rule gate | 100 refusals in the demo |
| Model size | int8 quantisation | 2.62× slower on float kernels |
| Accuracy small model | distillation | nothing gained at this capacity |
| Node classification | GNN when homophily ≥ 0.5 | −0.210 when homophily is low |
| No central data | FedAvg | 0.019 accuracy vs pooled, 0.364 class spread |
| Early drift detection | PSI on inputs | false alarms if thresholds are naive |
| Forecast accuracy | ridge on lags | seasonal naive is only 21% worse |

## What did not work, and why it matters

- **Distillation** on an easy task: hard labels carry all the signal.
- **Quantisation for speed**: dequantising every forward pass costs more than the arithmetic saved.
- **Pruning for latency**: dense kernels multiply zeros.
- **Instance retrieval as a metric**: label ambiguity caps it near chance.
- **GNNs without homophily**: message passing mixes classes.
- **Reporting the federated average**: hides a 0.364 per-class spread.

## The capstone in five rules

1. One primary metric, tied to the decision, with a baseline.
2. Split as deployment splits (time, site, patient — not randomly).
3. Report per-class or per-group, with n.
4. State uncertainty or say the sample cannot distinguish the models.
5. State what the result does not support, in the abstract.

## Three sentences to remember

1. A model is one component; the boundary around it is what makes it deployable.
2. Every compression is a trade, and the trade must be measured on the target.
3. If a claim cannot be reproduced by one command, it is not a result yet.

## Key terms

See the [glossary](../../resources/glossary.md), and the [module README](README.md) for the full
list introduced here.

---

[Module home](README.md) · [Quiz](quizzes/quiz-14.md) ·
[Proposal](assignments/asg-14-capstone-proposal.md) · [Capstone](capstone/README.md)
