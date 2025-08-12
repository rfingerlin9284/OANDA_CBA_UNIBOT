#!/usr/bin/env python3
"""
LIVE OANDA Position Consolidator - REAL MONEY ONLY
Consolidates multiple positions into single unified position with proper OCO protection
"""
import os
import sys
import json
import requests
from decimal import Decimal
from datetime import datetime

class LivePositionConsolidator:
    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID') 
        self.api_url = "https://api-fxtrade.oanda.com"  # LIVE ONLY
        
        if not self.api_key or not self.account_id:
            raise ValueError("LIVE credentials required: OANDA_API_KEY, OANDA_ACCOUNT_ID")
            
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_open_positions(self):
        """Get all open positions - DIRECT API CALL"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/openPositions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['positions']

    def get_pending_orders(self):
        """Get all pending orders - DIRECT API CALL"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/pendingOrders"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['orders']

    def cancel_order(self, order_id):
        """Cancel specific order - LIVE API"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/orders/{order_id}/cancel"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def close_position(self, instrument, side, units):
        """Close specific position - LIVE API"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/positions/{instrument}/close"
        data = {side: {"units": str(abs(units))}}
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def place_market_order(self, instrument, units, tp_price=None, sl_price=None):
        """Place new market order with OCO - LIVE API"""
        order_spec = {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": str(units),
                "timeInForce": "FOK"
            }
        }
        
        # Add OCO protection
        if tp_price:
            order_spec["order"]["takeProfitOnFill"] = {"price": str(tp_price)}
        if sl_price:
            order_spec["order"]["stopLossOnFill"] = {"price": str(sl_price)}
            
        url = f"{self.api_url}/v3/accounts/{self.account_id}/orders"
        response = requests.post(url, headers=self.headers, json=order_spec)
        response.raise_for_status()
        return response.json()

    def consolidate_positions(self, instrument, target_sl_price=None, target_tp_price=None):
        """
        Consolidate all positions for an instrument into single position
        with unified SL/TP around specified levels
        """
        print(f"🔄 Consolidating {instrument} positions...")
        
        # Get current positions
        positions = self.get_open_positions()
        target_positions = [p for p in positions if p['instrument'] == instrument]
        
        if not target_positions:
            print(f"❌ No open positions found for {instrument}")
            return
            
        # Calculate total exposure
        total_long = sum(Decimal(p['long']['units']) for p in target_positions if Decimal(p['long']['units']) > 0)
        total_short = sum(abs(Decimal(p['short']['units'])) for p in target_positions if Decimal(p['short']['units']) < 0)
        
        net_units = total_long - total_short
        
        print(f"📊 Current exposure: {total_long} long, {total_short} short")
        print(f"📊 Net position: {net_units} units")
        
        if net_units == 0:
            print("✅ Already flat - no consolidation needed")
            return
            
        # Cancel all existing OCO orders for this instrument
        print("🗑️  Canceling existing OCO orders...")
        pending_orders = self.get_pending_orders()
        for order in pending_orders:
            if order['instrument'] == instrument and order['type'] in ['TAKE_PROFIT', 'STOP_LOSS']:
                self.cancel_order(order['id'])
                print(f"   Canceled {order['type']} order {order['id']}")
        
        # Close all existing positions
        print("🔄 Closing existing positions...")
        for position in target_positions:
            if Decimal(position['long']['units']) > 0:
                self.close_position(instrument, 'longUnits', position['long']['units'])
                print(f"   Closed long position: {position['long']['units']} units")
            if Decimal(position['short']['units']) < 0:
                self.close_position(instrument, 'shortUnits', abs(Decimal(position['short']['units'])))
                print(f"   Closed short position: {abs(Decimal(position['short']['units']))} units")
        
        # Open new consolidated position with OCO
        if net_units != 0:
            print(f"🎯 Opening consolidated position: {net_units} units")
            result = self.place_market_order(
                instrument=instrument,
                units=int(net_units),
                tp_price=target_tp_price,
                sl_price=target_sl_price
            )
            
            trade_id = result.get('orderFillTransaction', {}).get('id')
            print(f"✅ Consolidated position opened - Trade ID: {trade_id}")
            
            if target_tp_price:
                print(f"   Take Profit: {target_tp_price}")
            if target_sl_price:
                print(f"   Stop Loss: {target_sl_price}")
        
        return {
            'instrument': instrument,
            'consolidated_units': int(net_units),
            'tp_price': target_tp_price,
            'sl_price': target_sl_price,
            'timestamp': datetime.utcnow().isoformat()
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: consolidate_positions.py INSTRUMENT [TP_PRICE] [SL_PRICE]")
        print("Example: consolidate_positions.py EUR_USD 1.1670 1.1595")
        sys.exit(1)
    
    instrument = sys.argv[1]
    tp_price = Decimal(sys.argv[2]) if len(sys.argv) > 2 else None
    sl_price = Decimal(sys.argv[3]) if len(sys.argv) > 3 else None
    
    try:
        consolidator = LivePositionConsolidator()
        result = consolidator.consolidate_positions(instrument, sl_price, tp_price)
        
        if result:
            print(f"\n🎉 Consolidation complete:")
            print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
