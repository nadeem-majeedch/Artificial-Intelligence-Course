# M01 — Module Summary and References

[← Module home](README.md) · [Course home](../../README.md) · [Next module: M02 →](../M02-intelligent-agents-and-environments/README.md)

A one-page recap of what M01 established, the formulas worth remembering, and where to read
further. Use it before the quiz and before starting M02.

## The five ideas worth keeping

1. **AI is goal-directed computation in partly known environments, not a product category.**
   Four flags — perceives, decides, adapts, goal-directed — turn an argument about vibes into an
   argument about mechanism. Narrow/general is about task scope; weak/strong is about minds.
2. **The AI winters were expectation–capability gaps, not technical extinctions.** Promises have
   compounded faster than delivered capability twice; the mechanism (brittleness, exponential cost,
   funding structure) still operates, so the questions you ask of a claim are timeless.
3. **Symbolic, learned and generative methods coexist because they fail differently.** A rule fails
   readably and needs maintenance; a model fails through drift and opacity. Choose the failure mode
   you can afford, and expect to combine both.
4. **An error rate is not an evaluation.** Multiply by volume, check calibration, look at the tail,
   and ask what the deployment changes about the data. Ten thousand errors a day at 99.5% accuracy
   is a department, not a rounding error.
5. **Reliability compounds, so verification beats optimism.** $0.95^{20} \approx 0.36$ without
   checks; a cheap per-step verifier lifts a twenty-step plan above 0.86. This is why agents need
   checkpoints, and why "it works in the demo" is a claim about one step.

## Formula sheet

| Quantity | Formula | Where |
| :--- | :--- | :--- |
| Capability score | $s(x)=\sum \mathbb{1}[\text{flag}]$, verdict from score and adaptation | [L01-01](lessons/L01-01-what-is-artificial-intelligence.md#6-mathematical-formulation) |
| Expectation–capability gap | $g(t)=P_0(1+\alpha)^t/(C_0+\beta t)$ | [L01-02](lessons/L01-02-history-and-ai-winters.md#6-mathematical-formulation) |
| Empirical and true error | $\hat R(f)=\frac1n\sum \mathbb{1}[f(x_i)\ne y_i]$, $R(f)=\mathbb E[\cdot]$ | [L01-03](lessons/L01-03-symbolic-statistical-generative.md#6-mathematical-formulation) |
| Errors per day | $N(1-a)$ | [L01-04](lessons/L01-04-ai-capabilities-and-limitations.md#6-mathematical-formulation) |
| Precision / recall | $TP/(TP+FP)$, $TP/(TP+FN)$ | [L01-04](lessons/L01-04-ai-capabilities-and-limitations.md#6-mathematical-formulation) |
| Expected calibration error | $\frac1B\sum_i\lvert \hat a_i-p_i\rvert$ | [L01-04](lessons/L01-04-ai-capabilities-and-limitations.md#6-mathematical-formulation) |
| Compounded plan failure | $p^n$ for $n$ independent steps | [L01-04](lessons/L01-04-ai-capabilities-and-limitations.md#5-worked-examples) |
| Retention | $R(t)=e^{-t/S}$ | [L01-05](lessons/L01-05-course-workflow-and-study-habits.md#6-mathematical-formulation) |

## Terms added to your vocabulary

| Term | One-line meaning |
| :--- | :--- |
| Narrow / general / superintelligent AI | task scope: one task / any intellectual task / beyond human across the board |
| Weak / strong AI | philosophical claim: simulation without mind / simulation as mind |
| Turing Test | behavioural test of indistinguishability in text conversation |
| AI winter | funding and credibility collapse after promises outrun capability |
| Symbolic vs connectionist | explicit rules and logic vs distributed weights learned from data |
| Inductive bias | the assumptions that make generalisation from examples possible |
| Calibration | agreement between stated confidence and observed accuracy |
| Distribution shift | change in inputs between training and deployment |
| Feedback loop | deployment changes the data the model will be trained on next |

Every term links from the [glossary](../../resources/glossary.md).

## Self-check before M02

- Can you score a described system and defend each flag?
- Can you explain a winter without naming a single villain?
- Can you say why a 96% accuracy claim is not yet evidence of anything?
- Can you compute ECE from three buckets, by hand?
- Can you compute the success probability of a twelve-step plan at 0.97 per step?

If any answer is no, the relevant lesson is one click away in the [module map](README.md#module-map).

## References

**Foundational**

- Turing, A. M. (1950). *Computing Machinery and Intelligence*. Mind 59(236), 433–460.
- McCarthy, J., Minsky, M., Rochester, N. & Shannon, C. (1955). *A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence*.
- Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain*. Psychological Review 65(6).

**Textbooks**

- Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. — Chapters 1–2 underpin this module.
- Mitchell, M. (2019). *Artificial Intelligence: A Guide for Thinking Humans*. Farrar, Straus and Giroux.
- Domingos, P. (2015). *The Master Algorithm*. Basic Books.

**On evaluation and its failure modes**

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. (2017). *On Calibration of Modern Neural Networks*. ICML.
- Sculley, D. et al. (2015). *Hidden Technical Debt in Machine Learning Systems*. NeurIPS.
- Pineau, J. et al. (2021). *Improving Reproducibility in Machine Learning Research*. JMLR 22.

**History and context**

- Crevier, D. (1993). *AI: The Tumultuous History of the Search for Artificial Intelligence*. Basic Books.
- Haenlein, M. & Kaplan, A. (2019). *A Brief History of Artificial Intelligence*. California Management Review 61(4).

## What comes next

[M02 — Intelligent Agents and Environments](../M02-intelligent-agents-and-environments/README.md) turns the
vocabulary of this module into running code: percepts, actions, rationality, PEAS descriptions, and
five agent architectures you implement yourself.
