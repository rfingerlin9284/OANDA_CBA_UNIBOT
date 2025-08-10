#!/usr/bin/env python3
import os, time, json
from termcolor import colored

LOG_FILE = os.path.join("logs", "ml_predictions.log")
FVG_LOG = os.path.join("logs", "clean_ml_stream.log")

def colorize(source, text):
    if "coinbase" in source.lower():
        return colored(text, "red")
    elif "oanda" in source.lower():
        return colored(text, "yellow")
    return text

def follow(filename):
    with open(filename, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()

def parse_and_print(line):
    if not line.strip(): return
    try:
        if line.startswith("ML DECISION: "):
            payload = json.loads(line.replace("ML DECISION: ", ""))
            system = payload.get("system", "")
            model = payload.get("model", "")
            prediction = payload.get("prediction", "")
            confidence = payload.get("confidence", 0)
            fib = payload.get("fibonacci", "N/A")
            fvg = payload.get("fvg_signal", "N/A")
            output = f"[{system}] Model: {model} | Prediction: {prediction} ({round(confidence*100, 2)}%) | FVG: {fvg} | Fib: {fib}"
            print(colorize(system, output))
    except Exception as e:
        print(colored("Parse error: " + str(e), "magenta"))

for line in follow(LOG_FILE):
    parse_and_print(line)
