"""Classical NLP pipeline: segmentation, tokenisation, normalisation, stemming,
lemmatisation, bag-of-words, n-grams and TF-IDF — all implemented explicitly.

NLTK and spaCy are used where they are genuinely the right tool (Porter stemmer,
WordNet lemmas, spaCy's tokeniser and lemmatiser). Everything that a learner should be
able to reproduce by hand (BoW, n-grams, TF-IDF) is implemented here in NumPy so the
formulas in L08-01 and L08-02 match the code exactly.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

import numpy as np

from text_data import URDU_STOPWORDS, normalise_urdu, urdu_tokenize

# ---------------------------------------------------------------------------
# Optional backends — each degrades gracefully with a clear message
# ---------------------------------------------------------------------------
try:
    import nltk
    from nltk.corpus import stopwords as nltk_stopwords
    from nltk.corpus import wordnet
    from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
    from nltk.tokenize import sent_tokenize as nltk_sent_tokenize
    from nltk.tokenize import word_tokenize as nltk_word_tokenize
    ENGLISH_STOPWORDS = set(nltk_stopwords.words("english"))
    NLTK_READY = True
except Exception:  # pragma: no cover - only when corpora are absent
    ENGLISH_STOPWORDS = set("""a an the and or but if while of to in on at by for with
        from as is are was were be been being it its this that these those he she they
        we you i not no do does did have has had will would can could should""".split())
    NLTK_READY = False

try:
    import spacy
    NLP = spacy.load("en_core_web_sm")
    SPACY_READY = True
except Exception:  # pragma: no cover
    NLP = None
    SPACY_READY = False

try:
    from tokenizers import Tokenizer, models, pre_tokenizers, trainers, normalizers
    TOKENIZERS_READY = True
except Exception:  # pragma: no cover
    TOKENIZERS_READY = False


# ---------------------------------------------------------------------------
# 1. Sentence segmentation
# ---------------------------------------------------------------------------
ABBREVIATIONS = {"mr", "mrs", "dr", "prof", "e.g", "i.e", "vs", "etc", "no", "st"}


def sentence_split(text: str, language: str = "en") -> list[str]:
    """Split on sentence-final punctuation, without breaking common abbreviations.

    Urdu uses its own full stop (\u06d4), so the pattern accepts both. A real system
    would use a trained segmenter; the rule-based version is transparent and is what
    most pipelines fall back to.
    """
    if language == "ur":
        pieces = re.split(r"(?<=[\u06d4?!])\s+", text.strip())
        return [piece.strip() for piece in pieces if piece.strip()]

    protected = text
    for abbr in ABBREVIATIONS:
        # Keep the original capitalisation; only the full stop is hidden from the splitter.
        protected = re.sub(rf"(?i)\b{re.escape(abbr)}\.",
                           lambda match: match.group(0)[:-1] + "<DOT>", protected)
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", protected)
    return [piece.replace("<DOT>", ".").strip() for piece in pieces if piece.strip()]


def sentences_nltk(text: str) -> list[str]:
    """NLTK Punkt segmentation, for comparison with the rule-based splitter."""
    if not NLTK_READY:
        raise RuntimeError("NLTK corpora are not installed; run nltk.download('punkt_tab')")
    return nltk_sent_tokenize(text)


# ---------------------------------------------------------------------------
# 2. Tokenisation
# ---------------------------------------------------------------------------
TOKEN_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?|[^\sA-Za-z\d]")


def tokenize(text: str, language: str = "en") -> list[str]:
    """Language-aware tokeniser: Urdu uses the script-aware splitter from text_data."""
    if language == "ur":
        return urdu_tokenize(text)
    return TOKEN_PATTERN.findall(text)


def tokenize_nltk(text: str) -> list[str]:
    if not NLTK_READY:
        raise RuntimeError("NLTK corpora are not installed")
    return nltk_word_tokenize(text)


def tokenize_spacy(text: str) -> list[tuple[str, str, bool]]:
    """Return (token, lemma, is_stop) triples from spaCy's pipeline."""
    if not SPACY_READY:
        raise RuntimeError("spaCy model en_core_web_sm is not installed")
    doc = NLP(text)
    return [(token.text, token.lemma_, token.is_stop) for token in doc]


# ---------------------------------------------------------------------------
# 3. Normalisation, stopwords, stemming, lemmatisation
# ---------------------------------------------------------------------------
def normalise_text(text: str, language: str = "en", lowercase: bool = True) -> str:
    """Canonical text form: unicode NFC, whitespace collapsed, optional case folding."""
    import unicodedata

    text = unicodedata.normalize("NFC", text)
    if language == "ur":
        text = normalise_urdu(text)
    if lowercase:
        text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def stopword_set(language: str = "en") -> set[str]:
    return URDU_STOPWORDS if language == "ur" else ENGLISH_STOPWORDS


def remove_stopwords(tokens, language: str = "en") -> list[str]:
    stops = stopword_set(language)
    return [token for token in tokens if token.lower() not in stops]


PORTER = PorterStemmer() if NLTK_READY else None


def stem(tokens) -> list[str]:
    """Porter stemming: suffix stripping, no dictionary required.

    'studies', 'studied' and 'study' all reduce to 'studi'. Fast and language-agnostic
    to implement, but it produces non-words.
    """
    if PORTER is None:
        raise RuntimeError("NLTK is required for the Porter stemmer")
    return [PORTER.stem(token) for token in tokens]


def lemmatize(tokens, language: str = "en") -> list[str]:
    """WordNet lemmatisation with the noun and verb lexicons.

    Lemmas are real words ('studies' -> 'study'), which matters when the output is
    shown to a human or used as a feature name. It needs a dictionary and part of
    speech, so it is slower than stemming and unavailable for Urdu without a lexicon.
    """
    if language == "ur":
        raise ValueError("WordNet covers English; Urdu lemmatisation needs an Urdu lexicon")
    if not NLTK_READY:
        raise RuntimeError("NLTK WordNet is required for lemmatisation")
    lemmatizer = WordNetLemmatizer()
    out = []
    for token in tokens:
        noun = wordnet.synsets(token, pos=wordnet.NOUN)
        verb = wordnet.synsets(token, pos=wordnet.VERB)
        pos = wordnet.NOUN if noun else (wordnet.VERB if verb else wordnet.NOUN)
        out.append(lemmatizer.lemmatize(token, pos=pos))
    return out


# ---------------------------------------------------------------------------
# 4. Bag of words and n-grams
# ---------------------------------------------------------------------------
def ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    if n < 1:
        raise ValueError("n must be >= 1")
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


class BagOfWords:
    """Count vectoriser: vocabulary from the training texts only.

    Parameters
    ----------
    min_df : int
        Ignore terms appearing in fewer documents (a cheap way to drop typos).
    max_features : int, optional
        Keep the most frequent terms only.
    ngram_range : tuple[int, int]
        Inclusive range of n-gram sizes to include.
    binary : bool
        Count presence instead of frequency.
    """

    def __init__(self, min_df: int = 1, max_features: int | None = None,
                 ngram_range: tuple[int, int] = (1, 1), binary: bool = False,
                 language: str = "en", lowercase: bool = True):
        self.min_df = min_df
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.binary = binary
        self.language = language
        self.lowercase = lowercase
        self.vocabulary_: dict[str, int] = {}

    def _terms(self, text: str) -> list[str]:
        tokens = tokenize(normalise_text(text, self.language, self.lowercase), self.language)
        low, high = self.ngram_range
        terms = []
        for n in range(low, high + 1):
            terms.extend(" ".join(gram) for gram in ngrams(tokens, n))
        return terms

    def fit(self, texts):
        document_frequency = Counter()
        for text in texts:
            document_frequency.update(set(self._terms(text)))
        items = [(term, df) for term, df in document_frequency.items() if df >= self.min_df]
        items.sort(key=lambda pair: (-pair[1], pair[0]))
        if self.max_features is not None:
            items = items[: self.max_features]
        self.vocabulary_ = {term: index for index, (term, _) in enumerate(items)}
        return self

    def transform(self, texts):
        matrix = np.zeros((len(texts), len(self.vocabulary_)), dtype=np.float32)
        for row, text in enumerate(texts):
            for term, count in Counter(self._terms(text)).items():
                column = self.vocabulary_.get(term)
                if column is not None:
                    matrix[row, column] = 1.0 if self.binary else count
        return matrix

    def fit_transform(self, texts):
        return self.fit(texts).transform(texts)

    def get_feature_names_out(self) -> np.ndarray:
        return np.array([term for term, _ in sorted(self.vocabulary_.items(), key=lambda kv: kv[1])])


# ---------------------------------------------------------------------------
# 5. TF-IDF
# ---------------------------------------------------------------------------
class TfidfVectorizer(BagOfWords):
    """TF-IDF with smoothed idf and L2 normalisation.

    idf(t) = log((1 + n) / (1 + df(t))) + 1
    tf-idf  = tf(t, d) * idf(t), then each row is scaled to unit L2 norm.
    The +1 in both places keeps terms that appear in every document at a small but
    non-zero weight, which avoids zero rows.
    """

    def __init__(self, sublinear_tf: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.sublinear_tf = sublinear_tf
        self.idf_: np.ndarray | None = None

    def fit(self, texts):
        super().fit(texts)
        counts = super().transform(texts)
        document_frequency = (counts > 0).sum(axis=0)
        n_documents = len(texts)
        self.idf_ = np.log((1 + n_documents) / (1 + document_frequency)) + 1.0
        return self

    def transform(self, texts):
        counts = super().transform(texts)
        tf = counts.astype(np.float64)
        if self.sublinear_tf:
            tf = np.where(tf > 0, 1.0 + np.log(np.where(tf > 0, tf, 1.0)), 0.0)
        weighted = tf * self.idf_
        norms = np.linalg.norm(weighted, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return (weighted / norms).astype(np.float32)

    def fit_transform(self, texts):
        return self.fit(texts).transform(texts)


# ---------------------------------------------------------------------------
# 6. Subword tokenisation (WordPiece trained locally, no download)
# ---------------------------------------------------------------------------
def train_wordpiece(corpus, vocab_size: int = 300, show_progress: bool = False):
    """Train a WordPiece model on a corpus with the `tokenizers` library.

    WordPiece is the algorithm behind BERT's tokeniser: frequent character sequences
    become tokens, and any unseen word is split into known pieces plus '##' continuations.
    Training locally means the lesson runs offline and on Urdu text too.
    """
    if not TOKENIZERS_READY:
        raise RuntimeError("pip install tokenizers to train a WordPiece model")
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
    tokenizer.normalizer = normalizers.NFC()
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.WordPieceTrainer(
        vocab_size=vocab_size,
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
        show_progress=show_progress,
    )
    tokenizer.train_from_iterator(corpus, trainer=trainer)
    return tokenizer


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    text = ("Dr. Smith arrived at 9 a.m. He said the results were good. "
            "The model studies language; it does not study images!")

    print("backends: nltk", NLTK_READY, "spacy", SPACY_READY, "tokenizers", TOKENIZERS_READY)
    print("rule sentences:", sentence_split(text))
    if NLTK_READY:
        print("nltk sentences:", sentences_nltk(text))

    tokens = tokenize(normalise_text(text))
    print("tokens:", len(tokens), tokens[:8])
    if NLTK_READY:
        print("stems:", stem(tokens[:8]))
        print("lemmas:", lemmatize(tokens[:8]))
    if SPACY_READY:
        triples = tokenize_spacy("The models studied language quickly.")
        print("spacy (token, lemma, stop):", triples[:4])

    urdu = "\u064a\u06c1 \u06a9\u062a\u0627\u0628 \u0628\u06c1\u062a \u0627\u0686\u06be\u06cc \u06c1\u06d2\u06d4 \u06a9\u06cc\u0627 \u0622\u067e \u0646\u06d2 \u067e\u0691\u06be\u06cc\u061f"
    print("urdu tokens:", len(urdu_tokenize(urdu)))
    print("urdu after stopwords:", len(remove_stopwords(urdu_tokenize(urdu), "ur")))

    docs = ["the film was good and the acting was good",
            "the film was bad but the acting was good",
            "a good film with good acting"]

    bow = BagOfWords(ngram_range=(1, 1)).fit(docs)
    print("bow vocab size:", len(bow.vocabulary_), "matrix:", bow.transform(docs).shape)
    bigram = BagOfWords(ngram_range=(1, 2)).fit(docs)
    print("bow+bigram vocab size:", len(bigram.vocabulary_))

    tfidf = TfidfVectorizer().fit(docs)
    first = tfidf.transform(docs)[0]
    top = np.argsort(first)[::-1][:3]
    names = tfidf.get_feature_names_out()
    print("top tfidf terms doc0:", [(names[i], round(float(first[i]), 3)) for i in top])

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer as SkTfidf
        sk_vectoriser = SkTfidf(norm="l2", smooth_idf=True, token_pattern=r"(?u)\b\w+\b")
        sk = sk_vectoriser.fit_transform(docs).toarray()
        sk_names = list(sk_vectoriser.get_feature_names_out())
        ours = tfidf.transform(docs)
        ours_names = list(tfidf.get_feature_names_out())
        shared = sorted(set(sk_names) & set(ours_names))
        sk_cols = [sk_names.index(term) for term in shared]
        our_cols = [ours_names.index(term) for term in shared]
        print("shared terms:", len(shared), "of", len(ours_names),
              "| max abs difference:", round(float(np.abs(sk[:, sk_cols] - ours[:, our_cols]).max()), 12))
    except Exception as error:  # pragma: no cover
        print("sklearn comparison skipped:", error)

    if TOKENIZERS_READY:
        from text_data import embedding_corpus
        tokenizer = train_wordpiece(embedding_corpus(300, seed=0), vocab_size=200)
        encoded = tokenizer.encode("the tea is hot and the bread is fresh")
        print("wordpiece tokens:", encoded.tokens[:12])
        print("wordpiece vocab:", tokenizer.get_vocab_size())
