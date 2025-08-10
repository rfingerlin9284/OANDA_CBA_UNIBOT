#!/usr/bin/env python3
"""
📖 WOLFPACK-LITE LOGGER
Terminal output + file logging for live trading
"""

import os
import json
from datetime import datetime

class SniperLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.trade_log = os.path.join(log_dir, "trade_log.txt")
        self.missed_log = os.path.join(log_dir, "missed_log.txt")
        self.pnl_log = os.path.join(log_dir, "pnl_log.txt")
        self.streak_file = os.path.join(log_dir, "streak_data.json")
        
        # Create logs directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize streak data
        self.streak_data = self.load_streak_data()
    
    def timestamp(self):
        """Get formatted timestamp"""
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    def log_trade(self, message, log_type="TRADE"):
        """
        📊 LOG TRADE EXECUTION
        Outputs to both terminal and file
        """
        timestamp = self.timestamp()
        formatted_msg = f"[{timestamp}] {log_type}: {message}"
        
        # Terminal output with colors
        if "✅" in message or "PROFIT" in message:
            print(f"\033[92m{formatted_msg}\033[0m")  # Green
        elif "❌" in message or "LOSS" in message:
            print(f"\033[91m{formatted_msg}\033[0m")  # Red
        elif "🔄" in message or "TRAIL" in message:
            print(f"\033[93m{formatted_msg}\033[0m")  # Yellow
        else:
            print(f"\033[94m{formatted_msg}\033[0m")  # Blue
        
        # File logging
        with open(self.trade_log, "a", encoding="utf-8") as f:
            f.write(formatted_msg + "\n")
    
    def log_missed(self, symbol, reason, fvg_data=None):
        """
        ❌ LOG MISSED OPPORTUNITIES
        Track why trades were skipped
        """
        timestamp = self.timestamp()
        message = f"[{timestamp}] MISSED {symbol}: {reason}"
        
        if fvg_data:
            message += f" | FVG: {fvg_data.get('type', 'N/A')} @ {fvg_data.get('midpoint', 'N/A')}"
        
        print(f"\033[95m{message}\033[0m")  # Magenta
        
        with open(self.missed_log, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    
    def log_pnl(self, symbol, side, entry, exit, pnl, balance, streak):
        """
        💰 LOG PNL UPDATES
        Track running balance and streaks
        """
        timestamp = self.timestamp()
        
        pnl_sign = "+" if pnl > 0 else ""
        message = (f"[{timestamp}] PNL: {symbol} {side.upper()} | "
                  f"Entry: {entry} Exit: {exit} | "
                  f"P&L: {pnl_sign}${pnl:.2f} | "
                  f"Balance: ${balance:.2f} | "
                  f"Streak: {streak}")
        
        # Color based on profit/loss
        if pnl > 0:
            print(f"\033[92m{message}\033[0m")  # Green
        else:
            print(f"\033[91m{message}\033[0m")  # Red
        
        with open(self.pnl_log, "a", encoding="utf-8") as f:
            f.write(message + "\n")
        
        # Update streak data
        self.update_streak_data(pnl > 0, balance)
    
    def log_error(self, error_msg, context="SYSTEM"):
        """
        🚨 LOG ERRORS
        Track system errors and API issues
        """
        timestamp = self.timestamp()
        message = f"[{timestamp}] ERROR ({context}): {error_msg}"
        
        print(f"\033[91m{message}\033[0m")  # Red
        
        with open(self.trade_log, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    
    def log_signal(self, symbol, signal_type, confluence_score, entry_data):
        """
        🎯 LOG SIGNALS
        Track FVG signals and confluence
        """
        message = (f"🎯 SIGNAL {symbol} {signal_type.upper()} | "
                  f"Confluence: {confluence_score:.1f} | "
                  f"RSI: {entry_data.get('rsi', 0):.1f} | "
                  f"Entry: {entry_data.get('fvg_midpoint', 0):.5f}")
        
        self.log_trade(message, "SIGNAL")
    
    def load_streak_data(self):
        """Load streak and balance data from file"""
        try:
            if os.path.exists(self.streak_file):
                with open(self.streak_file, "r") as f:
                    return json.load(f)
        except:
            pass
        
        # Default streak data
        return {
            "balance": 3000.0,
            "win_streak": 0,
            "loss_streak": 0,
            "total_trades": 0,
            "winning_trades": 0,
            "total_pnl": 0.0,
            "best_streak": 0,
            "worst_streak": 0,
            "last_updated": self.timestamp()
        }
    
    def update_streak_data(self, is_win, new_balance):
        """Update and save streak data"""
        self.streak_data["balance"] = new_balance
        self.streak_data["total_trades"] += 1
        self.streak_data["last_updated"] = self.timestamp()
        
        if is_win:
            self.streak_data["winning_trades"] += 1
            self.streak_data["win_streak"] += 1
            self.streak_data["loss_streak"] = 0
            
            if self.streak_data["win_streak"] > self.streak_data["best_streak"]:
                self.streak_data["best_streak"] = self.streak_data["win_streak"]
        else:
            self.streak_data["loss_streak"] += 1
            self.streak_data["win_streak"] = 0
            
            if self.streak_data["loss_streak"] > abs(self.streak_data["worst_streak"]):
                self.streak_data["worst_streak"] = -self.streak_data["loss_streak"]
        
        # Calculate total PnL
        self.streak_data["total_pnl"] = new_balance - 3000.0  # Starting capital
        
        # Save to file
        with open(self.streak_file, "w") as f:
            json.dump(self.streak_data, f, indent=2)
    
    def get_streak_multiplier(self):
        """
        🔥 GET POSITION SIZE MULTIPLIER
        Based on current streak
        """
        win_streak = self.streak_data["win_streak"]
        loss_streak = self.streak_data["loss_streak"]
        
        # Win streak scaling
        if win_streak >= 5:
            return 1.4  # +40%
        elif win_streak >= 3:
            return 1.25  # +25%
        
        # Loss streak reduction
        elif loss_streak >= 2:
            return 0.5  # -50%
        
        return 1.0  # Normal size
    
    def print_daily_stats(self):
        """
        📊 PRINT DAILY PERFORMANCE
        Summary for terminal output
        """
        data = self.streak_data
        win_rate = (data["winning_trades"] / max(data["total_trades"], 1)) * 100
        
        print("\n" + "="*60)
        print("📊 WOLFPACK-LITE DAILY STATS")
        print("="*60)
        print(f"💰 Balance: ${data['balance']:.2f}")
        print(f"📈 Total P&L: ${data['total_pnl']:.2f}")
        print(f"🎯 Trades: {data['total_trades']} | Win Rate: {win_rate:.1f}%")
        print(f"🔥 Win Streak: {data['win_streak']} | Loss Streak: {data['loss_streak']}")
        print(f"🏆 Best Streak: {data['best_streak']} | Worst: {data['worst_streak']}")
        print(f"⚡ Current Multiplier: {self.get_streak_multiplier():.1f}x")
        print("="*60 + "\n")

# Global logger instance
logger = SniperLogger()

# Convenience functions
def log_trade(msg, log_type="TRADE"):
    logger.log_trade(msg, log_type)

def log_missed(symbol, reason, fvg_data=None):
    logger.log_missed(symbol, reason, fvg_data)

def log_pnl(symbol, side, entry, exit, pnl, balance, streak):
    logger.log_pnl(symbol, side, entry, exit, pnl, balance, streak)

def log_error(error_msg, context="SYSTEM"):
    logger.log_error(error_msg, context)

def log_signal(symbol, signal_type, confluence_score, entry_data):
    logger.log_signal(symbol, signal_type, confluence_score, entry_data)

if __name__ == "__main__":
    print("📖 Logger initialized")
    logger.print_daily_stats()
