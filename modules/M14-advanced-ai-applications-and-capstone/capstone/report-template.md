# Capstone Report Template

Copy this file, rename it `report.md`, and fill it in. Target length: six pages excluding
references. Delete the guidance in square brackets as you go.

---

# [Project title]

**Author** [name] · **Module** M14 · **Date** [date]
**Repository** [path or link] · **Reproduction command** `python reproduce.py`

## Abstract (150 words)

[The problem, the data, the method, the primary result **with its number**, and the single most
important limitation. Write this last and rewrite it after the results change.]

## 1. Problem and motivation

### 1.1 The decision

[What decision does this support? Who makes it now, and with what information? What happens
without the system?]

### 1.2 Why a learned approach

[Why not a rule, a lookup table, or a human process? If a rule would do, say so and justify the
model anyway — or change project.]

### 1.3 Scope

**In scope:** [bullet list]
**Out of scope:** [bullet list — deployment, users, claims you will not make]

## 2. Related work

[Three to five sources. For each: what it did, what you borrowed, and where it disagrees with
another source. A list of summaries with no connection to your method scores in the 3–5 band.]

## 3. Data

| | |
| :--- | :--- |
| Source | [name, URL] |
| Licence | [exact licence] |
| Size | [rows / images / documents] |
| Target | [definition, and who produced it] |
| Split | [how, and why it matches deployment] |

[Known gaps: missing groups, label noise, collection conditions. Two or three sentences, honest.]

## 4. Method

### 4.1 Baseline

[The trivial method and its number. This number appears in every results table.]

### 4.2 Approach

[Architecture or algorithm, in one diagram and two paragraphs. Justify the step up from the
baseline — capacity, representation, or a specific failure of the baseline.]

### 4.3 Training and reproducibility

[Seeds, epochs, hyperparameters, environment. If a reader cannot rerun it from this section and
the repository, it is incomplete.]

## 5. Results

### 5.1 Primary metric

| Model | [Primary metric] | [Supporting 1] | [Supporting 2] | n |
| :--- | ---: | ---: | ---: | ---: |
| Baseline (trivial) | | | | |
| Baseline (standard) | | | | |
| Yours | | | | |

[Uncertainty: intervals, seed spread, or an explicit statement that the sample cannot distinguish
these models.]

### 5.2 Per-class or subgroup results

| Slice | n | [Metric] | Gap vs overall |
| :--- | ---: | ---: | ---: |
| | | | |

[Where is the model worst, and who does that affect?]

### 5.3 Ablation

| Variant | [Metric] | Change |
| :--- | ---: | ---: |
| Full model | | |
| − component | | |

[One ablation that isolates the thing you claim matters.]

## 6. Error analysis

[Three concrete failures: what the input was, what the model said, what was correct, and why.
Not "the model struggles with rare classes" — show three examples and explain the pattern.]

## 7. Explainability and limitations

### 7.1 Explanation

[One global and one local explanation (see M13's L13-02), with a fidelity or stability number.
If you used an interpretable model, say so — that is a legitimate answer.]

### 7.2 Limitations

[Each limitation must be traceable to a measurement or a data property. "The dataset may be
biased" is not a limitation; "only 42 images of class X, and accuracy on X is 0.51" is.]

### 7.3 What this does not support

[The prototype boundary. State that the system is not validated for clinical, financial, legal or
safety-critical use if it touches those domains, and what validation would require.]

## 8. Ethics and data protection

[Personal data yes/no, licence compliance, affected parties, and any mitigation. Two paragraphs
maximum; specificity beats length.]

## 9. Conclusion and next steps

[What is now known, what would you do with another month, and what would you measure first.]

## References

[Consistent style. Cite the dataset and the papers your method rests on.]

## Appendix A — Reproduction

```bash
pip install -r requirements.txt
python reproduce.py     # regenerates every table in this report
```

[Seeds, hardware, runtime. A reader should be able to check one number in under ten minutes.]

## Appendix B — Model card

[Use M13's `code/governance.py` template. Even a one-page card is worth marks: intended use,
out-of-scope, data, metrics, subgroup results, limitations, monitoring.]

---

[Capstone home](README.md) · [Rubric](rubric.md) · [Writing guide](report-writing.md)
