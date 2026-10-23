from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FederationPeer:
    agent_id: str
    capabilities: List[str]
    permissions: Dict[str, Any] = field(default_factory=dict)
    endpoint: str = "local://default"


class FederationGateway:
    def __init__(self) -> None:
        self.peers: Dict[str, FederationPeer] = {}
        self.knowledge: Dict[str, list[str]] = {}
        self.skills: Dict[str, list[str]] = {}

    def register(self, peer: FederationPeer) -> None:
        self.peers[peer.agent_id] = peer

    def discover_compatible(self, required_capabilities: List[str]) -> List[str]:
        matches: List[str] = []
        for agent_id, peer in self.peers.items():
            if all(cap in peer.capabilities for cap in required_capabilities):
                matches.append(agent_id)
        return matches

    def publish_knowledge(self, agent_id: str, knowledge: List[str]) -> None:
        self.knowledge.setdefault(agent_id, []).extend(knowledge)

    def publish_skill(self, agent_id: str, skill: str) -> None:
        self.skills.setdefault(agent_id, []).append(skill)

    def leave(self, agent_id: str) -> None:
        self.peers.pop(agent_id, None)
