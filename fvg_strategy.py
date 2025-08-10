"""
FAIR VALUE GAP (FVG) STRATEGY - EXPLICIT RULES & PARAMETERS
LIVE TRADING ONLY - REAL MONEY AT RISK
(Strategy rules as in your original block)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional

# === CUSTOM INDICATORS - NO TALIB REQUIRED ===
def calculate_ema(prices: List[float], period: int) -> float:
    if len(prices) < period:
        return prices[-1] if prices else 0
    alpha = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = alpha * price + (1 - alpha) * ema
    return ema

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0
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

def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
    if len(highs) < 2 or len(highs) != len(lows) or len(highs) != len(closes):
        return 0.01
    true_ranges = []
    for i in range(1, len(highs)):
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        true_ranges.append(max(tr1, tr2, tr3))
    if len(true_ranges) < period:
        return sum(true_ranges) / len(true_ranges) if true_ranges else 0.01
    return sum(true_ranges[-period:]) / period

class FVGStrategy:
    """Fair Value Gap Strategy with Explicit Rules"""

    def __init__(self):
        self.FVG_GAP_THRESHOLD = 0.002
        self.MIN_CONFIDENCE = 0.80
        self.RISK_REWARD_RATIO = 3.0
        self.ATR_VOLATILITY_MIN = 0.005
        self.FIBONACCI_LEVELS = [0.618, 0.786]
        self.SETUP_EXPIRY_CANDLES = 3
        self.EMA_PERIOD = 21
        self.RSI_PERIOD = 14
        self.ATR_PERIOD = 14
        print("🎯 FVG Strategy initialized with explicit rules")
        print(f"📊 Gap threshold: {self.FVG_GAP_THRESHOLD*100}%")
        print(f"🎯 Min confidence: {self.MIN_CONFIDENCE}")
        print(f"💰 Risk:Reward = 1:{self.RISK_REWARD_RATIO}")

    def detect_bullish_fvg(self, candles: List[Dict]) -> Optional[Dict]:
        if len(candles) < 3:
            return None
        candle1 = candles[-3]
        candle2 = candles[-2]
        candle3 = candles[-1]
        condition1 = candle1['high'] < candle3['low']
        condition2 = candle2['close'] < candle3['close']
        if not (condition1 and condition2):
            return None
        gap_size = candle3['low'] - candle1['high']
        gap_percentage = gap_size / candle3['low']
        if gap_percentage < self.FVG_GAP_THRESHOLD:
            return None
        entry = (candle1['high'] + candle3['low']) / 2
        sl = candle1['low']
        risk = entry - sl
        tp = entry + (risk * self.RISK_REWARD_RATIO)
        return {
            'direction': 'BUY',
            'entry': round(entry, 5),
            'sl': round(sl, 5),
            'tp': round(tp, 5),
            'gap_size': round(gap_percentage * 100, 2),
            'risk': round(risk, 5),
            'reward': round(risk * self.RISK_REWARD_RATIO, 5),
            'setup_type': 'Bullish FVG',
            'candle1_high': candle1['high'],
            'candle3_low': candle3['low']
        }

    def detect_bearish_fvg(self, candles: List[Dict]) -> Optional[Dict]:
        if len(candles) < 3:
            return None
        candle1 = candles[-3]
        candle2 = candles[-2]
        candle3 = candles[-1]
        condition1 = candle1['low'] > candle3['high']
        condition2 = candle2['close'] > candle3['close']
        if not (condition1 and condition2):
            return None
        gap_size = candle1['low'] - candle3['high']
        gap_percentage = gap_size / candle3['high']
        if gap_percentage < self.FVG_GAP_THRESHOLD:
            return None
        entry = (candle1['low'] + candle3['high']) / 2
        sl = candle1['high']
        risk = sl - entry
        tp = entry - (risk * self.RISK_REWARD_RATIO)
        return {
            'direction': 'SELL',
            'entry': round(entry, 5),
            'sl': round(sl, 5),
            'tp': round(tp, 5),
            'gap_size': round(gap_percentage * 100, 2),
            'risk': round(risk, 5),
            'reward': round(risk * self.RISK_REWARD_RATIO, 5),
            'setup_type': 'Bearish FVG',
            'candle1_low': candle1['low'],
            'candle3_high': candle3['high']
        }

    def calculate_indicators(self, candles: List[Dict]) -> Dict:
        if len(candles) < max(self.EMA_PERIOD, self.RSI_PERIOD, self.ATR_PERIOD):
            return {}
        closes = [c['close'] for c in candles]
        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        ema = calculate_ema(closes, self.EMA_PERIOD)
        rsi = calculate_rsi(closes, self.RSI_PERIOD)
        atr = calculate_atr(highs, lows, closes, self.ATR_PERIOD)
        current_price = closes[-1]
        return {
            'ema': ema,
            'rsi': rsi,
            'atr': atr,
            'atr_percentage': (atr / current_price) if atr > 0 else 0,
            'price_above_ema': current_price > ema if ema > 0 else None,
            'rsi_bullish': rsi > 50 if rsi > 0 else None
        }

    def check_fibonacci_confluence(self, candles: List[Dict], setup: Dict) -> bool:
        if len(candles) < 20:
            return True
        highs = [c['high'] for c in candles[-20:]]
        lows = [c['low'] for c in candles[-20:]]
        swing_high = max(highs)
        swing_low = min(lows)
        fib_range = swing_high - swing_low
        fib_618 = swing_high - (fib_range * 0.618)
        fib_786 = swing_high - (fib_range * 0.786)
        entry = setup['entry']
        tolerance = entry * 0.001
        near_618 = abs(entry - fib_618) <= tolerance
        near_786 = abs(entry - fib_786) <= tolerance
        return near_618 or near_786

    def calculate_confidence(self, setup: Dict, indicators: Dict, fib_confluence: bool) -> float:
        confidence = 0.5
        if setup['gap_size'] > 0.3:
            confidence += 0.1
        if indicators.get('rsi') is not None:
            if setup['direction'] == 'BUY' and indicators['rsi_bullish']:
                confidence += 0.1
            elif setup['direction'] == 'SELL' and not indicators['rsi_bullish']:
                confidence += 0.1
        if indicators.get('price_above_ema') is not None:
            if setup['direction'] == 'BUY' and indicators['price_above_ema']:
                confidence += 0.1
            elif setup['direction'] == 'SELL' and not indicators['price_above_ema']:
                confidence += 0.1
        if indicators.get('atr_percentage') is not None:
            if indicators['atr_percentage'] >= self.ATR_VOLATILITY_MIN:
                confidence += 0.1
        if fib_confluence:
            confidence += 0.1
        return min(confidence, 1.0)

    def scan_for_signals(self, candles: List[Dict], pair: str) -> Optional[Dict]:
        if len(candles) < 25:
            return None
        indicators = self.calculate_indicators(candles)
        bullish_setup = self.detect_bullish_fvg(candles)
        if bullish_setup:
            fib_confluence = self.check_fibonacci_confluence(candles, bullish_setup)
            confidence = self.calculate_confidence(bullish_setup, indicators, fib_confluence)
            if confidence >= self.MIN_CONFIDENCE:
                return {
                    **bullish_setup,
                    'pair': pair,
                    'confidence': round(confidence, 2),
                    'indicators': indicators,
                    'fib_confluence': fib_confluence,
                    'timestamp': candles[-1].get('timestamp', 0),
                    'signal_type': 'FVG_BULLISH'
                }
        bearish_setup = self.detect_bearish_fvg(candles)
        if bearish_setup:
            fib_confluence = self.check_fibonacci_confluence(candles, bearish_setup)
            confidence = self.calculate_confidence(bearish_setup, indicators, fib_confluence)
            if confidence >= self.MIN_CONFIDENCE:
                return {
                    **bearish_setup,
                    'pair': pair,
                    'confidence': round(confidence, 2),
                    'indicators': indicators,
                    'fib_confluence': fib_confluence,
                    'timestamp': candles[-1].get('timestamp', 0),
                    'signal_type': 'FVG_BEARISH'
                }
        return None

    def validate_setup(self, signal: Dict) -> bool:
        risk = signal['risk']
        reward = signal['reward']
        if reward / risk < self.RISK_REWARD_RATIO * 0.9:
            return False
        if signal['gap_size'] < self.FVG_GAP_THRESHOLD * 100:
            return False
        if signal['confidence'] < self.MIN_CONFIDENCE:
            return False
        return True

if __name__ == "__main__":
    strategy = FVGStrategy()
    # Sample bullish FVG data
    sample_candles = [
        {'high': 1.1000, 'low': 1.0980, 'close': 1.0990, 'timestamp': 1620000000},
        {'high': 1.1010, 'low': 1.0985, 'close': 1.0995, 'timestamp': 1620000300},
        {'high': 1.1030, 'low': 1.1015, 'close': 1.1025, 'timestamp': 1620000600},  # Gap created
    ]
    # Add more candles for indicators
    for i in range(22):
        sample_candles.insert(0, {
            'high': 1.0950 + (i * 0.001),
            'low': 1.0940 + (i * 0.001),
            'close': 1.0945 + (i * 0.001),
            'timestamp': 1620000000 - ((22-i) * 300)
        })
    signal = strategy.scan_for_signals(sample_candles, "EUR/USD")
    if signal:
        print("✅ FVG Signal Detected:")
        print(f"  Direction: {signal['direction']}")
        print(f"  Entry: {signal['entry']}")
        print(f"  SL: {signal['sl']}")
        print(f"  TP: {signal['tp']}")
        print(f"  Confidence: {signal['confidence']}")
        print(f"  Gap Size: {signal['gap_size']}%")
    else:
        print("❌ No FVG signal detected")
