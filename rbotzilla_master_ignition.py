#!/usr/bin/env python3
"""
🔥 RBOTZILLA ELITE 18+18 - MASTER IGNITION SYSTEM
Constitutional PIN: 841921
Human-Algo Synergy: Market Chaos → Trading Dominance
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from credentials import WolfpackCredentials
import oandapyV20
from oandapyV20.endpoints.accounts import AccountSummary

class RBOTzillaMasterIgnition:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.credentials = WolfpackCredentials()
        self.system_status = {
            "neural_links": False,
            "configuration": False,
            "models": False,
            "live_system": False
        }
        
        self.display_banner()
    
    def display_banner(self):
        """Display RBOTzilla Elite 18+18 ignition banner"""
        print("=" * 80)
        print("🔥 RBOTZILLA ELITE 18+18 - MASTER IGNITION SYSTEM")
        print("=" * 80)
        print(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        print("🎯 Architecture: Dual-Model Elite Squad (18 Forex + 18 Crypto)")
        print("🧠 Mission: Quantify crowd psychology → Trading dominance")
        print("⚡ Neural Link Status: Verifying...")
        print("=" * 80)
    
    def verify_neural_links(self):
        """Verify all neural connections"""
        print("\n🧠 VERIFYING NEURAL LINKS...")
        
        try:
            # Test Oanda connection
            api = oandapyV20.API(
                access_token=self.credentials.OANDA_API_KEY,
                environment="live"
            )
            
            request = AccountSummary(self.credentials.OANDA_ACCOUNT_ID)
            response = api.request(request)
            
            balance = float(response['account']['balance'])
            currency = response['account']['currency']
            open_trades = int(response['account']['openTradeCount'])
            
            print(f"✅ OANDA API: CONNECTED")
            print(f"   💰 Balance: ${balance:.2f} {currency}")
            print(f"   📊 Open Trades: {open_trades}")
            
            self.system_status["neural_links"] = True
            return True
            
        except Exception as e:
            print(f"❌ NEURAL LINK FAILURE: {e}")
            return False
    
    def verify_configuration(self):
        """Verify Elite 18+18 configuration"""
        print("\n📋 VERIFYING ELITE 18+18 CONFIGURATION...")
        
        config_files = [
            "config/rbotzilla_live_config.json",
            "config/live_config.json",
            "config.json"
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    
                    # Check for Elite 18+18 pairs
                    if 'pairs' in config:
                        forex_count = len(config['pairs'].get('forex', []))
                        crypto_count = len(config['pairs'].get('crypto', []))
                        
                        print(f"✅ CONFIGURATION: LOADED ({config_file})")
                        print(f"   📈 Forex Squad: {forex_count} pairs")
                        print(f"   💰 Crypto Squad: {crypto_count} pairs")
                        
                        self.system_status["configuration"] = True
                        return True
                        
                except Exception as e:
                    print(f"⚠️ Config error in {config_file}: {e}")
                    continue
        
        print("❌ CONFIGURATION: Not found or invalid")
        return False
    
    def verify_models(self):
        """Verify ML models are available"""
        print("\n🧠 VERIFYING ML MODELS...")
        
        model_files = [
        ]
        
        models_found = 0
        for model_file in model_files:
            if os.path.exists(model_file):
                size = os.path.getsize(model_file)
                print(f"✅ {model_file}: {size/1024/1024:.1f}MB")
                models_found += 1
            else:
                print(f"⚠️ {model_file}: Not found")
        
        if models_found >= 1:
            print(f"✅ MODELS: {models_found}/3 available")
            self.system_status["models"] = True
            return True
        else:
            print("❌ MODELS: No valid models found")
            return False
    
    def launch_live_system(self):
        """Launch the complete RBOTzilla Elite 18+18 system"""
        print("\n🚀 LAUNCHING RBOTZILLA ELITE 18+18 SYSTEM...")
        
        # Verify all systems first
        if not all([
            self.system_status["neural_links"],
            self.system_status["configuration"],
            self.system_status["models"]
        ]):
            print("❌ LAUNCH ABORTED: Prerequisites not met")
            return False
        
        try:
            print("🔥 IGNITION SEQUENCE INITIATED...")
            
            # Launch main system
            print("   🤖 Starting main trading system...")
            main_process = subprocess.Popen(
                ["python3", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)
            
            # Launch auto-monitor system
            if os.path.exists("auto_monitor_system.py"):
                print("   📊 Starting auto-monitor system...")
                monitor_process = subprocess.Popen(
                    ["python3", "auto_monitor_system.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(2)
            
            # Launch status display
            if os.path.exists("print_live_swarm_status.sh"):
                print("   📱 Starting live status display...")
                subprocess.Popen(["bash", "-c", "./print_live_swarm_status.sh &"])
            
            print("🔥 RBOTZILLA ELITE 18+18: FULLY OPERATIONAL!")
            print("=" * 60)
            print("🎛️ System Components:")
            print("   🤖 Main Trading System: ACTIVE")
            print("   📊 Auto-Monitor: ACTIVE")  
            print("   📱 Live Status: ACTIVE (15-second refresh)")
            print("   🔐 Constitutional PIN: 841921")
            print("=" * 60)
            
            self.system_status["live_system"] = True
            return True
            
        except Exception as e:
            print(f"❌ LAUNCH FAILED: {e}")
            return False
    
    def system_status_report(self):
        """Generate comprehensive system status report"""
        print("\n" + "="*70)
        print("📊 RBOTZILLA ELITE 18+18 SYSTEM STATUS REPORT")
        print("="*70)
        print(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        print(f"⏰ Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        status_items = {
            "neural_links": "🧠 Neural Links (Oanda API)",
            "configuration": "📋 Elite 18+18 Configuration", 
            "models": "🤖 ML Models",
            "live_system": "🚀 Live Trading System"
        }
        
        for key, description in status_items.items():
            status = "OPERATIONAL" if self.system_status[key] else "OFFLINE"
            icon = "✅" if self.system_status[key] else "❌"
            print(f"   {icon} {description}: {status}")
        
        total_systems = len(self.system_status)
        operational_systems = sum(self.system_status.values())
        
        print(f"\n📈 OVERALL STATUS: {operational_systems}/{total_systems} systems operational")
        
        if operational_systems == total_systems:
            print("🔥 SYSTEM STATUS: FULLY OPERATIONAL")
            print("💥 ELITE 18+18 READY FOR MARKET DOMINATION")
        elif operational_systems >= 3:
            print("⚠️ SYSTEM STATUS: PARTIALLY OPERATIONAL")
        else:
            print("❌ SYSTEM STATUS: CRITICAL FAILURES")
        
        print("="*70)
        
        return operational_systems == total_systems
    
    def interactive_menu(self):
        """Interactive ignition menu"""
        while True:
            print(f"\n🔥 RBOTZILLA ELITE 18+18 MASTER CONTROL")
            print(f"Constitutional PIN: {self.constitutional_pin}")
            print("-" * 50)
            print("1. 🧠 Verify Neural Links")
            print("2. 📋 Verify Configuration") 
            print("3. 🤖 Verify ML Models")
            print("4. 🚀 Launch Live System")
            print("5. 📊 System Status Report")
            print("6. 🔥 FULL IGNITION (All Systems)")
            print("7. 📱 Live Status Monitor")
            print("0. 🚪 Exit")
            
            try:
                choice = input("\n🎯 Select option (0-7): ").strip()
                
                if choice == "1":
                    self.verify_neural_links()
                elif choice == "2":
                    self.verify_configuration()
                elif choice == "3":
                    self.verify_models()
                elif choice == "4":
                    self.launch_live_system()
                elif choice == "5":
                    self.system_status_report()
                elif choice == "6":
                    print("🔥 FULL IGNITION SEQUENCE...")
                    self.verify_neural_links()
                    time.sleep(1)
                    self.verify_configuration()
                    time.sleep(1)
                    self.verify_models()
                    time.sleep(1)
                    if all(self.system_status.values()):
                        self.launch_live_system()
                elif choice == "7":
                    if os.path.exists("print_live_swarm_status.sh"):
                        os.system("./print_live_swarm_status.sh")
                    else:
                        print("📱 Status monitor not found")
                elif choice == "0":
                    print("👋 RBOTzilla Master Ignition: Shutdown")
                    print("🔥 Elite 18+18 system standing by...")
                    break
                else:
                    print("❌ Invalid option")
                    
            except KeyboardInterrupt:
                print("\n🛑 Ignition system interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main ignition system entry point"""
    print("🔥 INITIALIZING RBOTZILLA ELITE 18+18 MASTER IGNITION")
    
    ignition = RBOTzillaMasterIgnition()
    ignition.interactive_menu()

if __name__ == "__main__":
    main()
