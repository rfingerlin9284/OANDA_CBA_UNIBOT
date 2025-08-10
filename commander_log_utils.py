import os, datetime

def log_commander_event(msg):
    print(msg)
    os.makedirs("logs", exist_ok=True)
    with open("logs/clean_ml_stream.log", "a") as f:
        f.write(f"{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} | {msg}\n")
