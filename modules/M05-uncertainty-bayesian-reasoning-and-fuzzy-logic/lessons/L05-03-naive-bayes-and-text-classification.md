# L05-03 — Naive Bayes and Text Classification

| Module | M05 · Uncertainty, Bayesian Reasoning and Fuzzy Logic |
| :--- | :--- |
| Level | 300 |
| Study time | 80 minutes |
| Prerequisites | [L05-02](L05-02-bayesian-networks-independence-and-inference.md) · [LP04-01](../../../prerequisites/P04-data-preparation-and-visualization/lessons/LP04-01-dataset-structures-csv-and-json.md) |
| Notebook | NB-05-01 Uncertainty Workbench |

[← Previous: L05-02](L05-02-bayesian-networks-independence-and-inference.md) · [Next: L05-04 Fuzzy Sets →](L05-04-fuzzy-sets-membership-functions-and-operations.md)

## 1. Learning Objectives

- **Derive** the naive Bayes decision rule from Bayes' theorem and one independence assumption.
- **Implement** multinomial naive Bayes with Laplace smoothing.
- **Explain** why the assumption is false and why the classifier still works.
- **Diagnose** the two standard failures: unseen words and class imbalance.

## 2. Prerequisite Knowledge

Bayes' theorem and the network factorisation — L05-01 and L05-02.

## 3. Conceptual Explanation

### 3.1 The assumption

Naive Bayes assumes features are conditionally independent given the class:

$$P(c\mid x) \propto P(c)\prod_{i=1}^{n} P(x_i \mid c)$$

For text, $x_i$ are tokens. The assumption is plainly false — words co-occur — but the *decision*
only needs the argmax to be right, not the probabilities to be calibrated.

### 3.2 Smoothing is not optional

A word never seen in the spam class makes $P(w\mid\text{spam}) = 0$, which zeroes the entire product.
Laplace smoothing adds a pseudo-count:

$$P(w\mid c) = \frac{\text{count}(w,c) + \alpha}{\sum_{w'} \text{count}(w',c) + \alpha|V|}$$

### 3.3 What it is good for

Naive Bayes is a fast, strong baseline for text: training is one pass, prediction is a dot product in
log space. Its weakness is correlated features and its inability to model word order — which is why
M08 moves on to learned representations.

## 4. Worked Example — three-word vocabulary

Classes spam/ham, vocabulary {free, meeting, invoice}, $\alpha = 1$.

Counts: spam (free 8, meeting 1, invoice 3, total 12); ham (free 2, meeting 9, invoice 1, total 12).

$P(\text{free}\mid\text{spam}) = \frac{8+1}{12+3} = 0.6$; $P(\text{free}\mid\text{ham}) = \frac{3}{15} = 0.2$.

Message "free invoice": spam score $\propto 0.5 \times 0.6 \times \frac{4}{15} = 0.08$; ham score
$\propto 0.5 \times 0.2 \times \frac{2}{15} = 0.0133$. Posterior spam ≈ 0.857.

## 5. Mathematical Formulation

Log-space decision rule (numerically stable):

$$\hat{c} = \arg\max_c \left[\log P(c) + \sum_i \log P(x_i \mid c)\right]$$

## 6. Python Implementation

```python
import math
from collections import Counter, defaultdict


class NaiveBayes:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.counts = defaultdict(Counter)
        self.class_counts = Counter()
        self.vocab = set()

    def fit(self, docs, labels):
        for doc, label in zip(docs, labels):
            self.class_counts[label] += 1
            for w in doc.split():
                self.counts[label][w] += 1
                self.vocab.add(w)
        self.totals = {c: sum(self.counts[c].values()) for c in self.class_counts}

    def predict(self, doc):
        scores = {}
        for c, n in self.class_counts.items():
            logp = math.log(n / sum(self.class_counts.values()))
            for w in doc.split():
                logp += math.log((self.counts[c][w] + self.alpha) /
                                 (self.totals[c] + self.alpha * len(self.vocab)))
            scores[c] = logp
        best = max(scores, key=scores.get)
        return best, scores


docs = ["free money now", "free invoice attached", "meeting at noon",
        "free meeting tomorrow", "invoice for meeting room"]
labels = ["spam", "spam", "ham", "ham", "ham"]
nb = NaiveBayes().fit(docs, labels)
print(nb.predict("free meeting")[0])
print(nb.predict("invoice attached")[0])
```

## 7. Practical Applications

- **Spam and phishing filters** — the classic deployment.
- **Support ticket routing** — 20 categories, thousands of tickets a day.
- **Sentiment baselines** — the number every neural model must beat.
- **Language identification** — character n-grams with the same rule.

## 8. Common Mistakes

- No smoothing, so one unseen word vetoes the class.
- Multiplying probabilities instead of adding logs, causing underflow.
- Evaluating with accuracy on a 5%-positive dataset.
- Treating the posterior as calibrated and using it as a probability threshold.
- Adding features that are duplicates of each other and then blaming the model.

## 9. Exercises

1. Add bigrams and measure accuracy against unigrams on the same split.
2. Vary $\alpha \in \{0.1, 1, 10\}$ and plot accuracy.
3. Build a confusion matrix and report per-class precision and recall.
4. Construct a document where the independence assumption changes the answer, and explain it.

## 10. Self-Assessment

1. What exactly is assumed independent?
2. Why add $\alpha$, and what does $|V|$ contribute?
3. Why evaluate in log space?
4. When would you prefer logistic regression to naive Bayes?

## 11. Key Terms

**Naive Bayes**, **conditional independence**, **Laplace smoothing**, **prior**, **log-likelihood**, **baseline**.

## 12. Further Reading

- Russell & Norvig, section 13.6.
- Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, chapter 13.

## What to Do Next

[L05-04](L05-04-fuzzy-sets-membership-functions-and-operations.md) switches from randomness to
vagueness — a different kind of uncertainty.
