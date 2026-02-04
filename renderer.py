import requests, pathlib

def render(source: str):
    path = pathlib.Path("artifacts/target.txt")
    try:
        if source.startswith("http"):
            r = requests.get(f"https://r.jina.ai/{source}", timeout=15)
            r.raise_for_status()
            path.write_text(r.text, encoding="utf-8")
        else:
            path.write_text(source, encoding="utf-8")
        return path
    except Exception as e:
        path.write_text(f"[ERROR] {e}", encoding="utf-8")
        return path
