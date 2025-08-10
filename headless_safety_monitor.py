#!/usr/bin/env python3
# 🤖 HEADLESS BOT SAFETY MONITOR - Automated Integrity Surveillance
# Runs continuously in background to monitor bot safety

import time
import json
import os
import sys
from datetime import datetime, timedelta
from ai_integrity_check import BotIntegrityChecker

class HeadlessSafetyMonitor:
    def __init__(self, check_interval=300):  # 5 minutes default
        self.check_interval = check_interval
        self.running = True
        self.last_status = "UNKNOWN"
        self.alert_history = []
        
    def log_event(self, level, message):
        """Log monitoring events"""
        timestamp = datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.alert_history.append(event)
        
        # Keep only last 100 events
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]
            
        print(f"[{timestamp}] [{level}] {message}")
        
    def should_emergency_lock(self, checker):
        """Determine if emergency lock should be engaged"""
        critical_failures = 0
        
        # Check for critical issues
        for alert in checker.alerts:
            if alert["level"] == "CRITICAL":
                critical_failures += 1
                
        # Emergency lock conditions
        if critical_failures >= 2:
            return True
            
        # Check for unauthorized trading activity
        for alert in checker.alerts:
            if "live orders detected" in alert["message"].lower():
                return True
                
        return False
        
    def emergency_lock_bot(self):
        """Engage emergency bot lock"""
        try:
            # Create BOT_LOCK file
            with open(".BOT_LOCK", "w") as f:
                f.write(f"EMERGENCY_LOCK_{datetime.now().isoformat()}\n")
                f.write("Automatic safety lock due to integrity violations\n")
                
            self.log_event("CRITICAL", "🚨 EMERGENCY BOT LOCK ENGAGED")
            
            # Try to stop systemd service
            os.system("systemctl --user stop horsemen-oanda.service 2>/dev/null")
            
            # Try to kill running processes
            os.system("pkill -f 'python3 main.py' 2>/dev/null")
            
            self.log_event("INFO", "🛑 Bot processes terminated")
            
        except Exception as e:
            self.log_event("ERROR", f"❌ Emergency lock failed: {e}")
            
    def run_safety_check(self):
        """Run integrity check and handle results"""
        self.log_event("INFO", "🔍 Starting automated safety check...")
        
        try:
            checker = BotIntegrityChecker()
            is_secure = checker.run_full_check()
            
            self.last_status = checker.status
            
            # Handle results
            if checker.status == "CRITICAL":
                self.log_event("CRITICAL", f"🚨 CRITICAL SECURITY ISSUES DETECTED: {checker.checks_failed} failures")
                
                if self.should_emergency_lock(checker):
                    self.emergency_lock_bot()
                    
            elif checker.status == "WARNING":
                self.log_event("WARNING", f"⚠️ Security warnings detected: {checker.checks_failed} issues")
                
            else:
                self.log_event("INFO", f"✅ Bot security verified: {checker.checks_passed} checks passed")
                
            # Save monitoring log
            monitor_log = {
                "timestamp": datetime.now().isoformat(),
                "status": checker.status,
                "checks_passed": checker.checks_passed,
                "checks_failed": checker.checks_failed,
                "alerts": checker.alerts[-10:]  # Last 10 alerts
            }
            
            with open("safety_monitor.log", "a") as f:
                f.write(json.dumps(monitor_log) + "\n")
                
        except Exception as e:
            self.log_event("ERROR", f"❌ Safety check failed: {e}")
            
    def cleanup_old_logs(self):
        """Clean up old monitoring logs"""
        try:
            # Remove logs older than 7 days
            cutoff = datetime.now() - timedelta(days=7)
            
            for filename in os.listdir("."):
                if filename.startswith("integrity_report_") and filename.endswith(".json"):
                    file_time = os.path.getmtime(filename)
                    if datetime.fromtimestamp(file_time) < cutoff:
                        os.remove(filename)
                        
        except Exception as e:
            self.log_event("ERROR", f"Log cleanup failed: {e}")
            
    def run_monitor(self):
        """Main monitoring loop"""
        self.log_event("INFO", f"🤖 Starting headless safety monitor (interval: {self.check_interval}s)")
        
        try:
            while self.running:
                # Run safety check
                self.run_safety_check()
                
                # Cleanup old logs (once per day)
                if datetime.now().hour == 0 and datetime.now().minute < 10:
                    self.cleanup_old_logs()
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log_event("INFO", "🛑 Monitor shutdown requested")
            
        except Exception as e:
            self.log_event("ERROR", f"❌ Monitor crashed: {e}")
            
        finally:
            self.log_event("INFO", "🏁 Safety monitor stopped")

if __name__ == "__main__":
    # Command line arguments
    interval = 300  # 5 minutes default
    
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 headless_safety_monitor.py [interval_seconds]")
            sys.exit(1)
    
    monitor = HeadlessSafetyMonitor(check_interval=interval)
    monitor.run_monitor()
