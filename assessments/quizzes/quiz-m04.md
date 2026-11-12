# QUIZ-M04 — Knowledge Representation and Logical Reasoning

| | |
| :--- | :--- |
| Module | M04 · Knowledge Representation and Logical Reasoning |
| Questions | 11 (20 marks) |
| Time | 35 minutes |
| Covers | L04-01 … L04-07 |
| Pass mark | 12 / 20 |

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m04.md)

Closed book. Show truth tables and derivations — method marks are awarded.

---

## Part A — Multiple choice (4 marks)

**Q4.1** A sentence is *valid* when it is

- A. true in at least one interpretation
- B. true in every interpretation
- C. derivable by resolution
- D. true in the intended model only

**Q4.2** Resolution requires the premises to be in

- A. disjunctive normal form
- B. conjunctive normal form
- C. Horn form only
- D. first-order logic only

**Q4.3** Forward chaining is *data-driven* because it

- A. starts from the query and works backwards
- B. starts from known facts and applies rules until nothing new follows
- C. explores all interpretations
- D. uses heuristics to order clauses

**Q4.4** In first-order logic, unification is the process of

- A. proving a sentence by contradiction
- B. finding a substitution that makes two atomic sentences identical
- C. converting to CNF
- D. evaluating quantifiers over a finite domain

## Part B — True or false, with a reason (2 marks)

**Q4.5** "If a knowledge base entails $\alpha$, then some inference procedure will derive $\alpha$
in finite time."

## Part C — Conceptual (4 marks)

**Q4.6** (2 marks) Distinguish *entailment* from *inference*. Why does the distinction matter when
choosing an inference procedure?

**Q4.7** (2 marks) Give one strength and one limitation of a rule-based expert system compared with
a learned classifier, using the same task as the example.

## Part D — Numerical (4 marks)

**Q4.8** (2 marks) How many rows does a truth table for a sentence over four proposition symbols
have? How many of them must be checked to refute validity by finding a countermodel?

**Q4.9** (2 marks) A rule base has 6 rules and 5 initial facts. Forward chaining in the worst case
matches every rule against the working memory on each pass. How many rule-matching passes are
possible before the procedure must stop, assuming each pass adds at most one new fact?

## Part E — Tracing (4 marks)

**Q4.10** Facts: $P$, $Q$. Rules:

1. $P \wedge Q \Rightarrow R$
2. $R \Rightarrow S$
3. $S \wedge P \Rightarrow T$

Trace forward chaining and list the derived facts in order. Then state whether $T$ is entailed.

## Part F — Python output (2 marks)

**Q4.11** What does this print?

```python
facts = {"P", "Q"}
rules = [({"P", "Q"}, "R"), ({"R"}, "S"), ({"S", "P"}, "T")]
changed = True
while changed:
    changed = False
    for body, head in rules:
        if body <= facts and head not in facts:
            facts.add(head); changed = True
print(sorted(facts))
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m04.md) · [Next quiz](quiz-m05.md)
