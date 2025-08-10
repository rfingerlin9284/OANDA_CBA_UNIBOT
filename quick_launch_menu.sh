#!/bin/bash
# 🎯 QUICK LAUNCH MENU - RBOTzilla Elite 18+18
# Constitutional PIN: 841921

echo "🔥 RBOTzilla Elite 18+18 - Quick Launch Menu"
echo "Constitutional PIN: 841921"
echo ""
echo "🚀 LAUNCH OPTIONS:"
echo ""
echo "1. 🎛️  Launch Master Auto-Monitor System"
echo "      ./launch_master_auto_monitor.sh"
echo ""
echo "2. 📊  Show Enhanced Live Status"
echo "      ./print_live_swarm_status.sh"
echo ""
echo "3. 🌐  Open Dashboard Control (localhost:5001)"
echo "      http://localhost:5001"
echo ""
echo "4. 📱  Open Main Trading Dashboard (localhost:8000)"
echo "      http://localhost:8000"
echo ""
echo "5. ⚙️   Manual Monitor Controls:"
echo "      python3 auto_monitor_system.py status"
echo "      python3 auto_monitor_system.py toggle [monitor] [on/off/auto-on/auto-off]"
echo ""
echo "🟢 DEFAULT STATUS: OPEN, CONNECTED, LIVE"
echo "🤖 Auto-opening terminals for all new output"
echo "🎛️ Dashboard toggles for complete control"
echo ""

read -p "Enter choice (1-5) or press Enter to exit: " choice

case $choice in
    1)
        echo "🚀 Launching Master Auto-Monitor System..."
        ./launch_master_auto_monitor.sh
        ;;
    2)
        echo "📊 Showing Enhanced Live Status..."
        ./print_live_swarm_status.sh
        ;;
    3)
        echo "🌐 Opening Dashboard Control..."
        echo "Visit: http://localhost:5001"
        ;;
    4)
        echo "📱 Opening Main Trading Dashboard..."
        echo "Visit: http://localhost:8000"
        ;;
    5)
        echo "⚙️ Manual controls available via command line"
        echo "Use: python3 auto_monitor_system.py [status|toggle]"
        ;;
    "")
        echo "👋 Goodbye!"
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
