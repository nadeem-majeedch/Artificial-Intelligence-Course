# QUIZ-M14 — Advanced AI Applications and Capstone Projects

| | |
| :--- | :--- |
| Module | M14 · Advanced AI Applications and Capstone Projects |
| Questions | 11 (20 marks) |
| Time | 40 minutes |
| Covers | L14-01 … L14-05 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m14.md)

---

## Part A — Multiple choice (4 marks)

**Q14.1** A rule gate in a hybrid system provides

- A. higher accuracy in every case
- B. a guarantee that no output violates the policy
- C. faster inference
- D. better calibration

**Q14.2** A population stability index above 0.25 conventionally indicates

- A. stable inputs
- B. a distribution shift worth acting on
- C. overfitting
- D. label leakage

**Q14.3** A GNN is likely to help when

- A. homophily is low
- B. homophily is high and features alone are weak
- C. the graph is complete
- D. depth is very large

**Q14.4** A model registry exists to record

- A. GPU temperatures
- B. model versions, metrics, owners and approval status
- C. prompt templates only
- D. training logs verbatim

## Part B — True or false, with a reason (2 marks)

**Q14.5** "8-bit quantisation always makes inference faster."

## Part C — Conceptual (4 marks)

**Q14.6** (2 marks) Why is instance-level image–text retrieval a misleading metric for a dataset
where many captions describe the same class?

**Q14.7** (2 marks) Why should a federated system report per-client accuracy as well as the global
average?

## Part D — Numerical (6 marks)

**Q14.8** (3 marks) A distilled model is 18.8 KB and its int8 version is 5.2 KB. What percentage of
the float model's size is the int8 model, to one decimal place? What is the compression factor?

**Q14.9** (3 marks) A forecast has MAE 3.79 and 80% interval coverage 0.84 with mean width 13.81.
Interpret the coverage number: is the interval too wide, too narrow, or appropriate?

## Part E — Tracing (3 marks)

**Q14.10** Two nodes have features $x_1=2$, $x_2=6$ and are connected to each other (no self-loops).
One mean-aggregation message-passing step gives both nodes the same value. What is it, and what does
that imply at depth 8?

## Part F — Python output (2 marks)

**Q14.11** What does this print?

```python
ref = [0.5] * 10
cur = [0.5] * 9 + [0.9]
p = [0.1] * 10
q = [0.1] * 9 + [0.1]
print(len(ref), len(cur), round(sum(q), 3))
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m14.md) · [Capstone](../README.md)
