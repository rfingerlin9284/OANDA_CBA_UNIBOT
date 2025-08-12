import os, argparse
from .instrumentation import jlog
from .feed import load_csv, synthetic
from .signals import aggregate_signal
from .risk import fib_leverage, tp_sl_from_atr
from .mathlib import atr
from .broker import SandboxBroker
def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--symbol",default=os.getenv("SYMBOL","EUR_USD"))
    p.add_argument("--csv",help="CSV with ts,open,high,low,close")
    p.add_argument("--steps",type=int,default=1200)
    return p.parse_args()
def main():
    a=parse_args(); env=os.environ
    jlog("sandbox.start",symbol=a.symbol,run=os.getenv("RUN_ID"))
    stream = load_csv(a.csv) if a.csv else synthetic(a.steps)
    base=float(env.get("BASE_LEVERAGE","1")); maxlev=float(env.get("MAX_LEVERAGE","5"))
    w_fvg=float(env.get("W_FVG","0.60")); w_mom=float(env.get("W_MOMENTUM","0.25")); w_mr=float(env.get("W_MEANREV","0.15"))
    fvg_lb=int(env.get("FVG_LOOKBACK","50")); fast=int(env.get("SMA_FAST","10")); slow=int(env.get("SMA_SLOW","30"))
    mr_p=int(env.get("MR_PERIOD","50")); atr_p=int(env.get("ATR_PERIOD","14"))
    tp_m=float(env.get("TP_ATR","2.0")); sl_m=float(env.get("SL_ATR","1.2"))
    risk=float(env.get("RISK_PER_TRADE","0.01"))
    broker=SandboxBroker(a.symbol); ohlc=[]
    for i,bar in enumerate(stream):
        o,h,l,c=bar["o"],bar["h"],bar["l"],bar["c"]; ohlc.append((o,h,l,c)); broker.mark(c)
        if len(ohlc)<max(slow,mr_p,fvg_lb,atr_p)+3: continue
        sig=aggregate_signal(ohlc,w_fvg,w_mom,w_mr,fvg_lb,fast,slow,mr_p)
        aatr=atr(ohlc,atr_p); tp,sl=tp_sl_from_atr(ohlc,atr_p,tp_m,sl_m,sig["side"])
        equity=broker.positions()["equity"]; dist=abs(tp-sl); size=0.0
        if dist>0: size=(equity*risk/dist)*fib_leverage(base,maxlev,sig["confidence"])
        jlog("signal.evaluated",side=sig["side"],confidence=round(sig["confidence"],4),
             atr=aatr,tp=tp,sl=sl,size=round(size,4))
        if sig["confidence"]>=0.60 and size>0: broker.place_order(sig["side"],size,c,tp,sl)
        if (i%50)==0: jlog("account.snapshot",**broker.positions(),open_orders=len(broker.open_orders()))
    jlog("sandbox.done",**broker.positions())
if __name__=="__main__": main()
