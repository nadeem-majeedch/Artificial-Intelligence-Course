# Laboratory and Assessment Audit — Phase 23

**Scope:** 38 laboratories, 8 mini-projects, 14 quizzes with answer keys, 14 programming assignments,
8 analytical assignments.
**Method:** every file was machine-checked for the required sections and for rubric/extension/starter-code
presence, then a stratified sample was read closely (M02, M03, M04, M09, M10, M13 labs; quiz M01 and its
key; MP-01/MP-06 pages) and a sample of numeric answers was recomputed by hand.

## 1. Structural completeness

| Artefact | Count | With a rubric/criteria | With extension tasks | With starter code |
| :--- | ---: | ---: | ---: | ---: |
| Laboratories | 38 | 38 | 34 | 20 |
| Mini-projects | 8 | 8 (3 rubrics added in this audit) | 3 | 2 |
| Programming assignments | 14 | 14 | 0 | 0 |
| Analytical assignments | 8 | 8 | 0 | 0 |
| Quizzes | 14 | — | — | — |
| Quiz answer keys | 14 | — | — | — |

Two templates are in use:

- **Numbered template (11 labs: M04, M09, M10)** — 14 sections: objectives, scenario, problem statement,
  background, dataset and licensing, software, step-by-step tasks, starter code, expected behaviour,
  metrics, testing, submission, rubric, extensions.
- **Older template (27 labs: M01–M03, M05–M08, M11–M14)** — scenario, your role, what you are given,
  requirements, tasks, deliverables, evaluation criteria, extension challenges, hints, reflection, time
  budget.

Both are complete learning units. The numbered template is stronger on dataset licensing and testing; the
older one is stronger on role framing and reflection. The inconsistency is documented rather than
rewritten, because rewriting 27 functioning labs would risk more damage than it repairs.

**18 labs have no inline starter-code block.** They reference a module code file or notebook instead
(for example LAB-02-01 names `environments.GridWorld` and the notebook). That is workable but weaker for a
student with no instructor: the code exists, but the lab does not scaffold the first step.

## 2. Scenario quality

Sampled labs use realistic, specific professional situations with a named decision-maker and a measurable
deliverable:

- **LAB-02-01** — a facilities company rejects a robot-vacuum fleet after a reflex controller loops in one
  corner; the student must specify and compare controllers and explain the failure to a manager.
- **LAB-03-01** — a courier company wants shortest legal routes and evidence about its route sheet, with
  one-way streets and an explicit statement that traffic data is *not* provided.
- **LAB-04-01/02/03** — advising expert system, family-logic inference, and the same troubleshooting
  scenario solved by logic and by Bayes, so the paradigms are compared rather than described.
- **LAB-09-01…04** — synthetic leaves/signs/road scenes with a required corruption study, and a baseline
  that scores mIoU 0.65 with obstacle Dice 0.00, which the lab requires the student to explain.
- **LAB-10-01…04** — gridworld, cliff walking, CartPole DQN, and policy-gradient/PPO, each with a stated
  evaluation protocol and a warning that short CPU runs do not demonstrate convergence.
- **LAB-13-01/02** — fairness audit and prompt-injection testing with synthetic data and a written scope
  limitation.

No lab asks a student to break a real system, use personal data, or present a teaching model as
operational. The high-stakes framing is qualified in the text (see `LICENSING-AND-REFERENCES-AUDIT.md`).

## 3. Instructions, expected results and testing

- Every lab states what "done" looks like and how it is marked; the numbered template also states metrics
  and a testing procedure.
- Expected results are ranges or qualitative criteria, not fabricated exact numbers, except where a
  deterministic seed makes an exact value reproducible (M09/M10), and those values were reproduced in
  this audit.
- Four labs have no extension task (LAB-13-01, LAB-13-02, LAB-14-01, LAB-14-02). Extensions are
  optional by design, so this is a completeness gap rather than a defect.

## 4. Assignments and projects

- **Programming assignments (14)** each carry requirements, a marking scheme and a submission format. They
  are text specifications, not scaffolds, which is appropriate for assessed work; no starter code is
  expected and none is claimed.
- **Analytical assignments (8)** are essay/derivation tasks with rubrics; they cover complexity, derivation,
  evaluation, error analysis, dataset bias, paper analysis and architecture evaluation. They align with
  M03, M05, M06, M08, M13 content.
- **Difficulty progression** is visible: PA-01 is NumPy/Python, PA-06 is a full ML pipeline with leakage
  constraints, PA-10 compares tabular and deep RL, PA-14 is an explainability/security audit.
- **Three mini-projects had no marking table** (MP-06, MP-07, MP-11). Each describes deliverables and
  failure modes but never says how marks are split, which makes self-assessment impossible. **Fixed in this
  audit** by appending a five-criterion weighting table to each, consistent with the rubrics already used by
  MP-01, MP-04, MP-10 and MP-13.
- **Five mini-projects have no extension section** and six contain no code block. For MP-01 (an audit),
  MP-06/07/11 (sprints with their own repo conventions) and MP-12 (multi-tool agent), the absence of inline
  code is a deliberate design choice — the work is the student's own — but it is a self-study obstacle.

## 5. Quiz and answer-key verification

All 14 quizzes have a matching answer key, and every key covers the same parts as its quiz (5–7 parts each,
by section count). A sample of numeric answers was recomputed by hand:

- **Quiz M01, Q1.7** — weighted capability score (weights 3, 2, 3 out of 8): (a) 5, (b) 8, (c) 0. The key
  states 5, 8, 0. **Correct.**
- **Quiz M01, Q1.8** — 873/1000: proportion 0.873, 87.3%, error rate 127 per 1,000. The key states exactly
  that, and explicitly warns against the common error of writing 0.127%. **Correct.**
- **Quiz M01, Q1.9** — chronology (Dartmouth 1956 → first AI winter → expert-systems boom → ImageNet 2012 →
  transformer 2017) is consistent with the module's history lesson.
- **Quiz M01, Q1.10** — the Python snippet prints `5 0.625`; the key gives `5 0.625`. **Correct.**

The remaining keys were checked for structure, consistency of part numbering and presence of marks; their
individual subject answers were not all recomputed, and this report does not claim otherwise.

## 6. Alignment with lessons

Each lab names the lessons it pairs with, and the pairing is accurate on inspection: LAB-09-03 uses the
detection metrics defined in L09-04; LAB-10-02 uses the SARSA/Q-learning contrast from L10-03; LAB-04-02
uses the unification and proof-tree material from L04-05/06. Assignments are mapped in the module pages and
in `assessments/README.md`. No lab depends on material that appears only later in the course.

## 7. Self-study suitability

A student working alone gets: a scenario, a specification, reference code, expected behaviour and a marking
scheme. What they do not always get is a worked first step (18 labs), a hint when stuck (only the older
template has hints), or a marking table (three projects, now fixed). These are the concrete obstacles to
unsupervised completion, and they are reported rather than smoothed over.

## 8. Verdict for this audit

The laboratory and assessment suite is substantive, aligned and honestly framed. Its gaps are scaffolding
(starter code and hints in older labs) and marking transparency in three mini-projects, which this audit
repaired. No lab was found to be a placeholder, and no assessment was found to be unmarkable.
