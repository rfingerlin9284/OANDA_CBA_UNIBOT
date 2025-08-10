#!/usr/bin/env python3
"""
🧪 LIVE ORDER TEST - RBOTzilla Elite 18×18
Execute minimal risk test orders on OANDA and Coinbase
Constitutional PIN: 841921
"""

from executor import TradeExecutor
import sys
import os

def test_live_orders():
    """Execute minimal risk test orders"""
    print("🧪 LIVE ORDER EXECUTION TEST")
    print("=" * 50)
    print("🚨 WARNING: LIVE TRADING WITH REAL MONEY")
    print("📊 Testing minimal risk orders...")
    
    try:
        # Test OANDA - 1 unit EUR/USD (minimal risk ~$1)
        print("\n📈 OANDA Test: 1 unit EUR/USD")
        print("   Risk: ~$1.00 | SL: 10 pips | TP: 10 pips")
        
        oanda_executor = TradeExecutor("OANDA")
        oanda_result = oanda_executor.execute_oanda_oco(
            pair="EUR/USD",
            direction="BUY",
            entry=1.1000,     # Entry price 
            sl=1.0990,        # Stop loss: 10 pips
            tp=1.1010,        # Take profit: 10 pips
            position_size=1   # 1 unit = minimal risk
        )
        
        if oanda_result:
            print("✅ OANDA Order: EXECUTED")
        else:
            print("❌ OANDA Order: FAILED")
            
    except Exception as e:
        print(f"❌ OANDA Error: {e}")
    
    try:
        # Test Coinbase - 0.0001 BTC (~$5 risk)
        print("\n📈 Coinbase Test: 0.0001 BTC/USD")
        print("   Risk: ~$5.00 | SL: $500 | TP: $500")
        
        coinbase_executor = TradeExecutor("COINBASE")
        coinbase_result = coinbase_executor.execute_coinbase_oco(
            pair="BTC/USD",
            direction="BUY",
            entry=50000.0,    # Entry price
            sl=49500.0,       # Stop loss: $500
            tp=50500.0,       # Take profit: $500
            position_size=0.0001  # 0.0001 BTC = minimal risk
        )
        
        if coinbase_result:
            print("✅ Coinbase Order: EXECUTED")
        else:
            print("❌ Coinbase Order: FAILED")
            
    except Exception as e:
        print(f"❌ Coinbase Error: {e}")
    
    print("\n🎯 Test Orders Completed")
    print("📋 Check logs/clean_ml_stream.log for details")

if __name__ == "__main__":
    test_live_orders()
