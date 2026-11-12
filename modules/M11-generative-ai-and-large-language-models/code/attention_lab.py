"""attention_lab.py -- attention mechanics with real numbers (M11, L11-02).

Part 1 is pure NumPy: scaled dot-product attention, causal and padding masks,
multi-head projections and sinusoidal position encodings, with every
intermediate value printed so you can check the hand-worked examples.
Part 2 opens distilgpt2 and measures what its attention heads actually do:
entropy per layer, how much mass sits on the current token, and how far each
head looks back.

Run ``python attention_lab.py``. The numbers in L11-02 and NB-11-01 come from
this file.
"""

from __future__ import annotations

import numpy as np

np.set_printoptions(precision=3, suppress=True)


# ---------------------------------------------------------------------------
# 1. The mechanics
# ---------------------------------------------------------------------------

def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax: subtract the max before exponentiating."""
    x = np.asarray(x, dtype=float)
    shifted = x - x.max(axis=axis, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=axis, keepdims=True)


def scaled_dot_product_attention(Q, K, V, mask=None, return_weights=False):
    """softmax(Q K^T / sqrt(d_k) + mask) V, with the mask added before softmax."""
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    if mask is not None:
        scores = scores + mask
    weights = softmax(scores, axis=-1)
    out = weights @ V
    return (out, weights, scores) if return_weights else out


def causal_mask(n: int, neg: float = -1e9) -> np.ndarray:
    """Upper triangle (and diagonal-free future) set to a large negative number."""
    return np.triu(np.full((n, n), neg), k=1)


def padding_mask(lengths, total: int, neg: float = -1e9) -> np.ndarray:
    """Mask out keys at positions >= length for each query row."""
    m = np.zeros((len(lengths), total))
    for i, L in enumerate(lengths):
        m[i, L:] = neg
    return m


def multi_head_attention(Q, K, V, n_heads: int, seed: int = 0):
    """Split into heads with fixed random projections, attend, concat, project."""
    rng = np.random.default_rng(seed)
    n, d = Q.shape
    assert d % n_heads == 0, "d_model must divide by n_heads"
    d_head = d // n_heads
    Wq, Wk, Wv = (rng.normal(0, 1 / np.sqrt(d), (d, d)) for _ in range(3))
    Wo = rng.normal(0, 1 / np.sqrt(d), (d, d))
    Qp, Kp, Vp = Q @ Wq, K @ Wk, V @ Wv

    heads, weights = [], []
    for h in range(n_heads):
        sl = slice(h * d_head, (h + 1) * d_head)
        out, w = scaled_dot_product_attention(Qp[:, sl], Kp[:, sl], Vp[:, sl],
                                              return_weights=True)[0], \
            scaled_dot_product_attention(Qp[:, sl], Kp[:, sl], Vp[:, sl],
                                         return_weights=True)[1]
        heads.append(out)
        weights.append(w)
    concat = np.concatenate(heads, axis=-1)
    return concat @ Wo, np.stack(weights)


def sinusoidal_positions(n: int, d: int) -> np.ndarray:
    """Classic transformer position encoding, shape (n, d)."""
    pos = np.arange(n)[:, None]
    i = np.arange(0, d, 2)[None, :]
    angle = pos / np.power(10000, i / d)
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(angle)
    pe[:, 1::2] = np.cos(angle[:, :d // 2])
    return pe


def softmax_saturation(d_k: int, trials: int = 2000, seed: int = 0) -> dict:
    """Show why the sqrt(d_k) divisor matters: unscaled logits saturate."""
    rng = np.random.default_rng(seed)
    q = rng.normal(size=(1, d_k))
    K = rng.normal(size=(10, d_k))
    raw = (q @ K.T)[0]
    scaled = raw / np.sqrt(d_k)
    w_raw, w_scaled = softmax(raw), softmax(scaled)
    return {
        "d_k": d_k,
        "raw_logit_range": (float(raw.min()), float(raw.max())),
        "raw_max_weight": float(w_raw.max()),
        "scaled_max_weight": float(w_scaled.max()),
        "raw_entropy": float(-(w_raw * np.log(w_raw + 1e-12)).sum()),
        "scaled_entropy": float(-(w_scaled * np.log(w_scaled + 1e-12)).sum()),
        "max_entropy": float(np.log(len(raw))),
    }


# ---------------------------------------------------------------------------
# 2. What a pretrained model's heads do
# ---------------------------------------------------------------------------

def attention_profile(sentence: str, model_name: str = "distilgpt2") -> dict:
    """Mean attention entropy per layer, mass on self, and mean look-back distance."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, attn_implementation="eager")
    model.eval()
    enc = tok(sentence, return_tensors="pt")
    with torch.no_grad():
        out = model(**enc, output_attentions=True)

    # attentions: tuple of (1, heads, seq, seq), one per layer
    n_tokens = enc["input_ids"].shape[1]
    ids = enc["input_ids"][0].tolist()
    pieces = [tok.decode([i]) for i in ids]
    layers = []
    positions = torch.arange(n_tokens, dtype=torch.float)
    for layer_idx, attn in enumerate(out.attentions):
        a = attn[0].double()                      # (heads, seq, seq)
        ent = -(a * torch.log(a + 1e-12)).sum(-1)  # (heads, seq)
        # mass on the query's own position
        self_mass = torch.diagonal(a, dim1=-2, dim2=-1).mean(-1)
        # expected distance |i - j| under the attention distribution
        dist = (a * (positions[None, :, None] - positions[None, None, :]).abs()).sum(-1)
        layers.append({
            "layer": layer_idx,
            "mean_entropy": float(ent.mean()),
            "max_entropy": float(np.log(n_tokens)),
            "self_mass": float(self_mass.mean()),
            "mean_distance": float(dist.mean()),
            "head_entropies": [round(float(e.mean()), 3) for e in ent],
        })
    return {"tokens": n_tokens, "pieces": pieces, "layers": layers,
            "n_layers": len(layers), "n_heads": len(layers[0]["head_entropies"])}


def next_token_report(prompt: str, model_name: str = "distilgpt2", k: int = 5) -> list:
    """Top-k next tokens with probabilities and ranks, for L11-03."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    enc = tok(prompt, return_tensors="pt")
    with torch.no_grad():
        logits = model(**enc).logits[0, -1]
    probs = torch.softmax(logits, -1)
    top = torch.topk(probs, k)
    return [{"token": tok.decode([i]), "id": int(i), "p": float(p)}
            for p, i in zip(top.values, top.indices)]


# ---------------------------------------------------------------------------
# 3. Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 78)
    print("1. One head by hand: Q=(1,0), K=I2, V=[[10,0],[0,20]], d_k=2")
    print("=" * 78)
    q = np.array([[1.0, 0.0]])
    k = np.eye(2)
    v = np.array([[10.0, 0.0], [0.0, 20.0]])
    out, w, scores = scaled_dot_product_attention(q, k, v, return_weights=True)
    print("scores        :", scores)
    print("weights       :", w, " row sums:", w.sum(axis=1))
    print("output        :", out)
    print("check         : 0.670*10 = 6.70, 0.330*20 = 6.60")

    print("\n" + "=" * 78)
    print("2. Causal mask on four tokens")
    print("=" * 78)
    rng = np.random.default_rng(0)
    Q = rng.normal(size=(4, 3))
    K = rng.normal(size=(4, 3))
    V = rng.normal(size=(4, 3))
    _, w_causal, _ = scaled_dot_product_attention(Q, K, V, mask=causal_mask(4),
                                                  return_weights=True)
    print(w_causal)
    print("row 0 attends only to token 0 (weight 1.0); row 3 attends to all four.")

    print("\n" + "=" * 78)
    print("3. Padding mask: lengths [4, 2] over 4 key positions")
    print("=" * 78)
    m = padding_mask([4, 2], 4)
    _, w_pad, _ = scaled_dot_product_attention(np.ones((2, 3)), np.ones((4, 3)),
                                               np.ones((4, 3)), mask=m, return_weights=True)
    print(w_pad)
    print("masked columns get zero weight: ", np.allclose(w_pad[1, 2:], 0.0))

    print("\n" + "=" * 78)
    print("4. Why divide by sqrt(d_k)?  (10 keys, 2000-seed logits)")
    print("=" * 78)
    for d_k in (4, 16, 64, 256):
        r = softmax_saturation(d_k)
        print(f"  d_k={d_k:4d}  raw logits [{r['raw_logit_range'][0]:7.2f},"
              f"{r['raw_logit_range'][1]:6.2f}]  max weight raw {r['raw_max_weight']:.4f}"
              f" scaled {r['scaled_max_weight']:.4f}  entropy raw {r['raw_entropy']:.4f}"
              f" scaled {r['scaled_entropy']:.4f} (max {r['max_entropy']:.4f})")

    print("\n" + "=" * 78)
    print("5. Multi-head attention: 6 tokens, d_model=12, 3 heads")
    print("=" * 78)
    rng = np.random.default_rng(1)
    X = rng.normal(size=(6, 12))
    out, heads_w = multi_head_attention(X, X, X, n_heads=3)
    print("output shape  :", out.shape, " weights shape:", heads_w.shape)
    for h in range(3):
        print(f"  head {h}: max weight {heads_w[h].max():.3f} "
              f"mean entropy {float(-(heads_w[h] * np.log(heads_w[h] + 1e-12)).sum(-1).mean()):.3f}")
    print("total attention entropy (nats), all heads:", 
          round(float(-(heads_w * np.log(heads_w + 1e-12)).sum(-1).mean()), 3))

    print("\n" + "=" * 78)
    print("6. Sinusoidal position encodings, first 8 positions of d=16")
    print("=" * 78)
    pe = sinusoidal_positions(8, 16)
    print(np.round(pe[:4, :8], 3))
    print("dot product of neighbouring position vectors:",
          [round(float(pe[i] @ pe[i + 1]), 1) for i in range(3)])

    print("\n" + "=" * 78)
    print("7. distilgpt2 attention on a real sentence")
    print("=" * 78)
    sentence = "The library opens at eight and closes at eleven on weekdays."
    prof = attention_profile(sentence)
    print(f"tokens ({prof['tokens']}):", prof["pieces"])
    print(f"{'layer':>5} {'entropy':>8} {'max':>6} {'self':>7} {'mean |i-j|':>11}")
    for L in prof["layers"]:
        print(f"{L['layer']:5d} {L['mean_entropy']:8.3f} {L['max_entropy']:6.3f} "
              f"{L['self_mass']:7.3f} {L['mean_distance']:11.3f}")
    print("\nhead entropies, layer 0:", prof["layers"][0]["head_entropies"])
    print("head entropies, layer 5:", prof["layers"][-1]["head_entropies"])

    print("\n" + "=" * 78)
    print("8. Next-token distribution for two prompts")
    print("=" * 78)
    for prompt in ("The library opens at", "The capital of France is"):
        rows = next_token_report(prompt)
        print(f"  {prompt!r}")
        for r in rows:
            print(f"    {r['token']!r:12s} p={r['p']:.4f}")
        print(f"    top-5 mass: {sum(r['p'] for r in rows):.4f}")


if __name__ == "__main__":
    main()
