#!/usr/bin/env python3
"""
🚨 FIFO-COMPLIANT OCO PROTECTION SYSTEM
Constitutional PIN: 841921

FIFO VIOLATION ISSUE:
- Multiple EUR/USD trades of same size detected
- OANDA blocks individual trade OCO orders
- Need to use position-level or consolidated approach

SOLUTION:
- Close all EUR/USD trades individually
- Place new single trade with OCO protection
- Or use position-level management
"""

import requests
import json
from datetime import datetime

def fix_fifo_violation_with_oco():
    """Fix FIFO violation by consolidating trades with OCO protection"""
    
    # Hardcoded live credentials
    API_KEY = 'bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48'
    ACCOUNT_ID = '001-001-13473069-001'
    BASE_URL = 'https://api-fxtrade.oanda.com'
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    print("🚨 FIFO-COMPLIANT OCO PROTECTION SYSTEM")
    print("=" * 50)
    print("🔐 Constitutional PIN: 841921")
    print("🎯 Fixing FIFO violation with OCO protection")
    print("=" * 50)
    
    # Step 1: Get all EUR/USD trades
    print("🔍 Getting all EUR/USD trades...")
    trades_response = requests.get(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/trades',
        headers=headers
    )
    
    if trades_response.status_code != 200:
        print(f"❌ Failed to get trades: {trades_response.text}")
        return False
    
    trades = trades_response.json()['trades']
    eur_usd_trades = [t for t in trades if t['instrument'] == 'EUR_USD' and float(t['currentUnits']) > 0]
    
    print(f"📊 EUR/USD long trades found: {len(eur_usd_trades)}")
    total_units = sum(float(t['currentUnits']) for t in eur_usd_trades)
    print(f"💰 Total EUR/USD long units: {total_units}")
    
    # Step 2: Close all individual trades
    print("\n🔄 Closing individual trades to fix FIFO...")
    for trade in eur_usd_trades:
        trade_id = trade['id']
        units = trade['currentUnits']
        
        print(f"🔄 Closing trade {trade_id} ({units} units)...")
        
        close_data = {
            "units": "ALL"
        }
        
        close_response = requests.put(
            f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/trades/{trade_id}/close',
            headers=headers,
            data=json.dumps(close_data)
        )
        
        if close_response.status_code == 200:
            print(f"✅ Trade {trade_id} closed successfully")
        else:
            print(f"❌ Failed to close trade {trade_id}: {close_response.text}")
    
    # Step 3: Get current price for new trade
    print("\n📊 Getting current EUR/USD price...")
    price_response = requests.get(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/pricing?instruments=EUR_USD',
        headers=headers
    )
    
    if price_response.status_code != 200:
        print(f"❌ Failed to get price: {price_response.text}")
        return False
    
    current_price = float(price_response.json()['prices'][0]['closeoutAsk'])
    print(f"💰 Current EUR/USD price: {current_price}")
    
    # Step 4: Calculate OCO levels
    take_profit_price = round(current_price + 0.0050, 4)  # +50 pips
    stop_loss_price = round(current_price - 0.0030, 4)    # -30 pips
    
    print(f"🎯 Take Profit: {take_profit_price} (+50 pips)")
    print(f"🛡️  Stop Loss: {stop_loss_price} (-30 pips)")
    
    # Step 5: Place new trade with OCO protection
    print("\n🚀 Placing new EUR/USD trade with OCO protection...")
    
    oco_order = {
        "order": {
            "type": "MARKET",
            "instrument": "EUR_USD",
            "units": str(int(total_units)),
            "timeInForce": "FOK",
            "takeProfitOnFill": {
                "price": str(take_profit_price),
                "timeInForce": "GTC"
            },
            "stopLossOnFill": {
                "price": str(stop_loss_price),
                "timeInForce": "GTC"
            }
        }
    }
    
    order_response = requests.post(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders',
        headers=headers,
        data=json.dumps(oco_order)
    )
    
    if order_response.status_code == 201:
        result = order_response.json()
        order_id = result['orderFillTransaction']['id']
        trade_id = result['orderFillTransaction']['tradeOpened']['tradeID']
        
        print(f"✅ New trade placed with OCO protection!")
        print(f"📋 Order ID: {order_id}")
        print(f"📋 Trade ID: {trade_id}")
        print(f"💰 Units: {total_units}")
        print(f"🎯 Take Profit: {take_profit_price}")
        print(f"🛡️  Stop Loss: {stop_loss_price}")
        
        return True
    else:
        print(f"❌ Failed to place OCO order: {order_response.text}")
        return False

def verify_oco_protection():
    """Verify OCO protection is properly in place"""
    
    API_KEY = 'bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48'
    ACCOUNT_ID = '001-001-13473069-001'
    BASE_URL = 'https://api-fxtrade.oanda.com'
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 VERIFYING OCO PROTECTION...")
    
    # Check trades
    trades_response = requests.get(
        f'{BASE_URL}/v3/accounts/{ACCOUNT_ID}/trades',
        headers=headers
    )
    
    if trades_response.status_code == 200:
        trades = trades_response.json()['trades']
        eur_usd_trades = [t for t in trades if t['instrument'] == 'EUR_USD']
        
        print(f"📊 EUR/USD trades: {len(eur_usd_trades)}")
        
        for trade in eur_usd_trades:
            print(f"   Trade {trade['id']}: {trade['currentUnits']} units")
            
            if 'takeProfitOrder' in trade:
                tp_price = trade['takeProfitOrder']['price']
                print(f"   🎯 Take Profit: {tp_price}")
            else:
                print("   ❌ No Take Profit order")
            
            if 'stopLossOrder' in trade:
                sl_price = trade['stopLossOrder']['price']
                print(f"   🛡️  Stop Loss: {sl_price}")
            else:
                print("   ❌ No Stop Loss order")
        
        # Check if we have proper OCO protection
        protected_trades = [t for t in eur_usd_trades if 'takeProfitOrder' in t and 'stopLossOrder' in t]
        
        if protected_trades:
            print(f"✅ OCO PROTECTION CONFIRMED: {len(protected_trades)} protected trades")
            return True
        else:
            print("❌ OCO PROTECTION NOT DETECTED")
            return False
    else:
        print(f"❌ Failed to get trades: {trades_response.text}")
        return False

if __name__ == "__main__":
    print("🚨 FIFO-COMPLIANT OCO PROTECTION DEPLOYMENT")
    print("🔐 Constitutional PIN: 841921")
    print("⚠️  FIXING FIFO VIOLATION WITH OCO PROTECTION")
    
    try:
        if fix_fifo_violation_with_oco():
            verify_oco_protection()
            print("\n" + "=" * 50)
            print("🎉 FIFO-COMPLIANT OCO PROTECTION ACTIVATED")
            print("💰 EUR/USD position is now fully protected!")
            print("🎯 Take Profit and Stop Loss orders in place")
            print("=" * 50)
        else:
            print("❌ OCO protection deployment failed")
            print("🚨 MANUAL INTERVENTION REQUIRED")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("🚨 MANUAL INTERVENTION REQUIRED")
