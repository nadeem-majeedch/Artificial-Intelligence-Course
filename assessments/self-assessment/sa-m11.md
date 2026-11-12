# SA-M11 — Self-Assessment: Generative AI and LLMs

Module M11 · [Module](../../modules/M11-generative-ai-and-large-language-models/README.md) · [Quiz](../quizzes/quiz-m11.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Explain next-token prediction and how it yields generation
- [ ] Compute and interpret perplexity
- [ ] Describe the pretraining → instruction tuning → preference tuning pipeline
- [ ] Explain temperature, top-k and top-p, and their trade-offs
- [ ] Distinguish prompting, retrieval and fine-tuning as interventions
- [ ] Explain LoRA and when it is preferable to full fine-tuning
- [ ] State why perplexity is not comparable across tokenisers

## Knowledge-check questions

1. Mean NLL is 1.2 nats/token. What is the perplexity?
2. Why does a higher temperature not change the argmax but change the sample?
3. What does instruction tuning change that pretraining does not?
4. Give one failure retrieval cannot fix, and explain why.
5. LoRA on a $768\times768$ matrix with $r=16$: how many trainable parameters?

## Practical competency checklist

- [ ] Build a prompt with explicit delimiters and an output contract
- [ ] Measure answer quality on a fixed question set
- [ ] Test refusal on unanswerable questions
- [ ] Report cost and latency alongside quality

## Suggested revision topics

Language modelling objective · decoding strategies · scaling and alignment · prompting ·
retrieval augmentation · parameter-efficient fine-tuning · evaluation and hallucination.

## Readiness test for M12

Without notes:

1. Compute perplexity from a mean NLL.
2. Explain what LoRA trains and what it freezes.
3. Name the three interventions for adding knowledge and when each is appropriate.

If any is shaky, revisit L11-02 and L11-06 before M12.
