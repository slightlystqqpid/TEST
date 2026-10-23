# SYZYGY Master Runbook

## Environment bootstrap

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python - <<'PY'
from syzygy.bootstrap import bootstrap_environment
bootstrap_environment('.')
print('bootstrap complete')
PY
```

## Validation

```bash
pytest -q
```

## Expected results

- `manifest.json` exists and contains lifecycle states.
- `agent_registry.json` contains seeded agents.
- `layer_registry.json` is created for dependency control.
- Tests pass under Python 3.11+.

## Security notes

- Human approval for protected actions must check an explicit credential.
- Approval is bound to the reviewed artifact version and checksum.
- Audit receipts are chain-verified but cannot prove truth beyond integrity.
