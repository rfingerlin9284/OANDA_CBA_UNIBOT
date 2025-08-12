from .mathlib import atr
FIB=[0.0,0.236,0.382,0.5,0.618,0.786,1.0]
def fib_leverage(base,maxlev,conf):
    i=int(round(conf*(len(FIB)-1))); i=max(0,min(len(FIB)-1,i))
    return max(1.0, min(maxlev, base*(1.0+FIB[i]*(maxlev-1.0))))
def tp_sl_from_atr(ohlc,atr_p,tp_m,sl_m,side):
    a=atr(ohlc,atr_p); last=ohlc[-1][3]
    if side=="LONG":  return last+a*tp_m, last-a*sl_m
    else:             return last-a*tp_m, last+a*sl_m
