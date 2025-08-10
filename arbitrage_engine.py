#!/usr/bin/env python3
"""
⚡ ARBITRAGE ENGINE
24/7 Coinbase Spot vs OANDA Forex Arbitrage
Hamilton, NJ Timezone-Aware Trading
"""

import time
import threading
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

from logger import logger, log_trade, log_error

@dataclass
class ArbitrageOpportunity:
    """Data class for arbitrage opportunities"""
    pair: str
    coinbase_price: float
    oanda_price: float
    spread_pct: float
    profit_potential: float
    direction: str  # 'long_cb_short_oanda' or 'long_oanda_short_cb'
    timestamp: datetime
    confidence: float

class ArbitrageEngine:
    """
    ⚡ ARBITRAGE ENGINE
    Detects and executes arbitrage between Coinbase spot and OANDA forex
    """
    
    def __init__(self, coinbase_api, oanda_api, credentials, session_manager, portfolio_manager):
        """Initialize arbitrage engine"""
        self.coinbase = coinbase_api
        self.oanda = oanda_api
        self.creds = credentials
        self.session_manager = session_manager
        self.portfolio_manager = portfolio_manager
        
        # Arbitrage parameters
        self.min_spread_pct = 0.15  # Minimum 0.15% spread to consider
        self.max_spread_pct = 5.0   # Maximum 5% spread (safety)
        self.min_profit_usd = 10.0  # Minimum $10 profit potential
        self.max_position_size = 1000.0  # Maximum $1000 per arbitrage
        
        # Trading pairs for arbitrage (crypto pairs available on both platforms)
        self.arbitrage_pairs = [
            'BTC/USD', 'ETH/USD', 'LTC/USD', 'BCH/USD',
            'EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF',
            'AUD/USD', 'USD/CAD', 'NZD/USD'
        ]
        
        # Tracking
        self.active_arbitrages = {}
        self.opportunities_found = 0
        self.trades_executed = 0
        self.total_profit = 0.0
        
        # Threading
        self.is_running = False
        self.scan_thread = None
        
        logger.info("⚡ Arbitrage Engine initialized")
    
    def start_scanning(self):
        """Start 24/7 arbitrage scanning"""
        if self.is_running:
            logger.warning("Arbitrage engine already running")
            return
        
        self.is_running = True
        self.scan_thread = threading.Thread(target=self._arbitrage_loop, daemon=True)
        self.scan_thread.start()
        
        log_trade("⚡ ARBITRAGE ENGINE STARTED - 24/7 scanning", "ARBITRAGE")
    
    def stop_scanning(self):
        """Stop arbitrage scanning"""
        self.is_running = False
        if self.scan_thread:
            self.scan_thread.join(timeout=5)
        
        log_trade("⚡ ARBITRAGE ENGINE STOPPED", "ARBITRAGE")
    
    def _arbitrage_loop(self):
        """Main arbitrage scanning loop"""
        scan_count = 0
        
        while self.is_running:
            try:
                scan_count += 1
                
                # Get current market session
                session_info = self.session_manager.get_current_session_info()
                current_session = session_info['current_session']
                
                # Adjust scanning frequency based on market session
                if current_session in ['london', 'new_york']:
                    scan_interval = 5  # 5 seconds during major sessions
                elif current_session == 'china':
                    scan_interval = 10  # 10 seconds during China session
                else:
                    scan_interval = 30  # 30 seconds during off hours
                
                # Log scanning status every 50 scans
                if scan_count % 50 == 0:
                    log_trade(f"⚡ Arbitrage Scan #{scan_count} [{current_session}] | Opportunities: {self.opportunities_found} | Executed: {self.trades_executed} | Profit: ${self.total_profit:.2f}", "ARBITRAGE")
                
                # Scan for arbitrage opportunities
                opportunities = self._scan_arbitrage_opportunities()
                
                # Execute profitable opportunities
                for opportunity in opportunities:
                    if self._should_execute_arbitrage(opportunity):
                        self._execute_arbitrage(opportunity)
                
                # Clean up expired opportunities
                self._cleanup_old_opportunities()
                
                time.sleep(scan_interval)
                
            except Exception as e:
                log_error(f"Arbitrage scanning error: {str(e)}", "ARBITRAGE")
                time.sleep(10)  # Wait 10 seconds before retrying
    
    def _scan_arbitrage_opportunities(self) -> List[ArbitrageOpportunity]:
        """Scan for arbitrage opportunities"""
        opportunities = []
        
        for pair in self.arbitrage_pairs:
            try:
                # Get prices from both platforms
                cb_price = self._get_coinbase_price(pair)
                oanda_price = self._get_oanda_price(pair)
                
                if cb_price and oanda_price:
                    opportunity = self._calculate_arbitrage(pair, cb_price, oanda_price)
                    if opportunity:
                        opportunities.append(opportunity)
                        self.opportunities_found += 1
                
            except Exception as e:
                log_error(f"Error scanning {pair}: {str(e)}", "ARBITRAGE")
                continue
        
        return opportunities
    
    def _get_coinbase_price(self, pair: str) -> Optional[float]:
        """Get current price from Coinbase"""
        try:
            ticker = self.coinbase.fetch_ticker(pair)
            return float(ticker['last'])
        except Exception as e:
            log_error(f"Error fetching Coinbase price for {pair}: {str(e)}", "ARBITRAGE")
            return None
    
    def _get_oanda_price(self, pair: str) -> Optional[float]:
        """Get current price from OANDA"""
        try:
            # Convert pair format for OANDA (BTC/USD -> BTC_USD)
            oanda_pair = pair.replace('/', '_')
            
            # Fetch current price from OANDA
            from oandapyV20.endpoints.pricing import PricingInfo
            
            params = {"instruments": oanda_pair}
            request = PricingInfo(accountID=self.creds.OANDA_ACCOUNT_ID, params=params)
            response = self.oanda.request(request)
            
            if response['prices']:
                price_data = response['prices'][0]
                # Use mid price for arbitrage calculation
                bid = float(price_data['bids'][0]['price'])
                ask = float(price_data['asks'][0]['price'])
                return (bid + ask) / 2.0
            
            return None
            
        except Exception as e:
            log_error(f"Error fetching OANDA price for {pair}: {str(e)}", "ARBITRAGE")
            return None
    
    def _calculate_arbitrage(self, pair: str, cb_price: float, oanda_price: float) -> Optional[ArbitrageOpportunity]:
        """Calculate arbitrage opportunity"""
        try:
            # Calculate spread
            spread_pct = abs(cb_price - oanda_price) / min(cb_price, oanda_price) * 100
            
            # Check if spread meets minimum threshold
            if spread_pct < self.min_spread_pct or spread_pct > self.max_spread_pct:
                return None
            
            # Determine direction
            if cb_price > oanda_price:
                direction = 'short_cb_long_oanda'
                profit_potential = (cb_price - oanda_price) * self.max_position_size / cb_price
            else:
                direction = 'long_cb_short_oanda'
                profit_potential = (oanda_price - cb_price) * self.max_position_size / oanda_price
            
            # Check minimum profit threshold
            if profit_potential < self.min_profit_usd:
                return None
            
            # Calculate confidence based on spread size and market session
            session_info = self.session_manager.get_current_session_info()
            base_confidence = min(spread_pct / 1.0, 1.0)  # Higher spread = higher confidence
            
            # Boost confidence during major trading sessions
            if session_info['current_session'] in ['london', 'new_york']:
                confidence = min(base_confidence * 1.2, 1.0)
            else:
                confidence = base_confidence
            
            return ArbitrageOpportunity(
                pair=pair,
                coinbase_price=cb_price,
                oanda_price=oanda_price,
                spread_pct=spread_pct,
                profit_potential=profit_potential,
                direction=direction,
                timestamp=datetime.now(),
                confidence=confidence
            )
            
        except Exception as e:
            log_error(f"Error calculating arbitrage for {pair}: {str(e)}", "ARBITRAGE")
            return None
    
    def _should_execute_arbitrage(self, opportunity: ArbitrageOpportunity) -> bool:
        """Determine if arbitrage should be executed"""
        try:
            # Check if we already have a position in this pair
            if opportunity.pair in self.active_arbitrages:
                return False
            
            # Check portfolio balance
            balances = self.portfolio_manager.get_total_balances()
            if balances['total_usd'] < self.max_position_size * 2:  # Need 2x for both sides
                return False
            
            # Check confidence threshold
            if opportunity.confidence < 0.7:  # Require 70% confidence
                return False
            
            # Check market session - be more conservative during off hours
            session_info = self.session_manager.get_current_session_info()
            if session_info['current_session'] == 'off_hours' and opportunity.spread_pct < 0.3:
                return False  # Require higher spread during off hours
            
            return True
            
        except Exception as e:
            log_error(f"Error evaluating arbitrage: {str(e)}", "ARBITRAGE")
            return False
    
    def _execute_arbitrage(self, opportunity: ArbitrageOpportunity):
        """Execute arbitrage trade"""
        try:
            log_trade(f"⚡ EXECUTING ARBITRAGE: {opportunity.pair} | Spread: {opportunity.spread_pct:.2f}% | Profit: ${opportunity.profit_potential:.2f}", "ARBITRAGE")
            
            # Calculate position sizes
            position_size = min(self.max_position_size, opportunity.profit_potential * 50)  # Conservative sizing
            
            # Execute both sides of the arbitrage
            if opportunity.direction == 'long_cb_short_oanda':
                # Buy on Coinbase, sell on OANDA
                cb_order = self._place_coinbase_order(opportunity.pair, 'buy', position_size)
                oanda_order = self._place_oanda_order(opportunity.pair, 'sell', position_size)
            else:
                # Sell on Coinbase, buy on OANDA
                cb_order = self._place_coinbase_order(opportunity.pair, 'sell', position_size)
                oanda_order = self._place_oanda_order(opportunity.pair, 'buy', position_size)
            
            # Track the arbitrage
            if cb_order and oanda_order:
                self.active_arbitrages[opportunity.pair] = {
                    'opportunity': opportunity,
                    'coinbase_order': cb_order,
                    'oanda_order': oanda_order,
                    'timestamp': datetime.now(),
                    'position_size': position_size
                }
                
                self.trades_executed += 1
                self.total_profit += opportunity.profit_potential
                
                log_trade(f"✅ ARBITRAGE EXECUTED: {opportunity.pair} | Orders placed on both platforms", "ARBITRAGE")
            else:
                log_error(f"Failed to execute arbitrage for {opportunity.pair}", "ARBITRAGE")
                
        except Exception as e:
            log_error(f"Error executing arbitrage: {str(e)}", "ARBITRAGE")
    
    def _place_coinbase_order(self, pair: str, side: str, amount: float) -> Optional[dict]:
        """Place order on Coinbase"""
        try:
            # Implementation depends on your existing order placement logic
            # This is a placeholder - integrate with your actual Coinbase order system
            log_trade(f"📋 Coinbase {side} order: {pair} | Amount: ${amount:.2f}", "ARBITRAGE")
            return {"id": f"cb_{datetime.now().timestamp()}", "status": "filled"}
        except Exception as e:
            log_error(f"Coinbase order error: {str(e)}", "ARBITRAGE")
            return None
    
    def _place_oanda_order(self, pair: str, side: str, amount: float) -> Optional[dict]:
        """Place order on OANDA"""
        try:
            # Implementation depends on your existing order placement logic
            # This is a placeholder - integrate with your actual OANDA order system
            log_trade(f"📋 OANDA {side} order: {pair} | Amount: ${amount:.2f}", "ARBITRAGE")
            return {"id": f"oanda_{datetime.now().timestamp()}", "status": "filled"}
        except Exception as e:
            log_error(f"OANDA order error: {str(e)}", "ARBITRAGE")
            return None
    
    def _cleanup_old_opportunities(self):
        """Clean up old arbitrage positions"""
        try:
            current_time = datetime.now()
            expired_pairs = []
            
            for pair, arbitrage_data in self.active_arbitrages.items():
                # Close arbitrage after 1 hour or if profitable
                if current_time - arbitrage_data['timestamp'] > timedelta(hours=1):
                    expired_pairs.append(pair)
            
            for pair in expired_pairs:
                self._close_arbitrage(pair)
                
        except Exception as e:
            log_error(f"Error cleaning up arbitrages: {str(e)}", "ARBITRAGE")
    
    def _close_arbitrage(self, pair: str):
        """Close an arbitrage position"""
        try:
            if pair in self.active_arbitrages:
                arbitrage_data = self.active_arbitrages[pair]
                
                # Close both positions (implementation needed)
                log_trade(f"🔄 CLOSING ARBITRAGE: {pair}", "ARBITRAGE")
                
                # Remove from active arbitrages
                del self.active_arbitrages[pair]
                
        except Exception as e:
            log_error(f"Error closing arbitrage for {pair}: {str(e)}", "ARBITRAGE")
    
    def get_arbitrage_stats(self) -> Dict:
        """Get arbitrage statistics"""
        return {
            'opportunities_found': self.opportunities_found,
            'trades_executed': self.trades_executed,
            'total_profit': self.total_profit,
            'active_arbitrages': len(self.active_arbitrages),
            'is_running': self.is_running
        }
