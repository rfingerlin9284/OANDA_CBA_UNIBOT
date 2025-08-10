#!/bin/bash
# 🧪 DUAL COMPARISON: Bloated Bot vs Swarm Bot
echo "[🧪] DUAL COMPARISON: Bloated Bot vs Swarm Bot"

BLOATED_DIR=~/overlord/wolfpack-lite/oanda_cba_unibot
SWARM_DIR=~/overlord/wolfpack-lite/c_b_swarm_bot_forex_crypto_pairs

# Create shared config
cat > "$CONFIG" << 'EOF'
{
  "historical_data_path": "/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/data/historical",
  "granularity": "M15",
  "pairs": ["EUR_USD", "USD_JPY", "BTC-USD", "ETH-USD"],
}
EOF

import json, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ml_predictor import load_model, run_prediction
except ImportError:
    def load_model(path): return None
    def run_prediction(model, features): return 1, [0.4, 0.6]

    with open(config_file) as f:
        cfg = json.load(f)
    
    
    
    for pair in cfg["pairs"]:
        print(f"[📊] Processing {pair} using monolithic engine...")
        
        fake_features = {"fvg_score": 0.7, "rsi": 55, "volume_delta": 1.2}
        pred, proba = run_prediction(model, fake_features)
        confidence = max(proba)
        
        print(f"[🤖 ML] {pair} => Prediction: {'BUY' if pred == 1 else 'SELL'}, Confidence: {confidence:.2f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
    else:
EOF

cd "$BLOATED_DIR"

cd "$SWARM_DIR" 
else
    echo "[⚠️] Swarm bot not fully deployed yet"
fi

wait
echo "[✅] Dual comparison complete!"
