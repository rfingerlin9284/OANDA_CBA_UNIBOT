#!/usr/bin/env python3
"""
🤖 Enhanced Autonomous OANDA Trading Bot
Integrates OCO trade engine with comprehensive safety and monitoring
"""

import os
import time
import json
import sys
import random
from datetime import datetime, timedelta
from load_config import load_config
from oco_trade_engine_oanda import OandaOCOTradeEngine
from config_debugger import run_config_debugger

class AutonomousOandaBot:
    def __init__(self, config_path="small_cap_config_oanda.json"):
        self.config_path = config_path
        self.config = None
        self.trade_engine = None
        self.last_config_mtime = None
        self.trade_count_today = 0
        self.last_trade_time = {}
        self.daily_reset_time = None
        self.bot_start_time = datetime.now()
        
        print("🤖 AUTONOMOUS OANDA BOT INITIALIZING")
        print("=" * 50)
        
        # Initial setup
        self.reload_config()
        self.initialize_trade_engine()
        self.reset_daily_counters()
        
    def reload_config(self):
        """Reload configuration if file has changed"""
        try:
            current_mtime = os.path.getmtime(self.config_path)
            if self.last_config_mtime is None or current_mtime != self.last_config_mtime:
                print("🔄 Loading/reloading configuration...")
                self.config = load_config(self.config_path)
                self.last_config_mtime = current_mtime
                
                # Run safety validation
                if not run_config_debugger():
                    print("❌ Config validation failed!")
                    return False
                    
                print("✅ Configuration loaded and validated")
                return True
            return True
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return False
    
    def initialize_trade_engine(self):
        """Initialize the OCO trade engine"""
        try:
            self.trade_engine = OandaOCOTradeEngine(self.config_path)
            print("✅ OCO Trade Engine initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize trade engine: {e}")
            return False
    
    def reset_daily_counters(self):
        """Reset daily trading counters"""
        now = datetime.now()
        if self.daily_reset_time is None or now.date() > self.daily_reset_time.date():
            self.trade_count_today = 0
            self.daily_reset_time = now
            print(f"🔄 Daily counters reset for {now.strftime('%Y-%m-%d')}")
    
    def liveulate_ml_signal(self):
        """Simulate ML trading signal with realistic confidence levels"""
        # Simulate realistic ML confidence distribution
        base_confidence = random.uniform(0.70, 0.95)
        
        # Bias toward higher confidence during "good" market conditions
        market_bias = random.uniform(0.95, 1.05)  # Simulate market conditions
        confidence = min(base_confidence * market_bias, 0.99)
        
        # Select currency pair with realistic probabilities
        major_pairs = ["EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD", "USD_CHF"]
        yen_pairs = ["EUR_JPY", "GBP_JPY", "AUD_JPY"]
        exotic_pairs = ["EUR_GBP", "EUR_AUD", "NZD_USD"]
        
        # Weight toward major pairs (70%), then yen pairs (20%), then exotic (10%)
        rand = random.random()
        if rand < 0.7:
            pair = random.choice(major_pairs)
        elif rand < 0.9:
            pair = random.choice(yen_pairs)
        else:
            pair = random.choice(exotic_pairs)
        
        # Direction with slight bias
        direction = "buy" if random.random() > 0.48 else "sell"  # Slight buy bias
        
        return confidence, pair, direction
    
    def check_cooldown(self, pair):
        """Check if cooldown period has passed for this pair"""
        last_time = self.last_trade_time.get(pair, 0)
        cooldown_period = self.config.get("cooldown_seconds", 300)
        return time.time() - last_time > cooldown_period
    
    def check_trading_conditions(self):
        """Check all conditions required for trading"""
        print(f"\n🔍 CHECKING TRADING CONDITIONS")
        
        # Bot enabled check
        if not self.config.get("bot_enabled", True):
            print("🛑 Bot disabled in config. Pausing...")
            return False, "Bot disabled"
        
        # Daily trade limit
        max_trades = self.config.get("max_trades_per_day", 2)
        if self.trade_count_today >= max_trades:
            print(f"🎯 Daily trade limit reached: {self.trade_count_today}/{max_trades}")
            return False, "Daily limit reached"
        
        # Check for BOT_LOCK file (emergency stop)
        lock_file = ".BOT_LOCK"
        if os.path.exists(lock_file):
            print("🔒 BOT_LOCK file detected. Trading suspended.")
            return False, "Emergency lock active"
        
        print("✅ All trading conditions met")
        return True, "Ready to trade"
    
    def execute_trade_if_valid(self, confidence, pair, direction):
        """Execute trade if all conditions are met"""
        print(f"\n📡 SIGNAL RECEIVED:")
        print(f"   📊 Pair: {pair}")
        print(f"   📈 Direction: {direction.upper()}")
        print(f"   🧠 ML Confidence: {confidence:.3f}")
        
        # Check ML confidence threshold
        min_confidence = self.config.get("ml_confidence_min", 0.82)
        if confidence < min_confidence:
            print(f"❌ Confidence too low: {confidence:.3f} < {min_confidence}")
            return False
        
        # Check cooldown for this pair
        if not self.check_cooldown(pair):
            cooldown = self.config.get("cooldown_seconds", 300)
            print(f"❌ Cooldown active for {pair} ({cooldown}s)")
            return False
        
        # Validate with trade engine
        if not self.trade_engine.validate_trade_conditions(pair, confidence):
            print(f"❌ Trade engine validation failed")
            return False
        
        print(f"🚀 EXECUTING TRADE...")
        
        # Execute the OCO trade
        success = self.trade_engine.place_oco_trade(pair, direction, confidence)
        
        if success:
            self.trade_count_today += 1
            self.last_trade_time[pair] = time.time()
            print(f"✅ TRADE EXECUTED SUCCESSFULLY!")
            print(f"   📊 Trades today: {self.trade_count_today}")
            return True
        else:
            print(f"❌ Trade execution failed")
            return False
    
    def display_status(self):
        """Display current bot status"""
        uptime = datetime.now() - self.bot_start_time
        max_trades = self.config.get("max_trades_per_day", 2)
        
        print(f"\n📊 BOT STATUS:")
        print(f"   ⏰ Uptime: {str(uptime).split('.')[0]}")
        print(f"   📈 Trades today: {self.trade_count_today}/{max_trades}")
        print(f"   🧠 ML threshold: {self.config.get('ml_confidence_min', 0)}")
        print(f"   💰 Risk per trade: {self.config.get('risk_per_trade', 0)*100:.1f}%")
        print(f"   🔐 OCO required: {self.config.get('oco_required', False)}")
        print(f"   🤖 Bot enabled: {self.config.get('bot_enabled', True)}")
    
    def run(self):
        """Main trading loop"""
        print(f"\n🚀 STARTING AUTONOMOUS TRADING LOOP")
        print(f"   Strategy: {self.config.get('strategy_name', 'Unknown')}")
        print(f"   Mode: {'LIVE' if self.config.get('live_mode') else 'live_mode'}")
        print(f"   Target: ${self.config.get('daily_target', 400)}/day")
        
        loop_count = 0
        
        try:
            while True:
                loop_count += 1
                
                # Reload config if changed
                if not self.reload_config():
                    print("⚠️ Config reload failed, continuing with current config...")
                
                # Reset daily counters if new day
                self.reset_daily_counters()
                
                # Check if trading is allowed
                can_trade, reason = self.check_trading_conditions()
                if not can_trade:
                    if reason == "Daily limit reached":
                        print(f"💤 Daily trading complete. Sleeping for 1 hour...")
                        time.sleep(3600)  # Sleep 1 hour
                    elif reason == "Bot disabled":
                        print(f"💤 Bot disabled. Checking again in 5 minutes...")
                        time.sleep(300)   # Sleep 5 minutes
                    elif reason == "Emergency lock active":
                        print(f"🔒 Emergency lock active. Checking again in 30 seconds...")
                        time.sleep(30)    # Sleep 30 seconds
                    continue
                
                # Display status every 10 loops
                if loop_count % 10 == 0:
                    self.display_status()
                
                # Generate ML signal
                confidence, pair, direction = self.liveulate_ml_signal()
                
                # Attempt to execute trade
                if self.execute_trade_if_valid(confidence, pair, direction):
                    print(f"🎉 Trade successful! Waiting for next opportunity...")
                else:
                    print(f"⏭️ Signal rejected, continuing...")
                
                # Wait before next signal check
                signal_interval = self.config.get("signal_check_interval", 10)
                print(f"⏰ Next signal check in {signal_interval} seconds...")
                time.sleep(signal_interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Bot stopped by user (Ctrl+C)")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print(f"🔄 Bot will restart in 30 seconds...")
            time.sleep(30)

def main():
    """Main function with error handling and restart logic"""
    max_restarts = 5
    restart_count = 0
    
    while restart_count < max_restarts:
        try:
            bot = AutonomousOandaBot()
            bot.run()
            break  # If we get here, bot stopped normally
            
        except Exception as e:
            restart_count += 1
            print(f"\n❌ Bot crashed: {e}")
            print(f"🔄 Restart attempt {restart_count}/{max_restarts}")
            
            if restart_count < max_restarts:
                print(f"⏰ Restarting in 60 seconds...")
                time.sleep(60)
            else:
                print(f"💀 Max restarts reached. Bot shutting down.")
                break

if __name__ == "__main__":
    print("🤖 Enhanced Autonomous OANDA Bot")
    print("=" * 40)
    print("Features:")
    print("✅ Mandatory OCO orders")
    print("✅ Risk-based position sizing") 
    print("✅ ML confidence filtering")
    print("✅ Configurable parameters")
    print("✅ Emergency lock system")
    print("✅ Auto-restart capability")
    print("=" * 40)
    
    main()
