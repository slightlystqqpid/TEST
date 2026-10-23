from __future__ import annotations

from syzygy.verification import VerificationEngine


def test_verification_rejects_missing_provenance_and_hash_mismatch():
    verifier = VerificationEngine()
    report = verifier.verify_artifact("artifact-verify", "contents", "invalid_hash", "", tests=["test-case"], security_checks=["permission-check"])
    assert report.integrity_ok is False
    assert report.provenance_ok is False
    assert report.overall() is False
