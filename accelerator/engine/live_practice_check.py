import os, time, uuid, yaml, json
from unibot.adapters.oanda import Oanda

CFG=os.path.join(os.path.dirname(__file__),"..","config","accelerated_replay.yaml")
cfg=yaml.safe_load(open(CFG))
t=cfg["practice_trade"]; sym=t["symbol"]; side=t["side"]; units=int(t["units"])
pip = 0.0001 if "JPY" not in sym.replace("/","") else 0.01
mid = float(os.getenv("PRACTICE_MID","1.10000"))
tp = mid + (t["tp_pips"]*pip if side=="buy" else -t["tp_pips"]*pip)
sl = mid - (t["sl_pips"]*pip if side=="buy" else +t["sl_pips"]*pip)
cid=f"lab-{int(time.time())}-{uuid.uuid4().hex[:6]}"
o=Oanda()
print("[PRACTICE] placing:", dict(symbol=sym, side=side, units=units, mid=round(mid,5), tp=round(tp,5), sl=round(sl,5), cid=cid))
resp=o.place_order_oco(sym, side, units, mid, tp, sl, client_id=cid)
print("[PRACTICE] response:", json.dumps(resp)[:800])
