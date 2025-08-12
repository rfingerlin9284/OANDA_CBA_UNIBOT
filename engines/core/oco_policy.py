import os, math, time, json
from dataclasses import dataclass

def _as_bool(v): return str(v).lower() in {"1","true","yes","on"}

@dataclass
class OcoInputs:
    entry: float
    side_sign: int          # +1 long, -1 short
    pip: float
    atr: float
    ml_edge: float
    equity_usd: float
    tick_value_usd: float

class EnvPolicy:
    """Loads all policy knobs from .env.common and broker .env (already exported)."""

    def __init__(self):
        # Hard fail flag
        self.strict_oco = _as_bool(os.getenv("STRICT_OCO", "true"))

        # Risk
        self.risk_pct = float(os.getenv("RISK_PCT_PER_TRADE", "0.005"))
        self.max_sl_pips = float(os.getenv("MAX_SL_PIPS", "30"))
        self.min_sl_pips = float(os.getenv("MIN_SL_PIPS", "5"))

        # Volatility + ML
        self.atr_tp_mult = float(os.getenv("ATR_TP_MULT", "2.2"))
        self.atr_sl_mult = float(os.getenv("ATR_SL_MULT", "1.2"))
        self.ml_w_tp = float(os.getenv("ML_EDGE_WEIGHT_TP", "0.6"))
        self.ml_w_sl = float(os.getenv("ML_EDGE_WEIGHT_SL", "0.4"))
        self.fixed_tp_pips = float(os.getenv("FIXED_TP_PIPS", "0"))
        self.fixed_sl_pips = float(os.getenv("FIXED_SL_PIPS", "0"))

        # Expressions (strings)
        self.tp_expr = os.getenv("OCO_TP_EXPR")
        self.sl_expr = os.getenv("OCO_SL_EXPR")
        if not self.tp_expr or not self.sl_expr:
            raise RuntimeError("OCO formulas missing in .env.common (OCO_TP_EXPR / OCO_SL_EXPR).")

    def _safe_eval(self, expr: str, scope: dict) -> float:
        # extremely small expression sandbox: allow only operators and min/max
        allowed_names = {"min":min, "max":max, "abs":abs}
        return eval(expr, {"__builtins__":{}}, {**allowed_names, **scope})

    def compute(self, inp: OcoInputs) -> tuple[float,float]:
        pip = max(inp.pip, 1e-10)
        atr = max(inp.atr, pip)
        ml_edge = float(inp.ml_edge)

        # risk -> pips cap
        tick_val = max(inp.tick_value_usd, 1e-9)
        equity = max(inp.equity_usd, 0.0)
        risk_pips_cap = (self.risk_pct * equity / tick_val)  # pip-size applied in expr

        scope = dict(
            entry=inp.entry,
            side_sign=int(inp.side_sign),
            pip=pip,
            atr=atr,
            ml_edge=ml_edge,
            ATR_TP_MULT=self.atr_tp_mult,
            ATR_SL_MULT=self.atr_sl_mult,
            MAX_SL_PIPS=self.max_sl_pips,
            MIN_SL_PIPS=self.min_sl_pips,
            FIXED_TP_PIPS=self.fixed_tp_pips,
            FIXED_SL_PIPS=self.fixed_sl_pips,
            risk_pips_cap=risk_pips_cap
        )

        tp = float(self._safe_eval(self.tp_expr, scope))
        sl = float(self._safe_eval(self.sl_expr, scope))

        # guardrails
        if inp.side_sign == +1 and not (sl < inp.entry < tp):
            raise RuntimeError(f"Long OCO invalid (sl={sl} entry={inp.entry} tp={tp})")
        if inp.side_sign == -1 and not (tp < inp.entry < sl):
            raise RuntimeError(f"Short OCO invalid (tp={tp} entry={inp.entry} sl={sl})")

        return tp, sl
