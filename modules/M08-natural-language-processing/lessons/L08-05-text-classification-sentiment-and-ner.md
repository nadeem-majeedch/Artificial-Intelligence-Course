# L08-05 — Text Classification, Sentiment Analysis and Named Entity Recognition

| Module | M08 · Natural Language Processing |
| :--- | :--- |
| Level | 300 |
| Study time | 100 minutes |
| Prerequisites | [L08-03](L08-03-bag-of-words-ngrams-and-tfidf.md) · [L06-02](../../M06-machine-learning-fundamentals/lessons/L06-02-data-splitting-leakage-and-cross-validation.md) |
| Code | [`code/classify.py`](../code/classify.py) · Notebook `nb-08-02` |
| Labs | [LAB-08-02](../labs/lab-08-02-news-and-document-classification.md), [LAB-08-03](../labs/lab-08-03-urdu-and-english-sentiment-and-ner.md) |

[← Previous: L08-04](L08-04-word-embeddings-word2vec-and-similarity.md) · [Next: L08-06 Sequence Models and Transformers →](L08-06-sequence-models-attention-and-transformers.md)

## 1. Learning Objectives

- **Build** a text classifier with TF-IDF and a linear model, and evaluate it with macro-F1 and a confusion matrix.
- **Distinguish** document classification from sequence labelling, and choose the right metric for each.
- **Implement** BIO tagging with a rule-based tagger and score it with span-level F1.
- **Analyse** errors by class, length and language instead of reporting one aggregate number.

## 2. Prerequisite Knowledge

TF-IDF ([L08-03](L08-03-bag-of-words-ngrams-and-tfidf.md)) and classification metrics
([L06-02](../../M06-machine-learning-fundamentals/lessons/L06-02-data-splitting-leakage-and-cross-validation.md)).

## 3. Conceptual Explanation

### 3.1 Classification

Features → linear model → label. With TF-IDF this is a strong baseline: fast, explainable (inspect the
coefficients), and hard to beat on small corpora. Evaluate with **macro-F1** when classes are imbalanced
and you care about the rare ones; report the confusion matrix, because a single number hides which
confusion you have.

### 3.2 Sentiment is not just classification

Three complications that generic classification ignores:

1. **Negation and scope** — "not bad" is positive; "not good" is negative; the difference is one word.
2. **Intensity and contrast** — "great, but the delivery was late".
3. **Domain shift** — "sick" in gaming versus healthcare.

A model with unigram features learns "not" as a weak negative indicator and gets these wrong; bigrams
fix some, none fix sarcasm.

### 3.3 Named entity recognition is sequence labelling

Each token gets a tag in BIO: `B-PER`, `I-PER`, `O`. Metrics are computed on **spans**, not tokens: a
predicted span must match exactly (or by overlap, if you say so). Token accuracy is meaningless when
95% of tokens are `O` — a tagger that outputs only `O` scores 0.95 accuracy and 0 F1.

### 3.4 Urdu NER and sentiment

Same algorithms, different obstacles: no case, agglutination, inconsistent orthography, and sparse
labelled data. Rule-based gazetteers work better than expected for names and places; character n-grams
help with affixes. Any pre-trained Urdu model must be checked for availability and measured — the
existence of a model card is not evidence of quality on your data.

## 4. Worked Example — a tiny sentiment set with negation

| Text | Unigram prediction | Bigram prediction | True |
| :--- | :--- | :--- | :--- |
| "good service" | positive | positive | positive |
| "not good service" | positive (sees *good*) | negative (sees *not_good*) | negative |
| "not bad at all" | negative (sees *bad*) | positive | positive |
| "great, but late" | positive | positive | mixed/negative |

Accuracy: unigrams 0.50, bigrams 0.75 on these four — with four examples, that difference is a
hypothesis, not a result. Write it as one.

## 5. Mathematical Formulation

Macro-F1 over $K$ classes:

$$F1_{\text{macro}} = \frac{1}{K}\sum_{k=1}^{K}\frac{2P_kR_k}{P_k+R_k},\qquad
P_k = \frac{TP_k}{TP_k+FP_k},\quad R_k = \frac{TP_k}{TP_k+FN_k}$$

Span-level precision/recall for NER compares predicted span sets with gold span sets per document;
exact-match F1 is the standard, and partial-match F1 must be labelled as such when reported.

## 6. Python Implementation

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline

train = ["good service", "not good service", "not bad at all", "great, but late",
         "excellent support", "terrible support", "the delivery was late",
         "not happy with the delay"]
labels = ["pos", "neg", "pos", "neg", "pos", "neg", "neg", "neg"]

for ngram in ((1, 1), (1, 2)):
    model = make_pipeline(TfidfVectorizer(ngram_range=ngram, sublinear_tf=True),
                          LogisticRegression(max_iter=1000))
    model.fit(train, labels)
    print(ngram, model.predict(["not good service", "not bad at all"]))
```

```text
(1, 1) ['pos' 'neg']
(1, 2) ['neg' 'pos']
```

With bigrams the negation is captured; with unigrams it is not. This is a 8-example demonstration of a
mechanism, not a benchmark.

### BIO tagging and span scoring

```python
def bio_spans(tokens, tags):
    spans, current = [], None
    for token, tag in zip(tokens, tags):
        if tag.startswith("B-"):
            if current: spans.append(current)
            current = [tag[2:], token]
        elif tag.startswith("I-") and current and tag[2:] == current[0]:
            current[1] += " " + token
        else:
            if current: spans.append(current); current = None
    if current: spans.append(current)
    return {(kind, text) for kind, text in spans}


tokens = ["Ali", "works", "in", "Lahore", "."]
tags = ["B-PER", "O", "O", "B-LOC", "O"]
print(bio_spans(tokens, tags))
```

```text
{('PER', 'Ali'), ('LOC', 'Lahore')}
```

## 7. Practical Applications

- **Ticket routing** — macro-F1 matters because rare categories are the expensive ones.
- **Review monitoring** — sentiment by product and by week, with error analysis by language.
- **Document intake** — entity extraction for names, dates, amounts.
- **Urdu support** — separate models, separate evaluation, reported separately.

## 8. Common Mistakes

- Reporting accuracy on a 90%-negative dataset.
- Token-level F1 for a span task, or span F1 with a matching rule you did not state.
- Training and testing on documents from the same template.
- Mixing Urdu and English into one model without reporting per-language results.
- Treating a pre-trained Urdu tagger as validated because it loads without error.

## 9. Exercises

1. Reproduce the unigram/bigram table and add two more negation examples; report what changes.
2. Build a confusion matrix on a 40-document set you assemble and name the dominant confusion.
3. Extend `bio_spans` to handle `I-` tags that follow `O`, and state the rule you chose.
4. Score a rule-based Urdu tagger on ten sentences and report exact-match span F1.

## 10. Self-Assessment

1. When is macro-F1 the right metric, and what does it hide?
2. Why does a unigram sentiment model get "not good" wrong?
3. Why is token accuracy useless for NER?
4. What must you report for a pre-trained Urdu model before using it?

## 11. Key Terms

**Macro-F1**, **confusion matrix**, **negation scope**, **domain shift**, **BIO tagging**, **span F1**, **gazetteer**, **character n-gram**.

## 12. Further Reading

- Jurafsky & Martin, chapters 4 and 8.
- Daumé III, *A Course in Machine Learning*, chapter on structured prediction.

## What to Do Next

[L08-06](L08-06-sequence-models-attention-and-transformers.md) replaces hand-built features with learned
sequence representations.
