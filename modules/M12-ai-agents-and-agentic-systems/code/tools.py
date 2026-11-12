"""tools.py -- the fixed tool set agents may call in M12.

Six tools, chosen so every safety lesson has a concrete case:

    search_docs        read-only, no side effects, safe to call freely
    calculator         pure function, sandboxed AST evaluator (no eval)
    read_note          reads agent memory, rejects path-like ids
    write_note         low-risk side effect inside agent memory
    send_email         EXTERNAL side effect; requires human approval
    escalate_to_human  the safe default when the agent cannot proceed

Design rules, enforced in ``agent_core.ToolRegistry``:

1. Every tool declares a JSON-schema for its arguments; nothing is passed through.
2. Every tool declares a scope; the agent's role must hold that scope.
3. Tools never execute shell commands, open arbitrary paths, or reach the network
   beyond the mocked email transport.
4. Failures return ``status: error`` rather than raising, so the loop can recover.

Run ``python tools.py`` for a smoke test of all six.
"""

from __future__ import annotations

import ast
import operator
import re

from agent_data import DOCS, INITIAL_NOTES

# ---------------------------------------------------------------------------
# Declarations
# ---------------------------------------------------------------------------

TOOL_SPECS = [
    {
        "name": "search_docs",
        "description": "Search the admissions corpus and return the best matching documents.",
        "scope": "read",
        "side_effect": False,
        "requires_approval": False,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "what to look for"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression such as '11800 + 8415'.",
        "scope": "compute",
        "side_effect": False,
        "requires_approval": False,
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "arithmetic only"},
            },
            "required": ["expression"],
        },
    },
    {
        "name": "read_note",
        "description": "Read a stored note by id.",
        "scope": "read",
        "side_effect": False,
        "requires_approval": False,
        "parameters": {
            "type": "object",
            "properties": {"note_id": {"type": "string"}},
            "required": ["note_id"],
        },
    },
    {
        "name": "write_note",
        "description": "Store a short note and return its id. Low risk.",
        "scope": "write",
        "side_effect": True,
        "requires_approval": False,
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "send_email",
        "description": "Send an email. External side effect: always needs human approval.",
        "scope": "external",
        "side_effect": True,
        "requires_approval": True,
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["to", "subject", "body"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": "Hand the conversation to a human adviser with a reason.",
        "scope": "read",
        "side_effect": False,
        "requires_approval": False,
        "parameters": {
            "type": "object",
            "properties": {"reason": {"type": "string"}},
            "required": ["reason"],
        },
    },
]

TOOL_BY_NAME = {s["name"]: s for s in TOOL_SPECS}

# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> set[str]:
    return set(_WORD.findall(text.lower()))


def search_docs(ctx: dict, query: str) -> dict:
    """Keyword search with idf weighting; deterministic and dependency-free."""
    q = _tokens(query)
    if not q:
        return {"status": "error", "error": "empty query"}
    n_docs = len(DOCS)
    df = {}
    for d in DOCS.values():
        toks = _tokens(d["title"] + " " + d["text"])
        for t in q:
            if t in toks:
                df[t] = df.get(t, 0) + 1
    scored = []
    for doc_id, d in DOCS.items():
        toks = _tokens(d["title"] + " " + d["text"])
        score = sum((1.0 + (n_docs - df[t]) / n_docs) for t in q if t in toks)
        # a hit in the title is worth more
        score += 1.5 * sum(1 for t in q if t in _tokens(d["title"]))
        if score > 0:
            scored.append((score, doc_id))
    scored.sort(reverse=True)
    top = [{"id": doc_id, "title": DOCS[doc_id]["title"],
            "text": DOCS[doc_id]["text"], "score": round(score, 3)}
           for score, doc_id in scored[:3]]
    if not top:
        return {"status": "ok", "output": {"results": [],
                                           "note": "no document matched"}}
    return {"status": "ok", "output": {"results": top}}


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod, ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.UAdd: operator.pos}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError("only numeric constants are allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval_node(node.left), _eval_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 12:
            raise ValueError("exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"disallowed syntax: {type(node).__name__}")


def calculator(ctx: dict, expression: str) -> dict:
    """Arithmetic only, via an AST whitelist. No names, no calls, no imports."""
    if len(expression) > 120:
        return {"status": "error", "error": "expression too long"}
    try:
        tree = ast.parse(expression, mode="eval")
        value = _eval_node(tree)
    except Exception as exc:
        return {"status": "error", "error": f"cannot evaluate: {exc}"}
    if isinstance(value, float):
        value = round(value, 6)
    return {"status": "ok", "output": {"expression": expression, "value": value}}


_NOTE_ID = re.compile(r"^note-[a-z0-9-]{1,40}$")


def read_note(ctx: dict, note_id: str) -> dict:
    """Read from agent memory. Ids are validated, so path traversal is impossible."""
    if not _NOTE_ID.match(note_id):
        return {"status": "error",
                "error": "invalid note id: expected note-<slug>, no slashes or dots"}
    notes = ctx["notes"]
    if note_id not in notes:
        return {"status": "error", "error": f"no note with id {note_id}"}
    return {"status": "ok", "output": {"note_id": note_id, "text": notes[note_id]}}


def write_note(ctx: dict, text: str) -> dict:
    """Append to agent memory; the id is generated, never supplied by the model."""
    text = text.strip()
    if not text:
        return {"status": "error", "error": "cannot store an empty note"}
    if len(text) > 500:
        return {"status": "error", "error": "note too long (max 500 characters)"}
    note_id = f"note-{len(ctx['notes']) + 1}"
    ctx["notes"][note_id] = text
    return {"status": "ok", "output": {"note_id": note_id, "text": text}}


_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def send_email(ctx: dict, to: str, subject: str, body: str) -> dict:
    """Mock transport. Reached only after the approval gate; records to ctx['outbox']."""
    if not _EMAIL_RE.match(to):
        return {"status": "error", "error": "invalid email address"}
    if not subject.strip():
        return {"status": "error", "error": "subject is required"}
    ctx.setdefault("outbox", []).append({"to": to, "subject": subject, "body": body})
    return {"status": "ok", "output": {"sent": True, "to": to, "subject": subject,
                                       "bytes": len(body)}}


def escalate_to_human(ctx: dict, reason: str) -> dict:
    ctx.setdefault("escalations", []).append(reason)
    return {"status": "ok", "output": {"escalated": True, "reason": reason}}


HANDLERS = {
    "search_docs": search_docs,
    "calculator": calculator,
    "read_note": read_note,
    "write_note": write_note,
    "send_email": send_email,
    "escalate_to_human": escalate_to_human,
}


def initial_notes() -> dict:
    return dict(INITIAL_NOTES)


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def main() -> None:
    ctx = {"notes": initial_notes()}
    print("=" * 74)
    print("tool smoke test")
    print("=" * 74)
    for spec in TOOL_SPECS:
        print(f"  {spec['name']:18s} scope={spec['scope']:9s} "
              f"side_effect={spec['side_effect']!s:5s} "
              f"approval={spec['requires_approval']!s:5s} "
              f"args={list(spec['parameters']['properties'])}")

    print("\nsearch_docs('ielts english requirement'):")
    out = search_docs(ctx, "ielts english requirement")
    for r in out["output"]["results"]:
        print(f"  {r['id']} {r['title'][:44]:44s} score {r['score']}")

    print("\ncalculator('26400 - 4000'):", calculator(ctx, "26400 - 4000")["output"])
    print("calculator('__import__(\"os\").system(\"echo hi\")'):",
          calculator(ctx, '__import__("os").system("echo hi")'))
    print("calculator('2 ** 99'):", calculator(ctx, "2 ** 99"))

    print("\nwrite_note:", write_note(ctx, "IELTS 6.5 required")["output"])
    print("read_note(note-3):", read_note(ctx, "note-3")["output"])
    print("read_note('../../etc/hosts'):", read_note(ctx, "../../etc/hosts"))
    print("send_email (handler level, no gate):",
          send_email(ctx, "student@example.com", "Fees", "International fee is 26,400 GBP.")["output"])
    print("outbox size:", len(ctx["outbox"]))
    print("escalate:", escalate_to_human(ctx, "visa appeal")["output"])


if __name__ == "__main__":
    main()
