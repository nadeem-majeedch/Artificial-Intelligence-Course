# M08 — Natural Language Processing

| Level | 300 |
| :--- | :--- |
| Study time | 24.3 hours — guided 9.5 · practical 9.0 · assessment 5.8 · project 0.0 |
| Lessons | 6 of 6 |
| Course outcome | CLO6, CLO7 — process text, build features, classify and label it, and reason about sequence models |
| Prerequisites | [M07 Neural Networks](../M07-neural-networks-and-deep-learning/README.md) (for L08-06), [P01](../../prerequisites/P01-python-programming/README.md) |

[← Previous module: M07](../M07-neural-networks-and-deep-learning/README.md) · [Course home](../../README.md) · [All modules](../README.md) · [Next module: M09](../README.md#m09)

## Overview

Language is the domain where modern AI is most visible and least understood. This module starts with the
unglamorous foundations — Unicode normalisation, script-specific tokenisation, TF-IDF — because they
explain what a model actually sees, then moves through embeddings and classification to attention and
transformers. Urdu appears throughout as a second language: same algorithms, different problems.

Everything runs offline on CPU. No paid API, no model download, no external dataset is required: the
corpora in the lessons and notebooks are small and synthetic, and that limitation is stated every time a
number is quoted.

## Learning outcomes

By the end of this module you will be able to:

1. **Prepare** English and Urdu text without destroying information, and justify each normalisation choice.
2. **Build** bag-of-words, n-gram and TF-IDF features by hand and with scikit-learn, and evaluate them.
3. **Train** a text classifier and report macro-F1, per-class F1 and a confusion matrix instead of accuracy.
4. **Score** sequence labelling at span level, and explain why token accuracy misleads.
5. **Compute** scaled dot-product attention and explain what a transformer block adds.
6. **Judge** whether a task needs a transformer or a linear baseline, with a cost argument.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L08-01 | Introduction to NLP and the Text Pipeline | Lesson | 75 m | [Read](lessons/L08-01-introduction-to-nlp-and-the-text-pipeline.md) |
| L08-02 | Preprocessing, Tokenization, Stemming and Lemmatization | Lesson | 100 m | [Read](lessons/L08-02-preprocessing-tokenization-stemming-lemmatization.md) |
| L08-03 | Bag of Words, N-grams and TF-IDF | Lesson | 90 m | [Read](lessons/L08-03-bag-of-words-ngrams-and-tfidf.md) |
| L08-04 | Word Embeddings, Word2Vec and Semantic Similarity | Lesson | 95 m | [Read](lessons/L08-04-word-embeddings-word2vec-and-similarity.md) |
| L08-05 | Text Classification, Sentiment Analysis and NER | Lesson | 100 m | [Read](lessons/L08-05-text-classification-sentiment-and-ner.md) |
| L08-06 | Sequence Models, Attention and Transformers | Lesson | 110 m | [Read](lessons/L08-06-sequence-models-attention-and-transformers.md) |
| NB-08-01 | Tokenisation and Features | Notebook | 60 m | [Open](notebooks/nb-08-01-tokenisation-and-features.ipynb) |
| NB-08-02 | Classification, Sentiment and NER | Notebook | 60 m | [Open](notebooks/nb-08-02-classification-and-ner.ipynb) |
| NB-08-03 | Attention and Sequences | Notebook | 45 m | [Open](notebooks/nb-08-03-attention-and-sequences.ipynb) |
| LAB-08-01 | Text Preprocessing and Feature Extraction | Lab | 2 h | [Start](labs/lab-08-01-text-preprocessing-and-feature-extraction.md) |
| LAB-08-02 | News and Document Classification | Lab | 2.5 h | [Start](labs/lab-08-02-news-and-document-classification.md) |
| LAB-08-03 | Urdu and English Sentiment and NER | Lab | 3 h | [Start](labs/lab-08-03-urdu-and-english-sentiment-and-ner.md) |
| QUIZ-08 | Module self-check | Quiz | 30 m | [Take](../../assessments/quizzes/quiz-m08.md) |

## Reference code

The module's original reference code is preserved and still runs:
`text_data.py` (corpus), `text_pipeline.py` (normalisation and TF-IDF), `classify.py` (classifiers),
`embeddings.py` (static and contextual embeddings), `seq_models.py` (tagging and classification).
The lessons implement the same ideas in minimal form so each step is visible.

## Datasets and licensing

| Data used | Provenance | Licence |
| :--- | :--- | :--- |
| Lessons, notebooks, labs | Small corpora written for this course | Created for this repository; reuse with attribution |
| Optional: Urdu sentiment corpora | Public collections exist, with differing terms | Check before redistributing; not included here |
| Optional: 20 Newsgroups | scikit-learn loader, download required | See the dataset's bundled terms |

No pre-trained Urdu model is bundled, and no claim is made that any specific model supports Urdu well.
If you load one, record its name, revision and measured performance on your own labelled data.

## Language coverage and its limits

- **English** — full preprocessing, features, classification, sentiment, NER, attention.
- **Urdu** — normalisation (NFKC, Arabic-script variants, diacritics), script-specific tokenisation and
  sentence splitting on `۔`, negation handling, sentiment and span tagging on synthetic data.
- **Stated limitations** — no large Urdu corpus, no validated pre-trained Urdu model, no Roman-Urdu
  handling. Labs require students to report these limits rather than paper over them.

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L08-01, L08-02, NB-08-01 | 3.5 h |
| 2 | L08-03, start LAB-08-01 | 3 h |
| 3 | L08-04, L08-05, NB-08-02 | 3.5 h |
| 4 | LAB-08-02 | 2.5 h |
| 5 | L08-06, NB-08-03 | 2.5 h |
| 6 | LAB-08-03 | 3 h |

## Assessment for this module

| Component | Weight |
| :--- | ---: |
| LAB-08-01 (pipeline determinism, both scripts) | 25% |
| LAB-08-02 (classification, imbalance, error analysis) | 30% |
| LAB-08-03 (bilingual sentiment, span NER, limitations) | 30% |
| QUIZ-08 | 15% |

## Key terms introduced

**Normalisation**, **NFKC**, **tokenisation**, **sentence segmentation**, **stemming**, **lemmatization**,
**bag of words**, **n-gram**, **TF-IDF**, **co-occurrence**, **PPMI**, **skip-gram**, **static vs
contextual embedding**, **macro-F1**, **BIO tagging**, **span F1**, **attention**, **positional
encoding**. Definitions: [glossary](../../resources/glossary/nlp-and-vision.md).

## Navigation

[← Previous module: M07](../M07-neural-networks-and-deep-learning/README.md) · [Course home](../../README.md) ·
[All modules](../README.md) · [Next module: M09](../README.md#m09)

## Assignment

[PA-08 — Text Classification from TF-IDF to a Transformer](../../assessments/programming/pa-08-nlp.md)
