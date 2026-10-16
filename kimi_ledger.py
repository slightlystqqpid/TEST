#!/usr/bin/env python3
import json,hashlib,sys
from pathlib import Path
import blake3
from datetime import datetime

LEDGER = Path('provenance.ledger')

def hash_file(path):
    b = Path(path).read_bytes()
    import hashlib
    return hashlib.sha256(b).hexdigest(), blake3.blake3(b).hexdigest()

def append_entry(entry: dict):
    entry_json = json.dumps(entry, separators=(',',':'), sort_keys=True)
    with LEDGER.open('a') as f:
        f.write(entry_json+'\n')
    return entry_json

if __name__=='__main__':
    print('Usage: python kimi_ledger.py artifact_file.json actor reviewer notes')
    if len(sys.argv) < 4:
        print('example: python kimi_ledger.py transcript.json alpha alice "initial run"')
        sys.exit(1)
    artifact = sys.argv[1]
    actor = sys.argv[2]
    reviewer = sys.argv[3]
    notes = ' '.join(sys.argv[4:]) if len(sys.argv)>4 else ''
    sha256,blake3h = hash_file(artifact)
    entry = {
        "event":"manual_append",
        "actor":actor,
        "artifact_file":artifact,
        "sha256":sha256,
        "blake3":blake3h,
        "reviewer":reviewer,
        "timestamp":datetime.utcnow().isoformat()+'Z',
        "notes":notes
    }
    out = append_entry(entry)
    print('Appended to ledger:', out)
