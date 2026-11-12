"""protocols.py -- tool and agent protocols, framework-free (M12, L12-02 and L12-04).

Two protocols matter in practice:

1. **MCP (Model Context Protocol)** -- how a host discovers and calls tools
   exposed by a server, over JSON-RPC 2.0. The wire shapes below are the ones
   MCP uses: ``initialize``, ``tools/list`` and ``tools/call``, with content
   returned as a list of typed blocks.

2. **Agent-to-agent envelopes** -- how one agent hands a task to another. There
   is no single standard in wide use yet; what follows is a minimal, validated
   envelope with the fields every real design needs: sender, recipient,
   capability, delegation depth and a correlation id.

Both demos run in-process. Nothing here opens a socket, which is deliberate: you
should understand the message shapes before you debug a transport.

Run ``python protocols.py``.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from agent_core import ToolCall, ToolRegistry
from tools import TOOL_SPECS


# ---------------------------------------------------------------------------
# 1. MCP-shaped JSON-RPC server
# ---------------------------------------------------------------------------

JSONRPC_VERSION = "2.0"


class MCPError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code, self.message = code, message


class MCPServer:
    """Exposes the module's tools with MCP-shaped request/response bodies."""

    def __init__(self, registry: ToolRegistry, ctx: dict, server_name: str = "northfield-tools",
                 version: str = "1.0.0"):
        self.registry = registry
        self.ctx = ctx
        self.server_name = server_name
        self.version = version
        self.initialised = False
        self.request_log: list[dict] = []

    # -- transport ---------------------------------------------------------
    def handle(self, request: dict) -> dict:
        """Process one JSON-RPC request object and return a response object."""
        self.request_log.append({"ts": round(time.time(), 3), "method": request.get("method")})
        req_id = request.get("id")
        try:
            if request.get("jsonrpc") != JSONRPC_VERSION:
                raise MCPError(-32600, "invalid request: jsonrpc must be 2.0")
            method = request.get("method")
            params = request.get("params") or {}
            if method == "initialize":
                result = self._initialize(params)
            elif method == "tools/list":
                result = self._tools_list()
            elif method == "tools/call":
                result = self._tools_call(params)
            else:
                raise MCPError(-32601, f"method not found: {method}")
            return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "result": result}
        except MCPError as exc:
            return {"jsonrpc": JSONRPC_VERSION, "id": req_id,
                    "error": {"code": exc.code, "message": exc.message}}
        except Exception as exc:
            return {"jsonrpc": JSONRPC_VERSION, "id": req_id,
                    "error": {"code": -32603, "message": f"internal error: {exc}"}}

    # -- methods -----------------------------------------------------------
    def _initialize(self, params: dict) -> dict:
        self.initialised = True
        return {
            "protocolVersion": params.get("protocolVersion", "2025-06-18"),
            "serverInfo": {"name": self.server_name, "version": self.version},
            "capabilities": {"tools": {"listChanged": False}},
        }

    def _tools_list(self) -> dict:
        if not self.initialised:
            raise MCPError(-32002, "server not initialised")
        return {"tools": [
            {"name": s["name"], "description": s["description"],
             "inputSchema": s["parameters"],
             "annotations": {"readOnlyHint": not s["side_effect"],
                             "requiresApproval": s["requires_approval"]}}
            for s in TOOL_SPECS
        ]}

    def _tools_call(self, params: dict) -> dict:
        if not self.initialised:
            raise MCPError(-32002, "server not initialised")
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not name:
            raise MCPError(-32602, "invalid params: name is required")
        result = self.registry.execute(ToolCall(name, arguments), self.ctx)
        if result["status"] == "ok":
            text = json.dumps(result.get("output"), default=str)
            return {"content": [{"type": "text", "text": text}], "isError": False}
        return {"content": [{"type": "text",
                             "text": result.get("error", "tool error")}], "isError": True}


# ---------------------------------------------------------------------------
# 2. Agent-to-agent envelope
# ---------------------------------------------------------------------------

@dataclass
class A2AEnvelope:
    sender: str
    recipient: str
    capability: str
    payload: dict
    correlation_id: str
    depth: int = 0
    protocol: str = "a2a/0.1"
    ttl_seconds: int = 30
    created: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {"protocol": self.protocol, "sender": self.sender,
                "recipient": self.recipient, "capability": self.capability,
                "payload": self.payload, "correlation_id": self.correlation_id,
                "depth": self.depth, "ttl": self.ttl_seconds,
                "created": round(self.created, 3)}


REQUIRED_FIELDS = ("protocol", "sender", "recipient", "capability", "payload",
                   "correlation_id", "depth", "ttl")


def validate_envelope(envelope: dict, registry_of_agents: dict, max_depth: int = 3) -> dict:
    """Validate shape, recipient, capability, depth and expiry before dispatch."""
    missing = [f for f in REQUIRED_FIELDS if f not in envelope]
    if missing:
        return {"valid": False, "error": f"missing fields: {missing}"}
    if envelope["recipient"] not in registry_of_agents:
        return {"valid": False, "error": f"unknown agent: {envelope['recipient']}"}
    caps = registry_of_agents[envelope["recipient"]].get("capabilities", set())
    if envelope["capability"] not in caps:
        return {"valid": False,
                "error": f"{envelope['recipient']} lacks capability "
                         f"{envelope['capability']!r}"}
    if envelope["depth"] > max_depth:
        return {"valid": False, "error": "delegation depth exceeded"}
    if time.time() - envelope["created"] > envelope["ttl"]:
        return {"valid": False, "error": "envelope expired"}
    return {"valid": True}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    registry = ToolRegistry()
    ctx = {"notes": {"note-seed-1": "Applicant needs IELTS 6.5."},
           "roles": ["assistant"], "max_tool_calls": 10, "tool_catalogue": ""}
    server = MCPServer(registry, ctx)

    print("=" * 84)
    print("1. MCP handshake and tool discovery")
    print("=" * 84)
    init = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                          "params": {"protocolVersion": "2025-06-18"}})
    print("  initialize ->", json.dumps(init["result"], indent=None)[:110])
    listing = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    tools = listing["result"]["tools"]
    print(f"  tools/list -> {len(tools)} tools")
    for t in tools:
        print(f"    {t['name']:18s} readOnly={t['annotations']['readOnlyHint']!s:5s} "
              f"approval={t['annotations']['requiresApproval']!s:5s} "
              f"args={list(t['inputSchema']['properties'])}")

    print("\n" + "=" * 84)
    print("2. tools/call: success, schema error, unknown method")
    print("=" * 84)
    ok = server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                        "params": {"name": "calculator",
                                   "arguments": {"expression": "26400 - 4000"}}})
    print("  calculator ->", ok["result"]["content"][0]["text"])
    bad = server.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                         "params": {"name": "calculator", "arguments": {}}})
    print("  missing arg ->", bad["result"])
    unknown = server.handle({"jsonrpc": "2.0", "id": 5, "method": "tools/delete"})
    print("  unknown method ->", unknown["error"])
    uninit = MCPServer(ToolRegistry(), ctx).handle({"jsonrpc": "2.0", "id": 6,
                                                   "method": "tools/list"})
    print("  before initialize ->", uninit["error"])

    print("\n" + "=" * 84)
    print("3. Approval-required tool through the protocol")
    print("=" * 84)
    r = server.handle({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                       "params": {"name": "send_email",
                                  "arguments": {"to": "student@example.com",
                                                "subject": "Fees", "body": "26,400 GBP"}}})
    print("  send_email -> isError:", r["result"]["isError"],
          "|", r["result"]["content"][0]["text"][:64])
    print("  outbox (must be empty):", len(ctx.get("outbox", [])))

    print("\n" + "=" * 84)
    print("4. Agent-to-agent envelope validation")
    print("=" * 84)
    agents = {"researcher": {"capabilities": {"retrieve"}},
              "writer": {"capabilities": {"compose"}}}
    good = A2AEnvelope("planner", "researcher", "retrieve",
                       {"task": "ielts requirement"}, "corr-001", depth=1).to_dict()
    print("  valid   ->", validate_envelope(good, agents))
    wrong_cap = dict(good, capability="compute")
    print("  bad cap ->", validate_envelope(wrong_cap, agents))
    too_deep = dict(good, depth=7)
    print("  depth   ->", validate_envelope(too_deep, agents))
    stale = dict(good, created=time.time() - 120)
    print("  expired ->", validate_envelope(stale, agents))
    print("  envelope keys:", list(good))
    print("  request log:", server.request_log[-3:])


if __name__ == "__main__":
    main()
