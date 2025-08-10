#!/bin/bash
# 🔥 AUTO-MONITORING DAEMON - RBOTzilla Elite 18+18
# Constitutional PIN: 841921
# Auto-launches all monitoring terminals when needed

DAEMON_PID_FILE="/tmp/rbotzilla_monitor_daemon.pid"
LOG_DIR="logs"
MONITOR_STATE_FILE="/tmp/monitor_states.json"

# Initialize default states (OPEN, CONNECTED, LIVE)
init_monitor_states() {
    cat > "$MONITOR_STATE_FILE" << 'EOF'
{
    "health_monitor": {
        "enabled": true,
        "status": "LIVE",
        "terminal_id": null,
        "log_file": "logs/ping_output.log"
    },
    "trading_monitor": {
        "enabled": true, 
        "status": "LIVE",
        "terminal_id": null,
        "log_file": "logs/swarm_stdout.log"
    },
    "dashboard_monitor": {
        "enabled": true,
        "status": "LIVE", 
        "terminal_id": null,
        "log_file": "logs/dashboard_stdout.log"
    },
    "system_monitor": {
        "enabled": true,
        "status": "LIVE",
        "terminal_id": null,
        "log_file": "logs/system_status.json"
    },
    "error_monitor": {
        "enabled": true,
        "status": "LIVE",
        "terminal_id": null,
        "log_file": "logs/swarm_stderr.log"
    }
}
EOF
}

# Function to launch a monitoring terminal
launch_monitor_terminal() {
    local monitor_name=$1
    local log_file=$2
    local title=$3
    
    # Create monitoring script for this specific monitor
    cat > "/tmp/monitor_${monitor_name}.sh" << EOF
#!/bin/bash
echo "🔥 ${title} - Constitutional PIN: 841921 🔥"
echo "============================================="
echo "📊 Monitoring: ${log_file}"
echo "🔄 Auto-refresh active"
echo "❌ Press Ctrl+C to close"
echo "============================================="
echo ""

# Monitor the log file with auto-restart
while true; do
    if [ -f "${log_file}" ]; then
        tail -f "${log_file}" 2>/dev/null | while read line; do
            echo "[$(date '+%H:%M:%S')] \$line"
        done
    else
        echo "⏳ Waiting for ${log_file} to be created..."
        sleep 5
    fi
    
    # If tail exits, restart it
    sleep 1
done
EOF
    
    chmod +x "/tmp/monitor_${monitor_name}.sh"
    
    # Launch in new terminal (VS Code integrated terminal)
    echo "🚀 Launching ${title} monitor..."
    nohup bash "/tmp/monitor_${monitor_name}.sh" > "/tmp/${monitor_name}_output.log" 2>&1 &
    local pid=$!
    echo $pid > "/tmp/${monitor_name}_terminal.pid"
    
    return $pid
}

# Function to check and restart dead monitors
check_and_restart_monitors() {
    local monitors=("health_monitor" "trading_monitor" "dashboard_monitor" "system_monitor" "error_monitor")
    local titles=("HEALTH STATUS MONITOR" "TRADING ACTIVITY MONITOR" "DASHBOARD ACTIVITY MONITOR" "SYSTEM STATUS MONITOR" "ERROR MONITOR")
    local log_files=("logs/ping_output.log" "logs/swarm_stdout.log" "logs/dashboard_stdout.log" "logs/system_status.json" "logs/swarm_stderr.log")
    
    for i in "${!monitors[@]}"; do
        local monitor="${monitors[$i]}"
        local title="${titles[$i]}"
        local log_file="${log_files[$i]}"
        local pid_file="/tmp/${monitor}_terminal.pid"
        
        # Check if monitor is enabled
        local enabled=$(python3 -c "import json; data=json.load(open('$MONITOR_STATE_FILE')); print(data['$monitor']['enabled'])" 2>/dev/null || echo "true")
        
        if [ "$enabled" = "True" ] || [ "$enabled" = "true" ]; then
            # Check if terminal is still running
            if [ -f "$pid_file" ]; then
                local pid=$(cat "$pid_file")
                if ! kill -0 "$pid" 2>/dev/null; then
                    echo "🔄 Restarting $title monitor (PID $pid died)"
                    launch_monitor_terminal "$monitor" "$log_file" "$title"
                fi
            else
                echo "🚀 Starting $title monitor for first time"
                launch_monitor_terminal "$monitor" "$log_file" "$title"
            fi
        else
            # Monitor is disabled, kill if running
            if [ -f "$pid_file" ]; then
                local pid=$(cat "$pid_file")
                kill "$pid" 2>/dev/null && rm "$pid_file"
                echo "⏹️ Stopped $title monitor (disabled)"
            fi
        fi
    done
}

# Main daemon loop
daemon_main() {
    echo "🔥 RBOTzilla Auto-Monitor Daemon Started - Constitutional PIN: 841921"
    echo "📅 Started: $(date)"
    echo "🎯 Monitoring 5 output streams with auto-restart"
    
    # Initialize states if not exists
    [ ! -f "$MONITOR_STATE_FILE" ] && init_monitor_states
    
    while true; do
        check_and_restart_monitors
        sleep 10  # Check every 10 seconds
    done
}

# Control functions
start_daemon() {
    if [ -f "$DAEMON_PID_FILE" ] && kill -0 "$(cat "$DAEMON_PID_FILE")" 2>/dev/null; then
        echo "✅ Daemon already running (PID: $(cat "$DAEMON_PID_FILE"))"
        return 0
    fi
    
    echo "🚀 Starting RBOTzilla Auto-Monitor Daemon..."
    daemon_main &
    echo $! > "$DAEMON_PID_FILE"
    echo "✅ Daemon started (PID: $!)"
    
    # Also create the API endpoints for dashboard toggles
    create_dashboard_api
}

stop_daemon() {
    if [ -f "$DAEMON_PID_FILE" ]; then
        local pid=$(cat "$DAEMON_PID_FILE")
        if kill "$pid" 2>/dev/null; then
            echo "⏹️ Daemon stopped (PID: $pid)"
            rm "$DAEMON_PID_FILE"
            
            # Clean up monitor terminals
            for pid_file in /tmp/*_terminal.pid; do
                [ -f "$pid_file" ] && kill "$(cat "$pid_file")" 2>/dev/null && rm "$pid_file"
            done
        else
            echo "⚠️ Daemon not running"
            rm "$DAEMON_PID_FILE" 2>/dev/null
        fi
    else
        echo "⚠️ Daemon not running"
    fi
}

# Create dashboard API integration
create_dashboard_api() {
    cat > "dashboard/monitor_api.py" << 'EOF'
#!/usr/bin/env python3
"""
🎮 DASHBOARD MONITOR API - Toggle Controls
Constitutional PIN: 841921
"""
import json
import os
from flask import Flask, request, jsonify

MONITOR_STATE_FILE = "/tmp/monitor_states.json"

def load_monitor_states():
    try:
        with open(MONITOR_STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_monitor_states(states):
    with open(MONITOR_STATE_FILE, 'w') as f:
        json.dump(states, f, indent=2)

app = Flask(__name__)

@app.route('/api/monitors', methods=['GET'])
def get_monitors():
    """Get all monitor states"""
    states = load_monitor_states()
    return jsonify(states)

@app.route('/api/monitors/<monitor_name>/toggle', methods=['POST'])
def toggle_monitor(monitor_name):
    """Toggle a specific monitor on/off"""
    states = load_monitor_states()
    
    if monitor_name in states:
        states[monitor_name]['enabled'] = not states[monitor_name]['enabled']
        states[monitor_name]['status'] = "LIVE" if states[monitor_name]['enabled'] else "OFFLINE"
        save_monitor_states(states)
        
        return jsonify({
            "success": True,
            "monitor": monitor_name,
            "enabled": states[monitor_name]['enabled'],
            "status": states[monitor_name]['status']
        })
    else:
        return jsonify({"error": "Monitor not found"}), 404

@app.route('/api/monitors/toggle-all', methods=['POST'])
def toggle_all_monitors():
    """Toggle all monitors on/off"""
    data = request.get_json()
    enable_all = data.get('enable', True)
    
    states = load_monitor_states()
    for monitor in states:
        states[monitor]['enabled'] = enable_all
        states[monitor]['status'] = "LIVE" if enable_all else "OFFLINE"
    
    save_monitor_states(states)
    return jsonify({"success": True, "all_enabled": enable_all})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
EOF
    
    echo "✅ Dashboard API created for monitor toggles"
}

# Command handling
case "${1:-start}" in
    start)
        start_daemon
        ;;
    stop)
        stop_daemon
        ;;
    restart)
        stop_daemon
        sleep 2
        start_daemon
        ;;
    status)
        if [ -f "$DAEMON_PID_FILE" ] && kill -0 "$(cat "$DAEMON_PID_FILE")" 2>/dev/null; then
            echo "✅ Daemon running (PID: $(cat "$DAEMON_PID_FILE"))"
            echo "📊 Monitor states:"
            cat "$MONITOR_STATE_FILE" 2>/dev/null || echo "No states file"
        else
            echo "❌ Daemon not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "🔥 RBOTzilla Auto-Monitor Daemon - Constitutional PIN: 841921"
        echo "🎯 Automatically manages all monitoring terminals"
        echo "🎮 Integrates with dashboard for toggle controls"
        echo "⚡ Default state: OPEN, CONNECTED, LIVE"
        ;;
esac
