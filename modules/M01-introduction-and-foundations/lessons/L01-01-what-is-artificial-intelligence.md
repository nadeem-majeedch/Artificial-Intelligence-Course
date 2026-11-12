# L01-01 — What Is Artificial Intelligence? Definitions, Goals and Myths

| Module | M01 · Introduction and Foundations of Artificial Intelligence |
| :--- | :--- |
| Level | 100 |
| Study time | 60 minutes |
| Prerequisites | None |
| Notebook | [NB-01-01 Capability Test Bench](../notebooks/nb-01-01-capability-test-bench.ipynb) |
| Lab | [LAB-01-01 Claim Audit](../labs/lab-01-01-claim-audit.md) |

[← Module start](../README.md) · [Next: L01-02 A Brief History of AI and the AI Winters →](L01-02-history-and-ai-winters.md)

## On this page

- [1. Learning Objectives](#1-learning-objectives)
- [2. Prerequisite Knowledge](#2-prerequisite-knowledge)
- [3. Conceptual Explanation](#3-conceptual-explanation)
- [4. The Procedure: Four Questions That Decide "Is This AI?"](#4-the-procedure-four-questions-that-decide-is-this-ai)
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

[Module start](../README.md) · [Module home](../README.md) · [Next: L01-02 A Brief History of AI and the AI Winters →](L01-02-history-and-ai-winters.md)

## 1. Learning Objectives

By the end of this lesson you will be able to:

- **Define** artificial intelligence precisely enough to argue about a specific system, and separate the goal of AI from the techniques used to pursue it.
- **Apply** a four-question capability test to a described system and justify the verdict in writing.
- **Distinguish** narrow, general and superintelligent AI, and weak from strong AI, without conflating them.
- **Evaluate** the Turing Test as a definition of intelligence, naming what it measures and what it deliberately ignores.

## 2. Prerequisite Knowledge

This lesson assumes only that you can read a short Python program. Nothing else is required; it is the first lesson of the course.

If you have never written code, work through [P01 Python Programming](../../../prerequisites/P01-python-programming/README.md) first — lessons 1 and 2 are enough to read everything here.

## 3. Conceptual Explanation

### 3.1 The intuition

Imagine three systems on a desk.

1. A thermostat that turns the heating on when the room drops below 19 °C.
2. A spam filter that moves suspicious mail to a folder.
3. A chess engine that beats the national champion.

Most people say the third is AI and hesitate over the first two. But why? The thermostat *perceives* (temperature), *decides* (heat or not) and *acts* (switches a relay). By that description it is an agent. What it lacks is any notion of alternatives it could weigh, and any ability to improve.

The hesitation is the interesting part, because it tells you the word "AI" is doing two jobs at once. Sometimes it names **a goal**: make machines do what would require intelligence if a person did it. Sometimes it names **a set of techniques**: search, logic, probability, learning. And sometimes it names **a marketing category**: whatever is being sold this year. A definition that only covers one of these jobs will fail you in a conversation about the other two.

### 3.2 The formal idea

We will use a definition that is precise enough to test, and honest about its own history:

> **Artificial intelligence** is the engineering discipline of building systems that select actions to achieve goals in environments they only partly know, using computation rather than direct human control.

Unpack the four clauses, because each one excludes something:

| Clause | What it requires | What it excludes |
| :--- | :--- | :--- |
| *select actions* | a choice among alternatives | a fixed mechanical transformation with no alternatives |
| *to achieve goals* | a criterion for better and worse | behaviour with no objective, however clever |
| *environments they only partly know* | uncertainty, partial observability | a fully specified, closed computation |
| *computation, not direct human control* | the system decides | a person operating a machine by hand |

Under this definition a thermostat is a very small agent, a spreadsheet formula is a calculator, and a chess engine is unmistakably AI. That ordering matches how practitioners talk, which is a good sign.

Alongside the definition you need four labels that are constantly misused:

- **Narrow AI** — a system that performs one task or a narrow family of tasks. Every deployed system today is narrow, including the ones that write essays.
- **General AI (AGI)** — a hypothetical system that can learn and perform any intellectual task a human can, transferring knowledge between domains without being retrained for each.
- **Superintelligence** — a hypothetical system that surpasses human performance across the board. It is a subject of speculation and safety research, not a product.
- **Weak AI / strong AI** — a distinction about *claims*, not capability. Weak AI (in the philosophical sense) holds that a machine can *simulate* intelligence without being conscious; strong AI holds that a sufficiently faithful simulation *is* a mind. A narrow system can be discussed under either claim, so "weak AI" is not a synonym for "narrow AI".

Notice the trap: "narrow" versus "general" is about *scope of task*. "Weak" versus "strong" is about *whether there is a mind*. Mixing the two produces sentences like "chatbots are weak AI, so AGI is close", which contains no usable claim at all.

### 3.3 Why it matters

You will spend the rest of this course building systems and reading claims about them. The single most useful skill you can take from this lesson is the habit of asking *which* claim is being made: a capability claim ("it can do X"), a generality claim ("it can do X in any domain"), or a mind claim ("it understands X"). Most public disagreement about AI is people answering different questions and not noticing.

### 3.4 The Turing Test, and what it is actually for

Alan Turing's 1950 paper proposed replacing the question "can machines think?" with an operational one: can a machine's text responses be distinguished from a person's by an interrogator? If not, we say it passes.

Read the move carefully, because it is a template for the whole field. Turing did not answer the philosophical question; he **replaced an untestable question with a measurable one**. That is the same manoeuvre we use later when we replace "does this model understand language?" with "what accuracy does it reach on held-out text?".

The test has known weaknesses, and you should be able to state them:

- It measures **imitation of human conversation**, not intelligence in general. A system can pass by being charming and vague.
- It is **binary and gameable**: the interrogator knows the setup, and the machine can refuse, deflect or flatter.
- It says nothing about **reliability, memory, or truth**. A confident wrong answer is indistinguishable from a confident right one inside a five-minute chat.
- Modern systems trained on human text make the test much easier for reasons that have little to do with reasoning.

Its lasting contribution is not the test itself but the standard it sets: *define success as an observable behaviour, then measure it*. You will meet that standard again in every evaluation chapter of this course.

## 4. The Procedure: Four Questions That Decide "Is This AI?"

Pseudocode first; the executable version follows in §7.

```text
FUNCTION classify_system(system):
    score <- number of TRUE flags among
             perceives, decides, adapts, goal_directed
    IF score <= 1:            RETURN "automation, not really AI"
    IF score == 2:            RETURN "borderline - often sold as AI"
    IF system.adapts:         RETURN "AI: learning system"
    RETURN "AI: hand-written rules"
```

The procedure is deliberately crude. Its value is that it forces you to commit to four yes/no judgements instead of arguing about a vibe. When you disagree with someone about whether a product "is AI", the disagreement usually reduces to one of these four flags — and then it becomes a productive conversation.

## 5. Worked Examples

### Example 1 — A thermostat, a spreadsheet, a spam filter, a chess engine

Apply the four flags:

| System | Perceives | Decides | Adapts | Goal-directed | Score | Verdict |
| :--- | :-: | :-: | :-: | :-: | ---: | :--- |
| Thermostat | ✓ | ✓ | ✗ | ✓ | 3 | AI: hand-written rules |
| Spreadsheet `SUM` | ✗ | ✓ | ✗ | ✗ | 1 | automation |
| Spam filter | ✓ | ✓ | ✓ | ✓ | 4 | AI: learning system |
| Chess engine | ✓ | ✓ | ✗ | ✓ | 3 | AI: hand-written rules |

Three of the four land in the AI region, and the spreadsheet does not — even though the spreadsheet is the one people trust most. That is not a paradox: trust comes from determinism and a closed specification, not from intelligence.

### Example 2 — Where the definition bites: a recommendation feed

A video platform ranks videos for each user. Perceives? Yes — watch history, dwell time, skips. Decides? Yes — an ordering. Adapts? Yes — retrained on new behaviour. Goal-directed? Yes, but note *whose* goal: engagement, not the user's learning.

Score 4, "AI: learning system". Now change one detail: the ranking is a fixed editorial list written by humans, served unchanged. Perceives ✗, adapts ✗, score 2 — "borderline". The *outcome* the user sees may look identical; the system is not the same kind of thing at all. This is why you describe systems by their mechanism, not by their surface behaviour.

## 6. Mathematical Formulation

The capability score is a counting rule with equal weights:

$$
s(x) = \mathbb{1}[\text{perceives}] + \mathbb{1}[\text{decides}] + \mathbb{1}[\text{adapts}] + \mathbb{1}[\text{goal-directed}], \qquad s \in \{0,1,2,3,4\}
$$

where $\mathbb{1}[\cdot]$ is 1 when the condition holds and 0 otherwise.

| Symbol | Meaning |
| :--- | :--- |
| $\mathbb{1}[\cdot]$ | indicator function: 1 if true, 0 if false |
| $s(x)$ | capability score of system $x$, an integer 0–4 |
| perceives | the system receives observations from its environment |
| adapts | the system's behaviour changes as a result of experience |

Equal weights are a choice, not a law. Make them explicit when you use the rule: if you care most about adaptation, weight it double and say so. A score whose weights are hidden is not a measurement.

## 7. Python Implementation

```python
from dataclasses import dataclass


@dataclass
class System:
    """A described system, scored on four capability flags."""
    name: str
    perceives: bool
    decides: bool
    adapts: bool
    goal_directed: bool


def classify(system: System) -> str:
    """Return a short verdict for a system, given its four capability flags."""
    score = sum([system.perceives, system.decides, system.adapts, system.goal_directed])
    if score <= 1:
        return "automation, not really AI"
    if score == 2:
        return "borderline - often sold as AI"
    if system.adapts:
        return "AI: learning system"
    return "AI: hand-written rules"


systems = [
    System("thermostat", True, True, False, True),
    System("spreadsheet SUM", False, True, False, False),
    System("spam filter", True, True, True, True),
    System("chess engine", True, True, False, True),
]
for system in systems:
    flags = [system.perceives, system.decides, system.adapts, system.goal_directed]
    print(f"{system.name:16s} score={sum(flags)}  {classify(system)}")
```

**Output**

```text
thermostat       score=3  AI: hand-written rules
spreadsheet SUM  score=1  automation, not really AI
spam filter      score=4  AI: learning system
chess engine     score=3  AI: hand-written rules
```

The output matches the table in Example 1 exactly, which is the point of writing the rule as code: you cannot quietly change a flag while arguing.

## 8. Practical Applications

- **Product due diligence — procurement and investment.** "AI-powered" appears on systems that are rule tables with a nicer interface. Asking the four questions, and asking for the model card or evaluation report, separates a genuine learning system from a rebranded spreadsheet before money changes hands.
- **Regulation and compliance.** Rules such as the EU AI Act attach obligations to systems that *infer* from data rather than execute fixed logic. The perceives/adapts distinction is the boundary regulators are trying to draw, so describing a system accurately is now a legal skill, not a semantic one.
- **Research framing.** Choosing the label commits you to a literature. A "learning system" claim is evaluated with held-out data; a "hand-written rules" claim is evaluated with coverage and edge-case analysis. Getting the label wrong sends you to the wrong evaluation method.

## 9. Common Mistakes

| Mistake | What you will see | Why it happens | Fix |
| :--- | :--- | :--- | :--- |
| Treating "AI" as one property | Arguments that stall on "but is it *really* AI?" | The word carries a goal, a technique set and a marketing meaning at once | Say which of the three you mean before arguing |
| Confusing narrow with weak | "It is only weak AI, so AGI is near" | Scope of task and philosophy of mind are different axes | Name the axis: narrow/general is scope; weak/strong is about minds |
| Judging by surface behaviour | Calling an editorial feed "AI" because the page looks the same | Outputs are observable; mechanisms are not | Describe the mechanism: what does it sense, and does it change? |
| Treating the Turing Test as a pass/fail definition of intelligence | "It passed, so it thinks" | The test was designed to avoid defining thinking, not to define it | Use it as a behavioural benchmark with stated limits |
| Over-weighting one flag | "It learns, therefore it is intelligent" | Learning is impressive and easy to demo | Score all four; state your weights |

## 10. Practical Exercises

1. **Score six systems.** Choose: a lift button, a spelling checker, a voice assistant, a fraud detector, a self-checkout, a chess engine. Fill the four-flag table. Where you are unsure, write the question you would ask an engineer to settle it.
2. **Rewrite a marketing sentence.** Find a sentence claiming a product "uses AI to personalise your experience". Rewrite it three ways: as a capability claim, as a mechanism claim, and as an evaluation claim.
3. **Break the score.** Construct a system with score 4 that you would *not* call AI, or explain why none exists. (Hint: consider a system that perceives and adapts but has a trivial goal, such as a light that dims gradually.)
4. **Turing Test variant.** Design a five-minute text test that a system trained on human text would *fail* but a person would pass. State exactly what capability your test isolates, and why the original test does not isolate it.
5. **Classify the debate.** Find two public arguments about AI (news, blog, paper). For each, label what the author is actually claiming: capability, generality or mind. Note where the disagreement is really about definitions.

## 11. Self-Assessment

**1.** State the four-clause definition of AI used in this lesson and give one system excluded by each clause.
<details><summary>Show answer</summary>

AI is the engineering discipline of building systems that (i) select actions, (ii) to achieve goals, (iii) in environments they only partly know, (iv) using computation rather than direct human control. A fixed pulley excludes (i); a random noise generator excludes (ii); a sorting function on a fully specified array excludes (iii); a person driving a car excludes (iv).

</details>

**2.** A vending machine accepts coins, dispenses the selected item, and refuses when stock is empty. Apply the four-flag procedure and defend your score.
<details><summary>Show answer</summary>

Perceives ✓ (coins, selection, stock sensor), decides ✓ (dispense or refuse), adapts ✗ (behaviour does not change with experience; a restock is a human intervention), goal-directed ✓ (deliver the paid item). Score 3 → "AI: hand-written rules". A reasonable dissent: the goal is trivial and the environment fully specified, so many engineers would call it automation. The procedure makes the dissent precise instead of emotional.

</details>

**3.** Explain why "weak AI" is not a synonym for "narrow AI", with an example that is narrow but would be strong under the philosophical reading.
<details><summary>Show answer</summary>

Narrow describes task scope; weak/strong describes whether the system has a mind. A system that plays only Go is narrow. If it genuinely understood positions in the way a person does, a strong-AI theorist would call it strong despite the narrow scope. Conversely a general assistant that merely simulates understanding without any inner life is weak AI by the philosophical definition, however broad its scope.

</details>

**4.** Give two reasons the Turing Test is a weak definition of intelligence, and one reason it was nevertheless a good move.
<details><summary>Show answer</summary>

Weaknesses: it measures conversational imitation rather than reasoning or reliability, and it is gameable by deflection and flattery; it also says nothing about memory, truthfulness or competence outside the chat. It was a good move because it converted an unfalsifiable question into a measurable protocol, and that habit — define success as observable behaviour — is what makes evaluation possible.

</details>

**5.** A system's outputs are identical to a learning system's, but its ranking is a fixed human-written list. Which parts of your description change, and why does that matter for how you evaluate it?
<details><summary>Show answer</summary>

Perception and adaptation change: score drops from 4 to 2. Evaluation changes too — a fixed list is assessed for coverage, editorial bias and staleness, not for generalisation on held-out data. Identical outputs do not imply identical failure modes, and the failure modes are what evaluation must target.

</details>

## 12. Key Terms

- **Artificial intelligence** — the discipline of building systems that select actions to achieve goals in partly known environments, by computation.
- **Narrow AI** — a system that performs one task or a narrow family of tasks.
- **General AI (AGI)** — a hypothetical system that can perform any intellectual task a human can, transferring across domains.
- **Superintelligence** — a hypothetical system surpassing human performance across the board.
- **Weak AI** — the position that a machine can simulate intelligence without consciousness.
- **Strong AI** — the position that a sufficiently faithful simulation of intelligence is a mind.
- **Turing Test** — a behavioural test in which a machine passes if its text responses cannot be distinguished from a person's.

All of these are defined in the [glossary](../../../resources/glossary.md).

## 13. Further Reading

- Turing, A. M. (1950). *Computing Machinery and Intelligence*. Mind 59(236), 433–460. — The original test; read it for the *argument*, which is more careful than its later caricature.
- Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach*, 4th ed., Chapter 1. — The standard definition of AI as rational action, and the history compressed into twenty pages.
- McCarthy, J. (2007). *What Is Artificial Intelligence?* Stanford CS. — A short, blunt definition from the person who named the field.
- Mitchell, M. (2019). *Artificial Intelligence: A Guide for Thinking Humans*, Chapters 1–3. — A careful treatment of what current systems do and do not do.

## What to Do Next

Run [NB-01-01](../notebooks/nb-01-01-capability-test-bench.ipynb) to score systems yourself, then read [L01-02 — A Brief History of AI and the AI Winters](L01-02-history-and-ai-winters.md) to see how these definitions were fought over in practice.

---

**Navigation:** [← Module start](../README.md) · [Next: L01-02 A Brief History of AI and the AI Winters →](L01-02-history-and-ai-winters.md)
