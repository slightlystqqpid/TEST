from __future__ import annotations

from syzygy.collaboration import CollaborationEngine, AgentSession


def test_handoff_records_transfer_before_private_retention():
    engine = CollaborationEngine()
    session = AgentSession("S-01", "CODEX", "patch a module")
    engine.add_session(session)
    result = engine.handoff("S-01", "VIBE", ["artifact.py", "test.py"])
    assert result["status"] == "HANDOFF_RECORDED"
