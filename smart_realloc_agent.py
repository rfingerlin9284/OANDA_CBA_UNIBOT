#!/usr/bin/env python3
# 🔄 Smart Reallocation Agent - Intelligent capital redeployer
# Redeploys capital from failed/killed trades to better opportunities

import logging
from datetime import datetime
import json

class SmartReallocAgent:
    def __init__(self, min_realloc_confidence=0.75, max_realloc_attempts=3):
        self.min_realloc_confidence = min_realloc_confidence
        self.max_realloc_attempts = max_realloc_attempts
        self.reallocation_history = []
        
    def reallocate_on_kill(self, trade_data, ml_model, router):
        """
        Intelligently redeploy capital from killed trades
        Returns: (success: bool, new_trades: list, reason: str)
        """
        try:
            bad_trade_amount = trade_data.get('capital_used', 0)
            symbol = trade_data.get('symbol', 'UNKNOWN')
            kill_reason = trade_data.get('kill_reason', 'Unknown')
            
            logging.info(f"🔄 REALLOCATION TRIGGERED: {symbol} killed ({kill_reason}), ${bad_trade_amount} to redeploy")
            
            # Get top opportunities from ML model
            top_opps = self.get_top_opportunities(ml_model, min_conf=self.min_realloc_confidence, limit=5)
            
            if not top_opps:
                reason = f"❌ NO REALLOCATION: No opportunities above {self.min_realloc_confidence:.0%} confidence"
                logging.warning(reason)
                return False, [], reason
            
            # Filter out the same symbol that just failed
            filtered_opps = [opp for opp in top_opps if opp.get('symbol') != symbol]
            
            if not filtered_opps:
                reason = f"❌ NO REALLOCATION: All top opportunities are same symbol ({symbol})"
                logging.warning(reason)
                return False, [], reason
            
            # Select best opportunity
            best_opp = filtered_opps[0]
            
            # Calculate reallocation amount (slightly reduced to account for fees)
            realloc_amount = bad_trade_amount * 0.95  # 5% buffer for fees
            
            # Execute reallocation
            success = self.execute_reallocation(best_opp, realloc_amount, router)
            
            if success:
                reason = f"✅ REALLOCATION SUCCESS: ${realloc_amount:.2f} → {best_opp['symbol']} (conf: {best_opp['confidence']:.1%})"
                new_trades = [best_opp]
                self.log_reallocation(trade_data, best_opp, realloc_amount, "SUCCESS")
            else:
                reason = f"❌ REALLOCATION FAILED: Could not execute trade for {best_opp['symbol']}"
                new_trades = []
                self.log_reallocation(trade_data, best_opp, realloc_amount, "FAILED")
            
            logging.info(reason)
            return success, new_trades, reason
            
        except Exception as e:
            reason = f"❌ REALLOCATION ERROR: {str(e)}"
            logging.error(reason)
            return False, [], reason
    
    def get_top_opportunities(self, ml_model, min_conf=0.75, limit=5):
        """Get top trading opportunities from ML model"""
        try:
            # This would interface with your actual ML model
            # For now, return mock data structure
            opportunities = []
            
            # Mock implementation - replace with actual ML model call
            mock_symbols = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'NZD_USD']
            
            for i, symbol in enumerate(mock_symbols[:limit]):
                if hasattr(ml_model, 'predict'):
                    # Use actual ML model if available
                    prediction = ml_model.predict(symbol)
                else:
                    # Mock prediction
                    confidence = 0.65 + (i * 0.05)  # Decreasing confidence
                    prediction = {
                        'symbol': symbol,
                        'confidence': confidence,
                        'expected_return': 0.008 - (i * 0.001),
                        'strategy_id': f'strat_{i+1}',
                        'direction': 'BUY' if i % 2 == 0 else 'SELL'
                    }
                
                if prediction.get('confidence', 0) >= min_conf:
                    opportunities.append(prediction)
            
            # Sort by approval score (confidence * expected return)
            opportunities.sort(key=lambda x: x.get('confidence', 0) * x.get('expected_return', 0), reverse=True)
            
            return opportunities[:limit]
            
        except Exception as e:
            logging.error(f"Error getting ML opportunities: {e}")
            return []
    
    def execute_reallocation(self, opportunity, amount, router):
        """Execute the reallocation trade"""
        try:
            symbol = opportunity['symbol']
            direction = opportunity.get('direction', 'BUY')
            
            # Calculate position size based on amount and direction
            units = amount * 1000 if direction == 'BUY' else -amount * 1000  # Simple unit calculation
            
            # Mock price calculation - replace with actual market data
            price = 1.1000  # This should come from real market data
            sl = price * 0.998 if direction == 'BUY' else price * 1.002
            tp = price * 1.005 if direction == 'BUY' else price * 0.995
            
            # Use router to place the trade
            if hasattr(router, 'place_order'):
                success = router.place_order(symbol, units, price, sl, tp)
                return success
            else:
                logging.warning("Router doesn't have place_order method")
                return False
                
        except Exception as e:
            logging.error(f"Error executing reallocation: {e}")
            return False
    
    def log_reallocation(self, original_trade, new_opportunity, amount, status):
        """Log reallocation attempts for analysis"""
        reallocation = {
            'timestamp': datetime.now().isoformat(),
            'original_symbol': original_trade.get('symbol'),
            'original_amount': original_trade.get('capital_used'),
            'kill_reason': original_trade.get('kill_reason'),
            'new_symbol': new_opportunity['symbol'],
            'new_confidence': new_opportunity['confidence'],
            'realloc_amount': amount,
            'status': status
        }
        
        self.reallocation_history.append(reallocation)
        
        # Keep only last 50 reallocations
        if len(self.reallocation_history) > 50:
            self.reallocation_history = self.reallocation_history[-50:]
    
    def get_reallocation_stats(self):
        """Get reallocation performance statistics"""
        if not self.reallocation_history:
            return {"total_reallocations": 0}
        
        recent = self.reallocation_history[-20:]
        successful = len([r for r in recent if r['status'] == 'SUCCESS'])
        
        return {
            "total_reallocations": len(self.reallocation_history),
            "recent_reallocations": len(recent),
            "success_rate": successful / len(recent) if recent else 0,
            "avg_confidence": sum(r['new_confidence'] for r in recent) / len(recent) if recent else 0
        }
