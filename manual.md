# SYZYGY Doorbell Quick Manual (visual learner)

## Human view (left)  |  Backend view (right)

[Doorbell] - click -> opens Post Office   |  Post Office (SQLite queue) shows work orders
   |                                           - work_id, payload_hash, scope, status
   v                                           - ledger file (provenance.ledger) appended for events
[Post Office] list -> select work -> APPROVE  |  Authorization gate verifies scope and witness
   |                                           - if preauthorized: allow lease
   v                                           - Worker poller claims lease, writes receipts
[Task List/Dashboard] shows progress             |  Salazar Memory Bridge (checkpoint store)
[Receipts view] -> verify hashes                |  UHL = provenance.ledger (JSONL)

## Quick step-by-step (human)
1. Ring the Doorbell (opens mailbox)
2. Inspect the work order: check payload_hash and scope
3. If acceptable, toggle "Allow preauthorized execution" or require YES for protected writes
4. Monitor Task List — Receipts appear as steps complete
5. When the final receipt is verified, the task is done. No extra human step required for preauthorized successor runs.

## Failure cases (what to watch for)
- payload_hash mismatch -> do NOT approve
- worker never claims lease -> inspect worker logs
- receipt signature simulated? -> require human reviewer and escalate

