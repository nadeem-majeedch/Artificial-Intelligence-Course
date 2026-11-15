"""Generic variable elimination for discrete Bayesian networks.

A factor is a function from a set of variables to a non-negative number. Variable
elimination answers P(query | evidence) by restricting factors to the evidence once,
multiplying factors that share a variable, and summing out hidden variables in a chosen
order. Nothing here is specific to the alarm network: the network is supplied as a list
of factors, and the posterior is computed from them.

Uses NumPy for the dense tables. Intended for teaching: the tables are small, and the
point is that the answer is computed, never hardcoded.
"""

from itertools import product

import numpy as np


class Factor:
    """A discrete factor over an ordered tuple of boolean variables."""

    def __init__(self, variables, table):
        self.variables = tuple(variables)
        self.table = {tuple(k): float(v) for k, v in table.items()}
        for assignment in self.table:
            if len(assignment) != len(self.variables):
                raise ValueError("table keys must match the variable list")
        self._dense = None

    # ---- construction -------------------------------------------------
    @classmethod
    def from_array(cls, variables, values):
        variables = tuple(variables)
        array = np.asarray(values, dtype=float)
        expected = (2,) * len(variables)
        if array.shape != expected:
            if array.size == 2 ** len(variables):
                array = array.reshape(expected)      # accept flat tables in variable order
            else:
                raise ValueError(f"expected shape {expected}, got {array.shape}")
        # Index 0 on every axis means True, matching the (True, False) order used
        # throughout this module. Storing numpy's integer indices directly would make
        # `table[(True, ...)]` resolve to the False slice, because True == 1.
        table = {}
        for idx in np.ndindex(array.shape):
            table[tuple(i == 0 for i in idx)] = array[idx]
        return cls(variables, table)

    def dense(self):
        """Values as an ndarray indexed by the variable order (True first)."""
        if self._dense is None:
            shape = (2,) * len(self.variables)
            array = np.zeros(shape)
            for assignment, value in self.table.items():
                array[tuple(0 if v is True else 1 for v in assignment)] = value
            self._dense = array
        return self._dense

    def __repr__(self):
        return f"Factor({self.variables})"

    def is_zero(self):
        return float(self.dense().sum()) == 0.0

    # ---- operations ---------------------------------------------------
    def restrict(self, evidence):
        """Condition on evidence: drop those variables and fix their values."""
        fixed = {v: bool(evidence[v]) for v in self.variables if v in evidence}
        if not fixed:
            return Factor(self.variables, self.table)
        remaining = tuple(v for v in self.variables if v not in fixed)
        table = {}
        for assignment in product([True, False], repeat=len(remaining)):
            full = {}
            it = iter(assignment)
            for v in self.variables:
                full[v] = fixed[v] if v in fixed else next(it)
            table[assignment] = self.table[tuple(full[v] for v in self.variables)]
        return Factor(remaining, table)

    def multiply(self, other):
        """Factor product over the union of the variables."""
        common = tuple(v for v in self.variables if v in other.variables)
        # align the two tables on the shared variables
        merged_vars = list(self.variables) + [v for v in other.variables if v not in self.variables]
        table = {}
        for assignment in product([True, False], repeat=len(merged_vars)):
            values = dict(zip(merged_vars, assignment))
            a = tuple(values[v] for v in self.variables)
            b = tuple(values[v] for v in other.variables)
            table[assignment] = self.table[a] * other.table[b]
        return Factor(merged_vars, table)

    def sum_out(self, variable):
        """Marginalise away one variable."""
        if variable not in self.variables:
            raise ValueError(f"{variable} is not in {self.variables}")
        remaining = tuple(v for v in self.variables if v != variable)
        table = {}
        for assignment in product([True, False], repeat=len(remaining)):
            values = dict(zip(remaining, assignment))
            total = 0.0
            for value in (True, False):
                values[variable] = value
                total += self.table[tuple(values[v] for v in self.variables)]
            table[assignment] = total
        return Factor(remaining, table)

    def normalize(self):
        """Divide by the total, returning (factor, total)."""
        total = float(self.dense().sum())
        if total <= 0.0:
            raise ValueError("cannot normalise a factor with zero mass")
        table = {k: v / total for k, v in self.table.items()}
        return Factor(self.variables, table), total

    def value(self, **assignment):
        return self.table[tuple(bool(assignment[v]) for v in self.variables)]


def variable_elimination(factors, query, evidence=None, order=None, trace=None):
    """P(query=True | evidence) by variable elimination.

    factors: list of Factor objects whose product is the joint distribution.
    order:   elimination order for hidden variables; default keeps the given order.
    trace:   optional list; each elimination step is appended as a dict.
    """
    evidence = dict(evidence or {})
    known = {v for f in factors for v in f.variables}
    unknown_evidence = set(evidence) - known
    if unknown_evidence:
        raise ValueError(f"evidence names unknown variables: {sorted(unknown_evidence)}")
    non_boolean = [v for v in evidence.values() if not isinstance(v, bool)]
    if non_boolean:
        raise ValueError(f"evidence values must be True or False, got {non_boolean}")
    if query not in known:
        raise ValueError(f"unknown query variable {query!r}")
    if query in evidence:
        raise ValueError("query variable appears in the evidence")
    factors = [f.restrict(evidence) for f in factors]
    hidden = []
    for f in factors:
        for v in f.variables:
            if v != query and v not in hidden:
                hidden.append(v)
    if order is None:
        order = hidden
    unknown = [v for v in order if v not in hidden]
    if unknown:
        raise ValueError(f"not hidden variables (already fixed or unknown): {unknown}")
    for variable in order:
        touching = [f for f in factors if variable in f.variables]
        rest = [f for f in factors if variable not in f.variables]
        if not touching:
            continue
        product_factor = touching[0]
        for f in touching[1:]:
            product_factor = product_factor.multiply(f)
        before = product_factor
        summed = product_factor.sum_out(variable)
        if trace is not None:
            trace.append({"eliminated": variable, "before": before, "after": summed})
        factors = rest + [summed]
    result = factors[0]
    for f in factors[1:]:
        result = result.multiply(f)
    for leftover in [v for v in result.variables if v != query]:
        result = result.sum_out(leftover)
    if result.variables != (query,):
        raise ValueError(f"query variable {query!r} vanished during elimination")
    normalised, total = result.normalize()
    return normalised.value(**{query: True}), total


# ---------------------------------------------------------------------------
# The alarm network as factors
# ---------------------------------------------------------------------------

def alarm_factors():
    from alarm_network import (
        P_ALARM_TRUE, P_BURGLARY, P_EARTHQUAKE, P_JOHN_CALLS, P_MARY_CALLS,
    )

    f_burglary = Factor.from_array(["B"], [P_BURGLARY[True], P_BURGLARY[False]])
    f_earthquake = Factor.from_array(["E"], [P_EARTHQUAKE[True], P_EARTHQUAKE[False]])
    # P(A | B, E): axis order (A, B, E), each in (True, False) order
    values = np.zeros((2, 2, 2))
    for ai, a in enumerate((True, False)):
        for bi, b in enumerate((True, False)):
            for ei, e in enumerate((True, False)):
                values[ai, bi, ei] = P_ALARM_TRUE[(b, e)] if a else 1 - P_ALARM_TRUE[(b, e)]
    f_alarm = Factor.from_array(["A", "B", "E"], values)

    # P(J | A) and P(M | A): axis order (child, A)
    def child_factor(name, table):
        values = np.zeros((2, 2))
        for ci, c in enumerate((True, False)):
            for ai, a in enumerate((True, False)):
                values[ci, ai] = table[a] if c else 1 - table[a]
        return Factor.from_array([name, "A"], values)

    f_john = child_factor("J", P_JOHN_CALLS)
    f_mary = child_factor("M", P_MARY_CALLS)
    return [f_burglary, f_earthquake, f_alarm, f_john, f_mary]


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


def run_tests():
    """Factor algebra, agreement with enumeration, and agreement with brute force."""
    import alarm_network as net

    # --- factor algebra on hand-checkable examples
    a = Factor.from_array(["X"], [0.2, 0.8])
    b = Factor.from_array(["X"], [0.5, 0.1])
    product = a.multiply(b)
    assert abs(product.value(X=True) - 0.10) < 1e-12
    assert abs(product.value(X=False) - 0.08) < 1e-12
    assert abs(a.sum_out("X").value() - 1.0) < 1e-12          # sums to 1 over X
    assert abs(product.sum_out("X").value() - 0.18) < 1e-12   # individual factor does not
    restricted = a.restrict({"X": True})
    assert restricted.variables == () and abs(restricted.value() - 0.2) < 1e-12
    normed, total = product.normalize()
    assert abs(total - 0.18) < 1e-12
    assert abs(normed.value(X=True) - 0.10 / 0.18) < 1e-12

    # independent variables: product of marginals is the joint
    p = Factor.from_array(["X"], [0.2, 0.8])
    q = Factor.from_array(["Y"], [0.3, 0.7])
    pq = p.multiply(q)
    assert abs(pq.value(X=True, Y=True) - 0.06) < 1e-12

    # --- agreement with enumeration for every evidence case
    def order_for(ev):
        fixed = {n for n in ("E", "A") if n in ev}
        default = [v for v in ("E", "A") if v not in fixed]
        return default

    for label, ev in EVIDENCE_CASES:
        ve, _ = variable_elimination(alarm_factors(), "B", ev, order=order_for(ev))
        enum, _ = net.enumerate_posterior("B", ev)
        assert abs(ve - enum) < 1e-12, (label, ve, enum)

    # --- agreement with brute force over the 32 joint entries
    table = net.joint_table()
    for label, ev in EVIDENCE_CASES:
        den = sum(v for k, v in table.items()
                  if all(k[net.NODES.index(n)] == val for n, val in ev.items()))
        num = sum(v for k, v in table.items()
                  if k[0] is True and all(k[net.NODES.index(n)] == val for n, val in ev.items()))
        ve, total = variable_elimination(alarm_factors(), "B", ev, order=order_for(ev))
        assert abs(ve - num / den) < 1e-12, (label, ve, num / den)
        assert abs(total - den) < 1e-12, (label, total, den)

    # --- elimination order must not change the answer
    for order in (["E", "A"], ["A", "E"]):
        ve, _ = variable_elimination(alarm_factors(), "B", {"J": True, "M": True}, order=order)
        assert abs(ve - 0.2841718) < 1e-6, (order, ve)

    # --- A is a valid query too
    ve_a, _ = variable_elimination(alarm_factors(), "A", {"J": True}, order=["E", "M", "B"])
    assert abs(ve_a - net.enumerate_posterior("A", {"J": True})[0]) < 1e-12

    # --- invalid usage raises
    for bad in ({"B": True}, {"X": True}):
        try:
            variable_elimination(alarm_factors(), "B", bad, order=["E", "A"])
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError(f"accepted invalid evidence/query: {bad}")

    return True


if __name__ == "__main__":
    print(f"{'evidence':24s} {'VE':>8s} {'enumeration':>12s} {'abs diff':>10s}")
    import alarm_network as net
    for label, ev in EVIDENCE_CASES:
        fixed = {n for n in ("E", "A") if n in ev}
        ve, _ = variable_elimination(alarm_factors(), "B", ev,
                                     order=[v for v in ("E", "A") if v not in fixed])
        enum, _ = net.enumerate_posterior("B", ev)
        print(f"{label:24s} {ve:8.4f} {enum:12.4f} {abs(ve - enum):10.1e}")
    print("tests passed:", run_tests())

    trace = []
    variable_elimination(alarm_factors(), "B", {"J": True, "M": True}, order=["E", "A"], trace=trace)
    print("\nintermediate factors, evidence J=True, M=True, order E then A:")
    for step in trace:
        print("  eliminate", step["eliminated"], ":", step["before"].variables,
              "->", step["after"].variables, step["after"].table)
