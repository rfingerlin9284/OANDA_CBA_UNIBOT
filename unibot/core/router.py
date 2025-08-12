import time, uuid, os
try:
    from guards.sniper_gate import guard_place_order, record_fill
    _HAS_GUARD=True
except Exception:
    _HAS_GUARD=False
    def guard_place_order(symbol, side, units, price, pip_value, open_positions_for_symbol, last_fill_price=None, tp=None, sl=None):
        # ultra-minimal fallback: enforce no pyramiding + 30m cooldown + ensure TP/SL present
        cd_path=f"state/{symbol.replace('/','_')}.cooldown"
        import json, pathlib, time
        pathlib.Path("state").mkdir(exist_ok=True)
        now=time.time(); last=0.0
        if os.path.exists(cd_path):
            try: last=float(open(cd_path).read().strip())
            except: pass
        if open_positions_for_symbol>0: return False, {"reason":"no-pyramiding"}
        if now-last<30*60: return False, {"reason":f"cooldown: {int((30*60-(now-last))//60)}m remaining"}
        if tp is None or sl is None: return False, {"reason":"tp/sl required"}
        open(cd_path,"w").write(str(now))
        return True, {"tp":tp,"sl":sl}
    def record_fill(symbol, fill_price): pass

from unibot.adapters.oanda import Oanda

def one_shot_entry(symbol:str, side:str, units:int, price:float, pip_val:float,
                   open_count:int=0, last_fill:float|None=None):
    ok, params = guard_place_order(symbol, side, units, price, pip_val, open_count, last_fill)
    if not ok: return {"status":"blocked", "reason":params["reason"], "guard":("real" if _HAS_GUARD else "fallback")}
    broker = Oanda()
    cid = f"rbot-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    resp = broker.place_order_oco(symbol, side, units, price, params["tp"], params["sl"], client_id=cid)
    record_fill(symbol, price)
    return {"status":"placed", "cid":cid, "resp":resp, "guard":("real" if _HAS_GUARD else "fallback")}
