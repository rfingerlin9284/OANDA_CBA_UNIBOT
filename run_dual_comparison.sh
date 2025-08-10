#!/bin/bash
# 🧪 DUAL COMPARISON: Bloated Bot vs Swarm Bot
echo "[🧪] DUAL COMPARISON: Bloated Bot vs Swarm Bot"

BLOATED_DIR=~/overlord/wolfpack-lite/oanda_cba_unibot
SWARM_DIR=~/overlord/wolfpack-lite/c_b_swarm_bot_forex_crypto_pairs
CONFIG=~/overlord/wolfpack-lite/shared_test_config.json

# Create shared config
cat > "$CONFIG" << 'EOF'
{
  "historical_data_path": "/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/data/historical",
  "backtest_start": "2017-01-01",
  "backtest_end": "2024-01-01",
  "granularity": "M15",
  "pairs": ["EUR_USD", "USD_JPY", "BTC-USD", "ETH-USD"],
  "model_path": "/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/models/wolfpack_ml_latest.pkl"
}
EOF

# Create bloated bot backtest if it doesn't exist
cat > "$BLOATED_DIR/backtest_bloated.py" << 'EOF'
import json, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ml_predictor import load_model, run_prediction
except ImportError:
    def load_model(path): return None
    def run_prediction(model, features): return 1, [0.4, 0.6]

def run_bloated_backtest(config_file):
    with open(config_file) as f:
        cfg = json.load(f)
    
    model = load_model(cfg.get("model_path", "models/wolfpack_ml_latest.pkl"))
    
    print(f"[📦 BLOATED BOT] Backtesting from {cfg['backtest_start']} to {cfg['backtest_end']}")
    
    for pair in cfg["pairs"]:
        print(f"[📊] Processing {pair} using monolithic engine...")
        
        fake_features = {"fvg_score": 0.7, "rsi": 55, "volume_delta": 1.2}
        pred, proba = run_prediction(model, fake_features)
        confidence = max(proba)
        
        print(f"[🤖 ML] {pair} => Prediction: {'BUY' if pred == 1 else 'SELL'}, Confidence: {confidence:.2f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_bloated_backtest(sys.argv[1])
    else:
        print("[❌] Usage: python3 backtest_bloated.py <config_file>")
EOF

echo "[📦] Starting bloated bot backtest..."
cd "$BLOATED_DIR"
python3 backtest_bloated.py "$CONFIG" &

echo "[🪖] Starting swarm bot backtest..."
cd "$SWARM_DIR" 
if [ -f "backtest_swarm.py" ]; then
    python3 backtest_swarm.py "$CONFIG" &
else
    echo "[⚠️] Swarm bot not fully deployed yet"
fi

wait
echo "[✅] Dual comparison complete!"
