# LAB-P02-02 — Gradient Descent by Hand

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Effort | 2.5 hours, suggested split: session 1 = tasks 1–3, session 2 = tasks 4–6 |
| Lessons covered | [LP02-04](../lessons/LP02-04-derivatives-partial-derivatives-and-gradients.md), [LP02-05](../lessons/LP02-05-optimization-fundamentals.md) |
| Dataset | generated in the lab (fixed seed) |
| Notebook | [NB-P02-02](../notebooks/nb-p02-02-calculus-and-optimization.ipynb) — support for the descent traces |

[← Unit home](../README.md) · [Prerequisites home](../../README.md)

## Scenario

A courier company records daily delivery volume and the number of riders on shift. The operations
manager, Ms. Rabia, wants a one-line rule — "each extra rider handles about $k$ more parcels" — that she
can use for shift planning next month. She distrusts the spreadsheet's built-in trendline because nobody
can say what it minimises. She wants the loss function written down, the gradient derived, and the fit
produced by a method she can explain to her supervisor.

## Your role

You are the analyst on the task. You report to Ms. Rabia and you will be judged on **explainability**:
the fit must come from an algorithm whose every step you can describe without a library.

## What you are given

| Item | Location | Notes |
| :--- | :--- | :--- |
| Daily records | generated in Task 1 | 80 days, two columns |
| Starter code | none | NumPy and Matplotlib only |
| Constraints | — | no scikit-learn, no SciPy optimisers, no `np.polyfit` |

**Not provided:** initialisation values, a learning rate, or a convergence criterion. Choosing them,
and being able to justify the choice, is the exercise.

## Requirements

**Functional**

- R1 — Generate `riders` uniform on $[5, 25]$ and `parcels` = $3 \times \text{riders} + 40 + \varepsilon$
  with $\varepsilon \sim \mathcal{N}(0, 25)$, using a fixed seed.
- R2 — Implement mean squared error and its two partial derivatives for the model
  $\hat{y} = wx + b$ in closed form.
- R3 — Verify both partials numerically with central differences at the initial parameters.
- R4 — Implement gradient descent with a step budget, a tolerance on the gradient norm, and a stored
  loss history.
- R5 — Compare the fitted $(w, b)$ with `np.linalg.lstsq` and report the difference in the loss.

**Non-functional**

- N1 — The whole script runs in under 5 seconds.
- N2 — Same seed, same numbers, every run.
- N3 — No library performs the optimisation; `lstsq` is used only for the final comparison.

## Tasks

1. **Generate and plot.** Produce the 80-day dataset and a scatter of parcels against riders, with axis
   labels carrying units. *(success: the scatter shows a clear upward trend and no obvious curvature)*
2. **Write the loss.** Implement `mse(w, b, x, y)` returning a float, and confirm it equals the mean of
   squared residuals computed by hand for `w=0, b=0`. *(success: your value matches a two-line check to
   1e-9)*
3. **Derive the gradient.** Write `grad(w, b, x, y)` returning
   $\left(\frac{2}{n}\sum x_i(\hat{y}_i - y_i),\ \frac{2}{n}\sum(\hat{y}_i - y_i)\right)$, then compare
   it with central differences at three random parameter pairs. *(success: relative difference below
   1e-6 for all three)*
4. **Run descent.** Start from $(0, 0)$, run 200 steps with $\eta = 0.01$, and plot the loss history on a
   log scale. *(success: the curve decreases monotonically and flattens)*
5. **Compare learning rates.** Repeat with $\eta \in \{0.001, 0.01, 0.02\}$ and plot all three loss
   curves together. Identify which converges fastest and which diverges, and connect the divergence to
   the curvature of the problem. *(success: you can name the approximate bound on $\eta$ for your data)*
6. **Report to the manager.** Give the fitted rule in one sentence with units, the loss, a comparison
   with `lstsq`, and one limitation — for example that the relationship is assumed linear and constant
   over the month.

## Deliverables

| File | Contents |
| :--- | :--- |
| `lab_p02_02.py` | Runnable script implementing R1–R5 |
| `descent_traces.png` | Loss curves for the three learning rates, log scale, legend |
| `fit.png` | Scatter with the fitted line and its equation in the title |
| `report.md` | ≤ 500 words: derivation, convergence evidence, the rule, the limitation |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Derivation and verification | 35% | Both partials correct, numeric check passes at several points | Correct but unverified | Wrong factor or sign |
| Optimisation behaviour | 25% | Learning-rate comparison explained via curvature | Runs, results reported | Does not converge or no analysis |
| Code quality | 20% | Clear functions, docstrings, reproducible | Works, monolithic | Does not run |
| Communication | 20% | The rule is quotable and the limitation is real | Understandable | Numbers without meaning |

## Extension challenges

1. **Standardise the feature.** Divide `riders` and `parcels` by their standard deviations, rerun with the
   same learning rates, and explain why convergence changes.
2. **Momentum.** Add a velocity term $v \leftarrow \beta v + \nabla L$ and
   $\theta \leftarrow \theta - \eta v$. Report how many steps are needed with $\beta = 0.9$.
3. **Two features.** Add a weekend indicator and extend the gradient to three parameters. Verify
   numerically before running.

## Hints

<details><summary>Hint 1 — getting started</summary>

Write the residual vector $\hat{y} - y$ once and reuse it in both partials; recalculating it in each
expression is the most common source of mismatched gradients.

</details>

<details><summary>Hint 2 — the likely sticking point</summary>

With `riders` up to 25, the loss surface is steep, so $10^{-2}$ may already be near the stability limit
and larger values will oscillate. If the loss jumps between two values, halve the learning rate rather
than adding iterations.

</details>

<details><summary>Hint 3 — checking your work</summary>

Three invariants: the numeric and analytic gradients agree; the loss never increases under a stable
learning rate; and your final loss is within a few percent of `lstsq`'s. If the third fails while the
first two pass, you have converged to a different point than the optimum — check the sign convention in
the update.

</details>

## Reflection

1. Gradient descent needed hundreds of steps for a problem that `lstsq` solves in one. When is the
   iterative method the right choice anyway?
2. What does the log-scale loss curve tell you that a linear-scale one would hide?
3. If Ms. Rabia doubled the number of riders next month, would your rule still apply? What would you
   need to check?

## Time budget

| Session | Tasks | Time |
| :--- | :--- | ---: |
| 1 | 1–3 | 75 min |
| 2 | 4–6 | 75 min |
