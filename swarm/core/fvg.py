from typing import List, Tuple

def true_range(h, l, c_prev): return max(h-l, abs(h-c_prev), abs(l-c_prev))
def atr_pips(candles:List[Tuple[float,float,float,float]], n:int=14)->float:
    # candles: [(o,h,l,c), ...] newest last
    trs=[]; 
    for i in range(1, min(len(candles), n+1)):
        o,h,l,c = candles[-i]
        _,ph,pl,pc = candles[-i-1]
        trs.append(true_range(h,l,pc))
    if not trs: return 10.0
    return (sum(trs)/len(trs))*10000.0

def fvg_weight(candles:List[Tuple[float,float,float,float]])->Tuple[str,float]:
    """Return ('bull'|'bear'|'none', weight 0..1) based on fresh FVG size vs ATR."""
    if len(candles)<3: return ("none",0.0)
    o1,h1,l1,c1 = candles[-3]
    o2,h2,l2,c2 = candles[-2]
    o3,h3,l3,c3 = candles[-1]
    # Bearish FVG if h3 < l1 (hidden gap), Bullish if l3 > h1
    direction="none"; gap=0.0
    if h3 < l1: 
        direction="bear"; gap=(l1-h3)
    elif l3 > h1:
        direction="bull"; gap=(l3-h1)
    atr=atr_pips(candles)
    weight=min(1.0, max(0.0, (gap*10000.0)/(atr if atr>0 else 1)))
    return (direction, weight)
