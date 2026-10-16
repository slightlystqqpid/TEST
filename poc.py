#!/usr/bin/env python3
"""
POC: SYZYGY Doorbell -> Post Office -> Worker -> Receipt
Non-destructive demo. Uses SQLite for queue and a JSONL provenance ledger.
Run: python3 poc.py
"""
import sqlite3, json, os, hashlib, time, uuid
from datetime import datetime, timezone

DB_FILE = 'postoffice.db'
LEDGER_FILE = 'provenance.ledger'
OUTPUT_DIR = 'output'; os.makedirs(OUTPUT_DIR, exist_ok=True)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

# Utility hashes
def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()

def init_db():
    c = sqlite3.connect(DB_FILE)
    cur = c.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS work_orders(
        work_id TEXT PRIMARY KEY, version INTEGER, seq INTEGER, payload_hash TEXT,
        payload TEXT, status TEXT, created_by TEXT, created_at TEXT)
    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS leases(
        lease_id TEXT PRIMARY KEY, work_id TEXT, worker_id TEXT, expires_at TEXT)
    ''')
    c.commit(); c.close()

# Append one-line JSON to ledger
def append_ledger(entry):
    with open(LEDGER_FILE,'a') as f:
        f.write(json.dumps(entry, separators=(',',':')) + "\n")

# Create a safe no-op payload and enqueue
def create_work(title='noop-demo'):
    work_id = f"wf-{int(time.time())}-{str(uuid.uuid4())[:8]}"
    payload = {"task":"noop","params":{"message":"hello from poc","title":title}}
    payload_bytes = json.dumps(payload, separators=(',',':')).encode('utf-8')
    p_hash = 'sha256:' + sha256_hex(payload_bytes)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('INSERT INTO work_orders(work_id,version,seq,payload_hash,payload,status,created_by,created_at) VALUES (?,?,?,?,?,?,?,?)',
                (work_id,1,1,p_hash,json.dumps(payload), 'queued', 'alpha', now_iso()))
    conn.commit(); conn.close()
    append_ledger({"event":"work_created","work_id":work_id,"payload_hash":p_hash,"created_at":now_iso()})
    print('Enqueued', work_id)
    return work_id

# Worker polls, claims lease, executes safe action, writes receipts
def worker_poll_and_execute(worker_id='dev-worker-v1'):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT work_id,payload_hash,payload FROM work_orders WHERE status='queued' ORDER BY seq LIMIT 1")
    row = cur.fetchone()
    if not row:
        print('No work found')
        return None
    work_id,p_hash,payload_json = row
    # claim lease
    lease_id = 'lease-' + str(uuid.uuid4())[:8]
    expires = now_iso()
    cur.execute('INSERT INTO leases(lease_id,work_id,worker_id,expires_at) VALUES (?,?,?,?)', (lease_id,work_id,worker_id,expires))
    cur.execute("UPDATE work_orders SET status='claimed' WHERE work_id=?", (work_id,))
    conn.commit()
    conn.close()
    append_ledger({"event":"lease_acquired","work_id":work_id,"lease_id":lease_id,"worker_id":worker_id,"timestamp":now_iso()})
    # simulate execution with checkpoints
    checkpoint=1
    # checkpoint 1: pulled payload
    chk1 = sha256_hex(payload_json.encode('utf-8'))
    receipt1 = {
        "event":"work_receipt","work_id":work_id,"worker_id":worker_id,
        "lease_id":lease_id,"checkpoint":checkpoint,
        "step":"pull-payload","checkpoint_hash":"sha256:"+chk1,
        "step_outcome":"ok","prev_receipt_hash":None,
        "timestamp":now_iso(),"signature":{"scheme":"SIMULATED","signer_id":worker_id,"signature":"SIMULATED_SIG"}
    }
    append_ledger(receipt1)
    print('Checkpoint 1 written')
    # perform safe action: write a line to output file
    filename = os.path.join(OUTPUT_DIR, f"{work_id}.txt")
    with open(filename,'a') as f:
        f.write(f"{now_iso()} - {worker_id} executed noop: {payload_json}\n")
    # checkpoint 2: wrote artifact
    checkpoint += 1
    with open(filename,'rb') as f: b=f.read()
    chk2 = sha256_hex(b)
    receipt2 = {
        "event":"work_receipt","work_id":work_id,"worker_id":worker_id,
        "lease_id":lease_id,"checkpoint":checkpoint,
        "step":"write-artifact","checkpoint_hash":"sha256:"+chk2,
        "step_outcome":"ok","prev_receipt_hash":"sha256:"+chk1,
        "timestamp":now_iso(),"signature":{"scheme":"SIMULATED","signer_id":worker_id,"signature":"SIMULATED_SIG"}
    }
    append_ledger(receipt2)
    print('Checkpoint 2 written, artifact created:', filename)
    # mark completed
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE work_orders SET status='completed' WHERE work_id=?", (work_id,))
    conn.commit(); conn.close()
    append_ledger({"event":"work_completed","work_id":work_id,"worker_id":worker_id,"timestamp":now_iso()})
    # schedule an unattended successor work (preauthorized)
    successor_id = f"wf-{int(time.time())}-{str(uuid.uuid4())[:8]}"
    succ_payload = {"task":"noop","params":{"message":"successor run","title":"successor"}}
    succ_bytes = json.dumps(succ_payload, separators=(',',':')).encode('utf-8')
    succ_hash = 'sha256:' + sha256_hex(succ_bytes)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('INSERT INTO work_orders(work_id,version,seq,payload_hash,payload,status,created_by,created_at) VALUES (?,?,?,?,?,?,?,?)',
                (successor_id,1,2,succ_hash,json.dumps(succ_payload),'queued','system_auto',now_iso()))
    conn.commit(); conn.close()
    append_ledger({"event":"work_created_auto","work_id":successor_id,"payload_hash":succ_hash,"created_at":now_iso()})
    print('Auto successor enqueued', successor_id)
    return work_id

if __name__=='__main__':
    init_db()
    w = create_work()
    time.sleep(1)
    worker_poll_and_execute()
    time.sleep(1)
    print('Done. Inspect provenance.ledger and output/')
