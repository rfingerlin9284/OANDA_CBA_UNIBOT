import os, math, time, json, pathlib
import pandas as pd, requests, ccxt
from typing import List, Dict, Tuple

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; DATA.mkdir(parents=True, exist_ok=True)
def _ins_fx(sym:str)->str: return sym.replace("/","_").upper()

def fetch_oanda_fx(symbol:str, granularity:str, years:int)->pd.DataFrame:
    api=os.getenv("OANDA_API_BASE","https://api-fxpractice.oanda.com")
    key=os.getenv("OANDA_API_KEY",""); hdr={"Authorization":f"Bearer {key}"} if key else {}
    # chunk by ~5000 candles
    out=[]; params={"price":"M","granularity":granularity,"count":"5000"}
    # walk back by time windows (approx 10y). We'll just loop pages until stop.
    url=f"{api}/v3/instruments/{_ins_fx(symbol)}/candles"
    fetched=0; max_pages=400
    while fetched<years*30 and max_pages>0:
        r=requests.get(url,params=params,headers=hdr,timeout=30); r.raise_for_status()
        js=r.json(); cds=js.get("candles",[])
        if not cds: break
        for c in cds:
            mid=c.get("mid",{})
            out.append({"time":c["time"],"o":float(mid["o"]),"h":float(mid["h"]),"l":float(mid["l"]),"c":float(mid["c"])})
        fetched+=1; max_pages-=1
        # page using "from" by earliest time seen
        params={"price":"M","granularity":granularity,"to":out[0]["time"],"count":"5000"}
        time.sleep(0.05)  # gentle
    df=pd.DataFrame(out).drop_duplicates("time").sort_values("time").reset_index(drop=True)
    return df

def fetch_ccxt(exchange_id:str, symbol:str, timeframe:str, years:int)->pd.DataFrame:
    ex=getattr(ccxt, exchange_id)()
    ms_per_candle = ex.parse_timeframe(timeframe)*1000
    now = int(time.time()*1000)
    since = now - years*365*24*60*60*1000
    limit = 1000
    out=[]
    while True:
        ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        if not ohlcv: break
        out += ohlcv
        since = ohlcv[-1][0] + ms_per_candle
        if since >= now: break
        time.sleep(ex.rateLimit/1000.0)
    df=pd.DataFrame(out, columns=["ts","o","h","l","c","v"])
    df["time"]=pd.to_datetime(df["ts"],unit="ms").dt.strftime("%Y-%m-%dT%H:%M:%S")
    return df[["time","o","h","l","c"]].drop_duplicates("time").reset_index(drop=True)

def ensure_data(sym:str, is_fx:bool, gran:str, years:int, exchange_id:str=None)->pathlib.Path:
    fname = DATA/f"{sym.replace('/','_')}_{gran}_{'FX' if is_fx else exchange_id}.csv"
    if fname.exists(): return fname
    if is_fx:
        df=fetch_oanda_fx(sym, gran, years)
    else:
        df=fetch_ccxt(exchange_id, sym.replace("USD","/USD").replace("USDT","/USDT"), gran, years)
    df.to_csv(fname, index=False)
    return fname
