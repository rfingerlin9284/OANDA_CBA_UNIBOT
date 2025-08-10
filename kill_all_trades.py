#!/usr/bin/env python3
"""
Emergency Trade Killer - Close All Open Positions
PIN 841921 Authorization Required
"""

import os
import sys
import oandapyV20
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.trades as trades
from dotenv import load_dotenv

load_dotenv()

def emergency_close_all_trades():
    """Close all open trades immediately"""
    
    # Verify PIN
    if os.getenv("CONSTITUTIONAL_PIN") != "841921":
        print("❌ CONSTITUTIONAL PIN REQUIRED")
        return False
    
    api_key = os.getenv("OANDA_API_KEY")
    account_id = os.getenv("OANDA_ACCOUNT_ID")
    
    if not api_key or not account_id:
        print("❌ Missing OANDA credentials")
        return False
    
    client = oandapyV20.API(access_token=api_key, environment="live")
    
    try:
        print("🔥 EMERGENCY TRADE CLOSURE INITIATED")
        print("=" * 50)
        
        # Get all open trades
        r = trades.TradesList(account_id)
        response = client.request(r)
        open_trades = response.get('trades', [])
        
        if not open_trades:
            print("✅ No open trades found")
            return True
        
        print(f"📊 Found {len(open_trades)} open trades")
        
        # Close each trade
        for trade in open_trades:
            trade_id = trade['id']
            instrument = trade['instrument']
            units = trade['currentUnits']
            unrealized_pl = trade['unrealizedPL']
            
            print(f"🔥 Closing {instrument} | Units: {units} | P/L: {unrealized_pl}")
            
            try:
                # Close trade
                close_data = {"units": "ALL"}
                r = trades.TradeClose(account_id, trade_id, data=close_data)
                close_response = client.request(r)
                
                if 'orderFillTransaction' in close_response:
                    realized_pl = close_response['orderFillTransaction'].get('pl', '0')
                    print(f"✅ Closed {instrument} | Realized P/L: {realized_pl}")
                else:
                    print(f"⚠️ Close response for {instrument}: {close_response}")
                    
            except Exception as e:
                print(f"❌ Failed to close {instrument}: {e}")
        
        # Verify all trades closed
        r = trades.TradesList(account_id)
        response = client.request(r)
        remaining_trades = response.get('trades', [])
        
        if remaining_trades:
            print(f"⚠️ {len(remaining_trades)} trades still open")
            return False
        else:
            print("✅ ALL TRADES SUCCESSFULLY CLOSED")
            return True
            
    except Exception as e:
        print(f"❌ Emergency closure failed: {e}")
        return False

if __name__ == "__main__":
    print("🚨 EMERGENCY TRADE KILLER")
    print("This will close ALL open positions immediately!")
    
    confirm = input("Type 'KILL ALL TRADES' to confirm: ")
    if confirm == "KILL ALL TRADES":
        success = emergency_close_all_trades()
        if success:
            print("\n🎯 All trades killed successfully!")
        else:
            print("\n❌ Some trades may still be open - check manually")
    else:
        print("❌ Confirmation failed - no trades closed")
