# LAB-08-01 — Text Preprocessing and Feature Extraction

| | |
| :--- | :--- |
| Module | M08 · Natural Language Processing |
| Time | 2 hours |
| Level | 300 |
| Pairs with | L08-01, L08-02, L08-03 |
| Notebook | `nb-08-01-tokenisation-and-features.ipynb` |

[Module home](../README.md) · [Lab 2](lab-08-02-news-and-document-classification.md) · [Lab 3](lab-08-03-urdu-and-english-sentiment-and-ner.md)

## Scenario

A support desk receives 400 messages a day in English and Urdu, mixed in one inbox. The routing model
built last year performs well in testing and badly in production. The postmortem finds three causes: the
tokeniser drops Urdu sentence boundaries, stopword removal deleted negations, and the vectoriser was
refitted on each new batch, so the same message scored differently on different days.

You are asked to rebuild the text pipeline so that the same message always produces the same features,
in both scripts, and to prove it with tests.

## Problem statement

Design, implement and test a deterministic preprocessing and feature-extraction pipeline for mixed
English/Urdu text.

## Dataset information

| Item | Detail |
| :--- | :--- |
| Source | **Synthetic**, generated for this course; no real customer data |
| Size | 40 short messages (20 English, 20 Urdu), included inline in the starter code |
| Labels | topic only (billing, delivery, account) |
| Licence | Created for this repository; reuse permitted with attribution to the course |
| Why synthetic | Licensing and privacy; the pipeline lesson does not need scale |

## Requirements

- **R1** One `preprocess(text)` function that records every decision it makes (case, diacritics, digit handling).
- **R2** Script detection and a per-script tokeniser; Urdu sentence splitting on `۔`.
- **R3** Negation preserved in both languages: no stopword list may remove negation words.
- **R4** A fitted vectoriser saved once and reused; no refitting per batch.
- **R5** Determinism test: the same input produces byte-identical features twice, and after a reload.
- **R6** A table of feature counts and vocabulary size for unigrams, unigrams+bigrams, and TF-IDF.

## Tasks

1. **Inventory** (20 min). List every normalisation step and what it destroys.
2. **Tokenise** (30 min). Implement and test both scripts; include a mixed-script message.
3. **Vectorise** (30 min). Build counts and TF-IDF by hand, then with scikit-learn; compare.
4. **Persist** (20 min). Save the fitted vectoriser, reload, and confirm identical output.
5. **Measure** (20 min). Vocabulary size and matrix sparsity for each configuration.

## Starter code

```python
import re, unicodedata

MESSAGES = [
    ("The parcel has not arrived and the tracking page is blank", "delivery"),
    ("میں نے ادائیگی کی ہے لیکن رسید نہیں آئی", "billing"),
    ("Please close my account, I am not happy", "account"),
]

def normalise(text):
    return unicodedata.normalize("NFKC", text).strip()

def tokenise(text):
    if re.search(r"[\u0600-\u06FF]", text):
        return re.findall(r"[\u0600-\u06FF]+|[A-Za-z]+|\d+(?:\.\d+)?", normalise(text))
    return re.findall(r"[A-Za-z]+(?:'[a-z]+)?|\d+(?:\.\d+)?", normalise(text).lower())
```

## Expected behaviour

- Both scripts tokenise without dropping characters; the Urdu full stop is a boundary.
- "not" and "نہیں" survive every configuration.
- Reloaded vectoriser produces identical vectors (assert equality, not approximate).
- Vocabulary grows by roughly 5–10× when bigrams are added on this corpus.

## Testing

| Test | Expected |
| :--- | :--- |
| Urdu sentence count | 2 sentences for a two-sentence paragraph |
| Negation survival | `not` and `نہیں` present after preprocessing |
| Determinism | identical vectors across two runs and after reload |
| Sparse shape | rows = documents, columns = vocabulary |
| Idempotence | `preprocess(preprocess(x)) == preprocess(x)` |

## Deliverables

| File | Contents |
| :--- | :--- |
| `pipeline.py` | `preprocess`, `tokenise`, vectoriser, persistence |
| `tests_pipeline.py` | The five tests above |
| `report.md` | Feature-count table and the three postmortem causes, fixed |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Correctness | 30% | both scripts, negation preserved | English only | broken tokens |
| Determinism | 25% | persistence + reload test | same-run test | none |
| Measurement | 20% | vocabulary/sparsity table with interpretation | numbers | none |
| Testing | 15% | all five tests | three | none |
| Explanation | 10% | names what each step destroys | describes steps | missing |

## Extension challenges

1. Add character n-grams for Urdu and show which tokens they recover from misspellings.
2. Add a mixed-script message (`WiFi کی سہولت نہیں`) and state the tokenisation rule you chose.
3. Measure the effect of diacritic removal on duplicate detection.
4. Add a hash-based vectoriser and compare memory and determinism with the vocabulary one.

## Reflection

1. Which of the three postmortem causes would a test have caught earliest?
2. What did you decide about digits, and what does that decision make impossible later?
3. Is your pipeline ready for a third script? What would have to change?

---

[Module home](../README.md) · [Lab 2](lab-08-02-news-and-document-classification.md) · [Lab 3](lab-08-03-urdu-and-english-sentiment-and-ner.md)
