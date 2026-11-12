# QUIZ-M13 — Responsible, Explainable and Secure AI

| | |
| :--- | :--- |
| Module | M13 · Responsible, Explainable and Secure AI |
| Questions | 11 (20 marks) |
| Time | 40 minutes |
| Covers | L13-01 … L13-06 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m13.md)

---

## Part A — Multiple choice (4 marks)

**Q13.1** Demographic parity requires

- A. equal true-positive rates
- B. equal selection rates across groups
- C. equal precision
- D. equal accuracy

**Q13.2** A SHAP implementation whose values do not sum to $f(x)-\mathbb E[f]$ violates

- A. symmetry
- B. the efficiency property
- C. dummy
- D. additivity

**Q13.3** An adversarial example with $\varepsilon=0.2$ on an 8×8 image is

- A. visible to a human as a large change
- B. a bounded perturbation within the pixel range that changes the prediction
- C. a poisoned training row
- D. a membership inference query

**Q13.4** A model card's fairness section is adequate when it states

- A. that the model was designed fairly
- B. the definition chosen, the measured gap, and the threshold for action
- C. only overall accuracy
- D. that a lawyer approved it

## Part B — True or false, with a reason (2 marks)

**Q13.5** "Reweighing the training data removes disparity caused by biased labels."

## Part C — Conceptual (4 marks)

**Q13.6** (2 marks) Why is accuracy not a fairness metric? Use the recruitment numbers.

**Q13.7** (2 marks) Explain why an attribution can rank a feature first while a different feature
actually determined the decision.

## Part D — Numerical (6 marks)

**Q13.8** (3 marks) Selection rates are 0.172 (group A) and 0.096 (group B). Compute the disparate
impact ratio and state whether it falls below the 80% screening threshold.

**Q13.9** (3 marks) A membership-inference attack reports AUC 0.513 with a train–test confidence gap
of 0.009. Interpret both numbers.

## Part E — Tracing (3 marks)

**Q13.10** FGSM with $\varepsilon=0.1$ and $\text{sign}(\nabla_x L)=[+1,-1]$ applied to
$x=[0.4,0.7]$ (pixels clipped to $[0,1]$). Give $x'$.

## Part F — Python output (2 marks)

**Q13.11** What does this print?

```python
sel = {"A": 0.172, "B": 0.096}
di = min(sel.values()) / max(sel.values())
print(f"{di:.3f}", di < 0.8)
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m13.md) · [Next quiz](quiz-m14.md)
