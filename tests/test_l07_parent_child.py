from __future__ import annotations

from syzygy.parent_child_engine import ParentChildLayerEngine


def test_child_spawn_requires_acceptance():
    engine = ParentChildLayerEngine()
    engine.define("L07", "Child Engine", objective="dependency launch")
    assert engine.can_spawn_child("L07") is False
    engine.finalize("L07")
    assert engine.can_spawn_child("L07") is True
