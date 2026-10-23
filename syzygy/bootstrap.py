from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


REQUIRED_DIRECTORIES = (
    "agents",
    "audit",
    "branches",
    "checkpoints",
    "data",
    "environments",
    "forks",
    "layers",
    "memory",
    "receipts",
    "sessions",
    "tasks",
    "tests",
    "tmp",
)

REQUIRED_FILES = (
    "manifest.json",
    "agent_registry.json",
    "layer_registry.json",
)


def build_default_manifest() -> Dict[str, Any]:
    return {
        "project": "SYZYGY",
        "version": "0.1.0",
        "lifecycle": [
            "CREATE",
            "INITIALIZE",
            "LOAD",
            "VALIDATE",
            "ACTIVATE",
            "PAUSE",
            "RESUME",
            "CHECKPOINT",
            "RESTORE",
            "SHUTDOWN",
        ],
        "agents": [
            {"id": "ALPHA", "role": "Human Authority", "capabilities": ["approve", "reject", "inspect"]},
            {"id": "CODEX", "role": "Engineering Agent", "capabilities": ["build", "patch", "verify"]},
            {"id": "VIBE", "role": "Evaluation Agent", "capabilities": ["test", "challenge", "verify"]},
            {"id": "GREEN-EYE", "role": "Operational Observer", "capabilities": ["observe", "report"]},
            {"id": "SYZYGY COORDINATOR", "role": "Workflow Orchestrator", "capabilities": ["schedule", "handoff"]},
            {"id": "WITNESS", "role": "Evidence Observer", "capabilities": ["audit", "compare"]},
        ],
        "layers": [
            {"id": "L00", "name": "Environment Foundation", "state": "DEFINED"},
            {"id": "L01", "name": "Identity & Session Engine", "state": "DEFINED"},
            {"id": "L02", "name": "Memory Governance", "state": "DEFINED"},
            {"id": "L03", "name": "Spatial Memory Topography", "state": "DEFINED"},
        ],
        "security": {
            "require_human_approval_for": ["ROM", "governance", "merge"],
            "audit_hash_chain": True,
            "simulate_human_operator": "ALPHA_TEST_OPERATOR",
        },
    }


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def bootstrap_environment(root: str | Path | None = None) -> Dict[str, Any]:
    """Create the base SYZYGY project structure and manifests.

    The function intentionally uses only the Python standard library so the result
    remains reproducible in a clean-room environment.
    """
    root_path = Path(root) if root else Path.cwd()
    root_path.mkdir(parents=True, exist_ok=True)

    manifest = build_default_manifest()
    for directory in REQUIRED_DIRECTORIES:
        (root_path / directory).mkdir(parents=True, exist_ok=True)

    for filename in REQUIRED_FILES:
        (root_path / filename).touch(exist_ok=True)

    _write_json(root_path / "manifest.json", manifest)

    agent_registry = {
        "seed_data": True,
        "agents": manifest["agents"],
    }
    _write_json(root_path / "agent_registry.json", agent_registry)

    layer_registry = {
        "seed_data": True,
        "layers": manifest["layers"],
    }
    _write_json(root_path / "layer_registry.json", layer_registry)

    return {
        "root": str(root_path),
        "manifest": manifest,
        "directories": list(REQUIRED_DIRECTORIES),
        "files": list(REQUIRED_FILES),
        "status": "CREATED",
    }


def validate_environment(root: str | Path | None = None) -> Dict[str, Any]:
    root_path = Path(root) if root else Path.cwd()
    missing = []
    for directory in REQUIRED_DIRECTORIES:
        if not (root_path / directory).is_dir():
            missing.append(directory)
    for filename in REQUIRED_FILES:
        if not (root_path / filename).is_file():
            missing.append(filename)

    return {
        "root": str(root_path),
        "missing": missing,
        "valid": not missing,
        "status": "VALIDATED" if not missing else "INVALID",
    }


if __name__ == "__main__":
    result = bootstrap_environment()
    print(json.dumps(result, indent=2, sort_keys=True))
