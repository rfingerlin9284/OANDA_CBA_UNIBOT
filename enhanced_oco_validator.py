#!/usr/bin/env python3
"""Enhanced OCO Validator with Real-Time P&L Monitoring"""
import json
import time
import os
from datetime import datetime
from oandapyV20 import API
from oandapyV20.endpoints.positions import OpenPositions
from oandapyV20.endpoints.orders import OrderList

def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except:
        pass
    return env_vars

def check_enhanced_oco_status():
    """Enhanced OCO status with profit/loss tracking"""
    env_vars = load_env()
    
    try:
        api = API(access_token=env_vars.get('OANDA_API_TOKEN'), environment='live')
        account_id = env_vars.get('OANDA_ACCOUNT_ID')
        
        print(f"\n📦 ENHANCED OCO STATUS SCAN: {time.strftime('%H:%M:%S')}")
        print("═" * 60)
        
        # Get positions
        positions_request = OpenPositions(accountID=account_id)
        api.request(positions_request)
        positions = positions_request.response.get('positions', [])
        
        # Get orders
        orders_request = OrderList(accountID=account_id)
        api.request(orders_request)
        orders = orders_request.response.get('orders', [])
        
        position_count = 0
        protected_count = 0
        total_unrealized = 0.0
        alerts = []
        
        for position in positions:
            instrument = position['instrument']
            long_units = float(position['long']['units'])
            short_units = float(position['short']['units'])
            
            if long_units != 0 or short_units != 0:
                position_count += 1
                unrealized_pnl = float(position['unrealizedPL'])
                total_unrealized += unrealized_pnl
                
                # Check for protective orders
                has_sl = any(o.get('instrument') == instrument and 'STOP_LOSS' in o.get('type', '') for o in orders)
                has_tp = any(o.get('instrument') == instrument and 'TAKE_PROFIT' in o.get('type', '') for o in orders)
                
                # Enhanced status with P&L analysis
                if has_sl and has_tp:
                    protected_count += 1
                    if unrealized_pnl > 0:
                        print(f"✅ [OCO SECURED] {instrument} | P&L: \033[92m${unrealized_pnl:>6.2f}\033[0m")
                    else:
                        print(f"✅ [OCO SECURED] {instrument} | P&L: \033[91m${unrealized_pnl:>6.2f}\033[0m")
                else:
                    protected_count += 0
                    print(f"🚨 [NAKED POSITION] {instrument} | P&L: \033[91m${unrealized_pnl:>6.2f}\033[0m")
                    alerts.append(f"❌ OCO Missing for {instrument}")
                    print(f"   Stop Loss: {'✅' if has_sl else '❌'}")
                    print(f"   Take Profit: {'✅' if has_tp else '❌'}")
                
                # Additional alerts for losing positions
                if unrealized_pnl < -10:  # Alert if losing more than $10
                    alerts.append(f"⚠️ Large loss on {instrument}: ${unrealized_pnl:.2f}")
        
        # Summary
        if position_count == 0:
            print("\033[94m[✅ NO OPEN POSITIONS]\033[0m")
        else:
            protection_rate = (protected_count / position_count) * 100
            color = '\033[92m' if total_unrealized > 0 else '\033[91m'
            print(f"\n📊 PORTFOLIO SUMMARY:")
            print(f"   Protection Rate: {protected_count}/{position_count} ({protection_rate:.1f}%)")
            print(f"   Total Unrealized: {color}${total_unrealized:.2f}\033[0m")
        
        print("═" * 60)
        
        # Return alerts for logging
        return alerts
        
    except Exception as e:
        error_msg = f"❌ OCO SCAN ERROR: {e}"
        print(error_msg)
        return [error_msg]

if __name__ == "__main__":
    while True:
        alerts = check_enhanced_oco_status()
        for alert in alerts:
            print(f"[ALERT] {alert}")
        
        # Log alerts to file
        if alerts:
            with open('logs/oco_alerts.log', 'a') as f:
                for alert in alerts:
                    f.write(f"{datetime.now()} - {alert}\n")
        
        time.sleep(60)  # Check every minute
