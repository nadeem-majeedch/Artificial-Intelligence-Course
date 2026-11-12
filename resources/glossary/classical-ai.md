# Glossary — Classical AI (M03, M04, M05)

Search, knowledge representation, logic and reasoning under uncertainty. M03 and M05 have no
published lessons in this repository, so their entries link to the module page and are marked
**module page only**. Back to the [glossary index](README.md).

## A

### A\* search
**Abbreviation.** A\* · **Module.** M03
**Simple definition.** A best-first search that expands the node with the lowest estimated total
cost, $f = g + h$.
**Detailed explanation.** The cost so far $g$ keeps the search honest about what has been spent;
the heuristic $h$ focuses it on the goal. With an admissible heuristic A\* is optimal; with a
consistent one it never re-expands a node. The price is memory: it stores every frontier node.
**Mathematics.** $f(n) = g(n) + h(n)$; optimality requires $h(n) \le h^*(n)$.
**Practical example.** Routing on a road graph with straight-line distance as $h$ explores far
fewer nodes than Dijkstra while returning the same shortest path.
**Related.** [State space](#state-space), [Admissible heuristic](#admissible-heuristic), [Breadth-first search](#breadth-first-search)
**Where it is taught.** Module page only — [M03 Problem Solving and Search](../../modules/README.md#m03)

### Admissible heuristic
**Abbreviation.** — · **Module.** M03
**Simple definition.** A heuristic that never overestimates the true cost to the goal.
**Detailed explanation.** Admissibility is the condition that makes A\* optimal: if $h$ never
overestimates, the first time the goal is expanded its cost is minimal. A heuristic can be
admissible but inconsistent, in which case A\* still finds an optimal solution but may reopen
nodes.
**Mathematics.** $0 \le h(n) \le h^*(n)$ for every node $n$.
**Practical example.** Straight-line distance is admissible for road routing because no road is
shorter than the straight line; a heuristic that ignored one-way streets would not be.
**Related.** [A\* search](#a-search), [State space](#state-space)
**Where it is taught.** Module page only — [M03 Problem Solving and Search](../../modules/README.md#m03)

### Alpha–beta pruning
**Abbreviation.** — · **Module.** M03
**Simple definition.** Discarding branches of a game tree that cannot change the final decision.
**Detailed explanation.** Pruning returns the same value as minimax while examining fewer nodes,
because once a move is provably worse than an alternative it need not be explored further. With
perfect move ordering it roughly halves the exponent, which is why chess engines reach depth.
**Mathematics.** Prune when $\alpha \ge \beta$; best case examines $O(b^{d/2})$ nodes instead of $O(b^d)$.
**Practical example.** A chess engine at depth 12 with good ordering examines about as many nodes
as an unpruned depth-6 search.
**Related.** [State space](#state-space), [A\* search](#a-search)
**Where it is taught.** Module page only — [M03 Problem Solving and Search](../../modules/README.md#m03)

## B

### Bayes' rule
**Abbreviation.** — · **Module.** M05
**Simple definition.** The rule that turns a likelihood and a prior into a posterior.
**Detailed explanation.** It is the formal statement of learning from evidence: what you believed
before, reweighted by how well each hypothesis predicted what you saw. Almost every probabilistic
method in the course is Bayes' rule applied to a different representation.
**Mathematics.** $P(H \mid E) = \dfrac{P(E \mid H)\,P(H)}{P(E)}$
**Practical example.** A test with 90% sensitivity and 90% specificity at 0.8% prevalence yields
$P(\text{disease} \mid +) \approx 0.073$ — the posterior is dominated by the prior.
**Related.** [Prior and posterior](#prior-and-posterior), [Bayesian network](#bayesian-network), [Conditional independence](#conditional-independence)
**Where it is taught.** Module page only — [M05 Reasoning Under Uncertainty](../../modules/README.md#m05)

### Bayesian network
**Abbreviation.** BN · **Module.** M05
**Simple definition.** A directed acyclic graph whose nodes are variables and whose edges encode
conditional dependence.
**Detailed explanation.** The graph is a compact factorisation of a joint distribution: each node
depends only on its parents, so a distribution that would need exponentially many numbers needs
only the local tables. Inference then means computing a posterior given evidence, which is exact
in trees and approximate in general graphs.
**Mathematics.** $P(X_1,\dots,X_n) = \prod_{i} P(X_i \mid \text{Pa}(X_i))$
**Practical example.** A medical network with 20 binary variables needs ~200 parameters instead of
$2^{20}$; entering a symptom updates every diagnosis through the graph.
**Related.** [Bayes' rule](#bayes-rule), [Conditional independence](#conditional-independence), [Prior and posterior](#prior-and-posterior)
**Where it is taught.** Module page only — [M05 Reasoning Under Uncertainty](../../modules/README.md#m05)

### Breadth-first search
**Abbreviation.** BFS · **Module.** M03
**Simple definition.** Exploring all nodes at depth $d$ before any node at depth $d+1$.
**Detailed explanation.** BFS is complete and optimal when every step costs the same, because it
reaches the shallowest goal first. Its cost is memory: the frontier holds an entire level, which
is why it is unusable on large graphs where depth-first or A\* fits.
**Mathematics.** Time and space $O(b^d)$ for branching factor $b$ and goal depth $d$.
**Practical example.** Finding the shortest number of friend-connections between two people in a
social graph: correct, but the frontier at depth 4 is already millions of nodes.
**Related.** [Depth-first search](#depth-first-search), [A\* search](#a-search), [State space](#state-space)
**Where it is taught.** Module page only — [M03 Problem Solving and Search](../../modules/README.md#m03)

## C

### Conditional independence
**Abbreviation.** CI · **Module.** M05
**Simple definition.** Two variables are independent given a third when knowing the third makes
the first uninformative about the second.
**Detailed explanation.** Conditional independence is what makes probabilistic models tractable:
it licenses dropping factors from a joint distribution. In a Bayesian network it is read off the
graph by d-separation, and getting it wrong is the main source of both overconfidence and
spurious edges.
**Mathematics.** $X \perp Y \mid Z \iff P(X,Y \mid Z) = P(X \mid Z)P(Y \mid Z)$
**Practical example.** A patient's fever and cough are dependent overall but independent given
influenza; conditioning on the shared cause removes the correlation.
**Related.** [Bayesian network](#bayesian-network), [Bayes' rule](#bayes-rule)
**Where it is taught.** Module page only — [M05 Reasoning Under Uncertainty](../../modules/README.md#m05)

## D

### Depth-first search
**Abbreviation.** DFS · **Module.** M03
**Simple definition.** Following one branch as far as possible before backtracking.
**Detailed explanation.** DFS needs memory linear in depth, which makes it the practical choice on
huge trees, but it is not optimal and can loop in graphs with cycles unless visited nodes are
tracked. It is the skeleton of backtracking search for constraint problems.
**Mathematics.** Space $O(bm)$ for maximum depth $m$; time $O(b^m)$.
**Practical example.** Solving a Sudoku by filling the next empty cell and backtracking on
contradiction is depth-first search with constraint checks.
**Related.** [Breadth-first search](#breadth-first-search), [State space](#state-space)
**Where it is taught.** Module page only — [M03 Problem Solving and Search](../../modules/README.md#m03)

## E

### Expected utility
**Abbreviation.** EU · **Module.** M05
**Simple definition.** The average utility of an action, weighted by the probability of each
outcome.
**Detailed explanation.** When outcomes are uncertain, comparing best cases is wrong; comparing
expected utilities is the decision-theoretic standard. It requires both a probability model and a
utility that reflects the decision-maker's actual preferences, including risk.
**Mathematics.** $EU(a) = \sum_s P(s \mid a)\,U(s)$
**Practical example.** Two investments with the same expected return can differ in ruin
probability; expected utility with a concave $U$ prefers the one that cannot bankrupt you.
**Related.** [Bayes' rule](#bayes-rule), [Markov decision process](#markov-decision-process)
**Where it is taught.** Module page only — [M05 Reasoning Under Uncertainty](../../modules/README.md#m05)

## F

### First-order logic
**Abbreviation.** FOL · **Module.** M04
**Simple definition.** Logic with objects, relations and quantifiers, rather than bare propositions.
**Detailed explanation.** FOL can say *all* students are enrolled in some course, which
propositional logic cannot without one sentence per student. The gain in expressiveness costs
decidability: general FOL entailment is only semi-decidable, which is why inference is restricted
to restricted forms such as Horn clauses.
**Mathematics.** $\forall x\,(\text{Student}(x) \to \exists y\,(\text{Course}(y) \land \text{Enrolled}(x,y)))$
**Practical example.** A university rule base states one quantified rule instead of 4,000
per-student facts, and the same rule applies to next year's intake.
**Related.** [Propositional logic](#propositional-logic), [Unification](#unification), [Resolution](#resolution)
**Where it is taught.** [L04-04 First-order logic and quantifiers](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-04-first-order-logic-and-quantifiers.md)

### Forward chaining
**Abbreviation.** — · **Module.** M04
**Simple definition.** Deriving new facts from known facts until nothing new follows.
**Detailed explanation.** Forward chaining is data-driven: it fires rules whose premises are
satisfied and adds their conclusions. It is the natural engine for monitoring and alerting, where
facts arrive continuously and the question is "what follows from this?" rather than "is this true?".
**Mathematics.** $KB \vdash \alpha$ by repeated application of modus ponens.
**Practical example.** A fraud rule base adds `flag(account)` when `velocity > 10` and
`new_device`, then fires a second rule that blocks the card — all without being asked a question.
**Related.** [Backward chaining](#backward-chaining), [Knowledge base](#knowledge-base), [Resolution](#resolution)
**Where it is taught.** [L04-05 Unification and chaining](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-05-unification-and-chaining.md)

### Backward chaining
**Abbreviation.** — · **Module.** M04
**Simple definition.** Working backwards from a goal to the facts that would support it.
**Detailed explanation.** Backward chaining is goal-driven: it asks which rules could conclude the
goal and recurses into their premises. It explores only what is relevant to the query, which is
why diagnostic and advisory systems use it.
**Mathematics.** Prove $\alpha$ by finding a rule with head $\alpha$ and proving its body.
**Practical example.** A medical advisor asked "does this patient have influenza?" checks only the
rules that conclude influenza, rather than deriving every fact about the patient.
**Related.** [Forward chaining](#forward-chaining), [Unification](#unification), [Knowledge base](#knowledge-base)
**Where it is taught.** [L04-05 Unification and chaining](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-05-unification-and-chaining.md)

## K

### Knowledge base
**Abbreviation.** KB · **Module.** M04
**Simple definition.** A set of sentences a reasoning system treats as true.
**Detailed explanation.** The knowledge base is the declarative half of a knowledge-based agent;
the inference procedure is the procedural half. Separating them lets knowledge be edited without
rewriting the engine, which is the whole point of symbolic representation.
**Mathematics.** $KB = \{s_1, \dots, s_n\}$; the agent believes $\alpha$ when $KB \models \alpha$.
**Practical example.** A clinical guideline encoded as 300 rules can be reviewed by a clinician,
versioned, and audited line by line — unlike a weight matrix.
**Related.** [Propositional logic](#propositional-logic), [First-order logic](#first-order-logic), [Forward chaining](#forward-chaining)
**Where it is taught.** [L04-01 Knowledge representation fundamentals](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-01-knowledge-representation-fundamentals.md)

## M

### Markov decision process
**Abbreviation.** MDP · **Module.** M05
**Simple definition.** A sequential decision model with states, actions, transition
probabilities, rewards and a discount factor.
**Detailed explanation.** The Markov property says the next state depends only on the current
state and action, which makes the problem solvable by dynamic programming. MDPs are the bridge
between M05's uncertainty and M10's reinforcement learning: an MDP with unknown transitions is
exactly the RL setting.
**Mathematics.** $\langle S, A, P(s' \mid s,a), R(s,a), \gamma \rangle$
**Practical example.** A maintenance scheduler trades the cost of servicing now against the
probability of failure next month — a small MDP solved by value iteration.
**Related.** [Expected utility](#expected-utility), [Conditional independence](#conditional-independence)
**Where it is taught.** Module page only — [M05 Reasoning Under Uncertainty](../../modules/README.md#m05)

## P

### Prior and posterior
**Abbreviation.** — · **Module.** M05
**Simple definition.** The belief before seeing evidence, and the belief after.
**Detailed explanation.** The prior is not bias to be eliminated; it is the information you had
before the data arrived, and ignoring it produces overconfident conclusions. A posterior becomes
the next prior, which is how sequential updating works.
**Mathematics.** $P(H)$ prior; $P(H \mid E) \propto P(E \mid H)P(H)$ posterior.
**Practical example.** A spam filter starting at a 20% prior moves to 0.94 posterior after one
message containing "unsubscribe" and three links.
**Related.** [Bayes' rule](#bayes-rule), [Bayesian network](#bayesian-network)
**Where it is taught.** Module page only — [M05 Reasoning Under Uncertainty](../../modules/README.md#m05)

### Propositional logic
**Abbreviation.** PL · **Module.** M04
**Simple definition.** Logic whose atoms are true/false propositions combined with and, or, not
and implication.
**Detailed explanation.** Propositional logic is decidable: truth tables and resolution decide
entailment mechanically. Its limitation is expressiveness — it cannot quantify over objects — and
its practical limitation is that a knowledge base grows linearly with the number of individuals.
**Mathematics.** $\models$ is defined by truth tables over $2^n$ assignments.
**Practical example.** A access-control policy ("adult and verified, or staff") is a propositional
formula checked against a request in microseconds.
**Related.** [First-order logic](#first-order-logic), [Resolution](#resolution), [Knowledge base](#knowledge-base)
**Where it is taught.** [L04-02 Propositional logic](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-02-propositional-logic.md)

## R

### Resolution
**Abbreviation.** — · **Module.** M04
**Simple definition.** A single inference rule that derives a resolvent from two clauses
containing complementary literals.
**Detailed explanation.** Resolution is refutation-complete: to prove $\alpha$, add $\neg\alpha$
and derive the empty clause. With unification it extends to first-order logic, which is why it is
the basis of logic programming and automated theorem provers.
**Mathematics.** $\dfrac{p \lor A,\ \neg p \lor B}{A \lor B}$
**Practical example.** Proving that a scheduling constraint is unsatisfiable by resolving the
clause set to the empty clause, with each step recorded for audit.
**Related.** [Unification](#unification), [Propositional logic](#propositional-logic), [Knowledge base](#knowledge-base)
**Where it is taught.** [L04-06 Resolution and automated reasoning](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-06-resolution-and-automated-reasoning.md)

## S

### State space
**Abbreviation.** — · **Module.** M03
**Simple definition.** The set of configurations a problem can be in, with the moves that connect
them.
**Detailed explanation.** Formulating a problem as a state space — initial state, actions,
transition function, goal test, path cost — is the step that makes search applicable. Most of the
difficulty in practice is choosing a representation that keeps the space small enough to search.
**Mathematics.** $S$ states, $A$ actions, $T: S \times A \to S$, cost $c(s,a,s')$.
**Practical example.** The 8-puzzle has 181,440 reachable states, small enough to solve
optimally; the 15-puzzle has $10^{13}$, which forces heuristics.
**Related.** [A\* search](#a-search), [Breadth-first search](#breadth-first-search), [Depth-first search](#depth-first-search)
**Where it is taught.** Module page only — [M03 Problem Solving and Search](../../modules/README.md#m03)

## U

### Unification
**Abbreviation.** — · **Module.** M04
**Simple definition.** Finding a substitution that makes two logical expressions identical.
**Detailed explanation.** Unification lets a rule with variables apply to concrete facts: the
most general unifier is used so no unnecessarily specific commitment is made. It is the operation
that makes first-order inference feel like pattern matching.
**Mathematics.** $\text{UNIFY}(p(X, b), p(a, Y)) = \{X/a,\ Y/b\}$
**Practical example.** The rule `parent(X, Y) :- father(X, Y)` unifies with `father(ali, sara)` to
conclude `parent(ali, sara)`.
**Related.** [First-order logic](#first-order-logic), [Resolution](#resolution), [Backward chaining](#backward-chaining)
**Where it is taught.** [L04-05 Unification and chaining](../../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-05-unification-and-chaining.md)

---

[Glossary index](README.md) · [Foundations](foundations.md) · [Machine learning](machine-learning.md) · [Quick reference](../glossary.md)
