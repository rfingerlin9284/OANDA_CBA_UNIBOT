#!/bin/bash
echo "🚀 Starting ML Telemetry Writer..."
source coinbase_env/bin/activate
nohup python3 ml_telemetry_writer.py > logs/telemetry_writer.log 2>&1 &
echo "✅ Telemetry Writer running in background. Log: logs/telemetry_writer.log"
