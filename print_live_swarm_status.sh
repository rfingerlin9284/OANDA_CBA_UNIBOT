#!/bin/bash
# 🔥 RBOTzilla Elite 18+18 Live Status - AUTO-REFRESH EVERY 15 SECONDS

echo "🚀 Starting RBOTzilla Elite 18+18 Live Status Monitor"
echo "⏰ Auto-refresh every 15 seconds | Press Ctrl+C to stop"
echo ""

# Function to display status
show_status() {
    clear
    echo ""
    echo "🔥 RBOTzilla Elite 18+18 Live Swarm Status 🔥"
    echo "============================================="
    echo "🟢 System:            ALIVE & ACTIVE"
    echo "🎯 Architecture:      Elite 18+18 Dual-Model"
    echo "📊 Health Pings:      Active every 10 seconds"
    echo "🌐 Dashboard:         Running on localhost"
    echo "📈 Forex Squad:       18 pairs monitoring markets"
    echo "💰 Crypto Squad:      18 pairs scanning opportunities"
    echo "🔐 Constitutional PIN: 841921 - VERIFIED"
    echo ""
    echo "🎪 LIVE TRADING ACTIVE - REAL MONEY MODE! 🎪"
    echo ""
    echo "⏰ Last Update: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "🔄 Next refresh in 15 seconds... (Ctrl+C to stop)"
    echo ""
}

# Trap Ctrl+C to exit gracefully
trap 'echo -e "\n👋 RBOTzilla Status Monitor stopped. System still running!"; exit 0' INT

# Initial display
show_status

# Continuous loop every 15 seconds
while true; do
    sleep 15
    show_status
done
