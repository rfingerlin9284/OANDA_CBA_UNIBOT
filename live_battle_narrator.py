import os, datetime, time

def log_commander_event(msg):
    print(msg)
    os.makedirs("logs", exist_ok=True)
    with open("logs/clean_ml_stream.log", "a") as f:
        f.write(f"{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} | {msg}\n")

def narrator_boot():
    log_commander_event("=== LIVE BATTLE NARRATOR ONLINE ===")
    log_commander_event("ML, OCO, trade execution, watchdog modules ready for real-time narration.")

def narrator_heartbeat():
    while True:
        log_commander_event("NARRATOR HEARTBEAT | Active commentary, OCO and ML events streaming.")
        time.sleep(7)

if __name__ == "__main__":
    narrator_boot()
    narrator_heartbeat()
