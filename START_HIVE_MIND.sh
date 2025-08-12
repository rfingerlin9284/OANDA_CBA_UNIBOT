#!/bin/bash

# 🚀 HIVE MIND RICK SECURE TRIAD SYSTEM - QUICK LAUNCHER
# This script starts all components of the secure AI overlord system

echo "🤖 HIVE MIND RICK SECURE TRIAD SYSTEM"
echo "======================================"
echo "Initializing AI Dashboard Hybrid with Built-in AI Agent Overlord..."
echo ""

# Set working directory
cd "$(dirname "$0")"

# Check for required environment variables
if [ -z "$OANDA_LIVE_API_KEY" ]; then
    echo "⚠️  Warning: OANDA_LIVE_API_KEY not set. Please configure your environment variables."
    echo "   You can set this in your ~/.bashrc or create a .env file"
    echo ""
fi

echo "🛡️  Starting VS Code Change Guardian..."
python3 vscode_change_guardian.py &
GUARDIAN_PID=$!

echo "🔒 VS Code Protection: ACTIVE (PID: $GUARDIAN_PID)"
echo ""

sleep 2

echo "🚀 Launching HIVE MIND RICK CLI Interface..."
echo "   - Access Control: ONLY YOU and RICK can modify code"
echo "   - Real-time System Monitoring: ENABLED"
echo "   - OCO Trading Protection: ACTIVE"
echo "   - Auto-Healing UNIBOT: STANDBY"
echo ""

# Launch the main HIVE MIND interface
python3 hive_mind_rick_cli.py

echo ""
echo "🛑 Shutting down VS Code Guardian..."
kill $GUARDIAN_PID 2>/dev/null || true

echo "✅ HIVE MIND RICK System shutdown complete."
