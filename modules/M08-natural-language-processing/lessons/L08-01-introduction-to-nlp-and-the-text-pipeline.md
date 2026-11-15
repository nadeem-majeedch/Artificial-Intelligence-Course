# L08-01 — Introduction to NLP and the Text Pipeline

| Module | M08 · Natural Language Processing |
| :--- | :--- |
| Level | 300 |
| Study time | 75 minutes |
| Prerequisites | [LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md) · [L08-02](L08-02-preprocessing-tokenization-stemming-lemmatization.md) next |
| Code | [`code/text_data.py`](../code/text_data.py), [`code/text_pipeline.py`](../code/text_pipeline.py) |

[← Module start](../README.md) · [Next: L08-02 Preprocessing →](L08-02-preprocessing-tokenization-stemming-lemmatization.md)

## 1. Learning Objectives

- **Describe** the stages a string passes through to become a model input, and name what each stage can destroy.
- **Explain** why "NLP" is not one task but a family, using at least four task types.
- **Identify** the unit of prediction (document, sentence, token, span) in a described problem.
- **Choose** an evaluation metric that matches the unit of prediction.

## 2. Prerequisite Knowledge

Python functions, loops, dictionaries and files —
[LP01-04](../../../prerequisites/P01-python-programming/lessons/LP01-04-functions-and-collections.md).

## 3. Conceptual Explanation

### 3.1 The pipeline

```text
raw text → normalisation → segmentation → tokenisation → features → model → prediction → evaluation
```

Each arrow is a decision with a cost. Lowercasing makes "Apple" and "apple" the same token and
destroys the company. Removing stopwords speeds training and deletes negation ("not good"). The
pipeline is where most real NLP errors are born, and they are invisible in aggregate accuracy.

### 3.2 The task families

| Task | Unit of prediction | Example metric |
| :--- | :--- | :--- |
| Classification | document | accuracy, macro-F1 |
| Sentiment | document or sentence | macro-F1 per class |
| Sequence labelling (POS, NER) | token | span-level F1 |
| Language modelling | next token | perplexity |
| Translation / summarisation | sequence | BLEU, ROUGE, human rating |
| Retrieval / QA | document or span | recall@k, exact match |

Mixing units across tasks is the most common evaluation mistake: token-level accuracy for NER looks
excellent because most tokens are "not an entity".

### 3.3 Why language is hard for computers

Ambiguity, compositionality, long-range dependencies, and — in Urdu and other morphologically rich
languages — a word boundary that does not correspond to a space and a vocabulary that grows fast.
L08-02 handles the script-level problems; L08-06 shows what attention does about the rest.

## 4. Pseudocode

```text
function PIPELINE(text):
    text  <- normalise(text)          # unicode, case, digits -- log every choice
    units <- segment(text)            # sentences or documents
    tokens <- tokenise(units)         # words, subwords, characters
    feats <- vectorise(tokens)        # counts, TF-IDF, embeddings
    return model.predict(feats)
```

## 5. Worked Example — one sentence, three pipelines

Input: `"The fan is NOT working, temperature 31°C!"`

| Pipeline | Tokens | What is kept | What is lost |
| :--- | :--- | :--- | :--- |
| Minimal (split on space) | 7 tokens incl. punctuation | punctuation, negation | "31°C" glued to "!" |
| Standard | lowercase, strip punctuation, keep negation word | `the, fan, is, not, working, temperature, 31c` | case, punctuation intensity |
| Aggressive | plus stopword removal | `fan, working, temperature, 31c` | **negation** — the label flips |

The third pipeline classifies the complaint as neutral. This is not a hypothetical: stopword lists
built for English contain negation words, and using them on sentiment data is a classic self-inflicted
bug.

## 6. Mathematical Formulation

A model is a function $f: \mathcal{V}^n \to \mathcal{Y}$ over a vocabulary $\mathcal{V}$. Its training
objective is empirical risk minimisation:

$$\hat{\theta} = \arg\min_{\theta} \frac{1}{N}\sum_{i=1}^{N} \ell\left(f_\theta(x_i), y_i\right) + \lambda\|\theta\|^2$$

with $\ell$ chosen for the unit of prediction — cross-entropy for classification, token-level
cross-entropy for labelling, and span-level decoding for NER.

## 7. Python Implementation

```python
import re
import unicodedata

NEGATIONS = {"not", "no", "never", "n't"}


def normalise(text):
    text = unicodedata.normalize("NFKC", text)      # unify look-alike characters
    return text.strip()


def tokenise(text):
    """Lowercase word tokens that keep negation words and numbers."""
    return re.findall(r"[a-z]+|\d+(?:\.\d+)?", normalise(text).lower())


def stopword_free(tokens, stopwords={"the", "is", "a", "of"}):
    return [t for t in tokens if t not in stopwords]


sentence = "The fan is NOT working, temperature 31°C!"
tokens = tokenise(sentence)
print(tokens)
print(stopword_free(tokens), "| negation preserved:", "not" in stopword_free(tokens))
```

```text
['the', 'fan', 'is', 'not', 'working', 'temperature', '31']
['fan', 'not', 'working', 'temperature', '31'] | negation preserved: True
```

## 8. Practical Applications

- **Complaint triage** — classify and route before a human reads it.
- **Search and retrieval** — the pipeline decides what "matching" means.
- **Healthcare coding** — span extraction where a missed negation is a clinical error.
- **Urdu/English support desks** — one pipeline per script, evaluated separately.

## 9. Common Mistakes

- Removing stopwords before sentiment or negation-sensitive tasks.
- Reporting token-level accuracy for a span task.
- Normalising digits ("31" → `<NUM>") and then trying to extract quantities.
- Training on one domain and evaluating on another without saying so.
- Treating an F1 of 0.9 on a 90%-negative dataset as success.

## 10. Exercises

1. Write the three pipelines in §5 and show which one flips the sentiment label on a second example you invent.
2. Take a task from the table, state its unit of prediction, and choose a metric; justify both.
3. Find a tokenisation decision that changes a downstream count in your own text data.
4. List every normalisation step your pipeline performs and what each could destroy.

## 11. Self-Assessment

1. Name four task families and their units of prediction.
2. Why can stopword removal be harmful?
3. What does a pipeline lose when it lowercases?
4. Why is token-level NER accuracy a misleading metric?

## 12. Key Terms

**Normalisation**, **segmentation**, **tokenisation**, **stopword**, **unit of prediction**, **macro-F1**, **span-level F1**, **perplexity**.

## 13. Further Reading

- Jurafsky & Martin, *Speech and Language Processing*, chapter 2.
- Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, chapter 2.

## What to Do Next

[L08-02](L08-02-preprocessing-tokenization-stemming-lemmatization.md) makes each pipeline stage
concrete, including the Urdu script problems.
