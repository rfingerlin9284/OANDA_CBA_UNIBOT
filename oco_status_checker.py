#!/usr/bin/env python3
"""
🔍 OCO VERIFICATION TOOL
Constitutional PIN: 841921
Check existing OCO orders and protection status
"""

import requests
import json

# HARD CODED OANDA LIVE CREDENTIALS
OANDA_TOKEN = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
OANDA_ACCOUNT = "001-001-13473069-001"
OANDA_API = "https://api-fxtrade.oanda.com/v3"

def check_oco_status():
    """Check all trades and their OCO protection"""
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Get open trades
    trades_response = requests.get(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/trades", headers=headers)
    
    # Get pending orders
    orders_response = requests.get(f"{OANDA_API}/accounts/{OANDA_ACCOUNT}/orders", headers=headers)
    
    if trades_response.status_code == 200 and orders_response.status_code == 200:
        trades = trades_response.json().get('trades', [])
        orders = orders_response.json().get('orders', [])
        
        print("🔍 CURRENT OCO PROTECTION STATUS")
        print("=" * 50)
        
        for trade in trades:
            trade_id = trade['id']
            instrument = trade['instrument']
            units = float(trade['currentUnits'])
            price = float(trade['price'])
            unrealized_pl = float(trade['unrealizedPL'])
            
            print(f"\n📊 Trade {trade_id}: {instrument}")
            print(f"   Position: {units:,.0f} units @ {price:.5f}")
            print(f"   P/L: ${unrealized_pl:.2f}")
            
            # Find related TP/SL orders
            tp_orders = [o for o in orders if o.get('tradeID') == trade_id and o['type'] == 'TAKE_PROFIT']
            sl_orders = [o for o in orders if o.get('tradeID') == trade_id and o['type'] == 'STOP_LOSS']
            
            if tp_orders:
                tp_order = tp_orders[0]
                print(f"   ✅ Take Profit: {tp_order['price']} (Order {tp_order['id']})")
            else:
                print(f"   ❌ No Take Profit")
            
            if sl_orders:
                sl_order = sl_orders[0]
                print(f"   ✅ Stop Loss: {sl_order['price']} (Order {sl_order['id']})")
            else:
                print(f"   ❌ No Stop Loss")
            
            if tp_orders and sl_orders:
                print(f"   🛡️ FULL OCO PROTECTION ACTIVE")
            else:
                print(f"   ⚠️ PARTIAL OR NO PROTECTION")
        
        print(f"\n📋 SUMMARY:")
        print(f"   Open Trades: {len(trades)}")
        print(f"   Pending Orders: {len(orders)}")
        
    else:
        print(f"❌ API Error: Trades={trades_response.status_code}, Orders={orders_response.status_code}")

if __name__ == "__main__":
    check_oco_status()
