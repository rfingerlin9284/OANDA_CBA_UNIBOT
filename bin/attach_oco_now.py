#!/usr/bin/env python3
import sys, time
from utils.line_renderer import render_trade_line

def main():
    try:
        # Expect your app to expose a local broker adapter
        from app_broker import broker  # <-- provide a thin wrapper to your live router
    except Exception as e:
        print("attach_oco_now: unable to import app_broker.broker adapter:", e)
        sys.exit(1)

    opens = broker.list_open("EUR/USD")
    for t in opens:
        # if no OCO, attach a conservative one NOW
        if not t.get("sl") or not t.get("tp"):
            side=t["side"]; px=broker.price("EUR/USD")
            sl = px - 0.0010 if side=="long" else px + 0.0010
            tp = None if t.get("tp_removed") else (px + 0.0012 if side=="long" else px - 0.0012)
            broker.ensure_oco(t["ticket"], tp, sl)
            print(render_trade_line({
                "status":"open","ticket":t["ticket"],"symbol":"EUR/USD","side":side,"units":t.get("units",0),
                "avg":t.get("avg",px),"current":px,"pl_pips":t.get("pl_pips",0.0),
                "oco":{"tp":tp or 0.0,"sl":sl,"trailing":False,"tp_removed":tp is None}
            }))
    print("attach_oco_now: done.")

if __name__=="__main__": main()
