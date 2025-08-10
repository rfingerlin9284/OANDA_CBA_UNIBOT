#!/bin/bash
# 🚀 RBOTZILLA LIVE MODE LAUNCHER
# Constitutional PIN: 841921

echo "🔐 CONSTITUTIONAL PIN VERIFICATION"
read -s -p "Enter Constitutional PIN: " PIN
echo ""

if [ "$PIN" != "841921" ]; then
    echo "❌ INVALID PIN - ACCESS DENIED"
    exit 1
fi

echo "✅ PIN VERIFIED - LAUNCHING LIVE SWARM"
echo "🔥 SWITCHING TO LIVE MODE - REAL MONEY AT RISK"
echo "Press Ctrl+C to stop the swarm at any time"
echo ""

# Launch with live mode flags
python3 main.py --live --secure --constitutional-pin 841921 --narration
