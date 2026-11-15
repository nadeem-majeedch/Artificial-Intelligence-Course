# L08-02 — Preprocessing, Tokenization, Stemming and Lemmatization

| Module | M08 · Natural Language Processing |
| :--- | :--- |
| Level | 300 |
| Study time | 100 minutes |
| Prerequisites | [L08-01](L08-01-introduction-to-nlp-and-the-text-pipeline.md) |
| Code | [`code/text_pipeline.py`](../code/text_pipeline.py) · Notebook `nb-08-01` |
| Libraries | NLTK, spaCy (optional; the lesson's code runs without downloads) |

[← Previous: L08-01](L08-01-introduction-to-nlp-and-the-text-pipeline.md) · [Next: L08-03 BoW and TF-IDF →](L08-03-bag-of-words-ngrams-and-tfidf.md)

## 1. Learning Objectives

- **Implement** normalisation, sentence splitting and word tokenisation without a library, then with one.
- **Distinguish** stemming from lemmatization and say when the difference changes a result.
- **Apply** an Urdu-aware pipeline: Unicode normalisation, script-specific tokenisation, RTL handling.
- **Justify** each preprocessing step by naming what it gains and what it destroys.

## 2. Prerequisite Knowledge

The pipeline and its trade-offs — [L08-01](L08-01-introduction-to-nlp-and-the-text-pipeline.md).

## 3. Conceptual Explanation

### 3.1 Normalisation

Unicode is not a single encoding: the same Urdu letter can arrive as one code point or as a base plus a
combining mark. Apply **NFKC** (compatibility composition) as a baseline, then decide about:

- Arabic-script variants: `ي` vs `ی`, `ك` vs `ک`, and the optional `ہ`/`ه`;
- diacritics (harakat) — usually removed for Urdu, but they disambiguate;
- zero-width joiners — meaningful in Urdu typography, invisible in most editors.

Every step is a modelling decision. Log it in a `preprocess` function so the decision is testable.

### 3.2 Tokenisation

English word tokenisation is "split on whitespace plus handle punctuation". Urdu adds:

| Problem | Example | Consequence |
| :--- | :--- | :--- |
| No case | `اردو` | case-based rules unavailable |
| Agglutination | `کتابوں` (books) | vocabulary explosion, stemming matters |
| Postpositions as separate words | `گھر میں` | multi-word units |
| Arabic-script punctuation | `۔` (full stop) | sentence splitters trained on `.` fail |
| RTL ordering with numbers | `31°C` inside Urdu text | display and regex both surprise |
| Mixed script | `WiFi کی سہولت` | one tokeniser per script, or a mixed rule |

### 3.3 Stemming versus lemmatization

- **Stemming** chops affixes with rules: `studies → studi`, `studying → studi`. Fast, language-specific,
  produces non-words.
- **Lemmatization** returns a dictionary form using morphology: `studies → study`, `was → be`. Slower,
  needs a lexicon or POS tags.

They differ where it matters: `better → better` (stem) versus `better → good` (lemma). For Urdu,
stemming is harder because affixes are more productive and orthography is less standardised; published
Urdu stemmers exist but their coverage should be measured on your corpus, not assumed.

### 3.4 What a library gives you, and what it costs

`nltk` and `spaCy` ship tokenisers and lemmatisers, but their pretrained models are **downloads** and
their Urdu support is thinner than their English support. This module's code therefore implements the
baseline in pure Python, so nothing depends on a download, and shows the library call as an option.

## 4. Pseudocode

```text
function PREPROCESS(text, script):
    text  <- NFKC(text)
    text  <- unify_script_variants(text)      # e.g. Arabic yeh -> Urdu yeh
    text  <- strip_diacritics(text)           # optional, log the choice
    sents <- split_sentences(text, script_punctuation)
    toks  <- tokenise(sents, script)
    return toks
```

## 5. Worked Example — the same sentence in both scripts

English: `"The students are studying NLP, aren't they?"`

| Step | Output |
| :--- | :--- |
| tokens | `the, students, are, studying, nlp, aren't, they` |
| stem (Porter) | `the, student, are, studi, nlp, aren't, they` |
| lemma (spaCy) | `the, student, be, study, nlp, aren't, they` |

Urdu: `"طلبہ نیچرل لینگویج پروسیسنگ پڑھ رہے ہیں۔"` ("Students are studying natural language processing.")

| Step | Output |
| :--- | :--- |
| NFKC + variant unification | unchanged here, but `ي`→`ی`, `ك`→`ک` applied generally |
| sentence split on `۔` | one sentence |
| tokens | `طلبہ, نیچرل, لینگویج, پروسیسنگ, پڑھ, رہے, ہیں` |
| stem (light suffix strip `وں`, `یں`, `ہیں`) | `طلبہ, نیچرل, لینگویج, پروسیسنگ, پڑھ, رہے, ہی` |

Note what the light stemmer did to `ہیں` → `ہی` — wrong. This is the honest state of rule-based Urdu
stemming: it needs a lexicon of exceptions before it is usable, and you should measure it.

## 6. Mathematical Formulation

A tokeniser is a segmentation of a character string into spans $[i_k, j_k)$ maximising a score, often
implemented as a decision at each boundary. Rule-based tokenisers are deterministic functions; learned
tokenisers (BPE, L08-06) maximise

$$\sum_{k} \log P(\text{token}_k) \quad \text{subject to } \bigcup_k \text{token}_k = \text{text}$$

Vocabulary size $|V|$ and average token length trade off against sequence length: shorter tokens mean
longer sequences and more compute.

## 7. Python Implementation

```python
import re
import unicodedata

ARABIC_VARIANTS = {"ي": "ی", "ك": "ک", "ۀ": "ہ"}
DIACRITICS = re.compile(r"[\u064B-\u0652]")          # harakat
URDU_SENTENCE_END = re.compile(r"[۔?!]")


def normalise_urdu(text):
    text = unicodedata.normalize("NFKC", text)
    for src, dst in ARABIC_VARIANTS.items():
        text = text.replace(src, dst)
    return DIACRITICS.sub("", text)


def tokenise(text, script="latin"):
    text = normalise_urdu(text) if script == "urdu" else text
    if script == "urdu":
        # Urdu: keep the Arabic-script block plus Latin words in mixed text
        return re.findall(r"[\u0600-\u06FF]+|[A-Za-z]+|\d+(?:\.\d+)?", text)
    return re.findall(r"[A-Za-z]+(?:'[a-z]+)?|\d+(?:\.\d+)?", text.lower())


def split_sentences(text, script="latin"):
    pattern = URDU_SENTENCE_END if script == "urdu" else re.compile(r"[.!?]")
    return [s.strip() for s in pattern.split(text) if s.strip()]


en = "The students are studying NLP, aren't they?"
ur = "طلبہ نیچرل لینگویج پروسیسنگ پڑھ رہے ہیں۔ وہ کلاس میں ہیں۔"
print(tokenise(en))
print(tokenise(ur, "urdu"))
print(split_sentences(ur, "urdu"))
```

```text
['the', 'students', 'are', 'studying', 'nlp', "aren't", 'they']
['طلبہ', 'نیچرل', 'لینگویج', 'پروسیسنگ', 'پڑھ', 'رہے', 'ہیں', 'وہ', 'کلاس', 'میں', 'ہیں']
['طلبہ نیچرل لینگویج پروسیسنگ پڑھ رہے ہیں', 'وہ کلاس میں ہیں']
```

Optional library equivalents (require a one-time model download, so they are not used in the module's
executed notebooks):

```python
# import nltk; nltk.download("punkt")            # English tokeniser
# import spacy; nlp = spacy.load("en_core_web_sm")  # English lemma + POS
# Urdu: no official spaCy pipeline is bundled; check what is actually installed
# before claiming Urdu support.
```

## 8. Practical Applications

- **Support desks** — separate pipelines per language, evaluated separately.
- **Search** — stemming increases recall, harms precision on names and codes.
- **Compliance** — diacritic removal can change a legal meaning; log it.
- **Mixed-script input** — `WiFi کی سہولت` needs a tokeniser that keeps both scripts.

## 9. Common Mistakes

- Applying an English tokeniser to Urdu text: `۔` is not a sentence boundary to it, so the whole
  paragraph becomes one sentence.
- Claiming a library "supports Urdu" without checking that a model is installed and measured.
- Stripping diacritics and then asking why homographs are confused.
- Using a stemmer and a lemmatizer in the same pipeline, so both vocabularies coexist.
- Lowercasing codes and identifiers (`A-12` → `a-12`), then failing to match records.

## 10. Exercises

1. Extend `ARABIC_VARIANTS` with two more equivalences and show which tokens merge in a sample.
2. Write a light Urdu suffix stripper for `وں`, `یں`, `ات`; find three wrong stems.
3. Compare word counts for the same Urdu paragraph before and after normalisation.
4. Take a mixed-script string and show what your tokeniser returns; state the rule you would add.

## 11. Self-Assessment

1. Why is NFKC a baseline rather than a complete normalisation?
2. Give two Urdu tokenisation problems an English tokeniser cannot handle.
3. When does lemmatization beat stemming, and at what cost?
4. What must you verify before claiming Urdu support in a model?

## 12. Key Terms

**NFKC**, **diacritic**, **harakat**, **agglutination**, **stemming**, **lemmatization**, **sentence segmentation**, **mixed script**, **RTL**.

## 13. Further Reading

- Unicode Standard Annex #15 (normalisation forms).
- Jurafsky & Martin, chapter 2; for Urdu, the CLE Urdu Digest corpora documentation.

## What to Do Next

[L08-03](L08-03-bag-of-words-ngrams-and-tfidf.md) turns tokens into features.
