from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class MemoryTier(str, Enum):
    ROM = "ROM"
    RAM = "RAM"
    CACHE = "CACHE"
    ARCHIVE = "ARCHIVE"


@dataclass
class MemoryPackage:
    package_id: str
    name: str
    tier: MemoryTier
    owner: str
    location: str = "WORLD/PROPERTY/ZONE/ROOM"
    metadata: Dict[str, str] = field(default_factory=dict)
    version: int = 1
    checked_out: bool = False
    provenance: str = "seed"


class MemoryManager:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else Path.cwd()
        self.packages: Dict[str, MemoryPackage] = {}
        self.tiers = {
            MemoryTier.ROM: [],
            MemoryTier.RAM: [],
            MemoryTier.CACHE: [],
            MemoryTier.ARCHIVE: [],
        }

    def register_package(self, package: MemoryPackage) -> None:
        self.packages[package.package_id] = package
        self.tiers.setdefault(package.tier, []).append(package.package_id)

    def checkout(self, package_id: str, agent_id: str) -> MemoryPackage:
        package = self.packages[package_id]
        if package.checked_out:
            raise RuntimeError(f"Package {package_id} already checked out")
        package.checked_out = True
        package.owner = agent_id
        return package

    def checkin(self, package_id: str) -> MemoryPackage:
        package = self.packages[package_id]
        package.checked_out = False
        return package

    def promote(self, package_id: str, target: MemoryTier) -> MemoryPackage:
        package = self.packages[package_id]
        package.tier = target
        return package

    def list_by_tier(self, tier: MemoryTier) -> List[str]:
        return list(self.tiers.get(tier, []))

    def seed_default_packages(self) -> None:
        defaults = [
            MemoryPackage(
                package_id="ROM-01",
                name="governance-baseline",
                tier=MemoryTier.ROM,
                owner="ALPHA",
                location="WORLD/PROPERTY/ZONE/ROOM/ANCHOR",
                provenance="seed",
            ),
            MemoryPackage(
                package_id="RAM-01",
                name="active-session-draft",
                tier=MemoryTier.RAM,
                owner="CODEX",
                location="WORLD/PROPERTY/ZONE/ROOM/ANCHOR",
                provenance="seed",
            ),
            MemoryPackage(
                package_id="CACHE-01",
                name="retrieval-cache",
                tier=MemoryTier.CACHE,
                owner="GREEN-EYE",
                location="WORLD/PROPERTY/ZONE/ROOM/ANCHOR",
                provenance="seed",
            ),
            MemoryPackage(
                package_id="ARCHIVE-01",
                name="historical-provenance",
                tier=MemoryTier.ARCHIVE,
                owner="WITNESS",
                location="WORLD/PROPERTY/ZONE/ROOM/ANCHOR",
                provenance="seed",
            ),
        ]
        for package in defaults:
            self.register_package(package)
