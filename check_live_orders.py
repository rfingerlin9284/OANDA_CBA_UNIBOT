#!/usr/bin/env python3
"""
🔍 LIVE ORDER VERIFICATION SCRIPT
Constitutional PIN: 841921
Checks for live orders and OCO setups
"""

from credentials import OANDA_API_KEY, OANDA_ACCOUNT_ID
import requests
import json

def check_account_status():
    """Check OANDA account for live orders and trades"""
    headers = {'Authorization': f'Bearer {OANDA_API_KEY}'}
    
    # Account summary
    url = f'https://api-fxtrade.oanda.com/v3/accounts/{OANDA_ACCOUNT_ID}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            account = data['account']
            print(f'🏦 OANDA ACCOUNT STATUS:')
            print(f'   ├─ Balance: ${account["balance"]}')
            print(f'   ├─ Margin Used: ${account["marginUsed"]}')
            print(f'   ├─ Open Trades: {account["openTradeCount"]}')
            print(f'   ├─ Open Positions: {account["openPositionCount"]}')
            print(f'   └─ Pending Orders: {account["pendingOrderCount"]}')
            print()
            
            # Check for open trades
            if int(account["openTradeCount"]) > 0:
                trades_url = f'https://api-fxtrade.oanda.com/v3/accounts/{OANDA_ACCOUNT_ID}/trades'
                trades_response = requests.get(trades_url, headers=headers)
                if trades_response.status_code == 200:
                    trades_data = trades_response.json()
                    print(f'📊 LIVE TRADES ({len(trades_data["trades"])}):')
                    for trade in trades_data["trades"]:
                        print(f'   ├─ Trade ID: {trade["id"]}')
                        print(f'   ├─ Instrument: {trade["instrument"]}')
                        print(f'   ├─ Units: {trade["currentUnits"]}')
                        print(f'   ├─ Unrealized PL: ${trade["unrealizedPL"]}')
                        print(f'   └─ Open Time: {trade["openTime"]}')
                        print()
            
            # Check for pending orders
            if int(account["pendingOrderCount"]) > 0:
                orders_url = f'https://api-fxtrade.oanda.com/v3/accounts/{OANDA_ACCOUNT_ID}/orders'
                orders_response = requests.get(orders_url, headers=headers)
                if orders_response.status_code == 200:
                    orders_data = orders_response.json()
                    print(f'⏳ PENDING ORDERS ({len(orders_data["orders"])}):')
                    for order in orders_data["orders"]:
                        print(f'   ├─ Order ID: {order["id"]}')
                        print(f'   ├─ Type: {order["type"]}')
                        print(f'   ├─ Instrument: {order["instrument"]}')
                        print(f'   ├─ Units: {order["units"]}')
                        if "price" in order:
                            print(f'   ├─ Price: {order["price"]}')
                        print(f'   └─ Create Time: {order["createTime"]}')
                        print()
                        
                        # Check for OCO orders
                        if order["type"] in ["MARKET_IF_TOUCHED", "LIMIT", "STOP"]:
                            print(f'   🎯 POTENTIAL OCO ORDER DETECTED')
                            if "takeProfitOnFill" in order:
                                print(f'      ├─ Take Profit: {order["takeProfitOnFill"]["price"]}')
                            if "stopLossOnFill" in order:
                                print(f'      └─ Stop Loss: {order["stopLossOnFill"]["price"]}')
            
            # Summary
            if int(account["openTradeCount"]) == 0 and int(account["pendingOrderCount"]) == 0:
                print(f'📋 STATUS: NO LIVE ORDERS OR TRADES CURRENTLY ACTIVE')
                print(f'💡 System is streaming prices but not placing orders yet')
                
        else:
            print(f'❌ Failed to get account info: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error checking account: {e}')

if __name__ == "__main__":
    print(f'🔍 RBOTZILLA ELITE 18+18 - LIVE ORDER VERIFICATION')
    print(f'🔐 Constitutional PIN: 841921')
    print(f'═══════════════════════════════════════════════════')
    check_account_status()
