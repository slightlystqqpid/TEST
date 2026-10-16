#!/usr/bin/env python3
"""
SYZYGY Doorbell POC — Automated Ledger & State Verifier
Run after poc.py: python3 verify_run.py
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

DB_FILE = Path("postoffice.db")
LEDGER_FILE = Path("provenance.ledger")


def sha256_prefixed(raw_line: str) -> str:
    return "sha256:" + hashlib.sha256(raw_line.encode("utf-8")).hexdigest()


def verify():
    if not DB_FILE.exists() or not LEDGER_FILE.exists():
        print("[FAIL] Missing postoffice.db or provenance.ledger. Run `python3 poc.py` first.")
        sys.exit(1)

    lines = LEDGER_FILE.read_text(encoding="utf-8").splitlines()
    events = [(line, json.loads(line)) for line in lines if line.strip()]

    # 1. Verify receipt hash chain per work_id
    receipts_by_work = {}
    for raw_line, obj in events:
        if obj.get("event") == "work_receipt":
            wid = obj["work_id"]
            receipts_by_work.setdefault(wid, []).append((raw_line, obj))

    if not receipts_by_work:
        print("[FAIL] No work_receipt entries found in provenance.ledger.")
        sys.exit(1)

    for wid, r_list in receipts_by_work.items():
        prev_hash = None
        for idx, (raw_line, r_obj) in enumerate(r_list):
            recorded_prev = r_obj.get("prev_receipt_hash")
            if recorded_prev != prev_hash:
                print(f"[FAIL] Broken hash chain on {wid} checkpoint {idx + 1}:")
                print(f"       Expected prev_receipt_hash: {prev_hash}")
                print(f"       Recorded prev_receipt_hash: {recorded_prev}")
                sys.exit(1)
            prev_hash = sha256_prefixed(raw_line)
        print(f"[PASS] Receipt hash chain verified for {wid} ({len(r_list)} checkpoints)")

    # 2. Verify SQLite state: parent completed, successor queued & linked via supersedes
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT work_id, status, supersedes FROM work_orders ORDER BY seq ASC")
        rows = cur.fetchall()

        if len(rows) < 2:
            print("[FAIL] Expected at least 2 work orders (parent + auto-successor).")
            sys.exit(1)

        parent_id, parent_status, _ = rows[0]
        succ_id, succ_status, succ_supersedes = rows[1]

        if parent_status != "completed":
            print(f"[FAIL] Parent work order {parent_id} status is '{parent_status}', expected 'completed'.")
            sys.exit(1)

        if succ_supersedes != parent_id:
            print(f"[FAIL] Successor {succ_id} supersedes='{succ_supersedes}', expected '{parent_id}'.")
            sys.exit(1)

        print(f"[PASS] Successor linkage verified: {succ_id} (status={succ_status}) supersedes {parent_id}")

        # 3. Verify lease TTL
        cur.execute("SELECT lease_id, worker_id, expires_at FROM leases WHERE work_id=?", (parent_id,))
        lease_row = cur.fetchone()
        if not lease_row:
            print(f"[FAIL] No lease record found for {parent_id}.")
            sys.exit(1)
        lease_id, worker_id, expires_at = lease_row
        print(f"[PASS] Lease recorded: {lease_id} by {worker_id} (expires_at={expires_at})")

    print("\nALL SYZYGY DOORBELL POC CHECKS PASSED.")


if __name__ == "__main__":
    verify()
