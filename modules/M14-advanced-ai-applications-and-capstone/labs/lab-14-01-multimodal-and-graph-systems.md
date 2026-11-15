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
python graphs.py         # ~2 min
```

Both use scikit-learn's bundled digits data (UCI dataset, CC BY 4.0; not redistributed) and
synthetic graphs. No downloads,
no GPU. Every number below comes from the committed scripts, run on five seeds and reported as
mean ± standard deviation; the commands take about a minute in total.

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

## 3. Part B — Graph neural networks (60 minutes)

The reference script now runs **two graph families** under **two evaluation protocols**. Your job
is not to confirm that a GCN wins; it is to say where, by how much, and under what assumptions.

### B0. Protocols and controls

| Term | Meaning here |
| --- | --- |
| **Transductive** | One graph. 20% of nodes are labelled for training, the rest are test nodes. Test-node features and edges are visible to message passing. This is the easier setting. |
| **Inductive** | Disjoint 60/20/20 train/validation/test nodes. The test subgraph is hidden during training; validation chooses the epoch; test metrics are computed once. At inference, test features and test-to-training edges are available, as in a deployed graph service. |
| **Matched control** | The transductive model uses exactly the same train/test nodes as the inductive run, so only protocol and test-test visibility differ. |

Three controls make the comparison meaningful:

- **10% of training labels are flipped**; test and validation labels are clean.
- **Five seeds** per condition, reported as mean ± standard deviation.
- The **test set is never used for model selection**. Training uses fixed epochs in the
transductive runs and validation early stopping in the inductive runs.

Families:

- **random-mix** — each of a node's four edge slots is same-class with probability `homophily`,
  otherwise uniform over all nodes.
- **SBM** — stochastic block model with within-class probability `p_in` and cross-class `p_out`.
  Lower `p_out` means higher homophily. Edges are independent given the class blocks.

### B1. Read the graph before the model

Run `python graphs.py` in `code/`. It prints for each family: nodes, edges, mean degree, measured
edge homophily. The defaults are 200 nodes, 5 classes, 12 weak features, label noise 10%, five
seeds.

- Why is homophily a property of the data rather than of the model?
- The features are deliberately weak (MLP 0.399 transductive, 0.370 inductive). Why does that
  matter for this experiment?
- The MLP scores the same on both families. Why is that expected, and what does it tell you
  about what the families change?

### B2. Transductive and inductive results

Measured, five seeds, mean ± standard deviation (accuracy; macro-F1 in the script output):

```text
  random-mix, transductive        random-mix, inductive
    majority  0.200                 majority  0.200
    MLP       0.399 ± 0.042         MLP       0.370 ± 0.091
    GCN       0.866 ± 0.020         GCN       0.945 ± 0.029
    gap       +0.467                gap       +0.575

  SBM, transductive               SBM, inductive
    majority  0.200                 majority  0.200
    MLP       0.399 ± 0.042         MLP       0.370 ± 0.091
    GCN       0.794 ± 0.029         GCN       0.835 ± 0.020
    gap       +0.395                gap       +0.465
```

- Does the GCN advantage survive the inductive protocol? By how much in each family?
- The inductive MLP is higher than the transductive MLP. Is that a protocol effect, a
  label-budget effect, or both? Use the matched control (2b in the output) to answer: at the same
  60% label budget the control gives MLP 0.405 ± 0.048 and GCN 0.855 ± 0.062 (random-mix),
  0.830 ± 0.068 (SBM).
- What can you *not* conclude from comparing two protocols with different test sets?

Depth still matters. Transductive, five seeds:

```text
  random-mix  GCN-2 0.866 ± 0.020   GCN-4 0.821 ± 0.028   GCN-8 0.273 ± 0.186
  SBM         GCN-2 0.794 ± 0.029   GCN-4 0.825 ± 0.029   GCN-8 0.319 ± 0.157
```

The 8-layer model collapses toward chance (0.2), and its across-seed spread is large. Explain
oversmoothing in one sentence, then explain why "deeper is better" is false here specifically.

### B3. Homophily

Transductive sweep, measured edge homophily, five seeds:

```text
  random-mix                     SBM
   h      MLP   GCN   gain        h      MLP   GCN   gain
  0.187  0.399 0.268 -0.131      0.127  0.399 0.279 -0.120
  0.385  0.399 0.424 +0.025      0.325  0.399 0.407 +0.009
  0.586  0.399 0.691 +0.293      0.590  0.399 0.672 +0.274
  0.773  0.399 0.866 +0.467      0.747  0.399 0.794 +0.395
  1.000  0.399 0.906 +0.508      1.000  0.399 0.844 +0.445
```

- Where is the crossover in each family? Report the measured homophily, not the requested value.
- What happens when the graph is heterophilous, and why is the graph worse than ignoring it?
- At perfect homophily the GCN reaches 0.906/0.844, not 1.000. What does the 10% label noise
  explain, and what would a sceptical reviewer still ask about the task?
- For a fraud-detection graph where fraudsters connect to each other, is homophily high or low?
  What does that imply for a GCN on that graph?

### B4. Label noise

Transductive, five seeds:

```text
  noise   random-mix MLP/GCN     SBM MLP/GCN
  0.00    0.430 / 0.984          0.430 / 0.905
  0.10    0.399 / 0.866          0.399 / 0.794
  0.20    0.350 / 0.760          0.350 / 0.729
```

- How sensitive is the GCN advantage to label noise? Does the gap shrink monotonically?
- Why does a noiseless run approach saturation while the noisy runs do not?
- Which would you report to a reviewer, and why?

### B5. Cost and failure analysis

- Compute the number of edges from the printout and estimate aggregation cost per layer. At what
  graph size would a dense adjacency matrix (N² floats) exceed 1 GB? Show the arithmetic.
- Run the per-class table for at least one family. Which class is worst, and is the error pattern
  consistent with class confusion or with label noise?

### B6. What the results answer

1. **Does the GCN beat the MLP under both families?** Yes, at the default setting, under both
   protocols: +0.467 random-mix and +0.395 SBM transductive; +0.575 and +0.465 inductive.
2. **How does homophily affect the GCN?** Monotonically in these sweeps: gain rises from about
   −0.13 at 0.13–0.19 homophily to +0.51/+0.45 at perfect homophily.
3. **What happens when the graph is heterophilous?** The GCN is worse than the feature-only
   model; message passing averages across classes.
4. **Does the advantage remain under inductive evaluation?** Yes in this experiment, and it is
   not smaller. Absolute accuracies are not directly comparable across protocols because the
   splits differ; the matched control isolates test-test visibility.
5. **How sensitive is it to label noise?** Both models degrade; the GCN's advantage shrinks from
   +0.554 to +0.410 (random-mix) and from +0.475 to +0.379 (SBM) as noise rises from 0% to 20%.
6. **When does graph structure provide little benefit?** At low homophily, at very high label
   noise, and when features already separate the classes — the last is why the starter no longer
   gives one feature a large class offset.

## 4. Part C — Compare and decide (30 minutes)

Fill in:

| System | Data | Metric | Best result | Assumption it depends on |
| :--- | :--- | :--- | ---: | :--- |
| Two-tower retrieval | digits + captions | digit-level retrieval | | captions name the class |
| GCN | synthetic graph | node accuracy | 0.866 transductive; 0.945 inductive | homophily above ~0.4 |

Then answer: for each system, name one dataset property that would invalidate your result.

## 5. Reflection questions

1. The multimodal model reached 0.904 zero-shot while its instance retrieval sat at chance. Which
   number would you put in an abstract, and what would you be obliged to explain?
2. What did the two-family, two-protocol comparison change about how you would choose a graph
   architecture in future?
3. Both experiments used synthetic or bundled data. State precisely what each result does not
   license, including the SBM's independent-edge assumption.
4. A reviewer asks whether your inductive result used test labels during model selection. What
   evidence would you show them?
5. If your capstone uses a graph or multimodal component, which assumption from this lab would
   you test first?
6. The graph loses at low homophily. Write the sentence you would put in a paper reporting that
   negative result, without hiding it.

## 6. Marking criteria

| Criterion | Weight | Strong |
| :--- | ---: | :--- |
| Measurement | 30% | all numbers reproduced with seeds, both families and protocols |
| Metric reasoning | 25% | chance levels computed, macro-F1 and confusion matrix read correctly |
| Assumption testing | 25% | homophily, label noise and protocol tested, not asserted |
| Reflection | 20% | states what the results do not establish, including the negative regime |

---

[Module home](../README.md) · [Lab 14-02](lab-14-02-efficient-serving.md) ·
[Summary](../summary.md)

## Starter material

A runnable starter is provided: [`starters/lab-14-01_starter.py`](starters/lab-14-01_starter.py).
It builds a weak-feature graph, trains on 20% of nodes with 10% flipped labels, and prints the
graph model against a feature-only baseline over five seeds. It is transductive and supports two
families:

```bash
python lab-14-01_starter.py              # random-mix (default)
python lab-14-01_starter.py --family sbm # stochastic block model
```

```text
 edge homophily  graph mean  graph sd  baseline    gain
          0.500       0.562     0.041     0.590  -0.027
          0.628       0.671     0.054     0.590  +0.081
          0.750       0.804     0.053     0.590  +0.214
          0.874       0.886     0.047     0.590  +0.296
          1.000       0.952     0.015     0.590  +0.362

SBM (p_out 0.20, 0.06, 0.02, 0.01, 0.0):
 edge homophily  graph mean  graph sd  baseline    gain
          0.370       0.641     0.110     0.590  +0.051
          0.658       0.729     0.057     0.590  +0.139
          0.855       0.927     0.015     0.590  +0.338
          0.924       0.974     0.019     0.590  +0.384
          1.000       0.993     0.009     0.590  +0.403
```

Read the table before writing code: at random mixing the graph adds nothing, and below it the
graph is worse than ignoring edges entirely. The parts left for you are marked `TODO`. Run it
before you write anything.

Module reference code: [`../code/`](../code/).

## Extension challenges (optional)

Optional work for students who want the research-flavoured version of this lab.

1. **Modality ablation.** Fuse two real encoders (for example M09 image features and M08
   text embeddings) and report accuracy with image only, text only, and both. State whether
   fusion beats the better single modality, and by how much relative to seed spread.
2. **Graph or no graph.** Compare message passing against a feature-only model on a dataset
   where the graph is genuinely informative. If the graph does not help, prove it rather
   than asserting it.
3. **Heterogeneous edges.** Add a second edge type and a relation-specific weight matrix.
   Report the parameter cost and whether the extra relation earns it.
