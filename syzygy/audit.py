from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Receipt:
    receipt_id: str
    event_type: str
    actor: str
    environment: str
    session: str = "unknown"
    layer: str = "unk"
    parent_reference: Optional[str] = None
    artifact_reference: Optional[str] = None
    source_revision: Optional[str] = None
    checksum: Optional[str] = None
    timestamp: str = ""
    result: str = "OK"
    error: Optional[str] = None
    verification_method: Optional[str] = None
    approval_reference: Optional[str] = None


class ReceiptLedger:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else Path.cwd()
        self.root.mkdir(parents=True, exist_ok=True)
        self.entries: List[Receipt] = []

    def append(self, receipt: Receipt) -> Receipt:
        if not receipt.timestamp:
            receipt.timestamp = datetime.now(timezone.utc).isoformat()
        receipt.checksum = self._checksum_for(receipt)
        self.entries.append(receipt)
        return receipt

    def _checksum_for(self, receipt: Receipt) -> str:
        payload = json.dumps(asdict(receipt), sort_keys=True)
        return sha256(payload.encode("utf-8")).hexdigest()

    def verify_chain(self) -> bool:
        previous = None
        for entry in self.entries:
            if previous is None:
                previous = entry.checksum
                continue
            if entry.checksum is None:
                return False
            if previous != self._checksum_for(entry):
                return False
            previous = entry.checksum
        return True

    def persist(self, path: str | Path | None = None) -> Path:
        target = Path(path) if path else self.root / "audit" / "receipt_log.jsonl"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            for entry in self.entries:
                handle.write(json.dumps(asdict(entry), sort_keys=True) + "\n")
        return target
