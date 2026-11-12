"""First-order logic: terms, unification, chaining and resolution.

Standard library only. The module supports the subset of first-order
logic that the module's lessons and labs need: predicates, variables,
constants, function symbols, the connectives and both quantifiers.

Run ``python fol_core.py`` for a self-checking demonstration.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from typing import Iterable, Iterator


# ---------------------------------------------------------------------------
# 1. Terms
# ---------------------------------------------------------------------------


class Term:
    """Base class for first-order terms."""


@dataclass(frozen=True)
class Var(Term):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Const(Term):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Func(Term):
    name: str
    args: tuple[Term, ...]

    def __str__(self) -> str:
        return f"{self.name}({', '.join(map(str, self.args))})"


def func(name: str, *args: Term) -> Func:
    return Func(name, tuple(args))


Substitution = dict[str, Term]


# ---------------------------------------------------------------------------
# 2. Formulas
# ---------------------------------------------------------------------------


class Formula:
    """Base class for first-order formulas."""


@dataclass(frozen=True)
class Pred(Formula):
    name: str
    args: tuple[Term, ...] = ()

    def __str__(self) -> str:
        if not self.args:
            return self.name
        return f"{self.name}({', '.join(map(str, self.args))})"


def pred(name: str, *args: Term) -> Pred:
    return Pred(name, tuple(args))


@dataclass(frozen=True)
class NotF(Formula):
    arg: Formula

    def __str__(self) -> str:
        inner = self.arg
        if isinstance(inner, (AndF, OrF, ImpliesF)):
            return f"¬({inner})"
        return f"¬{inner}"


@dataclass(frozen=True)
class AndF(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"


@dataclass(frozen=True)
class OrF(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"


@dataclass(frozen=True)
class ImpliesF(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} → {self.right})"


@dataclass(frozen=True)
class Forall(Formula):
    var: Var
    body: Formula

    def __str__(self) -> str:
        return f"∀{self.var} {self.body}"


@dataclass(frozen=True)
class Exists(Formula):
    var: Var
    body: Formula

    def __str__(self) -> str:
        return f"∃{self.var} {self.body}"


_ASCII = {"∧": "and", "∨": "or", "¬": "not ", "→": "->", "∀": "forall ", "∃": "exists "}


def plain(text: str) -> str:
    """ASCII-safe spelling, for consoles that cannot print logic symbols."""
    for fancy, simple in _ASCII.items():
        text = text.replace(fancy, simple)
    return text


# ---------------------------------------------------------------------------
# 3. Substitution
# ---------------------------------------------------------------------------


def walk(term: Term, subst: Substitution) -> Term:
    """Follow a chain of variable bindings to its end."""
    while isinstance(term, Var) and term.name in subst:
        term = subst[term.name]
    return term


def substitute(term: Term, subst: Substitution) -> Term:
    term = walk(term, subst)
    if isinstance(term, Func):
        return Func(term.name, tuple(substitute(a, subst) for a in term.args))
    return term


def substitute_formula(formula: Formula, subst: Substitution) -> Formula:
    """Apply *subst* to every free variable of *formula* (capture-avoiding enough here)."""
    if isinstance(formula, Pred):
        return Pred(formula.name, tuple(substitute(a, subst) for a in formula.args))
    if isinstance(formula, NotF):
        return NotF(substitute_formula(formula.arg, subst))
    if isinstance(formula, (AndF, OrF, ImpliesF)):
        return type(formula)(substitute_formula(formula.left, subst),
                             substitute_formula(formula.right, subst))
    if isinstance(formula, (Forall, Exists)):
        inner = {k: v for k, v in subst.items() if k != formula.var.name}
        return type(formula)(formula.var, substitute_formula(formula.body, inner))
    raise TypeError(formula)


# ---------------------------------------------------------------------------
# 4. Unification
# ---------------------------------------------------------------------------


def occurs(var: Var, term: Term) -> bool:
    term = walk(term, {})
    if term == var:
        return True
    if isinstance(term, Func):
        return any(occurs(var, a) for a in term.args)
    return False


def unify(x: Term, y: Term, subst: Substitution | None = None) -> Substitution | None:
    """Most general unifier of two terms, or None.

    >>> unify(pred("p", Var("x")).args[0], Const("a"))
    {'x': Const(name='a')}
    """
    if subst is None:
        subst = {}
    x, y = walk(x, subst), walk(y, subst)
    if x == y:
        return subst
    if isinstance(x, Var):
        if occurs(x, y):
            return None
        return {**subst, x.name: y}
    if isinstance(y, Var):
        if occurs(y, x):
            return None
        return {**subst, y.name: x}
    if isinstance(x, Func) and isinstance(y, Func):
        if x.name != y.name or len(x.args) != len(y.args):
            return None
        for a, b in zip(x.args, y.args):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None


def unify_atoms(p: Pred, q: Pred, subst: Substitution | None = None) -> Substitution | None:
    if p.name != q.name or len(p.args) != len(q.args):
        return None
    if subst is None:
        subst = {}
    for a, b in zip(p.args, q.args):
        subst = unify(a, b, subst)
        if subst is None:
            return None
    return subst


# ---------------------------------------------------------------------------
# 5. Clauses and resolution
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Clause:
    """A disjunction of literals; a literal is (positive?, Pred)."""

    literals: frozenset[tuple[bool, Pred]]

    def __str__(self) -> str:
        if not self.literals:
            return "□"
        parts = []
        for positive, atom in sorted(self.literals, key=lambda lit: (not lit[0], str(lit[1]))):
            parts.append(str(atom) if positive else f"¬{atom}")
        return " ∨ ".join(parts)


def _standardize(formula: Formula, tag: str) -> Formula:
    """Rename every variable in *formula* with a unique suffix (avoid capture)."""
    mapping: dict[str, str] = {}

    def rename(formula: Formula) -> Formula:
        if isinstance(formula, Pred):
            return Pred(formula.name, tuple(_rename_term(a, mapping, tag) for a in formula.args))
        if isinstance(formula, NotF):
            return NotF(rename(formula.arg))
        if isinstance(formula, (AndF, OrF, ImpliesF)):
            return type(formula)(rename(formula.left), rename(formula.right))
        if isinstance(formula, (Forall, Exists)):
            mapping[formula.var.name] = f"{formula.var.name}_{tag}"
            return type(formula)(Var(mapping[formula.var.name]), rename(formula.body))
        raise TypeError(formula)

    return rename(formula)


def _rename_term(term: Term, mapping: dict[str, str], tag: str) -> Term:
    if isinstance(term, Var):
        return Var(mapping.get(term.name, f"{term.name}_{tag}"))
    if isinstance(term, Func):
        return Func(term.name, tuple(_rename_term(a, mapping, tag) for a in term.args))
    return term


def _eliminate_arrows(formula: Formula) -> Formula:
    if isinstance(formula, Pred):
        return formula
    if isinstance(formula, NotF):
        return NotF(_eliminate_arrows(formula.arg))
    if isinstance(formula, ImpliesF):
        return OrF(NotF(_eliminate_arrows(formula.left)), _eliminate_arrows(formula.right))
    if isinstance(formula, (AndF, OrF)):
        return type(formula)(_eliminate_arrows(formula.left), _eliminate_arrows(formula.right))
    if isinstance(formula, (Forall, Exists)):
        return type(formula)(formula.var, _eliminate_arrows(formula.body))
    raise TypeError(formula)


def _nnf(formula: Formula, negated: bool = False) -> Formula:
    """Negation normal form: negations only in front of predicates."""
    if isinstance(formula, Pred):
        return NotF(formula) if negated else formula
    if isinstance(formula, NotF):
        return _nnf(formula.arg, not negated)
    if isinstance(formula, AndF):
        constructor = OrF if negated else AndF
        return constructor(_nnf(formula.left, negated), _nnf(formula.right, negated))
    if isinstance(formula, OrF):
        constructor = AndF if negated else OrF
        return constructor(_nnf(formula.left, negated), _nnf(formula.right, negated))
    if isinstance(formula, (Forall, Exists)):
        if isinstance(formula, Forall):
            constructor = Exists if negated else Forall
        else:
            constructor = Forall if negated else Exists
        return constructor(formula.var, _nnf(formula.body, negated))
    raise TypeError(formula)


def _skolemize(formula: Formula, universals: tuple[str, ...],
               counter: Iterator[int]) -> Formula:
    if isinstance(formula, (Pred, NotF)):
        return formula
    if isinstance(formula, AndF):
        return AndF(_skolemize(formula.left, universals, counter),
                    _skolemize(formula.right, universals, counter))
    if isinstance(formula, OrF):
        return OrF(_skolemize(formula.left, universals, counter),
                   _skolemize(formula.right, universals, counter))
    if isinstance(formula, Forall):
        return _skolemize(formula.body, universals + (formula.var.name,), counter)
    if isinstance(formula, Exists):
        name = f"sk{next(counter)}"
        if universals:
            term: Term = Func(name, tuple(Var(u) for u in universals))
        else:
            term = Const(name)
        return _skolemize(substitute_formula(formula.body, {formula.var.name: term}),
                          universals, counter)
    raise TypeError(formula)


def _cnf_parts(formula: Formula) -> list[frozenset[tuple[bool, Pred]]]:
    if isinstance(formula, AndF):
        return _cnf_parts(formula.left) + _cnf_parts(formula.right)
    literals: set[tuple[bool, Pred]] = set()

    def collect(node: Formula) -> None:
        if isinstance(node, OrF):
            collect(node.left)
            collect(node.right)
        elif isinstance(node, NotF):
            literals.add((False, node.arg))       # type: ignore[arg-type]
        elif isinstance(node, Pred):
            literals.add((True, node))
        else:
            raise TypeError(f"not in CNF: {node}")

    collect(formula)
    return [frozenset(literals)]


def to_clauses(formula: Formula, tag: str = "0") -> list[Clause]:
    """Convert a closed formula to a list of clauses (with skolemisation)."""
    body = _eliminate_arrows(formula)
    body = _standardize(body, tag)
    body = _nnf(body)
    body = _skolemize(body, (), count(0))
    return [Clause(lits) for lits in _cnf_parts(body)]


def resolve_clauses(ci: Clause, cj: Clause) -> list[Clause]:
    """All binary resolvents of two clauses, after unifying complementary literals."""
    resolvents: list[Clause] = []
    for pi, ai in ci.literals:
        for pj, aj in cj.literals:
            if pi == pj:
                continue
            subst = unify_atoms(ai, aj)
            if subst is None:
                continue
            literals: set[tuple[bool, Pred]] = set()
            for p, atom in ci.literals:
                if (p, atom) != (pi, ai):
                    literals.add((p, substitute_formula(atom, subst)))  # type: ignore[arg-type]
            for p, atom in cj.literals:
                if (p, atom) != (pj, aj):
                    literals.add((p, substitute_formula(atom, subst)))  # type: ignore[arg-type]
            resolvents.append(Clause(frozenset(literals)))
    return resolvents


def fol_resolution(kb: Iterable[Formula], query: Formula,
                   max_steps: int = 400) -> tuple[bool, list[str]]:
    """Prove KB ⊨ query by refutation, with a readable trace."""
    clauses: list[Clause] = []
    for i, formula in enumerate(list(kb) + [NotF(query)]):
        clauses.extend(to_clauses(formula, tag=str(i)))

    trace = [f"start: {len(clauses)} clauses"]
    for c in clauses:
        trace.append(f"  given: {plain(str(c))}")

    seen = set(clauses)
    for _ in range(max_steps):
        new: list[Clause] = []
        for i, ci in enumerate(clauses):
            for cj in clauses[i + 1:]:
                for resolvent in resolve_clauses(ci, cj):
                    if not resolvent.literals:
                        trace.append(f"resolve {plain(str(ci))} with {plain(str(cj))} -> empty clause")
                        return True, trace
                    if resolvent not in seen:
                        seen.add(resolvent)
                        new.append(resolvent)
                        trace.append(f"resolve {plain(str(ci))} with {plain(str(cj))} "
                                     f"-> {plain(str(resolvent))}")
        if not new:
            trace.append("no new clauses: no refutation exists")
            return False, trace
        clauses.extend(new)
    trace.append(f"step limit {max_steps} reached")
    return False, trace


# ---------------------------------------------------------------------------
# 6. Forward chaining over definite clauses
# ---------------------------------------------------------------------------


def variables_in(formula: Formula) -> set[str]:
    """Names of the variables occurring in *formula*."""
    found: set[str] = set()

    def term_vars(term: Term) -> None:
        if isinstance(term, Var):
            found.add(term.name)
        elif isinstance(term, Func):
            for a in term.args:
                term_vars(a)

    def walk_formula(node: Formula) -> None:
        if isinstance(node, Pred):
            for a in node.args:
                term_vars(a)
        elif isinstance(node, NotF):
            walk_formula(node.arg)
        elif isinstance(node, (AndF, OrF, ImpliesF)):
            walk_formula(node.left)
            walk_formula(node.right)
        elif isinstance(node, (Forall, Exists)):
            found.add(node.var.name)
            walk_formula(node.body)

    walk_formula(formula)
    return found


def _conjuncts(formula: Formula) -> list[Formula]:
    if isinstance(formula, AndF):
        return _conjuncts(formula.left) + _conjuncts(formula.right)
    return [formula]


def and_all(parts: list[Formula]) -> Formula:
    """Right-associated conjunction of one or more formulas."""
    if not parts:
        raise ValueError("empty conjunction")
    result = parts[-1]
    for part in reversed(parts[:-1]):
        result = AndF(part, result)
    return result


def _strip_forall(formula: Formula) -> tuple[Formula, list[Var]]:
    variables: list[Var] = []
    while isinstance(formula, Forall):
        variables.append(formula.var)
        formula = formula.body
    return formula, variables


@dataclass
class Rule:
    """A definite clause: conjunction of positive atoms implies one atom."""

    body: list[Pred]
    head: Pred
    label: str = ""

    def __str__(self) -> str:
        body = " ∧ ".join(map(str, self.body))
        return f"{body} → {self.head}" if body else str(self.head)


def as_rule(formula: Formula, label: str = "") -> Rule:
    """Turn ∀x (P ∧ Q → R) into a Rule; raise for non-definite clauses."""
    body_formula, _variables = _strip_forall(formula)
    if not isinstance(body_formula, ImpliesF):
        raise ValueError(f"not an implication: {formula}")
    head = body_formula.right
    if not isinstance(head, Pred):
        raise ValueError(f"head is not an atom: {head}")
    parts = _conjuncts(body_formula.left)
    if not all(isinstance(p, Pred) for p in parts):
        raise ValueError("body must be a conjunction of atoms")
    return Rule([p for p in parts if isinstance(p, Pred)], head, label)  # type: ignore[arg-type]


def _fresh(rule: Rule, tag: int) -> Rule:
    """Rename a rule's variables so joins do not collide."""
    renamed = _standardize(ImpliesF(and_all(list(rule.body)), rule.head), tag=str(tag))
    return as_rule(renamed, rule.label)


def forward_chain(rules: Iterable[Rule], facts: Iterable[Pred],
                  max_iterations: int = 50) -> tuple[set[Pred], list[str]]:
    """Derive every atom entailed by the definite-clause KB, with a derivation log."""
    known: set[Pred] = set(facts)
    rules = list(rules)
    log: list[str] = [f"seed facts: {len(known)}"]
    for iteration in range(1, max_iterations + 1):
        added: set[Pred] = set()
        derived_by: dict[Pred, str] = {}
        for index, rule in enumerate(rules):
            fresh = _fresh(rule, index + 1000 * iteration)
            for subst in _match_body(fresh.body, known):
                conclusion = substitute_formula(fresh.head, subst)
                if isinstance(conclusion, Pred) and conclusion not in known:
                    added.add(conclusion)
                    derived_by[conclusion] = rule.label or str(rule)
        for conclusion in sorted(added, key=str):
            log.append(f"iter {iteration}: {plain(str(conclusion))} "
                       f"from rule '{derived_by[conclusion]}'")
        if not added:
            log.append(f"fixpoint after {iteration} iteration(s)")
            return known, log
        known |= added
    log.append(f"iteration limit {max_iterations} reached")
    return known, log


def _match_body(body: list[Pred], known: set[Pred]) -> Iterator[Substitution]:
    """All substitutions making every atom in *body* true in *known*."""
    if not body:
        yield {}
        return
    first, rest = body[0], body[1:]
    for fact in known:
        subst = unify_atoms(first, fact)
        if subst is None:
            continue
        remaining = [substitute_formula(atom, subst) for atom in rest]
        for deeper in _match_body(remaining, known):  # type: ignore[arg-type]
            yield {**subst, **deeper}


# ---------------------------------------------------------------------------
# 7. Backward chaining
# ---------------------------------------------------------------------------


def backward_chain(rules: Iterable[Rule], facts: Iterable[Pred], goal: Pred,
                   max_depth: int = 12) -> list[Substitution]:
    """SLD resolution: substitutions that make *goal* true, in proof order."""
    rules = list(rules)
    fact_set = list(facts)

    def prove(goal: Pred, subst: Substitution, depth: int) -> Iterator[Substitution]:
        """Yield substitutions extending *subst* that satisfy *goal*."""
        if depth > max_depth:
            return
        target = substitute_formula(goal, subst)
        if not isinstance(target, Pred):
            return
        for fact in fact_set:
            unified = unify_atoms(target, fact)
            if unified is not None:
                yield {**subst, **unified}
        for index, rule in enumerate(rules):
            fresh = _fresh(rule, index + 10 * depth)
            matched = unify_atoms(target, fresh.head)
            if matched is None:
                continue
            goals = [substitute_formula(atom, matched) for atom in fresh.body]
            yield from prove_all(goals, {**subst, **matched}, depth + 1)

    def prove_all(goals: list[Pred], subst: Substitution,
                  depth: int) -> Iterator[Substitution]:
        if not goals:
            yield subst
            return
        first, rest = goals[0], goals[1:]
        for extended in prove(first, subst, depth):
            remaining = [substitute_formula(atom, extended) for atom in rest]
            yield from prove_all(remaining, extended, depth)  # type: ignore[arg-type]

    asked = variables_in(goal)
    found: list[Substitution] = []
    seen: set[tuple] = set()
    for solution in prove(goal, {}, 0):
        answer = {name: substitute(Var(name), solution) for name in asked if name in solution}
        key = tuple(sorted((k, str(v)) for k, v in answer.items()))
        if key not in seen:
            seen.add(key)
            found.append(answer)
    return found


# ---------------------------------------------------------------------------
# 8. Demonstration
# ---------------------------------------------------------------------------


def demo() -> None:
    x, y = Var("x"), Var("y")
    socrates = Const("socrates")

    human = lambda t: pred("human", t)          # noqa: E731
    mortal = lambda t: pred("mortal", t)        # noqa: E731

    kb = [Forall(x, ImpliesF(human(x), mortal(x))), human(socrates)]

    print("== unification ==")
    print("unify human(x), human(socrates):", unify_atoms(human(x), human(socrates)))
    print("unify f(x, b), f(a, y):",
          unify(func("f", x, Const("b")), func("f", Const("a"), y)))
    print("unify f(x, x), f(a, b):",
          unify(func("f", x, x), func("f", Const("a"), Const("b"))))

    print("\n== resolution ==")
    proved, trace = fol_resolution(kb, mortal(socrates))
    print("proved mortal(socrates):", proved)
    for line in trace[-6:]:
        print("  ", line)

    print("\n== forward chaining ==")
    rules = [as_rule(Forall(x, ImpliesF(human(x), mortal(x))), "all humans are mortal")]
    facts = [human(socrates), human(Const("plato"))]
    derived, log = forward_chain(rules, facts)
    print("derived:", sorted(plain(str(f)) for f in derived))
    for line in log:
        print("  ", line)

    print("\n== backward chaining ==")
    parent = lambda a, b: pred("parent", a, b)      # noqa: E731
    ancestor = lambda a, b: pred("ancestor", a, b)  # noqa: E731
    family_rules = [
        as_rule(Forall([x, y][0], Forall(y, ImpliesF(parent(x, y), ancestor(x, y)))),
                "parent implies ancestor"),
        as_rule(Forall(x, Forall(y, Forall(Var("z"),
                    ImpliesF(AndF(parent(x, y), ancestor(y, Var("z"))),
                             ancestor(x, Var("z")))))), "ancestor is transitive"),
    ]
    family_facts = [parent(Const("ann"), Const("bob")), parent(Const("bob"), Const("cid"))]
    answers = backward_chain(family_rules, family_facts, ancestor(Var("who"), Const("cid")))
    print("who is an ancestor of cid?",
          sorted({plain(str(s["who"])) for s in answers if "who" in s}))

    print("\n== clause form ==")
    for clause in to_clauses(Forall(x, ImpliesF(human(x), mortal(x))), tag="1"):
        print("  ", plain(str(clause)))


if __name__ == "__main__":
    demo()
