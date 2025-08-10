
# === TELEMETRY LOGGER START ===
import json, os
from datetime import datetime

def log_telemetry(prediction, confidence, model_name):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "model": model_name
    }
    with open("logs/ml_predictions.log", "a") as f:
        f.write("ML DECISION: " + json.dumps(payload) + "\n")
# === TELEMETRY LOGGER END ===
