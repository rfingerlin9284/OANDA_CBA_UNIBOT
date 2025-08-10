#!/usr/bin/env python3
"""
🧠 ML-ENHANCED OANDA SNIPER - HYBRID AI DECISION ENGINE
Integrates lightweight + heavy ML models with existing FVG strategy
"""

import sys
import os

# Add scripts directory to path for ML imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

try:
    from ml_hybrid_engine import ml_engine
    from oanda_feature_extractor import feature_extractor
    ML_ENABLED = True
    print("[✅] ML Hybrid Engine loaded successfully")
except ImportError as e:
    print(f"[⚠️] ML components not available: {e}")
    ML_ENABLED = False

# Import existing components
from sniper_core import SniperCore
from fvg_strategy import FVGStrategy
from capital_manager import capital_manager
from emergency_bail import is_bailout_triggered, record_trade_result
from timezone_manager import get_current_session, is_trading_session
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
from datetime import datetime
import time
import json

class MLEnhancedOANDASniper(SniperCore):
    """OANDA Sniper with ML hybrid decision engine"""
    
    def __init__(self):
        super().__init__()
        self.api = oandapyV20.API(access_token=os.getenv('OANDA_API_KEY'))
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        self.fvg_strategy = FVGStrategy()
        self.ml_confidence_threshold = 0.75
        self.trade_history = []
        
    def enhanced_trade_decision(self, pair_data, pair_name):
        """Enhanced trading decision using ML + FVG combination"""
        
        # Check emergency bail first
        if is_bailout_triggered():
            return False, "Emergency bail active"
        
        # Check session and trading hours
        if not is_trading_session():
            return False, "Outside trading hours"
        
        # Traditional FVG analysis
        fvg_signal = self.fvg_strategy.analyze(pair_data, pair_name)
        
        if not fvg_signal['signal']:
            return False, "No FVG signal"
        
        # ML Enhancement (if available)
        if ML_ENABLED:
            try:
                # Extract features for ML
                features = feature_extractor.extract_features(
                    pair_data, 
                    orderbook_data=self.get_orderbook_data(pair_name),
                    pair=pair_name
                )
                
                # Get ML prediction
                ml_decision = ml_engine.predict(features)
                confidence_scores = ml_engine.get_confidence_scores(features)
                
                # Combined decision logic
                if ml_decision and confidence_scores['heavy'] > self.ml_confidence_threshold:
                    decision_reason = f"ML+FVG: Heavy={confidence_scores['heavy']:.3f}, Light={confidence_scores['light']:.3f}"
                    return True, decision_reason
                else:
                    return False, f"ML rejected: Heavy={confidence_scores['heavy']:.3f} < {self.ml_confidence_threshold}"
                    
            except Exception as e:
                print(f"[⚠️] ML prediction failed: {e}, falling back to FVG only")
                return fvg_signal['signal'], "FVG only (ML failed)"
        else:
            # Fall back to FVG only if ML not available
            return fvg_signal['signal'], "FVG only (ML not loaded)"
    
    def get_orderbook_data(self, pair_name):
        """Get order book data for ML feature extraction"""
        try:
            r = pricing.PricingInfo(accountID=self.account_id, params={"instruments": pair_name})
            response = self.api.request(r)
            
            # Extract bid/ask data
            prices = response.get('prices', [])
            if prices:
                price_data = prices[0]
                return {
                    'bids': [[price_data.get('bids', [{}])[0].get('price', '0'), '1000']],
                    'asks': [[price_data.get('asks', [{}])[0].get('price', '0'), '1000']]
                }
        except Exception as e:
            print(f"[⚠️] Failed to get orderbook for {pair_name}: {e}")
        
        return None
    
    def execute_ml_trade(self, pair_name, signal_data, decision_reason):
        """Execute trade with ML-enhanced position sizing"""
        
        try:
            # Get current capital
            current_capital = capital_manager.get()
            if current_capital <= 0:
                return False, "Insufficient capital"
            
            # ML-enhanced position sizing
            base_risk = 0.02  # 2% base risk
            if ML_ENABLED:
                try:
                    confidence_scores = ml_engine.get_confidence_scores(features)
                    
                    # Adjust risk based on ML confidence
                    ml_multiplier = min(confidence_scores['heavy'] * 1.5, 2.0)
                    adjusted_risk = base_risk * ml_multiplier
                    
                except Exception as e:
                    print(f"[⚠️] ML position sizing failed: {e}")
                    adjusted_risk = base_risk
            else:
                adjusted_risk = base_risk
            
            # Calculate position size
            risk_amount = current_capital * adjusted_risk
            
            # Get current price
            r = pricing.PricingInfo(accountID=self.account_id, params={"instruments": pair_name})
            response = self.api.request(r)
            
            if not response.get('prices'):
                return False, "No price data available"
            
            current_price = float(response['prices'][0]['asks'][0]['price'])
            
            # Calculate position size based on risk
            stop_distance = signal_data.get('stop_distance', 0.001)
            position_size = int(risk_amount / stop_distance)
            
            # Limit position size
            max_position = int(current_capital * 0.1)  # Max 10% of capital
            position_size = min(position_size, max_position)
            
            if position_size < 100:  # Minimum position size
                return False, "Position size too small"
            
            # Create order
            side = signal_data.get('side', 'buy')
            order_data = {
                "order": {
                    "units": str(position_size if side == 'buy' else -position_size),
                    "instrument": pair_name,
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "stopLossOnFill": {
                        "price": str(current_price - stop_distance if side == 'buy' else current_price + stop_distance)
                    },
                    "takeProfitOnFill": {
                        "price": str(current_price + (stop_distance * 2) if side == 'buy' else current_price - (stop_distance * 2))
                    }
                }
            }
            
            # Execute order
            r = orders.OrderCreate(accountID=self.account_id, data=order_data)
            response = self.api.request(r)
            
            if response.get('orderFillTransaction'):
                trade_id = response['orderFillTransaction']['id']
                
                # Log trade
                trade_log = {
                    'timestamp': datetime.now().isoformat(),
                    'pair': pair_name,
                    'side': side,
                    'size': position_size,
                    'price': current_price,
                    'reason': decision_reason,
                    'trade_id': trade_id,
                    'ml_enhanced': ML_ENABLED
                }
                
                self.trade_history.append(trade_log)
                self.log_trade(trade_log)
                
                return True, f"Trade executed: {trade_id}"
            else:
                return False, f"Order failed: {response}"
                
        except Exception as e:
            return False, f"Trade execution failed: {e}"
    
        try:
            # This would typically call OANDA's candles endpoint
            # For now, return dummy data structure
            return [{
                'open': 1.0,
                'high': 1.002,
                'low': 0.998,
                'close': 1.001,
                'volume': 1000
            } for _ in range(count)]
        except Exception as e:
            print(f"[⚠️] Failed to get OHLC for {pair_name}: {e}")
            return []
    
    def log_trade(self, trade_data):
        """Log trade execution details"""
        log_entry = f"[{trade_data['timestamp']}] ML-ENHANCED TRADE: {trade_data['pair']} {trade_data['side']} {trade_data['size']} @ {trade_data['price']} | Reason: {trade_data['reason']}"
        
        with open("logs/trade_log.txt", "a") as f:
            f.write(log_entry + "\n")
        
        print(log_entry)
    
    def run_ml_enhanced_sniper(self):
        """Main ML-enhanced trading loop"""
        print("[🚀] Starting ML-Enhanced OANDA Sniper...")
        
        # OANDA major pairs
        pairs = [
            "EUR_USD", "GBP_USD", "USD_JPY", "USD_CHF",
            "AUD_USD", "USD_CAD", "NZD_USD", "EUR_GBP",
            "EUR_JPY", "GBP_JPY", "CHF_JPY", "AUD_JPY"
        ]
        
        trade_count = 0
        
        while True:
            try:
                session_info = get_current_session()
                print(f"[📊] Current session: {session_info['name']} | Capital: ${capital_manager.get():.2f}")
                
                if is_bailout_triggered():
                    print("[⛔] Emergency bail triggered - pausing trading")
                    time.sleep(300)  # Wait 5 minutes
                    continue
                
                for pair in pairs:
                    try:
                        # Get market data
                        
                        if not pair_data:
                            continue
                        
                        # Enhanced decision making
                        should_trade, reason = self.enhanced_trade_decision(pair_data, pair)
                        
                        if should_trade:
                            # Create signal data
                            signal_data = {
                                'side': 'buy',  # Simplified for this example
                                'stop_distance': 0.001,
                                'confidence': 0.8
                            }
                            
                            success, result = self.execute_ml_trade(pair, signal_data, reason)
                            
                            if success:
                                trade_count += 1
                                print(f"[✅] Trade #{trade_count}: {result}")
                                record_trade_result(True)  # Assume success for now
                            else:
                                print(f"[❌] Trade failed: {result}")
                    
                    except Exception as e:
                        print(f"[⚠️] Error processing {pair}: {e}")
                        continue
                    
                    time.sleep(1)  # Brief pause between pairs
                
                print(f"[💤] Cycle complete. Sleeping 30 seconds...")
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("[🛑] ML-Enhanced OANDA Sniper stopped by user")
                break
            except Exception as e:
                print(f"[❌] Unexpected error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    sniper = MLEnhancedOANDASniper()
    sniper.run_ml_enhanced_sniper()
