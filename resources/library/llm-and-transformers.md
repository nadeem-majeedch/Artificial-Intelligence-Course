# LLMs and Transformers

Resources for tokenisers, pretrained models, fine-tuning and serving. This is the fastest-moving part
of the library: prefer official documentation and recent papers over tutorials more than a year old.

[Library index](../README.md) · [Generative AI](generative-ai.md) · [Agents](ai-agents.md) · [Documentation](official-documentation.md)

---

### The Illustrated Transformer
**Jay Alammar** · 2018
- **URL:** https://jalammar.github.io/illustrated-transformer/
- **Modules:** M07, M08, M11 · **Level:** Beginner
- **Why:** The visual explanation most people used to understand self-attention for the first time. Read it before L07's attention lesson, then read the paper.
- **Access:** Free to read on the author's site.

### Hugging Face Transformers documentation
**Hugging Face** · current release
- **URL:** https://huggingface.co/docs/transformers/
- **Modules:** M08, M11 · **Level:** Intermediate
- **Why:** Task guides, model classes and generation utilities (`generate`, `Trainer`, tokenisers), kept in step with the library. The default reference for any pretrained-model work.
- **Access:** Free; Apache-2.0 licensed.

### Hugging Face LLM Course
**Hugging Face** · continuously updated
- **URL:** https://huggingface.co/learn
- **Modules:** M08, M11, M12 · **Level:** Intermediate
- **Why:** A structured course covering transformers, tokenisation, fine-tuning, evaluation and sharing, with runnable notebooks. Free, and closer to current practice than most textbooks.
- **Access:** Free to follow; code open source.

### The Annotated Transformer
**Alexander Rush** · Harvard NLP
- **URL:** https://nlp.seas.harvard.edu/annotated-transformer/
- **Modules:** M07, M11 · **Level:** Advanced
- **Why:** The paper's architecture implemented line by line in PyTorch, with the text beside the code. The best single resource for understanding what a transformer block computes.
- **Access:** Free to read online.

### The NLP Cookbook
**Hugging Face** · open-source repository
- **URL:** https://github.com/huggingface/cookbook
- **Modules:** M11, M12 · **Level:** Intermediate
- **Why:** Short recipes for common LLM tasks — classification, summarisation, retrieval, evaluation — each runnable and small enough to adapt.
- **Access:** Open source under the repository's licence.

### PEFT documentation (LoRA and adapters)
**Hugging Face** · current release
- **URL:** https://huggingface.co/docs/peft/
- **Modules:** M11 · **Level:** Intermediate
- **Why:** How low-rank adapters are attached, configured and merged, with the parameter counts made explicit. Read alongside the LoRA paper.
- **Access:** Free; Apache-2.0 licensed.

### vLLM documentation
**vLLM project** · current release
- **URL:** https://docs.vllm.ai/
- **Modules:** M11, M14 · **Level:** Advanced
- **Why:** Serving and batching for LLMs, including paged attention and throughput measurement. Useful if your capstone needs to answer more than a few requests per minute.
- **Access:** Free; Apache-2.0 licensed.

### Open LLM Leaderboard
**Hugging Face** · live benchmark
- **URL:** https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
- **Modules:** M11, M13 · **Level:** Intermediate
- **Why:** Comparable benchmark results across open models, useful for choosing a base model — and for seeing how much benchmark choice changes the ranking.
- **Access:** Free to view.

### Tokenizers documentation
**Hugging Face** · current release
- **URL:** https://huggingface.co/docs/tokenizers/
- **Modules:** M08, M11 · **Level:** Intermediate
- **Why:** Byte-pair encoding, WordPiece and Unigram explained with runnable examples, including the training of a tokeniser from scratch. Makes the tokenisation lessons concrete.
- **Access:** Free; Apache-2.0 licensed.

---

[Library index](../README.md) · [Generative AI](generative-ai.md) · [Agents](ai-agents.md) · [Papers](papers-and-surveys.md)
