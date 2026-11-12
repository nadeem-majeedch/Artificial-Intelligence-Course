# LAB-01-02 — Build a Turing-Test-Style Conversational System

| Module | M01 · Introduction and Foundations of Artificial Intelligence |
| :--- | :--- |
| Level | 100 |
| Effort | 60 minutes, suggested split: session 1 = tasks 1–3, session 2 = tasks 4–6 |
| Lessons covered | [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md), [L01-04](../lessons/L01-04-ai-capabilities-and-limitations.md), [L01-05](../lessons/L01-05-course-workflow-and-study-habits.md) |
| Dataset / assets | Starter implementation [`code/eliza_lite.py`](../code/eliza_lite.py); transcript set embedded in this lab |
| Notebook | [NB-01-01](../notebooks/nb-01-01-capability-test-bench.ipynb) — support for the cue statistics |

[← Module home](../README.md) · [Course home](../../../README.md)

## Scenario

The department is running a first-year seminar on "can machines think?" and the tutor wants the
students to *feel* the problem rather than debate it. She has one hour and no budget for an API.

Her plan: half the class talks to a pattern-matching program, half talks to a person typing
through a wall of paper, and everyone judges transcripts. She needs a working system, a fair
protocol, and an honest note on what the exercise does and does not show.

She asks you to build the system and the judging materials.

## Your role

You are the teaching assistant for the seminar. You report to the tutor and you will be judged on
whether the exercise is **fair and reproducible** — not on whether your program is convincing.

## What you are given

| Item | Location | Notes |
| :--- | :--- | :--- |
| Starter conversation system | [`code/eliza_lite.py`](../code/eliza_lite.py) | Rule list, pronoun reflection, deterministic replies |
| Transcript set | embedded in Task 3 | 10 excerpts, 5 written by a person, 5 produced by a system |
| Cue extractor | `extract_cues()` in the same file | word count, questions, first-person ratio, hedges, comma ratio |
| The original test | [L01-01 §3.4](../lessons/L01-01-what-is-artificial-intelligence.md) | what Turing proposed, and its known weaknesses |

**Not provided:** a language model, a crowd of human participants, or labels in the transcript
set — you must judge the excerpts yourself before revealing the answers.

## Requirements

**Functional**

- R1 — Run the starter system and hold a **six-turn conversation**; record the transcript verbatim.
- R2 — Add **three new rules** for a topic of your choice and show the transcript before and after.
- R3 — Judge all 10 excerpts blind, then compute your own **judge accuracy** against the labels.
- R4 — Compute cue statistics for both groups and state which cue separates them best.
- R5 — Write a **protocol** a class could follow: who judges, how many turns, what is controlled,
  and how labels are hidden.

**Non-functional**

- N1 — Deterministic: the same input produces the same replies, so two tutors get the same demo.
- N2 — Standard library only; no network calls, no model downloads.
- N3 — The protocol must be executable in one 50-minute seminar with no technical support.

## Tasks

1. **Talk to it.** Run `python eliza_lite.py`, then hold your own six-turn conversation. Save the
   transcript. Find one turn where the reply is *grammatical but semantically empty* — where the
   system has clearly not understood — and quote it. *(success: you can point to the exact turn
   where understanding would be required and is absent)*

2. **Extend it.** Add three rules for a new topic (for example lab access, exam stress, group
   projects). Re-run and show the transcript. Which of your rules can be defeated by a single
   unexpected word? *(success: at least one rule demonstrably fails on an input you designed)*

3. **Judge blind.** Copy the excerpts below into your script **without looking at the labels at the
   end of this lab**. Mark each `H` (human) or `M` (machine) on paper first. Then run the code to
   get your accuracy.

   ```python
   transcripts = [
       ("t1", "hi, sorry to bother you - is the lab open on saturday? i couldn't find it on the site"),
       ("t2", "I need help with my timetable."),
       ("t3", "i think my registration is broken?? it says pending but i paid on the 3rd"),
       ("t4", "Why do you need help with your timetable?"),
       ("t5", "honestly not sure, maybe the tutor changed the room and forgot to tell us"),
       ("t6", "Tell me more about feeling stuck."),
       ("t7", "my project partner disappeared again, third time this term, so I'm doing the whole report"),
       ("t8", "How does your supervisor being unhappy affect you?"),
       ("t9", "does the library have the 2019 edition? the catalogue says yes but the shelf says no"),
       ("t10", "What is your own answer to that?"),
   ]
   labels = {"t1": "H", "t2": "H", "t3": "H", "t4": "M", "t5": "H",
             "t6": "M", "t7": "H", "t8": "M", "t9": "H", "t10": "M"}
   ```

   *(success: your accuracy is recorded, and you can name the excerpt that fooled you)*

4. **Measure the cues.** Compute `extract_cues()` for each excerpt and compare the means of the two
   groups. Which cue separates them most cleanly? Which cue would fail on a *better* machine?
   *(success: you have a table of cue means, and one sentence on why surface cues are insufficient)*

5. **Design the protocol.** Write the judging protocol: number of turns, whether the judge knows
   the pairing, how topics are matched between human and machine, how long the judge has, and how
   ties are handled. Identify the one control that matters most and explain why.

6. **Write the verdict.** Three paragraphs for the tutor: what the exercise demonstrates, what it
   does *not* demonstrate about intelligence, and one change you would make if you had a real
   language model available.

## Deliverables

| File | Contents |
| :--- | :--- |
| `lab_01_02.py` | Your extended system, the transcript set, judge accuracy and cue table, runnable |
| `transcripts.md` | Your six-turn conversation, before and after your rules, with the empty-reply turn marked |
| `protocol.md` | The judging protocol, ≤ 400 words, with the key control named |
| `verdict.md` | ≤ 400 words, three paragraphs, including one limitation of the exercise |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Correctness | 30% | System runs, judge accuracy and cue means computed correctly | Runs, one metric missing | Crashes or fabricated numbers |
| Method justification | 25% | Explains why the protocol controls what it controls | Protocol present, weakly justified | No protocol |
| Evaluation | 20% | Names the cue that fails on better systems, with evidence | Cue table only | No analysis |
| Code quality | 15% | Deterministic, readable, rules separated from data | Works, monolithic | Does not run |
| Communication | 10% | Tutor could run the seminar from your notes | Understandable | Missing or unclear |

## Extension challenges

1. **Adversarial judge.** Write five excerpts designed to fool a judge in each direction: a human
   who sounds machine-like, and a machine reply that sounds human. Which is easier to write, and
   what does that say about the test?
2. **Memory.** Add a one-turn memory ("you said earlier that…") and re-run your transcript. Does
   memory alone make the system convincing? Where does it still fail?
3. **Score instead of decide.** Replace the binary judgement with a 1–5 confidence rating. Compute
   the correlation between confidence and correctness. Is the judge calibrated?

## Hints

<details><summary>Hint 1 — getting started</summary>

Run the starter file before editing it: `python eliza_lite.py`. If the demo prints replies, your
environment is fine and any later failure is in your rules, not your setup.

</details>

<details><summary>Hint 2 — the likely sticking point</summary>

Rules are matched against the *whole* lower-cased turn with `re.fullmatch`. A rule written for
`"i need (.*)"` will not fire on `"hi, i need help"` because of the leading `hi,`. Anchor with
`.*` at the start, or clean the input first — and notice that this brittleness is the point of
Task 2.

</details>

<details><summary>Hint 3 — checking your work</summary>

Judge accuracy must equal the number of correct marks divided by 10. If you get 1.0, check that
you did not look at the labels first — the exercise is worthless if you did, and your report will
say so.

</details>

## Reflection

1. Which requirement was hardest to satisfy, and what does that tell you about building a
   demonstration rather than a product?
2. A system can pass a five-minute text test and still fail at the first task that requires memory
   or verification. Where is that boundary in your own system?
3. Where could this kind of fluency mislead a real user, and what would you put in the interface to
   prevent it?

## Time budget

| Session | Tasks | Time |
| :--- | :--- | ---: |
| 1 | 1–3 | 35 min |
| 2 | 4–6 | 25 min |
