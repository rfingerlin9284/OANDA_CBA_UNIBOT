#!/usr/bin/env python3
"""
📊 WOLFPACK-LITE POSITION TRACKER
Persistent position file management and trade monitoring
LIVE TRADING ONLY - Real money position tracking
"""

import os
import json
import time
from datetime import datetime
from threading import Lock
from logger import log_trade, log_error, log_pnl

class PositionTracker:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.positions_file = os.path.join(data_dir, "active_positions.json")
        self.trades_history_file = os.path.join(data_dir, "trades_history.json")
        self.lock = Lock()
        
        # Create data directory
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize position files
        self.positions = self.load_positions()
        self.trades_history = self.load_trades_history()
        
        log_trade("📊 Position Tracker initialized", "TRACKER")
    
    def load_positions(self):
        """Load active positions from file"""
        try:
            if os.path.exists(self.positions_file):
                with open(self.positions_file, 'r') as f:
                    positions = json.load(f)
                    log_trade(f"📂 Loaded {len(positions)} active positions", "TRACKER")
                    return positions
        except Exception as e:
            log_error(f"Failed to load positions: {e}", "TRACKER")
        
        # Return empty dict if file doesn't exist or is corrupted
        return {}
    
    def load_trades_history(self):
        """Load trade history from file"""
        try:
            if os.path.exists(self.trades_history_file):
                with open(self.trades_history_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            log_error(f"Failed to load trade history: {e}", "TRACKER")
        
        return []
    
    def save_positions(self):
        """Save active positions to file"""
        try:
            with self.lock:
                with open(self.positions_file, 'w') as f:
                    json.dump(self.positions, f, indent=2)
                return True
        except Exception as e:
            log_error(f"Failed to save positions: {e}", "TRACKER")
            return False
    
    def save_trades_history(self):
        """Save trade history to file"""
        try:
            with self.lock:
                with open(self.trades_history_file, 'w') as f:
                    json.dump(self.trades_history, f, indent=2)
                return True
        except Exception as e:
            log_error(f"Failed to save trade history: {e}", "TRACKER")
            return False
    
    def add_position(self, order_id, symbol, side, size, entry_price, sl_price, tp_price, platform, trade_data=None):
        """
        ✅ ADD NEW POSITION
        Create position file entry for live tracking
        """
        position_data = {
            "order_id": order_id,
            "symbol": symbol,
            "side": side,
            "size": size,
            "entry_price": entry_price,
            "sl_price": sl_price,
            "tp_price": tp_price,
            "platform": platform,
            "status": "OPEN",
            "entry_time": datetime.utcnow().isoformat(),
            "last_update": datetime.utcnow().isoformat(),
            "unrealized_pnl": 0.0,
            "current_price": entry_price,
            "trade_data": trade_data or {}
        }
        
        with self.lock:
            self.positions[order_id] = position_data
            self.save_positions()
        
        log_trade(f"✅ POSITION ADDED: {symbol} {side.upper()} | Size: {size} | Entry: {entry_price}", "TRACKER")
        return True
    
    def update_position_price(self, order_id, current_price):
        """Update position with current market price"""
        if order_id not in self.positions:
            return False
        
        with self.lock:
            position = self.positions[order_id]
            position["current_price"] = current_price
            position["last_update"] = datetime.utcnow().isoformat()
            
            # Calculate unrealized P&L
            if position["side"].lower() == "buy":
                pnl = (current_price - position["entry_price"]) * position["size"]
            else:
                pnl = (position["entry_price"] - current_price) * position["size"]
            
            position["unrealized_pnl"] = pnl
            self.save_positions()
        
        return True
    
    def close_position(self, order_id, exit_price, exit_reason="MANUAL", realized_pnl=None):
        """
        🔒 CLOSE POSITION
        Move from active to history and calculate final P&L
        """
        if order_id not in self.positions:
            log_error(f"Position {order_id} not found for closure", "TRACKER")
            return False
        
        with self.lock:
            position = self.positions[order_id]
            
            # Calculate realized P&L if not provided
            if realized_pnl is None:
                if position["side"].lower() == "buy":
                    realized_pnl = (exit_price - position["entry_price"]) * position["size"]
                else:
                    realized_pnl = (position["entry_price"] - exit_price) * position["size"]
            
            # Create trade history entry
            trade_record = {
                **position,
                "exit_price": exit_price,
                "exit_time": datetime.utcnow().isoformat(),
                "exit_reason": exit_reason,
                "realized_pnl": realized_pnl,
                "status": "CLOSED",
                "duration_minutes": self._calculate_duration(position["entry_time"])
            }
            
            # Add to history
            self.trades_history.append(trade_record)
            self.save_trades_history()
            
            # Remove from active positions
            del self.positions[order_id]
            self.save_positions()
        
        # Log P&L
        log_pnl(
            position["symbol"], 
            position["side"], 
            position["entry_price"], 
            exit_price, 
            realized_pnl,
            self.get_total_balance(),
            self.get_current_streak()
        )
        
        log_trade(f"🔒 POSITION CLOSED: {position['symbol']} | P&L: ${realized_pnl:.2f} | Reason: {exit_reason}", "TRACKER")
        return True
    
    def _calculate_duration(self, entry_time_str):
        """Calculate trade duration in minutes"""
        try:
            entry_time = datetime.fromisoformat(entry_time_str.replace('Z', '+00:00'))
            now = datetime.utcnow().replace(tzinfo=entry_time.tzinfo)
            duration = (now - entry_time).total_seconds() / 60
            return round(duration, 2)
        except:
            return 0.0
    
    def get_active_positions(self):
        """Get all active positions"""
        return dict(self.positions)
    
    def get_position_count(self):
        """Get number of active positions"""
        return len(self.positions)
    
    def get_total_balance(self):
        """Calculate total balance from trade history"""
        starting_balance = 3000.0  # From credentials
        total_pnl = sum(trade.get("realized_pnl", 0) for trade in self.trades_history)
        return starting_balance + total_pnl
    
    def get_current_streak(self):
        """Get current win/loss streak"""
        if not self.trades_history:
            return 0
        
        # Look at recent trades to determine streak
        streak = 0
        last_result = None
        
        for trade in reversed(self.trades_history[-10:]):  # Last 10 trades
            pnl = trade.get("realized_pnl", 0)
            current_result = "win" if pnl > 0 else "loss"
            
            if last_result is None:
                last_result = current_result
                streak = 1
            elif current_result == last_result:
                streak += 1
            else:
                break
        
        return streak if last_result == "win" else -streak
    
    def get_daily_stats(self):
        """Get today's trading statistics"""
        today = datetime.utcnow().date()
        today_trades = [
            trade for trade in self.trades_history
            if trade.get("exit_time") and 
            datetime.fromisoformat(trade["exit_time"].replace('Z', '+00:00')).date() == today
        ]
        
        if not today_trades:
            return {
                "trades_count": 0,
                "total_pnl": 0.0,
                "win_rate": 0.0,
                "avg_pnl": 0.0
            }
        
        total_pnl = sum(trade.get("realized_pnl", 0) for trade in today_trades)
        wins = sum(1 for trade in today_trades if trade.get("realized_pnl", 0) > 0)
        win_rate = (wins / len(today_trades)) * 100
        avg_pnl = total_pnl / len(today_trades)
        
        return {
            "trades_count": len(today_trades),
            "total_pnl": total_pnl,
            "win_rate": win_rate,
            "avg_pnl": avg_pnl
        }
    
    def print_daily_summary(self):
        """Print daily trading summary"""
        stats = self.get_daily_stats()
        active_count = self.get_position_count()
        balance = self.get_total_balance()
        streak = self.get_current_streak()
        
        print("\n" + "="*60)
        print("📊 DAILY TRADING SUMMARY")
        print("="*60)
        print(f"💰 Current Balance: ${balance:.2f}")
        print(f"📈 Today's P&L: ${stats['total_pnl']:.2f}")
        print(f"📊 Today's Trades: {stats['trades_count']}")
        print(f"🎯 Win Rate: {stats['win_rate']:.1f}%")
        print(f"📍 Active Positions: {active_count}")
        
        if streak > 0:
            print(f"🔥 Win Streak: {streak}")
        elif streak < 0:
            print(f"❄️ Loss Streak: {abs(streak)}")
        else:
            print("⚪ No Current Streak")
        
        print("="*60)
    
    def cleanup_old_trades(self, days_to_keep=30):
        """Clean up old trade history (keep last 30 days)"""
        cutoff_date = datetime.utcnow().date()
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days_to_keep)
        
        with self.lock:
            original_count = len(self.trades_history)
            self.trades_history = [
                trade for trade in self.trades_history
                if trade.get("exit_time") and 
                datetime.fromisoformat(trade["exit_time"].replace('Z', '+00:00')).date() >= cutoff_date
            ]
            
            if len(self.trades_history) < original_count:
                self.save_trades_history()
                removed = original_count - len(self.trades_history)
                log_trade(f"🧹 Cleaned up {removed} old trade records", "TRACKER")

# Global position tracker instance
position_tracker = PositionTracker()

# Convenience functions for external use
def add_position(order_id, symbol, side, size, entry_price, sl_price, tp_price, platform, trade_data=None):
    """Add new position to tracking"""
    return position_tracker.add_position(order_id, symbol, side, size, entry_price, sl_price, tp_price, platform, trade_data)

def close_position(order_id, exit_price, exit_reason="MANUAL", realized_pnl=None):
    """Close position and move to history"""
    return position_tracker.close_position(order_id, exit_price, exit_reason, realized_pnl)

def get_active_positions():
    """Get all active positions"""
    return position_tracker.get_active_positions()

def get_position_count():
    """Get number of active positions"""
    return position_tracker.get_position_count()

def print_daily_summary():
    """Print daily trading summary"""
    return position_tracker.print_daily_summary()

if __name__ == "__main__":
    print("📊 Position Tracker - Testing")
    position_tracker.print_daily_summary()
