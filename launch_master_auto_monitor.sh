#!/bin/bash
# 🚀 MASTER AUTO-MONITOR LAUNCHER
# Constitutional PIN: 841921 | Auto-opening terminals, dashboard toggles

echo "🔥 LAUNCHING MASTER AUTO-MONITOR SYSTEM - PIN 841921"
echo "🟢 DEFAULT STATUS: OPEN, CONNECTED, LIVE"

# Kill any existing instances
pkill -f "auto_monitor_system.py" 2>/dev/null
pkill -f "dashboard_toggle_controller.py" 2>/dev/null
sleep 2

echo "🧹 Cleaned up existing instances"

# Create necessary directories
mkdir -p logs templates

# Set permissions
chmod +x auto_monitor_system.py
chmod +x dashboard_toggle_controller.py

echo "✅ Directories and permissions set"

# Start the dashboard toggle controller
echo "🎛️ Starting Dashboard Toggle Controller..."
python3 dashboard_toggle_controller.py &
DASHBOARD_PID=$!
sleep 3

echo "✅ Dashboard Toggle Controller started (PID: $DASHBOARD_PID)"
echo "🌐 Dashboard URL: http://localhost:5001"

# Start the auto-monitor system
echo "🤖 Starting Auto-Monitor System..."
python3 auto_monitor_system.py &
MONITOR_PID=$!
sleep 2

echo "✅ Auto-Monitor System started (PID: $MONITOR_PID)"

# Wait a moment for systems to initialize
echo "⏳ Initializing systems..."
sleep 5

echo ""
echo "🔥 MASTER AUTO-MONITOR SYSTEM: FULLY ACTIVE!"
echo "=============================================="
echo "🎛️ Dashboard Control:  http://localhost:5001"
echo "🤖 Auto-Monitor:       Running (PID: $MONITOR_PID)"
echo "🟢 Default Status:     OPEN, CONNECTED, LIVE"
echo "🔐 Constitutional PIN: 841921"
echo ""
echo "📊 FEATURES:"
echo "   ✅ Auto-opening terminals for new output"
echo "   ✅ Dashboard toggle switches for all monitors"
echo "   ✅ Real-time monitoring of all log feeds"
echo "   ✅ Health, Trading, Dashboard, System, Profit, Error monitors"
echo "   ✅ Default state: ALL MONITORS LIVE & AUTO-OPENING"
echo ""
echo "🎛️ DASHBOARD TOGGLES:"
echo "   🟢 ALL OPEN, CONNECTED, LIVE  (Default)"
echo "   🔴 ALL OFF                    (Manual control)"
echo "   🔄 Individual monitor toggles"
echo ""
echo "📱 ACCESS:"
echo "   Dashboard: http://localhost:5001"
echo "   Main System: http://localhost:8000"
echo ""

# Keep script running and show status
while true; do
    sleep 30
    echo "⏰ $(date '+%H:%M:%S') - Auto-Monitor System: ACTIVE | Dashboard: http://localhost:5001"
done
