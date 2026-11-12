# L06-01 — What Machine Learning Is, and What It Is Not

[← Module start](../README.md) · [Next: ? Lesson →](L06-02-data-splitting-leakage-and-cross-validation.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Framing a Problem Before You Model It](#4-the-procedure-framing-a-problem-before-you-model-it)
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

> **Module M06** · Lesson 1 of 10 · ~75 minutes · Level 300
> **Prerequisites:** P02 (vectors and gradients), P03 (probability), P04 (data preparation)

[Module overview](../README.md) · [Next lesson: L06-02 →](L06-02-data-splitting-leakage-and-cross-validation.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

1. **Define** machine learning as function approximation from data, and distinguish it from
   rule-based programming and from statistics done at scale.
2. **Place** AI, machine learning, deep learning and generative AI correctly in a containment
   diagram, and explain why the labels are not interchangeable.
3. **Classify** a problem into supervised, unsupervised, semi-supervised, self-supervised or
   reinforcement learning, and say what supervision signal each one uses.
4. **Describe** the seven-stage ML workflow and identify which stage most projects actually
   fail in.
5. **Refuse** a badly framed ML request, with a reason: no label, no baseline, no decision,
   or a target that cannot be observed at prediction time.

## 2. Prerequisite Knowledge

You should be comfortable with vectors, matrix multiplication and the idea of a derivative.
You should also know what a DataFrame is and how to compute a mean and a standard deviation.
If any of these is shaky, spend an hour in
[P02](../../../prerequisites/P02-mathematics-for-ai/README.md) and
[P04](../../../prerequisites/P04-data-preparation-and-visualization/README.md) first.

## 3. Conceptual Explanation

### 3.1 The one-sentence definition

> A computer program is said to **learn** from experience *E* with respect to some class of
> tasks *T* and performance measure *P* if its performance at tasks in *T*, as measured by *P*,
> improves with experience *E*. — Mitchell (1997)

Every word in that sentence is doing work. Take spam filtering: *T* is "label an email spam or
not", *E* is "a set of emails already labelled by users", *P* is "F1 on unseen emails". Change
*P* to accuracy and you have changed the problem, because accuracy on a 16%-spam inbox rewards
a model that never flags anything.

### 3.2 Learning versus programming

In ordinary programming you write the rule:

```python
if num_links > 2 and sender_known == 0:
    return "spam"
```

In machine learning you show examples and let the algorithm *choose* the rule. That trade has
three consequences you must keep in mind:

- **You no longer control the logic directly.** You control the data, the features, the model
  family and the objective — and you inspect what came out.
- **The rule is only as good as the examples.** Biased, stale or unrepresentative data produces
  a confident wrong rule. There is no compiler error for this.
- **You can solve problems whose rules you cannot write down** — recognising a face, ranking a
  search result — but you pay for it with statistical uncertainty.

### 3.3 AI, ML, DL, generative AI

```text
Artificial intelligence ................ the goal: systems that do tasks needing intelligence
└── Machine learning ................... the approach: improve at T with experience E
    ├── Classical ML ................... linear models, trees, k-NN, SVM, k-means
    └── Deep learning ................. many-layered neural networks
        └── Generative AI ............. models that produce text, images, audio, code
```

Deep learning is a *subset* of machine learning, not a replacement for it. On a 1,500-row
tabular loan dataset — the kind this module uses — gradient-boosted trees or logistic regression
usually match or beat a neural network, train in seconds, and can be explained to a regulator.
"The latest thing" is a hypothesis about performance, not a guarantee.

### 3.4 The five learning paradigms

| Paradigm | Supervision signal | Typical task | This module |
| :--- | :--- | :--- | :--- |
| Supervised | labelled pairs $(x, y)$ | predict a number or a class | L06-03 to L06-08 |
| Unsupervised | $x$ only | cluster, compress, detect oddities | L06-09 |
| Semi-supervised | a few labels, many unlabelled rows | classify with expensive labels | mentioned, not built |
| Self-supervised | labels generated from the data itself | predict a hidden part from the rest | mentioned, not built |
| Reinforcement | reward from interaction | choose actions over time | M10 |

Semi-supervised learning is what you do when a doctor can label 200 scans and you have 200,000.
Self-supervised learning is how language models are trained: hide the next word, predict it —
the label comes free with the text. Reinforcement learning is different in kind: the agent's
actions change what data it sees next, which is why it needs its own module.

### 3.5 The ML workflow

```text
1 Frame the problem      → what decision does this support? what is the cost of each error?
2 Collect and explore    → is there a label? is it measured before or after the outcome?
3 Prepare                → clean, impute, encode, scale, select features (L06-02)
4 Split                  → train / validation / test, before you look at anything (L06-02)
5 Fit and tune           → model families, hyperparameters, cross-validation (L06-03–06)
6 Evaluate honestly      → metrics tied to the decision, error analysis, baseline (L06-05)
7 Deploy and monitor     → drift, feedback loops, retraining policy (L06-10)
```

Stage 1 is where projects die, and it dies quietly. "Predict student success" is not a problem
statement; "flag, by week 4, the students who will fail the final exam, so an adviser can call
them, with a precision of at least 0.6" is. The second version tells you the features must be
available by week 4, that the label is the exam outcome, and that precision matters more than
recall because adviser time is the scarce resource.

### 3.6 What ML is bad at

- **Things with no data.** A model cannot learn a rare event it has seen twice.
- **Things that change.** A model trained on last year's applicants fails on this year's if the
  application form, the economy or the policy changed. This is distribution shift.
- **Causal questions.** A model that predicts loan approval from postcode has learned history,
  not merit. Prediction is not explanation and neither is causation.
- **Guarantees.** A 97% accurate fraud detector is wrong 3% of the time, and on 5,000
  transactions per day that is 150 mistakes. State the error rate in units of decisions, not
  percentages.

## 4. The Procedure: Framing a Problem Before You Model It

1. **Name the decision.** Who acts differently because of the prediction, and what do they do?
2. **Name the label.** What exactly is measured, when, and by whom? If it is measured after the
   decision, it may be a consequence rather than a target.
3. **Name the features available at prediction time.** Anything else is leakage.
4. **Name the cost asymmetry.** A missed fraud versus a blocked legitimate card; a missed
   at-risk student versus an unnecessary call.
5. **Choose the metric from the cost.** Accuracy only when classes and costs are balanced.
6. **Set the baseline.** Majority class, last year's rule, or the current human process. A model
   that cannot beat the baseline is not progress.
7. **Decide what "good enough" means before you see the test score.** Otherwise the score will
   define it for you.

## 5. Worked Examples

### Example 1 — Classify the task

| Request | Paradigm | Why |
| :--- | :--- | :--- |
| Predict a house's sale price | Supervised regression | Continuous label, historical sales |
| Group customers by buying behaviour | Unsupervised clustering | No label exists; the grouping is the output |
| Flag fraudulent transactions | Supervised classification (or anomaly detection) | Historical chargebacks, but only 0.8% positive |
| Predict the next word in a sentence | Self-supervised | The next word is its own label |
| Keep a robot upright | Reinforcement learning | Reward from falling or not falling |

### Example 2 — Why 70% accuracy can be worthless

The loan dataset in `code/datasets.py` has 1,500 applications of which 30% are approved.
A model that always predicts "rejected" is correct on the 70% rejected applications:

```text
majority baseline accuracy : 0.701
```

It has learned nothing, and any report that quotes only accuracy cannot tell it apart from a
real model. Now look at balanced accuracy on the two classes, or simply at recall for the
approved class, which is **0** for that baseline. This is the single most common way an ML
report misleads its reader, and it is why L06-05 exists.

### Example 3 — A prediction that cannot be made at prediction time

A team building a "will this student pass?" model includes `final_score` as a feature. Test
accuracy becomes **1.000**. The feature is the outcome. When the same pipeline is run on data
from week 1 of term, the feature does not exist. This is target leakage; LAB-06-04 is a
systematic hunt for it.

## 6. Mathematical Formulation

Supervised learning assumes an unknown joint distribution $P(X, Y)$ and a loss
$\ell(\hat{y}, y)$. The goal is a function $f$ from a hypothesis class $\mathcal{H}$ that
minimises the **risk**

$$
R(f) = \mathbb{E}_{(X,Y)\sim P}\big[\ell(f(X), Y)\big].
$$

You never see $P$; you see a sample of $n$ rows and minimise the **empirical risk**

$$
\hat{R}_n(f) = \frac{1}{n}\sum_{i=1}^{n}\ell(f(x_i), y_i).
$$

The gap between the two is the whole subject of generalisation (L06-06). A model can have
$\hat{R}_n = 0$ and $R$ close to a coin flip — the unlimited-depth decision tree in L06-06 does
exactly that.

For classification with two classes, a model usually outputs a score $s(x)\in[0,1]$ and you
choose a threshold $t$: predict positive when $s(x) \ge t$. The threshold is a decision about
costs, not a property of the model.

## 7. Python Implementation

The module's data generators are deterministic: the same seed gives the same rows on every
machine, so every number in these lessons can be reproduced.

```python
# run from modules/M06-machine-learning-fundamentals/code
import datasets as ds

print(ds.summary().to_string(index=False))
```

```text
     dataset  rows  columns                                                        task                      target positive_rate
    students   600        9 regression (final_score) and binary classification (passed)        final_score / passed         0.728
      houses   800        9                                                  regression             price_thousands             -
      emails  1200        9                           binary classification                     is_spam         0.158
    customers   500        6                                                   clustering none (four latent segments)             -
       loans  1500        8                           binary classification                     approved         0.300
   intrusion  3000       11                           binary classification                    is_attack         0.211
   attrition  1400       10                                                  binary classification                   attrition         0.159
transactions  5000        8                   anomaly detection / binary classification           is_fraud         0.008
```

Every one of these is synthetic and generated in-script. Each mirrors the schema of a real
public dataset named in `datasets.DATASETS`, so the labs can swap in the real file; the synthetic
rows must never be reported as real data.

A first look at one dataset:

```python
import datasets as ds
from prep import describe_frame

frame = ds.students()
print(describe_frame(frame).to_string(index=False))
print("pass rate:", round(frame["passed"].mean(), 3))
```

```text
            column  dtype  missing  unique    min    max
       study_hours float64        0     469    0.0  21.26
    attendance_pct float64       21     286   45.6  100.0
       prior_grade float64        0     369   18.4  100.0
       sleep_hours float64       14     329   3.81  10.19
     part_time_job     str        0       2      -      -
parental_education     str        0       3      -      -
  internet_at_home     str        0       2      -      -
       final_score float64        0     552  34.58  84.51
            passed   int64        0       2      0      1
pass rate: 0.728
```

Read that table before modelling anything. The missing values tell you an imputer is needed;
the `str` dtypes tell you an encoder is needed; `final_score` tells you which column is *not*
allowed to be a feature when the target is `passed`.

## 8. Practical Applications

- **Credit scoring** — supervised classification with a legally constrained feature set and an
  explicit adverse-action explanation requirement.
- **Predictive maintenance** — supervised regression on sensor windows, but labels are rare
  because failures are rare; often reframed as anomaly detection.
- **Customer segmentation** — unsupervised clustering used for marketing, with the clusters
  named by humans after inspection.
- **Recommendation** — a hybrid: supervised ranking plus self-supervised embeddings.
- **Demand forecasting** — regression with strong seasonality; naive seasonal baselines are
  surprisingly hard to beat.

## 9. Common Mistakes

1. **"More data always helps."** More *relevant* data helps; more rows of the same biased
   sample does not fix label bias.
2. **"Deep learning is the modern approach, so use it."** On tabular data with hundreds of rows,
   it usually loses to a linear model or a small forest.
3. **Reporting accuracy on imbalanced data.** See Example 2.
4. **Treating a prediction as an explanation.** Feature importance is not causation.
5. **Skipping the baseline.** Without one, you cannot tell whether the model is useful.
6. **Framing as ML when a rule would do.** If the policy is "reject under 18", write the rule.

## 10. Practical Exercises

1. For each of the eight datasets in `datasets.DATASETS`, write the task type, the label, the
   decision it supports, and one cost asymmetry.
2. Take the loan dataset and compute: majority-class accuracy, and the recall of that baseline
   for approved applications. Explain the difference in one sentence.
3. Write a problem statement for a system that predicts which library books will be overdue.
   Include the decision, the label, the prediction time, and the metric.
4. Find one feature in `datasets.students()` that would be leakage for a week-1 prediction and
   explain why.
5. Give an example where self-supervised learning is the only practical option, and one where
   semi-supervised learning is.

## 11. Self-Assessment

**Multiple choice**

1. Which statement is correct?
   a) All AI is machine learning. b) Deep learning is a subset of machine learning.
   c) Machine learning requires reinforcement learning. d) ML and statistics are unrelated.
2. A spam filter scores 98% accuracy on an inbox that is 2% spam. The model most likely
   a) is excellent. b) predicts "not spam" almost always. c) has high recall. d) is overfitted.
3. A model that predicts employee attrition from `exit_interview_score` has
   a) a strong feature. b) target leakage. c) class imbalance. d) no baseline.

**Short answer**

4. Explain why the choice of performance measure *P* changes which model you should ship.
5. Give two reasons a model can be accurate and useless.

<details>
<summary>Answers</summary>

1. **b**. 2. **b** — with 2% positives, predicting the majority gives 98%.
3. **b** — an exit-interview score exists only after the employee leaves.
4. Because the measure encodes the cost of errors. With rare positives, accuracy rewards
   ignoring them; F1 or recall rewards catching them. The shipped model should optimise the
   measure that matches the decision.
5. It can be accurate by predicting the majority class, and it can be accurate on data that no
   longer resembles the deployment population.

</details>

## 12. Key Terms

**Machine learning**, **supervised learning**, **unsupervised learning**, **semi-supervised
learning**, **self-supervised learning**, **reinforcement learning**, **label**, **feature**,
**target**, **hypothesis class**, **empirical risk**, **generalisation**, **baseline**,
**distribution shift**, **target leakage**, **class imbalance**.

All are defined in the [glossary](../../../resources/glossary.md).

## 13. Further Reading

- Mitchell, T. (1997). *Machine Learning*, Chapter 1. — The definition and the framing.
- Géron, A. (2022). *Hands-On Machine Learning*, Chapter 1. — The workflow, with code.
- Sculley, D. et al. (2015). *Hidden Technical Debt in Machine Learning Systems*. — What happens
  after the model works.

## What to Do Next

1. Run `python datasets.py` and `python prep.py` from the module's `code/` directory.
2. Do exercises 1–4; you will reuse the answers in LAB-06-01.
3. Continue to [L06-02 — Data Preparation, Splitting and Leakage](L06-02-data-splitting-leakage-and-cross-validation.md).

---

**Navigation:** [← Module start](../README.md) · [Next: ? Lesson →](L06-02-data-splitting-leakage-and-cross-validation.md)
