from __future__ import annotations

import json
from pathlib import Path

from syzygy.bootstrap import bootstrap_environment, validate_environment


def test_bootstrap_creates_required_layout(tmp_path):
    root = tmp_path / "syzygy-root"
    result = bootstrap_environment(root)
    assert result["status"] == "CREATED"
    assert (root / "manifest.json").exists()
    assert (root / "agent_registry.json").exists()
    assert (root / "layer_registry.json").exists()
    assert (root / "agents").is_dir()
    assert (root / "sessions").is_dir()
    assert (root / "receipts").is_dir()


def test_bootstrap_validation_passes(tmp_path):
    root = tmp_path / "syzygy-root"
    bootstrap_environment(root)
    outcome = validate_environment(root)
    assert outcome["valid"] is True
    assert outcome["status"] == "VALIDATED"


def test_manifest_has_expected_seed_agents(tmp_path):
    root = tmp_path / "syzygy-root"
    result = bootstrap_environment(root)
    agencies = result["manifest"]["agents"]
    ids = {entry["id"] for entry in agencies}
    assert {"ALPHA", "CODEX", "VIBE", "GREEN-EYE"}.issubset(ids)
