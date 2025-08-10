#!/bin/bash
# 🧠 DAILY RETRAINING ENGINE FOR ML HYBRID MODELS

echo "[⏰] Running daily retrainer for light + heavy models..."

# Train light model (fast decisions)
python3 scripts/train_light_model.py

# Train heavy model (complex analysis)  
python3 scripts/train_heavy_model.py

echo "[✅] Models retrained and saved to /models/"
echo "[📊] Ready for next trading session with fresh ML models"
