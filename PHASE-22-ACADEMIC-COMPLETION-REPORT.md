# Phase 22 — Academic Completion Report

**Date:** 12 November 2026 · **Scope:** M09 Computer Vision, M10 Reinforcement Learning, M04 laboratories
and mini-project, study-hour reconciliation, navigation and validation.

Nothing was committed, staged or pushed. No workflow, Pages configuration or deployment was created.

## 1. Summary

| Deliverable | Status | Evidence |
| :--- | :--- | :--- |
| M09 module (6 lessons, 4 labs, 4 notebooks, code, page) | complete | files counted, notebooks executed |
| M10 module (5 lessons, 4 labs, 3 notebooks, project, code, page) | complete | files counted, notebooks executed |
| M04 (3 labs + mini-project + engine) | complete | files counted, engine self-test |
| Study-hour reconciliation (14 modules) | complete | computed from content, one convention |
| Navigation and curriculum integration | complete | 4,084 internal links, 0 broken |
| Validation | complete | see §7 |
| New notebooks executed from clean kernels | 7 of 7, 0 errors | see §6 |

## 2. M09 — Computer Vision

**Created:** `modules/M09-computer-vision/` with

- **6 lessons** — L09-01 introduction and image representation; L09-02 image processing and feature
  extraction; L09-03 classification and CNNs; L09-04 object detection; L09-05 image segmentation;
  L09-06 advanced vision (transfer learning, ViT, multimodal).
- **4 labs** — LAB-09-01 image processing and HOG features; LAB-09-02 CNN classification; LAB-09-03
  detection metrics and NMS; LAB-09-04 U-Net segmentation. Each carries scenario, problem statement,
  outcomes, background, dataset and licence, software, tasks, starter code, expected behaviour, metrics,
  testing, submission, rubric and extensions. Verified: 4 of 4 contain all required sections.
- **4 notebooks** — processing, classification, detection, segmentation. Executed from clean kernels with
  stored outputs; 0 errors.
- **`code/vision_core.py`** — synthetic dataset generators (leaves, signs, detection scenes, road masks),
  convolution, Sobel, Otsu, morphology, HOG, IoU, NMS, box matching, 11-point AP, Dice, mean IoU, TinyCNN,
  TinyUNet, `run_tests()`.

**Measured facts used in lessons and labs** (this machine, CPU):

| Claim | Measurement |
| :--- | :--- |
| Sign classifier, 3 epochs, 90/30 split | train 0.878, test 1.000 |
| HOG + logistic regression on the same split | test 1.000 |
| Leaf classifier, 8 epochs, 140/40 split | train 0.76, test 0.95 |
| HOG + logistic regression on leaves | test 0.95 |
| Colour-rule road baseline | pixel accuracy > 0.95, mIoU 0.65, obstacle Dice 0.00 |
| U-Net, 60 scenes, 15 epochs | training mIoU 0.95, about 29 s |

The module deliberately teaches the negative result: on tiny synthetic data the classical baseline matches
the CNN, so the CNN is not evidence of superiority.

**Dataset licensing:** every image is generated in code; no third-party dataset is redistributed and no
pretrained weights are used. The module says so in the page and in every lab, and states that synthetic
scenes are not field data.

## 3. M10 — Reinforcement Learning

**Preserved:** `rl_envs.py`, `dp.py`, `tabular.py`, `dqn.py` were not rewritten. One new file was added:
`experiments.py` (seeded comparisons + `run_tests()`).

**Created:**

- **5 lessons** — L10-01 foundations and MDPs; L10-02 value-based learning and DP; L10-03 temporal
  difference, SARSA and Q-learning; L10-04 DQN, policy gradients and PPO; L10-05 continuous actions, offline
  RL, reward hacking, multi-agent and safety.
- **4 labs** — grid-world Q-learning; SARSA vs Q-learning on cliff walking; CartPole DQN; policy-based
  learning and PPO. All 4 contain the required section set.
- **3 notebooks** — MDPs and DP; tabular control; deep RL. Executed, 0 errors.
- **MP-10 project** — inventory-control agent, with environment specification, architecture, milestones and
  rubric.
- **Module page rewritten** with hours, map, dependencies and fallbacks.

**Measured facts:**

| Claim | Measurement |
| :--- | :--- |
| SARSA vs Q-learning, cliff walking, 300 episodes, 3 seeds | SARSA tail −32.4, Q-learning tail −35.8 |
| Q-learning on 4×4 grid, 300 episodes | tail return above the random floor (asserted in `experiments.run_tests()`) |
| Greedy policy, clean vs slippery grid | return 0.80 vs 0.711, both success 1.0 |

**Honest limits.** The DQN and PPO labs are not solved benchmarks here: short CPU runs are enough to see
the curve move, not to reach the 500-step ceiling. The lessons and labs state expected ranges rather than
claiming a measured solve, and the labs require students to report their own numbers. The DQN/PPO budget is
therefore **not** evidence that the algorithms converge on this machine.

## 4. M04 — Laboratories and mini-project

**Created:** `code/expert_system.py` (unifying forward and backward chaining, explanations, a synthetic
advising knowledge base, a family knowledge base, and a tiny Bayesian network for the logic/probability
contrast), plus

- LAB-04-01 rule-based expert system (advising scenario);
- LAB-04-02 logic-based reasoning and inference (family knowledge base, proof trees);
- LAB-04-03 Bayesian and knowledge-based decision support (same troubleshooting scenario, two paradigms);
- PROJECT-04-01 intelligent university advisory expert system.

All three labs carry the full section set; the project carries problem statement, requirements,
architecture, starter code, milestones, expected functionality, criteria and extensions. The module page now
lists 3 labs and the project, and its "in preparation" note is gone.

**Defects found and fixed while building the engine** (the module's lessons described behaviour that did not
work):

1. The first implementation matched rule premises propositionally, so the recursive `ancestor` rule could
   never fire. Replaced with one-way unification and variable instantiation; the family rules now use `?x`
   variables.
2. Rule F5 encoded the aunt relation backwards (`parent(?p,?x), sibling(?x,?y)`), so no aunt was ever
   derived. Rewritten as `parent(?x,?y), sibling(?p,?x)`.
3. Forward chaining iterated `self.facts` while adding to it, raising `RuntimeError: Set changed size during
   iteration`. Bindings are now materialised before the fact set is mutated.

`expert_system.run_tests()` asserts soundness, proof-tree structure, transitivity, the negative cases, and
that `P(P | W) = 0.258` moves above its prior.

## 5. Study-hour reconciliation

A single convention is now written into **every** module page:

| Category | Definition |
| :--- | :--- |
| Guided study | lesson reading, examples, self-checks (sum of lesson headers) |
| Practical | lab time (from each lab's stated time) + 30 min per notebook |
| Independent assessment | quiz + programming assignment + self-assessment |
| Project | mini-project or capstone time |
| Total | the sum of the four; optional extensions excluded and stated separately |

Hours were computed from the files, not copied between documents:

| Module | Guided | Practical | Assessment | Project | Total |
| :--- | ---: | ---: | ---: | ---: | ---: |
| M01 | 4.5 | 2.5 | 3.8 | 0.0 | 10.8 |
| M02 | 7.1 | 6.0 | 4.8 | 0.0 | 17.9 |
| M03 | 10.0 | 5.0 | 4.9 | 0.0 | 19.9 |
| M04 | 8.8 | 9.0 | 4.8 | 9.0 | 31.6 |
| M05 | 8.8 | 7.0 | 4.8 | 0.0 | 20.6 |
| M06 | 10.0 | 12.0 | 5.9 | 0.0 | 27.9 |
| M07 | 8.0 | 9.0 | 5.9 | 0.0 | 22.9 |
| M08 | 9.5 | 9.0 | 5.8 | 0.0 | 24.3 |
| M09 | 7.5 | 13.5 | 5.8 | 0.0 | 26.8 |
| M10 | 6.7 | 12.5 | 5.9 | 9.0 | 34.1 |
| M11 | 7.0 | 8.5 | 5.8 | 0.0 | 21.3 |
| M12 | 8.0 | 5.0 | 5.8 | 0.0 | 18.8 |
| M13 | 9.0 | 5.5 | 5.9 | 2.0 | 22.4 |
| M14 | 7.5 | 5.5 | 5.9 | 14.0 | 32.9 |

Both central tables (`README.md` §9 and `modules/README.md`) now carry these totals, and
`docs/learning-path.md` was rewritten where it claimed M03, M05 and M09 were unpublished: Path A now lists
the published sequence with measured hours (≈185 against the 165-hour design figure), and the
specialisation table no longer says the vision and decision routes are incomplete.

**Known limitation:** the M06/M11/M07 lab hours come from each lab's own `~150 minutes` header, not from a
timed run. They are estimates by the author, consistent with the convention, and are not measurements.

## 6. Notebook execution

Seven new notebooks were executed from clean kernels with `nbclient` (240 s per-cell timeout, working
directory set to the notebook folder), and the stored outputs contain no error cells:

| Notebook | Module | Status |
| :--- | :--- | :--- |
| `nb-09-01-image-processing.ipynb` | M09 | PASS |
| `nb-09-02-cnn-classification.ipynb` | M09 | PASS |
| `nb-09-03-object-detection.ipynb` | M09 | PASS |
| `nb-09-04-image-segmentation.ipynb` | M09 | PASS |
| `nb-10-01-mdps-and-dynamic-programming.ipynb` | M10 | PASS |
| `nb-10-02-tabular-control-sarsa-and-q-learning.ipynb` | M10 | PASS |
| `nb-10-03-deep-reinforcement-learning.ipynb` | M10 | PASS |

The 28 previously existing notebooks were **not** re-executed in this phase, so
`NOTEBOOK-REGRESSION-REPORT.md` still stands as the record of that run; this report makes no claim about
them beyond their last recorded execution. The repository now contains 35 notebooks in total.

One notebook limitation is stated openly: NB-09-04's collapse cell uses a hand-written majority-class mask
as a stand-in for the unweighted model, because training the unweighted variant inside the notebook would
double its runtime. The lab asks students to run the unweighted training themselves; the notebook says the
numbers are the same order.

## 7. Validation results

| Check | Result |
| :--- | :--- |
| Markdown files scanned | 366 |
| Internal links / anchors checked | 4,084 |
| Broken links or anchors | **0** |
| Python files compiled | 72, **0 failures** |
| `vision_core.run_tests()` | True |
| `experiments.run_tests()` | True |
| `expert_system.run_tests()` | True |
| New labs with all required sections | 11 of 11 (M04 3, M09 4, M10 4) |
| New notebooks structurally valid, no error outputs | 7 of 7 |
| Quizzes with answer keys | 14 of 14 |
| Quizzes still claiming their module is unpublished | 0 |
| Lab / notebook totals | 38 labs, 35 notebooks, 89 module lessons |
| Dataset licensing | all new datasets generated in code; no third-party data redistributed |
| Duplicate content | M04 labs reuse the `expert_system` engine deliberately; M09 and M10 have no duplicated worked examples |

Bugs found during validation and fixed: 13 broken links (wrong PA, M07 and M05 filenames) in the new M09/M10
pages, plus the M04 rule-engine defects in §4.

## 8. Remaining gaps and caveats

1. **No measured DQN/PPO convergence** on this machine. The labs are runnable and bounded, but a student
   needs several minutes per run and the module does not claim a solved benchmark.
2. **All M09 data is synthetic.** Accuracies on generated images say nothing about field performance; the
   module repeats this in the page and every lab, and PA-09 requires a corruption study precisely because of it.
3. **Lab time estimates** in the older modules are authored, not measured (§5).
4. **M14 capstone hours** (14.0) were taken from the module page's own statement, not derived from a project
   file, because the capstone has no timed artefact.
5. **Older notebooks** were not re-executed in this phase.
6. **No instructor identity, licence file or CI** was added: those are owner decisions, not defects to fix
   silently.

## 9. Verdict

**PASS WITH WARNINGS.**

Every one of the fourteen advertised modules now has actual teaching material and practical learning
activities: lessons (89 in total), laboratories (38), notebooks (35), a project or assignment, and a module
page whose counts match the files. M09 and M10 are no longer syllabus entries, M04 no longer lacks labs, and
the three documents that disagreed about hours now share one definition and one set of numbers.

The warnings are about evidence, not completeness: the deep-RL labs are not measured to convergence here,
the vision data is synthetic by design, and several time estimates remain authored rather than timed. A
reader who needs a solved CartPole or a field-accurate leaf classifier will not find it in this repository,
and the module pages say so.
