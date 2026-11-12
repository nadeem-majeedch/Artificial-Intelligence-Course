"""Seeded, offline text corpora for module M08 (NLP).

Every dataset here is synthetic and generated in-script, so the lessons, notebooks and
labs reproduce without downloads. Each mirrors the schema of a named public corpus so
the real file can be substituted; licences for those real corpora are documented in the
module README and in each lab.

The module also ships a small but real Urdu preprocessing layer: normalisation of
Arabic-script variants, an Urdu stopword list and a tokeniser that understands Urdu
punctuation. Urdu is written right-to-left and the course console is not, so all printed
examples are kept to counts, tags or ASCII-safe output.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

import numpy as np

# ---------------------------------------------------------------------------
# Urdu preprocessing
# ---------------------------------------------------------------------------

#: Characters that look alike in Arabic script but are distinct code points.
URDU_NORMALISATION = {
    "\u064a": "\u06cc",  # ARABIC YEH -> FARSI YEH
    "\u0649": "\u06cc",  # ALEF MAKSURA -> FARSI YEH
    "\u0643": "\u06a9",  # ARABIC KAF -> KEHEH
    "\u0629": "\u06c1",  # TEH MARBUTA -> HEH GOAL (loanwords)
    "\u06c3": "\u06c1",
    "\u200c": "",        # zero-width non-joiner: remove so tokens join predictably
    "\u200d": "",
    "\ufeff": "",
}

DIACRITICS = re.compile(r"[\u064b-\u065f\u0670]")
TATWEEL = "\u0640"

URDU_STOPWORDS = set("""
اور یا لیکن مگر کی کا کے کو میں نے ہے ہیں تھا تھے تھی ہو گا گی گے
سے پر تک بھی تو ہی نہ نہیں جو جس جن یہ وہ اس ان کہ اگر تو بھی
ایک دو تین بہت کچھ سب کوئی کسی اپنے اپنی اپنا ہم آپ تم وہ
کیا کیوں کیسے کب کہاں جب تب اب پھر بھی صرف زیادہ کم
""".split())

URDU_PUNCTUATION = "۔،؟!؛:«»\"'()[]{}—–"


def normalise_urdu(text: str) -> str:
    """Apply the character-level normalisations that Urdu NLP pipelines rely on.

    Removes Arabic diacritics and tatweel, unifies look-alike letters, and strips the
    zero-width joiners that make otherwise identical words compare unequal.
    """
    text = unicodedata.normalize("NFC", text)
    text = DIACRITICS.sub("", text)
    text = text.replace(TATWEEL, "")
    for source, target in URDU_NORMALISATION.items():
        text = text.replace(source, target)
    return re.sub(r"\s+", " ", text).strip()


def urdu_tokenize(text: str) -> list[str]:
    """Whitespace + Urdu/Latin punctuation tokeniser.

    Urdu has no case and no apostrophe clitics, so a punctuation-aware split is a
    reasonable baseline. Real pipelines use a trained segmenter; see L08-01.
    """
    text = normalise_urdu(text)
    text = re.sub(r"([%s])" % re.escape(URDU_PUNCTUATION), r" \1 ", text)
    return [token for token in text.split() if token]


def urdu_word_counts(texts) -> Counter:
    counts = Counter()
    for text in texts:
        counts.update(urdu_tokenize(text))
    return counts


# ---------------------------------------------------------------------------
# Lexicons (synthetic, deliberately small and inspectable)
# ---------------------------------------------------------------------------
EN_POSITIVE = ["good", "great", "excellent", "brilliant", "love", "enjoyed", "best",
               "wonderful", "helpful", "fast", "reliable", "recommend"]
EN_NEGATIVE = ["bad", "awful", "boring", "hate", "terrible", "worst", "disappointing",
               "dull", "slow", "broken", "useless", "refund"]
EN_NEUTRAL = ["the", "a", "film", "product", "service", "was", "is", "and", "with",
              "some", "very", "really", "but", "not", "delivery", "staff", "price"]

UR_POSITIVE = ["اچھا", "زبردست", "بہترین", "پسند", "خوبصورت", "مددگار", "تیز",
               "قابلِ اعتماد", "سفارش", "عمدہ", "مزیدار", "آسان"]
UR_NEGATIVE = ["برا", "بیکار", "خراب", "نفرت", "مایوس", "سست", "ٹوٹا", "بے کار",
               "واپسی", "مشکل", "غیر معیاری", "دیر"]
UR_NEUTRAL = ["فلم", "پروڈکٹ", "سروس", "تھا", "تھی", "ہے", "اور", "کے", "ساتھ",
              "کچھ", "بہت", "لیکن", "نہیں", "دکان", "قیمت"]


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# 1. Bilingual sentiment (stands in for IMDB and Urdu review corpora)
# ---------------------------------------------------------------------------
def _urdu_variant(rng, text: str) -> str:
    """Introduce the character variants real Urdu text contains.

    Arabic yeh and kaf, plus optional diacritics, appear in user-generated Urdu and
    make two spellings of the same word compare unequal unless normalised first.
    """
    if rng.random() < 0.5:
        text = text.replace("\u06cc", "\u064a")
    if rng.random() < 0.5:
        text = text.replace("\u06a9", "\u0643")
    if rng.random() < 0.4:
        text = text.replace("\u06c1", "\u06c1\u064e")
    return text


def sentiment_corpus(n: int = 900, seed: int = 0, messy_urdu: bool = True):
    """Return (texts, labels, languages) with label 1 = positive.

    English rows are 6-12 tokens with one to three polar words; Urdu rows are built
    from the same pattern using Urdu lexicons. A tie in polar counts is labelled 0,
    which produces the genuinely ambiguous rows the error analysis must find.
    With `messy_urdu`, Urdu rows use the Arabic-script variants that real corpora
    contain, so the normalisation ablation in L08-06 has something to measure.
    """
    rng = _rng(seed)
    texts, labels, langs = [], [], []
    for _ in range(n):
        urdu = bool(rng.random() < 0.5)
        pos = UR_POSITIVE if urdu else EN_POSITIVE
        neg = UR_NEGATIVE if urdu else EN_NEGATIVE
        neu = UR_NEUTRAL if urdu else EN_NEUTRAL
        n_pos = int(rng.integers(0, 4))
        n_neg = int(rng.integers(0, 4))
        words = list(rng.choice(neu, size=int(rng.integers(2, 6)), replace=True))
        words += list(rng.choice(pos, size=n_pos, replace=True))
        words += list(rng.choice(neg, size=n_neg, replace=True))
        if rng.random() < 0.5:
            words.append("!" if not urdu else "!")
        rng.shuffle(words)
        text = " ".join(words)
        if urdu and messy_urdu:
            text = _urdu_variant(rng, text)
        texts.append(text)
        labels.append(1 if n_pos > n_neg else 0)
        langs.append("ur" if urdu else "en")
    return texts, np.array(labels), np.array(langs)


# ---------------------------------------------------------------------------
# 2. News categorisation (stands in for BBC News / 20 Newsgroups)
# ---------------------------------------------------------------------------
NEWS_TOPICS = {
    "politics": {
        "en": ["parliament", "election", "minister", "vote", "policy", "senate",
               "government", "campaign", "bill", "opposition"],
        "ur": ["پارلیمنٹ", "انتخاب", "وزیر", "ووٹ", "پالیسی", "حکومت", "مہم"],
    },
    "sport": {
        "en": ["match", "team", "coach", "league", "goal", "tournament", "player",
               "stadium", "final", "injury"],
        "ur": ["میچ", "ٹیم", "کوچ", "لیگ", "گول", "ٹورنامنٹ", "کھلاڑی", "اسٹیڈیم"],
    },
    "business": {
        "en": ["market", "shares", "profit", "investor", "bank", "inflation", "trade",
               "revenue", "merger", "economy"],
        "ur": ["مارکیٹ", "شیئر", "منافع", "سرمایہ کار", "بینک", "تجارت", "معیشت"],
    },
    "technology": {
        "en": ["software", "chip", "startup", "algorithm", "device", "launch",
               "battery", "network", "robot", "model"],
        "ur": ["سافٹ ویئر", "چپ", "اسٹارٹ اپ", "الگورتھم", "ڈیوائس", "نیٹ ورک"],
    },
    "health": {
        "en": ["hospital", "patient", "vaccine", "doctor", "clinic", "study",
               "treatment", "disease", "research", "health"],
        "ur": ["ہسپتال", "مریض", "ویکسین", "ڈاکٹر", "کلینک", "تحقیق", "بیماری"],
    },
}


def news_corpus(n: int = 750, seed: int = 0, english_only: bool = True,
                off_topic_rate: float = 0.35, label_noise: float = 0.08):
    """Return (documents, category_names, labels).

    Each document is 20-45 tokens drawn mostly from its own topic vocabulary, plus
    shared filler and a proportion of off-topic words. The off-topic noise is what
    makes this a classification problem instead of a lookup: roughly a third of the
    content words belong to another topic, so accuracy lands below 1.0.
    """
    rng = _rng(seed)
    topics = list(NEWS_TOPICS)
    filler = ["report", "said", "week", "official", "today", "new", "more", "would",
              "city", "group", "number", "first", "last", "year", "people"]
    docs, labels = [], []
    for _ in range(n):
        index = int(rng.integers(0, len(topics)))
        topic = topics[index]
        key = "en" if english_only else "ur"
        vocab = NEWS_TOPICS[topic][key]
        other_topics = [t for i, t in enumerate(topics) if i != index]
        other = NEWS_TOPICS[str(rng.choice(other_topics))][key]
        total = int(rng.integers(10, 18))
        n_other = int(round(total * off_topic_rate))
        words = list(rng.choice(vocab, size=total - n_other, replace=True))
        words += list(rng.choice(other, size=n_other, replace=True))
        words += list(rng.choice(filler, size=int(rng.integers(8, 18)), replace=True))
        rng.shuffle(words)
        docs.append(" ".join(words))
        # A realistic share of news items are mislabelled in the source data; keeping
        # that noise means accuracy cannot reach 1.0 and calibration matters.
        if rng.random() < label_noise:
            index = int(rng.integers(0, len(topics)))
        labels.append(index)
    return docs, topics, np.array(labels)


# ---------------------------------------------------------------------------
# 3. Spam detection (stands in for the UCI SMS Spam Collection)
# ---------------------------------------------------------------------------
SPAM_MARKERS = ["free", "winner", "prize", "click", "urgent", "cash", "claim",
                "offer", "credit", "guaranteed", "call now", "subscribe", "txt"]
HAM_MARKERS = ["meeting", "lunch", "project", "tomorrow", "thanks", "report",
               "schedule", "call me", "family", "invoice", "attached", "review"]


def spam_corpus(n: int = 900, seed: int = 0, leak_rate: float = 0.35):
    """Return (messages, labels) with label 1 = spam.

    `leak_rate` mixes some of the other class's markers into each message, so the
    classes overlap and a classifier has to weigh evidence instead of pattern-matching
    a single giveaway word.
    """
    rng = _rng(seed)
    messages, labels = [], []
    for _ in range(n):
        spam = bool(rng.random() < 0.35)
        markers = SPAM_MARKERS if spam else HAM_MARKERS
        other = HAM_MARKERS if spam else SPAM_MARKERS
        words = list(rng.choice(markers, size=int(rng.integers(2, 5)), replace=True))
        n_other = int(round(len(words) * leak_rate))
        if n_other:
            words += list(rng.choice(other, size=n_other, replace=True))
        words += list(rng.choice(["you", "your", "we", "please", "now", "today",
                                  "number", "message", "account"], size=3, replace=True))
        rng.shuffle(words)
        messages.append(" ".join(words))
        labels.append(int(spam))
    return messages, np.array(labels)


# ---------------------------------------------------------------------------
# 4. Named-entity sentences (stands in for CoNLL-2003)
# ---------------------------------------------------------------------------
PEOPLE = ["Ayesha Khan", "Imran Ali", "Sara Ahmed", "Bilal Hussain", "Maria Lopez",
          "John Smith", "Fatima Noor", "Chen Wei"]
ORGS = ["Karachi University", "Lahore Bank", "TechHub", "Ministry of Health",
        "Global Motors", "NUST", "Alfalah Textiles"]
LOCS = ["Islamabad", "Karachi", "Lahore", "Peshawar", "Quetta", "Multan", "Sialkot"]
DATES = ["Monday", "March 2024", "last week", "12 June", "yesterday", "2023"]


def ner_corpus(n: int = 300, seed: int = 0):
    """Return (sentences, spans) where spans is a list of (start, end, label) tuples.

    Offsets are character offsets into the sentence, the same convention spaCy uses,
    so the gazetteer baseline and the spaCy comparison in L08-04 are directly
    comparable.
    """
    rng = _rng(seed)
    templates = [
        "{PERSON} joined {ORG} in {DATE}.",
        "{ORG} announced a new office in {LOC} on {DATE}.",
        "{PERSON}, who works at {ORG}, travelled to {LOC} {DATE}.",
        "According to {PERSON}, {ORG} will hire staff in {LOC} by {DATE}.",
        "{LOC} hosted the {ORG} conference, {PERSON} said on {DATE}.",
    ]
    sentences, spans = [], []
    for _ in range(n):
        person = str(rng.choice(PEOPLE))
        org = str(rng.choice(ORGS))
        loc = str(rng.choice(LOCS))
        date = str(rng.choice(DATES))
        template = str(rng.choice(templates))
        values = {"PERSON": person, "ORG": org, "LOC": loc, "DATE": date}
        sentence = template.format(**values)
        found = []
        for label, value in values.items():
            start = sentence.find(value)
            if start >= 0:
                found.append((start, start + len(value), label))
        sentences.append(sentence)
        spans.append(sorted(found))
    return sentences, spans


# ---------------------------------------------------------------------------
# 5. Extractive question answering (stands in for SQuAD)
# ---------------------------------------------------------------------------
QA_FACTS = [
    ("The Nile is the longest river in Africa and flows through eleven countries.",
     "Which river is the longest in Africa?", "Nile"),
    ("The Eiffel Tower was completed in 1889 and stands in Paris.",
     "When was the Eiffel Tower completed?", "1889"),
    ("Photosynthesis converts light energy into chemical energy in plants.",
     "What does photosynthesis convert light energy into?", "chemical energy"),
    ("The human heart has four chambers and pumps blood through the body.",
     "How many chambers does the human heart have?", "four"),
    ("Python was created by Guido van Rossum and released in 1991.",
     "Who created Python?", "Guido van Rossum"),
    ("The Great Wall of China was built over many centuries to protect borders.",
     "Why was the Great Wall of China built?", "protect borders"),
    ("Water boils at 100 degrees Celsius at sea level.",
     "At what temperature does water boil at sea level?", "100 degrees Celsius"),
    ("The Pacific is the largest ocean on Earth and covers a third of its surface.",
     "Which is the largest ocean on Earth?", "Pacific"),
]


def qa_corpus(seed: int = 0, distractors: int = 2):
    """Return (contexts, questions, answers) — extractive QA with known answer spans.

    Each context is the fact sentence plus unrelated distractor sentences, so a model
    cannot succeed by matching the question to the only sentence available.
    """
    rng = _rng(seed)
    contexts, questions, answers = [], [], []
    for index, (fact, question, answer) in enumerate(QA_FACTS):
        others = [f for i, (f, _, _) in enumerate(QA_FACTS) if i != index]
        chosen = list(rng.choice(others, size=min(distractors, len(others)), replace=False))
        context = " ".join([fact] + chosen)
        contexts.append(context)
        questions.append(question)
        answers.append(answer)
    return contexts, questions, answers


# ---------------------------------------------------------------------------
# 6. Embedding corpus and a tiny parallel corpus for seq2seq
# ---------------------------------------------------------------------------
EMBED_TOPICS = {
    "food": ["bread", "rice", "tea", "milk", "sugar", "salt", "fruit", "water"],
    "weather": ["rain", "sun", "cloud", "wind", "storm", "heat", "cold", "snow"],
    "travel": ["train", "bus", "road", "city", "ticket", "station", "journey", "map"],
    "study": ["book", "exam", "teacher", "class", "note", "lesson", "question", "answer"],
}


def embedding_corpus(sentences: int = 1200, seed: int = 0):
    """Topic-clustered sentences: enough structure for word2vec/GloVe to learn.

    Words inside a topic co-occur far more often than across topics, so nearest
    neighbours should be same-topic words — the property the lessons check.
    """
    rng = _rng(seed)
    topics = list(EMBED_TOPICS)
    out = []
    for _ in range(sentences):
        topic = str(rng.choice(topics))
        words = list(rng.choice(EMBED_TOPICS[topic], size=int(rng.integers(4, 9)), replace=True))
        words += list(rng.choice(["the", "a", "is", "and", "we", "need", "some"], size=3, replace=True))
        rng.shuffle(words)
        out.append(" ".join(words))
    return out


PARALLEL_EN = ["the cat drinks milk", "the dog drinks water", "the boy reads a book",
               "the girl reads a book", "we need tea", "we need bread",
               "the train is late", "the bus is late", "the sun is hot",
               "the tea is hot", "she writes a letter", "he writes a letter"]
PARALLEL_UR = ["بلی دودھ پیتی ہے", "کتا پانی پیتا ہے", "لڑکا کتاب پڑھتا ہے",
               "لڑکی کتاب پڑھتی ہے", "ہمیں چائے چاہیے", "ہمیں روٹی چاہیے",
               "ٹرین دیر سے ہے", "بس دیر سے ہے", "دھوپ تیز ہے",
               "چائے گرم ہے", "وہ خط لکھتی ہے", "وہ خط لکھتا ہے"]


def parallel_corpus(repeats: int = 20, seed: int = 0):
    """Return (english, urdu) sentence pairs — a toy alignment task for seq2seq.

    Twelve templates repeated with small word-order noise. This is enough for a small
    encoder-decoder with attention to learn alignments; it is not a translation system.
    """
    rng = _rng(seed)
    en, ur = [], []
    for _ in range(repeats):
        for e, u in zip(PARALLEL_EN, PARALLEL_UR):
            en.append(e)
            ur.append(u)
    order = rng.permutation(len(en))
    return [en[i] for i in order], [ur[i] for i in order]


# ---------------------------------------------------------------------------
# Optional real-data loaders
# ---------------------------------------------------------------------------
def load_text_files(paths, encoding: str = "utf-8"):
    """Read one document per file; returns (documents, filenames)."""
    documents, names = [], []
    for path in paths:
        with open(path, encoding=encoding, errors="replace") as handle:
            documents.append(handle.read())
        names.append(path)
    return documents, names


if __name__ == "__main__":
    texts, labels, langs = sentiment_corpus(600, seed=0)
    print("sentiment:", len(texts), "rows; label counts:", np.bincount(labels),
          "; languages:", dict(Counter(langs)))
    print("english sample:", texts[int(np.where(langs == "en")[0][0])][:70])

    urdu_text = "\u064a\u06c1 \u0643\u062a\u0627\u0628 \u0628\u06c1\u062a \u0627\u0686\u06be\u06cc \u06c1\u06d2\u06d4"
    print("urdu normalise changed chars:", normalise_urdu(urdu_text) != urdu_text)
    print("urdu tokens:", len(urdu_tokenize(urdu_text)))

    docs, topics, labels = news_corpus(500, seed=0)
    print("news:", len(docs), "docs,", len(topics), "topics, counts:", np.bincount(labels))

    messages, spam = spam_corpus(600, seed=0)
    print("spam:", len(messages), "messages, spam rate:", round(float(spam.mean()), 3))

    sentences, spans = ner_corpus(200, seed=0)
    print("ner:", len(sentences), "sentences, entities:", sum(len(s) for s in spans))

    contexts, questions, answers = qa_corpus()
    print("qa:", len(contexts), "items; first answer:", answers[0])

    corpus = embedding_corpus(500, seed=0)
    print("embedding corpus:", len(corpus), "sentences")

    en, ur = parallel_corpus(repeats=2)
    print("parallel:", len(en), "pairs")
