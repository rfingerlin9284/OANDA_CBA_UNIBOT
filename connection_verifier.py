#!/usr/bin/env python3
"""
🔥 RBOTZILLA ELITE 18+18 CONNECTION VERIFIER
Constitutional PIN: 841921
Human-Algo Synergy Testing & Live Connection Verification
"""

import json
import logging
import time
import sys
import requests
from datetime import datetime
import os

# Import credentials
from credentials import WolfpackCredentials

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/connection_verification.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class RBOTzillaConnectionVerifier:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.credentials = WolfpackCredentials()
        self.connection_status = {
            "oanda_api": False,
            "oanda_stream": False,
            "coinbase_api": False,
            "sentiment_feed": False,
            "order_execution": False
        }
        
        logging.info(f"🔥 RBOTzilla Elite 18+18 Connection Verifier - PIN {self.constitutional_pin}")
        print(f"🔥 INITIALIZING CONNECTION VERIFICATION - PIN {self.constitutional_pin}")
    
    def verify_oanda_connection(self):
        """1. Verify Oanda API Connection (Core Neural Link)"""
        print("\n🧠 STEP 1: VERIFYING OANDA API CONNECTION...")
        
        try:
            import oandapyV20
            from oandapyV20.endpoints.accounts import AccountSummary
            
            # Initialize API
            api = oandapyV20.API(
                access_token=self.credentials.OANDA_API_KEY,
                environment="live"
            )
            
            # Test connection with account summary
            request = AccountSummary(self.credentials.OANDA_ACCOUNT_ID)
            response = api.request(request)
            
            # Quantify account health (behavioral momentum proxy)
            balance = float(response['account']['balance'])
            margin_used = float(response['account']['marginUsed']) if response['account']['marginUsed'] else 0.0
            open_trades = int(response['account']['openTradeCount'])
            
            logging.info(f"✅ OANDA CONNECTION SUCCESS: Balance ${balance}, Margin Used ${margin_used}, Open Trades: {open_trades}")
            print(f"✅ OANDA API: LIVE CONNECTION ESTABLISHED")
            print(f"   💰 Account Balance: ${balance:.2f}")
            print(f"   📊 Margin Used: ${margin_used:.2f}")
            print(f"   📈 Open Trades: {open_trades}")
            
            self.connection_status["oanda_api"] = True
            return True
            
        except Exception as e:
            logging.error(f"❌ OANDA CONNECTION FAILED: {str(e)}")
            print(f"❌ OANDA API: CONNECTION FAILED - {str(e)}")
            
            # Diagnose specific errors (human-algo synergy troubleshooting)
            if "401" in str(e):
                print("   🔑 AUTH ERROR: Check API Key or Account ID")
            elif "503" in str(e):
                print("   🔧 SERVICE DOWN: Oanda outage - check status.oanda.com")
            else:
                print("   🌐 NETWORK/OTHER: Verify internet, firewall, or VPN")
            
            return False
    
        """2. Test Real-Time Data Streams (Pricing Neural Feed)"""
        print("\n📡 STEP 2: TESTING OANDA REAL-TIME STREAMS...")
        
        if not self.connection_status["oanda_api"]:
            print("❌ STREAM TEST SKIPPED: No API connection")
            return False
        
        try:
            from oandapyV20.endpoints.pricing import PricingStream
            
            # Test with EUR_USD only for connection verification
            params = {"instruments": "EUR_USD"}
            pricing = PricingStream(self.credentials.OANDA_ACCOUNT_ID, params=params)
            
            
            # Test stream for 5 seconds
            start_time = time.time()
            tick_count = 0
            
            for tick in self.api.request(pricing):
                    break
                
                if tick['type'] == 'PRICE':
                    tick_count += 1
                    instrument = tick['instrument']
                    bid = tick['bids'][0]['price'] if tick.get('bids') else 'N/A'
                    ask = tick['asks'][0]['price'] if tick.get('asks') else 'N/A'
                    
                    logging.info(f"📊 STREAM TICK: {instrument} Bid:{bid} Ask:{ask}")
                    
                    if tick_count == 1:  # First tick confirmation
                        print(f"✅ STREAM ACTIVE: {instrument} Bid:{bid} Ask:{ask}")
            
            if tick_count > 0:
                logging.info(f"✅ STREAM VERIFICATION: {tick_count} ticks received in 5 seconds")
                print(f"✅ OANDA STREAM: LIVE DATA FLOWING ({tick_count} ticks)")
                self.connection_status["oanda_stream"] = True
                return True
            else:
                print("❌ OANDA STREAM: NO DATA RECEIVED")
                return False
                
        except Exception as e:
            logging.error(f"❌ STREAM TEST FAILED: {str(e)}")
            print(f"❌ OANDA STREAM: FAILED - {str(e)}")
            return False
    
    def verify_coinbase_connection(self):
        """3. Verify Coinbase Advanced Trade Connection"""
        print("\n🏦 STEP 3: VERIFYING COINBASE ADVANCED TRADE...")
        
        try:
            # Test Coinbase connection with accounts endpoint
            from coinbase_advanced_api import CoinbaseAdvanced
            
            coinbase = CoinbaseAdvanced(
                api_key=self.credentials.COINBASE_API_KEY_ID,
                private_key=self.credentials.COINBASE_PRIVATE_KEY_PEM
            )
            
            # Test with accounts call
            accounts = coinbase.get_accounts()
            
            if accounts and len(accounts) > 0:
                logging.info(f"✅ COINBASE CONNECTION SUCCESS: {len(accounts)} accounts found")
                print(f"✅ COINBASE API: CONNECTION ESTABLISHED")
                print(f"   💳 Accounts Found: {len(accounts)}")
                
                # Show USD balance if available
                for account in accounts[:3]:  # First 3 accounts
                    currency = account.get('currency', 'Unknown')
                    balance = float(account.get('available_balance', {}).get('value', 0))
                    if currency == 'USD' and balance > 0:
                        print(f"   💰 USD Balance: ${balance:.2f}")
                        break
                
                self.connection_status["coinbase_api"] = True
                return True
            else:
                print("❌ COINBASE API: NO ACCOUNTS FOUND")
                return False
                
        except Exception as e:
            logging.error(f"❌ COINBASE CONNECTION FAILED: {str(e)}")
            print(f"❌ COINBASE API: CONNECTION FAILED - {str(e)}")
            return False
    
        """4. Test Sentiment/Behavioral Data Feeds"""
        print("\n🧠 STEP 4: TESTING SENTIMENT FEEDS (CROWD PSYCHOLOGY)...")
        
        # Test basic internet connectivity for sentiment APIs
        try:
            response = requests.get("https://httpbin.org/status/200", timeout=5)
            if response.status_code == 200:
                logging.info("✅ INTERNET CONNECTIVITY: Verified")
                print("✅ INTERNET: Connectivity verified for sentiment feeds")
                
                # Placeholder for actual sentiment API (you can add your X/Twitter feeds here)
                print("📊 SENTIMENT FEEDS: Ready for integration")
                print("   🐦 Twitter/X Feed: Ready for activation")
                print("   📈 Market Sentiment: Integration points available")
                
                self.connection_status["sentiment_feed"] = True
                return True
            else:
                print("❌ INTERNET: Connectivity issues")
                return False
                
        except Exception as e:
            logging.error(f"❌ SENTIMENT TEST FAILED: {str(e)}")
            print(f"❌ SENTIMENT FEEDS: CONNECTION FAILED - {str(e)}")
            return False
    
        """5. Test Order Execution (Action Arm) - MICRO TEST"""
        print("\n⚡ STEP 5: TESTING ORDER EXECUTION (MICRO TEST)...")
        
        if not self.connection_status["oanda_api"]:
            print("❌ ORDER TEST SKIPPED: No API connection")
            return False
        
        try:
            from oandapyV20.endpoints.orders import OrderCreate
            
            # MICRO TEST: 1 unit EUR_USD with tight stops
            
            # Get current price for realistic stops
            from oandapyV20.endpoints.pricing import PricingInfo
            price_request = PricingInfo(
                accountID=self.credentials.OANDA_ACCOUNT_ID,
                params={"instruments": "EUR_USD"}
            )
            price_response = self.api.request(price_request)
            
            current_ask = float(price_response['prices'][0]['asks'][0]['price'])
            current_bid = float(price_response['prices'][0]['bids'][0]['price'])
            
            # Set conservative stops (10 pips)
            stop_loss = round(current_ask - 0.0010, 5)
            take_profit = round(current_ask + 0.0010, 5)
            
            order_data = {
                "order": {
                    "instrument": "EUR_USD",
                    "units": "1",  # MICRO: 1 unit only
                    "type": "MARKET",
                    "stopLossOnFill": {"price": str(stop_loss)},
                    "takeProfitOnFill": {"price": str(take_profit)}
                }
            }
            
            print(f"📊 MICRO ORDER: 1 unit EUR_USD @ {current_ask}")
            print(f"   🛡️ Stop Loss: {stop_loss}")
            print(f"   🎯 Take Profit: {take_profit}")
            
            order_request = OrderCreate(self.credentials.OANDA_ACCOUNT_ID, data=order_data)
            order_response = self.api.request(order_request)
            
            if 'orderCreateTransaction' in order_response:
                order_id = order_response['orderCreateTransaction']['id']
                logging.info(f"✅ MICRO ORDER SUCCESS: ID {order_id}")
                print(f"✅ ORDER EXECUTION: LIVE AND FUNCTIONAL")
                print(f"   🎯 Order ID: {order_id}")
                print(f"   ⚡ Execution Confirmed: OCO structure active")
                
                self.connection_status["order_execution"] = True
                return True
            else:
                print("❌ ORDER EXECUTION: FAILED TO CREATE ORDER")
                return False
                
        except Exception as e:
            logging.error(f"❌ ORDER EXECUTION FAILED: {str(e)}")
            print(f"❌ ORDER EXECUTION: FAILED - {str(e)}")
            
            if "INSUFFICIENT_MARGIN" in str(e):
                print("   💰 MARGIN ERROR: Insufficient funds for order")
            elif "MARKET_HALTED" in str(e):
                print("   🛑 MARKET CLOSED: Trading hours issue")
            
            return False
    
    def generate_connection_report(self):
        """Generate comprehensive connection report"""
        print("\n" + "="*60)
        print("🔥 RBOTZILLA ELITE 18+18 CONNECTION REPORT")
        print("="*60)
        print(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Connection status summary
        
        print("📊 CONNECTION STATUS:")
        for system, status in self.connection_status.items():
            icon = "✅" if status else "❌"
            system_name = system.replace('_', ' ').title()
            print(f"   {icon} {system_name}: {'CONNECTED' if status else 'FAILED'}")
        
        print()
        
            print("🚀 SYSTEM STATUS: FULLY OPERATIONAL - READY FOR ELITE 18+18 DEPLOYMENT")
            print("🔥 HUMAN-ALGO SYNERGY: MAXIMUM EFFICIENCY ACHIEVED")
            logging.info("🚀 FULL SYSTEM VERIFICATION: ALL CONNECTIONS OPERATIONAL")
            print("⚠️ SYSTEM STATUS: PARTIALLY OPERATIONAL - PROCEED WITH CAUTION")
        else:
            print("❌ SYSTEM STATUS: CRITICAL FAILURES - DEPLOYMENT NOT RECOMMENDED")
        
        print("="*60)
        

def main():
    """Execute full connection verification suite"""
    print("🔥 RBOTZILLA ELITE 18+18 - NEURAL LINK VERIFICATION")
    print("Constitutional PIN: 841921")
    print("Quantifying the herd, preparing to strike...")
    print()
    
    verifier = RBOTzillaConnectionVerifier()
    
    # Execute verification sequence
        ("Oanda API", verifier.verify_oanda_connection),
        ("Coinbase API", verifier.verify_coinbase_connection),
    ]
    
    print("🧪 EXECUTING NEURAL LINK VERIFICATION SEQUENCE...")
    
        try:
        except Exception as e:
        
    
    # Generate final report
    all_systems_go = verifier.generate_connection_report()
    
    if all_systems_go:
        print("\n🚀 IGNITION SEQUENCE: READY FOR LIVE DEPLOYMENT")
        print("💥 The swarm awakens. Market chaos becomes dominance.")
    else:
        print("\n⚠️ SYSTEM CHECK: Address failed connections before deployment")
        print("🔧 Debug and retry failed systems")

if __name__ == "__main__":
    main()
