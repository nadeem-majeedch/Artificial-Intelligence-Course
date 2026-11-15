# LAB-08-03 — Urdu and English Sentiment Analysis and Named Entity Recognition

| | |
| :--- | :--- |
| Module | M08 · Natural Language Processing |
| Time | 3 hours |
| Level | 300 |
| Pairs with | L08-05, L08-06 |
| Notebook | `nb-08-03-attention-and-sequences.ipynb` |

[Module home](../README.md) · [Lab 1](lab-08-01-text-preprocessing-and-feature-extraction.md) · [Lab 2](lab-08-02-news-and-document-classification.md)

## Scenario

A telecoms company handles complaints in English and Urdu. The analytics team has an English sentiment
model that works acceptably and no Urdu model at all. They ask for one bilingual report — and they
specifically want to know where the Urdu side is *not* trustworthy, because a wrong "positive" label on
an Urdu complaint has already caused an escalation failure.

## Problem statement

Build sentiment classification and entity extraction for both languages, report per-language results
separately, and document the limits of the Urdu side honestly.

## Dataset information

| Item | Detail |
| :--- | :--- |
| Source | **Synthetic**, created for this course: 60 English and 60 Urdu short complaints with sentiment labels, plus 20 bilingual sentences with BIO entity tags |
| Included | Inline in the starter code and in `code/text_data.py` |
| Licence | Created for this repository; reuse with attribution. No real customer text is used. |
| Public alternatives | Urdu sentiment corpora exist (e.g. Urdu Roman-Urdu and Urdu reviews collections) but their licences differ; check before redistributing |
| Explicit non-claim | No pre-trained Urdu model is bundled or validated here. If you load one, record its name, revision and evaluation on your data |

## Requirements

- **R1** Per-language preprocessing (L08-02) with negation preserved in both scripts.
- **R2** Sentiment classifier per language, evaluated with macro-F1 and a confusion matrix, reported separately.
- **R3** A bilingual comparison table; no pooled number that hides the weaker language.
- **R4** BIO entity tagging with **span-level** exact-match F1, per entity type.
- **R5** A limitations section naming at least three specific Urdu failure modes you observed.
- **R6** One honest statement about what a pre-trained multilingual model would and would not fix.

## Tasks

1. **Data** (25 min). Load both sets; report class balance per language.
2. **Baseline EN** (30 min). TF-IDF (1,2) + logistic regression; macro-F1 and confusion matrix.
3. **Baseline UR** (35 min). Same pipeline with the Urdu tokeniser; report separately.
4. **Negation study** (25 min). Two examples per language where unigrams fail and bigrams help; quote them.
5. **NER** (35 min). Rule/gazetteer tagger, then span F1 per type (`PER`, `LOC`, `ORG`).
6. **Limitations** (30 min). Three observed Urdu failure modes, each with an example.

## Starter code

```python
import re, unicodedata

URDU_NEG = {"نہیں", "نہ", "مت"}
EN_NEG = {"not", "no", "never"}

def tokenise(text, script):
    text = unicodedata.normalize("NFKC", text)
    if script == "ur":
        return re.findall(r"[\u0600-\u06FF]+|[A-Za-z]+|\d+", text)
    return re.findall(r"[A-Za-z]+(?:'[a-z]+)?|\d+", text.lower())

def bio_spans(tokens, tags):
    spans, cur = [], None
    for tok, tag in zip(tokens, tags):
        if tag.startswith("B-"):
            if cur: spans.append(tuple(cur))
            cur = [tag[2:], tok]
        elif tag.startswith("I-") and cur and tag[2:] == cur[0]:
            cur[1] += " " + tok
        else:
            if cur: spans.append(tuple(cur)); cur = None
    if cur: spans.append(tuple(cur))
    return set(spans)

print(bio_spans(["Ali", "lives", "in", "Lahore"], ["B-PER", "O", "O", "B-LOC"]))
```

## Expected behaviour

- English macro-F1 around 0.7–0.9 on 60 synthetic items; Urdu typically lower on the same size.
- Negation examples flip label with bigrams in both languages, though Urdu needs a negation list that includes `نہ` and `مت`.
- Span F1 is lower than token accuracy by a wide margin — report both once to show why.
- At least one Urdu failure comes from orthographic variation (same word, two spellings) and one from an unseen inflected form.

## Testing

| Test | Expected |
| :--- | :--- |
| Script routing | Urdu text uses the Urdu tokeniser |
| Negation preserved | negation tokens survive preprocessing in both languages |
| Span decoding | `I-` after `O` does not create a span |
| Per-language reporting | separate tables, no pooled accuracy |
| Licence note | dataset provenance and licence stated in the report |

## Deliverables

| File | Contents |
| :--- | :--- |
| `bilingual_sentiment.py` | Pipelines, models, metrics |
| `ner.py` | Tagger and span scorer |
| `results.md` | Per-language tables, NER per type |
| `limitations.md` | Three Urdu failure modes with examples |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Bilingual rigour | 30% | separate pipelines and metrics, honest comparison | both run | Urdu bolted on |
| NER evaluation | 25% | span F1 per type, decoding tested | token F1 | none |
| Error analysis | 25% | three specific Urdu modes with examples | two generic | none |
| Claims | 20% | no unsupported model claims; provenance stated | mostly careful | overclaims |

## Extension challenges

1. Add a character n-gram model for Urdu and measure whether it reduces the orthographic failures.
2. Load a multilingual encoder (download required), evaluate on the same Urdu split, and report the gap and the cost.
3. Add Roman-Urdu text and show what breaks in tokenisation and normalisation.
4. Build a bilingual gazetteer union and measure the cross-language transfer for `LOC`.

## Reflection

1. Which number would you put in front of the telecoms manager, and what caveat must accompany it?
2. Your Urdu model has 30 training items. What is the honest description of its performance?
3. Which failure mode would you fix first, and what would it cost?

---

[Module home](../README.md) · [Lab 1](lab-08-01-text-preprocessing-and-feature-extraction.md) · [Lab 2](lab-08-02-news-and-document-classification.md)
