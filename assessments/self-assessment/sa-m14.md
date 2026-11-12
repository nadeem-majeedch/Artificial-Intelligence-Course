# SA-M14 — Self-Assessment: Advanced Applications and Capstone

Module M14 · [Module](../../modules/M14-advanced-ai-applications-and-capstone/README.md) · [Quiz](../quizzes/quiz-m14.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Explain when a hybrid rule/model system is worth its complexity
- [ ] Describe knowledge distillation and what the student learns
- [ ] Explain quantisation and pruning, and their measured trade-offs
- [ ] Compute and interpret PSI for drift detection
- [ ] Explain message passing and homophily in a GNN
- [ ] Describe federated averaging and its limitations
- [ ] State the components of a production ML system

## Knowledge-check questions

1. Why did the hybrid system in the module score lower than the rules alone?
2. Why can int8 be slower than float despite being smaller?
3. PSI is 0.31 — what does that indicate and what do you do next?
4. Why did the 8-layer GCN score 0.25?
5. What does a global federated average hide?

## Practical competency checklist

- [ ] Reproduce a module experiment and its reported numbers
- [ ] Run an ablation and attribute the change
- [ ] Produce a drift report from reference and current distributions
- [ ] Present results with limits and one recommended next step

## Suggested revision topics

Hybrid and neurosymbolic systems · compression and serving cost · drift and monitoring · graph
learning · federated learning · MLOps and the model registry · capstone scoping.

## Readiness test for the capstone review

Without notes:

1. State your capstone's claim, the metric that would support it, and the baseline.
2. Name the failure mode most likely to undermine it, and the test that would reveal it.
3. Explain what you would measure if the model cannot be deployed as planned.

If any is shaky, revisit L14-02 and the capstone rubric before the review.
