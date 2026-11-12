# AI Agents

Resources for M12: the agent loop, tool use, planning, memory, multi-agent patterns and evaluation.
The field moves quickly; the papers here are the stable part.

[Library index](../README.md) · [LLMs](llm-and-transformers.md) · [Responsible AI](responsible-ai-and-security.md)

---

### LLM Powered Autonomous Agents
**Lilian Weng** · 2023
- **URL:** https://lilianweng.github.io/posts/2023-06-23-agent/
- **Modules:** M12 · **Level:** Intermediate
- **Why:** A clear decomposition of an agent into planning, memory and tool use, with the papers behind each. The best single overview before starting the module.
- **Access:** Free to read on the author's site.

### ReAct: Synergizing Reasoning and Acting in Language Models
**Yao et al.** · ICLR 2023
- **URL:** https://arxiv.org/abs/2210.03629
- **Modules:** M12 · **Level:** Advanced
- **Why:** The reason–act loop that most agents still follow, with the prompting pattern and the failure cases. Read §2 and the ablation table.
- **Access:** Open access on arXiv.

### Toolformer: Language Models Can Teach Themselves to Use Tools
**Schick et al.** · NeurIPS 2023
- **URL:** https://arxiv.org/abs/2302.04761
- **Modules:** M12 · **Level:** Advanced
- **Why:** How a model can learn when to call an API, and why self-supervised tool labelling is harder than it looks. Useful context for schema design.
- **Access:** Open access on arXiv.

### A Survey on Large Language Model based Autonomous Agents
**Wang, Ma, Feng, et al.** · 2023, revised 2025
- **URL:** https://arxiv.org/abs/2308.11432
- **Modules:** M12 · **Level:** Advanced
- **Why:** A unified framework for agent construction, applications and evaluation, with a large reference list. Use it to find the sub-area your project belongs to.
- **Access:** Open access on arXiv.

### OpenAI Cookbook — function calling and agents
**OpenAI** · open-source repository
- **URL:** https://github.com/openai/openai-cookbook
- **Modules:** M12 · **Level:** Intermediate
- **Why:** Working examples of tool schemas, parallel tool calls and agent loops, written against a real API. Useful even if you use another provider: the patterns transfer.
- **Access:** Open source on GitHub under the repository's MIT licence.

### LangGraph documentation
**LangChain** · current release
- **URL:** https://langchain-ai.github.io/langgraph/
- **Modules:** M12 · **Level:** Intermediate
- **Why:** A graph-based way to express agent control flow, with explicit state and checkpoints. Worth reading even if you build your own loop: it names the failure modes you will meet.
- **Access:** Free; MIT licensed.

### Model Context Protocol — specification
**Anthropic and contributors** · open standard
- **URL:** https://modelcontextprotocol.io/
- **Modules:** M12, M14 · **Level:** Advanced
- **Why:** A concrete protocol for exposing tools and data to models, with schemas and security considerations. The clearest example of standardising the tool boundary.
- **Access:** Free, open specification.

### AgentBench / evaluation harnesses
**THUDM** · open-source benchmark
- **URL:** https://github.com/THUDM/AgentBench
- **Modules:** M12 · **Level:** Advanced
- **Why:** A multi-environment benchmark for agents, useful for seeing how task success is measured across domains — and how easily it is gamed.
- **Access:** Open source under the repository's licence.

---

[Library index](../README.md) · [LLMs](llm-and-transformers.md) · [Responsible AI](responsible-ai-and-security.md) · [Papers](papers-and-surveys.md)
