import numpy as np
def detect_patterns(candles):
    prices = [c['close'] for c in candles]
    if len(prices) < 5: return None
    # Simple pattern checks
    if prices[-1] > prices[-2] > prices[-3]: return 'up_trend'
    if prices[-1] < prices[-2] < prices[-3]: return 'down_trend'
    if prices[-1] < np.min(prices[-5:]): return 'fresh_lows'
    if prices[-1] > np.max(prices[-5:]): return 'fresh_highs'
    return 'neutral'

def confluence_boost(base_score, pattern):
    if pattern in ['up_trend', 'down_trend']: return base_score + 0.5
    if pattern in ['fresh_lows', 'fresh_highs']: return base_score + 1.0
    return base_score
