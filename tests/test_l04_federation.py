from __future__ import annotations

from syzygy.approval import HALTApprovalGate
from syzygy.branching import BranchForkEngine
from syzygy.federation_service import FederationGatewayService, FederationRecord
from syzygy.parent_child_engine import ParentChildLayerEngine
from syzygy.spatial_memory import SpatialMemoryTopography
from syzygy.verification import VerificationEngine


def test_federation_discovery(local_registry):
    service = FederationGatewayService()
    service.register_peer(FederationRecord("CODEX", ["build", "patch"], permissions={"build": True}))
    service.register_peer(FederationRecord("VIBE", ["verify", "test"], permissions={"test": True}))
    assert service.discover("build") == ["CODEX"]


def test_verification_rejects_missing_hash_alignment():
    verifier = VerificationEngine()
    report = verifier.verify_artifact("artifact-2", "payload", "wrong-hash", "seed", tests=["unit"], security_checks=["permission"])
    assert report.integrity_ok is False
    assert report.acceptance_ok is False


def test_halt_gate_requires_explicit_credential():
    gate = HALTApprovalGate()
    try:
        gate.approve("ALPHA", "ART-2", "ROM", "abc", "BAD-CRED")
        raise AssertionError("Expected invalid credential failure")
    except ValueError:
        pass


def test_parent_child_engine_accepts_child_when_parent_accepted():
    engine = ParentChildLayerEngine()
    engine.define("L00", "Environment Foundation", objective="bootstrap")
    engine.finalize("L00")
    assert engine.can_spawn_child("L00") is True


def test_branch_engine_keeps_lineage_separate():
    brancher = BranchForkEngine()
    branch = brancher.create_branch("BR-2", "ROOT", "explore alternative patch", "CODEX", "rev-02", ["feature.py"])
    assert branch.parent_ref == "ROOT"
    assert branch.reason == "explore alternative patch"


def test_spatial_memory_supports_location_navigation():
    topography = SpatialMemoryTopography()
    topography.add_location("WORLD/PROPERTY/ZONE/ROOM", "semantic-room", "era-1")
    topography.add_card("CARD-1", "draft-memory", "WORLD/PROPERTY/ZONE/ROOM")
    assert topography.discover("WORLD/PROPERTY/ZONE/ROOM") == ["CARD-1"]
