# Responsible AI and Security

Resources for M13 and the audit in M14: fairness measurement, explanation, privacy, adversarial
machine learning, and the governance documents that make claims checkable.

[Library index](../README.md) · [Papers](papers-and-surveys.md) · [Agents](ai-agents.md)

---

### Interpretable Machine Learning (2nd edition)
**Christoph Molnar** · 2022
- **URL:** https://christophm.github.io/interpretable-ml-book/
- **Modules:** M13, M14 · **Level:** Intermediate
- **Why:** The practical reference for explanation methods, with the assumptions and failure modes of each stated plainly. Read the chapters on permutation importance, SHAP and LIME before evaluating your own explanation.
- **Access:** Free to read online; print edition sold by the author.

### Fairness and Machine Learning
**Solon Barocas, Moritz Hardt and Arvind Narayanan** · online book
- **URL:** https://fairmlbook.org/
- **Modules:** M13 · **Level:** Advanced
- **Why:** The rigorous treatment of fairness definitions and why they conflict. Chapters 2–3 give the formal grounding for the metrics M13 measures.
- **Access:** Free to read online.

### NIST AI 100-2: Adversarial Machine Learning — Taxonomy and Terminology
**Vassilev, Oprea, Fordyce and Anderson** · NIST, 2025
- **URL:** https://csrc.nist.gov/pubs/ai/100/2/e2025/final
- **Modules:** M13, M14 · **Level:** Intermediate
- **Why:** A standard vocabulary for evasion, poisoning, privacy and misuse attacks, with mitigations and their limits. Use its terms in your risk register so a reviewer can map it to a standard.
- **Access:** Free from NIST.

### NIST AI Risk Management Framework
**National Institute of Standards and Technology** · AI RMF 1.0, 2023
- **URL:** https://www.nist.gov/itl/ai-risk-management-framework
- **Modules:** M13, M14 · **Level:** Intermediate
- **Why:** The governance structure — govern, map, measure, manage — that turns a list of risks into an operating process. The playbook is the practical companion.
- **Access:** Free from NIST.

### UNESCO Recommendation on the Ethics of Artificial Intelligence
**UNESCO** · 2021
- **URL:** https://www.unesco.org/en/artificial-intelligence/recommendation-ethics
- **Modules:** M13 · **Level:** Beginner
- **Why:** The international policy baseline, adopted by member states, covering values, policy areas and accountability. Useful for the "who decides" part of a model card.
- **Access:** Free to read on UNESCO's site.

### Fairlearn
**Microsoft and contributors** · open-source toolkit
- **URL:** https://fairlearn.org/
- **Modules:** M13 · **Level:** Intermediate
- **Why:** Group metrics, disparity dashboards and mitigation algorithms with documented assumptions. The user guide explains what each metric does and does not tell you.
- **Access:** Free; MIT licensed.

### AI Fairness 360
**IBM Research** · open-source toolkit
- **URL:** https://github.com/Trusted-AI/AIF360
- **Modules:** M13 · **Level:** Advanced
- **Why:** A large catalogue of fairness metrics and bias-mitigation algorithms, with explanations of the trade-offs. Useful as a second opinion on a metric you have implemented.
- **Access:** Free; Apache-2.0 licensed.

### Adversarial Robustness Toolbox
**Linux Foundation AI & Data** · open-source library
- **URL:** https://github.com/Trusted-AI/adversarial-robustness-toolbox
- **Modules:** M13 · **Level:** Advanced
- **Why:** Implementations of evasion, poisoning, extraction and inference attacks, plus defences. Use it to check that your own attack implementation is doing what you think.
- **Access:** Open source under the repository's MIT licence.

### SHAP documentation
**Scott Lundberg and contributors** · current release
- **URL:** https://shap.readthedocs.io/
- **Modules:** M13 · **Level:** Intermediate
- **Why:** Explains the algorithm, the explainer variants and the plots, including the cautions about correlated features and the efficiency property your quiz asks about.
- **Access:** Free; MIT licensed.

### Adversarial Robustness: Theory and Practice
**Zico Kolter and Aleksander Madry** · course notes
- **URL:** https://adversarial-ml-tutorial.org/
- **Modules:** M13 · **Level:** Advanced
- **Why:** The mathematics of adversarial examples and robust training, with notebook exercises. Read the first two chapters to understand why FGSM works.
- **Access:** Free to read online.

---

[Library index](../README.md) · [Papers](papers-and-surveys.md) · [Documentation](official-documentation.md)
