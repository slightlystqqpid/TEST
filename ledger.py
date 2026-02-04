from datetime import datetime

def log(event):
    with open("logs/ulre.log","a") as f:
        f.write(f"{datetime.utcnow()} :: {event}\n")
