"""neurosymbolic.py -- hybrid, neuro-symbolic and explainable deep learning (M14, L14-01).

A benefit-eligibility decision, the classic place where pure ML is the wrong tool:

    rules only          an explicit policy, perfectly auditable, brittle to the soft cases
    model only          a neural network, accurate, and able to produce ineligible answers
    hybrid              the model ranks, the policy gates: every output is rule-compliant

The point is not that the hybrid is more accurate. It is that the hybrid cannot emit an
answer the policy forbids, which is what an auditor actually asks for.

Also measured: integrated gradients against the model, and where the attribution points
compared with the rule that actually binds. Saliency is not a reason.

Run ``python neurosymbolic.py``.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)
np.random.seed(0)

INCOME_CAP = 25_000.0
PER_PERSON = 5_000.0
SAVINGS_CAP = 3_000.0


# ---------------------------------------------------------------------------
# 1. The policy
# ---------------------------------------------------------------------------

def policy(income, savings, size, owns_property):
    """The published rule. Boolean, auditable, and the authority on eligibility."""
    income_ok = income < INCOME_CAP + PER_PERSON * size
    savings_ok = savings < SAVINGS_CAP
    property_ok = ~((owns_property > 0.5) & (income > 18_000))
    return income_ok & savings_ok & property_ok


def make_data(n=6000, seed=0):
    rng = np.random.default_rng(seed)
    size = rng.integers(1, 6, n).astype(float)
    income = rng.normal(22_000 + 4_000 * size, 9_000, n).clip(0, None)
    savings = rng.normal(2_400, 2_200, n).clip(0, None)
    owns = rng.binomial(1, 0.34, n).astype(float)
    age = rng.normal(42, 13, n)
    region = rng.integers(0, 9, n).astype(float)

    eligible = policy(income, savings, size, owns)
    # 3% of decisions were made by a caseworker who deviated from policy
    flip = rng.random(n) < 0.03
    label = np.where(flip, ~eligible, eligible).astype(int)

    X = np.column_stack([income / 10_000, savings / 1_000, size, owns, age / 10, region])
    return X.astype(np.float32), label, eligible, {
        "income": income, "savings": savings, "size": size, "owns": owns}


# ---------------------------------------------------------------------------
# 2. Model
# ---------------------------------------------------------------------------

class MLP(nn.Module):
    def __init__(self, d_in=6, hidden=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, hidden), nn.ReLU(),
                                 nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)


def train_model(X, y, epochs=40, seed=0, lr=3e-3):
    torch.manual_seed(seed)
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Xs = torch.tensor((X - mu) / sd, dtype=torch.float32)
    t = torch.tensor(y, dtype=torch.float32)
    model = MLP()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.BCEWithLogitsLoss()
    for _ in range(epochs):
        opt.zero_grad()
        loss = loss_fn(model(Xs), t)
        loss.backward()
        opt.step()
    return model, mu, sd


def predict(model, mu, sd, X):
    with torch.no_grad():
        logits = model(torch.tensor((X - mu) / sd, dtype=torch.float32))
        return torch.sigmoid(logits).numpy()


# ---------------------------------------------------------------------------
# 3. Integrated gradients (explainable deep learning)
# ---------------------------------------------------------------------------

def integrated_gradients(model, mu, sd, x, steps=48):
    """Attribution with respect to the zero baseline, averaged along the path."""
    x = np.asarray(x, dtype=np.float32)
    xs = (x - mu) / sd
    base = np.zeros_like(xs)
    total = np.zeros_like(xs)
    for a in np.linspace(0, 1, steps):
        point = torch.tensor((base + a * (xs - base))[None, :], dtype=torch.float32,
                             requires_grad=True)
        out = torch.sigmoid(model(point)).sum()
        out.backward()
        total += point.grad.detach().numpy()[0]
    return (xs - base) * total / steps


# ---------------------------------------------------------------------------
# 4. Evaluate the three designs
# ---------------------------------------------------------------------------

def evaluate(probs, eligible):
    """Accuracy against the caseworker labels is computed by the caller; here we report
    policy compliance: an answer of 'eligible' when the rule says otherwise."""
    decided = (probs >= 0.5).astype(int)
    violations = int(((decided == 1) & (~eligible)).sum())
    return decided, violations


def main():
    X, y, eligible, raw = make_data()
    n = len(y)
    split = int(0.7 * n)
    Xtr, Xte = X[:split], X[split:]
    ytr, yte = y[:split], y[split:]
    etr, ete = eligible[:split], eligible[split:]
    raw_te = {k: v[split:] for k, v in raw.items()}

    model, mu, sd = train_model(Xtr, ytr)
    probs = predict(model, mu, sd, Xte)

    model_pred, model_viol = evaluate(probs, ete)
    rules_pred = ete.astype(int)
    hybrid_pred = ((probs >= 0.5) & ete).astype(int)
    _, hybrid_viol = evaluate(hybrid_pred.astype(float), ete)

    def acc(pred):
        return float((pred == yte).mean())

    print("=" * 78)
    print("1. Three designs on the same decision (test n = %d)" % len(yte))
    print("=" * 78)
    print(f"{'design':16s} {'accuracy':>9} {'policy violations':>18} {'extra refusals':>15}")
    print(f"{'rules only':16s} {acc(rules_pred):9.3f} {0:18d} "
          f"{int((rules_pred == 0).sum() - (model_pred == 0).sum()):15d}")
    print(f"{'model only':16s} {acc(model_pred):9.3f} {model_viol:18d} {0:15d}")
    print(f"{'hybrid':16s} {acc(hybrid_pred):9.3f} {hybrid_viol:18d} "
          f"{int(((probs >= 0.5) & ~ete).sum()):15d}")
    print("\n  'extra refusals' counts people the model would have approved but the policy")
    print("  does not allow -- the price of compliance, paid by individuals.")

    # soft-case analysis: where does the model disagree with the rule and still win?
    disagree = np.where((model_pred == 1) & (~ete))[0]
    print(f"\n  model approved {len(disagree)} policy-ineligible applicants out of "
          f"{int((~ete).sum())} ({len(disagree)/max(1,int((~ete).sum())):.1%})")

    silent = int(((probs >= 0.5) & ete).sum())
    print(f"  hybrid approved {silent} eligible applicants "
          f"({silent/max(1,int(ete.sum())):.1%} of the eligible group)")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("2. Why the model thought so: integrated gradients vs the binding rule")
    print("=" * 78)
    names = ["income/10k", "savings/1k", "household", "owns property", "age/10", "region"]
    if len(disagree):
        i = int(disagree[0])
        attrs = integrated_gradients(model, mu, sd, Xte[i])
        order = np.argsort(-np.abs(attrs))
        print("  applicant:", {k: round(float(v[i]), 1) for k, v in raw_te.items()})
        print(f"  model probability {probs[i]:.3f}; policy says ineligible")
        print("  integrated gradients:")
        for j in order:
            print(f"    {names[j]:16s} {attrs[j]:+.3f}")
        print("\n  the binding rule is income < 25,000 + 5,000 x household, which the")
        print("  attribution does not state. An attribution ranks influence; a policy")
        print("  gives a reason. Only one of them can be appealed against.")

        print("\n  rule trace for this applicant:")
        inc, sav, size, owns = raw_te['income'][i], raw_te['savings'][i], \
            raw_te['size'][i], raw_te['owns'][i]
        print(f"    income {inc:,.0f} vs cap {INCOME_CAP + PER_PERSON*size:,.0f} -> "
              f"{'pass' if inc < INCOME_CAP + PER_PERSON*size else 'FAIL'}")
        print(f"    savings {sav:,.0f} vs cap {SAVINGS_CAP:,.0f} -> "
              f"{'pass' if sav < SAVINGS_CAP else 'FAIL'}")
        print(f"    property/income check -> "
              f"{'pass' if not (owns > 0.5 and inc > 18000) else 'FAIL'}")
    else:
        print("  no policy-violating approvals in this split")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("3. What the hybrid costs and buys")
    print("=" * 78)
    extra = int(((probs >= 0.5) & ~ete).sum())
    print(f"  accuracy: model {acc(model_pred):.3f}, rules {acc(rules_pred):.3f}, "
          f"hybrid {acc(hybrid_pred):.3f}")
    print(f"  policy violations: model {model_viol}, hybrid {hybrid_viol}")
    print(f"  cost: {extra} applicants refused whose caseworker had approved them")
    print("  the hybrid is not more accurate here; it is the only design whose output")
    print("  can be defended line by line to someone who was refused.")


if __name__ == "__main__":
    main()
