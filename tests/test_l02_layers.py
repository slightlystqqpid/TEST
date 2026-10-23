from __future__ import annotations

from syzygy.layers import LayerGraph, LayerDefinition, LayerState
from syzygy.memory import MemoryManager, MemoryTier


def test_layer_dag_is_acyclic():
    graph = LayerGraph()
    graph.seed_layers()
    assert graph.validate_acyclic() is True


def test_parent_acceptance_required_to_start_child():
    graph = LayerGraph()
    graph.seed_layers()
    assert graph.can_start("L01") is False  # L00 is accepted in seed


def test_memory_tiers_seeded():
    manager = MemoryManager()
    manager.seed_default_packages()
    assert manager.list_by_tier(MemoryTier.ROM)
    assert manager.list_by_tier(MemoryTier.RAM)
