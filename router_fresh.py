#!/usr/bin/env python3
"""
Fresh OANDA Router - Live Trading Only
Per deployment manual specifications
"""

import oandapyV20
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.accounts as accounts
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
import os
import json
from dotenv import load_dotenv

load_dotenv()

class OandaRouter:
    def __init__(self):
        """Initialize OANDA live connection"""
        from guardian_fresh import verify_live_mode
        verify_live_mode()
        
        self.api_key = os.getenv("OANDA_API_KEY")
        self.account_id = os.getenv("OANDA_ACCOUNT_ID")
        self.environment = os.getenv("OANDA_ENVIRONMENT", "live")
        
        # Live endpoint only
        self.client = oandapyV20.API(
            access_token=self.api_key,
            environment=self.environment
        )
        
        print(f"✅ OANDA Router initialized - LIVE MODE")
    
    def place_oco_order(self, pair, direction, units, entry_price, take_profit, stop_loss):
        """Place mandatory OCO order"""
        try:
            # Market order with OCO
            order_data = {
                "order": {
                    "type": "MARKET",
                    "instrument": pair,
                    "units": str(units) if direction == "BUY" else str(-units),
                    "takeProfitOnFill": {
                        "price": str(take_profit)
                    },
                    "stopLossOnFill": {
                        "price": str(stop_loss)
                    }
                }
            }
            
            r = orders.OrderCreate(accountID=self.account_id, data=order_data)
            response = self.client.request(r)
            
            print(f"✅ OCO Order placed: {pair} {direction} {units} units")
            return response
            
        except Exception as e:
            print(f"❌ OCO Order failed: {e}")
            return None
    
    def get_account_balance(self):
        """Get live account balance"""
        try:
            r = accounts.AccountDetails(accountID=self.account_id)
            response = self.client.request(r)
            balance = float(response['account']['balance'])
            return balance
        except Exception as e:
            print(f"❌ Balance check failed: {e}")
            return 0.0
    
    def get_open_positions(self):
        """Get current open positions"""
        try:
            r = positions.OpenPositions(accountID=self.account_id)
            response = self.client.request(r)
            return response['positions']
        except Exception as e:
            print(f"❌ Position check failed: {e}")
            return []

if __name__ == "__main__":
    router = OandaRouter()
    print(f"Account Balance: ${router.get_account_balance():.2f}")
    print(f"Open Positions: {len(router.get_open_positions())}")
