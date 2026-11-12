# M11 — Generative AI and Large Language Models

| Level | 400 |
| :--- | :--- |
| Study time | 24 hours |
| Lessons | 7 |
| Course outcome | CLO7 — build, evaluate and reason about generative and retrieval systems |
| Prerequisites | M07 (attention, essential), P04 (recommended). M08 is in the syllabus, but its lessons are not published; the NLP you actually need — tokenisation, embeddings, BM25 — is taught in L11-02 and L11-05 |

[Course home](../../README.md) · [All modules](../README.md) · [Previous module: M10](../README.md#m10) · [Next module: M12](../README.md#m12)

> **Start here if your goal is an LLM application.** You need attention (L07-07) and this module.
> You do not need to wait for M08: tokenisation, embeddings and BM25 are taught in L11-02 §3.7 and
> L11-05. After L11-02, go straight to
> [LAB-11-02](labs/lab-11-02-build-a-retrieval-augmented-assistant.md), which builds a working
> retrieval-augmented assistant end to end on CPU.

## Overview

This module answers two questions that are usually conflated: **what is happening inside a
generative model**, and **how do you build a reliable system around one?**

The first half is mechanism. You will tokenise text and see what a token actually costs, compute
attention by hand, train a VAE, a GAN and a diffusion model on the same data with the same
metrics, and watch a GAN collapse to three of ten classes while its loss curve looks healthy.

The second half is engineering. You will write decoding by hand, build a retrieval-augmented
assistant with dense, lexical and hybrid retrieval, implement LoRA from scratch, and finish
with an evaluation harness that separates retrieval quality, answer quality, grounding, refusal
behaviour, latency and cost.

Everything runs on CPU, locally, offline after the first model download. No API key is required
anywhere in the module; hosted APIs appear only as an optional comparison.

## Practical projects and where they are built

| # | Project | Where |
| :--- | :--- | :--- |
| 1 | Text generation application | [NB-11-01](notebooks/nb-11-01-tokens-attention-and-generative-models.ipynb), [LAB-11-01](labs/lab-11-01-prompt-engineering-laboratory.md) |
| 2 | PDF question-answering system | [LAB-11-02](labs/lab-11-02-build-a-retrieval-augmented-assistant.md) scenario A |
| 3 | University FAQ chatbot | [LAB-11-02](labs/lab-11-02-build-a-retrieval-augmented-assistant.md) scenario B |
| 4 | RAG-based document assistant | [ASG-11](assignments/asg-11-rag-evaluation-report.md), [MP-11](projects/mp-11-domain-qa-assistant.md) |
| 5 | Sentiment analysis using an LLM | [LAB-11-03](labs/lab-11-03-evaluation-harness.md) scenario A |
| 6 | Local LLM chatbot | [LAB-11-02](labs/lab-11-02-build-a-retrieval-augmented-assistant.md), `code/app.py` |
| 7 | Domain-specific document assistant | [MP-11](projects/mp-11-domain-qa-assistant.md) |
| 8 | Fine-tuning a small open model | [LAB-11-03](labs/lab-11-03-evaluation-harness.md) scenario C, `code/lora.py` |

## Models, data and licences

No weights or corpora are redistributed with this module. Everything is either authored here
or downloaded by name from the Hugging Face hub on first use.

| Asset | Licence | Size / note |
| :--- | :--- | :--- |
| `distilgpt2` | Apache-2.0 | 82M parameters, decoder; next-token sampling and perplexity |
| `google/flan-t5-small` | Apache-2.0 | 77M parameters, encoder–decoder; question answering |
| `sentence-transformers/all-MiniLM-L6-v2` | Apache-2.0 | 22M parameters, 384-dim embeddings |
| `distilbert-base-uncased-finetuned-sst-2-english` | Apache-2.0 | 67M parameters, sentiment baseline |
| The Northfield handbook (24 documents) | **CC0-1.0** | authored for this module; fictional institution |
| QA set, unanswerable set, sentiment set | **CC0-1.0** | authored for this module |
| scikit-learn `load_digits` | public-domain UCI data | 1,797 8×8 images, bundled with scikit-learn |

**Check licences before redistribution.** Apache-2.0 weights may be redistributed with
attribution; the CC0 corpus here may be used freely. A model's licence is separate from its
training data's licence, and neither is automatically inherited by your output — but a merged
adapter carries the base model's licence.

## Before you start

You need: Python with NumPy and PyTorch (CPU is enough), comfort with training loops, and the
attention material from M07. Install what is missing:

```bash
pip install transformers sentence-transformers torch numpy scikit-learn matplotlib
pip install faiss-cpu rank_bm25 pypdf streamlit
```

**Readiness self-check.** If you cannot do three of these, review M07 first:

1. Write the scaled dot-product attention formula and say why the divisor exists.
2. Explain the difference between cross-entropy and a likelihood.
3. Compute the KL divergence between two univariate Gaussians.
4. Explain why a test set must not be used for tuning.
5. Convert a 500-word document to an approximate token count.

## Module map

| ID | Title | Type | Time | Link |
| :--- | :--- | :--- | ---: | :--- |
| L11-01 | The Generative Modelling Landscape | Lesson | 90 m | [Read](lessons/L11-01-the-generative-modelling-landscape.md) |
| L11-02 | Inside a Large Language Model | Lesson | 90 m | [Read](lessons/L11-02-inside-a-large-language-model.md) |
| L11-03 | Pretraining, Instruction Tuning and Alignment | Lesson | 90 m | [Read](lessons/L11-03-pretraining-instruction-tuning-and-alignment.md) |
| L11-04 | Prompt Engineering and In-Context Learning | Lesson | 90 m | [Read](lessons/L11-04-prompt-engineering-and-in-context-learning.md) |
| L11-05 | Retrieval-Augmented Generation | Lesson | 90 m | [Read](lessons/L11-05-retrieval-augmented-generation.md) |
| L11-06 | Fine-Tuning and Parameter-Efficient Adaptation | Lesson | 90 m | [Read](lessons/L11-06-fine-tuning-and-parameter-efficient-adaptation.md) |
| L11-07 | Evaluating LLM Systems | Lesson | 90 m | [Read](lessons/L11-07-evaluating-llm-systems.md) |
| NB-11-01 | Tokens, Attention and Generative Models | Notebook | 60 m | [Open](notebooks/nb-11-01-tokens-attention-and-generative-models.ipynb) |
| NB-11-02 | Retrieval, Prompting and Evaluation | Notebook | 60 m | [Open](notebooks/nb-11-02-retrieval-prompting-and-evaluation.ipynb) |
| LAB-11-01 | Prompt Engineering Laboratory | Lab | 2.5 h | [Start](labs/lab-11-01-prompt-engineering-laboratory.md) |
| LAB-11-02 | Build a Retrieval-Augmented Assistant | Lab | 2.5 h | [Start](labs/lab-11-02-build-a-retrieval-augmented-assistant.md) |
| LAB-11-03 | An Evaluation Harness for LLM Systems | Lab | 2.5 h | [Start](labs/lab-11-03-evaluation-harness.md) |
| ASG-11 | A RAG System with an Evaluation Report | Assignment | 1.5 h | [Start](assignments/asg-11-rag-evaluation-report.md) |
| QUIZ-11 | Module self-check | Quiz | 30 m | [Take](quizzes/quiz-11.md) |
| MP-11 | Domain Question-Answering Assistant | Mini-project | 2 h | [Start](projects/mp-11-domain-qa-assistant.md) |

Total: 10.5 h lessons + 2 h notebooks + 7.5 h labs + 1.5 h assignment + 0.5 h quiz + 2 h
mini-project = **24 hours**.

Supporting code lives in [`code/`](code/):

| File | Contents |
| :--- | :--- |
| `gen_data.py` | the 24-document corpus, QA sets, sentiment set and a minimal PDF writer |
| `tokenizers_lab.py` | BPE from scratch, tokeniser comparison, context arithmetic, chunking |
| `attention_lab.py` | attention, masks, multi-head, positional encodings, pretrained head analysis |
| `gen_models.py` | VAE, GAN and DDPM on 8×8 digits with shared sample metrics |
| `llm_gen.py` | hand-written decoding, perplexity, grounding, quantisation, KV-cache timing |
| `prompts.py` | seven templates, structured output, injection experiment, template evaluation |
| `rag.py` | ingestion, chunking, FAISS + BM25, fusion, MaxSim reranking, evaluation |
| `lora.py` | LoRA layer, application, training, merging and verification |
| `llm_eval.py` | EM, token F1, ROUGE-L, recall@k, MRR, nDCG, support rate, κ, latency |
| `app.py` | Streamlit demo and CLI for the assistant |
| `build_notebooks.py` | regenerates and executes the two notebooks |

Every module runs standalone: `python gen_data.py`, `python tokenizers_lab.py`,
`python attention_lab.py`, `python gen_models.py`, `python llm_gen.py`, `python prompts.py`,
`python rag.py`, `python lora.py`, `python llm_eval.py`.

## Suggested study plan

| Day | Work | Time |
| :--- | :--- | ---: |
| 1 | L11-01, L11-02 | 3 h |
| 2 | NB-11-01 | 1.5 h |
| 3 | L11-03, L11-04 | 3 h |
| 4 | LAB-11-01 | 2.5 h |
| 5 | L11-05 | 2 h |
| 6 | LAB-11-02 (start) | 2.5 h |
| 7 | LAB-11-02 (finish), NB-11-02 | 3 h |
| 8 | L11-06 | 2 h |
| 9 | L11-07, LAB-11-03 | 3 h |
| 10 | ASG-11, QUIZ-11 | 2 h |
| 11 | MP-11, revision | 2 h |

Ten days at roughly 2.5 hours. If time is short, keep L11-01, L11-02, L11-05 and LAB-11-02;
they carry the mechanism and the system design.

## Assessment for this module

| Component | What is checked | Weight |
| :--- | :--- | ---: |
| LAB-11-01 | Prompt harness, intervals, structured output, injection honesty | 10% |
| LAB-11-02 | Retrieval comparison, ablations, refusal calibration, error analysis | 10% |
| LAB-11-03 | Harness design, adapter comparison, cost analysis | 10% |
| QUIZ-11 | Conceptual and numerical grasp | 10% |
| ASG-11 | Evaluation set quality, per-stage metrics, ablation discipline | 25% |
| MP-11 | Working assistant, sources, evaluation, licence honesty | 35% |

The assessment dimensions are described in the
[curriculum map](../../docs/CURRICULUM-MAP.md#8-assessment-model).

## Compute requirements

| Stage | CPU only | GPU (optional) |
| :--- | :--- | :--- |
| Tokenisation, attention lab | seconds | — |
| VAE / GAN / diffusion (8×8 digits) | 12–30 s per model | seconds |
| Sampling with distilgpt2 | 15–25 tokens/s | 10–50× faster |
| RAG index build | ~45 s for 48 chunks | small gain |
| RAG answer | ~1.8 s per question | ~0.3 s |
| LoRA, 40 steps | 12.4 s | seconds |

A 4-core laptop is sufficient for everything in the module. GPU exercises are marked optional
and never required for the graded work.

## Key terms introduced

**Generative model**, **discriminative model**, **ELBO**, **KL divergence**, **VAE**, **GAN**,
**mode collapse**, **diffusion**, **DDPM**, **noise schedule**, **autoregressive model**,
**perplexity**, **token**, **BPE**, **embedding**, **self-attention**, **multi-head attention**,
**causal mask**, **positional encoding**, **context window**, **next-token prediction**,
**pretraining**, **instruction tuning**, **SFT**, **RLHF**, **DPO**, **LoRA**, **QLoRA**,
**quantisation**, **KV cache**, **temperature**, **top-k**, **top-p**, **hallucination**,
**prompt injection**, **few-shot prompting**, **chain-of-thought**, **RAG**, **chunking**,
**BM25**, **hybrid retrieval**, **reranking**, **grounding**, **exact match**, **ROUGE-L**,
**nDCG**, **refusal rate**, **LLM-as-judge**.

All are defined in the [glossary](../../resources/glossary.md). The one-page recap is in
[summary.md](summary.md).

## Resources

- Jurafsky & Martin, *Speech and Language Processing*, 3rd edition drafts — chapters on
  transformers and LLMs, free online.
- Hugging Face `transformers` documentation and course — the API used throughout.
- Bommasani et al. (2021). *On the Opportunities and Risks of Foundation Models*.
- Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*.
- The module's [summary](summary.md) — formulas and every verified number.

## Navigation

[Course home](../../README.md) · [All modules](../README.md) · [Previous: M10](../README.md#m10) ·
[Next module: M12](../README.md#m12)
