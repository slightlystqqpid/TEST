from __future__ import annotations

from syzygy.identity import Agent, AgentRegistry, AuthorizationError


def test_agent_registry_seeded():
    registry = AgentRegistry()
    registry.seed_default_agents()
    assert "ALPHA" in registry._agents
    assert "CODEX" in registry._agents


def test_explicit_approval_requires_credential():
    registry = AgentRegistry()
    registry.seed_default_agents()
    try:
        registry.validate_agent("ALPHA", "approve", credential="WRONG")
        raise AssertionError("Expected approval to fail")
    except AuthorizationError:
        pass


def test_inactive_agent_is_rejected():
    registry = AgentRegistry()
    registry.seed_default_agents()
    registry.revoke("CODEX")
    try:
        registry.validate_agent("CODEX", "build")
        raise AssertionError("Expected revoked agent to fail")
    except AuthorizationError:
        pass
