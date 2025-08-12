import pandas as pd, numpy as np

def atr(df:pd.DataFrame, n:int=14):
    h,l,c=df["h"],df["l"],df["c"]
    tr=pd.concat([(h-l).abs(),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n,min_periods=n).mean()

def fvg_flags(df:pd.DataFrame):
    # simple 3-candle FVG: bullish if low3 > high1; bearish if high3 < low1
    h,l = df["h"], df["l"]
    bull = l.shift(-0) > h.shift(2)
    bear = h.shift(-0) < l.shift(2)
    return bull.fillna(False), bear.fillna(False)

def signals(df:pd.DataFrame, rules:dict, pip:float, is_crypto:bool):
    df=df.copy()
    df["atr"]=atr(df, n=int(rules["atr_period"]))
    ma=df["atr"].rolling(50,min_periods=50).mean()
    df["atr_ok"]=df["atr"] >= (float(rules["min_atr_multiple"])*ma)
    df["long_break"]=df["c"]>df["h"].rolling(20).max().shift(1)
    df["short_break"]=df["c"]<df["l"].rolling(20).min().shift(1)
    bfv, sfv = fvg_flags(df)
    df["long_fvg"]=bfv; df["short_fvg"]=sfv
    # spread/fees model
    if is_crypto:
        spread = float(rules["per_trade_spread_bps_crypto"])/10000.0
        df["spread"]=df["c"]*spread
    else:
        df["spread"]=float(rules["per_trade_spread_pips_fx"])*pip
    return df
