# PHASE 23B — Academic Quality Report

**Method:** all 89 lessons were checked structurally; a stratified sample was read in
detail, weighted toward the analytical M13/M14 material and the modules where a defect
would matter most. Lesson prose was not rewritten. Two content-level gaps are reported for
owner decision rather than patched, because filling them would mean authoring course
content during an audit.

---

## 1. Coverage of the review

| Check | Scope | Result |
| --- | --- | --- |
| Required sections | 89/89 lessons | 87 complete; 2 M13 lessons lack an explicit objectives list |
| Exercise sets | 89/89 lessons | 4–9 items each; median 5; no lesson below 4 |
| Objectives items | 89/89 lessons | 87 with 3–8 items; 2 with 0 (see §3) |
| Placeholder text | 89/89 lessons | no `TODO`/`TBD`/`FIXME`/"coming soon"; 88 "? Lesson" navigation placeholders found and fixed |
| Prose length | 89/89 lessons | 816–3,395 words; median 1,957; M12 is the shortest module (mean 944) |
| Deep reading | 8 lessons + 2 labs + 4 quiz answers | L01-01, L04-03, L07-02, L11-05, L13-01/02/03, L14-01/02, LAB-05-02, LAB-13-01, QUIZ-M05, QUIZ-M10 |
| Numerical spot checks | 4 answers + 32 audit assertions | all correct (see §5) |
| M13/M14 analytical exercises | all 12 sets in the two modules | graded, feasible, appropriate (see §4) |

Per-module lesson counts: M01 5, M02 5, M03 7, M04 7, M05 6, M06 10, M07 8, M08 6,
M09 6, M10 5, M11 7, M12 6, M13 6, M14 5.

## 2. What is academically sound

- **Structure is consistent.** Lessons follow objectives → prerequisite knowledge →
  conceptual explanation → procedure → worked example → mathematics → Python →
  applications → mistakes → exercises → self-check → key terms → further reading. M13/M14
  use a shorter analytical variant, which is appropriate for their material.
- **Exercises are graded and non-trivial.** L01-01 asks students to score six systems,
  rewrite a marketing claim three ways, construct a counter-example to the course's own
  scoring rule, and design a Turing-test variant; hints are present without answers.
  M12 mixes implementation tasks with architecture and failure-mode questions.
- **Self-assessment answers are worked, not one-line.** L01-01 answers include the
  reasoning and a stated dissent ("many engineers would call it automation"), which is
  exactly the critical-thinking behaviour the brief asks for.
- **The mathematics is correct in the sampled lessons.** The backpropagation derivation in
  L07-02 uses the standard batch conventions and is consistent with the `1/n` factor inside
  `Δ^(L)`; the resolution/modus-tollens proofs in L04-03 are sound; L09-02's Otsu
  description matches the implementation (quantised between observed min and max, returned
  in input units), which was the Phase 23 defect and remains fixed.
- **Learning objectives match exercises** in every sampled lesson: each objective has at
  least one exercise or self-check that requires it.
- **Claims are referenced where they need to be.** Advanced material is labelled
  (M11/M13/M14 are explicit about research-frontier status), and the bibliography is real
  rather than decorative — 95 entries, 38 arXiv identifiers, all verified in Phase 23B.

## 3. Defects found

### 3.1 Fixed during this audit (safe, mechanical)

| Defect | Location | Extent | Fix |
| --- | --- | --- | --- |
| Literal "? Lesson" in navigation links | 22 lesson files, 88 occurrences (both header and footer) | M06–M11 lessons | Replaced with the target lesson's identifier, matching the style already used in the same files (`Previous: L06-01`, `Next: L06-03 →`) |
| Heading said "four-line proof" while the proof has five lines | `modules/M04-…/lessons/L04-03-inference-rules-and-equivalence.md` lines 19 and 143 | 1 lesson | Renamed to "five-line proof" and updated the in-page anchor |
| Stale architecture links (Phase 23A leftovers checked) | `docs/ARCHITECTURE.md` | 3 paths + 1 duplicate diagram line | Already corrected in 23A; verified still present |

The navigation defect was user-visible on every affected lesson and had no academic
meaning; the fix changes link text only.

### 3.2 Reported for owner decision (content-level)

| Finding | Location | Why it is not fixed here |
| --- | --- | --- |
| **No explicit "What you will be able to do" section** | `L13-03-privacy-memorisation-and-model-attacks.md` (starts at "Why this lesson exists") and `L13-04-security-adversarial-examples-and-prompt-injection.md` | The lessons do state intended work in prose ("You will run two of these attacks…"), but writing a formal objectives list means authoring content. It is a consistency gap with L13-01/02/05/06, not a missing lesson. |
| **No deliverables section** | `modules/M05-…/labs/lab-05-02-bayesian-network-inference-and-diagnosis.md` | The lab has expected behaviour, tests, a rubric and reflection questions, but never says what to submit. Every other lab does. Adding it is a small authorial decision (report format and length). |
| **Study-hour table inconsistent with measured hours** | `docs/CURRICULUM-MAP.md` §2: modules ≈318 h, total ≈374 h; line 442 says 350.7 h measured (≈407 with prerequisites) | The measured sum of the 14 module READMEs is **350.7 h**, and 407 − 351 = 56 matches the prerequisite row, so the table is stale rather than wrong in method. Changing published course totals is an academic claim, so it needs the owner's decision. |
| **M14-01 starter does not demonstrate the graph effect** | `modules/M14-…/labs/starters/lab-14-01_starter.py` | The synthetic task saturates: graph model 1.000, feature-only baseline 1.000. The TODO asks whether the graph is doing any work, but the printed baseline makes the question uninteresting. Making the informative feature weaker would restore the intended contrast; that changes the exercise's expected output. |
| **Exercise counts above the 2–4 brief** | 8 M01–M11 lessons (7–9 items) | Deliberately not trimmed. Removing real exercises to satisfy a count would be the same error as padding. |

## 4. M13 and M14 analytical exercises

All twelve exercise sets were read. They are graded `Beginner/Intermediate/Advanced`, and
the advanced items are genuine independent work rather than harder restatements:

- **M13-01 fairness:** run the baseline and interpret four metrics; change the split seed
  and measure metric movement; remove the group-B label bias and compare DP vs equal
  opportunity; implement random selection and explain which definition it satisfies;
  bootstrap 95 % intervals; construct a dataset where reweighting changes the boundary.
- **M13-02 explainability:** permutation importance with the correlation caveat; partial
  dependence resolution; implement KernelSHAP with the kernel weight and report the
  efficiency gap; LIME stability vs sample count; constrained counterfactuals;
  shuffled-label sanity check at 5 % data.
- **M13-03/04** add threat-model, membership-inference, extraction and prompt-injection
  tasks with explicit "never attack a system you do not own" constraints.
- **M14-01:** contrastive retrieval, graph message passing, comparison and decision;
  exercises add modality ablation and heterogeneous edges.
- **M14-02:** serving/quantisation exercises add p95 budgets, a quantisation sweep and a
  rollback runbook.

They are feasible with the shipped synthetic data and CPU code; the only Python required is
where the topic itself is computational (SHAP, bootstrap, serving). No exercise in M13/M14
forces irrelevant implementation.

## 5. Numerical verification performed

| Item | Claim | Independent result |
| --- | --- | --- |
| QUIZ-M05 Q5.8 | P(D\|+) ≈ 0.167 | 0.0099 / 0.0594 = **0.1667** ✔ |
| QUIZ-M10 Q10.8 | G₀ = 2.62 | 1 + 0.9·0 + 0.81·2 = **2.62** ✔ |
| QUIZ-M10 Q10.9 | Q ← 3.3 | 2 + 0.5(1 + 3.6 − 2) = **3.3** ✔ |
| QUIZ-M10 Q10.10 | action B | Q(A)=1, Q(B)=4.5 → **B** ✔ |
| `audit/math_verify.py` | 32 claims across search, logic, probability, ML, NN, RL, fairness | **32/32 passed** |

## 6. Terminology and progression

- Terminology is used consistently in the sampled lessons: "hypothesis class", "entropy",
  "evidence", "posterior", "TD target", "replay buffer" are defined at first use and then
  reused. No conflicting definitions were found in the sample.
- Prerequisites are declared in every lesson, either as a front-matter table row
  (`| Prerequisites | … |`) or a "Prerequisite Knowledge" section; the structural checker
  initially flagged 25 M07/M11 lessons only because it looked for the wrong heading.
- Progression is coherent: M01 defines AI; M02 agent/environment vocabulary; M03 search;
  M04 logic; M05 uncertainty; M06–M09 learning; M10–M12 RL/generative/agents; M13–M14
  responsibility and systems. M13/M14 lessons reference earlier modules explicitly.

## 7. Limitations of this review

- Eight lessons were read closely, not all 89; the remaining 81 were checked structurally
  and through their exercises/objectives, which cannot detect a subtly wrong sentence.
- No subject-matter peer review was performed; "correct" here means "internally consistent,
  numerically checked where testable, and consistent with the cited literature".
- Prose style, accessibility and cultural fit were not assessed.
- The two content gaps in §3.2 need an author, not a checker.

## 8. Recommendation

Address the two §3.2 lesson/lab gaps and decide the study-hour table before academic
review. The rest of the sampled material meets the standard the course claims for itself.
