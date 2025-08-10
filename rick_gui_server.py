#!/usr/bin/env python3
"""
🎛️ RICK WEB DASHBOARD - GPT-Style Bot Controller
Mobile + Desktop Ready Flask Server
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import subprocess
import psutil
from datetime import datetime
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

class RickDashboard:
    def __init__(self):
        self.bot_status = {}
        self.chat_history = []
        self.authorized = False
        self.pin_code = os.getenv('RICK_DASHBOARD_PIN', '841921')
        
    def get_system_status(self):
        """Get real-time system status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'bots': {},
            'ml_models': self.check_ml_models(),
            'heartbeat': self.get_heartbeat_status(),
            'config': self.load_config()
        }
        
        # Check bot processes
        bots = [
            ('Heartbeat Monitor', 'heartbeat_checkin.sh')
        ]
        
        for bot_name, process_name in bots:
            status['bots'][bot_name] = {
                'running': self.is_process_running(process_name),
                'uptime': self.get_process_uptime(process_name),
                'cpu': self.get_process_cpu(process_name)
            }
        
        return status
    
    def is_process_running(self, process_name):
        """Check if a process is running"""
        try:
            result = subprocess.run(['pgrep', '-f', process_name], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def get_process_uptime(self, process_name):
        """Get process uptime in seconds"""
        try:
            result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
            if result.returncode == 0:
                pid = result.stdout.strip().split()[0]
                process = psutil.Process(int(pid))
                return time.time() - process.create_time()
        except:
            pass
        return 0
    
    def get_process_cpu(self, process_name):
        """Get process CPU usage"""
        try:
            result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
            if result.returncode == 0:
                pid = result.stdout.strip().split()[0]
                process = psutil.Process(int(pid))
                return process.cpu_percent()
        except:
            pass
        return 0.0
    
    def check_ml_models(self):
        """Check ML model status"""
        models = {
            'light_model': os.path.exists('models/../models/light_heavy_model.pkl'),
        }
        return models
    
    def get_heartbeat_status(self):
        try:
            with open('logs/health/heartbeat.log', 'r') as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip()
        except:
            pass
        return "No heartbeat data"
    
    def load_config(self):
        """Load system configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {"mode": "unknown"}
    
    def get_recent_logs(self, log_file, lines=50):
        """Get recent log entries"""
        try:
            result = subprocess.run(['tail', f'-{lines}', log_file], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.split('\n')
        except:
            pass
        return []
    
    def rick_chat_response(self, user_message):
        """Rick AI chat response"""
        responses = [
            f"🧠 Rick here! I see you're asking about: {user_message}",
            "📊 System status looks solid, boss. ML engines are humming.",
            "⏰ Current session: Market looking active today.",
            "🔥 Bot performance is within normal parameters.",
            "💡 Suggestion: Check the ML decision logs for insights.",
            "🚀 All systems green - ready for whatever you need!",
            "📈 The models are learning well from the recent data."
        ]
        
        import random
        response = random.choice(responses)
        
        self.chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'rick': response
        })
        
        return response

# Global dashboard instance
dashboard = RickDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(dashboard.get_system_status())

@app.route('/api/logs/<bot_name>')
def api_logs(bot_name):
    """API endpoint for bot logs"""
    log_files = {
        'heartbeat': 'logs/health/heartbeat.log'
    }
    
    log_file = log_files.get(bot_name, 'logs/system.log')
    logs = dashboard.get_recent_logs(log_file)
    
    return jsonify({'logs': logs})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Rick chat API"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not dashboard.authorized:
        return jsonify({'error': 'PIN required'})
    
    rick_response = dashboard.rick_chat_response(user_message)
    
    return jsonify({
        'user': user_message,
        'rick': rick_response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/auth', methods=['POST'])
def api_auth():
    """PIN authentication"""
    data = request.get_json()
    pin = data.get('pin', '')
    
    if pin == dashboard.pin_code:
        dashboard.authorized = True
        return jsonify({'success': True, 'message': '✅ Authorized - Welcome to Rick Dashboard'})
    else:
        return jsonify({'success': False, 'message': '❌ Invalid PIN'})

@app.route('/api/control/<action>', methods=['POST'])
def api_control(action):
    """Bot control actions"""
    if not dashboard.authorized:
        return jsonify({'error': 'PIN required'})
    
    try:
        if action == 'restart_ml':
            time.sleep(2)
                           stderr=subprocess.STDOUT)
        
        elif action == 'reset_bailout':
            subprocess.run(['python3', '-c', 'from emergency_bail import reset_bailout; reset_bailout()'])
            return jsonify({'success': True, 'message': '🔓 Bailout reset'})
        
        elif action == 'retrain_models':
            subprocess.run(['python3', 'scripts/train_light_model.py'])
            subprocess.run(['python3', 'scripts/quick_heavy_model.py'])
            return jsonify({'success': True, 'message': '🧠 Models retrained'})
        
        else:
            return jsonify({'error': 'Unknown action'})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🎛️ Starting Rick Dashboard Server...")
    print("🌐 Access at: http://localhost:5000")
    print(f"📱 PIN Code: {dashboard.pin_code} (from .env file)")
    app.run(host='0.0.0.0', port=5000, debug=False)
