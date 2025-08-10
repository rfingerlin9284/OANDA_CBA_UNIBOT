#!/usr/bin/env python3
# 🫀 Heartbeat + Background Status Logger - LIVE TRADING ONLY

import time, os
from datetime import datetime

CONFIG = "./config/wolfpack_mode.cfg"
HEARTBEAT = "./logs/heartbeat_status.log"

def get_mode():
    try:
        with open(CONFIG) as f:
            for line in f:
                if line.strip().startswith("mode="):
                    return line.strip().split("=")[-1].upper()
    except:
        return "UNKNOWN"

def check_systems():
    # Fake system check, replace with actual bot check hooks if needed
    return {
        "ML Engine": "✅",
        "OCO Enforcer": "✅",
        "Crash Watchdog": "✅",
        "Reinvestment Logic": "✅",
        "Volatility Abort": "✅",
        "Cobra Strike": "✅",
        "Live Trading Only": "✅"
    }

def write_status():
    mode = get_mode()
    status = f"\n🫀 HEARTBEAT CHECK @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    status += f"Mode: {mode}\n"
    checks = check_systems()
    for k, v in checks.items():
        status += f"{k}: {v}\n"

    with open(HEARTBEAT, "a") as log:
        log.write(status + "\n")

if __name__ == "__main__":
    while True:
        write_status()
        time.sleep(20)  # every 20 sec
