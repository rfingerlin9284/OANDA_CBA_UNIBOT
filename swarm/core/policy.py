from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class RiskPolicy:
    max_risk_pct: float = 0.5   # % per idea (tiny by default)
    min_sl_pips: float = 10.0   # absolute floor on SL distance
    atr_sl_mult: float = 0.8    # SL = max(min_sl_pips, ATR*mult)
    tp_rr: float = 1.2          # TP = RR * SL
    allow_tp_remove: bool = True
    sl_immutable: bool = True   # SL can *never* be removed

def oco_from_atr(entry:float, side:str, atr_pips:float, pol:RiskPolicy)->Tuple[float,float]:
    """Return (tp, sl) prices given entry, side, ATR in pips."""
    sl_pips = max(pol.min_sl_pips, atr_pips*pol.atr_sl_mult)
    tp_pips = sl_pips*pol.tp_rr
    if side.lower()=="long":
        sl = entry - sl_pips/10000.0
        tp = entry + tp_pips/10000.0
    else:
        sl = entry + sl_pips/10000.0
        tp = entry - tp_pips/10000.0
    return (tp, sl)
