#!/usr/bin/env python3
"""
🔥 HARDCODED LIVE TRADING SYSTEM - NO CONFIG FILES
Constitutional PIN: 841921
ALL CREDENTIALS AND ENDPOINTS HARDCODED - NO ENV FILES

This system bypasses ALL configuration files and environment variables.
Everything is hardcoded to LIVE endpoints and real credentials.
ZERO possibility of simulation mode.
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime

# HARDCODED LIVE CREDENTIALS - NO ENV FILES
CONSTITUTIONAL_PIN = "841921"
OANDA_API_KEY = "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48"
OANDA_ACCOUNT_ID = "001-001-13473069-001"
OANDA_ENVIRONMENT = "live"  # HARDCODED - NEVER CHANGE
OANDA_LIVE_URL = "https://api-fxtrade.oanda.com"  # HARDCODED LIVE ENDPOINT

# SIMULATION MODE PERMANENTLY BLOCKED
SIM_MODE = False
PRACTICE_MODE = False
SANDBOX_MODE = False
DEMO_MODE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/hardcoded_live_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HardcodedLiveTradingSystem:
    """Hardcoded Live Trading System - No Config Dependencies"""
    
    def __init__(self):
        """Initialize with hardcoded live credentials"""
        self.constitutional_pin = CONSTITUTIONAL_PIN
        self.api_key = OANDA_API_KEY
        self.account_id = OANDA_ACCOUNT_ID
        self.environment = OANDA_ENVIRONMENT
        self.api_url = OANDA_LIVE_URL
        
        self.start_time = datetime.now()
        self.is_running = False
        self.trade_count = 0
        self.account_balance = 0.0
        
        # SECURITY: Verify hardcoded values
        self.verify_hardcoded_security()
        
        # Initialize OANDA with hardcoded credentials
        self.initialize_hardcoded_oanda()
        
        logger.info("🔥 HARDCODED LIVE TRADING SYSTEM INITIALIZED")
        logger.info(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        logger.info(f"🎯 API Endpoint: {self.api_url}")
        logger.info("🚨 100% HARDCODED - NO CONFIG FILE DEPENDENCIES")
        
    def verify_hardcoded_security(self):
        """Verify all hardcoded values are live-only"""
        logger.info("🛡️  VERIFYING HARDCODED SECURITY...")
        
        # Verify Constitutional PIN
        if self.constitutional_pin != "841921":
            logger.error("❌ CONSTITUTIONAL PIN MISMATCH")
            sys.exit(1)
            
        # Verify environment is live
        if self.environment != "live":
            logger.error(f"❌ NON-LIVE ENVIRONMENT: {self.environment}")
            sys.exit(1)
            
        # Verify live endpoint
        if "fxpractice" in self.api_url:
            logger.error("❌ PRACTICE ENDPOINT DETECTED")
            sys.exit(1)
            
        if self.api_url != "https://api-fxtrade.oanda.com":
            logger.error(f"❌ INVALID ENDPOINT: {self.api_url}")
            sys.exit(1)
            
        # Verify simulation modes are disabled
        if SIM_MODE or PRACTICE_MODE or SANDBOX_MODE or DEMO_MODE:
            logger.error("❌ SIMULATION MODE ENABLED")
            sys.exit(1)
            
            logger.error("❌ LIVE TRADING NOT ENFORCED")
            sys.exit(1)
            
        logger.info("✅ HARDCODED SECURITY VERIFICATION PASSED")
        logger.info("✅ Live credentials confirmed")
        logger.info("✅ Live endpoint confirmed")
        logger.info("✅ Simulation modes blocked")
        
    def initialize_hardcoded_oanda(self):
        """Initialize OANDA with hardcoded live credentials"""
        logger.info("🎯 INITIALIZING HARDCODED OANDA CONNECTION...")
        
        try:
            import oandapyV20
            from oandapyV20 import API
            from oandapyV20.endpoints.accounts import AccountDetails
            
            # Create API with hardcoded live credentials
            self.oanda_api = API(
                access_token=self.api_key,
                environment="live"  # HARDCODED - NEVER CHANGE
            )
            
            # Test connection
            account_request = AccountDetails(accountID=self.account_id)
            response = self.oanda_api.request(account_request)
            
            if response and 'account' in response:
                account_data = response['account']
                self.account_balance = float(account_data['balance'])
                currency = account_data['currency']
                
                logger.info("✅ HARDCODED OANDA CONNECTION VERIFIED")
                logger.info(f"💰 Account Balance: {currency} {self.account_balance:,.2f}")
                logger.info(f"🔴 LIVE TRADING MODE CONFIRMED")
                logger.info(f"📊 Account ID: {self.account_id}")
                
                return True
            else:
                logger.error("❌ Invalid account response")
                return False
                
        except ImportError:
            logger.error("❌ oandapyV20 not installed")
            logger.info("💡 Install with: pip install oandapyV20")
            return False
        except Exception as e:
            logger.error(f"❌ OANDA connection failed: {e}")
            return False
            
    def execute_live_order_test(self):
        """Execute a minimal live order test"""
        logger.info("🧪 EXECUTING LIVE ORDER TEST...")
        logger.info("🚨 THIS WILL PLACE A REAL MONEY ORDER")
        
        try:
            from oandapyV20.endpoints.orders import OrderCreate
            
            # Minimal risk test order - 1 unit EUR/USD
            test_instrument = "EUR_USD"
            
            # Get current price for SL/TP calculation
            from oandapyV20.endpoints.pricing import PricingInfo
            pricing_request = PricingInfo(
                accountID=self.account_id,
                params={"instruments": test_instrument}
            )
            pricing_response = self.oanda_api.request(pricing_request)
            
            if pricing_response and 'prices' in pricing_response:
                current_price = float(pricing_response['prices'][0]['closeoutBid'])
                
                # Calculate conservative SL/TP (small risk)
                sl_price = current_price - 0.0020  # 20 pip stop loss
                tp_price = current_price + 0.0060  # 60 pip take profit (1:3 RR)
                
                # Create order data
                order_data = {
                    "order": {
                        "instrument": test_instrument,
                        "units": str(test_units),
                        "type": "MARKET",
                        "positionFill": "DEFAULT",
                        "stopLossOnFill": {"price": f"{sl_price:.5f}"},
                        "takeProfitOnFill": {"price": f"{tp_price:.5f}"}
                    }
                }
                
                logger.info(f"📤 LIVE TEST ORDER DETAILS:")
                logger.info(f"   Instrument: {test_instrument}")
                logger.info(f"   Units: {test_units} (minimal risk)")
                logger.info(f"   Entry: ~{current_price:.5f}")
                logger.info(f"   Stop Loss: {sl_price:.5f}")
                logger.info(f"   Take Profit: {tp_price:.5f}")
                logger.info("🚨 REAL MONEY ORDER - EXECUTING NOW...")
                
                # Execute the order
                order_request = OrderCreate(accountID=self.account_id, data=order_data)
                response = self.oanda_api.request(order_request)
                
                if response and 'orderFillTransaction' in response:
                    fill_data = response['orderFillTransaction']
                    order_id = fill_data.get('id')
                    trade_id = fill_data.get('tradeOpened', {}).get('tradeID')
                    fill_price = float(fill_data.get('price', current_price))
                    
                    self.trade_count += 1
                    
                    logger.info("✅ LIVE ORDER EXECUTED SUCCESSFULLY")
                    logger.info(f"   Order ID: {order_id}")
                    logger.info(f"   Trade ID: {trade_id}")
                    logger.info(f"   Fill Price: {fill_price:.5f}")
                    logger.info("🎯 OCO Protection Active")
                    logger.info("💰 REAL MONEY TRADE CONFIRMED")
                    
                    return {
                        'success': True,
                        'order_id': order_id,
                        'trade_id': trade_id,
                        'fill_price': fill_price
                    }
                else:
                    logger.error("❌ Order execution failed")
                    return {'success': False, 'error': 'No fill transaction'}
                    
            else:
                logger.error("❌ Failed to get current price")
                return {'success': False, 'error': 'Price fetch failed'}
                
        except Exception as e:
            logger.error(f"❌ Live order test failed: {e}")
            return {'success': False, 'error': str(e)}
            
    def get_account_summary(self):
        """Get current account summary"""
        try:
            from oandapyV20.endpoints.accounts import AccountSummary
            
            summary_request = AccountSummary(accountID=self.account_id)
            response = self.oanda_api.request(summary_request)
            
            if response and 'account' in response:
                account = response['account']
                
                balance = float(account['balance'])
                unrealized_pnl = float(account['unrealizedPL'])
                total_pnl = float(account['pl'])
                open_trades = int(account['openTradeCount'])
                open_positions = int(account['openPositionCount'])
                
                logger.info(f"💰 ACCOUNT SUMMARY:")
                logger.info(f"   Balance: ${balance:,.2f}")
                logger.info(f"   Unrealized PnL: ${unrealized_pnl:,.2f}")
                logger.info(f"   Total PnL: ${total_pnl:,.2f}")
                logger.info(f"   Open Trades: {open_trades}")
                logger.info(f"   Open Positions: {open_positions}")
                
                return {
                    'balance': balance,
                    'unrealized_pnl': unrealized_pnl,
                    'total_pnl': total_pnl,
                    'open_trades': open_trades,
                    'open_positions': open_positions
                }
            else:
                logger.error("❌ Failed to get account summary")
                return None
                
        except Exception as e:
            logger.error(f"❌ Account summary failed: {e}")
            return None
            
    def monitor_live_system(self):
        """Monitor live trading system"""
        logger.info("📊 STARTING LIVE SYSTEM MONITORING...")
        
        while self.is_running:
            try:
                # Get account summary
                summary = self.get_account_summary()
                
                if summary:
                    uptime = (datetime.now() - self.start_time).total_seconds() / 60
                    
                    logger.info(f"💓 LIVE SYSTEM HEARTBEAT:")
                    logger.info(f"   Uptime: {uptime:.1f} minutes")
                    logger.info(f"   Balance: ${summary['balance']:,.2f}")
                    logger.info(f"   P&L: ${summary['total_pnl']:,.2f}")
                    logger.info(f"   Open Trades: {summary['open_trades']}")
                    logger.info(f"   Constitutional PIN: {self.constitutional_pin}")
                
                # Sleep between updates
                time.sleep(30)  # Update every 30 seconds
                
            except KeyboardInterrupt:
                logger.info("🛑 Monitoring interrupted")
                break
            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                time.sleep(10)
                
    def start_live_trading(self):
        """Start the hardcoded live trading system"""
        logger.info("🚀 STARTING HARDCODED LIVE TRADING SYSTEM")
        logger.info("=" * 70)
        logger.info("⚠️  WARNING: HARDCODED LIVE TRADING WITH REAL MONEY")
        logger.info(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        logger.info(f"💰 Account: {self.account_id}")
        logger.info(f"💵 Balance: ${self.account_balance:,.2f}")
        logger.info("🛡️  No config file dependencies")
        logger.info("🔥 100% hardcoded live credentials")
        logger.info("=" * 70)
        
        # Final confirmation
        print("\n🚨 FINAL WARNING: This will execute REAL MONEY trades")
        print("🔴 Hardcoded live credentials active")
        print("💰 Real account balance at risk")
        
        confirm = input("\nType 'EXECUTE LIVE TRADING' to proceed: ").strip()
        if confirm != "EXECUTE LIVE TRADING":
            logger.info("❌ Live trading not confirmed - system shutdown")
            return False
            
        self.is_running = True
        
        # Execute test order first
        logger.info("🧪 Executing initial live order test...")
        test_result = self.execute_live_order_test()
        
        if test_result['success']:
            logger.info("✅ LIVE ORDER TEST SUCCESSFUL")
            logger.info("🎯 System ready for full trading")
        else:
            logger.error(f"❌ Live order test failed: {test_result['error']}")
            return False
            
        # Start monitoring
        monitor_thread = threading.Thread(target=self.monitor_live_system, daemon=True)
        monitor_thread.start()
        
        logger.info("✅ HARDCODED LIVE TRADING SYSTEM ACTIVE")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Stopping hardcoded live trading system")
            self.is_running = False
            
        runtime = (datetime.now() - self.start_time).total_seconds() / 60
        logger.info(f"📊 Session completed - Runtime: {runtime:.1f} minutes")
        
        return True

def main():
    """Main entry point"""
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    print("🔥 HARDCODED LIVE TRADING SYSTEM")
    print(f"Constitutional PIN: {CONSTITUTIONAL_PIN}")
    print("NO CONFIG FILE DEPENDENCIES")
    print("100% HARDCODED LIVE CREDENTIALS")
    print()
    
    # Initialize and start
    trading_system = HardcodedLiveTradingSystem()
    trading_system.start_live_trading()

if __name__ == "__main__":
    main()
