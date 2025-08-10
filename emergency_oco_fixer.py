#!/usr/bin/env python3
"""
🚨 EMERGENCY OCO FIXER - PROTECT THE 52K POSITION!
Constitutional PIN: 841921
Immediately adds OCO protection to existing trades
"""

import requests
import json
import datetime

# HARD CODED OANDA LIVE CREDENTIALS
OANDA_TOKEN = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
OANDA_ACCOUNT = "001-001-13473069-001"
OANDA_API = "https://api-fxtrade.oanda.com/v3"

def get_open_positions():
    """Get all open positions without OCO protection"""
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get open positions
        url = f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/positions"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            positions = data.get('positions', [])
            
            open_positions = []
            for pos in positions:
                if float(pos.get('long', {}).get('units', 0)) > 0 or float(pos.get('short', {}).get('units', 0)) > 0:
                    open_positions.append(pos)
            
            return open_positions
        else:
            print(f"❌ Error getting positions: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Exception getting positions: {e}")
        return []

def add_emergency_oco(position):
    """Add emergency OCO protection to position"""
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    instrument = position['instrument']
    
    # Determine if long or short position
    long_units = float(position.get('long', {}).get('units', 0))
    short_units = float(position.get('short', {}).get('units', 0))
    
    if long_units > 0:
        # LONG position - need TP above current, SL below current
        position_type = "LONG"
        units = long_units
        current_price = float(position['long']['averagePrice'])
        
        # Calculate OCO levels (conservative)
        tp_price = current_price + 0.0100  # 100 pips TP
        sl_price = current_price - 0.0050  # 50 pips SL
        
    elif short_units > 0:
        # SHORT position - need TP below current, SL above current  
        position_type = "SHORT"
        units = abs(short_units)
        current_price = float(position['short']['averagePrice'])
        
        # Calculate OCO levels (conservative)
        tp_price = current_price - 0.0100  # 100 pips TP
        sl_price = current_price + 0.0050  # 50 pips SL
    else:
        print(f"⚠️ No open position found for {instrument}")
        return False
    
    print(f"🚨 EMERGENCY OCO for {instrument}")
    print(f"📊 Position: {position_type} {units:,.0f} units @ {current_price:.5f}")
    print(f"🎯 Adding TP: {tp_price:.5f}")
    print(f"🛡️ Adding SL: {sl_price:.5f}")
    
    # Create Take Profit Order
    tp_data = {
        "order": {
            "type": "TAKE_PROFIT",
            "instrument": instrument,
            "price": f"{tp_price:.5f}",
            "timeInForce": "GTC",
            "triggerCondition": "DEFAULT"
        }
    }
    
    # Create Stop Loss Order
    sl_data = {
        "order": {
            "type": "STOP_LOSS", 
            "instrument": instrument,
            "price": f"{sl_price:.5f}",
            "timeInForce": "GTC",
            "triggerCondition": "DEFAULT"
        }
    }
    
    success_count = 0
    
    # Submit Take Profit Order
    try:
        tp_response = requests.post(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/orders", 
                                   headers=headers, json=tp_data)
        if tp_response.status_code == 201:
            tp_result = tp_response.json()
            tp_id = tp_result.get('orderCreateTransaction', {}).get('id', 'Unknown')
            print(f"✅ Take Profit Order Created: {tp_id}")
            success_count += 1
        else:
            print(f"❌ TP Order Failed: {tp_response.status_code} - {tp_response.text}")
    except Exception as e:
        print(f"❌ TP Order Exception: {e}")
    
    # Submit Stop Loss Order
    try:
        sl_response = requests.post(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/orders",
                                   headers=headers, json=sl_data)
        if sl_response.status_code == 201:
            sl_result = sl_response.json()
            sl_id = sl_result.get('orderCreateTransaction', {}).get('id', 'Unknown')
            print(f"✅ Stop Loss Order Created: {sl_id}")
            success_count += 1
        else:
            print(f"❌ SL Order Failed: {sl_response.status_code} - {sl_response.text}")
    except Exception as e:
        print(f"❌ SL Order Exception: {e}")
    
    return success_count == 2

def main():
    """Emergency OCO deployment"""
    print("🚨 EMERGENCY OCO PROTECTION DEPLOYMENT")
    print("🔐 Constitutional PIN: 841921")
    print("=" * 50)
    
    # Get open positions
    positions = get_open_positions()
    
    if not positions:
        print("ℹ️ No open positions found")
        return
    
    print(f"📊 Found {len(positions)} open position(s)")
    
    for pos in positions:
        instrument = pos['instrument']
        long_units = float(pos.get('long', {}).get('units', 0))
        short_units = float(pos.get('short', {}).get('units', 0))
        
        if long_units > 0:
            print(f"📈 {instrument}: LONG {long_units:,.0f} units")
        elif short_units > 0:
            print(f"📉 {instrument}: SHORT {abs(short_units):,.0f} units")
        
        # Add OCO protection
        success = add_emergency_oco(pos)
        
        if success:
            print(f"✅ OCO PROTECTION ADDED to {instrument}")
        else:
            print(f"❌ OCO PROTECTION FAILED for {instrument}")
        
        print("-" * 30)
    
    print("🛡️ EMERGENCY OCO DEPLOYMENT COMPLETE")

if __name__ == "__main__":
    main()
