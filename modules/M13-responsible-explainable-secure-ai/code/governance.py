"""governance.py -- risk registers, model cards, datasheets and audit checklists (M13, L13-05/06 / MP-13).

Governance is paperwork only when the paperwork is disconnected from measurements.
Here every artefact is generated from values you can reproduce:

    RiskRegister      likelihood x impact, controls, residual score, owner
    model_card()      intended use, metrics, subgroup results, limits, monitoring
    datasheet()       provenance, collection, preprocessing, known biases
    audit_checklist() the eight questions a reviewer should be able to answer

Run ``python governance.py`` to print the register and write the three documents
into ``outputs/``. Fill the measured values from your own audit; the examples
here come from the modules' own experiments.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


# ---------------------------------------------------------------------------
# 1. Risk register
# ---------------------------------------------------------------------------

RISKS = [
    {"id": "R1", "category": "fairness",
     "description": "Recruitment screen reproduces historical label bias",
     "likelihood": 4, "impact": 5, "owner": "model owner",
     "controls": ["group metrics in CI", "reweighing or threshold review", "human review of rejects"]},
    {"id": "R2", "category": "fairness",
     "description": "Proxy feature (tutoring access) drives student predictions",
     "likelihood": 4, "impact": 3, "owner": "data owner",
     "controls": ["proxy audit", "drop-and-compare ablation", "document the accuracy cost"]},
    {"id": "R3", "category": "privacy",
     "description": "Membership inference reveals who was in the training set",
     "likelihood": 3, "impact": 4, "owner": "privacy lead",
     "controls": ["regularisation", "output perturbation", "access logging"]},
    {"id": "R4", "category": "privacy",
     "description": "RAG assistant returns a confidential staff record",
     "likelihood": 4, "impact": 5, "owner": "service owner",
     "controls": ["document-level ACLs", "PII redaction", "leakage regression tests"]},
    {"id": "R5", "category": "security",
     "description": "Adversarial perturbation changes an image classification",
     "likelihood": 3, "impact": 3, "owner": "ML engineer",
     "controls": ["adversarial training", "input validation", "ensemble checks"]},
    {"id": "R6", "category": "security",
     "description": "Prompt injection causes an agent to send email",
     "likelihood": 4, "impact": 5, "owner": "platform owner",
     "controls": ["default-deny approvals", "action allowlist", "untrusted-text delimiting"]},
    {"id": "R7", "category": "security",
     "description": "Backdoored model passes clean evaluation",
     "likelihood": 2, "impact": 5, "owner": "supply chain owner",
     "controls": ["model provenance", "trigger scanning", "independent evaluation data"]},
    {"id": "R8", "category": "governance",
     "description": "Model card omits subgroup performance and monitoring",
     "likelihood": 3, "impact": 3, "owner": "product owner",
     "controls": ["template with mandatory fields", "review before release"]},
]

# Residual likelihood/impact after the listed controls are actually in place.
RESIDUAL = {"R1": (3, 4), "R2": (2, 2), "R3": (2, 3), "R4": (2, 2),
            "R5": (3, 3), "R6": (2, 3), "R7": (2, 4), "R8": (1, 2)}


def band(score: int) -> str:
    if score >= 16:
        return "critical"
    if score >= 10:
        return "high"
    if score >= 5:
        return "medium"
    return "low"


class RiskRegister:
    def __init__(self, risks=None, residual=None):
        self.risks = risks or RISKS
        self.residual = residual or RESIDUAL

    def rows(self) -> list[dict]:
        rows = []
        for r in self.risks:
            inherent = r["likelihood"] * r["impact"]
            rl, ri = self.residual.get(r["id"], (r["likelihood"], r["impact"]))
            rows.append({**r, "inherent": inherent, "band": band(inherent),
                         "residual": rl * ri, "residual_band": band(rl * ri),
                         "reduction": inherent - rl * ri})
        return sorted(rows, key=lambda x: -x["residual"])

    def to_markdown(self) -> str:
        lines = ["# Risk register", "",
                 "| ID | Category | Risk | L | I | Score | Band | Residual | Band | Controls |",
                 "| :--- | :--- | :--- | ---: | ---: | ---: | :--- | ---: | :--- | :--- |"]
        for row in self.rows():
            lines.append(
                f"| {row['id']} | {row['category']} | {row['description']} | "
                f"{row['likelihood']} | {row['impact']} | {row['inherent']} | "
                f"{row['band']} | {row['residual']} | {row['residual_band']} | "
                f"{'; '.join(row['controls'])} |")
        lines += ["", "Scores are likelihood (1-5) x impact (1-5). A residual band of",
                  "'high' or above blocks release until further controls are added.", ""]
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps(self.rows(), indent=2)


# ---------------------------------------------------------------------------
# 2. Model card
# ---------------------------------------------------------------------------

MODEL_CARD_TEMPLATE = """# Model card: {name}

| | |
| :--- | :--- |
| Version | {version} |
| Owner | {owner} |
| Licence | {licence} |
| Intended use | {intended_use} |
| Out of scope | {out_of_scope} |

## Training data

{data_summary}

## Metrics

| Slice | Accuracy | Selection rate | TPR | FPR | n |
| :--- | ---: | ---: | ---: | ---: | ---: |
{metric_rows}

## Fairness

- Demographic parity difference: {dp:.3f}
- Disparate impact ratio: {di:.3f} (80% rule threshold: 0.80)
- Equal opportunity difference: {eopp:.3f}
- Equalised odds difference: {eodds:.3f}

## Explainability

{explainability}

## Security and privacy

{security}

## Known limitations

{limitations}

## Monitoring

{monitoring}
"""


def model_card(name: str, version: str, owner: str, licence: str, intended_use: str,
               out_of_scope: str, data_summary: str, slices: list[dict],
               fairness: dict, explainability: str, security: str,
               limitations: list[str], monitoring: list[str]) -> str:
    rows = "\n".join(
        f"| {s['group']} | {s['accuracy']:.3f} | {s['selection_rate']:.3f} | "
        f"{s['tpr']:.3f} | {s['fpr']:.3f} | {s['n']} |" for s in slices)
    return MODEL_CARD_TEMPLATE.format(
        name=name, version=version, owner=owner, licence=licence,
        intended_use=intended_use, out_of_scope=out_of_scope,
        data_summary=data_summary, metric_rows=rows,
        dp=fairness["demographic_parity_difference"],
        di=fairness["disparate_impact_ratio"],
        eopp=fairness["equal_opportunity_difference"],
        eodds=fairness["equalized_odds_difference"],
        explainability=explainability, security=security,
        limitations="\n".join(f"- {x}" for x in limitations),
        monitoring="\n".join(f"- {x}" for x in monitoring))


# ---------------------------------------------------------------------------
# 3. Datasheet
# ---------------------------------------------------------------------------

def datasheet(name: str, motivation: str, composition: str, collection: str,
              preprocessing: list[str], known_bias: list[str], licence: str,
              maintenance: str) -> str:
    return "\n".join([
        f"# Datasheet: {name}", "",
        "## Motivation", motivation, "",
        "## Composition", composition, "",
        "## Collection process", collection, "",
        "## Preprocessing", *[f"- {p}" for p in preprocessing], "",
        "## Known bias and limits", *[f"- {b}" for b in known_bias], "",
        "## Licence", licence, "",
        "## Maintenance", maintenance, ""])


# ---------------------------------------------------------------------------
# 4. Audit checklist
# ---------------------------------------------------------------------------

CHECKLIST = [
    ("Purpose and scope", "Intended use, out-of-scope use and the decision the system supports are written down."),
    ("Data provenance", "Datasheet exists; licence, collection method and known gaps are documented."),
    ("Performance", "Accuracy and the metric tied to the decision are reported with a baseline and n."),
    ("Subgroup performance", "Metrics are reported per group with n per group; gaps are stated."),
    ("Explainability", "At least one global and one local explanation; fidelity and stability measured."),
    ("Privacy", "PII handling, retention and membership-inference risk assessed."),
    ("Security", "Injection, adversarial and tool-abuse tests run; residual risks listed."),
    ("Human oversight", "Approval gates, escalation path and a named accountable owner exist."),
    ("Monitoring", "Live metrics, drift checks, alert thresholds and a review cadence are specified."),
    ("Documentation", "Model card and risk register are current and reviewed before release."),
]


def audit_checklist(evidence: dict | None = None) -> str:
    evidence = evidence or {}
    lines = ["# Audit checklist", "",
             "| # | Area | Requirement | Evidence | Status |",
             "| ---: | :--- | :--- | :--- | :--- |"]
    for i, (area, requirement) in enumerate(CHECKLIST, start=1):
        ev = evidence.get(area, "")
        status = "complete" if ev else "missing"
        lines.append(f"| {i} | {area} | {requirement} | {ev or '-'} | {status} |")
    missing = sum(1 for area, _ in CHECKLIST if area not in evidence)
    lines += ["", f"**Missing evidence: {missing} of {len(CHECKLIST)} items.**",
              "", "An audit is not a vibe check. Each row needs a file, a number or a link.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    register = RiskRegister()
    print("=" * 92)
    print("Risk register (sorted by residual risk)")
    print("=" * 92)
    print(f"{'ID':4s} {'category':12s} {'L':>2} {'I':>2} {'score':>6} {'band':>9} "
          f"{'resid':>6} {'band':>9}")
    for row in register.rows():
        print(f"{row['id']:4s} {row['category']:12s} {row['likelihood']:2d} "
              f"{row['impact']:2d} {row['inherent']:6d} {row['band']:>9} "
              f"{row['residual']:6d} {row['residual_band']:>9}")
    (OUT / "risk-register.md").write_text(register.to_markdown(), encoding="utf-8")
    (OUT / "risk-register.json").write_text(register.to_json(), encoding="utf-8")

    card = model_card(
        name="Synthetic student pass predictor",
        version="1.0.0", owner="Teaching team", licence="CC0-1.0 (code), synthetic data",
        intended_use="Teaching explainability and fairness measurement",
        out_of_scope="Any real admission, progression or funding decision",
        data_summary="3,000 synthetic students; four features; label generated from a "
                     "logistic model that includes a group-correlated tutoring proxy.",
        slices=[
            {"group": "C", "accuracy": 0.866, "selection_rate": 0.996, "tpr": 0.998,
             "fpr": 0.981, "n": 454},
            {"group": "D", "accuracy": 0.857, "selection_rate": 0.993, "tpr": 0.995,
             "fpr": 0.986, "n": 446},
        ],
        fairness={"demographic_parity_difference": 0.004,
                  "disparate_impact_ratio": 0.996,
                  "equal_opportunity_difference": 0.003,
                  "equalized_odds_difference": 0.014},
        explainability="Logistic regression is the model; coefficients are reported. "
                       "Permutation importance and LIME agree on attendance and prior "
                       "attainment; LIME stability across five seeds is reported.",
        security="No user-facing prediction endpoint. Adversarial and injection tests "
                 "not applicable to this offline teaching model.",
        limitations=["synthetic data", "two groups only", "no temporal drift",
                     "label depends on the same proxy the model uses"],
        monitoring=["weekly subgroup metric review", "drift check on feature means",
                    "retrain when label distribution shifts by more than 5 points"])
    (OUT / "model-card.md").write_text(card, encoding="utf-8")

    sheet = datasheet(
        name="synthetic student pass prediction",
        motivation="Teach proxy discrimination without using real student records.",
        composition="3,000 rows, 4 features, 2 groups, binary label; generated in-script.",
        collection="Generated by rai_data.student(seed=0); no human subjects.",
        preprocessing=["no scaling required for tree/linear baselines",
                       "tutoring_access is intentionally retained as the proxy"],
        known_bias=["tutoring access correlates with group and predicts the label",
                    "prior attainment is correlated with tutoring access",
                    "no intersectional attributes"],
        licence="CC0-1.0",
        maintenance="Regenerated by script; version tied to the module release.")
    (OUT / "datasheet.md").write_text(sheet, encoding="utf-8")

    evidence = {"Purpose and scope": "model-card.md#intended-use",
                "Data provenance": "datasheet.md",
                "Performance": "fairness.py output",
                "Subgroup performance": "fairness.py output",
                "Explainability": "explain.py output",
                "Privacy": "security.py membership-inference",
                "Security": "llm_security.py injection results"}
    checklist = audit_checklist(evidence)
    (OUT / "audit-checklist.md").write_text(checklist, encoding="utf-8")

    print("\nwrote:")
    for name in ("risk-register.md", "risk-register.json", "model-card.md",
                 "datasheet.md", "audit-checklist.md"):
        p = OUT / name
        print(f"  {name:22s} {p.stat().st_size:6d} bytes")
    print("\naudit status:")
    print(f"  evidence provided for {len(evidence)} of {len(CHECKLIST)} areas")


if __name__ == "__main__":
    main()
