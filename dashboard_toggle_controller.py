#!/usr/bin/env python3
"""
🎛️ DASHBOARD TOGGLE CONTROLLER - RBOTzilla Elite 18+18
Constitutional PIN: 841921
Real-time toggle controls for auto-monitor system
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import subprocess
import threading
import time
from datetime import datetime

app = Flask(__name__)

class DashboardToggleController:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.config_file = "monitor_config.json"
        self.load_config()
    
    def load_config(self):
        """Load monitor configuration"""
        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        except:
            # Default configuration - ALL OPEN, CONNECTED, LIVE
            self.config = {
                "health_monitor": {"enabled": True, "auto_open": True},
                "trading_feed": {"enabled": True, "auto_open": True},
                "dashboard_feed": {"enabled": True, "auto_open": True},
                "system_logs": {"enabled": True, "auto_open": True},
                "profit_tracker": {"enabled": True, "auto_open": True},
                "error_monitor": {"enabled": True, "auto_open": True}
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def toggle_monitor(self, monitor_name, field, value):
        """Toggle specific monitor setting"""
        if monitor_name in self.config:
            self.config[monitor_name][field] = value
            self.save_config()
            
            # Restart auto-monitor system to apply changes
            try:
                subprocess.run(["pkill", "-f", "auto_monitor_system.py"], check=False)
                time.sleep(2)
                subprocess.Popen(["python3", "auto_monitor_system.py"], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            except:
                pass
            
            return True
        return False
    
    def get_system_status(self):
        """Get current system status"""
        status = {
            "pin": self.constitutional_pin,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "monitors": self.config,
            "system_health": "ALIVE & ACTIVE"
        }
        
        # Check for active terminals/processes
        try:
            result = subprocess.run(["pgrep", "-f", "tail -f"], 
                                  capture_output=True, text=True)
            status["active_terminals"] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            status["active_terminals"] = 0
        
        return status

# Global controller instance
controller = DashboardToggleController()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('toggle_dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(controller.get_system_status())

@app.route('/api/toggle', methods=['POST'])
def api_toggle():
    """API endpoint to toggle monitor settings"""
    data = request.json
    monitor_name = data.get('monitor')
    field = data.get('field')  # 'enabled' or 'auto_open'
    value = data.get('value')
    
    success = controller.toggle_monitor(monitor_name, field, value)
    
    return jsonify({
        'success': success,
        'message': f'Toggled {monitor_name}.{field} to {value}',
        'status': controller.get_system_status()
    })

@app.route('/api/toggle_all', methods=['POST'])
def api_toggle_all():
    """Toggle all monitors on/off"""
    data = request.json
    enabled = data.get('enabled', True)
    auto_open = data.get('auto_open', True)
    
    for monitor_name in controller.config:
        controller.config[monitor_name]['enabled'] = enabled
        controller.config[monitor_name]['auto_open'] = auto_open
    
    controller.save_config()
    
    # Restart auto-monitor system
    try:
        subprocess.run(["pkill", "-f", "auto_monitor_system.py"], check=False)
        time.sleep(2)
        subprocess.Popen(["python3", "auto_monitor_system.py"], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
    except:
        pass
    
    status_msg = "OPEN, CONNECTED, LIVE" if enabled and auto_open else "DISABLED"
    
    return jsonify({
        'success': True,
        'message': f'All monitors set to: {status_msg}',
        'status': controller.get_system_status()
    })

if __name__ == '__main__':
    # Create templates directory and HTML file
    os.makedirs('templates', exist_ok=True)
    
    # Run the dashboard
    print(f"🎛️ DASHBOARD TOGGLE CONTROLLER STARTING - PIN {controller.constitutional_pin}")
    print("🌐 Dashboard available at: http://localhost:5001")
    print("🟢 DEFAULT STATUS: OPEN, CONNECTED, LIVE")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
