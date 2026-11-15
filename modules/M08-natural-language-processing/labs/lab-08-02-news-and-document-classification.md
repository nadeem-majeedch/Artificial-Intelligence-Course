# LAB-08-02 — News and Document Classification

| | |
| :--- | :--- |
| Module | M08 · Natural Language Processing |
| Time | 2.5 hours |
| Level | 300 |
| Pairs with | L08-03, L08-05 |
| Notebook | `nb-08-02-classification-and-ner.ipynb` |

[Module home](../README.md) · [Lab 1](lab-08-01-text-preprocessing-and-feature-extraction.md) · [Lab 3](lab-08-03-urdu-and-english-sentiment-and-ner.md)

## Scenario

A campus news service publishes 60 short items a week across four sections. The editor wants automatic
section assignment so drafts reach the right editor, and she has one non-negotiable requirement: the
system must not silently bury the smallest section, because that is where the investigative pieces go.

You have 200 labelled items, an imbalanced distribution, and one afternoon.

## Problem statement

Build and evaluate a document classifier that is honest about the smallest class, and state the
operating point you would deploy.

## Dataset information

| Item | Detail |
| :--- | :--- |
| Source | **Synthetic** news items generated for this course, plus optional public corpora |
| Synthetic set | 120 items, 4 sections, distribution 45/35/28/12 |
| Optional public set | 20 Newsgroups (scikit-learn loader, download required, permissive licence for research use) |
| Licence | Synthetic items: created for this repository. 20 Newsgroups: see its bundled README before redistributing |
| Not used | Any scraped news site: licensing and copyright make redistribution unsafe |

## Requirements

- **R1** Train TF-IDF (unigrams, then unigrams+bigrams) with a linear classifier; report macro-F1 and per-class F1.
- **R2** A confusion matrix, with the smallest class visible.
- **R3** A stratified split, and a statement of the split sizes.
- **R4** One experiment that addresses the imbalance (class weights or resampling) and its measured effect.
- **R5** A deployment recommendation: which metric threshold, and what happens below it.
- **R6** An error analysis of five misclassifications, with the actual text quoted.

## Tasks

1. **Split** (15 min). Stratified 70/30; report counts per class.
2. **Baseline** (35 min). Unigram TF-IDF + logistic regression; macro-F1, per-class F1, confusion matrix.
3. **Bigrams** (25 min). Repeat and compare; state whether the difference is worth the vocabulary growth.
4. **Imbalance** (30 min). Add `class_weight="balanced"`; report the smallest class's recall before and after.
5. **Errors** (25 min). Five misclassified items, quoted, with a one-line cause each.
6. **Recommendation** (20 min). Operating point and escalation policy.

## Starter code

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# X: list of documents, y: section labels -- build or load your 120-item set here
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

model = make_pipeline(TfidfVectorizer(ngram_range=(1, 1), sublinear_tf=True),
                      LogisticRegression(max_iter=1000, class_weight="balanced"))
model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test), digits=3))
print(confusion_matrix(y_test, model.predict(X_test)))
```

## Expected behaviour

- Macro-F1 in the 0.6–0.85 range on synthetic items; the smallest class is the weakest.
- Bigrams give a small or negative gain at this corpus size — report it as such rather than tuning until it looks good.
- `class_weight="balanced"` raises the smallest class's recall and lowers overall accuracy slightly.
- At least one error is caused by a section-specific word appearing in a different section (e.g. "budget" in sport).

## Testing

| Test | Expected |
| :--- | :--- |
| Split integrity | no document in both splits |
| Vectoriser isolation | fitted on train only |
| Metric computation | macro-F1 matches a hand-computed two-class example |
| Reproducibility | same random_state, identical report |
| Class coverage | every class appears in both splits |

## Deliverables

| File | Contents |
| :--- | :--- |
| `classify_news.py` | Pipeline, experiments, metrics |
| `results.md` | Tables for unigram, bigram, balanced |
| `errors.md` | Five quoted errors with causes |
| `recommendation.md` | ≤ 250 words: operating point and escalation |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Evaluation | 30% | macro-F1, per-class, confusion, split sizes | accuracy only | unreported |
| Imbalance handling | 25% | measured effect on smallest class | attempted | ignored |
| Error analysis | 25% | quoted errors with causes | counts | none |
| Recommendation | 20% | specific operating point and policy | general advice | missing |

## Extension challenges

1. Add a fifth "unknown" class from out-of-distribution items and report the abstention rate.
2. Compare TF-IDF + logistic regression with a pre-trained encoder, including wall-clock cost; state whether the gap justifies the compute.
3. Calibrate the classifier and show how the operating point changes with a calibrated probability.
4. Repeat with Urdu items and report per-language metrics separately.

## Reflection

1. The editor's requirement is about the smallest class. Which metric did you choose, and why?
2. Your model is 78% accurate. What would you tell the editor it cannot do?
3. Which error would you most want a human to see before publication?

---

[Module home](../README.md) · [Lab 1](lab-08-01-text-preprocessing-and-feature-extraction.md) · [Lab 3](lab-08-03-urdu-and-english-sentiment-and-ner.md)
