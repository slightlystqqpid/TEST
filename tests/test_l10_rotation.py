from __future__ import annotations

from syzygy.rotation import RotationManager, RotationPolicy


def test_rotation_policy_is_explicit_and_deterministic():
    manager = RotationManager(now=None)
    manager.add_policy(RotationPolicy("cycle-30", interval_days=30, semantics=True, physical_replica=False))
    assert manager.rotate("cycle-30") is True
