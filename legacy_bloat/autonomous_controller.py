#!/usr/bin/env python3
"""
FULLY AUTONOMOUS OANDA BOT SYSTEM
Self-launching. Self-correcting. Self-scaling.
Built for small capital → scalable profit.

Integrates with existing main.py while adding full autonomy features.
"""

import os
import sys
import json
import time
import signal
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AutonomousController:
    def __init__(self, main_script_path="/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/main.py"):
        self.main_script = main_script_path
        self.config_path = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/autonomous_config.json"
        self.lock_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.BOT_LOCK"
        self.log_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/autonomous.log"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.bot_process = None
        self.config = self.load_config()
        self.is_running = True
        self.daily_profit = 0
        self.daily_loss = 0
        self.trade_count_today = 0
        self.start_time = datetime.now()
        
        # Performance tracking
        self.strategy_performance = {}
        self.last_config_mtime = os.path.getmtime(self.config_path) if os.path.exists(self.config_path) else 0
        
        self.logger.info("🤖 AUTONOMOUS CONTROLLER INITIALIZED")
    
    def load_config(self):
        """Load autonomous configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Config load error: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration if file is missing"""
        return {
            "AUTONOMOUS_CONTROL": {
                "bot_enabled": True,
                "auto_restart_on_config_change": True,
                "daily_restart_time": "07:00",
                "max_daily_loss": 200,
                "max_daily_trades": 50,
                "emergency_stop_on_drawdown": 0.15
            },
            "PROFIT_SCALING": {
                "target_daily_profit": 400,
                "confidence_scaling_threshold": 0.85,
                "position_amplifier_max": 3.0
            }
        }
    
    def check_emergency_conditions(self):
        """Check for emergency stop conditions"""
        config = self.config["AUTONOMOUS_CONTROL"]
        
        # Check daily loss limit
        if self.daily_loss >= config["max_daily_loss"]:
            self.logger.warning(f"⚠️ DAILY LOSS LIMIT HIT: ${self.daily_loss}")
            self.emergency_stop("Daily loss limit exceeded")
            return True
        
        # Check trade count limit
        if self.trade_count_today >= config["max_daily_trades"]:
            self.logger.warning(f"⚠️ DAILY TRADE LIMIT HIT: {self.trade_count_today}")
            self.emergency_stop("Daily trade limit exceeded")
            return True
        
        # Check lock file
        if os.path.exists(self.lock_file):
            self.logger.warning("⛔ BOT_LOCK file detected")
            self.emergency_stop("Manual lock file present")
            return True
        
        # Check bot_enabled flag
        if not config.get("bot_enabled", True):
            self.logger.warning("🛑 Bot disabled in config")
            self.emergency_stop("Bot disabled in configuration")
            return True
        
        return False
    
    def emergency_stop(self, reason):
        """Emergency stop with logging"""
        self.logger.critical(f"🚨 EMERGENCY STOP: {reason}")
        
        if self.bot_process and self.bot_process.poll() is None:
            self.bot_process.terminate()
            time.sleep(5)
            if self.bot_process.poll() is None:
                self.bot_process.kill()
        
        # Create emergency log
        emergency_log = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "daily_profit": self.daily_profit,
            "daily_loss": self.daily_loss,
            "trade_count": self.trade_count_today
        }
        
        with open("/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/emergency_stops.json", "a") as f:
            f.write(json.dumps(emergency_log) + "\n")
        
        # Sleep for cooldown period
        cooldown = 3600  # 1 hour
        self.logger.info(f"😴 Emergency cooldown: {cooldown} seconds")
        time.sleep(cooldown)
    
    def check_config_changes(self):
        """Check for configuration file changes"""
        try:
            current_mtime = os.path.getmtime(self.config_path)
            if current_mtime != self.last_config_mtime:
                self.logger.info("🔁 CONFIG CHANGED - Restarting bot...")
                self.last_config_mtime = current_mtime
                self.config = self.load_config()
                self.restart_bot()
                return True
        except Exception as e:
            self.logger.error(f"Config check error: {e}")
        return False
    
    def check_daily_restart(self):
        """Check if it's time for daily restart"""
        restart_time = self.config["AUTONOMOUS_CONTROL"].get("daily_restart_time", "07:00")
        try:
            restart_hour, restart_minute = map(int, restart_time.split(":"))
            now = datetime.now()
            restart_today = now.replace(hour=restart_hour, minute=restart_minute, second=0, microsecond=0)
            
            # If restart time has passed today and we haven't restarted yet
            if now >= restart_today and (now - self.start_time).total_seconds() > 3600:
                if now.hour == restart_hour and now.minute == restart_minute:
                    self.logger.info("🌅 DAILY RESTART TIME")
                    self.daily_restart()
                    return True
        except Exception as e:
            self.logger.error(f"Daily restart check error: {e}")
        return False
    
    def daily_restart(self):
        """Perform daily restart with fresh slate"""
        self.logger.info("🔄 PERFORMING DAILY RESTART")
        
        # Reset daily counters
        self.daily_profit = 0
        self.daily_loss = 0
        self.trade_count_today = 0
        self.start_time = datetime.now()
        
        # Clear strategy performance
        self.strategy_performance = {}
        
        # Restart bot
        self.restart_bot()
        
        self.logger.info("✅ DAILY RESTART COMPLETE")
    
    def restart_bot(self):
        """Restart the trading bot"""
        try:
            # Stop current bot
            if self.bot_process and self.bot_process.poll() is None:
                self.logger.info("🛑 Stopping current bot...")
                self.bot_process.terminate()
                time.sleep(10)
                if self.bot_process.poll() is None:
                    self.bot_process.kill()
            
            # Start new bot process
            self.logger.info("🚀 Starting fresh bot instance...")
            self.bot_process = subprocess.Popen([
                sys.executable, self.main_script
            ], cwd=os.path.dirname(self.main_script))
            
            self.logger.info(f"✅ Bot restarted with PID: {self.bot_process.pid}")
            
        except Exception as e:
            self.logger.error(f"Bot restart error: {e}")
    
    def monitor_bot_health(self):
        """Monitor bot process health"""
        if self.bot_process is None:
            self.logger.warning("⚠️ No bot process found - starting...")
            self.restart_bot()
            return
        
        # Check if process is still alive
        if self.bot_process.poll() is not None:
            exit_code = self.bot_process.returncode
            self.logger.warning(f"⚠️ Bot process died with exit code: {exit_code}")
            
            # Check if it was an intentional shutdown
            if exit_code == 0:
                self.logger.info("Bot shutdown cleanly")
            else:
                self.logger.error("Bot crashed - restarting...")
                time.sleep(30)  # Wait before restart
                self.restart_bot()
    
    def update_performance_metrics(self):
        """Update strategy performance metrics"""
        try:
            # Read trading logs to update performance
            log_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/smart.log"
            if os.path.exists(log_file):
                # Parse recent trades and update metrics
                # This would integrate with your existing logging
                pass
        except Exception as e:
            self.logger.error(f"Performance update error: {e}")
    
    def check_profit_targets(self):
        """Check if daily profit targets are met"""
        target = self.config["PROFIT_SCALING"]["target_daily_profit"]
        
        if self.daily_profit >= target:
            self.logger.info(f"🎯 DAILY TARGET ACHIEVED: ${self.daily_profit}")
            
            # Optional: Reduce risk or pause trading
            reduced_risk_mode = True
            return True
        
        return False
    
    def autonomous_loop(self):
        """Main autonomous control loop"""
        self.logger.info("🚀 STARTING AUTONOMOUS CONTROL LOOP")
        
        # Start initial bot
        self.restart_bot()
        
        while self.is_running:
            try:
                # Emergency condition checks
                if self.check_emergency_conditions():
                    continue
                
                # Configuration change detection
                if self.check_config_changes():
                    continue
                
                # Daily restart check
                if self.check_daily_restart():
                    continue
                
                # Bot health monitoring
                self.monitor_bot_health()
                
                # Performance tracking
                self.update_performance_metrics()
                
                # Profit target checking
                self.check_profit_targets()
                
                # Status report
                if int(time.time()) % 300 == 0:  # Every 5 minutes
                    self.logger.info(f"📊 STATUS: Profit ${self.daily_profit:.2f} | Loss ${self.daily_loss:.2f} | Trades {self.trade_count_today}")
                
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                self.logger.info("🛑 SHUTDOWN REQUESTED")
                self.is_running = False
                break
            except Exception as e:
                self.logger.error(f"Autonomous loop error: {e}")
                time.sleep(60)
    
    def shutdown(self):
        """Clean shutdown"""
        self.logger.info("🏁 AUTONOMOUS CONTROLLER SHUTDOWN")
        self.is_running = False
        
        if self.bot_process and self.bot_process.poll() is None:
            self.bot_process.terminate()
            time.sleep(10)
            if self.bot_process.poll() is None:
                self.bot_process.kill()

class ConfigWatcher(FileSystemEventHandler):
    """Watch for config file changes"""
    def __init__(self, controller):
        self.controller = controller
    
    def on_modified(self, event):
        if event.src_path.endswith('autonomous_config.json'):
            self.controller.logger.info("🔄 Config file changed")
            self.controller.check_config_changes()

def signal_handler(sig, frame, controller):
    """Handle shutdown signals"""
    controller.logger.info(f"Received signal {sig}")
    controller.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    controller = AutonomousController()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, controller))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, controller))
    
    try:
        controller.autonomous_loop()
    except Exception as e:
        controller.logger.critical(f"💥 AUTONOMOUS CONTROLLER CRASHED: {e}")
    finally:
        controller.shutdown()
