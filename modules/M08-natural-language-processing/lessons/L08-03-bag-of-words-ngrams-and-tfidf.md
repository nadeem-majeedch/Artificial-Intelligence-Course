# L08-03 — Bag of Words, N-grams and TF-IDF

| Module | M08 · Natural Language Processing |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | [L08-02](L08-02-preprocessing-tokenization-stemming-lemmatization.md) |
| Code | [`code/text_pipeline.py`](../code/text_pipeline.py) · Notebook `nb-08-02` |

[← Previous: L08-02](L08-02-preprocessing-tokenization-stemming-lemmatization.md) · [Next: L08-04 Embeddings →](L08-04-word-embeddings-word2vec-and-similarity.md)

## 1. Learning Objectives

- **Build** a bag-of-words matrix by hand, then with scikit-learn, and explain the difference.
- **Add** n-grams and say what word order buys and what it costs.
- **Compute** TF-IDF and explain each of its three decisions: term frequency, inverse document frequency, normalisation.
- **Show** a case where TF-IDF beats raw counts, and one where it does not.

## 2. Prerequisite Knowledge

Tokenisation and normalisation — [L08-02](L08-02-preprocessing-tokenization-stemming-lemmatization.md).

## 3. Conceptual Explanation

### 3.1 Bag of words

Represent a document by counts over a fixed vocabulary — a vector in $\mathbb{R}^{|V|}$. Order is
discarded, which is exactly why it works: for topic classification, "refund" appearing twice matters
more than where.

Problems: sparse (most entries zero), no meaning ("car" and "automobile" are unrelated dimensions),
and unbounded vocabulary.

### 3.2 N-grams

Take consecutive token sequences as features: `not good` is one feature, distinct from `good`.

| n | Feature | Gain | Cost |
| :--- | :--- | :--- | :--- |
| 1 | `good` | small vocabulary | no negation, no phrases |
| 2 | `not_good` | negation, idioms | vocabulary × 10 |
| 3 | `not_very_good` | more context | sparsity, overfitting |

Bigrams are the usual compromise for sentiment; trigrams on small corpora mostly memorise.

### 3.3 TF-IDF

$$\text{tfidf}(t,d) = \underbrace{\text{tf}(t,d)}_{\text{local importance}} \times
\underbrace{\log\frac{N+1}{\text{df}(t)+1} + 1}_{\text{rarity}}$$

then L2-normalise the document vector. The three decisions:

1. **tf** — raw count, or $1+\log \text{count}$, or binary presence;
2. **idf** — the smoothing above keeps a term in all documents from vanishing;
3. **normalisation** — without it, long documents dominate every similarity.

IDF is computed from the *training* corpus and applied unchanged at test time; recomputing it per batch
is a common and silent evaluation bug.

## 4. Worked Example — three documents

```
d1: "refund refund delay"
d2: "refund policy"
d3: "delay delay delay delay"
```

$N = 3$; $\text{df}(\text{refund}) = 2$, $\text{df}(\text{delay}) = 2$, $\text{df}(\text{policy}) = 1$.

$\text{idf}(\text{refund}) = \log(4/3) + 1 = 1.2877$; $\text{idf}(\text{delay}) = 1.2877$;
$\text{idf}(\text{policy}) = \log(4/2) + 1 = 1.6931$.

| doc | tf(refund) | tf(delay) | tf(policy) | L2-normalised tf-idf (refund, delay, policy) |
| :--- | ---: | ---: | ---: | :--- |
| d1 | 2 | 1 | 0 | (0.743, 0.371, 0) |
| d2 | 1 | 0 | 1 | (0.485, 0, 0.637) |
| d3 | 0 | 4 | 0 | (0, 1.0, 0) |

Note d1's refund weight (0.743) is *not* twice d2's (0.485): normalisation mixes the dimensions, which
is the point and also the source of most misunderstanding.

## 5. Mathematical Formulation

Cosine similarity between documents:

$$\cos(d_i,d_j) = \frac{\mathbf{x}_i \cdot \mathbf{x}_j}{\|\mathbf{x}_i\|_2\,\|\mathbf{x}_j\|_2}$$

With L2-normalised TF-IDF vectors this is a dot product, so similarity is bounded in $[-1, 1]$ and
independent of document length. A linear classifier on these vectors is then a strong baseline.

## 6. Python Implementation

```python
import math
import re

DOCS = ["refund refund delay", "refund policy", "delay delay delay delay"]


def make_vocab(docs):
    return sorted({w for d in docs for w in d.split()})


def tf(doc, vocab):
    counts = {w: 0 for w in vocab}
    for w in doc.split():
        counts[w] += 1
    return counts


def tfidf(docs):
    vocab = make_vocab(docs)
    df = {w: sum(1 for d in docs if w in d.split()) for w in vocab}
    n = len(docs)
    rows = []
    for d in docs:
        counts = tf(d, vocab)
        vec = {w: counts[w] * (math.log((n + 1) / (df[w] + 1)) + 1) for w in vocab}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        rows.append({w: round(v / norm, 3) for w, v in vec.items()})
    return vocab, rows


vocab, rows = tfidf(DOCS)
print(vocab)
for r in rows:
    print(r)


def cosine(a, b):
    return sum(a.get(w, 0) * b.get(w, 0) for w in vocab)


print("cos(d1,d2) =", round(cosine(rows[0], rows[1]), 3))
```

```text
['delay', 'policy', 'refund']
{'delay': 0.371, 'policy': 0.0, 'refund': 0.743}
{'delay': 0.0, 'policy': 0.637, 'refund': 0.485}
{'delay': 1.0, 'policy': 0.0, 'refund': 0.0}
cos(d1,d2) = 0.36
```

Library equivalent (no download needed):

```python
# from sklearn.feature_extraction.text import TfidfVectorizer
# vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, norm="l2")
# X = vec.fit_transform(train_docs); X_test = vec.transform(test_docs)   # fit only on train
```

## 7. Practical Applications

- **Ticket routing** — TF-IDF + linear model is still the honest baseline.
- **Search ranking** — BM25 is a refined TF-IDF and remains hard to beat on exact terms.
- **Duplicate detection** — cosine on TF-IDF with a threshold.
- **Urdu text** — identical maths; only the tokeniser changes (L08-02).

## 8. Common Mistakes

- Fitting the vectoriser on train+test, leaking vocabulary and IDF.
- Comparing raw and sublinear tf scores across experiments and calling it an improvement.
- Using trigrams on 200 documents, then reporting a 0.99 training score.
- Skipping normalisation, so long documents match everything.
- Assuming TF-IDF captures meaning: "car" and "automobile" remain orthogonal.

## 9. Exercises

1. Reproduce the table in §4 with `1 + log(tf)` and report what changes.
2. Add bigrams to a 20-document corpus you write and measure vocabulary growth.
3. Show a query where cosine on TF-IDF ranks the wrong document highest, and explain why.
4. Compute IDF on train only and on train+test for the same set; report the accuracy difference.

## 10. Self-Assessment

1. Why is the bag-of-words representation sparse, and why does that matter?
2. What does an n-gram feature capture that unigrams cannot?
3. Name the three design decisions inside TF-IDF.
4. Why must IDF come from the training corpus only?

## 11. Key Terms

**Bag of words**, **vocabulary**, **sparsity**, **n-gram**, **term frequency**, **document frequency**, **IDF smoothing**, **L2 normalisation**, **cosine similarity**, **BM25**.

## 12. Further Reading

- Manning, Raghavan & Schütze, chapters 6 and 8.
- Robertson & Zaragoza (2009) on BM25.

## What to Do Next

[L08-04](L08-04-word-embeddings-word2vec-and-similarity.md) replaces sparse counts with dense vectors
that carry meaning.
