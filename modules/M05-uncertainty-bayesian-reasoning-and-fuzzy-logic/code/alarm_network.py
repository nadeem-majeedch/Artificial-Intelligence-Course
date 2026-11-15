"""Alarm Bayesian network: full conditional probability tables and exact inference.

The classic Pearl/Russell-Norvig alarm network:

    Burglary  Earthquake
         \\      /
          Alarm
         /     \\
   JohnCalls  MaryCalls

Factorisation: P(B,E,A,J,M) = P(B) P(E) P(A|B,E) P(J|A) P(M|A)

Every table in this file stores *both* values of the child variable. The defect this
file repairs was a table that stored only P(A=True | b, e) and then used that same
number for the a=False branch, which left the joint distribution unnormalised.
"""

from itertools import product

NODES = ("B", "E", "A", "J", "M")

# P(B)
P_BURGLARY = {True: 0.001, False: 0.999}

# P(E) -- burglary and earthquake are independent: neither is an ancestor of the other.
P_EARTHQUAKE = {True: 0.002, False: 0.998}

# P(A=True | B, E). The complement is P(A=False | B, E); p_alarm() applies it.
P_ALARM_TRUE = {
    (True, True): 0.95,
    (True, False): 0.94,
    (False, True): 0.29,
    (False, False): 0.001,
}

# P(J | A) and P(M | A): the two callers are independent given the alarm.
P_JOHN_CALLS = {True: 0.90, False: 0.05}
P_MARY_CALLS = {True: 0.70, False: 0.01}


def p_alarm(a, b, e):
    """P(A=a | B=b, E=e) for both values of a."""
    p_true = P_ALARM_TRUE[(b, e)]
    return p_true if a else 1.0 - p_true


def joint(b, e, a, j, m):
    """One entry of the full joint distribution, by the network factorisation."""
    return (
        P_BURGLARY[b]
        * P_EARTHQUAKE[e]
        * p_alarm(a, b, e)
        * (P_JOHN_CALLS[a] if j else 1.0 - P_JOHN_CALLS[a])
        * (P_MARY_CALLS[a] if m else 1.0 - P_MARY_CALLS[a])
    )


def joint_table():
    """The 32 joint entries, keyed by (b, e, a, j, m)."""
    return {
        (b, e, a, j, m): joint(b, e, a, j, m)
        for b, e, a, j, m in product([True, False], repeat=5)
    }


def validate_evidence(evidence):
    """Return evidence as a validated dict; raise ValueError on anything else."""
    if not isinstance(evidence, dict):
        raise TypeError("evidence must be a dict of node -> bool")
    for node, value in evidence.items():
        if node not in NODES:
            raise ValueError(f"unknown node {node!r}; expected one of {NODES}")
        if not isinstance(value, bool):
            raise ValueError(f"evidence for {node!r} must be True or False, got {value!r}")
    return dict(evidence)


def enumerate_posterior(query_node, evidence=None, table=None):
    """P(query_node=True | evidence) by summing the joint over hidden variables.

    Returns (posterior, p_evidence). Raises ValueError for invalid evidence or a
    query node that is not in the network (or is in the evidence).
    """
    evidence = validate_evidence(evidence or {})
    if query_node not in NODES:
        raise ValueError(f"unknown query node {query_node!r}")
    if query_node in evidence:
        raise ValueError("the query node is part of the evidence; the answer is trivial")
    table = table if table is not None else joint_table()
    idx = {name: i for i, name in enumerate(NODES)}

    def matches(key, fixed):
        return all(key[idx[name]] == value for name, value in fixed.items())

    p_evidence = sum(v for k, v in table.items() if matches(k, evidence))
    if p_evidence == 0.0:
        raise ValueError("evidence has zero probability")
    p_query_and_evidence = sum(
        v for k, v in table.items()
        if matches(k, evidence) and k[idx[query_node]] is True
    )
    return p_query_and_evidence / p_evidence, p_evidence


EVIDENCE_CASES = [
    ("no evidence", {}),
    ("John calls", {"J": True}),
    ("Mary calls", {"M": True}),
    ("both call", {"J": True, "M": True}),
    ("John only", {"J": True, "M": False}),
    ("Mary only", {"J": False, "M": True}),
    ("neither calls", {"J": False, "M": False}),
    ("earthquake", {"E": True}),
    ("earthquake, both call", {"E": True, "J": True, "M": True}),
]


def evidence_table():
    """Measured posteriors used in the lesson and notebook."""
    rows = []
    for label, ev in EVIDENCE_CASES:
        posterior, p_ev = enumerate_posterior("B", ev)
        rows.append((label, ev, posterior, p_ev))
    return rows


def run_tests():
    """Self-checks: normalisation, evidence handling, posteriors, invalid input."""
    table = joint_table()

    # 1. The joint distribution must sum to 1.
    assert abs(sum(table.values()) - 1.0) < 1e-12, sum(table.values())
    assert len(table) == 32

    # 2. Marginals must match the priors.
    assert abs(sum(v for k, v in table.items() if k[0]) - 0.001) < 1e-12
    assert abs(sum(v for k, v in table.items() if k[1]) - 0.002) < 1e-12
    # B and E are independent, and the alarm children are independent given A.
    p_b = sum(v for k, v in table.items() if k[0])
    p_e = sum(v for k, v in table.items() if k[1])
    p_b_and_e = sum(v for k, v in table.items() if k[0] and k[1])
    assert abs(p_b_and_e - p_b * p_e) < 1e-15

    # 3. Published reference values (Russell & Norvig, AIMA ch. 14).
    assert abs(enumerate_posterior("B", {})[0] - 0.001) < 1e-12
    assert abs(enumerate_posterior("B", {"J": True, "M": True})[0] - 0.2841718) < 1e-6
    assert abs(enumerate_posterior("B", {"E": True})[0] - 0.001) < 1e-12
    # P(A) computed from the tables by hand: 0.002516442
    p_a = enumerate_posterior("A", {})[0]
    assert abs(p_a - 0.002516442) < 1e-9, p_a
    # Bayes check against the hand value P(A|J) = P(J|A)P(A)/P(J)
    p_j = enumerate_posterior("J", {})[0]
    p_a_given_j = enumerate_posterior("A", {"J": True})[0]
    assert abs(p_a_given_j - 0.90 * p_a / p_j) < 1e-12

    # 4. Evidence must change the posterior in the expected direction.
    p_none = enumerate_posterior("B", {})[0]
    p_j = enumerate_posterior("B", {"J": True})[0]
    p_m = enumerate_posterior("B", {"M": True})[0]
    p_jm = enumerate_posterior("B", {"J": True, "M": True})[0]
    assert p_none < p_j < p_jm and p_none < p_m < p_jm

    # 5. Explaining away: earthquake evidence defeats the callers' evidence.
    p_ejm = enumerate_posterior("B", {"E": True, "J": True, "M": True})[0]
    assert p_ejm < p_jm, (p_ejm, p_jm)

    # 6. Evidence must be handled symmetrically: P(B|J,M) is P(B|M,J).
    assert enumerate_posterior("B", {"J": True, "M": True}) == enumerate_posterior("B", {"M": True, "J": True})

    # 7. Invalid evidence must raise, not silently coerce.
    for bad in ({"X": True}, {"J": 1}, {"J": "yes"}):
        try:
            enumerate_posterior("B", bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid evidence accepted: {bad}")
    # 8. Querying a node that is evidence is a usage error.
    try:
        enumerate_posterior("B", {"B": True})
    except ValueError:
        pass
    else:
        raise AssertionError("query node in evidence was accepted")

    return True


if __name__ == "__main__":
    print(f"{'evidence':24s} {'P(B|e)':>8s} {'P(e)':>10s}")
    for label, ev, posterior, p_ev in evidence_table():
        print(f"{label:24s} {posterior:8.4f} {p_ev:10.7f}")
    print("joint total:", round(sum(joint_table().values()), 12))
    print("tests passed:", run_tests())
