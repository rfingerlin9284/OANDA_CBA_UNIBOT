import sys
import json
import time
import os
from datetime import datetime

def adjust_trailing_stop():
    return round(0.5 + time.time() % 1, 2)

def confirm_oco(mission):
    return "take_profit" in mission and "stop_loss" in mission

def shepherd_trade(mission_file):
    with open(mission_file, 'r') as f:
        mission = json.load(f)

    print(f"[🎯] TRADE STARTED — {mission['pair']} | {mission['direction'].upper()}")

    if not confirm_oco(mission):
        print("[❌] OCO missing — aborting mission.")
        return

    for step in range(10):
        sl_trail = adjust_trailing_stop()
        print(f"[🔄] {mission['pair']} | Trail SL: {sl_trail}")
        time.sleep(1)

    report = {
        "pair": mission["pair"],
        "status": "closed",
        "pnl": round(3.5 * time.time() % 5, 2),
        "closed_at": str(datetime.utcnow()),
        "origin": mission
    }

    os.makedirs("logs", exist_ok=True)
    with open(f"logs/report_{int(time.time())}.json", "w") as f:
        json.dump(report, f, indent=2)

    print("[📦] Trade complete. Report logged.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[❌] Usage: python3 trade_shepherd.py <mission_file>")
        sys.exit(1)
    shepherd_trade(sys.argv[1])
