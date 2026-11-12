# QUIZ-01 — Introduction and Foundations of AI self-check

| Module | M01 · Introduction and Foundations of Artificial Intelligence |
| :--- | :--- |
| Questions | 15 multiple choice + 4 short answer |
| Time | 30 minutes |
| Covers | [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md) … [L01-05](../lessons/L01-05-course-workflow-and-study-habits.md) |
| Pass mark | 12 / 15 before moving on |

[← Module home](../README.md) · [Course home](../../../README.md)

## How to use this quiz

Answer on paper first, without looking anything up. Then open each answer, mark yourself, and use
the revision map at the end to decide what to reread. A quiz you score without effort teaches you
nothing — the point is to find the gaps.

**Scoring guide**

| Score | What it means |
| :--- | :--- |
| 12+ / 15 | Move on to M02 |
| 9–11 / 15 | Reread §3 of the lessons you missed and redo their exercises |
| below 9 / 15 | Work through the module again; check the readiness self-check in the module README |

## Part A — Multiple choice

### Topic 1: Defining AI

**Q01.01** Which clause is *not* part of the working definition of AI used in L01-01?

- A. Selecting actions among alternatives
- B. Achieving goals in partly known environments
- C. Being implemented with a neural network
- D. Using computation rather than direct human control

<details><summary>Answer</summary>

**C.** The definition is about goal-directed computation in uncertain environments, not about any
particular implementation. A rule-based route planner satisfies it without a neural network; a
neural network that runs no decisions at all would not. → [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md)

</details>

**Q01.02** A system that perceives, decides and pursues a goal, but never changes its behaviour with
experience, scores 3 on the capability test. Which label does L01-01 assign?

- A. Automation, not really AI
- B. Borderline, often sold as AI
- C. AI: learning system
- D. AI: hand-written rules

<details><summary>Answer</summary>

**D.** Score 3 with `adapts = False` falls through to "AI: hand-written rules" — the chess engine and
thermostat case. Option C would require the adaptation flag. → [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md)

</details>

**Q01.03** Which pair is correctly matched?

- A. Narrow AI — a system limited to one task; weak AI — a claim that machines can simulate intelligence
- B. Narrow AI — a claim about consciousness; weak AI — a system limited to one task
- C. General AI — every deployed system today; superintelligence — a system that plays games well
- D. Strong AI — a system with narrow scope; weak AI — a system with broad scope

<details><summary>Answer</summary>

**A.** Narrow/general is task scope; weak/strong is the philosophical claim about minds. Mixing the
axes produces the most common confusion in public discussion. → [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md)

</details>

### Topic 2: History and winters

**Q01.04** The first AI winter is best explained by which combination?

- A. A single hardware failure and the invention of the transistor
- B. Brittleness outside toy domains, combinatorial explosion in search, and withdrawn funding after a critical report
- C. The publication of a paper proving all AI is impossible
- D. The replacement of symbolic methods by deep learning

<details><summary>Answer</summary>

**B.** The winter followed a gap between promised and delivered capability, driven by brittleness,
search cost growth, and funding withdrawal after the 1973 Lighthill report. Deep learning arrived
decades later, so D is anachronistic. → [L01-02](../lessons/L01-02-history-and-ai-winters.md)

</details>

**Q01.05** The knowledge-acquisition bottleneck refers to:

- A. The cost of labelling training data for neural networks
- B. The slow speed of computer memory in the 1970s
- C. The difficulty of extracting and maintaining expert rules in a symbolic system
- D. The limit on how much text a language model can read

<details><summary>Answer</summary>

**C.** Expert systems needed humans to write every rule, and those rules needed maintenance as the
domain changed. Machine learning attacks this bottleneck by fitting patterns from data instead.
→ [L01-02](../lessons/L01-02-history-and-ai-winters.md)

</details>

**Q01.06** Between 1980 and 2011, the mean gap between public AI milestones was larger than in the
other eras. What is the best interpretation?

- A. No research happened during that period
- B. Capability stopped improving until 2012
- C. Public milestones are a measure of visible events, not of internal progress
- D. The field had fewer researchers than in the 1960s

<details><summary>Answer</summary>

**C.** The expert-systems era and its collapse produced the slowest *visible* progress, while
statistical methods were being developed underneath. Milestone spacing measures publicity, not
capability. → [L01-02](../lessons/L01-02-history-and-ai-winters.md)

</details>

### Topic 3: Paradigms and containment

**Q01.07** Which statement about the relationship between AI, machine learning and deep learning is correct?

- A. They are three names for the same field
- B. ML is a subset of AI, and DL is a subset of ML
- C. AI is a subset of DL, which is a subset of ML
- D. Deep learning and symbolic AI are both subsets of machine learning

<details><summary>Answer</summary>

**B.** ML is one way of doing AI, and DL is one family within ML. Symbolic AI sits inside AI but
outside ML, which is why "AI versus ML" is a category error. → [L01-03](../lessons/L01-03-symbolic-statistical-generative.md)

</details>

**Q01.08** A rule classifier and a nearest-neighbour classifier both score 5/6 on the same six test
emails. What is the most defensible conclusion?

- A. The methods are equally good, so choose the simpler one
- B. The methods have different inductive biases and fail on different cases, so the comparison needs more data and a cost model
- C. Nearest neighbour is better because it learns from data
- D. The test set is too small, so neither method can be used in practice

<details><summary>Answer</summary>

**B.** Equal accuracy hides disjoint errors. The interesting evidence is *which* emails each method
gets wrong; deciding between them requires a larger evaluation and a model of error cost.
→ [L01-03](../lessons/L01-03-symbolic-statistical-generative.md)

</details>

**Q01.09** Inductive bias is best described as:

- A. A prejudice in the training data
- B. The assumptions a method uses to generalise beyond its training examples
- C. The tendency of a model to overfit
- D. A bug in the loss function

<details><summary>Answer</summary>

**B.** A learner cannot generalise without assumptions; k-NN assumes labels are locally constant
under a chosen distance, and the rule assumes a specific conjunction. Bias in data is a different
problem. → [L01-03](../lessons/L01-03-symbolic-statistical-generative.md)

</details>

### Topic 4: Capabilities and limits

**Q01.10** A system makes 500,000 decisions a day at 99% accuracy. How many errors per day?

- A. 50
- B. 500
- C. 5,000
- D. 50,000

<details><summary>Answer</summary>

**C.** $500{,}000 \times 0.01 = 5{,}000$. Whether that is acceptable depends on the cost of an error,
which accuracy alone does not tell you. → [L01-04](../lessons/L01-04-ai-capabilities-and-limitations.md)

</details>

**Q01.11** A model's predictions in the 90–99% confidence bucket are correct 87% of the time. What is
the correct description?

- A. The model is well calibrated
- B. The model is overconfident, and an "auto-approve above 90%" rule would approve some wrong cases
- C. The model is underconfident
- D. Calibration cannot be assessed from a bucket table

<details><summary>Answer</summary>

**B.** Stated confidence exceeds observed accuracy, so the model is overconfident. Setting a
threshold from stated confidence rather than measured accuracy lets errors through unreviewed.
→ [L01-04](../lessons/L01-04-ai-capabilities-and-limitations.md)

</details>

**Q01.12** Why does per-step reliability of 0.95 make a twenty-step plan unreliable?

- A. Because steps are usually dependent
- B. Because $0.95^{20} \approx 0.36$, so the plan succeeds about a third of the time even assuming independence
- C. Because 0.95 is below the 0.99 threshold required by theory
- D. Because errors cancel out over many steps

<details><summary>Answer</summary>

**B.** Failure probabilities compound multiplicatively. Independence is a generous assumption; real
dependence usually makes long plans worse, which is why verification at intermediate steps matters.
→ [L01-04](../lessons/L01-04-ai-capabilities-and-limitations.md)

</details>

### Topic 5: Workflow

**Q01.13** In the predict–run–explain loop, which step is most often skipped and why does it matter?

- A. Predict, because running is faster
- B. Explain, because a correct output feels like understanding
- C. Vary, because the code is already correct
- D. Run, because reading is sufficient

<details><summary>Answer</summary>

**B.** Without explaining the gap between prediction and output, the loop degrades into watching
code execute. Explaining is where the mental model is corrected. → [L01-05](../lessons/L01-05-course-workflow-and-study-habits.md)

</details>

**Q01.14** Your notebook cannot import NumPy but the terminal can. What is the first check?

- A. Reinstall NumPy
- B. Compare `sys.executable` in the notebook with the terminal's Python
- C. Restart the computer
- D. Convert the notebook to a script

<details><summary>Answer</summary>

**B.** The usual cause is a different interpreter or environment behind the kernel. Comparing
`sys.executable` distinguishes a kernel mismatch from a genuinely missing package.
→ [L01-05](../lessons/L01-05-course-workflow-and-study-habits.md)

</details>

**Q01.15** Which study pattern is best supported by the retention model in L01-05?

- A. One long session the night before an assessment
- B. Rereading the lesson three times in one sitting
- C. Several short sessions with retrieval, spread across a week
- D. Copying the worked examples by hand without testing recall

<details><summary>Answer</summary>

**C.** Each successful retrieval raises stability in $R(t)=e^{-t/S}$, so spaced retrieval flattens the
decay curve. Rereading and copying increase familiarity without strengthening retrieval.
→ [L01-05](../lessons/L01-05-course-workflow-and-study-habits.md)

</details>

## Part B — Short answer

**S01.01** A vendor claims their system "uses AI to personalise your experience". Rewrite this as a
capability claim, a mechanism claim, and an evaluation claim.

<details><summary>Model answer</summary>

Capability: "for each user, the system ranks items by predicted relevance". Mechanism: "a model
trained on interaction logs produces the ranking, refreshed weekly". Evaluation: "on held-out
weeks, the ranking improves click-through by X% over a popularity baseline, with per-group error
reported". A full-mark answer names all three and notes that the original sentence commits to none
of them.

</details>

**S01.02** Explain why both AI winters can be described as funding events rather than technical
extinctions, and name one thing that survived each.

<details><summary>Model answer</summary>

In both cases research continued while funding and credibility collapsed, because promises had
outrun delivered capability. After the first winter, symbolic reasoning and search survived and
continued to be taught and used; after the second, expert-system techniques survived inside
scheduling, configuration and database constraint systems, and statistical learning grew into the
next era. A full-mark answer separates the *technical* continuity from the *funding* discontinuity.

</details>

**S01.03** A hospital wants to deploy an imaging triage model trained on one scanner. Name the two
most important limitations and one concrete mitigation for each.

<details><summary>Model answer</summary>

Distribution shift: images from other scanners differ in noise and protocol, so accuracy on the
training distribution overstates performance — mitigate by testing on target-site images and
reporting per-site accuracy. Calibration: the score may not match observed accuracy, which matters
because clinicians act on it — mitigate by measuring calibration on site and setting thresholds from
measured accuracy. Accept also: no subgroup reporting, no drift monitoring, and accountability.

</details>

**S01.04** Two classifiers both score 5/6 on six emails. Give two reasons a single accuracy number
cannot settle which to deploy, and state what evidence you would collect instead.

<details><summary>Model answer</summary>

Six cases give a very imprecise estimate of true error, and the two methods fail on different
cases with different costs (missing spam versus blocking a newsletter). Instead, collect a larger
held-out set, report per-class precision and recall, inspect the error distribution by class, and
attach a cost model so the trade-off is explicit. A full-mark answer mentions that the choice also
depends on maintenance capacity, not only on accuracy.

</details>

## Revision map

| If you missed | Reread | Then do |
| :--- | :--- | :--- |
| Q01.01–03 | [L01-01](../lessons/L01-01-what-is-artificial-intelligence.md) | Redo exercises 1 and 3 |
| Q01.04–06 | [L01-02](../lessons/L01-02-history-and-ai-winters.md) | Re-run the milestone cell in [NB-01-01](../notebooks/nb-01-01-capability-test-bench.ipynb) |
| Q01.07–09 | [L01-03](../lessons/L01-03-symbolic-statistical-generative.md) | Redo the rule-versus-k-NN comparison with a third feature |
| Q01.10–12 | [L01-04](../lessons/L01-04-ai-capabilities-and-limitations.md) | Attempt [LAB-01-01](../labs/lab-01-01-claim-audit.md) tasks 3–5 |
| Q01.13–15 | [L01-05](../lessons/L01-05-course-workflow-and-study-habits.md) | Rebuild your study plan from the module map |
| S01.01–04 | All lessons | Write each answer again from memory, then compare |
