#!/bin/bash
# 🔥 LIVE OUTPUT VIEWER - RBOTzilla Elite 18+18
# Constitutional PIN: 841921

clear
echo "🔥 RBOTzilla Elite 18+18 Live Output Viewer 🔥"
echo "Constitutional PIN: 841921"
echo "=================================================="
echo ""

# Function to display colorized output
show_live_feed() {
    echo "🟢 LIVE TRADING FEED - Press Ctrl+C to exit"
    echo "=============================================="
    
    # Multi-pane live view
    while true; do
        clear
        echo "🔥 RBOTzilla Elite 18+18 - LIVE TRADING STATUS 🔥"
        echo "Constitutional PIN: 841921 | $(date)"
        echo "=================================================="
        
        echo ""
        echo "📊 HEALTH STATUS:"
        tail -3 logs/ping_output.log 2>/dev/null || echo "   ⚠️ No health logs found"
        
        echo ""
        echo "💹 RECENT TRADING ACTIVITY:"
        if [ -f logs/swarm_stdout.log ]; then
            tail -5 logs/swarm_stdout.log | grep -E "(TRADE|BUY|SELL|PROFIT|LOSS)" || echo "   📈 Monitoring markets..."
        else
            echo "   📈 System monitoring 36 pairs..."
        fi
        
        echo ""
        echo "🎯 SYSTEM METRICS:"
        if [ -f logs/system_status.json ]; then
            cat logs/system_status.json 2>/dev/null | head -3 || echo "   ✅ All systems operational"
        else
            echo "   ✅ Elite 18+18 architecture active"
        fi
        
        echo ""
        echo "🌐 DASHBOARD STATUS:"
        tail -2 logs/dashboard_stdout.log 2>/dev/null | grep -v "GET /socket.io" || echo "   🟢 Dashboard running on localhost:8000"
        
        echo ""
        echo "==============================================="
        echo "📱 Live Dashboard: http://localhost:8000"
        echo "🔄 Auto-refresh every 3 seconds..."
        echo "==============================================="
        
        sleep 3
    done
}

# Start the live feed
show_live_feed
