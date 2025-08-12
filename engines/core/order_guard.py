import os
from engines.core.oco_policy import EnvPolicy, OcoInputs

def compute_oco_or_die(order_ctx: dict) -> tuple[float,float]:
    """
    order_ctx:
      {
        "entry": float,
        "side": "buy"|"sell",
        "pip": float,
        "atr": float,
        "ml_edge": float,
        "equity_usd": float,
        "tick_value_usd": float
      }
    """
    policy = EnvPolicy()
    if not policy.strict_oco:
        raise RuntimeError("STRICT_OCO must be true; refusing to place non-OCO order.")

    side_sign = +1 if order_ctx["side"].lower() in {"buy","long"} else -1
    oi = OcoInputs(
        entry=float(order_ctx["entry"]),
        side_sign=side_sign,
        pip=float(order_ctx["pip"]),
        atr=float(order_ctx["atr"]),
        ml_edge=float(order_ctx.get("ml_edge", 0.0)),
        equity_usd=float(order_ctx["equity_usd"]),
        tick_value_usd=float(order_ctx["tick_value_usd"]),
    )
    return policy.compute(oi)
