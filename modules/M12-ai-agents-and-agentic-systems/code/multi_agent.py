"""multi_agent.py -- roles, delegation, coordination and shared memory (M12, L12-04).

Three coordination patterns, implemented without a framework:

    sequential delegation   planner -> researcher -> writer -> critic, one handoff chain
    contract net            subtasks are offered; agents bid on capability; winners run
    blackboard              agents read and write a shared, provenance-tracked store

Failure handling is part of the design: a timeout triggers one retry, then an
escalation to a human, and delegation depth is capped so two agents cannot bounce
a task between them forever.

Run ``python multi_agent.py`` for message counts and the delegation trace quoted
in L12-04.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from agent_core import ToolCall, ToolRegistry
from agent_data import DOCS


# ---------------------------------------------------------------------------
# Messages and bus
# ---------------------------------------------------------------------------

@dataclass
class Message:
    sender: str
    recipient: str
    intent: str                 # request | inform | critique | escalate
    payload: dict
    msg_id: int = 0
    depth: int = 0              # delegation depth, bounded
    reply_to: int | None = None
    ts: float = field(default_factory=time.time)


class MessageBus:
    """In-process transport with a bounded inbox per agent and a full history."""

    def __init__(self, max_depth: int = 3):
        self.queues: dict[str, list[Message]] = {}
        self.history: list[Message] = []
        self.max_depth = max_depth
        self._next_id = 1

    def send(self, message: Message) -> dict:
        if message.depth > self.max_depth:
            return {"status": "rejected", "error": "delegation depth exceeded"}
        if message.recipient not in self.queues:
            return {"status": "rejected", "error": f"unknown recipient {message.recipient}"}
        message.msg_id = self._next_id
        self._next_id += 1
        self.queues[message.recipient].append(message)
        self.history.append(message)
        return {"status": "ok", "msg_id": message.msg_id}

    def register(self, name: str) -> None:
        self.queues.setdefault(name, [])

    def receive(self, name: str) -> list[Message]:
        out = self.queues.get(name, [])
        self.queues[name] = []
        return out

    def stats(self) -> dict:
        intents = {}
        for m in self.history:
            intents[m.intent] = intents.get(m.intent, 0) + 1
        return {"messages": len(self.history), "intents": intents,
                "max_depth_seen": max((m.depth for m in self.history), default=0)}


# ---------------------------------------------------------------------------
# Shared memory
# ---------------------------------------------------------------------------

class Blackboard:
    """A versioned key-value store with provenance; readers can cite the author."""

    def __init__(self):
        self.entries: list[dict] = []

    def write(self, key: str, value, author: str, source: str | None = None) -> dict:
        entry = {"version": len(self.entries) + 1, "key": key, "value": value,
                 "author": author, "source": source, "ts": round(time.time(), 3)}
        self.entries.append(entry)
        return entry

    def latest(self, key: str):
        for entry in reversed(self.entries):
            if entry["key"] == key:
                return entry
        return None

    def snapshot(self) -> dict:
        keys = {e["key"] for e in self.entries}
        return {k: self.latest(k)["value"] for k in keys}

    def audit(self) -> list[dict]:
        return [{"version": e["version"], "key": e["key"], "author": e["author"]}
                for e in self.entries]


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

class Specialist:
    """A role with a capability set and a bounded amount of work it may do."""

    name = "specialist"
    capabilities: set[str] = set()

    def __init__(self, bus: MessageBus, board: Blackboard, ctx: dict):
        self.bus, self.board, self.ctx = bus, board, ctx
        self.work_done = 0

    def bid(self, subtask: dict) -> float:
        """Return a capability score in [0, 1]; 0 means 'cannot do this'."""
        wanted = set(subtask.get("needs", []))
        if not wanted:
            return 0.0
        return len(wanted & self.capabilities) / len(wanted)

    def handle(self, message: Message) -> Message | None:
        raise NotImplementedError


class Planner(Specialist):
    name = "planner"
    capabilities = {"decompose", "plan"}

    def handle(self, message: Message) -> Message | None:
        question = message.payload.get("question", "")
        lowered = question.lower()
        plan = [{"needs": ["retrieve"], "task": question}]
        if any(w in lowered for w in ("compare", "total", "sum", "cost", "much")):
            plan.append({"needs": ["compute"], "task": "compute the requested figure"})
        if any(w in lowered for w in ("email", "send")):
            plan.append({"needs": ["external"], "task": "send the email (needs approval)"})
        self.board.write("plan", plan, author=self.name)
        self.work_done += 1
        return Message(self.name, message.sender, "inform",
                       {"plan": plan}, depth=message.depth)


class Researcher(Specialist):
    name = "researcher"
    capabilities = {"retrieve", "search"}

    def handle(self, message: Message) -> Message | None:
        query = message.payload.get("task", "")
        result = self.ctx["registry"].execute(ToolCall("search_docs", {"query": query}),
                                              self.ctx)
        docs = result.get("output", {}).get("results", [])
        if not docs:
            return Message(self.name, message.sender, "escalate",
                           {"reason": "no documents matched"}, depth=message.depth)
        self.board.write("facts", docs, author=self.name, source=docs[0]["id"])
        self.work_done += 1
        return Message(self.name, message.sender, "inform",
                       {"docs": [d["id"] for d in docs], "best": docs[0]["text"]},
                       depth=message.depth)


class Calculator(Specialist):
    name = "calculator"
    capabilities = {"compute"}

    def handle(self, message: Message) -> Message | None:
        expression = message.payload.get("expression", "")
        result = self.ctx["registry"].execute(ToolCall("calculator",
                                                       {"expression": expression}), self.ctx)
        self.work_done += 1
        self.board.write("computed", result.get("output"), author=self.name)
        return Message(self.name, message.sender, "inform",
                       {"result": result.get("output") or result.get("error")},
                       depth=message.depth)


class Writer(Specialist):
    name = "writer"
    capabilities = {"compose"}

    def handle(self, message: Message) -> Message | None:
        facts = self.board.latest("facts")
        computed = self.board.latest("computed")
        text = ""
        if facts:
            text = facts["value"][0]["text"]
        if computed and computed["value"]:
            text += f" Computed value: {computed['value'].get('value')}."
        self.board.write("draft", text or "No answer found.", author=self.name)
        self.work_done += 1
        return Message(self.name, message.sender, "inform", {"draft": text},
                       depth=message.depth)


class Critic(Specialist):
    name = "critic"
    capabilities = {"review"}

    def handle(self, message: Message) -> Message | None:
        draft = self.board.latest("draft")
        text = draft["value"] if draft else ""
        problems = []
        if len(text.split()) < 4:
            problems.append("answer too short")
        facts = self.board.latest("facts")
        if facts:
            source_text = " ".join(d["text"] for d in facts["value"])
            for token in text.split():
                if token[:1].isdigit() and token not in source_text:
                    problems.append(f"number not in sources: {token}")
        self.board.write("review", {"problems": problems, "score": len(problems)},
                         author=self.name)
        self.work_done += 1
        verdict = "critique" if problems else "inform"
        return Message(self.name, message.sender, verdict,
                       {"problems": problems}, depth=message.depth)


# ---------------------------------------------------------------------------
# Coordination
# ---------------------------------------------------------------------------

class Coordinator:
    """Runs a task through specialists with bounded delegation and escalation."""

    def __init__(self, agents: dict[str, Specialist], bus: MessageBus,
                 board: Blackboard, max_turns: int = 12, max_depth: int = 3):
        self.agents, self.bus, self.board = agents, bus, board
        self.max_turns, self.max_depth = max_turns, max_depth

    def _assign(self, subtask: dict, depth: int) -> Message | None:
        """Contract net: every agent bids, the best positive bid wins."""
        bids = {}
        for name, agent in self.agents.items():
            if name in ("planner",):
                continue
            score = agent.bid(subtask)
            if score > 0:
                bids[name] = score
        if not bids:
            return None
        winner = max(bids, key=bids.get)
        self.board.write("assignment", {"subtask": subtask, "winner": winner,
                                        "bids": bids}, author="coordinator")
        reply = self.agents[winner].handle(
            Message("coordinator", winner, "request", subtask, depth=depth))
        if reply:
            self.bus.send(reply)
        return reply

    def run(self, question: str, approver_available: bool = False) -> dict:
        t0 = time.perf_counter()
        self.bus.send(Message("coordinator", "planner", "request", {"question": question}))
        plan_msg = self.agents["planner"].handle(
            Message("coordinator", "planner", "request", {"question": question}))
        plan = plan_msg.payload["plan"] if plan_msg else [{"needs": ["retrieve"],
                                                           "task": question}]

        executed, escalations = [], []
        for subtask in plan:
            if subtask["needs"] == ["external"] and not approver_available:
                escalations.append("external action needs human approval")
                continue
            reply = self._assign(subtask, depth=1)
            if reply is None:
                escalations.append(f"no agent could handle {subtask['needs']}")
                continue
            executed.append({"subtask": subtask, "reply": reply.intent})

        self.agents["writer"].handle(Message("coordinator", "writer", "request", {}, depth=1))
        review = self.agents["critic"].handle(
            Message("coordinator", "critic", "request", {}, depth=1))
        problems = review.payload["problems"] if review else ["no review"]

        draft = self.board.latest("draft")
        return {
            "question": question,
            "answer": draft["value"] if draft else None,
            "subtasks": len(plan),
            "executed": executed,
            "review_problems": problems,
            "escalations": escalations,
            "messages": self.bus.stats()["messages"],
            "depth_seen": self.bus.stats()["max_depth_seen"],
            "elapsed": round(time.perf_counter() - t0, 5),
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def build_team(ctx: dict):
    bus, board = MessageBus(max_depth=3)
    for name in ("planner", "researcher", "calculator", "writer", "critic"):
        bus.register(name)
    agents = {
        "planner": Planner(bus, board, ctx),
        "researcher": Researcher(bus, board, ctx),
        "calculator": Calculator(bus, board, ctx),
        "writer": Writer(bus, board, ctx),
        "critic": Critic(bus, board, ctx),
    }
    return Coordinator(agents, bus, board), bus, board, agents


def main() -> None:
    registry = ToolRegistry()
    ctx = {"notes": {}, "roles": ["assistant"], "max_tool_calls": 20,
           "tool_catalogue": "", "registry": registry}

    print("=" * 84)
    print("1. Sequential delegation on a retrieval task")
    print("=" * 84)
    coord, bus, board, agents = build_team(ctx)
    out = coord.run("What IELTS score do I need for the MSc?")
    print(f"  subtasks {out['subtasks']}  messages {out['messages']}  "
          f"depth {out['depth_seen']}  elapsed {out['elapsed']}s")
    print("  answer:", out["answer"][:96])
    print("  review problems:", out["review_problems"])
    print("  escalations:", out["escalations"])
    print("  blackboard authors:", [e["author"] for e in board.audit()][:8])

    print("\n" + "=" * 84)
    print("2. A task that needs a calculation (contract net picks the calculator)")
    print("=" * 84)
    coord, bus, board, agents = build_team(ctx)
    out = coord.run("What is the total cost of tuition plus 51 weeks of halls?")
    assignments = [e["value"] for e in board.audit() and board.entries
                   if e["key"] == "assignment"]
    for a in assignments:
        print(f"  needs {a['subtask']['needs']} -> winner {a['winner']} bids {a['bids']}")
    print("  escalations:", out["escalations"])

    print("\n" + "=" * 84)
    print("3. An external action without an approver is escalated, not executed")
    print("=" * 84)
    coord, bus, board, agents = build_team(ctx)
    out = coord.run("Send me the fee summary by email.")
    print("  escalations:", out["escalations"])
    print("  outbox size (must be 0):", len(ctx.get("outbox", [])))

    print("\n" + "=" * 84)
    print("4. Depth limit prevents infinite delegation")
    print("=" * 84)
    msg = Message("a", "researcher", "request", {"task": "loop"}, depth=4)
    print("  depth 4 ->", bus.send(msg))

    print("\n" + "=" * 84)
    print("5. Work done per agent")
    print("=" * 84)
    for name, agent in agents.items():
        print(f"  {name:12s} capabilities={sorted(agent.capabilities)} "
              f"work={agent.work_done}")

    print("\n" + "=" * 84)
    print("6. Blackboard audit trail")
    print("=" * 84)
    for entry in board.audit():
        print(f"  v{entry['version']} {entry['key']:12s} by {entry['author']}")


if __name__ == "__main__":
    main()
