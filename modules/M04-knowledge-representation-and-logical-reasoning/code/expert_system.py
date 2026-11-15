"""Rule-based reasoning, forward and backward chaining, with explanations.

Used by M04 lessons L04-05 and L04-07, by LAB-04-01, LAB-04-02, LAB-04-03 and PROJECT-04-01. The
module is deliberately small: the point is that a proof is a *data structure you can print*, not a
sentence written afterwards.

Contents
--------
Rule, KnowledgeBase            : facts, rules, forward chaining, backward chaining, explanations
advising_kb()                  : synthetic university academic-advising knowledge base
family_kb()                    : synthetic family relationships
BayesNet, bayes_posterior()    : a tiny binary-network enumerator, for LAB-04-03
run_tests()                    : invariants checked on every claim the module makes
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Iterable


# ---------------------------------------------------------------------------
# Rules and knowledge base
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Rule:
    """``if_all`` → ``then``. Facts are plain hashable tuples such as ``("gpa_above", 3.5)``."""

    id: str
    if_all: tuple
    then: tuple
    note: str = ""

    def __post_init__(self):
        object.__setattr__(self, "if_all", tuple(self.if_all))
        object.__setattr__(self, "then", tuple(self.then))


@dataclass
class Derivation:
    """One step of forward chaining: the rule, its premises, and what it concluded."""

    rule: Rule
    premises: tuple
    conclusion: tuple


VARIABLE_PREFIX = "?"


def is_var(token) -> bool:
    """A token such as ``?x`` is a variable; everything else is a constant."""
    return isinstance(token, str) and token.startswith(VARIABLE_PREFIX)


def unify(pattern: tuple, fact: tuple, subst: dict | None = None) -> dict | None:
    """One-way matching: bind variables in ``pattern`` so that it equals ``fact``.

    Returns the extended substitution, or ``None`` when the shapes or constants disagree. This is
    pattern matching rather than full unification (no occurs check, no variable renaming), which is
    all a rule engine over ground facts needs — and saying so is part of the lesson.
    """
    if len(pattern) != len(fact):
        return None
    subst = dict(subst or {})
    for p, f in zip(pattern, fact):
        if is_var(p):
            if p in subst:
                if subst[p] != f:
                    return None
            else:
                subst[p] = f
        elif p != f:
            return None
    return subst


def instantiate(pattern: tuple, subst: dict) -> tuple:
    """Replace bound variables in ``pattern``; unbound variables stay as they are."""
    return tuple(subst.get(token, token) if is_var(token) else token for token in pattern)


class KnowledgeBase:
    """Facts plus rules, with forward chaining, backward chaining and explanations.

    Rules may contain variables (``"?x"``). Forward chaining fires a rule once for every binding of
    its premises that is satisfied by known facts; backward chaining proves a goal by matching rule
    heads against it and proving the premises depth-first.
    """

    def __init__(self, facts: Iterable[tuple] = (), rules: Iterable[Rule] = ()):
        self.facts: set[tuple] = {tuple(f) for f in facts}
        self.rules: list[Rule] = list(rules)
        self.derivations: dict[tuple, Derivation] = {}

    # -- construction ------------------------------------------------------
    def add_fact(self, *fact) -> None:
        self.facts.add(tuple(fact))

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    # -- forward chaining --------------------------------------------------
    def forward_chain(self) -> list[Derivation]:
        """Fire rules until no new fact can be derived; return the derivations in order."""
        added: list[Derivation] = []
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                # materialise first: the generator walks self.facts, which this loop mutates
                for subst in list(self._bindings(rule.if_all, {})):
                    conclusion = instantiate(rule.then, subst)
                    if conclusion in self.facts:
                        continue
                    self.facts.add(conclusion)
                    premises = tuple(instantiate(p, subst) for p in rule.if_all)
                    derivation = Derivation(rule, premises, conclusion)
                    self.derivations.setdefault(conclusion, derivation)
                    added.append(derivation)
                    changed = True
        return added

    def _bindings(self, goals: tuple, subst: dict):
        """Every substitution that satisfies all ``goals``, depth-first over the fact set."""
        if not goals:
            yield subst
            return
        first, rest = goals[0], goals[1:]
        for fact in self.facts:
            extended = unify(instantiate(first, subst), fact, subst)
            if extended is None:
                continue
            yield from self._bindings(rest, extended)

    # -- backward chaining -------------------------------------------------
    def backward_chain(self, goal: tuple, depth: int = 0, seen: frozenset = frozenset()) -> dict | None:
        """Prove ``goal``. Returns a proof tree (``goal``, ``kind``, ``rule``, ``children``) or None."""
        return self._prove(tuple(goal), {}, depth, seen)

    def _prove(self, goal: tuple, subst: dict, depth: int, seen: frozenset) -> dict | None:
        goal = instantiate(goal, subst)
        if not any(is_var(t) for t in goal) and goal in self.facts:
            return {"goal": goal, "kind": "fact", "rule": None, "children": [], "subst": subst}
        if goal in seen or depth > 12:
            return None
        for rule in self.rules:
            bound = unify(rule.then, goal, subst)
            if bound is None:
                continue
            children, final = self._prove_all(rule.if_all, bound, depth + 1, seen | {goal})
            if children is not None:
                return {"goal": instantiate(rule.then, final), "kind": "rule", "rule": rule,
                        "children": children, "subst": final}
        for fact in self.facts:
            bound = unify(goal, fact, subst)
            if bound is not None:
                return {"goal": fact, "kind": "fact", "rule": None, "children": [], "subst": bound}
        return None

    def _prove_all(self, goals: tuple, subst: dict, depth: int, seen: frozenset):
        nodes = []
        for goal in goals:
            node = self._prove(goal, subst, depth, seen)
            if node is None:
                return None, subst
            nodes.append(node)
            subst = node["subst"]
        return nodes, subst

    # -- explanations ------------------------------------------------------
    def explain(self, fact: tuple) -> str:
        """Render the derivation of ``fact`` as indented text, or say it was given."""
        fact = tuple(fact)
        if fact not in self.derivations:
            if fact in self.facts:
                return f"{fmt(fact)} — given as a fact"
            return f"{fmt(fact)} — not in the knowledge base"
        return self._explain(fact, indent=0)

    def _explain(self, fact: tuple, indent: int) -> str:
        derivation = self.derivations[fact]
        pad = "  " * indent
        lines = [f"{pad}{fmt(fact)}  ← by {derivation.rule.id}: {derivation.rule.note}"]
        for premise in derivation.premises:
            if premise in self.derivations:
                lines.append(self._explain(premise, indent + 1))
            else:
                lines.append(f"{pad}  {fmt(premise)}  (given)")
        return "\n".join(lines)


def fmt(fact: tuple) -> str:
    """Readable rendering of a fact tuple: ``('gpa_above', 3.5)`` → ``gpa_above(3.5)``."""
    if len(fact) == 1:
        return str(fact[0])
    return f"{fact[0]}({', '.join(str(x) for x in fact[1:])})"


def proof_text(tree: dict | None, indent: int = 0) -> str:
    """Render a backward-chaining proof tree."""
    if tree is None:
        return "  " * indent + "unprovable"
    pad = "  " * indent
    if tree["kind"] == "fact":
        return f"{pad}{fmt(tree['goal'])} (given)"
    lines = [f"{pad}{fmt(tree['goal'])} ← {tree['rule'].id}"]
    for child in tree["children"]:
        lines.append(proof_text(child, indent + 1))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Knowledge bases
# ---------------------------------------------------------------------------

def advising_kb() -> KnowledgeBase:
    """A synthetic academic-advising knowledge base. Not an official university policy."""
    kb = KnowledgeBase(rules=[
        Rule("R1", [("gpa", "high")], ("eligible", "honours"), "GPA ≥ 3.5 qualifies for honours"),
        Rule("R2", [("gpa", "mid")], ("eligible", "standard"), "GPA 2.5–3.49 qualifies for standard"),
        Rule("R3", [("gpa", "low")], ("needs", "probation_meeting"), "GPA < 2.5 triggers a meeting"),
        Rule("R4", [("english", "passed")], ("satisfies", "language_requirement"),
             "a passed language test satisfies the requirement"),
        Rule("R5", [("satisfies", "language_requirement"), ("eligible", "honours")],
             ("admit", "honours_programme"), "both conditions must hold"),
        Rule("R6", [("eligible", "standard"), ("satisfies", "language_requirement")],
             ("admit", "standard_programme"), "standard route"),
        Rule("R7", [("admit", "honours_programme")], ("scholarship", "automatic"),
             "honours admission carries a scholarship"),
        Rule("R8", [("needs", "probation_meeting"), ("attended", "meeting")],
             ("cleared", "probation"), "the meeting clears probation"),
        Rule("R9", [("prereq_cs201", "passed"), ("prereq_cs202", "passed")],
             ("eligible", "cs301"), "both prerequisites unlock CS301"),
        Rule("R10", [("credits", "insufficient")], ("admit", "conditional"),
             "credit shortfall leads to conditional admission"),
    ])
    return kb


def family_kb() -> KnowledgeBase:
    """A family knowledge base: ground facts about parents, rules with variables for the rest."""
    kb = KnowledgeBase(rules=[
        Rule("F1", [("parent", "?x", "?y")], ("ancestor", "?x", "?y"), "a parent is an ancestor"),
        Rule("F2", [("parent", "?x", "?y"), ("ancestor", "?y", "?z")],
             ("ancestor", "?x", "?z"), "ancestor is transitive"),
        Rule("F3", [("parent", "?p", "?x"), ("parent", "?p", "?y"), ("different", "?x", "?y")],
             ("sibling", "?x", "?y"), "shared parent, distinct children"),
        Rule("F4", [("sibling", "?x", "?y")], ("sibling", "?y", "?x"), "sibling is symmetric"),
        Rule("F5", [("parent", "?x", "?y"), ("sibling", "?p", "?x")],
             ("uncle_or_aunt", "?p", "?y"), "a parent's sibling is the child's aunt or uncle"),
        Rule("F6", [("uncle_or_aunt", "?u", "?n")], ("relative", "?u", "?n"),
             "aunt and uncle are relatives"),
        Rule("F7", [("ancestor", "?a", "?b")], ("relative", "?a", "?b"), "ancestors are relatives"),
    ])
    for parent, child in [("ali", "sara"), ("ali", "hina"), ("sara", "zain"),
                          ("hina", "omar"), ("zain", "ayesha")]:
        kb.add_fact("parent", parent, child)
    for a, b in [("sara", "hina"), ("zain", "omar"), ("omar", "ayesha"),
                 ("sara", "zain"), ("hina", "omar")]:
        kb.add_fact("different", a, b)
    return kb


# ---------------------------------------------------------------------------
# A tiny Bayesian network (for LAB-04-03, to contrast with logic)
# ---------------------------------------------------------------------------

@dataclass
class BayesNet:
    """Binary Bayesian network: ``cpt[node][(assignment of parents...)] = P(node=True | parents)``.

    Parents are listed in ``self.parents[node]`` in the order used by the tuple key. A node with no
    parents uses ``()`` as its key, which makes the prior a one-entry table like every other row.
    """

    parents: dict
    cpt: dict = field(default_factory=dict)

    def prob(self, node: str, value: bool, assignment: dict) -> float:
        key = tuple(assignment[p] for p in self.parents[node])
        p_true = self.cpt[node][key]
        return p_true if value else 1.0 - p_true


def bayes_posterior(net: BayesNet, query: str, evidence: dict | None = None) -> dict:
    """Exact posterior for a binary network by enumerating all hidden variables."""
    evidence = dict(evidence or {})
    nodes = list(net.parents)
    hidden = [n for n in nodes if n not in evidence and n != query]
    totals = {True: 0.0, False: 0.0}
    for values in product([True, False], repeat=len(hidden)):
        assignment = {**evidence, **dict(zip(hidden, values))}
        for q in (True, False):
            full = {**assignment, query: q}
            p = 1.0
            consistent = True
            for node in nodes:
                parents = net.parents[node]
                if any(p_name not in full for p_name in parents):
                    consistent = False
                    break
                p *= net.prob(node, full[node], full)
            if consistent:
                totals[q] += p
    z = totals[True] + totals[False]
    if z == 0:
        raise ValueError("evidence has zero probability")
    return {True: totals[True] / z, False: totals[False] / z}


def troubleshooting_net() -> BayesNet:
    """Synthetic equipment network: power fault (P) and clog (C) cause overheating (O); O causes
    the warning light (W). Every number is invented for teaching."""
    net = BayesNet(parents={"P": (), "C": (), "O": ("P", "C"), "W": ("O",)})
    net.cpt = {
        "P": {(): 0.10},
        "C": {(): 0.20},
        "O": {(True, True): 0.95, (True, False): 0.80, (False, True): 0.70, (False, False): 0.05},
        "W": {(True,): 0.90, (False,): 0.10},
    }
    return net


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def run_tests() -> bool:
    """Check that the engines derive what they claim, and that logic and probability disagree."""
    kb = advising_kb()
    kb.add_fact("gpa", "high")
    kb.add_fact("english", "passed")
    derived = kb.forward_chain()
    assert ("eligible", "honours") in kb.facts
    assert ("admit", "honours_programme") in kb.facts
    assert ("scholarship", "automatic") in kb.facts
    assert len(derived) >= 4
    # nothing is derived from unsatisfied premises
    assert ("admit", "standard_programme") not in kb.facts
    assert ("needs", "probation_meeting") not in kb.facts

    # explanation mentions the rules that produced the conclusion
    text = kb.explain(("scholarship", "automatic"))
    assert "R7" in text and "R5" in text and "given" in text

    # backward chaining proves the goal from the given facts alone, without forward chaining
    fresh = advising_kb()
    fresh.add_fact("gpa", "high")
    fresh.add_fact("english", "passed")
    proof = fresh.backward_chain(("admit", "honours_programme"))
    assert proof is not None and proof["kind"] == "rule" and proof["rule"].id == "R5"
    assert fresh.backward_chain(("admit", "standard_programme")) is None
    assert "R1" in proof_text(proof)
    # once the fact is known, the answer is immediate rather than re-derived
    assert kb.backward_chain(("admit", "honours_programme"))["kind"] == "fact"

    # forward and backward chaining agree on every derived fact
    for fact, derivation in kb.derivations.items():
        assert kb.backward_chain(fact) is not None, fact
        assert all(p in kb.facts for p in derivation.premises)

    # transitivity: ali is an ancestor of ayesha through three generations
    fam = family_kb()
    fam.forward_chain()
    assert ("ancestor", "ali", "ayesha") in fam.facts
    assert ("sibling", "hina", "sara") in fam.facts
    assert ("uncle_or_aunt", "sara", "omar") in fam.facts
    assert ("ancestor", "ayesha", "ali") not in fam.facts, "ancestry is not symmetric"

    # probability: posteriors normalise, and evidence raises the explained cause
    net = troubleshooting_net()
    prior = bayes_posterior(net, "P")
    assert abs(prior[True] - 0.10) < 1e-12
    post = bayes_posterior(net, "P", {"W": True})
    assert post[True] > prior[True] and abs(sum(post.values()) - 1) < 1e-12
    # logical inference has no notion of 0.31; it either proves or it does not
    assert post[True] > 0 and post[True] < 1
    return True


if __name__ == "__main__":
    print("expert_system self-test:", run_tests())
    kb = advising_kb()
    kb.add_fact("gpa", "high")
    kb.add_fact("english", "passed")
    kb.forward_chain()
    print(kb.explain(("scholarship", "automatic")))
