#!/bin/bash
# 🎪 COMPREHENSIVE LIVE FEED - All Trading Activity
# Constitutional PIN: 841921

echo "🎪 Starting Comprehensive Live Feed..."
echo "🔐 Constitutional PIN: 841921"

# Create a multi-window live feed
{
    echo "🔥 === RBOTzilla Elite 18+18 LIVE FEED === 🔥"
    echo "Constitutional PIN: 841921 | Started: $(date)"
    echo ""
    
    # Monitor all log files liveultaneously
    (
        echo "📊 HEALTH PING MONITOR:"
        tail -f logs/ping_output.log 2>/dev/null | while read line; do
            echo "   🟢 $line"
        done
    ) &
    
    (
        echo "💹 TRADING ACTIVITY MONITOR:"
        tail -f logs/swarm_stdout.log 2>/dev/null | while read line; do
            if echo "$line" | grep -qE "(TRADE|BUY|SELL|PROFIT|LOSS|EUR|USD|BTC|ETH)"; then
                echo "   📈 $line"
            fi
        done
    ) &
    
    (
        echo "🌐 DASHBOARD ACTIVITY:"
        tail -f logs/dashboard_stdout.log 2>/dev/null | while read line; do
            if echo "$line" | grep -qE "(GET /api|POST |ERROR|stats)"; then
                echo "   🌐 $line"
            fi
        done
    ) &
    
    wait
} | tee live_feed_output.log
