# AA-02 — Complexity Analysis of a Training Pipeline

| | |
| :--- | :--- |
| Assignment | 02 |
| Difficulty | Intermediate |
| Estimated time | 2 hours |
| Prerequisites | P02, M06, M07 |
| Format | Derivation and analysis |
| Covers | asymptotic analysis, memory accounting, bottlenecks |

[Assessment index](../README.md) · [Analytical assignments](README.md)

## Background

"O(n²)" tells you how something scales, not whether it fits. A pipeline's real cost is a sum of
terms, one of which usually dominates — and it is often not the one people optimise.

## Problem scenario

A model has $d=512$ hidden units, $L=6$ layers, batch size $B=64$, sequence length $T=256$, and a
vocabulary of 32,000. Analyse training cost for one step.

## Learning outcomes

1. Derive parameter counts for embedding, attention and feed-forward blocks.
2. Derive FLOPs and activation memory for one forward pass.
3. Identify the dominant term for realistic values.
4. Explain the effect of batch size and sequence length separately.

## Tasks

1. **Parameters.** Embedding, per-layer attention ($W_Q,W_K,W_V,W_O$), feed-forward
   ($d\to4d\to d$), and output projection; give totals.
2. **FLOPs.** Forward FLOPs for the attention and feed-forward blocks as functions of $B,T,d,L$;
   evaluate at the given values.
3. **Memory.** Activation memory for one layer (store what backprop needs); multiply by $L$ and $B$.
4. **Dominant term.** Which term dominates at $T=256$? At $T=8{,}192$? Explain the crossover.
5. **Implication.** State one optimisation that follows from the analysis and one that does not.

## Constraints

- Show every formula before substituting.
- Use FLOPs as $2\times$ multiply-accumulate count; state this convention.
- Ignore constants below 1% of the total, and say which you ignored.

## Expected deliverables

A written derivation with a table of values at $T=256$ and $T=8{,}192$.

## Evaluation rubric

| Criterion | Weight | What is checked |
| :--- | ---: | :--- |
| Parameter derivation | 25% | correct counts with working |
| FLOP analysis | 30% | expressions correct, substitution right |
| Memory analysis | 20% | activation accounting, not just weights |
| Crossover explanation | 15% | attention vs FFN dominance explained |
| Implications | 10% | optimisation follows from the numbers |

## Bonus challenges

- Include the KV cache in inference memory and compute its size at $T=8{,}192$.
- Repeat with $d=128$ and explain how the dominant term changes.

---

[Assessment index](../README.md) · [AA-01](aa-01-algorithm-comparison.md) · [AA-03](aa-03-mathematical-derivation.md)
