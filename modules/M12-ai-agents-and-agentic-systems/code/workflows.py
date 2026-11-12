"""workflows.py -- sequential, conditional, iterative and plan-execute workflows (M12, L12-03).

A workflow is a graph of steps with explicit state. The four patterns below cover
most agent products:

    sequential      A -> B -> C, each step reads and writes shared state
    conditional     a router chooses one branch, then continues
    iterative       draft -> critique -> revise until a check passes or budget ends
    plan-execute    a plan is produced, executed step by step, and revised on failure

Also here: a JSON state store with provenance, retry with backoff, and a
fallback/escalation path -- the parts that make a workflow survive production.

Run ``python workflows.py`` for the traces and step counts quoted in L12-03.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from agent_core import AgentLoop, ScriptedPolicy, ToolRegistry
from guardrails import Budget


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class StateStore:
    """A JSON-backed state object. Every write records who wrote it and when."""

    def __init__(self, path: str | Path | None = None):
        self.data: dict = {}
        self.history: list[dict] = []
        self.path = Path(path) if path else None

    def write(self, key: str, value, author: str) -> None:
        self.data[key] = value
        self.history.append({"key": key, "author": author, "version": len(self.history) + 1,
                             "ts": round(time.time(), 3)})

    def read(self, key: str, default=None):
        return self.data.get(key, default)

    def save(self) -> None:
        if self.path:
            self.path.write_text(json.dumps({"data": self.data, "history": self.history},
                                            indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path):
        store = cls(path)
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        store.data, store.history = payload["data"], payload["history"]
        return store


# ---------------------------------------------------------------------------
# Reusable step helpers
# ---------------------------------------------------------------------------

def retry(fn, attempts: int = 3, base_delay: float = 0.0, on_error=None):
    """Call ``fn`` until it succeeds; return (result, attempts_used, errors)."""
    errors = []
    for i in range(attempts):
        try:
            result = fn()
            if result.get("status") == "error":
                errors.append(result.get("error"))
                continue
            return result, i + 1, errors
        except Exception as exc:
            errors.append(repr(exc))
            if base_delay:
                time.sleep(base_delay * (2 ** i))
    if on_error:
        return on_error(), attempts, errors
    return {"status": "error", "error": "all attempts failed", "errors": errors}, attempts, errors


def tool_step(tool: str, args_fn, ctx_key: str = "tool_results"):
    """Build a workflow step that calls one tool and records the result in state."""

    def step(state: StateStore, ctx: dict) -> dict:
        from agent_core import ToolCall

        registry = ctx["registry"]
        args = args_fn(state.data)
        result = registry.execute(ToolCall(tool, args), ctx)
        state.write(ctx_key, {"tool": tool, "args": args, "result": result}, author=f"tool:{tool}")
        return result

    return step


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

class SequentialWorkflow:
    """Run steps in order; stop at the first hard failure unless a step is optional."""

    def __init__(self, steps, name: str = "sequential"):
        self.steps = steps
        self.name = name

    def run(self, state: StateStore, ctx: dict) -> dict:
        trace = []
        for index, (label, step) in enumerate(self.steps):
            t0 = time.perf_counter()
            result = step(state, ctx)
            status = result.get("status", "ok") if isinstance(result, dict) else "ok"
            trace.append({"step": index, "label": label, "status": status,
                          "elapsed": round(time.perf_counter() - t0, 4)})
            if status == "error":
                return {"workflow": self.name, "status": "failed", "failed_at": label,
                        "trace": trace}
        return {"workflow": self.name, "status": "done", "trace": trace}


class ConditionalWorkflow:
    """A router picks exactly one branch; both branches converge on a final step."""

    def __init__(self, router, branches: dict, final_step, name: str = "conditional"):
        self.router, self.branches, self.final_step, self.name = router, branches, final_step, name

    def run(self, state: StateStore, ctx: dict) -> dict:
        branch = self.router(state.data)
        t0 = time.perf_counter()
        result = self.branches[branch](state, ctx)
        branch_status = result.get("status", "ok")
        tail = self.final_step(state, ctx)
        return {"workflow": self.name, "branch": branch, "status": tail.get("status", "ok"),
                "branch_status": branch_status,
                "elapsed": round(time.perf_counter() - t0, 4)}


class IterativeWorkflow:
    """Draft, critique, revise -- stop when the check passes or iterations run out."""

    def __init__(self, draft, critique, revise, check, max_iterations: int = 3,
                 name: str = "iterative"):
        self.draft, self.critique, self.revise = draft, critique, revise
        self.check, self.max_iterations, self.name = check, max_iterations, name

    def run(self, state: StateStore, ctx: dict) -> dict:
        state.write("draft", self.draft(state.data), author="drafter")
        log = []
        for i in range(self.max_iterations):
            verdict = self.critique(state.data["draft"])
            log.append({"iteration": i + 1, "score": verdict["score"],
                        "issues": verdict["issues"][:3]})
            if self.check(verdict):
                return {"workflow": self.name, "status": "done", "iterations": i + 1,
                        "converged": True, "log": log}
            state.write("draft", self.revise(state.data["draft"], verdict), author="reviser")
        return {"workflow": self.name, "status": "budget", "iterations": self.max_iterations,
                "converged": False, "log": log}


class PlanExecuteWorkflow:
    """Plan first, then execute; replan once if a step fails."""

    def __init__(self, planner, executor, max_replans: int = 1, name: str = "plan-execute"):
        self.planner, self.executor = planner, executor
        self.max_replans, self.name = max_replans, name

    def run(self, task: str, state: StateStore, ctx: dict) -> dict:
        plan = self.planner(task, state.data)
        state.write("plan", plan, author="planner")
        executed, replans = [], 0
        while plan:
            step = plan.pop(0)
            result = self.executor(step, state, ctx)
            executed.append({"step": step, "status": result.get("status", "ok")})
            if result.get("status") == "error" and replans < self.max_replans:
                replans += 1
                plan = self.planner(task, state.data, failed=step)
                state.write("plan", plan, author="replanner")
        return {"workflow": self.name, "status": "done", "executed": executed,
                "replans": replans}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    registry = ToolRegistry()
    ctx = {"notes": {}, "roles": ["assistant"], "max_tool_calls": 12,
           "tool_catalogue": "", "registry": registry}
    ctx["notes"] = {"note-seed-1": "Applicant needs IELTS 6.5."}

    print("=" * 82)
    print("1. Sequential: search -> calculate -> answer")
    print("=" * 82)
    state = StateStore()
    wf = SequentialWorkflow([
        ("search", tool_step("search_docs", lambda d: {"query": "international tuition fee"})),
        ("calculate", tool_step("calculator", lambda d: {"expression": "26400 - 4000"})),
    ])
    out = wf.run(state, ctx)
    print("  status:", out["status"], "| steps:", len(out["trace"]))
    for t in out["trace"]:
        print(f"    {t['label']:10s} {t['status']:6s} {t['elapsed']:.4f}s")
    print("  state keys:", list(state.data), "| history entries:", len(state.history))
    print("  calculator result:", state.read("tool_results")["result"]["output"])

    print("\n" + "=" * 82)
    print("2. Conditional: route on whether the question mentions a fee")
    print("=" * 82)

    def router(data):
        q = data.get("question", "")
        return "fees" if any(w in q.lower() for w in ("fee", "cost", "pay")) else "general"

    def branch_fees(state, ctx):
        state.write("answer", "International tuition is 26,400 GBP.", author="fees-branch")
        return {"status": "ok"}

    def branch_general(state, ctx):
        state.write("answer", "Please see the admissions pages.", author="general-branch")
        return {"status": "ok"}

    def finalise(state, ctx):
        state.write("final", state.read("answer"), author="finaliser")
        return {"status": "ok"}

    for question in ("What are the fees?", "Where is the campus?"):
        state = StateStore()
        state.write("question", question, author="user")
        out = ConditionalWorkflow(router, {"fees": branch_fees, "general": branch_general},
                                  finalise).run(state, ctx)
        print(f"  {question!r:30s} -> branch {out['branch']:8s} final {state.read('final')!r}")

    print("\n" + "=" * 82)
    print("3. Iterative: draft, critique, revise")
    print("=" * 82)

    def draft(data):
        return "The fee is 26400 GBP."

    def critique(text):
        issues = []
        if "26,400" not in text:
            issues.append("number not formatted with a comma")
        if "per year" not in text:
            issues.append("missing period")
        return {"score": len(issues), "issues": issues}

    def revise(text, verdict):
        if "number not formatted" in " ".join(verdict["issues"]):
            text = text.replace("26400", "26,400")
        if "missing period" in verdict["issues"]:
            text += " per year"
        return text

    state = StateStore()
    out = IterativeWorkflow(draft, critique, revise, lambda v: v["score"] == 0).run(state, ctx)
    print("  status:", out["status"], "| iterations:", out["iterations"],
          "| converged:", out["converged"])
    print("  final draft:", state.read("draft"))
    for entry in out["log"]:
        print("   ", entry)

    print("\n" + "=" * 82)
    print("4. Plan and execute, with one replan on failure")
    print("=" * 82)

    def planner(task, data, failed=None):
        if failed:
            return [{"tool": "escalate_to_human", "args": {"reason": "search failed"}}]
        return [{"tool": "search_docs", "args": {"query": "ielts requirement"}},
                {"tool": "search_docs", "args": {"query": ""}}]

    def executor(step, state, ctx):
        from agent_core import ToolCall

        return registry.execute(ToolCall(step["tool"], step["args"]), ctx)

    state = StateStore()
    out = PlanExecuteWorkflow(planner, executor).run("What IELTS do I need?", state, ctx)
    print("  status:", out["status"], "| replans:", out["replans"])
    for row in out["executed"]:
        print(f"    {row['step']['tool']:18s} {row['status']}")
    print("  escalation recorded:", state.read("tool_results")["result"].get("output"))

    print("\n" + "=" * 82)
    print("5. Retry with fallback")
    print("=" * 82)
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        return {"status": "error", "error": "timeout"} if calls["n"] < 3 else \
            {"status": "ok", "output": "recovered"}

    result, used, errors = retry(flaky, attempts=3,
                                 on_error=lambda: {"status": "ok", "output": "fallback"})
    print(f"  attempts {used}, errors {errors}, result {result['output']}")

    print("\n" + "=" * 82)
    print("6. Budget enforcement inside a workflow")
    print("=" * 82)
    budget = Budget(max_tool_calls=2)
    for i in range(4):
        allowed = budget.charge_tool(0.1)
        print(f"  tool call {i + 1}: allowed={allowed} exhausted={budget.exhausted()}")


if __name__ == "__main__":
    main()
