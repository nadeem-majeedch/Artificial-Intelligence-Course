"""lora.py -- LoRA from scratch, training and merging (M11, L11-06 / LAB-11-03).

Low-rank adaptation (Hu et al., 2021) freezes the pretrained weights and learns
a rank-r update to selected projections:

    W' = W + (alpha / r) * B A,     A in R^(d_in x r),  B in R^(r x d_out)

Only A and B are trained -- a fraction of a percent of the parameters. This file
implements the wrapper, applies it to a real pretrained model (distilgpt2),
trains on a small in-domain question/answer set, reports the trainable-parameter
budget and the held-out loss before and after, then merges the update back and
verifies that merging preserves the model's outputs.

No `peft` is used: the point is to see the twenty lines that matter. `peft` is
the production choice and is installed, but you should know what it wraps.

Run ``python lora.py``. Numbers quoted in L11-06 come from here.
"""

from __future__ import annotations

import math
import time

import torch
import torch.nn as nn

from gen_data import HANDBOOK, QA

MODEL = "distilgpt2"


# ---------------------------------------------------------------------------
# 1. The layer
# ---------------------------------------------------------------------------

class LoRALayer(nn.Module):
    """Wrap a Linear or transformers Conv1D with a frozen base plus a low-rank update."""

    def __init__(self, base: nn.Module, r: int = 8, alpha: float = 16.0):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad = False

        if isinstance(base, nn.Linear):
            d_in, d_out = base.in_features, base.out_features
            self.weight_is_transposed = False
        else:                                   # transformers Conv1D: weight is (d_in, d_out)
            d_in, d_out = base.weight.shape
            self.weight_is_transposed = True

        self.A = nn.Parameter(torch.empty(d_in, r))
        self.B = nn.Parameter(torch.zeros(r, d_out))
        nn.init.normal_(self.A, std=0.02)
        self.scale = alpha / r
        self.r, self.alpha = r, alpha

    def forward(self, x):
        return self.base(x) + self.scale * (x @ self.A @ self.B)


def apply_lora(model, r: int = 8, alpha: float = 16.0,
               targets=("c_attn", "c_proj", "c_fc")) -> dict:
    """Replace the named projections in place; returns a small report."""
    from transformers.pytorch_utils import Conv1D

    replaced = 0
    for name in [n for n, _ in model.named_modules()]:
        leaf = name.rsplit(".", 1)[-1]
        if leaf not in targets:
            continue
        module = model.get_submodule(name)
        if not isinstance(module, (nn.Linear, Conv1D)):
            continue
        parent = model.get_submodule(name.rsplit(".", 1)[0])
        setattr(parent, leaf, LoRALayer(module, r, alpha))
        replaced += 1
    for p in model.parameters():
        p.requires_grad = False
    for module in model.modules():
        if isinstance(module, LoRALayer):
            module.A.requires_grad = True
            module.B.requires_grad = True
    return {"layers_replaced": replaced, **param_report(model)}


def param_report(model) -> dict:
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"total": total, "trainable": trainable,
            "trainable_pct": 100.0 * trainable / total}


def merge_lora(model) -> int:
    """Fold scale * B A into the base weight and restore the plain module."""
    merged = 0
    for name in [n for n, m in model.named_modules() if isinstance(m, LoRALayer)]:
        layer = model.get_submodule(name)
        delta = layer.scale * (layer.A @ layer.B)          # (d_in, d_out)
        with torch.no_grad():
            if layer.weight_is_transposed:                 # Conv1D weight is (d_in, d_out)
                layer.base.weight += delta
            else:
                layer.base.weight += delta.T
        parent_name, leaf = name.rsplit(".", 1)
        setattr(model.get_submodule(parent_name), leaf, layer.base)
        merged += 1
    return merged


# ---------------------------------------------------------------------------
# 2. A small in-domain training set
# ---------------------------------------------------------------------------

def qa_pairs(n: int = 40) -> list[str]:
    """Format handbook QA as next-token-prediction examples."""
    rows = []
    for item in QA[:n]:
        rows.append(f"Question: {item['q']}\nAnswer: {item['a']}")
    return rows


def tokenise(tok, texts, max_len: int = 96):
    enc = tok(list(texts), padding=True, truncation=True, max_length=max_len,
              return_tensors="pt")
    labels = enc["input_ids"].clone()
    labels[enc["attention_mask"] == 0] = -100
    return enc["input_ids"], enc["attention_mask"], labels


@torch.no_grad()
def held_out_loss(model, tok, texts) -> float:
    model.eval()
    ids, mask, labels = tokenise(tok, texts)
    out = model(input_ids=ids, attention_mask=mask, labels=labels)
    model.train()
    return float(out.loss)


# ---------------------------------------------------------------------------
# 3. Train
# ---------------------------------------------------------------------------

def train_lora(steps: int = 40, batch_size: int = 2, lr: float = 1e-3, r: int = 8,
               alpha: float = 16.0, seed: int = 0, max_len: int = 96) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.manual_seed(seed)
    tok = AutoTokenizer.from_pretrained(MODEL)
    tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    report = apply_lora(model, r=r, alpha=alpha)

    rows = qa_pairs(40)
    train_texts, held_out = rows[:-6], rows[-6:]
    base_model = AutoModelForCausalLM.from_pretrained(MODEL)
    base_loss = held_out_loss(base_model, tok, held_out)
    before = held_out_loss(model, tok, held_out)

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)
    model.train()
    losses = []
    t0 = time.perf_counter()
    for step in range(steps):
        batch = [train_texts[(step * batch_size + i) % len(train_texts)]
                 for i in range(batch_size)]
        ids, mask, labels = tokenise(tok, batch, max_len)
        out = model(input_ids=ids, attention_mask=mask, labels=labels)
        opt.zero_grad()
        out.loss.backward()
        opt.step()
        losses.append(float(out.loss))
    seconds = time.perf_counter() - t0

    after = held_out_loss(model, tok, held_out)
    report.update({
        "base_loss": base_loss, "before_loss": before, "after_loss": after,
        "first_loss": losses[0], "last_loss": losses[-1],
        "mean_first5": sum(losses[:5]) / 5, "mean_last5": sum(losses[-5:]) / 5,
        "seconds": seconds, "model": model, "tok": tok, "r": r, "alpha": alpha,
        "losses": losses,
    })
    return report


def generation_check(model, tok, prompts, max_new_tokens: int = 16) -> list[str]:
    model.eval()
    out = []
    for prompt in prompts:
        enc = tok(prompt, return_tensors="pt")
        with torch.no_grad():
            ids = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False,
                                 pad_token_id=tok.eos_token_id)
        out.append(tok.decode(ids[0], skip_special_tokens=True))
    return out


# ---------------------------------------------------------------------------
# 4. Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 86)
    print("1. Parameter budget of LoRA on distilgpt2")
    print("=" * 86)
    from transformers import AutoModelForCausalLM

    for r in (4, 8, 16):
        model = AutoModelForCausalLM.from_pretrained(MODEL)
        rep = apply_lora(model, r=r)
        print(f"  r={r:2d}: {rep['layers_replaced']:2d} layers wrapped, "
              f"trainable {rep['trainable']:7,d} / {rep['total']:,d} = "
              f"{rep['trainable_pct']:.3f}%")
    del model

    print("\n" + "=" * 86)
    print("2. Train LoRA (r=8) for 40 steps on 34 handbook Q/A pairs")
    print("=" * 86)
    t0 = time.time()
    res = train_lora()
    print(f"  wall clock            : {res['seconds']:.1f}s training, {time.time() - t0:.1f}s total")
    print(f"  trainable parameters  : {res['trainable']:,} ({res['trainable_pct']:.3f}% of "
          f"{res['total']:,})")
    print(f"  held-out loss         : base {res['base_loss']:.3f} -> "
          f"before {res['before_loss']:.3f} -> after {res['after_loss']:.3f}")
    print(f"  training loss         : first {res['first_loss']:.3f}  "
          f"first-5 mean {res['mean_first5']:.3f}  last-5 mean {res['mean_last5']:.3f}")
    print(f"  loss path             : "
          f"{[round(float(x), 2) for x in res['losses'][::5]]}")

    print("\n" + "=" * 86)
    print("3. Generation before and after adaptation")
    print("=" * 86)
    prompts = ["Question: What is the accommodation deposit?\nAnswer:",
               "Question: When does the library open on weekdays?\nAnswer:"]
    from transformers import AutoModelForCausalLM

    base = AutoModelForCausalLM.from_pretrained(MODEL)
    base.eval()
    tok = res["tok"]
    before = generation_check(base, tok, prompts, 12)
    after = generation_check(res["model"], tok, prompts, 12)
    for p, b, a in zip(prompts, before, after):
        print(f"  prompt: {p.splitlines()[0]}")
        print(f"    base  -> {b!r}")
        print(f"    LoRA  -> {a!r}")
    print("  (twelve tokens; the adapter shifts style, it does not add facts)")

    print("\n" + "=" * 86)
    print("4. Merge the adapter back into the weights")
    print("=" * 86)
    fixed = tok("Question: How many items can I borrow?\nAnswer:", return_tensors="pt")
    with torch.no_grad():
        logits_before = res["model"](**fixed).logits.clone()
    merged = merge_lora(res["model"])
    with torch.no_grad():
        logits_after = res["model"](**fixed).logits.clone()
    diff = float((logits_before - logits_after).abs().max())
    total = sum(p.numel() for p in res["model"].parameters())
    print(f"  merged {merged} layers; trainable parameters now "
          f"{sum(p.numel() for p in res['model'].parameters() if p.requires_grad)}")
    print(f"  max |logit before - logit after| = {diff:.2e}")
    print(f"  parameter count restored to {total:,} (no extra weights at inference)")

    print("\n" + "=" * 86)
    print("5. What to compare before shipping an adapter")
    print("=" * 86)
    print("  size on disk  : base 328 MB (fp32) vs adapter "
          f"{res['trainable'] * 4 / 1e6:.1f} MB")
    print("  quality       : held-out loss and task metric, not training loss")
    print("  base vs tuned : run both on the same fixed evaluation set")
    print("  licence       : the base model's licence governs the merged weights")


if __name__ == "__main__":
    main()
