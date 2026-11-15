# Research Papers

The primary sources behind the course. Most are shorter and more readable than students expect —
a good paper is often clearer than the third-hand summary of it that circulates online.

You do not need to read papers to complete the course. You do need them if you want to know where
an idea came from, what its authors actually claimed, or what your capstone should build on.

**Course home:** [README](../README.md) · **Books:** [books.md](books.md) ·
**Documentation:** [documentation.md](documentation.md) · **Glossary:** [glossary.md](glossary.md)

## How to read a paper you are not ready for

A paper is not a novel; you are not expected to read every word.

1. **Read the title, abstract and figures.** Ten minutes. Decide whether it is relevant at all.
2. **Read the introduction's last two paragraphs.** They state the contribution and the result.
3. **Look at the main table or plot.** What did they measure, against what baseline?
4. **Read the method section only for the part you need.** Usually one idea, not the whole system.
5. **Skip the related-work section entirely** on a first pass. It is written for reviewers.
6. **Write one paragraph in your own words**: what problem, what idea, what evidence. If you cannot,
   you have not read it yet — you have only seen it.

Papers on arXiv are found unambiguously by their identifier (for example `1706.03762`) or by
searching the exact title.

## Foundations and classical AI

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Hart, Nilsson and Raphael (1968), "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"**, *IEEE Transactions on Systems Science and Cybernetics* | M03 | The paper that introduced A\*. Short, and the origin of the admissibility argument the course proves. |
| **Cortes and Vapnik (1995), "Support-vector networks"**, *Machine Learning* — [doi:10.1007/BF00994018](https://doi.org/10.1007/BF00994018) | M06 | The margin idea, stated cleanly. Useful for understanding why maximum-margin classification generalises. |
| **Breiman (2001), "Random Forests"**, *Machine Learning* | M06 | Bagging plus random feature selection, from the author. Explains the variance argument better than any summary. |
| **Pearl (1988), *Probabilistic Reasoning in Intelligent Systems*** (book) | M05 | Not a paper, but the source of Bayesian networks. See [books](books.md). |

## Neural networks and deep learning

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Rumelhart, Hinton and Williams (1986), "Learning representations by back-propagating errors"**, *Nature* | M07 | Two pages that made backpropagation famous. Read it after deriving the algorithm by hand. |
| **Hochreiter and Schmidhuber (1997), "Long Short-Term Memory"**, *Neural Computation* — [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735) | M07 | The gating mechanism that made sequence learning work for two decades. |
| **LeCun, Bottou, Bengio and Haffner (1998), "Gradient-based learning applied to document recognition"**, *Proceedings of the IEEE* | M09 | Convolutional networks applied end to end to handwriting recognition. Long, but the architecture diagrams are worth it. |
| **Krizhevsky, Sutskever and Hinton (2012), "ImageNet Classification with Deep Convolutional Neural Networks"**, *NeurIPS* | M09 | AlexNet: the result that started the deep-learning era, with the engineering details that made it work. |
| **Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov (2014), "Dropout: A Simple Way to Prevent Neural Networks from Overfitting"**, *JMLR* — [arXiv:1207.0580](https://arxiv.org/abs/1207.0580) (preprint: "Improving neural networks by preventing co-adaptation of feature detectors"; the JMLR paper is the published version) | M07 | The regulariser everyone uses, with the intuition clearly argued. |
| **Kingma and Ba (2015), "Adam: A Method for Stochastic Optimization"** — [arXiv:1412.6980](https://arxiv.org/abs/1412.6980) | M07 | The default optimiser, and why its bias correction matters. |
| **Ioffe and Szegedy (2015), "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"** — [arXiv:1502.03167](https://arxiv.org/abs/1502.03167) | M07 | Why normalising activations changes what is trainable. |
| **He, Zhang, Ren and Sun (2016), "Deep Residual Learning for Image Recognition"** — [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) | M07, M09 | Skip connections, and the solution to training very deep networks. |
| **Vaswani et al. (2017), "Attention Is All You Need"** — [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) | M07, M08, M11 | The transformer. Read it after M07's attention lesson; it is more approachable than its reputation. |

## Language

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Mikolov, Chen, Corrado and Dean (2013), "Efficient Estimation of Word Representations in Vector Space"** — [arXiv:1301.3781](https://arxiv.org/abs/1301.3781) | M08 | word2vec: the result that made embeddings standard. |
| **Pennington, Socher and Manning (2014), "GloVe: Global Vectors for Word Representation"**, *EMNLP* | M08 | The alternative to word2vec, built from co-occurrence statistics. |
| **Devlin, Chang, Lee and Toutanova (2019), "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"** — [arXiv:1810.04805](https://arxiv.org/abs/1810.04805) | M08 | Pretraining plus fine-tuning, which became the standard pattern for text tasks. |
| **Brown et al. (2020), "Language Models are Few-Shot Learners"** — [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) | M11 | GPT-3, and the discovery that scale produces in-context learning. |

## Vision

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Deng et al. (2009), "ImageNet: A Large-Scale Hierarchical Image Database"**, *CVPR* | M09 | The dataset that made modern vision possible, and a lesson in benchmark design. |
| **Long, Shelhamer and Darrell (2015), "Fully Convolutional Networks for Semantic Segmentation"**, *CVPR* — [arXiv:1411.4038](https://arxiv.org/abs/1411.4038) | M09 | Segmentation as dense prediction; the idea behind every segmentation model since. |
| **Ronneberger, Fischer and Brox (2015), "U-Net: Convolutional Networks for Biomedical Image Segmentation"** — [arXiv:1505.04597](https://arxiv.org/abs/1505.04597) | M09 | A small dataset, a clever architecture, and a result that changed medical imaging. |
| **Redmon, Divvala, Girshick and Farhadi (2016), "You Only Look Once: Unified, Real-Time Object Detection"**, *CVPR* | M09 | Detection as a single regression problem, which is why it became fast enough for video. |

## Reinforcement learning

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Sutton (1988), "Learning to Predict by the Methods of Temporal Differences"**, *Machine Learning* | M10 | TD learning, the idea underneath almost every modern RL method. |
| **Williams (1992), "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning"**, *Machine Learning* | M10 | REINFORCE: the policy-gradient method the course implements. |
| **Mnih et al. (2015), "Human-level control through deep reinforcement learning"**, *Nature* — [arXiv:1312.5602](https://arxiv.org/abs/1312.5602) (preprint: "Playing Atari with Deep Reinforcement Learning") | M10 | DQN, replay and target networks: the engineering that made deep RL stable. |
| **Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search"**, *Nature* | M10, M03 | AlphaGo, connecting search and learning — the clearest example of M03 and M10 working together. |
| **Schulman, Wolski, Dhariwal, Radford and Klimov (2017), "Proximal Policy Optimization Algorithms"** — [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) | M10 | PPO, still the default policy-gradient method in practice. |

## Generative models

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Kingma and Welling (2014), "Auto-Encoding Variational Bayes"** — [arXiv:1312.6114](https://arxiv.org/abs/1312.6114) | M11 | The VAE, and the reparameterisation trick that makes it trainable. |
| **Goodfellow et al. (2014), "Generative Adversarial Networks"** — [arXiv:1406.2661](https://arxiv.org/abs/1406.2661) | M11 | Two networks, one game. Worth reading for how a competitive objective can produce samples. |
| **Ho, Jain and Abbeel (2020), "Denoising Diffusion Probabilistic Models"** — [arXiv:2006.11239](https://arxiv.org/abs/2006.11239) | M11 | Diffusion as learned denoising — now the basis of most image generation. |
| **Ouyang et al. (2022), "Training language models to follow instructions with human feedback"** — [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) | M11 | InstructGPT: how preference data turns a text predictor into an assistant. |

## Working with language models

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Wei et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"** — [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) | M11 | Why "think step by step" changes accuracy, and when it does not. |
| **Lewis et al. (2020), "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** — [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) | M11 | The paper behind every RAG system you will build. |
| **Hu et al. (2021), "LoRA: Low-Rank Adaptation of Large Language Models"** — [arXiv:2106.09685](https://arxiv.org/abs/2106.09685) | M11 | Fine-tuning by learning small matrices, which is why adaptation became affordable. |
| **Bommasani et al. (2021), "On the Opportunities and Risks of Foundation Models"** — [arXiv:2108.07258](https://arxiv.org/abs/2108.07258) | M11, M13 | A long report, not a paper; read the introduction and the risk sections. |

## Agents

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Yao et al. (2023), "ReAct: Synergizing Reasoning and Acting in Language Models"** — [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) | M12 | The reason–act loop that most agents still follow. |
| **Schick et al. (2023), "Toolformer: Language Models Can Teach Themselves to Use Tools"** | M12 | How models can learn to call tools, and the limits of that approach. |
| **Wu et al. (2023), "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"** — [arXiv:2308.08155](https://arxiv.org/abs/2308.08155) | M12 | Multi-agent orchestration as a practical pattern. |

## Security, explanation and responsibility

| Paper | Module | Why it matters |
| :--- | :--- | :--- |
| **Szegedy et al. (2014), "Intriguing properties of neural networks"** — [arXiv:1312.6199](https://arxiv.org/abs/1312.6199) | M13 | Adversarial examples: the discovery that tiny, invisible changes break classifiers. |
| **Ribeiro, Singh and Guestrin (2016), "Why Should I Trust You? Explaining the Predictions of Any Classifier"** — [arXiv:1602.04938](https://arxiv.org/abs/1602.04938) | M13 | LIME, and a candid discussion of what local explanations do not tell you. |
| **Lundberg and Lee (2017), "A Unified Approach to Interpreting Model Predictions"** — [arXiv:1705.07874](https://arxiv.org/abs/1705.07874) | M13 | SHAP, and the game-theoretic argument behind feature attributions. |
| **Mitchell et al. (2019), "Model Cards for Model Reporting"** — [arXiv:1810.03993](https://arxiv.org/abs/1810.03993) | M13 | The documentation format you will produce in M13's assignment. |
| **Gebru et al. (2021), "Datasheets for Datasets"** — [arXiv:1803.09010](https://arxiv.org/abs/1803.09010) | M13, M06 | Documenting data provenance and limitations — the counterpart to model cards. |
| **Bender, Gebru, McMillan-Major and Shmitchell (2021), "On the Dangers of Stochastic Parrots"**, *FAccT* | M11, M13 | A widely cited critique of large-scale language modelling: data, cost, and harm. Read alongside the capability papers, not instead of them. |
| **Greshake et al. (2023), "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"** | M12, M13 | Why untrusted text is a security boundary, and how agents are attacked in practice. |

## A reading plan for the capstone

If you are starting M14 and want the minimum useful set: read **Attention Is All You Need**, the
**RAG** paper, **Model Cards**, and whichever paper is closest to your project's method. Four papers,
read properly, will serve you better than twenty skimmed ones — and they will give you the habit of
going to primary sources that outlasts this course.

**Navigation:** [Course home](../README.md) · [Books](books.md) ·
[Documentation](documentation.md) · [Glossary](glossary.md) ·
[Modules](../modules/README.md) · [FAQ](../docs/faq.md)
