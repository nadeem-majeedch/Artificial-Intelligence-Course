# L13-03 — Privacy, Memorisation and Model Attacks

| | |
| :--- | :--- |
| Level | 300 |
| Study time | 90 minutes |
| Prerequisites | L13-01, L13-02 |
| Code | `code/security.py` (sections 6–7), `code/llm_security.py` (section 2) |

[← Previous: L13-02 Explainability: From Importance to Counterfactuals](L13-02-explainability-from-importance-to-counterfactuals.md) · [Module home](../README.md) · [Next: L13-04 Security: Adversarial Examples and Prompt Injection →](L13-04-security-adversarial-examples-and-prompt-injection.md)

## Why this lesson exists

A model is a compressed function of its training data. Compression is lossy but not
lossless: some records leave traces. Privacy attacks exploit those traces to answer two
questions — *was this person in the training set?* and *can I reproduce the model?* — and,
in the worst case, *what did the training record contain?*

You will run two of these attacks against your own models, and — more importantly — see one
of them **fail**, because a model that does not overfit is hard to attack. That negative
result is the practical lesson: most privacy defence is just not overfitting, plus a few
structural controls.

**All exercises here use synthetic data and models you trained yourself. Never run a
membership-inference or extraction attack against a system you do not own.**

---

## 1. The threat model

| Attack | Attacker knows | Attacker wants | Signal exploited |
| :--- | :--- | :--- | :--- |
| Membership inference | model + one record | was this record in training? | confidence gap between seen and unseen data |
| Model extraction | query access | a copy of the model | input–output pairs are enough to fit a surrogate |
| Model inversion | model + target label | a representative input | gradient or confidence structure |
| Attribute inference | model + partial record | a hidden attribute | correlation with observed features |
| Training-data extraction | generative model | verbatim records | memorisation of rare sequences |

The line between "privacy" and "security" is thin: membership inference is a privacy attack
on a model, and model extraction is intellectual-property theft. The mechanisms are the
same family.

## 2. Membership inference

The idea: a model that overfits is more confident on records it saw. Train a classifier on
(confidence, correct?) features to separate members from non-members. If the attacker can do
that better than chance, membership leaks.

Measured on the 8×8-digit classifier (12 epochs, 1,257 training / 540 test):

```text
  mean confidence train 0.781  test 0.772
  attack AUC 0.513  TPR 0.500  FPR 0.491 at threshold 0.844
```

**The attack fails.** AUC 0.513 is chance. The confidence gap is 0.009 — the model
generalises about as well as it fits. Compare that with the same measurement on a deliberately
overfit model (LAB-13-02 asks you to build one): the gap grows, and the attack starts to
work.

What this teaches:

1. **Overfitting is a privacy bug, not only an accuracy bug.** The defence that costs nothing
   is regularisation, early stopping and more data.
2. **The metric decides the story.** report AUC and TPR at a fixed low FPR (say 1%), not
   accuracy: at 50/50 class balance a useless attack is 50% accurate.
3. **A failed attack is a result.** "We tested membership inference and got AUC 0.51" is a
   sentence for the model card. Omitting it because nothing was found is the mistake.

Defences, in order of cost-effectiveness:

| Defence | Mechanism | Cost |
| :--- | :--- | :--- |
| Regularise / early stop | shrinks the confidence gap | small accuracy loss |
| Train on more data | same | data cost |
| Limit output precision | return labels or coarse scores, not full probabilities | reduced utility |
| Output perturbation | add calibrated noise to confidences | measurable utility loss |
| Differential privacy (DP-SGD) | bounded per-example influence | larger accuracy loss, slower |
| Query auditing / rate limits | makes the attack expensive | operational overhead |

Differential privacy is the only one with a formal guarantee, and the guarantee is only as
good as the privacy budget you actually spend. $(\varepsilon,\delta)$-DP with a large
$\varepsilon$ is a claim, not a protection.

## 3. Model extraction

Model extraction needs no data and no weights — only the ability to query. Sample inputs,
record outputs, fit a surrogate.

```text
  queries 300  surrogate agreement 0.929  true accuracy 0.879
```

With 300 queries against a 1,797-image dataset, a logistic surrogate reproduces 92.9% of the
victim's predictions and reaches 87.9% accuracy itself. The victim's training set was never
touched.

Why this matters beyond IP:

- A stolen model can be attacked **offline**, without rate limits, to build transferable
  adversarial examples.
- Extraction is a precursor to membership inference with unlimited queries.
- For an API business, the model *is* the product.

Defences: rate limits per account, query diversity monitoring, watermarking (embed a
signature behaviour that survives extraction), returning coarse outputs, and — the honest
one — accepting that a public prediction API is extractable in principle and pricing
accordingly.

## 4. Model inversion and training-data extraction

Inversion reconstructs a representative input for a label: given "this is class 3" and
confidence access, optimise an input that maximises that confidence. Against a face
classifier this historically produced recognisable images; against tabular models it
produces plausible feature combinations, which is still disclosure when the features are
sensitive.

Generative models memorise more dramatically. An LLM that has seen a unique string can
emit it verbatim. The M11 module measured this indirectly: a RAG assistant grounded in
retrieved documents answered with exact spans from those documents, which is the mechanism
that makes leakage possible when the index contains confidential material.

Measured in `llm_security.py`, with one confidential record in a five-document index:

```text
  without controls: 1/5 queries leaked (rate 0.20)
  with controls   : 0/5 queries leaked (rate 0.00)
```

The leak came from a query that retrieved the confidential document because it shared
vocabulary with it ("salary reference"). The control that fixed it was not prompt wording —
it was filtering the document out of the index by access control before retrieval, plus PII
redaction on the way out. **Retrieval security is access control on documents, applied
before ranking.**

## 5. Privacy-preserving techniques and their limits

| Technique | What it protects | What it does not |
| :--- | :--- | :--- |
| De-identification | direct identifiers | re-identification by quasi-identifiers |
| k-anonymity | groups of size ≥ k | homogeneity and background-knowledge attacks |
| l-diversity / t-closeness | attribute diversity | still vulnerable to skilled linkage |
| Aggregation | individual values | differencing attacks across queries |
| DP-SGD | training influence | inference from deployed outputs |
| Synthetic data | raw records | leaks the generator if not DP-trained |
| Federated learning | raw data movement | gradients still leak (gradient inversion) |

The pattern: every technique protects a specific channel. Name the channel before claiming
protection.

## 6. What to put in the model card

```text
Privacy
- Training data: synthetic, generated in-script (CC0-1.0); no personal records.
- Membership inference: AUC 0.513 (chance); mean confidence gap train-test 0.009.
- Extraction: not applicable; the model is distributed, not served.
- Retention: no user data stored; no query logs in this teaching build.
```

Every claim is a measurement or an explicit "not applicable" with a reason. "We take privacy
seriously" is not a claim.

## 7. A realistic sequence for a new system

1. Classify the data: personal, sensitive, special category.
2. Decide what the model needs: can you train on aggregates, or on-device?
3. Train with the least capacity that meets the metric; regularise.
4. Measure membership inference against a held-out set you control.
5. Decide the output channel: full probabilities, top-1, or a band.
6. Add rate limits and query monitoring if the model is served.
7. Write the retention policy and the deletion path — including whether retraining is needed
   to honour a deletion request.

That last point is the uncomfortable one: deleting a row from a database does not remove its
influence from a trained model. Machine unlearning is an active research area; in practice,
"retrain without the row" is the only fully reliable answer, and it belongs in the policy.

## Common mistakes

| Mistake | Why it is wrong | Do instead |
| :--- | :--- | :--- |
| Reporting attack accuracy | 50% is chance at balanced classes | report AUC and TPR at low FPR |
| Concluding "no privacy risk" from one failed attack | one attack family | state which attacks you ran |
| De-identification as a complete control | quasi-identifier linkage | k-anonymity plus DP for the model |
| Assuming extraction needs weights | queries suffice | measure agreement with a surrogate |
| Filtering confidential docs at generation | they are already in the context | filter before retrieval |
| Claiming DP without a budget | unbounded epsilon is no guarantee | publish $\varepsilon,\delta$ |

## Exercises

**Beginner.** Run `python security.py` and copy sections 6 and 7. State in one sentence why
the membership attack fails here.

**Beginner.** In `llm_security.py`, remove the confidential-filter line in `rag_leakage` and
rerun. Which query leaks, and which retrieved document caused it?

**Intermediate.** Train the digit model for 60 epochs with no regularisation, then rerun
membership inference. Report the confidence gap and the attack AUC. Plot AUC against epochs.

**Intermediate.** Reduce the extraction query budget to 50, 100 and 200 and report surrogate
agreement each time. How many queries buy 90% agreement?

**Advanced.** Implement DP-SGD for the digit model with a per-example gradient clip and
Gaussian noise, sweep $\varepsilon\in\{1,3,8\}$, and report accuracy against membership
attack AUC.

**Advanced.** Design an access-control scheme for a RAG assistant over 500 mixed
public/confidential documents: where in the pipeline do you enforce it, and what does the
evaluation look like?

## Self-check

1. Why does a well-generalising model resist membership inference?
2. Name two defences against extraction and the cost of each.
3. Why is removing confidential documents after retrieval too late?
4. What does deleting a training row fail to do, and what is the reliable fix?
5. Write the privacy paragraph of a model card for a model you have trained.

## Key terms

**Membership inference**, **model extraction**, **model inversion**, **training-data
extraction**, **memorisation**, **confidence gap**, **DP-SGD**, **differential privacy**,
**k-anonymity**, **quasi-identifier**, **machine unlearning**, **query auditing**.

## Further reading

- Shokri et al. (2017). *Membership Inference Attacks Against Machine Learning Models*.
- Tramèr et al. (2016). *Stealing Machine Learning Models via Prediction APIs*.
- Carlini et al. (2021). *Extracting Training Data from Large Language Models*.
- Abadi et al. (2016). *Deep Learning with Differential Privacy* — DP-SGD.

---

[Previous: L13-02](L13-02-explainability-from-importance-to-counterfactuals.md) ·

---

**Navigation:** [← Previous: L13-02 Explainability: From Importance to Counterfactuals](L13-02-explainability-from-importance-to-counterfactuals.md) · [Module home](../README.md) · [Next: L13-04 Security: Adversarial Examples and Prompt Injection →](L13-04-security-adversarial-examples-and-prompt-injection.md)
