# QUIZ-M04 — Solutions and Explanations

[Quiz](quiz-m04.md) · [Assessment index](../README.md)

---

## Part A

**Q4.1 — B.** Valid means true under every interpretation. A is satisfiable, not valid; C confuses
a proof procedure with semantics; D is truth in one intended model, which is weaker than validity.

**Q4.2 — B.** Resolution operates on clauses — disjunctions of literals — so the formula must be in
CNF. Horn form (C) is a restricted subset convenient for chaining, not a requirement of resolution.

**Q4.3 — B.** Forward (data-driven) chaining starts from facts and fires rules whose premises are
satisfied; backward (goal-driven) chaining starts from the query — option A describes that.

**Q4.4 — B.** Unification finds a substitution $\theta$ such that two atomic sentences become
identical, enabling resolution in FOL. It is not proof by contradiction (that is the overall
strategy, refutation) nor CNF conversion.

## Part B

**Q4.5 — False.** Entailment is a semantic property; a *complete* proof procedure will derive it,
but completeness is not guaranteed for every procedure, and some (e.g. unrestricted forward
chaining on function symbols) may not terminate. Resolution is refutation-complete; a procedure
that only applies modus ponens is sound but incomplete.

## Part C

**Q4.6 — Model answer.** Entailment ($KB \models \alpha$) is a fact about models: every
interpretation satisfying the KB satisfies $\alpha$. Inference is a mechanical procedure that
derives sentences. The distinction matters because a procedure can be sound (derives only entailed
sentences) without being complete (misses some), or complete but slow; you choose based on which
guarantee the task needs.

**Q4.7 — Model answer.** Task: loan eligibility. Strength: the decision is auditable — each rule
can be shown to the applicant and to a regulator, and the system cannot output an outcome the
policy forbids. Limitation: the rules must be written by someone, so the system cannot exploit
patterns in data and degrades on cases the policy writer did not anticipate. A learned classifier
handles the unanticipated cases but cannot certify compliance (M14 measures exactly this: a model
produced 100 policy-violating approvals, a rule gate reduced it to zero).

## Part D

**Q4.8 —** $2^4 = 16$ rows. To refute validity you need to find **one** countermodel; in the worst
case all 16 rows are checked. (1 mark for 16, 1 for "one countermodel / up to 16 checks".)

**Q4.9 —** With 5 initial facts and at most one new fact per pass, at most 5 passes can add
anything; a 6th pass would confirm quiescence. Accept 5 (productive passes) or 6 (including the
final confirmation pass) if the reasoning is stated. 2 marks.

## Part E

**Q4.10 —** Pass 1: rule 1 fires ($P,Q$) → $R$. Pass 2: rule 2 fires ($R$) → $S$. Pass 3: rule 3
fires ($S,P$) → $T$. Derived in order: $R$, $S$, $T$. $T$ is entailed. (2 marks for the order, 2
for the entailment statement with the chain.)

## Part F

**Q4.11 —** `['P', 'Q', 'R', 'S', 'T']`

The loop runs until a pass adds nothing. Note the rule bodies are `set`s, so `body <= facts` is a
subset test; `{"S", "P"} <= facts` becomes true only after $S$ is derived, which is why the order
of passes matters even though the final set does not.

---

[Quiz](quiz-m04.md) · [Assessment index](../README.md) · [Next solutions](quiz-m05.md)
