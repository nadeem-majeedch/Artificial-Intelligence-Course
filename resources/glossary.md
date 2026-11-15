# Glossary

Every key term in the course, in one sentence. Terms appear here the first time a lesson uses them,
and the module reference at the end of each entry tells you where the idea is taught in full.

Use this page while reading: if a word is unfamiliar, look it up before continuing. Reading past an
unknown term is how a lesson turns into a fog.

**Course home:** [README](../README.md) · **Modules:** [modules/README.md](../modules/README.md) ·
**Books:** [books.md](books.md) · **Documentation index:** [docs/index.md](../docs/index.md)

**Expanded entries:** [detailed glossary](glossary/README.md) — definitions with mathematics,
worked examples and lesson links. **Diagrams:** [concept maps](../docs/CONCEPT-MAPS.md).

## A

- **A\* search** — best-first search that orders nodes by cost so far plus estimated cost to the goal; optimal when the heuristic never overestimates. *(M03)*
- **Accuracy** — the proportion of predictions that are correct; misleading when classes are imbalanced. *(M06)*
- **Action allowlist** — the set of actions an agent is permitted to take; anything outside it is refused regardless of what the prompt asks for. *(M13)*
- **Action value** — The expected return from taking action $a$ in state $s$ and then acting well. *(M10)*
- **Actuator** — The part of an agent that changes the environment. *(M02)*
- **Adversarial example** — an input perturbed slightly to change a model's prediction while looking unchanged to a person. *(M13)*
- **Agent evaluation** — Reporting task success, steps, tool-error rate and cost separately; a single aggregate score hides the failure that must be fixed. *(M12)* [Lesson](../modules/M12-ai-agents-and-agentic-systems/lessons/L12-06-mcp-security-evaluation-and-reliable-execution.md)
- **Agent loop** — The cycle of reasoning, acting, observing the result and deciding again. *(M12)*
- **Agent memory** — Two tiers: bounded working memory (notes, recent observations) and an external store queried on demand; the transcript is neither. *(M12)* [Lesson](../modules/M12-ai-agents-and-agentic-systems/lessons/L12-03-planning-memory-and-workflow-orchestration.md)
- **Agent orchestration** — Deciding the order and ownership of steps across agents and the shared state, with per-step postconditions, retries and one owner per subtask. *(M12)* [Lesson](../modules/M12-ai-agents-and-agentic-systems/lessons/L12-03-planning-memory-and-workflow-orchestration.md)
- **AI winter** — A period when funding and interest in AI collapsed after promises outran results. *(M01)*
- **Audit (AI)** — a claim-by-claim check that each required artefact exists, contains the required evidence and is current. *(M13)*
- **Automation bias** — the tendency of human reviewers to accept a system's suggestion instead of checking it. *(M13)*
- **Activation function** — an elementwise nonlinear function applied to a layer's output; without one, a deep network collapses into a single linear map. *(M07)*
- **Admissible heuristic** — a heuristic that never overestimates the true remaining cost, which is exactly what preserves A\*'s optimality. *(M03)*
- **Adapter** — a small set of newly trained weights attached to a frozen pretrained model, so one base model can serve many tasks. *(M11, M12)*
- **Agent** — anything that perceives its environment through sensors and acts on it through actuators. *(M02)*
- **Alpha–beta pruning** — discarding game-tree branches that cannot change the final decision, giving the same answer for less work. *(M03)*
- **Anomaly detection** — identifying observations that are unusual relative to the rest of the data, often without labels for the abnormal class. *(M06)*
- **Attention** — a mechanism that weights parts of the input by relevance when producing each output; the core of the transformer. *(M07, M11)*
- **AUC (area under the ROC curve)** — the probability that a randomly chosen positive is scored above a randomly chosen negative; a threshold-free measure of ranking quality. *(M06)*
- **Autoregressive model** — a model that generates a sequence one element at a time, each conditioned on what it has already produced. *(M11)*
- **Autoencoder** — a network trained to reconstruct its own input through a narrow bottleneck, used for compression, representation learning and anomaly scoring. *(M07)*
- **Average precision (AP)** — the area under the precision–recall curve, preferred to AUC when positives are rare. *(M06)*
## B

- **Backward chaining** — Working backwards from a goal to the facts that would support it. *(M04)*
- **Bag of words** — Representing a document by counts of its vocabulary words, ignoring order. *(M08)*
- **Bellman equation** — The recursive relationship between a state's value and its successors' values; the basis of policy evaluation and value iteration. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-02-value-based-reinforcement-learning.md)
- **BM25** — a lexical ranking function scoring documents by term overlap with saturation and length normalisation; strong on rare exact terms. *(M11)*
- **Backpropagation** — applying the chain rule backwards through a network to compute the gradient of the loss with respect to every parameter. *(M07)*
- **Backdoor** — a model behaviour learned from a poisoned training set that triggers only on a specific pattern and is invisible on clean evaluation. *(M13)*
- **Adversarial training** — training on adversarially perturbed examples so the model is robust in a neighbourhood, usually at a cost in clean accuracy. *(M13, M14)*
- **Adverse action reason** — the factor that actually determined a denial, which must be the binding constraint rather than the most salient feature. *(M14)*
- **Bagging** — training many models on bootstrap resamples and averaging them, which reduces variance. *(M06)*
- **Batch normalisation** — normalising a layer's activations per mini-batch (with running estimates at inference) to stabilise and speed up training. *(M07)*
- **Baseline** — the simple reference result a model must beat before its complexity is justified. *(M06)*
- **Batch** — the subset of training examples used for one parameter update. *(M07)*
- **Bayes' rule** — P(A | B) = P(B | A)·P(A) / P(B), which converts a likelihood into a posterior belief. *(M05)*
- **Bayesian network** — a directed acyclic graph of variables whose structure encodes conditional independence. *(M05)*
- **Bias (statistical)** — systematic error from a model too simple for the pattern; the counterpart of variance. *(M06)*
- **Bias (social)** — a systematic disadvantage a system produces for a group of people; a different thing from statistical bias. *(M13)*
- **Bias–variance trade-off** — the tension between a model too simple to capture the pattern and one too flexible to ignore the noise; expected error is their sum plus irreducible noise. *(M06)*
- **Boosting** — combining weak learners sequentially, each one correcting the errors of those before it. *(M06)*
- **Breadth-first search** — exploring every node at depth *d* before any at depth *d + 1*; complete and cost-optimal for unit costs, but memory-hungry. *(M03)*
## C

- **Catastrophic forgetting** — losing previously learned capability when a model is trained on new data, especially after aggressive fine-tuning. *(M07, M11)*
- **Causal mask** — an attention mask that prevents a position from attending to later positions, required when generating left to right. *(M07, M11)*
- **Causal masking** — Setting the attention logits for future positions to $-\infty$ so a language model cannot see tokens it is meant to predict. *(M08)* [Lesson](../modules/M08-natural-language-processing/lessons/L08-06-sequence-models-attention-and-transformers.md)
- **Chain-of-thought prompting** — asking a model to produce intermediate reasoning steps before its answer; helpful for capable models on decomposable tasks, harmful to span metrics. *(M11)*
- **Chain rule** — the rule for differentiating composed functions; the mathematical engine inside backpropagation. *(P02)*
- **Batch inference** — scoring a whole dataset at once and writing results to a table, trading freshness for throughput. *(M14)*
- **Calibration (group)** — agreement between predicted probabilities and observed frequencies within each group; overall calibration can hide per-group miscalibration. *(M13)*
- **Canary deployment** — routing a small share of traffic to a new model with automatic rollback on a metric breach. *(M14)*
- **Class imbalance** — a classification problem where one class is far rarer than the other, so accuracy favours the majority class. *(M06)*
- **Classification** — predicting a discrete label. *(M06)*
- **Clustering** — grouping unlabelled examples by similarity. *(M06)*
- **Conditional independence** — Two variables are independent given a third when knowing the third makes the first uninformative about the second. *(M05)*
- **Confusion matrix** — a table of predicted against actual classes, from which most classification metrics follow. *(M06)*
- **Connectionist AI** — The approach that builds intelligence from many simple learned units rather than explicit rules. *(M01)*
- **Constraint satisfaction problem** — A problem defined by variables, domains and constraints, solved by assigning values that satisfy every constraint; map colouring and timetabling are the standard examples. *(M03)* [Lesson](../modules/M03-problem-solving-and-search-algorithms/lessons/L03-06-constraint-satisfaction-problems.md)
- **Constraint satisfaction problem (CSP)** — a problem defined by variables, their domains and constraints, solved by search with constraint propagation. *(M03)*
- **Context window** — the maximum amount of text a language model can attend to at once, covering prompt plus generated tokens. *(M11)*
- **Cosine similarity** — the cosine of the angle between two vectors; on normalised embeddings it is a cheap semantic similarity score. *(M11)*
- **Chunking** — splitting documents into passages small enough to embed and retrieve, usually with overlap so sentences at boundaries survive. *(M11)*
- **Convolution** — sliding a small learned filter across an input to detect a local pattern. *(M07, M09)*
- **Convolutional neural network (CNN)** — a network of convolution, pooling and dense layers, suited to grid-structured data such as images. *(M07, M09)*
- **Counterfactual explanation** — the nearest input change that would reverse a decision, judged by proximity, actionability and plausibility. *(M13)*
- **Cross-entropy** — a loss measuring the difference between a predicted probability distribution and the true one. *(M07)*
- **Cross-validation** — repeatedly splitting data into training and validation folds to estimate generalisation. *(M06)*
## D

- **Data leakage** — information from outside the training set influencing training, so measured performance is inflated. *(M06)*
- **Data poisoning** — corrupting part of a training set so the fitted model is degraded or directed; a small fraction of labels can be enough. *(M13)*
- **Datasheet** — documentation of a dataset's motivation, composition, collection, preprocessing, known biases, licence and maintenance. *(M13)*
- **Default deny** — the policy that an agent may take no external or destructive action unless it was explicitly granted and approved. *(M13)*
- **Demographic parity** — the fairness definition requiring equal positive-decision rates across groups, regardless of qualification. *(M13)*
- **Depth-first search** — Following one branch as far as possible before backtracking. *(M03)*
- **Differential privacy** — a formal guarantee bounding any single record's influence on an output, parameterised by a privacy budget. *(M13)*
- **Disparate impact** — The ratio of one group's selection rate to another's. *(M13)*
- **Disparate impact ratio** — the smallest group selection rate divided by the largest; below 0.80 is the screening heuristic known as the 80% rule. *(M13)*
- **Concept drift** — a change in the relationship between inputs and target, so the same input should now produce a different output. *(M14)*
- **Contrastive learning** — training two encoders so matching pairs land close in a shared space and non-matching pairs land far apart. *(M14)*
- **Coverage (prediction interval)** — the fraction of realised outcomes inside the stated interval; a nominal 80% interval covering 66% is mis-specified. *(M14)*
- **Decision tree** — a model that partitions the input space through a sequence of threshold tests. *(M06)*
- **Deep learning** — machine learning with neural networks of many layers. *(M07)*
- **Diffusion model** — a generative model that learns to reverse a gradual noising process. *(M11)*
- **Discount factor (γ)** — the weight applied to future rewards when computing a return, trading immediate against long-term value. *(M10)*
- **Domain** — the set of values a variable may take; in a CSP, its allowed range. *(M03)*
- **DPO (direct preference optimisation)** — aligning a model to preferred outputs with a classification-style loss instead of a separate reward model. *(M11)*
- **Distillation** — training a small student on a larger teacher's soft outputs, useful when the student is capacity-limited relative to the task. *(M14)*
- **Drift** — A change in the data or the input–output relationship that degrades a deployed model. *(M14)*
- **Dropout** — randomly zeroing activations during training to discourage co-adaptation and reduce overfitting. *(M07)*
## E

- **Edge AI** — inference on a constrained device, where memory, power and the absence of a GPU shape the model more than accuracy does. *(M14)*
- **ELBO (evidence lower bound)** — a tractable lower bound on log-likelihood used to train latent-variable models such as the VAE. *(M11)*
- **Elimination ordering** — The sequence in which hidden variables are summed out; correctness is independent of it, cost is not, because it fixes the size of the largest intermediate factor. *(M05)* [Lesson](../modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-06-variable-elimination-and-factor-algebra.md)
- **Embedding** — a dense learned vector representation of a discrete item such as a word or a document. *(M06, M08, M11)*
- **Ensemble** — a model composed of several models whose predictions are combined. *(M06)*
- **Entailment** — the relation in which a conclusion follows necessarily from the premises. *(M04)*
- **Environment** — everything an agent perceives and acts upon, characterised by its observability, determinism and dynamics. *(M02)*
- **Epoch** — one complete pass over the training data. *(M07)*
- **Equal opportunity** — the fairness definition requiring equal true-positive rates across groups, so qualified people are selected at the same rate. *(M13)*
- **Equalised odds** — equal opportunity extended to false-positive rates, so both kinds of error are shared. *(M13)*
- **Evasion attack** — an attack at inference time that perturbs the input to obtain a wrong output, without touching the model. *(M13)*
- **Efficiency property** — the requirement that Shapley values sum to the prediction minus the baseline; the cheapest check that a SHAP implementation is correct. *(M13)*
- **Exact match (EM)** — the fraction of predictions identical to the gold answer after normalisation; harsh to verbosity. *(M11)*
- **Expected utility** — the probability-weighted average utility of the outcomes of an action. *(M05)*
- **Experience replay** — Storing transitions and sampling random minibatches so that consecutive, correlated samples stop dominating the gradient. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-04-deep-reinforcement-learning.md)
- **Expert system** — A knowledge base of hand-written rules plus an inference engine and an explanation facility; auditable and expensive to maintain. *(M04)* [Lesson](../modules/M04-knowledge-representation-and-logical-reasoning/lessons/L04-07-rule-based-and-expert-systems.md)
- **Explainability** — Producing a human-usable account of why a model produced an output. *(M13)*
- **Exploration–exploitation** — The choice between trying unknown actions and using the best known one. *(M10)*
- **Exploration–exploitation trade-off** — choosing between trying actions whose value is unknown and using actions known to work. *(M10)*
## F

- **F1** — The harmonic mean of precision and recall. *(M06)*
- **F1 score** — the harmonic mean of precision and recall. *(M06)*
- **Factor** — A function from an assignment of a set of variables to a non-negative number; a conditional probability table is a factor, and exact inference is arithmetic on factors. *(M05)* [Lesson](../modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-06-variable-elimination-and-factor-algebra.md)
- **Fairness** — Acceptable distribution of outcomes and errors across groups of people. *(M13)*
- **Feature** — an input variable used by a model. *(M06)*
- **Fast gradient sign method (FGSM)** — a one-step adversarial attack that perturbs each pixel by the sign of the loss gradient times epsilon. *(M13)*
- **Feature importance** — a global summary of how much a model relies on each input, by permutation, impurity or Shapley attribution. *(M13)*
- **Feature engineering** — constructing informative inputs from raw data. *(M06)*
- **FedAvg** — federated averaging: clients train locally and the server averages their weights each round, never seeing raw data. *(M14)*
- **Federated learning** — training across data holders without centralising their data, at the cost of communication and non-IID instability. *(M14)*
- **Few-shot prompting** — placing a small number of solved examples in the prompt; conditions the model without changing weights. *(M11)*
- **Fidelity (explanation)** — how well a surrogate explanation reproduces the model's behaviour in the neighbourhood it describes, usually a local R-squared. *(M13)*
- **Fine-tuning** — continuing the training of a pretrained model on a smaller, task-specific dataset. *(M07, M11)*
- **First-order logic** — Logic with objects, relations and quantifiers, rather than bare propositions. *(M04)*
- **Forward chaining** — deriving new facts from rules and known facts until nothing new follows. *(M04)*
- **Function approximation** — representing a value function or policy with a parameterised function instead of a lookup table. *(M10)*
- **Fuzzy logic** — reasoning with degrees of membership rather than true or false, for concepts that are genuinely vague. *(M05)*
## G

- **General AI** — A system that can perform any intellectual task a person can, including transferring skill to unfamiliar problems. *(M01)*
- **Generalisation** — performance on data the model has not seen; the entire point of learning. *(M06)*
- **Governance** — The rules, owners, reviews and records that keep an AI system accountable. *(M13)*
- **Gradient boosting** — An ensemble that adds trees sequentially, each fitted to the residual errors of the current model. *(M06)*
- **Gradient check** — Comparing an analytic gradient with a finite-difference estimate to catch backpropagation bugs. *(M07)*
- **Guardrail** — a runtime check that blocks or modifies an AI system's action before it causes harm, independent of what the model was asked to do. *(M12, M13)*
- **Generative adversarial network (GAN)** — a generator trained against a discriminator that learns to tell real data from generated data. *(M11)*
- **Gradient** — the vector of partial derivatives, pointing in the direction of steepest increase. *(P02)*
- **GRU (gated recurrent unit)** — a recurrent unit with reset and update gates; a lighter alternative to the LSTM. *(M07)*
- **Gradient descent** — iteratively stepping against the gradient to reduce a loss. *(P02, M07)*
- **Ground truth** — the trusted reference labels against which predictions are compared. *(M06)*
- **Grounding** — the degree to which an answer is supported by the retrieved context rather than generated freely. *(M11)*
## H

- **Hallucination** — fluent, confident generative output that is not supported by any evidence. *(M11)*
- **Heuristic** — a problem-specific estimate used to guide search. *(M03)*
- **Heuristic function** — An estimate $h(n)$ of the cost from node $n$ to the goal; admissible if it never overestimates, which is what preserves A\*'s optimality. *(M03)* [Lesson](../modules/M03-problem-solving-and-search-algorithms/lessons/L03-03-informed-search-greedy-and-a-star.md)
- **Hidden Markov model (HMM)** — a model in which observable outputs are produced by hidden states that follow a Markov chain. *(M05)*
- **Hold-out split** — Dividing data once into training, validation and test sets. *(M06)*
- **Human-in-the-loop** — A design in which a person approves or reviews consequential agent actions. *(M12)*
- **Hybrid AI** — A system that combines learned components with explicit rules, search or symbolic structure. *(M01)*
- **Hybrid retrieval** — combining dense and lexical retrieval scores, usually after normalising them, to cover both meaning and exact terms. *(M11)*
- **Graph neural network (GNN)** — a network that updates each node's representation by aggregating its neighbours', so the graph carries information the features do not. *(M14)*
- **Homophily** — the fraction of edges connecting nodes of the same class; below roughly 0.5, message passing mixes classes and can hurt. *(M14)*
- **Hybrid system** — a learned component inside an explicit boundary, such as a model that ranks while a rule decides. *(M14)*
- **Hyperparameter** — a setting chosen before training that controls how learning happens. *(M06)*
## I

- **Human oversight** — a control with a stated trigger, information for the reviewer, override authority, a time budget and a route for appeal. *(M13)*
- **Image classification** — Assigning a label to a whole image. *(M09)*
- **Imputation** — filling missing values with an estimate such as a mean, median or model prediction. *(M06)*
- **In-context learning** — Learning a task from examples placed in the prompt, with no weight update. *(M11)*
- **Inference (logical)** — deriving conclusions that follow from premises. *(M04)*
- **Inference (probabilistic)** — computing a posterior or a marginal from a probabilistic model. *(M05)*
- **Information gain** — the reduction in entropy obtained by splitting on a feature. *(M06)*
- **InfoNCE** — the contrastive loss that treats each paired example as the positive and the rest of the batch as negatives. *(M14)*
- **Integrated gradients** — an attribution that averages gradients along a path from a baseline to the input; a sensitivity measure, not a reason. *(M14)*
- **Instruction tuning** — supervised fine-tuning on instruction/response pairs so a base model follows directions rather than continuing text. *(M11)*
- **Instance-based learning** — prediction by comparing a new example with stored examples, as in k-nearest neighbours. *(M06)*
- **Interpretability** — the degree to which a person can understand why a model produced a particular output. *(M13)*
- **Intersection over Union** — The overlap between a predicted and a true region, divided by their union. *(M09)*
## K

- **k-means** — clustering that alternates assigning points to the nearest centre and moving each centre to the mean of its points, minimising within-cluster variance. *(M06)*
- **k-nearest neighbours (k-NN)** — predicting from the labels of the *k* most similar stored examples. *(M06)*
- **Knowledge base** — A set of sentences a reasoning system treats as true. *(M04)*
- **KV cache** — stored attention keys and values from previous tokens, so generation does not recompute them at every step. *(M11)*
- **Knowledge distillation** — training a small student model to reproduce a larger teacher's outputs, trading a little accuracy for much lower serving cost. *(M14)*
- **Knowledge graph** — a graph of entities and typed relations used as structured, queryable knowledge. *(M04)*
## L

- **Label** — the target value a supervised model is trained to predict. *(M06)*
- **Label bias** — bias introduced by the labelling policy itself, so equally qualified people receive different labels; reweighting cannot repair it. *(M13)*
- **Large language model (LLM)** — a transformer trained on large text corpora to predict the next token. *(M11)*
- **Latent space** — A compressed representation space in which a generative model operates. *(M11)*
- **Latent variable** — an unobserved variable that is inferred from observed data. *(M05)*
- **Latency budget** — the allocation of a request's time across network, features, inference and headroom, decided before choosing a model. *(M14)*
- **Learning rate** — the step size used in gradient-based training. *(M07)*
- **Lemmatization** — Reducing a word to its dictionary form using morphology, so *was* becomes *be*; slower and more accurate than stemming. *(M08)* [Lesson](../modules/M08-natural-language-processing/lessons/L08-02-preprocessing-tokenization-stemming-lemmatization.md)
- **LIME** — a local explanation that fits a weighted sparse linear surrogate to the model around one instance, reported with its fidelity. *(M13)*
- **Linear regression** — Fitting a line (or hyperplane) that minimises squared error. *(M06)*
- **Local search** — optimisation that moves between neighbouring solutions without remembering the path taken. *(M03)*
- **Log-odds** — the log of the odds, log(p/(1-p)); logistic regression is linear in the log-odds. *(M06)*
- **Logistic regression** — a linear model whose output is passed through a sigmoid to produce a probability. *(M06)*
- **LoRA (low-rank adaptation)** — parameter-efficient fine-tuning that learns small low-rank matrices instead of updating every weight. *(M11)*
- **Loss function** — the quantity that training minimises. *(M06)*
## M

- **Machine learning** — methods that improve performance on a task through experience, usually data. *(M06)*
- **Markov decision process** — A tuple $(S, A, P, R, \gamma)$: states, actions, transition probabilities, rewards and a discount; the formal object every RL algorithm optimises against. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-01-foundations-of-reinforcement-learning.md)
- **Markov decision process (MDP)** — a formal model of sequential decision making with states, actions, transition probabilities and rewards. *(M05, M10)*
- **Maximum likelihood estimation** — choosing the parameters that make the observed data most probable. *(P03)*
- **Membership function** — A function $\mu_A: X \to [0,1]$ giving the degree to which a value belongs to a fuzzy set; a temperature of 24 °C can be "warm to 0.6" and "hot to 0.1". *(M05)* [Lesson](../modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-04-fuzzy-sets-membership-functions-and-operations.md)
- **Membership inference** — an attack that decides whether a specific record was in the training set, exploiting the model's confidence gap. *(M13)*
- **Memory** — Stored state an agent carries between steps or sessions. *(M12)*
- **Mini-batch** — a small batch used for each update in stochastic gradient descent. *(M07)*
- **Model** — a parameterised function mapping inputs to outputs, fitted from data. *(M06)*
- **Message passing** — the aggregation step in a GNN, where each node combines its neighbours' representations with its own. *(M14)*
- **MLOps** — the practices that make a model reproducible and operable: versioned data and code, a registry, staged rollout and rollback. *(M14)*
- **Model Context Protocol** — An open protocol standardising how a host exposes tools, resources and prompts to a model; it solves integration, not trust — a server is still code to audit. *(M12)* [Lesson](../modules/M12-ai-agents-and-agentic-systems/lessons/L12-06-mcp-security-evaluation-and-reliable-execution.md)
- **Model registry** — the record of each model version's metrics, owner, approval status and deployment target. *(M14)*
- **Model card** — a short document recording a model's purpose, data, metrics, subgroup performance, limitations and monitoring plan. *(M06)*
- **Mode collapse** — a generator that produces a narrow set of outputs and stops covering the data distribution. *(M11)*
- **Model extraction** — reconstructing a functionally similar model from its input–output behaviour alone, without weights or training data. *(M13)*
- **Model inversion** — reconstructing a representative input for a target output or class from model access. *(M13)*
- **Model serving** — Running a trained model behind an interface that answers requests. *(M14)*
- **Monitoring** — Continuously measuring a deployed system's inputs, outputs and outcomes. *(M14)*
- **Monte Carlo method** — estimating a quantity by repeated random sampling. *(M10)*
- **Multi-armed bandit** — A one-state decision problem: choose among actions with unknown reward distributions to maximise total reward. *(M10)*
- **Multi-head attention** — running several attention operations in parallel on projected subspaces and concatenating their outputs. *(M07, M11)*
- **Multi-agent system** — several interacting agents whose outcomes depend on each other's actions. *(M12)*
- **Multilayer perceptron** — A feed-forward network with one or more hidden layers of nonlinear units. *(M07)*
## N

- **Named entity recognition** — Finding and classifying names of people, organisations, places and similar entities in text. *(M08)*
- **Narrow AI** — A system that performs one task or a narrow family of tasks well. *(M01)*
- **Negative transfer** — pretrained features that hurt performance because the source and target tasks differ too much. *(M07)*
- **Naïve Bayes** — a classifier that assumes features are conditionally independent given the class. *(M06)*
- **nDCG (normalised discounted cumulative gain)** — a ranking score that discounts relevant items by their position and normalises by the ideal ordering. *(M11)*
- **Natural language processing (NLP)** — the computational treatment of human language. *(M08)*
- **Neural network** — a composition of parameterised layers trained by gradient descent. *(M07)*
- **Non-maximum suppression** — Keeping the highest-scoring detection and deleting boxes that overlap it above a threshold, so one object yields one prediction. *(M09)* [Lesson](../modules/M09-computer-vision/lessons/L09-04-object-detection.md)
- **Normalisation** — rescaling inputs or activations to a standard range or distribution. *(M06, M07)*
## O

- **Object detection** — Locating objects in an image with bounding boxes and class labels. *(M09)*
- **One-hot encoding** — representing a categorical value as a vector with a single 1 and the rest 0. *(M06)*
- **Online inference** — Scoring a single request at the moment it arrives. *(M14)*
- **Ontology** — an explicit specification of the concepts and relations in a domain. *(M04)*
- **Neuro-symbolic AI** — systems that combine learned components with explicit rules or logic, usually for compliance or interpretability the model alone cannot provide. *(M14)*
- **Non-IID** — data whose distribution differs across clients, the normal case in federated learning and the reason averaging can be slow or unfair. *(M14)*
- **Optimiser** — The rule that turns gradients into parameter updates. *(M07)*
- **Orchestration** — The component that decides which agent or tool runs next, and with what input. *(M12)*
- **Oversmoothing** — the collapse of node representations toward a common vector after many message-passing layers, destroying class separability. *(M14)*
- **Overfitting** — fitting noise in the training data, so performance degrades on new data. *(M06)*
## P

- **Parameter** — a value learned from data during training. *(M06)*
- **Partial dependence** — the average model output as one feature is swept across its range, assuming the other features are independent of it. *(M13)*
- **PCA** — Projecting data onto the directions of greatest variance. *(M06)*
- **PEAS** — Performance measure, Environment, Actuators, Sensors: the template for specifying an agent's task. *(M02)*
- **Percept** — One unit of sensory input an agent receives at a moment in time. *(M02)*
- **Perceptron** — the earliest trainable linear classifier, and the ancestor of the neural network. *(M07)*
- **Permutation importance** — the drop in a metric when one feature is shuffled, repeated and averaged; model-agnostic but splits credit between correlated features. *(M13)*
- **Perplexity** — the exponential of mean negative log-likelihood per token; lower means the model finds the text more predictable. *(M11)*
- **Planning** — Decomposing a goal into ordered steps before acting. *(M12)*
- **Pointwise mutual information** — $\mathrm{PMI}(w,c)=\log\frac{P(w,c)}{P(w)P(c)}$, clipped at zero (PPMI) before factorisation — the classical way to turn co-occurrence counts into usable embeddings. *(M08)* [Lesson](../modules/M08-natural-language-processing/lessons/L08-04-word-embeddings-word2vec-and-similarity.md)
- **Policy gradient** — Ascending $\nabla_\theta \mathbb{E}[\log\pi_\theta(a\mid s)G_t]$: optimising the policy directly instead of deriving it from values. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-04-deep-reinforcement-learning.md)
- **Precision and recall** — Of the items flagged, the share that were right (precision); of the real positives, the share that were found (recall). *(M06)*
- **Prior and posterior** — The belief before seeing evidence, and the belief after. *(M05)*
- **Projected gradient descent (PGD)** — a multi-step adversarial attack that re-projects the perturbation into the epsilon-ball after each step. *(M13)*
- **Policy** — a mapping from states to actions. *(M10)*
- **Pooling** — downsampling a feature map by summarising local windows, usually with a maximum or mean. *(M07, M09)*
- **Positional encoding** — information added to token embeddings so a permutation-invariant attention mechanism can use order. *(M07)*
- **Population stability index (PSI)** — a symmetric divergence between a reference and a current feature distribution; stable below 0.10, alerting above 0.25. *(M14)*
- **Precision** — of the items predicted positive, the fraction that actually are positive. *(M06)*
- **Pretraining** — training a model on a large general task before adapting it to a specific one. *(M07)*
- **Prompt** — the input text that conditions a language model's output. *(M11)*
- **Prompt engineering** — Designing the instructions and context given to a model to obtain a reliable output. *(M11)*
- **Prompt injection** — an attack in which untrusted text causes a model to follow the attacker's instructions instead of the user's. *(M12, M13)*
- **Prompt template** — a parameterised prompt with fixed role, evidence, constraints and output format, versioned and evaluated like code. *(M11)*
- **Propositional logic** — Logic whose atoms are true/false propositions combined with and, or, not and implication. *(M04)*
- **Proxy variable** — a feature that stands in for a protected attribute, reproducing its disparity while appearing neutral. *(M13)*
- **Pruning** — removing parts of a model or a search tree that cannot affect the result. *(M03, M06)*
## Q

- **QLoRA** — fine-tuning adapters on a base model whose frozen weights are stored in 4-bit, making large-model tuning fit on one GPU. *(M11)*
- **Q-learning** — a model-free reinforcement-learning method that learns the value of taking an action in a state. *(M10)*
- **Quantisation** — storing weights in fewer bits (for example int8) to shrink a model and its memory use, usually at some accuracy cost. *(M11)*

## R

- **Random forest** — Many decision trees trained on bootstrap samples and random feature subsets, averaged. *(M06)*
- **Rational agent** — An agent that chooses the action expected to maximise its performance measure given what it knows. *(M02)*
- **Reconstruction error** — the difference between an autoencoder's output and its input; the anomaly score in a reconstruction-based detector. *(M07)*
- **Recourse** — the practical route by which an affected person can challenge or reverse a system's decision. *(M13)*
- **Recurrent neural network (RNN)** — a network whose hidden state is fed back at each time step, giving it memory over sequences. *(M07)*
- **Reproducibility** — The ability to obtain the same result from the same code, data and configuration. *(M14)*
- **Return** — The discounted sum of rewards from a time step onward. *(M10)*
- **Reward hacking** — optimising the measured reward in a way that satisfies the letter of the objective while defeating its purpose. *(M10, M11)*
- **Recall** — of the items that are actually positive, the fraction the model finds. *(M06)*
- **Regularisation strength** — the coefficient that trades training fit against a penalty on parameter size. *(M06)*
- **Regression** — predicting a continuous value. *(M06)*
- **Reranking** — rescoring a shortlist of retrieved passages with a more expensive model that sees the query and passage together. *(M11)*
- **Regularisation** — penalising model complexity to improve generalisation. *(M06)*
- **Reinforcement learning (RL)** — learning a policy from rewards obtained by interacting with an environment. *(M10)*
- **ReLU** — the activation max(0, x): cheap, and effective at limiting vanishing gradients. *(M07)*
- **Residual risk** — the risk remaining after controls are in place, which must be accepted by a named person with a review date. *(M13)*
- **Risk register** — the scored list of a system's risks with owners, controls and residual levels, used as a release gate. *(M13)*
- **Resolution** — a sound and complete inference rule used in automated theorem proving. *(M04)*
- **Retrieval-augmented generation (RAG)** — generating an answer conditioned on documents retrieved for the query. *(M11)*
- **Research prototype** — a system evaluated on one dataset with an offline split, which is not evidence of production or high-stakes reliability. *(M14)*
- **ROC and AUC** — The curve of true-positive rate against false-positive rate as the threshold moves, and the area under it. *(M06)*
- **Rollback** — reverting a deployment to the previous version, which requires that version to still exist and be addressable. *(M14)*
- **Rolling-origin backtest** — evaluating a forecaster by repeatedly training up to a cutoff and predicting the next window forward in time. *(M14)*
- **Rule gate** — a symbolic constraint that filters or vetoes a model's output, giving a compliance guarantee the model alone cannot. *(M14)*
- **Reweighing** — a pre-processing fairness technique that reweights (group, label) cells to equalise their influence; it cannot fix label bias. *(M13)*
- **Reward** — the scalar feedback that a reinforcement-learning agent seeks to maximise. *(M10)*
- **Risk acceptance** — the recorded decision by a named owner to tolerate a residual risk, with conditions and a review date. *(M13)*
- **RLHF (reinforcement learning from human feedback)** — using human preference judgements to align a language model's behaviour. *(M11)*
- **ROC curve** — a plot of true-positive rate against false-positive rate across decision thresholds. *(M06)*
- **ROUGE-L** — a summary-quality score based on the longest common subsequence of tokens between output and reference. *(M11)*
## S

- **SARSA** — On-policy TD control whose target uses the action the behaviour policy actually takes next; it learns the value of the exploring policy. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-03-temporal-difference-learning.md)
- **Search space (state space)** — the set of states reachable from the initial state through legal actions. *(M03)*
- **Selection rate** — the fraction of a group receiving a positive decision; the quantity behind demographic parity and disparate impact. *(M13)*
- **Shadow deployment** — Running a new model alongside the live one without using its output. *(M14)*
- **Soft labels** — a teacher's probability distribution used as a training target, carrying class-similarity information a hard label lacks. *(M14)*
- **Sparsity** — the fraction of weights that are exactly zero; it saves storage only unless the hardware or format can skip the zeros. *(M14)*
- **Self-attention** — attention of a sequence to itself, letting each position weigh every other position. *(M07, M11)*
- **Semantic segmentation** — labelling every pixel of an image with a class. *(M09)*
- **Shapley value** — a feature attribution from cooperative game theory that satisfies efficiency, symmetry, dummy and additivity. *(M13)*
- **Sigmoid** — the logistic function, mapping any real number into the interval (0, 1). *(M06)*
- **Silhouette** — a clustering quality score comparing each point's mean distance to its own cluster with its distance to the nearest other cluster; ranges from −1 to 1. *(M06)*
- **Softmax** — turning a vector of scores into a probability distribution. *(M06, M07)*
- **Stability (explanation)** — agreement of an explanation across reruns with different seeds; a reportable property of any sampling-based method. *(M13)*
- **Standardisation** — rescaling a feature to zero mean and unit variance. *(M06)*
- **State** — a representation of the situation relevant to deciding what to do next. *(M02, M03)*
- **State space** — The set of configurations a problem can be in, with the moves that connect them. *(M03)*
- **Stemming and lemmatisation** — Reducing words to a common root (stemming) or dictionary form (lemmatisation). *(M08)*
- **Stochastic** — involving randomness. *(M02)*
- **Supervised learning** — learning from labelled examples. *(M06)*
- **Supply-chain risk** — untrusted datasets, checkpoints, adapters or packages introducing poisoning or backdoors before the model is used. *(M13)*
- **Symbolic AI** — approaches that represent knowledge explicitly as symbols and rules. *(M01, M04)*

- **Support vector machine (SVM)** — a classifier that maximises the margin between classes, optionally using kernels. *(M06)*
## T

- **Target network** — A periodically refreshed copy of the Q-network used to compute bootstrap targets, so the target does not move with every update. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-04-deep-reinforcement-learning.md)
- **Temperature** — a sampling parameter controlling how random a language model's token choices are. *(M11)*
- **Temporal difference** — Learning a value estimate from a later value estimate instead of waiting for the true return. *(M10)*
- **Temporal-difference (TD) learning** — updating value estimates from the difference between successive estimates. *(M10)*
- **Temporal-difference learning** — Learning a value from a one-step reward plus the current estimate of the next state's value — biased but far lower variance than Monte Carlo. *(M10)* [Lesson](../modules/M10-reinforcement-learning/lessons/L10-03-temporal-difference-learning.md)
- **Tensor** — a multi-dimensional array; the basic data structure of deep learning. *(M07)*
- **TF-IDF** — Weighting a term by how often it appears in a document and how rare it is across the corpus. *(M08)*
- **Throughput and latency budget** — The requests a system handles per second, and the time one request is allowed to take. *(M14)*
- **Tokenization** — Splitting text into the units a model sees — words, subwords or characters; the choice fixes the vocabulary and the sequence length. *(M08)* [Lesson](../modules/M08-natural-language-processing/lessons/L08-02-preprocessing-tokenization-stemming-lemmatization.md)
- **Tool calling** — A model emitting a structured request — tool name plus JSON arguments — that the host validates, authorises and executes; the model never runs code itself. *(M12)* [Lesson](../modules/M12-ai-agents-and-agentic-systems/lessons/L12-02-llm-agents-tool-calling-and-structured-outputs.md)
- **Tool schema** — the declared name, arguments, types and descriptions of a tool an agent may call, used to validate a call before it runs. *(M12)*
- **Token** — a unit of text — word, subword or character — that a language model processes. *(M08, M11)*
- **Tokenisation** — splitting text into tokens. *(M08, M11)*
- **Tool use** — Letting a model call an external function with structured arguments and read the result. *(M12)*
- **Top-k sampling** — restricting each next-token choice to the k most probable tokens before sampling. *(M11)*
- **Top-p (nucleus) sampling** — restricting each next-token choice to the smallest set of tokens whose cumulative probability reaches p. *(M11)*
- **Training set** — the data used to fit parameters. *(M06)*
- **Transfer learning** — reusing a model trained on one task as the starting point for another. *(M07)*
- **Transformer** — an architecture built from self-attention and feed-forward layers; the basis of modern language and vision models. *(M07)*
- **Transparency** — the property that a system's purpose, data, behaviour and limits are documented well enough for an outsider to audit them. *(M13)*
- **Trigger (backdoor)** — the input pattern that activates a backdoored behaviour, often a small patch or a rare token sequence. *(M13)*
- **Turing test** — an operational test of machine intelligence based on indistinguishability in conversation. *(M01)*
## U

- **U-Net** — An encoder–decoder segmentation network whose skip connections carry fine spatial detail into the decoder. *(M09)* [Lesson](../modules/M09-computer-vision/lessons/L09-05-image-segmentation.md)
- **Uncertainty** — lack of complete information about the state of the world; handled with probability. *(M05)*
- **Underfitting** — a model too simple to capture the pattern, performing poorly on training and test data alike. *(M06)*
- **Unification** — Finding a substitution that makes two logical expressions identical. *(M04)*
- **Unsupervised learning** — finding structure in unlabelled data. *(M06)*
- **Utility** — a numerical measure of how desirable an outcome is. *(M05)*
## V

- **Two-tower model** — separate encoders for two modalities trained into one embedding space, the structure behind image-text retrieval. *(M14)*
- **Variable elimination** — Exact inference that multiplies the factors touching a variable, sums the variable out, and repeats — computing the same sum as enumeration but discarding each variable once. *(M05)* [Lesson](../modules/M05-uncertainty-bayesian-reasoning-and-fuzzy-logic/lessons/L05-06-variable-elimination-and-factor-algebra.md)
- **Vector index** — A data structure that finds the nearest vectors to a query quickly. *(M11)*
- **Vision Transformer** — A transformer over image patches with learned position embeddings; attention replaces convolution and needs more data to match it. *(M09)* [Lesson](../modules/M09-computer-vision/lessons/L09-06-advanced-computer-vision.md)
- **Vision-language model** — a model that relates images and text, by contrastive alignment or by generating text conditioned on images. *(M14)*
- **Validation set** — held-out data used to make tuning decisions without touching the test set. *(M06)*
- **Value function** — the expected return from a state, or from a state–action pair. *(M10)*
- **Vanishing gradient** — gradients shrinking towards zero through many layers, stalling learning. *(M07)*
- **Variance (statistical)** — the sensitivity of a fitted model to the particular training sample it saw. *(M06)*
- **Variational autoencoder (VAE)** — a latent-variable generative model trained on a reconstruction term plus a KL penalty to a prior. *(M11)*
- **Vector database** — an index that retrieves items by embedding similarity. *(M11, M12)*
## W

- **Weight** — a learnable multiplicative parameter in a model. *(M07)*
- **Word error rate (WER)** — edit distance between recognised and reference words divided by the reference length; sensitive to normalisation choices. *(M14)*
- **Weight decay** — an L2 penalty on parameters applied during training, shrinking weights to reduce overfitting. *(M06, M07)*
- **Word embedding** — a vector representation of a word learned from usage. *(M08)*

## X

- **Explainable AI (XAI)** — methods that make a model's behaviour intelligible to people. *(M13)*

## Z

- **Zero-shot** — performing a task without any task-specific training examples. *(M11)*

---

**Missing a term?** Every module page lists the terms it introduces. If a word in a lesson is not
here, the glossary is incomplete — note the lesson and the term.

**Navigation:** [Course home](../README.md) · [Modules](../modules/README.md) ·
[Prerequisites](../prerequisites/README.md) · [Books](books.md) ·
[Documentation](documentation.md) · [Research papers](research-papers.md) · [FAQ](../docs/faq.md)
