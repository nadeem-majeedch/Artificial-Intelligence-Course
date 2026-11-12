# A-09 — Multimodal Document Understanding

**Level** Advanced · **Time** 14 h capstone · **Prerequisites** M11, M14 (L14-04), M09

## Problem statement

Extract structured fields from scanned documents using both text and layout, and measure how much
the visual channel contributes over text alone.

## Motivation

Invoices, forms and receipts carry meaning in position as well as wording: a total is a total
because of where it sits. A text-only model loses that. The interesting result is the ablation:
how much does layout add, and on which fields?

## Scope

**In:** field extraction from synthetic or licensed documents, offline evaluation.
**Out:** real customer documents, deployment, any financial or legal claim.

## Objectives

1. Build a text-only baseline and a multimodal model (text + layout features).
2. Evaluate per field with exact-match and normalised scores.
3. Ablate layout to quantify its contribution.
4. Analyse failures by document quality and field type.

## Required knowledge

M11 tokenisation, M09 feature extraction, L14-04 two-tower and ablation discipline.

## Suggested architecture

```text
document image -> OCR (or synthetic text boxes) -> tokens + bounding boxes
               -> text encoder + layout features (x, y, w, h, font size)
               -> field classification / sequence labelling
               -> evaluate per field; ablate layout
```

## Dataset recommendations

- Synthetic documents you render (fully licensed, controllable layout), 300–1,000 pages.
- Licensed alternatives: a public form dataset with a permissive licence — verify before use.
- Do not use real invoices or personal documents.

## Suggested technologies

Python, PIL, scikit-learn; a small transformer only if available locally. Rendering synthetic
documents with PIL or reportlab is sufficient and keeps licensing clean.

## Implementation milestones

| Milestone | Artefact |
| :--- | :--- |
| M2 | synthetic corpus, text-only baseline per field |
| M3 | multimodal model, ablation table |
| M4 | failure analysis by field, report |

## Evaluation metrics

Primary: macro exact-match across fields on held-out documents. Supporting: per-field F1,
layout-contribution delta, performance by document quality bucket. Baseline: text-only.

## Expected deliverables

Generator, model, ablation table, model card, report.

## Challenges

1. **OCR dependency.** If you use OCR, its errors mix with model errors. Mitigation: synthetic
   text boxes first, then a noisy-OCR variant as a second experiment.
2. **Field imbalance.** Some fields are rare. Report per-field n.
3. **Layout leakage.** Document templates can reveal the label. Vary templates when generating.

## Possible extensions

- Add a two-tower retrieval component over document templates.
- Compare layout-as-features against layout-as-image (a small CNN over the page).

---

[Capstone home](../README.md) · [Rubric](../rubric.md) · [All briefs](../README.md#the-twelve-briefs)
