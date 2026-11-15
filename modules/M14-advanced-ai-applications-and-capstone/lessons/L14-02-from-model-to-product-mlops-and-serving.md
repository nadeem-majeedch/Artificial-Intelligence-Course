# L14-02 — From Model to Product: Serving, Compression and MLOps

| | |
| :--- | :--- |
| Level | 400 |
| Study time | 90 minutes |
| Prerequisites | M07, M11 (quantisation), L14-01 |
| Code | `code/efficiency.py` |

[← Previous: L14-01 AI in Practice: Case Studies, Hybrid and Neuro-Symbolic Systems](L14-01-ai-in-practice-case-studies-and-hybrid-systems.md) · [Module home](../README.md) · [Next: L14-03 Monitoring, Drift and Continuous Evaluation →](L14-03-monitoring-drift-and-continuous-evaluation.md)

## Why this lesson exists

A model that scores well is not a system. Between the notebook and the product sit four
constraints that never appear in a research paper: a latency budget, a memory budget, a
deployment target, and a lifecycle that has to keep working after you stop looking at it.

This lesson measures the three compression techniques everyone recommends and reports what they
actually cost here. Two of the results are counter-intuitive: distillation gained nothing, and
8-bit quantisation made inference slower.

## What you will be able to do

1. Sketch a serving path and assign a latency budget to each stage.
2. Compare distillation, quantisation and pruning on accuracy, size and latency together.
3. Explain why a smaller model can be slower, and when quantisation pays.
4. Describe what a model registry, canary and rollback are for.
5. Write an MLOps section that names artefacts and versions, not intentions.

---

## 1. The serving lifecycle

```text
train -> evaluate -> package -> registry -> deploy (shadow/canary) -> monitor -> retrain
             ^                                                            |
             +------------------------ retirement -----------------------+
```

Each arrow is an artefact with an identity:

| Stage | Artefact | Failure if missing |
| :--- | :--- | :--- |
| Train | data snapshot + code commit + seed | cannot reproduce the model |
| Evaluate | evaluation report tied to a model hash | cannot compare versions |
| Package | container or bundle with pinned dependencies | works on one machine |
| Registry | version, metrics, owner, approval | nobody knows what is live |
| Deploy | rollout plan and rollback trigger | a bad model stays up |
| Monitor | metrics, thresholds, on-call owner | drift goes unnoticed |
| Retire | decommission date and data plan | stale model keeps deciding |

Two serving patterns cover most cases:

- **Batch**: score everything nightly, write to a table. Simple, cheap, and stale by design.
- **Online**: score per request. Needs a latency budget, a fallback when the model is slow, and
  a versioned endpoint.

A latency budget is a subtraction problem. For a 200 ms request: 20 ms network, 30 ms feature
fetch, 100 ms inference, 50 ms headroom. If inference cannot fit, compress — or change the
requirement.

## 2. Three compressions, measured

`efficiency.py` trains a teacher and a student on 8×8 digits, then compresses:

```text
model                   accuracy   size KB    params   us/example (5 runs)
teacher                    0.967     332.0     85002     130.6–149.8
student (scratch)          0.902      18.8      4810      60.3–90.9
student (distilled)        0.898      18.8      4810      68.6–93.0
distilled int8             0.898       5.2        74     118.1–161.5
distilled 50% pruned       0.865      18.8      4810      59.3–90.3
```

Accuracy and size are deterministic under the fixed seed. Latency is a single-example CPU wall-clock
measurement and varies between runs, so the table reports the observed range.

**Measurement record.** Five independent runs on 15 November 2026: Windows 11
(`Windows-11-10.0.26300-SP0`), Intel64 Family 6 Model 142, Python 3.14.7, PyTorch 2.14.1+cpu,
NumPy 2.5.3, 4 PyTorch threads, CPU only. Model: the 4,810-parameter student trained for 40 epochs
on scikit-learn's 8×8 digits (`load_digits`, 1,797 examples, 70/30 stratified split, seed 0). The
harness warms up for 20 calls and reports the median of three trials of 300 single-example forward
passes, in eval mode and `torch.no_grad()`. Threads were not pinned and background load was not
controlled, which is why a range is reported. This is a desktop-CPU observation, not a target-device
or universal claim.

Read the columns in pairs, because each compression trades one for another.

### Distillation

The student reaches 0.902 on its own and 0.898 with the teacher's soft labels: a gain of
**−0.004**, i.e. nothing. The sweep agrees:

```text
temperature    alpha    accuracy
        1.0      0.3       0.872
        2.0      0.7       0.865
        4.0      0.3       0.811
        8.0      0.3       0.791
```

On an easy, low-capacity-bottleneck task the student can learn the mapping from hard labels
alone, so there is nothing for the teacher to add; and too high a temperature dilutes the signal
(it loses 0.08 at T=8, α=0.3). Distillation earns its keep when the student is capacity-limited
relative to the task, or when soft labels carry structure the hard label hides (class
similarity, label noise). **Measure it; do not assume it.**

The 0.902 student also beats the distilled one on accuracy; their latency ranges overlap, because
distillation changes training, not the inference graph, so any timing difference is measurement
noise.

### Quantisation

Symmetric per-output-channel int8 cuts the student from 18.8 KB to 5.2 KB (27.7%) at identical
accuracy (0.898; no class changed by more than 0.0005). In release validation it was **1.61–2.35×
slower** across five runs (median 1.68×). The earlier text reported 2.62× from one run on an
unrecorded machine; that value should be treated as a historical observation, not a reproducible
constant.

That slowdown is not a bug. This implementation dequantises weights on every forward pass —
multiply the int8 tensor by the scale, then run a float matmul. The arithmetic saved is smaller
than the conversion cost, so the model gets smaller and can be slower.

Quantisation pays when one of these is true:

- the target has int8 kernels (most mobile NPUs and server inference engines do);
- the bottleneck is memory bandwidth, not arithmetic;
- the model is large enough that weight loading dominates (a 7B-parameter model, not an 85k one).

Note also the `params` column: 74. Int8 weights are stored as buffers, not parameters, so the
parameter count is meaningless for a quantised model. **Report bytes, not parameter counts.**

### Pruning

50% of weights set to zero: accuracy 0.865 (−0.033), size unchanged (18.8 KB), latency ratio
0.80–1.30× across five runs (median 1.01×). That is no reliable speed change, not a demonstrated
slowdown; the earlier text's single-run 1.45× is historical. Dense storage and dense arithmetic do
not care that a value is zero. Pruning without a sparse kernel, a sparse format, or hardware
support buys nothing at inference.

Where pruning does pay: structured pruning (removing whole channels) with a smaller dense
matrix as the result, or unstructured pruning followed by sparse-aware hardware. Both need to be
measured on the target.

### The honest summary

| Method | Accuracy | Size | Latency | Verdict here |
| :--- | ---: | ---: | ---: | :--- |
| Distillation | −0.004 vs scratch | 5.7% of teacher | no inference change | no gain at this capacity |
| int8 | ±0.000 | 27.7% of float | 1.6–2.4× slower (median 1.7×) | size win, speed loss |
| Pruning 50% | −0.033 | 100% | 0.8–1.3× (median 1.0×) | storage claim only |

Every row is a trade, and none of them is "free efficiency". The ranges are five-run desktop-CPU
observations, not guarantees for another CPU, a mobile NPU or a serving runtime with int8 kernels.

## 3. Edge AI

Edge deployment adds constraints that change the design:

| Constraint | Consequence |
| :--- | :--- |
| Memory (often < 100 MB) | aggressive quantisation, small models |
| Power / thermal | sustained throughput, not peak |
| Intermittent connectivity | on-device inference, queued sync |
| No GPU, sometimes no FPU | int8 kernels or fixed point |
| Update latency | versioned bundles, rollback on device |
| Privacy | data stays local, which is often the point |

The measurement discipline does not change: accuracy, size, latency and energy on the *target*
device. A desktop CPU measurement is a hypothesis about the device, not a result.

## 4. Inference optimisation beyond compression

- **Batching.** Throughput rises with batch size; latency per request usually rises too. Choose
  which one your SLA is about.
- **Operator fusion.** Merge consecutive elementwise ops so intermediate tensors are never
  written to memory. This is why framework-specific runtimes beat naive PyTorch eager.
- **Caching.** For language models, the KV cache (M11) turns O(n²) recomputation into O(n); for
  retrieval, an embedding cache removes most encoder calls.
- **Distillation of the pipeline**, not just the model: replace a three-model cascade with one
  model that approximates it, then measure the error of the whole cascade.
- **Early exit / cascades.** Cheap model first, expensive model only on low confidence. Report the
  distribution of paths taken, or you cannot reason about cost.

## 5. MLOps: the minimum viable version

You do not need a platform team to do this correctly. Six things:

1. **Version everything**: data snapshot, code commit, hyperparameters, random seed, model hash.
2. **One command reproduces the evaluation** from the model hash.
3. **A registry row per model**: version, metrics, owner, approval status, deployment target.
4. **Shadow deploy** the new model alongside the old, comparing predictions on live traffic.
5. **Canary** 5% of traffic with automatic rollback on a metric breach.
6. **Retire explicitly** — a decommission date and a plan for the data.

The most common failure is not a missing platform; it is a model whose evaluation cannot be
reproduced, so nobody can tell whether the new version is better.

## Common mistakes

| Mistake | Why it is wrong | Do instead |
| :--- | :--- | :--- |
| Reporting only accuracy for a compressed model | hides size/latency trade | report all four columns |
| Assuming quantisation is faster | measured 1.6–2.4× slower on CPU float kernels | benchmark on the target |
| Assuming distillation always helps | measured −0.004 | compare against training without the teacher |
| Reporting parameter counts for int8 | weights are buffers | report bytes |
| Measuring latency on the dev laptop | not the deployment target | measure on target hardware |
| No rollback plan | a bad model stays live | canary with automatic rollback |

## Exercises

**Beginner.** Run `python efficiency.py`. Copy the five-row table and state, for each row, which
column it improved and which it degraded.

**Beginner.** Change the pruning fraction to 0.9 and rerun. Report accuracy and sparsity. Does
latency improve?

**Intermediate.** Implement batched inference at batch sizes 1, 8, 32, 128 and report throughput
(examples/second) alongside per-example latency. At what batch size does throughput stop
improving?

**Intermediate.** Make quantisation faster: precompute the dequantised weight matrix once, cache
it, and re-measure. Report the new latency and explain why the result changes.

**Advanced.** Distil the teacher into a student on a harder task (add label noise at 20%) and
report whether distillation helps there. Explain the difference from this task.

**Advanced.** Write the registry row and rollback plan for a model you would actually deploy:
fields, thresholds and who is paged.

## Self-check

1. Why did distillation gain nothing here?
2. Why was int8 slower, and name two conditions under which it would be faster.
3. What does pruning require before it improves latency?
4. Why is the parameter count misleading for a quantised model?
5. List the six artefacts a minimal MLOps setup needs.

## Key terms

**Serving**, **latency budget**, **batch inference**, **online inference**, **distillation**,
**soft labels**, **temperature**, **quantisation**, **int8**, **per-channel scale**, **pruning**,
**structured pruning**, **sparsity**, **operator fusion**, **batching**, **KV cache**,
**canary deployment**, **shadow deployment**, **model registry**, **rollback**.

## Further reading

- Hinton, Vinyals & Dean (2015). *Distilling the Knowledge in a Neural Network*.
- Jacob et al. (2018). *Quantization and Training of Neural Networks for Efficient
  Integer-Arithmetic-Only Inference*.
- Han, Mao & Dally (2016). *Deep Compression*.
- Sculley et al. (2015). *Hidden Technical Debt in Machine Learning Systems*.

---

[Previous: L14-01](L14-01-ai-in-practice-case-studies-and-hybrid-systems.md) ·

---

**Navigation:** [← Previous: L14-01 AI in Practice: Case Studies, Hybrid and Neuro-Symbolic Systems](L14-01-ai-in-practice-case-studies-and-hybrid-systems.md) · [Module home](../README.md) · [Next: L14-03 Monitoring, Drift and Continuous Evaluation →](L14-03-monitoring-drift-and-continuous-evaluation.md)
