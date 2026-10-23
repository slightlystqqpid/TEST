from __future__ import annotations

from syzygy.approval import HALTApprovalGate


def test_halt_gate_accepts_test_operator_credential():
    gate = HALTApprovalGate()
    record = gate.approve("ALPHA", "ART-1", "ROM", "hash-123", "ALPHA_TEST_OPERATOR", version="1.0")
    assert record.approved is True
    assert record.action == "ROM"
