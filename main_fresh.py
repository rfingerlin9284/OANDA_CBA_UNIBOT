#!/usr/bin/env python3
"""
Fresh Main Trading Bot - Live Mode Only
Per OANDA deployment manual - PIN 841921
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Import fresh modules
from guardian_fresh import verify_live_mode, validate_credentials
from router_fresh import OandaRouter

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/fresh_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FreshTradingBot:
    def __init__(self):
        """Initialize fresh trading bot"""
        # Verify live mode first
        verify_live_mode()
        
        if not validate_credentials():
            logger.error("❌ Credential validation failed")
            sys.exit(1)
        
        self.router = OandaRouter()
        self.running = True
        self.account_min = float(os.getenv("ACCOUNT_MIN", "3000"))
        self.max_risk = float(os.getenv("MAX_RISK_PER_TRADE", "0.02"))
        self.max_trades_per_day = int(os.getenv("MAX_TRADES_PER_DAY", "2"))
        self.pairs = os.getenv("TOP_PAIRS", "EUR_USD,USD_JPY,GBP_USD").split(",")
        
        logger.info("✅ Fresh Trading Bot initialized - LIVE MODE ONLY")
    
    def calculate_position_size(self, balance, risk_percent=0.02):
        """Calculate position size based on account balance"""
        if balance < self.account_min:
            logger.warning(f"⚠️ Balance ${balance:.2f} below minimum ${self.account_min}")
            return 0
        
        risk_amount = balance * risk_percent
        # Conservative position sizing for small accounts
        position_size = min(1000, int(risk_amount * 10))  # Max 1000 units
        return position_size
    
    def run_trading_cycle(self):
        """Main trading cycle"""
        logger.info("🚀 Starting fresh trading cycle")
        
        while self.running:
            try:
                # Get account status
                balance = self.router.get_account_balance()
                positions = self.router.get_open_positions()
                
                logger.info(f"💰 Balance: ${balance:.2f} | Positions: {len(positions)}")
                
                # Safety checks
                if balance < self.account_min:
                    logger.error(f"❌ Balance too low: ${balance:.2f}")
                    time.sleep(300)  # Wait 5 minutes
                    continue
                
                if len(positions) >= self.max_trades_per_day:
                    logger.info(f"📊 Max trades reached: {len(positions)}")
                    time.sleep(300)
                    continue
                
                # Simple EUR/USD trade example (replace with your strategy)
                if len(positions) == 0:  # Only if no open positions
                    position_size = self.calculate_position_size(balance)
                    if position_size > 0:
                        # Example trade parameters (replace with real strategy)
                        entry_price = 1.0900  # Example
                        take_profit = 1.0920   # +20 pips
                        stop_loss = 1.0880     # -20 pips
                        
                        logger.info(f"📈 Attempting EUR_USD trade: {position_size} units")
                        
                        # Place OCO order
                        result = self.router.place_oco_order(
                            pair="EUR_USD",
                            direction="BUY", 
                            units=position_size,
                            entry_price=entry_price,
                            take_profit=take_profit,
                            stop_loss=stop_loss
                        )
                        
                        if result:
                            logger.info("✅ Trade placed successfully")
                        else:
                            logger.error("❌ Trade placement failed")
                
                # Wait before next cycle
                time.sleep(60)  # 1 minute cycle
                
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown requested")
                self.running = False
                break
            except Exception as e:
                logger.error(f"❌ Trading cycle error: {e}")
                time.sleep(30)

def main():
    """Main entry point"""
    logger.info("🚀 Fresh OANDA Trading Bot Starting - LIVE MODE")
    logger.info("📋 PIN 841921 Required - Live Trading Only")
    
    try:
        bot = FreshTradingBot()
        bot.run_trading_cycle()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
