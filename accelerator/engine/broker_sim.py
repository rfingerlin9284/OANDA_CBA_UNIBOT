import os, random, json, math, time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

def now_ms(): return int(time.time()*1000)

@dataclass
class SimOrder:
    symbol: str
    side: str           # buy/sell
    units: int
    entry: float
    tp: Optional[float]
    sl: Optional[float]
    client_id: str
    tp_active: bool = True
    trailing_active: bool = False
    trail_dist: Optional[float] = None
    opened_ms: int = field(default_factory=now_ms)
    closed_ms: Optional[int] = None
    status: str = "OPEN"   # OPEN / CLOSED

class Oanda:  # masquerades as unibot.adapters.oanda.Oanda
    def __init__(self):
        self._state: Dict[str, Any] = {
            "positions": {},      # symbol -> net units
            "orders": {},         # client_id -> SimOrder
            "trade_log": []       # list of dicts
        }
        self._cfg = {
           "oco_drop_rate": float(os.getenv("SIM_OCO_DROP_RATE","0")),
           "trail_activation_R": float(os.getenv("SIM_TRAIL_ACT_R","1.5")),
           "trail_atr_mult": float(os.getenv("SIM_TRAIL_ATR","1.2")),
           "trail_min_pips": float(os.getenv("SIM_TRAIL_MIN_PIPS","6")),
        }

    def _log(self, ev: Dict[str,Any]):
        self._state["trade_log"].append(ev)

    # price() only needed for plumbing; replay injects price ticks
    def price(self, symbol:str)->float:
        return float(os.getenv("SIM_LAST_PRICE","1.10000"))

    def place_order_oco(self, symbol, side, units, entry, tp, sl, client_id, extras=None)->Dict[str,Any]:
        # simulate occasional missing OCO (fault injection)
        drop = random.random() < self._cfg["oco_drop_rate"]
        sim_tp = None if drop else tp
        order = SimOrder(symbol=symbol, side=side, units=int(units), entry=float(entry),
                         tp=sim_tp, sl=float(sl), client_id=client_id)
        self._state["orders"][client_id] = order
        self._state["positions"][symbol] = self._state["positions"].get(symbol,0) + (abs(units) if side=="buy" else -abs(units))
        self._log({"t":"place","cid":client_id,"sym":symbol,"side":side,"units":units,"entry":entry,"tp":sim_tp,"sl":sl,"oco_dropped":drop})
        return {"sim":"ok","orderCreateTransaction":{"clientExtensions":{"id":client_id}}}

    def cancel(self, broker_order_id:str)->None:
        # not used in sim MVP
        return

    def open_position(self, symbol:str)->Dict[str,Any]:
        net = self._state["positions"].get(symbol,0)
        return {"symbol":symbol,"netUnits":net}

    def consolidate(self, symbol:str)->Dict[str,Any]:
        # single-net position simulation
        return {"status":"ok","symbol":symbol,"net":self._state["positions"].get(symbol,0)}

    # SIM helpers the replay uses:
    def sim_ensure_oco(self, cid:str, tp:float):
        o = self._state["orders"].get(cid); 
        if o and o.tp is None:
            o.tp = tp
            self._log({"t":"fix_oco","cid":cid,"tp_set":tp})

    def sim_arm_trailing(self, cid:str, dist:float):
        o = self._state["orders"].get(cid)
        if o and not o.trailing_active:
            o.trailing_active = True; o.trail_dist = dist; o.tp_active=False
            self._log({"t":"trail_on","cid":cid,"dist":dist})

    def sim_step(self, cid:str, high:float, low:float, atr_pips:float, pip:float):
        o = self._state["orders"].get(cid)
        if not o or o.status != "OPEN": return None
        # trailing move?
        if o.trailing_active and o.trail_dist is not None:
            if o.side=="buy":
                new_sl = max(o.sl, high - o.trail_dist)
                if new_sl > o.sl + 1e-9: o.sl = new_sl; self._log({"t":"trail_adj","cid":cid,"sl":o.sl})
            else:
                new_sl = min(o.sl, low + o.trail_dist)
                if new_sl < o.sl - 1e-9: o.sl = new_sl; self._log({"t":"trail_adj","cid":cid,"sl":o.sl})
        # hit exits?
        hit_tp = (o.tp is not None) and ((high>=o.tp) if o.side=="buy" else (low<=o.tp))
        hit_sl = (low<=o.sl) if o.side=="buy" else (high>=o.sl)
        hit = None
        if hit_tp and hit_sl:
            hit = ("SL", o.sl)  # conservative
        elif hit_tp:
            hit = ("TP", o.tp)
        elif hit_sl:
            hit = ("SL", o.sl)
        if hit:
            label, px = hit
            o.status="CLOSED"; o.closed_ms=now_ms()
            self._state["positions"][o.symbol] = 0
            self._log({"t":"close","cid":cid,"how":label,"px":px})
            return {"cid":cid,"closed":True,"how":label,"px":px}
        return None
