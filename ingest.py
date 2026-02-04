import json

def ingest(token):
    path = f"memory/{token.replace('TOKEN::','')}"
    obj = json.loads(open(path).read())
    return obj["content"]
