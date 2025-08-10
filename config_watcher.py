#!/usr/bin/env python3
"""
CONFIG WATCHER & AUTO-RESTART MODULE
Monitors configuration changes and triggers intelligent restarts
"""

import os
import sys
import json
import time
import signal
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigWatcher:
    def __init__(self, config_path, main_script_path):
        self.config_path = config_path
        self.main_script_path = main_script_path
        self.last_mtime = os.path.getmtime(config_path) if os.path.exists(config_path) else 0
        
        # Setup logging
        log_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/config_watcher.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("🔍 CONFIG WATCHER INITIALIZED")
    
    def check_config_integrity(self):
        """Validate config file integrity before restart"""
        try:
            with open(self.config_path, 'r') as f:
                json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Invalid JSON in config: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Config check error: {e}")
            return False
    
    def trigger_intelligent_restart(self):
        """Trigger restart only if config is valid"""
        if not self.check_config_integrity():
            self.logger.warning("⚠️ Config invalid - skipping restart")
            return False
        
        self.logger.info("🔄 TRIGGERING INTELLIGENT RESTART")
        
        # Send restart signal to main process
        try:
            # Method 1: Use process file
            restart_flag = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.RESTART_REQUESTED"
            with open(restart_flag, 'w') as f:
                f.write(str(datetime.now().timestamp()))
            
            self.logger.info("✅ Restart signal sent")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Restart trigger error: {e}")
            return False
    
    def watch_loop(self):
        """Main config watching loop"""
        while True:
            try:
                current_mtime = os.path.getmtime(self.config_path)
                
                if current_mtime != self.last_mtime:
                    self.logger.info("📝 CONFIG FILE CHANGED")
                    self.last_mtime = current_mtime
                    
                    # Wait a moment for file to be fully written
                    time.sleep(2)
                    
                    # Trigger restart
                    self.trigger_intelligent_restart()
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Config watcher shutdown")
                break
            except Exception as e:
                self.logger.error(f"❌ Watch loop error: {e}")
                time.sleep(10)

class MultinstrumentStuckTradeKiller:
    """Kill trades that are stuck beyond time limits"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_hold_seconds = 21600  # 6 hours default
        
    def scan_and_kill_stuck_trades(self):
        """Scan all instruments for stuck trades and kill them"""
        try:
            from router_live_hardcoded import OandaRouter
            router = OandaRouter()
            
            # Get all open positions
            positions = router.get_positions()
            current_time = time.time()
            
            for position in positions:
                # Calculate hold time
                open_time = datetime.fromisoformat(position.get('time', ''))
                hold_time = current_time - open_time.timestamp()
                
                if hold_time > self.max_hold_seconds:
                    instrument = position.get('instrument')
                    units = position.get('units')
                    
                    self.logger.warning(f"⏰ STUCK TRADE DETECTED: {instrument} held for {hold_time/3600:.1f}h")
                    
                    # Force close the position
                    success = router.close_position(instrument)
                    
                    if success:
                        self.logger.info(f"✅ Stuck trade killed: {instrument}")
                    else:
                        self.logger.error(f"❌ Failed to kill stuck trade: {instrument}")
        
        except Exception as e:
            self.logger.error(f"❌ Stuck trade killer error: {e}")

def auto_disable_after_drawdown():
    """Auto-disable bot after significant drawdown"""
    try:
        # Read daily P/L from logs
        daily_loss = get_daily_loss()  # You'd implement this
        
        DRAWDOWN_LIMIT = 200  # $200 loss limit
        
        if daily_loss >= DRAWDOWN_LIMIT:
            logging.info(f"⚠️ DRAWDOWN LIMIT HIT: ${daily_loss}")
            
            # Create lock file
            lock_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.BOT_LOCK"
            with open(lock_file, 'w') as f:
                f.write(f"Auto-disabled due to ${daily_loss} drawdown at {datetime.now()}")
            
            logging.critical("🔒 BOT AUTO-DISABLED DUE TO DRAWDOWN")
            return True
    
    except Exception as e:
        logging.error(f"❌ Drawdown check error: {e}")
    
    return False

def get_daily_loss():
    """Calculate daily loss from logs"""
    # This would parse your trading logs
    # Placeholder implementation
    return 0

if __name__ == "__main__":
    config_path = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/autonomous_config.json"
    main_script = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/main.py"
    
    watcher = ConfigWatcher(config_path, main_script)
    
    # Also start stuck trade killer in background
    stuck_killer = MultinstrumentStuckTradeKiller()
    
    import threading
    
    def background_stuck_killer():
        while True:
            stuck_killer.scan_and_kill_stuck_trades()
            time.sleep(300)  # Check every 5 minutes
    
    # Start background thread
    killer_thread = threading.Thread(target=background_stuck_killer, daemon=True)
    killer_thread.start()
    
    # Start config watcher
    watcher.watch_loop()
