# Laboratories

Laboratories are where the course stops being tidy. Each one gives you a stakeholder, a set of
requirements, data you can obtain and a rubric. You decide what "good enough" means and defend it
with measurements.

!!! info "How the labs are assessed"
    A correct implementation without a baseline, an error analysis or a stated limitation is an
    unfinished piece of engineering. Every lab brief says what evidence earns each band.

## Laboratory method

1. **State the decision.** Write the stakeholder's decision in one sentence.
2. **Audit the inputs.** List what you were given and what you were not.
3. **Build a baseline.** The simplest method that could satisfy the requirement.
4. **Evaluate honestly.** Report the metric, baseline, subgroup results and one failure case.
5. **Write for the stakeholder.** Three actionable sentences plus one limitation.

## Labs by module

| Module | Laboratories | Open |
| :--- | :--- | :--- |
| M01 Introduction | Claim audit; Turing-test conversation | [Module labs](modules/M01-introduction-and-foundations/README.md#module-map) |
| M02 Agents | Intelligent vacuum; campus navigation | [Module labs](modules/M02-intelligent-agents-and-environments/README.md#module-map) |
| M03 Search | Route planning; game agent and timetable | [Module labs](modules/M03-problem-solving-and-search-algorithms/README.md#module-map) |
| M04 Knowledge representation | Expert system; logic inference; Bayesian decision support | [Module labs](modules/M04-knowledge-representation-and-logical-reasoning/README.md#module-map) |
| M05 Uncertainty | Bayesian/fuzzy decision system; network diagnosis | [Module labs](modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/README.md#module-map) |
| M06 Machine learning | Tabular prediction; model comparison; segmentation; leakage hunt | [Module labs](modules/M06-machine-learning-fundamentals/README.md#module-map) |
| M07 Neural networks | Network from scratch; image classifiers; sentiment and transfer | [Module labs](modules/M07-neural-networks-and-deep-learning/README.md#module-map) |
| M08 NLP | Preprocessing; document classification; Urdu/English sentiment and NER | [Module labs](modules/M08-natural-language-processing/README.md#module-map) |
| M09 Computer vision | Image features; CNN classification; detection; segmentation | [Module labs](modules/M09-computer-vision/README.md#module-map) |
| M10 Reinforcement learning | Q-learning; SARSA comparison; DQN CartPole; PPO introduction | [Module labs](modules/M10-reinforcement-learning/README.md#module-map) |
| M11 Generative AI | Prompt engineering; retrieval-augmented assistant; evaluation harness | [Module labs](modules/M11-generative-ai-and-large-language-models/README.md#module-map) |
| M12 Agentic AI | Tool-using agent; agent security and evaluation | [Module labs](modules/M12-ai-agents-and-agentic-systems/README.md#module-map) |
| M13 Responsible AI | Fairness audit; prompt-injection testing | [Module labs](modules/M13-responsible-explainable-secure-ai/README.md#module-map) |
| M14 Applications | Multimodal/graph systems; efficient serving and drift | [Module labs](modules/M14-advanced-ai-applications-and-capstone/README.md#module-map) |

The prerequisite track also contains five short laboratories that build the programming,
mathematics, probability and data-handling skills the module labs assume. Begin at the
[prerequisites page](prerequisites/README.md).

## Starter code and notebooks

Most labs include a starter script under `labs/starters/`, a related notebook, or both. Download
them from the module page or the laboratory brief. The reference implementations are teaching code,
not a substitute for your own experiment: read them, change them and report what happens.

## Reporting template

| Section | Minimum evidence |
| :--- | :--- |
| Decision | One sentence naming the stakeholder and choice |
| Data | Source, licence, size, split and known limitations |
| Method | Baseline, proposed method and why |
| Results | Primary metric, uncertainty and per-group results |
| Failure analysis | At least one error case and its cause |
| Recommendation | What to deploy, change or investigate next |
