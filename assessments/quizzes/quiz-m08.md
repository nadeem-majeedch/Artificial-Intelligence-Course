# QUIZ-M08 — Natural Language Processing

| | |
| :--- | :--- |
| Module | M08 · Natural Language Processing |
| Questions | 10 (20 marks) |
| Time | 35 minutes |
| Covers | L08-01 … L08-06 |
| Pass mark | 12 / 20 |

> **Availability.** This module's lessons, notebooks and labs are published in this repository; sit this paper after finishing them.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m08.md)

---

## Part A — Multiple choice (4 marks)

**Q8.1** Subword tokenisation (BPE, WordPiece) mainly addresses

- A. grammar errors
- B. out-of-vocabulary words and vocabulary size
- C. class imbalance
- D. sequence labelling

**Q8.2** The IDF term in TF-IDF

- A. increases the weight of words that appear in many documents
- B. decreases the weight of words that appear in many documents
- C. removes stop words
- D. normalises document length only

**Q8.3** A contextual embedding differs from a static word vector because it

- A. is always larger
- B. depends on the surrounding tokens
- C. is trained without labels
- D. uses subwords

**Q8.4** For named-entity recognition, the standard reporting unit is

- A. document accuracy
- B. token accuracy
- C. entity-level precision, recall and F1
- D. perplexity

## Part B — True or false, with a reason (2 marks)

**Q8.5** "TF-IDF representations preserve word order, which is why they work well for sentiment
classification."

## Part C — Conceptual (4 marks)

**Q8.6** (2 marks) Why is token accuracy a poor metric for NER? Give a concrete example.

**Q8.7** (2 marks) Explain the difference between a normalisation step and a tokenisation step, and
why the order matters.

## Part D — Numerical (6 marks)

**Q8.8** (3 marks) Corpus of two documents: `d1 = "cat dog"`, `d2 = "cat bird"`. Using
$\mathrm{tf}(t,d)=$ count / tokens in $d$ and $\mathrm{idf}(t)=\ln(N/\mathrm{df}(t))$, compute the
TF-IDF weight of `dog` and of `cat` in `d1` (three decimal places).

**Q8.9** (3 marks) Per-class F1 scores are 0.80, 0.60 and 0.90. Compute macro-F1 and micro-F1 if
each class has the same number of true instances and the per-class support is identical.

## Part E — Tracing (2 marks)

**Q8.10** Build the bag-of-words vector for `"the cat sat"` using the vocabulary
`["cat", "dog", "sat", "the"]` (binary presence).

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m08.md) · [Next quiz](quiz-m09.md)
