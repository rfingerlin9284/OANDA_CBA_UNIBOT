import os
import json
import time
from oandapyV20 import API
from oandapyV20.endpoints.orders import OrderCreate, OrderList
from oandapyV20.endpoints.positions import OpenPositions

# Load credentials
with open(".env") as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v

account_id = os.environ["OANDA_ACCOUNT_ID"]
api = API(access_token=os.environ["OANDA_API_TOKEN"], environment="live")

def submit_order_with_oco_verification(instrument, units, entry_price, sl_price, tp_price):
    """
    🛡️ EMERGENCY OCO FIX - Submit order with mandatory SL/TP verification
    """
    order_data = {
        "order": {
            "instrument": instrument,
            "units": str(units),
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {
                "price": str(sl_price)
            },
            "takeProfitOnFill": {
                "price": str(tp_price)
            }
        }
    }

    print(f"\033[94m📤 SUBMITTING MARKET ORDER: {units} {instrument}")
    print(f"   💣 SL: {sl_price} | 🎯 TP: {tp_price}\033[0m")

    try:
        # Submit the order
        r = OrderCreate(accountID=account_id, data=order_data)
        api.request(r)
        order_response = r.response
        
        print("\033[92m✅ ORDER ACCEPTED - Verifying OCO placement...\033[0m")
        
        # Wait for OANDA to process
        time.sleep(2)
        
        # Verify OCO orders were actually created
        oco_verified = verify_oco_on_server(instrument)
        
        if oco_verified:
            print("\033[92m🛡️ OCO VERIFICATION PASSED - Position is protected!\033[0m")
            return True
        else:
            print("\033[91m🚨 OCO VERIFICATION FAILED - EMERGENCY ALERT!\033[0m")
            print("Position may be naked - manual intervention required!")
            return False
            
    except Exception as e:
        print(f"\033[91m❌ ORDER SUBMISSION FAILED: {str(e)}\033[0m")
        return False

def verify_oco_on_server(instrument):
    """
    Verify that SL and TP orders actually exist on OANDA server
    """
    try:
        # Get all pending orders
        orders_request = OrderList(accountID=account_id)
        api.request(orders_request)
        orders = orders_request.response.get('orders', [])
        
        has_sl = False
        has_tp = False
        
        for order in orders:
            if (order.get('instrument') == instrument and 
                order.get('state') == 'PENDING'):
                
                if 'STOP_LOSS' in order.get('type', ''):
                    has_sl = True
                    print(f"   ✅ Stop Loss confirmed: {order.get('price', 'N/A')}")
                    
                elif 'TAKE_PROFIT' in order.get('type', ''):
                    has_tp = True
                    print(f"   ✅ Take Profit confirmed: {order.get('price', 'N/A')}")
        
        return has_sl and has_tp
        
    except Exception as e:
        print(f"❌ OCO verification error: {e}")
        return False

def emergency_naked_position_scan():
    """
    🚨 Scan for any naked positions and alert immediately
    """
    try:
        print("\n🔍 EMERGENCY NAKED POSITION SCAN:")
        print("=" * 50)
        
        # Get open positions
        positions_request = OpenPositions(accountID=account_id)
        api.request(positions_request)
        positions = positions_request.response.get('positions', [])
        
        # Get pending orders
        orders_request = OrderList(accountID=account_id)
        api.request(orders_request)
        orders = orders_request.response.get('orders', [])
        
        naked_positions = 0
        total_positions = 0
        
        for position in positions:
            instrument = position['instrument']
            long_units = float(position['long']['units'])
            short_units = float(position['short']['units'])
            
            if long_units != 0 or short_units != 0:
                total_positions += 1
                pnl = float(position['unrealizedPL'])
                
                # Check for protective orders
                has_sl = any(o.get('instrument') == instrument and 'STOP_LOSS' in o.get('type', '') for o in orders)
                has_tp = any(o.get('instrument') == instrument and 'TAKE_PROFIT' in o.get('type', '') for o in orders)
                
                if has_sl and has_tp:
                    print(f"\033[92m✅ PROTECTED: {instrument} | P&L: ${pnl:.2f}\033[0m")
                else:
                    naked_positions += 1
                    print(f"\033[91m🚨 NAKED: {instrument} | P&L: ${pnl:.2f}\033[0m")
                    print(f"   Stop Loss: {'✅' if has_sl else '❌'}")
                    print(f"   Take Profit: {'✅' if has_tp else '❌'}")
        
        if naked_positions > 0:
            print(f"\n\033[91m🚨 CRITICAL: {naked_positions}/{total_positions} positions are NAKED!\033[0m")
        else:
            print(f"\n\033[92m✅ All {total_positions} positions are protected\033[0m")
            
        print("=" * 50)
        return naked_positions == 0
        
    except Exception as e:
        print(f"❌ Position scan error: {e}")
        return False

if __name__ == "__main__":
    # Run emergency scan
    emergency_naked_position_scan()
    
    # submit_order_with_oco_verification("EUR_USD", 100, 1.0850, 1.0800, 1.0900)
