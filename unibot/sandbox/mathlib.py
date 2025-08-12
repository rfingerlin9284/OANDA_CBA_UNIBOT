import math
def sma(v,p):
    if p<=0 or len(v)<p: return float("nan")
    return sum(v[-p:])/float(p)
def zscore(v,p):
    if p<=1 or len(v)<p: return 0.0
    w=v[-p:]; mu=sum(w)/p
    var=sum((x-mu)**2 for x in w)/(p-1)
    sd=math.sqrt(max(var,1e-12))
    return (v[-1]-mu)/sd
def true_range(o,h,l,pc): return max(h-l, abs(h-pc), abs(l-pc))
def atr(ohlc,p):
    if len(ohlc)<p+1: return 0.0
    trs=[]
    for i in range(1,len(ohlc)):
        o,h,l,c=ohlc[i]; _,_,_,pc=ohlc[i-1]
        trs.append(true_range(o,h,l,pc))
    if len(trs)<p: return 0.0
    return sum(trs[-p:])/p
