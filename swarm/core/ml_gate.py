import os, pickle
from typing import Dict, Tuple
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
FOREX_MODEL = os.getenv("FOREX_MODEL", os.path.join(MODEL_DIR, "forex_latest.pkl"))

_model=None
def _load():
    global _model
    if _model is None:
        with open(FOREX_MODEL, "rb") as f:
            _model = pickle.load(f)
    return _model

def predict_proba(features:Dict)->Tuple[float,float]:
    """
    Returns (p_long, p_short) from your sklearn-like model.
    Features dict -> 1xN vector via stable key order.
    """
    m = _load()
    keys = sorted(features.keys())
    x = [[features[k] for k in keys]]
    try:
        proba = m.predict_proba(x)[0]
        # assume class order [long, short] if labeled as such; fallback evenly
        if len(proba)==2: return (float(proba[0]), float(proba[1]))
    except Exception:
        pass
    # fallback neutral
    return (0.5, 0.5)
