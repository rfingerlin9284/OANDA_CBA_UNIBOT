import time
import os
from oandapyV20 import API
from oandapyV20.endpoints.positions import OpenPositions
from oandapyV20.endpoints.orders import OrderCreate

# Profit threshold for position rotation
ROTATION_THRESHOLD = 15.0  # $15 profit locks and rotates
PAIRS = ["GBP_JPY", "AUD_JPY", "EUR_USD", "USD_JPY", "EUR_GBP"]

def check_and_rotate(api, account_id):
    """
    Profit lock and reentry scanner for position optimization
    Locks profits at $15 threshold and rotates to next best pair
    """
    try:
        # Get open positions
        positions_request = OpenPositions(accountID=account_id)
        api.request(positions_request)
        positions = positions_request.response.get('positions', [])
        
        for position in positions:
            instrument = position['instrument']
            unrealized_pnl = float(position['unrealizedPL'])
            
            # Check if profit threshold reached
            if unrealized_pnl >= ROTATION_THRESHOLD:
                print(f"🔄 PROFIT LOCK TRIGGERED: ${unrealized_pnl:.2f} on {instrument}")
                
                # Close profitable position
                close_position(api, account_id, instrument)
                
                # Wait for closure
                time.sleep(2)
                
                # Find next rotation pair
                next_pair = get_next_rotation_pair(instrument)
                if next_pair:
                    print(f"🎯 ROTATING TO: {next_pair}")
                    # Trigger new signal analysis for rotation pair
                    
        return True
        
    except Exception as e:
        print(f"❌ ROTATION ERROR: {e}")
        return False

def close_position(api, account_id, instrument):
    """Close position by creating opposing market order"""
    try:
        # Get current position size
        positions_request = OpenPositions(accountID=account_id)
        api.request(positions_request)
        positions = positions_request.response.get('positions', [])
        
        for position in positions:
            if position['instrument'] == instrument:
                long_units = float(position['long']['units'])
                short_units = float(position['short']['units'])
                
                if long_units > 0:
                    # Close long position
                    close_units = -int(long_units)
                elif short_units > 0:
                    # Close short position  
                    close_units = int(abs(short_units))
                else:
                    continue
                
                # Create closing order
                data = {
                    "order": {
                        "instrument": instrument,
                        "units": str(close_units),
                        "type": "MARKET"
                    }
                }
                
                order_request = OrderCreate(accountID=account_id, data=data)
                api.request(order_request)
                print(f"✅ POSITION CLOSED: {instrument} ({close_units} units)")
                return True
                
    except Exception as e:
        print(f"❌ CLOSE POSITION ERROR: {e}")
        return False

def get_next_rotation_pair(current_pair):
    """Get next pair in rotation sequence"""
    try:
        current_index = PAIRS.index(current_pair)
        next_index = (current_index + 1) % len(PAIRS)
        return PAIRS[next_index]
    except:
        return PAIRS[0]  # Default to first pair
