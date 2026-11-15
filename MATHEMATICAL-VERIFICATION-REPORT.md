# Mathematical Verification Report — Phase 23

**Method.** A harness (`_math_verify.py`, kept in the repository root as the audit artefact) re-derives
each claim independently of the course code: a second implementation, brute-force enumeration, a
finite-difference gradient, a reference library, or a truth table. **32 checks, 32 pass, 0 fail.**
Every check below was executed on this machine; the quoted numbers are the harness output.

## 1. Search and complexity

| Claim in the course | Independent check | Result |
| :--- | :--- | :--- |
| UCS returns the minimum-cost path | 120 random weighted graphs vs an independently written Dijkstra | PASS — costs equal to 1e-9 |
| A* is optimal with an admissible, consistent heuristic | same 120 graphs with exact distance-to-goal heuristic | PASS — costs equal to 1e-9 |
| Manhattan distance is consistent on a 4-connected grid | max over all edges of h(u) − c − h(v) | PASS — maximum exactly 0.0 |
| Greedy best-first is not optimal | 200 random graphs | PASS — suboptimal on 146/200 |
| Eight-queens conflict count is the number of attacking pairs | known solution and a full row | PASS — 0 and 28 (= C(8,2)) |

The lessons' complexity table (BFS O(b^d), UCS O(b^(1+C*/ε)), A* O(b^d) worst case with an admissible
heuristic) is consistent with the implementations: all three use a heap or a queue with a visited/best
map, and none re-expands a node whose recorded cost is already better.

**Reviewer observation (not a defect):** `astar` returns as soon as it pops the goal and reports the `g`
stored with that entry. That is optimal only when `h(goal) = 0`. The lessons always use h(goal)=0, but the
function does not enforce it; a student supplying a non-zero goal heuristic would get a suboptimal answer
without an error. A docstring note would close this.

## 2. Logic

| Claim | Check | Result |
| :--- | :--- | :--- |
| Unification includes an occurs check | `unify(x, f(x))` | PASS — returns `None` |
| Unification returns an MGU and composes substitutions | `p(X,b)` vs `p(a,Y)`; `p(a)` vs `p(b)` | PASS — {X/a, Y/b}; constants do not unify |
| Resolution is sound | KB {∀x human(x)→mortal(x), human(socrates)} ⊢ mortal(socrates)? and ⊢ mortal(plato)? | PASS — proved the first, refused the second |
| Implication matches its truth table | (P→Q) vs ¬P∨Q on four rows; modus ponens entailment | PASS — all four rows and both entailment directions |

During the audit an apparent soundness failure was traced to the harness reading `(bool, trace)` as a
truthy tuple; the implementation was correct. This is recorded because it is exactly the kind of false
positive an audit must not report as a defect.

Propositional model checking (`entails`) enumerates all assignments, so it is exponential by construction;
the lesson says so and points to resolution for the first-order case.

## 3. Probability

| Claim | Check | Result |
| :--- | :--- | :--- |
| Variable elimination equals the joint | 5-variable alarm network, 4 queries including evidence and a custom elimination order, vs brute-force enumeration | PASS — agreement to 1e-10; joint normalises to 1.0 |
| Bayes rule is internally consistent | P(P)=0.10, P(W)=0.2581, P(P|W)=P(P,W)/P(W) computed by full enumeration | PASS — equal to 1e-12; posterior sums to 1 |
| Factor arithmetic is correct | product, restrict, sum-out, normalise exercised by the VE comparison above | PASS |

The factor implementation stores `True` at index 0 on every axis and documents it, because NumPy's
integer indexing would otherwise make `table[(True, …)]` resolve to the `False` slice (`True == 1`). This
is a real trap that the code anticipates and explains.

## 4. Machine learning

| Claim | Check | Result |
| :--- | :--- | :--- |
| OLS closed form | coefficients vs `numpy.linalg.lstsq` | PASS — 1e-8 |
| Ridge closed form | coefficients vs (XᵀX+λI)⁻¹Xᵀy | PASS — 1e-6 |
| R² definition | 1 − SS_res/SS_tot on random vectors | PASS — 1e-12 |
| Gaussian naive Bayes | posterior vs hand-computed Gaussian likelihoods | PASS — 1e-8 |
| Gradient descent converges to OLS | 4,000 epochs, lr 0.05, 200 samples | PASS — final loss 0.002375, coefficients within 0.05 |
| Decision trees fit separable Boolean functions | AND and OR with depth 2 | PASS — 4/4 each |

**Documented limitation:** a greedy CART with a *strictly positive* gain requirement cannot split XOR,
because every single-feature split at the root reduces Gini impurity by exactly zero. The course does not
claim otherwise (no XOR claim appears in M06), and standard implementations behave the same way unless
zero-gain splits are permitted. It is recorded here so a future author does not mistake it for a bug.

## 5. Neural networks and attention

| Claim | Check | Result |
| :--- | :--- | :--- |
| Backpropagation matches numerical gradients | central differences on an MLP with 8 weights sampled per layer | PASS — max relative error 7.6e-9 |
| Softmax is a distribution and shift-invariant | rows sum to 1; `softmax(z+100)=softmax(z)` | PASS — 1e-12 |
| Additive attention is a distribution and respects masks | random encoder/decoder states with a 2-position mask | PASS — rows sum to 1, masked weights < 1e-7 |
| Attention formula matches Bahdanau | `score = vᵀ tanh(W_h h_enc + W_s s_dec)`, softmax over source, context = Σ α h | PASS — code matches the stated equation term for term |

The stacked attention block in M07 is cross-attention over encoder states; its mask is applied before
softmax, which is the correct order. No causal-mask claim is made for the encoder-decoder model, and the
causal language model in M08 uses a separate triangular mask.

## 6. Computer vision metrics

| Claim | Check | Result |
| :--- | :--- | :--- |
| Convolution is a correlation with zero padding in "same" mode | vs `scipy.signal.convolve2d` with a symmetric kernel | PASS — 3.3e-16 |
| Otsu threshold matches the reference implementation | bimodal image vs `skimage.filters.threshold_otsu` | PASS — 103.6/255 vs 105.2/255 |
| IoU uses (x, y, w, h) boxes | analytic 50/150 = 0.333 | PASS |
| Dice = 2|A∩B|/(|A|+|B|) | 4-pixel overlap of two 16-pixel masks | PASS — 0.25 |
| mIoU is the mean over the requested labels | two-label mean 72/96 and 4/28 | PASS — 0.4464 |
| NMS suppresses overlapping lower-score boxes | three boxes, one overlapping pair | PASS — keeps [0, 2] |

**Defect found and fixed:** `otsu_threshold` accepted a `bins` argument it never used, and it deduced the
intensity scale by casting to `uint8`. On an image normalised to [0, 1] every pixel truncated to 0 and the
function returned 0.0 — silently, with no error, producing an all-foreground mask. The implementation now
quantises the observed range into `bins` levels and returns the threshold in the input's own units, so the
uint8 and [0, 1] copies of one image split in the same place (verified to within 4/255 against skimage).
A regression assertion for the float case was added to `vision_core.run_tests()`, and the notebook that
uses the function was re-executed (10.1 s, 0 errors).

## 7. Reinforcement learning

| Claim | Check | Result |
| :--- | :--- | :--- |
| Value iteration satisfies Bellman optimality | max residual after convergence | PASS — 2.9e-12, 22 sweeps |
| Policy iteration and value iteration agree | max |V_pi − V*| on a slippery maze | PASS — 0.0 |
| Exact policy value matches iterative evaluation | closed-form linear solve vs 1e-12 iteration | PASS — 0.0 |
| Q-learning learns a usable policy | 800 episodes, then 50 greedy evaluation episodes | PASS — success 1.00, return 0.800 vs V*=1.000 |
| SARSA is safer than Q-learning on cliff walking | 300 episodes × 3 seeds | PASS — −32.42 vs −35.83 |
| TD(0) converges to V_pi | 3,000 episodes on FrozenLake vs exact solve | PASS |

The Bellman equations in the lessons use the same convention as the code: `V(s) = Σ p(s'|s,a)[r + γV(s')]`
for evaluation and `V(s) = max_a Q(s,a)` for optimality, with terminal states excluded from backup. The TD
targets use `r` for terminal transitions and `r + γ max Q` otherwise, which is the correct episodic form.

## 8. Generative models

VAE loss (reconstruction + KL), GAN min-max objective, diffusion forward/noise-prediction parameterisation
and LoRA's low-rank update `W + (α/r)BA` are stated correctly in M11 and implemented with matching
shapes. These were checked by reading the code against the stated equations and by the notebook execution
(loss curves finite, samples the right shape), **not** by a numerical identity test — there is no
closed-form target for a trained generator. That distinction is stated in the verdict.

## 9. What was not verified

- **Large-model claims** (transformer scaling, emergent behaviour, frontier LLM quality) are citations,
  not reproducible experiments; no attempt was made to verify them.
- **Probability and fuzzy inference** were checked through the alarm network and defuzzification
  behaviour, not through an exhaustive audit of every fuzzy rule in M05.
- **Optimisation theory** (convexity, convergence rates) is stated in M06/M07 without proof; the checks
  above confirm the implementations, not the theorems.
- Statistical claims about model comparisons rest on the course's own resampling code; no independent
  significance testing was performed.

## 10. Conclusion

Every quantitative claim that could be recomputed independently was recomputed and agreed, except one
genuine implementation defect (`otsu_threshold`), which is fixed and regression-tested. The mathematics
taught in the lessons is correct at the level it is pitched, and the explanations do not mislead where the
formulas are simplified.
