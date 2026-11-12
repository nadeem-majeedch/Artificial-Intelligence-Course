"""Text classification, sequence labelling and extractive QA for module M08.

Three supervised tasks and one structured task:
  * sentiment (bilingual, with and without Urdu normalisation)
  * news categorisation (five classes of synthetic news copy)
  * spam detection (imbalanced binary)
  * named-entity recognition (gazetteer baseline vs spaCy)
  * extractive question answering (TF-IDF retrieval plus span scoring)

Everything except the spaCy comparison runs with scikit-learn and the module's own
vectorisers. Splits are deterministic and stratified.
"""

from __future__ import annotations

from collections import Counter

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_recall_fscore_support)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

import text_data as td
from text_pipeline import (BagOfWords, TfidfVectorizer, ENGLISH_STOPWORDS, SPACY_READY,
                           normalise_text, stopword_set, tokenize)
if SPACY_READY:
    from text_pipeline import NLP


def _seed(seed: int = 0) -> np.random.Generator:
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# Naive Bayes from scratch (for the lesson, not for production)
# ---------------------------------------------------------------------------
class NaiveBayesText:
    """Multinomial naive Bayes with Laplace smoothing over a count matrix.

    log P(class | d) proportional to log P(class) + sum_t count(t, d) * log P(t | class)
    """

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha

    def fit(self, counts, labels):
        counts = np.asarray(counts, dtype=np.float64)
        labels = np.asarray(labels)
        self.classes_ = np.unique(labels)
        self.log_prior_ = np.log([np.mean(labels == c) for c in self.classes_])
        self.log_likelihood_ = np.zeros((len(self.classes_), counts.shape[1]))
        for row, c in enumerate(self.classes_):
            class_counts = counts[labels == c].sum(axis=0) + self.alpha
            self.log_likelihood_[row] = np.log(class_counts / class_counts.sum())
        return self

    def predict_log_proba(self, counts):
        scores = np.asarray(counts, dtype=np.float64) @ self.log_likelihood_.T + self.log_prior_
        scores -= scores.max(axis=1, keepdims=True)
        probabilities = np.exp(scores)
        return probabilities / probabilities.sum(axis=1, keepdims=True)

    def predict(self, counts):
        return self.classes_[np.argmax(self.predict_log_proba(counts), axis=1)]


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------
def summarise(y_true, y_pred, names=None) -> dict:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "confusion": confusion_matrix(y_true, y_pred).tolist(),
        "report": classification_report(y_true, y_pred, target_names=names, zero_division=0,
                                        digits=3),
    }


def top_features(model, feature_names, k: int = 8):
    """Most positive/negative coefficients per class for a linear model."""
    out = {}
    if not hasattr(model, "coef_"):
        return out
    for row, label in enumerate(getattr(model, "classes_", [])):
        weights = model.coef_[row] if model.coef_.shape[0] > 1 else model.coef_[0]
        order = np.argsort(weights)
        out[str(label)] = {
            "positive": [(feature_names[i], round(float(weights[i]), 3)) for i in order[::-1][:k]],
            "negative": [(feature_names[i], round(float(weights[i]), 3)) for i in order[:k]],
        }
    return out


def most_confused(y_true, y_pred, names=None, k: int = 3):
    matrix = confusion_matrix(y_true, y_pred)
    names = names or [str(i) for i in range(matrix.shape[0])]
    pairs = [(names[i], names[j], int(matrix[i, j]))
             for i in range(matrix.shape[0]) for j in range(matrix.shape[1]) if i != j]
    return sorted(pairs, key=lambda row: -row[2])[:k]


# ---------------------------------------------------------------------------
# 1. Sentiment, bilingual, with an Urdu normalisation ablation
# ---------------------------------------------------------------------------
def sentiment_experiment(n: int = 900, seed: int = 0, normalise_urdu: bool = True):
    """Train TF-IDF + logistic regression on English and Urdu rows together.

    Returns a dict with metrics plus the per-language breakdown, which is the number
    that matters: pooled accuracy hides a language that is failing.
    """
    texts, labels, langs = td.sentiment_corpus(n, seed=seed)
    if normalise_urdu:
        texts = [td.normalise_urdu(text) if lang == "ur" else text
                 for text, lang in zip(texts, langs)]

    indices = np.arange(len(texts))
    train_index, test_index = train_test_split(indices, test_size=0.3, random_state=seed,
                                               stratify=labels)
    vectoriser = TfidfVectorizer(language="en", ngram_range=(1, 2), min_df=2)
    X_train = vectoriser.fit_transform([texts[i] for i in train_index])
    X_test = vectoriser.transform([texts[i] for i in test_index])

    model = LogisticRegression(max_iter=1000, C=1.0).fit(X_train, labels[train_index])
    preds = model.predict(X_test)
    truth = labels[test_index]
    out = summarise(truth, preds, ["negative", "positive"])
    out["features"] = len(vectoriser.vocabulary_)
    out["majority_baseline"] = float(max(np.mean(truth), 1 - np.mean(truth)))

    test_langs = langs[test_index]
    out["by_language"] = {
        lang: float(accuracy_score(truth[test_langs == lang], preds[test_langs == lang]))
        for lang in ("en", "ur")
    }
    out["by_language_n"] = {lang: int((test_langs == lang).sum()) for lang in ("en", "ur")}
    return out


def sentiment_with_naive_bayes(n: int = 900, seed: int = 0):
    texts, labels, _ = td.sentiment_corpus(n, seed=seed)
    indices = np.arange(len(texts))
    train_index, test_index = train_test_split(indices, test_size=0.3, random_state=seed,
                                               stratify=labels)
    counts = BagOfWords(min_df=2, binary=False).fit([texts[i] for i in train_index])
    X_train = counts.transform([texts[i] for i in train_index])
    X_test = counts.transform([texts[i] for i in test_index])
    model = NaiveBayesText(alpha=1.0).fit(X_train, labels[train_index])
    return summarise(labels[test_index], model.predict(X_test))


# ---------------------------------------------------------------------------
# 2. News categorisation
# ---------------------------------------------------------------------------
def news_experiment(n: int = 750, seed: int = 0):
    docs, topics, labels = td.news_corpus(n, seed=seed)
    indices = np.arange(len(docs))
    train_index, test_index = train_test_split(indices, test_size=0.3, random_state=seed,
                                               stratify=labels)
    vectoriser = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=3000)
    X_train = vectoriser.fit_transform([docs[i] for i in train_index])
    X_test = vectoriser.transform([docs[i] for i in test_index])

    results = {}
    for name, model in [("naive_bayes", MultinomialNB(alpha=0.3)),
                        ("logreg", LogisticRegression(max_iter=1000)),
                        ("linear_svm", LinearSVC())]:
        model.fit(X_train, labels[train_index])
        preds = model.predict(X_test)
        results[name] = {
            "accuracy": float(accuracy_score(labels[test_index], preds)),
            "macro_f1": float(f1_score(labels[test_index], preds, average="macro")),
        }
        if name == "linear_svm":
            results["confused"] = most_confused(labels[test_index], preds, topics, 3)
            results["top_features"] = top_features(model, vectoriser.get_feature_names_out(), 5)
            results["report"] = classification_report(labels[test_index], preds,
                                                      target_names=topics, zero_division=0,
                                                      digits=3)
    results["features"] = len(vectoriser.vocabulary_)
    results["majority_baseline"] = float(max(np.bincount(labels[test_index])) / len(test_index))
    return results


# ---------------------------------------------------------------------------
# 3. Spam detection with class imbalance
# ---------------------------------------------------------------------------
def spam_experiment(n: int = 900, seed: int = 0, class_weight: str | None = None):
    messages, labels = td.spam_corpus(n, seed=seed)
    indices = np.arange(len(messages))
    train_index, test_index = train_test_split(indices, test_size=0.3, random_state=seed,
                                               stratify=labels)
    vectoriser = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_train = vectoriser.fit_transform([messages[i] for i in train_index])
    X_test = vectoriser.transform([messages[i] for i in test_index])

    model = LogisticRegression(max_iter=1000, class_weight=class_weight)
    model.fit(X_train, labels[train_index])
    preds = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels[test_index], preds, average=None, labels=[0, 1], zero_division=0)
    return {
        "accuracy": float(accuracy_score(labels[test_index], preds)),
        "precision_spam": float(precision[1]),
        "recall_spam": float(recall[1]),
        "f1_spam": float(f1[1]),
        "spam_rate": float(np.mean(labels[test_index])),
        "confused": most_confused(labels[test_index], preds, ["ham", "spam"], 2),
        "top_features": top_features(model, vectoriser.get_feature_names_out(), 6),
    }


# ---------------------------------------------------------------------------
# 4. Named-entity recognition: gazetteer vs spaCy
# ---------------------------------------------------------------------------
def ner_gazetteer(sentences, gazetteers=None):
    """Longest-match gazetteer lookup returning [(start, end, label)] per sentence."""
    gazetteers = gazetteers or {
        "PERSON": td.PEOPLE,
        "ORG": td.ORGS,
        "LOC": td.LOCS,
        "DATE": td.DATES,
    }
    found = []
    for sentence in sentences:
        spans = []
        for label, entries in gazetteers.items():
            for entry in entries:
                start = sentence.find(entry)
                while start >= 0:
                    spans.append((start, start + len(entry), label))
                    start = sentence.find(entry, start + 1)
        # Longest match wins, then earlier start, so nested entries do not double count.
        spans.sort(key=lambda span: (-(span[1] - span[0]), span[0]))
        kept = []
        for span in spans:
            if all(span[1] <= other[0] or span[0] >= other[1] for other in kept):
                kept.append(span)
        found.append(sorted(kept))
    return found


def ner_spacy(sentences):
    """spaCy's transformer-free English NER, mapped to the same four labels."""
    if not SPACY_READY:
        raise RuntimeError("spaCy model en_core_web_sm is not installed")
    mapping = {"PERSON": "PERSON", "ORG": "ORG", "GPE": "LOC", "LOC": "LOC", "DATE": "DATE"}
    found = []
    for sentence in sentences:
        doc = NLP(sentence)
        spans = []
        for entity in doc.ents:
            label = mapping.get(entity.label_)
            if label:
                spans.append((entity.start_char, entity.end_char, label))
        found.append(sorted(spans))
    return found


def score_spans(gold, predicted):
    """Exact-match precision, recall and F1 over (start, end, label) triples."""
    true_positive = sum(len(set(g) & set(p)) for g, p in zip(gold, predicted))
    total_gold = sum(len(g) for g in gold)
    total_predicted = sum(len(p) for p in predicted)
    precision = true_positive / total_predicted if total_predicted else 0.0
    recall = true_positive / total_gold if total_gold else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1,
            "gold": total_gold, "predicted": total_predicted, "correct": true_positive}


def ner_experiment(n: int = 300, seed: int = 0):
    sentences, spans = td.ner_corpus(n, seed=seed)
    gazetteer = ner_gazetteer(sentences)
    out = {"gazetteer": score_spans(spans, gazetteer)}
    if SPACY_READY:
        out["spacy"] = score_spans(spans, ner_spacy(sentences))
    return out


# ---------------------------------------------------------------------------
# 5. Extractive question answering
# ---------------------------------------------------------------------------
def _sentences(text):
    import re
    return [piece.strip() for piece in re.split(r"(?<=[.!?])\s+", text) if piece.strip()]


MONTHS = {"january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"}
NUMBER_WORDS = {"one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "hundred", "thousand"}


def _question_type(question: str) -> str:
    lowered = question.lower().strip()
    if lowered.startswith("when"):
        return "date"
    if lowered.startswith("how many") or lowered.startswith("how much"):
        return "number"
    if lowered.startswith("who"):
        return "person"
    if lowered.startswith("why"):
        return "reason"
    if lowered.startswith("which") or lowered.startswith("what"):
        return "thing"
    return "other"


def _strip_leading_article(span: str) -> str:
    for article in ("the ", "a ", "an "):
        if span.lower().startswith(article):
            return span[len(article):]
    return span


def _pattern_answer(sentence: str, kind: str) -> str | None:
    """Question-type patterns that a reading-comprehension model learns implicitly.

    'into X' answers a conversion question, 'to X' answers a purpose question, and the
    subject before the copula answers 'which/what'. On templated text these rules are
    strong; on natural text they are a fallback, not a solution.
    """
    import re

    if kind == "reason":
        match = re.search(r"\bto ([a-z][a-z ]{2,40}?)(?:[.,;]|$)", sentence)
        if match:
            return match.group(1).strip()
    if " into " in sentence.lower():
        tail = sentence.lower().split(" into ", 1)[1]
        tail = re.split(r" (?:in|on|at|for|with) |[.,;]", tail, maxsplit=1)[0]
        if tail.strip():
            return tail.strip()
    match = re.match(r"^(?:The |A |An )?(.+?)\s+(?:is|was|are|were)\s+", sentence)
    if match and kind in {"thing", "other"}:
        return match.group(1).strip()
    return None


def answer_question(context, question, max_span: int = 5):
    """Two-stage extractive QA: retrieve a sentence, then extract an answer span.

    Stage 1 uses TF-IDF cosine similarity between the question and each sentence.
    Stage 2 applies question-type patterns, then falls back to scoring every short
    span by inverse-document-frequency mass minus question overlap and length.
    """
    sentences = _sentences(context)
    corpus = sentences + [question]
    vectoriser = TfidfVectorizer()
    matrix = vectoriser.fit_transform(corpus)
    similarities = np.asarray(matrix[:-1] @ matrix[-1].T).ravel()
    best_sentence = sentences[int(np.argmax(similarities))]
    kind = _question_type(question)

    patterned = _pattern_answer(best_sentence, kind)
    if patterned:
        return {"sentence": best_sentence,
                "answer": _strip_leading_article(patterned).strip(" ,.;"),
                "similarity": float(np.max(similarities)), "method": "pattern"}

    names = list(vectoriser.get_feature_names_out())
    idf = dict(zip(names, vectoriser.idf_))
    question_terms = set(tokenize(normalise_text(question))) - ENGLISH_STOPWORDS
    tokens = best_sentence.split()

    def type_ok(span_tokens) -> bool:
        text = " ".join(span_tokens).lower()
        if kind == "date":
            return any(char.isdigit() for char in text) or any(m in text for m in MONTHS)
        if kind == "number":
            return any(char.isdigit() for char in text) or any(
                word in NUMBER_WORDS for word in text.split())
        if kind == "person":
            return any(token[:1].isupper() for token in span_tokens)
        return True

    candidates = []
    for start in range(len(tokens)):
        for end in range(start + 1, min(start + max_span, len(tokens)) + 1):
            span_tokens = tokens[start:end]
            content = [token for token in tokenize(normalise_text(" ".join(span_tokens)))
                       if token not in ENGLISH_STOPWORDS and token not in ".,;:"]
            if not content:
                continue
            score = sum(idf.get(token, 1.0) for token in content)
            score -= 2.0 * len(set(content) & question_terms) + 1.0 * len(span_tokens)
            candidates.append((score, type_ok(span_tokens),
                               " ".join(span_tokens).strip(" ,.;")))
    typed = [item for item in candidates if item[1]] or candidates
    best = max(typed, key=lambda item: item[0])
    return {"sentence": best_sentence, "answer": _strip_leading_article(best[2]),
            "similarity": float(np.max(similarities)), "method": "span"}


def qa_experiment(seed: int = 0):
    contexts, questions, answers = td.qa_corpus(seed=seed)
    results = [answer_question(c, q) for c, q in zip(contexts, questions)]
    predictions = [result["answer"] for result in results]
    exact = float(np.mean([p.strip().lower() == a.strip().lower()
                           for p, a in zip(predictions, answers)]))

    def token_f1(prediction, gold):
        pred_tokens = prediction.lower().split()
        gold_tokens = gold.lower().split()
        common = Counter(pred_tokens) & Counter(gold_tokens)
        overlap = sum(common.values())
        if not overlap:
            return 0.0
        precision = overlap / len(pred_tokens)
        recall = overlap / len(gold_tokens)
        return 2 * precision * recall / (precision + recall)

    return {
        "exact_match": exact,
        "token_f1": float(np.mean([token_f1(p, a) for p, a in zip(predictions, answers)])),
        "examples": list(zip(questions, answers, predictions)),
        "methods": Counter(result["method"] for result in results),
    }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== sentiment, bilingual TF-IDF + logistic regression ===")
    normalised = sentiment_experiment(900, seed=0, normalise_urdu=True)
    print("feature count:", normalised["features"],
          "| majority baseline:", round(normalised["majority_baseline"], 3))
    print("accuracy:", round(normalised["accuracy"], 3),
          "| macro F1:", round(normalised["macro_f1"], 3))
    print("by language:", {k: round(v, 3) for k, v in normalised["by_language"].items()},
          "n:", normalised["by_language_n"])

    raw = sentiment_experiment(900, seed=0, normalise_urdu=False)
    print("without Urdu normalisation: accuracy", round(raw["accuracy"], 3),
          "| urdu", round(raw["by_language"]["ur"], 3))

    nb = sentiment_with_naive_bayes(900, seed=0)
    print("naive Bayes accuracy:", round(nb["accuracy"], 3),
          "| macro F1:", round(nb["macro_f1"], 3))

    print()
    print("=== news categorisation ===")
    news = news_experiment(750, seed=0)
    print("features:", news["features"], "| majority:", round(news["majority_baseline"], 3))
    for name in ("naive_bayes", "logreg", "linear_svm"):
        print(f"{name:12s} accuracy {news[name]['accuracy']:.3f} macro F1 {news[name]['macro_f1']:.3f}")
    print("most confused:", news["confused"])

    print()
    print("=== spam detection ===")
    spam = spam_experiment(900, seed=0)
    print("accuracy:", round(spam["accuracy"], 3),
          "| spam precision:", round(spam["precision_spam"], 3),
          "| recall:", round(spam["recall_spam"], 3),
          "| f1:", round(spam["f1_spam"], 3))
    weighted = spam_experiment(900, seed=0, class_weight="balanced")
    print("with class_weight=balanced: precision", round(weighted["precision_spam"], 3),
          "recall", round(weighted["recall_spam"], 3), "f1", round(weighted["f1_spam"], 3))

    print()
    print("=== named-entity recognition ===")
    ner = ner_experiment(300, seed=0)
    for name, scores in ner.items():
        print(f"{name:10s} P {scores['precision']:.3f} R {scores['recall']:.3f} "
              f"F1 {scores['f1']:.3f} (gold {scores['gold']}, predicted {scores['predicted']})")

    print()
    print("=== extractive QA ===")
    qa = qa_experiment(seed=0)
    print("exact match:", round(qa["exact_match"], 3), "| token F1:", round(qa["token_f1"], 3))
    for question, gold, predicted in qa["examples"][:3]:
        print(f"  Q: {question}\n    gold: {gold!r} | predicted: {predicted!r}")
