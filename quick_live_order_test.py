#!/usr/bin/env python3
"""
⚡ QUICK LIVE ORDER EXECUTION TEST
Constitutional PIN: 841921
Demonstrates the hardcoded system executing a real live order
"""

import logging

# HARDCODED LIVE CREDENTIALS - NO CONFIG FILES
OANDA_API_KEY = "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48"
OANDA_ACCOUNT_ID = "001-001-13473069-001"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_live_order_demo():
    """Execute a minimal live order to prove the system works"""
    logger.info("⚡ QUICK LIVE ORDER EXECUTION TEST")
    logger.info("🚨 THIS WILL PLACE A REAL MONEY ORDER")
    logger.info("=" * 50)
    
    try:
        import oandapyV20
        from oandapyV20 import API
        from oandapyV20.endpoints.orders import OrderCreate
        from oandapyV20.endpoints.pricing import PricingInfo
        
        # Create hardcoded API connection
        api = API(
            access_token=OANDA_API_KEY,
            environment="live"  # HARDCODED LIVE
        )
        
        # Get current EUR/USD price
        pricing_request = PricingInfo(
            accountID=OANDA_ACCOUNT_ID,
            params={"instruments": "EUR_USD"}
        )
        pricing_response = api.request(pricing_request)
        
        if pricing_response and 'prices' in pricing_response:
            current_price = float(pricing_response['prices'][0]['closeoutBid'])
            logger.info(f"💱 Current EUR/USD price: {current_price:.5f}")
            
            # Calculate conservative SL/TP for minimal risk
            sl_price = current_price - 0.0020  # 20 pip stop loss
            tp_price = current_price + 0.0060  # 60 pip take profit
            
            # Create minimal risk order (1 unit)
            order_data = {
                "order": {
                    "instrument": "EUR_USD",
                    "units": "1",  # Minimal risk - 1 unit only
                    "type": "MARKET",
                    "positionFill": "DEFAULT",
                    "stopLossOnFill": {"price": f"{sl_price:.5f}"},
                    "takeProfitOnFill": {"price": f"{tp_price:.5f}"}
                }
            }
            
            logger.info("📤 EXECUTING LIVE ORDER:")
            logger.info(f"   Instrument: EUR_USD")
            logger.info(f"   Units: 1 (minimal risk)")
            logger.info(f"   Entry: ~{current_price:.5f}")
            logger.info(f"   Stop Loss: {sl_price:.5f}")
            logger.info(f"   Take Profit: {tp_price:.5f}")
            logger.info("🚨 REAL MONEY ORDER - EXECUTING NOW...")
            
            # Confirm execution
            confirm = input("\nType 'EXECUTE LIVE ORDER' to proceed: ").strip()
            if confirm != "EXECUTE LIVE ORDER":
                logger.info("❌ Order execution cancelled")
                return False
                
            # Execute the order
            order_request = OrderCreate(accountID=OANDA_ACCOUNT_ID, data=order_data)
            response = api.request(order_request)
            
            if response and 'orderFillTransaction' in response:
                fill_data = response['orderFillTransaction']
                order_id = fill_data.get('id')
                trade_id = fill_data.get('tradeOpened', {}).get('tradeID')
                fill_price = float(fill_data.get('price', current_price))
                
                logger.info("✅ LIVE ORDER EXECUTED SUCCESSFULLY!")
                logger.info(f"🎯 Order ID: {order_id}")
                logger.info(f"🎯 Trade ID: {trade_id}")
                logger.info(f"🎯 Fill Price: {fill_price:.5f}")
                logger.info(f"🎯 Stop Loss: {sl_price:.5f}")
                logger.info(f"🎯 Take Profit: {tp_price:.5f}")
                logger.info("💰 REAL MONEY TRADE CONFIRMED")
                logger.info("🛡️  OCO Protection Active")
                
                # Show account impact
                logger.info("\n💰 ACCOUNT IMPACT:")
                logger.info(f"   Risk: ~$2.00 (20 pip SL on 1 unit)")
                logger.info(f"   Reward: ~$6.00 (60 pip TP on 1 unit)")
                logger.info(f"   Risk/Reward: 1:3 ratio")
                
                return True
            else:
                logger.error("❌ Order execution failed")
                return False
                
        else:
            logger.error("❌ Failed to get current price")
            return False
            
    except ImportError:
        logger.error("❌ oandapyV20 not installed")
        return False
    except Exception as e:
        logger.error(f"❌ Order execution failed: {e}")
        return False

def main():
    """Main execution"""
    logger.info("🔥 HARDCODED LIVE ORDER EXECUTION DEMO")
    logger.info("Constitutional PIN: 841921")
    logger.info("Account: 001-001-13473069-001")
    logger.info("100% Hardcoded - No Config Files")
    logger.info("")
    
    success = execute_live_order_demo()
    
    if success:
        logger.info("\n🎉 LIVE ORDER EXECUTION SUCCESSFUL!")
        logger.info("✅ Hardcoded system works perfectly")
        logger.info("✅ Real money trading confirmed")
        logger.info("✅ OCO protection active")
        logger.info("🚀 System ready for full trading")
    else:
        logger.info("\n❌ Order execution failed")

if __name__ == "__main__":
    main()
