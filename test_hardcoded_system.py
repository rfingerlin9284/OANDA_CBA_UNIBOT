#!/usr/bin/env python3
"""
🧪 HARDCODED LIVE TRADING TEST
Constitutional PIN: 841921
Quick test to verify hardcoded system works without any config files
"""

import sys
import logging

# HARDCODED LIVE CREDENTIALS - BYPASSING ALL CONFIG FILES
OANDA_API_KEY = "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48"
OANDA_ACCOUNT_ID = "001-001-13473069-001"
OANDA_ENVIRONMENT = "live"
OANDA_LIVE_URL = "https://api-fxtrade.oanda.com"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def test_hardcoded_connection():
    """Test OANDA connection with hardcoded credentials"""
    logger.info("🧪 TESTING HARDCODED LIVE CONNECTION...")
    logger.info(f"🎯 Using hardcoded API key: {OANDA_API_KEY[:10]}...")
    logger.info(f"🎯 Using hardcoded account: {OANDA_ACCOUNT_ID}")
    logger.info(f"🎯 Using hardcoded endpoint: {OANDA_LIVE_URL}")
    
    try:
        import oandapyV20
        from oandapyV20 import API
        from oandapyV20.endpoints.accounts import AccountDetails
        
        # Create API with hardcoded values
        api = API(
            access_token=OANDA_API_KEY,
            environment="live"  # HARDCODED
        )
        
        # Test connection
        account_request = AccountDetails(accountID=OANDA_ACCOUNT_ID)
        response = api.request(account_request)
        
        if response and 'account' in response:
            account = response['account']
            balance = float(account['balance'])
            currency = account['currency']
            
            logger.info("✅ HARDCODED CONNECTION SUCCESSFUL")
            logger.info(f"💰 Account Balance: {currency} {balance:,.2f}")
            logger.info(f"🔴 LIVE MODE CONFIRMED")
            logger.info("🎯 No config files used - 100% hardcoded")
            
            return True, balance
        else:
            logger.error("❌ Invalid response from OANDA")
            return False, 0
            
    except ImportError:
        logger.error("❌ oandapyV20 not installed")
        logger.info("💡 Install with: pip install oandapyV20")
        return False, 0
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False, 0

def test_hardcoded_pricing():
    """Test getting live pricing with hardcoded credentials"""
    logger.info("📊 TESTING HARDCODED LIVE PRICING...")
    
    try:
        import oandapyV20
        from oandapyV20 import API
        from oandapyV20.endpoints.pricing import PricingInfo
        
        # Create API with hardcoded values
        api = API(
            access_token=OANDA_API_KEY,
            environment="live"  # HARDCODED
        )
        
        # Get EUR/USD pricing
        pricing_request = PricingInfo(
            accountID=OANDA_ACCOUNT_ID,
            params={"instruments": "EUR_USD"}
        )
        response = api.request(pricing_request)
        
        if response and 'prices' in response:
            price_data = response['prices'][0]
            bid = float(price_data['closeoutBid'])
            ask = float(price_data['closeoutAsk'])
            spread = ask - bid
            
            logger.info("✅ HARDCODED PRICING SUCCESSFUL")
            logger.info(f"💱 EUR/USD Bid: {bid:.5f}")
            logger.info(f"💱 EUR/USD Ask: {ask:.5f}")
            logger.info(f"💱 Spread: {spread:.5f}")
            logger.info("🔴 LIVE MARKET DATA CONFIRMED")
            
            return True, bid, ask
        else:
            logger.error("❌ No pricing data received")
            return False, 0, 0
            
    except Exception as e:
        logger.error(f"❌ Pricing test failed: {e}")
        return False, 0, 0

def main():
    """Run hardcoded tests"""
    logger.info("🔥 HARDCODED LIVE TRADING SYSTEM TEST")
    logger.info("=" * 50)
    logger.info("🛡️  NO CONFIG FILE DEPENDENCIES")
    logger.info("🎯 100% HARDCODED LIVE CREDENTIALS")
    logger.info("=" * 50)
    
    # Test 1: Connection
    success, balance = test_hardcoded_connection()
    if not success:
        logger.error("❌ Connection test failed - aborting")
        return False
        
    # Test 2: Pricing
    success, bid, ask = test_hardcoded_pricing()
    if not success:
        logger.error("❌ Pricing test failed")
        return False
        
    # Summary
    logger.info("\n🎯 HARDCODED TEST RESULTS:")
    logger.info("✅ Connection: SUCCESSFUL")
    logger.info("✅ Pricing: SUCCESSFUL") 
    logger.info("✅ Live mode: CONFIRMED")
    logger.info(f"✅ Account balance: ${balance:,.2f}")
    logger.info(f"✅ Current EUR/USD: {bid:.5f}")
    logger.info("\n🔥 HARDCODED SYSTEM READY FOR LIVE TRADING")
    logger.info("🚨 NO SIMULATION MODE POSSIBLE")
    
    return True

if __name__ == "__main__":
    if main():
        print("\n✅ All hardcoded tests passed!")
        print("🚀 Ready to run: python3 hardcoded_live_trading.py")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
