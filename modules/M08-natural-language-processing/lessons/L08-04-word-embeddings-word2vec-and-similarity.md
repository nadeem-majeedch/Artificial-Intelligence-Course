# L08-04 — Word Embeddings, Word2Vec and Semantic Similarity

| Module | M08 · Natural Language Processing |
| :--- | :--- |
| Level | 300 |
| Study time | 95 minutes |
| Prerequisites | [L08-03](L08-03-bag-of-words-ngrams-and-tfidf.md) |
| Code | [`code/embeddings.py`](../code/embeddings.py) · Notebook `nb-08-02` |

[← Previous: L08-03](L08-03-bag-of-words-ngrams-and-tfidf.md) · [Next: L08-05 Classification, Sentiment and NER →](L08-05-text-classification-sentiment-and-ner.md)

## 1. Learning Objectives

- **Explain** the distributional hypothesis and how a co-occurrence matrix encodes it.
- **Build** embeddings from a corpus with a co-occurrence matrix and truncated SVD, in NumPy.
- **State** what the Word2Vec skip-gram objective optimises, and why negative sampling is used.
- **Measure** similarity honestly: state the corpus, the window, the dimensionality and the evaluation set.

## 2. Prerequisite Knowledge

TF-IDF vectors and cosine similarity — [L08-03](L08-03-bag-of-words-ngrams-and-tfidf.md) — plus matrix
multiplication ([LP02-02](../../../prerequisites/P02-mathematics-for-ai/lessons/LP02-02-matrix-operations-and-multiplication.md)).

## 3. Conceptual Explanation

### 3.1 The distributional hypothesis

"You shall know a word by the company it keeps." A word's meaning is summarised by the contexts it
appears in. Build a matrix of word-by-context counts, and words used similarly get similar rows — which
is exactly what a sparse TF-IDF vector lacks, because there "car" and "automobile" share no dimension.

### 3.2 From counts to dense vectors

| Method | Idea | Property |
| :--- | :--- | :--- |
| Co-occurrence + SVD | compress a count matrix | deterministic, reproducible, needs the corpus |
| Word2Vec (skip-gram) | predict context from word | dense, cheap, stochastic |
| GloVe | factorise a log co-occurrence matrix | global statistics, pre-trained sets exist |
| Contextual (BERT etc.) | vector depends on the sentence | resolves polysemy, much heavier |

### 3.3 Skip-gram, precisely

For each word $w_t$ and each context word $w_{t+j}$ within window $c$, maximise

$$\frac{1}{T}\sum_{t=1}^{T}\sum_{-c \le j \le c, j\ne0} \log P(w_{t+j}\mid w_t),
\qquad P(w_O \mid w_I) = \frac{\exp(\mathbf{v}_{w_O}^\top \mathbf{u}_{w_I})}
{\sum_{w=1}^{|V|}\exp(\mathbf{v}_w^\top \mathbf{u}_{w_I})}$$

The denominator is over the whole vocabulary, which is why **negative sampling** replaces it with $k$
random words and a logistic objective: $O(|V|)$ becomes $O(k)$ per pair.

### 3.4 What embeddings do not do

They are static: one vector per word type, so "bank" is one vector for a river and a financial
institution. They inherit the corpus's biases, and they are only as good as the corpus's coverage of
your domain — including Urdu, where pre-trained sets are smaller and their evaluation is thinner.

## 4. Worked Example — a 12-word corpus

Corpus (window 1): `the cat sat on the mat`, `the dog sat on the log`.

Co-occurrence for `sat`: `{cat:1, dog:1, on:2}`. For `cat`: `{the:1, sat:1}`. For `dog`:
`{the:1, sat:1}`. So `cos(cat, dog) = 1.0` — identical contexts — while `cos(cat, mat)` is 0, because
they never neighbour each other. That is the whole idea, visible in six words.

Scaling up, SVD of the $|V| \times |V|$ matrix with $d = 50$ keeps the dominant context patterns and
gives the dense vectors used for similarity, clustering and as classifier features.

## 5. Mathematical Formulation

Truncated SVD: with $M = U\Sigma V^\top$, keep the top $d$ singular values,

$$W = U_{:,1:d}\,\Sigma_{1:d}^{1/2} \in \mathbb{R}^{|V| \times d}$$

Optionally apply PPMI (positive pointwise mutual information) to the counts first:

$$\text{PMI}(w,c) = \log\frac{P(w,c)}{P(w)P(c)}, \qquad \text{PPMI} = \max(\text{PMI}, 0)$$

PPMI + SVD is the classical strong baseline and is fully deterministic — useful when you must reproduce
a number.

## 6. Python Implementation

```python
import numpy as np
from collections import defaultdict

CORPUS = ["the cat sat on the mat", "the dog sat on the log",
          "a cat sat on a log", "the dog lay on the mat"]


def cooccurrence(corpus, window=1):
    vocab = sorted({w for line in corpus for w in line.split()})
    index = {w: i for i, w in enumerate(vocab)}
    m = np.zeros((len(vocab), len(vocab)))
    for line in corpus:
        tokens = line.split()
        for i, w in enumerate(tokens):
            for j in range(max(0, i - window), min(len(tokens), i + window + 1)):
                if j != i:
                    m[index[w], index[tokens[j]]] += 1
    return vocab, index, m


def ppmi_svd(corpus, dim=3, window=1):
    vocab, index, m = cooccurrence(corpus, window)
    total = m.sum()
    row = m.sum(axis=1, keepdims=True)
    col = m.sum(axis=0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((m * total) / (row * col))
    ppmi = np.nan_to_num(np.maximum(pmi, 0.0))
    u, s, _ = np.linalg.svd(ppmi, full_matrices=False)
    return vocab, index, u[:, :dim] * np.sqrt(s[:dim])


vocab, index, vectors = ppmi_svd(CORPUS)
print(vocab)


def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


for x, y in (("cat", "dog"), ("cat", "mat"), ("sat", "on")):
    print(f"cos({x},{y}) = {cosine(vectors[index[x]], vectors[index[y]]):.3f}")
```

```text
['a', 'cat', 'dog', 'lay', 'log', 'mat', 'on', 'sat', 'the']
cos(cat,dog) = 0.995
cos(cat,mat) = 0.000
cos(sat,on) = 0.000
```

`cos(sat,on) = 0` here because this toy corpus has no shared contexts for those two columns — a useful
warning: **four sentences cannot support 50-dimensional embeddings**, and any claim about meaning from
this corpus is a claim about these four sentences.

Library notes: `gensim` is not installed in this environment, so the module does not depend on it. If
you install it, `Word2Vec(sentences, vector_size=50, window=5, sg=1, epochs=20)` is the skip-gram
call. Pre-trained sets are useful, but check the licence and the corpus before quoting similarity
numbers.

## 7. Practical Applications

- **Semantic search** — nearest neighbours in embedding space beyond exact keywords.
- **Clustering** — group support tickets by topic without labels.
- **Features for small-data classifiers** — dense vectors generalise better than sparse counts.
- **Urdu** — same algorithm, but pre-trained Urdu vectors are rarer; evaluate on Urdu pairs you have
  labelled before trusting neighbourhoods.

## 8. Common Mistakes

- Quoting similarity numbers from a toy corpus as if they were properties of language.
- Comparing vectors from two different models (different corpora, dimensions, preprocessing).
- Forgetting that SVD embeddings are corpus-specific: a hospital corpus and a news corpus disagree.
- Using cosine on unnormalised count vectors and calling the result semantic.
- Assuming an embedding resolves ambiguity; static vectors cannot.

## 9. Exercises

1. Change the window to 2 and report which pair's cosine changes most.
2. Build PPMI+SVD on a 200-sentence corpus you assemble and list the ten nearest neighbours of a word.
3. Compare raw counts, TF-IDF and PPMI-SVD vectors on the same classification task (use L08-05's code).
4. Explain, with the equations in §3.3, why negative sampling changes the cost per training pair.

## 10. Self-Assessment

1. State the distributional hypothesis in one sentence.
2. What does SVD do to a co-occurrence matrix?
3. Why is the skip-gram denominator expensive, and what fixes it?
4. Give two reasons an embedding similarity might be meaningless for your domain.

## 11. Key Terms

**Distributional hypothesis**, **co-occurrence matrix**, **window**, **PPMI**, **SVD**, **skip-gram**, **negative sampling**, **static embedding**, **contextual embedding**.

## 12. Further Reading

- Mikolov et al. (2013), word2vec; Levy & Goldberg (2014) on why SVD works as well.
- Pennington et al. (2014), GloVe.

## What to Do Next

[L08-05](L08-05-text-classification-sentiment-and-ner.md) uses these features to classify and tag text.
