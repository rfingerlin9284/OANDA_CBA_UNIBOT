"""
CRYPTO MOMENTUM STRATEGY FOR COINBASE - EXPLICIT RULES
Constitutional PIN: 841921
LIVE TRADING ONLY - REAL MONEY AT RISK

Strategy Rules:
- Timeframe: 15-minute and 1-hour candles  
- Momentum Detection: RSI + Volume + Price Action
- Bullish: RSI > 55, Volume > 1.5x average, Price above 21 EMA
- Bearish: RSI < 45, Volume > 1.5x average, Price below 21 EMA
- Entry: Market order on momentum confirmation
- Stop Loss: 2% from entry (tight crypto stops)
- Take Profit: 1:4 Risk-Reward ratio minimum
- Min Confidence: 0.75 (Momentum + Volume + Trend alignment)
- Max Allocation: 5% of portfolio per trade
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple

# === CUSTOM INDICATORS - NO TALIB REQUIRED ===
def calculate_ema(prices: List[float], period: int) -> float:
    """Calculate Exponential Moving Average without TA-Lib"""
    if len(prices) < period:
        return prices[-1] if prices else 0
    
    alpha = 2 / (period + 1)
    ema = prices[0]
    
    for price in prices[1:]:
        ema = alpha * price + (1 - alpha) * ema
    
    return ema

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculate RSI without TA-Lib"""
    if len(prices) < period + 1:
        return 50.0  # Neutral RSI
    
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]
    
    if len(gains) < period:
        return 50.0
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


class CryptoMomentumStrategy:
    """Crypto Momentum Strategy with Volume Confirmation"""
    
    def __init__(self):
        # === STRATEGY PARAMETERS ===
        self.MIN_CONFIDENCE = 0.75      # 75% minimum confidence
        self.RISK_REWARD_RATIO = 4.0    # 1:4 RR minimum for crypto
        self.STOP_LOSS_PCT = 0.02       # 2% stop loss (tight for crypto)
        self.MIN_VOLUME_MULTIPLIER = 1.5 # Volume must be 1.5x average
        self.MAX_POSITION_PCT = 0.05    # 5% max allocation per trade
        
        # === INDICATOR PERIODS ===
        self.EMA_PERIOD = 21
        self.RSI_PERIOD = 14
        self.VOLUME_PERIOD = 20
        
        # === RSI THRESHOLDS ===
        self.RSI_BULLISH_THRESHOLD = 55
        self.RSI_BEARISH_THRESHOLD = 45
        
        print("🚀 Crypto Momentum Strategy initialized")
        print(f"📊 Min confidence: {self.MIN_CONFIDENCE}")
        print(f"💰 Risk:Reward = 1:{self.RISK_REWARD_RATIO}")
        print(f"🛡️ Stop Loss: {self.STOP_LOSS_PCT*100}%")
    
    def detect_bullish_momentum(self, candles: List[Dict]) -> Optional[Dict]:
        """
        BULLISH MOMENTUM DETECTION - EXPLICIT RULES
        
        Rules:
        1. RSI > 55 (momentum building)
        2. Volume > 1.5x average volume
        3. Price above 21 EMA (trend confirmation)
        4. Recent price action showing strength
        
        Entry: Current market price
        SL: Entry - 2%
        TP: Entry + (Risk * 4)
        """
        if len(candles) < max(self.EMA_PERIOD, self.RSI_PERIOD, self.VOLUME_PERIOD):
            return None
            
        # Convert to arrays and calculate indicators
        closes = [c['close'] for c in candles]
        volumes = [c.get('volume', 1000) for c in candles]  # Default volume if missing
        
        # Calculate indicators using custom functions
        rsi = calculate_rsi(closes, self.RSI_PERIOD)
        ema = calculate_ema(closes, self.EMA_PERIOD)
        avg_volume = sum(volumes[-self.VOLUME_PERIOD:]) / self.VOLUME_PERIOD
        
        current_price = closes[-1]
        current_volume = volumes[-1]
        
        # Check momentum conditions
        rsi_bullish = rsi > self.RSI_BULLISH_THRESHOLD
        above_ema = current_price > ema
        volume_surge = current_volume > (avg_volume * self.MIN_VOLUME_MULTIPLIER)
        
        # Price action strength (last 3 candles mostly green)
        recent_closes = closes[-3:]
        recent_opens = [c['open'] for c in candles[-3:]]
        green_candles = sum(1 for i in range(len(recent_closes)) if recent_closes[i] > recent_opens[i])
        price_strength = green_candles >= 2  # At least 2 of last 3 candles green
        
        if not (rsi_bullish and above_ema and volume_surge and price_strength):
            return None
            
        # === CALCULATE ENTRY/SL/TP ===
        entry = current_price
        sl = entry * (1 - self.STOP_LOSS_PCT)
        risk = entry - sl
        tp = entry + (risk * self.RISK_REWARD_RATIO)
        
        return {
            'direction': 'BUY',
            'entry': round(entry, 8),
            'sl': round(sl, 8),
            'tp': round(tp, 8),
            'risk': round(risk, 8),
            'reward': round(risk * self.RISK_REWARD_RATIO, 8),
            'setup_type': 'Bullish Momentum',
            'rsi': round(rsi, 2),
            'volume_ratio': round(current_volume / avg_volume, 2),
            'ema_distance': round((current_price - ema) / current_price * 100, 2)
        }
    
    def detect_bearish_momentum(self, candles: List[Dict]) -> Optional[Dict]:
        """
        BEARISH MOMENTUM DETECTION - EXPLICIT RULES
        
        Rules:
        1. RSI < 45 (momentum weakening)
        2. Volume > 1.5x average volume
        3. Price below 21 EMA (trend confirmation)
        4. Recent price action showing weakness
        
        Entry: Current market price
        SL: Entry + 2%
        TP: Entry - (Risk * 4)
        """
        if len(candles) < max(self.EMA_PERIOD, self.RSI_PERIOD, self.VOLUME_PERIOD):
            return None
            
        # Convert to arrays and calculate indicators
        closes = [c['close'] for c in candles]
        volumes = [c.get('volume', 1000) for c in candles]
        
        # Calculate indicators using custom functions
        rsi = calculate_rsi(closes, self.RSI_PERIOD)
        ema = calculate_ema(closes, self.EMA_PERIOD)
        avg_volume = sum(volumes[-self.VOLUME_PERIOD:]) / self.VOLUME_PERIOD
        
        current_price = closes[-1]
        current_volume = volumes[-1]
        
        # Check momentum conditions
        rsi_bearish = rsi < self.RSI_BEARISH_THRESHOLD
        below_ema = current_price < ema
        volume_surge = current_volume > (avg_volume * self.MIN_VOLUME_MULTIPLIER)
        
        # Price action weakness (last 3 candles mostly red)
        recent_closes = closes[-3:]
        recent_opens = [c['open'] for c in candles[-3:]]
        red_candles = sum(1 for i in range(len(recent_closes)) if recent_closes[i] < recent_opens[i])
        price_weakness = red_candles >= 2  # At least 2 of last 3 candles red
        
        if not (rsi_bearish and below_ema and volume_surge and price_weakness):
            return None
            
        # === CALCULATE ENTRY/SL/TP ===
        entry = current_price
        sl = entry * (1 + self.STOP_LOSS_PCT)
        risk = sl - entry
        tp = entry - (risk * self.RISK_REWARD_RATIO)
        
        return {
            'direction': 'SELL',
            'entry': round(entry, 8),
            'sl': round(sl, 8),
            'tp': round(tp, 8),
            'risk': round(risk, 8),
            'reward': round(risk * self.RISK_REWARD_RATIO, 8),
            'setup_type': 'Bearish Momentum',
            'rsi': round(rsi, 2),
            'volume_ratio': round(current_volume / avg_volume, 2),
            'ema_distance': round((current_price - ema) / current_price * 100, 2)
        }
    
    def calculate_confidence(self, setup: Dict) -> float:
        """
        CONFIDENCE CALCULATION FOR CRYPTO MOMENTUM
        
        Base: 0.5 (50% for valid momentum)
        + 0.1 if RSI shows strong momentum (>60 bull, <40 bear)
        + 0.1 if volume ratio > 2.0x
        + 0.1 if EMA distance > 1%
        + 0.05 if risk/reward > 4.5:1
        
        Max: 1.0 (100%)
        """
        confidence = 0.5  # Base score for valid momentum
        
        # Strong RSI momentum bonus
        if setup['direction'] == 'BUY' and setup['rsi'] > 60:
            confidence += 0.1
        elif setup['direction'] == 'SELL' and setup['rsi'] < 40:
            confidence += 0.1
            
        # High volume confirmation
        if setup['volume_ratio'] > 2.0:
            confidence += 0.1
            
        # Strong trend alignment
        if abs(setup['ema_distance']) > 1.0:  # >1% from EMA
            confidence += 0.1
            
        # Excellent risk/reward
        rr_ratio = setup['reward'] / setup['risk']
        if rr_ratio > 4.5:
            confidence += 0.05
            
        return min(confidence, 1.0)  # Cap at 100%
    
    def scan_for_signals(self, candles: List[Dict], pair: str) -> Optional[Dict]:
        """
        MAIN SIGNAL SCANNER - SCANS FOR MOMENTUM SIGNALS
        
        Returns complete signal with all parameters if confidence >= threshold
        """
        if len(candles) < 25:  # Need enough data for indicators
            return None
            
        # Check for bullish momentum
        bullish_setup = self.detect_bullish_momentum(candles)
        if bullish_setup:
            confidence = self.calculate_confidence(bullish_setup)
            
            if confidence >= self.MIN_CONFIDENCE:
                return {
                    **bullish_setup,
                    'pair': pair,
                    'confidence': round(confidence, 2),
                    'timestamp': candles[-1].get('timestamp', 0),
                    'signal_type': 'CRYPTO_MOMENTUM_BULL'
                }
        
        # Check for bearish momentum
        bearish_setup = self.detect_bearish_momentum(candles)
        if bearish_setup:
            confidence = self.calculate_confidence(bearish_setup)
            
            if confidence >= self.MIN_CONFIDENCE:
                return {
                    **bearish_setup,
                    'pair': pair,
                    'confidence': round(confidence, 2),
                    'timestamp': candles[-1].get('timestamp', 0),
                    'signal_type': 'CRYPTO_MOMENTUM_BEAR'
                }
        
        return None
    
    def validate_setup(self, signal: Dict) -> bool:
        """Final validation before trade execution"""
        
        # Check risk-reward ratio
        risk = signal['risk']
        reward = signal['reward']
        
        if reward / risk < self.RISK_REWARD_RATIO * 0.9:  # Allow 10% tolerance
            return False
            
        # Check confidence is above threshold
        if signal['confidence'] < self.MIN_CONFIDENCE:
            return False
            
        # Check volume confirmation
        if signal['volume_ratio'] < self.MIN_VOLUME_MULTIPLIER:
            return False
            
        return True


if __name__ == "__main__":
    # Test function
    strategy = CryptoMomentumStrategy()
    
    # Sample crypto momentum data
    sample_candles = []
    
    # Create sample data with momentum pattern
    base_price = 50000.0  # BTC price example
    for i in range(30):
        candle = {
            'open': base_price + (i * 100) + np.random.normal(0, 50),
            'high': base_price + (i * 120) + np.random.normal(0, 50),
            'low': base_price + (i * 80) + np.random.normal(0, 50),
            'close': base_price + (i * 110) + np.random.normal(0, 50),
            'volume': 1000 + (i * 50) + np.random.normal(0, 100),
            'timestamp': 1620000000 + (i * 900)  # 15-minute intervals
        }
        sample_candles.append(candle)
    
    signal = strategy.scan_for_signals(sample_candles, "BTC/USD")
    
    if signal:
        print("✅ Crypto Momentum Signal Detected:")
        print(f"  Direction: {signal['direction']}")
        print(f"  Entry: ${signal['entry']:.2f}")
        print(f"  SL: ${signal['sl']:.2f}")
        print(f"  TP: ${signal['tp']:.2f}")
        print(f"  Confidence: {signal['confidence']}")
        print(f"  RSI: {signal['rsi']}")
        print(f"  Volume Ratio: {signal['volume_ratio']}x")
    else:
        print("❌ No momentum signal detected")
