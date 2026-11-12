# Glossary — Applications (M14)

From model to product: serving, monitoring, efficiency and the capstone. Back to the
[glossary index](README.md).

## B

### Batch inference
**Abbreviation.** — · **Module.** M14
**Simple definition.** Scoring a whole dataset at once and writing the results to a table.
**Detailed explanation.** Batch trades freshness for throughput and cost: one large job amortises
start-up and uses hardware efficiently. It is the right default when decisions are not
latency-sensitive.
**Mathematics.** —
**Practical example.** A nightly churn score over 2 million customers takes 40 minutes on one GPU
and costs a fraction of serving the same 2 million requests online.
**Related.** [Online inference](#online-inference), [Model serving](#model-serving)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

## C

### Canary deployment
**Abbreviation.** — · **Module.** M14
**Simple definition.** Routing a small share of traffic to a new model and rolling back
automatically if a metric breaches.
**Detailed explanation.** Canaries bound the blast radius of a bad model. They only work if the
monitoring metric is aligned with the harm you care about and the rollback is automatic, not
someone's judgement at 3 a.m.
**Mathematics.** —
**Practical example.** 5% of traffic goes to v2 for an hour; error rate rises 0.4 points above the
threshold, and the router returns all traffic to v1 in under a minute.
**Related.** [Monitoring](#monitoring), [Drift](#drift), [Model serving](#model-serving)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

## D

### Distillation
**Abbreviation.** — · **Module.** M14
**Simple definition.** Training a small model to imitate a large one's outputs.
**Detailed explanation.** The student learns the teacher's softened distribution, which carries
more information than hard labels. Distillation buys latency and cost at some accuracy, and it is
the standard way to ship a research model in production.
**Mathematics.** $L = \text{KL}\!\left(p_{\text{teacher}}^{T} \,\|\, p_{\text{student}}^{T}\right)$ with temperature $T$.
**Practical example.** A 6-layer student distilled from a 24-layer teacher keeps 97% of accuracy
at 3.6× the throughput.
**Related.** [Quantisation](#quantisation), [Model serving](#model-serving)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

### Drift
**Abbreviation.** — · **Module.** M14
**Simple definition.** A change in the data or the input–output relationship that degrades a
deployed model.
**Detailed explanation.** Data drift moves the input distribution; concept drift changes what the
correct answer is for the same input. The first is detectable without labels, the second is not,
which is why label delay determines how fast you can notice.
**Mathematics.** $P(X)$ changes (data drift); $P(Y \mid X)$ changes (concept drift).
**Practical example.** A fraud model's inputs shift when a payment provider changes its checkout,
and precision falls 12 points before any label arrives.
**Related.** [Monitoring](#monitoring), [Canary deployment](#canary-deployment)
**Where it is taught.** [L14-03 Monitoring, drift and continuous evaluation](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-03-monitoring-drift-and-continuous-evaluation.md)

## M

### Model serving
**Abbreviation.** — · **Module.** M14
**Simple definition.** Running a trained model behind an interface that answers requests.
**Detailed explanation.** Serving is an engineering problem: batching, concurrency, cold starts,
versioning and rollback. The model is a small part of the system, and most incidents are
infrastructure, configuration or schema mismatches.
**Mathematics.** —
**Practical example.** A FastAPI service batches up to 16 requests within 20 ms, cutting p95
latency from 180 ms to 45 ms without changing the model.
**Related.** [Online inference](#online-inference), [Batch inference](#batch-inference), [Canary deployment](#canary-deployment)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

### Monitoring
**Abbreviation.** — · **Module.** M14
**Simple definition.** Continuously measuring a deployed system's inputs, outputs and outcomes.
**Detailed explanation.** Monitoring covers four layers: infrastructure, data quality, model
metrics and business outcomes. A dashboard that shows only infrastructure health will be green
while the model is wrong.
**Mathematics.** —
**Practical example.** Alerting on prediction-distribution shift catches a broken feature pipeline
two days before the accuracy dashboard moves, because labels arrive weekly.
**Related.** [Drift](#drift), [Canary deployment](#canary-deployment)
**Where it is taught.** [L14-03 Monitoring, drift and continuous evaluation](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-03-monitoring-drift-and-continuous-evaluation.md)

## O

### Online inference
**Abbreviation.** — · **Module.** M14
**Simple definition.** Scoring a single request at the moment it arrives.
**Detailed explanation.** Online inference must meet a latency budget, which constrains model size,
batching and feature computation. The hard part is usually the feature store, not the model.
**Mathematics.** —
**Practical example.** A card authorisation must answer in under 100 ms; a gradient-boosted model
with precomputed features takes 8 ms, a large transformer would not fit the budget.
**Related.** [Batch inference](#batch-inference), [Model serving](#model-serving), [Quantisation](#quantisation)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

## Q

### Quantisation
**Abbreviation.** — · **Module.** M14
**Simple definition.** Storing and computing with lower-precision numbers to shrink a model and
speed it up.
**Detailed explanation.** 8-bit integers are four times smaller than 32-bit floats and use faster
arithmetic, at a small accuracy cost that is usually recoverable with calibration. It is the
cheapest serving optimisation available.
**Mathematics.** $w_q = \text{round}(w / s) + z$, with scale $s$ and zero point $z$.
**Practical example.** 8-bit quantisation cuts a 500 MB model to 130 MB and halves latency, losing
0.6 accuracy points on the evaluation set.
**Related.** [Distillation](#distillation), [Online inference](#online-inference)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

## R

### Reproducibility (research)
**Abbreviation.** — · **Module.** M14
**Simple definition.** The ability to obtain the same result from the same code, data and
configuration.
**Detailed explanation.** Reproducibility requires more than a repository: seeds, versions, data
snapshots and hardware matter. Reading a paper critically means locating what was not reported —
baselines, variance, compute.
**Mathematics.** —
**Practical example.** A paper reports a single seed and no variance; re-running it with five
seeds gives a spread wider than the claimed improvement.
**Related.** [Monitoring](#monitoring), [Drift](#drift)
**Where it is taught.** [L14-04 Reading and reproducing AI research](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-04-reading-and-reproducing-ai-research.md)

## S

### Shadow deployment
**Abbreviation.** — · **Module.** M14
**Simple definition.** Running a new model alongside the live one without using its output.
**Detailed explanation.** Shadow mode measures how a candidate would behave on real traffic before
it affects anyone. It cannot measure outcomes that require action, which is why it complements
rather than replaces a canary.
**Mathematics.** —
**Practical example.** A candidate recommender runs for a week on live traffic; its agreement with
the incumbent is 71%, and the disagreements are reviewed before any rollout.
**Related.** [Canary deployment](#canary-deployment), [Monitoring](#monitoring)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

## T

### Throughput and latency budget
**Abbreviation.** — · **Module.** M14
**Simple definition.** The requests a system handles per second, and the time one request is
allowed to take.
**Detailed explanation.** The two trade against each other through batching and model size. A
budget is a design constraint: it decides the model, the hardware and the batching policy before
any code is written.
**Mathematics.** $\text{throughput} \approx \frac{\text{batch size}}{\text{latency per batch}}$
**Practical example.** A 250 ms p95 budget with 40 ms model time leaves room for one retry and a
feature lookup, and rules out a 900 ms reranker.
**Related.** [Online inference](#online-inference), [Quantisation](#quantisation), [Model serving](#model-serving)
**Where it is taught.** [L14-02 From model to product: MLOps and serving](../../modules/M14-advanced-ai-applications-and-capstone/lessons/L14-02-from-model-to-product-mlops-and-serving.md)

---

[Glossary index](README.md) · [Responsible AI](responsible-ai.md) · [Foundations](foundations.md) · [Quick reference](../glossary.md)
