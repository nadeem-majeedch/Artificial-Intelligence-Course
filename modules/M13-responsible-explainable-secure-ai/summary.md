# M13 — One-Page Summary

[Module home](README.md) · [Course home](../../README.md) · [Quiz](quizzes/quiz-13.md)

## The four questions

```text
who is harmed?  ->  group metrics, calibration, mitigation cost        (Part A)
why this output? ->  global + local explanations, fidelity, stability  (Part B)
how can it be broken? -> evasion, poisoning, injection, extraction     (Part C)
who decides?    ->  risk register, model card, oversight, monitoring   (Part D)
```

## Every measured number in the module

| Experiment | Measurement |
| :--- | :--- |
| Recruitment data | 4,000 rows; positive rate 0.219 (A) vs 0.067 (B); referral 0.283 vs 0.080 |
| Recruitment baseline | accuracy 0.947, AUC 0.981; selection 0.172 vs 0.096; TPR 0.745 vs 0.921; PPV 0.929 vs 0.673 |
| Disparity | DP difference 0.076, DI ratio 0.557, EOpp gap 0.176, EOdds gap 0.176 |
| Reweighing | no change: 0.947 / 0.076 / 0.176 |
| Group thresholds | 0.375 (A), 0.600 (B); DP gap 0.002; accuracy 0.954 |
| Drop `referral` | accuracy 0.892, DP 0.004, EOpp gap 0.168 |
| Student, with proxy | accuracy 0.798, AUC 0.777, DP 0.026, EOpp 0.021 |
| Student, without proxy | accuracy 0.793, AUC 0.726, DP 0.009, EOpp 0.009 |
| Loans | accuracy 0.672, AUC 0.606, DP 0.010, EOpp 0.015 |
| Loans calibration | A: predicted 0.671 / observed 0.693, Brier 0.206; B: 0.674 / 0.603, Brier 0.234 |
| Interpretable vs black box | logistic 0.798 / 0.777; gradient boosting 0.792 / 0.768 |
| Permutation importance (AUC drop) | tutoring 0.1445, prior attainment 0.0620, study hours 0.0514, attendance 0.0074 |
| Shapley, one instance | prediction 0.4978, base 0.7156, sum 0.2177 down; efficiency gap 0.00e+00 |
| LIME | local R² 0.259; stability mean r 0.972 (min 0.939) |
| Counterfactual | prior attainment 60.06 → 60.44, 0.034 sd, probability 0.498 → 0.541 |
| Shuffle sanity check | real max importance 0.1568 / AUC 0.731; shuffled 0.0111 / AUC 0.459 |
| Evasion ($\varepsilon=0.2$) | FGSM 0.913 → 0.030; PGD → 0.024 |
| Adversarial training | clean 0.587; at $\varepsilon=0.2$ 0.313 |
| Quantisation | adversarial 0.470 → 0.669; clean unchanged 0.913 |
| Poisoning (12 labels) | clean 0.870 (baseline 0.913); targeted error 0.182 (baseline 0.109) |
| Backdoor | clean accuracy 0.917; attack success 0.855; untriggered error 0.273 |
| Membership inference | AUC 0.513; confidence gap 0.009 |
| Model extraction | 300 queries; agreement 0.929; surrogate accuracy 0.879 |
| Prompt injection | unguarded 0.83, guarded 0.17 (content case I1 still succeeds) |
| RAG leakage | 1/5 queries before controls, 0/5 after |
| Agent tool abuse | 4/6 unsafe executions without guardrails, 0/6 with |
| Risk register | R1 residual 12 (high), R4 20 → 4, R6 20 → 6, R8 9 → 2 |
| Audit | evidence for 7 of 10 areas in the demo |

## Formulas

$$
\text{DP}=\max_g s_g-\min_g s_g,\qquad
\text{DI}=\frac{\min_g s_g}{\max_g s_g},\qquad
\text{EOpp gap}=\max_g \text{TPR}_g-\min_g \text{TPR}_g .
$$

$$
w(g,y)=\frac{\Pr(G=g)\Pr(Y=y)}{\Pr(G=g,Y=y)}
\quad\text{(Kamiran–Calders reweighing)}.
$$

$$
\phi_j=\sum_{S\subseteq F\setminus\{j\}}\frac{|S|!\,(|F|-|S|-1)!}{|F|!}
\big[v(S\cup\{j\})-v(S)\big],\qquad
\sum_j\phi_j=f(x)-\mathbb E[f].
$$

$$
x'=\operatorname{clip}\big(x+\varepsilon\,\operatorname{sign}(\nabla_x\mathcal L)\big)
\quad\text{(FGSM)}.
$$

$$
\text{risk}=\text{likelihood}\times\text{impact},\qquad
\text{residual}=\text{risk after controls}.
$$

## What actually worked

| Problem | Control that helped | Cost |
| :--- | :--- | :--- |
| Label bias in recruitment | group-specific thresholds (DP 0.076 → 0.002) | needs legal basis; different rules per group |
| Disparate selection via proxy | drop the proxy (DP 0.076 → 0.004) | 5.5 accuracy points |
| Proxy in student model | drop it (DP 0.026 → 0.009) | **+0.004** accuracy (helped) |
| Unreliable explanations | exact Shapley + efficiency check | $2^{|F|}$ evaluations |
| Opacity of local stories | report fidelity + stability | more computation |
| Evasion | adversarial training (0.030 → 0.313 at $\varepsilon=0.2$) | 32.6 points clean accuracy |
| Backdoor | provenance + post-receipt evaluation | process cost |
| Prompt injection | allowlist + default deny (0.83 → 0.17) | blocks legitimate actions too |
| RAG leakage | access control before retrieval (1/5 → 0/5) | refuses more questions |
| Tool abuse | approval gate (4/6 → 0/6) | human latency |

## What did not work, and why that matters

- **Reweighing** cannot fix conditional label bias; it only sees $P(Y\mid G)$.
- **Dropping a proxy** fixes parity, not the error-rate gap (EOpp 0.176 → 0.168).
- **Prompt wording** is not a security control; capabilities are.
- **Clean accuracy** cannot detect a backdoor — the backdoored model scored 0.917.
- **Input quantisation** raises attack cost without removing the vulnerability.
- **Detection** of injection is a logging signal, not a boundary (a paraphrase passes).

## The ten-item audit

Purpose · data provenance · performance · subgroup performance · explainability · privacy ·
security · human oversight · monitoring · documentation.

Each needs an artefact that exists, contains the required number, and is current. Seven of ten
in the demo; three deliberately missing.

## Three sentences to remember

1. Accuracy is not fairness, robustness, privacy or safety; each is a separate measurement with
   its own test set.
2. An explanation you have not evaluated — fidelity, stability, sanity — is a story.
3. Governance is a decision by a named person, with evidence, and a route to appeal.

## Key terms

See the [glossary](../../resources/glossary.md) for definitions of every bolded term in the
module, and the [module README](README.md) for the full list.

---

[Module home](README.md) · [Quiz](quizzes/quiz-13.md) ·
[Assignment](assignments/asg-13-model-card-and-audit-report.md)
