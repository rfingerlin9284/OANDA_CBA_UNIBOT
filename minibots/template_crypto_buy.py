import sys
import json
import time
import os
from datetime import datetime
from random import uniform

def liveulate_crypto_price(pair):
    if "BTC" in pair:
        return round(uniform(45000, 50000), 2)
    elif "ETH" in pair:
        return round(uniform(2800, 3200), 2)
    else:  # SOL
        return round(uniform(180, 220), 2)

def execute_trade(mission_file):
    with open(mission_file, 'r') as f:
        mission = json.load(f)
    
    pair = mission["pair"]
    entry_price = liveulate_crypto_price(pair)
    
    print(f"[🎯 CRYPTO BUY] {pair} | Entry: ${entry_price} | TP: ${mission['take_profit']} | SL: ${mission['stop_loss']}")
    
    # Simulate trade execution
    for i in range(8):
        current_price = liveulate_crypto_price(pair)
        pnl_pct = ((current_price - entry_price) / entry_price) * 100
        
        print(f"[🚀] {pair} | Price: ${current_price} | P&L: {pnl_pct:.2f}%")
        
        # Check exit conditions
        if current_price >= mission["take_profit"]:
            result = {"status": "TP_HIT", "pnl_pct": pnl_pct, "exit_price": current_price}
            break
        elif current_price <= mission["stop_loss"]:
            result = {"status": "SL_HIT", "pnl_pct": pnl_pct, "exit_price": current_price}
            break
        
        time.sleep(3)
    else:
        result = {"status": "TIMEOUT", "pnl_pct": pnl_pct, "exit_price": current_price}
    
    # Log results
    mission["result"] = result
    mission["completed_at"] = str(datetime.utcnow())
    
    log_file = f"logs/completed_{mission['bot_id']}.json"
    with open(log_file, "w") as f:
        json.dump(mission, f, indent=2)
    
    print(f"[✅] {pair} COMPLETE | {result['status']} | P&L: {result['pnl_pct']:.2f}%")
    
    # Clean up mission file
    os.remove(mission_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_trade(sys.argv[1])
