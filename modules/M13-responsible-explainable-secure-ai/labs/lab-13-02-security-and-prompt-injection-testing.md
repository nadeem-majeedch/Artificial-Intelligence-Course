# LAB-13-02 — Security and Prompt-Injection Testing

| | |
| :--- | :--- |
| Time | 2.5 hours |
| Level | 300 |
| Prerequisites | L13-03, L13-04 |
| Code | `code/security.py`, `code/llm_security.py`, `code/guardrails_m13.py` |

[Module home](../README.md) · [Lab 13-01](lab-13-01-fairness-audit.md) · [Assignment](../assignments/asg-13-model-card-and-audit-report.md)

## Purpose

Run five attack families against systems you built, measure how well they work, then measure
what each defence costs. Produce a security section for a model card.

**Scope and ethics.** Every experiment runs in-process against models you trained on
synthetic data or scikit-learn's public-domain digits, in a controlled local environment. You
are not to point any of this at a live service, an API you do not own, or another person's
chatbot. The deliverable is a defensive report, not an exploit.

**Deliverable.** A security report of at most 1,000 words plus tables, structured as in
section 7.

---

## 1. Setup

```bash
cd modules/M13-responsible-explainable-secure-ai/code
python security.py        # ~60-90 s on CPU: evasion, poisoning, backdoor, MI, extraction
python llm_security.py    # injection, RAG leakage, tool abuse
python guardrails_m13.py  # detection table and redaction
```

`security.py` trains five small models. If it is too slow, reduce `epochs` in `main()` and
record that you did — the numbers change, and the report must say so.

Note the simulator. `llm_security.ToyLLM` is not a language model; it is a deterministic
stand-in that obeys the last imperative it finds. `flan-t5-small` is too weak to comply with
injected instructions (M11 measured 0.00 compliance), so a real model cannot demonstrate the
attack. Say so in your report; do not present simulator results as measurements of a real
model.

## 2. Scenario 4 — adversarial image perturbations (40 minutes)

1. Copy the evasion table:

   ```text
       eps   FGSM acc   PGD acc
      0.00      0.913     0.913
      0.05      0.741     0.737
      0.10      0.470     0.461
      0.20      0.030     0.024
      0.30      0.000     0.015
   ```

2. Find the smallest $\varepsilon$ (to two decimals) where accuracy falls below 0.5. Report it
   as a fraction of the pixel range and describe what it would look like on a 224×224 photo.
3. Why is PGD usually stronger than FGSM, and where in the table does it lose?
4. Train the adversarially trained model's clean accuracy is 0.587 against 0.913. Compute the
   clean-accuracy cost and the robust-accuracy gain at $\varepsilon=0.2$ (0.313 vs 0.030).
   Is the trade worth it for a document scanner? For a medical image triage? Justify both.
5. Quantisation raises adversarial accuracy from 0.470 to 0.669 at $\varepsilon=0.1$ with no
   clean cost. Explain why it is nonetheless not a defence you would rely on.

## 3. Scenario 4b — poisoning and backdoor (35 minutes)

1. Poisoning flipped 12 labels (about 1%) and moved 30% of class 3 to class 8. Record clean
   accuracy (0.870 vs 0.913) and the targeted error rate (0.182 vs 0.109).
2. Raise the poison rate to 10% and 25%. Plot clean accuracy and targeted error against poison
   rate. Is the relationship linear?
3. The backdoor model has **clean accuracy 0.917** — better than the clean baseline — and an
   attack success rate of 0.855 on triggered inputs. Explain why clean evaluation cannot find
   it.
4. Change the trigger to a single white pixel. Does the attack still work? What does the
   answer imply for trigger detection as a defence?
5. Write the two-line procurement rule that would have prevented this model from being
   trusted on arrival.

## 4. Scenario 5 — prompt injection in a controlled chatbot (30 minutes)

1. Run `llm_security.py`. Record the six-case table, the unguarded rate (0.83) and the guarded
   rate (0.17).
2. Case I1 still succeeds under guardrails. Explain why an action allowlist cannot stop it,
   and what would.
3. For each of the three controls (sanitising, allowlist, redaction), state one attack it
   stops and one it does not.
4. Detection: run `guardrails_m13.py`. Which of the six injection cases does
   `detect_injection` miss entirely? What does that mean for using a detector as a security
   boundary?
5. Write one indirect-injection document (8–12 words) that evades the detector. Then propose a
   control that works without detection. Do not include anything that would function against a
   live system.

## 5. Scenario 6 — agent tool abuse (20 minutes)

1. Record the unsafe execution counts: 4/6 without guardrails, 0/6 with.
2. Which of the six requests are unsafe, and why is the "I am the administrator" one not
   authentication?
3. Add a `summarise_document` tool. Write its policy: allowed arguments, approval
   requirement, logging. Then craft two requests that should be denied and two that should be
   allowed, and check your policy against them.
4. Explain why default-deny is the correct default for external actions, in terms of
   reversibility.

## 6. Scenario 7 — RAG data leakage (20 minutes)

1. Record the leak rates: 1/5 without controls, 0/5 with.
2. Which query leaked, and which document did retrieval surface for it?
3. The guarded system now refuses to answer some questions it previously answered. Why is that
   the correct trade?
4. Describe the access-control enforcement point. Why is post-generation filtering too late?
5. Add a second confidential document that shares vocabulary with a public one, and rerun.
   Does the filter still hold?

## 7. Report structure

1. **Threat model**: what you attacked, with what access, what a real attacker would have that
   you do not.
2. **Results**: one table per attack family — attack strength, metric, before/after.
3. **Defences**: control, measured effect, cost, failure mode.
4. **Residual risk**: what remains, ranked, with the control you would add next.
5. **Model-card security paragraph**: six to ten lines, every claim a measurement.

## 8. Reflection questions

1. Accuracy 0.913 and robust accuracy 0.030 are the same model. Which number belongs in a
   product brochure, and what makes the other one honest?
2. A backdoored model scored *higher* on clean data than the clean baseline. What does this
   imply about evaluating artefacts you did not train?
3. Prompt injection is often described as a prompt-engineering problem. Using I1 and I6, argue
   that it is a capability problem.
4. The membership-inference attack failed (AUC 0.513). Should that result appear in the model
   card? What is the risk of reporting a negative result?
5. Every defence in this lab has a cost. Which cost would you refuse to pay, and for which
   system?

## 9. Marking criteria

| Criterion | Weight | Strong answers |
| :--- | ---: | :--- |
| Measurement | 30% | attack strength, metric and sample size all stated |
| Defence evaluation | 25% | cost reported with benefit; failure mode named |
| Threat-model discipline | 20% | scope respected; simulator disclosed |
| Residual risk | 15% | ranked, with a next control |
| Reflection | 10% | engages with reversibility and capability |

## 10. Common pitfalls

- Presenting simulator results as if a real LLM had been attacked.
- Reporting attack success without the poison rate, $\varepsilon$ or trigger definition.
- Declaring robustness after testing one $\varepsilon$.
- Using detection accuracy as evidence of a security boundary.
- Forgetting that the guarded RAG system now refuses more — utility has a cost too.

---

[Module home](../README.md) · [Lab 13-01](lab-13-01-fairness-audit.md) ·
[Assignment](../assignments/asg-13-model-card-and-audit-report.md)
