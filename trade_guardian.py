#!/usr/bin/env python3
"""
🛡️ TRADE GUARDIAN WATCHDOG
Enforces OCO compliance, monitors loss thresholds, heartbeats to dashboard
Ensures no naked positions exist - every trade MUST have OCO protection
"""

import time
import threading
from datetime import datetime, timedelta
from logger import log_trade, log_error

class TradeGuardian:
    def __init__(self, oco_executor, dashboard_feeder):
        self.oco_executor = oco_executor
        self.dashboard_feeder = dashboard_feeder
        self.running = False
        self.monitor_thread = None
        self.last_heartbeat = datetime.utcnow()
        
        # Tracking for violations
        self.violation_count = 0
        self.max_violations = 5  # Max violations before emergency stop
        
    def start_monitoring(self):
        """Start the guardian watchdog in background thread"""
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._guardian_loop, daemon=True)
        self.monitor_thread.start()
        log_trade("🛡️ Trade Guardian watchdog started - OCO enforcement active", "GUARDIAN")
    
    def _guardian_loop(self):
        """Main guardian monitoring loop"""
        check_count = 0
        
        while self.running:
            try:
                check_count += 1
                
                # Perform comprehensive checks
                self._enforce_oco_compliance()
                self._monitor_position_health()
                self._check_system_health()
                
                # Send heartbeat every 4 checks (1 minute)
                if check_count % 4 == 0:
                    self._send_heartbeat()
                
                # Log guardian status every 20 checks (5 minutes)
                if check_count % 20 == 0:
                    active_trades = len(self.oco_executor.active_trades)
                    log_trade(f"🛡️ Guardian Status: {active_trades} active trades, {self.violation_count} violations", "GUARDIAN_STATUS")
                
                time.sleep(15)  # Check every 15 seconds
                
            except Exception as e:
                log_error(f"Guardian monitoring error: {str(e)}", "GUARDIAN_ERROR")
                time.sleep(30)  # Longer pause on error
    
    def _enforce_oco_compliance(self):
        """
        🚨 ENFORCE MANDATORY OCO COMPLIANCE
        Check that every active trade has proper OCO protection
        """
        try:
            violations = []
            
            for order_id, trade_data in self.oco_executor.active_trades.items():
                symbol = trade_data.get("symbol", "unknown")
                platform = trade_data.get("platform", "unknown")
                
                # Check for missing OCO components
                missing_components = []
                
                if platform == "coinbase":
                    if not trade_data.get("sl_order_id"):
                        missing_components.append("SL")
                    if not trade_data.get("tp_order_id") and not trade_data.get("wave_riding", False):
                        missing_components.append("TP")
                        
                elif platform == "oanda":
                    if not trade_data.get("trade_id"):
                        missing_components.append("Trade ID")
                    # For OANDA, OCO is built into the trade, but we can verify it exists
                    
                if missing_components:
                    violation = {
                        "order_id": order_id,
                        "symbol": symbol,
                        "platform": platform,
                        "missing": missing_components,
                        "timestamp": datetime.utcnow()
                    }
                    violations.append(violation)
            
            # Handle violations
            if violations:
                self._handle_oco_violations(violations)
                
        except Exception as e:
            log_error(f"OCO compliance check failed: {str(e)}", "OCO_COMPLIANCE")
    
    def _handle_oco_violations(self, violations):
        """Handle detected OCO violations"""
        for violation in violations:
            self.violation_count += 1
            
            log_error(f"🚨 OCO VIOLATION #{self.violation_count}: {violation['symbol']} missing {violation['missing']}", "OCO_VIOLATION")
            
            # Attempt to fix the violation
            try:
                order_id = violation["order_id"]
                if order_id in self.oco_executor.active_trades:
                    # Force close the violating trade
                    self._emergency_close_trade(order_id, violation)
                    
            except Exception as e:
                log_error(f"Failed to close violating trade {violation['symbol']}: {str(e)}", "VIOLATION_FIX")
        
        # Emergency stop if too many violations
        if self.violation_count >= self.max_violations:
            log_error(f"🚨 CRITICAL: {self.violation_count} OCO violations - EMERGENCY SHUTDOWN", "CRITICAL_VIOLATIONS")
            self._trigger_emergency_shutdown()
    
    def _emergency_close_trade(self, order_id, violation):
        """Emergency close a trade that violates OCO compliance"""
        try:
            trade_data = self.oco_executor.active_trades[order_id]
            symbol = trade_data["symbol"]
            platform = trade_data["platform"]
            side = "sell" if trade_data["side"] == "buy" else "buy"
            size = trade_data["size"]
            
            log_trade(f"🚨 EMERGENCY CLOSING: {symbol} due to OCO violation", "EMERGENCY_CLOSE")
            
            if platform == "coinbase":
                # Market close the position
                close_order = self.oco_executor.coinbase.create_market_order(
                    symbol=symbol,
                    side=side,
                    amount=size
                )
                log_trade(f"🚨 Coinbase position closed: {symbol} Order: {close_order.get('id', 'unknown')}", "EMERGENCY_CLOSE")
                
            elif platform == "oanda":
                # Close OANDA trade
                trade_id = trade_data.get("trade_id")
                if trade_id:
                    close_response = self.oco_executor.oanda.trade.close(
                        accountID=self.oco_executor.creds.OANDA_ACCOUNT_ID,
                        tradeID=trade_id
                    )
                    log_trade(f"🚨 OANDA position closed: {symbol} Trade: {trade_id}", "EMERGENCY_CLOSE")
            
            # Remove from active trades
            if order_id in self.oco_executor.active_trades:
                del self.oco_executor.active_trades[order_id]
                
            # Update position tracker
            from position_tracker import close_position
            close_position(order_id, trade_data["entry_price"], "OCO_VIOLATION", 0.0)
            
        except Exception as e:
            log_error(f"Emergency close failed for {violation['symbol']}: {str(e)}", "EMERGENCY_CLOSE_FAIL")
    
    def _monitor_position_health(self):
        """Monitor overall position health and risk"""
        try:
            total_positions = len(self.oco_executor.active_trades)
            max_positions = getattr(self.oco_executor.creds, 'MAX_CONCURRENT_TRADES', 3)
            
            if total_positions > max_positions:
                log_error(f"🚨 Position limit exceeded: {total_positions}/{max_positions}", "POSITION_LIMIT")
                self._reduce_position_count()
            
            # Check for stale positions (older than 24 hours)
            current_time = time.time()
            for order_id, trade_data in list(self.oco_executor.active_trades.items()):
                age_hours = (current_time - trade_data.get("timestamp", current_time)) / 3600
                
                if age_hours > 24:
                    log_trade(f"⚠️ Stale position detected: {trade_data['symbol']} ({age_hours:.1f}h old)", "STALE_POSITION")
                    
        except Exception as e:
            log_error(f"Position health check failed: {str(e)}", "HEALTH_CHECK")
    
    def _reduce_position_count(self):
        """Reduce position count by closing oldest positions"""
        try:
            # Sort by timestamp (oldest first)
            sorted_trades = sorted(
                self.oco_executor.active_trades.items(),
                key=lambda x: x[1].get("timestamp", 0)
            )
            
            # Close oldest position
            if sorted_trades:
                order_id, trade_data = sorted_trades[0]
                self._emergency_close_trade(order_id, {"symbol": trade_data["symbol"], "reason": "position_limit"})
                
        except Exception as e:
            log_error(f"Position reduction failed: {str(e)}", "POSITION_REDUCE")
    
    def _check_system_health(self):
        """Check overall system health"""
        try:
            # Check memory usage, API connectivity, etc.
            current_time = datetime.utcnow()
            
            # Update last check time
            self.last_heartbeat = current_time
            
            # Log system stats periodically (optional)
            try:
                import psutil
                memory_percent = psutil.virtual_memory().percent
                
                if memory_percent > 90:
                    log_error(f"🚨 High memory usage: {memory_percent:.1f}%", "SYSTEM_HEALTH")
            except ImportError:
                # psutil not available, skip memory check
                pass
                
        except Exception as e:
            # Don't fail on system health checks
            pass
    
    def _send_heartbeat(self):
        """Send heartbeat to dashboard and logs"""
        try:
            timestamp = datetime.utcnow().isoformat()
            active_count = len(self.oco_executor.active_trades)
            
            # Heartbeat message
            heartbeat_msg = f"✅ Guardian OK | Active: {active_count} | Violations: {self.violation_count}"
            
            # Update dashboard if available
            if self.dashboard_feeder:
                self.dashboard_feeder.update_heartbeat(heartbeat_msg)
            
            # Write to heartbeat log
            with open("logs/heartbeat.log", "a") as f:
                f.write(f"[{timestamp}] {heartbeat_msg}\n")
                
            # Periodic detailed log
            log_trade(f"🛡️ {heartbeat_msg}", "HEARTBEAT")
            
        except Exception as e:
            log_error(f"Heartbeat failed: {str(e)}", "HEARTBEAT_FAIL")
    
    def _trigger_emergency_shutdown(self):
        """Trigger emergency system shutdown"""
        try:
            log_error("🚨 EMERGENCY SHUTDOWN TRIGGERED BY GUARDIAN", "EMERGENCY_SHUTDOWN")
            
            # Close all positions
            self.oco_executor.emergency_close_all()
            
            # Stop monitoring
            self.running = False
            
            # Send emergency notification
            if self.dashboard_feeder:
                self.dashboard_feeder.update_system_status("emergency", "🚨 EMERGENCY SHUTDOWN", 0)
            
            # Write emergency flag
            with open("logs/emergency_shutdown.flag", "w") as f:
                f.write(f"Emergency shutdown at {datetime.utcnow().isoformat()}\n")
                f.write(f"Reason: {self.violation_count} OCO violations\n")
                
        except Exception as e:
            log_error(f"Emergency shutdown failed: {str(e)}", "EMERGENCY_FAIL")
    
    def stop(self):
        """Stop the guardian monitoring"""
        self.running = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=10)
        log_trade("🛑 Trade Guardian stopped", "GUARDIAN_STOP")
    
    def get_guardian_status(self):
        """Get current guardian status"""
        return {
            "running": self.running,
            "violation_count": self.violation_count,
            "last_heartbeat": self.last_heartbeat,
            "active_trades": len(self.oco_executor.active_trades)
        }

# Emergency functions for manual guardian control
def emergency_reset_guardian(guardian):
    """Reset guardian violation count"""
    guardian.violation_count = 0
    log_trade("🔄 Guardian violation count reset", "GUARDIAN_RESET")

def force_oco_check(guardian):
    """Force an immediate OCO compliance check"""
    log_trade("🔍 Forcing OCO compliance check", "FORCE_CHECK")
    guardian._enforce_oco_compliance()

if __name__ == "__main__":
    print("🛡️ Trade Guardian watchdog ready")
    print("✅ Features:")
    print("   - Mandatory OCO enforcement")
    print("   - Position health monitoring") 
    print("   - System health checks")
    print("   - Emergency shutdown protection")
    print("   - Heartbeat monitoring")
