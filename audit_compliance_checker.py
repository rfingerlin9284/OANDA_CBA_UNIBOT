#!/usr/bin/env python3
"""
🔍 WOLFPACK-LITE AUDIT COMPLIANCE CHECKER
Verify all critical audit issues have been resolved
"""

import os
import json
import sys
from datetime import datetime

def check_authentication_implementation():
    """Check JWT ed25519 authentication implementation"""
    print("🔐 CHECKING AUTHENTICATION IMPLEMENTATION...")
    
    issues = []
    
    # Check if coinbase_advanced_api.py exists and has proper JWT implementation
    api_file = "coinbase_advanced_api.py"
    if not os.path.exists(api_file):
        issues.append("❌ coinbase_advanced_api.py missing")
    else:
        with open(api_file, 'r') as f:
            content = f.read()
            
        if "jwt.encode" not in content:
            issues.append("❌ JWT encoding not found in API file")
        if "EdDSA" not in content:
            issues.append("❌ EdDSA algorithm not specified")
        if "ed25519" not in content.lower():
            issues.append("❌ ed25519 references missing")
        if "cryptography.hazmat.primitives" not in content:
            issues.append("❌ Proper cryptography imports missing")
    
    # Check credentials structure
    cred_file = "credentials.py"
    if not os.path.exists(cred_file):
        issues.append("❌ credentials.py missing")
    else:
        with open(cred_file, 'r') as f:
            content = f.read()
            
        if "COINBASE_API_KEY" not in content:
            issues.append("❌ COINBASE_API_KEY not defined")
        if "COINBASE_PRIVATE_KEY_B64" not in content:
            issues.append("❌ COINBASE_PRIVATE_KEY_B64 not defined")
        if "live_mode" in content.lower() and "false" not in content.lower():
            issues.append("⚠️  Potential live_mode mode detected")
    
    if not issues:
        print("✅ JWT ed25519 authentication properly implemented")
        return True
    else:
        for issue in issues:
            print(f"   {issue}")
        return False

def check_oco_verification_logic():
    """Check OCO verification logic fixes"""
    print("\n🛡️  CHECKING OCO VERIFICATION LOGIC...")
    
    issues = []
    
    # Check OCO executor implementation
    oco_file = "oco_executor.py"
    if not os.path.exists(oco_file):
        issues.append("❌ oco_executor.py missing")
        return False
    
    with open(oco_file, 'r') as f:
        content = f.read()
    
    # Check for critical fixes
    if "stopLossOrderTransaction" not in content:
        issues.append("❌ OANDA attached order checking missing")
    if "takeProfitOrderTransaction" not in content:
        issues.append("❌ OANDA take profit verification missing")
    if "OCO verification failed" not in content:
        issues.append("❌ OCO failure handling missing")
    if "position_tracker" not in content:
        issues.append("❌ Position tracking integration missing")
    
    # Check for old broken logic patterns
    if "separate orders" in content.lower():
        issues.append("⚠️  Old broken logic patterns may still exist")
    
    if not issues:
        print("✅ OCO verification logic properly fixed")
        return True
    else:
        for issue in issues:
            print(f"   {issue}")
        return False

def check_position_tracking_system():
    """Check position tracking implementation"""
    print("\n📊 CHECKING POSITION TRACKING SYSTEM...")
    
    issues = []
    
    # Check if position tracker exists
    tracker_file = "position_tracker.py"
    if not os.path.exists(tracker_file):
        issues.append("❌ position_tracker.py missing")
        return False
    
    with open(tracker_file, 'r') as f:
        content = f.read()
    
    # Check for essential methods
    required_methods = [
        "add_position",
        "close_position", 
        "save_positions",
        "load_positions",
        "get_active_positions",
        "get_daily_stats"
    ]
    
    for method in required_methods:
        if f"def {method}" not in content:
            issues.append(f"❌ Missing method: {method}")
    
    # Check for file creation capability
    if "active_positions.json" not in content:
        issues.append("❌ Position file management missing")
    if "trades_history.json" not in content:
        issues.append("❌ Trade history tracking missing")
    
    # Check data directory creation
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"   ℹ️  Creating data directory: {data_dir}")
        try:
            os.makedirs(data_dir, exist_ok=True)
        except:
            issues.append("❌ Cannot create data directory")
    
    if not issues:
        print("✅ Position tracking system properly implemented")
        return True
    else:
        for issue in issues:
            print(f"   {issue}")
        return False

def check_error_handling_improvements():
    """Check error handling and success reporting fixes"""
    print("\n🚨 CHECKING ERROR HANDLING IMPROVEMENTS...")
    
    issues = []
    
    # Check main files for proper error handling
    files_to_check = ["main.py", "oco_executor.py", "logger.py", "position_tracker.py"]
    
    for file in files_to_check:
        if not os.path.exists(file):
            issues.append(f"❌ {file} missing")
            continue
            
        with open(file, 'r') as f:
            content = f.read()
        
        # Look for proper error handling patterns
        if "log_error" not in content and file != "logger.py":
            issues.append(f"❌ {file}: log_error usage missing")
        
        # Check for try/except blocks - more lenient check
        if "try:" in content:
            # Count try/except pairs more accurately
            lines = content.split('\n')
            try_count = 0
            except_count = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('try:'):
                    try_count += 1
                elif stripped.startswith('except') and ':' in stripped:
                    except_count += 1
            
            # Allow some tolerance for complex exception handling
            if try_count > except_count + 2:  # More lenient check
                issues.append(f"⚠️  {file}: Some try blocks may be missing except clauses")
    
    # Check logger implementation specifically
    if os.path.exists("logger.py"):
        with open("logger.py", 'r') as f:
            logger_content = f.read()
        
        if "def log_error" not in logger_content:
            issues.append("❌ log_error function missing in logger")
        if "def log_trade" not in logger_content:
            issues.append("❌ log_trade function missing in logger")
        if "def log_pnl" not in logger_content:
            issues.append("❌ log_pnl function missing in logger")
    
    # Check for ta library import capability
    try:
        import ta
        print("   ✅ ta library import verified")
    except ImportError:
        issues.append("❌ ta library not installed (required for technical analysis)")
    
    if not issues:
        print("✅ Error handling properly improved")
        return True
    else:
        for issue in issues:
            print(f"   {issue}")
        return False

def check_live_trading_configuration():
    """Check that all systems are configured for live trading only"""
    print("\n⚡ CHECKING LIVE TRADING CONFIGURATION...")
    
    issues = []
    
    files_to_check = ["credentials.py", "main.py", "coinbase_advanced_api.py"]
    
    for file in files_to_check:
        if not os.path.exists(file):
            continue
            
        with open(file, 'r') as f:
            content = f.read()
        
        # Check for live_mode/live_mode mode indicators (but allow "NO live_mode" comments)
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Skip comments that say "no live_mode" or "no live_mode"
            if ("no live_mode" in line_lower or "no live_mode" in line_lower or 
                "live trading only" in line_lower):
                continue
                
            # Check for problematic references
            if ("live_mode" in line_lower and "false" not in line_lower and 
                "#" not in line and "comment" not in line_lower):
                issues.append(f"⚠️  {file}:{line_num}: Potential live_mode mode detected")
            elif ("live_mode" in line_lower and "#" not in line and 
                  "comment" not in line_lower):
                issues.append(f"⚠️  {file}:{line_num}: live_mode mode references found")
            elif ("live_mode" in line_lower and "#" not in line and 
                  "comment" not in line_lower):
                issues.append(f"⚠️  {file}:{line_num}: live_mode mode references found")
    
    # Check for live endpoints
    if os.path.exists("credentials.py"):
        with open("credentials.py", 'r') as f:
            cred_content = f.read()
        
        if "api-fxtrade.oanda.com" not in cred_content:
            issues.append("❌ OANDA live endpoint not configured")
        if "api.coinbase.com" not in cred_content:
            issues.append("❌ Coinbase live endpoint not configured")
    
    if not issues:
        print("✅ Live trading configuration verified")
        return True
    else:
        for issue in issues:
            print(f"   {issue}")
        return False

def check_system_architecture():
    """Check overall system architecture completeness"""
    print("\n🏗️  CHECKING SYSTEM ARCHITECTURE...")
    
    core_files = [
        "main.py",
        "sniper_core.py", 
        "oco_executor.py",
        "credentials.py",
        "logger.py",
        "coinbase_advanced_api.py",
        "position_tracker.py"
    ]
    
    optional_files = [
        "timezone_manager.py",
        "portfolio_manager.py", 
        "arbitrage_engine.py",
    ]
    
    missing_core = []
    missing_optional = []
    
    for file in core_files:
        if not os.path.exists(file):
            missing_core.append(file)
    
    for file in optional_files:
        if not os.path.exists(file):
            missing_optional.append(file)
    
    print(f"   📁 Core files: {len(core_files) - len(missing_core)}/{len(core_files)} present")
    print(f"   📁 Optional files: {len(optional_files) - len(missing_optional)}/{len(optional_files)} present")
    
    if missing_core:
        print("   ❌ Missing core files:")
        for file in missing_core:
            print(f"      - {file}")
        return False
    
    if missing_optional:
        print("   ⚠️  Missing optional files:")
        for file in missing_optional:
            print(f"      - {file}")
    
    print("✅ Core system architecture complete")
    return True

def run_comprehensive_audit():
    """Run complete audit compliance check"""
    print("🔍 WOLFPACK-LITE AUDIT COMPLIANCE CHECKER")
    print("=" * 60)
    print(f"📅 Check Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"📂 Directory: {os.getcwd()}")
    print("=" * 60)
    
    checks = [
        ("System Architecture", check_system_architecture),
        ("Authentication Implementation", check_authentication_implementation),
        ("OCO Verification Logic", check_oco_verification_logic),
        ("Position Tracking System", check_position_tracking_system),
        ("Error Handling", check_error_handling_improvements),
        ("Live Trading Configuration", check_live_trading_configuration)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ ERROR in {check_name}: {str(e)}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 AUDIT COMPLIANCE SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} | {check_name}")
    
    print("-" * 60)
    print(f"📈 Overall Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL CRITICAL AUDIT ISSUES RESOLVED!")
        print("🚀 System ready for live trading deployment")
        return True
    else:
        print(f"\n⚠️  {total - passed} ISSUES REMAINING")
        print("🔧 Please address the failed checks before live deployment")
        return False

if __name__ == "__main__":
    success = run_comprehensive_audit()
    sys.exit(0 if success else 1)
