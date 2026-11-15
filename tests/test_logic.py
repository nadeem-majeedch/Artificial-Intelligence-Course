"""Tests for M04 logic: propositional model checking, unification, resolution, rules."""

import itertools

import pytest

import expert_system as es
import fol_core as fol
import prop_logic as pl


def truth_table(formula, names):
    rows = {}
    for values in itertools.product([False, True], repeat=len(names)):
        assignment = dict(zip(names, values))
        rows[values] = pl.evaluate(formula, assignment)
    return rows


def test_implication_matches_not_p_or_q():
    formula = pl.Implies(pl.Symbol("P"), pl.Symbol("Q"))
    rows = truth_table(formula, ["P", "Q"])
    for (p, q), value in rows.items():
        assert value is ((not p) or q)


def test_conjunction_and_disjunction_truth_tables():
    p, q = pl.Symbol("P"), pl.Symbol("Q")
    for (pv, qv), value in truth_table(pl.And(p, q), ["P", "Q"]).items():
        assert value is (pv and qv)
    for (pv, qv), value in truth_table(pl.Or(p, q), ["P", "Q"]).items():
        assert value is (pv or qv)


def test_entailment_modus_ponens_and_its_converse():
    p, q = pl.Symbol("P"), pl.Symbol("Q")
    assert pl.entails([pl.Implies(p, q), p], q)
    assert not pl.entails([pl.Implies(p, q)], q)
    assert pl.entails([pl.Implies(p, q), pl.Not(q)], pl.Not(p))


def test_satisfiability_matches_brute_force():
    p, q = pl.Symbol("P"), pl.Symbol("Q")
    contradiction = pl.And(p, pl.Not(p))
    assert not pl.is_satisfiable(contradiction)
    assert pl.is_satisfiable(pl.Or(p, q))
    assert pl.counterexample([pl.Implies(p, q)], q) is not None


def test_unification_builds_the_most_general_unifier():
    a, b = fol.Const("a"), fol.Const("b")
    subst = fol.unify_atoms(fol.pred("p", fol.Var("X"), b), fol.pred("p", a, fol.Var("Y")))
    assert subst is not None
    assert subst["X"] == a and subst["Y"] == b
    # applying the substitution makes the atoms identical
    left = fol.substitute_formula(fol.pred("p", fol.Var("X"), b), subst)
    right = fol.substitute_formula(fol.pred("p", a, fol.Var("Y")), subst)
    assert str(left) == str(right)


def test_unification_rejects_clashes_and_occurrences():
    X = fol.Var("x")
    assert fol.unify_atoms(fol.pred("p", fol.Const("a")), fol.pred("p", fol.Const("b"))) is None
    assert fol.unify(X, fol.func("f", X)) is None
    assert fol.occurs(X, fol.func("f", X)) is True


def test_resolution_proves_a_valid_entailment():
    x = fol.Var("x")
    kb = [fol.Forall(x, fol.ImpliesF(fol.pred("human", x), fol.pred("mortal", x))),
          fol.pred("human", fol.Const("socrates"))]
    proved, _trace = fol.fol_resolution(kb, fol.pred("mortal", fol.Const("socrates")))
    assert proved is True


def test_resolution_does_not_prove_a_non_entailment():
    x = fol.Var("x")
    kb = [fol.Forall(x, fol.ImpliesF(fol.pred("human", x), fol.pred("mortal", x))),
          fol.pred("human", fol.Const("socrates"))]
    proved, _trace = fol.fol_resolution(kb, fol.pred("mortal", fol.Const("plato")))
    assert proved is False


def derived_facts(kb):
    return {str(step) for step in kb.forward_chain()}


def test_forward_chaining_derives_transitive_facts():
    kb = es.family_kb()
    derived = derived_facts(kb)
    assert any("ancestor" in step for step in derived)
    assert any("sibling" in step or "uncle_or_aunt" in step for step in derived)


def test_backward_chaining_builds_a_proof_for_a_ground_goal():
    kb = es.family_kb()
    proof = kb.backward_chain(("ancestor", "ali", "sara"))
    assert proof is not None
    assert proof["children"][0]["kind"] == "fact"
    # a goal with no supporting facts fails rather than inventing one
    assert kb.backward_chain(("ancestor", "sara", "ali")) is None


def test_advisor_derives_honours_admission_and_explains_it():
    kb = es.advising_kb()
    kb.add_fact("gpa", "high")
    kb.add_fact("english", "passed")
    derived = derived_facts(kb)
    assert any("honours_programme" in step for step in derived)
    assert any("scholarship" in step for step in derived)
    assert kb.explain(("admit", "honours_programme"))


def test_rule_engine_does_not_fire_without_its_premises():
    kb = es.advising_kb()
    kb.add_fact("gpa", "high")          # language requirement not met
    derived = derived_facts(kb)
    assert any("honours" in step for step in derived)
    assert not any("honours_programme" in step for step in derived)
