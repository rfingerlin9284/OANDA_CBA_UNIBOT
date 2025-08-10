#!/usr/bin/env python3
import time
import json
import os
from termcolor import colored

LOG_FILE = "logs/ml_predictions.log"
SAVE_LOG_FILE = "logs/clean_ml_stream.log"

def color_by_source(system):
    if "coinbase" in system.lower():
        return "red", "🔴 [COINBASE] "
    elif "oanda" in system.lower():
        return "yellow", "🔶 [OANDA]    "
    else:
        return "white", "[UNKNOWN]   "

def format_output(system, model, prediction, confidence, fvg, fib):
    color, system_label = color_by_source(system)
    prediction = prediction.upper().ljust(6)
    fvg_status = "✅ confirmed" if str(fvg).lower() == "confirmed" else "❌ none"
    fib_display = fib if fib else "N/A"

    output = (
        f"{system_label} "
        f"{model.ljust(15)} | "
        f"Prediction: {prediction} | "
        f"Confidence: {confidence:>6.2f}% | "
        f"FVG: {fvg_status.ljust(12)} | "
        f"Fib Level: {fib_display}"
    )
    return colored(output, color), output

def print_filtered(line):
    try:
        if "ML DECISION" not in line:
            return

        payload = json.loads(line.split("ML DECISION:")[1].strip())
        prediction = payload.get("prediction", "UNKNOWN")
        confidence = float(payload.get("confidence", 0)) * 100
        model = payload.get("model", "N/A")
        system = payload.get("system", "N/A")
        fib = payload.get("fibonacci", "N/A")
        fvg = payload.get("fvg_signal", "N/A")

        colored_output, plain_output = format_output(system, model, prediction, confidence, fvg, fib)
        print(colored_output)

        with open(SAVE_LOG_FILE, "a") as log:
            log.write(plain_output + "\n")

    except Exception:
        pass  # Ignore malformed logs

def stream_log():
    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            print_filtered(line)

if __name__ == "__main__":
    stream_log()
