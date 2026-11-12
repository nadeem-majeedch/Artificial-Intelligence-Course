"""Four worked knowledge bases for M04, all built on ``fol_core``.

* ``FAMILY``         — a small genealogy, used for relations and unification.
* ``ADVISING``       — course prerequisites, generated as Horn clauses.
* ``TROUBLESHOOTING``— a printer fault KB, used for forward chaining.
* ``MEDICAL``        — a **synthetic** symptom KB for teaching only.

The medical KB is fabricated for coursework. It is not clinically
validated, must not be used for diagnosis, and its "diseases" are
pattern names, not conditions. The disclaimer is printed by ``demo()``
so that anyone running the file sees it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from fol_core import (
    AndF, Const, Forall, ImpliesF, Pred, Rule, Var, as_rule, backward_chain,
    forward_chain, plain, pred,
)

x, y, z = Var("x"), Var("y"), Var("z")


def as_term(value) -> object:
    """A string becomes a constant; a term is passed through unchanged."""
    return Const(value) if isinstance(value, str) else value


# ---------------------------------------------------------------------------
# 1. Family relations
# ---------------------------------------------------------------------------

ANN, BOB, CID, DAN, EVE, FINN = map(Const, ["ann", "bob", "cid", "dan", "eve", "finn"])


def parent(a, b) -> Pred:
    return pred("parent", a, b)


def ancestor(a, b) -> Pred:
    return pred("ancestor", a, b)


def sibling(a, b) -> Pred:
    return pred("sibling", a, b)


def different(a, b) -> Pred:
    return pred("different", as_term(a), as_term(b))


FAMILY_FACTS = [
    parent(ANN, BOB), parent(ANN, CID),      # ann is a parent of bob and cid
    parent(BOB, DAN), parent(BOB, EVE),      # bob is a parent of dan and eve
    parent(CID, FINN),
]

PEOPLE = [ANN, BOB, CID, DAN, EVE, FINN]

# First-order logic would write x != y inside the sibling rule. Definite
# clauses have no inequality, so the pairs are listed as facts. This is a
# standard, if inelegant, way to keep Horn clauses expressive enough.
FAMILY_FACTS += [different(a, b) for a in PEOPLE for b in PEOPLE if a != b]

FAMILY_RULES = [
    as_rule(Forall(x, Forall(y, ImpliesF(parent(x, y), ancestor(x, y)))),
            "a parent is an ancestor"),
    as_rule(Forall(x, Forall(y, Forall(z,
                ImpliesF(AndF(parent(x, y), ancestor(y, z)), ancestor(x, z))))),
            "an ancestor of a child is an ancestor"),
    as_rule(Forall(x, Forall(y, Forall(z,
                ImpliesF(AndF(AndF(parent(z, x), parent(z, y)), different(x, y)),
                         sibling(x, y))))),
            "children of a common parent are siblings"),
]


# ---------------------------------------------------------------------------
# 2. Academic advising
# ---------------------------------------------------------------------------

COURSES = {
    "cs101": [],
    "ma101": [],
    "cs201": ["cs101", "ma101"],
    "cs301": ["cs201"],
    "ds201": ["cs101", "ma101"],
    "cap400": ["cs301", "ds201"],
}

PASSED = {
    "ali": {"cs101", "ma101"},
    "bea": {"cs101", "ma101", "cs201"},
    "chen": {"cs101", "ma101", "cs201", "ds201"},
}


def _course_const(name: str) -> Const:
    return Const(name)


ADVISING_FACTS: list[Pred] = [
    pred("passed", Const(student), _course_const(course))
    for student, courses in PASSED.items()
    for course in sorted(courses)
]

ADVISING_RULES: list[Rule] = []
for course, prerequisites in COURSES.items():
    if not prerequisites:
        continue
    body = [pred("passed", x, _course_const(name)) for name in prerequisites]
    head = pred("eligible", x, _course_const(course))
    body_formula: object = body[0]
    for atom in body[1:]:
        body_formula = AndF(body_formula, atom)  # type: ignore[arg-type]
    ADVISING_RULES.append(as_rule(Forall(x, ImpliesF(body_formula, head)),  # type: ignore[arg-type]
                                  f"prerequisites of {course}"))


def missing_prerequisites(student: str, course: str) -> list[str]:
    """Prerequisites the student has not passed.

    Definite clauses cannot say "not passed", so absence is checked here.
    This is the closed-world assumption in procedural form.
    """
    return [p for p in COURSES[course] if p not in PASSED.get(student, set())]


# ---------------------------------------------------------------------------
# 3. Printer troubleshooting
# ---------------------------------------------------------------------------


def has(device, symptom) -> Pred:
    """has(device, symptom): both arguments may be terms or plain strings."""
    return pred("has", as_term(device), as_term(symptom))


def action(name) -> Pred:
    return pred("action", as_term(name))


DEVICE = Var("d")


TROUBLESHOOTING_FACTS = [
    has("printer", "no_display"),
    has("printer", "paper_loaded"),
]

TROUBLESHOOTING_RULES = [
    as_rule(Forall(DEVICE, ImpliesF(has(DEVICE, "no_display"), action("check_power_cable"))),
            "no display means check the power cable"),
    as_rule(Forall(DEVICE, ImpliesF(has(DEVICE, "no_display"), action("check_socket"))),
            "no display means check the socket"),
    as_rule(Forall(DEVICE, ImpliesF(
                AndF(has(DEVICE, "paper_jam"), has(DEVICE, "paper_loaded")),
                action("open_rear_panel"))), "jam while paper is loaded"),
    as_rule(Forall(DEVICE, ImpliesF(has(DEVICE, "streaky_print"), action("run_clean_cycle"))),
            "streaks mean run a clean cycle"),
    as_rule(Forall(DEVICE, ImpliesF(has(DEVICE, "blank_page"), action("check_toner"))),
            "blank page means check the toner"),
]


# ---------------------------------------------------------------------------
# 4. Synthetic medical KB (teaching only)
# ---------------------------------------------------------------------------


def symptom(name) -> Pred:
    return pred("symptom", as_term(name))


def hypothesis(name) -> Pred:
    return pred("hypothesis", as_term(name))


MEDICAL_FACTS = [
    symptom("fever"),
    symptom("cough"),
    symptom("fatigue"),
]

MEDICAL_RULES = [
    as_rule(Forall(x, Forall(y, Forall(z, ImpliesF(
                AndF(AndF(symptom(x), symptom(y)), symptom(z)),
                hypothesis("viral_syndrome"))))), "fever + cough + fatigue"),
    as_rule(Forall(x, ImpliesF(symptom(x), hypothesis("needs_assessment"))),
            "any symptom needs assessment"),
    as_rule(Forall(x, Forall(y, ImpliesF(
                AndF(symptom(x), symptom(y)), hypothesis("combined_picture")))),
            "two symptoms form a picture"),
]


@dataclass
class KnowledgeBase:
    """A named set of facts and rules, with its own query helpers."""

    name: str
    facts: list[Pred]
    rules: list[Rule]
    note: str = ""
    derived: set[Pred] = field(default_factory=set)

    def close(self) -> set[Pred]:
        self.derived, _log = forward_chain(self.rules, self.facts)
        return self.derived

    def ask(self, goal: Pred, max_depth: int = 8) -> list[dict]:
        return backward_chain(self.rules, self.facts, goal, max_depth=max_depth)


FAMILY = KnowledgeBase("family", FAMILY_FACTS, FAMILY_RULES, "genealogy")
ADVISING = KnowledgeBase("advising", ADVISING_FACTS, ADVISING_RULES, "course catalogue")
TROUBLESHOOTING = KnowledgeBase("troubleshooting", TROUBLESHOOTING_FACTS,
                               TROUBLESHOOTING_RULES, "printer faults")
MEDICAL = KnowledgeBase("medical-synthetic", MEDICAL_FACTS, MEDICAL_RULES,
                        "SYNTHETIC teaching data - not a diagnostic system")


def demo() -> None:
    print("=" * 66)
    print("MEDICAL KB DISCLAIMER: synthetic teaching data. Not clinically")
    print("validated. Never use for real diagnosis or patient decisions.")
    print("=" * 66)

    print("\n== family: who is an ancestor of dan? ==")
    for solution in FAMILY.ask(ancestor(Var("who"), DAN)):
        print("  ", plain(str(solution["who"])))

    print("\n== family: siblings of cid ==")
    for solution in FAMILY.ask(sibling(CID, Var("who"))):
        print("  ", plain(str(solution["who"])))

    print("\n== family: forward closure size ==")
    print("  atoms in closure (facts + derived):", len(FAMILY.close()))

    print("\n== advising: eligible courses (forward chaining) ==")
    derived = ADVISING.close()
    for atom in sorted((a for a in derived if a.name == "eligible"), key=str):
        print("  ", plain(str(atom)))

    print("\n== advising: what blocks chen from cap400? ==")
    print("  missing:", missing_prerequisites("chen", "cap400"))
    print("  missing for ali in cs201:", missing_prerequisites("ali", "cs201"))
    print("  chen eligible for cap400?", ADVISING.ask(pred("eligible", Const("chen"),
                                                          Const("cap400"))))

    print("\n== troubleshooting: actions for the recorded symptoms ==")
    for atom in sorted((a for a in TROUBLESHOOTING.close() if a.name == "action"), key=str):
        print("  ", plain(str(atom)))

    print("\n== medical (synthetic): triggered hypotheses ==")
    for atom in sorted((a for a in MEDICAL.close() if a.name == "hypothesis"), key=str):
        print("  ", plain(str(atom)))


if __name__ == "__main__":
    demo()
