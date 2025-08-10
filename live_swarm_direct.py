#!/usr/bin/env python3
"""
🚀 RBOTZILLA LIVE SWARM - DIRECT LAUNCH
Constitutional PIN: 841921 | Battle Narration Active
"""
import time
import threading
from datetime import datetime
import json

# Import our battle narrator
from live_battle_narrator import *

def live_trading_loop():
    """Main live trading loop with battle narration"""
    # Boot sequence
    boot_sequence()
    
    active_orders = 0
    total_pnl = 0.0
    
    try:
        while True:
            # Market scanning phase
            scan_commentary(24, 3)  # 24 pairs, 3 signals found
            time.sleep(2)
            
            # ML prediction phase
            indicators = {
                'rsi': 28.3,
                'fvg_detected': True, 
                'fibonacci_level': 0.618
            }
            ml_commentary(indicators, 'BUY', 0.87)
            time.sleep(1)
            
            # Order execution liveulation
            order_commentary('BUY', 'EUR/USD', 1.0841, 1.0952, 1.0739, 'ord_8429F')
            active_orders += 1
            time.sleep(1)
            
            # OCO enforcement
            oco_commentary('ord_8429F')
            time.sleep(1)
            
            # MiniBot spawn
            minibot_commentary('423', 'ord_8429F')
            time.sleep(2)
            
            # Status updates
            total_pnl += 12.45  # Simulated P&L
            status_ping(active_orders, total_pnl)
            
            # Wait before next cycle
            time.sleep(10)
            
    except KeyboardInterrupt:
        print(f"\n{narrator._colorize('🛑 SWARM SHUTDOWN INITIATED', 'red')}")
        print(f"{narrator._colorize('📊 Final Status: Orders = ' + str(active_orders) + f' | P&L = +${total_pnl:.2f}', 'cyan')}")
        print(f"{narrator._colorize('🫡 Mission complete, Commander. RBOTzilla standing down.', 'yellow')}")

if __name__ == "__main__":
    import sys
    
    # Check for constitutional PIN
    if "--constitutional-pin" in sys.argv:
        pin_index = sys.argv.index("--constitutional-pin") + 1
        if pin_index < len(sys.argv) and sys.argv[pin_index] == "841921":
            print(f"\n{narrator._colorize('🔐 CONSTITUTIONAL PIN VERIFIED: 841921', 'green')}")
            print(f"{narrator._colorize('🔥 RBOTZILLA LIVE SWARM ACTIVATION COMMENCING...', 'bold')}")
            time.sleep(1)
            live_trading_loop()
        else:
            print("❌ INVALID CONSTITUTIONAL PIN")
            sys.exit(1)
    else:
        print("❌ CONSTITUTIONAL PIN REQUIRED FOR LIVE MODE")
        sys.exit(1)
