#!/usr/bin/env python3
"""
🚨 EMERGENCY OCO FIXER V2 - WITH TRADE ID LOOKUP
Constitutional PIN: 841921
Immediately adds OCO protection to existing trades using proper trade IDs
"""

import requests
import json
import datetime

# HARD CODED OANDA LIVE CREDENTIALS
OANDA_TOKEN = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
OANDA_ACCOUNT = "001-001-13473069-001"
OANDA_API = "https://api-fxtrade.oanda.com/v3"

def get_open_trades():
    """Get all open trades with trade IDs"""
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get open trades (not positions)
        url = f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/trades"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            trades = data.get('trades', [])
            print(f"📊 Found {len(trades)} open trade(s)")
            return trades
        else:
            print(f"❌ Error getting trades: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Exception getting trades: {e}")
        return []

def add_emergency_oco_to_trade(trade):
    """Add emergency OCO protection to specific trade using trade ID"""
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    trade_id = trade['id']
    instrument = trade['instrument']
    units = float(trade['currentUnits'])
    current_price = float(trade['price'])
    unrealized_pl = float(trade['unrealizedPL'])
    
    print(f"🚨 EMERGENCY OCO for Trade {trade_id}")
    print(f"📊 {instrument}: {units:,.0f} units @ {current_price:.5f}")
    print(f"💰 Unrealized P/L: ${unrealized_pl:.2f}")
    
    if units > 0:
        # LONG position
        tp_price = current_price + 0.0100  # 100 pips TP
        sl_price = current_price - 0.0050  # 50 pips SL
    else:
        # SHORT position
        tp_price = current_price - 0.0100  # 100 pips TP  
        sl_price = current_price + 0.0050  # 50 pips SL
    
    print(f"🎯 Adding TP: {tp_price:.5f}")
    print(f"🛡️ Adding SL: {sl_price:.5f}")
    
    # Create Take Profit Order with Trade ID
    tp_data = {
        "order": {
            "type": "TAKE_PROFIT",
            "tradeID": trade_id,
            "price": f"{tp_price:.5f}",
            "timeInForce": "GTC"
        }
    }
    
    # Create Stop Loss Order with Trade ID
    sl_data = {
        "order": {
            "type": "STOP_LOSS",
            "tradeID": trade_id, 
            "price": f"{sl_price:.5f}",
            "timeInForce": "GTC"
        }
    }
    
    success_count = 0
    
    # Submit Take Profit Order
    try:
        print("📤 Submitting Take Profit Order...")
        tp_response = requests.post(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/orders", 
                                   headers=headers, json=tp_data)
        print(f"📡 TP Response: {tp_response.status_code} - {tp_response.text}")
        
        if tp_response.status_code == 201:
            tp_result = tp_response.json()
            tp_id = tp_result.get('orderCreateTransaction', {}).get('id', 'Unknown')
            print(f"✅ Take Profit Order Created: {tp_id}")
            success_count += 1
        else:
            print(f"❌ TP Order Failed: {tp_response.status_code}")
    except Exception as e:
        print(f"❌ TP Order Exception: {e}")
    
    # Submit Stop Loss Order
    try:
        print("📤 Submitting Stop Loss Order...")
        sl_response = requests.post(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/orders",
                                   headers=headers, json=sl_data)
        print(f"📡 SL Response: {sl_response.status_code} - {sl_response.text}")
        
        if sl_response.status_code == 201:
            sl_result = sl_response.json()
            sl_id = sl_result.get('orderCreateTransaction', {}).get('id', 'Unknown')
            print(f"✅ Stop Loss Order Created: {sl_id}")
            success_count += 1
        else:
            print(f"❌ SL Order Failed: {sl_response.status_code}")
    except Exception as e:
        print(f"❌ SL Order Exception: {e}")
    
    return success_count == 2

def main():
    """Emergency OCO deployment with trade IDs"""
    print("🚨 EMERGENCY OCO PROTECTION DEPLOYMENT V2")
    print("🔐 Constitutional PIN: 841921")
    print("=" * 50)
    
    # Get open trades (not positions)
    trades = get_open_trades()
    
    if not trades:
        print("ℹ️ No open trades found")
        return
    
    for trade in trades:
        trade_id = trade['id']
        instrument = trade['instrument']
        units = float(trade['currentUnits'])
        
        if units > 0:
            print(f"📈 Trade {trade_id}: LONG {units:,.0f} units of {instrument}")
        else:
            print(f"📉 Trade {trade_id}: SHORT {abs(units):,.0f} units of {instrument}")
        
        # Add OCO protection
        success = add_emergency_oco_to_trade(trade)
        
        if success:
            print(f"✅ OCO PROTECTION ADDED to Trade {trade_id}")
        else:
            print(f"❌ OCO PROTECTION FAILED for Trade {trade_id}")
        
        print("-" * 50)
    
    print("🛡️ EMERGENCY OCO DEPLOYMENT COMPLETE")

if __name__ == "__main__":
    main()
