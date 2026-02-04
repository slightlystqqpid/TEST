# ulre_cre_validator.py
import json
import sys
from pathlib import Path
from collections import defaultdict
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path("ulre_cre_event.schema.json")

# HEARTBEAT rules
PAIRINGS = {
    "HEARTBEAT_EMIT": "HEARTBEAT_ACK",
}

TERMINAL_OK = {"VERIFIED"}
TERMINAL_BAD = {"FAILED", "STALLED"}

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_events(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        raise ValueError("Events file must be a JSON object or list of objects.")

def validate_schema(events, schema):
    v = Draft202012Validator(schema)
    errors = []
    for i, e in enumerate(events):
        for err in v.iter_errors(e):
            errors.append((i, err.message))
    return errors

def index_by_lineage(events):
    by_id = {}
    children = defaultdict(list)
    for e in events:
        by_id[e["event_id"]] = e
    for e in events:
        for parent in e.get("lineage", []):
            children[parent].append(e["event_id"])
    return by_id, children

def check_heartbeat_pairs(events):
    emits = []
    acks = set()
    for e in events:
        if e["event_type"] == "HEARTBEAT_EMIT":
            emits.append(e)
        elif e["event_type"] == "HEARTBEAT_ACK":
            acks.add((e["source_id"], e["target_id"], e["content_hash"]))
    orphans = []
    for e in emits:
        key = (e["source_id"], e["target_id"], e["content_hash"])
        if key not in acks:
            orphans.append(e["event_id"])
    return orphans

def check_hash_integrity(events):
    bad = []
    for e in events:
        if e["error_code"] == 600:  # Hash mismatch
            bad.append(e["event_id"])
    return bad

def check_terminals(events):
    dangling = []
    for e in events:
        if e["heartbeat_state"] not in TERMINAL_OK | TERMINAL_BAD:
            # must eventually resolve
            dangling.append(e["event_id"])
    return dangling

def main():
    if len(sys.argv) != 2:
        print("Usage: python ulre_cre_validator.py <events.json>")
        sys.exit(1)

    events_path = Path(sys.argv[1])
    schema = load_schema()
    events = load_events(events_path)

    print(f"Loaded {len(events)} event(s).")

    # 1) Schema validation
    schema_errors = validate_schema(events, schema)
    if schema_errors:
        print("\n❌ Schema errors:")
        for i, msg in schema_errors:
            print(f"  - Event[{i}]: {msg}")
    else:
        print("✅ Schema valid.")

    # 2) Lineage index
    by_id, children = index_by_lineage(events)
    print(f"Lineage index built. Nodes: {len(by_id)}")

    # 3) Heartbeat pairing
    orphans = check_heartbeat_pairs(events)
    if orphans:
        print("\n⚠️ Orphan HEARTBEAT_EMIT (no ACK):")
        for oid in orphans:
            print("  -", oid)
    else:
        print("✅ All heartbeats acknowledged.")

    # 4) Hash integrity
    bad_hash = check_hash_integrity(events)
    if bad_hash:
        print("\n❌ Hash mismatch events:")
        for eid in bad_hash:
            print("  -", eid)
    else:
        print("✅ No hash mismatches flagged.")

    # 5) Terminal states
    dangling = check_terminals(events)
    if dangling:
        print("\n⚠️ Non-terminal (dangling) heartbeat states:")
        for eid in dangling:
            print("  -", eid)
    else:
        print("✅ All events resolved to terminal states.")

    print("\n— ULRE CRE VALIDATION COMPLETE —")

if __name__ == "__main__":
    main()
