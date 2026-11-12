# L01-02 — A Brief History of AI and the AI Winters

| Module | M01 · Introduction and Foundations of Artificial Intelligence |
| :--- | :--- |
| Level | 100 |
| Study time | 60 minutes |
| Prerequisites | [L01-01 What Is Artificial Intelligence?](L01-01-what-is-artificial-intelligence.md) |
| Notebook | [NB-01-01 Capability Test Bench](../notebooks/nb-01-01-capability-test-bench.ipynb) |
| Lab | [LAB-01-01 Claim Audit](../labs/lab-01-01-claim-audit.md) |

[← Previous: L01-01 What Is Artificial Intelligence? Definitions, Goals and Myths](L01-01-what-is-artificial-intelligence.md) · [Module home](../README.md) · [Next: L01-03 The Many Faces of AI: Symbolic, Statistical and Generative →](L01-03-symbolic-statistical-generative.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Reading a Hype Claim](#4-the-procedure-reading-a-hype-claim)
- [5. Worked Examples](#5-worked-examples)
- [6. Mathematical Formulation](#6-mathematical-formulation)
- [7. Python Implementation](#7-python-implementation)
- [8. Practical Applications](#8-practical-applications)
- [9. Common Mistakes](#9-common-mistakes)
- [10. Practical Exercises](#10-practical-exercises)
- [11. Self-Assessment](#11-self-assessment)
- [12. Key Terms](#12-key-terms)
- [13. Further Reading](#13-further-reading)
- [What to Do Next](#what-to-do-next)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Order** the major eras of AI and their representative systems, from symbolic reasoning to generative models.
- **Explain** the two AI winters as consequences of a specific mechanism — a widening gap between promises and delivered capability — rather than as accidents or bad luck.
- **Identify** the recurring failure pattern behind over-optimistic claims, and apply it to a claim you meet today.
- **Evaluate** whether a current development is a capability advance, an engineering advance, or a change in expectations.

## 2. Prerequisite Knowledge

You should already be able to:

- State the four-clause definition of AI and apply the capability test — see [L01-01](L01-01-what-is-artificial-intelligence.md).
- Read a short Python loop and print formatted output — see [LP01-03](../../../prerequisites/P01-python-programming/lessons/LP01-03-conditionals-loops-and-comprehensions.md).

## 3. Conceptual Explanation

### 3.1 The intuition

Every field has a founding myth that hides its actual dynamics. Ours goes: "AI started in 1956, had two setbacks, and then deep learning fixed everything."

The setbacks were not random. They followed a pattern that repeats often enough to be predictable:

1. A **demonstration** works on a small, controlled problem.
2. A **claim** generalises it to a much wider class of problems.
3. **Funding** arrives on the strength of the claim.
4. The wider problems turn out to need something the method does not have — world knowledge, data, compute, robustness.
5. **Disappointment** arrives at the same time as the next promising method, and the two get confused in the retelling.

Call this the **expectation–capability gap**. It is the single most useful idea in this lesson, because you will see versions of it in job advertisements, startup decks and news headlines every year of your career.

### 3.2 The formal idea: three eras and two winters

| Era | Rough dates | Dominant idea | Representative systems | What ended it |
| :--- | :--- | :--- | :--- | :--- |
| **Symbolic optimism** | 1956–1974 | Intelligence is manipulation of symbols and logic | Logic Theorist, ELIZA, SHRDLU | Combinatorial explosion; brittleness outside toy domains; the 1973 Lighthill report cut UK funding |
| **Expert systems boom** | 1980–1987 | Encode expert rules; commercialise them | XCON, MYCIN | Maintenance cost of thousands of hand-written rules; Lisp-machine market collapse in 1987 |
| **Statistical and deep learning** | 1990s–present | Learn the mapping from data instead of writing the rules | Deep Blue (1997), Watson (2011), AlexNet (2012), AlphaGo (2016), transformers (2017), ChatGPT (2022) | Not ended; the current limits are reliability, cost and evaluation |

Two things about this table matter more than the dates.

First, **the eras overlap and recur**. Symbolic methods never disappeared: they run scheduling engines, database constraints and type checkers today, and they reappear inside modern systems as tool calls and structured outputs. The history is a spiral, not a relay race.

Second, **each winter was a funding and credibility event, not a technical extinction**. Research continued during both. What vanished was the assumption that the next grant would arrive without a working system.

### 3.3 Why the winters happened: the mechanism, stated plainly

Both winters share three structural causes.

**Brittleness under distribution shift.** A program that answers questions about coloured blocks (SHRDLU) is not a program that answers questions. Symbolic systems failed not on their examples but one step outside them. The same weakness still exists in learned systems, which is why this course spends so long on evaluation.

**Combinatorial explosion.** Early optimism assumed that faster hardware and better search would scale. It does not: search cost grows exponentially in depth, so a factor-of-ten speed-up buys you a few more levels of a game, not a new domain. Complexity analysis in M03 is the formal version of this lesson.

**The knowledge bottleneck.** Expert systems needed a person to write every rule. XCON reportedly carried thousands of rules and needed a maintenance team; when the experts retired, the rules became archaeology. This is precisely the bottleneck that machine learning attacks — learn the rules from data — and it explains why the statistical turn won.

The gap is measurable in the shape of public milestones. The intervals between landmark systems are not uniform: long stretches of slow visible progress sit between bursts.

### 3.4 Why it matters

The practical value of history is diagnostic. When you read "this new model can reason", you can ask the three questions the winters taught us: *on what distribution was it demonstrated, what is the growth rate of its cost, and who maintains the knowledge it depends on?* You can ask them about any claim in this course, and about your own project before someone else asks them for you.

### 3.5 What actually changed after 2012

The statistical turn was not one idea but three arriving together:

- **Data** — the web produced text and images at a scale no hand-labelling project could match.
- **Compute** — GPUs, originally for graphics, made large matrix multiplication affordable.
- **Algorithms** — deeper networks, better initialisation, ReLU activations and dropout made training them possible.

Remove any one and the others are useless: data without compute cannot be used, compute without data overfits, and both without the algorithmic fixes fail to train. This is why "AI progress" is never a single invention, and why capability forecasts that assume one bottleneck are usually wrong.

## 4. The Procedure: Reading a Hype Claim

```text
FUNCTION assess_claim(claim):
    domain      <- the exact problems the demo used
    wider       <- the problems the claim promises
    IF wider is much larger than domain:
        ask: what does the method lack for `wider`?
             (world knowledge / data scale / robustness / cost)
    IF no public evaluation on `wider`:
        label claim as EXTRAPOLATION, not result
    IF cost grows faster than the task size:
        label as LIMITED SCALE, state the exponent
    RETURN one sentence naming evidence, gap and missing ingredient
```

The procedure is a discipline for reading, not a formula for truth. Its output is a sentence you can defend.

## 5. Worked Examples

### Example 1 — Measuring the rhythm of progress

The table below lists thirteen public milestones and the gap between consecutive ones. Run the code in §7 and you get:

| Year | Gap | Milestone |
| ---: | ---: | :--- |
| 1956 | +6 | Dartmouth workshop — the name "AI" |
| 1958 | +2 | Perceptron |
| 1966 | +8 | ELIZA |
| 1972 | +6 | SHRDLU |
| 1980 | +8 | XCON expert systems in industry |
| 1987 | +7 | Backpropagation popularised |
| 1997 | +10 | Deep Blue beats Kasparov |
| 2011 | +14 | Watson wins *Jeopardy!* |
| 2012 | +1 | AlexNet |
| 2016 | +4 | AlphaGo |
| 2017 | +1 | Transformer architecture |
| 2022 | +5 | ChatGPT |

Grouped by era: **1950–1979** has four milestones with a mean gap of **5.50 years**; **1980–2011** has four with a mean gap of **9.75 years**; **2012 onward** has four with a mean gap of **2.75 years**.

Read the middle row carefully — it is the one students skip. The expert-systems boom and the second winter produced the *slowest* visible progress of the entire history, not because nothing was happening but because the field was consolidating after a collapse. Progress in AI is bursty, and a burst is usually the delayed payoff of work done in a quiet period.

### Example 2 — Applying the claim procedure to a real sentence

Claim: *"Our model passes the bar exam, so it can work as a junior lawyer."*

- **Domain of the demo:** multiple-choice and essay questions with no client, no consequences, no adversarial counterparty, and no need to verify facts.
- **Wider claim:** advising a client, where a confident wrong citation is a serious harm.
- **What the method lacks:** reliable retrieval of authoritative sources, calibrated uncertainty, accountability, and the ability to notice that the question itself is wrong.
- **Verdict:** this is an *extrapolation*. The capability claim (exam performance) is supported; the deployment claim is not.

Notice the shape: the sentence is not false, it is *under-specified*, and the missing specification is exactly what an evaluation would supply. That is the winter mechanism in miniature.

## 6. Mathematical Formulation

The expectation–capability gap can be written as a ratio that grows over time when promises compound faster than capability:

$$
g(t) = \frac{P(t)}{C(t)}, \qquad P(t) = P_0(1+\alpha)^t, \quad C(t) = C_0 + \beta t
$$

| Symbol | Meaning |
| :--- | :--- |
| $P(t)$ | promised capability at year $t$ (an index, not a physical quantity) |
| $C(t)$ | delivered capability, modelled as linear for illustration |
| $\alpha$ | annual growth rate of promises |
| $\beta$ | annual absolute gain in capability |

If $\alpha > 0$ while $\beta$ is constant, $g(t) \to \infty$: the gap widens without bound even though capability improves. This is the mathematical content of "the promises outran the results". Winter arrives when funders notice $g(t)$ is large — not when $C(t)$ stops growing.

The model is illustrative, deliberately simple, and worth criticising: real capability is not a scalar, and different tasks have different $\beta$. Use it to reason about the *shape* of the dynamic, never to forecast a date.

## 7. Python Implementation

```python
milestones = [
    (1950, "Turing test paper"),
    (1956, "Dartmouth workshop - the name 'AI'"),
    (1958, "Perceptron"),
    (1966, "ELIZA"),
    (1972, "SHRDLU"),
    (1980, "XCON expert systems in industry"),
    (1987, "Backpropagation popularised"),
    (1997, "Deep Blue beats Kasparov"),
    (2011, "Watson wins Jeopardy!"),
    (2012, "AlexNet"),
    (2016, "AlphaGo"),
    (2017, "Transformer architecture"),
    (2022, "ChatGPT"),
]

gaps = [later[0] - earlier[0] for earlier, later in zip(milestones, milestones[1:])]
for (year, event), gap in zip(milestones[1:], gaps):
    print(f"{year}  +{gap:2d} yr  {event}")


def mean_gap(low: int, high: int) -> tuple[float, int]:
    """Mean gap between milestones in [low, high)."""
    chosen = [gap for (year, _), gap in zip(milestones[1:], gaps) if low <= year < high]
    return sum(chosen) / len(chosen), len(chosen)


for low, high, label in [(1950, 1980, "1950-1979"), (1980, 2012, "1980-2011"), (2012, 2030, "2012 onward")]:
    average, count = mean_gap(low, high)
    print(f"{label}: {count} milestones, mean gap {average:.2f} years")
```

**Output**

```text
1956  + 6 yr  Dartmouth workshop - the name 'AI'
1958  + 2 yr  Perceptron
1966  + 8 yr  ELIZA
1972  + 6 yr  SHRDLU
1980  + 8 yr  XCON expert systems in industry
1987  + 7 yr  Backpropagation popularised
1997  +10 yr  Deep Blue beats Kasparov
2011  +14 yr  Watson wins Jeopardy!
2012  + 1 yr  AlexNet
2016  + 4 yr  AlphaGo
2017  + 1 yr  Transformer architecture
2022  + 5 yr  ChatGPT
1950-1979: 4 milestones, mean gap 5.50 years
1980-2011: 4 milestones, mean gap 9.75 years
2012 onward: 4 milestones, mean gap 2.75 years
```

The numbers match Example 1. Note what the measure *cannot* tell you: it measures how often the public noticed something, not how much capability was gained. A field can make steady internal progress with no headline, which is exactly what 1980–2011 looked like from outside.

## 8. Practical Applications

- **Technology due diligence.** Investors and procurement teams run this analysis before adopting a system: what was demonstrated, on what data, and what happens one step outside it. History supplies the checklist.
- **Research strategy.** Knowing that the knowledge bottleneck drove the statistical turn tells you why curated data and evaluation sets are treated as first-class research outputs rather than paperwork.
- **Public communication and policy.** Funding cycles respond to claimed capability. Being able to name the gap mechanism is what lets an engineer give an honest forecast instead of a number that will be quoted out of context.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Reading history as a relay race | "Symbolic AI died in 1987" | Eras are taught as replacements, not layers | Say "fell out of fashion", not "died"; name where it still runs |
| Believing winters were purely technical failures | "The perceptron book killed neural networks" | One vivid anecdote explains a complex funding collapse | Name the three causes: brittleness, computational cost, funding |
| Treating milestone gaps as capability | "Progress is 3× faster since 2012" | Headlines are easier to count than capability | Use the measure for rhythm, and say what it omits |
| Assuming current limits will not recur | "This time is different, scaling solves everything" | Every era believed it | Ask which bottleneck the current method still has, and what it costs |
| Confusing an engineering advance with a scientific one | "GPUs are a breakthrough in intelligence" | Both are genuine advances | Separate the algorithmic claim from the infrastructure claim |

## 10. Practical Exercises

1. **Add three milestones.** Extend the list with three events after 2022 (for example, a multimodal model, an open-weights release, a regulation). Recompute the era means. Does the rhythm change? What does your choice of milestones reveal about what you count as progress?
2. **Reconstruct a winter.** For the 1973 Lighthill report or the 1987 Lisp-machine collapse, write four sentences: what was promised, what was delivered, who paid, and what the field did next.
3. **Apply the claim procedure.** Take one AI claim from this week's news. Fill in the domain/wider/evidence/cost fields and write the one-sentence verdict.
4. **Design a demonstration that would have prevented a winter.** What would the expert-systems community have had to show in 1985 for the second winter not to happen? Is that demonstration technically possible at the time?
5. **Test the model.** Using the formula in §6, choose $\alpha = 0.3$, $\beta = 1$, $P_0 = C_0 = 1$. Compute $g(t)$ for $t = 1, 5, 10$. At what $t$ does the promise exceed delivered capability by 5×? What does the answer depend on?

## 11. Self-Assessment

**1.** Name the three eras and the dominant idea of each.
<details><summary>Show answer</summary>

Symbolic optimism (1956–1974): intelligence is symbol manipulation and logic. Expert systems (1980–1987): encode human expertise as rules and commercialise it. Statistical and deep learning (1990s–present): learn input–output mappings from data instead of writing rules.

</details>

**2.** Why is "the perceptron controversy caused the first winter" an incomplete explanation?
<details><summary>Show answer</summary>

It names one episode in a broader funding collapse. The first winter had structural causes: symbolic systems were brittle outside toy domains, search costs grew exponentially, and funders withdrew after the 1973 Lighthill report. Minsky and Papert's book on perceptrons was a genuine technical critique of single-layer limits, but funding decisions responded to the gap between promises and delivered systems, not to one publication.

</details>

**3.** A vendor says their system "learns continuously from user feedback". Which historical bottleneck does that claim address, and what would you ask to test it?
<details><summary>Show answer</summary>

It addresses the knowledge-acquisition bottleneck that made expert systems expensive: rules had to be written by people. To test it, ask what data the feedback produces, how quickly the model changes, whether changes are validated before deployment, and whether a bad feedback loop can corrupt behaviour. Continuous learning without validation is a new failure mode, not a solved bottleneck.

</details>

**4.** Using the §6 model with $\alpha = 0.3$, $\beta = 1$, $P_0 = C_0 = 1$, compute $g(5)$ and $g(10)$.
<details><summary>Show answer</summary>

$P(5) = 1.3^5 \approx 3.71$, $C(5) = 6$, so $g(5) \approx 0.62$ — no gap yet. $P(10) = 1.3^{10} \approx 13.79$, $C(10) = 11$, so $g(10) \approx 1.25$. The ratio grows without bound because promises compound while capability is modelled as linear; the exact crossing point depends on both parameters, which is why the model is for reasoning about shape, not dates.

</details>

**5.** Which of these is a capability advance, an engineering advance, or a change in expectations: (a) a new GPU with twice the memory bandwidth, (b) a model that solves a benchmark 10 points higher with the same architecture, (c) a company renaming its rules engine "AI"?
<details><summary>Show answer</summary>

(a) engineering advance — infrastructure that changes what is affordable; (b) capability advance if the benchmark is held out and representative, otherwise an expectation change dressed as a result; (c) change in expectations/marketing only, with no technical change. The interesting cases are always (b), because that is where evaluation quality decides the verdict.

</details>

## 12. Key Terms

- **AI winter** — a period of withdrawn funding and credibility following a gap between promised and delivered capability.
- **Symbolic AI** — intelligence implemented by manipulating explicit symbols and rules.
- **Expert system** — a rule base plus an inference engine, designed to reproduce a specialist's decisions.
- **Knowledge acquisition bottleneck** — the cost of extracting and maintaining rules from human experts.
- **Combinatorial explosion** — growth of the search space so fast that added speed buys little added depth.
- **Perceptron** — an early linear classifier; its single-layer limits were proved in 1969.
- **Backpropagation** — the algorithm that made multi-layer networks trainable, popularised in 1986.

See the [glossary](../../../resources/glossary.md) for the full list.

## 13. Further Reading

- Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach*, 4th ed., Chapter 1. — The standard compressed history, with the primary sources cited.
- Haenlein, M. & Kaplan, A. (2019). *A Brief History of Artificial Intelligence: On the Past, Present, and Future of Artificial Intelligence*. California Management Review. — Written for managers; useful for seeing how the eras are sold.
- Crevier, D. (1993). *AI: The Tumultuous History of the Search for Artificial Intelligence*. — Detailed on the expert-systems collapse and the Lisp-machine market.
- Krizhevsky, A., Sutskever, I. & Hinton, G. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. — The paper usually named as the start of the current era; read the error rates, not only the architecture.

## What to Do Next

Read [L01-03 — The Many Faces of AI](L01-03-symbolic-statistical-generative.md) to see how the three traditions in this history coexist in one system, then try [LAB-01-01](../labs/lab-01-01-claim-audit.md), where you audit a real capability claim end to end.

---

**Navigation:** [← Previous: L01-01 What Is Artificial Intelligence? Definitions, Goals and Myths](L01-01-what-is-artificial-intelligence.md) · [Module home](../README.md) · [Next: L01-03 The Many Faces of AI: Symbolic, Statistical and Generative →](L01-03-symbolic-statistical-generative.md)
