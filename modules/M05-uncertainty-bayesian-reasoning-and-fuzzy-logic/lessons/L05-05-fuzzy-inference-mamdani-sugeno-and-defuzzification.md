# L05-05 — Fuzzy Inference: Mamdani, Sugeno and Defuzzification

| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | [L05-04](L05-04-fuzzy-sets-membership-functions-and-operations.md) |
| Notebook | NB-05-01 Uncertainty Workbench |

[← Previous: L05-04](L05-04-fuzzy-sets-membership-functions-and-operations.md) · [Module home](../README.md)

## 1. Learning Objectives

- **Build** a rule base with antecedents, connectives and consequents.
- **Execute** the three inference steps: fuzzification, rule evaluation, aggregation.
- **Defuzzify** with centroid and weighted average, and compare their outputs.
- **Choose** Mamdani or Sugeno from the application's requirements.

## 2. Prerequisite Knowledge

Membership functions and fuzzy operators — [L05-04](L05-04-fuzzy-sets-membership-functions-and-operations.md).

## 3. Conceptual Explanation

### 3.1 The pipeline

```text
crisp inputs -> fuzzify -> evaluate rules -> aggregate -> defuzzify -> crisp output
```

1. **Fuzzify:** each input gets a membership in each term.
2. **Evaluate:** antecedent strength = $\min$ (AND) or $\max$ (OR) of the memberships.
3. **Implication:** clip (Mamdani, $\min$) or scale (product) the consequent term by that strength.
4. **Aggregate:** union of all clipped consequents.
5. **Defuzzify:** centroid of the aggregate, or a weighted average of rule outputs.

### 3.2 Mamdani versus Sugeno

| | Mamdani | Sugeno (TSK) |
| :--- | :--- | :--- |
| Consequent | fuzzy set | function, often a constant |
| Output | requires defuzzification | weighted average, cheap |
| Interpretability | high — rules read like sentences | lower |
| Computation | heavier | light, differentiable |
| Typical use | control with human-readable rules | optimisation, adaptive control |

### 3.3 Defuzzification choices

Centroid (centre of area) is smooth and symmetric with respect to the aggregate but ignores which
rule fired. Weighted average of rule outputs is cheaper and fails when all rule strengths are zero —
which must be handled explicitly with a default.

## 4. Worked Example — fan control

Inputs: temperature (cold/warm/hot), humidity (dry/wet). Output: fan speed (low/medium/high).

Rules:

1. IF temp is hot THEN fan is high
2. IF temp is warm AND humidity is wet THEN fan is high
3. IF temp is warm THEN fan is medium
4. IF temp is cold THEN fan is low

At temp 26 °C (hot 0.25, warm 0.6) and humidity 70% (wet 0.5):

- R1 strength 0.25 → clip *high*
- R2 strength $\min(0.6,0.5)=0.5$ → clip *high*
- R3 strength 0.6 → clip *medium*

Aggregate of the clipped sets, centroid ≈ 68% fan speed. The dominating rule is R3, not the "hot"
rule, because a 0.6 membership beats 0.25 — a result worth checking by hand.

## 5. Mathematical Formulation

Mamdani aggregation and centroid:

$$\mu_{\text{agg}}(y) = \max_i \min\left(w_i, \mu_{C_i}(y)\right), \qquad
y^\* = \frac{\int y\,\mu_{\text{agg}}(y)\,dy}{\int \mu_{\text{agg}}(y)\,dy}$$

Sugeno: $y^\* = \sum_i w_i z_i / \sum_i w_i$ with consequent values $z_i$; if $\sum_i w_i = 0$, use a
defined default.

## 6. Python Implementation

```python
def tri(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    return (x - a) / (b - a) if x <= b else (c - x) / (c - b)


def fan_control(temp, humidity):
    hot, warm, cold = tri(temp, 22, 40, 40), tri(temp, 10, 20, 30), tri(temp, 0, 0, 18)
    wet = tri(humidity, 40, 100, 100)
    w1, w2, w3, w4 = hot, min(warm, wet), warm, cold

    # Sugeno-style consequents: crisp fan speeds for low/medium/high
    speeds = {"low": 20.0, "medium": 50.0, "high": 90.0}
    rules = [(w1, "high"), (w2, "high"), (w3, "medium"), (w4, "low")]
    num = sum(w * speeds[s] for w, s in rules)
    den = sum(w for w, _ in rules)
    return (num / den if den else 0.0), {s: round(w, 2) for w, s in rules}


print(fan_control(26, 70))
print(fan_control(5, 20))
print(fan_control(35, 95))
```

## 7. Practical Applications

- **HVAC and process control** — smooth actions from imprecise sensors.
- **Braking and traction** — anti-lock logic with continuous inputs.
- **Decision systems** — loan or risk scoring with linguistic categories.
- **Consumer appliances** — the classic washing-machine and rice-cooker controllers.

## 8. Common Mistakes

- A rule base with no coverage for some input region, so the denominator is zero.
- Forgetting to clip consequents, so every rule contributes its full height.
- Comparing a Mamdani centroid with a Sugeno weighted average as if they were the same quantity.
- Rules that contradict each other with equal strength, producing a mid-range output that satisfies nobody.
- Tuning memberships by eye without a test set of inputs and expected outputs.

## 9. Exercises

1. Implement the centroid defuzzification on a discretised output universe and compare with the Sugeno value at 26 °C.
2. Add a "very hot" term and a rule; show the effect at 35 °C.
3. Find an input pair where no rule fires and implement a documented default.
4. Build a test table of 10 inputs and expected fan-speed ranges; run it.

## 10. Self-Assessment

1. What are the five steps of a fuzzy inference system?
2. Give two reasons to choose Sugeno over Mamdani.
3. What happens when all rule strengths are zero, and how should it be handled?
4. Why is the centroid called the centre of area?

## 11. Key Terms

**Fuzzification**, **rule strength**, **implication**, **aggregation**, **defuzzification**, **centroid**, **Mamdani**, **Sugeno**.

## 12. Further Reading

- Mamdani & Assilian (1975), the original steam-engine controller.
- Takagi & Sugeno (1985), fuzzy identification of systems.

## What to Do Next

Work [LAB-05-01](../labs/lab-05-01-bayesian-and-fuzzy-decision-system.md), which builds both a naive
Bayes spam filter and a fuzzy traffic controller.
