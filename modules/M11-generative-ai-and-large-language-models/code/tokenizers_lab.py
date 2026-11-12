"""tokenizers_lab.py -- tokenisation, vocabularies and the context window (M11, L11-02).

Three layers:

1. Byte-pair encoding from scratch (Sennrich et al., 2016): learn merges on a
   corpus, apply them, and watch a rare word split into known pieces.
2. Comparison of character, word, subword and byte tokenisation on the same
   sentence, with real counts from the GPT-2 tokenizer.
3. Practical accounting: context-window arithmetic, chunking with overlap,
   padding masks and the token cost of a chat transcript.

Run ``python tokenizers_lab.py`` for the numbers quoted in the lesson and in
NB-11-01.
"""

from __future__ import annotations

import re
from collections import Counter

# ---------------------------------------------------------------------------
# 1. BPE from scratch
# ---------------------------------------------------------------------------

END = "</w>"          # marks the end of a word, as in the original BPE paper


def word_counts(texts) -> Counter:
    """Split on whitespace and punctuation, keep counts of each word form."""
    counts: Counter = Counter()
    for text in texts:
        for w in re.findall(r"[a-z]+|[0-9]+|[^\sa-z0-9]", text.lower()):
            counts[w] += 1
    return counts


def to_symbols(counts: Counter) -> dict:
    """Every word becomes a tuple of characters plus the end-of-word marker."""
    return {tuple(list(w) + [END]): c for w, c in counts.items()}


def most_common_pair(vocab: dict) -> tuple[tuple[str, str], int]:
    pairs: Counter = Counter()
    for symbols, freq in vocab.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[(a, b)] += freq
    return pairs.most_common(1)[0]


def merge_vocab(vocab: dict, pair: tuple[str, str]) -> dict:
    a, b = pair
    merged = a + b
    out = {}
    for symbols, freq in vocab.items():
        new, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
                new.append(merged)
                i += 2
            else:
                new.append(symbols[i])
                i += 1
        out[tuple(new)] = freq
    return out


def learn_bpe(texts, num_merges: int = 25, verbose: bool = False):
    """Learn ``num_merges`` merge rules; returns (merges, vocab_at_each_step)."""
    vocab = to_symbols(word_counts(texts))
    merges, history = [], []
    for step in range(num_merges):
        pair, freq = most_common_pair(vocab)
        vocab = merge_vocab(vocab, pair)
        merges.append((pair, freq))
        history.append(len(vocab))
        if verbose:
            print(f"  merge {step + 1:2d}: {pair[0]!r} + {pair[1]!r} -> "
                  f"{pair[0] + pair[1]!r}  (freq {freq}, types now {len(vocab)})")
    return merges, history


def apply_bpe(word: str, merges) -> list[str]:
    """Apply learned merges in order, longest-standing rule first."""
    symbols = list(word.lower()) + [END]
    for (a, b), _ in merges:
        out, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
                out.append(a + b)
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        symbols = out
    return symbols


def bpe_vocab_size(merges, base_alphabet: int) -> int:
    """Base symbols plus one new symbol per merge."""
    return base_alphabet + len(merges)


# ---------------------------------------------------------------------------
# 2. Comparing granularities
# ---------------------------------------------------------------------------

def compare_granularities(sentence: str) -> dict:
    """Same sentence in four tokenisations, with counts and per-token strings."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained("distilgpt2")
    subword_ids = tok(sentence)["input_ids"]
    subword = [tok.decode([i]) for i in subword_ids]
    return {
        "characters": len(sentence),
        "words": len(sentence.split()),
        "subword_tokens": len(subword_ids),
        "bytes": len(sentence.encode("utf-8")),
        "subword_pieces": subword,
        "chars_per_token": len(sentence) / len(subword_ids),
        "words_per_token": len(sentence.split()) / len(subword_ids),
    }


def token_report(texts, name: str = "corpus") -> dict:
    """Aggregate tokenisation statistics for a collection of texts."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained("distilgpt2")
    total_tokens = total_chars = total_words = 0
    vocab_used = set()
    longest = 0
    for t in texts:
        ids = tok(t)["input_ids"]
        total_tokens += len(ids)
        total_chars += len(t)
        total_words += len(t.split())
        vocab_used.update(ids)
        longest = max(longest, len(ids))
    return {
        "name": name,
        "documents": len(texts),
        "tokens": total_tokens,
        "chars": total_chars,
        "words": total_words,
        "chars_per_token": total_chars / total_tokens,
        "tokens_per_word": total_tokens / total_words,
        "vocab_used": len(vocab_used),
        "longest_document_tokens": longest,
    }


def whitespace_and_numbers() -> dict:
    """Where tokenisers surprise people: spaces, digits, case, unicode."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained("distilgpt2")
    probes = ["hello", " hello", "Hello", "HELLO", "1234", "1234567890",
              "2026-11-11", "9,250", "don't", "Northfield", "cafe"]
    out = {}
    for p in probes:
        ids = tok(p)["input_ids"]
        out[p] = {"n_tokens": len(ids), "pieces": [tok.decode([i]) for i in ids]}
    return out


# ---------------------------------------------------------------------------
# 3. Context-window arithmetic and chunking
# ---------------------------------------------------------------------------

def context_budget(prompt_tokens: int, window: int, reserve_output: int) -> dict:
    """How many tokens are left for retrieved context, and how much is truncated."""
    available = window - prompt_tokens - reserve_output
    return {
        "window": window,
        "prompt": prompt_tokens,
        "reserved_output": reserve_output,
        "available_for_context": max(0, available),
        "overflow": max(0, -available),
    }


def chunk_text(text: str, tok, size: int = 120, overlap: int = 20) -> list[dict]:
    """Split text into token windows with overlap, decoding each window back."""
    ids = tok(text)["input_ids"]
    step = max(1, size - overlap)
    chunks = []
    for start in range(0, max(1, len(ids)), step):
        window = ids[start:start + size]
        if not window:
            break
        chunks.append({
            "start": start,
            "n_tokens": len(window),
            "text": tok.decode(window),
        })
        if start + size >= len(ids):
            break
    return chunks


def chat_token_cost(turns, tok) -> dict:
    """Token cost of a transcript and of the cheapest possible next turn."""
    text = "\n".join(f"{role}: {msg}" for role, msg in turns)
    ids = tok(text)["input_ids"]
    return {"turns": len(turns), "tokens": len(ids),
            "mean_tokens_per_turn": len(ids) / len(turns)}


# ---------------------------------------------------------------------------
# 4. Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 78)
    print("1. BPE from scratch on the module corpus")
    print("=" * 78)
    from gen_data import HANDBOOK
    texts = [d["text"] for d in HANDBOOK.values()]
    base_alphabet = len(set("abcdefghijklmnopqrstuvwxyz0123456789")) + 1
    merges, history = learn_bpe(texts, num_merges=18, verbose=True)
    print(f"base alphabet   : {base_alphabet} symbols")
    print(f"vocab after 18  : {bpe_vocab_size(merges, base_alphabet)} symbols")
    print(f"word types      : {len(word_counts(texts))}")
    for word in ("library", "students", "mitigating", "university", "2026"):
        print(f"  {word:12s} -> {apply_bpe(word, merges)}")

    print("\n" + "=" * 78)
    print("2. One sentence, four granularities")
    print("=" * 78)
    sentence = "Northfield University charges 9,250 GBP for undergraduate tuition."
    g = compare_granularities(sentence)
    print(f"sentence        : {sentence}")
    print(f"characters      : {g['characters']}")
    print(f"words           : {g['words']}")
    print(f"subword tokens  : {g['subword_tokens']}  "
          f"({g['chars_per_token']:.2f} chars/token, {g['words_per_token']:.2f} words/token)")
    print(f"utf-8 bytes     : {g['bytes']}")
    print(f"pieces          : {g['subword_pieces']}")

    print("\n" + "=" * 78)
    print("3. Corpus-level tokenisation statistics")
    print("=" * 78)
    rep = token_report(texts, "handbook")
    for k, v in rep.items():
        print(f"  {k:24s} {v if isinstance(v, str) else round(v, 3) if isinstance(v, float) else v}")

    print("\nWhitespace and number probes (GPT-2 tokenizer):")
    for p, info in whitespace_and_numbers().items():
        print(f"  {p!r:16s} {info['n_tokens']} token(s) {info['pieces']}")

    print("\n" + "=" * 78)
    print("4. Context-window arithmetic")
    print("=" * 78)
    for window, prompt, reserve in ((1024, 300, 200), (1024, 900, 200), (4096, 300, 500),
                                    (2048, 1800, 300)):
        b = context_budget(prompt, window, reserve)
        print(f"  window {window:5d}  prompt {prompt:5d}  reserve {reserve:4d}  "
              f"context {b['available_for_context']:5d}  overflow {b['overflow']}")

    print("\n" + "=" * 78)
    print("5. Chunking the handbook")
    print("=" * 78)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("distilgpt2")
    doc = HANDBOOK["hb-10"]["text"]
    total = len(tok(doc)["input_ids"])
    for size, overlap in ((120, 20), (60, 10)):
        chunks = chunk_text(doc, tok, size, overlap)
        print(f"  size {size:3d} overlap {overlap:2d}: {total} tokens -> "
              f"{len(chunks)} chunks {[c['n_tokens'] for c in chunks]}")

    turns = [("system", "You are the Northfield handbook assistant."),
             ("user", "What is the library policy on group rooms?"),
             ("assistant", "Group rooms can be booked online up to seven days in advance."),
             ("user", "And how long can I keep one?")]
    print("\nchat transcript:", chat_token_cost(turns, tok))


if __name__ == "__main__":
    main()
