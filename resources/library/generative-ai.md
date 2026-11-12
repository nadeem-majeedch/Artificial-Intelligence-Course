# Generative AI

Resources for the generative half of M11: autoencoders, GANs, diffusion models and how to evaluate
what they produce.

[Library index](../README.md) · [LLMs and transformers](llm-and-transformers.md) · [Documentation](official-documentation.md)

---

### Understanding Deep Learning — Part III
**Simon J. D. Prince** · MIT Press, 2023
- **URL:** https://udlbook.github.io/udlbook/
- **Modules:** M11 · **Level:** Intermediate
- **Why:** The clearest textbook treatment of generative modelling: autoencoders, GANs, normalising flows and diffusion, each with the mathematics laid out step by step.
- **Access:** Free PDF from the author; print edition sold by MIT Press.

### Generative Deep Learning, 2nd edition
**David Foster** · O'Reilly, 2023
- **URL:** https://www.oreilly.com/library/view/generative-deep-learning/9781098134174/
- **Modules:** M11 · **Level:** Intermediate
- **Why:** Practical, code-first chapters on VAEs, GANs, diffusion and text generation. Good when you want to build one rather than derive it.
- **Access:** Purchase (O'Reilly); many libraries provide access.

### Hugging Face Diffusers documentation
**Hugging Face** · current release
- **URL:** https://huggingface.co/docs/diffusers/
- **Modules:** M11 · **Level:** Intermediate
- **Why:** Pipelines, schedulers and training scripts for diffusion models, including the tutorials that condition generation on text. The reference for the image-generation labs.
- **Access:** Free; Apache-2.0 licensed.

### The Annotated Diffusion Model
**Rogge and Rasul (Hugging Face blog)** · 2022
- **URL:** https://huggingface.co/blog/annotated-diffusion
- **Modules:** M11 · **Level:** Intermediate
- **Why:** Walks through DDPM line by line, from the forward noising process to the sampling loop, with code for each equation. The best bridge between the paper and working code.
- **Access:** Free to read on the Hugging Face blog.

### Lil'Log: Generative models
**Lilian Weng** · blog series
- **URL:** https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
- **Modules:** M11 · **Level:** Advanced
- **Why:** A rigorous but readable survey of diffusion mathematics, with the derivations the textbook skips. Read after the DDPM paper if the variational bound felt like magic.
- **Access:** Free to read on the author's site.

### Fréchet Inception Distance (FID) — reference implementation
**mseitzer / pytorch-fid** · open-source repository
- **URL:** https://github.com/mseitzer/pytorch-fid
- **Modules:** M11 · **Level:** Intermediate
- **Why:** A small, readable implementation of the metric used to compare generative models. Useful for understanding what FID actually measures — and why it can mislead.
- **Access:** Open source on GitHub under the repository's Apache-2.0 licence.

### Stable Diffusion (model card and code)
**Stability AI / CompVis** · open-source release
- **URL:** https://github.com/CompVis/stable-diffusion
- **Modules:** M11, M13 · **Level:** Intermediate
- **Why:** A real text-to-image system with its model card, limitations and licence in one place. Read the limitations section before using it in a project.
- **Access:** Model weights available under the licence stated on the model card; code open source.

### The Illustrated Stable Diffusion
**Jay Alammar** · blog
- **URL:** https://jalammar.github.io/illustrated-stable-diffusion/
- **Modules:** M11 · **Level:** Beginner
- **Why:** Diagrams the components of a text-to-image pipeline — text encoder, U-Net, scheduler, decoder — so the architecture stops being a list of names.
- **Access:** Free to read on the author's site.

---

[Library index](../README.md) · [LLMs](llm-and-transformers.md) · [Papers](papers-and-surveys.md)
