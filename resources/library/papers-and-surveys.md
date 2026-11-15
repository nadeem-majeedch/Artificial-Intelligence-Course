# Papers and Surveys

Primary sources, organised by the module they serve. Each entry gives the venue so you can cite it
correctly, and an open-access link where one exists.

Two rules for this page: **cite what you read**, and **do not cite a paper you have only seen quoted**.
Where a paper is paywalled and has no author preprint, the entry says so rather than inventing a link.

[Library index](../README.md) · [Research papers with reading guidance](../research-papers.md) · [Textbooks](textbooks.md)

---

## Foundations and classical AI

### A Formal Basis for the Heuristic Determination of Minimum Cost Paths
Hart, Nilsson and Raphael · *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 1968
- **URL:** No stable free copy; available through university libraries.
- **Modules:** M03 · **Level:** Advanced
- **Why:** The paper that introduced A\* and the admissibility argument. Six pages; read it after you have implemented the algorithm.
- **Access:** Paywalled (IEEE).

### Learning representations by back-propagating errors
Rumelhart, Hinton and Williams · *Nature*, 323, 1986
- **URL:** No free edition; available through university libraries.
- **Modules:** M07 · **Level:** Advanced
- **Why:** The short paper that made backpropagation widely adopted. Read it after deriving the gradients by hand in PA-07.
- **Access:** Paywalled (Nature).

### Support-vector networks
Cortes and Vapnik · *Machine Learning*, 20, 1995
- **URL:** No stable free copy; available through university libraries.
- **DOI:** [10.1007/BF00994018](https://doi.org/10.1007/BF00994018)
- **Modules:** M06 · **Level:** Advanced
- **Why:** The margin formulation of the SVM, stated cleanly. Explains why maximum-margin classifiers generalise.
- **Access:** Paywalled (Springer).

### Random Forests
Leo Breiman · *Machine Learning*, 45, 2001
- **URL:** No stable free copy; author's technical report circulated widely.
- **Modules:** M06 · **Level:** Advanced
- **Why:** Bagging plus random feature selection, from the author. The variance argument is clearer here than in any summary.
- **Access:** Paywalled (Springer).

### Reinforcement Learning: A Survey
Kaelbling, Littman and Moore · *Journal of Artificial Intelligence Research*, 4, 1996
- **URL:** https://www.jair.org/
- **Modules:** M10 · **Level:** Advanced
- **Why:** The survey that framed the field's questions — exploration, credit assignment, generalisation — most of which are still open.
- **Access:** Open access via JAIR.

## Machine learning and deep learning

### Deep learning
LeCun, Bengio and Hinton · *Nature*, 521, 2015
- **URL:** https://www.nature.com/articles/nature14539
- **Modules:** M07 · **Level:** Intermediate
- **Why:** A short, authoritative overview of representation learning, written for a broad scientific audience. Good orientation before M07.
- **Access:** Paywalled (Nature); often available through institutions.

### ImageNet Classification with Deep Convolutional Neural Networks
Krizhevsky, Sutskever and Hinton · *NeurIPS*, 2012
- **URL:** https://proceedings.neurips.cc/
- **Modules:** M09 · **Level:** Advanced
- **Why:** AlexNet — the result that started the deep-learning era, with the engineering details (ReLU, dropout, GPU training) that made it work.
- **Access:** Open access via the NeurIPS proceedings.

### Deep Residual Learning for Image Recognition
He, Zhang, Ren and Sun · *CVPR*, 2016
- **URL:** https://arxiv.org/abs/1512.03385
- **Modules:** M07, M09 · **Level:** Advanced
- **Why:** Skip connections and why depth stopped hurting. Read §3 for the degradation problem.
- **Access:** Open access on arXiv.

### Attention Is All You Need
Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser and Polosukhin · *NeurIPS*, 2017
- **URL:** https://arxiv.org/abs/1706.03762
- **Modules:** M07, M08, M11 · **Level:** Advanced
- **Why:** The transformer. Read §3 with the M07 attention lesson open; the equations are shorter than their reputation.
- **Access:** Open access on arXiv.

### BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
Devlin, Chang, Lee and Toutanova · *NAACL*, 2019
- **URL:** https://arxiv.org/abs/1810.04805
- **Modules:** M08 · **Level:** Advanced
- **Why:** Pretraining plus fine-tuning, which became the standard pattern for text tasks. Read §3 for the masked-language-model objective.
- **Access:** Open access on arXiv.

### Language Models are Few-Shot Learners
Brown et al. · *NeurIPS*, 2020
- **URL:** https://arxiv.org/abs/2005.14165
- **Modules:** M11 · **Level:** Advanced
- **Why:** GPT-3, and the observation that scale produces in-context learning. Long; read the introduction, §2 and the limitations section.
- **Access:** Open access on arXiv.

### Training language models to follow instructions with human feedback
Ouyang et al. · *NeurIPS*, 2022
- **URL:** https://arxiv.org/abs/2203.02155
- **Modules:** M11 · **Level:** Advanced
- **Why:** InstructGPT: how preference data and reinforcement learning from human feedback turn a text predictor into an assistant, and what it costs.
- **Access:** Open access on arXiv.

## Vision

### ImageNet: A Large-Scale Hierarchical Image Database
Deng, Dong, Socher, Li, Li and Fei-Fei · *CVPR*, 2009
- **URL:** https://ieeexplore.ieee.org/document/5206848
- **DOI:** [10.1109/CVPR.2009.5206848](https://doi.org/10.1109/CVPR.2009.5206848)
- **Modules:** M09 · **Level:** Intermediate
- **Why:** The dataset that made modern vision possible, and a lesson in benchmark design. Read §2 for the collection protocol.
- **Access:** Paywalled (IEEE); the dataset itself is separately licensed for research.

### Fully Convolutional Networks for Semantic Segmentation
Long, Shelhamer and Darrell · *CVPR*, 2015
- **URL:** https://arxiv.org/abs/1411.4038
- **Modules:** M09 · **Level:** Advanced
- **Why:** Segmentation as dense prediction, which is the idea behind every segmentation model since. Read §3.
- **Access:** Open access on arXiv.

### You Only Look Once: Unified, Real-Time Object Detection
Redmon, Divvala, Girshick and Farhadi · *CVPR*, 2016
- **URL:** https://arxiv.org/abs/1506.02640
- **Modules:** M09 · **Level:** Advanced
- **Why:** Detection as a single regression problem, which is why it became fast enough for video. The grid-and-anchors design is best understood with the figures.
- **Access:** Open access on arXiv.

### Mask R-CNN
He, Gkioxari, Dollár and Girshick · *ICCV*, 2017
- **URL:** https://arxiv.org/abs/1703.06870
- **Modules:** M09 · **Level:** Advanced
- **Why:** Instance segmentation by adding a mask branch to a detector. A good example of an architecture that is mostly careful engineering.
- **Access:** Open access on arXiv.

## Reinforcement learning

### Human-level control through deep reinforcement learning
Mnih et al. · *Nature*, 518, 2015
- **URL:** https://www.nature.com/articles/nature14236
- **Modules:** M10 · **Level:** Advanced
- **Why:** DQN with experience replay and target networks — the engineering that made deep RL stable. The methods section is the part to read.
- **Access:** Paywalled (Nature); the 2013 preprint "Playing Atari with Deep Reinforcement Learning" is on arXiv (1312.5602).

### Mastering the game of Go with deep neural networks and tree search
Silver et al. · *Nature*, 529, 2016
- **URL:** https://www.nature.com/articles/nature16961
- **Modules:** M03, M10 · **Level:** Advanced
- **Why:** AlphaGo, where search and learned evaluation meet. The clearest worked example of M03 and M10 cooperating.
- **Access:** Paywalled (Nature).

### Proximal Policy Optimization Algorithms
Schulman, Wolski, Dhariwal, Radford and Klimov · 2017
- **URL:** https://arxiv.org/abs/1707.06347
- **Modules:** M10 · **Level:** Advanced
- **Why:** PPO, still the default policy-gradient method in practice. The clipped objective is explained in §3 in three equations.
- **Access:** Open access on arXiv.

## Generative models

### Auto-Encoding Variational Bayes
Kingma and Welling · *ICLR*, 2014
- **URL:** https://arxiv.org/abs/1312.6114
- **Modules:** M11 · **Level:** Advanced
- **Why:** The VAE and the reparameterisation trick that makes it trainable. Read §2.3–2.4 slowly.
- **Access:** Open access on arXiv.

### Generative Adversarial Networks
Goodfellow, Pouget-Abadie, Mirza, Xu, Warde-Farley, Ozair, Courville and Bengio · *NeurIPS*, 2014
- **URL:** https://arxiv.org/abs/1406.2661
- **Modules:** M11 · **Level:** Advanced
- **Why:** Two networks, one minimax game. Worth reading for how a competitive objective can produce samples.
- **Access:** Open access on arXiv.

### Denoising Diffusion Probabilistic Models
Ho, Jain and Abbeel · *NeurIPS*, 2020
- **URL:** https://arxiv.org/abs/2006.11239
- **Modules:** M11 · **Level:** Advanced
- **Why:** Diffusion as learned denoising, now the basis of most image generation. The training objective in §3 is the part to take away.
- **Access:** Open access on arXiv.

### High-Resolution Image Synthesis with Latent Diffusion Models
Rombach, Blattmann, Lorenz, Esser and Ommer · *CVPR*, 2022
- **URL:** https://arxiv.org/abs/2112.10752
- **Modules:** M11 · **Level:** Advanced
- **Why:** The architecture behind Stable Diffusion: diffuse in a compressed latent space rather than pixels. Read §3 for the trade-off.
- **Access:** Open access on arXiv.

## Language-model applications

### Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
Lewis et al. · *NeurIPS*, 2020
- **URL:** https://arxiv.org/abs/2005.11401
- **Modules:** M11, M12 · **Level:** Advanced
- **Why:** The paper behind every RAG system. Note what it evaluates — factual recall — and what it does not claim.
- **Access:** Open access on arXiv.

### LoRA: Low-Rank Adaptation of Large Language Models
Hu et al. · *ICLR*, 2022
- **URL:** https://arxiv.org/abs/2106.09685
- **Modules:** M11 · **Level:** Advanced
- **Why:** Fine-tuning by learning small matrices, which is why adaptation became affordable. §4 gives the parameter arithmetic your quiz asks for.
- **Access:** Open access on arXiv.

### Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
Wei et al. · *NeurIPS*, 2022
- **URL:** https://arxiv.org/abs/2201.11903
- **Modules:** M11 · **Level:** Advanced
- **Why:** Why "think step by step" changes accuracy, and on which tasks it does not. Read the ablations, not just the headline.
- **Access:** Open access on arXiv.

### Direct Preference Optimization: Your Language Model is Secretly a Reward Model
Rafailov, Sharma, Mitchell, Ermon, Manning and Finn · *NeurIPS*, 2023
- **URL:** https://arxiv.org/abs/2305.18290
- **Modules:** M11 · **Level:** Advanced
- **Why:** Preference tuning without a separate reward model, which is why it spread quickly. The derivation in §4 is the point.
- **Access:** Open access on arXiv.

## Agents

### ReAct: Synergizing Reasoning and Acting in Language Models
Yao et al. · *ICLR*, 2023
- **URL:** https://arxiv.org/abs/2210.03629
- **Modules:** M12 · **Level:** Advanced
- **Why:** The reason–act loop that most agents still follow. Read §2 and the ablation showing that reasoning without acting, or acting without reasoning, is worse.
- **Access:** Open access on arXiv.

### Toolformer: Language Models Can Teach Themselves to Use Tools
Schick et al. · *NeurIPS*, 2023
- **URL:** https://arxiv.org/abs/2302.04761
- **Modules:** M12 · **Level:** Advanced
- **Why:** Learning when to call an API from self-supervision. Useful for thinking about what a tool schema can and cannot express.
- **Access:** Open access on arXiv.

### A Survey on Large Language Model based Autonomous Agents
Wang, Ma, Feng, et al. · 2023, revised 2025
- **URL:** https://arxiv.org/abs/2308.11432
- **Modules:** M12 · **Level:** Advanced
- **Why:** A unified construction framework plus applications and evaluation methods. The best entry point to the agent literature.
- **Access:** Open access on arXiv.

## Responsibility, explanation and security

### Intriguing properties of neural networks
Szegedy et al. · *ICLR*, 2014
- **URL:** https://arxiv.org/abs/1312.6199
- **Modules:** M13 · **Level:** Advanced
- **Why:** The discovery that tiny, often invisible perturbations change predictions. The origin of the adversarial-example literature.
- **Access:** Open access on arXiv.

### Explaining and Harnessing Adversarial Examples
Goodfellow, Shlens and Szegedy · *ICLR*, 2015
- **URL:** https://arxiv.org/abs/1412.6572
- **Modules:** M13 · **Level:** Advanced
- **Why:** FGSM — the one-step attack your quiz traces — and the linearity explanation for why it works.
- **Access:** Open access on arXiv.

### "Why Should I Trust You?" Explaining the Predictions of Any Classifier
Ribeiro, Singh and Guestrin · *KDD*, 2016
- **URL:** https://arxiv.org/abs/1602.04938
- **Modules:** M13 · **Level:** Advanced
- **Why:** LIME, and a candid discussion of what local explanations do not establish. Read the "trusting the explainer" section.
- **Access:** Open access on arXiv.

### A Unified Approach to Interpreting Model Predictions
Lundberg and Lee · *NeurIPS*, 2017
- **URL:** https://arxiv.org/abs/1705.07874
- **Modules:** M13 · **Level:** Advanced
- **Why:** SHAP, the efficiency property, and the game-theoretic argument behind additive attributions.
- **Access:** Open access on arXiv.

### Model Cards for Model Reporting
Mitchell, Wu, Zaldivar, Barnes, Vasserman, Hutchinson, Spitzer, Raji and Gebru · *FAT\**, 2019
- **URL:** https://arxiv.org/abs/1810.03993
- **Modules:** M13, M14 · **Level:** Intermediate
- **Why:** The documentation format you produce in M13's audit. Short, and the examples make the sections concrete.
- **Access:** Open access on arXiv.

### Datasheets for Datasets
Gebru, Morgenstern, Vecchione, Wortman Vaughan, Wallach, Daumé III and Crawford · *Communications of the ACM*, 2021
- **URL:** https://arxiv.org/abs/1803.09010
- **Modules:** M06, M13 · **Level:** Intermediate
- **Why:** The dataset counterpart to model cards: provenance, collection, preprocessing and known limitations. Use it when auditing the data behind a model.
- **Access:** Open access on arXiv.

### Deep Learning with Differential Privacy
Abadi, Chu, Goodfellow, McMahan, Mironov, Talwar and Zhang · *ACM CCS*, 2016
- **URL:** https://arxiv.org/abs/1607.00133
- **Modules:** M13 · **Level:** Advanced
- **Why:** Differentially private SGD and the privacy–accuracy trade-off stated as a budget. The definition in §2 is the part to understand.
- **Access:** Open access on arXiv.

### Membership Inference Attacks Against Machine Learning Models
Shokri, Stronati, Song and Shmatikov · *IEEE Symposium on Security and Privacy*, 2017
- **URL:** https://arxiv.org/abs/1610.05820
- **Modules:** M13 · **Level:** Advanced
- **Why:** The attack behind the AUC you report in the audit, and why overfitting makes it easier.
- **Access:** Open access on arXiv.

### Counterfactual Fairness
Kusner, Loftus, Russell and Silva · *NeurIPS*, 2017
- **URL:** https://arxiv.org/abs/1703.06856
- **Modules:** M13 · **Level:** Advanced
- **Why:** Fairness defined causally: the decision would be the same in a counterfactual world. The clearest statement of why group metrics are not the whole story.
- **Access:** Open access on arXiv.

### Fairness in Machine Learning: A Survey
Caton and Haas · *ACM Computing Surveys*, 56(7), 2024
- **URL:** https://arxiv.org/abs/2010.04053
- **Modules:** M13 · **Level:** Advanced
- **Why:** Organises mitigation into pre-, in- and post-processing and names the four dilemmas that keep the field arguing. A good map of the literature.
- **Access:** Open access on arXiv.

### Explainable Artificial Intelligence (XAI): Concepts, Taxonomies, Opportunities and Challenges toward Responsible AI
Barredo Arrieta et al. · *Information Fusion*, 58, 2020
- **URL:** https://arxiv.org/abs/1910.10045
- **Modules:** M13 · **Level:** Advanced
- **Why:** A long, well-structured survey of explanation methods and their taxonomies. Read the taxonomy sections and the challenges, not the whole 67 pages.
- **Access:** Open access on arXiv.

### Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead
Cynthia Rudin · *Nature Machine Intelligence*, 1, 2019
- **URL:** No free edition; available through university libraries.
- **Modules:** M13 · **Level:** Advanced
- **Why:** The strongest argument that post-hoc explanation is the wrong goal for consequential decisions. Read it as a challenge to the module's own emphasis.
- **Access:** Paywalled (Nature).

### NIST AI 100-2: Adversarial Machine Learning — Taxonomy and Terminology
Vassilev, Oprea, Fordyce and Anderson · NIST, 2025
- **URL:** https://csrc.nist.gov/pubs/ai/100/2/e2025/final
- **Modules:** M13, M14 · **Level:** Intermediate
- **Why:** A standard taxonomy of attacks and mitigations, including for generative and agentic systems. Use its vocabulary in your risk register.
- **Access:** Free from NIST.

---

[Library index](../README.md) · [Reading guidance](../research-papers.md) · [Responsible AI resources](responsible-ai-and-security.md)
