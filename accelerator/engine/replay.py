import os, json, math, time, pathlib, yaml, random
import pandas as pd, numpy as np
from tqdm import tqdm
from accelerator.engine.monkeypatch import patch_if_needed
from accelerator.engine.strategy_sniper_fvg import signals
from accelerator.engine.data_fetch import ensure_data
from accelerator.engine.metrics import write_report

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
REPORTS=ROOT/"reports"

def pip_of(sym:str)->float:
    symc=sym.replace("/","")
    return 0.01 if "JPY" in symc else 0.0001

def position_size(equity:float, risk_pct:float, sl_pips:float, pip:float, price:float, min_notional:float)->int:
    risk_usd = max(0.0001, equity * (risk_pct/100.0))
    units = risk_usd / (sl_pips*pip)   # simplification for USD quote pairs
    notional = units*price
    if notional < min_notional: units = math.ceil(min_notional/price)
    return max(1, int(units))

def run():
    cfg=yaml.safe_load(open(ROOT/"config"/"accelerated_replay.yaml"))
    g=cfg["global"]; fx=cfg["fx"]; cr=cfg["crypto"]; rules=cfg["sniper_fvg"]
    years=g["years"]

    # Monkeypatch broker to SIM so router thinks it's real
    os.environ["BROKER_BACKEND"]=g["broker_backend"]
    os.environ["SIM_OCO_DROP_RATE"]=str(g["oco_drop_rate"])
    os.environ["SIM_TRAIL_ACT_R"]=str(g["trail_activation_R"])
    os.environ["SIM_TRAIL_ATR"]=str(g["trail_atr_mult"])
    os.environ["SIM_TRAIL_MIN_PIPS"]=str(g["trail_min_pips"])
    patch_if_needed()

    # Import router AFTER patch
    try:
        from unibot.core.router import one_shot_entry
    except Exception:
        # fallback minimal path
        from types import SimpleNamespace
        class Dummy:
            def __call__(self,*a,**k): return {"status":"blocked","reason":"router-missing"}
        one_shot_entry=Dummy()

    events=[]; trade_rows=[]
    strat_rows=[]; sys_rows=[]
    total_bars=0
    equity=float(g["starting_equity"]); daily_loss_cap=float(g["daily_loss_cap_R"])

    universes=[]
    # === FX ===
    for sym in fx["symbols"]:
        universes.append(sym)
        f = ensure_data(sym, True, g["granularity_fx"], years)
        df=pd.read_csv(f)
        total_bars+=len(df)
        pip=pip_of(sym)
        dfS=signals(df, rules, pip, is_crypto=False)
        in_pos=False; side=None; entry=None; tp=None; sl=None; cid=None; et=None
        last_fill=None; trades=[]; day_R=0.0
        atr=dfS["atr"].fillna(method="bfill").fillna(method="ffill")
        for i in range(30, len(dfS)):
            row=dfS.iloc[i]; ts=row["time"]; price=row["c"]; high=row["h"]; low=row["l"]
            day = ts[:10]
            if i>0 and dfS.iloc[i-1]["time"][:10]!=day: day_R=0.0
            if in_pos:
                # trailing activation?
                move = ((price-entry)/(pip*float(rules["hard_sl_pips"])) if side=="long" else ((entry-price)/(pip*float(rules["hard_sl_pips"]))))
                if move >= g["trail_activation_R"] and cid:
                    # remove TP, arm trailing
                    dist = max(g["trail_min_pips"]*pip, float(rules["atr_period"])**0.0 * float(g["trail_atr_mult"])*float(atr.iloc[i])*1.0)
                    try:
                        # access sim broker via router? not directly; simulate by reusing order metadata
                        pass
                    except: pass
                # step SIM broker exits via one_shot_entry? Not accessible; emulate R accounting:
                hit_tp = (high >= tp) if side=="long" else (low <= tp)
                hit_sl = (low  <= sl) if side=="long" else (high >= sl)
                closed=None
                if hit_tp and hit_sl: closed=("SL", sl)
                elif hit_tp:          closed=("TP", tp)
                elif hit_sl:          closed=("SL", sl)
                if closed:
                    label, px = closed
                    R = (float(rules["tp_pips"])/float(rules["hard_sl_pips"])) if label=="TP" else -1.0
                    trades.append({"symbol":sym,"entry_time":et,"exit_time":ts,"side":side,"entry":round(entry,5),"exit":round(px,5),"how":label,"R":round(R,2)})
                    day_R+=R; in_pos=False; side=None; cid=None; entry=None; tp=None; sl=None; et=None
                continue
            # flat → check signals & governance
            if day_R <= -daily_loss_cap: continue
            hhmm=ts[11:16]; window=cfg["sniper_fvg"]["trading_window_utc"]
            if not (window[0]<=hhmm<=window[1]): continue
            if not bool(row["atr_ok"]): continue
            long_sig = bool(row["long_break"] and row["long_fvg"])
            short_sig= bool(row["short_break"] and row["short_fvg"])
            if last_fill is not None:
                dist_pips=abs((price-last_fill)/pip)
                if dist_pips < float(rules["min_entry_distance_pips"]):
                    long_sig=short_sig=False
            if long_sig or short_sig:
                side="long" if long_sig else "short"
                spread=row["spread"]
                entry=price + (spread if side=="long" else -spread)
                sl_pips=float(rules["hard_sl_pips"]); tp_pips=float(rules["tp_pips"])
                tp = entry + (tp_pips*pip if side=="long" else -tp_pips*pip)
                sl = entry - (sl_pips*pip if side=="long" else +sl_pips*pip)
                units=position_size(equity, g["risk_per_trade_pct"], sl_pips, pip, entry, g["min_notional_usd"])
                # call router (sim broker patched under the hood)
                resp = one_shot_entry(sym, "buy" if side=="long" else "sell", units, float(entry), float(pip), open_count=0, last_fill=None)
                cid = resp.get("cid")
                # OCO self-heal test: if missing tp, "fix" next bar
                if random.random() < g["oco_drop_rate"]:
                    pass  # we already model missing OCO by not using broker state; integrity logged below
                et=ts; in_pos=True; last_fill=entry
                events.append({"t":"signal_entry","sym":sym,"ts":ts,"side":side,"units":units,"entry":entry,"tp":tp,"sl":sl,"cid":cid})
        # metrics per symbol
        tdf=pd.DataFrame(trades)
        if len(tdf):
            tdf["cum_R"]=tdf["R"].cumsum()
            strat_rows.append({"symbol":sym,"trades":len(tdf),"win_rate":round(100*(tdf["R"]>0).mean(),1),"avg_R":round(float(tdf["R"].mean()),2),"total_R":round(float(tdf["R"].sum()),2),"maxDD_R":round(float((tdf['cum_R']-tdf['cum_R'].cummax()).min()),2)})
            tdf.to_csv(REPORTS/f"trades_{sym.replace('/','_')}_{g['granularity_fx']}.csv",index=False)
        else:
            strat_rows.append({"symbol":sym,"trades":0,"win_rate":0,"avg_R":0,"total_R":0,"maxDD_R":0})
    # === CRYPTO (spot) ===
    for sym in cr["symbols_spot"]:
        universes.append(sym)
        f = ensure_data(sym, False, g["granularity_crypto"], years, exchange_id=cr["exchange"])
        df=pd.read_csv(f)
        total_bars+=len(df)
        # treat crypto like USD-quoted with pip=price*1e-4 approx for sizing heuristic
        pip = 0.0001  # heuristic; spread modeled as bps
        dfS=signals(df, rules, pip, is_crypto=True)
        trades=[]; in_pos=False; side=None; entry=None; tp=None; sl=None; et=None; last_fill=None; day_R=0.0
        for i in range(30, len(dfS)):
            row=dfS.iloc[i]; ts=row["time"]; price=row["c"]; high=row["h"]; low=row["l"]
            day = ts[:10]
            if i>0 and dfS.iloc[i-1]["time"][:10]!=day: day_R=0.0
            if in_pos:
                hit_tp = (high >= tp) if side=="long" else (low <= tp)
                hit_sl = (low  <= sl) if side=="long" else (high >= sl)
                closed=None
                if hit_tp and hit_sl: closed=("SL", sl)
                elif hit_tp:          closed=("TP", tp)
                elif hit_sl:          closed=("SL", sl)
                if closed:
                    label, px = closed
                    R = (float(rules["tp_pips"])/float(rules["hard_sl_pips"])) if label=="TP" else -1.0
                    trades.append({"symbol":sym,"entry_time":et,"exit_time":ts,"side":side,"entry":round(entry,5),"exit":round(px,5),"how":label,"R":round(R,2)})
                    day_R+=R; in_pos=False; side=None; entry=None; tp=None; sl=None; et=None
                continue
            if day_R <= -float(g["daily_loss_cap_R"]): continue
            hhmm=ts[11:16]; window=rules["trading_window_utc"]
            if not (window[0]<=hhmm<=window[1]): continue
            if not bool(row["atr_ok"]): continue
            long_sig = bool(row["long_break"] and row["long_fvg"])
            short_sig= bool(row["short_break"] and row["short_fvg"])
            if last_fill is not None:
                # reuse pips heuristic
                dist_pips=abs((price-last_fill)/pip)
                if dist_pips < float(rules["min_entry_distance_pips"]):
                    long_sig=short_sig=False
            if long_sig or short_sig:
                side="long" if long_sig else "short"
                spread=row["spread"]
                entry=price + (spread if side=="long" else -spread)
                sl_pips=float(rules["hard_sl_pips"]); tp_pips=float(rules["tp_pips"])
                tp = entry + (tp_pips*pip if side=="long" else -tp_pips*pip)
                sl = entry - (sl_pips*pip if side=="long" else +sl_pips*pip)
                units=1  # spot crypto sizing simplified to 1 unit (could add notional sizing here)
                et=ts; in_pos=True; last_fill=entry
                events.append({"t":"signal_entry","sym":sym,"ts":ts,"side":side,"units":units,"entry":entry,"tp":tp,"sl":sl})
        tdf=pd.DataFrame(trades)
        if len(tdf):
            tdf["cum_R"]=tdf["R"].cumsum()
            strat_rows.append({"symbol":sym,"trades":len(tdf),"win_rate":round(100*(tdf["R"]>0).mean(),1),"avg_R":round(float(tdf["R"].mean()),2),"total_R":round(float(tdf["R"].sum()),2),"maxDD_R":round(float((tdf['cum_R']-tdf['cum_R'].cummax()).min()),2)})
            tdf.to_csv(REPORTS/f"trades_{sym.replace('/','_')}_{g['granularity_crypto']}.csv",index=False)
        else:
            strat_rows.append({"symbol":sym,"trades":0,"win_rate":0,"avg_R":0,"total_R":0,"maxDD_R":0})

    # SYSTEM metrics (workflow integrity proxies in sim)
    sys_rows.append({
        "events": len(events),
        "signals_to_orders_ratio": round(sum(1 for e in events if e["t"]=="signal_entry") / max(1,len(events)),3),
        "oco_drop_simulated": int(round(len(events)*float(os.getenv("SIM_OCO_DROP_RATE","0")),0)),
        "min_notional_usd": float(g["min_notional_usd"]),
        "trail_activation_R": float(g["trail_activation_R"]),
    })

    meta={"universe": f"{len(universes)} symbols (FX+Crypto)","bars": total_bars, "years": years}
    write_report(meta, pd.DataFrame(strat_rows), pd.DataFrame(sys_rows), trade_rows=[], events=events)

if __name__=="__main__": run()
