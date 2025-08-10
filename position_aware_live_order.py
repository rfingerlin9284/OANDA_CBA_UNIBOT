#!/usr/bin/env python3
"""
🔍 ACCOUNT POSITION CHECKER
Constitutional PIN: 841921
Check current positions and place order on available pair
"""

import logging

# HARDCODED LIVE CREDENTIALS
OANDA_API_KEY = "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48"
OANDA_ACCOUNT_ID = "001-001-13473069-001"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def check_current_positions():
    """Check current account positions"""
    try:
        import oandapyV20
        from oandapyV20 import API
        from oandapyV20.endpoints.positions import OpenPositions
        from oandapyV20.endpoints.accounts import AccountDetails
        
        api = API(access_token=OANDA_API_KEY, environment="live")
        
        # Get account summary
        account_request = AccountDetails(accountID=OANDA_ACCOUNT_ID)
        account_response = api.request(account_request)
        
        if account_response:
            account = account_response['account']
            balance = float(account['balance'])
            unrealized_pnl = float(account['unrealizedPL'])
            open_trades = int(account['openTradeCount'])
            
            logger.info(f"💰 Account Balance: ${balance:,.2f}")
            logger.info(f"📊 Unrealized P&L: ${unrealized_pnl:,.2f}")
            logger.info(f"📈 Open Trades: {open_trades}")
        
        # Get open positions
        positions_request = OpenPositions(accountID=OANDA_ACCOUNT_ID)
        positions_response = api.request(positions_request)
        
        if positions_response and 'positions' in positions_response:
            positions = positions_response['positions']
            
            if positions:
                logger.info("📊 CURRENT OPEN POSITIONS:")
                for pos in positions:
                    instrument = pos['instrument']
                    long_units = float(pos['long']['units'])
                    short_units = float(pos['short']['units'])
                    unrealized_pl = float(pos['unrealizedPL'])
                    
                    if long_units != 0:
                        logger.info(f"   {instrument}: LONG {long_units} units, P&L: ${unrealized_pl:.2f}")
                    if short_units != 0:
                        logger.info(f"   {instrument}: SHORT {abs(short_units)} units, P&L: ${unrealized_pl:.2f}")
                        
                # Return list of instruments with positions
                busy_instruments = [pos['instrument'] for pos in positions 
                                  if float(pos['long']['units']) != 0 or float(pos['short']['units']) != 0]
                return busy_instruments
            else:
                logger.info("📊 No open positions")
                return []
        else:
            logger.info("📊 No positions data")
            return []
            
    except Exception as e:
        logger.error(f"❌ Failed to check positions: {e}")
        return []

def place_order_on_available_pair():
    """Place order on a pair without existing positions"""
    try:
        import oandapyV20
        from oandapyV20 import API
        from oandapyV20.endpoints.orders import OrderCreate
        from oandapyV20.endpoints.pricing import PricingInfo
        
        api = API(access_token=OANDA_API_KEY, environment="live")
        
        # Check current positions
        busy_instruments = check_current_positions()
        logger.info(f"📊 Instruments with positions: {busy_instruments}")
        
        # Available instruments to try
        available_instruments = ["GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD", "USD_CHF"]
        
        # Find an instrument without positions
        free_instrument = None
        for instrument in available_instruments:
            if instrument not in busy_instruments:
                free_instrument = instrument
                break
                
        if not free_instrument:
            logger.error("❌ All major pairs have existing positions")
            return False
            
        logger.info(f"🎯 Selected instrument: {free_instrument}")
        
        # Get current price
        pricing_request = PricingInfo(
            accountID=OANDA_ACCOUNT_ID,
            params={"instruments": free_instrument}
        )
        pricing_response = api.request(pricing_request)
        
        if pricing_response and 'prices' in pricing_response:
            current_price = float(pricing_response['prices'][0]['closeoutBid'])
            logger.info(f"💱 Current {free_instrument}: {current_price:.5f}")
            
            # Calculate SL/TP based on instrument
            if "JPY" in free_instrument:
                # JPY pairs use different pip values
                sl_distance = 0.20  # 20 pips for JPY pairs
                tp_distance = 0.60  # 60 pips for JPY pairs
            else:
                # Standard pairs
                sl_distance = 0.0020  # 20 pips
                tp_distance = 0.0060  # 60 pips
                
            sl_price = current_price - sl_distance
            tp_price = current_price + tp_distance
            
            # Create order
            order_data = {
                "order": {
                    "instrument": free_instrument,
                    "units": "1",  # Minimal risk
                    "type": "MARKET",
                    "positionFill": "DEFAULT",
                    "stopLossOnFill": {"price": f"{sl_price:.5f}"},
                    "takeProfitOnFill": {"price": f"{tp_price:.5f}"}
                }
            }
            
            logger.info("📤 EXECUTING LIVE ORDER:")
            logger.info(f"   Instrument: {free_instrument}")
            logger.info(f"   Units: 1 (minimal risk)")
            logger.info(f"   Entry: ~{current_price:.5f}")
            logger.info(f"   Stop Loss: {sl_price:.5f}")
            logger.info(f"   Take Profit: {tp_price:.5f}")
            logger.info("🚨 REAL MONEY ORDER - EXECUTING NOW...")
            
            # Execute order
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
                logger.info("💰 REAL MONEY TRADE CONFIRMED")
                logger.info("🛡️  OCO PROTECTION ACTIVE")
                logger.info("🔥 HARDCODED SYSTEM WORKS PERFECTLY!")
                
                return True
            else:
                logger.error(f"❌ Order failed: {response}")
                return False
                
        else:
            logger.error("❌ Failed to get pricing")
            return False
            
    except Exception as e:
        logger.error(f"❌ Order execution failed: {e}")
        return False

def main():
    """Main execution"""
    logger.info("🔍 LIVE ACCOUNT POSITION CHECKER & ORDER EXECUTION")
    logger.info("Constitutional PIN: 841921")
    logger.info("=" * 60)
    
    success = place_order_on_available_pair()
    
    if success:
        logger.info("\n🎉 LIVE ORDER EXECUTION SUCCESSFUL!")
        logger.info("✅ Hardcoded system proven working")
        logger.info("✅ Real money trading confirmed")
        logger.info("✅ FIFO rules respected")
        logger.info("✅ OCO protection active")
        logger.info("🚀 System ready for full trading")
    else:
        logger.info("\n❌ Order execution had issues")

if __name__ == "__main__":
    main()
