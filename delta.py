from difflib import SequenceMatcher
import json, pathlib

def compute(old, new):
    ratio = SequenceMatcher(None, old, new).ratio()
    if ratio < 0.82:
        delta = new
    else:
        delta = ""
    out = pathlib.Path("memory/delta.json")
    out.write_text(json.dumps({"delta": delta}))
    return out
