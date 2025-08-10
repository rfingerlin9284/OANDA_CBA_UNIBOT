import requests
import time
import os
from oandapyV20 import API
from oandapyV20.endpoints.positions import OpenPositions
from oandapyV20.endpoints.orders import OrderList

def color(text, c): 
    return f"\033[{c}m{text}\033[0m"

def check_oco_status():
    """Live OCO status verification with visual indicators"""
    try:
        # Load environment
        for line in open('.env'):
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
        
        api = API(access_token=os.environ['OANDA_API_TOKEN'], environment='live')
        account_id = os.environ['OANDA_ACCOUNT_ID']
        
        print("📦 OCO STATUS SCAN:", time.strftime("%H:%M:%S"))
        print("────────────────────────────────────────────")
        
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
        
        for position in positions:
            instrument = position['instrument']
            long_units = float(position['long']['units'])
            short_units = float(position['short']['units'])
            
            if long_units != 0 or short_units != 0:
                position_count += 1
                pnl = float(position['unrealizedPL'])
                
                # Check for protective orders
                has_sl = any(o.get('instrument') == instrument and 'STOP_LOSS' in o.get('type', '') for o in orders)
                has_tp = any(o.get('instrument') == instrument and 'TAKE_PROFIT' in o.get('type', '') for o in orders)
                
                if has_sl and has_tp:
                    protected_count += 1
                    print(color(f"[✅ OCO SECURED] {instrument} | P&L: ${pnl:.2f}", "92"))
                else:
                    print(color(f"[🚨 NAKED POSITION] {instrument} | P&L: ${pnl:.2f}", "91"))
                    print(f"   Stop Loss: {'✅' if has_sl else '❌'}")
                    print(f"   Take Profit: {'✅' if has_tp else '❌'}")
        
        if position_count == 0:
            print(color("[✅ NO OPEN POSITIONS]", "94"))
        else:
            protection_rate = (protected_count / position_count) * 100
            print(f"📊 PROTECTION RATE: {protected_count}/{position_count} ({protection_rate:.1f}%)")
        
        print("────────────────────────────────────────────")
        
    except Exception as e:
        print(color(f"❌ OCO SCAN ERROR: {e}", "91"))

if __name__ == "__main__":
    check_oco_status()
