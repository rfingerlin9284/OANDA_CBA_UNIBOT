#!/usr/bin/env python3
"""
LIVE Direct Position Manager - NO CACHE, LIVE API ONLY
Real-time position monitoring and management with OCO protection
"""
import os
import requests
import json
from datetime import datetime
from decimal import Decimal

class LivePositionManager:
    def __init__(self):
        # LIVE ENDPOINTS ONLY
        self.api_url = "https://api-fxtrade.oanda.com"
        self.stream_url = "https://stream-fxtrade.oanda.com"
        
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        
        if not self.api_key or not self.account_id:
            raise ValueError("LIVE credentials required")
            
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_live_account_summary(self):
        """DIRECT API - Account summary"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/summary"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['account']

    def get_live_positions(self):
        """DIRECT API - All positions"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/openPositions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['positions']

    def get_live_orders(self):
        """DIRECT API - All pending orders"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/pendingOrders"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['orders']

    def get_live_pricing(self, instruments):
        """DIRECT API - Real-time pricing"""
        if isinstance(instruments, str):
            instruments = [instruments]
        
        instruments_str = ','.join(instruments)
        url = f"{self.api_url}/v3/accounts/{self.account_id}/pricing"
        params = {'instruments': instruments_str}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()['prices']

    def place_oco_order(self, instrument, units, entry_price, tp_price, sl_price):
        """Place market order with OCO protection - LIVE API"""
        order_spec = {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": str(units),
                "timeInForce": "FOK",
                "takeProfitOnFill": {"price": str(tp_price)},
                "stopLossOnFill": {"price": str(sl_price)},
                "clientExtensions": {
                    "id": f"live-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    "comment": "LIVE_OCO_PROTECTED"
                }
            }
        }
        
        url = f"{self.api_url}/v3/accounts/{self.account_id}/orders"
        response = requests.post(url, headers=self.headers, json=order_spec)
        response.raise_for_status()
        return response.json()

    def update_stop_loss(self, trade_id, new_sl_price):
        """Update stop loss for existing trade - LIVE API"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/trades/{trade_id}/orders"
        
        order_spec = {
            "order": {
                "type": "STOP_LOSS",
                "tradeID": str(trade_id),
                "price": str(new_sl_price),
                "timeInForce": "GTC"
            }
        }
        
        response = requests.post(url, headers=self.headers, json=order_spec)
        response.raise_for_status()
        return response.json()

    def cancel_order(self, order_id):
        """Cancel order - LIVE API"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/orders/{order_id}/cancel"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def close_position(self, instrument, side="ALL"):
        """Close position - LIVE API"""
        url = f"{self.api_url}/v3/accounts/{self.account_id}/positions/{instrument}/close"
        
        if side == "ALL":
            data = {"longUnits": "ALL", "shortUnits": "ALL"}
        elif side == "LONG":
            data = {"longUnits": "ALL"}
        elif side == "SHORT": 
            data = {"shortUnits": "ALL"}
        else:
            raise ValueError("side must be ALL, LONG, or SHORT")
            
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def calculate_position_pnl(self, position, current_price):
        """Calculate real-time P&L in pips"""
        instrument = position['instrument']
        
        # Determine pip size
        pip_size = Decimal('0.01') if 'JPY' in instrument else Decimal('0.0001')
        
        total_pnl_pips = Decimal('0')
        
        # Long position P&L
        if Decimal(position['long']['units']) > 0:
            long_units = Decimal(position['long']['units'])
            avg_price = Decimal(position['long']['averagePrice'])
            current = Decimal(str(current_price['bid']))
            pnl_pips = (current - avg_price) / pip_size
            total_pnl_pips += pnl_pips
            
        # Short position P&L  
        if Decimal(position['short']['units']) < 0:
            short_units = abs(Decimal(position['short']['units']))
            avg_price = Decimal(position['short']['averagePrice'])
            current = Decimal(str(current_price['ask']))
            pnl_pips = (avg_price - current) / pip_size
            total_pnl_pips += pnl_pips
            
        return float(total_pnl_pips)

    def show_live_status(self):
        """Display real-time account status"""
        print("🔴 LIVE TRADING STATUS 🔴")
        print("=" * 50)
        
        # Account summary
        account = self.get_live_account_summary()
        print(f"Account ID: {account['id']}")
        print(f"Balance: ${account['balance']}")
        print(f"Unrealized P&L: ${account['unrealizedPL']}")
        print(f"Margin Used: ${account['marginUsed']}")
        print(f"Margin Available: ${account['marginAvailable']}")
        print()
        
        # Open positions
        positions = self.get_live_positions()
        if positions:
            print("📈 LIVE POSITIONS:")
            for pos in positions:
                instrument = pos['instrument']
                pricing = self.get_live_pricing(instrument)[0]
                pnl_pips = self.calculate_position_pnl(pos, pricing)
                
                long_units = pos['long']['units']
                short_units = pos['short']['units']
                
                if long_units != '0':
                    print(f"  {instrument} LONG: {long_units} units @ {pos['long']['averagePrice']}")
                if short_units != '0':
                    print(f"  {instrument} SHORT: {short_units} units @ {pos['short']['averagePrice']}")
                    
                print(f"    Current: {pricing['bid']}/{pricing['ask']} | P&L: {pnl_pips:+.1f} pips")
                print()
        else:
            print("📈 No open positions")
            
        # Pending orders
        orders = self.get_live_orders()
        if orders:
            print("📋 PENDING ORDERS:")
            for order in orders:
                print(f"  {order['id']}: {order['type']} {order['instrument']}")
                print(f"    Units: {order.get('units', 'N/A')} | Price: {order.get('price', 'N/A')}")
                print()
        else:
            print("📋 No pending orders")

def main():
    try:
        manager = LivePositionManager()
        manager.show_live_status()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
