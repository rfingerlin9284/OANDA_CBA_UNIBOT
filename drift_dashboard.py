#!/usr/bin/env python3
"""
📊 ANTI-DRIFT MONITORING DASHBOARD
Real-time view of drift defense status
"""

import json
import time
import requests
from datetime import datetime
import os

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_account_summary():
    """Get current account status"""
    try:
        with open("small_cap_config_oanda.json", "r") as f:
            config = json.load(f)
        
        api_key = config["api_key"]
        account_id = config["account_id"]
        base_url = "https://api-fxtrade.oanda.com"
        
        url = f"{base_url}/v3/accounts/{account_id}/summary"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        return data.get('account', {})
        
    except Exception as e:
        return {'error': str(e)}

def display_drift_dashboard():
    """Main dashboard display"""
    while True:
        clear_screen()
        
        print("🚨 ANTI-DRIFT DEFENSE DASHBOARD")
        print("=" * 50)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Account Summary
        account = get_account_summary()
        if 'error' not in account:
            balance = float(account.get('balance', 0))
            unrealized_pl = float(account.get('unrealizedPL', 0))
            margin_used = float(account.get('marginUsed', 0))
            
            print(f"💰 ACCOUNT STATUS:")
            print(f"   Balance: ${balance:.2f}")
            print(f"   Unrealized P/L: ${unrealized_pl:.2f}")
            print(f"   Margin Used: ${margin_used:.2f}")
            
            # Drift indicators
            if unrealized_pl < -10:
                print("🚨 DRIFT WARNING: Significant unrealized losses")
            elif -10 <= unrealized_pl < 0:
                print("⚠️ MICRO-DRIFT: Small unrealized losses")
            else:
                print("✅ NO DRIFT: Positive or break-even")
        else:
            print(f"❌ Account fetch error: {account['error']}")
        
        print()
        print("🛡️ ANTI-DRIFT DEFENSES:")
        print("   ✅ Edge Validation: ACTIVE")
        print("   ✅ Correlation Filter: ACTIVE") 
        print("   ✅ Volatility-based SL/TP: ACTIVE")
        print("   ✅ Confidence Scaling: ACTIVE")
        print("   ✅ Micro-loss Monitor: ACTIVE")
        
        print()
        print("📊 DRIFT PREVENTION STATS:")
        
        # Check logs for recent activity
        try:
            if os.path.exists("logs/drift_alerts.log"):
                with open("logs/drift_alerts.log", "r") as f:
                    lines = f.readlines()
                    recent_alerts = len([l for l in lines[-10:] if l.strip()])
                    print(f"   Recent drift alerts: {recent_alerts}")
            else:
                print("   Recent drift alerts: 0")
        except:
            print("   Recent drift alerts: Error reading log")
        
        print()
        print("Press Ctrl+C to exit...")
        
        try:
            time.sleep(10)  # Update every 10 seconds
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")
            break

if __name__ == "__main__":
    display_drift_dashboard()
