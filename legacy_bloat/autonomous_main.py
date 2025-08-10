#!/usr/bin/env python3
"""
🤖 OANDA Autonomous Bot - Main Trading Loop
Developer Manual Implementation
For small-cap trading with full protection, automation, and daily scaling logic

Starting Capital: $3,000-$4,000
Daily Goal: $80-$120 (initial) → $400/day (target)
Risk Per Trade: 2%
Leverage: 30:1
Trade Frequency: 1-2 trades per day
Target R:R Ratio: 2:1
"""
import os
import time
import json
import sys
import random
import csv
from datetime import datetime, timedelta
from load_config import load_config, is_bot_enabled, get_decimal_precision

# Global variables
CONFIG_PATH = "small_cap_config_oanda.json"
last_mtime = 0
config = None
trade_count_today = 0
last_trade_time = {}
daily_profit = 0.0
start_time = time.time()

def initialize_system():
    """Initialize the autonomous trading system"""
    global config, last_mtime
    
    print("\n" + "="*60)
    print("🤖 OANDA AUTONOMOUS BOT - INITIALIZING")
    print("="*60)
    print("📊 Small-cap trading with full protection")
    print("💰 Target: $400/day with 2% risk per trade")
    print("🛡️ OCO enforcement and ML confidence filtering")
    print("="*60)
    
    # Load initial configuration
    if os.path.exists(CONFIG_PATH):
        config = load_config(CONFIG_PATH)
        last_mtime = os.path.getmtime(CONFIG_PATH)
    else:
        print(f"❌ Configuration file not found: {CONFIG_PATH}")
        sys.exit(1)
    
    # Validate bot is enabled
    if not is_bot_enabled(config):
        print("🛑 Bot is disabled in configuration")
        print("   Set 'bot_enabled': true to enable autonomous trading")
        return False
    
    # Check for BOT_LOCK file (emergency stop)
    if os.path.exists('.BOT_LOCK'):
        print("🔒 BOT_LOCK file detected - trading disabled")
        print("   Remove .BOT_LOCK file to enable trading")
        return False
    
    # Initialize trade log CSV if enabled
    if config.get('log_trades_to_csv', False):
        initialize_trade_log()
    
    print("✅ System initialized successfully")
    return True

def initialize_trade_log():
    """Initialize CSV trade logging"""
    csv_path = config.get('csv_log_path', 'trade_log.csv')
    
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'timestamp', 'pair', 'entry', 'sl', 'tp', 
                'result', 'model', 'confidence', 'risk_amount',
                'position_size', 'daily_count'
            ])
        print(f"📝 Trade log initialized: {csv_path}")

def check_config_updates():
    """Check for configuration file updates and reload if needed"""
    global config, last_mtime
    
    current_mtime = os.path.getmtime(CONFIG_PATH)
    if current_mtime != last_mtime:
        print("🔁 Configuration file updated - reloading...")
        config = load_config(CONFIG_PATH)
        last_mtime = current_mtime
        return True
    return False

def liveulate_ml_signal():
    """Simulate ML trading signal with confidence score"""
    # In real implementation, this would connect to your ML model
    pairs = ["EUR_USD", "USD_JPY", "GBP_USD", "AUD_USD", "USD_CAD", "USD_CHF", 
             "EUR_GBP", "EUR_JPY", "GBP_JPY", "AUD_JPY", "NZD_USD", "EUR_AUD"]
    
    confidence = random.uniform(0.65, 0.95)
    pair = random.choice(pairs)
    direction = random.choice(["BUY", "SELL"])
    
    # Simulate price data
    base_price = {
        "EUR_USD": 1.1234, "USD_JPY": 149.50, "GBP_USD": 1.2567,
        "AUD_USD": 0.6789, "USD_CAD": 1.3456, "USD_CHF": 0.8901,
        "EUR_GBP": 0.8765, "EUR_JPY": 163.45, "GBP_JPY": 187.89,
        "AUD_JPY": 101.23, "NZD_USD": 0.6123, "EUR_AUD": 1.6543
    }
    
    current_price = base_price.get(pair, 1.0000) + random.uniform(-0.01, 0.01)
    
    return {
        'confidence': confidence,
        'pair': pair,
        'direction': direction,
        'entry_price': current_price,
        'timestamp': datetime.now()
    }

def cooldown_passed(pair, cooldown_seconds):
    """Check if cooldown period has passed for a currency pair"""
    if pair not in last_trade_time:
        return True
    
    time_elapsed = time.time() - last_trade_time[pair]
    return time_elapsed > cooldown_seconds

def calculate_position_size(pair, entry_price, risk_amount):
    """Calculate position size based on risk management"""
    # Get decimal precision for the pair
    precision = get_decimal_precision(pair, config)
    
    # Base position size from config
    base_size = config.get('base_position_size', 2000)
    lot_cap = config.get('lot_size_cap', 2000)
    
    # Calculate position size based on risk
    # This is liveplified - in real implementation would use account balance
    position_size = min(base_size, lot_cap)
    
    return position_size

def calculate_oco_levels(pair, entry_price, direction, risk_ratio=2.0):
    """Calculate stop-loss and take-profit levels for OCO orders"""
    precision = get_decimal_precision(pair, config)
    
    # Calculate pip value based on pair type
    if 'JPY' in pair:
        pip_value = 0.01
        min_distance = 20  # 20 pips minimum for JPY pairs
    else:
        pip_value = 0.0001
        min_distance = 20  # 20 pips minimum
    
    pip_distance = min_distance * pip_value
    
    if direction == "BUY":
        stop_loss = round(entry_price - pip_distance, precision)
        take_profit = round(entry_price + (pip_distance * risk_ratio), precision)
    else:  # SELL
        stop_loss = round(entry_price + pip_distance, precision)
        take_profit = round(entry_price - (pip_distance * risk_ratio), precision)
    
    return stop_loss, take_profit

def log_trade_to_csv(trade_data):
    """Log trade data to CSV file"""
    if not config.get('log_trades_to_csv', False):
        return
    
    csv_path = config.get('csv_log_path', 'trade_log.csv')
    
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            trade_data['timestamp'],
            trade_data['pair'],
            trade_data['entry'],
            trade_data['sl'],
            trade_data['tp'],
            trade_data.get('result', 'PENDING'),
            trade_data['model'],
            trade_data['confidence'],
            trade_data['risk_amount'],
            trade_data['position_size'],
            trade_data['daily_count']
        ])

def execute_trade(signal):
    """Execute a trade based on ML signal (live_mode for manual implementation)"""
    global trade_count_today, daily_profit
    
    pair = signal['pair']
    direction = signal['direction']
    entry_price = signal['entry_price']
    confidence = signal['confidence']
    
    # Calculate risk amount (2% of account)
    account_balance = 3500  # Simulated account balance
    risk_amount = account_balance * config['risk_per_trade']
    
    # Calculate position size
    position_size = calculate_position_size(pair, entry_price, risk_amount)
    
    # Calculate OCO levels
    risk_ratio = config.get('min_reward_risk_ratio', 2.0)
    stop_loss, take_profit = calculate_oco_levels(pair, entry_price, direction, risk_ratio)
    
    # Prepare trade data
    trade_data = {
        'timestamp': datetime.now().isoformat(),
        'pair': pair,
        'direction': direction,
        'entry': entry_price,
        'sl': stop_loss,
        'tp': take_profit,
        'model': config.get('strategy_name', 'JohnsScalp'),
        'confidence': confidence,
        'risk_amount': risk_amount,
        'position_size': position_size,
        'daily_count': trade_count_today + 1
    }
    
    # In real implementation, this would place actual orders via OANDA API
    print(f"🚀 EXECUTING TRADE:")
    print(f"   📊 Pair: {pair} | Direction: {direction}")
    print(f"   💰 Entry: {entry_price} | Size: {position_size}")
    print(f"   🛡️ Stop Loss: {stop_loss} | Take Profit: {take_profit}")
    print(f"   🎯 Risk: ${risk_amount:.2f} | R:R Ratio: {risk_ratio}")
    print(f"   🧠 ML Confidence: {confidence:.2f}")
    
    # Update tracking variables
    trade_count_today += 1
    last_trade_time[pair] = time.time()
    
    # Log to CSV
    log_trade_to_csv(trade_data)
    
    # Simulate trade result (for live_mode purposes)
    liveulate_trade_result(trade_data)
    
    return True

def liveulate_trade_result(trade_data):
    """Simulate trade result for live_modenstration"""
    global daily_profit
    
    # Simulate random outcome (70% win rate)
    win = random.random() < 0.70
    
    if win:
        profit = trade_data['risk_amount'] * 2  # 2:1 R:R ratio
        daily_profit += profit
        print(f"   ✅ Trade Result: +${profit:.2f} (WIN)")
    else:
        loss = -trade_data['risk_amount']
        daily_profit += loss
        print(f"   ❌ Trade Result: ${loss:.2f} (LOSS)")
    
    print(f"   📈 Daily P&L: ${daily_profit:.2f}")

def check_daily_limits():
    """Check if daily trading limits have been reached"""
    global trade_count_today
    
    max_trades = config.get('max_trades_per_day', 2)
    
    if trade_count_today >= max_trades:
        print(f"🎯 Daily trade limit reached: {trade_count_today}/{max_trades}")
        return False
    
    return True

def reset_daily_counters():
    """Reset daily counters at start of new trading day"""
    global trade_count_today, daily_profit, start_time
    
    current_time = datetime.now()
    start_datetime = datetime.fromtimestamp(start_time)
    
    # Reset if it's a new day
    if current_time.date() > start_datetime.date():
        print(f"📅 New trading day - resetting counters")
        print(f"   Previous day P&L: ${daily_profit:.2f}")
        print(f"   Previous day trades: {trade_count_today}")
        
        trade_count_today = 0
        daily_profit = 0.0
        start_time = time.time()
        
        return True
    
    return False

def display_status():
    """Display current bot status"""
    uptime = time.time() - start_time
    uptime_hours = uptime / 3600
    
    print(f"\n📊 BOT STATUS UPDATE")
    print(f"   🕐 Uptime: {uptime_hours:.1f} hours")
    print(f"   📈 Daily P&L: ${daily_profit:.2f}")
    print(f"   🎯 Trades Today: {trade_count_today}/{config.get('max_trades_per_day', 2)}")
    print(f"   🤖 Strategy: {config.get('strategy_name', 'Unknown')}")
    print(f"   🛡️ OCO Required: {config.get('oco_required', False)}")

def main_trading_loop():
    """Main autonomous trading loop"""
    print("\n🚀 Starting autonomous trading loop...")
    print("   Press Ctrl+C to stop")
    
    loop_count = 0
    
    while True:
        try:
            # Check for emergency stop
            if os.path.exists('.BOT_LOCK'):
                print("🔒 BOT_LOCK detected - pausing trading")
                time.sleep(60)
                continue
            
            # Check for configuration updates
            check_config_updates()
            
            # Check if bot is still enabled
            if not is_bot_enabled(config):
                print("🛑 Bot disabled in config - pausing...")
                time.sleep(300)  # Wait 5 minutes before checking again
                continue
            
            # Reset daily counters if new day
            reset_daily_counters()
            
            # Check daily trading limits
            if not check_daily_limits():
                print("⏳ Daily limit reached - waiting for next day...")
                time.sleep(3600)  # Wait 1 hour before checking again
                continue
            
            # Get ML signal
            signal = liveulate_ml_signal()
            
            print(f"\n📡 Signal #{loop_count + 1}: {signal['pair']} | "
                  f"Confidence: {signal['confidence']:.3f} | "
                  f"Direction: {signal['direction']}")
            
            # Check ML confidence threshold
            if signal['confidence'] >= config['ml_confidence_min']:
                # Check cooldown period
                if cooldown_passed(signal['pair'], config['cooldown_seconds']):
                    # Execute trade
                    print("✅ Signal passed all filters - executing trade")
                    execute_trade(signal)
                else:
                    remaining_cooldown = config['cooldown_seconds'] - (time.time() - last_trade_time.get(signal['pair'], 0))
                    print(f"⏳ Cooldown active for {signal['pair']} - {remaining_cooldown:.0f}s remaining")
            else:
                print(f"❌ Signal rejected - confidence {signal['confidence']:.3f} < {config['ml_confidence_min']}")
            
            # Display status every 10 loops
            if loop_count % 10 == 0:
                display_status()
            
            loop_count += 1
            
            # Sleep before next signal check
            time.sleep(10)  # Check for new signals every 10 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Trading loop stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in trading loop: {e}")
            time.sleep(30)  # Wait 30 seconds before continuing

def main():
    """Main entry point for autonomous bot"""
    if not initialize_system():
        print("❌ System initialization failed")
        sys.exit(1)
    
    try:
        main_trading_loop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        print("\n🏁 Autonomous bot shutdown complete")

if __name__ == "__main__":
    main()
