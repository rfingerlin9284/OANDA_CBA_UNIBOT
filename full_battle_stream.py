#!/usr/bin/env python3
import time, os
from termcolor import colored

LOG_FILES = [
    "logs/ml_predictions.log",
    "logs/live_trades.log",
    "logs/oco_enforcer.log",
    "logs/system_health.log",
    "logs/clean_ml_stream.log"
]

KEYWORDS = {
    "ML DECISION": "cyan",
    "LIVE ORDER SENT": "green",
    "EXECUTED": "green",
    "TP": "blue",
    "SL": "red",
    "OCO": "yellow",
    "MINIBOT": "magenta",
    "TRAILING": "yellow",
    "TRIGGERED": "red",
    "HEALTH": "white",
    "ERROR": "red",
    "WARNING": "yellow",
    "BUY": "cyan",
    "SELL": "magenta",
    "HOLD": "white"
}

def color_line(line):
    for keyword, color in KEYWORDS.items():
        if keyword in line.upper():
            return colored(line.strip(), color)
    return colored(line.strip(), "white")

def follow_logs():
    file_handles = {}
    for log in LOG_FILES:
        if os.path.exists(log):
            file_handles[log] = open(log, "r")
            file_handles[log].seek(0, os.SEEK_END)

    while True:
        for path, f in file_handles.items():
            line = f.readline()
            if line:
                print(color_line(line))
        time.sleep(0.2)

if __name__ == "__main__":
    print(colored("🔊 FULL BATTLE STREAM ACTIVE — HUMAN MODE ENABLED\n", "white", attrs=["bold"]))
    follow_logs()
