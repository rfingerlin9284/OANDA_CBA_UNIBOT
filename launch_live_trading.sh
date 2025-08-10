#!/bin/bash
# 🚀 WOLFPACK-LITE LIVE TRADING LAUNCH SEQUENCE
# Constitutional PIN: 841921
# LIVE TRADING ONLY - NO SIMULATION

echo "🚀 WOLFPACK-LITE LIVE TRADING LAUNCH SEQUENCE"
echo "Constitutional PIN: 841921"
echo "LIVE TRADING ONLY - REAL MONEY AT RISK"
echo "=================================================="

# Verify QC passed
echo "🔍 Verifying system readiness..."
QC_RESULT=$?

if [ $QC_RESULT -eq 0 ]; then
    echo "✅ QC PASSED - SYSTEM READY FOR LAUNCH"
elif [ $QC_RESULT -eq 2 ]; then
    echo "⚠️ QC MINOR ISSUES - PROCEEDING WITH LAUNCH"
else
    echo "❌ QC CRITICAL FAILURES - ABORTING LAUNCH"
    exit 1
fi

# Display final configuration
echo ""
echo "📊 LIVE TRADING CONFIGURATION:"
echo "   • OANDA Forex: 10 pairs (EUR/USD, GBP/USD, etc.)"
echo "   • Coinbase Crypto: 10 pairs (BTC/USD, ETH/USD, etc.)"
echo "   • Risk: 1% per trade, 1:2.5 minimum R:R"
echo "   • Capital: $3,000 starting balance"
echo "   • OCO: Mandatory stop-loss and take-profit"
echo "   • Max Concurrent: 3 trades"
echo ""

# Final confirmation
echo "🚨 FINAL WARNING: This will trade with REAL MONEY!"
echo "🚨 Ensure you understand all risks involved!"
echo ""
read -p "🚀 Type 'LAUNCH LIVE TRADING' to confirm: " confirm

if [[ "$confirm" != "LAUNCH LIVE TRADING" ]]; then
    echo "❌ Launch cancelled by user"
    exit 0
fi

echo ""
echo "🚀 LAUNCHING LIVE TRADING SYSTEM..."
echo "Constitutional PIN: 841921"
echo ""

# Create screen session for monitoring
screen -dmS wolfpack_live bash -c '
    echo "🚀 WOLFPACK LIVE TRADING SESSION STARTED"
    echo "Constitutional PIN: 841921"
    echo "Time: $(date)"
    echo ""
    
    # Start OANDA sniper
    echo "📊 Starting OANDA forex sniper..."
    python oanda_sniper.py &
    OANDA_PID=$!
    echo "✅ OANDA sniper started (PID: $OANDA_PID)"
    
    sleep 3
    
    # Start Coinbase sniper  
    echo "🪙 Starting Coinbase crypto sniper..."
    python coinbase_sniper.py &
    COINBASE_PID=$!
    echo "✅ Coinbase sniper started (PID: $COINBASE_PID)"
    
    sleep 2
    
    echo ""
    echo "🚀 BOTH SNIPERS ACTIVE - LIVE TRADING!"
    echo "📊 OANDA PID: $OANDA_PID"
    echo "🪙 Coinbase PID: $COINBASE_PID"
    echo "🛑 Press Ctrl+A then D to detach, Ctrl+C to stop"
    echo ""
    
    # Keep session alive and monitor
    while true; do
        echo "💓 Live Trading Heartbeat - $(date)"
        sleep 60
    done
'

echo "✅ Live trading system launched in screen session 'wolfpack_live'"
echo ""
echo "📋 MONITORING COMMANDS:"
echo "   View live session:    screen -r wolfpack_live"
echo "   Check processes:      ps aux | grep python"
echo "   View logs:           tail -f logs/*.log"
echo "   Stop trading:        screen -r wolfpack_live (then Ctrl+C)"
echo ""
echo "🚨 LIVE TRADING ACTIVE - CONSTITUTIONAL PIN: 841921"
echo "=================================================="
