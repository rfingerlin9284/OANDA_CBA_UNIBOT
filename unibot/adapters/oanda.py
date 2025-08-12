import os, requests, json
from typing import Dict, Any
from .base import Broker

API   = os.getenv("OANDA_API_BASE",   "https://api-fxpractice.oanda.com")
STREAM= os.getenv("OANDA_STREAM_URL", "https://stream-fxpractice.oanda.com")
ACCT  = os.getenv("OANDA_ACCOUNT_ID", "")
KEY   = os.getenv("OANDA_API_KEY",    "")

def _hdr():
    if not KEY: raise RuntimeError("OANDA_API_KEY not set")
    return {"Authorization": f"Bearer {KEY}", "Content-Type":"application/json"}

def _ins(symbol:str)->str:
    return symbol.replace("/","_").upper()

def _pretty(resp:requests.Response)->str:
    try: return json.dumps(resp.json(), indent=2)
    except Exception: return f"HTTP {resp.status_code} {resp.text[:400]}"

class Oanda(Broker):
    def price(self, symbol:str)->float:
        ins = _ins(symbol)
        r = requests.get(f"{API}/v3/instruments/{ins}/candles?count=1&price=M", headers=_hdr(), timeout=10)
        if not r.ok: raise RuntimeError(f"price() failed: {_pretty(r)}")
        return float(r.json()["candles"][0]["mid"]["c"])

    def place_order_oco(self, symbol, side, units, entry, tp, sl, client_id, extras=None)->Dict[str,Any]:
        ins = _ins(symbol)
        if side not in ("buy","sell"): raise ValueError("side must be 'buy' or 'sell'")
        body = {
          "order": {
            "type":"MARKET",
            "instrument": ins,
            "units": str(units if side=="buy" else -abs(units)),
            "clientExtensions":{"id": client_id},
            "takeProfitOnFill":{"price": f"{tp:.5f}"},
            "stopLossOnFill"  :{"price": f"{sl:.5f}"}
          }
        }
        r = requests.post(f"{API}/v3/accounts/{ACCT}/orders", json=body, headers=_hdr(), timeout=20)
        if not r.ok: raise RuntimeError(f"place_order_oco() failed: {_pretty(r)}")
        return r.json()

    def cancel(self, broker_order_id:str)->None:
        r = requests.put(f"{API}/v3/accounts/{ACCT}/orders/{broker_order_id}/cancel", headers=_hdr(), timeout=10)
        if not r.ok: raise RuntimeError(f"cancel() failed: {_pretty(r)}")

    def open_position(self, symbol:str)->Dict[str,Any]:
        ins = _ins(symbol)
        r = requests.get(f"{API}/v3/accounts/{ACCT}/openPositions", headers=_hdr(), timeout=10)
        if not r.ok: raise RuntimeError(f"open_position() failed: {_pretty(r)}")
        for p in r.json().get("positions",[]):
            if p.get("instrument")==ins: return p
        return {}

    def consolidate(self, symbol:str)->Dict[str,Any]:
        return {"status":"todo"}
