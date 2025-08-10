import pandas as pd

def detect_trade_signal(df):
    """
    Sample logic:
    - Buys if RSI < 30 and FVG is bullish
    - Sells if RSI > 70 and FVG is bearish
    """
    if len(df) < 2:
        return None

    prev = df.iloc[-2]


    if rsi is None or fvg is None:
        return None

    if rsi < 30 and fvg == "bullish":
        return "buy"
    elif rsi > 70 and fvg == "bearish":
        return "sell"
    return None
