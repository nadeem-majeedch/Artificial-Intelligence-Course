# QUIZ-M08 — Solutions and Explanations

> **Availability.** M08 (Natural Language Processing) — reference code only in this repository, so this paper cannot be attempted
> yet. It is included so the assessment set is complete, and it is a preview
> rather than an assessment until the module's lessons are published.

[Quiz](quiz-m08.md) · [Assessment index](../README.md)

---

## Part A

**Q8.1 — B.** Subword units let a fixed vocabulary cover unseen words by composition, shrinking the
vocabulary while removing most out-of-vocabulary cases. They do not fix grammar or imbalance.

**Q8.2 — B.** IDF is $\ln(N/\mathrm{df})$: a term appearing in every document has $\mathrm{df}=N$
and weight zero. That is what down-weights ubiquitous words.

**Q8.3 — B.** Contextual encoders produce a different vector for "bank" in "river bank" and "bank
loan"; static vectors assign one vector per word type.

**Q8.4 — C.** NER is scored at the entity level, because a partially correct span is not a correct
entity. Token accuracy hides boundary errors and the abundance of O tokens.

## Part B

**Q8.5 — False.** TF-IDF is a bag-of-words representation: it discards order entirely. It works for
sentiment because individual words carry signal, not because order is preserved; "not good" and
"good not" get identical vectors, which is a known limitation.

## Part C

**Q8.6 — Model answer.** Most tokens are outside any entity, so a model that predicts "no entity"
everywhere scores very high token accuracy while finding nothing. Entity-level F1 is the metric
that reflects the task: a missed person name is a false negative regardless of how many other
tokens were labelled correctly.

**Q8.7 — Model answer.** Normalisation unifies surface forms (lowercasing, unicode folding,
stripping punctuation); tokenisation splits the text into units. Order matters because normalising
after tokenising can corrupt tokens (e.g. lowercasing a case-sensitive identifier), and tokenising
before normalising may produce units that no longer merge consistently.

## Part D

**Q8.8 —**

- `dog`: $\mathrm{tf}=1/2=0.5$, $\mathrm{df}=1$, $\mathrm{idf}=\ln(2/1)=0.693$, weight
  $0.5\times0.693=0.347$.
- `cat`: $\mathrm{tf}=1/2=0.5$, $\mathrm{df}=2$, $\mathrm{idf}=\ln(2/2)=0$, weight $0$.

The word in every document carries no discriminative weight — that is the point of IDF.

**Q8.9 —** Macro-F1 $=(0.80+0.60+0.90)/3=0.767$. With equal support and equal per-class
performance weighting, micro-F1 equals the accuracy over all instances, which here equals the
average of the per-class F1s only if the confusion structure is symmetric; with identical support
and no cross-class confusion assumed, micro-F1 $=0.767$ as well. State the assumption: micro-F1
weights by support, so it equals macro-F1 only when supports are equal.

## Part E

**Q8.10 —** Vocabulary order `[cat, dog, sat, the]` → `[1, 0, 1, 1]` for "the cat sat". Each present
word contributes 1, absent 0. (Binary presence, not counts.)

---

[Quiz](quiz-m08.md) · [Previous solutions](quiz-m07.md) · [Assessment index](../README.md)
