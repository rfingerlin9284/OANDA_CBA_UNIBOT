from .mathlib import sma, zscore
def detect_fvg(ohlc, lookback=50):
    n=len(ohlc); bull=bear=0.0; gap=0.0
    if n<3: return {"bull":0.0,"bear":0.0,"gap":0.0}
    start=max(2,n-lookback)
    for i in range(start,n):
        if i<2: continue
        _,hi2,lo2,_=ohlc[i-2]; o,h,l,c=ohlc[i]
        if l>hi2: bull=1.0; gap=max(gap,l-hi2)
        if h<lo2: bear=1.0; gap=max(gap,lo2-h)
    return {"bull":bull,"bear":bear,"gap":gap}
def momentum_weight(closes,fast,slow):
    sf=sma(closes,fast); ss=sma(closes,slow)
    if sf!=sf or ss!=ss: return 0.0
    base=0.0 if ss==0 else (sf-ss)/abs(ss)
    base=max(-0.02,min(0.02,base))
    return (base+0.02)/0.04
def meanrev_weight(closes,p):
    z=zscore(closes,p); z=max(-3.0,min(3.0,z))
    return min(1.0,abs(z)/3.0)
def aggregate_signal(ohlc,w_fvg,w_mom,w_mr,fvg_lb,fast,slow,mr_p):
    closes=[c for _,_,_,c in ohlc]
    fvgr=detect_fvg(ohlc,fvg_lb)
    mom=momentum_weight(closes,fast,slow)
    mr=meanrev_weight(closes,mr_p)
    mom_dir=1.0 if (sma(closes,fast)>sma(closes,slow)) else -1.0
    dir_score=(fvgr["bull"]-fvgr["bear"])+0.5*mom_dir
    side="LONG" if dir_score>=0 else "SHORT"
    conf=max(0.0,min(1.0, w_fvg*(fvgr["bull"] or fvgr["bear"])+w_mom*mom+w_mr*mr))
    return {"side":side,"confidence":conf,"fvg_gap":fvgr["gap"]}
