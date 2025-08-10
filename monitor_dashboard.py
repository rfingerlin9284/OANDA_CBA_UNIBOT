#!/usr/bin/env python3
"""
🎮 DASHBOARD MONITOR CONTROLS - RBOTzilla Elite 18+18
Constitutional PIN: 841921
Live Toggle Interface for Auto-Monitoring
"""

import json
import os
import subprocess
import time
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
MONITOR_STATE_FILE = "/tmp/monitor_states.json"

class MonitorController:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.init_default_states()
    
    def init_default_states(self):
        """Initialize with OPEN, CONNECTED, LIVE defaults"""
        if not os.path.exists(MONITOR_STATE_FILE):
            default_states = {
                "health_monitor": {
                    "name": "Health Status Monitor",
                    "enabled": True,
                    "status": "LIVE",
                    "log_file": "logs/ping_output.log",
                    "last_update": datetime.now().isoformat()
                },
                "trading_monitor": {
                    "name": "Trading Activity Monitor", 
                    "enabled": True,
                    "status": "LIVE",
                    "log_file": "logs/swarm_stdout.log",
                    "last_update": datetime.now().isoformat()
                },
                "dashboard_monitor": {
                    "name": "Dashboard Activity Monitor",
                    "enabled": True,
                    "status": "LIVE",
                    "log_file": "logs/dashboard_stdout.log",
                    "last_update": datetime.now().isoformat()
                },
                "system_monitor": {
                    "name": "System Status Monitor",
                    "enabled": True,
                    "status": "LIVE",
                    "log_file": "logs/system_status.json",
                    "last_update": datetime.now().isoformat()
                },
                "error_monitor": {
                    "name": "Error Monitor",
                    "enabled": True,
                    "status": "LIVE",
                    "log_file": "logs/swarm_stderr.log",
                    "last_update": datetime.now().isoformat()
                }
            }
            self.save_states(default_states)
    
    def load_states(self):
        try:
            with open(MONITOR_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            self.init_default_states()
            return self.load_states()
    
    def save_states(self, states):
        with open(MONITOR_STATE_FILE, 'w') as f:
            json.dump(states, f, indent=2)
    
    def toggle_monitor(self, monitor_id, force_state=None):
        states = self.load_states()
        if monitor_id in states:
            if force_state is not None:
                states[monitor_id]['enabled'] = force_state
            else:
                states[monitor_id]['enabled'] = not states[monitor_id]['enabled']
            
            states[monitor_id]['status'] = "LIVE" if states[monitor_id]['enabled'] else "OFFLINE"
            states[monitor_id]['last_update'] = datetime.now().isoformat()
            self.save_states(states)
            
            # Trigger daemon to restart monitors
            subprocess.run(['pkill', '-USR1', '-f', 'auto_monitor_daemon'], capture_output=True)
            
            return states[monitor_id]
        return None
    
    def toggle_all(self, enable_all=True):
        states = self.load_states()
        for monitor_id in states:
            states[monitor_id]['enabled'] = enable_all
            states[monitor_id]['status'] = "LIVE" if enable_all else "OFFLINE"
            states[monitor_id]['last_update'] = datetime.now().isoformat()
        
        self.save_states(states)
        subprocess.run(['pkill', '-USR1', '-f', 'auto_monitor_daemon'], capture_output=True)
        return states

controller = MonitorController()

@app.route('/')
def dashboard():
    """Main dashboard with toggle controls"""
    return render_template('monitor_dashboard.html', 
                         constitutional_pin=controller.constitutional_pin)

@app.route('/api/monitors')
def get_monitors():
    """Get all monitor states"""
    states = controller.load_states()
    return jsonify({
        "constitutional_pin": controller.constitutional_pin,
        "timestamp": datetime.now().isoformat(),
        "monitors": states
    })

@app.route('/api/monitors/<monitor_id>/toggle', methods=['POST'])
def toggle_monitor(monitor_id):
    """Toggle specific monitor"""
    result = controller.toggle_monitor(monitor_id)
    if result:
        return jsonify({
            "success": True,
            "constitutional_pin": controller.constitutional_pin,
            "monitor_id": monitor_id,
            "state": result
        })
    return jsonify({"error": "Monitor not found"}), 404

@app.route('/api/monitors/toggle-all', methods=['POST'])
def toggle_all():
    """Toggle all monitors"""
    data = request.get_json()
    enable_all = data.get('enable', True)
    states = controller.toggle_all(enable_all)
    
    return jsonify({
        "success": True,
        "constitutional_pin": controller.constitutional_pin,
        "action": "enable_all" if enable_all else "disable_all",
        "monitors": states
    })

@app.route('/api/restart-daemon', methods=['POST'])
def restart_daemon():
    """Restart the monitoring daemon"""
    try:
        subprocess.run(['./auto_monitor_daemon.sh', 'restart'], 
                      capture_output=True, text=True)
        return jsonify({
            "success": True,
            "message": "Daemon restarted",
            "constitutional_pin": controller.constitutional_pin
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the daemon if not running
    subprocess.run(['./auto_monitor_daemon.sh', 'start'], capture_output=True)
    
    print("🎮 Monitor Dashboard starting on http://localhost:5002")
    print(f"🔐 Constitutional PIN: {controller.constitutional_pin}")
    print("🎯 All monitors default to: OPEN, CONNECTED, LIVE")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
