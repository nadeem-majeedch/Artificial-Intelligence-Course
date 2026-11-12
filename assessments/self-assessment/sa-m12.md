# SA-M12 — Self-Assessment: AI Agents

Module M12 · [Module](../../docs/CURRICULUM-MAP.md) · [Quiz](../quizzes/quiz-m12.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Describe the agent loop: plan, act, observe, update
- [ ] Write a tool schema and validate arguments
- [ ] Explain planning vs reacting and when each is appropriate
- [ ] Describe short-term and long-term memory in an agent
- [ ] Identify coordination failure modes in multi-agent systems
- [ ] State why loops need step and cost bounds
- [ ] Explain why prompt claims are not authorisation

## Knowledge-check questions

1. Why must a tool schema reject unknown keys?
2. What is the difference between an agent's memory and its context window?
3. Give one multi-agent failure that a single agent would not have.
4. Why is "the agent said it succeeded" not evidence of success?
5. What should be logged for every tool call?

## Practical competency checklist

- [ ] Implement a tool-calling loop with a step cap
- [ ] Handle tool exceptions and empty results
- [ ] Add default-deny permissions
- [ ] Evaluate on a fixed task set with success, steps and errors

## Suggested revision topics

Agent architectures · tool calling and schemas · planning · memory · multi-agent coordination ·
guardrails and permissions · evaluation and logging.

## Readiness test for M13

Without notes:

1. Write a JSON schema for a `search` tool with a required query and a limit.
2. Explain two guardrails and the failure each prevents.
3. Design a 10-task evaluation for an agent in one paragraph.

If any is shaky, revisit L12-03 and L12-06 before M13.
