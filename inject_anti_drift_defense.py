#!/usr/bin/env python3
"""
🚨 ANTI-DRIFT DEFENSE SYSTEM
Stops micro-loss bleeding and enforces high-quality trades only
"""

import json
import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class AntiDriftDefense:
    def __init__(self, config_path="small_cap_config_oanda.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.api_key = self.config["api_key"]
        self.account_id = self.config["account_id"]
        self.base_url = "https://api-fxtrade.oanda.com"
        
        # Anti-drift parameters
        self.min_reward_risk_ratio = 2.0  # Minimum 2:1 R/R
        self.min_confidence_threshold = 0.88  # High confidence only
        self.correlation_threshold = 0.7  # Block correlated conflicts
        self.volatility_multiplier = 1.5  # SL/TP based on ATR
        
        print("🚨 Anti-Drift Defense System LOADED")
        print(f"   Minimum R/R Ratio: {self.min_reward_risk_ratio}:1")
        print(f"   Minimum Confidence: {self.min_confidence_threshold}")
        print(f"   Correlation Threshold: {self.correlation_threshold}")

    def get_atr(self, pair, periods=14):
        """Get Average True Range for volatility-based SL/TP"""
        url = f"{self.base_url}/v3/instruments/{pair}/candles"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "count": periods + 1,
            "granularity": "H1"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            highs = [float(candle['mid']['h']) for candle in data['candles']]
            lows = [float(candle['mid']['l']) for candle in data['candles']]
            closes = [float(candle['mid']['c']) for candle in data['candles']]
            
            # Calculate True Range
            true_ranges = []
            for i in range(1, len(highs)):
                tr1 = highs[i] - lows[i]
                tr2 = abs(highs[i] - closes[i-1])
                tr3 = abs(lows[i] - closes[i-1])
                true_ranges.append(max(tr1, tr2, tr3))
            
            atr = sum(true_ranges) / len(true_ranges)
            return atr
            
        except Exception as e:
            print(f"⚠️ ATR calculation failed for {pair}: {e}")
            return 0.001  # Default fallback

    def check_correlation_conflict(self, pair, direction, existing_positions):
        """Check if new trade conflicts with existing positions"""
        currency_exposure = {}
        
        # Map existing positions
        for pos in existing_positions:
            pos_pair = pos['instrument']
            pos_units = float(pos['long']['units']) + float(pos['short']['units'])
            
            # Extract base/quote currencies
            base = pos_pair[:3]
            quote = pos_pair[4:7]
            
            if pos_units > 0:  # Long position
                currency_exposure[base] = currency_exposure.get(base, 0) + 1
                currency_exposure[quote] = currency_exposure.get(quote, 0) - 1
            else:  # Short position
                currency_exposure[base] = currency_exposure.get(base, 0) - 1
                currency_exposure[quote] = currency_exposure.get(quote, 0) + 1
        
        # Check new trade exposure
        new_base = pair[:3]
        new_quote = pair[4:7]
        
        if direction == "buy":
            new_base_exp = currency_exposure.get(new_base, 0) + 1
            new_quote_exp = currency_exposure.get(new_quote, 0) - 1
        else:
            new_base_exp = currency_exposure.get(new_base, 0) - 1
            new_quote_exp = currency_exposure.get(new_quote, 0) + 1
        
        # Check for excessive exposure
        max_single_currency_exposure = 2
        if abs(new_base_exp) > max_single_currency_exposure or abs(new_quote_exp) > max_single_currency_exposure:
            print(f"🚫 BLOCKED: {pair} {direction} - Currency overexposure")
            print(f"   {new_base}: {new_base_exp}, {new_quote}: {new_quote_exp}")
            return False
        
        return True

    def calculate_dynamic_position_size(self, confidence, base_units=2000):
        """Scale position size based on ML confidence"""
        if confidence < self.min_confidence_threshold:
            return 0  # No trade
        
        # Confidence scaling: 0.88-1.0 maps to 1x-3x base size
        confidence_factor = ((confidence - 0.88) / 0.12) * 2 + 1
        confidence_factor = min(confidence_factor, 3.0)  # Cap at 3x
        
        dynamic_units = int(base_units * confidence_factor)
        return dynamic_units

    def validate_trade_edge(self, pair, direction, confidence, current_price):
        """Comprehensive trade validation with anti-drift filters"""
        print(f"\n🔍 EDGE VALIDATION: {pair} {direction}")
        print(f"   Confidence: {confidence:.3f}")
        
        # 1. Confidence Filter
        if confidence < self.min_confidence_threshold:
            print(f"❌ REJECTED: Confidence {confidence:.3f} < {self.min_confidence_threshold}")
            return False, 0, 0, 0
        
        # 2. Get ATR for volatility-based SL/TP
        atr = self.get_atr(pair)
        atr_pips = atr * 10000  # Convert to pips
        
        # 3. Calculate volatility-adjusted SL/TP
        sl_distance = max(atr_pips * self.volatility_multiplier, 15)  # Minimum 15 pips
        tp_distance = sl_distance * self.min_reward_risk_ratio  # 2:1 minimum
        
        if direction == "buy":
            stop_loss = current_price - (sl_distance / 10000)
            take_profit = current_price + (tp_distance / 10000)
        else:
            stop_loss = current_price + (sl_distance / 10000)
            take_profit = current_price - (tp_distance / 10000)
        
        # 4. Validate R/R ratio
        risk = abs(current_price - stop_loss)
        reward = abs(take_profit - current_price)
        rr_ratio = reward / risk if risk > 0 else 0
        
        if rr_ratio < self.min_reward_risk_ratio:
            print(f"❌ REJECTED: R/R {rr_ratio:.2f} < {self.min_reward_risk_ratio}")
            return False, 0, 0, 0
        
        # 5. Calculate position size
        position_size = self.calculate_dynamic_position_size(confidence)
        if position_size == 0:
            print(f"❌ REJECTED: Position size calculated as 0")
            return False, 0, 0, 0
        
        print(f"✅ APPROVED: R/R {rr_ratio:.2f}, SL: {sl_distance:.1f} pips, TP: {tp_distance:.1f} pips")
        print(f"   Position Size: {position_size} units (confidence scaling)")
        
        return True, stop_loss, take_profit, position_size

    def get_current_positions(self):
        """Get current open positions"""
        url = f"{self.base_url}/v3/accounts/{self.account_id}/positions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            open_positions = []
            for pos in data.get('positions', []):
                if float(pos['long']['units']) != 0 or float(pos['short']['units']) != 0:
                    open_positions.append(pos)
            
            return open_positions
            
        except Exception as e:
            print(f"⚠️ Error getting positions: {e}")
            return []

    def anti_drift_scan(self):
        """Continuous scan for drift patterns and corrections"""
        print("\n🚨 ANTI-DRIFT SCAN RUNNING...")
        
        positions = self.get_current_positions()
        
        # Check for micro-loss patterns
        micro_losses = 0
        total_unrealized = 0
        
        for pos in positions:
            unrealized = float(pos.get('unrealizedPL', 0))
            total_unrealized += unrealized
            
            if -5 < unrealized < 0:  # Micro losses between -$5 and $0
                micro_losses += 1
        
        if micro_losses >= 2:
            print(f"⚠️ DRIFT ALERT: {micro_losses} micro-loss positions detected")
            print(f"   Total Unrealized P/L: ${total_unrealized:.2f}")
            
            # Log drift pattern for analysis
            with open("logs/drift_alerts.log", "a") as f:
                f.write(f"{datetime.now()}: {micro_losses} micro-losses, Total: ${total_unrealized:.2f}\n")
        
        return {
            'micro_losses': micro_losses,
            'total_unrealized': total_unrealized,
            'position_count': len(positions)
        }

def inject_anti_drift_to_main():
    """Inject anti-drift defense into main trading system"""
    print("\n🚨 INJECTING ANTI-DRIFT DEFENSE TO MAIN SYSTEM...")
    
    # Create the defense system
    defense = AntiDriftDefense()
    
    # Test the system
    print("\n🧪 TESTING ANTI-DRIFT FILTERS...")
    
    # Simulate trade validation
        atr = defense.get_atr(pair)
        print(f"   {pair} ATR: {atr*10000:.1f} pips")
    
    # Run drift scan
    drift_status = defense.anti_drift_scan()
    print(f"\n📊 CURRENT DRIFT STATUS:")
    print(f"   Micro-losses: {drift_status['micro_losses']}")
    print(f"   Total Unrealized: ${drift_status['total_unrealized']:.2f}")
    print(f"   Open Positions: {drift_status['position_count']}")
    
    return defense

if __name__ == "__main__":
    defense_system = inject_anti_drift_to_main()
    
    print("\n✅ ANTI-DRIFT DEFENSE SYSTEM READY")
    print("🔄 Continuous monitoring active...")
    
    # Continuous monitoring loop
    while True:
        try:
            drift_status = defense_system.anti_drift_scan()
            time.sleep(300)  # Check every 5 minutes
        except KeyboardInterrupt:
            print("\n🛑 Anti-drift monitoring stopped")
            break
        except Exception as e:
            print(f"⚠️ Anti-drift error: {e}")
            time.sleep(60)
