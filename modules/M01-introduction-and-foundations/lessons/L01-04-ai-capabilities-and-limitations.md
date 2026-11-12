# L01-04 — What AI Can and Cannot Do Today

| Module | M01 · Introduction and Foundations of Artificial Intelligence |
| :--- | :--- |
| Level | 100 |
| Study time | 50 minutes |
| Prerequisites | [L01-03 Symbolic, Statistical and Generative](L01-03-symbolic-statistical-generative.md) |
| Notebook | [NB-01-01 Capability Test Bench](../notebooks/nb-01-01-capability-test-bench.ipynb) |
| Lab | [LAB-01-01 Claim Audit](../labs/lab-01-01-claim-audit.md) |

[← Previous: L01-03 The Many Faces of AI: Symbolic, Statistical and Generative](L01-03-symbolic-statistical-generative.md) · [Module home](../README.md) · [Next: L01-05 How This Course Works: Tools, Workflow and Study Habits →](L01-05-course-workflow-and-study-habits.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Auditing a Capability Claim](#4-the-procedure-auditing-a-capability-claim)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Python Implementation](#7-python-implementation)
- [8. Practical Applications](#8-practical-applications)
- [9. Common Mistakes](#9-common-mistakes)
- [10. Practical Exercises](#10-practical-exercises)
- [11. Self-Assessment](#11-self-assessment)
- [12. Key Terms](#12-key-terms)
- [13. Further Reading](#13-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Categorise** a claim about AI capability as perception, prediction, generation or action, and name the evidence that would support it.
- **Compute** the operational cost of a stated error rate at production volume, including the difference between accuracy and harm.
- **Diagnose** overconfidence from a calibration table and explain why a single accuracy figure hides it.
- **Evaluate** a real-world AI system's likely failure modes from its deployment context: distribution shift, feedback loops, and accountability.

## 2. Prerequisite Knowledge

You should already be able to:

- Distinguish symbolic, statistical and generative approaches — [L01-03](L01-03-symbolic-statistical-generative.md).
- Compute a mean and a proportion — [LP03-01](../../../prerequisites/P03-probability-and-statistics/lessons/LP03-01-descriptive-statistics.md).
- Read a Python list comprehension and a formatted print — [LP01-03](../../../prerequisites/P01-python-programming/lessons/LP01-03-conditionals-loops-and-comprehensions.md).

## 3. Conceptual Explanation

### 3.1 The intuition

Ask a room what AI can do and you get two useless answers: "everything" and "nothing". Both come from arguing about examples rather than categories.

The useful question is not *can it?* but *what kind of task is it, and what would count as evidence?* Four task families cover almost everything deployed today:

| Family | What the system does | Example | Evidence that it works |
| :--- | :--- | :--- | :--- |
| **Perception** | maps raw signal to a category or structure | speech recognition, defect detection | accuracy by class, robustness under noise |
| **Prediction** | estimates an unknown quantity from features | credit risk, demand, disease risk | held-out error, calibration, subgroup error |
| **Generation** | produces structured content | translation, summarisation, code, images | human judgement, factuality, downstream task success |
| **Action** | chooses moves in an environment | route planning, game play, robot control | solution quality, cost, safety under perturbation |

A system can be excellent in one family and hopeless in another. The current generation of language models is extraordinary at generation and prediction-from-text, mediocre at reliable multi-step action, and weak at *knowing when it does not know* — which is a property cutting across all four.

### 3.2 What works, and why it works

Three conditions explain nearly every success story:

1. **Abundant labelled or self-supervised data** in the same distribution as deployment.
2. **A cheap, well-defined objective** — next token, bounding box, click, default.
3. **A tolerance for occasional error**, or a human in the loop to catch it.

Remove any one and the system that looked impressive in a paper becomes a liability in production. Spam filtering satisfies all three. Autonomous driving satisfies (1) only partially, struggles with (2) because "safe" is not a cheap objective, and fails (3) because the cost of an error is unbounded.

### 3.3 What does not work yet, stated carefully

Avoid the two lazy extremes. These are the honest limitations:

- **Reliability at the tail.** Systems perform well on average and fail on rare inputs. Medical imaging models lose accuracy on scanners from a different manufacturer; speech models lose accuracy on accents absent from training. The tail is where harm concentrates.
- **Calibration.** A model's stated confidence is usually not its accuracy. That matters whenever a human or downstream system uses the score to decide.
- **Long-horizon planning.** Multi-step tasks compound error: at 95% per step, a twenty-step plan succeeds about 36% of the time ($0.95^{20} \approx 0.358$). This arithmetic, not mystique, is why agents need checkpoints and verification.
- **Common-sense and causal reasoning.** Systems predict correlations in text and images; they do not reliably represent what causes what, which is why they produce confident nonsense about physical situations.
- **Data hunger and cost.** Capability scales with data and compute, and both have prices — financial, environmental and legal.
- **Accountability.** When a model denies a loan, "the model decided" is not an answer a regulator accepts.

### 3.4 Real systems, described by mechanism

| System | Mechanism | Principal failure mode |
| :--- | :--- | :--- |
| Recommendation feed | learned ranking from interaction logs | feedback loops narrow what is shown, so the training data drifts |
| Fraud detection | classifier over transaction features, rules for hard blocks | adversarial shift: fraudsters adapt to the model |
| Machine translation | sequence-to-sequence neural model | confident errors on idiom, names, low-resource languages |
| Medical imaging triage | convolutional classifier prioritising scans | sensitivity to scanner and protocol differences |
| Route planning | graph search over a road network with learned travel times | stale or biased traffic estimates; map errors |
| Spam filtering | text classifier plus blocklists | false positives on legitimate bulk mail |
| Coding assistant | generative model conditioned on context | plausible code that does not compile or silently changes behaviour |

Read the middle column: every row is a *mechanism*, not a brand. That is the level at which you can reason about failure, and it is the level this course teaches.

### 3.5 Why it matters

The gap between "works in a demo" and "works in a hospital" is almost never about the model. It is about the evaluation, the data pipeline, the monitoring, and the human process around it. Learning to say precisely *which* of those is missing is the difference between an engineer and a spectator.

## 4. The Procedure: Auditing a Capability Claim

```text
FUNCTION audit(claim):
    task_family <- perception | prediction | generation | action
    dataset     <- what data was used, how collected, who is in it
    metric      <- what number is reported, on which split
    base_rate   <- how often the event happens without any model
    tail        <- what the report says about rare inputs / subgroups
    loop        <- does deployment change the data the model sees?
    RETURN table of the six fields; label each UNKNOWN where missing
```

Every field you cannot fill is a risk, not a detail. A claim with four UNKNOWNs is a hypothesis, however impressive the demonstration.

## 5. Worked Examples

### Example 1 — 99.5% accuracy, and what it costs

A system makes 2,000,000 decisions a day with 99.5% accuracy. Compute the errors:

- errors per day $= 2{,}000{,}000 \times (1 - 0.995) = 10{,}000$
- errors per minute $= 10{,}000 / 1440 \approx 6.9$

Ten thousand wrong decisions a day is not a rounding error; it is a department. Whether that is acceptable depends entirely on the task: at 10,000 mislabelled photographs, nothing happens; at 10,000 wrongly declined payments, the system is unusable. **Accuracy without a cost model is not an evaluation.**

### Example 2 — A calibration table

A model reports confidence with each prediction. Evaluation on 600 held-out cases, grouped by stated confidence:

| Stated confidence | Cases | Actually correct | Observed accuracy |
| :--- | ---: | ---: | ---: |
| 50–69% | 200 | 120 | 60.0% |
| 70–89% | 200 | 150 | 75.0% |
| 90–99% | 200 | 174 | 87.0% |

Two things to notice. The ordering is right — higher confidence does mean more accuracy, so the score carries information. But the top bucket claims at least 90% and delivers 87%, and the middle bucket claims about 80% and delivers 75%. The model is **overconfident**, and it is most overconfident exactly where people stop checking.

Expected calibration error, using bucket midpoints $p_i \in \{0.595, 0.795, 0.945\}$ and observed accuracies $\hat{a}_i$:

$$
\text{ECE} = \frac{1}{3}\sum_{i=1}^{3} \lvert \hat{a}_i - p_i \rvert = \frac{0.005 + 0.045 + 0.075}{3} \approx 0.042
$$

Four percentage points of average miscalibration. If a downstream rule says "act automatically above 90%", 13% of those automatic actions are wrong — and the model never told anyone.

### Example 3 — Compounding error in a plan

An agent completes each step correctly with probability 0.95, independently. A twenty-step plan succeeds with probability $0.95^{20} \approx 0.358$. Raise per-step reliability to 0.99 and it becomes $0.99^{20} \approx 0.818$ — still one failure in five.

This is the arithmetic argument for decomposition and verification. If each step can be checked cheaply (does the file exist? does the code compile?), the plan's success rate is governed by the checker, not by the model. Whenever you read "the agent completes long tasks", the first question is: *with what per-step verification?*

## 6. Mathematical Formulation

Accuracy and error volume:

$$
\text{errors per day} = N \cdot (1 - a), \qquad N = \text{decisions per day},\ a = \text{accuracy}
$$

Precision and recall, when the positive class is the one that matters:

$$
\text{precision} = \frac{TP}{TP + FP}, \qquad \text{recall} = \frac{TP}{TP + FN}
$$

| Symbol | Meaning |
| :--- | :--- |
| $TP, FP, FN$ | true positives, false positives, false negatives |
| $a$ | accuracy, the proportion of correct decisions |
| $p_i$ | stated confidence for bucket $i$ |
| $\hat{a}_i$ | observed accuracy for bucket $i$ |

Precision answers "when it says yes, how often is it right"; recall answers "of the real yeses, how many did it find". A fraud system tuned for recall blocks more legitimate transactions; one tuned for precision misses more fraud. Publishing only accuracy hides which trade was made.

## 7. Python Implementation

```python
decisions_per_day = 2_000_000
accuracy = 0.995

errors = decisions_per_day * (1 - accuracy)
print(f"{decisions_per_day:,} decisions/day at {accuracy:.1%} accuracy")
print(f"-> {errors:,.0f} errors/day = {errors / 24 / 60:.1f} errors/minute")

# (confidence bucket, cases, correct) from an evaluation run
buckets = [("50-69%", 200, 120), ("70-89%", 200, 150), ("90-99%", 200, 174)]
midpoints = {"50-69%": 0.595, "70-89%": 0.795, "90-99%": 0.945}

print("confidence  cases  observed accuracy")
for name, cases, correct in buckets:
    print(f"{name:>10s}  {cases:5d}  {correct / cases:16.1%}")

ece = sum(abs(correct / cases - midpoints[name]) for name, cases, correct in buckets) / len(buckets)
print(f"expected calibration error: {ece:.3f}")
```

**Output**

```text
2,000,000 decisions/day at 99.5% accuracy
-> 10,000 errors/day = 6.9 errors/minute
confidence  cases  observed accuracy
    50-69%    200             60.0%
    70-89%    200             75.0%
    90-99%    200             87.0%
expected calibration error: 0.042
```

The ECE matches the hand calculation in Example 2. Note that you could not have derived it from the accuracy on its own: calibration requires that the model reports confidence *and* that you check it.

## 8. Practical Applications

- **Clinical decision support.** A triage model is deployed with a human reading every case it flags, because recall is prioritised and the cost of a miss is high. The system's calibration determines how much the clinician can trust the score.
- **Financial compliance.** A model that blocks transactions must produce reasons. This pushes teams towards interpretable models or post-hoc explanations, and towards rules for the cases where explanations are mandatory.
- **Public services and benefits.** Error rates translate directly into wrongly denied claims. Procurement now asks for subgroup error rates and an appeals process, because aggregate accuracy hid exactly those failures in past deployments.
- **Software engineering.** Coding assistants are deployed as suggestions, not commits, because per-step error compounds and the compiler is a cheap verifier. The human review step is the verification loop that makes the tool usable.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Reporting accuracy alone | "97% accurate" with no base rate or split | One number is easy to quote | Report base rate, metric, split, and subgroup errors |
| Confusing confidence with accuracy | "The model is 95% sure" | Interfaces display a probability | Check calibration; a stated confidence is a claim, not a fact |
| Ignoring the base rate | "Our fraud model catches 99% of fraud" | Precision is invisible without prevalence | Compute precision at the real prevalence |
| Assuming independence in long tasks | "Per-step 95% means it works" | Multiplication is invisible in demos | Compute $p^n$; add verification steps |
| Treating a benchmark as deployment | "State of the art on the leaderboard" | Benchmarks are the only shared measure | Ask what differs between benchmark and deployment distribution |

## 10. Practical Exercises

1. **Cost model.** A document classifier makes 800,000 decisions a day at 98.7% accuracy. How many errors per day? If 3% of errors cause a manual correction costing 4 minutes, how many staff-hours per day does that require?
2. **Precision versus recall.** A screening test has $TP = 180$, $FP = 60$, $FN = 20$. Compute precision and recall. Then compute precision when prevalence is ten times lower with the same sensitivity and specificity. What happens, and why?
3. **Build a calibration table.** For any model you can run (even a rule of thumb), collect 30 predictions with confidence buckets and compute observed accuracy per bucket. Is it overconfident or underconfident?
4. **Compound plans.** Compute the success probability of a 12-step task at per-step reliability 0.9, 0.95 and 0.99. At which reliability does a 12-step plan exceed 50%?
5. **Audit a real system.** Choose a deployed AI product you use. Fill the six audit fields from §4. Mark the UNKNOWNs, then write one sentence on which unknown worries you most and why.

## 11. Self-Assessment

**1.** Name the four task families and give one deployed example of each.
<details><summary>Show answer</summary>

Perception — speech recognition or defect detection; prediction — credit risk or demand forecasting; generation — translation or code completion; action — route planning or game play. Each family is evaluated with different evidence: per-class accuracy, held-out error and calibration, human judgement and factuality, and solution quality or safety respectively.

</details>

**2.** A model is 99% accurate on a task where the positive class occurs in 1 in 1,000 cases, and it always predicts negative. What are its accuracy, recall and precision?
<details><summary>Show answer</summary>

Accuracy 99.9% (it is right on all 999 negatives out of 1,000). Recall 0, because it never finds a positive. Precision is undefined (no positive predictions). This is why accuracy is useless for rare events, and why class imbalance must be stated with any accuracy figure.

</details>

**3.** Using the calibration table in Example 2, what fraction of predictions in the 90–99% bucket are wrong, and why does that matter for an "auto-approve above 90%" rule?
<details><summary>Show answer</summary>

13% are wrong (100% − 87%). If the rule auto-approves whenever stated confidence exceeds 90%, then 13% of those approvals are errors — and because the rule removes human review, nobody catches them. The model's confidence is not the probability of being correct, so the threshold must be set from measured accuracy, not from stated confidence.

</details>

**4.** Compute $0.97^{30}$ and interpret it for a thirty-step agent.
<details><summary>Show answer</summary>

$0.97^{30} \approx 0.401$. Even at 97% per-step reliability, a thirty-step plan without verification succeeds about 40% of the time. The engineering response is to verify or checkpoint at intermediate steps, so that failures are detected locally instead of aborting the whole plan.

</details>

**5.** Which limitation is most relevant to a medical imaging system trained on one hospital's scanners, and what would you do about it?
<details><summary>Show answer</summary>

Distribution shift at the tail: images from different scanners have different noise, contrast and protocols, so accuracy on the training distribution overstates accuracy at a new site. Mitigate by testing on images from the target site, reporting per-site performance, and monitoring for drift after deployment rather than assuming generalisation.

</details>

## 12. Key Terms

- **Perception** — mapping raw signals to categories or structure.
- **Calibration** — agreement between stated confidence and observed accuracy.
- **Expected calibration error (ECE)** — average gap between stated confidence and observed accuracy across buckets.
- **Distribution shift** — a change in the input distribution between training and deployment.
- **Precision** — the fraction of positive predictions that are correct.
- **Recall** — the fraction of actual positives that are found.
- **Feedback loop** — a deployment effect where model outputs change the future training data.
- **Base rate** — how often the target event occurs without any model.

Definitions are collected in the [glossary](../../../resources/glossary.md).

## 13. Further Reading

- Russell, S. (2019). *Human Compatible*, Chapters 1–3. — A sober account of capability versus reliability, written before the current hype peak.
- Guo, C. et al. (2017). *On Calibration of Modern Neural Networks*. — The paper that made overconfidence a mainstream engineering concern.
- Mitchell, M. (2019). *Artificial Intelligence: A Guide for Thinking Humans*, Chapters 4–6. — Case studies of systems that worked and systems that failed, with the mechanism named.
- Sculley, D. et al. (2015). *Hidden Technical Debt in Machine Learning Systems*. — Why deployment, not modelling, is where most projects break.

## What to Do Next

Take [LAB-01-01](../labs/lab-01-01-claim-audit.md), where you apply this audit to a real claim and produce a one-page evidence table, then read [L01-05](L01-05-course-workflow-and-study-habits.md) to set up the workflow the rest of the course assumes.

---

**Navigation:** [← Previous: L01-03 The Many Faces of AI: Symbolic, Statistical and Generative](L01-03-symbolic-statistical-generative.md) · [Module home](../README.md) · [Next: L01-05 How This Course Works: Tools, Workflow and Study Habits →](L01-05-course-workflow-and-study-habits.md)
