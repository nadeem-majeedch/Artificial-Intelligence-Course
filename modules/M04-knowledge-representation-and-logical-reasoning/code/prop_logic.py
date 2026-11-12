"""Propositional logic: syntax, semantics, normal forms, resolution.

Standard library only. Every public function is exercised in
``demo()`` at the bottom of the file, so ``python prop_logic.py`` is a
self-check as well as a demonstration.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator

_ASCII = {
    "∧": "and", "∨": "or", "¬": "not ", "→": "->", "↔": "<->",
    "□": "empty clause", "⊨": "entails", "⊢": "proves",
}


def plain(text: str) -> str:
    """ASCII-safe spelling, for consoles that cannot print logic symbols."""
    for fancy, simple in _ASCII.items():
        text = text.replace(fancy, simple)
    return text


# ---------------------------------------------------------------------------
# 1. Syntax
# ---------------------------------------------------------------------------


class Formula:
    """Base class for propositional formulas."""

    def __and__(self, other: "Formula") -> "Formula":
        return And(self, other)

    def __or__(self, other: "Formula") -> "Formula":
        return Or(self, other)

    def __invert__(self) -> "Formula":
        return Not(self)

    def __rshift__(self, other: "Formula") -> "Formula":
        return Implies(self, other)


@dataclass(frozen=True)
class Symbol(Formula):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Not(Formula):
    arg: Formula

    def __str__(self) -> str:
        inner = self.arg
        if isinstance(inner, (And, Or, Implies, Iff)):
            return f"¬({inner})"
        return f"¬{inner}"


@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"


@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"


@dataclass(frozen=True)
class Implies(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} → {self.right})"


@dataclass(frozen=True)
class Iff(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} ↔ {self.right})"


def iff(left: Formula, right: Formula) -> Iff:
    """Explicit biconditional.

    Use this rather than ``==``: dataclass equality compares two formulas
    structurally and returns a bool, which is not a formula.
    """
    return Iff(left, right)


def symbols(formula: Formula) -> list[str]:
    """Return the proposition symbols of *formula*, sorted alphabetically."""
    seen: set[str] = set()

    def walk(node: Formula) -> None:
        if isinstance(node, Symbol):
            seen.add(node.name)
        elif isinstance(node, Not):
            walk(node.arg)
        elif isinstance(node, (And, Or, Implies, Iff)):
            walk(node.left)
            walk(node.right)

    walk(formula)
    return sorted(seen)


# ---------------------------------------------------------------------------
# 2. Semantics: truth tables and entailment by model enumeration
# ---------------------------------------------------------------------------


def evaluate(formula: Formula, assignment: dict[str, bool]) -> bool:
    """Truth value of *formula* under *assignment*."""
    if isinstance(formula, Symbol):
        return assignment[formula.name]
    if isinstance(formula, Not):
        return not evaluate(formula.arg, assignment)
    if isinstance(formula, And):
        return evaluate(formula.left, assignment) and evaluate(formula.right, assignment)
    if isinstance(formula, Or):
        return evaluate(formula.left, assignment) or evaluate(formula.right, assignment)
    if isinstance(formula, Implies):
        return (not evaluate(formula.left, assignment)) or evaluate(formula.right, assignment)
    if isinstance(formula, Iff):
        return evaluate(formula.left, assignment) == evaluate(formula.right, assignment)
    raise TypeError(f"not a formula: {formula!r}")


def all_assignments(names: Iterable[str]) -> Iterator[dict[str, bool]]:
    """Every row of a truth table over *names*."""
    names = list(names)
    for values in product([False, True], repeat=len(names)):
        yield dict(zip(names, values))


def truth_table(formula: Formula) -> tuple[list[str], list[list[bool]]]:
    """Header and rows (inputs then output) for *formula*."""
    names = symbols(formula)
    rows = [[assignment[n] for n in names] + [evaluate(formula, assignment)]
            for assignment in all_assignments(names)]
    return names + [str(formula)], rows


def satisfies(formula: Formula, assignment: dict[str, bool]) -> bool:
    return evaluate(formula, assignment)


def is_valid(formula: Formula) -> bool:
    """True when *formula* is true in every model (a tautology)."""
    return all(evaluate(formula, a) for a in all_assignments(symbols(formula)))


def is_satisfiable(formula: Formula) -> bool:
    return any(evaluate(formula, a) for a in all_assignments(symbols(formula)))


def entails(kb: Iterable[Formula], query: Formula) -> bool:
    """Model checking: KB ⊨ query iff every model of KB is a model of query."""
    kb = list(kb)
    names = sorted({n for f in kb + [query] for n in symbols(f)})
    for assignment in all_assignments(names):
        if all(evaluate(f, assignment) for f in kb) and not evaluate(query, assignment):
            return False
    return True


def counterexample(kb: Iterable[Formula], query: Formula) -> dict[str, bool] | None:
    """A model of the KB that falsifies *query*, or None if there is none."""
    kb = list(kb)
    names = sorted({n for f in kb + [query] for n in symbols(f)})
    for assignment in all_assignments(names):
        if all(evaluate(f, assignment) for f in kb) and not evaluate(query, assignment):
            return assignment
    return None


# ---------------------------------------------------------------------------
# 3. Normal forms
# ---------------------------------------------------------------------------


def to_nnf(formula: Formula) -> Formula:
    """Push negations inward until they sit on symbols only."""
    if isinstance(formula, Symbol):
        return formula
    if isinstance(formula, Not):
        inner = formula.arg
        if isinstance(inner, Symbol):
            return formula
        if isinstance(inner, Not):
            return to_nnf(inner.arg)
        if isinstance(inner, And):
            return Or(to_nnf(Not(inner.left)), to_nnf(Not(inner.right)))
        if isinstance(inner, Or):
            return And(to_nnf(Not(inner.left)), to_nnf(Not(inner.right)))
        if isinstance(inner, Implies):           # ¬(a → b) ≡ a ∧ ¬b
            return And(to_nnf(inner.left), to_nnf(Not(inner.right)))
        if isinstance(inner, Iff):
            left = And(to_nnf(inner.left), to_nnf(Not(inner.right)))
            right = And(to_nnf(Not(inner.left)), to_nnf(inner.right))
            return Or(left, right)
        raise TypeError(inner)
    if isinstance(formula, Implies):
        return Or(to_nnf(Not(formula.left)), to_nnf(formula.right))
    if isinstance(formula, Iff):
        left = And(to_nnf(formula.left), to_nnf(formula.right))
        right = And(to_nnf(Not(formula.left)), to_nnf(Not(formula.right)))
        return Or(left, right)
    if isinstance(formula, And):
        return And(to_nnf(formula.left), to_nnf(formula.right))
    if isinstance(formula, Or):
        return Or(to_nnf(formula.left), to_nnf(formula.right))
    raise TypeError(formula)


def to_cnf(formula: Formula) -> Formula:
    """Conjunctive normal form: a conjunction of clauses (each a disjunction)."""
    nnf = to_nnf(formula)
    distributed = _distribute(nnf)
    return _flatten_and(distributed)


def _distribute(formula: Formula) -> Formula:
    if isinstance(formula, (Symbol, Not)):
        return formula
    if isinstance(formula, And):
        return And(_distribute(formula.left), _distribute(formula.right))
    if isinstance(formula, Or):
        left, right = _distribute(formula.left), _distribute(formula.right)
        if isinstance(left, And):
            return And(_distribute(Or(left.left, right)), _distribute(Or(left.right, right)))
        if isinstance(right, And):
            return And(_distribute(Or(left, right.left)), _distribute(Or(left, right.right)))
        return Or(left, right)
    raise TypeError(formula)


def _flatten_and(formula: Formula) -> Formula:
    result = formula
    while isinstance(result, And) and isinstance(result.left, And):
        result = And(result.left.left, And(result.left.right, result.right))
    return result


def clauses(formula: Formula) -> list[frozenset[tuple[str, bool]]]:
    """CNF as a list of clauses; a clause is a set of (symbol, positive?) literals."""

    def collect(node: Formula, out: list[frozenset[tuple[str, bool]]]) -> None:
        if isinstance(node, And):
            collect(node.left, out)
            collect(node.right, out)
        else:
            out.append(_clause(node, set()))

    cnf = to_cnf(formula)
    out: list[frozenset[tuple[str, bool]]] = []
    collect(cnf, out)
    return out


def _clause(node: Formula, acc: set[tuple[str, bool]]) -> frozenset[tuple[str, bool]]:
    if isinstance(node, Or):
        _clause(node.left, acc)
        _clause(node.right, acc)
    elif isinstance(node, Symbol):
        acc.add((node.name, True))
    elif isinstance(node, Not) and isinstance(node.arg, Symbol):
        acc.add((node.arg.name, False))
    else:  # pragma: no cover - guarded by to_cnf
        raise TypeError(f"clause is not a disjunction of literals: {node}")
    return frozenset(acc)


def clause_str(clause: Iterable[tuple[str, bool]]) -> str:
    parts = [name if positive else f"¬{name}" for name, positive in sorted(clause)]
    return " ∨ ".join(parts) if parts else "□"      # □ is the empty clause


# ---------------------------------------------------------------------------
# 4. Propositional resolution
# ---------------------------------------------------------------------------


def resolve(ci: frozenset[tuple[str, bool]],
            cj: frozenset[tuple[str, bool]]) -> set[frozenset[tuple[str, bool]]]:
    """All resolvents of two clauses (one per complementary literal pair)."""
    resolvents: set[frozenset[tuple[str, bool]]] = set()
    for name, positive in ci:
        if (name, not positive) in cj:
            merged = (ci - {(name, positive)}) | (cj - {(name, not positive)})
            resolvents.add(frozenset(merged))
    return resolvents


def resolution_refutation(kb: Iterable[Formula], query: Formula,
                          max_steps: int = 200) -> tuple[bool, list[str]]:
    """Prove KB ⊨ query by refutation. Returns (proved, trace)."""
    working: list[frozenset[tuple[str, bool]]] = []
    for formula in list(kb) + [Not(query)]:
        working.extend(clauses(formula))

    trace = [f"start: {len(working)} clauses"]
    seen = {c for c in working}
    steps = 0
    while steps < max_steps:
        steps += 1
        new: list[frozenset[tuple[str, bool]]] = []
        for i, ci in enumerate(working):
            for cj in working[i + 1:]:
                for resolvent in resolve(ci, cj):
                    if not resolvent:
                        trace.append(f"resolve {clause_str(ci)} with {clause_str(cj)} -> □")
                        return True, trace
                    if resolvent not in seen:
                        seen.add(resolvent)
                        new.append(resolvent)
                        trace.append(
                            f"resolve {clause_str(ci)} with {clause_str(cj)} "
                            f"-> {clause_str(resolvent)}"
                        )
        if not new:
            trace.append("no new clauses: no refutation exists")
            return False, trace
        working.extend(new)
    trace.append(f"step limit {max_steps} reached")
    return False, trace


# ---------------------------------------------------------------------------
# 5. Demonstration
# ---------------------------------------------------------------------------


def demo() -> None:
    rain, wet, indoors = Symbol("rain"), Symbol("wet"), Symbol("indoors")
    kb = [rain >> wet, wet >> ~indoors, rain]

    print("== truth table for rain -> wet ==")
    header, rows = truth_table(rain >> wet)
    print(" | ".join(plain(h) for h in header))
    for row in rows:
        print(" | ".join("T" if v else "F" for v in row))

    print("\n== entailment ==")
    print("KB entails not indoors?", entails(kb, Not(indoors)))
    print("KB entails wet?", entails(kb, wet))
    print("KB entails indoors?", entails(kb, indoors))
    print("counterexample for indoors:", counterexample(kb, indoors))

    print("\n== CNF ==")
    print("cnf of (rain -> wet) -> indoors:", plain(str(to_cnf((rain >> wet) >> indoors))))
    print("clauses:", [plain(clause_str(c)) for c in clauses((rain >> wet) >> indoors)])

    print("\n== resolution ==")
    proved, trace = resolution_refutation(kb, Not(indoors))
    print("proved not indoors:", proved)
    for line in trace:
        print("  ", plain(line))

    print("\n== resolution cannot prove a non-entailment ==")
    proved, _ = resolution_refutation(kb, indoors)
    print("proved indoors:", proved)


if __name__ == "__main__":
    demo()
