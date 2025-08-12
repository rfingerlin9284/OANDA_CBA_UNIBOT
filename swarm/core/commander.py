from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional
from .policy import RiskPolicy, oco_from_atr
from .fvg import fvg_weight, atr_pips
from .ml_gate import predict_proba

@dataclass
class SwarmConfig:
    min_spacing_pips: float = 0.25  # fraction of ATR used later
    max_adds: int = 4
    ml_thresh_open: float = 0.58
    ml_thresh_add: float = 0.60
    weight_mix: float = 0.5 # blend ML prob with FVG weight
    units_base: int = 1000

class BrokerIF:
    """Adapter your router must satisfy."""
    def price(self, symbol:str)->float: ...
    def place_market_with_oco(self, symbol:str, side:str, units:int, tp:float, sl:float, tags:Dict[str,str])->str: ...
    def list_open(self, symbol:str)->List[Dict[str,Any]]: ...
    def ensure_oco(self, ticket:str, tp:Optional[float], sl:float)->None: ...
    def trailing_sl(self, ticket:str, new_sl:float)->None: ...

class SwarmCommander:
    def __init__(self, broker:BrokerIF, risk:RiskPolicy=RiskPolicy(), cfg:SwarmConfig=SwarmConfig()):
        self.broker=broker; self.risk=risk; self.cfg=cfg

    def _score(self, side:str, fvg_dir:str, fvg_w:float, feats:Dict)->float:
        p_long, p_short = predict_proba(feats)
        p = p_long if side=="long" else p_short
        # boost if FVG agrees; dampen if opposes
        if (side=="long" and fvg_dir=="bull") or (side=="short" and fvg_dir=="bear"):
            p = self.cfg.weight_mix*p + (1-self.cfg.weight_mix)*max(0.5, fvg_w)
        elif fvg_dir!="none":
            p = self.cfg.weight_mix*p + (1-self.cfg.weight_mix)*min(0.5, 1-fvg_w)
        return p

    def evaluate_and_trade(self, symbol:str, side:str, candles:List[Tuple[float,float,float,float]], equity_usd:float, existing_adds:int=0)->Dict:
        """Gate + OCO calc + optional fire. Returns dict with decision + oco if fired."""
        # Build simple features (extend with your set)
        atr = atr_pips(candles)
        fdir,fwt = fvg_weight(candles)
        feats = {"atr":atr, "fvg_bear":1.0 if fdir=="bear" else 0.0, "fvg_bull":1.0 if fdir=="bull" else 0.0}
        score = self._score(side, fdir, fwt, feats)

        thresh = self.cfg.ml_thresh_open if existing_adds==0 else self.cfg.ml_thresh_add
        decision = {"score":score, "threshold":thresh, "allowed": score>=thresh, "atr_pips":atr, "fvg_dir":fdir, "fvg_weight":fwt}
        if not decision["allowed"]:
            decision["status"]="blocked"
            return decision

        # Position sizing: tiny risk; assume 10-pip pipValue ≈ $1 per 10k
        units = self.cfg.units_base
        entry = self.broker.price(symbol)
        tp, sl = oco_from_atr(entry, side, atr, self.risk)

        # FIRE with OCO; SL immutable enforced by broker.ensure_oco/watchdog
        ticket = self.broker.place_market_with_oco(symbol, side, units, tp, sl, {"type":"swarm","sl_immutable":str(self.risk.sl_immutable)})
        decision.update({"status":"fired","ticket":ticket,"entry":entry,"tp":tp,"sl":sl,"units":units})
        return decision
