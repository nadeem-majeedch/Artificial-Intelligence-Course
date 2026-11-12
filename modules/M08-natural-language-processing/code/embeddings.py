"""Word embeddings from scratch: skip-gram with negative sampling, and GloVe.

Both models are small enough to train on the synthetic corpus in seconds on a CPU.
The point is not benchmark quality — it is that every number in L08-03 is produced by
code you can read. A contextual-embedding helper wraps Hugging Face Transformers when
a checkpoint is available locally.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np

from text_data import EMBED_TOPICS, embedding_corpus, normalise_urdu
from text_pipeline import tokenize


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# Shared vocabulary utilities
# ---------------------------------------------------------------------------
def build_vocab(corpus, min_count: int = 1, language: str = "en"):
    """Return (word_to_index, index_to_word, counts) from tokenised sentences."""
    counter = Counter()
    for text in corpus:
        counter.update(tokenize(normalise_urdu(text) if language == "ur" else text.lower(), language))
    words = [word for word, count in counter.most_common() if count >= min_count]
    index = {word: i for i, word in enumerate(words)}
    return index, words, counter


def cosine_similarity(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    unit = matrix / norms
    return unit @ unit.T


def nearest_neighbours(matrix, words, word, k: int = 5):
    """Return [(neighbour, cosine)] for the k most similar words."""
    if word not in words:
        raise KeyError(f"{word!r} is not in the vocabulary")
    index = words.index(word)
    matrix_norm = matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)
    scores = matrix_norm @ matrix_norm[index]
    order = np.argsort(-scores)
    out = [(words[i], float(scores[i])) for i in order if i != index][:k]
    return out


def analogy(matrix, words, a: str, b: str, c: str, k: int = 3):
    """Solve a - b + c ~= ? using normalised vectors (the classic king/queen test)."""
    unit = matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)
    target = unit[words.index(a)] - unit[words.index(b)] + unit[words.index(c)]
    scores = unit @ (target / max(np.linalg.norm(target), 1e-12))
    banned = {words.index(a), words.index(b), words.index(c)}
    order = [i for i in np.argsort(-scores) if i not in banned][:k]
    return [(words[i], float(scores[i])) for i in order]


def topic_purity(matrix, words) -> float:
    """Fraction of words whose single nearest neighbour belongs to the same topic.

    Uses the topic lists in text_data.EMBED_TOPICS, so it measures the only structure
    the synthetic corpus actually contains. Chance level is about 1/4.
    """
    topic_of = {word: topic for topic, vocab in EMBED_TOPICS.items() for word in vocab}
    unit = matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)
    scores = unit @ unit.T
    np.fill_diagonal(scores, -np.inf)
    hits, total = 0, 0
    for i, word in enumerate(words):
        if word not in topic_of:
            continue
        neighbour = words[int(np.argmax(scores[i]))]
        total += 1
        hits += int(topic_of.get(neighbour) == topic_of[word])
    return hits / total if total else float("nan")


# ---------------------------------------------------------------------------
# 1. word2vec: skip-gram with negative sampling
# ---------------------------------------------------------------------------
class SkipGram:
    """Skip-gram with negative sampling (SGNS), trained with plain SGD.

    Objective per (centre, context) pair:
        log sigmoid(w_c . v_o) + sum_{k=1..K} log sigmoid(-w_c . v_neg_k)
    with negatives drawn from the unigram distribution raised to 0.75.
    """

    def __init__(self, dim: int = 16, window: int = 2, negative: int = 5,
                 lr: float = 0.05, epochs: int = 12, subsample: float = 1e-4,
                 seed: int = 0):
        self.dim = dim
        self.window = window
        self.negative = negative
        self.lr = lr
        self.epochs = epochs
        self.subsample = subsample
        self.seed = seed
        self.losses: list[float] = []

    def fit(self, corpus, min_count: int = 2, language: str = "en"):
        rng = _rng(self.seed)
        self.word_to_index, self.words, counts = build_vocab(corpus, min_count, language)
        vocab_size = len(self.words)
        self.context_vectors_ = rng.normal(0, 0.1, (vocab_size, self.dim))
        self.vectors_ = rng.normal(0, 0.1, (vocab_size, self.dim))

        sentences = [[self.word_to_index[w] for w in tokenize(
            normalise_urdu(text) if language == "ur" else text.lower(), language)
            if w in self.word_to_index] for text in corpus]

        # Negative-sampling distribution: unigram counts ** 0.75, normalised.
        counts_array = np.array([counts[w] for w in self.words], dtype=np.float64) ** 0.75
        self.negative_distribution_ = counts_array / counts_array.sum()

        # Subsampling of frequent words, as in the original paper.
        frequencies = np.array([counts[w] for w in self.words]) / sum(counts.values())
        keep_probability = np.minimum(1.0, np.sqrt(self.subsample / np.maximum(frequencies, 1e-12)))

        for _ in range(self.epochs):
            epoch_loss, pairs = 0.0, 0
            for sentence in sentences:
                for position, centre in enumerate(sentence):
                    if rng.random() > keep_probability[centre]:
                        continue
                    left = max(0, position - self.window)
                    right = min(len(sentence), position + self.window + 1)
                    for neighbour_position in range(left, right):
                        if neighbour_position == position:
                            continue
                        context = sentence[neighbour_position]
                        epoch_loss += self._update(centre, context, rng)
                        pairs += 1
            self.losses.append(epoch_loss / max(pairs, 1))

        # The usual convention: the input matrix is the embedding.
        self.embeddings_ = self.vectors_
        return self

    def _update(self, centre: int, context: int, rng) -> float:
        negatives = rng.choice(len(self.words), size=self.negative, p=self.negative_distribution_)
        targets = np.concatenate(([context], negatives))
        labels = np.zeros(len(targets))
        labels[0] = 1.0

        centre_vector = self.vectors_[centre]
        context_vectors = self.context_vectors_[targets]
        scores = context_vectors @ centre_vector
        probabilities = 1.0 / (1.0 + np.exp(-np.clip(scores, -30, 30)))
        loss = -np.mean(labels * np.log(probabilities + 1e-12)
                        + (1 - labels) * np.log(1 - probabilities + 1e-12))

        gradient = (probabilities - labels) * self.lr
        self.vectors_[centre] -= gradient @ context_vectors
        self.context_vectors_[targets] -= np.outer(gradient, centre_vector)
        return float(loss)

    def similarity(self, word: str, k: int = 5):
        return nearest_neighbours(self.embeddings_, self.words, word, k)


# ---------------------------------------------------------------------------
# 2. GloVe: weighted least squares on the log co-occurrence matrix
# ---------------------------------------------------------------------------
class GloVe:
    """GloVe trained on a co-occurrence matrix with the standard weighting function.

        J = sum_{i,j} f(X_ij) (w_i . c_j + b_i + c_j' - log X_ij)^2
        f(x) = min(1, (x / x_max) ** 0.75)
    """

    def __init__(self, dim: int = 16, window: int = 3, x_max: float = 10.0,
                 lr: float = 0.05, epochs: int = 40, seed: int = 0):
        self.dim = dim
        self.window = window
        self.x_max = x_max
        self.lr = lr
        self.epochs = epochs
        self.seed = seed
        self.losses: list[float] = []

    def fit(self, corpus, min_count: int = 2, language: str = "en"):
        rng = _rng(self.seed)
        self.word_to_index, self.words, _ = build_vocab(corpus, min_count, language)
        vocab_size = len(self.words)

        cooccurrence = np.zeros((vocab_size, vocab_size), dtype=np.float64)
        for text in corpus:
            tokens = [self.word_to_index[w] for w in tokenize(
                normalise_urdu(text) if language == "ur" else text.lower(), language)
                if w in self.word_to_index]
            for i, centre in enumerate(tokens):
                for j in range(max(0, i - self.window), min(len(tokens), i + self.window + 1)):
                    if i == j:
                        continue
                    cooccurrence[centre, tokens[j]] += 1.0 / abs(i - j)

        rows, cols = np.nonzero(cooccurrence)
        values = cooccurrence[rows, cols]
        log_values = np.log(values)
        weights = np.minimum(1.0, (values / self.x_max) ** 0.75)

        self.vectors_ = (rng.random((vocab_size, self.dim)) - 0.5) / self.dim
        context = (rng.random((vocab_size, self.dim)) - 0.5) / self.dim
        bias_word = np.zeros(vocab_size)
        bias_context = np.zeros(vocab_size)
        grad_w = np.ones_like(self.vectors_)
        grad_c = np.ones_like(context)
        grad_bw = np.ones(vocab_size)
        grad_bc = np.ones(vocab_size)

        for _ in range(self.epochs):
            predictions = (self.vectors_[rows] * context[cols]).sum(axis=1) \
                + bias_word[rows] + bias_context[cols]
            errors = predictions - log_values
            loss = float(np.sum(weights * errors ** 2))
            self.losses.append(loss)

            gradient = 2.0 * weights * errors
            word_grad = gradient[:, None] * context[cols]
            context_grad = gradient[:, None] * self.vectors_[rows]

            np.add.at(grad_w, rows, word_grad ** 2)
            np.add.at(grad_c, cols, context_grad ** 2)
            np.add.at(grad_bw, rows, gradient ** 2)
            np.add.at(grad_bc, cols, gradient ** 2)

            # AdaGrad updates keep the tiny model stable without tuning per-row rates.
            np.add.at(self.vectors_, rows, -self.lr * word_grad / np.sqrt(grad_w[rows]))
            np.add.at(context, cols, -self.lr * context_grad / np.sqrt(grad_c[cols]))
            np.add.at(bias_word, rows, -self.lr * gradient / np.sqrt(grad_bw[rows]))
            np.add.at(bias_context, cols, -self.lr * gradient / np.sqrt(grad_bc[cols]))

        self.embeddings_ = self.vectors_ + context
        return self

    def similarity(self, word: str, k: int = 5):
        return nearest_neighbours(self.embeddings_, self.words, word, k)


# ---------------------------------------------------------------------------
# 3. Contextual embeddings via Transformers
# ---------------------------------------------------------------------------
def contextual_vectors(sentences, model_name: str = "distilbert-base-uncased"):
    """Return token-level contextual vectors: {sentence: [(token, vector)]}.

    Requires a cached Hugging Face checkpoint. Raises RuntimeError with an explicit
    message when the checkpoint is not available offline; the lesson shows the
    fallback so the concept is still testable with static embeddings.
    """
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        model = AutoModel.from_pretrained(model_name)
    except Exception as error:  # pragma: no cover - network dependent
        raise RuntimeError(
            f"Contextual vectors need the checkpoint {model_name!r} in the local HF cache: {error}"
        ) from error

    model.eval()
    out = {}
    with torch.no_grad():
        for sentence in sentences:
            encoded = tokenizer(sentence, return_tensors="pt")
            hidden = model(**encoded).last_hidden_state[0]
            tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"][0])
            out[sentence] = [(token, hidden[i].numpy()) for i, token in enumerate(tokens)]
    return out


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    corpus = embedding_corpus(1200, seed=0)
    print("corpus sentences:", len(corpus))

    sg = SkipGram(dim=16, window=2, negative=5, epochs=12, seed=0).fit(corpus, min_count=2)
    print("skip-gram vocab:", len(sg.words), "| first loss:", round(sg.losses[0], 4),
          "-> last:", round(sg.losses[-1], 4))
    print("skip-gram nearest to 'tea':", [(w, round(s, 3)) for w, s in sg.similarity("tea", 4)])
    print("skip-gram topic purity:", round(topic_purity(sg.embeddings_, sg.words), 3))

    glove = GloVe(dim=16, window=3, epochs=40, seed=0).fit(corpus, min_count=2)
    print("glove vocab:", len(glove.words), "| first loss:", round(glove.losses[0], 1),
          "-> last:", round(glove.losses[-1], 1))
    print("glove nearest to 'tea':", [(w, round(s, 3)) for w, s in glove.similarity("tea", 4)])
    print("glove topic purity:", round(topic_purity(glove.embeddings_, glove.words), 3))

    both = set(sg.words) & set(glove.words)
    sg_matrix = np.stack([sg.embeddings_[sg.words.index(w)] for w in sorted(both)])
    gl_matrix = np.stack([glove.embeddings_[glove.words.index(w)] for w in sorted(both)])
    correlation = np.corrcoef(cosine_similarity(sg_matrix).ravel(),
                              cosine_similarity(gl_matrix).ravel())[0, 1]
    print("similarity-matrix correlation between the two models:", round(float(correlation), 3))
