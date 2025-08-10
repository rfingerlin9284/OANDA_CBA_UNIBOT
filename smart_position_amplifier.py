#!/usr/bin/env python3
"""Smart Position Amplifier - Dynamic Sizing Based on Confidence & Performance"""
import time
from datetime import datetime, timedelta

class SmartPositionAmplifier:
    def __init__(self):
        self.base_position = 1000  # Base units
        self.max_amplification = 5.0  # Max 5x amplification
        self.confidence_threshold = 0.85
        self.performance_history = {}
        
    def calculate_amplified_position(self, instrument, ml_confidence, recent_performance):
        """
        💪 SMART AMPLIFICATION: 3-5x positions for prime setups
        Fixes: +10.9 pips = $0.89 profit (too small for $400/day goal)
        """
        amplifier = 1.0
        
        # 1. Confidence Amplifier (Primary)
        if ml_confidence > 0.95:
            amplifier += 3.0  # 4x total for ultra-high confidence
            print(f"🚀 ULTRA CONFIDENCE: {ml_confidence:.1%} → 4x position")
        elif ml_confidence > 0.90:
            amplifier += 2.0  # 3x total for very high confidence
            print(f"🎯 HIGH CONFIDENCE: {ml_confidence:.1%} → 3x position")
        elif ml_confidence > self.confidence_threshold:
            amplifier += 1.0  # 2x total for good confidence
            print(f"📈 GOOD CONFIDENCE: {ml_confidence:.1%} → 2x position")
        
        # 2. Performance Momentum Amplifier
        if instrument in recent_performance:
            win_rate = recent_performance[instrument].get('win_rate', 0.5)
            avg_profit = recent_performance[instrument].get('avg_profit', 0)
            
            if win_rate > 0.75 and avg_profit > 15:  # 75%+ wins, $15+ avg
                amplifier += 1.0
                print(f"💰 PERFORMANCE BONUS: {win_rate:.1%} wins → +1x amplifier")
        
        # 3. Cap amplification
        final_amplifier = min(amplifier, self.max_amplification)
        final_position = int(self.base_position * final_amplifier)
        
        print(f"📊 POSITION SIZING:")
        print(f"   Base: {self.base_position:,} units")
        print(f"   Amplifier: {final_amplifier:.1f}x")
        print(f"   Final: {final_position:,} units")
        
        return final_position, final_amplifier

    """Test position amplification"""
    amp = SmartPositionAmplifier()
    
    scenarios = [
        ("EUR_USD", 0.97, {"EUR_USD": {"win_rate": 0.80, "avg_profit": 25}}),
        ("GBP_JPY", 0.88, {"GBP_JPY": {"win_rate": 0.60, "avg_profit": 8}}),
        ("USD_JPY", 0.75, {})
    ]
    
    for instrument, confidence, performance in scenarios:
        print(f"\n🧪 Testing {instrument}:")
        position, amplifier = amp.calculate_amplified_position(instrument, confidence, performance)

if __name__ == "__main__":
