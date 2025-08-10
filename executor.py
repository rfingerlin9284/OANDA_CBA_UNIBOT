"""
TRADE EXECUTOR - LIVE TRADING ONLY
REAL MONEY AT RISK - NO live_mode/PRACTICE MODE

Executes OCO trades on both OANDA and Coinbase
Hardcoded live credentials - no live_mode logic
"""

import time
import oandapyV20
import ccxt
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.endpoints.accounts import AccountDetails
from datetime import datetime
from typing import Dict, Optional, Union
import json

from credentials import WolfpackCredentials
from logger import log_trade, log_error


class TradeExecutor:
    """Execute trades with OCO logic - LIVE TRADING ONLY"""
    
    def __init__(self, platform: str):
        """
        Initialize executor for specific platform
        platform: 'OANDA' or 'COINBASE'
        """
        self.platform = platform.upper()
        self.creds = WolfpackCredentials()
        
        print(f"⚡ Initializing {self.platform} Trade Executor")
        print("🚨 LIVE TRADING MODE - REAL MONEY AT RISK!")
        
        if self.platform == "OANDA":
            self.api = oandapyV20.API(
                access_token=self.creds.OANDA_API_KEY,
                environment="live"  # LIVE TRADING ENVIRONMENT
            )
        elif self.platform == "COINBASE":
            self.exchange = ccxt.coinbase({
                'apiKey': self.creds.COINBASE_API_KEY,
                'secret': self.creds.COINBASE_SECRET,
                'password': self.creds.COINBASE_PASSPHRASE,
                'ssl': True,
                'live_mode': False,  # LIVE TRADING ONLY
                'urls': {
                    'api': 'https://api.coinbase.com',  # LIVE ENDPOINT
                }
            })
        
        print(f"✅ {self.platform} executor initialized for LIVE trading")
    
    def calculate_position_size(self, entry_price: float, sl_price: float, pair: str) -> float:
        """Calculate position size based on risk management"""
        try:
            # Get account balance
            if self.platform == "OANDA":
                request = AccountDetails(self.creds.OANDA_ACCOUNT_ID)
                response = self.api.request(request)
                balance = float(response['account']['balance'])
                
                # Calculate risk amount (1% of balance)
                risk_amount = balance * (self.creds.RISK_PER_TRADE / 100)
                
                # Calculate pip value and position size
                risk_pips = abs(entry_price - sl_price)
                position_size = risk_amount / risk_pips
                
                # OANDA uses units (not lots)
                return int(position_size)
                
            elif self.platform == "COINBASE":
                balance = self.exchange.fetch_balance()
                usd_balance = balance.get('USD', {}).get('free', 0)
                
                # Calculate risk amount (1% of USD balance)
                risk_amount = usd_balance * (self.creds.RISK_PER_TRADE / 100)
                
                # Calculate position size in base currency
                risk_points = abs(entry_price - sl_price)
                position_size = risk_amount / risk_points
                
                return round(position_size, 6)
                
        except Exception as e:
            log_error(f"Error calculating position size: {e}", "POSITION_CALC")
            return 0
    
    def execute_oanda_oco(self, pair: str, direction: str, entry: float, 
                         sl: float, tp: float, position_size: int) -> bool:
        """Execute OCO order on LIVE OANDA"""
        try:
            # Convert pair format (EUR/USD -> EUR_USD)
            instrument = pair.replace('/', '_')
            
            # Determine order side
            units = position_size if direction == "BUY" else -position_size
            
            # Create market order with SL and TP
            order_data = {
                "order": {
                    "type": "MARKET",
                    "instrument": instrument,
                    "units": str(units),
                    "stopLossOnFill": {
                        "price": str(round(sl, 5))
                    },
                    "takeProfitOnFill": {
                        "price": str(round(tp, 5))
                    }
                }
            }
            
            # Execute order
            request = OrderCreate(self.creds.OANDA_ACCOUNT_ID, data=order_data)
            response = self.api.request(request)
            
            if 'orderFillTransaction' in response:
                fill = response['orderFillTransaction']
                log_trade(
                    f"LIVE OANDA OCO executed: {direction} {units} {instrument} @ {fill['price']}", 
                    pair
                )
                print(f"✅ OANDA OCO order filled at {fill['price']}")
                return True
            else:
                log_error(f"OANDA order not filled: {response}", "OANDA_ORDER")
                return False
                
        except Exception as e:
            log_error(f"OANDA OCO execution failed: {e}", "OANDA_OCO")
            return False
    
    def execute_coinbase_oco(self, pair: str, direction: str, entry: float,
                           sl: float, tp: float, position_size: float) -> bool:
        """Execute OCO-like order on LIVE Coinbase"""
        try:
            # Coinbase doesn't have native OCO, so we'll place market order
            # and then set stop-loss and take-profit separately
            
            side = 'buy' if direction == "BUY" else 'sell'
            
            # Place market order
            order = self.exchange.create_market_order(
                symbol=pair,
                side=side,
                amount=position_size
            )
            
            if order['status'] == 'closed':  # Filled immediately
                fill_price = order['average']
                
                log_trade(
                    f"LIVE Coinbase market order executed: {direction} {position_size} {pair} @ ${fill_price}", 
                    pair
                )
                
                # Note: Coinbase Advanced Trade supports stop-loss orders
                # but implementation would require additional API calls
                # For now, we'll rely on external monitoring
                
                print(f"✅ Coinbase market order filled at ${fill_price}")
                print(f"⚠️  Manual OCO monitoring required (SL: ${sl}, TP: ${tp})")
                return True
            else:
                log_error(f"Coinbase order not filled: {order}", "COINBASE_ORDER")
                return False
                
        except Exception as e:
            log_error(f"Coinbase OCO execution failed: {e}", "COINBASE_OCO")
            return False
    
    def execute_oco_trade(self, pair: str, direction: str, entry: float,
                         sl: float, tp: float, confidence: float) -> bool:
        """
        Execute OCO trade based on platform
        LIVE TRADING ONLY - REAL MONEY AT RISK
        """
        try:
            print(f"\n⚡ EXECUTING LIVE OCO TRADE:")
            print(f"   Platform: {self.platform}")
            print(f"   Pair: {pair}")
            print(f"   Direction: {direction}")
            print(f"   Entry: {entry}")
            print(f"   SL: {sl}")
            print(f"   TP: {tp}")
            print(f"   Confidence: {confidence}")
            print("   🚨 REAL MONEY AT RISK!")
            
            # Calculate position size
            position_size = self.calculate_position_size(entry, sl, pair)
            
            if position_size <= 0:
                log_error("Position size calculation failed", "POSITION_SIZE")
                return False
            
            print(f"   Position Size: {position_size}")
            
            # Execute based on platform
            if self.platform == "OANDA":
                return self.execute_oanda_oco(pair, direction, entry, sl, tp, int(position_size))
            elif self.platform == "COINBASE":
                return self.execute_coinbase_oco(pair, direction, entry, sl, tp, position_size)
            else:
                log_error(f"Unknown platform: {self.platform}", "PLATFORM_ERROR")
                return False
                
        except Exception as e:
            log_error(f"OCO trade execution failed: {e}", "OCO_EXECUTION")
            return False
    
    def check_order_status(self, order_id: str) -> Dict:
        """Check status of executed order"""
        try:
            if self.platform == "OANDA":
                # Implementation for OANDA order status check
                pass
            elif self.platform == "COINBASE":
                # Implementation for Coinbase order status check
                pass
                
        except Exception as e:
            log_error(f"Error checking order status: {e}", "ORDER_STATUS")
            return {}
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel pending order"""
        try:
            if self.platform == "OANDA":
                # Implementation for OANDA order cancellation
                pass
            elif self.platform == "COINBASE":
                # Implementation for Coinbase order cancellation
                pass
                
        except Exception as e:
            log_error(f"Error cancelling order: {e}", "ORDER_CANCEL")
            return False


# === TESTING FUNCTIONS ===
def test_oanda_executor():
    """Test OANDA executor with live_mode trade"""
    print("🧪 Testing OANDA Executor...")
    
    executor = TradeExecutor("OANDA")
    
    # Test position size calculation
    position_size = executor.calculate_position_size(1.1000, 1.0980, "EUR/USD")
    print(f"Calculated position size: {position_size}")
    

def test_coinbase_executor():
    """Test Coinbase executor with live_mode trade"""
    print("🧪 Testing Coinbase Executor...")
    
    executor = TradeExecutor("COINBASE")
    
    # Test position size calculation
    position_size = executor.calculate_position_size(50000.0, 49000.0, "BTC/USD")
    print(f"Calculated position size: {position_size}")


if __name__ == "__main__":
    print("⚡ Trade Executor - LIVE TRADING ONLY")
    print("🚨 WARNING: This executes real money trades!")
    test_oanda_executor()
    test_coinbase_executor()
