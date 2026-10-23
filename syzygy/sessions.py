from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Session:
    session_id: str
    agent_id: str
    environment_id: str
    task: str
    current_layer: str = "L00"
    branch: Optional[str] = None
    spatial_cursor: str = "WORLD/PROPERTY/ZONE/ROOM/ANCHOR"
    memory_refs: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    permission_scope: str = "local"
    start_time: str = ""
    end_time: Optional[str] = None
    checkpoint_history: List[str] = field(default_factory=list)
    handoff_records: List[Dict[str, str]] = field(default_factory=list)
    completion_state: str = "ACTIVE"

    def __post_init__(self) -> None:
        if not self.start_time:
            self.start_time = datetime.utcnow().isoformat()

    def checkpoint(self, label: str) -> str:
        self.checkpoint_history.append(label)
        return label

    def handoff(self, to_agent: str, transferred: List[str], retained_private: List[str]) -> Dict[str, str]:
        record = {
            "from": self.agent_id,
            "to": to_agent,
            "transferred": ",".join(transferred),
            "retained_private": ",".join(retained_private),
            "time": datetime.utcnow().isoformat(),
        }
        self.handoff_records.append(record)
        return record


class SessionManager:
    def __init__(self) -> None:
        self.sessions: Dict[str, Session] = {}

    def create_session(self, session: Session) -> Session:
        if session.session_id in self.sessions:
            raise ValueError(f"Session already exists: {session.session_id}")
        self.sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> Session:
        return self.sessions[session_id]

    def suspend(self, session_id: str) -> Session:
        session = self.get(session_id)
        session.completion_state = "PAUSED"
        return session

    def resume(self, session_id: str) -> Session:
        session = self.get(session_id)
        session.completion_state = "ACTIVE"
        return session
