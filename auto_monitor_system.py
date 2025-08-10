#!/usr/bin/env python3
"""
🔥 AUTO-MONITOR SYSTEM - RBOTzilla Elite 18+18
Constitutional PIN: 841921
Auto-opening terminals, dashboard toggles, default LIVE/CONNECTED
"""

import os
import subprocess
import time
import json
import threading
from datetime import datetime
import signal
import sys

class AutoMonitorSystem:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.monitor_config = {
            "health_monitor": {"enabled": True, "auto_open": True},
            "trading_feed": {"enabled": True, "auto_open": True},
            "dashboard_feed": {"enabled": True, "auto_open": True},
            "system_logs": {"enabled": True, "auto_open": True},
            "profit_tracker": {"enabled": True, "auto_open": True},
            "error_monitor": {"enabled": True, "auto_open": True}
        }
        self.terminals = {}
        self.running = True
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Save initial config
        self.save_config()
        
        print(f"🔥 AUTO-MONITOR SYSTEM INITIALIZED - PIN {self.constitutional_pin}")
        print("🟢 DEFAULT STATUS: OPEN, CONNECTED, LIVE")
    
    def save_config(self):
        """Save monitor configuration"""
        with open("monitor_config.json", "w") as f:
            json.dump(self.monitor_config, f, indent=2)
    
    def load_config(self):
        """Load monitor configuration"""
        try:
            with open("monitor_config.json", "r") as f:
                self.monitor_config = json.load(f)
        except:
            pass  # Use defaults
    
    def open_terminal(self, title, command):
        """Open new terminal with command"""
        try:
            # For GNOME Terminal
            cmd = f'gnome-terminal --title="{title}" --tab -- bash -c "{command}; exec bash"'
            process = subprocess.Popen(cmd, shell=True)
            self.terminals[title] = process
            print(f"✅ Opened terminal: {title}")
            return process
        except Exception as e:
            # Fallback to xterm
            try:
                cmd = f'xterm -title "{title}" -e "{command}" &'
                process = subprocess.Popen(cmd, shell=True)
                self.terminals[title] = process
                print(f"✅ Opened xterm: {title}")
                return process
            except Exception as e2:
                print(f"⚠️ Failed to open terminal for {title}: {e2}")
                return None
    
    def monitor_health_feed(self):
        """Monitor system health with auto-opening terminal"""
        if not self.monitor_config["health_monitor"]["enabled"]:
            return
            
        while self.running:
            try:
                # Check if health log exists and has new content
                health_log = "logs/ping_output.log"
                if os.path.exists(health_log):
                    # Get file size
                    current_size = os.path.getsize(health_log)
                    
                    # If file has content and auto-open enabled
                    if current_size > 0 and self.monitor_config["health_monitor"]["auto_open"]:
                        if "Health Monitor" not in self.terminals:
                            self.open_terminal("Health Monitor", f"tail -f {health_log}")
                
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Health monitor error: {e}")
                time.sleep(10)
    
    def monitor_trading_feed(self):
        """Monitor trading activity with auto-opening terminal"""
        if not self.monitor_config["trading_feed"]["enabled"]:
            return
            
        while self.running:
            try:
                # Check for trading logs
                for log_file in ["logs/trading.log", "logs/main_output.log", "oanda_trading.log"]:
                    if os.path.exists(log_file):
                        current_size = os.path.getsize(log_file)
                        
                        if current_size > 0 and self.monitor_config["trading_feed"]["auto_open"]:
                            if "Trading Feed" not in self.terminals:
                                self.open_terminal("Trading Feed", f"tail -f {log_file}")
                                break
                
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Trading feed error: {e}")
                time.sleep(10)
    
    def monitor_dashboard_feed(self):
        """Monitor dashboard activity with auto-opening terminal"""
        if not self.monitor_config["dashboard_feed"]["enabled"]:
            return
            
        while self.running:
            try:
                dashboard_log = "logs/dashboard_stdout.log"
                if os.path.exists(dashboard_log):
                    current_size = os.path.getsize(dashboard_log)
                    
                    if current_size > 0 and self.monitor_config["dashboard_feed"]["auto_open"]:
                        if "Dashboard Feed" not in self.terminals:
                            self.open_terminal("Dashboard Feed", f"tail -f {dashboard_log}")
                
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Dashboard feed error: {e}")
                time.sleep(10)
    
    def monitor_system_logs(self):
        """Monitor system logs with auto-opening terminal"""
        if not self.monitor_config["system_logs"]["enabled"]:
            return
            
        while self.running:
            try:
                # Look for any log files with recent activity
                log_files = []
                if os.path.exists("logs"):
                    for file in os.listdir("logs"):
                        if file.endswith(".log"):
                            log_path = f"logs/{file}"
                            if os.path.getsize(log_path) > 0:
                                log_files.append(log_path)
                
                if log_files and self.monitor_config["system_logs"]["auto_open"]:
                    if "System Logs" not in self.terminals:
                        # Monitor all log files
                        cmd = f"tail -f {' '.join(log_files)}"
                        self.open_terminal("System Logs", cmd)
                
                time.sleep(10)
            except Exception as e:
                print(f"⚠️ System logs error: {e}")
                time.sleep(15)
    
    def monitor_profit_tracker(self):
        """Monitor profit/PnL with auto-opening terminal"""
        if not self.monitor_config["profit_tracker"]["enabled"]:
            return
            
        while self.running:
            try:
                # Look for profit-related logs
                profit_files = ["logs/profit.log", "logs/pnl.log", "logs/performance.log"]
                
                for pfile in profit_files:
                    if os.path.exists(pfile) and os.path.getsize(pfile) > 0:
                        if self.monitor_config["profit_tracker"]["auto_open"]:
                            if "Profit Tracker" not in self.terminals:
                                self.open_terminal("Profit Tracker", f"tail -f {pfile}")
                                break
                
                time.sleep(8)
            except Exception as e:
                print(f"⚠️ Profit tracker error: {e}")
                time.sleep(15)
    
    def monitor_errors(self):
        """Monitor errors with auto-opening terminal"""
        if not self.monitor_config["error_monitor"]["enabled"]:
            return
            
        while self.running:
            try:
                # Look for error logs
                error_files = ["logs/error.log", "logs/exceptions.log"]
                
                for efile in error_files:
                    if os.path.exists(efile) and os.path.getsize(efile) > 0:
                        if self.monitor_config["error_monitor"]["auto_open"]:
                            if "Error Monitor" not in self.terminals:
                                self.open_terminal("Error Monitor", f"tail -f {efile}")
                                break
                
                time.sleep(12)
            except Exception as e:
                print(f"⚠️ Error monitor error: {e}")
                time.sleep(15)
    
    def toggle_monitor(self, monitor_name, enabled=None, auto_open=None):
        """Toggle monitor on/off and auto-open"""
        if monitor_name in self.monitor_config:
            if enabled is not None:
                self.monitor_config[monitor_name]["enabled"] = enabled
            if auto_open is not None:
                self.monitor_config[monitor_name]["auto_open"] = auto_open
            
            self.save_config()
            status = "ENABLED" if self.monitor_config[monitor_name]["enabled"] else "DISABLED"
            auto_status = "AUTO-OPEN" if self.monitor_config[monitor_name]["auto_open"] else "MANUAL"
            print(f"🔄 {monitor_name}: {status} | {auto_status}")
    
    def status_report(self):
        """Print current status"""
        print(f"\n🔥 AUTO-MONITOR SYSTEM STATUS - PIN {self.constitutional_pin}")
        print("=" * 60)
        
        for monitor, config in self.monitor_config.items():
            enabled_icon = "🟢" if config["enabled"] else "🔴"
            auto_icon = "🚀" if config["auto_open"] else "📋"
            print(f"{enabled_icon} {auto_icon} {monitor.replace('_', ' ').title()}")
        
        print(f"\n📊 Active Terminals: {len(self.terminals)}")
        for term_name in self.terminals:
            print(f"   🖥️  {term_name}")
        
        print(f"\n⏰ Status Time: {datetime.now().strftime('%H:%M:%S')}")
    
    def start_monitoring(self):
        """Start all monitoring threads"""
        print("🚀 STARTING AUTO-MONITOR SYSTEM...")
        
        # Start monitoring threads
        threads = []
        
        monitors = [
            ("Health Monitor", self.monitor_health_feed),
            ("Trading Feed", self.monitor_trading_feed),
            ("Dashboard Feed", self.monitor_dashboard_feed),
            ("System Logs", self.monitor_system_logs),
            ("Profit Tracker", self.monitor_profit_tracker),
            ("Error Monitor", self.monitor_errors)
        ]
        
        for name, func in monitors:
            thread = threading.Thread(target=func, name=name, daemon=True)
            thread.start()
            threads.append(thread)
            print(f"✅ Started: {name}")
        
        print("\n🔥 AUTO-MONITOR SYSTEM: FULLY ACTIVE")
        print("🟢 DEFAULT STATUS: OPEN, CONNECTED, LIVE")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(30)
                self.status_report()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Auto-Monitor System...")
            self.running = False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        sys.exit(0)

def main():
    system = AutoMonitorSystem()
    
    # Handle shutdown signals
    signal.signal(signal.SIGINT, system.signal_handler)
    signal.signal(signal.SIGTERM, system.signal_handler)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            system.status_report()
            return
        elif sys.argv[1] == "toggle":
            if len(sys.argv) > 3:
                monitor_name = sys.argv[2]
                action = sys.argv[3].lower()
                if action == "on":
                    system.toggle_monitor(monitor_name, enabled=True)
                elif action == "off":
                    system.toggle_monitor(monitor_name, enabled=False)
                elif action == "auto-on":
                    system.toggle_monitor(monitor_name, auto_open=True)
                elif action == "auto-off":
                    system.toggle_monitor(monitor_name, auto_open=False)
            return
    
    # Start the monitoring system
    system.start_monitoring()

if __name__ == "__main__":
    main()
