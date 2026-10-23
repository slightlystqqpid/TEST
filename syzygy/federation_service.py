from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FederationRecord:
    agent_id: str
    capabilities: List[str]
    endpoint: str = "local://simulated"
    permissions: Dict[str, bool] = field(default_factory=dict)


class FederationGatewayService:
    def __init__(self) -> None:
        self.peers: Dict[str, FederationRecord] = {}

    def register_peer(self, record: FederationRecord) -> None:
        self.peers[record.agent_id] = record

    def discover(self, capability: str) -> List[str]:
        return [agent_id for agent_id, record in self.peers.items() if capability in record.capabilities]

    def publish_skill(self, agent_id: str, skill: str) -> None:
        if agent_id in self.peers:
            self.peers[agent_id].capabilities.append(skill)
