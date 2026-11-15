"""Tests for M12 agent execution and guardrails.

These test the safety machinery, not the language model: argument validation, scope
checks, the approval gate, budget enforcement and the audit log.
"""

import json

import pytest

import agent_core as ac
import tools


def email_spec():
    for spec in ac.TOOL_SPECS:
        if spec["name"] == "send_email":
            return spec
    pytest.skip("send_email tool is not registered")


def test_validate_args_reports_missing_required_fields():
    spec = email_spec()
    problems = ac.validate_args(spec, {"to": "a@b.c"})
    assert any("missing required" in p for p in problems)


def test_validate_args_reports_unknown_arguments_and_wrong_types():
    spec = email_spec()
    problems = ac.validate_args(spec, {"to": "a@b.c", "subject": "s", "body": "b", "extra": 1})
    assert any("unknown argument" in p for p in problems)
    problems = ac.validate_args(spec, {"to": 5, "subject": "s", "body": "b"})
    assert any("must be string" in p for p in problems)


def test_validate_args_rejects_a_boolean_where_an_integer_is_required():
    spec = {"parameters": {"required": ["n"], "properties": {"n": {"type": "integer"}}}}
    assert ac.validate_args(spec, {"n": True})
    assert not ac.validate_args(spec, {"n": 3})


def test_approval_gate_denies_by_default():
    gate = ac.ApprovalGate()
    approved, reason = gate.request(ac.ToolCall("send_email", {"to": "a@b.c", "subject": "s", "body": "b"}), {})
    assert approved is False
    assert "denied" in reason.lower()
    assert gate.pending  # the request is recorded for a human


def test_approval_gate_honours_an_explicit_policy():
    gate = ac.ApprovalGate(policy=lambda request: request["tool"] == "send_email")
    approved, _reason = gate.request(
        ac.ToolCall("send_email", {"to": "a@b.c", "subject": "s", "body": "b"}), {})
    assert approved is True


def test_registry_rejects_an_unknown_tool_and_audits_it():
    registry = ac.ToolRegistry()
    result = registry.execute(ac.ToolCall("rm_rf", {}), {"roles": ["assistant"]})
    assert result["status"] == "error"
    assert result["code"] == "unknown_tool"
    assert registry.audit.entries[-1]["status"] == "unknown_tool"


def test_registry_enforces_role_scopes():
    registry = ac.ToolRegistry(role_scopes={"reader": {"read"}})
    result = registry.execute(ac.ToolCall("calculator", {"expression": "1+1"}), {"roles": ["reader"]})
    assert result["code"] == "scope_denied"


def test_registry_enforces_the_tool_call_budget():
    registry = ac.ToolRegistry()
    ctx = {"roles": ["assistant"], "max_tool_calls": 0}
    result = registry.execute(ac.ToolCall("calculator", {"expression": "1+1"}), ctx)
    assert result["code"] == "budget_exceeded"


def test_registry_blocks_an_external_write_without_approval():
    registry = ac.ToolRegistry(role_scopes={"assistant": {"read", "compute", "write", "external"}})
    call = ac.ToolCall("send_email", {"to": "a@b.c", "subject": "s", "body": "b"})
    result = registry.execute(call, {"roles": ["assistant"]})
    assert result["code"] == "approval_denied"     # the default gate denies
    assert registry.call_count == 0                 # nothing was executed


def test_calculator_computes_arithmetic_and_refuses_code():
    ok = tools.calculator({}, "2 + 3 * 4")
    assert "14" in json.dumps(ok)
    bad = tools.calculator({}, "__import__('os').system('echo hi')")
    assert "error" in json.dumps(bad).lower() or "status" in bad


def test_scripted_policy_finishes_after_its_actions():
    policy = ac.ScriptedPolicy([{"thought": "search", "tool": "search_docs", "args": {"query": "x"}}])
    first = policy.next_action("task", ac.Trace("task"), {})
    last = policy.next_action("task", ac.Trace("task"), {})
    assert first.get("tool") == "search_docs"
    assert "final" in last


def test_audit_log_records_every_call_in_order():
    registry = ac.ToolRegistry()
    registry.execute(ac.ToolCall("calculator", {"expression": "1+1"}), {"roles": ["assistant"]})
    registry.execute(ac.ToolCall("calculator", {"expression": "2*3"}), {"roles": ["assistant"]})
    assert len(registry.audit.entries) == 2
    assert registry.audit.entries[0]["args"]["expression"] == "1+1"
