# Reinforcement Learning

Resources for M10. Start with the book, use the course when a lecture explains it better, and use the
libraries when you want a reference implementation to compare against your own.

[Library index](../README.md) · [Textbooks](textbooks.md) · [OER](open-educational-resources.md) · [Agents](ai-agents.md)

---

### Reinforcement Learning: An Introduction (2nd edition)
**Richard S. Sutton and Andrew G. Barto** · MIT Press, 2018
- **URL:** http://incompleteideas.net/book/the-book-2nd.html
- **Modules:** M10 · **Level:** Intermediate
- **Why:** The source text for the module's notation and structure. Chapters 3–6 cover MDPs, dynamic programming, Monte Carlo and TD; chapters 9–13 cover approximation and policy gradients.
- **Access:** Free PDF from the authors; print edition sold by MIT Press.

### Spinning Up in Deep RL
**OpenAI** · 2018, maintained as a reference
- **URL:** https://spinningup.openai.com/en/latest/
- **Modules:** M10 · **Level:** Intermediate
- **Why:** Explains VPG, TRPO, PPO, DDPG, TD3 and SAC with runnable implementations and a glossary. The "key concepts" page is the best short summary of what M10 assumes.
- **Access:** Free; code released under MIT.

### Reinforcement Learning course (David Silver)
**David Silver (UCL / DeepMind)** · lecture series
- **URL:** https://www.davidsilver.uk/teaching/
- **Modules:** M03, M10 · **Level:** Intermediate
- **Why:** Ten lectures from MDPs to planning and learning, with slides and video. Lecture 8 (integrating learning and planning) connects M03's search to M10's value functions.
- **Access:** Free slides and videos linked from the course page.

### Gymnasium documentation
**Farama Foundation** · current release
- **URL:** https://gymnasium.farama.org/
- **Modules:** M10 · **Level:** Intermediate
- **Why:** The environment API used in the labs: `reset`, `step`, spaces, wrappers and vectorised environments. Read "Basic Usage" before writing a training loop.
- **Access:** Free; MIT licensed.

### Stable-Baselines3
**DLR-RM and contributors** · current release
- **URL:** https://stable-baselines3.readthedocs.io/
- **Modules:** M10 · **Level:** Intermediate
- **Why:** Well-tested PPO, A2C, DQN and SAC with sensible defaults. Use it as a baseline when your hand-written agent underperforms and you want to know whether the bug is in the algorithm or the environment.
- **Access:** Free; MIT licensed.

### CleanRL
**CleanRL contributors** · open-source implementations
- **URL:** https://github.com/vwxyzjn/cleanrl
- **Modules:** M10 · **Level:** Advanced
- **Why:** Single-file implementations of policy-gradient and Q-learning algorithms, each small enough to read in one sitting. The best way to see what production RL code actually looks like.
- **Access:** Open source on GitHub under the repository's MIT licence.

### PettingZoo
**Farama Foundation** · current release
- **URL:** https://pettingzoo.farama.org/
- **Modules:** M10, M12 · **Level:** Advanced
- **Why:** Multi-agent environments with a consistent API. Use it if your capstone involves cooperation or competition between agents.
- **Access:** Free; MIT licensed.

### Deep Reinforcement Learning course (Hugging Face)
**Hugging Face** · online course
- **URL:** https://huggingface.co/learn/deep-rl-course
- **Modules:** M10 · **Level:** Intermediate
- **Why:** A guided, hands-on course that trains agents in hosted environments, with units on Q-learning, policy gradients and multi-agent settings.
- **Access:** Free to follow online.

---

[Library index](../README.md) · [Textbooks](textbooks.md) · [Papers](papers-and-surveys.md)
