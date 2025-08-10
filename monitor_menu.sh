#!/bin/bash
# 🔥 SIMPLE LIVE MONITOR - RBOTzilla Elite 18+18
# Constitutional PIN: 841921

echo "🎯 Choose your monitoring option:"
echo "================================="
echo "1. Health Status Monitor"
echo "2. Trading Activity Monitor"  
echo "3. Dashboard Activity Monitor"
echo "4. Complete System Monitor"
echo "5. Background Process Status"
echo ""

read -p "Enter option (1-5): " choice

case $choice in
    1)
        echo "📊 Starting Health Status Monitor..."
        tail -f logs/ping_output.log
        ;;
    2)
        echo "💹 Starting Trading Activity Monitor..."
        tail -f logs/swarm_stdout.log 2>/dev/null || echo "No trading logs yet"
        ;;
    3)
        echo "🌐 Starting Dashboard Activity Monitor..."
        tail -f logs/dashboard_stdout.log
        ;;
    4)
        echo "🎪 Starting Complete System Monitor..."
        echo "Press Ctrl+C to stop"
        while true; do
            clear
            echo "🔥 RBOTzilla Elite 18+18 - COMPLETE STATUS 🔥"
            echo "Constitutional PIN: 841921 | $(date)"
            echo "=============================================="
            echo ""
            echo "📊 HEALTH (Last 2):"
            tail -2 logs/ping_output.log
            echo ""
            echo "🌐 DASHBOARD (Active):"
            tail -2 logs/dashboard_stdout.log | grep -E "(api|GET)" || echo "   🟢 Running on localhost:8000"
            echo ""
            echo "🎯 PROCESSES:"
            ps aux | grep -E "(dashboard|python)" | grep -v grep | head -2
            echo ""
            echo "=============================================="
            echo "🔄 Auto-refresh in 5 seconds..."
            sleep 5
        done
        ;;
    5)
        echo "🎯 Background Process Status:"
        ps aux | grep -E "(python|dashboard|main)" | grep -v grep
        echo ""
        echo "📊 System Resources:"
        free -h
        ;;
    *)
        echo "❌ Invalid option"
        ;;
esac
