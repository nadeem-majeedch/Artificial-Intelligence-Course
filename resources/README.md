# Learning Resource Library

A curated set of resources for this course, organised so that you can find the right thing for the
module you are working on without reading a hundred reviews first. Everything here was chosen against
four criteria: it is **authoritative** (official documentation, a university course, a peer-reviewed
paper, or a recognised research laboratory), it is **useful at the point you need it**, it is
**available** (free wherever a good free option exists), and it is **current enough** to describe the
tools the course actually uses.

**Course home:** [README](../README.md) · **Modules:** [modules/README.md](../modules/README.md) ·
**Glossary:** [glossary.md](glossary.md) · [Detailed glossary](glossary/README.md) · [Concept maps](../docs/CONCEPT-MAPS.md) · **Assessment index:** [assessments/README.md](../assessments/README.md)

## How the library is organised

| Page | What it covers | Start here if |
| :--- | :--- | :--- |
| [Textbooks](library/textbooks.md) | 14 books, free where possible | you want one book to go deeper on a module |
| [Open educational resources](library/open-educational-resources.md) | University courses, MOOCs, free curricula | you want a second explanation or a full course |
| [Official documentation](library/official-documentation.md) | Python, NumPy, scikit-learn, PyTorch, TensorFlow/Keras, Hugging Face, OpenCV | you are writing code and need the reference |
| [Reinforcement learning](library/reinforcement-learning.md) | Courses, libraries, tutorials for M10 | you are implementing or debugging an agent |
| [Generative AI](library/generative-ai.md) | VAEs, GANs, diffusion, evaluation | you are working on M11's generative half |
| [LLMs and transformers](library/llm-and-transformers.md) | Tokenisers, pretrained models, fine-tuning, serving | you are building with language models |
| [AI agents](library/ai-agents.md) | Tool use, planning, evaluation, frameworks | you are building the M12 system |
| [Responsible AI and security](library/responsible-ai-and-security.md) | Fairness, explanation, privacy, adversarial ML, governance | you are auditing a model or writing the M13 artefacts |
| [Papers and surveys](library/papers-and-surveys.md) | ~26 primary sources and surveys, with venues | you need the original claim, not a summary |

Two older pages remain useful and are not duplicated here: [books.md](books.md) is a longer annotated
reading list with opinions about *why* each book is worth your time, and
[research-papers.md](research-papers.md) has a reading method for papers you are not ready for. The
library pages are the compact, field-by-field catalogue; those pages are the commentary.

## Reading a library entry

Every entry carries the same seven fields, so you can decide in ten seconds whether to open it:

```text
### Title
Author or organisation · year / version
- URL: where to get it
- Modules: which modules it serves
- Level: Beginner / Intermediate / Advanced
- Why: what it is good for, specifically
- Access: free, open access, or paid
```

**Level** is relative to this course, not to the field. *Beginner* means readable before the module;
*Intermediate* means after its lessons; *Advanced* means after its assignment, when you want the
research framing.

## Module map

If you only read one thing per module, read this:

| Module | First choice | Then |
| :--- | :--- | :--- |
| M01 Foundations | AIMA ch. 1–2 ([textbook](library/textbooks.md)) | Mitchell, *AI: A Guide for Thinking Humans* |
| M02 Agents | AIMA ch. 2 | [Gymnasium docs](library/official-documentation.md) |
| M03 Search | AIMA ch. 3–4 | Hart, Nilsson & Raphael (1968) in [papers](library/papers-and-surveys.md) |
| M04 Knowledge-based | AIMA ch. 7–9 | your module's rule-base code |
| M05 Uncertainty | Blitzstein & Hwang, ch. 1–3 | AIMA ch. 13 |
| M06 Machine learning | scikit-learn user guide | *Elements of Statistical Learning* |
| M07 Neural networks | *Understanding Deep Learning* | PyTorch tutorials |
| M08 NLP | Jurafsky & Martin, ch. 2–8 | Hugging Face course |
| M09 Vision | CS231n notes | OpenCV Python tutorials |
| M10 RL | Sutton & Barto | Spinning Up |
| M11 Generative AI / LLMs | *Understanding Deep Learning*, part III | HF Transformers docs |
| M12 Agents | ReAct (2023) | Lilian Weng's agent post in [agents](library/ai-agents.md) |
| M13 Responsible AI | Molnar, *Interpretable ML* | NIST AI 100-2 |
| M14 Advanced / capstone | the paper closest to your method | model cards + datasheets |

## Access and licensing

The library prefers free and open access, and says which is which:

- **Free / open access** — readable now, no payment. arXiv preprints, university course pages and
  most official documentation fall here. arXiv papers are free to read and cite; the author's
  licence (often CC BY or CC BY-NC-ND) governs redistribution, so link rather than re-upload.
- **Free to use on the site** — a hosted course or tutorial you can read, but which is not licensed
  for copying. Do not reproduce it in your own materials.
- **Paid** — a book or paywalled paper. Most are in university libraries; check before buying.
- **Open-source code** — repositories are usable under their stated licence (Apache-2.0, MIT,
  BSD-3-Clause are common). Read the `LICENSE` file before copying code into your capstone.

No textbook chapters or papers are reproduced in this repository. The library points; it does not
copy. Where a resource is a book, the entry links to the publisher or the author's free edition, not
to a pirated PDF.

## Keeping this useful

A resource that has moved or gone stale is worse than no entry. If a link fails, note the module and
the entry and it will be replaced. The collection is reviewed when modules change; the papers page is
the most volatile, since venues and preprint versions change more often than books do.

---

[Course home](../README.md) · [Textbooks](library/textbooks.md) · [OER](library/open-educational-resources.md) ·
[Documentation](library/official-documentation.md) · [Papers](library/papers-and-surveys.md) · [Glossary](glossary.md)
