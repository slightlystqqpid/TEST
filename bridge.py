from renderer import render
from encoder import encode
from transfer import send
from ingest import ingest
from delta import compute
from ledger import log

src = input("Paste URL or text: ")

artifact = render(src)
log("RENDER_COMPLETE")

encoded = encode(artifact)
log("ENCODE_COMPLETE")

token = send(encoded)
log(f"TRANSFER::{token}")

content = ingest(token)
log("INGEST_COMPLETE")

old = ""
delta = compute(old, content)
log("DELTA_COMPLETE")

print("\n--- INGESTED ---\n", content[:500])
