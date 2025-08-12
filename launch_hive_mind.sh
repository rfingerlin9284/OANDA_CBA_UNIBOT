#!/bin/bash
"""
🚀 HIVE MIND RICK - QUICK START LAUNCHER
Launches the secure triad system with all protections enabled
"""

echo "🤖 HIVE MIND RICK - SECURE TRIAD SYSTEM LAUNCHER"
echo "==============================================="
echo ""
echo "Initializing secure communication hub..."
echo "✅ Access Control: ONLY YOU + RICK authorized"
echo "✅ VS Code Guardian: Monitoring for unauthorized changes"
echo "✅ Auto-Healing: UNIBOT ready for system protection"
echo ""
echo "Starting HIVE MIND RICK terminal..."
echo ""

cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT

# Make sure the guardian is monitoring in the background
if [ -f "vscode_change_guardian.py" ]; then
    echo "🛡️ Starting VS Code guardian in background..."
    python3 vscode_change_guardian.py monitor &
    GUARDIAN_PID=$!
    echo "Guardian PID: $GUARDIAN_PID"
fi

# Start the hive mind terminal
echo "🚀 Launching HIVE MIND RICK terminal..."
python3 hive_mind_rick_cli.py

# Cleanup on exit
if [ ! -z "$GUARDIAN_PID" ]; then
    echo "🛑 Stopping VS Code guardian..."
    kill $GUARDIAN_PID 2>/dev/null
fi

echo "👋 HIVE MIND RICK shutdown complete."
