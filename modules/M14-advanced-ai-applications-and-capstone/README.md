# M14 — Advanced AI Applications and Capstone Projects

| Level | 400 |
| :--- | :--- |
| Study time | 32.9 hours — guided 7.5 · practical 5.5 · assessment 5.9 · project 14.0 |
| Lessons | 5 |
| Course outcome | CLO8 — integrate the course in one scoped, evaluated, honestly reported system |
| Prerequisites | M13, plus the modules named by your chosen capstone brief |

[Course home](../../README.md) · [All modules](../README.md) · [Previous module: M13](../README.md#m13)

## Overview

This module is where the course turns outward. The first half is the part of applied AI that no
single earlier module covered: systems that mix learned and symbolic parts, models that must be
compressed before they can be served, perception pipelines with more than one modality, graphs,
federated training, and the monitoring that keeps any of it working after release.

The second half is your capstone: one brief from twelve, four milestones, a rubric applied to
evidence rather than effort.

Everything here is measured on data you can obtain and code you can run on a laptop. Four results
are deliberately counter-intuitive, because they are the ones people get wrong:

- a **rules-only** baseline beat the neural model (0.972 vs 0.877) and the **hybrid** was the only
  deployable design, at the cost of 100 additional refusals;
- a distilled student **gained nothing** over training without a teacher (−0.004);
- 8-bit quantisation made inference **1.6–2.4× slower** in five release-validation runs while shrinking the model to 27.7% of its size;
- a graph network **lost** 0.131 accuracy to a feature-only model when homophily was low, in
  both a random-mix and a stochastic-block-model graph, while retaining its advantage under an
  inductive split.

## Advanced topics and where each is taught

| Topic | Lesson | Measured demo |
| :--- | :--- | :--- |
| Hybrid AI systems | L14-01 | rules vs model vs hybrid gate |
| Neuro-symbolic AI | L14-01 | policy + network, 100 → 0 violations |
| Explainable deep learning | L14-01 | integrated gradients vs binding rule |
| Multimodal AI | L14-04 | two-tower contrastive model |
| Vision-language models | L14-04 | zero-shot 0.152 → 0.904 |
| Speech recognition | L14-04 | mechanism + WER/CER evaluation (no demo; see scope note) |
| Text-to-speech | L14-04 | mechanism + MOS/RTF evaluation (no demo) |
| Multimodal LLMs | L14-04, L14-05 | retrieval and grounding evaluation |
| Time-series intelligence | L14-03 | backtest, intervals, coverage 0.66 vs 0.80 |
| Graph neural networks | L14-04 | GCN vs MLP, two families, transductive + inductive, homophily/noise sweeps |
| Federated learning | L14-04 | FedAvg 0.898 vs central 0.917 |
| Edge AI | L14-02 | memory/latency/power constraints |
| Model compression | L14-02 | distillation, pruning |
| Quantisation | L14-02 | int8, size 27.7%, latency 1.6–2.4× slower |
| Knowledge distillation | L14-02 | temperature sweep |
| Model optimisation | L14-02 | operator fusion, batching, caching |
| AI inference optimisation | L14-02 | throughput vs latency measurement |
| MLOps introduction | L14-02 | registry, canary, rollback |
| Model monitoring | L14-03 | PSI 3.777 alert |
| AI system deployment | L14-02, L14-03 | latency budget, serving patterns |
| Emerging AI research directions | L14-04 | eight directions with open problems |

**Scope note on speech.** The module covers ASR/TTS mechanism and evaluation, but ships no audio
demo: the course environment has no audio stack, and a toy vocoder would teach less than a careful
reading of one evaluation section. Stated rather than hidden.

## Practical projects and where they are built

| # | Project | Where |
| :--- | :--- | :--- |
| 1 | Student performance prediction | [B-01](capstone/briefs/b-01-student-performance-prediction.md) |
| 2 | Intelligent FAQ chatbot | [B-02](capstone/briefs/b-02-intelligent-faq-chatbot.md) |
| 3 | Image classification application | [B-03](capstone/briefs/b-03-image-classification-application.md) |
| 4 | News classification system | [B-04](capstone/briefs/b-04-news-classification-system.md) |
| 5 | RAG university document assistant | [I-05](capstone/briefs/i-05-rag-university-document-assistant.md) |
| 6 | Plant disease detection | [I-06](capstone/briefs/i-06-plant-disease-detection.md) |
| 7 | Traffic sign recognition | [I-07](capstone/briefs/i-07-traffic-sign-recognition.md) |
| 8 | Recommendation system | [I-08](capstone/briefs/i-08-recommendation-system.md) |
| 9 | Multimodal document understanding | [A-09](capstone/briefs/a-09-multimodal-document-understanding.md) |
| 10 | Multi-agent research assistant | [A-10](capstone/briefs/a-10-multi-agent-research-assistant.md) |
| 11 | Medical image segmentation prototype | [A-11](capstone/briefs/a-11-medical-image-segmentation-prototype.md) |
| 12 | Secure AI agent with runtime monitoring | [A-12](capstone/briefs/a-12-secure-ai-agent-with-runtime-monitoring.md) |

Every brief carries the same thirteen sections: problem, motivation, objectives, scope, required
knowledge, architecture, datasets, technologies, milestones, metrics, deliverables, challenges and
extensions.

## Data, models and licences

| Asset | Licence | Note |
| :--- | :--- | :--- |
| scikit-learn `load_digits` | **CC BY 4.0** (UCI dataset); BSD-3-Clause loader | 1,797 8×8 images, loaded at runtime; not redistributed |
| Synthetic eligibility data | **CC0-1.0** | generated in `neurosymbolic.py` |
| Synthetic graphs | **CC0-1.0** | generated in `graphs.py` |
| Synthetic daily series | **CC0-1.0** | generated in `timeseries_monitor.py` |
| Templated captions | **CC0-1.0** | generated in `multimodal.py` |

No weights are downloaded. Capstone datasets are named in each brief with their licence and a
warning to verify it; the module never redistributes a third-party dataset.

## Before you start

```bash
pip install numpy scikit-learn torch
```

`networkx` is optional. No GPU, no API key, no network access is needed for the module's own code.

**Readiness self-check.** If you cannot do three of these, review the module named:

1. Run a leakage-free pipeline and defend its metric (M06).
2. Explain what a convolution layer learns and compute its parameter count (M07).
3. Build a retrieval index and measure recall@k (M11).
4. Compute a group metric and write a fairness statement (M13).
5. State the difference between a research prototype and a deployed system (M13).

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L14-01 | AI in Practice: Case Studies, Hybrid and Neuro-Symbolic Systems | Lesson | 90 m | [Read](lessons/L14-01-ai-in-practice-case-studies-and-hybrid-systems.md) |
| L14-02 | From Model to Product: Serving, Compression and MLOps | Lesson | 90 m | [Read](lessons/L14-02-from-model-to-product-mlops-and-serving.md) |
| L14-03 | Monitoring, Drift and Continuous Evaluation | Lesson | 90 m | [Read](lessons/L14-03-monitoring-drift-and-continuous-evaluation.md) |
| L14-04 | Reading and Reproducing AI Research | Lesson | 90 m | [Read](lessons/L14-04-reading-and-reproducing-ai-research.md) |
| L14-05 | Capstone Studio: Scoping, Milestones and Defence | Lesson | 90 m | [Read](lessons/L14-05-capstone-studio.md) |
| NB-14-01 | Capstone Starter Kit | Notebook | 60 m | [Open](notebooks/nb-14-01-capstone-starter-kit.ipynb) |
| LAB-14-01 | Multimodal and Graph Systems | Lab | 2.5 h | [Start](labs/lab-14-01-multimodal-and-graph-systems.md) |
| LAB-14-02 | Efficient Serving: Compression, Latency and Drift | Lab | 2.5 h | [Start](labs/lab-14-02-efficient-serving.md) |
| ASG-14 | Capstone Proposal | Assignment | 2 h | [Start](assignments/asg-14-capstone-proposal.md) |
| QUIZ-14 | Module self-check | Quiz | 30 m | [Take](quizzes/quiz-14.md) |
| CAP-14 | Capstone project (brief + milestones + rubric + report) | Project | 14 h | [Studio](capstone/README.md) |

Total: 7.5 h guided study + 5.5 h practical + 5.9 h assessment + 14 h capstone =
**32.9 hours**. The per-artifact estimates above are rounded planning values and sum to 30;
the module total uses the category figures that every other module page and the curriculum map
report.

Supporting code lives in [`code/`](code/):

| File | Contents |
| :--- | :--- |
| `neurosymbolic.py` | policy, MLP, integrated gradients, rules/model/hybrid comparison |
| `multimodal.py` | two-tower contrastive model, retrieval metrics, zero-shot evaluation |
| `efficiency.py` | teacher/student distillation, int8 quantisation, pruning, latency harness |
| `graphs.py` | random-mix and SBM graphs, GCN, MLP, transductive + inductive protocols, homophily/depth/noise sweeps, accuracy/macro-F1/confusion matrix |
| `federated.py` | non-IID client split, FedAvg, DP noise, per-client accuracy |
| `timeseries_monitor.py` | rolling-origin backtest, interval coverage, PSI drift monitor |
| `build_notebooks.py` | regenerates and executes NB-14-01 |

```bash
python neurosymbolic.py && python multimodal.py && python efficiency.py
python graphs.py && python federated.py && python timeseries_monitor.py
```

## Capstone studio

| File | Purpose |
| :--- | :--- |
| [`capstone/briefs/`](capstone/briefs/) | twelve briefs, four per level |
| [`capstone/rubric.md`](capstone/rubric.md) | ten criteria, 100 points, band descriptors |
| [`capstone/milestones.md`](capstone/milestones.md) | four gates with checklists |
| [`capstone/report-template.md`](capstone/report-template.md) | the report skeleton |
| [`capstone/report-writing.md`](capstone/report-writing.md) | numbers, figures, limitations |

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L14-01 | 1.5 h |
| 2 | L14-02, NB-14-01 | 2.5 h |
| 3 | LAB-14-02 | 2.5 h |
| 4 | L14-03 | 1.5 h |
| 5 | L14-04, LAB-14-01 | 4 h |
| 6 | L14-05, ASG-14 | 3.5 h |
| 7–12 | Capstone: M2 (4 h), M3 (5 h), M4 (3 h) | 14 h |
| 13 | QUIZ-14, defence preparation | 0.5 h |

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-14-01 | Metric reasoning, assumption testing, reproduction | 10% |
| LAB-14-02 | Compression table, latency budget, monitoring plan | 10% |
| QUIZ-14 | Conceptual grasp of the measured results | 5% |
| ASG-14 | Scope, feasibility, evaluation plan, failure condition | 15% |
| CAP-14 (rubric) | The ten criteria in [`capstone/rubric.md`](capstone/rubric.md) | 60% |

The assessment dimensions are described in the
[curriculum map](../../docs/CURRICULUM-MAP.md#8-assessment-model).

## Compute requirements

| Stage | CPU only | GPU (optional) |
| :--- | :--- | :--- |
| `neurosymbolic.py` | ~15 s | — |
| `multimodal.py` | ~20 s | small gain |
| `efficiency.py` | ~60 s | seconds |
| `graphs.py` | ~40 s | small gain |
| `federated.py` | ~90 s | 10× faster |
| `timeseries_monitor.py` | ~25 s | — |

Everything runs on a 4-core laptop. The capstone's compute needs depend on the brief; every brief
names a CPU-feasible path.

## Key terms introduced

**Hybrid system**, **neuro-symbolic AI**, **rule gate**, **adverse action reason**, **integrated
gradients**, **contrastive learning**, **InfoNCE**, **zero-shot classification**, **two-tower
model**, **quantisation**, **distillation**, **soft labels**, **pruning**, **sparsity**,
**latency budget**, **canary deployment**, **model registry**, **message passing**,
**homophily**, **oversmoothing**, **FedAvg**, **non-IID**, **PSI**, **coverage**,
**rolling-origin backtest**, **concept drift**, **research prototype**, **reproduction
package**.

All are defined in the [glossary](../../resources/glossary.md). The one-page recap is in
[summary.md](summary.md).

## Resources

- Hinton, Vinyals & Dean (2015). *Distilling the Knowledge in a Neural Network*.
- Radford et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision*.
- Kipf & Welling (2017). *Semi-Supervised Classification with Graph Convolutional Networks*.
- McMahan et al. (2017). *Communication-Efficient Learning of Deep Networks from Decentralized Data*.
- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*.
- Sculley et al. (2015). *Hidden Technical Debt in Machine Learning Systems*.
- The module's [summary](summary.md) — every verified number in one table.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) · [Previous: M13](../README.md#m13)
