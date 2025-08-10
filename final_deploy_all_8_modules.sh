#!/bin/bash
# 🏠 Final Deployment: RBOTzilla Overlord (All 8 Modules)
# Created on: 2025-08-07 01:00:24

ROOT="/home/ing/overlord/wolfpack-lite/oanda_cba_unibot"
cd "$ROOT" || exit 1

echo "🚀 Deploying RBOTzilla Overlord - All Modules"

# 1. Start Flask-SocketIO WebSocket Server
nohup python3 dashboard/socket_stream_server.py >> logs/socketio.log 2>&1 &
echo "🧠 Flask-SocketIO WebSocket Server started"

# 2. Start Live Battle Narrator
nohup python3 live_battle_narrator.py >> logs/live_battle_narrator.log 2>&1 &
echo "🎤 Live Battle Narrator started"

# 3. Start Flask Web Dashboard UI
cd "$ROOT/dashboard"
nohup python3 app.py >> ../logs/dashboard.log 2>&1 &
cd "$ROOT"
echo "🖥️ Web Dashboard Interface started"

# 4. Start OCO Enforcer Watchdog
nohup python3 watchdogs/oco_enforcer.py >> logs/oco_enforcer.log 2>&1 &
echo "🛡️ OCO Enforcer Watchdog started"

# 5. Start ML Telemetry Logger
nohup python3 ml/ml_telemetry_logger.py >> logs/ml_predictions.log 2>&1 &
echo "📊 ML Telemetry Logger started"

# 6. Start Market Routers (OANDA + CBA)
nohup python3 router_oanda_live.py >> logs/oanda_router.log 2>&1 &
nohup python3 router_coinbase_live.py >> logs/coinbase_router.log 2>&1 &
echo "📡 Routers (OANDA + Coinbase Advanced) started"

# 7. Start System Health Auditor
nohup python3 watchdogs/system_health_auditor.py >> logs/system_health.log 2>&1 &
echo "📈 System Health Auditor started"

# 8. Start Command API + Status Broadcaster
nohup python3 dashboard/status_broadcaster.py >> logs/status_api.log 2>&1 &
echo "📡 Command Receiver + Status Broadcaster started"

echo "✅ ALL MODULES LAUNCHED SUCCESSFULLY"
