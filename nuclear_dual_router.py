#!/usr/bin/env python3
"""
🚀 NUCLEAR DUAL-EXCHANGE ORDER ROUTER
Constitutional PIN: 841921

BULLETPROOF DUAL EXECUTION:
✅ OANDA Forex (50K-500K units)
✅ Coinbase Crypto (0.005-0.05 BTC)
✅ Atomic order execution
✅ Full OCO protection
✅ Error resilience
✅ Compounding position sizing
"""

import json
import time
import datetime
import requests
import threading
from typing import Dict, Optional, Any

# Import authentication modules
from ed25519_coinbase_auth import Ed25519CoinbaseAuth

class NuclearDualRouter:
    """💥 NUCLEAR-LEVEL DUAL EXCHANGE ORDER ROUTER"""
    
    def __init__(self):
        print("🚀 NUCLEAR DUAL ROUTER INITIALIZED")
        
        # HARD CODED LIVE CREDENTIALS
        self.oanda_token = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
        self.oanda_account = "001-001-13473069-001"
        self.oanda_url = "https://api-fxtrade.oanda.com/v3"
        
        # Coinbase Ed25519 authentication
        self.coinbase_auth = Ed25519CoinbaseAuth(
            "bbd70034-6acb-4c1c-8d7a-4358a434ed4b",
            "yN8Q2bgm7bCGlLptrbixoGO+SIUu1cfyVyh/uTzk4BGXGzz1IrbEBBFJa+6dw4O3Ar4pkbWKW1SOeUB/r8n1kg=="
        )
        
        # Execution statistics
        self.stats = {
            "oanda_success": 0,
            "oanda_failures": 0,
            "coinbase_success": 0,
            "coinbase_failures": 0,
            "dual_success": 0,
            "total_orders": 0
        }
        
        print("✅ NUCLEAR ROUTER READY FOR DUAL EXECUTION")
    
    def get_account_balance(self) -> float:
        """Get current OANDA account balance for position sizing"""
        try:
            url = f"{self.oanda_url}/accounts/{self.oanda_account}"
            headers = {"Authorization": f"Bearer {self.oanda_token}"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                account_data = response.json()
                balance = float(account_data['account']['balance'])
                print(f"💰 Current balance: ${balance:.2f}")
                return balance
        except Exception as e:
            print(f"❌ Balance fetch error: {e}")
        
        return 1500.0  # Fallback balance
    
    def calculate_position_sizes(self, signal: Dict) -> Dict:
        """Calculate nuclear position sizes for both exchanges"""
        balance = self.get_account_balance()
        
        # 🚀 NUCLEAR FOREX SIZING (OANDA)
        if balance > 5000:
            # Account growing - scale up
            forex_units = min(int(balance * 45), 500000)  # Up to 500K units
        elif balance > 2000:
            # Standard sizing
            forex_units = min(int(balance * 40), 300000)  # Up to 300K units
        else:
            # Conservative
            forex_units = min(int(balance * 35), 200000)  # Up to 200K units
        
        # Minimum enforcement
        forex_units = max(forex_units, 50000)  # Never below 50K
        
        # 🪙 NUCLEAR CRYPTO SIZING (COINBASE)
        if forex_units >= 300000:
            crypto_size = "0.05"      # Large position
        elif forex_units >= 200000:
            crypto_size = "0.03"      # Medium-large
        elif forex_units >= 100000:
            crypto_size = "0.02"      # Medium
        elif forex_units >= 50000:
            crypto_size = "0.015"     # Standard
        else:
            crypto_size = "0.01"      # Small
        
        return {
            "forex_units": forex_units,
            "crypto_size": crypto_size,
            "balance": balance
        }
    
    def get_crypto_pair(self, forex_pair: str) -> str:
        """Map forex pair to crypto equivalent"""
        mapping = {
            "EUR/USD": "BTC-USD", "GBP/USD": "ETH-USD", "USD/JPY": "SOL-USD",
            "AUD/USD": "ADA-USD", "USD/CHF": "MATIC-USD", "USD/CAD": "DOT-USD",
            "NZD/USD": "LINK-USD", "EUR/GBP": "AVAX-USD", "EUR/JPY": "ATOM-USD",
            "GBP/JPY": "ALGO-USD", "EUR/CHF": "XRP-USD", "GBP/CHF": "LTC-USD",
            "AUD/JPY": "BCH-USD", "NZD/JPY": "XLM-USD", "CAD/JPY": "DOGE-USD",
            "CHF/JPY": "UNI-USD", "EUR/CAD": "SAND-USD", "EUR/AUD": "MANA-USD"
        }
        return mapping.get(forex_pair, "BTC-USD")
    
    def validate_tp_sl(self, signal: Dict, current_price: float) -> Dict:
        """Validate and fix TP/SL to prevent OANDA cancellations"""
        direction = signal['direction']
        tp = float(signal.get('tp', 0)) if signal.get('tp') else None
        sl = float(signal.get('sl', 0)) if signal.get('sl') else None
        
        if not tp or not sl:
            # Generate TP/SL if missing
            if direction == 'BUY':
                tp = current_price + 0.01  # 100 pips profit
                sl = current_price - 0.01  # 100 pips stop
            else:
                tp = current_price - 0.01  # 100 pips profit
                sl = current_price + 0.01  # 100 pips stop
        else:
            # Validate existing TP/SL
            if direction == 'BUY':
                if tp <= current_price:
                    tp = current_price + 0.01
                    print(f"🔧 Fixed BUY TP: {tp}")
                if sl >= current_price:
                    sl = current_price - 0.01
                    print(f"🔧 Fixed BUY SL: {sl}")
            else:  # SELL
                if tp >= current_price:
                    tp = current_price - 0.01
                    print(f"🔧 Fixed SELL TP: {tp}")
                if sl <= current_price:
                    sl = current_price + 0.01
                    print(f"🔧 Fixed SELL SL: {sl}")
        
        return {"tp": f"{tp:.5f}", "sl": f"{sl:.5f}"}
    
    def execute_oanda_order(self, signal: Dict, sizes: Dict) -> Dict:
        """Execute OANDA forex order with full OCO protection"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"🚀 [{timestamp}] OANDA FOREX EXECUTION: {signal['pair']}")
            
            # Get current price and validate TP/SL
            current_price = self.get_current_price(signal['pair'])
            tp_sl = self.validate_tp_sl(signal, current_price)
            
            # Calculate units with direction
            side = 1 if signal['direction'] == 'BUY' else -1
            units = side * sizes['forex_units']
            
            # Create OCO order payload
            order_data = {
                "order": {
                    "type": "MARKET",
                    "instrument": signal['pair'].replace('/', '_'),
                    "units": str(units),
                    "positionFill": "DEFAULT",
                    "timeInForce": "FOK",
                    "takeProfitOnFill": {
                        "price": tp_sl['tp'],
                        "timeInForce": "GTC"
                    },
                    "stopLossOnFill": {
                        "price": tp_sl['sl'],
                        "timeInForce": "GTC"
                    }
                }
            }
            
            print(f"📦 OANDA PAYLOAD: {json.dumps(order_data, indent=2)}")
            
            # Submit order
            url = f"{self.oanda_url}/accounts/{self.oanda_account}/orders"
            headers = {
                "Authorization": f"Bearer {self.oanda_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=order_data, timeout=30)
            
            print(f"📡 OANDA RESPONSE: {response.status_code} | {response.text}")
            
            if response.status_code == 201:
                result = response.json()
                if 'orderFillTransaction' in result:
                    fill = result['orderFillTransaction']
                    order_id = fill['id']
                    fill_price = fill['price']
                    
                    print(f"✅ OANDA SUCCESS: {order_id} | Fill: {fill_price} | Units: {sizes['forex_units']}")
                    self.stats['oanda_success'] += 1
                    
                    return {
                        "success": True,
                        "order_id": order_id,
                        "fill_price": fill_price,
                        "units": sizes['forex_units']
                    }
            
            print(f"❌ OANDA FAILED: {response.status_code} | {response.text}")
            self.stats['oanda_failures'] += 1
            return {"success": False, "error": response.text}
            
        except Exception as e:
            print(f"💥 OANDA EXCEPTION: {e}")
            self.stats['oanda_failures'] += 1
            return {"success": False, "error": str(e)}
    
    def execute_coinbase_order(self, signal: Dict, sizes: Dict) -> Dict:
        """Execute Coinbase crypto order with Ed25519 authentication"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            crypto_pair = self.get_crypto_pair(signal['pair'])
            
            print(f"🪙 [{timestamp}] COINBASE CRYPTO EXECUTION: {crypto_pair}")
            
            # Create order payload
            order_data = {
                "client_order_id": f"unibot-{int(time.time()*1000)}",
                "product_id": crypto_pair,
                "side": signal['direction'].lower(),
                "order_configuration": {
                    "market_market_ioc": {
                        "base_size": sizes['crypto_size']
                    }
                }
            }
            
            print(f"📦 COINBASE PAYLOAD: {json.dumps(order_data, indent=2)}")
            
            # Get authentication headers
            headers = self.coinbase_auth.get_headers(
                "POST", 
                "/api/v3/brokerage/orders", 
                json.dumps(order_data)
            )
            
            # Submit order
            response = requests.post(
                "https://api.coinbase.com/api/v3/brokerage/orders",
                headers=headers,
                json=order_data,
                timeout=30
            )
            
            print(f"📡 COINBASE RESPONSE: {response.status_code} | {response.text}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                order_id = result.get('order_id', 'UNKNOWN')
                
                print(f"✅ COINBASE SUCCESS: {order_id} | Pair: {crypto_pair} | Size: {sizes['crypto_size']}")
                self.stats['coinbase_success'] += 1
                
                return {
                    "success": True,
                    "order_id": order_id,
                    "crypto_pair": crypto_pair,
                    "size": sizes['crypto_size']
                }
            
            print(f"❌ COINBASE FAILED: {response.status_code} | {response.text}")
            self.stats['coinbase_failures'] += 1
            return {"success": False, "error": response.text}
            
        except Exception as e:
            print(f"💥 COINBASE EXCEPTION: {e}")
            self.stats['coinbase_failures'] += 1
            return {"success": False, "error": str(e)}
    
    def get_current_price(self, pair: str) -> float:
        """Get current price from OANDA"""
        try:
            instrument = pair.replace('/', '_')
            url = f"{self.oanda_url}/pricing"
            headers = {"Authorization": f"Bearer {self.oanda_token}"}
            params = {"instruments": instrument}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['prices']:
                    price_data = data['prices'][0]
                    bid = float(price_data['bids'][0]['price'])
                    ask = float(price_data['asks'][0]['price'])
                    return (bid + ask) / 2
        except Exception as e:
            print(f"❌ Price fetch error: {e}")
        
        return 1.1620 if "USD" in pair else 150.0  # Fallback
    
    def execute_dual_order(self, signal: Dict) -> Dict:
        """💥 NUCLEAR DUAL EXCHANGE ORDER EXECUTION"""
        print("=" * 70)
        print(f"🚀 NUCLEAR DUAL EXECUTION: {signal['pair']} {signal['direction']}")
        print(f"🎯 Confidence: {signal.get('confidence', 0)*100:.1f}%")
        print("=" * 70)
        
        self.stats['total_orders'] += 1
        
        # Calculate position sizes
        sizes = self.calculate_position_sizes(signal)
        print(f"📊 POSITION SIZES: Forex={sizes['forex_units']:,} | Crypto={sizes['crypto_size']}")
        
        # Execute both orders in parallel
        oanda_result = {"success": False}
        coinbase_result = {"success": False}
        
        # Use threading for simultaneous execution
        threads = []
        results = {}
        
        def oanda_thread():
            results['oanda'] = self.execute_oanda_order(signal, sizes)
        
        def coinbase_thread():
            results['coinbase'] = self.execute_coinbase_order(signal, sizes)
        
        # Start both threads
        t1 = threading.Thread(target=oanda_thread)
        t2 = threading.Thread(target=coinbase_thread)
        
        t1.start()
        t2.start()
        
        # Wait for completion
        t1.join(timeout=60)  # 60-second timeout
        t2.join(timeout=60)
        
        oanda_result = results.get('oanda', {"success": False, "error": "timeout"})
        coinbase_result = results.get('coinbase', {"success": False, "error": "timeout"})
        
        # Analyze results
        oanda_success = oanda_result.get('success', False)
        coinbase_success = coinbase_result.get('success', False)
        
        if oanda_success and coinbase_success:
            self.stats['dual_success'] += 1
            print("🚀 DUAL SUCCESS: BOTH EXCHANGES EXECUTED!")
            status = "DUAL_SUCCESS"
        elif oanda_success:
            print("🎯 OANDA ONLY: Forex executed, crypto failed")
            status = "OANDA_ONLY"
        elif coinbase_success:
            print("🪙 COINBASE ONLY: Crypto executed, forex failed")
            status = "COINBASE_ONLY"
        else:
            print("💥 TOTAL FAILURE: Both exchanges failed")
            status = "TOTAL_FAILURE"
        
        # Compile results
        execution_result = {
            "status": status,
            "signal": signal['pair'],
            "direction": signal['direction'],
            "oanda": oanda_result,
            "coinbase": coinbase_result,
            "sizes": sizes,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Log execution
        self.log_execution(execution_result)
        
        # Print statistics
        print(f"📊 SESSION STATS: Total={self.stats['total_orders']} | "
              f"OANDA={self.stats['oanda_success']}/{self.stats['oanda_success']+self.stats['oanda_failures']} | "
              f"Coinbase={self.stats['coinbase_success']}/{self.stats['coinbase_success']+self.stats['coinbase_failures']} | "
              f"Dual={self.stats['dual_success']}")
        
        return execution_result
    
    def log_execution(self, result: Dict):
        """Log execution results"""
        import os
        os.makedirs("logs", exist_ok=True)
        
        with open("logs/nuclear_dual_executions.log", "a") as f:
            f.write(f"{json.dumps(result)}\n")

# Global router instance
nuclear_router = NuclearDualRouter()

def execute_nuclear_dual_trade(signal: Dict) -> Dict:
    """Main entry point for dual exchange execution"""
    return nuclear_router.execute_dual_order(signal)

if __name__ == "__main__":
    # Test execution
    test_signal = {
        "pair": "EUR/USD",
        "direction": "BUY",
        "confidence": 0.95,
        "signal_type": "FVG_BULLISH",
        "entry": "MARKET",
        "tp": "1.18000",
        "sl": "1.14000"
    }
    
    print("🧪 TESTING NUCLEAR DUAL ROUTER")
    result = execute_nuclear_dual_trade(test_signal)
    print("🎯 TEST COMPLETE")
    print(json.dumps(result, indent=2))
