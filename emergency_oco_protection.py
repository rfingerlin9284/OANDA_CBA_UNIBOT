#!/usr/bin/env python3
"""
🚨 EMERGENCY OCO PROTECTION FOR LIVE EUR/USD POSITION
Constitutional PIN: 841921

CRITICAL SITUATION:
- 2 units EUR/USD LONG position detected
- NO OCO protection in place
- LIVE MONEY AT RISK

This script creates immediate OCO protection:
- Take Profit: +50 pips (1.1687)
- Stop Loss: -30 pips (1.1607)
"""

import requests
import json
from datetime import datetime

def create_emergency_oco():
    """Create emergency OCO protection for EUR/USD position"""
    
    # Hardcoded live credentials
    API_KEY = 'bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48'
    ACCOUNT_ID = '001-001-13473069-001'
    BASE_URL = 'https://api-fxtrade.oanda.com'
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    print("🚨 EMERGENCY OCO PROTECTION SYSTEM")
    print("=" * 50)
    print("🔐 Constitutional PIN: 841921")
    print("🎯 Target: 2 units EUR/USD LONG position")
    print("=" * 50)
    
    # Get current price
    print("📊 Getting current EUR/USD price...")
    price_response = requests.get(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/pricing?instruments=EUR_USD',
        headers=headers
    )
    
    if price_response.status_code != 200:
        print(f"❌ Failed to get price: {price_response.text}")
        return False
    
    current_price = float(price_response.json()['prices'][0]['closeoutBid'])
    print(f"💰 Current EUR/USD price: {current_price}")
    
    # Calculate OCO levels
    take_profit_price = round(current_price + 0.0050, 4)  # +50 pips
    stop_loss_price = round(current_price - 0.0030, 4)    # -30 pips
    
    print(f"🎯 Take Profit: {take_profit_price} (+50 pips)")
    print(f"🛡️  Stop Loss: {stop_loss_price} (-30 pips)")
    
    # Create OCO order
    oco_order = {
        "order": {
            "type": "TAKE_PROFIT",
            "tradeID": "REPLACE_WITH_TRADE_ID",  # Need to get this
            "price": str(take_profit_price),
            "timeInForce": "GTC"
        }
    }
    
    # First, get the trade ID
    print("\n🔍 Getting trade ID...")
    trades_response = requests.get(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/trades',
        headers=headers
    )
    
    if trades_response.status_code != 200:
        print(f"❌ Failed to get trades: {trades_response.text}")
        return False
    
    trades = trades_response.json()['trades']
    eur_usd_trades = [t for t in trades if t['instrument'] == 'EUR_USD' and float(t['currentUnits']) > 0]
    
    if not eur_usd_trades:
        print("❌ No EUR/USD long trades found")
        return False
    
    trade_id = eur_usd_trades[0]['id']
    print(f"📋 Trade ID found: {trade_id}")
    
    # Create Take Profit order
    print("\n🎯 Creating Take Profit order...")
    tp_order = {
        "order": {
            "type": "TAKE_PROFIT",
            "tradeID": trade_id,
            "price": str(take_profit_price),
            "timeInForce": "GTC"
        }
    }
    
    tp_response = requests.post(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders',
        headers=headers,
        data=json.dumps(tp_order)
    )
    
    if tp_response.status_code == 201:
        tp_order_id = tp_response.json()['orderCreateTransaction']['id']
        print(f"✅ Take Profit order created: {tp_order_id}")
    else:
        print(f"❌ Take Profit order failed: {tp_response.text}")
        return False
    
    # Create Stop Loss order
    print("🛡️  Creating Stop Loss order...")
    sl_order = {
        "order": {
            "type": "STOP_LOSS",
            "tradeID": trade_id,
            "price": str(stop_loss_price),
            "timeInForce": "GTC"
        }
    }
    
    sl_response = requests.post(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders',
        headers=headers,
        data=json.dumps(sl_order)
    )
    
    if sl_response.status_code == 201:
        sl_order_id = sl_response.json()['orderCreateTransaction']['id']
        print(f"✅ Stop Loss order created: {sl_order_id}")
    else:
        print(f"❌ Stop Loss order failed: {sl_response.text}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 EMERGENCY OCO PROTECTION ACTIVATED")
    print(f"📊 Trade ID: {trade_id}")
    print(f"🎯 Take Profit: {take_profit_price} (Order: {tp_order_id})")
    print(f"🛡️  Stop Loss: {stop_loss_price} (Order: {sl_order_id})")
    print("💰 Position is now protected!")
    print("=" * 50)
    
    return True

def verify_protection():
    """Verify OCO protection is in place"""
    
    API_KEY = 'bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48'
    ACCOUNT_ID = '001-001-13473069-001'
    BASE_URL = 'https://api-fxtrade.oanda.com'
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 VERIFYING OCO PROTECTION...")
    
    # Check orders
    orders_response = requests.get(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders',
        headers=headers
    )
    
    if orders_response.status_code == 200:
        orders = orders_response.json()['orders']
        eur_usd_orders = [o for o in orders if 'EUR_USD' in str(o)]
        
        tp_orders = [o for o in orders if o.get('type') == 'TAKE_PROFIT']
        sl_orders = [o for o in orders if o.get('type') == 'STOP_LOSS']
        
        print(f"📊 Total pending orders: {len(orders)}")
        print(f"🎯 Take Profit orders: {len(tp_orders)}")
        print(f"🛡️  Stop Loss orders: {len(sl_orders)}")
        
        if tp_orders and sl_orders:
            print("✅ OCO PROTECTION CONFIRMED!")
            return True
        else:
            print("❌ OCO PROTECTION NOT COMPLETE")
            return False
    else:
        print(f"❌ Failed to verify orders: {orders_response.text}")
        return False

if __name__ == "__main__":
    print("🚨 EMERGENCY OCO PROTECTION DEPLOYMENT")
    print("🔐 Constitutional PIN: 841921")
    print("⚠️  LIVE MONEY PROTECTION SYSTEM")
    
    try:
        if create_emergency_oco():
            verify_protection()
        else:
            print("❌ OCO protection deployment failed")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("🚨 MANUAL INTERVENTION REQUIRED")
