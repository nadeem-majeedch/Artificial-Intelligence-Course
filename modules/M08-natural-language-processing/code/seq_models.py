"""Language modelling, sequence-to-sequence with attention, and Transformers for M08.

Four models, all small enough for a CPU:

1. `NGramLM` — add-k smoothed n-gram language model with perplexity and sampling.
2. `Seq2SeqAttention` — GRU encoder/decoder with additive attention, trained on a tiny
   English-Urdu parallel corpus (this is an alignment demo, not a translator).
3. `TinyCausalLM` — a decoder-only Transformer trained on the same corpus, for
   perplexity comparison and temperature/top-k generation.
4. Hugging Face helpers — tokenizer inspection, masked-language-model probing and a
   fine-tuning loop that runs only when a checkpoint is cached locally.

The Hugging Face paths are optional by design: the module must work offline, and a
classroom machine may not have a 250 MB checkpoint to spare.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np
import torch
import torch.nn as nn

import text_data as td
from text_pipeline import normalise_text, tokenize

PAD, SOS, EOS, UNK = "<pad>", "<sos>", "<eos>", "<unk>"


def set_seed(seed: int = 0) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


# ---------------------------------------------------------------------------
# 1. n-gram language model
# ---------------------------------------------------------------------------
class NGramLM:
    """Interpolated-free n-gram model with add-k smoothing.

    P(w_t | history) = (count(history, w_t) + k) / (count(history) + k * |V|)
    Perplexity is exp(-mean log P(token)), computed over the evaluation tokens only.
    """

    def __init__(self, n: int = 2, k: float = 0.1, language: str = "en"):
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.k = k
        self.language = language
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary: list[str] = []

    def _tokens(self, text: str) -> list[str]:
        return tokenize(normalise_text(text, self.language), self.language) + [EOS]

    def fit(self, corpus):
        tokens = Counter()
        for text in corpus:
            tokens.update(self._tokens(text))
        self.vocabulary = [word for word, _ in tokens.most_common()]
        for text in corpus:
            sequence = [SOS] * (self.n - 1) + self._tokens(text)
            for i in range(self.n - 1, len(sequence)):
                history = tuple(sequence[i - self.n + 1:i])
                self.counts[history][sequence[i]] += 1
                self.context_totals[history] += 1
        return self

    def probability(self, history: tuple, word: str) -> float:
        history = tuple(history[-(self.n - 1):]) if self.n > 1 else ()
        counts = self.counts.get(history, Counter())
        total = self.context_totals.get(history, 0)
        return (counts.get(word, 0) + self.k) / (total + self.k * (len(self.vocabulary) + 1))

    def log_probability(self, text: str) -> tuple[float, int]:
        sequence = [SOS] * (self.n - 1) + self._tokens(text)
        total = 0.0
        scored = 0
        for i in range(self.n - 1, len(sequence)):
            history = tuple(sequence[i - self.n + 1:i])
            total += math.log(self.probability(history, sequence[i]))
            scored += 1
        return total, scored

    def perplexity(self, corpus) -> float:
        total, scored = 0.0, 0
        for text in corpus:
            log_likelihood, count = self.log_probability(text)
            total += log_likelihood
            scored += count
        return float(math.exp(-total / max(scored, 1)))

    def generate(self, seed_text: str = "", length: int = 12, seed: int = 0,
                 temperature: float = 1.0) -> str:
        rng = np.random.default_rng(seed)
        sequence = [SOS] * (self.n - 1) + self._tokens(seed_text)[:-1] if seed_text else [SOS] * (self.n - 1)
        for _ in range(length):
            history = tuple(sequence[-(self.n - 1):]) if self.n > 1 else ()
            counts = self.counts.get(history, Counter())
            if not counts:
                break
            words = list(counts)
            weights = np.array([counts[word] for word in words], dtype=float) ** (1.0 / max(temperature, 1e-6))
            weights /= weights.sum()
            choice = words[int(rng.choice(len(words), p=weights))]
            if choice == EOS:
                break
            sequence.append(choice)
        return " ".join(sequence[self.n - 1:])


# ---------------------------------------------------------------------------
# 2. Sequence-to-sequence with additive attention
# ---------------------------------------------------------------------------
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed=32, hidden=64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed, padding_idx=0)
        self.gru = nn.GRU(embed, hidden, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, hidden = self.gru(embedded)
        return outputs, hidden


class Attention(nn.Module):
    """Bahdanau additive attention: score = v^T tanh(W_h h_enc + W_s s_dec)."""

    def __init__(self, hidden):
        super().__init__()
        self.key = nn.Linear(hidden, hidden, bias=False)
        self.query = nn.Linear(hidden, hidden, bias=False)
        self.score = nn.Linear(hidden, 1, bias=False)

    def forward(self, decoder_state, encoder_outputs, mask):
        # decoder_state: (batch, hidden); encoder_outputs: (batch, src_len, hidden)
        energy = torch.tanh(self.key(encoder_outputs) + self.query(decoder_state).unsqueeze(1))
        scores = self.score(energy).squeeze(-1)
        scores = scores.masked_fill(mask, float("-inf"))
        weights = torch.softmax(scores, dim=1)
        context = torch.bmm(weights.unsqueeze(1), encoder_outputs).squeeze(1)
        return context, weights


class Decoder(nn.Module):
    def __init__(self, vocab_size, embed=32, hidden=64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed, padding_idx=0)
        self.gru = nn.GRU(embed + hidden, hidden, batch_first=True)
        self.attention = Attention(hidden)
        self.output = nn.Linear(hidden * 2, vocab_size)

    def forward(self, token, hidden, encoder_outputs, mask):
        embedded = self.embedding(token)                      # (batch, 1, embed)
        state = hidden[-1]                                    # (batch, hidden)
        combined = torch.cat([embedded, state.unsqueeze(1)], dim=-1)
        out, hidden = self.gru(combined, hidden)
        context, weights = self.attention(hidden[-1], encoder_outputs, mask)
        logits = self.output(torch.cat([out.squeeze(1), context], dim=-1))
        return logits, hidden, weights


class Seq2SeqAttention(nn.Module):
    """Encoder-decoder with attention over source tokens (batch_first throughout)."""

    def __init__(self, src_vocab, tgt_vocab, embed=32, hidden=64):
        super().__init__()
        self.encoder = Encoder(src_vocab, embed, hidden)
        self.decoder = Decoder(tgt_vocab, embed, hidden)
        self.hidden = hidden

    def forward(self, source, target, teacher_forcing: bool = True):
        mask = source == 0
        encoder_outputs, hidden = self.encoder(source)
        batch, tgt_len = target.shape
        logits = torch.zeros(batch, tgt_len - 1, self.decoder.output.out_features)
        weights = torch.zeros(batch, tgt_len - 1, source.shape[1])
        token = target[:, 0].unsqueeze(1)
        for step in range(tgt_len - 1):
            step_logits, hidden, step_weights = self.decoder(
                token, hidden, encoder_outputs, mask)
            logits[:, step] = step_logits
            weights[:, step] = step_weights
            token = target[:, step + 1].unsqueeze(1) if teacher_forcing else step_logits.argmax(-1, keepdim=True)
        return logits, weights

    @torch.no_grad()
    def translate(self, source, max_len: int = 12):
        """Greedy decoding. Returns token ids and the attention weights."""
        mask = source == 0
        encoder_outputs, hidden = self.encoder(source)
        token = torch.full((source.shape[0], 1), 1, dtype=torch.long)  # <sos>
        output = []
        weights_out = []
        for _ in range(max_len):
            step_logits, hidden, weights = self.decoder(token, hidden, encoder_outputs, mask)
            token = step_logits.argmax(-1, keepdim=True)
            output.append(token)
            weights_out.append(weights)
            if bool((token == 2).all()):  # every hypothesis ended with <eos>
                break
        return torch.cat(output, dim=1), torch.stack(weights_out, dim=1)


def _vocabulary(sentences, tokenizer):
    counter = Counter()
    for sentence in sentences:
        counter.update(tokenizer(sentence))
    words = [PAD, SOS, EOS, UNK] + [word for word, _ in counter.most_common() if word not in (PAD, SOS, EOS, UNK)]
    return {word: index for index, word in enumerate(words)}, words


def _encode(sentences, vocab, tokenizer, add_sos=False, add_eos=True):
    sequences = []
    for sentence in sentences:
        ids = [vocab.get(word, 3) for word in tokenizer(sentence)]
        sequences.append(([1] if add_sos else []) + ids + ([2] if add_eos else []))
    length = max(len(sequence) for sequence in sequences)
    padded = np.zeros((len(sequences), length), dtype=np.int64)
    for row, sequence in enumerate(sequences):
        padded[row, :len(sequence)] = sequence
    return padded


def train_seq2seq(repeats: int = 20, epochs: int = 80, seed: int = 0, holdout: int = 2):
    """Train the attention model on the toy parallel corpus.

    Returns a dict with the model, vocabularies and accuracy on the training templates
    and on held-out templates. Held-out accuracy near zero is the expected, honest
    result for a 12-sentence corpus: the model memorises, it does not generalise.
    """
    set_seed(seed)
    english, urdu = td.parallel_corpus(repeats=repeats, seed=seed)
    all_templates = sorted(set(english))
    held = set(all_templates[-holdout:])
    train_pairs = [(e, u) for e, u in zip(english, urdu) if e not in held]
    test_pairs = list(dict.fromkeys([(e, u) for e, u in zip(english, urdu) if e in held]))

    src_vocab, src_words = _vocabulary([e for e, _ in train_pairs], lambda s: s.lower().split())
    tgt_vocab, tgt_words = _vocabulary([u for _, u in train_pairs], td.urdu_tokenize)

    source = torch.as_tensor(_encode([e for e, _ in train_pairs], src_vocab,
                                     lambda s: s.lower().split(), add_eos=False))
    target = torch.as_tensor(_encode([u for _, u in train_pairs], tgt_vocab, td.urdu_tokenize,
                                     add_sos=True))

    model = Seq2SeqAttention(len(src_words), len(tgt_words))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    losses = []
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        logits, _ = model(source, target)
        loss = criterion(logits.reshape(-1, logits.shape[-1]), target[:, 1:].reshape(-1))
        loss.backward()
        optimizer.step()
        losses.append(float(loss.item()))

    def accuracy(pairs):
        if not pairs:
            return float("nan")
        src = torch.as_tensor(_encode([e for e, _ in pairs], src_vocab,
                                      lambda s: s.lower().split(), add_eos=False))
        gold = [td.urdu_tokenize(u) for _, u in pairs]
        predicted, _ = model.translate(src)
        index_to_word = {i: w for w, i in tgt_vocab.items()}
        correct = 0
        for row, gold_tokens in enumerate(gold):
            predicted_tokens = []
            for index in predicted[row].tolist():
                if index == 2:
                    break
                predicted_tokens.append(index_to_word.get(index, UNK))
            correct += int(predicted_tokens == gold_tokens)
        return correct / len(pairs)

    return {
        "model": model,
        "src_vocab": src_vocab,
        "tgt_vocab": tgt_vocab,
        "src_words": src_words,
        "tgt_words": tgt_words,
        "losses": losses,
        "train_accuracy": accuracy(list(dict.fromkeys(train_pairs))),
        "heldout_accuracy": accuracy(test_pairs) if test_pairs else float("nan"),
        "heldout": test_pairs,
    }


def attention_alignment(model, src_vocab, src_words, tgt_vocab, sentence: str):
    """Return [(output_token_id, best_source_word, weight)] for one sentence."""
    model.eval()
    tokens = sentence.lower().split()
    source = torch.as_tensor([[src_vocab.get(word, 3) for word in tokens]])
    predicted, weights = model.translate(source)
    alignment = []
    for step, index in enumerate(predicted[0].tolist()):
        row = weights[0, step].numpy()
        best = int(np.argmax(row))
        alignment.append((index, tokens[best] if best < len(tokens) else "", float(row[best])))
    return alignment


# ---------------------------------------------------------------------------
# 3. Decoder-only Transformer language model
# ---------------------------------------------------------------------------
class TinyCausalLM(nn.Module):
    """Decoder-only Transformer: token + position embeddings, causal encoder, LM head."""

    def __init__(self, vocab_size, max_len=12, d_model=64, nhead=4, layers=2, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.position = nn.Parameter(torch.zeros(1, max_len, d_model))
        block = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=128,
                                           dropout=dropout, batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(block, num_layers=layers)
        self.head = nn.Linear(d_model, vocab_size)
        self.max_len = max_len

    def forward(self, x):
        length = x.shape[1]
        mask = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
        padding = x == 0
        hidden = self.embedding(x) + self.position[:, :length, :]
        hidden = self.encoder(hidden, mask=mask, src_key_padding_mask=padding)
        return self.head(hidden)


def train_causal_lm(corpus, epochs: int = 30, seed: int = 0, max_len: int = 10, lr: float = 1e-3):
    """Train the tiny LM on word sequences; returns model, vocab and the loss curve."""
    set_seed(seed)
    tokenizer = lambda text: tokenize(normalise_text(text))
    vocab, words = _vocabulary(corpus, tokenizer)
    sequences = [["<sos>"] + tokenizer(text)[:max_len - 1] + ["<eos>"] for text in corpus]
    padded = np.zeros((len(sequences), max_len + 1), dtype=np.int64)
    for row, sequence in enumerate(sequences):
        ids = [vocab[word] for word in sequence]
        padded[row, :len(ids)] = ids[:max_len + 1]

    data = torch.as_tensor(padded)
    inputs, targets = data[:, :-1], data[:, 1:]
    model = TinyCausalLM(len(words), max_len=max_len)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    losses = []
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        logits = model(inputs)
        loss = criterion(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
        loss.backward()
        optimizer.step()
        losses.append(float(loss.item()))
    return {"model": model, "vocab": vocab, "words": words, "losses": losses,
            "inputs": inputs, "targets": targets}


def causal_lm_perplexity(bundle) -> float:
    model, inputs, targets = bundle["model"], bundle["inputs"], bundle["targets"]
    model.eval()
    with torch.no_grad():
        logits = model(inputs)
        log_probs = torch.log_softmax(logits, dim=-1)
        mask = targets != 0
        picked = log_probs.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
        mean = picked[mask].mean()
    return float(torch.exp(-mean))


def sample_causal_lm(bundle, prompt: str = "the", length: int = 10, temperature: float = 1.0,
                     top_k: int | None = 5, seed: int = 0):
    """Sample from the LM with temperature and optional top-k truncation."""
    set_seed(seed)
    model, vocab = bundle["model"], bundle["vocab"]
    index_to_word = {i: w for w, i in vocab.items()}
    model.eval()
    tokens = [vocab.get(word, 3) for word in tokenize(normalise_text(prompt))]
    tokens = [vocab["<sos>"]] + tokens
    with torch.no_grad():
        for _ in range(length):
            logits = model(torch.as_tensor([tokens[-model.max_len:]]))[0, -1] / max(temperature, 1e-6)
            if top_k:
                values, indices = torch.topk(logits, min(top_k, logits.numel()))
                probs = torch.softmax(values, dim=-1)
                choice = int(indices[torch.multinomial(probs, 1)])
            else:
                choice = int(torch.multinomial(torch.softmax(logits, dim=-1), 1))
            tokens.append(choice)
            if index_to_word.get(choice) == "<eos>":
                break
    return " ".join(index_to_word.get(index, UNK) for index in tokens[1:])


# ---------------------------------------------------------------------------
# 4. Hugging Face helpers (optional)
# ---------------------------------------------------------------------------
def hf_availability(model_name: str = "distilbert-base-uncased") -> tuple[bool, str]:
    """Check whether a checkpoint is usable offline; return (available, message)."""
    try:
        from transformers import AutoConfig, AutoTokenizer
        AutoConfig.from_pretrained(model_name, local_files_only=True)
        AutoTokenizer.from_pretrained(model_name, use_fast=False, local_files_only=True)
        return True, f"{model_name} is cached locally"
    except Exception as error:
        return False, f"{model_name} is not cached ({type(error).__name__}); skipping"


def hf_mlm_probe(sentence: str, model_name: str = "distilbert-base-uncased"):
    """Masked-language-model probe: fill one [MASK] and report the top predictions."""
    from transformers import AutoModelForMaskedLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForMaskedLM.from_pretrained(model_name).eval()
    inputs = tokenizer(sentence, return_tensors="pt")
    mask_index = (inputs["input_ids"] == tokenizer.mask_token_id).nonzero()[0, 1]
    with torch.no_grad():
        logits = model(**inputs).logits[0, mask_index]
    top = torch.topk(logits, 5).indices.tolist()
    return [tokenizer.decode([index]).strip() for index in top]


def hf_finetune_sentiment(model_name: str = "distilbert-base-uncased", n: int = 400,
                          epochs: int = 1, seed: int = 0, lr: float = 5e-5):
    """Fine-tune a small encoder on the synthetic sentiment corpus.

    Returns a metrics dict, or raises RuntimeError when the checkpoint is not cached.
    Two hundred training rows for one epoch is enough to show the workflow; it is not
    enough to beat TF-IDF, which is exactly what L08-05 reports.
    """
    available, message = hf_availability(model_name)
    if not available:
        raise RuntimeError(message)

    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    set_seed(seed)
    texts, labels, _ = td.sentiment_corpus(n, seed=seed)
    split = int(len(texts) * 0.8)
    train_texts, train_labels = texts[:split], labels[:split]
    test_texts, test_labels = texts[split:], labels[split:]

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    def encode(batch):
        return tokenizer(batch, padding=True, truncation=True, max_length=48, return_tensors="pt")

    train_enc = encode(train_texts)
    test_enc = encode(test_texts)
    train_y = torch.as_tensor(train_labels)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        logits = model(**train_enc).logits
        loss = nn.CrossEntropyLoss()(logits, train_y)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        predictions = model(**test_enc).logits.argmax(dim=1).numpy()
    return {
        "accuracy": float((predictions == test_labels).mean()),
        "majority": float(max(np.mean(test_labels), 1 - np.mean(test_labels))),
        "params": int(sum(parameter.numel() for parameter in model.parameters())),
        "train_rows": split, "test_rows": len(test_texts), "loss": float(loss.item()),
    }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    corpus = td.embedding_corpus(600, seed=0)

    print("=== n-gram language models ===")
    for n in (1, 2, 3):
        model = NGramLM(n=n, k=0.1).fit(corpus[:450])
        print(f"n={n}: perplexity {model.perplexity(corpus[450:]):8.2f} | "
              f"vocab {len(model.vocabulary)}")
    bigram = NGramLM(n=2, k=0.1).fit(corpus)
    print("sample (temperature 0.8):", bigram.generate("the tea", length=8, temperature=0.8))
    print("sample (temperature 1.5):", bigram.generate("the tea", length=8, temperature=1.5))

    print()
    print("=== encoder-decoder with attention ===")
    bundle = train_seq2seq(repeats=20, epochs=80, seed=0, holdout=2)
    print("loss:", round(bundle["losses"][0], 3), "->", round(bundle["losses"][-1], 4))
    print("train template accuracy:", round(bundle["train_accuracy"], 3))
    print("held-out template accuracy:", round(bundle["heldout_accuracy"], 3),
          f"({len(bundle['heldout'])} templates)")
    example = bundle["heldout"][0][0] if bundle["heldout"] else "the cat drinks milk"
    alignment = attention_alignment(bundle["model"], bundle["src_vocab"], bundle["src_words"],
                                    bundle["tgt_vocab"], example)
    print("source:", example)
    print("alignment (output token id, source word, weight):",
          [(index, word, round(weight, 2)) for index, word, weight in alignment[:6]])

    print()
    print("=== decoder-only Transformer language model ===")
    lm = train_causal_lm(td.embedding_corpus(600, seed=0), epochs=30, seed=0)
    print("parameters:", sum(p.numel() for p in lm["model"].parameters()))
    print("loss:", round(lm["losses"][0], 3), "->", round(lm["losses"][-1], 3))
    print("perplexity:", round(causal_lm_perplexity(lm), 2))
    for temperature in (0.7, 1.2):
        print(f"sample at temperature {temperature}:",
              sample_causal_lm(lm, "the", length=8, temperature=temperature, seed=0))

    print()
    print("=== Hugging Face ===")
    available, message = hf_availability()
    print(message)
    if available:
        try:
            print("masked-LM fill for 'the tea is [MASK]':", hf_mlm_probe("the tea is [MASK]"))
        except Exception as error:
            print("MLM probe failed:", type(error).__name__)
