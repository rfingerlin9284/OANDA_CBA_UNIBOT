#!/usr/bin/env python3
"""
🛡️ TRADE EDGE VALIDATOR
Prevents micro-loss drift by enforcing high-quality trade standards
"""

import json
import requests
import numpy as np
from datetime import datetime

class TradeEdgeValidator:
    def __init__(self, config_path="small_cap_config_oanda.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.api_key = self.config["api_key"]
        self.account_id = self.config["account_id"]
        self.base_url = "https://api-fxtrade.oanda.com"
        
        # Edge validation thresholds
        self.min_edge_ratio = 2.5  # Minimum expected profit vs risk
        self.min_pip_distance = 20  # Minimum pips from entry to TP
        self.max_correlation = 0.8  # Maximum allowed correlation with existing trades
        
        print("🛡️ Trade Edge Validator ACTIVATED")
        print(f"   Min Edge Ratio: {self.min_edge_ratio}:1")
        print(f"   Min Pip Distance: {self.min_pip_distance}")

    def get_current_price(self, pair):
        """Get current bid/ask prices"""
        url = f"{self.base_url}/v3/accounts/{self.account_id}/pricing"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"instruments": pair}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if 'prices' in data and len(data['prices']) > 0:
                price_data = data['prices'][0]
                bid = float(price_data['bids'][0]['price'])
                ask = float(price_data['asks'][0]['price'])
                mid = (bid + ask) / 2
                spread = ask - bid
                
                return {
                    'bid': bid,
                    'ask': ask,
                    'mid': mid,
                    'spread': spread,
                    'spread_pips': spread * 10000
                }
        except Exception as e:
            print(f"⚠️ Price fetch error for {pair}: {e}")
            return None

    def calculate_volatility_bands(self, pair, periods=20):
        """Calculate volatility bands for dynamic SL/TP"""
        url = f"{self.base_url}/v3/instruments/{pair}/candles"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "count": periods,
            "granularity": "H1"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            closes = [float(candle['mid']['c']) for candle in data['candles']]
            highs = [float(candle['mid']['h']) for candle in data['candles']]
            lows = [float(candle['mid']['l']) for candle in data['candles']]
            
            # Calculate ATR
            true_ranges = []
            for i in range(1, len(highs)):
                tr1 = highs[i] - lows[i]
                tr2 = abs(highs[i] - closes[i-1])
                tr3 = abs(lows[i] - closes[i-1])
                true_ranges.append(max(tr1, tr2, tr3))
            
            atr = np.mean(true_ranges)
            volatility_pips = atr * 10000
            
            return {
                'atr': atr,
                'volatility_pips': volatility_pips,
                'dynamic_sl': max(volatility_pips * 1.5, 25),  # Min 25 pips
                'dynamic_tp': max(volatility_pips * 3.0, 50)   # Min 50 pips
            }
            
        except Exception as e:
            print(f"⚠️ Volatility calculation error for {pair}: {e}")
            return {
                'atr': 0.001,
                'volatility_pips': 10,
                'dynamic_sl': 25,
                'dynamic_tp': 50
            }

    def validate_trade_edge(self, pair, direction, ml_confidence, current_price=None):
        """
        Main validation function - returns True only for high-edge trades
        """
        print(f"\n🛡️ EDGE VALIDATION: {pair} {direction.upper()}")
        
        # Get current pricing if not provided
        if current_price is None:
            price_data = self.get_current_price(pair)
            if not price_data:
                print("❌ REJECTED: Unable to get current price")
                return False, {}
            current_price = price_data['mid']
            spread_pips = price_data['spread_pips']
        else:
            spread_pips = 2.0  # Default spread assumption
        
        # Get volatility data
        vol_data = self.calculate_volatility_bands(pair)
        
        # 1. CONFIDENCE FILTER
        min_confidence = 0.87
        if ml_confidence < min_confidence:
            print(f"❌ REJECTED: ML Confidence {ml_confidence:.3f} < {min_confidence}")
            return False, {}
        
        # 2. SPREAD FILTER
        max_spread_pips = 5.0
        if spread_pips > max_spread_pips:
            print(f"❌ REJECTED: Spread {spread_pips:.1f} pips > {max_spread_pips}")
            return False, {}
        
        # 3. DYNAMIC SL/TP CALCULATION
        sl_pips = vol_data['dynamic_sl']
        tp_pips = vol_data['dynamic_tp']
        
        # Ensure minimum edge ratio
        if tp_pips / sl_pips < self.min_edge_ratio:
            tp_pips = sl_pips * self.min_edge_ratio
        
        # Calculate actual prices
        if direction.lower() == "buy":
            entry_price = current_price
            stop_loss = entry_price - (sl_pips / 10000)
            take_profit = entry_price + (tp_pips / 10000)
        else:
            entry_price = current_price
            stop_loss = entry_price + (sl_pips / 10000)
            take_profit = entry_price - (tp_pips / 10000)
        
        # 4. EDGE RATIO VALIDATION
        risk_pips = abs((entry_price - stop_loss) * 10000)
        reward_pips = abs((take_profit - entry_price) * 10000)
        edge_ratio = reward_pips / risk_pips if risk_pips > 0 else 0
        
        if edge_ratio < self.min_edge_ratio:
            print(f"❌ REJECTED: Edge ratio {edge_ratio:.2f} < {self.min_edge_ratio}")
            return False, {}
        
        # 5. MINIMUM DISTANCE FILTER
        if reward_pips < self.min_pip_distance:
            print(f"❌ REJECTED: Reward {reward_pips:.1f} pips < {self.min_pip_distance}")
            return False, {}
        
        # 6. POSITION SIZE CALCULATION (confidence-based)
        base_units = 2000
        confidence_multiplier = ((ml_confidence - 0.85) / 0.15) * 2 + 1  # 1x to 3x scaling
        confidence_multiplier = min(max(confidence_multiplier, 1.0), 3.0)
        position_size = int(base_units * confidence_multiplier)
        
        # All validations passed
        trade_data = {
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'position_size': position_size,
            'risk_pips': risk_pips,
            'reward_pips': reward_pips,
            'edge_ratio': edge_ratio,
            'confidence_multiplier': confidence_multiplier,
            'volatility_pips': vol_data['volatility_pips']
        }
        
        print(f"✅ APPROVED: Edge {edge_ratio:.2f}, Risk {risk_pips:.1f}p, Reward {reward_pips:.1f}p")
        print(f"   Position: {position_size} units ({confidence_multiplier:.1f}x confidence scaling)")
        print(f"   Volatility: {vol_data['volatility_pips']:.1f} pips")
        
        return True, trade_data

    def check_portfolio_correlation(self, new_pair, new_direction):
        """Check if new trade correlates with existing positions"""
        try:
            # Get current positions
            url = f"{self.base_url}/v3/accounts/{self.account_id}/positions"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            data = response.json()
            
            # Analyze currency exposure
            currency_exposure = {}
            for pos in data.get('positions', []):
                if float(pos['long']['units']) != 0 or float(pos['short']['units']) != 0:
                    pair = pos['instrument']
                    net_units = float(pos['long']['units']) + float(pos['short']['units'])
                    
                    base_curr = pair[:3]
                    quote_curr = pair[4:7]
                    
                    if net_units > 0:  # Long position
                        currency_exposure[base_curr] = currency_exposure.get(base_curr, 0) + 1
                        currency_exposure[quote_curr] = currency_exposure.get(quote_curr, 0) - 1
                    else:  # Short position
                        currency_exposure[base_curr] = currency_exposure.get(base_curr, 0) - 1
                        currency_exposure[quote_curr] = currency_exposure.get(quote_curr, 0) + 1
            
            # Check new trade impact
            new_base = new_pair[:3]
            new_quote = new_pair[4:7]
            
            if new_direction.lower() == "buy":
                new_base_exp = currency_exposure.get(new_base, 0) + 1
                new_quote_exp = currency_exposure.get(new_quote, 0) - 1
            else:
                new_base_exp = currency_exposure.get(new_base, 0) - 1
                new_quote_exp = currency_exposure.get(new_quote, 0) + 1
            
            # Correlation limits
            max_single_exposure = 3
            if abs(new_base_exp) > max_single_exposure or abs(new_quote_exp) > max_single_exposure:
                print(f"❌ REJECTED: Currency overexposure - {new_base}: {new_base_exp}, {new_quote}: {new_quote_exp}")
                return False
            
            return True
            
        except Exception as e:
            print(f"⚠️ Correlation check error: {e}")
            return True  # Allow trade if check fails

def integrate_edge_validator():
    """Function to integrate with main trading system"""
    validator = TradeEdgeValidator()
    
    print("\n🛡️ TRADE EDGE VALIDATOR INTEGRATION COMPLETE")
    print("🔍 Now enforcing high-edge trades only...")
    
    return validator

if __name__ == "__main__":
    # Test the validator
    validator = integrate_edge_validator()
    
    # Test validation on common pairs
        print(f"\n🧪 Testing {pair}...")
        is_valid, trade_data = validator.validate_trade_edge(pair, "buy", 0.89)
        if is_valid:
            print(f"   ✅ Would execute with {trade_data['position_size']} units")
        else:
            print(f"   ❌ Trade rejected")
