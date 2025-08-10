#!/bin/bash
# === RBOTzilla 18x18 Unibot Headless Launcher ===

cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot

echo "🧠 Starting RBOTzilla LIVE HEADLESS MODE..."

source coinbase_env/bin/activate

# Check/launch logs
mkdir -p logs
touch logs/live_trades.log logs/ml_predictions.log logs/oco_enforcer.log logs/clean_ml_stream.log

# Launch ML core (runs your 18x18 models)
nohup python3 main.py > logs/main.log 2>&1 &

# Launch OANDA+Coinbase router (for orders/execution)
nohup python3 router_oanda_live.py > logs/oanda_router.log 2>&1 &
nohup python3 router_coinbase_live.py > logs/coinbase_router.log 2>&1 &

# Launch OCO enforcer (protects TP/SL)
nohup python3 oco_enforcer.py > logs/oco_enforcer.log 2>&1 &

# Launch trade narrator (commander-level output)
nohup python3 live_battle_narrator.py > logs/narrator.log 2>&1 &

# Auto-restarting clean commander stream in its own terminal window (or tmux pane)
while true; do
  python3 full_battle_stream.py
  echo "⚠️ Stream closed or crashed — restarting in 2s..."
  sleep 2
done
