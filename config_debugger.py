#!/usr/bin/env python3
"""
🔍 Enhanced Config Debugger - OANDA Bot Safety Validator
Comprehensive validation and safety checks for trading configuration
"""

from load_config import load_config
import json

def run_config_debugger():
    """Run comprehensive config debugging and safety validation"""
    print("� CONFIG DEBUGGER & SAFETY VALIDATOR")
    print("=" * 50)
    
    try:
        config = load_config()
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return False
    
    issues = []
    warnings = []
    
    # CRITICAL SAFETY CHECKS
    print(f"\n� CRITICAL SAFETY CHECKS:")
    
    # OCO protection - MOST IMPORTANT
    if not config.get("oco_required", False):
        issues.append("❌ OCO protection DISABLED - EXTREMELY DANGEROUS!")
    else:
        print(f"   ✅ OCO protection: ENABLED (SAFE)")
    
    # Risk management
    risk_pct = config.get("risk_per_trade", 0)
    if risk_pct > 0.05:
        issues.append(f"⚠️ Risk per trade DANGEROUS: {risk_pct*100:.1f}% (max: 5%)")
    else:
        print(f"   ✅ Risk per trade: {risk_pct*100:.1f}% (SAFE)")
    
    # Stop Loss validation
    sl_pct = config.get("stop_loss_pct", 0)
    if sl_pct == 0:
        issues.append("❌ No stop loss percentage defined")
    elif sl_pct > 0.01:  # 1%
        warnings.append(f"⚠️ Stop loss wide: {sl_pct*100:.2f}%")
    else:
        print(f"   ✅ Stop loss: {sl_pct*100:.2f}% (GOOD)")
    
    # Take Profit validation
    tp_pct = config.get("take_profit_pct", 0)
    if tp_pct == 0:
        issues.append("❌ No take profit percentage defined")
    else:
        print(f"   ✅ Take profit: {tp_pct*100:.2f}%")
    
    # Risk-reward ratio
    if sl_pct > 0 and tp_pct > 0:
        rr_ratio = tp_pct / sl_pct
        if rr_ratio < 1.5:
            warnings.append(f"⚠️ Low RR ratio: {rr_ratio:.1f}:1")
        else:
            print(f"   ✅ Risk-reward ratio: {rr_ratio:.1f}:1 (EXCELLENT)")
    
    # ML confidence
    ml_min = config.get("ml_confidence_min", 0)
    if ml_min < 0.75:
        issues.append(f"⚠️ ML confidence too low: {ml_min}")
    else:
        print(f"   ✅ ML confidence: {ml_min} (GOOD)")
    
    # Display results
    if issues:
        print(f"\n🚨 CRITICAL ISSUES:")
        for issue in issues:
            print(f"   {issue}")
        print(f"\n❌ CONFIG UNSAFE - Fix issues before trading!")
        return False
    
    if warnings:
        print(f"\n⚠️ WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
    
    print(f"\n✅ Config safety validation PASSED")
    return True
        
        # Risk management
        print("\n🛡️ RISK MANAGEMENT:")
        print(f"  🔹 Lot size cap: {config.get('lot_size_cap', 0)}")
        print(f"  🔹 OCO required: {config.get('oco_required', False)}")
        print(f"  🔹 Bot enabled: {config.get('bot_enabled', False)}")
        print(f"  🔹 Min R:R ratio: {config.get('min_reward_risk_ratio', 'NOT SET')}")
        
        # Decimal precision settings
        print("\n📊 DECIMAL PRECISION:")
        decimal_prec = config.get('decimal_precision', {})
        for pair, precision in decimal_prec.items():
            print(f"  🔹 {pair}: {precision} decimals")
        
        # Logging settings
        print("\n📝 LOGGING:")
        print(f"  🔹 Log trades to CSV: {config.get('log_trades_to_csv', False)}")
        print(f"  🔹 CSV log path: {config.get('csv_log_path', 'NOT SET')}")
        
        # Anti-drift protection
        print("\n🔒 ANTI-DRIFT PROTECTION:")
        print(f"  🔹 Anti-drift enabled: {config.get('anti_drift_enabled', False)}")
        print(f"  🔹 Drift monitoring: {config.get('drift_monitoring_enabled', False)}")
        print(f"  🔹 Drift check interval: {config.get('drift_check_interval', 0)} seconds")
        
        # Safety analysis
        print("\n🚨 SAFETY ANALYSIS:")
        if issues:
            print("❌ ISSUES FOUND:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("✅ All safety checks passed")
        
        # Bot status
        print("\n🤖 BOT STATUS:")
        bot_enabled = config.get('bot_enabled', False)
        if bot_enabled:
            print("✅ Bot is ENABLED and ready for autonomous trading")
        else:
            print("🛑 Bot is DISABLED - autonomous trading paused")
        
        # Live mode warning
        if config.get('live_mode', False):
            print("\n⚠️  LIVE TRADING MODE ACTIVE")
            print("   Real money will be used for trades!")
        else:
            print("\n🧪 live_mode/live_mode mode")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Error during config debugging: {e}")
        return False

def quick_safety_check():
    """Quick safety validation without full debug output"""
    try:
        config = load_config()
        issues = validate_config_safety(config)
        
        if issues:
            print("🚨 SAFETY ISSUES DETECTED:")
            for issue in issues:
                print(f"   {issue}")
            return False
        else:
            print("✅ Config safety validation passed")
            return True
            
    except Exception as e:
        print(f"❌ Safety check failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_safety_check()
    else:
        run_config_debugger()
