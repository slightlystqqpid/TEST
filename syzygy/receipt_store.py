from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ExecutionReceipt:
    layer_id: str
    parent_dependencies: List[str]
    files_created: List[str]
    tests_run: List[str]
    pass_fail: str
    verification_evidence: str
    security_findings: List[str]
    unresolved_issues: List[str]
    approval_status: str
    completion_state: str
    next_child_eligibility: str


class ExecutionLedger:
    def __init__(self) -> None:
        self.entries: List[ExecutionReceipt] = []

    def record(self, entry: ExecutionReceipt) -> None:
        self.entries.append(entry)

    def export(self) -> List[Dict[str, object]]:
        return [
            {
                "layer_id": e.layer_id,
                "parent_dependencies": e.parent_dependencies,
                "files_created": e.files_created,
                "tests_run": e.tests_run,
                "pass_fail": e.pass_fail,
                "verification_evidence": e.verification_evidence,
                "security_findings": e.security_findings,
                "unresolved_issues": e.unresolved_issues,
                "approval_status": e.approval_status,
                "completion_state": e.completion_state,
                "next_child_eligibility": e.next_child_eligibility,
            }
            for e in self.entries
        ]
