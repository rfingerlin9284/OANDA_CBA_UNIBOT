#!/usr/bin/env python3
"""
🧠 Enhanced Config Loader with Safety Validation
Loads and validates small_cap_config_oanda.json with comprehensive checks
"""
import json
import os
from datetime import datetime

def load_config(path="small_cap_config_oanda.json"):
    """Load and validate configuration file"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Config file not found: {path}")
    
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Invalid JSON in config file: {e}")
    
    print(f"\n🧠 Config Loaded: {path}")
    print(f"   📊 Strategy: {config.get('strategy_name', 'Unknown')}")
    print(f"   💰 Risk: {config.get('risk_per_trade', 0)*100:.1f}%")
    print(f"   🧠 ML Threshold: {config.get('ml_confidence_min', 0):.2f}")
    print(f"   📈 Max Trades/Day: {config.get('max_trades_per_day', 0)}")
    print(f"   🔐 OCO Required: {config.get('oco_required', False)}")
    print(f"   🛑 Stop Loss: {config.get('stop_loss_pct', 0)*100:.2f}%")
    print(f"   ✅ Take Profit: {config.get('take_profit_pct', 0)*100:.2f}%")
    print(f"Strategy: {config.get('strategy_name', 'Unknown')}")
    print(f"Risk: {config.get('risk_per_trade', 0)*100}% | ML ≥ {config.get('ml_confidence_min', 0)} | Max trades/day: {config.get('max_trades_per_day', 0)}")
    print(f"OCO Required: {config.get('oco_required', False)} | Bot Enabled: {config.get('bot_enabled', False)}")
    
    return config

def get_decimal_precision(pair, config):
    """Get decimal precision for a currency pair"""
    return config.get('decimal_precision', {}).get(pair, 5)

def is_bot_enabled(config):
    """Check if bot is enabled in config"""
    return config.get('bot_enabled', False)

def validate_config_safety(config):
    """Validate configuration for safety parameters"""
    safety_checks = []
    
    # Risk validation
    risk = config.get('risk_per_trade', 0)
    if risk > 0.05:
        safety_checks.append(f"⚠️ High risk per trade: {risk*100}%")
    
    # ML confidence validation
    ml_conf = config.get('ml_confidence_min', 0)
    if ml_conf < 0.75:
        safety_checks.append(f"⚠️ Low ML confidence threshold: {ml_conf}")
    
    # Trade frequency validation
    max_trades = config.get('max_trades_per_day', 0)
    if max_trades > 5:
        safety_checks.append(f"⚠️ High trade frequency: {max_trades}/day")
    
    # OCO validation
    if not config.get('oco_required', False):
        safety_checks.append("❌ OCO protection disabled")
    
    return safety_checks

if __name__ == "__main__":
    # Test the config loader
    try:
        config = load_config()
        safety_issues = validate_config_safety(config)
        
        print("\n" + "="*50)
        print("🔧 CONFIG LOADER TEST")
        print("="*50)
        
        if safety_issues:
            print("🚨 SAFETY ISSUES FOUND:")
            for issue in safety_issues:
                print(f"   {issue}")
        else:
            print("✅ Configuration is safe for trading")
            
    except Exception as e:
        print(f"❌ Error loading config: {e}")
