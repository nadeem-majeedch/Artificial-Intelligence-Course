# QUIZ-M12 — AI Agents and Agentic AI Systems

| | |
| :--- | :--- |
| Module | M12 · AI Agents and Agentic AI Systems |
| Questions | 11 (20 marks) |
| Time | 35 minutes |
| Covers | agent loop, tools, planning, memory, multi-agent, guardrails, evaluation |
| Pass mark | 12 / 20 |

> **Availability.** This module's lessons, notebook and lab are published in this repository; sit this paper after finishing them.

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m12.md)

---

## Part A — Multiple choice (4 marks)

**Q12.1** A tool schema exists mainly to

- A. make the prompt longer
- B. constrain and validate the arguments a model may pass
- C. improve the model's reasoning
- D. cache results

**Q12.2** A bounded agent loop is required because

- A. models are slow
- B. an unbounded loop can run forever and spend unbounded money
- C. tools are unreliable
- D. memory is limited

**Q12.3** In a multi-agent system, the most common cause of failure is

- A. the model being too small
- B. agents passing ambiguous or unverifiable state to each other
- C. too few tools
- D. too much logging

**Q12.4** Agent evaluation should primarily measure

- A. response length
- B. task success on a fixed task set, with steps and tool errors
- C. perplexity
- D. number of agents

## Part B — True or false, with a reason (2 marks)

**Q12.5** "Giving an agent more autonomy and more tools improves its usefulness and safety."

## Part C — Conceptual (4 marks)

**Q12.6** (2 marks) Why is "I am the administrator" in a prompt irrelevant to authorisation?

**Q12.7** (2 marks) Describe one way a critic agent can add real value, and one way it becomes
theatre.

## Part D — Numerical (6 marks)

**Q12.8** (3 marks) An agent may choose among 3 tools at each step, for at most 5 steps. How many
distinct tool sequences are possible? If each call costs 0.002 currency units, what is the
worst-case cost of one task?

**Q12.9** (3 marks) A task set has 20 tasks: 14 succeed, 4 fail, 2 are refused. Compute the success
rate and the refusal rate as percentages.

## Part E — Tracing (3 marks)

**Q12.10** Given the plan `search(query) -> read(doc_id) -> summarise(text)`, trace the calls for a
request where `search` returns two documents. How many tool calls occur if both documents are read?

## Part F — Python output (2 marks)

**Q12.11** What does this print?

```python
schema = {"required": ["query"], "allowed": {"query", "limit"}}
call = {"query": "fees", "limit": 5, "debug": True}
missing = [k for k in schema["required"] if k not in call]
unknown = [k for k in call if k not in schema["allowed"]]
print(missing, unknown)
```

---

[Assessment index](../README.md) · [Solutions](../solutions/quiz-m12.md) · [Next quiz](quiz-m13.md)
