import sys
import json
import time
import os
from datetime import datetime
from random import uniform

def liveulate_forex_price():
    return round(uniform(1.0800, 1.1200), 5)

def execute_trade(mission_file):
    with open(mission_file, 'r') as f:
        mission = json.load(f)
    
    pair = mission["pair"]
    entry_price = liveulate_forex_price()
    
    print(f"[🎯 FOREX SELL] {pair} | Entry: {entry_price} | TP: {mission['take_profit']} | SL: {mission['stop_loss']}")
    
    # Simulate trade execution for SELL
    for i in range(10):
        current_price = liveulate_forex_price()
        pnl = (entry_price - current_price) * 10000  # Pips for sell
        
        print(f"[📉] {pair} | Price: {current_price} | P&L: {pnl:.1f} pips")
        
        # Check exit conditions (reversed for sell)
        if current_price <= mission["take_profit"]:
            result = {"status": "TP_HIT", "pnl": pnl, "exit_price": current_price}
            break
        elif current_price >= mission["stop_loss"]:
            result = {"status": "SL_HIT", "pnl": pnl, "exit_price": current_price}
            break
        
        time.sleep(2)
    else:
        result = {"status": "TIMEOUT", "pnl": pnl, "exit_price": current_price}
    
    # Log results
    mission["result"] = result
    mission["completed_at"] = str(datetime.utcnow())
    
    log_file = f"logs/completed_{mission['bot_id']}.json"
    with open(log_file, "w") as f:
        json.dump(mission, f, indent=2)
    
    print(f"[✅] {pair} COMPLETE | {result['status']} | P&L: {result['pnl']:.1f} pips")
    
    # Clean up mission file
    os.remove(mission_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_trade(sys.argv[1])
