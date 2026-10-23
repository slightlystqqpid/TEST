from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class LayerRecord:
    layer_id: str
    name: str
    parent_dependencies: List[str]
    objective: str
    status: str = "DESIGNED"
    code_path: Optional[str] = None
    test_path: Optional[str] = None


class LayerManifest:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else Path.cwd()
        self.records: Dict[str, LayerRecord] = {}
        self._bootstrap()

    def _bootstrap(self) -> None:
        layers = [
            LayerRecord("L00", "Environment Foundation", [], "Project bootstrap, manifests, and validation.", "CREATED", "syzygy/bootstrap.py", "tests/test_l00_bootstrap.py"),
            LayerRecord("L01", "Identity & Session Engine", ["L00"], "Agent registry, sessions, and revocation controls.", "AUTHORED", "syzygy/identity.py", "tests/test_l01_identity.py"),
            LayerRecord("L02", "Memory Governance", ["L00"], "ROM/RAM/CACHE/ARCHIVE and memory promotion policy.", "AUTHORED", "syzygy/memory.py", "tests/test_l02_layers.py"),
            LayerRecord("L03", "Spatial Memory Topography", ["L00"], "Location hierarchy and memory navigation model.", "AUTHORED", "syzygy/spatial_memory.py", "tests/test_l01_l10_layers.py"),
            LayerRecord("L04", "Federation Gateway", ["L00", "L01"], "Peers, discovery, knowledge, skills, and local federation API.", "AUTHORED", "syzygy/federation.py", "tests/test_l04_federation.py"),
            LayerRecord("L05", "Verification & Receipts", ["L00", "L04"], "Independent verification, provenance, and evidence receipts.", "AUTHORED", "syzygy/verification.py", "tests/test_l05_verification.py"),
            LayerRecord("L06", "HALT Human Approval", ["L00", "L05"], "Human authorization gate for protected operations.", "AUTHORED", "syzygy/approval.py", "tests/test_l06_halt.py"),
            LayerRecord("L07", "Parent–Child Layer Engine", ["L00", "L06"], "Dependency validation and controlled child spawning.", "AUTHORED", "syzygy/parent_child_engine.py", "tests/test_l07_parent_child.py"),
            LayerRecord("L08", "Branch & Fork Engine", ["L00", "L07"], "Lineage, divergence, branch/fork separation, and merge logic.", "AUTHORED", "syzygy/branching.py", "tests/test_l08_branch_fork.py"),
            LayerRecord("L09", "Multi-Agent Collaboration", ["L00", "L01", "L04"], "Cross-agent coordination and session handoff.", "AUTHORED", "syzygy/collaboration.py", "tests/test_l09_collaboration.py"),
            LayerRecord("L10", "Recovery & Rotation", ["L00", "L02", "L03", "L05"], "Checkpoints, recovery, and C.Y.C.L.E. rotation.", "AUTHORED", "syzygy/rotation.py", "tests/test_l10_rotation.py"),
            LayerRecord("L11", "End-to-End Evaluation", ["L00", "L01", "L03", "L04", "L05", "L06", "L08", "L09", "L10"], "Evaluation, integration, and adversarial scenario testing.", "AUTHORED", "syzygy/demo.py", "tests/test_l11_e2e.py"),
        ]
        for layer in layers:
            self.records[layer.layer_id] = layer

    def as_dict(self) -> Dict[str, Any]:
        return {key: {
            "name": value.name,
            "parent_dependencies": value.parent_dependencies,
            "objective": value.objective,
            "status": value.status,
            "code_path": value.code_path,
            "test_path": value.test_path,
        } for key, value in self.records.items()}

    def save(self, path: str | Path | None = None) -> Path:
        target = Path(path) if path else self.root / "layer_manifest.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(__import__("json").dumps(self.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target
