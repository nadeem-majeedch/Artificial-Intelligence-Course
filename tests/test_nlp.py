"""Tests for M08 NLP: preprocessing, vectorisers, n-gram model and attention."""

import math

import numpy as np
import pytest
import torch

import text_pipeline as tp
from seq_models import Attention, NGramLM


def test_sentence_split_keeps_abbreviations_and_terminators():
    text = "Dr. Smith arrived. The model failed! Did it? Yes."
    sentences = tp.sentence_split(text)
    assert len(sentences) == 4
    assert sentences[0].startswith("Dr. Smith")


def test_tokenize_separates_punctuation_and_respects_case():
    tokens = tp.tokenize("Models, trained on data, fail.")
    assert "Models" in tokens          # tokenisation does not lowercase; normalise does
    assert "," in tokens
    assert all(token.strip() == token for token in tokens)


def test_normalise_lowercases_and_collapses_whitespace():
    assert tp.normalise_text("  Hello   WORLD  ") == "hello world"


def test_stopword_removal_keeps_content_words():
    tokens = tp.tokenize("the model is not very good at this task")
    kept = tp.remove_stopwords(tokens)
    assert "the" not in kept and "is" not in kept
    assert "model" in kept and "task" in kept


def test_stemming_maps_verb_inflections_to_one_form():
    stems = tp.stem(["running", "runs", "run"])
    assert len(set(stems)) == 1


def test_ngrams_have_the_requested_length():
    grams = tp.ngrams(["a", "b", "c", "d"], 3)
    assert grams == [("a", "b", "c"), ("b", "c", "d")]


def test_bag_of_words_counts_and_vocabulary_come_from_training_texts():
    texts = ["red apple", "green apple", "red pepper"]
    vectoriser = tp.BagOfWords().fit(texts)
    matrix = vectoriser.transform(["red apple apple"])
    index = {term: i for i, term in enumerate(vectoriser.get_feature_names_out())}
    assert matrix.shape == (1, len(index))
    assert matrix[0, index["red"]] == 1
    assert matrix[0, index["apple"]] == 2
    assert "green" not in index or matrix[0, index["green"]] == 0


def test_tfidf_rows_are_l2_normalised_and_idf_downweights_common_terms():
    texts = ["machine learning model", "machine learning pipeline", "quantum annealing"]
    vectoriser = tp.TfidfVectorizer().fit(texts)
    matrix = vectoriser.transform(texts)
    norms = np.linalg.norm(matrix, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-6)
    index = {term: i for i, term in enumerate(vectoriser.get_feature_names_out())}
    assert vectoriser.idf_[index["machine"]] < vectoriser.idf_[index["quantum"]]


def test_ngram_probabilities_form_a_distribution_over_the_vocabulary():
    corpus = ["the cat sat on the mat", "the dog sat on the log"]
    model = NGramLM(n=2, k=0.1).fit(corpus)
    vocabulary = model.vocabulary + [tp.EOS if hasattr(tp, "EOS") else "</s>"]
    total = sum(model.probability(("the",), word) for word in set(vocabulary))
    assert 0 < total <= 1.0 + 1e-9


def test_ngram_model_prefers_corpus_sentences_to_nonsense():
    corpus = ["the cat sat on the mat", "the dog sat on the log"]
    model = NGramLM(n=2, k=0.1).fit(corpus)
    good = model.perplexity(["the cat sat on the mat"])
    bad = model.perplexity(["quantum banana telescope wrestling"])
    assert good < bad
    assert math.isfinite(good)


def test_ngram_rejects_an_invalid_order():
    with pytest.raises(ValueError):
        NGramLM(n=0)


def test_attention_weights_are_a_masked_distribution():
    torch.manual_seed(0)
    attention = Attention(8)
    decoder = torch.randn(3, 8)
    encoder = torch.randn(3, 5, 8)
    mask = torch.zeros(3, 5, dtype=torch.bool)
    mask[:, 4] = True
    context, weights = attention(decoder, encoder, mask)
    assert context.shape == (3, 8)
    assert torch.allclose(weights.sum(dim=1), torch.ones(3), atol=1e-6)
    assert torch.all(weights[:, 4] < 1e-7)
