from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Dict, List, Optional


class AuthorizationError(RuntimeError):
    pass


@dataclass
class Agent:
    agent_id: str
    name: str
    role: str
    capabilities: List[str] = field(default_factory=list)
    permissions: Dict[str, bool] = field(default_factory=dict)
    active: bool = True
    credential: Optional[str] = None

    def authorize(self, action: str) -> bool:
        if not self.active:
            return False
        return self.permissions.get(action, False) or action in self.capabilities

    def fingerprint(self) -> str:
        raw = f"{self.agent_id}:{self.name}:{self.role}:{','.join(sorted(self.capabilities))}"
        return sha256(raw.encode("utf-8")).hexdigest()


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(f"Agent already exists: {agent.agent_id}")
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        if agent_id not in self._agents:
            raise KeyError(agent_id)
        return self._agents[agent_id]

    def revoke(self, agent_id: str) -> None:
        agent = self.get(agent_id)
        agent.active = False

    def list(self) -> List[Agent]:
        return list(self._agents.values())

    def seed_default_agents(self) -> None:
        defaults = [
            Agent(
                "ALPHA",
                "ALPHA",
                "Human Authority",
                capabilities=["approve", "reject", "inspect", "revoke"],
                permissions={
                    "approve": True,
                    "reject": True,
                    "inspect": True,
                    "revoke": True,
                    "ROM": True,
                },
                credential="ALPHA_TEST_OPERATOR",
            ),
            Agent(
                "CODEX",
                "CODEX",
                "Engineering Agent",
                capabilities=["build", "patch", "verify"],
                permissions={"build": True, "patch": True, "verify": True},
            ),
            Agent(
                "VIBE",
                "VIBE",
                "Evaluation Agent",
                capabilities=["test", "challenge", "verify"],
                permissions={"test": True, "challenge": True, "verify": True},
            ),
            Agent(
                "GREEN-EYE",
                "GREEN-EYE",
                "Operational Observer",
                capabilities=["observe", "report"],
                permissions={"observe": True, "report": True},
            ),
        ]
        for agent in defaults:
            self.register(agent)

    def validate_agent(self, agent_id: str, action: str, credential: Optional[str] = None) -> Agent:
        agent = self.get(agent_id)
        if not agent.active:
            raise AuthorizationError(f"Agent {agent_id} is inactive")
        if action in {"approve", "ROM", "governance"} and credential != agent.credential:
            raise AuthorizationError(f"Invalid credential for protected action on {agent_id}")
        if not agent.authorize(action):
            raise AuthorizationError(f"Agent {agent_id} lacks permission: {action}")
        return agent
