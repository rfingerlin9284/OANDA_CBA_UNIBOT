#!/usr/bin/env python3
"""
CRITICAL STOP LOSS FIX - Emergency Order Submission Patch
This module ensures OCO orders are properly submitted to OANDA
"""

from oandapyV20.endpoints.orders import OrderCreate, OrderCancel, OrderList
from oandapyV20.endpoints.positions import OpenPositions
import time
import json

def place_order_with_oco(api, account_id, instrument, units, sl_price, tp_price):
    """
    Place market order with mandatory OCO (Stop Loss + Take Profit)
    Verifies OCO attachment and fails gracefully if not confirmed
    """
    
    # Build order with OCO
    data = {
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
    
    print(f"🔧 SUBMITTING OCO ORDER: {instrument} | Units: {units} | SL: {sl_price} | TP: {tp_price}")
    
    try:
        # Submit order
        order_request = OrderCreate(accountID=account_id, data=data)
        response = api.request(order_request)
        
        # Extract transaction details
        if 'orderCreateTransaction' in response:
            order_id = response['orderCreateTransaction']['id']
            print(f"✅ ORDER ACCEPTED: Transaction ID {order_id}")
            
            # Verify OCO orders were created
            time.sleep(1)  # Allow OANDA to process
            oco_verified = verify_oco_orders(api, account_id, instrument)
            
            if oco_verified:
                print(f"✅ OCO VERIFIED: Stop Loss and Take Profit orders confirmed for {instrument}")
                return True
            else:
                print(f"❌ OCO VERIFICATION FAILED: No SL/TP orders found for {instrument}")
                print("🚨 CRITICAL: Position opened without protection!")
                return False
                
        else:
            print(f"❌ ORDER RESPONSE INVALID: {response}")
            return False
            
    except Exception as e:
        print(f"❌ ORDER SUBMISSION FAILED: {str(e)}")
        print(f"   Instrument: {instrument}")
        print(f"   Units: {units}")
        print(f"   SL: {sl_price}")
        print(f"   TP: {tp_price}")
        return False

def verify_oco_orders(api, account_id, instrument):
    """
    Verify that both Stop Loss and Take Profit orders exist for the instrument
    """
    try:
        # Get pending orders
        orders_request = OrderList(accountID=account_id)
        api.request(orders_request)
        orders = orders_request.response.get('orders', [])
        
        has_stop_loss = False
        has_take_profit = False
        
        for order in orders:
            if order.get('instrument') == instrument and order.get('state') == 'PENDING':
                if order.get('type') == 'STOP_LOSS':
                    has_stop_loss = True
                    print(f"   ✅ Stop Loss found: {order['stopLossOnFill']['price'] if 'stopLossOnFill' in order else 'N/A'}")
                elif order.get('type') == 'TAKE_PROFIT':
                    has_take_profit = True
                    print(f"   ✅ Take Profit found: {order['takeProfitOnFill']['price'] if 'takeProfitOnFill' in order else 'N/A'}")
        
        return has_stop_loss and has_take_profit
        
    except Exception as e:
        print(f"❌ OCO VERIFICATION ERROR: {e}")
        return False

def emergency_position_scan(api, account_id):
    """
    Scan for naked positions (positions without stop loss/take profit)
    """
    try:
        # Get open positions
        positions_request = OpenPositions(accountID=account_id)
        api.request(positions_request)
        positions = positions_request.response.get('positions', [])
        
        # Get pending orders
        orders_request = OrderList(accountID=account_id)
        api.request(orders_request)
        orders = orders_request.response.get('orders', [])
        
        print("🔍 EMERGENCY POSITION SCAN:")
        print("=" * 50)
        
        for position in positions:
            instrument = position['instrument']
            long_units = float(position['long']['units'])
            short_units = float(position['short']['units'])
            
            if long_units != 0 or short_units != 0:
                # Check for protective orders
                has_sl = any(o['instrument'] == instrument and o['type'] == 'STOP_LOSS' for o in orders)
                has_tp = any(o['instrument'] == instrument and o['type'] == 'TAKE_PROFIT' for o in orders)
                
                pnl = float(position['unrealizedPL'])
                
                if has_sl and has_tp:
                    print(f"✅ {instrument}: PROTECTED (SL + TP) | P&L: ${pnl:.2f}")
                else:
                    print(f"🚨 {instrument}: NAKED POSITION | P&L: ${pnl:.2f}")
                    print(f"   Stop Loss: {'✅' if has_sl else '❌'}")
                    print(f"   Take Profit: {'✅' if has_tp else '❌'}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ POSITION SCAN ERROR: {e}")

if __name__ == "__main__":
    # Test the emergency scan
    import os
    from oandapyV20 import API
    
    # Load environment
    for line in open('.env'):
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value
    
    api = API(access_token=os.environ['OANDA_API_TOKEN'], environment='live')
    emergency_position_scan(api, os.environ['OANDA_ACCOUNT_ID'])
