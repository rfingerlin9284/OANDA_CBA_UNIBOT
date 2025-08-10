import os
import json
import time
import uuid
from datetime import datetime


FOREX_PAIRS = ["EUR_USD", "USD_JPY", "GBP_USD"]
CRYPTO_PAIRS = ["BTC-USD", "ETH-USD", "SOL-USD"]
MISSIONS_PATH = "missions"

def detect_fvg(pair):
    return {
        "pair": pair,
        "direction": "buy",
        "confidence": 0.91,
        "fvg_score": 0.77,
        "fibonacci_ratio": 3,
        "timestamp": str(datetime.utcnow()),
        "take_profit": 2.1,
        "stop_loss": 1.1
    }

def already_active(pair):
    if not os.path.exists(MISSIONS_PATH):
        return False
    for f in os.listdir(MISSIONS_PATH):
        if f.endswith(".json"):
            with open(os.path.join(MISSIONS_PATH, f), 'r') as mf:
                try:
                    mdata = json.load(mf)
                    if mdata.get("pair") == pair:
                        return True
                except:
                    continue
    return False

def launch_mini_bot(mission_data):
    bot_id = str(uuid.uuid4())[:8]
    os.makedirs(MISSIONS_PATH, exist_ok=True)
    filename = f"{MISSIONS_PATH}/mission_{bot_id}.json"
    with open(filename, "w") as f:
        json.dump(mission_data, f, indent=2)
    os.system(f"nohup python3 trade_shepherd.py {filename} &")

def run_fvg_controller():
    pairs = FOREX_PAIRS + CRYPTO_PAIRS
    while True:
        for pair in pairs:
            if already_active(pair):
                print(f"[⏳] {pair} already has an active mission. Skipping.")
                continue
            signal = detect_fvg(pair)
            if signal["confidence"] >= 0.90 and signal["fibonacci_ratio"] >= 3:
                print(f"[🚨] SIGNAL: {pair} | Deploying mini-bot...")
                launch_mini_bot(signal)
            else:
                print(f"[🧪] {pair} skipped — no valid signal.")
        time.sleep(5)

if __name__ == "__main__":
    print(f"[🧠] WOLF CONTROLLER ACTIVE — ENV: {ENVIRONMENT.upper()}")
    run_fvg_controller()
