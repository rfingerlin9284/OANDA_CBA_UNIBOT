#!/usr/bin/env python3
"""
🔥 RBOTZILLA ELITE 18+18 - LIVE IGNITION SYSTEM
Constitutional PIN: 841921
Human-Algo Synergy: Market Chaos → Dominance
"""

import os
import json
import time
import logging
from datetime import datetime
import subprocess
import sys

# Import credentials and API
from credentials import WolfpackCredentials
import oandapyV20
from oandapyV20.endpoints.accounts import AccountSummary
from oandapyV20.endpoints.pricing import PricingStream

class RBOTzillaIgnitionSystem:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.credentials = WolfpackCredentials()
        
        # Setup logging
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/ignition_system.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.display_banner()
        
    def display_banner(self):
        """Display RBOTzilla Elite 18+18 banner"""
        print("=" * 80)
        print("🔥 RBOTZILLA ELITE 18+18 - IGNITION SYSTEM")
        print("=" * 80)
        print(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        print("🎯 Architecture: Dual-Model Elite Squad (18 Forex + 18 Crypto)")
        print("🧠 Human-Algo Synergy: Quantifying crowd psychology in real-time")
        print("💥 Mission: Turn market chaos into trading dominance")
        print("=" * 80)
        
    def verify_neural_links(self):
        """Quick verification of all neural connections"""
        print("\n🧠 VERIFYING NEURAL LINKS...")
        
        status = {
            "oanda_api": False,
            "oanda_stream": False,
            "account_health": False,
            "system_ready": False
        }
        
        try:
            # Test Oanda API
            api = oandapyV20.API(
                access_token=self.credentials.OANDA_API_KEY,
                environment="live"
            )
            
            request = AccountSummary(self.credentials.OANDA_ACCOUNT_ID)
            response = api.request(request)
            
            balance = float(response['account']['balance'])
            open_trades = int(response['account']['openTradeCount'])
            
            print(f"✅ OANDA API: CONNECTED (Balance: ${balance:.2f})")
            status["oanda_api"] = True
            
            print("📡 Testing real-time stream...")
            params = {"instruments": "EUR_USD"}
            pricing = PricingStream(self.credentials.OANDA_ACCOUNT_ID, params=params)
            
            start_time = time.time()
            for tick in api.request(pricing):
                    break
                if tick['type'] == 'PRICE':
                    print("✅ LIVE STREAM: DATA FLOWING")
                    status["oanda_stream"] = True
                    break
            
            # Account health check
            if balance > 100:  # Minimum balance threshold
                print(f"✅ ACCOUNT HEALTH: SUFFICIENT CAPITAL (${balance:.2f})")
                status["account_health"] = True
            else:
                print(f"⚠️ ACCOUNT HEALTH: LOW BALANCE (${balance:.2f})")
            
            status["system_ready"] = all([
                status["oanda_api"],
                status["oanda_stream"],
                status["account_health"]
            ])
            
            return status
            
        except Exception as e:
            print(f"❌ NEURAL LINK FAILURE: {e}")
            logging.error(f"Neural link verification failed: {e}")
            return status
    
    def display_elite_squad_config(self):
        """Display Elite 18+18 configuration"""
        print("\n🏆 ELITE 18+18 SQUAD CONFIGURATION:")
        print("-" * 50)
        
        forex_pairs = [
            "EUR_USD", "USD_JPY", "GBP_USD", "USD_CHF", "AUD_USD", "NZD_USD",
            "EUR_JPY", "GBP_JPY", "EUR_GBP", "USD_CAD", "EUR_CHF", "AUD_JPY", 
            "CHF_JPY", "GBP_CHF", "NZD_JPY", "CAD_JPY", "EUR_AUD", "GBP_AUD"
        ]
        
        crypto_pairs = [
            "BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD", "XRP-USD", "ADA-USD",
            "AVAX-USD", "LINK-USD", "MATIC-USD", "DOT-USD", "LTC-USD", "APT-USD",
            "BCH-USD", "UNI-USD", "OP-USD", "NEAR-USD", "INJ-USD", "XLM-USD"
        ]
        
        print("📈 FOREX ELITE SQUAD (18 pairs):")
        for i, pair in enumerate(forex_pairs, 1):
            print(f"   {i:2d}. {pair}")
        
        print("\n💰 CRYPTO ELITE SQUAD (18 pairs):")
        for i, pair in enumerate(crypto_pairs, 1):
            print(f"   {i:2d}. {pair}")
        
        print(f"\n🎯 TOTAL COVERAGE: {len(forex_pairs) + len(crypto_pairs)} pairs")
        print("🚀 ARCHITECTURE: Dual-Model Specialized Neural Networks")
    
    def launch_live_system(self):
        """Launch the live RBOTzilla Elite 18+18 system"""
        print("\n🚀 LAUNCHING LIVE SYSTEM...")
        
        # Verify neural links first
        status = self.verify_neural_links()
        
        if not status["system_ready"]:
            print("❌ LAUNCH ABORTED: Neural links not ready")
            print("🔧 Fix connection issues and retry")
            return False
        
        print("\n✅ ALL SYSTEMS GO - LAUNCHING RBOTZILLA ELITE 18+18")
        
        # Create launch command
        launch_commands = [
            "python3 main.py &",
            "python3 dashboard_toggle_controller.py &", 
            "python3 auto_monitor_system.py &"
        ]
        
        print("🔥 IGNITION SEQUENCE:")
        for i, cmd in enumerate(launch_commands, 1):
            print(f"   {i}. {cmd}")
        
        try:
            # Launch main system
            print("\n🚀 Starting main trading system...")
            main_process = subprocess.Popen(
                ["python3", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Launch dashboard controller
            print("🎛️ Starting dashboard controller...")
            dashboard_process = subprocess.Popen(
                ["python3", "dashboard_toggle_controller.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Launch auto-monitor
            print("🤖 Starting auto-monitor system...")
            monitor_process = subprocess.Popen(
                ["python3", "auto_monitor_system.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(5)  # Allow systems to start
            
            print("\n🔥 RBOTZILLA ELITE 18+18: FULLY OPERATIONAL!")
            print("=" * 60)
            print("🎛️ Dashboard Control:  http://localhost:5001")
            print("📱 Main System:        http://localhost:8000")
            print("🤖 Auto-Monitor:       Active with terminal auto-opening")
            print("📊 Status Display:     ./print_live_swarm_status.sh")
            print("=" * 60)
            
            # Log successful launch
            logging.info("🚀 RBOTzilla Elite 18+18 successfully launched")
            logging.info(f"Main PID: {main_process.pid}")
            logging.info(f"Dashboard PID: {dashboard_process.pid}")
            logging.info(f"Monitor PID: {monitor_process.pid}")
            
            return True
            
        except Exception as e:
            print(f"❌ LAUNCH FAILED: {e}")
            logging.error(f"Launch failed: {e}")
            return False
    
    def show_live_status(self):
        """Show current live status"""
        print("\n📊 LIVE SYSTEM STATUS:")
        print("-" * 40)
        
        try:
            # Check if processes are running
            processes = ["main.py", "dashboard_toggle_controller.py", "auto_monitor_system.py"]
            
            for process in processes:
                result = subprocess.run(
                    ["pgrep", "-f", process],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    pids = result.stdout.strip().split('\n')
                    print(f"✅ {process}: Running (PID: {', '.join(pids)})")
                else:
                    print(f"❌ {process}: Not running")
            
            # Show current time and uptime info
            print(f"\n⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🔐 Constitutional PIN: {self.constitutional_pin}")
            print("🎯 System: RBOTzilla Elite 18+18 Dual-Model")
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")

def main():
    """Main ignition system interface"""
    ignition = RBOTzillaIgnitionSystem()
    
    print("\n🎛️ IGNITION SYSTEM MENU:")
    print("1. 🔍 Verify Neural Links")
    print("2. 📋 Show Elite Squad Config")
    print("3. 🚀 Launch Live System") 
    print("4. 📊 Show Live Status")
    print("5. 🔥 Full Ignition (Verify + Launch)")
    print("6. 📱 Status Display (15-second refresh)")
    print("0. 🚪 Exit")
    
    while True:
        try:
            choice = input("\n🎯 Select option (0-6): ").strip()
            
            if choice == "1":
                ignition.verify_neural_links()
            elif choice == "2":
                ignition.display_elite_squad_config()
            elif choice == "3":
                ignition.launch_live_system()
            elif choice == "4":
                ignition.show_live_status()
            elif choice == "5":
                print("🔥 FULL IGNITION SEQUENCE INITIATED...")
                ignition.verify_neural_links()
                time.sleep(2)
                ignition.launch_live_system()
            elif choice == "6":
                print("📱 Launching status display...")
                os.system("./print_live_swarm_status.sh")
            elif choice == "0":
                print("👋 Ignition system shutdown. RBOTzilla standing by.")
                break
            else:
                print("❌ Invalid option. Try again.")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Ignition system interrupted. RBOTzilla standing by.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
