# LAB-14-01 — Multimodal and Graph Systems

| | |
| :--- | :--- |
| Time | 2.5 hours |
| Level | 400 |
| Prerequisites | L14-04, M07 |
| Code | `code/multimodal.py`, `code/graphs.py` |

[Module home](../README.md) · [Lab 14-02](lab-14-02-efficient-serving.md) · [Rubric](../capstone/rubric.md)

## Purpose

Build a two-tower vision-language model and a graph network from scratch, then find the
conditions under which each one works. Both labs are built so that a plausible assumption fails,
and finding it is the deliverable.

**Deliverable.** A short report (≤900 words) with four tables and the answers to the prompts.

---

## 1. Setup

```bash
cd modules/M14-advanced-ai-applications-and-capstone/code
python multimodal.py     # ~15 s
python graphs.py         # ~30 s
```

Both use scikit-learn's bundled digits data (public domain) and synthetic graphs. No downloads,
no GPU.

## 2. Part A — Contrastive retrieval (50 minutes)

### A1. The baseline is chance

Before training, the script prints retrieval metrics and zero-shot accuracy. Record them.

Chance for image-to-text R@1 is not 0.5 and not 0.1 — compute it: with roughly 36 captions per
digit in the test set, what is the probability that a randomly chosen caption is the exact paired
one?

### A2. Training

Record the loss and retrieval metrics at steps 1, 50, 100, 200, 300. Answer:

- Does the loss keep falling? Does R@1 follow it?
- Zero-shot accuracy goes 0.152 → 0.904. Why can a classifier work when retrieval does not?

### A3. The metric trap

Instance-level R@1 is 0.024, at chance. Digit-level retrieval is 0.961.

- Explain in two sentences why the first number is uninformative for this dataset.
- If you reported only the first number, what would you conclude, and would you be wrong?

### A4. Change the data, change the result

Modify `build_captions` so that each caption is unique: append the image index
(`"sample 0421: a clear sheet of the number three"`). Rerun.

- Does instance-level R@1 rise? To what?
- Does zero-shot accuracy change? Why?

This separates "the model cannot align modalities" from "the captions are ambiguous".

### A5. Failure analysis

The per-class table shows the worst class at 0.87. Inspect a few failures: are they visually
ambiguous digits (4/9, 3/8) or caption-noise cases? Write one paragraph.

## 3. Part B — Graph neural networks (50 minutes)

### B1. Read the graph before the model

The script prints measured edge homophily (0.825). Answer:

- Why is homophily a property of the data rather than of the model?
- The features are deliberately weak (MLP 0.600). Why does that matter for this experiment?

### B2. Depth

Record MLP, GCN-2, GCN-4, GCN-8. The 8-layer model collapses to 0.250.

- Explain oversmoothing in one sentence.
- Why does this make "deeper is better" false for GNNs specifically?

### B3. Break the assumption

The homophily sweep gives:

```text
   homophily     MLP   GCN-2    gain
         0.1   0.550   0.340  -0.210
         0.3   0.550   0.500  -0.050
         0.5   0.550   0.880  +0.330
         0.7   0.550   1.000  +0.450
         0.9   0.550   1.000  +0.450
```

- At what homophily does the graph stop helping? Report the crossover.
- For a fraud-detection graph where fraudsters connect to each other, is homophily high or low?
  What does that imply for a GNN on that graph?

### B4. Cost

Compute the number of edges and estimate the aggregation cost per layer. At what graph size would
a dense adjacency matrix (N² floats) exceed 1 GB? Show the arithmetic.

## 4. Part C — Compare and decide (30 minutes)

Fill in:

| System | Data | Metric | Best result | Assumption it depends on |
| :--- | :--- | :--- | ---: | :--- |
| Two-tower retrieval | digits + captions | digit-level retrieval | | captions name the class |
| GCN | synthetic graph | node accuracy | | homophily ≥ 0.5 |

Then answer: for each system, name one dataset property that would invalidate your result.

## 5. Reflection questions

1. The multimodal model reached 0.904 zero-shot while its instance retrieval sat at chance. Which
   number would you put in an abstract, and what would you be obliged to explain?
2. What did the homophily sweep change about how you would choose an architecture in future?
3. Both experiments used synthetic or bundled data. State precisely what each result does not
   license.
4. If your capstone uses a graph or multimodal component, which assumption from this lab would
   you test first?

## 6. Marking criteria

| Criterion | Weight | Strong |
| :--- | ---: | :--- |
| Measurement | 30% | all numbers reproduced with seeds |
| Metric reasoning | 25% | chance levels computed and ambiguity explained |
| Assumption testing | 25% | homophily/ambiguity tested, not asserted |
| Reflection | 20% | states what the results do not establish |

---

[Module home](../README.md) · [Lab 14-02](lab-14-02-efficient-serving.md) ·
[Summary](../summary.md)
