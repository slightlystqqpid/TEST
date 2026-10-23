from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class LayerState(str, Enum):
    DEFINED = "DEFINED"
    READY = "READY"
    BUILDING = "BUILDING"
    BUILT = "BUILT"
    TESTING = "TESTING"
    VERIFIED = "VERIFIED"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    ACCEPTED = "ACCEPTED"
    SEALED = "SEALED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"
    SUPERSEDED = "SUPERSEDED"


@dataclass
class LayerDefinition:
    layer_id: str
    name: str
    parents: List[str] = field(default_factory=list)
    objective: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    state: LayerState = LayerState.DEFINED
    version: str = "0.1.0"


class LayerGraph:
    def __init__(self) -> None:
        self.layers: Dict[str, LayerDefinition] = {}

    def add_layer(self, layer: LayerDefinition) -> None:
        if layer.layer_id in self.layers:
            raise ValueError(f"Layer already exists: {layer.layer_id}")
        self.layers[layer.layer_id] = layer

    def validate_acyclic(self) -> bool:
        visited: set[str] = set()
        active: set[str] = set()

        def visit(node: str) -> bool:
            if node in active:
                return False
            if node in visited:
                return True
            active.add(node)
            for parent in self.layers[node].parents:
                if parent not in self.layers:
                    return False
                if not visit(parent):
                    return False
            active.remove(node)
            visited.add(node)
            return True

        for layer_id in self.layers:
            if not visit(layer_id):
                return False
        return True

    def can_start(self, layer_id: str) -> bool:
        layer = self.layers[layer_id]
        for parent_id in layer.parents:
            parent = self.layers.get(parent_id)
            if parent is None:
                return False
            if parent.state not in {LayerState.ACCEPTED, LayerState.SEALED}:
                return False
        return True

    def seed_layers(self) -> None:
        seed = [
            LayerDefinition("L00", "Environment Foundation", objective="Create a reproducible baseline", acceptance_criteria=["manifest exists", "directories valid"], state=LayerState.ACCEPTED),
            LayerDefinition("L01", "Identity & Session Engine", parents=["L00"], objective="Agent registry and sessions", acceptance_criteria=["registry and audit live"], state=LayerState.READY),
            LayerDefinition("L02", "Memory Governance", parents=["L00"], objective="ROM/RAM/CACHE/ARCHIVE policies", acceptance_criteria=["memory tiers present"], state=LayerState.READY),
            LayerDefinition("L03", "Spatial Memory Topography", parents=["L00"], objective="Memory topology and navigation", acceptance_criteria=["location hierarchy maps"], state=LayerState.READY),
        ]
        for layer in seed:
            self.add_layer(layer)
