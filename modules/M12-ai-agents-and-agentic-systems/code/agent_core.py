"""agent_core.py -- a framework-independent agent runtime (M12, L12-01 to L12-03).

The runtime is deliberately small and explicit. Frameworks such as LangGraph,
AutoGen or n8n add ergonomics, persistence and UI, but every one of them
implements these same five pieces:

    the loop        observe -> decide -> act -> observe, until a stop condition
    the registry    tool specs, argument validation, scope checks, audit
    the state       messages, notes, plan, step counter, budget
    the approval    a human gate in front of irreversible actions
    the trace       an ordered record you can evaluate and debug

Learning these here means that when you open a framework you are reading a
configuration of familiar ideas, not a new subject.

Run ``python agent_core.py`` for a scripted demonstration of the loop, the
registry refusing an unauthorised call, and the approval gate.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from tools import HANDLERS, TOOL_BY_NAME, TOOL_SPECS, initial_notes

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

@dataclass
class ToolCall:
    tool: str
    args: dict
    call_id: int = 0


@dataclass
class Step:
    index: int
    thought: str
    call: ToolCall | None
    observation: dict | None
    status: str
    elapsed: float = 0.0


@dataclass
class Trace:
    task: str
    steps: list[Step] = field(default_factory=list)
    answer: str | None = None
    status: str = "running"            # running | done | denied | awaiting_approval | budget
    approval_requests: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "task": self.task,
            "status": self.status,
            "answer": self.answer,
            "steps": [
                {"index": s.index, "thought": s.thought, "status": s.status,
                 "tool": s.call.tool if s.call else None,
                 "args": s.call.args if s.call else None,
                 "observation": s.observation, "elapsed": round(s.elapsed, 4)}
                for s in self.steps
            ],
            "approval_requests": self.approval_requests,
        }


class AuditLog:
    """Append-only, hash-chained log of every tool decision."""

    def __init__(self):
        self.entries: list[dict] = []
        self._prev = "genesis"

    def add(self, **fields) -> dict:
        entry = {"ts": round(time.time(), 3), "prev": self._prev, **fields}
        payload = json.dumps(entry, sort_keys=True, default=str)
        entry["hash"] = hex(abs(hash(payload)))[2:14]
        self._prev = entry["hash"]
        self.entries.append(entry)
        return entry

    def verify(self) -> bool:
        prev = "genesis"
        for entry in self.entries:
            if entry["prev"] != prev:
                return False
            prev = entry["hash"]
        return True


# ---------------------------------------------------------------------------
# Argument validation (JSON-schema subset, no dependency)
# ---------------------------------------------------------------------------

_PY_TYPES = {"string": str, "integer": int, "number": (int, float),
             "boolean": bool, "object": dict, "array": list}


def validate_args(spec: dict, args: dict) -> list[str]:
    """Return a list of problems; empty means valid."""
    problems = []
    params = spec["parameters"]
    if not isinstance(args, dict):
        return ["arguments must be an object"]
    for key in params.get("required", []):
        if key not in args:
            problems.append(f"missing required argument: {key}")
    for key, value in args.items():
        schema = params["properties"].get(key)
        if schema is None:
            problems.append(f"unknown argument: {key}")
            continue
        expected = _PY_TYPES.get(schema.get("type"))
        if expected and not isinstance(value, expected):
            problems.append(f"{key} must be {schema['type']}")
        if schema.get("type") == "integer" and isinstance(value, bool):
            problems.append(f"{key} must be integer")
    return problems


# ---------------------------------------------------------------------------
# Approval gate
# ---------------------------------------------------------------------------

class ApprovalGate:
    """A human decision in front of an irreversible action.

    ``policy`` is a callable ``(request) -> bool``. The default denies, which is
    the correct default: an unattended agent must never be able to send email.
    """

    def __init__(self, policy=None):
        self.policy = policy
        self.pending: list[dict] = []

    def request(self, call: ToolCall, ctx: dict) -> tuple[bool, str]:
        req = {"tool": call.tool, "args": call.args,
               "reason": TOOL_BY_NAME[call.tool].get("description", ""),
               "requires_approval": True}
        self.pending.append(req)
        if self.policy is None:
            return False, "denied: no approval policy configured (default deny)"
        ok = bool(self.policy(req))
        return ok, "approved" if ok else "denied by approver"


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class ToolRegistry:
    """Validates, authorises, executes and audits tool calls."""

    def __init__(self, specs=None, role_scopes=None, audit: AuditLog | None = None,
                 gate: ApprovalGate | None = None):
        self.specs = specs or TOOL_SPECS
        self.by_name = {s["name"]: s for s in self.specs}
        self.role_scopes = role_scopes or {"assistant": {"read", "compute", "write"}}
        self.audit = audit or AuditLog()
        self.gate = gate or ApprovalGate()
        self.call_count = 0

    def execute(self, call: ToolCall, ctx: dict) -> dict:
        spec = self.by_name.get(call.tool)
        if spec is None:
            return self._fail(call, ctx, "unknown_tool", f"no tool named {call.tool}")
        if self.call_count >= ctx.get("max_tool_calls", 12):
            return self._fail(call, ctx, "budget_exceeded", "tool-call budget exhausted")

        allowed = set()
        for role in ctx.get("roles", []):
            allowed |= self.role_scopes.get(role, set())
        if spec["scope"] not in allowed:
            return self._fail(call, ctx, "scope_denied",
                              f"role lacks scope {spec['scope']!r}")

        problems = validate_args(spec, call.args)
        if problems:
            return self._fail(call, ctx, "invalid_arguments", "; ".join(problems))

        if spec["requires_approval"]:
            approved, reason = self.gate.request(call, ctx)
            if not approved:
                return self._fail(call, ctx, "approval_denied", reason)

        self.call_count += 1
        t0 = time.perf_counter()
        try:
            result = HANDLERS[call.tool](ctx, **call.args)
        except Exception as exc:                    # handler bugs must not kill the loop
            result = {"status": "error", "error": f"handler crashed: {exc!r}"}
        elapsed = time.perf_counter() - t0
        self.audit.add(tool=call.tool, args=call.args, status=result["status"],
                       elapsed=round(elapsed, 6))
        return result

    def _fail(self, call: ToolCall, ctx: dict, code: str, message: str) -> dict:
        self.audit.add(tool=call.tool, args=call.args, status=code, error=message)
        return {"status": "error", "error": message, "code": code}


# ---------------------------------------------------------------------------
# Policies
# ---------------------------------------------------------------------------

class ScriptedPolicy:
    """A fixed list of actions; used by tests and by labs that isolate the loop."""

    def __init__(self, actions: list[dict]):
        self.actions = actions
        self.i = 0

    def next_action(self, task: str, trace: Trace, ctx: dict) -> dict:
        if self.i >= len(self.actions):
            return {"thought": "script exhausted", "final": "script complete"}
        action = self.actions[self.i]
        self.i += 1
        return action


class RulePolicy:
    """A keyword baseline with no language model: search, then quote.

    It exists to prove the harness works and to give the model-based policies a
    floor to beat. It is not intended to be good.
    """

    def __init__(self):
        self.stage = 0

    def next_action(self, task: str, trace: Trace, ctx: dict) -> dict:
        lowered = task.lower()
        if any(p in lowered for p in ("ignore your instructions", "attacker@", "database")):
            return {"thought": "policy violation", "final":
                    "I cannot do that: it conflicts with my operating rules."}
        if self.stage == 0 and any(w in lowered for w in ("email", "send")):
            return {"thought": "sending requires approval", "final":
                    "I need approval before sending email."}
        if self.stage == 0:
            self.stage = 1
            return {"thought": "search the corpus", "tool": "search_docs",
                    "args": {"query": task}}
        results = []
        for step in trace.steps:
            if step.observation and step.observation.get("status") == "ok":
                out = step.observation.get("output", {})
                results.extend(out.get("results", []))
        if not results:
            return {"thought": "nothing found", "final":
                    "I could not find that in the corpus."}
        best = results[0]
        numbers = [t for t in best["text"].replace(",", "").split()
                   if t.replace(".", "").isdigit()]
        answer = best["text"]
        if numbers:
            answer = f"{answer} (figures: {', '.join(numbers[:4])})"
        return {"thought": "answer from top document", "final": answer}


class LLMPolicy:
    """A local flan-t5-small policy that must emit JSON tool calls.

    Every parse failure is recorded. The measured parse rate is the lesson: a
    77M-parameter model cannot be trusted to produce structured actions, which
    is why real agents use larger models or grammar-constrained decoding.
    """

    PROMPT = """You control an assistant with these tools:
{tools}
Reply with JSON only, one of:
{{"tool": "<name>", "args": {{...}}}}
{{"final": "<answer>"}}

Question: {task}
Previous observations: {history}
JSON:"""

    def __init__(self, model_name: str = "google/flan-t5-small", max_retries: int = 2):
        self.model_name = model_name
        self.max_retries = max_retries
        self.parse_failures = 0
        self.calls = 0
        self._tok = None
        self._model = None

    def _load(self):
        if self._model is None:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

            self._tok = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self._model.eval()
        return self._tok, self._model

    def _generate(self, prompt: str) -> str:
        import torch

        tok, model = self._load()
        enc = tok(prompt, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=48, do_sample=False)
        return tok.decode(out[0], skip_special_tokens=True).strip()

    def parse(self, raw: str) -> dict | None:
        start, end = raw.find("{"), raw.rfind("}")
        if start == -1 or end <= start:
            return None
        try:
            obj = json.loads(raw[start:end + 1])
        except json.JSONDecodeError:
            return None
        if not isinstance(obj, dict):
            return None
        if "final" in obj and isinstance(obj["final"], str):
            return {"final": obj["final"]}
        if "tool" in obj and isinstance(obj.get("args", {}), dict):
            return {"tool": obj["tool"], "args": obj.get("args", {})}
        return None

    def next_action(self, task: str, trace: Trace, ctx: dict) -> dict:
        history = []
        for step in trace.steps[-3:]:
            if step.call:
                history.append(f"{step.call.tool}({step.call.args}) -> "
                               f"{step.observation.get('status') if step.observation else '?'}")
        prompt = self.PROMPT.format(tools=ctx["tool_catalogue"], task=task,
                                    history=" | ".join(history) or "none")
        last_error = ""
        for attempt in range(self.max_retries + 1):
            self.calls += 1
            raw = self._generate(prompt + (f"\nPrevious attempt failed: {last_error}"
                                          if last_error else ""))
            action = self.parse(raw)
            if action:
                action.setdefault("thought", f"model action (attempt {attempt + 1})")
                return action
            last_error = "not valid JSON with tool/args or final"
        self.parse_failures += 1
        return {"thought": "model failed to produce a valid action",
                "final": "I could not decide on a valid action."}


# ---------------------------------------------------------------------------
# The loop
# ---------------------------------------------------------------------------

class AgentLoop:
    """Observe -> decide -> act -> observe, bounded by steps and tool calls."""

    def __init__(self, policy, registry: ToolRegistry | None = None,
                 max_steps: int = 8, roles=("assistant",)):
        self.policy = policy
        self.registry = registry or ToolRegistry()
        self.max_steps = max_steps
        self.roles = list(roles)

    def new_context(self, notes: dict | None = None, **extra) -> dict:
        ctx = {"notes": notes if notes is not None else initial_notes(),
               "roles": self.roles, "max_tool_calls": 12,
               "tool_catalogue": _catalogue_text()}
        ctx.update(extra)
        return ctx

    def run(self, task: str, ctx: dict | None = None) -> Trace:
        ctx = ctx or self.new_context()
        trace = Trace(task=task)
        for i in range(self.max_steps):
            if self.registry.call_count >= ctx["max_tool_calls"]:
                trace.status = "budget"
                return trace
            action = self.policy.next_action(task, trace, ctx)
            thought = action.get("thought", "")
            if "final" in action:
                trace.answer = action["final"]
                trace.status = "done"
                trace.steps.append(Step(i, thought, None, None, "final"))
                return trace
            call = ToolCall(action["tool"], action.get("args", {}), i)
            t0 = time.perf_counter()
            observation = self.registry.execute(call, ctx)
            elapsed = time.perf_counter() - t0
            trace.steps.append(Step(i, thought, call, observation,
                                    observation.get("code") or observation["status"], elapsed))
            if observation.get("code") == "approval_denied":
                trace.status = "awaiting_approval"
                trace.approval_requests = list(self.registry.gate.pending)
                return trace
        trace.status = "budget"
        return trace


def _catalogue_text() -> str:
    lines = ["Available tools:"]
    for spec in TOOL_SPECS:
        args = ", ".join(f"{k}: {v['type']}" for k, v in
                         spec["parameters"]["properties"].items())
        lines.append(f"- {spec['name']}({args}) -> {spec['description']}")
    return "\n".join(lines)


def approve_all(req: dict) -> bool:
    """A permissive approver for demonstrations and tests. Never use in production."""
    return True


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 78)
    print("1. A scripted loop: search, calculate, answer")
    print("=" * 78)
    actions = [
        {"thought": "find the fees", "tool": "search_docs", "args": {"query": "international tuition fee"}},
        {"thought": "subtract the award", "tool": "calculator",
         "args": {"expression": "26400 - 4000"}},
        {"thought": "compose the answer", "final": "You would pay 22,400 GBP."},
    ]
    loop = AgentLoop(ScriptedPolicy(actions))
    trace = loop.run("What will I pay after the merit award?")
    for step in trace.steps:
        if step.call:
            obs = step.observation
            summary = obs.get("output") if obs["status"] == "ok" else obs.get("error")
            print(f"  step {step.index}: {step.call.tool}({step.call.args}) -> "
                  f"{str(summary)[:70]}")
        else:
            print(f"  step {step.index}: {step.thought}")
    print("  status:", trace.status, "| answer:", trace.answer)
    print("  audit entries:", len(loop.registry.audit.entries), "| chain valid:",
          loop.registry.audit.verify())

    print("\n" + "=" * 78)
    print("2. Permissions: the same call from a role without the scope")
    print("=" * 78)
    reg = ToolRegistry(role_scopes={"reader": {"read", "compute"},
                                    "assistant": {"read", "compute", "write", "external"}})
    read_only = AgentLoop(ScriptedPolicy([
        {"thought": "store a note", "tool": "write_note", "args": {"text": "hello"}},
    ]), registry=reg, roles=("reader",))
    t = read_only.run("store a note")
    print("  reader ->", t.steps[0].observation)
    reg2 = ToolRegistry()
    writer = AgentLoop(ScriptedPolicy([
        {"thought": "store a note", "tool": "write_note", "args": {"text": "hello"}},
    ]), registry=reg2, roles=("assistant",))
    t2 = writer.run("store a note")
    print("  assistant ->", t2.steps[0].observation["output"])

    print("\n" + "=" * 78)
    print("3. Approval gate: default deny, then an explicit approver")
    print("=" * 78)
    call = ToolCall("send_email", {"to": "student@example.com", "subject": "Fees",
                                   "body": "International fee: 26,400 GBP."})
    loop_deny = AgentLoop(ScriptedPolicy([{"thought": "email", "tool": "send_email",
                                           "args": call.args}]),
                          registry=ToolRegistry(gate=ApprovalGate()))
    t3 = loop_deny.run("email me the fees")
    print("  default deny ->", t3.status, "|", t3.steps[0].observation["error"])

    loop_ok = AgentLoop(ScriptedPolicy([{"thought": "email", "tool": "send_email",
                                         "args": call.args}]),
                        registry=ToolRegistry(gate=ApprovalGate(approve_all)))
    ctx = loop_ok.new_context()
    t4 = loop_ok.run("email me the fees", ctx)
    print("  approved ->", t4.status, "| outbox:", len(ctx["outbox"]))

    print("\n" + "=" * 78)
    print("4. Injection and bad arguments are rejected before execution")
    print("=" * 78)
    bad = AgentLoop(ScriptedPolicy([
        {"thought": "path traversal", "tool": "read_note",
         "args": {"note_id": "../../etc/hosts"}},
        {"thought": "unknown arg", "tool": "calculator",
         "args": {"expression": "2+2", "shell": "rm -rf /"}},
        {"thought": "unknown tool", "tool": "delete_all", "args": {}},
    ]))
    t5 = bad.run("try unsafe calls")
    for step in t5.steps:
        print(f"  {step.call.tool:14s} -> {step.observation['code']}: "
              f"{step.observation['error']}")


if __name__ == "__main__":
    main()
