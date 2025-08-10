#!/bin/bash
# === RBOTzilla FINAL SWARM LAUNCHER ===
# Author: The AI Commander
# Auto-launches ML, order routing, narrator, OCO, and full battle stream

cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot

echo "🧠 RBOTzilla Swarm Ignition Starting..."
source coinbase_env/bin/activate

# === PIN LOCK (optional override here if not used)
PIN="841921"
echo "🔐 Confirming PIN..."
if [[ "$PIN" != "841921" ]]; then
    echo "❌ Invalid PIN. Abort."
    exit 1
fi

# === Environment Check
ENV_CHECK=$(grep '"environment": "live"' config/live_config.json)
if [[ -z "$ENV_CHECK" ]]; then
    echo "❌ Environment NOT set to live. Please update config/live_config.json"
    exit 1
fi
echo "✅ Environment confirmed: LIVE"

# === STEP 1: ML CORE
echo "🚀 Launching ML Engine (main.py)..."
nohup python3 main.py > logs/main.log 2>&1 &
sleep 1

# === STEP 2: Order Execution
echo "🎯 Launching Order Execution (router_oanda_live.py)..."
nohup python3 router_oanda_live.py > logs/order_router.log 2>&1 &
sleep 1

# === STEP 3: Battle Narrator
echo "🗣️ Launching Narrator (live_battle_narrator.py)..."
nohup python3 live_battle_narrator.py > logs/narrator.log 2>&1 &
sleep 1

# === STEP 4: OCO Enforcer
echo "🛡️ Launching OCO Enforcer..."
nohup python3 oco_enforcer.py > logs/oco_enforcer.log 2>&1 &
sleep 1

# === STEP 5: Terminal Battle Stream
echo "🔊 Launching Full Battle Stream (human readable logs)..."
python3 full_battle_stream.py
