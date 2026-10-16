# SYZYGY Doorbell Demo

Designed-by: GitHub Copilot (@copilot) | Concept & System Architecture: Carlos A. Salazar (Alpha)

This repository contains a non-destructive, locally runnable proof-of-concept for the Doorbell -> Post Office -> Authorization -> Worker -> Verification model.

Included files
--------------
- README.md
- WORKORDER.schema.json
- RECEIPT.schema.json
- poc.py
- kimi_ledger.py
- manual.md
- diagram.puml
- manifest.json
- verify_run.py
- HARDENING.md
- .gitignore

Quick start
-----------
1. Create a virtual environment and install optional dependencies:
   python3 -m venv venv
   source venv/bin/activate
   pip install blake3 jsonschema

2. Run the local demo:
   python3 poc.py

3. Validate the receipt chain and lifecycle:
   python3 verify_run.py

Notes
-----
- The POC intentionally does not delete files or perform destructive actions.
- All signatures in receipts are simulated placeholders, not production cryptographic attestations.
- The success path includes a preauthorized unattended successor task.

Repository notes
----------------
- Runtime artifacts (`postoffice.db`, `output/`, `provenance.ledger`) are ignored in `.gitignore`.
- All ledger entries are canonical JSON lines, making them easy to audit with `verify_run.py`.
