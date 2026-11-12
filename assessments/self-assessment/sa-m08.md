# SA-M08 — Self-Assessment: Natural Language Processing

Module M08 · [Module](../../docs/CURRICULUM-MAP.md) · [Quiz](../quizzes/quiz-m08.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Explain the effect of normalisation choices on downstream metrics
- [ ] Compare word, subword and character tokenisation
- [ ] Compute TF-IDF weights for a small corpus
- [ ] Distinguish static and contextual embeddings
- [ ] Explain entity-level scoring for NER
- [ ] Describe what a transformer block computes

## Knowledge-check questions

1. Why does subword tokenisation reduce out-of-vocabulary rates?
2. In a two-document corpus where a word appears in both, what is its IDF?
3. Why is token accuracy a poor NER metric?
4. What does "contextual" mean for an embedding, concretely?
5. Why is macro-F1 preferred over accuracy for imbalanced text classification?

## Practical competency checklist

- [ ] Build a TF-IDF pipeline with a validation-tuned `min_df`
- [ ] Inspect tokenisation of an unusual string and explain the result
- [ ] Report per-class metrics for a text classifier
- [ ] Group misclassifications into at least three categories

## Suggested revision topics

Preprocessing and normalisation · tokenisation · bag of words and TF-IDF · embeddings ·
sequence labelling and entity scoring · attention and transformers · evaluation under imbalance.

## Readiness test for M09

Without notes:

1. Compute a TF-IDF vector for a two-document corpus.
2. Explain why the same word can have two embeddings in one sentence.
3. State the metric you would report for NER and why.

If any is shaky, revisit L08-02 and L08-05 before M09.
