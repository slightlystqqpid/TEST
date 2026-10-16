# SYZYGY Doorbell Demo

Designed-by: GitHub Copilot (@copilot) | Concept & System Architecture: Carlos A. Salazar (Alpha)

This repository contains a NON-DESTRUCTIVE proof-of-concept (POC) demonstrating the Doorbell → Post Office → Authorization → Worker → Verification flow for SYZYGY.

What is included
- WORKORDER.schema.json — formal JSON Schema for work orders
- RECEIPT.schema.json — formal JSON Schema for ledger receipts
- poc.py — a minimal, non-destructive Python POC using SQLite and file-backed ledger (no external network or destructive actions)
- kimi_ledger.py — helper to hash artifact files and append ledger entries
- manifest.json — listing of artifacts and provenance header
- manual.md — human-facing quickstart and walkthrough (visual + backend view)
- diagram.puml — PlantUML sequence diagram for the flow

How to use
1. Clone this branch and inspect files.
2. Run the POC locally (see README instructions below). It performs a safe no-op payload and demonstrates an unattended successor executing automatically.

Security & constraints
- This POC is intentionally non-destructive and offline. It does not access external services or modify system files beyond writing into local output/ and provenance.ledger files in the working directory.
- Signatures are simulated placeholders. Use TPM/HSM and real keys for production.

If you want me to open a PR into the default branch or move files elsewhere, confirm and I will proceed.
