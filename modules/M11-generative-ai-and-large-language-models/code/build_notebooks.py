"""build_notebooks.py -- generate and execute the M11 notebooks (maintainer tool).

Writes the two notebooks from source cells, runs them with nbclient against the
module's own code, and stores them with outputs stripped so the repository stays
small. The code cells are exactly the calls used in the lessons, so a notebook
that stops running is a signal that the module code changed behaviour.

    python build_notebooks.py            # build, execute, strip
    python build_notebooks.py --keep     # keep outputs for inspection
"""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "notebooks"


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(src: str):
    return nbf.v4.new_code_cell(src.strip("\n"))


NB1 = [
    md("""
# NB-11-01 — Tokens, Attention and Generative Models

This workbench accompanies L11-01 and L11-02. Every number printed here comes from the
module's own code on your machine; the tests are deterministic (fixed seeds, greedy decoding)
so the values should match the lessons to the printed precision.

Run the cells in order. The first model load takes longer than the rest.
"""),
    code("""
import sys, time
sys.path.insert(0, ".")

import numpy as np
import matplotlib.pyplot as plt

from gen_data import HANDBOOK
texts = [d["text"] for d in HANDBOOK.values()]
print("documents:", len(texts))
print("words:", sum(len(t.split()) for t in texts))
print("characters:", sum(len(t) for t in texts))
"""),
    md("""
## 1. Tokenisation

BPE learns merges from the corpus. Eighteen merges on a 37-symbol base alphabet produce a
55-symbol vocabulary — a toy version of what a real tokeniser does 50,000 times.
"""),
    code("""
from tokenizers_lab import learn_bpe, apply_bpe, bpe_vocab_size, compare_granularities, token_report

merges, history = learn_bpe(texts, num_merges=12)
print("merges learned:", len(merges), "vocab:", bpe_vocab_size(merges, 37))
for w in ("library", "students", "mitigating"):
    print(f"{w:12s} -> {apply_bpe(w, merges)}")

s = "Northfield University charges 9,250 GBP for undergraduate tuition."
g = compare_granularities(s)
print({k: g[k] for k in ("characters", "words", "subword_tokens", "chars_per_token")})
print(g["subword_pieces"])

rep = token_report(texts)
print({k: rep[k] for k in ("tokens", "chars_per_token", "tokens_per_word", "vocab_used")})
"""),
    md("""
## 2. Attention by hand

The scaled dot-product formula, one head, every intermediate value printed. Note that the
softmax weights are never one-hot — that softness is what makes attention differentiable.
"""),
    code("""
from attention_lab import (scaled_dot_product_attention, causal_mask, softmax_saturation,
                           multi_head_attention, sinusoidal_positions)

q = np.array([[1.0, 0.0]]); k = np.eye(2); v = np.array([[10.0, 0.0], [0.0, 20.0]])
out, w, scores = scaled_dot_product_attention(q, k, v, return_weights=True)
print("scores", scores, "weights", w, "output", out)

print(causal_mask(4))
for d_k in (4, 64, 256):
    r = softmax_saturation(d_k)
    print(f"d_k={d_k:4d} raw max {r['raw_max_weight']:.4f} entropy {r['raw_entropy']:.4f}"
          f" | scaled max {r['scaled_max_weight']:.4f} entropy {r['scaled_entropy']:.4f}")

pe = sinusoidal_positions(8, 16)
print(pe[:3, :6].round(3))
"""),
    md("""
## 3. What a pretrained model's heads do

distilgpt2 has 6 layers and 12 heads. On a 13-token sentence, attention sharpens with depth
and looks further back — measured, not assumed.
"""),
    code("""
from attention_lab import attention_profile, next_token_report

prof = attention_profile("The library opens at eight and closes at eleven on weekdays.")
print("tokens:", prof["tokens"])
for L in prof["layers"]:
    print(f"layer {L['layer']}  entropy {L['mean_entropy']:.3f}  "
          f"self {L['self_mass']:.3f}  lookback {L['mean_distance']:.3f}")

for row in next_token_report("The library opens at")[:3]:
    print(f"  {row['token']!r:10s} p={row['p']:.4f}")
"""),
    md("""
## 4. Three generative families, one metric

`gen_models.py` trained a VAE, a GAN and a diffusion model on the same 1,797 8×8 digits. The
differences below are the lesson: the GAN's loss looked fine while it covered three classes.
"""),
    code("""
data = np.load("gen_samples.npz")
fig, axes = plt.subplots(4, 8, figsize=(10, 5))
for row, name in enumerate(["real", "vae", "gan", "ddpm"]):
    for col in range(8):
        axes[row, col].imshow(data[name][col].reshape(8, 8), cmap="gray", vmin=0, vmax=1)
        axes[row, col].axis("off")
    axes[row, 0].set_title(name, loc="left", fontsize=10)
plt.tight_layout(); plt.show()

fig, ax = plt.subplots(1, 2, figsize=(10, 3))
ax[0].plot(data["vae_loss"]); ax[0].set_title("VAE loss"); ax[0].set_xlabel("epoch")
ax[1].plot(data["gan_d"], label="D"); ax[1].plot(data["gan_g"], label="G")
ax[1].set_title("GAN losses"); ax[1].legend()
plt.tight_layout(); plt.show()
print("ddpm first/last 100 mean:", data["ddpm_loss"][:100].mean().round(4),
      data["ddpm_loss"][-100:].mean().round(4))
"""),
    md("""
## 5. Decoding is a policy

The same model and prompt, seven decoding strategies. Greedy collapses to newlines here;
nucleus sampling with a temperature and a repetition penalty is the only varied output.
"""),
    code("""
from llm_gen import sample_text, perplexity

configs = [("greedy", dict(greedy=True)), ("T 0.7", dict(temperature=0.7)),
           ("T 1.0", dict(temperature=1.0)), ("top-p 0.9", dict(top_p=0.9)),
           ("top-k 40", dict(top_k=40))]
for name, kw in configs:
    r = sample_text("The library opens at", **kw)
    print(f"{name:12s} entropy {r['mean_entropy']:.3f} distinct2 {r['distinct_2']:.2f} "
          f"rep {r['repetition_rate']:.2f} -> {r['text'][:38]!r}")

print(perplexity("The wellbeing service offers free, confidential counselling."))
"""),
    md("""
## Exercises

1. Change `num_merges` to 40 and report the vocabulary size and how `mitigating` splits.
2. Compute attention with `d_k=16` and a 2-key example by hand, then verify in code.
3. Train the VAE with `beta=4.0` and compare sample diversity with `beta=1.0`.
4. Find a prompt where greedy decoding is *better* than sampled decoding, and explain why.
"""),
]

NB2 = [
    md("""
# NB-11-02 — Retrieval, Prompting and Evaluation

This workbench accompanies L11-04, L11-05 and L11-07. It builds the RAG assistant over the
24-document handbook, compares retrievers, tests two prompt templates, and scores the results
at every stage.
"""),
    code("""
import sys
sys.path.insert(0, ".")

import numpy as np
from gen_data import QA, UNANSWERABLE, HANDBOOK
from rag import RAGSystem, evaluate_retrievers, build_context

system = RAGSystem()
print("documents:", len(system.docs), "chunks:", len(system.chunks))
print("embedding dim:", system.dense.embs.shape[1],
      "backend:", "faiss" if system.dense.faiss else "numpy")
"""),
    md("""
## 1. Retrieval quality

Dense, lexical and hybrid retrieval on 30 labelled questions. BM25 wins at rank 1 because the
questions quote the handbook almost verbatim; fusion fixes the dense misses.
"""),
    code("""
res = evaluate_retrievers(system, QA)
print(f"{'retriever':16s} {'R@1':>6} {'R@3':>6} {'MRR':>6} {'nDCG@3':>7}")
for name, rep in res.items():
    print(f"{name:16s} {rep['recall@1']:6.2f} {rep['recall@3']:6.2f} "
          f"{rep['mrr']:6.3f} {rep['ndcg@3']:7.3f}")
"""),
    md("""
## 2. One question through the pipeline

Watch the ranking change at each stage, then read the context the generator actually saw.
"""),
    code("""
q = "How much is the accommodation deposit and when is it refunded?"
for name, index in (("bm25", system.bm25), ("dense", system.dense), ("hybrid", system.hybrid)):
    hits = index.search(q, 3)
    print(f"{name:8s}", [(system.chunks[i].chunk_id, round(s, 2)) for i, s in hits])

out = system.answer(q)
print("answer:", out["answer"], "| docs:", out["docs"], "| support:", round(out["support"], 2))
print(out["context"][:300])
"""),
    md("""
## 3. Prompts, measured

Two templates, six questions, one model. Few-shot costs twice the prompt tokens here; whether
it helps is a question for the data, not for intuition.
"""),
    code("""
from prompts import TEMPLATES, render, generate
from llm_eval import answer_report

for name in ("zero-shot", "few-shot"):
    preds = []
    for item in QA[:6]:
        p = render(TEMPLATES[name], HANDBOOK[item["source"]]["text"], item["q"])
        text, _ = generate(p)
        preds.append(text)
    rep = answer_report([(p, i["a"]) for p, i in zip(preds, QA[:6])])
    print(f"{name:10s} EM {rep['exact_match']:.2f} F1 {rep['token_f1']:.2f} "
          f"mean chars {np.mean([len(p) for p in preds]):.1f}")
    print("   ", preds[:3])
"""),
    md("""
## 4. Evaluation at every stage

Retrieval, answers, grounding, refusal behaviour and cost — reported separately, because a
single end-to-end number hides which stage failed.
"""),
    code("""
from llm_eval import support_rate, unsupported_numbers, is_refusal

pairs, supports = [], []
for item in QA[:12]:
    o = system.answer(item["q"])
    pairs.append((o["answer"], item["a"]))
    supports.append(o["support"])
rep = answer_report(pairs)
print("EM", round(rep["exact_match"], 2), "F1", round(rep["token_f1"], 2),
      "support", round(float(np.mean(supports)), 2))

answers = [system.answer(q)["answer"] for q in UNANSWERABLE]
print("refusal rate on unanswerable:", round(np.mean([is_refusal(a) for a in answers]), 2))
for q, a in list(zip(UNANSWERABLE, answers))[:4]:
    print("   ", q[:44], "->", a)

ctx = HANDBOOK["hb-01"]["text"]
print("support:", round(support_rate("The library opens at 07:00.", ctx), 2),
      "unsupported numbers:", unsupported_numbers("The library opens at 07:00.", ctx))
"""),
    md("""
## 5. Where it goes wrong

Two failures from the twelve questions above, both invisible to the retrieval metrics:
a right document with the wrong span, and a number from the wrong section.
"""),
    code("""
for item in QA[:8]:
    o = system.answer(item["q"])
    flag = "OK " if o["answer"].strip().lower() == item["a"].strip().lower() else "ERR"
    print(f"{flag} {item['q'][:48]:48s} -> {o['answer']!r} (gold {item['a']!r})")
"""),
    md("""
## Exercises

1. Set the fusion weight `alpha` to 0.0 and 1.0 and explain the two endpoints.
2. Add a refusal threshold on the top retrieval score and report refusal and over-refusal.
3. Build five questions that need two documents and see whether retrieval finds both.
4. Replace MaxSim reranking with a cross-encoder and compare nDCG@3 and latency.
"""),
]


def build(cells, path: Path, execute: bool, keep: bool) -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3",
                                 "language": "python"}
    nb.metadata["language_info"] = {"name": "python"}
    if execute:
        client = NotebookClient(nb, timeout=900, kernel_name="python3",
                                resources={"metadata": {"path": str(HERE)}})
        client.execute()
        if not keep:
            for cell in nb.cells:
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None
    path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, str(path))
    print(f"wrote {path.relative_to(HERE.parent)} ({len(nb.cells)} cells)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true", help="keep cell outputs")
    ap.add_argument("--no-exec", action="store_true", help="write without executing")
    args = ap.parse_args()
    build(NB1, OUT / "nb-11-01-tokens-attention-and-generative-models.ipynb",
          not args.no_exec, args.keep)
    build(NB2, OUT / "nb-11-02-retrieval-prompting-and-evaluation.ipynb",
          not args.no_exec, args.keep)


if __name__ == "__main__":
    main()
