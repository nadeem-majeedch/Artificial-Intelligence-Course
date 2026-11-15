"""Tests for M05 probability: factors, variable elimination, Bayes consistency."""

import itertools

import numpy as np
import pytest

import alarm_network
import expert_system as es
from variable_elimination import Factor, alarm_factors, variable_elimination


def enumerate_joint(factors, variables):
    joint = {}
    for values in itertools.product([True, False], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        weight = 1.0
        for factor in factors:
            weight *= factor.value(**{v: assignment[v] for v in factor.variables})
        joint[values] = weight
    return joint, variables


def test_factor_product_and_sum_out_match_hand_computation():
    f = Factor(["A"], {(True,): 0.3, (False,): 0.7})
    g = Factor(["A", "B"], {(True, True): 0.9, (True, False): 0.1,
                            (False, True): 0.2, (False, False): 0.8})
    product = f.multiply(g)
    assert product.value(A=True, B=True) == pytest.approx(0.3 * 0.9)
    marginal = product.sum_out("A")
    assert marginal.value(B=True) == pytest.approx(0.3 * 0.9 + 0.7 * 0.2)
    assert marginal.value(B=False) == pytest.approx(0.3 * 0.1 + 0.7 * 0.8)


def test_restrict_conditions_without_losing_mass():
    f = Factor(["A", "B"], {(True, True): 0.4, (True, False): 0.1,
                            (False, True): 0.3, (False, False): 0.2})
    restricted = f.restrict({"A": True})
    assert restricted.variables == ("B",)
    assert restricted.value(B=True) == pytest.approx(0.4)
    assert restricted.value(B=False) == pytest.approx(0.1)


def test_factor_rejects_a_table_with_the_wrong_arity():
    with pytest.raises(ValueError):
        Factor(["A", "B"], {(True,): 0.5})


def test_normalise_rejects_zero_mass():
    with pytest.raises(ValueError):
        Factor(["A"], {(True,): 0.0, (False,): 0.0}).normalize()


def test_variable_elimination_matches_enumeration_for_four_queries():
    factors = alarm_factors()
    variables = []
    for factor in factors:
        for name in factor.variables:
            if name not in variables:
                variables.append(name)
    joint, _ = enumerate_joint(factors, variables)
    assert sum(joint.values()) == pytest.approx(1.0, abs=1e-12)
    cases = [("A", {}), ("B", {"J": True}), ("E", {"A": True, "M": True}),
             ("B", {"J": True, "M": True})]
    for query, evidence in cases:
        observed, _mass = variable_elimination(factors, query, evidence)
        numerator = denominator = 0.0
        for values, weight in joint.items():
            assignment = dict(zip(variables, values))
            if all(assignment[k] == v for k, v in evidence.items()):
                denominator += weight
                if assignment[query]:
                    numerator += weight
        assert observed == pytest.approx(numerator / denominator, abs=1e-10)


def test_variable_elimination_rejects_bad_evidence():
    factors = alarm_factors()
    with pytest.raises(ValueError):
        variable_elimination(factors, "A", {"Nope": True})
    with pytest.raises(ValueError):
        variable_elimination(factors, "A", {"B": 1})    # not a bool
    with pytest.raises(ValueError):
        variable_elimination(factors, "A", {"A": True})  # query in evidence


def test_alarm_network_numbers_are_the_textbook_ones():
    assert alarm_network.P_BURGLARY[True] == pytest.approx(0.001)
    assert alarm_network.P_EARTHQUAKE[True] == pytest.approx(0.002)


def test_alarm_joint_table_is_a_normalised_distribution():
    table = alarm_network.joint_table()
    assert len(table) == 32
    assert sum(table.values()) == pytest.approx(1.0, abs=1e-12)


def test_alarm_posterior_rises_with_independent_calls():
    prior, _ = alarm_network.enumerate_posterior("B")
    john_only, _ = alarm_network.enumerate_posterior("B", {"J": True})
    both, _ = alarm_network.enumerate_posterior("B", {"J": True, "M": True})
    assert 0.0 < prior < john_only < both < 1.0
    # explaining away: an earthquake explains the alarm, so it lowers P(Burglary)
    with_quake, _ = alarm_network.enumerate_posterior("B", {"J": True, "M": True, "E": True})
    assert with_quake < both


def test_alarm_evidence_validation_rejects_bad_input():
    with pytest.raises(ValueError):
        alarm_network.validate_evidence({"Intruder": True})
    with pytest.raises(ValueError):
        alarm_network.validate_evidence({"J": 1})
    with pytest.raises(ValueError):
        alarm_network.enumerate_posterior("B", {"B": True})


def test_bayes_posterior_equals_joint_over_evidence():
    net = es.troubleshooting_net()
    nodes = list(net.parents)

    def joint(**fixed):
        rest = [n for n in nodes if n not in fixed]
        total = 0.0
        for values in itertools.product([True, False], repeat=len(rest)):
            full = {**fixed, **dict(zip(rest, values))}
            weight = 1.0
            for node in nodes:
                weight *= net.prob(node, full[node], full)
            total += weight
        return total

    prior = joint(P=True)
    evidence = joint(W=True)
    both = joint(P=True, W=True)
    posterior = es.bayes_posterior(net, "P", {"W": True})
    assert posterior[True] == pytest.approx(both / evidence, abs=1e-12)
    assert posterior[True] + posterior[False] == pytest.approx(1.0)
    assert posterior[True] > prior


def test_posterior_with_zero_probability_evidence_raises():
    net = es.troubleshooting_net()
    net.cpt["W"] = {(True,): 0.0, (False,): 0.0}
    with pytest.raises(ValueError):
        es.bayes_posterior(net, "P", {"W": True})
