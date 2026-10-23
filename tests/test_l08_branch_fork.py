from __future__ import annotations

from syzygy.branching import BranchForkEngine


def test_branching_tracks_lineage():
    engine = BranchForkEngine()
    branch = engine.create_branch("BR-01", "ROOT", "alternative fix", "CODEX", "rev-abc", ["module.py"])
    assert branch.agent_id == "CODEX"
    assert branch.status == "OPEN"
    assert branch.provenance == ["ROOT"]
