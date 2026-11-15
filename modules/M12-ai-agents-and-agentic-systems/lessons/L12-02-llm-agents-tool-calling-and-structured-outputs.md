# L12-02 — LLM Agents, Tool Calling and Structured Outputs

| Module | M12 · AI Agents and Agentic AI Systems |
| :--- | :--- |
| Level | 400 |
| Study time | 80 minutes |
| Prerequisites | [L12-01](L12-01-foundations-and-architecture-of-ai-agents.md) · [L11-04](../../M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md) |
| Code | `code/tools.py`, `code/agent_core.py` |

[← Previous: L12-01](L12-01-foundations-and-architecture-of-ai-agents.md) · [Next: L12-03 Planning and Memory →](L12-03-planning-memory-and-workflow-orchestration.md)

## 1. Learning Objectives

- **Define** tools with schemas rather than prose, and validate arguments before execution.
- **Distinguish** a tool call from an authorisation: the model proposes, the host decides.
- **Implement** structured output with a parser that fails safely.
- **Measure** how schema strictness changes malformed-call rate.

## 2. Prerequisite Knowledge

The agent loop from [L12-01](L12-01-foundations-and-architecture-of-ai-agents.md), and prompting
with examples from [L11-04](../../M11-generative-ai-and-large-language-models/lessons/L11-04-prompt-engineering-and-in-context-learning.md).

## 3. Conceptual Explanation

### 3.1 Tools are interfaces, not suggestions

A tool is a function with a name, a description, a parameter schema and a return schema. The model
sees the schema and emits a call; the host validates the call against the schema and executes it.
Everything security-relevant follows from that split: the model never executes anything.

### 3.2 Structured outputs

Free-text output forces the host to parse prose, which fails unpredictably. A schema-constrained
output — JSON with required fields, enums for categories, and a refusal field — turns "the model
said something odd" into "validation failed", which is testable.

### 3.3 The validation boundary

| Layer | Enforces | If missing |
| :--- | :--- | :--- |
| Schema | types, required fields, enums | runtime `KeyError`, wrong tool invoked |
| Permission | which tools this user/session may call | privilege escalation |
| Side-effect policy | read vs write, spend limits | irreversible damage |
| Idempotency | retries do not duplicate effects | double refunds |

### 3.4 Retries need a stopping rule

A malformed call is often fixable by returning the validation error to the model. That retry must be
bounded (two attempts), and it must not apply to authorisation failures — retrying a forbidden
action is how an agent turns a denial into a loop.

## 4. Pseudocode

```text
function CALL_TOOL(name, args, schemas, permissions):
    if name not in schemas: return error("unknown_tool")
    if not permitted(name, permissions): return error("not_permitted")
    if not validates(args, schemas[name]): return error("invalid_arguments", detail)
    return execute(name, args)          # host code, never generated code
```

## 5. Worked Example — a schema that prevents a class of bugs

Tool `refund(order_id: str, amount: float)` with `amount > 0` and `amount <= order_total`.

| Call | Result |
| :--- | :--- |
| `refund("4471", 25.0)` | executed |
| `refund(4471, 25)` | rejected: `order_id` must be a string |
| `refund("4471", -5)` | rejected: amount must be positive |
| `refund("4471", 500)` | rejected: exceeds order total |

Without the schema, the third and fourth calls would reach the payment API. Validation is cheaper
than a reversal.

## 6. Mathematical Formulation

Malformed-call rate with and without schema constraint, over $n$ calls:

$$\text{MCR} = \frac{1}{n}\sum_{i=1}^{n} \mathbb{1}[\text{validate}(c_i) = \text{false}]$$

A useful agent target is MCR below 2% *after* one bounded repair attempt; higher means the schema or
the description is wrong, not the model.

## 7. Python Implementation

```python
import json

SCHEMAS = {
    "refund": {"order_id": str, "amount": float},
    "lookup_order": {"order_id": str},
}


def validate(name, args):
    schema = SCHEMAS.get(name)
    if schema is None:
        return "unknown_tool"
    for key, typ in schema.items():
        if key not in args:
            return f"missing {key}"
        if not isinstance(args[key], typ):
            return f"{key} must be {typ.__name__}"
    extra = set(args) - set(schema)
    return f"unexpected {sorted(extra)}" if extra else None


def parse(raw):
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"invalid_json: {exc.msg}"
    if obj.get("type") != "tool_call":
        return None, "not_a_tool_call"
    problem = validate(obj["name"], obj.get("args", {}))
    return (None, problem) if problem else (obj, None)


ok, err = parse('{"type":"tool_call","name":"refund","args":{"order_id":"4471","amount":25.0}}')
print("accepted:", ok is not None, "error:", err)
ok, err = parse('{"type":"tool_call","name":"refund","args":{"order_id":4471,"amount":25}}')
print("accepted:", ok is not None, "error:", err)
```

## 8. Practical Applications

- **Ticketing** — `create_ticket`, `assign`, `close`, each with schema and permission.
- **Finance operations** — read-only tools for analysis, write tools behind approval.
- **Coding assistants** — file read, patch, run tests; the patch tool is the only write path.
- **Data pipelines** — query tools with row limits, so a bad query cannot scan a warehouse.

## 9. Common Mistakes

- Describing tools in prose and hoping the model formats arguments correctly.
- Accepting extra fields "just in case", which lets a model smuggle in unauthorised parameters.
- Retrying authorisation failures.
- Returning raw exceptions to the model, leaking internals and inviting exploitation.
- Making the write tool and the read tool the same function with a flag.

## 10. Exercises

1. Add an `enum` constraint to a `priority` argument and show which invalid values it rejects.
2. Implement the bounded repair loop (two attempts) and measure the recovery rate on five malformed calls.
3. Write a permission layer that blocks `refund` for a read-only session, and test it.
4. Design schemas for three tools in a domain you know, then list what each schema prevents.

## 11. Self-Assessment

1. Who executes a tool call, and why does that matter for security?
2. What does schema validation convert a vague failure into?
3. Why must authorisation failures not be retried?
4. What is a reasonable malformed-call target after one repair attempt?

## 12. Key Terms

**Tool schema**, **function calling**, **structured output**, **validation boundary**, **permission**, **idempotency**, **repair attempt**.

## 13. Further Reading

- Yao et al. (2022), ReAct; Schick et al. (2023), Toolformer.
- The JSON Schema specification, for the constraint vocabulary.

## What to Do Next

[L12-03](L12-03-planning-memory-and-workflow-orchestration.md) adds planning and memory, the two
components that make multi-step work possible — and the two that make it unpredictable.
