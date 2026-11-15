# Capstone Studio

The capstone is most of M14: about 14 of its 32.9 hours. This directory holds everything except
your own work.

| File | What it is |
| :--- | :--- |
| [`briefs/`](briefs/) | twelve project briefs, four per level, each with all thirteen required sections |
| [`rubric.md`](rubric.md) | the marking scheme, with band descriptors |
| [`milestones.md`](milestones.md) | four gates with the evidence each requires |
| [`report-template.md`](report-template.md) | the report skeleton, ready to fill |
| [`report-writing.md`](report-writing.md) | structure, numbers, figures and the limitations section |
| [`../assignments/asg-14-capstone-proposal.md`](../assignments/asg-14-capstone-proposal.md) | the proposal you submit before starting |

## The twelve briefs

### Beginner

| ID | Project | Primary skill |
| :--- | :--- | :--- |
| [B-01](briefs/b-01-student-performance-prediction.md) | Student performance prediction | tabular pipeline, leakage discipline |
| [B-02](briefs/b-02-intelligent-faq-chatbot.md) | Intelligent FAQ chatbot | retrieval, grounding, refusal |
| [B-03](briefs/b-03-image-classification-application.md) | Image classification application | transfer learning, per-class evaluation |
| [B-04](briefs/b-04-news-classification-system.md) | News classification system | text preprocessing, macro metrics |

### Intermediate

| ID | Project | Primary skill |
| :--- | :--- | :--- |
| [I-05](briefs/i-05-rag-university-document-assistant.md) | RAG university document assistant | retrieval evaluation, citation |
| [I-06](briefs/i-06-plant-disease-detection.md) | Plant disease detection | field shift, error analysis |
| [I-07](briefs/i-07-traffic-sign-recognition.md) | Traffic sign recognition | robustness, small classes |
| [I-08](briefs/i-08-recommendation-system.md) | Recommendation system | ranking metrics, offline/online gap |

### Advanced

| ID | Project | Primary skill |
| :--- | :--- | :--- |
| [A-09](briefs/a-09-multimodal-document-understanding.md) | Multimodal document understanding | two-tower models, layout + text |
| [A-10](briefs/a-10-multi-agent-research-assistant.md) | Multi-agent research assistant | orchestration, evaluation of agents |
| [A-11](briefs/a-11-medical-image-segmentation-prototype.md) | Medical image segmentation prototype | segmentation metrics, safe claims |
| [A-12](briefs/a-12-secure-ai-agent-with-runtime-monitoring.md) | Secure AI agent with runtime monitoring | guardrails, drift and abuse monitoring |

Each brief names its prerequisite modules, so you can choose early.

## How the capstone runs

```text
proposal (ASG-14) -> M1 approved -> M2 data + baseline -> M3 model + evaluation
                                 -> M4 report + demo -> defence
```

Four milestones, each producing an artefact. The rubric is applied at M4, but read it at M1 —
the marks are decided by choices made at the start, not at the end.

## Ground rules

1. **Data.** Synthetic, public-domain, or openly licensed data. State the licence in the report.
   If you use a dataset with personal data, say what the licence permits and do not redistribute.
2. **Scope.** One primary metric, one dataset (two if comparing), one baseline. Extensions are
   optional and unmarked.
3. **Honesty.** Every number in your report must come from a command in your repository. If you
   did not measure it, write "not measured".
4. **High-stakes claims.** A prototype is not a product. Do not claim clinical, financial, legal or
   safety reliability without the validation that claim requires. State the limitation
   explicitly, in the abstract, not only in the footnotes.
5. **No deployment.** Nothing in this capstone requires serving to real users, and doing so is out
   of scope for the assessment.

## Time budget

| Stage | Hours |
| :--- | ---: |
| Proposal and literature (ASG-14) | 2 |
| M2 data pipeline and baseline | 4 |
| M3 model, evaluation, error analysis | 5 |
| M4 report, demo, defence | 3 |
| Total capstone | 14 |

If you are behind at M2, cut scope — not evaluation. A smaller project with a real baseline and a
per-class table scores higher than a large one with a demo.

## What "done" looks like

- A repository that reproduces every number with one command.
- A report with a primary metric, a baseline, a per-class or subgroup table, uncertainty, and a
  limitations section that states what the result does not support.
- A five-slide defence that names a failure before the audience does.
- A model card, even a one-page one.

---

[Module home](../README.md) · [Rubric](rubric.md) · [Milestones](milestones.md) ·
[Report template](report-template.md)
