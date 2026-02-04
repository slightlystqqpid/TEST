import json, hashlib, gzip, pathlib, datetime

def encode(text_path):
    data = text_path.read_text(encoding="utf-8")
    h = hashlib.sha256(data.encode()).hexdigest()
    payload = {
        "hash": h,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "content": data
    }
    out = pathlib.Path("memory/encoded.json")
    out.write_text(json.dumps(payload, indent=2))
    return out
